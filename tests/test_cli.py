"""Test the CLI interface."""

import pytest
from unittest.mock import patch, MagicMock
import argparse

from textbooks_to_rl.cli import create_parser, setup_logging
from textbooks_to_rl.question_generator.models import QuestionDifficulty


def test_create_parser():
    """Test parser creation."""
    parser = create_parser()
    
    assert isinstance(parser, argparse.ArgumentParser)
    assert parser.prog == "textbooks-to-rl"
    
    # Test default values
    args = parser.parse_args([])
    assert args.model == "Qwen/QwQ-32B"
    assert args.pages_per_group == 3
    assert args.batch_size == 100
    assert args.questions_per_chunk == 10
    assert args.difficulty == QuestionDifficulty.UNDERGRAD.value
    assert args.no_verify is False
    assert args.verbose is False


def test_parser_arguments():
    """Test parser with arguments."""
    parser = create_parser()
    
    args = parser.parse_args([
        "--model", "gpt-4o-mini",
        "--output-dir", "custom_output",
        "--pages-per-group", "5",
        "--batch-size", "50",
        "--difficulty", "grad",
        "--no-verify",
        "--verbose"
    ])
    
    assert args.model == "gpt-4o-mini"
    assert str(args.output_dir) == "custom_output"
    assert args.pages_per_group == 5
    assert args.batch_size == 50
    assert args.difficulty == "grad"
    assert args.no_verify is True
    assert args.verbose is True


def test_setup_logging():
    """Test logging setup."""
    with patch('textbooks_to_rl.cli.logging.basicConfig') as mock_basic_config:
        setup_logging(verbose=False)
        mock_basic_config.assert_called_once()
        
        # Check that INFO level was set (not DEBUG)
        call_args = mock_basic_config.call_args[1]
        assert call_args['level'] == 20  # INFO level
        
    with patch('textbooks_to_rl.cli.logging.basicConfig') as mock_basic_config:
        setup_logging(verbose=True)
        mock_basic_config.assert_called_once()
        
        # Check that DEBUG level was set
        call_args = mock_basic_config.call_args[1]
        assert call_args['level'] == 10  # DEBUG level


def test_difficulty_choices():
    """Test that all difficulty choices are valid."""
    parser = create_parser()
    
    # Test valid difficulty levels
    for difficulty in QuestionDifficulty:
        args = parser.parse_args(["--difficulty", difficulty.value])
        assert args.difficulty == difficulty.value
    
    # Test invalid difficulty level
    with pytest.raises(SystemExit):
        parser.parse_args(["--difficulty", "invalid_difficulty"])