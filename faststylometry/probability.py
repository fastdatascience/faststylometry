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

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.linear_model import LogisticRegression

from faststylometry.burrows_delta import calculate_burrows_delta
from faststylometry.corpus import Corpus


def every_item_but_one(l: list, idx: int) -> list:
    """
    Returns every item in the list except for the one at index idx.
    :param l: a list to process.
    :param idx: the index to be excluded from the list.
    :return: the list l minus the item at index idx.
    """
    return [item for i, item in enumerate(l) if i != idx]


def get_calibration_curve(corpus: Corpus) -> tuple:
    """
    Calculates the probability calibration curve of the Burrows' Delta calculation on the train corpus, using a cross-validation technique.
    :param corpus: the corpus for which we desire a probability calibration curve.
    :return: two arrays, an array of ground truths (0: different authors, 1: same author), and of Burrows' delta values. These can be used to calibrate a model such as logistic regression, or to generate a ROC curve.
    """
    ground_truths = []

    delta_values = []

    num_books = len(corpus.authors)

    for i in range(num_books):
        tmp_train_corpus = Corpus(every_item_but_one(corpus.authors, i), every_item_but_one(corpus.books, i),
                                  every_item_but_one(corpus.tokens, i))
        tmp_test_corpus = Corpus(corpus.authors[i:i + 1], corpus.books[i:i + 1], corpus.tokens[i:i + 1])

        true_author = tmp_test_corpus.authors[0]

        df_delta = calculate_burrows_delta(tmp_train_corpus, tmp_test_corpus)

        ground_truths.extend(list(df_delta.index == true_author))
        delta_values.extend(list(df_delta.iloc[:, 0]))

    return np.asarray(ground_truths), np.asarray(delta_values)


def calibrate(corpus: Corpus, model: BaseEstimator = LogisticRegression(class_weight="balanced")):
    ground_truths, delta_values = get_calibration_curve(corpus)

    model.fit(np.reshape(delta_values, (-1, 1)), ground_truths)

    corpus.probability_model = model


def predict_proba(train_corpus: Corpus, test_corpus: Corpus) -> pd.DataFrame:
    """
    Returns the probability that the test corpus is by the same author as the training corpus.

    :param train_corpus: The corpus to serve as a baseline for the word frequency calculations.
    :param test_corpus: The corpus to compare it with.
    :return: The probability according to the calibrated model, that the test corpus was by the same author as the train corpus.
    """
    df_delta = calculate_burrows_delta(train_corpus, test_corpus)

    df_probas = pd.DataFrame()
    for test_author_idx in range(df_delta.shape[1]):
        values = train_corpus.probability_model.predict_proba(
            np.reshape(list(df_delta.iloc[:, test_author_idx]), (-1, 1)))[:,
                 1]
        df_probas[df_delta.columns[test_author_idx]] = list(values)

    df_probas.index = df_delta.index

    return df_probas
