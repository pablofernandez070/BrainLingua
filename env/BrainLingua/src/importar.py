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
    archivo_txt = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if archivo_txt:
        with open(archivo_txt, "r") as file:
            texto = file.read()
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, texto)

def leer_docx(text_box):
    archivo_docx = filedialog.askopenfilename(filetypes=[("Word Files", "*.docx")])
    if archivo_docx:
        doc = docx.Document(archivo_docx)
        texto = ""
        for paragraph in doc.paragraphs:
            texto += paragraph.text + "\n"
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, texto)
