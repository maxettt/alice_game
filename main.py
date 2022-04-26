import requests
import json
from operator import itemgetter
from utils import *

# new comment
name = hello()
word = input_word()
words = selection_of_words(word)
table = open_json()
add_word_in_table(word, table)
table = open_json()
check_word(name, word, table)