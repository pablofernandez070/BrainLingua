# aplicacion.py
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from PIL import Image, ImageTk 
from text_analysis import TextAnalyzer
from menu import MenuBar
from importar import leer_pdf, leer_txt, leer_docx

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("BrainLingua")
        
        # Establecer el tamaño de la ventana
        self.root.geometry("1000x800")
        self.root.configure(bg="white")
        
        # Inicializar la barra de menú
        self.menu_bar = MenuBar(root)

        # Estilo para el Treeview
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Treeview", foreground="black", rowheight=25)

        # Estilo para los botones
        self.style.configure("TButton", background="#537AF5", foreground="white", padding=10)
        self.style.map("TButton", background=[('active', '#537AF5'), ('pressed', '#537AF5')])

        # Imagen logotipo
        # Cargar la imagen del logotipo
        self.logo_image = Image.open("env/BrainLingua/src/img/prueba_logo.png")  # Asegúrate de tener una imagen llamada "logo.png"
        self.logo_image = self.logo_image.resize((40, 40))  # Reducir el tamaño del logotipo
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)

        # Cargar la imagen para el botón desde el archivo
        self.imagen_boton_delete = PhotoImage(file="env/BrainLingua/src/img/Delete.png")
        self.imagen_boton_delete = self.imagen_boton_delete.subsample(8, 8)

        # Crear un Label para mostrar el logotipo
        self.logo_label = tk.Label(root, image=self.logo_photo)
        self.logo_label.grid(row=0, column=0, pady=(5, 0), padx=5, sticky="w")  # Alineado a la izquierda

        # Texto de bienvenida
        self.welcome_text = "¡Bienvenido a BrainLingua!\nEste programa realiza análisis de texto y ofrece diversas funcionalidades para trabajar con documentos de texto."
        self.welcome_label = tk.Label(root, text=self.welcome_text, justify="left", bg="white")
        self.welcome_label.grid(row=0, column=1, columnspan=2, pady=(5, 0), padx=10, sticky="w")  # Alineado a la izquierda y ocupando dos columnas


        # Cuadro de texto con dimensiones específicas
        self.text_box = tk.Text(root, width=80, height=10, borderwidth=2, relief="solid", bg='#EAE7E6')
        self.text_box.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        # Frame para los botones
        self.button_frame = tk.Frame(root, bg="white")
        self.button_frame.grid(row=1, column=2, padx=5, pady=5)

        # Botón analizar
        self.boton01 = ttk.Button(self.button_frame, text="Analyze", command=self.store_and_display_analysis)
        self.boton01.grid(row=0, column=0, padx=5, pady=5)

        # Botón para limpiar el cuadro de texto
        self.boton_limpiar = ttk.Button(self.button_frame, image=self.imagen_boton_delete, command=self.clear_text_box)
        self.boton_limpiar.grid(row=0, column=1, padx=5, pady=5)

        # Botón para importar texto desde un archivo PDF
        self.boton_pdf = ttk.Button(self.button_frame, text="Importar PDF", command=lambda: leer_pdf(self.text_box))
        self.boton_pdf.grid(row=1, column=0, padx=5, pady=5)

        # Botón para importar texto desde un archivo TXT
        self.boton_txt = ttk.Button(self.button_frame, text="Importar TXT", command=lambda: leer_txt(self.text_box))
        self.boton_txt.grid(row=1, column=1, padx=5, pady=5)

        # Botón para importar texto desde un archivo DOCX
        self.boton_docx = ttk.Button(self.button_frame, text="Importar DOCX", command=lambda: leer_docx(self.text_box))
        self.boton_docx.grid(row=2, column=0, padx=5, pady=5)

        # Botón para análisis avanzado
        self.boton_analisis_avanzado = ttk.Button(self.button_frame, text="Análisis avanzado", command=self.abrir_analisis_avanzado)
        self.boton_analisis_avanzado.grid(row=2, column=1, padx=5, pady=5)  # Este botón ocupa la segunda fila

        # Variable para almacenar el texto del cuadro de texto
        self.stored_text = ""

        # Objeto TextAnalyzer para analizar el texto
        self.analyzer = TextAnalyzer()

        # Configurar el Treeview para mostrar los resultados en una tabla
        self.tree = ttk.Treeview(root, show="headings")
        self.tree.grid(row=2, column=0, columnspan=3, sticky="nsew")

        # Asegurarse de que las columnas y filas se expandan cuando se redimensione la ventana
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

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
        # Crear una nueva ventana para el

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
