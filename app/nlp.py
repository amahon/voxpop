


import csv

import nltk
from bs4 import BeautifulSoup
from bson.code import Code
from bson.objectid import ObjectId
from nltk.corpus import stopwords


AFFECTIVE_WORD_FILE = 'corpus/Ratings_Warriner_et_al.csv'

_affective_words = None

def load_affective_words():
    global _affective_words

    if not _affective_words:
        _affective_words = {}
        with open(AFFECTIVE_WORD_FILE, 'rb') as csvfile:
            word_reader = csv.DictReader(csvfile, delimiter=',', quotechar='|')
            for row in word_reader:
                _affective_words[row['Word']] = row

load_affective_words()

