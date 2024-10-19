from textblob import Word
from utils.verbsList import verbs

class Processor():
    def __init__(self):
        pass

    def process_nouns(self, cont_sent_tag):
        for i, (word, tag) in enumerate(cont_sent_tag):
            if tag.startswith('NN'):
                word = Word(word).singularize()
                cont_sent_tag[i] = (word, 'NN')
        return cont_sent_tag

    # Funkcja uzupełniająca słownik słowami występującymi po czasownikach

    def verbs_sequels(self,sent_lem_tags):
        for i, (word, tag) in enumerate(sent_lem_tags):
            verb = ""
            if tag.startswith('V'):
                verb = word
                if i + 1 < len(sent_lem_tags) and (sent_lem_tags[i + 1][1] == 'TO' or sent_lem_tags[i + 1][1] == 'RP'):
                    verb += " to"
                    if verb in verbs and i + 2 < len(sent_lem_tags):
                        verbs[verb].append(sent_lem_tags[i + 2][0])
                        continue
                if verb in verbs:
                    if i + 1 < len(sent_lem_tags):
                        verbs[verb].append(sent_lem_tags[i + 1][0])  # Dodanie słowa po czasowniku
