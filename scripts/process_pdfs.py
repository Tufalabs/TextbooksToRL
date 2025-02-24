import logging
import sys
from pathlib import Path
import PyPDF2

def setup_logging():
    """Setup logging to both file and console."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('pdf_processing.log')
        ]
    )

def process_pdf(pdf_path: Path, output_path: Path) -> None:
    """Convert a single PDF file to text.
    
    Args:
        pdf_path: Path to the PDF file
        output_path: Path where to save the text file
    """
    try:
        with open(pdf_path, 'rb') as pdf_file:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Extract text from all pages
            text = []
            for page in pdf_reader.pages:
                text.append(page.extract_text())
            
            # Write combined text to output file
            with open(output_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write('\n'.join(text))
                
    except Exception as e:
        logging.error(f"Error processing PDF {pdf_path}: {str(e)}")
        raise

def process_pdfs(input_dir: str = "textbooks/pdf", output_dir: str = "textbooks/txt"):
    """Process all PDFs in input directory to text files in output directory."""
    setup_logging()
    logger = logging.getLogger(__name__)
    
    # Create Path objects
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    try:
        # Get all PDF files
        pdf_files = list(input_path.glob("*.pdf"))
        logger.info(f"Found {len(pdf_files)} PDF files to process")
        
        # Process each PDF
        for pdf_file in pdf_files:
            try:
                output_file = output_path / f"{pdf_file.stem}.txt"
                process_pdf(pdf_file, output_file)
                logger.info(f"Processed {pdf_file.name}")
            except Exception as e:
                logger.error(f"Failed to process {pdf_file.name}: {str(e)}")
                continue
        
        logger.info("PDF processing complete!")
        
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process PDFs to text files')
    parser.add_argument('--textbooks-dir', default='textbooks/pdf', help='Directory containing PDF textbooks')
    parser.add_argument('--parsed-dir', default='textbooks/txt', help='Directory for parsed text files')
    
    args = parser.parse_args()
    process_pdfs(args.textbooks_dir, args.parsed_dir) 