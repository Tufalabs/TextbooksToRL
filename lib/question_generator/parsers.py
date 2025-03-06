import re
from typing import List
from .models import QuestionAnswer

class ResponseParser:
    """Class for parsing responses from the LLM."""
    
    @staticmethod
    def extract_qa_pairs(text: str) -> List[QuestionAnswer]:
        """Extract question-answer pairs from text that contains XML-like tags or markdown-style formatting."""
        print("MODEL OUTPUT: ", text)
        
        # First try XML pattern
        xml_pattern = r'(?:<source>(.*?)</source>\s*)?<question>(.*?)</question>\s*<solution>(.*?)</solution>'
        xml_matches = re.findall(xml_pattern, text, re.DOTALL)
        
        if xml_matches:
            print(f"Found {len(xml_matches)} question-answer pairs using XML pattern")
            return ResponseParser._process_matches(xml_matches)
        
        # If no XML matches, try markdown-style pattern
        # Look for ### Question X followed by ### Solution X
        md_pattern = r'### Question (?:\d+|[A-Za-z]+)(.*?)(?:---|### Solution (?:\d+|[A-Za-z]+))(.*?)(?:---|### Question|$)'
        md_matches = re.findall(md_pattern, text, re.DOTALL)
        
        if md_matches:
            # Convert to same format as XML matches (source, question, solution)
            formatted_matches = [(None, q.strip(), s.strip()) for q, s in md_matches]
            print(f"Found {len(formatted_matches)} question-answer pairs using markdown pattern")
            return ResponseParser._process_matches(formatted_matches)
            
        print("No question-answer pairs found in text")
        return []
    
    @staticmethod
    def _process_matches(matches):
        """Process matches to create QuestionAnswer objects, removing duplicates."""
        # Track used questions to avoid duplicates
        seen_questions = set()
        qa_pairs = []
        
        for match in matches:
            # If source is present, it's in match[0], otherwise it's an empty string or None
            source, question, solution = match
            question_clean = question.strip()
            
            # Skip if we've seen this question before
            if question_clean in seen_questions:
                continue
                
            seen_questions.add(question_clean)
            
            qa = QuestionAnswer(
                question=question_clean,
                solution=solution.strip(),
                source=source.strip() if source else None  # Convert empty string to None
            )
            qa_pairs.append(qa)
        
        print(f"After removing duplicates: {len(qa_pairs)} unique questions")  # Debug print
        return qa_pairs

    @staticmethod
    def extract_hints(text: str) -> List[str]:
        """Extract hints from formatted text."""
        # Remove the <hints> tags
        text = text.replace('<hints>', '').replace('</hints>', '')
        
        # Split by numbered items and clean up
        hints = [hint.strip() for hint in re.split(r'\d+\.', text) if hint.strip()]
        return hints 