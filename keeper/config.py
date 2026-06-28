from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import yaml


DEFAULT_CONFIG = {
    "schedule": {"timezone": "Asia/Shanghai"},
    "strategy": {"name": "random", "min_commit": 1, "max_commit": 5},
    "generator": {"name": "heartbeat", "file": "heartbeat.md"},
    "commit": {
        "style": "conventional",
        "scope": "repo",
        "types": [
            "docs", "chore", "refactor", "style", "test", "ci",
        ],
        "messages": [
            "update project activity",
            "daily maintenance",
            "keep repository active",
            "auto sync",
        ],
    },
    "repository": {"path": "."},
}


@dataclass
class Config:
    github_token: str = ""
    github_username: str = ""
    schedule: dict = field(default_factory=lambda: DEFAULT_CONFIG["schedule"])
    strategy: dict = field(default_factory=lambda: DEFAULT_CONFIG["strategy"])
    generator: dict = field(default_factory=lambda: DEFAULT_CONFIG["generator"])
    commit: dict = field(default_factory=lambda: DEFAULT_CONFIG["commit"])
    repository: dict = field(default_factory=lambda: DEFAULT_CONFIG["repository"])

    @classmethod
    def load(cls, path: str | Path | None = None) -> "Config":
        config = cls()

        config.github_token = os.environ.get("INPUT_GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
        config.github_username = os.environ.get("INPUT_GITHUB_USERNAME") or os.environ.get("GITHUB_USERNAME", "")

        config_path = Path(path or os.environ.get("INPUT_CONFIG_PATH", "config.yaml"))
        if config_path.exists():
            with open(config_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)
            if data:
                if "github" in data:
                    gh = data["github"]
                    config.github_token = gh.get("token") or os.environ.get("GITHUB_TOKEN", config.github_token)
                    config.github_username = gh.get("username") or os.environ.get(
                        "GITHUB_USERNAME", config.github_username
                    )
                if "schedule" in data:
                    config.schedule = {**config.schedule, **data["schedule"]}
                if "strategy" in data:
                    config.strategy = {**config.strategy, **data["strategy"]}
                if "generator" in data:
                    config.generator = {**config.generator, **data["generator"]}
                if "commit" in data:
                    config.commit = {**config.commit, **data["commit"]}
                if "repository" in data:
                    config.repository = {**config.repository, **data["repository"]}

        repo_path = Path(config.repository.get("path", "."))
        config.repository["path"] = str(repo_path.resolve())

        return config
