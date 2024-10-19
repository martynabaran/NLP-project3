# Funkcja lematyzująca czasowniki
import nltk
from nltk import WordNetLemmatizer

lem = WordNetLemmatizer()

class Lemmatizer:
    def __init__(self):
        pass

    def verb_to_wordnet(self, verb_tag):
        if verb_tag.startswith('V') or verb_tag.startswith('JJ'):
            return 'v'

    def transform_v_to_base(self, cont_sent_tag):
        cont_sent_lem = []

        for i in cont_sent_tag:
            wordnet_verb = self.verb_to_wordnet(i[1])

            if wordnet_verb is not None:
                cont_sent_lem.append(lem.lemmatize(i[0], wordnet_verb))
            else:
                cont_sent_lem.append(i[0])

        sent_lem_tags = nltk.pos_tag(cont_sent_lem)
        return sent_lem_tags
