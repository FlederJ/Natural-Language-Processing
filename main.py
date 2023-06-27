import nltk

from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *
import pickle
import random

nltk.download('gutenberg')
nltk.download('punkt')
nltk.download('stopwords')

import string

import gensim
from gensim.models.phrases import Phraser, Phrases
from gensim.models.word2vec import Word2Vec

from sklearn.manifold import TSNE

import pandas as pd
from bokeh.io import output_notebook, output_file
from bokeh.plotting import show, figure

from nltk.corpus import gutenberg

gberg_sents = gutenberg.sents()

stpwrds = stopwords.words('english') + list(string.punctuation)

stemmer = PorterStemmer()


def gbergSentN(text, n=None):
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


def gbergSentBigram(text):
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


def save_phraser(phraser, filename):
    with open(filename, 'wb') as f:
        pickle.dump(phraser, f)


def load_phraser(filename):
    with open(filename, 'rb') as f:
        phraser = pickle.load(f)
    return phraser


def list_to_string(s):
    str = ""
    for i in s:
        str += i + " "
    return str


phraser_filename = 'phraser.pkl'
try:
    phraser = load_phraser(phraser_filename)
    print("Phraser loaded from file.")
except FileNotFoundError:
    print("Phraser not found. Creating a new one.")
    clean_sents = gbergSentBigram(gberg_sents)
    phraser = Phraser(Phrases(clean_sents))
    save_phraser(phraser, phraser_filename)
    print("Phraser saved to file.")


def get_frozen_phrases_items(frozen_phrases):
    return [(phrase, score)
            for phrase, score in frozen_phrases.phrasegrams.items()]


def select_next_word(next_words_with_score):
    word_scores = next_words_with_score[1::2]
    total_score = sum(word_scores)

    random_value = random.uniform(0, total_score)

    cumulative_score = 0
    selected_word = None

    for i in range(0, len(next_words_with_score), 2):
        word = next_words_with_score[i]
        score = next_words_with_score[i + 1]
        cumulative_score += score
        if cumulative_score >= random_value:
            selected_word = word
            break

    return selected_word


def possible_next_words(word, phraser):
    next_words_with_score = []
    for k, v in get_frozen_phrases_items(phraser):
        if k[:len(word) + 1] == word + "_":
            next_words_with_score.append(k[len(word):])
            next_words_with_score.append(v)
    return next_words_with_score


def predict_next_word(word, phraser):
    # step 1: get all second words for word with their score
    next_words_with_score = possible_next_words(word, phraser)
    next_word = select_next_word(next_words_with_score)
    if next_word != None:
        return next_word
    else:
        return "[END]"


def input_autocomplete():
    new_word = input(
        "Type a word or a sentence and the model will continue it: ")
    new_word = new_word.split(" ")[-1].lower()

    generated_text = new_word + " "

    if new_word != "exit" or new_word != "quit" or new_word != "q":

        while True:
            next_word = predict_next_word(new_word, phraser)
            if next_word == "[END]":
                print(f"new generated text: \n {generated_text}")
                input_autocomplete()
            elif "_" in next_word:
                if next_word[0] == "_":
                    next_word[0].replace("_", "")
                    word_list = next_word.split("_")
                    old_word_s = word_list[1:-1]
                    new_word = word_list[-1]
                    generated_text += list_to_string(
                        old_word_s) + new_word + " "
            else:
                if next_word[0] == "_":
                    next_word.replace("_", "")

                generated_text += next_word + " "
                new_word = next_word
    else:
        print("ended")


input_autocomplete()

# TODO: bei "don t" nicht nur "t" als nächstes Wort nehmen => weitergeführter Text
# evtl "english words with apostrophes" aus nltk finden und damit vergleichen