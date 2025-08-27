"""Test the data models."""

import pytest
from pathlib import Path

from textbooks_to_rl.textbook_manager.models import TextbookPage, Textbook
from textbooks_to_rl.question_generator.models import (
    QuestionDifficulty,
    QuestionDomain,
    QuestionAnswer,
    ValidationResult,
)


def test_textbook_page():
    """Test TextbookPage model."""
    page = TextbookPage(
        content="Sample content",
        page_number=1,
        textbook_name="test_book",
        chapter="Chapter 1",
        section="Section 1.1"
    )
    
    assert page.content == "Sample content"
    assert page.page_number == 1
    assert page.textbook_name == "test_book"
    assert page.chapter == "Chapter 1"
    assert page.section == "Section 1.1"


def test_textbook():
    """Test Textbook model."""
    test_path = Path("/test/path")
    textbook = Textbook(
        name="test_book",
        path=test_path,
        txt_path=test_path / "test.txt",
        pages=[],
        total_pages=0
    )
    
    assert textbook.name == "test_book"
    assert textbook.path == test_path
    assert textbook.total_pages == 0
    assert len(textbook.pages) == 0


def test_question_difficulty():
    """Test QuestionDifficulty enum."""
    assert QuestionDifficulty.HIGH_SCHOOL.value == "high_school"
    assert QuestionDifficulty.UNDERGRAD.value == "undergrad"
    assert QuestionDifficulty.GRAD.value == "grad"
    
    # Test description method
    desc = QuestionDifficulty.UNDERGRAD.get_description()
    assert "undergraduate" in desc.lower()


def test_question_domain():
    """Test QuestionDomain enum."""
    assert QuestionDomain.CALCULUS.value == "calculus"
    assert QuestionDomain.LINEAR_ALGEBRA.value == "linear_algebra"
    assert QuestionDomain.OTHER.value == "other"


def test_question_answer():
    """Test QuestionAnswer model."""
    qa = QuestionAnswer(
        question="What is 2+2?",
        solution="4",
        source="test_source",
        hints=["Think about basic addition"],
        domain=QuestionDomain.OTHER
    )
    
    assert qa.question == "What is 2+2?"
    assert qa.solution == "4"
    assert qa.source == "test_source"
    assert qa.hints == ["Think about basic addition"]
    assert qa.domain == QuestionDomain.OTHER


def test_validation_result():
    """Test ValidationResult model."""
    result = ValidationResult(
        is_correct=True,
        score=0.95,
        feedback="Correct answer!"
    )
    
    assert result.is_correct is True
    assert result.score == 0.95
    assert result.feedback == "Correct answer!"