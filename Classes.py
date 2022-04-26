from utils import hello, input_word, selection_of_words
# import requests
class BasicWord:

    def __init__(self, word, sub_word):
        self.word = word
        self.sub_word = sub_word

    def has_subwords(self, candidate):
        return candidate.lower() in self.sub_word

    def count_subwords(self, subwords):
        return len(subwords)

    def __repr__(self):
        return f"Слово '{self.word}' содержит {len(self.sub_word)} подслов"


class Gamers:

    def __init__(self, name, password, words):
        self.name = name
        self.password = password
        self.words = words


