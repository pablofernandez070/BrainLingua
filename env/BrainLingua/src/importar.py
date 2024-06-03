# importar.py
import tkinter as tk
from tkinter import filedialog
import fitz
import docx

def leer_pdf(text_box):
    archivo_pdf = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if archivo_pdf:
        documento = fitz.open(archivo_pdf)
        texto_completo = ""
        for pagina_num in range(documento.page_count):
            pagina = documento.load_page(pagina_num)
            texto_pagina = pagina.get_text("text")
            texto_completo += texto_pagina
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, texto_completo)

def leer_txt(text_box):
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
    if not file_path:
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, content)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        tk.messagebox.showerror("Error", "No se pudo leer el archivo. Asegúrate de que el archivo está codificado en UTF-8.")

def leer_docx(text_box):
    archivo_docx = filedialog.askopenfilename(filetypes=[("Word Files", "*.docx")])
    if archivo_docx:
        doc = docx.Document(archivo_docx)
        texto = ""
        for paragraph in doc.paragraphs:
            texto += paragraph.text + "\n"
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, texto)
