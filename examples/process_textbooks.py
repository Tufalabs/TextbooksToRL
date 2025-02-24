from lib.textbook_manager import TextbookManager
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize manager with your directories
manager = TextbookManager(
    textbooks_dir="path/to/textbooks",
    parsed_dir="path/to/parsed_textbooks"
)

# Process all PDFs in the directory
manager.process_directory()

# Print summary
print("\nProcessed Textbooks:")
for name in manager.get_all_textbook_names():
    textbook = manager.get_textbook(name)
    print(f"- {name}: {textbook.total_pages} pages")

# Example: Generate questions from random pages
from lib.question_generator import QuestionGenerator
generator = QuestionGenerator()

async def generate_questions_from_textbooks():
    # Get random pages from each textbook
    for textbook in manager.get_all_textbooks():
        page = manager.get_random_page(textbook.name)
        if page:
            print(f"\nGenerating questions from {textbook.name}, page {page.page_number}")
            questions = await generator.generate_questions(
                page.content,
                num_questions=2,
                verify=True
            )
            
            for i, q in enumerate(questions, 1):
                print(f"\nQuestion {i}:")
                print(q.question)
                print(f"\nDomain: {q.domain.value if q.domain else 'Unknown'}")

# Run it
if __name__ == "__main__":
    import asyncio
    asyncio.run(generate_questions_from_textbooks()) 