from __future__ import annotations

import random
import subprocess
from pathlib import Path


COMMIT_TYPES = [
    "docs", "chore", "refactor", "style", "test", "ci",
]
COMMIT_SCOPES = ["repo", "meta", "project", "config", "workflow"]
COMMIT_SUBJECTS = [
    "update project activity",
    "daily maintenance",
    "keep repository active",
    "auto sync",
    "bump activity log",
    "refresh heartbeat",
    "periodic update",
    "housekeeping",
]


def build_message(config: dict) -> str:
    style = config.get("style", "conventional")
    types = config.get("types", COMMIT_TYPES)
    scopes = config.get("scopes", COMMIT_SCOPES)
    messages = config.get("messages", COMMIT_SUBJECTS)

    if style == "conventional":
        commit_type = random.choice(types)
        scope = random.choice(scopes)
        subject = random.choice(messages)
        return f"{commit_type}({scope}): {subject}"
    return random.choice(messages)


def run_git(cmd: list[str], cwd: Path, check: bool = True, env: dict | None = None) -> tuple[int, str, str]:
    result = subprocess.run(
        ["git"] + cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=60,
        env=env,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"git {' '.join(cmd)} failed:\n{result.stderr}")
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def commit_and_push(
    repo_path: Path,
    message: str,
    env: dict | None = None,
) -> None:
    run_git(["add", "-A"], cwd=repo_path, env=env)
    code, _, _ = run_git(["diff", "--cached", "--quiet"], cwd=repo_path, check=False, env=env)
    if code == 0:
        print("No changes to commit.")
        return

    run_git(["commit", "-m", message], cwd=repo_path, env=env)
    run_git(["push"], cwd=repo_path, env=env)
