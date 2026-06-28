from __future__ import annotations

import os
import random
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .config import Config
from .generators.loader import get_generator
from .git.operations import build_message, commit_and_push
from .strategy import get_strategy


def run(config: Config) -> int:
    repo_path = Path(config.repository["path"])
    strategy = get_strategy(config.strategy.get("name", "random"))
    generator = get_generator(config.generator.get("name", "heartbeat"))

    now = datetime.now(timezone.utc).astimezone()
    schedule = strategy.generate_schedule(now, config.strategy)

    if not schedule:
        print(f"No commits scheduled for {now.strftime('%Y-%m-%d')}")
        return 0

    push_env = os.environ.copy()
    remote_url = push_env.get("REMOTE_URL", "")
    if remote_url:
        token = push_env.get("INPUT_GITHUB_TOKEN") or push_env.get("GITHUB_TOKEN", "")
        username = push_env.get("INPUT_GITHUB_USERNAME") or push_env.get("GITHUB_USERNAME", "")
        if token and "github.com" in remote_url:
            authed_url = remote_url.replace("https://github.com", f"https://{username}:{token}@github.com")
            run_git_cmd(repo_path, ["remote", "set-url", "origin", authed_url])

    run_git_cmd(repo_path, ["config", "user.name", config.github_username or "github-activity-keeper"])
    run_git_cmd(repo_path, ["config", "user.email", f"{config.github_username or 'bot'}@users.noreply.github.com"])

    if config.commit.get("style") == "conventional":
        run_git_cmd(repo_path, ["config", "--local", "core.hooksPath", "/dev/null"])

    commit_count = 0
    for dt in schedule:
        delay = (dt - datetime.now(timezone.utc).astimezone()).total_seconds()
        if delay > 0:
            jitter = random.uniform(0, 30)
            total_delay = delay + jitter
            if total_delay > 300:
                print(f"Too far in the future ({total_delay:.0f}s), skipping.")
                continue
            print(f"Waiting {total_delay:.0f}s until next commit...")
            time.sleep(total_delay)

        msg = generator.generate(repo_path, config.generator)
        if msg is None:
            continue

        commit_msg = build_message(config.commit)
        try:
            commit_and_push(repo_path, commit_msg)
            commit_count += 1
            print(f"  [{dt.strftime('%H:%M:%S')}] {commit_msg}")
        except RuntimeError as e:
            print(f"  [{dt.strftime('%H:%M:%S')}] Failed: {e}")

    print(f"Done. {commit_count} commit(s) made.")
    return commit_count


def run_git_cmd(repo_path: Path, cmd: list[str]) -> None:
    from .git.operations import run_git

    run_git(cmd, cwd=repo_path)
