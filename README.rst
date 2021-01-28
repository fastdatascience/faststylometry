Burrows Delta
=============

By Thomas Wood, https://freelancedatascientist.net, Fast Data Science https://fastdatascience.com


Source code at https://github.com/woodthom2/faststylometry

Tutorial at https://freelancedatascientist.net/fast-stylometry-tutorial/

Python library for calculating the Burrows Delta.

Burrows' Delta is an algorithm for comparing the similarity of the writing styles of documents, known as forensic stylometry https://fastdatascience.com/how-you-can-identify-the-author-of-a-document

* A useful explanation of the maths and thinking behind Burrows' Delta and how it works: https://programminghistorian.org/en/lessons/introduction-to-stylometry-with-python#third-stylometric-test-john-burrows-delta-method-advanced



Requirements
============

Python 3.6 and above

Installation
============

::

  pip install faststylometry

Usage examples
==============

Demonstration of Burrows' Delta on a small corpus downloaded from Project Gutenberg.

We will test the Burrows' Delta code on two "unknown" texts: Sense and Sensibility by Jane Austen, and Villette by Charlotte Bronte. Both authors are in our training corpus.

You can get the training corpus by cloning https://github.com/woodthom2/faststylometry, the data is in faststylometry/data.

To create a corpus and add books, the pattern is as follows:

.. code:: python

  corpus = Corpus()
  corpus.add_book("Jane Austen", "Pride and Prejudice", [whole book text])

Here is the pattern for creating a corpus and adding books from a directory on your system. You can also use the method util.load_corpus_from_folder(folder, pattern).


.. code:: python

  import os
  import re

  from faststylometry.corpus import Corpus

  corpus = Corpus()
  for root, _, files in os.walk(folder):
      for filename in files:
          if filename.endswith(".txt") and "_" in filename:
              with open(os.path.join(root, filename), "r", encoding="utf-8") as f:
                  text = f.read()
              author, book = re.split("_-_", re.sub(r'\.txt', '', filename))

              corpus.add_book(author, book, text)

If you have books of different lengths in your corpus, you may want to split it into segments of the same length. The following command will split all

.. code:: python

  split_corpus = corpus.split(1000)


Example 1

Load a corpus and calculate Burrows' Delta

.. code:: python

  from faststylometry.util import load_corpus_from_folder
  from faststylometry.en import tokenise_remove_pronouns_en
  from faststylometry.burrows_delta import calculate_burrows_delta

  train_corpus = load_corpus_from_folder("faststylometry/data/train")

  train_corpus.tokenise(tokenise_remove_pronouns_en)

  test_corpus_sense_and_sensibility = load_corpus_from_folder("faststylometry/data/test", pattern="sense")

  test_corpus_sense_and_sensibility.tokenise(tokenise_remove_pronouns_en)

  calculate_burrows_delta(train_corpus, test_corpus_sense_and_sensibility)

returns a Pandas dataframe of Burrows' Delta scores

Example 2

Using the probability calibration functionality, you can calculate the probability of two books being by the same author.

.. code:: python

  from faststylometry.probability import predict_proba, calibrate
  calibrate(train_corpus)
  predict_proba(train_corpus, test_corpus_sense_and_sensibility)

outputs a Pandas dataframe of probabilities.

Who to contact
==============

Thomas Wood at Fast Data Science https://fastdatascience.com

