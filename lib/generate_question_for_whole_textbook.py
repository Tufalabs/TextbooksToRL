import asyncio
from typing import List, Optional
from enum import Enum

async def generate_questions_for_textbook(
    textbook_name: str,
    textbook_manager,
    generator,
    questions_per_page: int = 5,
    batch_size: int = 50,
    difficulty: Optional[Enum] = None
) -> List:
    """
    Generate questions for an entire textbook using batched async processing.
    
    Args:
        textbook_name: Name of the textbook to process
        textbook_manager: TextbookManager instance to handle page retrieval
        generator: QuestionGenerator instance
        questions_per_page: Number of questions to generate per page
        batch_size: Number of pages to process in each batch
        difficulty: Difficulty level for questions (QuestionDifficulty enum)
    
    Returns:
        List of generated questions
    """
    
    async def process_page(page_num: int) -> List:
        passage = textbook_manager.get_page(textbook_name, page_number=page_num)
        if passage is None:
            print(f"Warning: Could not load page {page_num}")
            return []
        
        print(f"Processing page {page_num}...")
        try:
            questions = await generator.generate_questions(
                passage.content,
                num_questions=questions_per_page,
                difficulty=difficulty,
                verify=False,
                src=passage.page_number
            )
            print(f"✓ Completed page {page_num} - generated {len(questions)} questions")
            return questions
        except Exception as e:
            print(f"Error processing page {page_num}: {str(e)}")
            return []

    num_pages = textbook_manager.get_num_pages(textbook_name)
    print(f"Number of pages in textbook: {num_pages}")
    
    all_questions = []
    
    # Process pages in batches
    for batch_start in range(0, num_pages, batch_size):
        batch_end = min(batch_start + batch_size, num_pages)
        print(f"\nProcessing batch of pages {batch_start} to {batch_end-1}...")
        
        batch_results = await asyncio.gather(
            *[process_page(i) for i in range(batch_start, batch_end)]
        )
        
        # Add batch results to all_questions
        for page_questions in batch_results:
            all_questions.extend(page_questions)
        
        print(f"Batch complete. Total questions so far: {len(all_questions)}")
    
    print(f"\nFinished processing all pages. Total questions generated: {len(all_questions)}")
    return all_questions


# Example usage:
"""
# Import necessary dependencies
from your_question_generator import QuestionGenerator, QuestionDifficulty
from your_textbook_manager import TextbookManager

async def main():
    textbook_manager = TextbookManager()
    generator = QuestionGenerator(model_name="gpt-4-mini")
    
    questions = await generate_questions_for_textbook(
        textbook_name="your_textbook",
        textbook_manager=textbook_manager,
        generator=generator,
        questions_per_page=5,
        difficulty=QuestionDifficulty.UNDERGRAD
    )
    
    # Do something with the questions...

if __name__ == "__main__":
    asyncio.run(main())
"""
