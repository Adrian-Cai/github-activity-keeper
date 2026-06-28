from __future__ import annotations

from .base import ContentGenerator
from .heartbeat import HeartbeatGenerator
from .markdown import MarkdownGenerator

GENERATORS: dict[str, type[ContentGenerator]] = {
    "heartbeat": HeartbeatGenerator,
    "markdown": MarkdownGenerator,
}


def get_generator(name: str) -> ContentGenerator:
    cls = GENERATORS.get(name)
    if cls is None:
        raise ValueError(f"Unknown generator: {name}. Available: {list(GENERATORS.keys())}")
    return cls()
