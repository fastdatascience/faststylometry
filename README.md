![Fast Data Science logo](https://raw.githubusercontent.com/fastdatascience/brand/main/primary_logo.svg)

<a href="https://fastdatascience.com"><span align="left">🌐 fastdatascience.com</span></a>
<a href="https://www.linkedin.com/company/fastdatascience/"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/linkedin.svg" alt="Fast Data Science | LinkedIn" width="21px"/></a>
<a href="https://twitter.com/fastdatascienc1"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/x.svg" alt="Fast Data Science | X" width="21px"/></a>
<a href="https://www.instagram.com/fastdatascience/"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/instagram.svg" alt="Fast Data Science | Instagram" width="21px"/></a>
<a href="https://www.facebook.com/fastdatascienceltd"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/fb.svg" alt="Fast Data Science | Facebook" width="21px"/></a>
<a href="https://www.youtube.com/channel/UCLPrDH7SoRT55F6i50xMg5g"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/yt.svg" alt="Fast Data Science | YouTube" width="21px"/></a>

# Fast Stylometry Python library

<!-- badges: start -->
![my badge](https://badgen.net/badge/Status/In%20Development/orange)

[![PyPI package](https://img.shields.io/badge/pip%20install-faststylometry-brightgreen)](https://pypi.org/project/faststylometry/) [![version number](https://img.shields.io/pypi/v/faststylometry?color=green&label=version)](https://github.com/fastdatascience/faststylometry/releases) [![License](https://img.shields.io/github/license/fastdatascience/faststylometry)](https://github.com/fastdatascience/faststylometry/blob/main/LICENSE)

<!-- badges: end -->

# Fast Stylometry - Burrows Delta

Developed by Fast Data Science, https://fastdatascience.com

Source code at https://github.com/fastdatascience/faststylometry

Tutorial at https://fastdatascience.com/fast-stylometry-python-library/

Python library for calculating the Burrows Delta.

Burrows' Delta is an algorithm for comparing the similarity of the writing styles of documents, known as [forensic stylometry](https://fastdatascience.com/how-you-can-identify-the-author-of-a-document/).

* [A useful explanation of the maths and thinking behind Burrows' Delta and how it works](https://programminghistorian.org/en/lessons/introduction-to-stylometry-with-python#third-stylometric-test-john-burrows-delta-method-advanced)


# Installing Fast Stylometry Python package

You can install from [PyPI](https://pypi.org/project/faststylometry).

```
pip install faststylometry
```



# Usage examples

Demonstration of Burrows' Delta on a small corpus downloaded from Project Gutenberg.

We will test the Burrows' Delta code on two "unknown" texts: Sense and Sensibility by Jane Austen, and Villette by Charlotte Bronte. Both authors are in our training corpus.

You can get the training corpus by cloning https://github.com/woodthom2/faststylometry, the data is in faststylometry/data.

## Create a corpus

To create a corpus and add books, the pattern is as follows:

```
corpus = Corpus()
corpus.add_book("Jane Austen", "Pride and Prejudice", [whole book text])
```

Here is the pattern for creating a corpus and adding books from a directory on your system. You can also use the method ```util.load_corpus_from_folder(folder, pattern)```.

```
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
```

## Example 1

Load a corpus and calculate Burrows' Delta

```
from faststylometry.util import load_corpus_from_folder
from faststylometry.en import tokenise_remove_pronouns_en
from faststylometry.burrows_delta import calculate_burrows_delta

train_corpus = load_corpus_from_folder("faststylometry/data/train")

train_corpus.tokenise(tokenise_remove_pronouns_en)

test_corpus_sense_and_sensibility = load_corpus_from_folder("faststylometry/data/test", pattern="sense")

test_corpus_sense_and_sensibility.tokenise(tokenise_remove_pronouns_en)

calculate_burrows_delta(train_corpus, test_corpus_sense_and_sensibility)
```

returns a Pandas dataframe of Burrows' Delta scores

## Example 2

Using the probability calibration functionality, you can calculate the probability of two books being by the same author.

```
from faststylometry.probability import predict_proba, calibrate
calibrate(train_corpus)
predict_proba(train_corpus, test_corpus_sense_and_sensibility)
```

outputs a Pandas dataframe of probabilities.

# Who to contact

Thomas Wood at [Fast Data Science](https://fastdatascience.com)

## Contributing to the project

If you'd like to contribute to this project, you can contact us at https://fastdatascience.com/ or make a pull request on our [Github repository](https://github.com/fastdatascience/faststylometry). You can also [raise an issue](https://github.com/fastdatascience/faststylometry/issues). 

## Developing the library

### Automated tests

Test code is in **tests/** folder using [unittest](https://docs.python.org/3/library/unittest.html).

The testing tool `tox` is used in the automation with GitHub Actions CI/CD.

### Use tox locally

Install tox and run it:

```
pip install tox
tox
```

In our configuration, tox runs a check of source distribution using [check-manifest](https://pypi.org/project/check-manifest/) (which requires your repo to be git-initialized (`git init`) and added (`git add .`) at least), setuptools's check, and unit tests using pytest. You don't need to install check-manifest and pytest though, tox will install them in a separate environment.

The automated tests are run against several Python versions, but on your machine, you might be using only one version of Python, if that is Python 3.9, then run:

```
tox -e py39
```

Thanks to GitHub Actions' automated process, you don't need to generate distribution files locally. But if you insist, click to read the "Generate distribution files" section.

### Continuous integration/deployment to PyPI

This package is based on the template https://pypi.org/project/example-pypi-package/

This package

- uses GitHub Actions for both testing and publishing
- is tested when pushing `master` or `main` branch, and is published when create a release
- includes test files in the source distribution
- uses **setup.cfg** for [version single-sourcing](https://packaging.python.org/guides/single-sourcing-package-version/) (setuptools 46.4.0+)

## Re-releasing the package manually

The code to re-release Harmony on PyPI is as follows:

```
source activate py311
pip install twine
rm -rf dist
python setup.py sdist
twine upload dist/*
```

## Who worked on the Fast Stylometry library?

The tool was developed:

* Thomas Wood ([Fast Data Science](https://fastdatascience.com))

## License of Fast Stylometry library

MIT License. Copyright (c) 2023 [Fast Data Science](https://fastdatascience.com)

## Citing the Fast Stylometry library

Wood, T.A., Fast Stylometry [Computer software], Version 1.0.2, accessed at [https://fastdatascience.com/fast-stylometry-python-library](https://fastdatascience.com/fast-stylometry-python-library), Fast Data Science Ltd (2023)

```
@unpublished{faststylometry,
    AUTHOR = {Wood, T.A.},
    TITLE  = {Fast Stylometry (Computer software), Version 1.0.2},
    YEAR   = {2023},
    Note   = {To appear},
}
```
