from datasets import load_dataset
import json

def get_math_test_set():
    # Load the counting_and_probability subset from MATH-lighteval
    dataset = load_dataset("digitallearninggmbh/MATH-lighteval")
    
    # Convert the dataset to a list of dictionaries
    test_data = list(dataset['test'])
    
    # Save to JSON file
    output_path = 'data/math_test_counting_probability.json'
    
    # Ensure the directory exists
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Write to JSON file with proper formatting
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)
    
    print(f"Dataset saved to {output_path}")
    return test_data

if __name__ == "__main__":
    get_math_test_set()