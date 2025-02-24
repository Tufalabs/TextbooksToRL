import os
from pathlib import Path
from typing import List, Optional, Dict
import logging
from .models import Textbook, TextbookPage
import PyPDF2  # Add this import at the top

logger = logging.getLogger(__name__)

class TextbookManager:
    """Manages textbook content and access."""
    
    def __init__(
        self,
        textbooks_dir: str = "textbooks/txt",
        pdf_dir: Optional[str] = None,
    ):
        self.textbooks_dir = Path(textbooks_dir)
        self.pdf_dir = Path(pdf_dir) if pdf_dir else None
        self.textbooks: Dict[str, Textbook] = {}
        
        # Create directories if they don't exist
        self.textbooks_dir.mkdir(exist_ok=True, parents=True)
        if self.pdf_dir:
            self.pdf_dir.mkdir(exist_ok=True, parents=True)
        
        # Load all textbooks on initialization
        self._load_textbooks()

    def _load_textbooks(self) -> None:
        """Load all textbooks from the txt directory."""
        txt_files = list(self.textbooks_dir.glob("*.txt"))
        
        for txt_path in txt_files:
            name = txt_path.stem
            
            # Create Textbook object
            textbook = Textbook(
                name=name,
                path=txt_path,
                txt_path=txt_path,
                pages=[],
                total_pages=0
            )
            
            self._load_text_content(textbook)
            self.textbooks[name] = textbook

    def _load_text_content(self, textbook: Textbook) -> None:
        """Load content from txt file and split into pages."""
        try:
            with open(textbook.txt_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split content into roughly page-sized chunks (3000 characters each)
            chunk_size = 3000
            chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
            
            # Create pages
            textbook.pages = [
                TextbookPage(
                    content=chunk,
                    page_number=i+1,
                    textbook_name=textbook.name
                )
                for i, chunk in enumerate(chunks)
            ]
            textbook.total_pages = len(textbook.pages)
            
        except Exception as e:
            logger.error(f"Error loading textbook {textbook.name}: {str(e)}")
            raise

    def get_textbook(self, name: str) -> Optional[Textbook]:
        """Get a textbook by name."""
        return self.textbooks.get(name)

    def get_page(self, textbook_name: str, page_number: int) -> Optional[TextbookPage]:
        """Get a specific page from a textbook."""
        textbook = self.get_textbook(textbook_name)
        if not textbook or page_number < 1 or page_number > textbook.total_pages:
            return None
        return textbook.pages[page_number - 1]

    def get_random_page(self, textbook_name: str) -> Optional[TextbookPage]:
        """Get a random page from a textbook."""
        import random
        textbook = self.get_textbook(textbook_name)
        if not textbook or not textbook.pages:
            return None
        return random.choice(textbook.pages)

    def get_all_textbook_names(self) -> List[str]:
        """Get list of all textbook names."""
        return list(self.textbooks.keys())

    def process_directory(self) -> None:
        """Process all PDFs in the pdf directory to text files."""
        if not self.pdf_dir:
            raise ValueError("PDF directory not specified")
        
        pdf_files = list(self.pdf_dir.glob("*.pdf"))
        for pdf_path in pdf_files:
            try:
                # Process PDF to text
                output_path = self.textbooks_dir / f"{pdf_path.stem}.txt"
                self._process_pdf(pdf_path, output_path)
                logger.info(f"Processed {pdf_path.name}")
            except Exception as e:
                logger.error(f"Error processing {pdf_path.name}: {str(e)}")
                raise

    def _process_pdf(self, pdf_path: Path, output_path: Path) -> None:
        """Convert a PDF file to text."""
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
            logger.error(f"Error processing PDF {pdf_path}: {str(e)}")
            raise 