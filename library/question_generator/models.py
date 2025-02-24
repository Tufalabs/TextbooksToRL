from dataclasses import dataclass
from typing import List, Optional

@dataclass
class QuestionAnswer:
    """Data class representing a question-answer pair with optional hints and source."""
    question: str
    solution: str
    source: Optional[str] = None
    hints: Optional[List[str]] = None

@dataclass
class ValidationResult:
    """Data class representing the result of a solution validation."""
    is_correct: bool
    score: float
    feedback: Optional[str] = None 