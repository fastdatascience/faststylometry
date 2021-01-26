class Corpus:

    def __init__(self, authors=None, books=None, tokens=None):
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

    def add_book(self, author, book, text):
        self.authors.append(author)
        self.books.append(book)
        self.texts.append(text)

    def tokenise(self, tokenise):
        self.tokens = [tokenise(text) for text in self.texts]

    def split(self, segment_length=1000):

        new_authors = []
        new_books = []
        new_tokens = []

        for author_id in range(len(self.authors)):
            for segment_start in range(0, len(self.tokens[author_id]), segment_length):
                segment_tokens = self.tokens[author_id][
                                 segment_start:min(segment_start + segment_length, len(self.tokens[author_id]))]
                new_authors.append(self.authors[author_id])
                new_books.append(self.books[author_id])
                new_tokens.append(segment_tokens)

        return Corpus(new_authors, new_books, new_tokens)

    # Methods for calculating
