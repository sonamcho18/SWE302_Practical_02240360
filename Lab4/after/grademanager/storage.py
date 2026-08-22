"""File persistence for student records, isolated from business logic
so the rest of the app can be tested without touching the filesystem."""

from pathlib import Path
from typing import List

from .models import Student


def save_students(students: List[Student], file_path: str) -> None:
    """Write student records to a CSV-style text file."""
    with open(file_path, "w", encoding="utf-8") as handle:
        for student in students:
            marks = ";".join(str(mark) for mark in student.marks)
            handle.write(f"{student.name},{student.term},{marks}\n")


def load_students(file_path: str) -> List[Student]:
    """Read student records from a CSV-style text file.

    Returns an empty list if the file does not exist, rather than
    silently printing an error.
    """
    path = Path(file_path)
    if not path.exists():
        return []

    students: List[Student] = []
    with open(path, "r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            name, term, marks_str = line.split(",")
            marks = [float(m) for m in marks_str.split(";") if m]
            students.append(Student(name=name, term=term, marks=marks))
    return students
