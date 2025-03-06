import logging
import sys
from pathlib import Path
import fitz  # PyMuPDF
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import traceback
import os

def setup_logging():
    """Setup logging to both file and console with more detailed formatting."""
    # Clear previous log file if it exists
    log_path = Path('pdf_processing.log')
    if log_path.exists():
        log_path.unlink()
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Setup file handler
    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    
    # Setup console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Setup logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # Remove existing handlers if any
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

def extract_text_with_pymupdf(pdf_path: Path, output_path: Path) -> bool:
    """Extract text from PDF using PyMuPDF (fitz).
    
    Args:
        pdf_path: Path to the PDF file
        output_path: Path where to save the text file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Verify file exists before attempting to open
        if not pdf_path.exists():
            logging.error(f"File does not exist: {pdf_path}")
            return False
            
        # Open the PDF
        doc = fitz.open(pdf_path)
        
        extracted_text = []
        # Process each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            # Extract text with improved layout preservation
            text = page.get_text()
            if text.strip():  # Only add if text is not empty
                extracted_text.append(text)
                
        # Check if we got anything meaningful
        if not extracted_text:
            logging.warning(f"No text extracted from {pdf_path.name}")
            doc.close()
            return False
            
        # Write combined text to output file
        with open(output_path, 'w', encoding='utf-8', errors='replace') as txt_file:
            txt_file.write('\n\n'.join(extracted_text))
            
        doc.close()
        return True
    
    except Exception as e:
        logging.error(f"PyMuPDF extraction failed for {pdf_path.name}: {str(e)}")
        logging.debug(traceback.format_exc())
        return False

def process_pdf(pdf_path: Path, output_path: Path) -> bool:
    """Process a single PDF file to text.
    
    Args:
        pdf_path: Path to the PDF file
        output_path: Path where to save the text file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        logging.info(f"Processing: {pdf_path}")
        
        # First attempt: PyMuPDF
        if extract_text_with_pymupdf(pdf_path, output_path):
            logging.info(f"Successfully processed {pdf_path.name} with PyMuPDF")
            
            # Quick verification - check file size and content
            if output_path.stat().st_size > 100:  # Arbitrary minimum size
                with open(output_path, 'r', encoding='utf-8', errors='replace') as f:
                    # Check first few lines for actual content
                    sample = f.read(1000)
                    if len(sample.split()) > 20:  # At least some words
                        return True
            
            logging.warning(f"Extraction produced too little content for {pdf_path.name}")
        
        # If we get here, the primary method failed or produced insufficient content
        logging.warning(f"Could not extract meaningful text from {pdf_path.name}")
        return False
        
    except Exception as e:
        logging.error(f"Error processing PDF {pdf_path.name}: {str(e)}")
        logging.debug(traceback.format_exc())
        return False

def worker(pdf_file, input_path, output_path):
    """Worker function for thread pool."""
    try:
        pdf_path = input_path / pdf_file.name  # Use name to create proper path
        output_file = output_path / f"{pdf_file.stem}.txt"
        success = process_pdf(pdf_path, output_file)
        return pdf_file.name, success
    except Exception as e:
        logging.error(f"Worker failed for {pdf_file.name}: {str(e)}")
        return pdf_file.name, False

def process_pdfs(input_dir: str = "textbooks/pdf", output_dir: str = "textbooks/txt", max_workers: int = 4):
    """Process all PDFs in input directory to text files in output directory with parallel processing.
    
    Args:
        input_dir: Directory containing PDF files
        output_dir: Directory for output text files
        max_workers: Maximum number of worker threads
    """
    logger = setup_logging()
    
    # Create Path objects - resolve to absolute paths to avoid path issues
    input_path = Path(input_dir).resolve()
    output_path = Path(output_dir).resolve()
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Debug path information
    logging.info(f"Input directory (absolute): {input_path}")
    logging.info(f"Output directory (absolute): {output_path}")
    
    try:
        # Get all PDF files directly from the directory
        pdf_files = list(input_path.glob("*.pdf"))
        
        if not pdf_files:
            logging.warning(f"No PDF files found in {input_dir}")
            # Try listing directory contents for debugging
            all_files = list(input_path.iterdir())
            logging.info(f"Directory contents: {[f.name for f in all_files]}")
            return
            
        logging.info(f"Found {len(pdf_files)} PDF files to process")
        
        # Process a single PDF first as a test case
        if pdf_files:
            test_pdf = pdf_files[0]
            logging.info(f"Testing with first PDF: {test_pdf.name}")
            test_output = output_path / f"{test_pdf.stem}_test.txt"
            success = process_pdf(test_pdf, test_output)
            if success:
                logging.info("Test processing successful, continuing with batch processing")
            else:
                logging.warning("Test processing failed, checking for issues before continuing")
        
        # Process PDFs in parallel
        results = {"success": 0, "failed": 0}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all tasks and wrap with tqdm for progress bar
            futures = {executor.submit(worker, pdf_file, input_path, output_path): pdf_file.name 
                      for pdf_file in pdf_files}
            
            # Show progress bar
            for future in tqdm(futures, desc="Processing PDFs", unit="file"):
                pdf_name, success = future.result()
                if success:
                    results["success"] += 1
                else:
                    results["failed"] += 1
                
        # Log summary
        logger.info(f"PDF processing complete! Successfully processed: {results['success']}, Failed: {results['failed']}")
        
        # List failed files if any
        if results["failed"] > 0:
            failed_files = [f for f in output_path.glob("*.txt") if f.stat().st_size < 100]
            if failed_files:
                logger.warning(f"Files with potentially insufficient content: {', '.join(f.name for f in failed_files)}")
        
    except Exception as e:
        logger.error(f"Error during processing: {str(e)}")
        logger.debug(traceback.format_exc())
        raise

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Process PDFs to text files')
    parser.add_argument('--textbooks-dir', default='textbooks/pdf', help='Directory containing PDF textbooks')
    parser.add_argument('--parsed-dir', default='textbooks/txt', help='Directory for parsed text files')
    parser.add_argument('--max-workers', type=int, default=4, help='Maximum number of parallel workers')
    
    args = parser.parse_args()
    process_pdfs(args.textbooks_dir, args.parsed_dir, args.max_workers)