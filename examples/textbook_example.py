from lib.textbook_manager import TextbookManager

# Initialize the manager
manager = TextbookManager(
    textbooks_dir="path/to/textbooks",
    parsed_dir="path/to/parsed_textbooks"
)

# Get a specific textbook
textbook = manager.get_textbook("calculus_textbook")
if textbook:
    print(f"Loaded {textbook.name} with {textbook.total_pages} pages")

# Get a specific page
page = manager.get_page("calculus_textbook", 42)
if page:
    print(f"Page {page.page_number} content:")
    print(page.content)

# Get a random page
random_page = manager.get_random_page("calculus_textbook")
if random_page:
    print(f"Random page {random_page.page_number}:")
    print(random_page.content)

# Get a range of pages
pages = manager.get_page_range("calculus_textbook", 10, 15)
for page in pages:
    print(f"Page {page.page_number}")
    print(page.content)
    print("-" * 80)

# Search across all textbooks
results = manager.search_content("derivative")
for page in results:
    print(f"Found in {page.textbook_name}, page {page.page_number}")
    print(page.content)
    print("-" * 80) 