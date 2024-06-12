import tkinter as tk
from tkinter import ttk, PhotoImage, filedialog, messagebox
from PIL import Image, ImageTk
import openpyxl
import matplotlib.pyplot as plt

from text_analysis import TextAnalyzer
from menu import MenuBar
from importar import leer_pdf, leer_txt, leer_docx
from analisis_avanzado import abrir_analisis_avanzado
from chart_converter import convertir_a_grafica
from audio import transcribe_audio
from excel_exporter import exportar_a_excel

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("BrainLingua NLP")
        self.root.state('zoomed')  
        self.root.configure(bg="#2e2e2e")
        
        self.analisis_realizado = False
        
        self.menu_bar = MenuBar(root)
        self._setup_styles()
        self._setup_widgets()

        self.analyzer = TextAnalyzer()
        self.stored_text = ""

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", 
                        background="#2e2e2e",
                        foreground="white", 
                        fieldbackground="#2e2e2e",
                        rowheight=25)
        style.configure("Treeview.Heading",
                        background="#404040",
                        foreground="white")
        style.configure("TButton", 
                        background="#207567",  
                        foreground="white", 
                        padding=10)
        style.map("TButton", 
                background=[('active', '#1a5c52'), ('pressed', '#207567')])
        style.configure("TLabel",
                        background="#2e2e2e",
                        foreground="white")
        style.configure("TEntry",
                        background="#2e2e2e",
                        foreground="white",
                        fieldbackground="#2e2e2e")

    def _setup_widgets(self):
        # Agregar logotipo y texto de bienvenida
        self._add_logo()
        self._add_welcome_text()

        # Crear frame principal
        self.main_frame = tk.Frame(self.root, bg="#2e2e2e")
        self.main_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Crear frame izquierdo para los botones
        self.left_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Crear frame derecho para el cuadro de texto y la tabla de resultados
        self.right_frame = tk.Frame(self.main_frame, bg="#2e2e2e")
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # Agregar botones, cuadro de texto y tabla de resultados
        self._add_buttons(self.left_frame)
        self._add_text_box(self.right_frame)
        self._setup_treeview(self.right_frame)

        # Configurar pesos para las columnas y filas del grid
        self.main_frame.grid_columnconfigure(0, weight=1, minsize=200)
        self.main_frame.grid_columnconfigure(1, weight=4)
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

    def _add_logo(self):
        logo_image = Image.open("env/BrainLingua/src/img/prueba_logo.png").resize((40, 40))
        logo_photo = ImageTk.PhotoImage(logo_image)
        tk.Label(self.root, image=logo_photo, bg="#2e2e2e").grid(row=0, column=0, pady=(5, 0), padx=5, sticky="w")
        self.root.image = logo_photo  # Prevent garbage collection

    def _add_welcome_text(self):
        welcome_text = (
            "¡Bienvenido a BrainLingua!\n"
            "Este programa realiza análisis de texto y ofrece diversas funcionalidades "
            "para trabajar con documentos de texto."
        )
        tk.Label(self.root, text=welcome_text, justify="left", bg="#2e2e2e", fg="white", font=("Helvetica", 12)).grid(
            row=0, column=1, columnspan=3, pady=(5, 0), padx=10, sticky="w"
        )

    def _add_text_box(self, parent_frame):
        text_frame = tk.Frame(parent_frame, bg="#2e2e2e")
        text_frame.grid(row=0, column=0, sticky="nsew")

        self.text_box = tk.Text(text_frame, width=80, height=15, borderwidth=2, relief="solid", bg='white', fg='black', insertbackground='black', highlightthickness=2, highlightbackground='#207567')
        self.text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Placeholder functionality
        self.placeholder_text = "Inserte el texto a analizar..."
        self.text_box.insert("1.0", self.placeholder_text)
        self.text_box.bind("<FocusIn>", self._clear_placeholder)
        self.text_box.bind("<FocusOut>", self._add_placeholder)

        # Agregar botón para borrar el texto
        imagen_boton_delete = PhotoImage(file="env/BrainLingua/src/img/Delete.png").subsample(8, 8)
        ttk.Button(text_frame, image=imagen_boton_delete, command=self.clear_text_box).pack(side=tk.RIGHT, padx=5, pady=5)
        self.root.image_delete = imagen_boton_delete

        # Agregar botón para realizar el análisis
        img_analysis = PhotoImage(file="env/BrainLingua/src/img/EJECUTAR.png").subsample(15, 15)
        ttk.Button(text_frame, image=img_analysis, text='Ejecutar', compound=tk.LEFT, command=self.store_and_display_analysis).pack(side=tk.RIGHT, padx=5, pady=5)
        self.root.image_analysis = img_analysis

        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)

    def _clear_placeholder(self, event):
        if self.text_box.get("1.0", tk.END).strip() == self.placeholder_text:
            self.text_box.delete("1.0", tk.END)
            self.text_box.config(fg='black')

    def _add_placeholder(self, event):
        if not self.text_box.get("1.0", tk.END).strip():
            self.text_box.insert("1.0", self.placeholder_text)
            self.text_box.config(fg='grey')

    def _add_buttons(self, parent_frame):
        button_options = {"width": 40}

        # Cargar las imágenes para los botones
        img_import_pdf = PhotoImage(file="env/BrainLingua/src/img/PDF.png").subsample(10, 10)
        img_import_txt = PhotoImage(file="env/BrainLingua/src/img/TXT.png").subsample(10, 10)
        img_import_docx = PhotoImage(file="env/BrainLingua/src/img/DOCX.png").subsample(10, 10)
        img_advanced_analysis = PhotoImage(file="env/BrainLingua/src/img/ANALISIS_AVANZADO.png").subsample(15, 15)
        img_transcribe_audio = PhotoImage(file="env/BrainLingua/src/img/MP3.png").subsample(10, 10)
        img_convert_graph = PhotoImage(file="env/BrainLingua/src/img/GRAFICA.png").subsample(10, 10)

        # Almacenar las imágenes para evitar que se recojan como basura
        self.root.images = {
            "import_pdf": img_import_pdf,
            "import_txt": img_import_txt,
            "import_docx": img_import_docx,
            "advanced_analysis": img_advanced_analysis,
            "transcribe_audio": img_transcribe_audio,
            "convert_graph": img_convert_graph
        }

        # Definir los botones y sus comandos
        buttons = [
            ("Importar PDF", lambda: leer_pdf(self.text_box), img_import_pdf),
            ("Importar TXT", lambda: leer_txt(self.text_box), img_import_txt),
            ("Importar DOCX", lambda: leer_docx(self.text_box), img_import_docx),
            ("Análisis avanzado", lambda: abrir_analisis_avanzado(self.root, self.text_box.get("1.0", tk.END)), img_advanced_analysis),
            ("Importar Audio", self.transcribe_audio_from_button, img_transcribe_audio),
            ("Convertir a gráfica", lambda: convertir_a_grafica(self), img_convert_graph)
        ]

        # Agregar los botones al frame
        for i, (text, command, image) in enumerate(buttons):
            ttk.Button(parent_frame, text=text, command=command, image=image, compound=tk.LEFT, **button_options).pack(pady=5)

    def _setup_treeview(self, parent_frame):
        # Crear el Treeview para mostrar los resultados del análisis
        self.tree = ttk.Treeview(parent_frame, show="headings")
        self.tree.grid(row=1, column=0, sticky="nsew")  # Treeview en la fila 1
        parent_frame.grid_rowconfigure(1, weight=1)
        parent_frame.grid_columnconfigure(0, weight=1)

        # Ajustar las columnas para que se autoescale al contenido
        self.tree.column("#0", stretch=tk.YES)
        for col in self.tree["columns"]:
            self.tree.column(col, stretch=tk.YES)

        # Crear un frame para el botón debajo del Treeview
        button_frame = tk.Frame(parent_frame, bg="#2e2e2e")
        button_frame.grid(row=2, column=0, sticky="ew")  # Botón en la fila 2

        # BOTON SAVE
        img_save = PhotoImage(file="env/BrainLingua/src/img/SAVE.png").subsample(15, 15)
        ttk.Button(button_frame, image=img_save, text='Guardar', compound=tk.LEFT, command=lambda: exportar_a_excel(self.tree, self.analisis_realizado)).pack(side=tk.RIGHT, padx=5, pady=5)
        self.root.img_export_excel = img_save

        parent_frame.grid_rowconfigure(2, weight=0)
        parent_frame.grid_columnconfigure(0, weight=1)

    def store_and_display_analysis(self):
        # Limpiar resultados anteriores
        self.tree.delete(*self.tree.get_children())
        self.stored_text = self.text_box.get("1.0", tk.END).strip()
        if not self.stored_text:
            return
        self.analisis_realizado = True

        # Analizar el texto y obtener las estadísticas
        analysis_results = self.analyzer.analyze_text(self.stored_text)

        # Definir las columnas de la tabla si hay resultados
        if analysis_results:
            columns = list(analysis_results[0].keys())
            self.tree["columns"] = columns

            # Configurar las cabeceras de las columnas
            for col in columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, anchor=tk.CENTER)

            # Insertar los valores en la tabla
            for result in analysis_results:
                values = [result[col] for col in columns]
                self.tree.insert("", "end", values=values)

            # Ajustar las columnas para que se autoescalen al contenido
            for col in self.tree["columns"]:
                self.tree.column(col, stretch=tk.YES)

    def clear_text_box(self):
        # Limpiar el cuadro de texto
        self.text_box.delete("1.0", tk.END)

    def transcribe_audio_from_button(self):
        # Transcribir audio desde un archivo
        audio_file_path = filedialog.askopenfilename(filetypes=[("Archivos de audio MP3", "*.mp3")])
        if audio_file_path:
            transcription = transcribe_audio(audio_file_path)
            # print("Texto transcrito:", transcription)  # Esta línea se ha comentado para evitar la impresión
        else:
            print("No se seleccionó ningún archivo MP3.")

def main():
    # Iniciar la aplicación
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()

if __name__ == "__main__":
    main()
