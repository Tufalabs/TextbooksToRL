from lib.textbook_manager import TextbookManager
from typing import Optional, List
from pathlib import Path

class TextbookInterface:
    """Interface for interacting with processed textbooks."""
    
    def __init__(self, parsed_dir: str = "parsed_textbooks"):
        self.manager = TextbookManager(parsed_dir=parsed_dir)
        
    def list_available_textbooks(self) -> List[str]:
        """Get list of available textbooks."""
        return self.manager.get_all_textbook_names()
    
    def get_page(self, textbook_name: str, page_number: int) -> Optional[str]:
        """Get content of a specific page."""
        page = self.manager.get_page(textbook_name, page_number)
        return page.content if page else None
    
    def get_random_page(self, textbook_name: str) -> Optional[str]:
        """Get content of a random page."""
        page = self.manager.get_random_page(textbook_name)
        return page.content if page else None
    
    def get_page_range(self, textbook_name: str, start: int, end: int) -> List[str]:
        """Get content from a range of pages."""
        pages = self.manager.get_page_range(textbook_name, start, end)
        return [page.content for page in pages]
    
    def search_textbooks(self, query: str) -> List[tuple[str, int, str]]:
        """Search all textbooks for content."""
        results = self.manager.search_content(query)
        return [(page.textbook_name, page.page_number, page.content) for page in results]

# Example usage
if __name__ == "__main__":
    interface = TextbookInterface()
    
    # List available textbooks
    print("Available textbooks:")
    for book in interface.list_available_textbooks():
        print(f"- {book}")
    
    # Example: Get a specific page
    textbook = interface.list_available_textbooks()[0]  # First textbook
    content = interface.get_page(textbook, 1)
    if content:
        print(f"\nFirst page of {textbook}:")
        print(content)
    
    # Example: Search
    results = interface.search_textbooks("calculus")
    print("\nSearch results for 'calculus':")
    for book, page, content in results:
        print(f"\nFound in {book}, page {page}:")
        print(content[:200] + "...")  # First 200 chars 