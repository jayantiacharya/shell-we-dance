**CS 3030 - Scripting Languages**
**Team Members:** Jayanti Acharya (W01469558) | Omar Bustos (W01477301) | Eric Zavala Moguel (W01518822)
**Date:** 2026-07-23

> **Instructions:** Fill in every section below. Delete all instruction
> comments (lines starting with `>`). Commit this file on a feature branch,
> open a PR, merge it into `main`, and submit the GitHub link on Canvas.
> Do not begin implementation until your instructor approves this proposal.
> This file is intentionally both the editable template and the final submitted
> proposal. Edit it directly.

---

## Section 1: Problem Statement

### What problem does your tool solve?
Checking the health of a local or containerized dev environment today means manually SSHing in and running a handful of commands (df, top, ps, docker ps, tailing logs) every time something feels off. Because it's manual, checks get skipped, and issues like a filling disk or a crashed container go unnoticed until something actually breaks. This tool automates that monitoring loop end-to-end and surfaces the results as a live dashboard, so no one has to remember to go check.

### Who would use this tool and how?
A small dev team or solo developer running local services or Docker containers who wants at-a-glance visibility into system health without manually checking in. A typical workflow: the pipeline runs automatically on a schedule, collects metrics, and updates a dashboard the developer can glance at each morning (or whenever) to see disk usage, CPU load, and container status — with a clear alert log if anything crossed a threshold overnight.

### Why is automation the right solution here?
A manual process is inconsistent, people forget to check, and it has no history: you only know the current state, not the trend over time. It also doesn't scale past one person checking one machine by hand. A scheduled pipeline runs the same checks every time, keeps a timestamped record so you can spot trends, and can alert automatically the moment a threshold is crossed — none of which a one-off manual check or a bare GUI tool gives you without someone actively driving it.

---

## Section 2: Technical Design

### Core Components

| Component | Technology | Responsibility |
| --- | --- | --- |
| `collect_metrics.sh` | Bash | Collects disk usage, CPU load, running processes, log file sizes, and Docker container status |
| `aggregator.py` | Python | Parses Bash output, normalizes into structured JSON, checks values against thresholds |
| `Dockerfile` / `docker-compose.yml` | Docker | Containerizes a lightweight Python HTTP server that renders the JSON as an HTML dashboard |
| `health-check.yml` | GitHub Actions | Cron-scheduled workflow that runs the collection pipeline and commits the updated JSON |
| `alerts.log` handling | Logging/Security | Timestamped alert log when thresholds are exceeded, with rotation/retention policy |

### Technology Domains Used

- [x] Bash scripting (file operations, error handling, functions)
- [x] Python scripting (data processing, pytest, argparse)
- [x] Docker / container orchestration
- [x] CI/CD pipelines / GitHub Actions
- [x] Logging, archiving, and security best practices

### Data Flow Diagram

[collect_metrics.sh] --> [raw metric output] --> [aggregator.py] --> [health.json]
                                                          |
                                                          +--> [alerts.log, if threshold exceeded]

[health.json] --> [Docker: Python HTTP server] --> [HTML dashboard]

[GitHub Actions cron] --> triggers [collect_metrics.sh] on schedule --> commits updated [health.json]

### External Dependencies

- Python standard library `http.server` (or Flask, if we want routing) for serving the dashboard
- `psutil` (optional) for cleaner CPU/process metrics in Python, or native Bash tools (`df`, `top`, `ps`) if we keep collection Bash-only
- Docker base image: `python:3.12-slim`
- GitHub Actions (`schedule` cron trigger)
- `pytest` for the aggregator's test suite

---

## Section 3: Scope and Feasibility

### Core Features (Must Have)


1. We would need a collector to collect system metrics. A collector script that uses bash would work best. This collector will record things like the size of our file logs or disk usage.
2. An aggregator would check if the things we are recording / tracking are over the limit. We would use python for this script!
3. For an infra dashboard, we would need to create a simple UI and use some sort of server for it. Docker would be a great choice. Perhaps the dashboard can be created using HTML.
4. Github action workflow(s) would be great to use here. We could use it to test or shellcheck when we push out the script. We can also have a workflow where the data recording (such as the disk usage, CPU load, log file size, etc) happens on a schedule so that we can see if something is over the limit without a push.

### Stretch Features (Nice to Have)

1. A logging module working with the aggregator would be nice for error checking or testing. It is also nice just to see if our thresholds are working.
2. We could add basic authentication to the server dashboard if we would like.

### Scope Justification

This scope works well for the 10 day window. We have practiced the core pieces before so it should not take too long to implement into this project. The Bash collector will be building on the loops and log parsing code that we have done in Module 2. The Python aggregator we have also practiced in module 3, and the docker part was practiced in project 4. The Github actions workflow code is being done right now in project 5, which we can practice side by side with this project. With the knowledge and experience we should be able to finish on time.

### Known Risks and Mitigations

| Risk | Likelihood | Mitigation |
| --- | --- | --- |
| The cron worflow job could collide with someone's feature branch if it commits at a bad time | Medium | We're keeping the cron commits limited to the metrics file on main only, so feature branches don't touch it |
| Docker might act differently depending on what OS it's running on | Medium | We'll just test on Ubuntu and have it skip Docker metrics gracefully if the daemon isn't there |
| With three of us working at once, we could end up duplicating work or blocking each other | Low | Everyone owns their own piece from the start, and we'll check in at each milestone |
| Our threshold numbers (like the 85% disk check) are kind of just guesses right now | Low | We'll test them against real sample data before finalizing them in |
| We might get tempted to build something fancier than what's actually been taught and get stuck | Low | All four core features are based on stuff we've already done in Projects 3–5, so this one should be pretty low risk 

## Section 4: Git and Collaboration Plan

### Repository

- Repository URL: https://github.com/cs3030-valle-su26/cs3030-project7-shell-we-dance

### Planned Feature Branches

| Branch Name | Owner | Description |
| --- | --- | --- |
| feature/metric-collectors | Eric Zavala Moguel | Bash scripts to collect disk, CPU, process, and Docker status metrics |
| feature/aggregator | Jayanti Acharya | Python aggregator that parses metrics into JSON and checks thresholds |
| feature/dashboard-docker | Omar Bustos | Dockerfile/compose setup and HTTP server rendering the HTML dashboard |
| feature/ci-cron-workflow | Eric Zavala Moguel | GitHub Actions cron workflow to run the pipeline on a schedule |

### Commit Conventions

We will follow conventional commit format: feat: fix: docs: test: chore: refactor:

### Work Division (Teams Only)

The work will be divided by parts. The parts are seperated as so: Eric will handle the the Bash Collecter script, as well as the Github Actions workflow. Jayanti will be building the Python aggregator and Omar will be working on the Docker Container and the dashboard. Everyone will have their own branch will need to open a pull request before merging into main. That way the other two members can review it. We will also check in with each other at each milestone to makesure everything is still connecting the way it should.

## Section 5: Timeline and Milestones

| Date | Milestone | Responsible |
| --- | --- | --- |
| Day 1 | Proposal approved, repository pulled by all members, and implementation begins | All |
| Day 2 | Project folder structure finalized and feature branches confirmed | All |
| Day 3 | Bash metric collector functional for disk usage, CPU load, process count, log file size, and Docker status | Eric Zavala Moguel |
| Day 4 | Python aggregator reads raw metric output and generates structured JSON | Jayanti Acharya |
| Day 5 | Threshold detection and alert logging completed | Jayanti Acharya |
| Day 6 | Dockerfile, Docker Compose setup, and basic dashboard server completed | Omar Bustos |
| Day 7 | HTML dashboard displays health data from `health.json` | Omar Bustos |
| Day 8 | GitHub Actions workflow runs tests, shellcheck, linting, and Docker validation | Eric Zavala Moguel |
| Day 9 | End-to-end testing complete, documentation updated, and video demo recorded | All |
| Day 10 | Final review completed, PR merged, and Canvas submission completed | All |

---

## Section 6: Testing Strategy

### How will you verify your tool works?

We will verify the Infrastructure Health Dashboard using unit tests, integration tests, manual testing, Docker validation, and GitHub Actions workflow checks. The goal is to confirm that each major component works individually and that the full pipeline works from metric collection to dashboard output.

### Unit tests with pytest

We will use `pytest` to test the Python aggregator. The tests will verify that the aggregator can correctly parse metric data, detect threshold violations, generate JSON output, and handle missing or invalid input.

The pytest suite will test:

- Disk usage parsing
- CPU/load metric parsing
- Process count parsing
- Docker status parsing
- Log file size parsing
- Threshold detection logic
- Alert message generation
- JSON report structure
- Missing or unavailable metric values
- Invalid input handling

Expected command:

```bash
pytest src/ --cov=src --cov-report=term-missing
```

### Integration tests

For integration testing, we will run the complete workflow from start to finish. The Bash collector will collect system metrics and write raw output. The Python aggregator will process that output and create `health.json` and `alerts.log`. The dashboard server will then read the JSON file and display the results in the browser.

End-to-end test scenario:

1. Run the Bash metric collector.
2. Confirm raw metrics are created.
3. Run the Python aggregator.
4. Confirm `health.json` is created.
5. Confirm `alerts.log` is created when thresholds are exceeded.
6. Start the dashboard server.
7. Open the dashboard in a browser.
8. Confirm the dashboard displays current health data.

Expected commands:

```bash
bash collect_metrics.sh
python3 aggregator.py --input raw_metrics.json --output health.json
python3 dashboard.py --port 8000
```

### Manual testing

We will manually test common edge cases to make sure the tool handles errors gracefully instead of crashing.

Manual test cases:

- Normal healthy environment
- Disk usage over the threshold
- Docker running normally
- Docker not installed or not running
- Empty metrics file
- Invalid JSON input
- Missing output file
- Large log file warning
- Dashboard loading successfully in a browser
- Docker Compose startup and shutdown

### Docker testing

We will verify that the project can run inside a container. This confirms that the dashboard has a consistent runtime environment and can be started without relying only on one developer’s local setup.

Expected commands:

```bash
docker build -t infrastructure-health-dashboard .
docker compose config
docker compose up
```

### CI/CD testing

The GitHub Actions workflow will run on pushes and pull requests. At minimum, the workflow will include two jobs.

The first job will validate Python code:

- Install dependencies
- Run pytest
- Run pylint
- Run black formatting check

The second job will validate Bash and Docker:

- Run Bash syntax check
- Run shellcheck
- Build the Docker image
- Validate Docker Compose configuration
- Run a basic smoke test

Expected commands:

```bash
bash -n collect_metrics.sh
shellcheck *.sh
pytest src/ --cov=src --cov-report=term-missing
pylint *.py
black --check .
docker build -t infrastructure-health-dashboard .
docker compose config
```

### Definition of Done

Our project is complete when:

- The proposal is approved by the instructor.
- The Bash metric collector runs successfully.
- The Python aggregator generates structured JSON health data.
- Threshold violations are detected correctly.
- Alerts are written to `alerts.log`.
- The HTML dashboard displays the latest health status.
- Docker image builds successfully.
- Docker Compose starts the dashboard successfully.
- GitHub Actions has at least two passing jobs on `main`.
- Pytest tests pass.
- Bash and Python lint checks pass or are documented.
- README is complete with setup, usage, architecture, testing instructions, known limitations, and reflection.
- The team has at least 5 feature branches.
- The team has at least 3 merged pull requests.
- The team has at least 15 conventional commits.
- At least one merge conflict is resolved and documented.
- The final video demo is recorded with all team members participating.
- The GitHub repository link and video link are submitted on Canvas.

---

## Instructor Approval

*Leave this section blank — your instructor will complete it.*

- [ ] Approved as submitted
- [ ] Approved with the following modifications:
- [ ] Needs revision:

**Instructor signature / date:** _______________
