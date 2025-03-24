import os
import asyncio
from typing import Dict, List, Union, Tuple, Optional
from src.tobyawesomeailibrary.inference import generate_text

class QuestionFilter:
    """
    Filter unsolvable questions using LLM judgment.
    """
    
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.prompt_template = """
Evaluate if the following math problem is solvable given the information provided.
Question: {question}

You SHOULD NOT try and solve. Just filter out respones that reference external information not provided in question e.g in figure but not provided in question.


Your task: Determine if this question is solvable with ONLY the information provided.
Respond with EXACTLY ONE WORD: either "True" if the question is solvable, or "False" if it's not solvable.
"""

    async def is_solvable(self, question: Union[str, Dict]) -> Tuple[bool, str]:
        """
        Determine if a question is solvable based on LLM judgment.
        
        Args:
            question: Either a question string or a dictionary containing the question
            
        Returns:
            Tuple of (is_solvable, response_text)
        """
        if isinstance(question, dict):
            question_text = question.get("question", "")
            if not question_text:
                print(f"No question text found in {question}")
                return False, "No question text found"
        else:
            question_text = question
        
        # Format the prompt with the question
        prompt = self.prompt_template.format(question=question_text)
        
        # Get judgment from LLM
        try:
            response = await generate_text(model=self.model, prompt=prompt)
            response = response.strip().lower()
            
            # Check if the response contains "true" or "false"
            if "true" in response:
                return True, response
            elif "false" in response:
                return False, response
            else:
                # Default to false if response is unclear
                return False, f"Unclear response: {response}"
        except Exception as e:
            return False, f"Error: {str(e)}"

async def filter_question_file(file_path: str, model: str = "gpt-4o-mini") -> Dict:
    """
    Filter a single question file to determine if it's solvable.
    
    Args:
        file_path: Path to the JSON question file
        model: The LLM model to use for judgment
        
    Returns:
        Dictionary with the judgment results
    """
    try:
        import json
        with open(file_path, 'r') as f:
            question_data = json.load(f)
        
        filter_instance = QuestionFilter(model=model)
        is_solvable, response = await filter_instance.is_solvable(question_data)
        
        return {
            "file_path": file_path,
            "is_solvable": is_solvable,
            "response": response
        }
    
    except Exception as e:
        return {
            "file_path": file_path,
            "is_solvable": False,
            "response": f"Error: {str(e)}"
        }

async def filter_directory(directory_path: str, output_path: Optional[str] = None, model: str = "gpt-4o-mini") -> Dict:
    """
    Filter all question files in a directory.
    
    Args:
        directory_path: Path to directory containing question JSON files
        output_path: Optional path to save filtered results
        model: The LLM model to use for judgment
        
    Returns:
        Dictionary with lists of solvable and unsolvable questions
    """
    result = {
        "solvable": [],
        "unsolvable": [],
        "responses": {}
    }
    
    tasks = []
    
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            tasks.append(filter_question_file(file_path, model))
    
    # Run all filtering tasks concurrently
    judgments = await asyncio.gather(*tasks)
    
    # Process results
    for judgment in judgments:
        filename = os.path.basename(judgment["file_path"])
        if judgment["is_solvable"]:
            result["solvable"].append(filename)
        else:
            result["unsolvable"].append(filename)
        result["responses"][filename] = judgment["response"]
    
    # Save results if output path is specified
    if output_path:
        import json
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
    
    return result


