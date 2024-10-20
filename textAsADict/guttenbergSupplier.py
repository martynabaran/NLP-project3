import nltk
from nltk import sent_tokenize
from nltk.corpus import gutenberg


class GutenbergSupplier:
    def __init__(self):
        # Download the required resources
        nltk.download('gutenberg')
        nltk.download('punkt')

    def get_text(self):
        sentences = gutenberg.sents()
        sentences_joined = [' '.join(sentence) for sentence in sentences]
        return ' '.join(sentences_joined)[:1000000]
