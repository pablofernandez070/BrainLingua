# En tu archivo analisis_avanzado.py
import tkinter as tk
from tkinter import ttk
from collections import Counter
from text_analysis import TextAnalyzer

def abrir_analisis_avanzado(parent, text):
    # Crear la ventana de análisis avanzado
    ventana_analisis = tk.Toplevel(parent)
    ventana_analisis.title("Análisis Avanzado")
    ventana_analisis.geometry("1000x400")
    ventana_analisis.configure(bg="#2e2e2e")

    # Función para actualizar la tabla según la categoría gramatical seleccionada
    def actualizar_tabla():
        selected_pos = combo_pos.get()
        pos_tags = analyzer.pos_tag_text(text)
        selected_words = [word for word, pos in pos_tags if pos == selected_pos]
        word_counts = Counter(selected_words)
        most_common_words = word_counts.most_common(10)

        # Limpiar la tabla antes de actualizar
        for item in tree.get_children():
            tree.delete(item)

        # Insertar los datos actualizados en la tabla
        for word, count in most_common_words:
            tree.insert("", tk.END, values=(word, count))

    # Crear un frame para el análisis avanzado
    frame_avanzado = ttk.Frame(ventana_analisis, style="TFrame")
    frame_avanzado.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)

    # Crear un frame para la búsqueda de palabras específicas
    frame_busqueda = ttk.Frame(ventana_analisis, style="TFrame")
    frame_busqueda.pack(fill=tk.BOTH, expand=True, side=tk.RIGHT)

    # Analizar el texto para obtener los sustantivos
    analyzer = TextAnalyzer()
    pos_tags = analyzer.pos_tag_text(text)

    # Crear un menú desplegable para seleccionar la categoría gramatical
    ttk.Label(frame_avanzado, text="Seleccionar Categoría Gramatical:", style="TLabel").pack(pady=5)
    combo_pos = ttk.Combobox(frame_avanzado, values=["NOUN", "ADJ", "VERB"], state="readonly")
    combo_pos.pack()
    combo_pos.current(0)  # Establecer la selección predeterminada
    combo_pos.bind("<<ComboboxSelected>>", lambda event: actualizar_tabla())  # Actualizar la tabla cuando se cambie la selección
    
    # Crear la tabla para el análisis avanzado
    tree = ttk.Treeview(frame_avanzado, columns=("word", "count"), show='headings')
    tree.heading("word", text="Palabra")
    tree.heading("count", text="Frecuencia")
    tree.column("word", anchor=tk.CENTER)
    tree.column("count", anchor=tk.CENTER)
    tree.pack(fill=tk.BOTH, expand=True)

    # Insertar los datos iniciales en la tabla (sustantivos por defecto)
    selected_words = [word for word, pos in pos_tags if pos == "NOUN"]
    word_counts = Counter(selected_words)
    most_common_words = word_counts.most_common(10)
    for word, count in most_common_words:
        tree.insert("", tk.END, values=(word, count))

    # Crear una etiqueta y una entrada para buscar palabras específicas
    ttk.Label(frame_busqueda, text="Buscar Palabra Específica:", style="TLabel").pack(pady=5)
    entry_palabra = ttk.Entry(frame_busqueda, width=30)
    entry_palabra.pack(pady=5)

    # Función para buscar la frecuencia de una palabra específica
    def buscar_palabra():
        palabra = entry_palabra.get().strip()
        if not palabra:
            return
        count = text.lower().split().count(palabra.lower())
        ttk.Label(frame_busqueda, text=f"La palabra '{palabra}' aparece {count} veces.", style="TLabel").pack(pady=5)

    # Botón para realizar la búsqueda
    ttk.Button(frame_busqueda, text="Buscar", command=buscar_palabra).pack(pady=5)

    # Configurar estilos
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

    ventana_analisis.mainloop()
