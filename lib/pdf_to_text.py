from pathlib import Path
import PyPDF2

def convert_pdf_to_text(pdf_path: Path) -> str:
    """Convert a PDF file to text, preserving page markers."""
    text = []
    
    try:
        with open(pdf_path, 'rb') as file:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Get number of pages
            num_pages = len(pdf_reader.pages)
            
            # Extract text from each page
            for page_num in range(num_pages):
                # Add page marker
                text.append(f"\n<<<PAGE {page_num + 1}>>>\n")
                
                # Get page
                page = pdf_reader.pages[page_num]
                
                # Extract text from page
                text.append(page.extract_text())
                
        return "\n".join(text)
        
    except Exception as e:
        raise Exception(f"Error converting PDF to text: {str(e)}") 