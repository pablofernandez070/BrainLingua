import speech_recognition as sr
from tkinter import filedialog, Tk

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="es-ES")
            return text
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
        except sr.RequestError as e:
            print(f"Error al solicitar el reconocimiento de voz; {e}")

def main():
    root = Tk()
    root.withdraw()  # Ocultar la ventana principal de Tkinter
    audio_file = filedialog.askopenfilename(filetypes=[("Archivos de audio MP3", "*.mp3")])
    
    if audio_file:
        transcription = transcribe_audio(audio_file)
        print("Texto transcrito:", transcription)
    else:
        print("No se seleccionó ningún archivo MP3.")

if __name__ == "__main__":
    main()
