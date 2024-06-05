import tkinter as tk
from tkinter import ttk, PhotoImage, filedialog, messagebox

def abrir_analisis_avanzado(self):
    if not self.analisis_realizado:
        messagebox.showwarning("Error", "Por favor, ejecute un análisis antes de realizar un análisis avanzado.")
        return

    advanced_window = tk.Toplevel(self.root)
    advanced_window.title("Análisis Avanzado")
    advanced_window.configure(bg="#2e2e2e")

    ttk.Label(advanced_window, text="Buscar palabra:", style="TLabel").pack(pady=5)
    entry_palabra = ttk.Entry(advanced_window, width=30)
    entry_palabra.pack(pady=5)

    def buscar_palabra():
        palabra = entry_palabra.get().strip()
        if not palabra:
            return
        count = self.stored_text.lower().split().count(palabra.lower())
        ttk.Label(advanced_window, text=f"La palabra '{palabra}' aparece {count} veces.", style="TLabel").pack(pady=5)

    ttk.Button(advanced_window, text="Buscar", command=buscar_palabra).pack(pady=5)
