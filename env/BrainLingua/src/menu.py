import tkinter as tk
from tkinter import ttk, messagebox

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
        self.file_menu.add_command(label="Abrir", command= self.show_pendiente_info)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Guardar", command= self.show_pendiente_info)
        self.file_menu.add_command(label="Guardar como...", command= self.show_pendiente_info)
        self.file_menu.add_command(label="Recientes", command= self.show_pendiente_info)
        self.file_menu.add_command(label="Imprimir", command= self.show_pendiente_info)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Salir", command=root.quit)

        # Agregar opciones al menú Diccionario
        self.dictionary_menu.add_command(label="Buscar", command= self.show_pendiente_info)
        self.dictionary_menu.add_command(label="Añadir", command= self.show_pendiente_info)
        self.dictionary_menu.add_command(label="Eliminar", command= self.show_pendiente_info)

        # Agregar opciones al menú Ayuda
        self.help_menu.add_command(label="Acerca de", command=self.show_about_info)

        # Agregar opciones al menú Configuración
        self.config_menu.add_command(label="Opción 1", command= self.show_pendiente_info)
        self.config_menu.add_command(label="Opción 2", command= self.show_pendiente_info)

        # Configurar la barra de menú en la ventana principal
        root.config(menu=self.menu_bar)

    def show_about_info(self):
        about_message = (
            "BrainLingua\n"
            "Versión 1.0\n"
            "Aplicación para la transcripción y análisis de texto y audio.\n\n"
            "Desarrollado por: Pablo Fernández Planas\n"
            "Contacto: pablofernandezplanas@gmail.com\n\n"
            "CATEGORIAS TABLA:\n\n"
            "ADJ: Adjetivos\n"
            "ADP: Adposiciones\n"
            "ADV: Adverbios\n"
            "AUX: Verbos auxiliares\n"
            "CONJ: Conjunciones\n"
            "CCONJ: Conjunciones de coordinación\n"
            "DET: Determinantes\n"
            "INTJ: Interjecciones\n"
            "NOUN: Sustantivos\n"
            "NUM: Numerales\n"
            "PART: Partículas\n"
            "PRON: Pronombres\n"
            "PROPN: Nombres propios\n"
            "PUNCT: Signos de puntuación\n"
            "SCONJ: Conjunciones subordinadas\n"
            "SYM: Símbolos\n"
            "VERB: Verbos\n"
            "X: Otros\n"
            "TW: Palabras Totales\n"
            "NS: Numero de Oraciones\n"
            "Avg W/S: Promedio de palabras por oración\n"
            "PM: Palabras malsonantes\n"
            "PG: Palabras mayores a 6 letras\n"
        )
        messagebox.showinfo("Acerca de BrainLingua", about_message)

    def show_pendiente_info(self):
        about_message = (
            "La presente funcionalidad está en desarrollo\n"
            "Disculpe las molestias\n"
        )
        messagebox.showinfo("En Desarrollo", about_message)