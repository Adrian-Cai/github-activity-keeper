from __future__ import annotations

import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .base import ContentGenerator

QUOTES = [
    "Keep shipping. Keep building.",
    "Consistency beats intensity.",
    "Small steps every day lead to big results.",
    "Code is poetry in motion.",
    "The best time to start was yesterday. The next best time is now.",
    "Automate everything that can be automated.",
    "Quality is not an act, it is a habit.",
    "Done is better than perfect.",
    "First, solve the problem. Then, write the code.",
    "Make it work, make it right, make it fast.",
    "Simplicity is the ultimate sophistication.",
    "Talk is cheap. Show me the code.",
    "Any fool can write code that a computer can understand. Good programmers write code that humans can understand.",
    "Premature optimization is the root of all evil.",
    "The only way to go fast is to go well.",
]


class MarkdownGenerator(ContentGenerator):
    name = "markdown"

    def generate(self, repo_path: Path, config: dict) -> Optional[str]:
        filepath = repo_path / "daily.md"
        now = datetime.now(timezone.utc).astimezone()
        quote = random.choice(config.get("quotes", QUOTES))
        line = f"- {now.strftime('%Y-%m-%d')} — {quote}\n"
        if filepath.exists():
            content = filepath.read_text(encoding="utf-8")
        else:
            content = "# Daily Quotes\n\n"
        content += line
        filepath.write_text(content, encoding="utf-8")
        date_str = now.strftime("%Y-%m-%d")
        return f"daily quote: {date_str}"
