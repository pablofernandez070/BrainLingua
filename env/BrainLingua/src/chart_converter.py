import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt


def convertir_a_grafica(self):
    if not self.analisis_realizado:
        messagebox.showerror("Error", "Realice un análisis primero.")
        return

    pos_counts, total_words, num_sentences = self.analyzer.analyze_text(self.stored_text)
    count_palabras_malsonantes = self.analyzer.count_palabras_malsonantes(self.stored_text)

    # Agregar la columna de palabras malsonantes a las categorías
    categorias = list(pos_counts.keys()) + ["Total Words", "Num Sentences", "Media Palabras por Oración", "Palabras malsonantes"]
    valores = list(pos_counts.values()) + [total_words, num_sentences, total_words / num_sentences if num_sentences != 0 else 0, count_palabras_malsonantes]

    plt.figure(figsize=(10, 8))
    plt.bar(categorias, valores, color='#207567')
    plt.xlabel('Categorías y Métricas')
    plt.ylabel('Frecuencia o Valor')
    plt.title('Frecuencia de categorías gramaticales y métricas adicionales')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()