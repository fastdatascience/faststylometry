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

import operator
import re
from collections import Counter

import numpy as np
import pandas as pd
from faststylometry import Corpus


def get_top_tokens(corpus: Corpus, vocab_size: int, words_to_exclude: set, tok_match_pattern: str) -> list:
    """
    Identify the n highest ranking tokens in the corpus.

    :param corpus: The corpus to look for the commonest words in. The corpus must be tokenised.
    :param vocab_size: The n most common words in the corpus will be used.
    :return: A list of the n most common tokens in the corpus.
    """

    assert (len(corpus.tokens) > 0)  # you should have tokenised the corpus.

    token_freqs = Counter()
    for token_seq in corpus.tokens:
        for token in token_seq:
            if token not in words_to_exclude:
                token_freqs[token] += 1

    if tok_match_pattern:
        re_alpha = re.compile(tok_match_pattern)
        for tok in list(token_freqs.keys()):
            if not re_alpha.match(tok):
                del token_freqs[tok]

    corpus.top_tokens = [tok for tok, freq in
                         sorted(token_freqs.items(), key=operator.itemgetter(1), reverse=True)[:vocab_size]]
    corpus.top_tokens_set = set(corpus.top_tokens)

    return corpus.top_tokens


def set_top_tokens(corpus: Corpus, top_tokens: list):
    """
    Use a predefined set of tokens to calculate Burrows' Delta on this corpus.
    You would do this, if the corpus is a test corpus, and your model has been trained on a training corpus.

    :param corpus: the corpus you want to set the top tokens for.
    :param top_tokens: the top tokens which you have calculated elsewhere, e.g. from a training corpus.
    """
    corpus.top_tokens = top_tokens
    corpus.top_tokens_set = set(top_tokens)


def get_token_counts(corpus: Corpus):
    """
    Calculate the number of times each of the top tokens occurs in the corpus, and store this data in two dataframes in the corpus.

    :param corpus: The corpus to run the operation on and store the result in.
    """
    token_counts = np.zeros((len(corpus.authors), len(corpus.top_tokens)))

    total_token_counts = np.asarray([len(tokens) for tokens in corpus.tokens])

    for idx in range(len(corpus.authors)):

        this_work_token_counts = Counter()
        for tok in corpus.tokens[idx]:
            if tok in corpus.top_tokens_set:
                this_work_token_counts[tok] += 1

        for tok_idx, tok in enumerate(corpus.top_tokens):
            token_counts[idx, tok_idx] = this_work_token_counts.get(tok, 0)

    corpus.token_counts = token_counts
    corpus.total_token_counts = total_token_counts
    corpus.author_book_combinations = [a + " - " + b for a, b in zip(corpus.authors, corpus.books)]

    ## OLD LOGIC
    # corpus.df_token_counts = pd.DataFrame(token_counts, columns=corpus.top_tokens)
    #
    # corpus.df_token_counts["author"] = corpus.authors
    # author_book_combinations = [a + " - " + b for a, b in zip(corpus.authors, corpus.books)]
    # corpus.df_token_counts["author_book"] = author_book_combinations
    #
    # corpus.df_total_token_counts = pd.DataFrame({"count": total_token_counts})
    # corpus.df_total_token_counts["author"] = corpus.authors
    # corpus.df_total_token_counts["author_book"] = author_book_combinations


def get_token_counts_by_author(corpus: Corpus):
    """
    Group the token counts across works by the same author, so we have a token count for each author.
    :param corpus:  The corpus to run the operation on and store the result in.
    """
    corpus.all_unique_authors = sorted(set(corpus.authors))
    corpus.author_to_author_id = dict([(author, idx) for idx, author in enumerate(corpus.all_unique_authors)])
    corpus.author_ids = [corpus.author_to_author_id[author_name] for author_name in corpus.authors]

    corpus.token_counts_by_author = np.stack(
        [np.bincount(corpus.author_ids, corpus.token_counts[:, i]) for i in range(len(corpus.top_tokens))])
    corpus.total_token_counts_by_author = np.bincount(corpus.author_ids, corpus.total_token_counts)

    # OLD LOGIC
    # corpus.df_token_counts_by_author = corpus.df_token_counts.groupby("author").sum()
    # corpus.df_total_token_counts_by_author = corpus.df_total_token_counts.groupby("author").sum()


def get_token_counts_by_author_and_book(corpus: Corpus):
    """
    Group the token counts across works by the same author and book, so we have a token count for each book.
    :param corpus:  The corpus to run the operation on and store the result in.
    """
    corpus.all_unique_authors = sorted(set(corpus.author_book_combinations))
    corpus.author_to_author_id = dict([(author, idx) for idx, author in enumerate(corpus.all_unique_authors)])
    corpus.author_ids = [corpus.author_to_author_id[author_name] for author_name in corpus.author_book_combinations]

    corpus.token_counts_by_author = np.stack(
        [np.bincount(corpus.author_ids, corpus.token_counts[:, i]) for i in range(len(corpus.top_tokens))])
    corpus.total_token_counts_by_author = np.bincount(corpus.author_ids, corpus.total_token_counts)

    # OLD LOGIC
    # corpus.df_token_counts_by_author = corpus.df_token_counts.groupby("author_book").sum()
    # corpus.df_total_token_counts_by_author = corpus.df_total_token_counts.groupby("author_book").sum()


def get_token_proportions(corpus: Corpus):
    """
    Calculate the fraction of words in each author's subcorpus which are equal to each word in our vocabulary.
    :param corpus:  The corpus to run the operation on and store the result in.
    """

    corpus.token_proportions = corpus.token_counts_by_author / corpus.total_token_counts_by_author


def get_author_z_scores(test_corpus: Corpus, train_corpus: Corpus = None) -> pd.DataFrame:
    """
    Calculate the Z-score relating the test corpus to each author's subcorpus in the training corpus.
    :param test_corpus:  The corpus to run the operation on and store the result in.
    :param train_corpus: The training corpus with a number of authors' subcorpora, which will be compared to the test corpus.
    :return: A dataframe of Z-scores for each author in the training corpus.
    """
    if not train_corpus:
        train_corpus = test_corpus
    test_corpus.author_z_scores = np.zeros(test_corpus.token_proportions.shape)
    for i in range(test_corpus.author_z_scores.shape[0]):
        test_corpus.author_z_scores[i, :] = (test_corpus.token_proportions[i, :] - train_corpus.token_proportions[
            i].mean()) / train_corpus.token_proportions[i].std(ddof=1)

    return test_corpus.author_z_scores


def calculate_difference_from_train_corpus(test_corpus, train_corpus=None):
    """
    Calculate the difference between the Z-scores of the test corpus and the Z-scores of each author in the training corpus.
    :param test_corpus:  The corpus to run the operation on and store the result in.
    :param train_corpus: The training corpus with a number of authors' subcorpora, which will be compared to the test corpus.
    """
    test_corpus.difference_matrices = [None] * len(test_corpus.all_unique_authors)
    for test_author_id in range(len(test_corpus.all_unique_authors)):
        test_corpus.difference_matrices[test_author_id] = np.zeros(train_corpus.author_z_scores.shape)
        for col in range(train_corpus.author_z_scores.shape[1]):
            test_corpus.difference_matrices[test_author_id][:, col] = train_corpus.author_z_scores[:,
                                                                      col] - test_corpus.author_z_scores[:,
                                                                             test_author_id]

    test_corpus.difference_matrix = np.stack(test_corpus.difference_matrices)


def calculate_burrows_delta(train_corpus: Corpus, test_corpus: Corpus, vocab_size: int = 50, words_to_exclude: set = {},
                            tok_match_pattern: str = r'^[a-z][a-z]+$') -> pd.DataFrame:
    """
    Calculate the Burrows' Delta statistic for the test corpus vs every author's subcorpus in the training corpus.
    :param train_corpus: A corpus of known authors, which we will use as a benchmark to compare to the test corpus by an unknown author.
    :param test_corpus: The corpus by an unknown author.
    :param vocab_size: We will take the top n tokens from the training corpus and use as the vocabulary for the model. Normally 50-100 make sensible values.
    :return: A DataFrame of Burrows' Delta values for each author in the training corpus.
    """
    get_top_tokens(train_corpus, vocab_size, words_to_exclude, tok_match_pattern)
    get_token_counts(train_corpus)
    get_token_counts_by_author(train_corpus)
    get_token_proportions(train_corpus)
    get_author_z_scores(train_corpus)

    set_top_tokens(test_corpus, train_corpus.top_tokens)
    get_token_counts(test_corpus)
    get_token_counts_by_author_and_book(test_corpus)
    get_token_proportions(test_corpus)
    get_author_z_scores(test_corpus, train_corpus)

    calculate_difference_from_train_corpus(test_corpus, train_corpus)

    deltas = np.mean(np.abs(test_corpus.difference_matrix), axis=1).T

    df_delta = pd.DataFrame(deltas, columns=test_corpus.all_unique_authors, index=train_corpus.all_unique_authors)

    return df_delta
