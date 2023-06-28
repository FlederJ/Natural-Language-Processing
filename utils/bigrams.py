import nltk

from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

nltk.download('gutenberg')
nltk.download('punkt')
nltk.download('stopwords')

import string

import gensim
from gensim.models.phrases import Phraser, Phrases

from nltk.corpus import gutenberg

gberg_sents = gutenberg.sents()

stpwrds = stopwords.words('english') + list(string.punctuation)

stemmer = PorterStemmer()


def gberg_sent_n(text, n=None):
    gberg_sents_clean = []
    if n != None:
        for w in text[n]:
            if w.lower() not in stpwrds:
                gberg_sents_clean.append(stemmer.stem(w.lower()))
    else:
        for w in gberg_sents:
            for v in w:
                if v.lower() not in stpwrds:
                    gberg_sents_clean.append(stemmer.stem(v.lower()))

    print(gberg_sents_clean)
    return gberg_sents_clean


def gberg_sent_bigram(text):
    lower_sents = []
    for s in text:
        lower_sents.append([
            w.lower() for w in s if w.lower() not in list(string.punctuation)
        ])

    lower_bigram = Phraser(Phrases(lower_sents))

    clean_sents = []
    for s in lower_sents:
        clean_sents.append(lower_bigram[s])
    return clean_sents
