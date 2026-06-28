from __future__ import annotations

import random
from abc import ABC, abstractmethod
from datetime import datetime, time, timedelta, timezone


class CommitStrategy(ABC):
    @abstractmethod
    def generate_schedule(self, date: datetime, config: dict) -> list[datetime]:
        ...


class RandomStrategy(CommitStrategy):
    def generate_schedule(self, date: datetime, config: dict) -> list[datetime]:
        min_c = config.get("min_commit", 1)
        max_c = config.get("max_commit", 5)
        count = random.randint(min_c, max_c)
        times = set()
        base = date.replace(hour=0, minute=0, second=0, microsecond=0)
        for _ in range(count * 3):
            total_minutes = random.randint(0, 24 * 60 - 1)
            h, m = divmod(total_minutes, 60)
            t = time(h, m)
            times.add(t)
            if len(times) >= count:
                break
        return [base.replace(hour=t.hour, minute=t.minute, second=random.randint(0, 59)) for t in sorted(times)]


class WorkdayStrategy(CommitStrategy):
    def generate_schedule(self, date: datetime, config: dict) -> list[datetime]:
        if date.weekday() >= 5:
            return []
        min_c = 2
        max_c = 6
        if date.weekday() < 5:
            if config.get("mode") == "workaholic":
                min_c, max_c = 6, 10
            elif config.get("mode") == "slacker":
                max_c = 3
        return RandomStrategy().generate_schedule(date, {"min_commit": min_c, "max_commit": max_c})


class WorktimeStrategy(CommitStrategy):
    def generate_schedule(self, date: datetime, config: dict) -> list[datetime]:
        if date.weekday() >= 5:
            return RandomStrategy().generate_schedule(date, {"min_commit": 0, "max_commit": 1})
        min_c = config.get("min_commit", 1)
        max_c = config.get("max_commit", 4)
        count = random.randint(min_c, max_c)
        times = set()
        base = date.replace(hour=0, minute=0, second=0, microsecond=0)
        work_start = 9
        work_end = 18
        for _ in range(count * 5):
            h = random.randint(work_start, work_end)
            m = random.randint(0, 59)
            t = time(h, m)
            times.add(t)
            if len(times) >= count:
                break
        return [base.replace(hour=t.hour, minute=t.minute, second=random.randint(0, 59)) for t in sorted(times)]


STRATEGIES: dict[str, type[CommitStrategy]] = {
    "random": RandomStrategy,
    "workday": WorkdayStrategy,
    "worktime": WorktimeStrategy,
}


def get_strategy(name: str) -> CommitStrategy:
    cls = STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown strategy: {name}. Available: {list(STRATEGIES.keys())}")
    return cls()
