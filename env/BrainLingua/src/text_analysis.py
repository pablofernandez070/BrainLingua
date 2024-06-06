# En tu archivo text_analysis.py
from palabras_malsonantes import contar_palabras_malsonantes
import spacy
from collections import Counter

class TextAnalyzer:
    def __init__(self):
        self.nlp = spacy.load("es_core_news_md")
        self.previous_searches = []

    def analyze_text(self, text):
        # Tokenizar y analizar el texto usando SpaCy
        doc = self.nlp(text)

        # Dividir el texto en oraciones
        sentences = [sent.text.strip() for sent in doc.sents]

        # Contar numero oraciones
        num_sentences = len(sentences)

        # Calcular el recuento total de palabras
        words = [token.text for token in doc if token.is_alpha]
        total_words = len(words)

        # Obtener todas las categorías gramaticales posibles
        pos_counts = Counter([token.pos_ for token in doc])

        # Guardar la búsqueda actual en la lista de búsquedas anteriores
        self.previous_searches.append(text)

        # Imprimir la lista de búsquedas anteriores en la consola
        print("Búsquedas anteriores:", self.previous_searches)

        return pos_counts, total_words, num_sentences
    
    def average_words_per_sentence(self, text):
        doc = self.nlp(text)
        sentences = list(doc.sents)
        if not sentences:
            return 0.0

        total_words = sum(sum(1 for token in sentence if token.is_alpha) for sentence in sentences)
        average = total_words / len(sentences)
        
        return average
    
    """def count_palabras_largas(self, text):
        doc = self.nlp(txt)"""
        

    def count_palabras_malsonantes(self, text):
        # Utilizar la función importada desde palabras_malsonantes
        return contar_palabras_malsonantes(text)
    
    def get_previous_searches(self):
        return self.previous_searches

    def pos_tag_text(self, text):
        doc = self.nlp(text)
        pos_tags = [(token.text, token.pos_) for token in doc]
        return pos_tags
