"""Unit tests for the grade_calculator module.

These tests are only possible because the refactored code separates
pure calculation logic from I/O and global state.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from grademanager.grade_calculator import letter_grade, grade_for_student
from grademanager.models import Student


@pytest.mark.parametrize(
    "average,expected",
    [
        (95, "A"),
        (90, "A"),
        (85, "B"),
        (80, "B"),
        (75, "C"),
        (70, "C"),
        (65, "D"),
        (60, "D"),
        (59, "F"),
        (0, "F"),
    ],
)
def test_letter_grade_boundaries(average, expected):
    assert letter_grade(average) == expected


def test_grade_for_student_computes_average_first():
    student = Student(name="Sonam", term="T1", marks=[85, 90, 78])
    assert grade_for_student(student) == "B"


def test_average_raises_on_no_marks():
    student = Student(name="Empty", term="T1", marks=[])
    with pytest.raises(ValueError):
        student.average()
