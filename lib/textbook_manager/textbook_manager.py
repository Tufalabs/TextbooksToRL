import os
from pathlib import Path
from typing import List, Optional, Dict
import logging
from .models import Textbook, TextbookPage

logger = logging.getLogger(__name__)

class TextbookManager:
    """Manages textbook content and access."""
    
    def __init__(
        self,
        textbooks_dir: str = "textbooks/txt",  # Changed default directory
    ):
        self.textbooks_dir = Path(textbooks_dir)
        self.textbooks: Dict[str, Textbook] = {}
        
        # Create directory if it doesn't exist
        self.textbooks_dir.mkdir(exist_ok=True, parents=True)
        
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