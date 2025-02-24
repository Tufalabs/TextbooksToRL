import os
from pathlib import Path
import random
from typing import List, Optional, Dict
import logging
from .models import Textbook, TextbookPage
from ..pdf_to_text import convert_pdf_to_text  # Assuming this is your existing converter

logger = logging.getLogger(__name__)

class TextbookManager:
    """Manages textbook content and access."""
    
    def __init__(
        self,
        textbooks_dir: str = "textbooks",
        parsed_dir: str = "parsed_textbooks"
    ):
        self.textbooks_dir = Path(textbooks_dir)
        self.parsed_dir = Path(parsed_dir)
        self.parsed_dir.mkdir(exist_ok=True)
        self.textbooks: Dict[str, Textbook] = {}
        
        # Create directories if they don't exist
        self.textbooks_dir.mkdir(exist_ok=True)
        
        # Load all textbooks on initialization
        self._load_textbooks()

    def _load_textbooks(self) -> None:
        """Load all textbooks from the textbooks directory."""
        pdf_files = list(self.textbooks_dir.glob("*.pdf"))
        
        for pdf_path in pdf_files:
            name = pdf_path.stem
            txt_path = self.parsed_dir / f"{name}.txt"
            
            # Create Textbook object without pages initially
            textbook = Textbook(
                name=name,
                path=pdf_path,
                txt_path=txt_path,
                pages=[],
                total_pages=0  # Will be updated when parsed
            )
            
            if textbook.is_parsed:
                self._load_parsed_content(textbook)
            else:
                self._parse_new_textbook(textbook)
                
            self.textbooks[name] = textbook

    def _parse_new_textbook(self, textbook: Textbook) -> None:
        """Parse a new textbook and save to txt."""
        logger.info(f"Parsing new textbook: {textbook.name}")
        
        try:
            # Use your existing pdf_to_text converter
            content = convert_pdf_to_text(textbook.path)
            
            # Save the content
            with open(textbook.txt_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self._load_parsed_content(textbook)
            
        except Exception as e:
            logger.error(f"Error parsing textbook {textbook.name}: {str(e)}")
            raise

    def _load_parsed_content(self, textbook: Textbook) -> None:
        """Load content from parsed txt file."""
        with open(textbook.txt_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split content into pages (assuming pages are marked with some delimiter)
        # Modify this based on your PDF to text conversion format
        pages = self._split_into_pages(content)
        
        textbook.pages = [
            TextbookPage(
                content=page_content,
                page_number=i+1,
                textbook_name=textbook.name
            )
            for i, page_content in enumerate(pages)
        ]
        textbook.total_pages = len(textbook.pages)

    def _split_into_pages(self, content: str) -> List[str]:
        """Split content into pages based on delimiter."""
        # Modify this based on your PDF to text conversion format
        # This is just an example assuming pages are separated by a specific marker
        return [page.strip() for page in content.split("<<<PAGE>>>") if page.strip()]

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
        textbook = self.get_textbook(textbook_name)
        if not textbook or not textbook.pages:
            return None
        return random.choice(textbook.pages)

    def get_page_range(
        self,
        textbook_name: str,
        start_page: int,
        end_page: int
    ) -> List[TextbookPage]:
        """Get a range of pages from a textbook."""
        textbook = self.get_textbook(textbook_name)
        if not textbook:
            return []
            
        start_page = max(1, start_page)
        end_page = min(textbook.total_pages, end_page)
        
        return textbook.pages[start_page-1:end_page]

    def search_content(self, query: str) -> List[TextbookPage]:
        """Search for content across all textbooks."""
        results = []
        for textbook in self.textbooks.values():
            for page in textbook.pages:
                if query.lower() in page.content.lower():
                    results.append(page)
        return results

    def get_all_textbooks(self) -> List[Textbook]:
        """Get list of all loaded textbooks."""
        return list(self.textbooks.values())

    def get_all_textbook_names(self) -> List[str]:
        """Get list of all textbook names."""
        return list(self.textbooks.keys())

    def process_directory(self, directory: str = None) -> None:
        """Process all PDFs in a directory."""
        if directory:
            self.textbooks_dir = Path(directory)
        
        logger.info(f"Processing all PDFs in {self.textbooks_dir}")
        pdf_files = list(self.textbooks_dir.glob("**/*.pdf"))  # Include subdirectories
        
        for pdf_path in pdf_files:
            try:
                relative_path = pdf_path.relative_to(self.textbooks_dir)
                # Use subdirectory in name if present
                name = str(relative_path.parent / relative_path.stem).replace('/', '_')
                txt_path = self.parsed_dir / f"{name}.txt"
                
                if txt_path.exists():
                    logger.info(f"Already processed {name}")
                    continue
                    
                logger.info(f"Processing {name}")
                textbook = Textbook(
                    name=name,
                    path=pdf_path,
                    txt_path=txt_path,
                    pages=[],
                    total_pages=0
                )
                
                self._parse_new_textbook(textbook)
                self.textbooks[name] = textbook
                
            except Exception as e:
                logger.error(f"Error processing {pdf_path}: {str(e)}") 