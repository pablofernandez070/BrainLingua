import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

def convertir_a_grafica(self):
    if not self.analisis_realizado:
        messagebox.showerror("Error", "Realice un análisis primero.")
        return

    # Obtener el diccionario de variables del análisis de texto
    variables = self.analyzer.analyze_text(self.stored_text)
    
    # Definir las categorías y valores para la gráfica
    categorias = list(variables.keys())  # Las categorías son las claves del diccionario
    valores = list(variables.values())   # Los valores son los valores del diccionario

    # Crear la gráfica de barras
    plt.figure(figsize=(10, 8))
    barras = plt.bar(categorias, valores, color='#207567')
    plt.xlabel('Categorías y Métricas')
    plt.ylabel('Frecuencia o Valor')
    plt.title('Frecuencia de categorías gramaticales y métricas adicionales')
    plt.xticks(rotation=45, ha='right')

    # Agregar los valores encima de cada barra
    for barra in barras:
        altura = barra.get_height()
        plt.text(barra.get_x() + barra.get_width() / 2, altura, f'{altura:.2f}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

