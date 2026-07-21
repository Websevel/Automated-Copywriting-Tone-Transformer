"""
prompt_compiler.py
-------------------
Builds the "Master Instruction Template" and injects user variables into it.
This is the "Protecting Brand Voice" step from the project checklist:
the end user only supplies raw facts (product, tone, platform) — this
module is the gatekeeper that enforces the actual structured prompt.
"""

# Platform-specific rules the model must follow.
# Each platform gets its own character limit and style hint.
PLATFORM_RULES = {
    "linkedin": {
        "max_chars": 1300,
        "style_hint": "professional, thought-leadership style, can use line breaks",
    },
    "instagram": {
        "max_chars": 2200,
        "style_hint": "casual, emoji-friendly, hook in the first line, add relevant hashtags",
    },
    "twitter": {
        "max_chars": 280,
        "style_hint": "punchy, single idea, no fluff",
    },
    "email": {
        "max_chars": 1500,
        "style_hint": "includes a subject line, greeting, body, and call-to-action",
    },
}


def compile_prompt(product_name: str, platform: str, tone: str) -> str:
    """
    Merges user variables into the hidden master template.
    Returns the final prompt string ready to send to the model.
    """
    platform_key = platform.lower().strip()
    rules = PLATFORM_RULES.get(
        platform_key,
        {"max_chars": 1000, "style_hint": "clear and professional"},
    )

    master_template = f"""You are a senior marketing copywriter.

TASK: Write marketing copy for the following product, strictly for the platform specified.

Product: {product_name}
Platform: {platform}
Tone: {tone}

STRICT RULES YOU MUST FOLLOW:
- Maximum length: {rules['max_chars']} characters. Do not exceed this.
- Style for this platform: {rules['style_hint']}
- Do not include any preamble like "Here is your copy:" — output ONLY the final copy.
- Do not use markdown formatting like ** or #.

Write the copy now."""

    return master_template


def get_char_limit(platform: str) -> int:
    return PLATFORM_RULES.get(platform.lower().strip(), {"max_chars": 1000})["max_chars"]
