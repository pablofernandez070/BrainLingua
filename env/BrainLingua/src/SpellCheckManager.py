# spellcheck_manager.py
from spellchecker import SpellChecker

class SpellCheckManager:
    def __init__(self, language='es'):
        self.spell_checker = SpellChecker(language='es')
    
    def corregir_ortografia(self, texto):
        palabras = texto.split()
        texto_corregido = []

        for palabra in palabras:
            # Eliminar signos de puntuación al final de la palabra
            while palabra and palabra[-1] in ".,:;?!¿":
                palabra = palabra[:-1]

            if self.spell_checker.unknown([palabra]):
                # La palabra no está en el diccionario, sugerir correcciones
                correcciones = self.spell_checker.correction(palabra)
                if correcciones:
                    palabra_corregida = correcciones  # Seleccionar la primera corrección sugerida
                else:
                    palabra_corregida = palabra  # Si no hay correcciones sugeridas, conservar la palabra original
            else:
                palabra_corregida = palabra  # La palabra está en el diccionario, no es un error ortográfico
            texto_corregido.append(palabra_corregida)

        return ' '.join(texto_corregido)
    
    def obtener_palabras_incorrectas(self, texto):
        palabras = texto.split()
        palabras_incorrectas = [palabra for palabra in palabras if self.spell_checker.unknown([palabra])]
        return palabras_incorrectas