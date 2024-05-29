# text_analysis.py
import spacy
from collections import Counter

class TextAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("es_core_news_md")
        self.previous_searches = []

    def analyze_text(self, text):
        # Tokenizar y analizar el texto usando SpaCy
        doc = self.nlp(text)

        # Obtener todas las categorías gramaticales posibles
        pos_counts = Counter([token.pos_ for token in doc])

        # Calcular el recuento total de palabras
        words = [token.text for token in doc if token.is_alpha]
        total_words = len(words)

        # Guardar la búsqueda actual en la lista de búsquedas anteriores
        self.previous_searches.append(text)

        # Imprimir la lista de búsquedas anteriores en la consola
        print("Búsquedas anteriores:", self.previous_searches)

        return pos_counts, total_words

    def get_previous_searches(self):
        return self.previous_searches
