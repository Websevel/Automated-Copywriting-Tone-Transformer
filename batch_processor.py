"""
batch_processor.py
-------------------
Reads a CSV of products and generates copy for all of them concurrently.
Uses asyncio.gather + a Semaphore to avoid overwhelming the local Ollama
server with too many requests at once (the "Semaphore Gate" concept).
"""

import asyncio
import csv
import json

import ollama
from generator import generate_copy_async

MAX_CONCURRENT_REQUESTS = 3  # local models are heavier than APIs — keep this modest


async def process_row(client, semaphore, row):
    async with semaphore:
        result = await generate_copy_async(
            client,
            product_name=row["product_name"],
            platform=row["platform"],
            tone=row["tone"],
            temperature=float(row.get("temperature", 0.7)),
            top_p=float(row.get("top_p", 0.9)),
        )
        print(f"  ✓ Done: {row['product_name']} ({row['platform']})")
        return result


async def run_batch(csv_path: str, output_path: str = "batch_output.json"):
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    print(f"Loaded {len(rows)} rows from {csv_path}. Generating with up to "
          f"{MAX_CONCURRENT_REQUESTS} concurrent requests...\n")

    client = ollama.AsyncClient()
    semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

    tasks = [process_row(client, semaphore, row) for row in rows]
    results = await asyncio.gather(*tasks)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump([r.model_dump() for r in results], f, indent=2)

    print(f"\nAll done. Results saved to {output_path}")


def run_batch_sync(csv_path: str, output_path: str = "batch_output.json"):
    """Entry point called from main.py (keeps main.py free of asyncio boilerplate)."""
    asyncio.run(run_batch(csv_path, output_path))
