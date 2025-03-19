import os
from lib.textbook_manager import TextbookManager
import argparse

def main():
    parser = argparse.ArgumentParser(description='Extract a range of pages from a textbook and save to a text file')
    parser.add_argument('textbook_name', help='Name of the textbook')
    parser.add_argument('start_page', type=int, help='Starting page number')
    parser.add_argument('end_page', type=int, help='Ending page number')
    parser.add_argument('--output-file', help='Output file path (default: extracted_pages.txt)')
    args = parser.parse_args()
    
    # Set default output file if not provided
    output_file = args.output_file if args.output_file else f"{args.textbook_name}_pages_{args.start_page}-{args.end_page}.txt"
    
    # Initialize textbook manager
    textbook_manager = TextbookManager()
    
    # Validate textbook exists
    textbook = textbook_manager.get_textbook(args.textbook_name)
    if not textbook:
        print(f"Error: Textbook '{args.textbook_name}' not found")
        return
    
    # Validate page range
    total_pages = textbook.total_pages
    start_page = max(1, min(args.start_page, total_pages))
    end_page = max(start_page, min(args.end_page, total_pages))
    
    print(f"Extracting pages {start_page} to {end_page} from '{args.textbook_name}'")
    print(f"Total pages in textbook: {total_pages}")
    
    # Combine content from all pages
    combined_content = ""
    page_count = 0
    
    for page_num in range(start_page, end_page + 1):
        current_passage = textbook_manager.get_page(args.textbook_name, page_number=page_num)
        if current_passage:
            page_count += 1
            # Add page number header
            combined_content += f"\n\n===== PAGE {page_num} =====\n\n"
            combined_content += current_passage.content
        else:
            print(f"Warning: Could not find page {page_num}")
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else '.', exist_ok=True)
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(combined_content)
    
    print(f"Successfully extracted {page_count} pages")
    print(f"Content saved to {output_file}")

if __name__ == "__main__":
    main() 