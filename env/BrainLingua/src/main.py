# aplicacion.py
import tkinter as tk
import csv
import openpyxl
import matplotlib.pyplot as plt
import re
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk 
from text_analysis import TextAnalyzer
from menu import MenuBar
from importar import leer_pdf, leer_txt, leer_docx
from SpellCheckManager import SpellCheckManager

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("BrainLingua")
        self.Spell_check_manager = SpellCheckManager(language='es')
        self.analisis_realizado = False
        
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

        # Registrar el evento FocusOut para el cuadro de texto
        self.text_box.bind("<FocusOut>", self.resaltar_errores_ortograficos)

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

        #Boton para exportar a EXCEL
        self.boton_exportar_excel = ttk.Button(self.button_frame, text="Exportar a Excel", command=self.exportar_a_excel)
        self.boton_exportar_excel.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        # En el método __init__ de la clase Aplicacion
        self.boton_grafica = ttk.Button(self.button_frame, text="Convertir a gráfica", command=self.convertir_a_grafica)
        self.boton_grafica.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

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

        self.analisis_realizado = True

        # Analizar el texto utilizando TextAnalyzer
        pos_counts, total_words, num_sentences = self.analyzer.analyze_text(self.stored_text)
        avg_words_per_sentence = self.analyzer.average_words_per_sentence(self.stored_text)

        # Configurar las columnas del Treeview basado en las categorías POS
        self.tree["columns"] = list(pos_counts.keys()) + ["Total Words"] + ["N Sentences"] + ["Avg Words/Sentence"]
        for pos in pos_counts.keys():
            self.tree.heading(pos, text=pos)
            self.tree.column(pos, anchor=tk.CENTER, width=100)
        
        self.tree.heading("Total Words", text="Total Words")
        self.tree.column("Total Words", anchor=tk.CENTER, width=100)

        self.tree.heading("N Sentences", text="N Sentences")
        self.tree.column("N Sentences", anchor=tk.CENTER, width=100)

        self.tree.heading("Avg Words/Sentence", text="Avg Words/Sentence")
        self.tree.column("Avg Words/Sentence", anchor=tk.CENTER, width=150)

        # Insertar los resultados del análisis en la tabla
        self.tree.insert("", "end", values=[pos_counts[pos] for pos in pos_counts.keys()] + [total_words] + [num_sentences] + [avg_words_per_sentence])

    def clear_text_box(self):
        # Limpiar el contenido del cuadro de texto
        self.text_box.delete("1.0", tk.END)
    
    

    def abrir_analisis_avanzado(self):
        # Comprobar si se ha realizado un análisis
        if not self.analisis_realizado:  
            messagebox.showwarning("Error", "Por favor, ejecute un análisis antes de realizar un analisis avanzado.")
            return

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

    def exportar_a_excel(self):
        # Comprobar si se ha realizado un análisis
        if not self.analisis_realizado:  
            messagebox.showwarning("Exportar a Excel", "Por favor, realice un análisis antes de exportar los datos.")
            return
        
        # Obtener todas las filas del Treeview
        filas = self.tree.get_children()

        # Obtener las columnas del Treeview
        columnas = self.tree["columns"]

        # Abrir un cuadro de diálogo para seleccionar la ubicación del archivo Excel
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx")])
        
        if file_path:
            # Crear un nuevo libro de trabajo de Excel
            workbook = openpyxl.Workbook()
            sheet = workbook.active

            # Escribir los encabezados de las columnas
            for idx, columna in enumerate(columnas, start=1):
                sheet.cell(row=1, column=idx, value=columna)

            # Escribir los datos de cada fila
            for idx, fila in enumerate(filas, start=2):
                # Obtener los valores de la fila
                valores_fila = [self.tree.set(fila, columna) for columna in columnas]
                
                # Escribir los valores en el archivo Excel
                for col, valor in enumerate(valores_fila, start=1):
                    sheet.cell(row=idx, column=col, value=valor)

            # Guardar el archivo Excel
            workbook.save(file_path)

            messagebox.showinfo("Exportar a Excel", "Los datos han sido exportados correctamente.")
    
    def convertir_a_grafica(self):
        if not self.analisis_realizado:
            messagebox.showerror("Error", "Realice un análisis primero.")
            return
        
        # Obtener los datos para el gráfico
        pos_counts, total_words, num_sentences = self.analyzer.analyze_text(self.stored_text)
        categorias = list(pos_counts.keys())
        valores = list(pos_counts.values())

        # Añadir los datos de total_words y num_sentences a las listas
        categorias.append("Total Words")
        categorias.append("Num Sentences")
        valores.append(total_words)
        valores.append(num_sentences)

        # Calcular la media de palabras por oración
        if num_sentences != 0:
            media_palabras_por_oracion = total_words / num_sentences
            categorias.append("Media Palabras por Oración")
            valores.append(media_palabras_por_oracion)

        # Crear el gráfico de barras
        plt.figure(figsize=(10, 8))
        plt.bar(categorias, valores, color='skyblue')
        plt.xlabel('Categorías y Métricas')
        plt.ylabel('Frecuencia o Valor')
        plt.title('Frecuencia de categorías gramaticales y métricas adicionales')
        plt.xticks(rotation=45, ha='right')  # Rotar etiquetas del eje x para mayor claridad

        # Mostrar el gráfico en una nueva ventana
        plt.tight_layout()  # Ajustar el diseño del gráfico para evitar superposiciones
        plt.show()
    
    def resaltar_errores_ortograficos(self, event):
        self.text_box.tag_remove("highlight", "1.0", tk.END)  # Remove any previous highlights

        texto_actual = self.text_box.get("1.0", tk.END).strip()
        palabras_incorrectas = self.Spell_check_manager.obtener_palabras_incorrectas(texto_actual)

        for palabra in palabras_incorrectas:
            start_index = "1.0"
            while True:
                start_index = self.text_box.search(palabra, start_index, tk.END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(palabra)}c"
                self.text_box.tag_add("highlight", start_index, end_index)
                start_index = end_index

        self.text_box.tag_config("highlight", foreground="red")


def main():
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()

if __name__ == "__main__":
    main()
