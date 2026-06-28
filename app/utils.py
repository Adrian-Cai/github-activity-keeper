from __future__ import annotations

import random
from datetime import datetime, timedelta, timezone
from typing import List


def now(tz: str = "Asia/Shanghai") -> datetime:
    return datetime.now(timezone.utc).astimezone()


def generate_commit_hours(count: int) -> List[int]:
    hours = set()
    while len(hours) < count:
        hours.add(random.randint(0, 23))
    return sorted(hours)
