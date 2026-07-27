# Infra Health Dashboard

CS 3030 — Final Capstone Project | Weber State University
Team: Shell We Dance — Jayanti Acharya, Omar Bustos, Eric Zavala Moguel

## What This Tool Does

Infra Health Dashboard automates monitoring of a local or containerized dev
environment. Instead of manually checking disk usage, CPU load, and Docker
container status by hand, this tool collects those metrics on a schedule,
checks them against thresholds, and displays the results on a live HTML
dashboard — so problems get caught automatically instead of by chance.

## Architecture

```text
[collect metrics: orchestrator.sh] --> [raw_metrics.txt]
                                              |
                                              v
                              [aggregate: processor.py] --> [health.json]
                                              |
                                              v
                       [Docker: dashboard_server.py] --> [HTML dashboard]

[GitHub Actions cron: health-check.yml] --> triggers orchestrator.sh on a
                                              schedule, commits updated
                                              health.json
```

| Component | File | Owner | Role |
| --- | --- | --- | --- |
| Bash collector | `src/orchestrator.sh` | Eric | Collects disk, CPU, process, and Docker metrics |
| Config | `config.yaml` | Eric | Values the orchestrator reads at runtime |
| Python aggregator | `src/processor.py` | Jayanti | Parses metrics, checks thresholds, writes `health.json` |
| Aggregator tests | `tests/test_processor.py` | Jayanti | pytest suite for the aggregator |
| Dashboard server | `src/dashboard_server.py` | Omar | Serves `health.json` as an HTML page |
| Container setup | `Dockerfile`, `docker-compose.yml` | Omar | Containerizes and runs the dashboard |
| Scheduled pipeline | `.github/workflows/health-check.yml` | Eric | Runs the pipeline on a cron schedule |
| CI checks | `.github/workflows/ci.yml` | (provided) | Lint/test checks on every push |
| Data contract | `docs/schema.md` | All | Agreed format between components |

## Setup and Usage

<!-- TODO: fill in once implementation is complete — every command here should
     actually work when tested on a clean machine. -->

```bash
# Clone the repo
git clone https://github.com/cs3030-valle-su26/cs3030-project7-shell-we-dance.git
cd cs3030-project7-shell-we-dance

# Install git hooks (once, after cloning)
bash scripts/setup-hooks.sh

# TODO: install any Python dependencies
pip install -r requirements.txt

# TODO: run the metrics collector + aggregator
./src/orchestrator.sh

# TODO: build and run the dashboard
docker compose up --build
```

## Example Commands and Output

<!-- TODO: add once features are working — show a real command and its
     real output, e.g. running orchestrator.sh and the resulting log lines,
     or curling the dashboard and showing the HTML/metrics returned. -->

## Running Tests

<!-- TODO: confirm exact command + expected coverage once tests are written -->

```bash
pytest src/ --cov=src --cov-report=term-missing
```

## Known Limitations

<!-- TODO: be honest here — e.g. does this only work on Linux? does Docker
     detection fail gracefully if Docker isn't installed? no auth on the
     dashboard? fill this in as you discover real limitations. -->

## Reflection

<!-- TODO: write this near the end — what worked, what you'd change, what
     you learned building this. Separate from the individual Canvas quiz. -->
