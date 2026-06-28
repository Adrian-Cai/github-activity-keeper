from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class ContentGenerator(ABC):
    name: str = ""

    @abstractmethod
    def generate(self, repo_path: Path, config: dict) -> Optional[str]:
        ...
