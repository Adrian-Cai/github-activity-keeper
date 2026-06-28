from __future__ import annotations

import argparse
import sys

from .config import Config
from .scheduler import run


def main() -> None:
    parser = argparse.ArgumentParser(description="GitHub Activity Keeper")
    parser.add_argument("--config", "-c", default="config.yaml", help="Path to config file")
    args = parser.parse_args()

    config = Config.load(args.config)

    if not config.github_token:
        print("Error: GitHub token is required. Set GITHUB_TOKEN or INPUT_GITHUB_TOKEN.", file=sys.stderr)
        sys.exit(1)

    count = run(config)
    sys.exit(0 if count >= 0 else 1)


if __name__ == "__main__":
    main()
