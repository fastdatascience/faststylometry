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

import re

is_number_pattern = re.compile(r'.*\d.*')

re_words = re.compile(r"\w+")

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


def tokenise_remove_pronouns_en(text: str) -> list:
    """
    Tokenise a sentence according to English rules, and remove all pronouns.
    Remove all apostrophes since words like don't etc can be written in nonstandard ways.

    :param text: the original sentence.
    :return: all non-pronoun tokens.
    """
    text_normalised = re.sub("['’]", "", text.lower())
    tokens = [tok for tok in re_words.findall(text_normalised) if not is_number_pattern.match(tok)]

    tokens_without_stopwords = [tok for tok in tokens if tok not in stopwords]

    return tokens_without_stopwords
