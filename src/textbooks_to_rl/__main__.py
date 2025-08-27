"""
Allow running the package as a module with python -m textbooks_to_rl.
"""

from .cli import cli_main

if __name__ == "__main__":
    cli_main()
