list = ["1", "sv", "yeet"]

next_word = "_for_i_am"


def listToString(s):
    str = ""
    for i in s:
        str += i + " "
        print(str)
    return str


if next_word[0] == "_":
    next_word[0].replace("_", "")
    word_list = next_word.split("_")
    old_word_s = word_list[1:-1]
    print(old_word_s)
    new_word = word_list[-1]
    print(listToString(old_word_s) + new_word + " ")
