from __future__ import annotations

import os
import sys
from pathlib import Path

from . import config as cfg
from . import git_client
from .generators.heartbeat import HeartbeatGenerator
from .generators.quote import QuoteGenerator
from .generators.readme import ReadmeGenerator
from .scheduler import pick_hours, should_commit

GENERATORS = {
    "heartbeat": HeartbeatGenerator(),
    "quote": QuoteGenerator(),
    "readme": ReadmeGenerator(),
}


def main() -> None:
    config = cfg.load()
    repo_path = Path(".").resolve()

    scheduler_cfg = config.get("scheduler", {})
    commit_hours = pick_hours(
        min_c=scheduler_cfg.get("min_commit", 1),
        max_c=scheduler_cfg.get("max_commit", 4),
        profile=scheduler_cfg.get("mode", "random"),
    )

    commit_msg = should_commit(commit_hours, config)
    if commit_msg is None:
        print(f"[{commit_hours}] Not in schedule, skip.")
        return

    enabled_gens = config.get("generator", {}).get("enabled", ["heartbeat"])
    active_gen_names = [g for g in enabled_gens if g in GENERATORS]
    if not active_gen_names:
        print("No generators enabled.")
        return

    chosen = __import__("random").choice(active_gen_names)
    gen = GENERATORS[chosen]

    result = gen.generate(repo_path, config.get("generator", {}))
    if result is None:
        print(f"Generator {chosen} produced nothing.")
        return

    push_env = os.environ.copy()
    remote_url = push_env.get("REMOTE_URL", "")
    token = os.environ.get("INPUT_GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN", "")
    username = config["github"].get("username", "")
    if token and remote_url and "github.com" in remote_url:
        authed = remote_url.replace("https://github.com", f"https://{username}:{token}@github.com")
        git_client._exec(["remote", "set-url", "origin", authed], cwd=repo_path, env=push_env)

    email = config["github"].get("email", "")
    git_client.setup(repo_path, username, email, env=push_env)

    ok = git_client.commit_and_push(repo_path, commit_msg, env=push_env)
    if ok:
        print(f"OK  [{commit_msg}] ({result})")
    else:
        print("No changes to commit.")


if __name__ == "__main__":
    main()
