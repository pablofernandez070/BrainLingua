# En tu archivo text_analysis.py
from palabras_malsonantes import contar_palabras_malsonantes
import spacy
from collections import Counter

class TextAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("es_core_news_md")
        self.previous_searches = []
        self.previous_analyses = []  # Lista para almacenar los resultados de cada análisis

        # Definir las variables que se inicializan en 0
        self.variables = {
            "ADJ": 0,  # Adjetivos
            "ADP": 0,  # Adposiciones
            "ADV": 0,  # Adverbios
            "AUX": 0,  # Verbos auxiliares
            "CONJ": 0,  # Conjunciones
            "CCONJ": 0,  # Conjunciones de coordinación
            "DET": 0,  # Determinantes
            "INTJ": 0,  # Interjecciones
            "NOUN": 0,  # Sustantivos
            "NUM": 0,  # Numerales
            "PART": 0,  # Partículas
            "PRON": 0,  # Pronombres
            "PROPN": 0,  # Nombres propios
            "PUNCT": 0,  # Signos de puntuación
            "SCONJ": 0,  # Conjunciones subordinadas
            "SYM": 0,  # Símbolos
            "VERB": 0,  # Verbos
            "X": 0,  # Otros
            "Total Words": 0,
            "N Sentences": 0,
            "Avg Words/Sentence": 0,
            "PM": 0,  # Palabras malsonantes
            "PG": 0,  # Palabras mayores a 6 letras
        }

    def analyze_text(self, text):
        # Resetear las variables antes del nuevo análisis
        self.reset_variables()

        # Tokenizar y analizar el texto usando SpaCy
        doc = self.nlp(text)

        # Dividir el texto en oraciones
        sentences = [sent.text.strip() for sent in doc.sents]

        # Contar número de oraciones
        num_sentences = len(sentences)
        self.variables["N Sentences"] = num_sentences

        # Calcular el recuento total de palabras
        words = [token.text for token in doc if token.is_alpha]
        total_words = len(words)
        self.variables["Total Words"] = total_words

        # Obtener todas las categorías gramaticales posibles
        pos_counts = Counter([token.pos_ for token in doc])
        for pos, count in pos_counts.items():
            if pos in self.variables:
                self.variables[pos] = count

        # Calcular el promedio de palabras por oración
        avg_words_per_sentence = self.average_words_per_sentence(text)
        self.variables["Avg Words/Sentence"] = avg_words_per_sentence

        # Contar palabras malsonantes
        count_palabras_malsonantes = self.count_palabras_malsonantes(text)
        self.variables["PM"] = count_palabras_malsonantes

        # Contar el número de palabras mayores a 6 letras
        palabras_mayores_seis_letras = sum(1 for word in text.split() if len(word) > 6)
        self.variables["PG"] = palabras_mayores_seis_letras

        # Guardar los resultados del análisis actual en la lista de análisis anteriores
        self.previous_analyses.append(self.variables.copy())  # Copy evita que se sobreescriba

        # Guardar la búsqueda actual en la lista de búsquedas anteriores
        self.previous_searches.append(text)

        # Imprimir la lista de búsquedas anteriores en la consola
        print("Búsquedas anteriores:", self.previous_searches)

        return self.previous_analyses

    def reset_variables(self):
        for key in self.variables:
            self.variables[key] = 0

    def average_words_per_sentence(self, text):
        doc = self.nlp(text)
        sentences = list(doc.sents)
        if not sentences:
            return 0.0

        total_words = sum(sum(1 for token in sentence if token.is_alpha) for sentence in sentences)
        average = total_words / len(sentences)
        
        return average

    def count_palabras_malsonantes(self, text):
        # Utilizar la función importada desde palabras_malsonantes
        return contar_palabras_malsonantes(text)

    def get_previous_searches(self):
        return self.previous_searches

    def get_previous_analyses(self):
        return self.previous_analyses

    def pos_tag_text(self, text):
        doc = self.nlp(text)
        pos_tags = [(token.text, token.pos_) for token in doc]
        return pos_tags
