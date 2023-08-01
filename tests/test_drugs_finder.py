'''
MIT License

Copyright (c) 2023 Fast Data Science Ltd (https://fastdatascience.com)

Maintainer: Thomas Wood

Tutorial at https://fastdatascience.com/faststylometry-python-library/

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

import unittest

from faststylometry.drugs_finder import find_drugs

class TestDrugsFinder(unittest.TestCase):

    def test_drugs_1(self):
        drugs = find_drugs("i bought some Sertraline".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Sertraline", drugs[0][0]['name'])

    def test_drugs_lowercase(self):
        drugs = find_drugs("i bought some sertraline".split(" "))

        self.assertEqual(0, len(drugs))

    def test_drugs_synonym(self):
        drugs = find_drugs("i bought some Zoloft".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Sertraline", drugs[0][0]['name'])

    def test_drugs_synonym_lc(self):
        drugs = find_drugs("i bought some zoloft".split(" "))

        self.assertEqual(0, len(drugs))

    def test_generic_lc(self):
        drugs = find_drugs("i bought some Rimonabant".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Rimonabant", drugs[0][0]['name'])

    def test_two_word_drug(self):
        drugs = find_drugs("i bought some Amphotericin B".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Amphotericin B", drugs[0][0]['name'])

    def test_hemlibra(self):
        drugs = find_drugs("i bought some HEMLIBRA".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Emicizumab", drugs[0][0]['name'])
