"""
generator.py
------------
Handles the actual calls to the local Ollama model.
Contains both a synchronous function (for single requests via CLI)
and an async function (for the batch pipeline).
"""

import ollama
from prompt_compiler import compile_prompt, get_char_limit
from models import CopyResult

# Change this to whatever model you've pulled locally, e.g. "llama3", "mistral", "phi3"
MODEL_NAME = "phi3"


def generate_copy(product_name: str, platform: str, tone: str,
                   temperature: float = 0.7, top_p: float = 0.9) -> CopyResult:
    """Synchronous single generation — used by the CLI's default mode."""
    prompt = compile_prompt(product_name, platform, tone)

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": temperature,
            "top_p": top_p,
        },
    )

    text = response["message"]["content"].strip()
    limit = get_char_limit(platform)

    return CopyResult(
        product_name=product_name,
        platform=platform,
        tone=tone,
        generated_copy=text,
        char_count=len(text),
        within_limit=len(text) <= limit,
    )


async def generate_copy_async(client: "ollama.AsyncClient", product_name: str,
                               platform: str, tone: str,
                               temperature: float = 0.7, top_p: float = 0.9) -> CopyResult:
    """Async version — used by the batch pipeline for concurrent requests."""
    prompt = compile_prompt(product_name, platform, tone)

    response = await client.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        options={
            "temperature": temperature,
            "top_p": top_p,
        },
    )

    text = response["message"]["content"].strip()
    limit = get_char_limit(platform)

    return CopyResult(
        product_name=product_name,
        platform=platform,
        tone=tone,
        generated_copy=text,
        char_count=len(text),
        within_limit=len(text) <= limit,
    )
