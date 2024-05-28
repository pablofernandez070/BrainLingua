# aplicacion.py
import tkinter as tk
from tkinter import ttk
from text_analysis import TextAnalyzer
from menu import MenuBar
from importar import leer_pdf, leer_txt, leer_docx

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("BrainLingua")
        
        # Establecer el tamaño de la ventana
        self.root.geometry("1000x650")  
        
        # Inicializar la barra de menú
        self.menu_bar = MenuBar(root)

        # Estilo para el Treeview
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", background="#f0f0f0", foreground="black", rowheight=25, fieldbackground="#f0f0f0")

        # Estilo para los botones
        self.style.configure("TButton", background="#4caf60", foreground="white", padding=10)

        # Cuadro de texto con dimensiones específicas
        self.text_box = tk.Text(root, width=80, height=10)
        self.text_box.pack(pady=5)

        # Frame para los botones
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=5)

        # Botón que almacena el texto del cuadro de texto en una variable
        self.boton01 = ttk.Button(self.button_frame, text="Analyze", command=self.store_and_display_analysis)
        self.boton01.grid(row=0, column=0, padx=5)

        # Botón para limpiar el cuadro de texto
        self.boton_limpiar = ttk.Button(self.button_frame, text="Limpiar", command=self.clear_text_box)
        self.boton_limpiar.grid(row=0, column=1, padx=5)

        # Botón para importar texto desde un archivo PDF
        self.boton_pdf = ttk.Button(self.button_frame, text="Importar PDF", command=lambda: leer_pdf(self.text_box))
        self.boton_pdf.grid(row=0, column=2, padx=5)

        # Botón para importar texto desde un archivo TXT
        self.boton_txt = ttk.Button(self.button_frame, text="Importar TXT", command=lambda: leer_txt(self.text_box))
        self.boton_txt.grid(row=0, column=3, padx=5)

        # Botón para importar texto desde un archivo DOCX
        self.boton_docx = ttk.Button(self.button_frame, text="Importar DOCX", command=lambda: leer_docx(self.text_box))
        self.boton_docx.grid(row=0, column=4, padx=5)

        # Botón para análisis avanzado
        self.boton_analisis_avanzado = ttk.Button(self.button_frame, text="Análisis avanzado", command=self.abrir_analisis_avanzado)
        self.boton_analisis_avanzado.grid(row=0, column=5, padx=5)

        # Variable para almacenar el texto del cuadro de texto
        self.stored_text = ""

        # Objeto TextAnalyzer para analizar el texto
        self.analyzer = TextAnalyzer()

        # Configurar el Treeview para mostrar los resultados en una tabla
        self.tree = ttk.Treeview(root, show="headings")
        self.tree.pack(fill=tk.BOTH, expand=True)

    def store_and_display_analysis(self):
        # Limpiar la tabla antes de insertar nuevos datos
        self.tree.delete(*self.tree.get_children())
        
        # Obtener el texto del cuadro de texto
        self.stored_text = self.text_box.get("1.0", tk.END).strip()
        if not self.stored_text:
            return

        print(f"Texto almacenado: {self.stored_text}")

        # Analizar el texto utilizando TextAnalyzer
        pos_counts, total_words = self.analyzer.analyze_text(self.stored_text)

        # Configurar las columnas del Treeview basado en las categorías POS
        self.tree["columns"] = list(pos_counts.keys()) + ["Total Words"]
        for pos in pos_counts.keys():
            self.tree.heading(pos, text=pos)
            self.tree.column(pos, anchor=tk.CENTER, width=100)
        
        self.tree.heading("Total Words", text="Total Words")
        self.tree.column("Total Words", anchor=tk.CENTER, width=100)

        # Insertar los resultados del análisis en la tabla
        self.tree.insert("", "end", values=[pos_counts[pos] for pos in pos_counts.keys()] + [total_words])

    def clear_text_box(self):
        # Limpiar el contenido del cuadro de texto
        self.text_box.delete("1.0", tk.END)

    def abrir_analisis_avanzado(self):
        # Crear una nueva ventana para el análisis avanzado
        self.advanced_window = tk.Toplevel(self.root)
        self.advanced_window.title("Análisis Avanzado")

        # Etiqueta y entrada de texto para la palabra a buscar
        self.label_palabra = ttk.Label(self.advanced_window, text="Buscar palabra:")
        self.label_palabra.pack(pady=5)

        self.entry_palabra = ttk.Entry(self.advanced_window, width=30)
        self.entry_palabra.pack(pady=5)

        # Botón para iniciar la búsqueda
        self.boton_buscar = ttk.Button(self.advanced_window, text="Buscar", command=self.buscar_palabra)
        self.boton_buscar.pack(pady=5)

    def buscar_palabra(self):
        # Obtener la palabra a buscar
        palabra = self.entry_palabra.get().strip()
        if not palabra:
            return

        # Contar las ocurrencias de la palabra en el texto almacenado
        count = self.stored_text.lower().split().count(palabra.lower())

        # Mostrar el resultado en una etiqueta
        self.resultado_label = ttk.Label(self.advanced_window, text=f"La palabra '{palabra}' aparece {count} veces.")
        self.resultado_label.pack(pady=5)

def main():
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()

if __name__ == "__main__":
    main()
