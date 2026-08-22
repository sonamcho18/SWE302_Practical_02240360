"""Pure grading logic, kept separate from I/O so it is easy to unit test."""

from .models import Student

# Named constants instead of "magic numbers" scattered through the code.
GRADE_THRESHOLDS = (
    (90, "A"),
    (80, "B"),
    (70, "C"),
    (60, "D"),
)
FAILING_GRADE = "F"


def letter_grade(average: float) -> str:
    """Convert a numeric average into a letter grade.

    Args:
        average: the student's average mark (0-100).

    Returns:
        A single-letter grade string: A, B, C, D, or F.
    """
    for threshold, grade in GRADE_THRESHOLDS:
        if average >= threshold:
            return grade
    return FAILING_GRADE


def grade_for_student(student: Student) -> str:
    """Compute the letter grade for a given student."""
    return letter_grade(student.average())
