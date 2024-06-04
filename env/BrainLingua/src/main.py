import tkinter as tk
from tkinter import ttk, PhotoImage, filedialog, messagebox
from PIL import Image, ImageTk
import openpyxl
import matplotlib.pyplot as plt
from text_analysis import TextAnalyzer
from menu import MenuBar
from importar import leer_pdf, leer_txt, leer_docx
from SpellCheckManager import SpellCheckManager
from audio import transcribe_audio

class Aplicacion:
    def __init__(self, root):
        self.root = root
        self.root.title("BrainLingua NLP")
        self.root.state('zoomed')  # Para iniciar la aplicación en modo maximizado
        self.root.configure(bg="white")
        
        self.Spell_check_manager = SpellCheckManager(language='es')
        self.analisis_realizado = False
        
        self.menu_bar = MenuBar(root)
        self._setup_styles()
        self._setup_widgets()

        self.analyzer = TextAnalyzer()
        self.stored_text = ""

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", foreground="black", rowheight=25)
        style.configure("TButton", background="#537AF5", foreground="white", padding=10)
        style.map("TButton", background=[('active', '#537AF5'), ('pressed', '#537AF5')])

    def _setup_widgets(self):
        self._add_logo()
        self._add_welcome_text()

        # Crear frame principal
        self.main_frame = tk.Frame(self.root, bg="white")
        self.main_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Crear frame izquierdo para los botones
        self.left_frame = tk.Frame(self.main_frame, bg="white")
        self.left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Crear frame derecho para el cuadro de texto y la tabla de resultados
        self.right_frame = tk.Frame(self.main_frame, bg="white")
        self.right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

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
        tk.Label(self.root, image=logo_photo, bg="white").grid(row=0, column=0, pady=(5, 0), padx=5, sticky="w")
        self.root.image = logo_photo  # Prevent garbage collection

    def _add_welcome_text(self):
        welcome_text = (
            "¡Bienvenido a BrainLingua!\n"
            "Este programa realiza análisis de texto y ofrece diversas funcionalidades "
            "para trabajar con documentos de texto."
        )
        tk.Label(self.root, text=welcome_text, justify="left", bg="white", font=("Helvetica", 12)).grid(
            row=0, column=1, columnspan=3, pady=(5, 0), padx=10, sticky="w"
        )

    def _add_text_box(self, parent_frame):
        text_frame = tk.Frame(parent_frame, bg="white")
        text_frame.grid(row=0, column=0, sticky="nsew")

        self.text_box = tk.Text(text_frame, width=80, height=10, borderwidth=2, relief="solid", bg='#EAE7E6')
        self.text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text_box.bind("<FocusOut>", self.resaltar_errores_ortograficos)

        imagen_boton_delete = PhotoImage(file="env/BrainLingua/src/img/Delete.png").subsample(8, 8)
        ttk.Button(text_frame, image=imagen_boton_delete, command=self.clear_text_box).pack(side=tk.RIGHT, padx=5, pady=5)
        self.root.image_delete = imagen_boton_delete  # Prevent garbage collection

    def _add_buttons(self, parent_frame):
        button_options = {"width": 20}
        buttons = [
            ("Ejecutar Análisis", self.store_and_display_analysis),
            ("Importar PDF", lambda: leer_pdf(self.text_box)),
            ("Importar TXT", lambda: leer_txt(self.text_box)),
            ("Importar DOCX", lambda: leer_docx(self.text_box)),
            ("Análisis avanzado", self.abrir_analisis_avanzado),
            ("Exportar a Excel", self.exportar_a_excel),
            ("Transcribir Audio", self.transcribe_audio_from_button),
            ("Convertir a gráfica", self.convertir_a_grafica)
        ]

        for i, (text, command) in enumerate(buttons):
            ttk.Button(parent_frame, text=text, command=command, **button_options).pack(pady=5)

    def _setup_treeview(self, parent_frame):
        self.tree = ttk.Treeview(parent_frame, show="headings")
        self.tree.grid(row=1, column=0, sticky="nsew")
        parent_frame.grid_rowconfigure(1, weight=1)
        parent_frame.grid_columnconfigure(0, weight=1)

    def store_and_display_analysis(self):
        self.tree.delete(*self.tree.get_children())
        self.stored_text = self.text_box.get("1.0", tk.END).strip()
        if not self.stored_text:
            return
        self.analisis_realizado = True

        # Analizar el texto y obtener las estadísticas
        pos_counts, total_words, num_sentences = self.analyzer.analyze_text(self.stored_text)
        avg_words_per_sentence = self.analyzer.average_words_per_sentence(self.stored_text)
        count_palabras_malsonantes = self.analyzer.count_palabras_malsonantes(self.stored_text)  # Nuevo

        # Definir las columnas de la tabla
        columns = list(pos_counts.keys()) + ["Total Words", "N Sentences", "Avg Words/Sentence", "Palabras Malsonantes"]  # Modificado
        self.tree["columns"] = columns

        # Configurar las cabeceras de las columnas
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=100)

        # Insertar los valores en la tabla
        values = [pos_counts[pos] for pos in pos_counts.keys()] + [total_words, num_sentences, avg_words_per_sentence, count_palabras_malsonantes]  # Modificado
        self.tree.insert("", "end", values=values)

    def clear_text_box(self):
        self.text_box.delete("1.0", tk.END)

    def abrir_analisis_avanzado(self):
        if not self.analisis_realizado:
            messagebox.showwarning("Error", "Por favor, ejecute un análisis antes de realizar un análisis avanzado.")
            return

        advanced_window = tk.Toplevel(self.root)
        advanced_window.title("Análisis Avanzado")

        ttk.Label(advanced_window, text="Buscar palabra:").pack(pady=5)
        entry_palabra = ttk.Entry(advanced_window, width=30)
        entry_palabra.pack(pady=5)

        def buscar_palabra():
            palabra = entry_palabra.get().strip()
            if not palabra:
                return
            count = self.stored_text.lower().split().count(palabra.lower())
            ttk.Label(advanced_window, text=f"La palabra '{palabra}' aparece {count} veces.").pack(pady=5)

        ttk.Button(advanced_window, text="Buscar", command=buscar_palabra).pack(pady=5)

    def exportar_a_excel(self):
        if not self.analisis_realizado:
            messagebox.showwarning("Exportar a Excel", "Por favor, realice un análisis antes de exportar los datos.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Archivos de Excel", "*.xlsx")])
        if not file_path:
            return

        workbook = openpyxl.Workbook()
        sheet = workbook.active

        for idx, col in enumerate(self.tree["columns"], start=1):
            sheet.cell(row=1, column=idx, value=col)

        for idx, item in enumerate(self.tree.get_children(), start=2):
            for col_idx, col in enumerate(self.tree["columns"], start=1):
                sheet.cell(row=idx, column=col_idx, value=self.tree.set(item, col))

        workbook.save(file_path)
        messagebox.showinfo("Exportar a Excel", "Los datos han sido exportados correctamente.")

    def convertir_a_grafica(self):
        if not self.analisis_realizado:
            messagebox.showerror("Error", "Realice un análisis primero.")
            return

        pos_counts, total_words, num_sentences = self.analyzer.analyze_text(self.stored_text)
        categorias = list(pos_counts.keys())
        valores = list(pos_counts.values())
        categorias.extend(["Total Words", "Num Sentences", "Media Palabras por Oración"])
        valores.extend([total_words, num_sentences, total_words / num_sentences if num_sentences != 0 else 0])

        plt.figure(figsize=(10, 8))
        plt.bar(categorias, valores, color='skyblue')
        plt.xlabel('Categorías y Métricas')
        plt.ylabel('Frecuencia o Valor')
        plt.title('Frecuencia de categorías gramaticales y métricas adicionales')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

    def resaltar_errores_ortograficos(self, event):
        self.text_box.tag_remove("highlight", "1.0", tk.END)
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

    def transcribe_audio_from_button(self):
        audio_file_path = filedialog.askopenfilename(filetypes=[("Archivos de audio MP3", "*.mp3")])
        if audio_file_path:
            transcription = transcribe_audio(audio_file_path)
            print("Texto transcrito:", transcription)
        else:
            print("No se seleccionó ningún archivo MP3.")

def main():
    root = tk.Tk()
    app = Aplicacion(root)
    root.mainloop()

if __name__ == "__main__":
    main()
