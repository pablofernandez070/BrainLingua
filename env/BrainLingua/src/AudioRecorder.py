import tkinter as tk
from tkinter import ttk
import speech_recognition as sr

class AudioRecorder:
    def __init__(self, parent, text_box):
        self.parent = parent
        self.text_box = text_box

    def record_voice(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.text_box.insert(tk.END, "Grabando...\n")
            self.parent.update()
            audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language='es-ES')
            self.text_box.insert(tk.END, text + "\n")
            self.text_box.insert(tk.END, "Presiona el botón para grabar de nuevo\n")
        except sr.UnknownValueError:
            self.text_box.insert(tk.END, "No se pudo entender el audio\n")
        except sr.RequestError as e:
            self.text_box.insert(tk.END, f"Error en la solicitud: {e}\n")
