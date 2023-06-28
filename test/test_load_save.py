from naturallangprocessing.utils import load_save, bigrams


def test_load_create_phraser():
    file = bigrams.gberg_sent_bigram(bigrams.gberg_sents)
    phraser = load_save.create_phraser(file)
    assert load_save.load_or_create_phraser(file) == phraser