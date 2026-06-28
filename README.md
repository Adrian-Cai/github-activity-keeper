# GitHub Activity Keeper

> Keep your GitHub activity graph green with **meaningful** commits — not spam.

A configurable, open-source tool that automatically performs lightweight repository maintenance tasks. Works via **GitHub Actions** or **Docker**.

---

## Quick Start (GitHub Actions)

1. **Fork** or **create** a repository
2. Add this workflow to `.github/workflows/activity.yml`:

```yaml
on:
  schedule:
    - cron: "0 */3 * * *"
  workflow_dispatch:

jobs:
  keep-alive:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install pyyaml
      - run: python -m keeper
        env:
          INPUT_GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          INPUT_GITHUB_USERNAME: ${{ github.repository_owner }}
```

3. That's it. The bot will run every 3 hours and make 1–5 commits per day.

---

## Configuration

Copy `config.yaml` and customize:

```yaml
strategy:
  name: workday      # random | workday | worktime
  min_commit: 2
  max_commit: 6

generator:
  name: heartbeat    # heartbeat | markdown
  file: heartbeat.md

commit:
  style: conventional
  types: [docs, chore, refactor, style, test, ci]
```

### Strategies

| Strategy    | Behavior                              |
|-------------|---------------------------------------|
| `random`    | 1–5 commits at random times daily     |
| `workday`   | 2–6 on weekdays, 0 on weekends        |
| `worktime`  | 1–4 during 9–18 on weekdays           |

### Generators

| Generator   | Writes                               |
|-------------|--------------------------------------|
| `heartbeat` | Timestamps to `heartbeat.md`         |
| `markdown`  | Daily random quotes to `daily.md`    |

---

## Docker

```bash
docker run --rm \
  -v $(pwd):/app \
  -e GITHUB_TOKEN=your_token \
  -e GITHUB_USERNAME=your_username \
  ghcr.io/yourname/github-activity-keeper
```

---

## Development

```bash
git clone https://github.com/yourname/github-activity-keeper
cd github-activity-keeper
pip install pyyaml
python -m keeper --config config.yaml
```

---

## Philosophy

This tool is about **consistency**, not deception. It performs real repository maintenance — updating logs, refreshing metadata, and keeping your projects tidy. It's designed for developers who:

- Want to maintain an accurate activity history
- Use commit tracking for accountability
- Keep "archive" repos from appearing abandoned
- Like seeing their green squares 🟩

---

## License

MIT
