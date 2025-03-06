import os
import json
import pyarrow as pa
import pyarrow.parquet as pq
import re

def extract_boxed_answer(solution):
    """Extract the answer from \boxed{...} in the solution, handling nested braces."""
    def find_matching_brace(s, start):
        count = 1
        i = start
        while i < len(s) and count > 0:
            if s[i] == '{':
                count += 1
            elif s[i] == '}':
                count -= 1
            i += 1
        return i - 1 if count == 0 else -1

    boxed_start = solution.find('\\boxed{')
    if boxed_start == -1:
        return ""
    
    content_start = boxed_start + 7  # length of '\boxed{'
    content_end = find_matching_brace(solution, content_start)
    
    if content_end == -1:
        return ""
    
    return solution[content_start:content_end]

if __name__ == '__main__':
    # Path to the MATH dataset test file
    file_path = 'MATH_prob_test_set.json'
    
    test_samples = []
    total_questions = 0
    max_samples = 256  # Set maximum number of samples
    
    # Define the math problem instruction
    instruction_following = (
        "Solve the following mathematics problem. Show your work step by step, "
        "then provide your final answer wrapped in box"
    )
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading file: {e}")
        exit(1)

    # Process each problem in the file
    for problem in data:
        if len(test_samples) >= max_samples:  # Stop after reaching max samples
            break
            
        if not isinstance(problem, dict):
            continue
        
        problem_text = problem.get("problem", "")
        solution = problem.get("solution", "")
        
        if not problem_text or not solution:
            continue

        # Extract the boxed answer as ground truth
        ground_truth = extract_boxed_answer(solution)
        
        # Build the prompt by combining the problem with the instruction
        prompt_content = f"{problem_text}\n{instruction_following}"
        
        # Build a sample dictionary for this problem
        sample = {
            "data_source": "math",
            "prompt": [{
                "role": "user",
                "content": prompt_content
            }],
            "ability": "math",
            "reward_model": {
                "style": "rule",
                "ground_truth": ground_truth
            },
            "extra_info": {
                "solution": solution,
                "level": problem.get("level", ""),
                "type": problem.get("type", "")
            }
        }
        
        test_samples.append(sample)
        total_questions += 1

    # Create output directory
    output_dir = './output'
    os.makedirs(output_dir, exist_ok=True)
    
    # Save as JSON
    with open(os.path.join(output_dir, 'test.json'), 'w') as f:
        json.dump(test_samples, f, indent=2)

    # Save as Parquet
    test_table = pa.Table.from_pylist(test_samples)
    pq.write_table(test_table, os.path.join(output_dir, 'test.parquet'))

    print(f"Math test dataset created successfully with {total_questions} questions.")
    print(f"Final dataset contains {len(test_samples)} problems.")
