from __future__ import annotations

import random

TYPES = [
    "docs", "chore", "refactor", "style", "test", "ci", "build",
]

SCOPES = [
    "project", "repo", "config", "workflow", "examples",
    "docs", "meta", "activity", "readme",
]

SUBJECTS = [
    "update activity log",
    "refresh heartbeat",
    "daily maintenance",
    "keep repository active",
    "improve examples",
    "cleanup project",
    "update documentation",
    "bump metadata",
    "auto sync",
    "periodic refresh",
    "housekeeping",
    "polish formatting",
    "refresh fixtures",
    "tidy up structure",
    "sync latest changes",
]


def generate(config: dict) -> str:
    style = config.get("style", "conventional")
    if style == "conventional":
        t = random.choice(TYPES)
        s = random.choice(SCOPES)
        v = random.choice(SUBJECTS)
        return f"{t}({s}): {v}"
    return random.choice(SUBJECTS)
