import operator
from collections import Counter

import numpy as np
import pandas as pd


def get_top_tokens(self):
    token_freqs = Counter()
    for token_seq in self.tokens:
        for token in token_seq:
            token_freqs[token] += 1

    self.top_tokens = [tok for tok, freq in sorted(token_freqs.items(), key=operator.itemgetter(1), reverse=True)[:50]]
    self.top_tokens_set = set(self.top_tokens)

    return self.top_tokens


def set_top_tokens(self, top_tokens):
    self.top_tokens = top_tokens
    self.top_tokens_set = set(top_tokens)

    return self.top_tokens


def get_token_counts(self):
    token_counts = np.zeros((len(self.authors), len(self.top_tokens)))

    total_token_counts = np.asarray([len(tokens) for tokens in self.tokens])

    for idx in range(len(self.authors)):

        this_work_token_counts = Counter()
        for tok in self.tokens[idx]:
            if tok in self.top_tokens_set:
                this_work_token_counts[tok] += 1

        for tok_idx, tok in enumerate(self.top_tokens):
            token_counts[idx, tok_idx] = this_work_token_counts.get(tok, 0)

    self.df_token_counts = pd.DataFrame(token_counts, columns=self.top_tokens)
    self.df_token_counts["author"] = self.authors

    self.df_total_token_counts = pd.DataFrame({"count": total_token_counts})
    self.df_total_token_counts["author"] = self.authors


def get_token_counts_by_author(self):
    self.df_token_counts_by_author = self.df_token_counts.groupby("author").sum()
    self.df_total_token_counts_by_author = self.df_total_token_counts.groupby("author").sum()


def get_token_proportions(self):
    token_proportions = self.df_token_counts_by_author.to_numpy() / self.df_total_token_counts_by_author.to_numpy()

    self.df_token_proportions = pd.DataFrame(token_proportions, columns=self.top_tokens,
                                             index=self.df_token_counts_by_author.index)


def get_author_z_scores(self, training_corpus=None):
    if not training_corpus:
        training_corpus = self
    self.df_author_z_scores = (
                                      self.df_token_proportions - training_corpus.df_token_proportions.mean()) / training_corpus.df_token_proportions.std()

    return self.df_author_z_scores


def calculate_difference_from_train_corpus(self, train_corpus=None):
    # self is the test corpus
    self.df_difference = train_corpus.df_author_z_scores.sub(self.df_author_z_scores.iloc[0, :])


def calculate_burrows_delta(train_corpus, test_corpus):
    get_top_tokens(train_corpus)
    get_token_counts(train_corpus)
    get_token_counts_by_author(train_corpus)
    get_token_proportions(train_corpus)
    get_author_z_scores(train_corpus)

    set_top_tokens(test_corpus, train_corpus.top_tokens)
    get_token_counts(test_corpus)
    get_token_counts_by_author(test_corpus)
    get_token_proportions(test_corpus)
    get_author_z_scores(test_corpus, train_corpus)

    calculate_difference_from_train_corpus(test_corpus, train_corpus)

    series_delta = test_corpus.df_difference.abs().mean(axis=1)

    df_delta = series_delta.to_frame().rename({0: "delta"}, axis=1)

    return df_delta
