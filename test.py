import nltk
from nltk.tokenize import word_tokenize as wt, sent_tokenize
from nltk.stem import WordNetLemmatizer
from textblob import Word

# Inicjalizacja lematyzatora
lem = WordNetLemmatizer()

# Lista czasowników zamieniona na słownik z pustymi listami
verbs = {
    'be': [], 'have': [], 'do': [], 'say': [], 'go to': [], 'get': [], 'make': [], 'know': [], 'think about': [],
    'take': [], 'see': [], 'come to': [], 'want': [], 'look at': [], 'use': [], 'find': [], 'give to': [], 
    'tell about': [], 'work on': [], 'call': [], 'try': [], 'ask for': [], 'need': [], 'feel like': [], 
    'become': [], 'leave for': [], 'put on': [], 'mean': [], 'keep': [], 'let': [], 'begin with': [], 'seem': [],
    'help': [], 'talk to': [], 'turn into': [], 'start with': [], 'show': [], 'hear about': [], 'play with': [], 
    'run to': [], 'move to': [], 'like': [], 'live in': [], 'believe in': [], 'hold on to': [], 'bring to': [], 
    'happen to': [], 'write about': [], 'provide for': [], 'sit on': [], 'stand by': [], 'lose to': [], 
    'pay for': [], 'meet with': [], 'include in': [], 'continue with': [], 'set up': [], 'learn about': [], 
    'change into': [], 'lead to': [], 'understand': [], 'watch': [], 'follow': [], 'stop at': [], 'create': [], 
    'speak to': [], 'read about': [], 'allow for': [], 'add to': [], 'spend on': [], 'grow into': [], 
    'open to': [], 'walk to': [], 'win against': [], 'offer': [], 'remember': [], 'love': [], 'consider': [], 
    'appear in': [], 'buy for': [], 'wait for': [], 'serve as': [], 'die from': [], 'send to': [], 
    'expect from': [], 'build': [], 'stay at': [], 'fall into': [], 'cut into': [], 'reach for': [], 
    'kill': [], 'remain': [], 'suggest to': [], 'drink': [], 'eat': [], 'pass by': [], 'sell to': [], 
    'require': [], 'report on': [], 'decide on': [], 'pull': [], 'invest in': [], 'focus on': [], 
    'prepare for': [], 'talk about': [], 'fight against': [], 'agree with': [], 'dream of': [], 'depend on': [], 
    'apply for': [], 'argue with': [], 'listen to': [], 'care about': [], 'hope for': [], 'plan for': []
}

# Główna funkcja przetwarzająca tekst
def text_transition(text):
    sentences = sent_tokenize(text)
    for sentence in sentences:
        print(f"Przetwarzanie zdania: {sentence}")       
        cont_sent_token = wt(sentence)
        print(f"Tokeny: {cont_sent_token}")
        cont_sent_tag = nltk.pos_tag(cont_sent_token)
        print(f"Tagowanie POS: {cont_sent_tag}")
        cont_sent_tag_baseNouns = process_nouns(cont_sent_tag)
        # Lematyzacja czasowników
        sent_lem_tags = transform_v_to_base(cont_sent_tag_baseNouns)  
        verbs_sequels(sent_lem_tags)

    print(f"Wynikowy słownik czasowników:\n {verbs}")

# Funkcja lematyzująca czasowniki
def verb_to_wordnet(verb_tag):
    if verb_tag.startswith('V') or verb_tag.startswith('JJ'):
        return 'v'
    
def transform_v_to_base(cont_sent_tag):
    cont_sent_lem = []

    for i in cont_sent_tag:
        wordnet_verb = verb_to_wordnet(i[1])
        
        if wordnet_verb is not None:
            cont_sent_lem.append(lem.lemmatize(i[0], wordnet_verb))
        else:
            cont_sent_lem.append(i[0])

    print(f"Zdanie po lematyzacji: {cont_sent_lem}")
    sent_lem_tags = nltk.pos_tag(cont_sent_lem)
    return sent_lem_tags

# Funkcja uzupełniająca słownik słowami występującymi po czasownikach
# TODO
# - logika dodawnaia słów: które części mowy dodajmey
#  czy dodajemy tylko nouns czy moze wszytsko
def verbs_sequels(sent_lem_tags):
    for i, (word, tag) in enumerate(sent_lem_tags):
        verb = ""
        if tag.startswith('V'):
            verb = word
            if i + 1 < len(sent_lem_tags) and (sent_lem_tags[i+1][1] == 'TO' or sent_lem_tags[i+1][1] == 'RP'):  
                verb += " to"
                if verb in verbs and i + 2 < len(sent_lem_tags):
                    verbs[verb].append(sent_lem_tags[i+2][0])
                    continue
            if verb in verbs:
                if i + 1 < len(sent_lem_tags):
                    verbs[verb].append(sent_lem_tags[i+1][0])  # Dodanie słowa po czasowniku
        
def process_nouns(cont_sent_tag):
    
    for i,(word, tag) in enumerate(cont_sent_tag):
            if tag.startswith('NN'):
                word = Word(word).singularize()
                cont_sent_tag[i] = (word, 'NN')
    return cont_sent_tag
# Przykładowy tekst do przetworzenia
cont_sent = 'Harry Potter is coming to Hogwarts. Bees are buzzing around the honeycomb.'
text_transition(cont_sent)
