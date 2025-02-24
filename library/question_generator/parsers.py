import re
from typing import List
from .models import QuestionAnswer

class ResponseParser:
    """Class for parsing responses from the LLM."""
    
    @staticmethod
    def extract_qa_pairs(text: str) -> List[QuestionAnswer]:
        """Extract question-answer pairs from text that contains XML-like tags."""
        pattern = r'<source>(.*?)</source>.*?<question>(.*?)</question>\s*<solution>(.*?)</solution>'
        matches = re.findall(pattern, text, re.DOTALL)
        
        return [
            QuestionAnswer(
                question=question.strip(),
                solution=solution.strip(),
                source=source.strip()
            )
            for source, question, solution in matches
        ]

    @staticmethod
    def extract_hints(text: str) -> List[str]:
        """Extract hints from formatted text."""
        text = text.replace('<hints>', '').replace('</hints>', '')
        hints = [hint.strip() for hint in re.split(r'\d+\.', text) if hint.strip()]
        return hints 