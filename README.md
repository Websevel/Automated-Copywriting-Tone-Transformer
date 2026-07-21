# Automated Copywriting & Tone Transformer

A local, 100% free CLI tool that generates platform-specific marketing copy
from a raw product description, using Ollama running on your own machine.

## What it does
- Takes a product name, target platform (LinkedIn / Instagram / Twitter / Email), and tone.
- Compiles a structured "master prompt" that enforces platform character limits and style.
- Sends it to a local Ollama model and returns clean, ready-to-post copy.
- Supports batch mode: feed it a CSV of many products and it generates all of them
  concurrently using `asyncio`.

## Setup (Windows/Mac/Linux, VS Code)

### 1. Confirm Ollama is running
You said you already have Ollama installed. Just make sure it's running and pull a model:

```bash
ollama pull llama3
```

(Other good free options if llama3 is slow on your machine: `mistral`, `phi3`, `gemma2`.
If you use a different model, change `MODEL_NAME` in `generator.py`.)

### 2. Open the project folder in VS Code
File → Open Folder → select `copywriter_project`.

### 3. Create a virtual environment (recommended, keeps things clean)
Open a terminal inside VS Code (`` Ctrl+` ``) and run:

```bash
python -m venv venv
```

Activate it:
- Windows: `venv\Scripts\activate`
- Mac/Linux: `source venv/bin/activate`

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

## Running it

### Single product
```bash
python main.py --product "Wireless Noise-Cancelling Headphones" --platform instagram --tone witty
```

Optional creativity controls:
```bash
python main.py --product "Standing Desk" --platform linkedin --tone professional --temperature 0.3 --top_p 0.85
```

### Batch mode (many products at once)
A sample `products.csv` is included. Just run:
```bash
python main.py --batch products.csv
```

This will generate copy for every row concurrently and save results to `batch_output.json`.

### GUI mode (Streamlit)
A simple local web interface is included too — same logic, just a form instead of flags:
```bash
streamlit run app.py
```
This opens a browser tab (usually `http://localhost:8501`) with fields for product, platform,
tone, and sliders for temperature/top_p. Still 100% local and free — Streamlit just renders
the page in your browser, no data leaves your machine.

## Files in this project
| File | Purpose |
|---|---|
| `main.py` | CLI entry point (argparse) |
| `app.py` | Streamlit GUI front-end |
| `prompt_compiler.py` | Builds the master prompt + platform rules |
| `generator.py` | Calls Ollama (sync + async) |
| `batch_processor.py` | Concurrent batch generation from CSV |
| `models.py` | Pydantic schemas for validating output |
| `products.csv` | Sample batch input |

## Note on model name
`generator.py` defaults to `MODEL_NAME = "llama3"`. If you're using `phi3` (or another model),
change that line to match whatever `ollama list` shows on your machine.

## Things to experiment with (from the assignment's conclusion)
- Compare `--temperature 0.2` vs `--temperature 0.9` on the same product/platform — notice
  how much the wording varies.
- Try the same product on `twitter` vs `linkedin` and see how the length/style constraints
  change the output.
- Increase `MAX_CONCURRENT_REQUESTS` in `batch_processor.py` and see if your machine can
  handle it — local models are heavier than a hosted API, so there's a real limit here.

## Cost
$0. Everything runs locally through Ollama — no API keys, no billing.
