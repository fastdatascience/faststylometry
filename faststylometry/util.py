import os
import re

from faststylometry.corpus import Corpus


def load_corpus_from_folder(folder: str, pattern: str = None) -> Corpus:
    """
    Iterates over the .txt files in a folder and adds their contents to the corpus.

    Assumes that files are of the format [author]_-_[title].txt.

    :param folder: the folder ony our local system to iterate over.
    :param pattern: an optional filter to apply to the filenames.
    :return: a corpus of the files found.
    """
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
