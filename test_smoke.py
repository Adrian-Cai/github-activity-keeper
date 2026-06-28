"""Smoke test for GitHub Activity Keeper."""
from datetime import datetime
from pathlib import Path

from keeper.config import Config
from keeper.strategy import get_strategy, RandomStrategy, WorkdayStrategy, WorktimeStrategy
from keeper.generators.heartbeat import HeartbeatGenerator
from keeper.generators.markdown import MarkdownGenerator
from keeper.generators.loader import get_generator
from keeper.git.operations import build_message


def test_config_load():
    cfg = Config.load("config.yaml")
    assert cfg.strategy["name"] == "random"
    assert cfg.generator["name"] == "heartbeat"
    assert cfg.commit["style"] == "conventional"
    assert cfg.repository["path"].endswith("github-activity-keeper")


def test_random_strategy():
    s = RandomStrategy()
    dt = datetime.now()
    sched = s.generate_schedule(dt, {"min_commit": 2, "max_commit": 5})
    assert 2 <= len(sched) <= 5
    for t in sched:
        assert t.date() == dt.date()


def test_workday_strategy():
    s = WorkdayStrategy()
    dt = datetime.now()
    sched = s.generate_schedule(dt, {})
    weekday = dt.weekday()
    if weekday < 5:
        assert len(sched) >= 1
    else:
        assert len(sched) == 0


def test_worktime_strategy():
    s = WorktimeStrategy()
    dt = datetime.now()
    sched = s.generate_schedule(dt, {})
    weekday = dt.weekday()
    if weekday < 5:
        for t in sched:
            assert 9 <= t.hour <= 18


def test_strategy_lookup():
    for name in ("random", "workday", "worktime"):
        s = get_strategy(name)
        assert s is not None


def test_heartbeat_generator(tmp_path):
    g = HeartbeatGenerator()
    result = g.generate(tmp_path, {"file": "test_hb.md"})
    assert result is not None
    assert (tmp_path / "test_hb.md").exists()
    content = (tmp_path / "test_hb.md").read_text(encoding="utf-8")
    assert "Heartbeat" in content or "-" in content or ":" in content


def test_markdown_generator(tmp_path):
    g = MarkdownGenerator()
    result = g.generate(tmp_path, {"quotes": ["test quote"]})
    assert result is not None
    assert (tmp_path / "daily.md").exists()
    content = (tmp_path / "daily.md").read_text(encoding="utf-8")
    assert "test quote" in content


def test_generator_lookup():
    for name in ("heartbeat", "markdown"):
        g = get_generator(name)
        assert g is not None


def test_commit_message():
    cfg = {"style": "conventional", "types": ["docs"], "scopes": ["repo"], "messages": ["test message"]}
    msg = build_message(cfg)
    assert msg.startswith("docs(repo):")
    assert "test message" in msg


def test_commit_message_plain():
    cfg = {"style": "plain", "messages": ["hello world"]}
    msg = build_message(cfg)
    assert msg == "hello world"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
