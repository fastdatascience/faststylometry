import re

import nltk

is_alpha_pattern = re.compile(r'^\w+$')

# pronouns
stopwords = {"he",
             "her",
             "hers",
             "herself",
             "him",
             "himself",
             "his",
             "i",
             "me",
             "mine",
             "my",
             "myself",
             "our",
             "ours",
             "ourselves",
             "she",
             "thee",
             "their",
             "them",
             "themselves",
             "they",
             "thou",
             "thy",
             "thyself",
             "us",
             "we",
             "ye",
             "you",
             "your",
             "yours",
             "yourself", }


def tokenise_remove_pronouns_en(text):
    tokens = [tok for tok in nltk.word_tokenize(text.lower()) if is_alpha_pattern.match(tok)]

    tokens_without_stopwords = [tok for tok in tokens if tok not in stopwords]

    return tokens_without_stopwords
