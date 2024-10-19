import nltk
from nltk import sent_tokenize
from nltk.tokenize import word_tokenize as wt

from textAsADict.guttenbergSupplier import GutenbergSupplier
from utils.lemmatizer import Lemmatizer
from utils.processor import Processor
from setOperationsHandler import SetOperationsHandler
from pdfToText.textReader import TextReader
from utils.verbsList import verbs


class TextToDictionary:
    def __init__(self):
        self.lemmatizer = Lemmatizer()
        self.verbs = verbs
        self.processor = Processor()
        self.set_operation_handler = SetOperationsHandler()
        self.text = GutenbergSupplier().get_text()

    # Główna funkcja przetwarzająca tekst
    def text_transition(self, text):
        sentences = sent_tokenize(text)
        for sentence in sentences:
           # print(f"Przetwarzanie zdania: {sentence}")
            cont_sent_token = wt(sentence)
           # print(f"Tokeny: {cont_sent_token}")
            cont_sent_tag = nltk.pos_tag(cont_sent_token)
           # print(f"Tagowanie POS: {cont_sent_tag}")
            cont_sent_tag_baseNouns = self.processor.process_nouns(cont_sent_tag)
            # Lematyzacja czasowników
            sent_lem_tags = self.lemmatizer.transform_v_to_base(cont_sent_tag_baseNouns)
            self.processor.verbs_sequels(sent_lem_tags)
        # print(f"Wynikowy słownik czasowników:\n {verbs}")
        return verbs

    def get_dictionary(self):
        return self.text_transition(self.text)
