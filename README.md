# RL Dataset Generator from Textbooks

A tool that automatically processes textbooks to create Reinforcement Learning (RL) datasets. This project converts PDF textbooks into structured data that can be used for training RL models.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up API keys:
```bash
export OPENAI_API_KEY='your-key'
export ANTHROPIC_API_KEY='your-key'
export DEEPSEEK_API_KEY='your-key'
export DEEPINFRA_API_KEY='your-key'
```

## Usage Instructions

### Step 1: Add Textbooks
Place your PDF textbooks in the directory:
```bash
textbooks/pdf/
```

### Step 2: Parse PDFs
First, run the parsing script to convert PDFs to text format:
```bash
python scripts/process_pdfs.py --textbooks-dir textbooks/pdfs --parsed-dir textbooks/txt
```
This will:
- Process all PDFs in `textbooks/pdf/`
- Convert them to text format
- Save the results in `textbooks/txt/`

### Step 3: Generate RL Dataset
After parsing is complete, run the main script:
```bash
python main.py
```

#### Optional Arguments
Customize the generation process:
```bash
python main.py \
  --model deepseek-chat \
  --output-dir generated_questions/DS-MATH3.0 \
  --pages-per-group 5 \
  --batch-size 100 \
  --questions-per-chunk 10
```

### Step 4: Filter Generated Questions
Filter the generated questions to identify which ones are solvable:
```bash
python filter.py --folders generated_questions/DS-MATH3.0 --output-dir filtered_results --model gpt-4o-mini
```

This will process all questions in the specified folders and add a `filter_response` field to each JSON, indicating whether the question is solvable.

#### Filter Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--folders` | List of folders containing question JSONs | Required |
| `--output-dir` | Directory to save filtered results | filtered_questions |
| `--model` | AI model for filtering | gpt-4o-mini |
| `--batch-size` | Number of files to process in parallel | 200 |

#### Filter Output
The filter script produces:
1. Filtered JSON files with added `filter_response` field (true = solvable)
2. A summary statistics file (`filter_stats.json`) showing how many questions were processed and filtered

## Command Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--model` | AI model for generation | deepseek-chat |
| `--output-dir` | Dataset output directory | generated_questions/DS-MATH3.0 |
| `--pages-per-group` | Pages per processing group | 5 |
| `--batch-size` | Parallel processing batch size | 100 |
| `--questions-per-chunk` | Questions per text chunk | 10 |

## Project Structure

##Passing PDF to text

```