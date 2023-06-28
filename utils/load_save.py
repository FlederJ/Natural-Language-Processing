from utils import bigrams
import pickle
from gensim.models.phrases import Phraser, Phrases


def save_phraser(phraser, filename):
    with open(filename, 'wb') as f:
        pickle.dump(phraser, f)


def load_phraser(filename):
    with open(filename, 'rb') as f:
        phraser = pickle.load(f)
    return phraser


def create_phraser(file):
    clean_sents = bigrams.gbergSentBigram(file)
    return Phraser(Phrases(clean_sents))


def load_or_create_phraser(file):
    phraser_filename = 'test/files/phraser.pkl'
    try:
        phraser = load_phraser(phraser_filename)
        print("Phraser loaded from file.")
    except FileNotFoundError:
        print("Phraser not found. Creating a new one.")
        phraser = create_phraser(file)
        save_phraser(phraser, phraser_filename)
        print("Phraser saved to file.")
