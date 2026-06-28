from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from .base import ContentGenerator


class HeartbeatGenerator(ContentGenerator):
    name = "heartbeat"

    def generate(self, repo_path: Path, config: dict) -> Optional[str]:
        filename = config.get("file", "heartbeat.md")
        filepath = repo_path / filename
        now = datetime.now(timezone.utc).astimezone()
        line = f"{now.strftime('%Y-%m-%d %H:%M:%S %Z')}\n"
        if filepath.exists():
            content = filepath.read_text(encoding="utf-8")
        else:
            content = "# Heartbeat\n\n"
        content += line
        filepath.write_text(content, encoding="utf-8")
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        return f"heartbeat: {timestamp}"
