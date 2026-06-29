from __future__ import annotations

import subprocess
from pathlib import Path


def _exec(cmd: list[str], cwd: Path, env: dict | None = None):
    result = subprocess.run(
        ["git"] + cmd,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=60,
        env=env,
    )
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(cmd)} failed:\n{result.stderr}")
    return result.stdout.strip()


def setup(repo_path: Path, username: str, email: str = "", env: dict | None = None):
    _exec(["config", "user.name", username or "github-activity-keeper"], cwd=repo_path, env=env)
    email = email or f"{username or 'bot'}@users.noreply.github.com"
    _exec(["config", "user.email", email], cwd=repo_path, env=env)
    _exec(["config", "--local", "core.hooksPath", "/dev/null"], cwd=repo_path, env=env)


def commit_and_push(repo_path: Path, message: str, env: dict | None = None) -> bool:
    _exec(["add", "-A"], cwd=repo_path, env=env)

    result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=str(repo_path),
        capture_output=True,
        text=True,
        timeout=30,
        env=env,
    )
    if result.returncode == 0:
        return False

    _exec(["commit", "-m", message], cwd=repo_path, env=env)
    _exec(["push"], cwd=repo_path, env=env)
    return True
