from __future__ import annotations

from pathlib import Path

from ..utils import now
from .base import Generator


class HeartbeatGenerator(Generator):
    name = "heartbeat"

    def generate(self, repo_path: Path, config: dict) -> str | None:
        filepath = repo_path / "data" / "heartbeat.md"
        filepath.parent.mkdir(parents=True, exist_ok=True)

        ts = now().strftime("%Y-%m-%d %H:%M")
        line = f"{ts}\n"

        if filepath.exists():
            content = filepath.read_text(encoding="utf-8")
        else:
            content = "# Activity\n\n"
        content += line
        filepath.write_text(content, encoding="utf-8")
        return f"heartbeat: {ts}"
