"""
models.py
---------
Defines the strict output shape we expect from the model using Pydantic.
This is the "Define the Pydantic Models" step from the project checklist.
"""

from pydantic import BaseModel, Field


class CopyRequest(BaseModel):
    """What the user asked for."""
    product_name: str
    platform: str
    tone: str
    temperature: float = Field(default=0.7, ge=0.0, le=1.5)
    top_p: float = Field(default=0.9, ge=0.0, le=1.0)


class CopyResult(BaseModel):
    """What we generated, plus metadata for auditing/debugging."""
    product_name: str
    platform: str
    tone: str
    generated_copy: str
    char_count: int
    within_limit: bool
