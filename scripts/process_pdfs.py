from lib.textbook_manager import TextbookManager
import logging
import sys
from pathlib import Path

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('pdf_processing.log')
        ]
    )

def process_pdfs(textbooks_dir: str = "textbooks", parsed_dir: str = "parsed_textbooks"):
    """Process all PDFs in textbooks directory to text files."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Initialize manager
        manager = TextbookManager(
            textbooks_dir=textbooks_dir,
            parsed_dir=parsed_dir
        )
        
        # Process all PDFs
        logger.info("Starting PDF processing...")
        manager.process_directory()
        
        # Print summary
        print("\nProcessed Textbooks:")
        for name in manager.get_all_textbook_names():
            textbook = manager.get_textbook(name)
            print(f"- {name}: {textbook.total_pages} pages")
            
        logger.info("PDF processing complete!")
        
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process PDFs to text files')
    parser.add_argument('--textbooks-dir', default='textbooks', help='Directory containing PDF textbooks')
    parser.add_argument('--parsed-dir', default='parsed_textbooks', help='Directory for parsed text files')
    
    args = parser.parse_args()
    process_pdfs(args.textbooks_dir, args.parsed_dir) 