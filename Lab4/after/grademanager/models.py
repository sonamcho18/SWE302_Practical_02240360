"""Data models for the grade manager."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Student:
    """Represents a single student and their recorded marks."""

    name: str
    term: str
    marks: List[float] = field(default_factory=list)

    def average(self) -> float:
        """Return the average of this student's marks.

        Raises:
            ValueError: if the student has no marks recorded.
        """
        if not self.marks:
            raise ValueError(f"{self.name} has no marks recorded")
        return sum(self.marks) / len(self.marks)
