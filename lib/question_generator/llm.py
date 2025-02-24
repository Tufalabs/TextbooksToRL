from typing import Optional, Tuple
from src.tobyawesomeailibrary.inference import generate_text
from src.tobyawesomeailibrary.eval_response import evaluate_text

class LLMInterface:
    """Interface for interacting with the language model."""
    
    def __init__(self, model_name: str = "gpt-4"):
        self.model_name = model_name
        self.max_completion_tokens = 1000  # Limit completion length

    async def generate(self, prompt: str) -> str:
        """Generate text from a prompt."""
        return await generate_text(
            model=self.model_name,
            prompt=prompt,
            max_tokens=self.max_completion_tokens
        )

    async def evaluate(
        self,
        student_solution: str,
        correct_solution: str
    ) -> Tuple[bool, str]:
        """Evaluate if a solution is correct (1) or incorrect (0).
        Returns:
            Tuple[bool, str]: (is_correct, feedback)
            - is_correct: True if correct, False if incorrect
            - feedback: Explanation of the evaluation
        """
        result = await evaluate_text(
            self.model_name,
            student_solution,
            correct_solution
        )
        
        # Convert to binary outcome
        is_correct = bool(int(result[0]))  # 1 -> True, 0 -> False
        feedback = result[1] if len(result) > 1 else None
        
        return is_correct, feedback 