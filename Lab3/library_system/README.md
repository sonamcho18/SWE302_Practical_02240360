# SWE302 - Lab 3: Practicing Test-Driven Development (TDD)

## System: Library Management System

A small in-memory Library Management System built entirely using the
Red -> Green -> Refactor TDD cycle.

## Functionalities Developed Using TDD

### 1. Add a Book
Requirements:
- A book can be added with a valid ID, title and author.
- A duplicate book ID must be rejected.
- An empty title must be rejected.
- An empty book ID must be rejected.

### 2. Borrow a Book
Requirements:
- A registered user can borrow an available book.
- A book that is already borrowed cannot be borrowed again.
- A user cannot borrow more than 5 books at a time.
- An invalid (non-existent) book ID must be rejected.

### 3. Return a Book
Requirements:
- A user who borrowed a book can return it.
- A user who did NOT borrow the book cannot return it.
- A book that is not currently borrowed cannot be returned again.
- An invalid (non-existent) book ID must be rejected.
- Returning a book frees up the user's borrow slot.

## Project Structure

```
library_system/
├── src/
│   ├── __init__.py
│   └── library.py        # Production code (Book, Library classes)
├── tests/
│   ├── __init__.py
│   └── test_library.py   # Automated unit tests (13 tests)
└── README.md
```

## Testing Framework
Python's built-in `unittest` framework (no external installation required).

## How to Run the Tests

From the `library_system/` directory:

```bash
python3 -m unittest discover -s tests -v
```

Expected result: `Ran 13 tests ... OK`

## TDD Process Followed

For every functionality above, the following cycle was applied and is
documented with screenshots in the accompanying report:

1. **RED** - Write a failing test first.
2. **GREEN** - Write the minimum production code to make it pass.
3. **REFACTOR** - Clean up the code while keeping all tests passing.

This cycle was repeated for all three functionalities (13 test cases in
total), covering valid input, invalid input, boundary values and business
rule violations.
