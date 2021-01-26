import re
import operator
import pandas as pd
import numpy as np
from collections import Counter
from faststylometry.corpus import Corpus
import os


def load_corpus_from_folder(folder, pattern=None):
    corpus = Corpus()
    for root, _, files in os.walk(folder):
        for filename in files:
            if pattern is not None and not pattern in filename:
                continue
            if filename.endswith(".txt") and "_" in filename:
                with open(os.path.join(root, filename), "r", encoding="utf-8") as f:
                    text = f.read()
                author, book = re.split("_-_", re.sub(r'\.txt', '', filename))

                corpus.add_book(author, book, text)
    return corpus
