from pathlib import Path

import tempfile
from pathlib import Path

from app import config
from app.commit_message import generate as gen_msg
from app.generators.heartbeat import HeartbeatGenerator
from app.generators.quote import QuoteGenerator
from app.generators.readme import ReadmeGenerator
from app.git_client import _exec, setup
from app.scheduler import pick_hours, should_commit, PROFILES
from app.utils import generate_commit_hours


def test_config_load():
    cfg = config.load()
    assert "github" in cfg
    assert "scheduler" in cfg
    assert "generator" in cfg


def test_commit_hours_count():
    hours = generate_commit_hours(3)
    assert len(hours) == 3
    for h in hours:
        assert 0 <= h <= 23
    assert hours == sorted(hours)


def test_pick_hours_random():
    hours = pick_hours(2, 5, "random")
    assert 2 <= len(hours) <= 5


def test_pick_hours_profiles():
    for name in PROFILES:
        hours = pick_hours(1, 3, name)
        assert len(hours) >= 1


def test_commit_message_conventional():
    msg = gen_msg({"style": "conventional"})
    assert "(" in msg
    assert "):" in msg


def test_commit_message_plain():
    msg = gen_msg({"style": "plain"})
    assert "(" not in msg


def test_heartbeat(tmp_path):
    g = HeartbeatGenerator()
    result = g.generate(tmp_path, {})
    assert result is not None
    assert result.startswith("heartbeat:")
    assert (tmp_path / "data" / "heartbeat.md").exists()


def test_quote(tmp_path):
    g = QuoteGenerator()
    result = g.generate(tmp_path, {"quotes": ["test quote"]})
    assert result is not None
    assert result.startswith("quote:")
    assert (tmp_path / "data" / "quotes.md").exists()


def test_readme(tmp_path):
    readme = tmp_path / "README.md"
    readme.write_text("# Hello\n", encoding="utf-8")
    g = ReadmeGenerator()
    result = g.generate(tmp_path, {})
    assert result is not None
    assert result.startswith("readme:")
    content = readme.read_text(encoding="utf-8")
    assert "Last updated" in content


def test_readme_no_file(tmp_path):
    g = ReadmeGenerator()
    result = g.generate(tmp_path, {})
    assert result is None


def test_git_setup_email():
    with tempfile.TemporaryDirectory() as d:
        repo = Path(d)
        from app.git_client import _exec
        _exec(["init"], cwd=repo)
        setup(repo, "testuser", "test@example.com")
        out = _exec(["config", "user.email"], cwd=repo)
        assert out == "test@example.com"


def test_should_commit():
    cfg = {"scheduler": {}, "commit": {"style": "conventional"}}
    msg = should_commit([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], cfg)
    assert msg is not None
    msg2 = should_commit([], cfg)
    assert msg2 is None
