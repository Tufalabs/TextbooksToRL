# TextbooksToRL

A tool that automatically processes textbooks to generate structured question-answer datasets for machine learning and reinforcement learning training.

## How It Works

1. **Extract Text**: Converts PDF textbooks to text format
2. **Process Pages**: Splits content into manageable chunks (3-5 pages)
3. **Generate Questions**: Uses AI models to create questions from each chunk
4. **Verify Solutions**: Checks answers by feeding page back in with question to ensure same answer
5. **Output Dataset**: Saves structured JSON files with questions, solutions, and metadata

The tool supports multiple difficulty levels (high school → PhD) and various AI models (OpenAI, Anthropic, DeepSeek, etc.).

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Set up API keys:
```bash
export OPENAI_API_KEY='your-key'
export ANTHROPIC_API_KEY='your-key'
export DEEPSEEK_API_KEY='your-key'
export DEEPINFRA_API_KEY='your-key'
```

## Usage

### Basic Usage
```bash
# Generate questions from textbooks
uv run textbooks-to-rl --help

# Run with custom settings
uv run textbooks-to-rl \
  --model "Qwen/QwQ-32B" \
  --output-dir "my_questions" \
  --difficulty undergrad \
  --verbose
```

### Step 1: Add Textbooks
Place PDF files in `textbooks/pdfs/` or process them:
```bash
uv run python scripts/process_pdfs.py
```

### Step 2: Generate Questions
```bash
# Basic generation
uv run textbooks-to-rl

# With custom options
uv run textbooks-to-rl \
  --pages-per-group 5 \
  --batch-size 50 \
  --questions-per-chunk 8 \
  --difficulty grad \
  --no-verify
```

### Step 3: Filter Questions (Optional)
```bash
uv run python scripts/filter.py \
  --folders generated_questions \
  --output-dir filtered_results \
  --model gpt-4o-mini
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--model` | AI model for generation | Qwen/QwQ-32B |
| `--output-dir` | Output directory | generated_questions |
| `--textbooks-dir` | Textbooks directory | textbooks/txt |
| `--pages-per-group` | Pages per processing group | 3 |
| `--batch-size` | Parallel batch size | 100 |
| `--questions-per-chunk` | Questions per chunk | 10 |
| `--difficulty` | Question difficulty level | undergrad |
| `--no-verify` | Skip solution verification | False |
| `--verbose` | Enable debug logging | False |

## Development

```bash
# Install with dev dependencies
uv sync --dev

# Run code quality checks
uv run ruff check src/ --fix
uv run pytest
```