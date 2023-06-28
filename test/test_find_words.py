from naturallangprocessing.utils import find_words 
from gensim.models.phrases import Phraser, Phrases

def test_list_to_string():
    list = ["1",2,"hi",349,[2]]
    print(find_words.list_to_string(list))
    assert find_words.list_to_string(list) == "1 2 hi 349 2"
    