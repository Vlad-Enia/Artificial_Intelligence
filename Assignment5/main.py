import lightrdf
import nltk
import functools
import re


### Ex. 2 ###
def ex2(word):
    word = word.lower()
    parser = lightrdf.Parser()  # or lightrdf.xml.Parser() for xml
    for triple in parser.parse("./CSO.3.3.owl", base_iri=None):
        if 'superTopicOf' in triple[1]:
            superTopic = triple[0].rsplit('/', 1)[1]
            superTopicList = superTopic.split('_')
            subTopic = triple[2].rsplit('/', 1)[1]
            subTopicList = subTopic.split('_')
            if (word in superTopicList) or (word in subTopicList):
                print(superTopic, ' - superTopicOf - ', subTopic)

w = input('Ex.2 word: ')
ex2(w)


### Ex. 3 ###

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

fp = open('computer-science.txt', 'rb')
data = fp.read().decode(encoding='utf-8')

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sentences = tokenizer.tokenize(data)

fd_w = open('sentences.txt', 'w')

expr = re.compile('[n|v]*n[n|v]*v[n|v*]*n[n|v]*')
for sentence in sentences:
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    res = list(filter(lambda e: e[1][0] == 'N' or e[1][0] == 'V', tagged))

    n_v_sequence = functools.reduce(lambda a, b: (a + 'v' if b[1][0] == 'V' else a + 'n'), res, '')
    if expr.match(n_v_sequence):
        fd_w.write(sentence.replace('\n', ' '))
        fd_w.write('\n\n')
    else:
        print("SENTENCE NOT WRITTEN:", sentence)
        print("ANNOTATION:", tagged)
        print("REDUCED SEQUENCE:", n_v_sequence)
        print('\n\n')

fd_w.close()


### Ex. 4 ###

def is_word_in_ontology(word):
    word = word.lower()
    parser = lightrdf.Parser()  # or lightrdf.xml.Parser() for xml
    for triple in parser.parse("./CSO.3.3.owl", base_iri=None):
        if 'superTopicOf' in triple[1]:
            superTopic = triple[0].rsplit('/', 1)[1]
            superTopicList = superTopic.split('_')
            subTopic = triple[2].rsplit('/', 1)[1]
            subTopicList = subTopic.split('_')
            if (word in superTopicList) or (word in subTopicList):
                return True
    return False


fp = open('sentences.txt', 'r')
data = fp.read()
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
sentences = tokenizer.tokenize(data)

for sentence in sentences:
    tokens = nltk.word_tokenize(sentence)
    for word in tokens:
        if is_word_in_ontology(word):
            print("FOUND:", sentence)
            break