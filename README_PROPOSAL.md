# Project 7 Part 1: Final Capstone Proposal

CS 3030 - Scripting Languages | Weber State University

15 Points

---

## Overview

The Final Capstone is your opportunity to build something real. You will design
and implement an original automation or DevOps tool that integrates at least
**three** of the five technology domains you have learned in CS 3030:

| Domain | Covered In |
| --- | --- |
| Bash scripting (file ops, error handling, functions) | Projects 1 & 2 |
| Python scripting (data processing, pytest, argparse) | Project 3 |
| Docker & container orchestration | Project 4 |
| CI/CD pipelines & GitHub Actions | Project 5 |
| Logging, archiving & security best practices | Projects 1–5 |

**Part 1 is the proposal.** Before writing a single line of implementation code,
you must clearly define what you are building, why it matters, how it fits in a
roughly 10-day implementation window, and who is on your team.

**Your proposal must be approved by the instructor before you begin Part 2.**

---

## Team Policy

- **Teams of exactly 2 are strongly encouraged.** Collaboration produces stronger
  projects and mirrors real-world DevOps work.
- Solo students are allowed, but scope expectations are **identical** — the same
  three domains, the same quality bar, the same deliverables. No accommodation
  is made for working alone.
- Teams of 3 are not permitted.
- Both team members submit identical Canvas links pointing to the shared repository.
- The Git history must show commits authored by both members.

---

## What to Submit

1. Open `PROPOSAL.md` at the root of your project repository.
2. Fill in every section completely. Delete all instruction comments.
3. Push to your GitHub repository.
4. Submit the GitHub link on Canvas before the deadline.

In this starter repository, `PROPOSAL.md` is intentionally both the editable
template and the final proposal file. Edit it directly rather than creating a
second copy.

Your `PROPOSAL.md` file must be named exactly `PROPOSAL.md` at the repository root.

---

## Example Project Ideas

You may build any of the following, adapt one, or propose something entirely
original. Original proposals are encouraged — and often produce the most
interesting final projects.

---

### Idea A: Infrastructure Health Dashboard

**What it does:** Monitors the health of a local or containerized environment
and serves a live HTML dashboard.

**How it works:**

- Bash scripts collect metrics: disk usage, CPU load, running processes, log
  file sizes, Docker container status
- A Python aggregator reads the Bash output, normalizes it into a structured
  JSON store, and detects thresholds (e.g., disk > 85%)
- A GitHub Actions cron workflow runs the collection pipeline on a schedule
  and commits updated JSON to the repository
- A Docker container hosts a simple Python HTTP server that renders the JSON
  as an HTML health dashboard

**Key deliverables:** Bash metric collectors, Python aggregator with pytest
suite, Dockerfile + docker-compose, GitHub Actions cron workflow, HTML dashboard
generator, alert log when thresholds are exceeded.

---

### Idea B: Dev Environment Bootstrap Tool

**What it does:** Provisions a fresh development environment idempotently from
a single command.

**How it works:**

- A Bash installer checks for and installs required language runtimes, tools,
  and dotfiles from a Git repository (idempotent — safe to run multiple times)
- A Python validator runs health checks on the provisioned environment and
  produces a JSON audit report of what was installed, skipped, or failed
- A Dockerfile defines a reproducible service (database, cache, or message
  queue) started by the installer
- A GitHub Actions smoke-test workflow clones a fresh Ubuntu environment,
  runs the installer, and verifies the validator passes

**Key deliverables:** Idempotent Bash installer with rollback on failure,
Python validator with pytest suite, Dockerfile for services, GitHub Actions
smoke-test, JSON audit report with timestamps.

---

### Idea C: Multi-Project CI/CD Aggregator

**What it does:** Polls multiple GitHub repositories for pipeline health,
detects anomalies, and generates daily summary reports.

**How it works:**

- A Python client polls the GitHub REST API for pipeline run results across
  a configurable list of repositories (with retry logic and rate-limit handling)
- An anomaly detector flags repeated failures, slow builds, and flapping tests
  using rolling-window statistics
- Results are stored in a local SQLite database with a schema designed for
  trend queries
- A report generator produces HTML and CSV summaries per repository per day
- The entire pipeline runs inside a Docker container triggered by a GitHub
  Actions cron job that uploads the reports as artifacts

**Key deliverables:** Python API client, anomaly detector, SQLite schema,
HTML/CSV reporter, Dockerfile, GitHub Actions cron workflow with artifact upload.

---

### Idea D: Log Intelligence Pipeline

**What it does:** Ingests raw log files, parses and analyzes them, detects
error spikes, and rotates processed logs automatically.

**How it works:**

- A Bash watcher monitors a configurable directory for new or modified log
  files (using polling or `inotifywait`)
- A Python parser handles multiple formats (syslog, JSON-structured, Apache
  access, custom application logs), extracts error events, and detects spikes
  using rolling-window statistics
- A rotation module compresses processed logs with gzip and enforces a
  retention policy
- On each push, a GitHub Actions workflow runs the full pipeline against
  sample log files, verifies tests pass, and uploads a structured JSON report
  as an artifact

**Key deliverables:** Bash watcher, Python multi-format parser, spike
detector, rotation module, GitHub Actions workflow with artifact upload,
pytest suite with ≥70% coverage.

---

### Idea E: Containerized Code Quality Gate

**What it does:** Accepts a Git repository URL, runs a full quality scan
inside Docker, and produces a structured pass/fail report.

**How it works:**

- A Bash orchestrator clones the target repository into a Docker container,
  runs the quality engine, and collects the output
- A Python quality engine runs shellcheck on Bash files, pylint + black on
  Python files, and a custom pattern-matching script that flags common secret
  patterns (API keys, passwords, tokens)
- The engine produces a structured JSON report and an HTML summary with
  per-file scores and issue counts
- A GitHub Actions integration posts a pass/fail status check back to the
  scanned repository via the GitHub Checks API

**Key deliverables:** Bash orchestrator, Python quality engine, secret scanner,
Dockerfile, JSON + HTML report generator, GitHub Actions integration.

---

## Proposal Requirements

Your `PROPOSAL.md` must address all six sections defined in the root
`PROPOSAL.md` file:

1. **Problem Statement** — what the tool solves, who uses it, why automation
2. **Technical Design** — component table, domain checklist (≥3), data flow,
   dependencies
3. **Scope and Feasibility** — core features, stretch features, justification,
   risk table
4. **Git and Collaboration Plan** — repo URL, ≥4 planned branches with owners,
   conventional commits confirmation, work division
5. **Timeline and Milestones** — a clear roughly 10-day plan with named owners
6. **Testing Strategy** — ≥2 concrete methods, measurable Definition of Done

See `docs/proposal_rubric.md` for the complete grading rubric.

---

## Approval Workflow

| Score | Outcome |
| --- | --- |
| 12–15 | Auto-approved as submitted |
| 9–11 | Approved with required revisions documented in Canvas feedback |
| Below 9 | Requires a meeting with the instructor and resubmission |

You will receive feedback on Canvas within 3 business days of submission.
**Do not begin Part 2 implementation until you receive approval.**

---

## Timeline

Plan your work across a roughly 10-day implementation window after approval.

| Day | Milestone |
| --- | --- |
| Day 0 | Proposal submitted and awaiting approval |
| Day 1 | Instructor approval received; implementation begins |
| Day 3 | Core Bash and Python components functional |
| Day 5 | Docker and/or CI/CD components integrated |
| Day 7 | All core features complete; tests passing |
| Day 9 | Documentation polished; video recorded |
| Day 10 | Canvas submission with GitHub link and video link |

---

## Getting Started

```bash
# 1. Create your project repository on GitHub
# 2. Clone it locally
git clone https://github.com/YOUR-ORG/YOUR-REPO.git
cd YOUR-REPO

# 3. Fill in PROPOSAL.md completely, then push
git checkout -b feature/proposal
git add PROPOSAL.md
git commit -m "docs(proposal): add initial capstone proposal"
git push -u origin feature/proposal
# Open a PR → merge → submit the GitHub link on Canvas
```
