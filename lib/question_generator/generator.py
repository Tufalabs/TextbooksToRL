from typing import List, Optional
import sys
import os
import json
from datetime import datetime
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from src.tobyawesomeailibrary.inference import generate_text
from src.tobyawesomeailibrary.eval_response import evaluate_text
from .models import QuestionAnswer, ValidationResult, QuestionDomain, QuestionDifficulty
from .prompt_templates import QuestionPromptTemplates
from .parsers import ResponseParser

class QuestionGenerator:
    """Main class for generating and managing questions."""
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name
        self.parser = ResponseParser()
        self.templates = QuestionPromptTemplates()
        self.output_dir = "generated_questions"
        os.makedirs(self.output_dir, exist_ok=True)

    async def generate_questions(
        self, 
        passage: str, 
        num_questions: int = 3,
        difficulty: QuestionDifficulty = QuestionDifficulty.UNDERGRAD,
        verify: bool = True,
        verification_threshold: float = 0.8,
        src: Optional[str] = None,
        save_json: bool = True,
        add_hints: bool = False,
        classify_domain: bool = False
    ) -> List[QuestionAnswer]:
        """Generate questions from a passage and return structured data."""
        # Generate extra questions if verification is enabled
        target_questions = num_questions * 2 if verify else num_questions
        prompt = self.templates.question_generation(passage, target_questions, difficulty)
        response = await generate_text(model=self.model_name, prompt=prompt)
        
        qa_pairs = self.parser.extract_qa_pairs(response)
        print(f"Generated {len(qa_pairs)} initial questions at {difficulty.value} level")
        
        verified_pairs = []
        for qa in qa_pairs:
            if verify:
                is_valid = await self._verify_question_solution(qa, passage, verification_threshold)
                if is_valid:
                    if add_hints:
                        await self._add_hints(qa, difficulty)
                    if classify_domain:
                        await self._classify_domain(qa)
                    if src:
                        qa.source = src
                    verified_pairs.append(qa)
                    if len(verified_pairs) >= num_questions:
                        break
            else:
                if add_hints:
                    await self._add_hints(qa, difficulty)
                if classify_domain:
                    await self._classify_domain(qa)
                if src:
                    qa.source = src
                verified_pairs.append(qa)
                if len(verified_pairs) >= num_questions:
                    break

        # Save questions to JSON files
        if save_json:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            for i, qa in enumerate(verified_pairs):
                question_dict = {
                    "source": qa.source,
                    "question": qa.question,
                    "solution": qa.solution,
                    "hints": qa.hints,
                    "difficulty": difficulty.value,
                    "domain": qa.domain.value if qa.domain else None,
                    "timestamp": timestamp,
                    "difficulty_description": difficulty.get_description(),
                    "model": self.model_name
                }
                
                filename = f"question_{timestamp}_{i+1}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w') as f:
                    json.dump(question_dict, f, indent=4)

        return verified_pairs

    async def _classify_domain(self, qa: QuestionAnswer) -> None:
        """Classify the domain of a question."""
        domains = [d.value for d in QuestionDomain]
        domains_str = ", ".join(domains)
        
        classification_prompt = f"""
        Classify this question into exactly one of these domains: {domains_str}

        Question: {qa.question}
        Solution: {qa.solution}

        Respond with ONLY the domain name from the list above that best matches.
        Do not include any other text in your response.
        """
        
        domain_str = await generate_text(model=self.model_name, prompt=classification_prompt)
        domain_str = domain_str.strip().lower()
        
        try:
            qa.domain = QuestionDomain(domain_str)
        except ValueError:
            print(f"Warning: Invalid domain '{domain_str}', defaulting to OTHER")  # Debug print
            qa.domain = QuestionDomain.OTHER

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
        
        model_solution = await generate_text(model=self.model_name, prompt=verification_prompt)
        validation_result = await self.validate_solution(
            qa.question,
            qa.solution,
            model_solution
        )
        
        return validation_result.score >= threshold

    async def _add_hints(
        self, 
        qa: QuestionAnswer, 
        difficulty: QuestionDifficulty = QuestionDifficulty.UNDERGRAD
    ) -> None:
        """Add hints to a QuestionAnswer object."""
        prompt = self.templates.hint_generation(qa.question, difficulty)
        hints_text = await generate_text(model=self.model_name, prompt=prompt)
        qa.hints = self.parser.extract_hints(hints_text)

    async def validate_solution(
        self, 
        question: str, 
        student_solution: str, 
        correct_solution: str
    ) -> ValidationResult:
        """Validate a student's solution against the correct solution."""
        eval_result = await evaluate_text(
            self.model_name,
            student_solution,
            correct_solution
        )
        
        return ValidationResult(
            is_correct=eval_result[0] == 1,
            score=float(eval_result[0]),
            feedback=None
        ) 