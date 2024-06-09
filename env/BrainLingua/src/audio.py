import speech_recognition as sr
from pydub import AudioSegment
import os
import matplotlib.pyplot as plt

def mp3_to_wav(mp3_path):
    audio = AudioSegment.from_mp3(mp3_path)
    wav_path = mp3_path.replace('.mp3', '.wav')
    audio.export(wav_path, format="wav")
    return wav_path

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    wav_file = mp3_to_wav(audio_file)
    with sr.AudioFile(wav_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="es-ES")
            return text
        except sr.UnknownValueError:
            return "No se pudo entender el audio"
        except sr.RequestError as e:
            return f"Error al solicitar el reconocimiento de voz; {e}"
        finally:
            os.remove(wav_file)  # Eliminar el archivo WAV temporal
