# Final Capstone Proposal

**CS 3030 - Scripting Languages**
**Team Members:** Jayanti Acharya (W01469558) | Omar Bustos (A#######) | Eric Zavala Moguel (A#######)
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

<!-- 3-5 concrete, testable deliverables that define a passing project. -->

1.
2.
3.

### Stretch Features (Nice to Have)

<!-- What would you add with extra time? Not required for a passing grade. -->

1.
2.

### Scope Justification

<!-- Why is this scope achievable in a roughly 10-day window? Reference the time available and comparable past projects. -->

### Known Risks and Mitigations

| Risk | Likelihood | Mitigation |
| --- | --- | --- |
| e.g. GitHub API rate limiting | Medium | Cache responses, use authenticated requests |
| [add a project risk] | [Low/Medium/High] | [how you will reduce or handle it] |

---

## Section 4: Git and Collaboration Plan

### Repository

- Repository URL: *(this repository's URL — update once you have it)*

### Planned Feature Branches

<!-- At least 4 branches. For teams, assign an owner to each. -->

| Branch Name | Owner | Description |
| --- | --- | --- |
| `feature/` | | |
| `feature/` | | |
| `feature/` | | |
| `feature/` | | |

### Commit Conventions

We will follow conventional commit format: `feat:` `fix:` `docs:` `test:` `chore:` `refactor:`

Example: `feat(parser): add JSON log detection`

### Work Division (Teams Only)

<!-- How will you split the work? Pair programming, divide by component, rotating roles? -->

---

## Section 5: Timeline and Milestones

<!-- Use relative day markers across a roughly 10-day project span after approval.
     Replace the sample milestones below with your own plan. -->

| Date | Milestone | Responsible |
| --- | --- | --- |
| [Day 1] | Proposal approved and implementation begins | Both |
| [Day 3] | Core Bash/Python components functional | [name] |
| [Day 5] | Docker and/or CI/CD components functional | [name] |
| [Day 7] | All core features complete, tests passing | Both |
| [Day 9] | Documentation complete and video recorded | Both |
| [Day 10] | Canvas submission completed | Both |

---

## Section 6: Testing Strategy

### How will you verify your tool works?

- **Unit tests (pytest):** [which functions/modules will you test?]
- **Integration tests:** [what end-to-end scenario will you run?]
- **Manual testing:** [what edge cases will you try by hand?]

### Definition of Done

<!-- Measurable and specific — how will you know when core features are complete? -->

Our project is complete when:

---

## Instructor Approval

*Leave this section blank — your instructor will complete it.*

- [ ] Approved as submitted
- [ ] Approved with the following modifications:
- [ ] Needs revision:

**Instructor signature / date:** _______________
