import random


def list_to_string(s):
    str = ""
    for i in s:
        str += i + " "
    return str


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


def input_autocomplete(phraser):
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
