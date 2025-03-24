import os
import json
import asyncio
import argparse
from typing import List, Dict, Any
from tqdm import tqdm  # For progress bar
from lib.filter_question import QuestionFilter

async def process_batch(files: List[str], output_dir: str, model: str = "gpt-4o-mini") -> None:
    """
    Process a batch of question files and filter them.
    
    Args:
        files: List of file paths to process
        output_dir: Directory to save filtered results
        model: Model to use for filtering
    """
    filter_instance = QuestionFilter(model=model)
    tasks = []
    
    for file_path in files:
        tasks.append(process_file(file_path, filter_instance, output_dir))
    
    await asyncio.gather(*tasks)

async def process_file(file_path: str, filter_instance: QuestionFilter, output_dir: str) -> None:
    """
    Process a single question file and save if it's unsolvable.
    
    Args:
        file_path: Path to the question JSON file
        filter_instance: Instance of QuestionFilter
        output_dir: Directory to save filtered results
    """
    try:
        with open(file_path, 'r') as f:
            question_data = json.load(f)
        
        # Check if question is solvable
        is_solvable, response = await filter_instance.is_solvable(question_data)
        # print(is_solvable)
        # If the question is NOT solvable, save it to the output directory
        
        # Add filtered flag to the question data
        question_data["filtered"] = True
        question_data["filter_response"] = is_solvable
        
        # Create output file path
        filename = os.path.basename(file_path)
        output_file_path = os.path.join(output_dir, filename)
        
        # Save the filtered question
        with open(output_file_path, 'w') as f:
            json.dump(question_data, f, indent=4)
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

async def filter_folder(folder_path: str, output_base_dir: str, model: str = "gpt-4o-mini", batch_size: int = 200) -> Dict[str, int]:
    """
    Filter all question files in a folder.
    
    Args:
        folder_path: Path to folder containing question JSON files
        output_base_dir: Base directory for saving filtered results
        model: Model to use for filtering
        batch_size: Number of files to process in a batch
        
    Returns:
        Statistics about processing
    """
    # Folder name is the last part of the path
    folder_name = os.path.basename(folder_path)
    
    # Create output directory
    output_dir = os.path.join(output_base_dir, f"filtered-{folder_name}")
    os.makedirs(output_dir, exist_ok=True)
    
    # Get all JSON files in the folder
    json_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.json')]
    
    print(f"Processing {len(json_files)} files from {folder_name}")
    
    # Process files in batches
    stats = {
        "total": len(json_files),
        "processed": 0,
        "folder": folder_name
    }
    
    # Process in batches with progress bar
    for i in tqdm(range(0, len(json_files), batch_size), desc=f"Processing {folder_name}"):
        batch = json_files[i:i+batch_size]
        await process_batch(batch, output_dir, model)
        stats["processed"] += len(batch)
    
    # Count how many files were filtered
    filtered_files = [f for f in os.listdir(output_dir) if f.endswith('.json')]
    stats["filtered"] = len(filtered_files)
    
    return stats

async def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description="Filter unsolvable questions across multiple folders")
    parser.add_argument("--folders", nargs="+", required=True, help="List of folders to process")
    parser.add_argument("--output-dir", default="filtered_questions", help="Base directory for output")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model to use for filtering")
    parser.add_argument("--batch-size", type=int, default=200, help="Batch size for processing")
    args = parser.parse_args()
    
    # Create base output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Process each folder
    all_stats = []
    for folder in args.folders:
        stats = await filter_folder(folder, args.output_dir, args.model, args.batch_size)
        all_stats.append(stats)
        print(f"Folder {stats['folder']}: Processed {stats['processed']}/{stats['total']}, Filtered: {stats['filtered']}")
    
    # Save overall statistics
    with open(os.path.join(args.output_dir, "filter_stats.json"), 'w') as f:
        json.dump(all_stats, f, indent=4)
    
    print("Filtering complete!")
    print(f"Total folders processed: {len(all_stats)}")
    print(f"Total questions processed: {sum(s['total'] for s in all_stats)}")
    print(f"Total questions filtered: {sum(s['filtered'] for s in all_stats)}")

if __name__ == "__main__":
    asyncio.run(main())