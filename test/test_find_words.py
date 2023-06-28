from naturallangprocessing.utils import find_words
from gensim.models.phrases import Phraser, Phrases


def test_list_to_string():
    list = ["1", "2", "hi", "349", "2"]
    print(find_words.list_to_string(list))
    assert find_words.list_to_string(
        list) == "1 2 hi 349 2 "  # needs a space at the end
    # only works if the list is 1d and contains only str


def test_get_frozen_phrases_items():
    pass


def test_select_next_word():
    pass  # since the outcome is random, the testing can not be applied here easily


def test_possible_next_words():
    pass


# since phrases uses a trained model it cannot be testet without using a preexisting model, which would be the same model it shoud be apllied to and as such the result would be the same and the testing is mostly useless
