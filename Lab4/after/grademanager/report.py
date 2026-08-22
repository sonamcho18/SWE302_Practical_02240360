"""Report generation, kept separate from console printing for testability."""

from typing import List

from .grade_calculator import grade_for_student
from .models import Student


def build_report(students: List[Student]) -> str:
    """Build a plain-text grade report for a list of students.

    Students with no marks are reported as "N/A" instead of crashing
    the whole report.
    """
    lines = ["REPORT"]
    for student in students:
        try:
            grade = grade_for_student(student)
        except ValueError:
            grade = "N/A"
        lines.append(f"{student.name} ({student.term}) - {grade}")
    return "\n".join(lines)
