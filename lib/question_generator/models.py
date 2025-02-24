from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class QuestionDomain(Enum):
    CALCULUS = "calculus"
    LINEAR_ALGEBRA = "linear_algebra"
    PROBABILITY = "probability"
    STATISTICS = "statistics"
    PHYSICS_MECHANICS = "physics_mechanics"
    PHYSICS_ELECTRICITY = "physics_electricity"
    PHYSICS_THERMODYNAMICS = "physics_thermodynamics"
    CHEMISTRY = "chemistry"
    BIOLOGY = "biology"
    COMPUTER_SCIENCE = "computer_science"
    OTHER = "other"

class QuestionDifficulty(Enum):
    HIGH_SCHOOL = "high_school"
    UNDERGRAD = "undergrad"
    GRAD = "grad"
    PHD = "phd"
    EXPERT = "expert"
    
    def get_description(self) -> str:
        descriptions = {
            "high_school": "Basic concepts suitable for high school students",
            "undergrad": "College undergraduate level complexity",
            "grad": "Graduate school level depth and complexity",
            "phd": "Advanced theoretical concepts and research-level problems",
            "expert": "Industry expert level requiring deep domain knowledge"
        }
        return descriptions[self.value]

@dataclass
class QuestionAnswer:
    """Data class representing a question-answer pair with optional hints and source."""
    question: str
    solution: str
    source: Optional[str] = None
    hints: Optional[List[str]] = None
    domain: Optional[QuestionDomain] = None

@dataclass
class ValidationResult:
    """Data class representing the result of a solution validation."""
    is_correct: bool
    score: float
    feedback: Optional[str] = None 