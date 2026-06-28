# GitHub Activity Keeper

> Automatically keep your GitHub repositories active with configurable, meaningful maintenance tasks.

---

## How It Works

```text
GitHub Action (every hour)
        │
        ▼
Reads config.yaml
        │
        ▼
Is this hour in today's schedule?
        │
        ▼
Pick a random Generator (heartbeat / quote / readme)
        │
        ▼
Modify a repository file
        │
        ▼
Generate Commit Message → git add → git commit → git push
```

---

## Quick Start (GitHub Actions)

Add this workflow to `.github/workflows/activity.yml`:

```yaml
on:
  schedule:
    - cron: "0 * * * *"
  workflow_dispatch:

jobs:
  keep-alive:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v5
      - uses: actions/setup-python@v6
        with:
          python-version: "3.11"
      - run: pip install pyyaml
      - run: python -m app.main
        env:
          INPUT_GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          INPUT_GITHUB_USERNAME: ${{ github.repository_owner }}
```

---

## Configuration

```yaml
github:
  username: your_name

scheduler:
  timezone: Asia/Shanghai
  mode: random         # random | student | office-worker | maintainer | night-owl
  min_commit: 1
  max_commit: 4

generator:
  enabled:
    - heartbeat
    - readme
    - quote

commit:
  style: conventional  # conventional | plain
```

### Scheduler Profiles

| Mode            | Pattern                                    |
|-----------------|--------------------------------------------|
| `random`        | 1-4 commits at completely random hours     |
| `student`       | Evenings and weekends favored              |
| `office-worker` | Weekday work hours (9-12, 14-18) favored   |
| `maintainer`    | Light activity almost every day            |
| `night-owl`     | Late night hours (22-3) weighted           |

### Generators

| Generator    | Writes                     |
|--------------|----------------------------|
| `heartbeat`  | Timestamp to `data/heartbeat.md` |
| `quote`      | Random dev quote to `data/quotes.md` |
| `readme`     | Update `> Last updated` in README.md |

The Action runs hourly; a generator is selected randomly each time. This creates realistic, uneven commit patterns.

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

## Why Hourly?

Running once per day creates all commits at `00:00` — clearly artificial.

By running hourly and checking "is this hour scheduled?", your commit times naturally scatter across the day:

```
09:17  14:06  20:31
```

This matches real development rhythms.

---

## License

MIT
