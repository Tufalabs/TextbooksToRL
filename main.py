import argparse
import asyncio
from lib.question_generator import QuestionGenerator
from lib.question_generator.models import QuestionDifficulty
from lib.textbook_manager import TextbookManager
import os
import json
import random

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Generate questions from textbooks')
    parser.add_argument('--model', 
                       default="Qwen/QwQ-32B",
                       help='Model to use for generation (default: deepseek-chat)')
    parser.add_argument('--output-dir', 
                       default="generated_questions/DS-MATH3.0",
                       help='Directory to save generated questions')
    parser.add_argument('--pages-per-group', 
                       type=int, 
                       default=3,
                       help='Number of pages to process together (default: 5)')
    parser.add_argument('--batch-size', 
                       type=int, 
                       default=100,
                       help='Number of page groups to process in parallel (default: 100)')
    parser.add_argument('--questions-per-chunk', 
                       type=int, 
                       default=10,
                       help='Number of questions to generate per chunk (default: 10)')
    return parser.parse_args()

# Initialize manager
textbook_manager = TextbookManager()
generator = QuestionGenerator(model_name="Qwen/QwQ-32B", output_dir="generated_questions/QWQ")

# Create list of coroutines for each page

async def process_pages(textbook_name, start_page, num_pages=3):
    """Process multiple consecutive pages and generate questions from their combined content."""
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
            print(f"Warning: Could not find page {page_num} in {textbook_name}")
    
    if combined_passage is None:
        print(f"Warning: Could not load any pages starting from {start_page}")
        return []
    
    print(f"Processing pages {start_page}-{start_page + num_pages - 1}...")
    try:
        questions = await generator.generate_questions(
            combined_passage.content,
            num_questions=10,
            difficulty=QuestionDifficulty.UNDERGRAD,
            verify=False,
            src=f"{textbook_name}_pages_{start_page}-{start_page + num_pages - 1}"
        )
        print(f"✓ Completed pages {start_page}-{start_page + num_pages - 1} - generated {len(questions)} questions")
        return questions
    except Exception as e:
        print(f"Error processing pages {start_page}-{start_page + num_pages - 1}: {str(e)}")
        return []

async def main():
    """Main async function to process textbooks and generate questions."""
    args = parse_args()
  
    # Initialize manager with command line arguments
    textbook_manager = TextbookManager()
    generator = QuestionGenerator(
        model_name=args.model, 
        output_dir=args.output_dir
    )
    
    # Check for already processed textbooks by looking at output directory
    processed_textbooks = set()
    output_dir = args.output_dir
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            if filename.endswith('.json'):
                try:
                    with open(os.path.join(output_dir, filename), 'r') as f:
                        question_data = json.load(f)
                        if 'source' in question_data:
                            source = question_data['source']
                            # Extract textbook name before '_pages_'
                            textbook_name = source.split('_pages_')[0]
                            processed_textbooks.add(textbook_name)
                except Exception as e:
                    print(f"Error reading {filename}: {e}")
    
    print(f"Found {len(processed_textbooks)} already processed textbooks: {processed_textbooks}")
    
    # Get all textbook names and shuffle them
    textbook_names = [f.replace('.txt', '') for f in os.listdir('textbooks/txt') if f.endswith('.txt')]
    random.shuffle(textbook_names)  # Shuffle the textbooks
    
    # Filter out already processed textbooks by checking if the textbook name is contained in any processed source
    unprocessed_textbooks = []
    for textbook in textbook_names:
        if not any(textbook in processed_source for processed_source in processed_textbooks):
            unprocessed_textbooks.append(textbook)
    
    textbook_names = unprocessed_textbooks
    print(f"Found {len(textbook_names)} unprocessed textbooks: {textbook_names}")
    
    all_questions = []
    PAGES_PER_GROUP = args.pages_per_group
    BATCH_SIZE = args.batch_size

    for textbook_name in textbook_names:
        num_pages = textbook_manager.get_num_pages(textbook_name)
        print(f"\nProcessing textbook: {textbook_name}")
        print(f"Number of pages: {num_pages}")
        
        textbook_questions = []
        
        # Process pages in groups and batches
        for batch_start in range(0, num_pages, BATCH_SIZE * PAGES_PER_GROUP):
            batch_end = min(batch_start + BATCH_SIZE * PAGES_PER_GROUP, num_pages)
            print(f"\nProcessing batch of pages {batch_start} to {batch_end-1}...")
            
            tasks = []
            for group_start in range(batch_start, batch_end, PAGES_PER_GROUP):
                if group_start < num_pages:
                    actual_pages = min(PAGES_PER_GROUP, num_pages - group_start)
                    tasks.append(process_pages(textbook_name, group_start, actual_pages))
            
            batch_results = await asyncio.gather(*tasks)
            
            for page_questions in batch_results:
                textbook_questions.extend(page_questions)
            
            print(f"Batch complete. Questions for {textbook_name} so far: {len(textbook_questions)}")
        
        all_questions.extend(textbook_questions)
        print(f"\nFinished processing {textbook_name}. Total questions: {len(textbook_questions)}")

    verified_questions = all_questions
    print(f"\nFinished processing all textbooks. Total questions generated: {len(verified_questions)}")
    return verified_questions

if __name__ == "__main__":
    verified_questions = asyncio.run(main())
