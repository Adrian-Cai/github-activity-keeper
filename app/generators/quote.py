from __future__ import annotations

import random
from pathlib import Path

from ..utils import now
from .base import Generator

QUOTES = [
    "Ship small, iterate fast.",
    "Tests are documentation.",
    "Keep learning.",
    "Consistency beats intensity.",
    "Small steps every day lead to big results.",
    "Code is poetry in motion.",
    "Automate everything that can be automated.",
    "Quality is not an act, it is a habit.",
    "Done is better than perfect.",
    "First, solve the problem. Then, write the code.",
    "Make it work, make it right, make it fast.",
    "Simplicity is the ultimate sophistication.",
    "Talk is cheap. Show me the code.",
    "Premature optimization is the root of all evil.",
    "The only way to go fast is to go well.",
    "Write code for humans first, computers second.",
    "A commit a day keeps the burnout away.",
    "Refactor mercilessly.",
    "Document your decisions, not your code.",
    "Good code is its own best documentation.",
]


class QuoteGenerator(Generator):
    name = "quote"

    def generate(self, repo_path: Path, config: dict) -> str | None:
        filepath = repo_path / "data" / "quotes.md"
        filepath.parent.mkdir(parents=True, exist_ok=True)

        quote = random.choice(config.get("quotes", QUOTES))
        line = f"> {quote}\n\n"

        if filepath.exists():
            content = filepath.read_text(encoding="utf-8")
        else:
            content = "# Quotes\n\n"
        content += line
        filepath.write_text(content, encoding="utf-8")
        return f"quote: {quote}"
