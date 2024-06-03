import speech_recognition as sr

def transcribe_audio(audio_file):
    # Inicializar el reconocedor de voz
    recognizer = sr.Recognizer()

    # Abrir el archivo de audio
    with sr.AudioFile(audio_file) as source:
        # Escuchar el contenido del archivo de audio
        audio_data = recognizer.record(source)

        try:
            # Utilizar Google Speech Recognition para transcribir el audio
            text = recognizer.recognize_google(audio_data, language="es-ES")
            return text
        except sr.UnknownValueError:
            print("No se pudo entender el audio")
        except sr.RequestError as e:
            print(f"Error al solicitar el reconocimiento de voz; {e}")


# Ruta del archivo de audio MP3
audio_file = "audio.mp3"

# Transcribir el audio
transcription = transcribe_audio(audio_file)
print("Texto transrito:", transcription)
