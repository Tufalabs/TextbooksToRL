from PyPDF2 import PdfReader
import os

def extract_text_from_pdf(pdf_path, output_path):
    """
    Extract text from a PDF file and save it to a text file.
    
    Args:
        pdf_path (str): Path to the PDF file
        output_path (str): Path where the text file will be saved
    """
    # Create PDF reader object
    reader = PdfReader(pdf_path)
    
    # Open text file to write
    with open(output_path, 'w', encoding='utf-8') as output_file:
        # Iterate through all pages
        for page_num, page in enumerate(reader.pages, 1):
            # Extract text from page
            text = page.extract_text()
            
            # Write page number and text
            output_file.write(f'\n\n=== Page {page_num} ===\n\n')
            output_file.write(text)

# Example usage
if __name__ == "__main__":
    pdf_path = "textbooks/vector_calc.pdf"
    output_path = "textbooks_text/vector_calc_text.txt"
    
    try:
        # Create the output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        extract_text_from_pdf(pdf_path, output_path)
        print(f"Text successfully extracted to {output_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


