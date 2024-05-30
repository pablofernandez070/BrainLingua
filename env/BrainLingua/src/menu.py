import tkinter as tk
from tkinter import ttk

class MenuBar:
    def __init__(self, root):
        self.root = root

        # Crear un objeto Style
        self.style = ttk.Style()

        # Configurar el estilo de la barra de menú
        self.style.theme_use('clam')
        self.style.configure('MenuBar.TMenubutton', background='#ADD8E6')  # Configurar el color de fondo a azul claro

        # Crear un objeto Menu
        self.menu_bar = tk.Menu(root)

        # Crear los menús principales
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.dictionary_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.config_menu = tk.Menu(self.menu_bar, tearoff=0)

        # Configurar los menús principales
        self.menu_bar.add_cascade(label="Archivo", menu=self.file_menu)
        self.menu_bar.add_cascade(label="Diccionario", menu=self.dictionary_menu)
        self.menu_bar.add_cascade(label="Ayuda", menu=self.help_menu)
        self.menu_bar.add_cascade(label="Configuración", menu=self.config_menu)

        # Agregar opciones al menú Archivo
        self.file_menu.add_command(label="Abrir")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=root.quit)

        # Agregar opciones al menú Diccionario
        self.dictionary_menu.add_command(label="Buscar")
        self.dictionary_menu.add_command(label="Añadir")
        self.dictionary_menu.add_command(label="Eliminar")

        # Agregar opciones al menú Ayuda
        self.help_menu.add_command(label="Acerca de")

        # Agregar opciones al menú Configuración
        self.config_menu.add_command(label="Opción 1")
        self.config_menu.add_command(label="Opción 2")

        # Configurar la barra de menú en la ventana principal
        root.config(menu=self.menu_bar)