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
python parse_pdfs.py
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
python scripts/process_pdfs.py --textbooks-dir textbooks/pdfs --parsed-dir textbooks/txt
```

## How It Works

1. **PDF Processing**:
   - Converts PDF textbooks to text format
   - Splits content into manageable chunks

2. **Dataset Generation**:
   - Processes multiple pages in parallel
   - Uses AI models (DeepSeek, Claude, etc.) to generate Q&A pairs
   - Creates structured data suitable for RL training

3. **Batch Processing**:
   - Handles large textbooks efficiently
   - Processes pages in groups for better context
   - Runs multiple batches concurrently