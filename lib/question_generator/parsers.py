import re
from typing import List
from .models import QuestionAnswer

class ResponseParser:
    """Class for parsing responses from the LLM."""
    
    @staticmethod
    def extract_qa_pairs(text: str) -> List[QuestionAnswer]:
        """Extract question-answer pairs from text that contains XML-like tags."""
        # Pattern to match question and solution groups, with optional source
        pattern = r'(?:<source>(.*?)</source>\s*)?<question>(.*?)</question>\s*<solution>(.*?)</solution>'
        matches = re.findall(pattern, text, re.DOTALL)
        
        print(f"Found {len(matches)} question-answer pairs in text")  # Debug print
        
        # Track used questions to avoid duplicates
        seen_questions = set()
        qa_pairs = []
        
        for match in matches:
            # If source is present, it's in match[0], otherwise it's an empty string
            source, question, solution = match
            question_clean = question.strip()
            
            # Skip if we've seen this question before
            if question_clean in seen_questions:
                continue
                
            seen_questions.add(question_clean)
            
            qa = QuestionAnswer(
                question=question_clean,
                solution=solution.strip(),
                source=source.strip() or None  # Convert empty string to None
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