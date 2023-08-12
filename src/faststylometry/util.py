'''
MIT License

Copyright (c) 2023 Fast Data Science Ltd (https://fastdatascience.com)

Maintainer: Thomas Wood

Tutorial at https://fastdatascience.com/fast-stylometry-python-library/

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

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
                text = text.strip()

                if len(text) == 0:
                    print ("Warning! Empty document: ", filename)
                    print ("Skipping...")
                    continue
                author, book = re.split("_-_", re.sub(r'\.txt', '', filename), maxsplit = 1)

                corpus.add_book(author, book, text)
    return corpus
