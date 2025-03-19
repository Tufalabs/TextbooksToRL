import asyncio
from lib.question_generator import QuestionGenerator
from lib.question_generator.models import QuestionDifficulty
from lib.textbook_manager import TextbookManager
import argparse

async def process_page(textbook_manager, textbook_name, page_num, generator=None, questions_per_page=10):
    """Process a single page and generate questions."""
    current_passage = textbook_manager.get_page(textbook_name, page_number=page_num)
    if not current_passage:
        print(f"Warning: Could not find page {page_num} in {textbook_name}")
        return []
    
    print(f"Processing page {page_num}...")
    try:
        questions = await generator.generate_questions(
            current_passage.content,
            num_questions=questions_per_page,
            difficulty=QuestionDifficulty.UNDERGRAD,
            verify=False,
            src=f"{textbook_name}_page_{page_num}"
        )
        print(f"✓ Completed page {page_num} - generated {len(questions)} questions")
        return questions
    except Exception as e:
        print(f"Error processing page {page_num}: {str(e)}")
        return []

async def main():
    parser = argparse.ArgumentParser(description='Process specific page range from a textbook')
    parser.add_argument('textbook_name', help='Name of the textbook to process')
    parser.add_argument('start_page', type=int, help='Starting page number')
    parser.add_argument('end_page', type=int, help='Ending page number')
    parser.add_argument('--pages-per-group', type=int, default=1, 
                        help='Number of pages to process together (default: 1)')
    parser.add_argument('--batch-size', type=int, default=10, 
                        help='Number of page groups to process in parallel (default: 10)')
    parser.add_argument('--questions-per-page', type=int, default=10,
                        help='Number of questions to generate per page (default: 10)')
    parser.add_argument('--model', default="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
                        help='Model to use for generation (default: gpt-4o)')
    parser.add_argument('--output-dir', default="generated_questions/Sterwart-chap-15",
                        help='Directory to save generated questions')
    args = parser.parse_args()

    # Initialize manager and generator
    textbook_manager = TextbookManager()
    generator = QuestionGenerator(
        model_name=args.model, 
        output_dir=args.output_dir
    )

    # Validate page range
    num_pages = textbook_manager.get_num_pages(args.textbook_name)
    if not num_pages:
        print(f"Error: Textbook '{args.textbook_name}' not found")
        return
    
    start_page = max(1, min(args.start_page, num_pages))
    end_page = max(start_page, min(args.end_page, num_pages))
    
    print(f"\nProcessing textbook: {args.textbook_name}")
    print(f"Processing pages {start_page} to {end_page}")
    print(f"Using model: {args.model}")
    print(f"Questions per page: {args.questions_per_page}")
    print(f"Batch size: {args.batch_size}")
    
    all_questions = []
    
    # Process pages in batches for parallelism
    for batch_start in range(start_page, end_page + 1, args.batch_size):
        batch_end = min(batch_start + args.batch_size, end_page + 1)
        print(f"\nProcessing batch of pages {batch_start} to {batch_end-1}...")
        
        # Create tasks for each page in the batch
        tasks = []
        for page_num in range(batch_start, batch_end):
            tasks.append(process_page(
                textbook_manager, 
                args.textbook_name, 
                page_num, 
                generator, 
                args.questions_per_page
            ))
        
        # Run batch of tasks in parallel
        batch_results = await asyncio.gather(*tasks)
        
        # Collect results
        for page_questions in batch_results:
            all_questions.extend(page_questions)
        
        print(f"Batch complete. Total questions so far: {len(all_questions)}")
    
    print(f"\nFinished processing pages {start_page}-{end_page}")
    print(f"Total questions generated: {len(all_questions)}")
    return all_questions

if __name__ == "__main__":
    questions = asyncio.run(main())