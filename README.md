# Infrastructure Health Dashboard

**CS 3030 — Final Capstone Project | Weber State University**

**Team: Shell We Dance**
- Jayanti Acharya
- Omar Bustos
- Eric Zavala Moguel

## What This Tool Does

Infrastructure Health Dashboard automates basic monitoring of a Linux development or container environment. The Bash collector gathers system metrics, the Python processor evaluates and structures those metrics, and a Dockerized HTTP dashboard displays the latest infrastructure health information in a browser.

The project reduces manual system checks by combining metric collection, threshold processing, automated testing, Docker deployment, logging, and scheduled GitHub Actions into one reproducible workflow.

## Architecture

```text
                    Infrastructure Health Dashboard

        +----------------------+
        |  src/orchestrator.sh |
        |    Bash Collector    |
        +----------+-----------+
                   |
                   | writes
                   v
        +----------------------+
        |   raw_metrics.txt    |
        +----------+-----------+
                   |
                   | input
                   v
        +----------------------+
        |   src/processor.py   |
        |  Python Processor    |
        +----------+-----------+
                   |
                   | writes
                   v
        +----------------------+
        |     health.json      |
        +----------+-----------+
                   |
                   | read-only mount
                   v
        +----------------------+
        | Docker / Compose     |
        | dashboard_server.py  |
        +----------+-----------+
                   |
                   v
        +----------------------+
        |   HTML Dashboard     |
        |   localhost:8000     |
        +----------------------+

        GitHub Actions CI
          |
          +--> ShellCheck
          +--> Black
          +--> Pylint
          +--> pytest + coverage
          +--> Docker integration test
          +--> Scheduled metrics collection
```

## Components

| Component | File | Owner | Purpose |
| --- | --- | --- | --- |
| Bash collector | `src/orchestrator.sh` | Eric | Collects disk, CPU, process, log-directory, and Docker metrics |
| Configuration | `config.yaml` | Eric | Defines collector paths and runtime configuration |
| Python processor | `src/processor.py` | Jayanti | Parses raw metrics, evaluates thresholds, and writes `health.json` |
| Processor tests | `tests/test_processor.py` | Jayanti | Tests processor parsing and threshold behavior |
| Dashboard server | `src/dashboard_server.py` | Omar | Serves the HTML dashboard and `/health.json` endpoint |
| Dashboard tests | `tests/test_dashboard_server.py` | Omar | Tests loading, rendering, errors, and HTTP integration |
| Docker image | `Dockerfile` | Omar | Builds the dashboard using a multi-stage, non-root image |
| Compose stack | `docker-compose.yml` | Omar | Runs the dashboard with a custom network and named volume |
| CI/CD | `.github/workflows/ci.yml` | Team | Runs linting, tests, coverage, Docker integration, and scheduled collection |
| Data contract | `docs/schema.md` | Team | Defines the collector and processor data formats |

## Requirements

The application itself uses Python standard-library modules and does not require third-party runtime Python libraries.

Recommended environment:

- Linux
- Python 3.12 or newer
- Docker Engine
- Docker Compose
- Git

Development and testing packages are listed in `requirements.txt`.

## Setup

Clone the repository:

```bash
git clone https://github.com/cs3030-valle-su26/cs3030-project7-shell-we-dance.git
cd cs3030-project7-shell-we-dance
```

Install the Git commit hook:

```bash
bash scripts/setup-hooks.sh
```

Install the testing and quality dependencies:

```bash
python3 -m pip install -r requirements.txt
```

## Run the Complete Pipeline

### 1. Collect Infrastructure Metrics

```bash
bash src/orchestrator.sh
```

Example successful output:

```text
[INFO] orchestrator.sh: Disk usage: 25%
[INFO] orchestrator.sh: CPU load (1min): 0.76
[INFO] orchestrator.sh: Process count: 180
[INFO] orchestrator.sh: Docker available: true, running containers: 1
[INFO] orchestrator.sh: Wrote raw metrics to raw_metrics.txt
[INFO] orchestrator.sh: === orchestrator.sh finished successfully ===
```

The collector creates:

```text
raw_metrics.txt
```

### 2. Process the Collected Metrics

```bash
python3 src/processor.py \
  --input raw_metrics.txt \
  --output health.json
```

Example successful output:

```text
[INFO] Processor initialized: input=raw_metrics.txt format=json
[INFO] Loaded 6 metrics from input.
[INFO] Processing complete. 6 metrics processed, 0 alerts.
[INFO] Writing json output to: health.json
[INFO] Output written successfully.
```

Example `health.json` structure:

```json
{
  "timestamp": "2026-08-12T09:05:48.227195+00:00",
  "input": "raw_metrics.txt",
  "items_processed": 6,
  "errors": [],
  "metrics": {
    "disk_usage_percent": 25,
    "cpu_load_1min": 0.76,
    "process_count": 180,
    "log_size_kb": 0,
    "docker_available": true,
    "docker_container_count": 1
  },
  "alerts": []
}
```

### 3. Start the Docker Dashboard

After `health.json` has been generated:

```bash
docker compose up --build -d
```

Check the container:

```bash
docker compose ps
```

A successful deployment reports the dashboard container as healthy:

```text
Up (...) (healthy)
```

Open the dashboard in a browser:

```text
http://localhost:8000
```

The raw JSON endpoint is available at:

```text
http://localhost:8000/health.json
```

You can verify both endpoints from the terminal:

```bash
curl --fail http://127.0.0.1:8000/
curl --fail http://127.0.0.1:8000/health.json
```

Stop the dashboard:

```bash
docker compose down
```

## Dashboard Behavior

The dashboard reads the latest `health.json` every time a request is made. Updated metrics can therefore appear without rebuilding or restarting the Docker container.

Dashboard states are:

- **HEALTHY** — no active alerts or errors
- **WARNING** — one or more threshold alerts are present
- **ERROR** — the health report cannot be read or contains errors

The server also handles missing files and invalid JSON without terminating the HTTP service.

## Running Tests

Run the complete project test suite with the required coverage gate:

```bash
pytest tests/ \
  --cov=src \
  --cov-report=term-missing \
  --cov-fail-under=70 \
  -v
```

Validated result:

```text
15 passed
Required test coverage of 70% reached.
Total coverage: 71.01%
```

Testing includes:

- valid metrics parsing
- malformed input handling
- missing-file handling
- threshold alert behavior
- valid dashboard JSON loading
- invalid JSON handling
- operating-system read errors
- HEALTHY and WARNING dashboard rendering
- malformed dashboard data handling
- real HTTP server integration
- `/health.json` endpoint validation
- HTML endpoint validation
- HEAD request support
- HTTP 404 behavior

## Code Quality

### Black

```bash
black --check src/
```

Validated result:

```text
2 files would be left unchanged.
```

### Pylint

```bash
pylint src/ --fail-under=7.0
```

Validated project score:

```text
9.79/10
```

### ShellCheck

```bash
find src/ -name "*.sh" -print0 | xargs -0 -r shellcheck
```

A successful run produces no ShellCheck findings.

## Docker Design

The dashboard container uses several containerization and security practices:

- multi-stage Docker build
- Python 3.12 slim base image
- Python syntax validation during the build stage
- dedicated non-root `dashboard` user
- Docker `HEALTHCHECK`
- read-only `health.json` bind mount
- named Docker Compose volume
- custom Docker network
- automatic restart policy

The dashboard image was validated locally below the project's 300 MB rubric limit.

## CI/CD

`.github/workflows/ci.yml` runs automated quality gates for the project.

The CI pipeline includes:

1. ShellCheck
2. Black formatting validation
3. Pylint with a minimum score of 7.0
4. pytest with a 70% coverage requirement
5. Docker Compose build and integration validation
6. HTTP endpoint validation
7. scheduled infrastructure metric collection

The scheduled workflow generates fresh metrics, processes them into `health.json`, and can commit an updated health report back to the repository.

## Known Limitations

- The collector is primarily designed for Linux environments and relies on Linux system paths and utilities.
- Metrics collected by GitHub Actions describe the temporary GitHub-hosted runner rather than a user's workstation or a production server.
- The dashboard does not currently implement authentication or HTTPS.
- The dashboard is intended for lightweight infrastructure monitoring rather than enterprise-scale observability.
- `health.json` must be generated before starting the Docker Compose dashboard.
- Threshold behavior is implemented by the Python processor rather than through an interactive dashboard configuration interface.

## Reflection

Building the Infrastructure Health Dashboard demonstrated how independently developed Bash, Python, Docker, testing, and CI/CD components can be connected through a clearly defined data contract. Using `raw_metrics.txt` and `health.json` as stable interfaces allowed the team members to develop and test their components independently before combining them into the complete pipeline.

The project also demonstrated the value of automated validation. Unit and integration tests, linting, coverage gates, Docker health checks, and CI integration testing exposed problems that could easily be missed during manual testing. If the project were extended, useful improvements would include configurable thresholds, authentication, historical metric storage, richer visualizations, and deployment to a persistent monitoring host.
