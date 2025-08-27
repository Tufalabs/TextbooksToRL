#!/usr/bin/env python3
"""
Legacy entry point for textbooks-to-rl.
This file is deprecated. Use `textbooks-to-rl` command or `python -m textbooks_to_rl.cli` instead.
"""

import warnings
import sys

warnings.warn(
    "main.py is deprecated. Use 'textbooks-to-rl' command or 'python -m textbooks_to_rl.cli' instead.",
    DeprecationWarning,
    stacklevel=2,
)

# Import and run the new CLI
from src.textbooks_to_rl.cli import cli_main

if __name__ == "__main__":
    cli_main()
