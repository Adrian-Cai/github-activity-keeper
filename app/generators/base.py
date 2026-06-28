from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path


class Generator(ABC):
    name: str = ""

    @abstractmethod
    def generate(self, repo_path: Path, config: dict) -> str | None:
        ...
