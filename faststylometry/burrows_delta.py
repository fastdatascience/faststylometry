import operator
from collections import Counter

import numpy as np
import pandas as pd

from faststylometry import Corpus


def get_top_tokens(corpus: Corpus, vocab_size: int) -> list:
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
            token_freqs[token] += 1

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

    corpus.df_token_counts = pd.DataFrame(token_counts, columns=corpus.top_tokens)

    corpus.df_token_counts["author"] = corpus.authors
    author_book_combinations = [a + " - " + b for a, b in zip(corpus.authors, corpus.books)]
    corpus.df_token_counts["author_book"] = author_book_combinations

    corpus.df_total_token_counts = pd.DataFrame({"count": total_token_counts})
    corpus.df_total_token_counts["author"] = corpus.authors
    corpus.df_total_token_counts["author_book"] = author_book_combinations


def get_token_counts_by_author(corpus: Corpus):
    """
    Group the token counts across works by the same author, so we have a token count for each author.
    :param corpus:  The corpus to run the operation on and store the result in.
    """
    corpus.df_token_counts_by_author = corpus.df_token_counts.groupby("author").sum()
    corpus.df_total_token_counts_by_author = corpus.df_total_token_counts.groupby("author").sum()


def get_token_counts_by_author_and_book(corpus: Corpus):
    """
    Group the token counts across works by the same author and book, so we have a token count for each book.
    :param corpus:  The corpus to run the operation on and store the result in.
    """
    corpus.df_token_counts_by_author = corpus.df_token_counts.groupby("author_book").sum()
    corpus.df_total_token_counts_by_author = corpus.df_total_token_counts.groupby("author_book").sum()


def get_token_proportions(corpus: Corpus):
    """
    Calculate the fraction of words in each author's subcorpus which are equal to each word in our vocabulary.
    :param corpus:  The corpus to run the operation on and store the result in.
    """
    token_proportions = corpus.df_token_counts_by_author.to_numpy() / corpus.df_total_token_counts_by_author.to_numpy()

    corpus.df_token_proportions = pd.DataFrame(token_proportions, columns=corpus.top_tokens,
                                               index=corpus.df_token_counts_by_author.index)


def get_author_z_scores(test_corpus: Corpus, training_corpus: Corpus = None) -> pd.DataFrame:
    """
    Calculate the Z-score relating the test corpus to each author's subcorpus in the training corpus.
    :param test_corpus:  The corpus to run the operation on and store the result in.
    :param training_corpus: The training corpus with a number of authors' subcorpora, which will be compared to the test corpus.
    :return: A dataframe of Z-scores for each author in the training corpus.
    """
    if not training_corpus:
        training_corpus = test_corpus
    test_corpus.df_author_z_scores = (
                                             test_corpus.df_token_proportions - training_corpus.df_token_proportions.mean()) / training_corpus.df_token_proportions.std()

    return test_corpus.df_author_z_scores


def calculate_difference_from_train_corpus(test_corpus, train_corpus=None):
    """
    Calculate the difference between the Z-scores of the test corpus and the Z-scores of each author in the training corpus.
    :param test_corpus:  The corpus to run the operation on and store the result in.
    :param train_corpus: The training corpus with a number of authors' subcorpora, which will be compared to the test corpus.
    """
    test_corpus.df_difference = [None] * len(test_corpus.df_author_z_scores)
    for i in range(len(test_corpus.df_author_z_scores)):
        test_corpus.df_difference[i] = train_corpus.df_author_z_scores.sub(test_corpus.df_author_z_scores.iloc[i, :])


def calculate_burrows_delta(train_corpus: Corpus, test_corpus: Corpus, vocab_size: int = 50) -> pd.DataFrame:
    """
    Calculate the Burrows' Delta statistic for the test corpus vs every author's subcorpus in the training corpus.
    :param train_corpus: A corpus of known authors, which we will use as a benchmark to compare to the test corpus by an unknown author.
    :param test_corpus: The corpus by an unknown author.
    :param vocab_size: We will take the top n tokens from the training corpus and use as the vocabulary for the model. Normally 50-100 make sensible values.
    :return: A DataFrame of Burrows' Delta values for each author in the training corpus.
    """
    get_top_tokens(train_corpus, vocab_size)
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

    deltas = {}
    for test_author_idx in range(len(test_corpus.df_author_z_scores)):
        deltas[test_corpus.df_author_z_scores.index[test_author_idx]] = test_corpus.df_difference[
            test_author_idx].abs().mean(axis=1)

    df_delta = pd.concat(deltas, axis=1)

    return df_delta
