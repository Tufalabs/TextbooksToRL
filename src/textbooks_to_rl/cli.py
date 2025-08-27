"""
Command-line interface for textbooks-to-rl.
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path

from . import __version__
from .question_generator import QuestionGenerator
from .question_generator.models import QuestionDifficulty
from .textbook_manager import TextbookManager


def setup_logging(verbose: bool = False) -> None:
    """Set up logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def create_parser() -> argparse.ArgumentParser:
    """Create and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="textbooks-to-rl",
        description="Generate questions from textbooks for reinforcement learning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    parser.add_argument(
        "--model",
        default="Qwen/QwQ-32B",
        help="Model to use for generation (default: %(default)s)",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("generated_questions"),
        help="Directory to save generated questions (default: %(default)s)",
    )

    parser.add_argument(
        "--textbooks-dir",
        type=Path,
        default=Path("textbooks/txt"),
        help="Directory containing textbook txt files (default: %(default)s)",
    )

    parser.add_argument(
        "--pages-per-group",
        type=int,
        default=3,
        help="Number of pages to process together (default: %(default)s)",
    )

    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="Number of page groups to process in parallel (default: %(default)s)",
    )

    parser.add_argument(
        "--questions-per-chunk",
        type=int,
        default=10,
        help="Number of questions to generate per chunk (default: %(default)s)",
    )

    parser.add_argument(
        "--difficulty",
        type=str,
        choices=[d.value for d in QuestionDifficulty],
        default=QuestionDifficulty.UNDERGRAD.value,
        help="Difficulty level for generated questions (default: %(default)s)",
    )

    parser.add_argument(
        "--no-verify",
        action="store_true",
        help="Skip solution verification step",
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    return parser


async def process_pages(
    textbook_name: str,
    start_page: int,
    num_pages: int,
    textbook_manager: TextbookManager,
    generator: QuestionGenerator,
    difficulty: QuestionDifficulty,
    questions_per_chunk: int,
    verify: bool,
) -> list:
    """Process multiple consecutive pages and generate questions from their combined content."""
    logger = logging.getLogger(__name__)

    combined_passage = None

    # Combine the content from multiple pages
    for page_num in range(start_page, start_page + num_pages):
        current_passage = textbook_manager.get_page(textbook_name, page_number=page_num)
        if current_passage:
            if combined_passage is None:
                combined_passage = current_passage
            else:
                combined_passage.content += "\n\n" + current_passage.content
        else:
            logger.warning(f"Could not find page {page_num} in {textbook_name}")

    if combined_passage is None:
        logger.warning(f"Could not load any pages starting from {start_page}")
        return []

    logger.info(f"Processing pages {start_page}-{start_page + num_pages - 1}...")

    try:
        questions = await generator.generate_questions(
            combined_passage.content,
            num_questions=questions_per_chunk,
            difficulty=difficulty,
            verify=verify,
            src=f"{textbook_name}_pages_{start_page}-{start_page + num_pages - 1}",
        )
        logger.info(
            f"✓ Completed pages {start_page}-{start_page + num_pages - 1} "
            f"- generated {len(questions)} questions"
        )
        return questions
    except Exception as e:
        logger.error(
            f"Error processing pages {start_page}-{start_page + num_pages - 1}: {e}"
        )
        return []


async def main() -> int:
    """Main async function to process textbooks and generate questions."""
    parser = create_parser()
    args = parser.parse_args()

    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)

    # Validate directories
    if not args.textbooks_dir.exists():
        logger.error(f"Textbooks directory not found: {args.textbooks_dir}")
        return 1

    # Create output directory if it doesn't exist
    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Initialize components
    try:
        textbook_manager = TextbookManager(str(args.textbooks_dir))
        generator = QuestionGenerator(
            model_name=args.model, output_dir=str(args.output_dir)
        )
        difficulty = QuestionDifficulty(args.difficulty)
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        return 1

    # Get available textbooks
    textbook_names = textbook_manager.get_all_textbook_names()
    if not textbook_names:
        logger.error("No textbooks found in the specified directory")
        return 1

    logger.info(f"Found {len(textbook_names)} textbooks: {textbook_names}")

    all_questions = []
    verify = not args.no_verify

    for textbook_name in textbook_names:
        num_pages = textbook_manager.get_num_pages(textbook_name)
        if num_pages is None:
            logger.warning(f"Could not determine page count for {textbook_name}")
            continue

        logger.info(f"Processing textbook: {textbook_name} ({num_pages} pages)")

        textbook_questions = []

        # Process pages in groups and batches
        for batch_start in range(0, num_pages, args.batch_size * args.pages_per_group):
            batch_end = min(
                batch_start + args.batch_size * args.pages_per_group, num_pages
            )
            logger.info(
                f"Processing batch of pages {batch_start} to {batch_end - 1}..."
            )

            tasks = []
            for group_start in range(batch_start, batch_end, args.pages_per_group):
                if group_start < num_pages:
                    actual_pages = min(args.pages_per_group, num_pages - group_start)
                    tasks.append(
                        process_pages(
                            textbook_name,
                            group_start,
                            actual_pages,
                            textbook_manager,
                            generator,
                            difficulty,
                            args.questions_per_chunk,
                            verify,
                        )
                    )

            batch_results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in batch_results:
                if isinstance(result, Exception):
                    logger.error(f"Batch processing error: {result}")
                else:
                    textbook_questions.extend(result)

            logger.info(
                f"Batch complete. Questions for {textbook_name} so far: {len(textbook_questions)}"
            )

        all_questions.extend(textbook_questions)
        logger.info(
            f"Finished processing {textbook_name}. Total questions: {len(textbook_questions)}"
        )

    logger.info(
        f"Finished processing all textbooks. Total questions generated: {len(all_questions)}"
    )
    return 0


def cli_main() -> None:
    """Entry point for the CLI."""
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    cli_main()
