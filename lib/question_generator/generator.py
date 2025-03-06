from typing import List, Optional
import sys
import os
import json
from datetime import datetime
import asyncio
from sympy import simplify, sympify
from sympy.parsing.latex import parse_latex
import unittest

# Adjust the path so that the inference/evaluation modules can be imported.
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.tobyawesomeailibrary.inference import generate_text
from src.tobyawesomeailibrary.eval_response import evaluate_text
from lib.question_generator.models import QuestionAnswer, ValidationResult, QuestionDomain, QuestionDifficulty
from lib.question_generator.prompt_templates import QuestionPromptTemplates
from lib.question_generator.parsers import ResponseParser

# -----------------------------------------------------------------------------
# Utility Functions for LaTeX Processing and Math Equivalence Checking
# -----------------------------------------------------------------------------

def extract_boxed_expression(latex_str: str) -> str:
    """
    Extract the expression inside the \boxed{...} command, handling nested braces.
    If not found, returns the entire string.
    """
    latex_str = latex_str.strip()
    
    if "\\boxed{" not in latex_str:
        return latex_str.strip()
    
    start_idx = latex_str.index("\\boxed{") + 7  # len("\\boxed{")
    brace_count = 1
    end_idx = start_idx
    
    while brace_count > 0 and end_idx < len(latex_str):
        if latex_str[end_idx] == '{':
            brace_count += 1
        elif latex_str[end_idx] == '}':
            brace_count -= 1
        end_idx += 1
    
    if brace_count == 0:
        return latex_str[start_idx:end_idx-1].strip()
    return latex_str.strip()

def _parse_math_expr(expr_str: str):
    """
    Try parsing the math expression using sympy's LaTeX parser.
    If that fails (e.g. antlr4 isn't installed), fall back to sympy.sympify
    after replacing '^' with '**' for exponentiation.
    """
    try:
        return parse_latex(expr_str)
    except Exception:
        expr_str_modified = expr_str.replace('^', '**')
        return sympify(expr_str_modified)

def check_math_equivalence(expected_latex: str, verification_latex: str) -> bool:
    """
    Check if two LaTeX math expressions are mathematically equivalent.
    First, ensure both expressions have a \boxed{...} wrapper.
    Then extract the inner expression and attempt to parse using Sympy.
    If parsing fails, fall back to a normalized string comparison.
    """
    has_boxed_expected = "\\boxed{" in expected_latex
    has_boxed_verification = "\\boxed{" in verification_latex
    if has_boxed_expected != has_boxed_verification:
        return False

    # Extract boxed expressions first
    expected_inner = extract_boxed_expression(expected_latex)
    verification_inner = extract_boxed_expression(verification_latex)
    
    # Handle equals signs by taking the right-most part
    if "=" in expected_inner:
        expected_inner = expected_inner.split("=")[-1].strip()
    if "=" in verification_inner:
        verification_inner = verification_inner.split("=")[-1].strip()

    try:
        expected_expr = _parse_math_expr(expected_inner)
        verification_expr = _parse_math_expr(verification_inner)
    except Exception:
        normalized_expected = expected_inner.replace(" ", "").lower()
        normalized_verification = verification_inner.replace(" ", "").lower()
        return normalized_expected == normalized_verification

    difference = simplify(expected_expr - verification_expr)
    return difference == 0

# -----------------------------------------------------------------------------
# Main Class for Generating and Managing Questions
# -----------------------------------------------------------------------------

class QuestionGenerator:
    """Main class for generating and managing questions."""
    
    def __init__(self, model_name: str = "gpt-4o-mini", output_dir: str = "generated_questions", verification_model: Optional[str] = None):
        self.model_name = model_name
        self.verification_model = verification_model or model_name
        self.parser = ResponseParser()
        self.templates = QuestionPromptTemplates()
        self.output_dir = output_dir
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
        classify_domain: bool = False,
        verification_model: Optional[str] = None
    ) -> List[QuestionAnswer]:
        """Generate questions from a passage and return structured data."""
        current_verification_model = verification_model or self.verification_model
        
        # Generate questions using the prompt template.
        prompt = self.templates.question_generation(passage, num_questions, difficulty)
        response = await generate_text(model=self.model_name, prompt=prompt)
        
        qa_pairs = self.parser.extract_qa_pairs(response)
        print(f"Generated {len(qa_pairs)} initial questions at {difficulty.value} level")
        
        verified_pairs = []
        for qa in qa_pairs:
            if verify:
                is_valid = await self._verify_question_solution(
                    qa, 
                    passage, 
                    verification_threshold,
                    current_verification_model,
                    verification_attempts=3
                )
                qa.is_valid = is_valid
                if is_valid:
                    if add_hints:
                        await self._add_hints(qa, difficulty)
                    if classify_domain:
                        await self._classify_domain(qa)
                    if src:
                        qa.source = src
                    verified_pairs.append(qa)
            else:
                qa.is_valid = None
                if add_hints:
                    await self._add_hints(qa, difficulty)
                if classify_domain:
                    await self._classify_domain(qa)
                if src:
                    qa.source = src
                verified_pairs.append(qa)

        # Save questions to JSON files.
        if save_json:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            diff_serializable = difficulty.value if hasattr(difficulty, "value") else difficulty
            
            # Calculate and print validation percentage
            if verify:
                valid_count = len(verified_pairs)
                total_count = len(qa_pairs)
                valid_percentage = (valid_count / total_count) * 100 if total_count > 0 else 0
                print(f"Valid questions: {valid_count}/{total_count} ({valid_percentage:.1f}%)")
            
            for i, qa in enumerate(verified_pairs):
                boxed_solution = None
                if "\\boxed{" in qa.solution:
                    try:
                        last_start = qa.solution.rindex("\\boxed{") + 7
                        brace_count = 1
                        last_end = last_start
                        while brace_count > 0 and last_end < len(qa.solution):
                            if qa.solution[last_end] == '{':
                                brace_count += 1
                            elif qa.solution[last_end] == '}':
                                brace_count -= 1
                            last_end += 1
                        boxed_solution = qa.solution[last_start:last_end-1]
                    except ValueError:
                        pass

                question_dict = {
                    "source": qa.source,
                    "question": qa.question,
                    "solution": qa.solution,
                    "hints": qa.hints,
                    "difficulty": diff_serializable,
                    "domain": qa.domain.value if qa.domain else None,
                    "timestamp": timestamp,
                    "difficulty_description": difficulty.get_description(),
                    "model": self.model_name,
                    "boxed_solution": boxed_solution,
                    "validated": qa.is_valid
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
            print(f"Warning: Invalid domain '{domain_str}', defaulting to OTHER")
            qa.domain = QuestionDomain.OTHER

    async def _verify_question_solution(
        self, 
        qa: QuestionAnswer, 
        source_text: str,
        threshold: float,
        verification_model: str,
        verification_attempts: int = 3
    ) -> bool:
        """
        Verify a question's solution with multiple concurrent attempts.
        Uses the improved math equivalence check to compare solutions.
        """
        verification_prompt = f"""
        Reference text:
        {source_text}

        Your answer must be precise and include a final answer in a \\boxed{{...}} format.

        Question:
        {qa.question}

        Solve the problem step by step.
        """
        verification_tasks = [
            generate_text(model=verification_model, prompt=verification_prompt)
            for _ in range(verification_attempts)
        ]
        model_solutions = await asyncio.gather(*verification_tasks)
        original_answer = qa.solution

        print("\n=== Solution Comparison ===")
        print(f"Original boxed: {extract_boxed_expression(original_answer)}")
        
        for i, model_solution in enumerate(model_solutions, 1):
            is_equivalent = check_math_equivalence(original_answer, model_solution)
            print(f"Verification {i} boxed: {extract_boxed_expression(model_solution)}")
            print(f"Equivalent: {is_equivalent}")
            
            if is_equivalent:
                return True
        return False

    async def _add_hints(self, qa: QuestionAnswer, difficulty: QuestionDifficulty = QuestionDifficulty.UNDERGRAD) -> None:
        """Add hints to a QuestionAnswer object."""
        prompt = self.templates.hint_generation(qa.question, difficulty)
        hints_text = await generate_text(model=self.model_name, prompt=prompt)
        qa.hints = self.parser.extract_hints(hints_text)

    async def validate_solution(self, question: str, student_solution: str, correct_solution: str) -> ValidationResult:
        """Validate a student's solution against the correct solution."""
        eval_result = await evaluate_text(self.model_name, student_solution, correct_solution)
        boxed_solution = None
        if "\\boxed{" in correct_solution:
            try:
                last_start = correct_solution.rindex("\\boxed{") + 7
                last_end = correct_solution.index("}", last_start)
                boxed_solution = correct_solution[last_start:last_end]
            except ValueError:
                pass
        
        return ValidationResult(
            is_correct=eval_result[0] == 1,
            score=float(eval_result[0]),
            feedback=None,
            boxed_solution=boxed_solution
        )

# -----------------------------------------------------------------------------
# Unit Tests for the Math Equivalence Checker
# -----------------------------------------------------------------------------

class TestMathEquivalence(unittest.TestCase):
    def test_equivalent_simple(self):
        expr1 = r"\boxed{1+2}"
        expr2 = r"\boxed{3}"
        self.assertTrue(check_math_equivalence(expr1, expr2))

    def test_equivalent_with_spaces(self):
        expr1 = r"\boxed{1 + 2}"
        expr2 = r"\boxed{ 3 }"
        self.assertTrue(check_math_equivalence(expr1, expr2))

    def test_non_equivalent(self):
        expr1 = r"\boxed{1+2}"
        expr2 = r"\boxed{4}"
        self.assertFalse(check_math_equivalence(expr1, expr2))

    def test_equivalent_complex(self):
        expr1 = r"\boxed{(x+1)^2}"
        expr2 = r"\boxed{x^2+2*x+1}"
        self.assertTrue(check_math_equivalence(expr1, expr2))

    def test_malformed_latex(self):
        # If one expression lacks \boxed{}, they should not be equivalent.
        expr1 = "1+2"
        expr2 = r"\boxed{3}"
        self.assertFalse(check_math_equivalence(expr1, expr2))

    def test_equivalent_with_equals(self):
        expr1 = r"\boxed{x^2 + 1}"
        expr2 = r"\boxed{f(x) = x^2 + 1}"
        self.assertTrue(check_math_equivalence(expr1, expr2))

    def test_equivalent_multiple_equals(self):
        expr1 = r"\boxed{x = y = 1}"
        expr2 = r"\boxed{1}"
        self.assertTrue(check_math_equivalence(expr1, expr2))

# -----------------------------------------------------------------------------
# Run Unit Tests if executed as main
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    unittest.main()
