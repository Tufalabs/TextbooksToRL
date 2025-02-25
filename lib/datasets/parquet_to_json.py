import pandas as pd
import json
from pathlib import Path

def parquet_to_json(input_path: str, output_path: str, orient: str = 'records') -> None:
    """
    Convert a Parquet file to JSON format.
    
    Args:
        input_path (str): Path to the input Parquet file
        output_path (str): Path where the JSON file will be saved
        orient (str): The format of the JSON output. Default is 'records'.
                     Options include: 'records', 'split', 'index', 'columns', 'values'
    """
    try:
        # Read the Parquet file
        df = pd.read_parquet(input_path)
        
        # Convert to JSON
        json_str = df.to_json(orient=orient)
        
        # Parse the JSON string to ensure it's properly formatted
        json_data = json.loads(json_str)
        
        # Write to file with proper indentation
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4)
            
        print(f"Successfully converted {input_path} to {output_path}")
        
    except Exception as e:
        print(f"Error converting file: {str(e)}")

def main():
    # Example usage
    input_file = "test-00000-of-00001.parquet"
    output_file = "output.json"
    
    parquet_to_json(input_file, output_file)

if __name__ == "__main__":
    main()
