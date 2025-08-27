"""
Textbooks to RL - A tool for generating reinforcement learning training questions from textbooks.
"""

__version__ = "0.1.0"
__author__ = "Toby Simonds"
__email__ = "toby@example.com"

from .question_generator import QuestionGenerator
from .textbook_manager import TextbookManager

__all__ = [
    "QuestionGenerator",
    "TextbookManager",
    "__version__",
]
