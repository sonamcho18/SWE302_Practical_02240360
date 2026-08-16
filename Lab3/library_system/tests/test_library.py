import unittest
from src.library import Library


class TestAddBook(unittest.TestCase):

    def setUp(self):
        self.library = Library()

    def test_should_add_book_successfully(self):
        self.library.add_book("B1", "Clean Code", "Robert C. Martin")
        self.assertTrue(self.library.book_exists("B1"))

    def test_should_reject_duplicate_book_id(self):
        self.library.add_book("B1", "Clean Code", "Robert C. Martin")
        with self.assertRaises(ValueError):
            self.library.add_book("B1", "Another Title", "Another Author")

    def test_should_reject_empty_title(self):
        with self.assertRaises(ValueError):
            self.library.add_book("B2", "", "Some Author")

    def test_should_reject_empty_book_id(self):
        with self.assertRaises(ValueError):
            self.library.add_book("", "Some Title", "Some Author")


class TestBorrowBook(unittest.TestCase):

    def setUp(self):
        self.library = Library()
        self.library.add_book("B1", "Clean Code", "Robert C. Martin")
        self.library.add_book("B2", "The Pragmatic Programmer", "Andrew Hunt")

    def test_should_allow_user_to_borrow_available_book(self):
        self.library.borrow_book("U1", "B1")
        self.assertTrue(self.library.is_borrowed("B1"))

    def test_should_not_allow_borrowing_already_borrowed_book(self):
        self.library.borrow_book("U1", "B1")
        with self.assertRaises(ValueError):
            self.library.borrow_book("U2", "B1")

    def test_should_reject_invalid_book_id(self):
        with self.assertRaises(ValueError):
            self.library.borrow_book("U1", "DOES_NOT_EXIST")

    def test_should_not_allow_user_to_borrow_more_than_five_books(self):
        for i in range(3, 8):
            self.library.add_book(f"B{i}", f"Book {i}", "Some Author")
        for i in [1, 2, 3, 4, 5]:
            self.library.borrow_book("U1", f"B{i}")
        with self.assertRaises(ValueError):
            self.library.borrow_book("U1", "B6")


class TestReturnBook(unittest.TestCase):

    def setUp(self):
        self.library = Library()
        self.library.add_book("B1", "Clean Code", "Robert C. Martin")
        self.library.borrow_book("U1", "B1")

    def test_should_allow_user_to_return_borrowed_book(self):
        self.library.return_book("U1", "B1")
        self.assertFalse(self.library.is_borrowed("B1"))

    def test_should_reject_return_by_user_who_did_not_borrow_it(self):
        with self.assertRaises(ValueError):
            self.library.return_book("U2", "B1")

    def test_should_reject_returning_a_book_that_is_not_borrowed(self):
        self.library.return_book("U1", "B1")
        with self.assertRaises(ValueError):
            self.library.return_book("U1", "B1")

    def test_should_reject_returning_invalid_book_id(self):
        with self.assertRaises(ValueError):
            self.library.return_book("U1", "DOES_NOT_EXIST")

    def test_should_free_up_borrow_slot_after_return(self):
        self.library.return_book("U1", "B1")
        self.library.borrow_book("U1", "B1")
        self.assertTrue(self.library.is_borrowed("B1"))


if __name__ == "__main__":
    unittest.main()
