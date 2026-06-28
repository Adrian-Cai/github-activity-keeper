from __future__ import annotations

from pathlib import Path

from ..utils import now
from .base import Generator


class ReadmeGenerator(Generator):
    name = "readme"

    def generate(self, repo_path: Path, config: dict) -> str | None:
        filepath = repo_path / "README.md"

        if not filepath.exists():
            return None

        ts = now().strftime("%Y-%m-%d %H:%M")
        content = filepath.read_text(encoding="utf-8")

        lines = content.splitlines()
        new_lines = []
        updated = False
        for line in lines:
            if line.lower().startswith("> last updated"):
                new_lines.append(f"> Last updated: {ts}")
                updated = True
            else:
                new_lines.append(line)

        if not updated:
            new_lines.append("")
            new_lines.append(f"> Last updated: {ts}")

        filepath.write_text("\n".join(new_lines), encoding="utf-8")
        return f"readme: {ts}"
