from dataclasses import dataclass
from pathlib import Path
from typing import Optional, List

@dataclass
class TextbookPage:
    """Represents a single page from a textbook."""
    content: str
    page_number: int
    textbook_name: str
    chapter: Optional[str] = None
    section: Optional[str] = None

@dataclass
class Textbook:
    """Represents a textbook with its content."""
    name: str
    path: Path
    txt_path: Path
    pages: List[TextbookPage]
    total_pages: int
    
    @property
    def is_parsed(self) -> bool:
        """Check if textbook has already been parsed to txt."""
        return self.txt_path.exists() 