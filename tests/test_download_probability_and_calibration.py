'''
MIT License

Copyright (c) 2023 Fast Data Science Ltd (https://fastdatascience.com)

Maintainer: Thomas Wood

Tutorial at https://fastdatascience.com/drug-named-entity-recognition-python-library/

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
import unittest
import numpy as np
from faststylometry import download_examples
from faststylometry import load_corpus_from_folder
from faststylometry import predict_proba, calibrate
from faststylometry import tokenise_remove_pronouns_en



class TestFastStylometry(unittest.TestCase):

    def setUp(self):
        self.data_path = download_examples()

        self.train_corpus = load_corpus_from_folder("data/train")

        self.train_corpus.tokenise(tokenise_remove_pronouns_en)

        # Load Sense and Sensibility, written by Jane Austen (marked as "janedoe")
        # and Villette, written by Charlotte Bronte (marked as "currerbell", Bronte's real pseudonym)

        self.test_corpus = load_corpus_from_folder("data/test", pattern=None)
        # You can set pattern to a string value to just load a subset of the corpus.

        self.test_corpus.tokenise(tokenise_remove_pronouns_en)

        calibrate(self.train_corpus)

    def test_download_examples(self):
        files_downloaded = os.listdir(self.data_path)

        self.assertLess(0, len(files_downloaded))


    def test_all_calibrated_probabilities_within_sensible_range(self):
        proba_output = predict_proba(self.train_corpus, self.test_corpus)

        for row_no in range(len(proba_output)):
            for col in proba_output.columns:
                print (f"Checking column {col} row {row_no}")
                self.assertGreater(1, proba_output[col].iloc[row_no])
                self.assertLess(0, proba_output[col].iloc[row_no])

    def test_calibration_curve(self):
        probability_curve = self.train_corpus.probability_model.predict_proba(np.asarray([[0], [1], [2], [3], [4], [5]]))[:,1]
        self.assertLess(0.9, probability_curve[0])
        self.assertGreater(0.01, probability_curve[4])


if __name__ == "__main__":
    unittest.main()