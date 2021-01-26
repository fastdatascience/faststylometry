import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

from faststylometry.burrows_delta import calculate_burrows_delta
from faststylometry.corpus import Corpus


def every_item_but_one(l, idx):
    return [item for i, item in enumerate(l) if i != idx]


def get_calibration_curve(corpus):
    ground_truths = []

    delta_values = []

    num_books = len(corpus.authors)

    for i in range(num_books):
        tmp_train_corpus = Corpus(every_item_but_one(corpus.authors, i), every_item_but_one(corpus.books, i),
                                  every_item_but_one(corpus.tokens, i))
        tmp_test_corpus = Corpus(corpus.authors[i:i + 1], corpus.books[i:i + 1], corpus.tokens[i:i + 1])

        true_author = tmp_test_corpus.authors[0]

        burrows_delta = calculate_burrows_delta(tmp_train_corpus, tmp_test_corpus)

        ground_truths.extend(list(burrows_delta.index == true_author))
        delta_values.extend(list(burrows_delta.delta))

    return np.asarray(ground_truths), np.asarray(delta_values)


def calibrate(corpus, model=LogisticRegression(class_weight="balanced")):
    ground_truths, delta_values = get_calibration_curve(corpus)

    model.fit(np.reshape(delta_values, (-1, 1)), ground_truths)

    corpus.probability_model = model


def predict_proba(train_corpus, test_corpus):
    delta = calculate_burrows_delta(train_corpus, test_corpus)

    values = train_corpus.probability_model.predict_proba(np.reshape(delta.to_numpy(), (-1, 1)))[:, 1]

    return pd.DataFrame({"author": delta.index, "proba": values}).set_index("author")
