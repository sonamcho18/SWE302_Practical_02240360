MAX_BOOKS_PER_USER = 5


class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.is_borrowed = False
        self.borrowed_by = None


class Library:
    def __init__(self):
        self._books = {}
        self._borrowed_counts = {}

    def add_book(self, book_id, title, author):
        self._validate_not_empty(book_id, "Book ID")
        self._validate_not_empty(title, "Title")
        if self.book_exists(book_id):
            raise ValueError(f"Book with ID '{book_id}' already exists.")
        self._books[book_id] = Book(book_id, title, author)

    def book_exists(self, book_id):
        return book_id in self._books

    def borrow_book(self, user_id, book_id):
        book = self._get_book_or_raise(book_id)
        self._ensure_book_is_available(book)
        self._ensure_user_is_under_borrow_limit(user_id)
        book.is_borrowed = True
        book.borrowed_by = user_id
        self._borrowed_counts[user_id] = self._borrowed_counts.get(user_id, 0) + 1

    def is_borrowed(self, book_id):
        return self._get_book_or_raise(book_id).is_borrowed

    @staticmethod
    def _ensure_book_is_available(book):
        if book.is_borrowed:
            raise ValueError(f"Book '{book.book_id}' is already borrowed.")

    def _ensure_user_is_under_borrow_limit(self, user_id):
        if self._borrowed_counts.get(user_id, 0) >= MAX_BOOKS_PER_USER:
            raise ValueError(f"User '{user_id}' cannot borrow more than {MAX_BOOKS_PER_USER} books.")

    def return_book(self, user_id, book_id):
        book = self._get_book_or_raise(book_id)
        self._ensure_book_can_be_returned_by(book, user_id)
        book.is_borrowed = False
        book.borrowed_by = None
        self._borrowed_counts[user_id] = max(0, self._borrowed_counts.get(user_id, 0) - 1)

    @staticmethod
    def _ensure_book_can_be_returned_by(book, user_id):
        if not book.is_borrowed:
            raise ValueError(f"Book '{book.book_id}' is not currently borrowed.")
        if book.borrowed_by != user_id:
            raise ValueError(f"Book '{book.book_id}' was not borrowed by user '{user_id}'.")

    def _get_book_or_raise(self, book_id):
        if not self.book_exists(book_id):
            raise ValueError(f"Book with ID '{book_id}' does not exist.")
        return self._books[book_id]

    @staticmethod
    def _validate_not_empty(value, field_name):
        if not value:
            raise ValueError(f"{field_name} cannot be empty.")
