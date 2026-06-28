from __future__ import annotations

import random
from datetime import datetime, timezone
from typing import Dict, List

from .utils import generate_commit_hours, now

PROFILES: Dict[str, dict] = {
    "student": {
        "min_commit": 1,
        "max_commit": 3,
        "weight": {h: 1 for h in range(24)},
    },
    "office-worker": {
        "min_commit": 1,
        "max_commit": 4,
        "weight": {h: (1 if 0 <= h <= 7 or h >= 19 else 4 if 9 <= h <= 12 or 14 <= h <= 18 else 2) for h in range(24)},
    },
    "maintainer": {
        "min_commit": 1,
        "max_commit": 3,
        "weight": {h: 2 for h in range(24)},
    },
    "night-owl": {
        "min_commit": 1,
        "max_commit": 3,
        "weight": {h: (3 if h >= 22 or h <= 3 else 1) for h in range(24)},
    },
}


def pick_hours(min_c: int, max_c: int, profile: str = "random") -> List[int]:
    if profile == "random":
        count = random.randint(min_c, max_c)
        return generate_commit_hours(count)

    cfg = PROFILES.get(profile)
    if not cfg:
        count = random.randint(min_c, max_c)
        return generate_commit_hours(count)

    count = random.randint(cfg["min_commit"], cfg["max_commit"])
    weights = cfg["weight"]
    all_hours = list(range(24))
    chosen = set()
    while len(chosen) < count:
        h = random.choices(all_hours, weights=[weights[h] for h in all_hours], k=1)[0]
        chosen.add(h)
    return sorted(chosen)


def should_commit(commit_hours: List[int], config: dict) -> str | None:
    dt = now(config.get("timezone", "Asia/Shanghai"))
    current_hour = dt.hour

    if current_hour not in commit_hours:
        return None

    from .commit_message import generate as gen_msg
    return gen_msg(config.get("commit", {}))
