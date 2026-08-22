"""Entry point for the Grade Manager application."""

from grademanager.models import Student
from grademanager.report import build_report
from grademanager.storage import save_students

DATA_FILE = "data.txt"


def seed_students() -> list[Student]:
    """Create the starting set of students for this demo run."""
    return [
        Student(name="Sonam", term="T1", marks=[85, 90, 78]),
        Student(name="Karma", term="T1", marks=[60, 55, 40]),
        Student(name="Pema", term="T1", marks=[95, 92, 99]),
    ]


def main() -> None:
    students = seed_students()
    print(build_report(students))
    save_students(students, DATA_FILE)


if __name__ == "__main__":
    main()
