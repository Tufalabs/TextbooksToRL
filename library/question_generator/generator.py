from typing import List, Optional
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.tobyawesomeailibrary.inference import generate_text
from src.tobyawesomeailibrary.eval_response import evaluate_text
from .models import QuestionAnswer, ValidationResult
from .prompt_templates import QuestionPromptTemplates
from .parsers import ResponseParser

class QuestionGenerator:
    """Main class for generating and managing questions."""
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name
        self.parser = ResponseParser()
        self.templates = QuestionPromptTemplates()

    async def generate_questions(
        self, 
        passage: str, 
        num_questions: int = 3,
        verify: bool = True,
        verification_threshold: float = 0.8
    ) -> List[QuestionAnswer]:
        """
        Generate questions from a passage and return structured data.
        
        Args:
            passage: The text passage to generate questions from
            num_questions: Number of questions to generate
            verify: Whether to verify solutions are correct
            verification_threshold: Minimum score for a question to be considered valid
        """
        prompt = self.templates.question_generation(passage, num_questions * 2 if verify else num_questions)
        response = await generate_text(model=self.model_name, prompt=prompt)
        
        qa_pairs = self.parser.extract_qa_pairs(response)
        verified_pairs = []

        for qa in qa_pairs:
            if verify:
                # Verify the solution is correct by having the model solve it independently
                is_valid = await self._verify_question_solution(qa, passage, verification_threshold)
                if is_valid:
                    await self._add_hints(qa)
                    verified_pairs.append(qa)
                    if len(verified_pairs) >= num_questions:
                        break
            else:
                await self._add_hints(qa)
                verified_pairs.append(qa)
                if len(verified_pairs) >= num_questions:
                    break

        return verified_pairs

    async def _verify_question_solution(
        self, 
        qa: QuestionAnswer, 
        source_text: str,
        threshold: float
    ) -> bool:
        """Verify a question-solution pair is valid by having the model solve it independently."""
        verification_prompt = f"""
        Given this source text:
        {source_text}

        Please solve this question:
        {qa.question}

        Provide a detailed solution.
        """
        
        # Generate a new solution independently
        model_solution = await generate_text(model=self.model_name, prompt=verification_prompt)
        
        # Validate the original solution against the model's solution
        validation_result = await self.validate_solution(
            qa.question,
            qa.solution,
            model_solution
        )
        
        return validation_result.score >= threshold

    async def _add_hints(self, qa: QuestionAnswer) -> None:
        """Add hints to a QuestionAnswer object."""
        prompt = self.templates.hint_generation(qa.question)
        hints_text = await generate_text(model=self.model_name, prompt=prompt)
        qa.hints = self.parser.extract_hints(hints_text)

    async def validate_solution(self, 
                              question: str, 
                              student_solution: str, 
                              correct_solution: str) -> ValidationResult:
        """Validate a student's solution against the correct solution."""
        eval_result = await evaluate_text(
            self.model_name,
            student_solution,
            correct_solution
        )
        
        return ValidationResult(
            is_correct=eval_result[0] == 1,
            score=float(eval_result[0]),
            feedback=None  # Could be extended to include feedback
        ) 