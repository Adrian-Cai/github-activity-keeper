from __future__ import annotations

import os
from pathlib import Path

import yaml

CONFIG_PATH = Path(os.environ.get("INPUT_CONFIG_PATH", "config.yaml"))


def load() -> dict:
    config = {
        "github": {
            "username": os.environ.get("INPUT_GITHUB_USERNAME") or os.environ.get("GITHUB_USERNAME", ""),
            "email": os.environ.get("INPUT_GITHUB_EMAIL") or os.environ.get("GITHUB_EMAIL", ""),
        },
        "scheduler": {"timezone": "Asia/Shanghai", "mode": "random", "min_commit": 1, "max_commit": 4},
        "generator": {"enabled": ["heartbeat", "readme", "quote"]},
        "commit": {"style": "conventional"},
    }

    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        if "github" in data:
            config["github"].update(data["github"])
        if "scheduler" in data:
            config["scheduler"].update(data["scheduler"])
        if "generator" in data:
            config["generator"].update(data["generator"])
        if "commit" in data:
            config["commit"].update(data["commit"])

    return config
