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

class Corpus:

    def __init__(self, authors: list = None, books: list = None, tokens: list = None):
        """
        Create a new corpus object, which is empty by default, but which can be initialised optionally with a set of books.
        :param authors: A list of strings representing author names. If a set of books are being used to initialise the corpus, len(authors) must equal len(books) and len(tokens)
        :param books:  A list of strings representing book titles.
        :param tokens: A list of lists representing tokens in the books.
        """
        if authors and books and tokens:
            self.authors = authors
            self.books = books
            self.tokens = tokens
            self.texts = None
        else:
            self.authors = []
            self.books = []
            self.tokens = []
            self.texts = []

    def add_book(self, author: str, book: str, text: str):
        """
        Add a single book to the corpus. This can only be done if the corpus has not been initialised with books in the constructor.
        :param author: The author's name as string.
        :param book: The book title as string.
        :param text: The book content as string.
        """
        assert (len(self.tokens) == 0)
        self.authors.append(author)
        self.books.append(book)
        self.texts.append(text)

    def tokenise(self, tokenise):
        """
        Tokenise all books in the corpus using the custom tokenisation function.

        :param tokenise: a tokenise function which takes a str and returns a list of tokens. It is language-specific and should remove pronouns.
        """
        self.tokens = [tokenise(text) for text in self.texts]

    def split(self, segment_length: int = 1000):
        """
        Split the books in the corpus into smaller books of a specified maximum length. So if segment_length = 1000 and you have a book of length 1500,
        it will be split into two books of lengths 1000 and 500 respectively, with the same author and title attributes.
        This Corpus object is not modified but a new instance will be constructed.

        :param segment_length: The maximum length of books in the new corpus.
        :return: The new corpus with split books.
        """
        new_authors = []
        new_books = []
        new_tokens = []

        for author_id in range(len(self.authors)):
            for ctr, segment_start in enumerate(range(0, len(self.tokens[author_id]), segment_length)):
                segment_tokens = self.tokens[author_id][
                                 segment_start:min(segment_start + segment_length, len(self.tokens[author_id]))]
                new_authors.append(self.authors[author_id])
                new_books.append(self.books[author_id] + "_" + str(ctr))
                new_tokens.append(segment_tokens)

        return Corpus(new_authors, new_books, new_tokens)
