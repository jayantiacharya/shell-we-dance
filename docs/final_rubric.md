# CS 3030 Project 7 Part 2 — Final Implementation Grading Rubric

Total Points: 175 (+ up to 15 bonus)

Because every student's project is different, this rubric evaluates
**technology-domain quality** rather than specific functions. The same criteria
apply to all projects regardless of what the tool does.

**Solo and team students are graded identically.** The scope requirement (≥3
domains) is the same for everyone.

---

## Category 1: Bash Component (25 points)

Evaluates the quality of all Bash scripting in the project. If your project
uses no Bash at all, this category scores 0 — plan your domain selection
accordingly.

| Points | Level | Description |
| --- | --- | --- |
| 23–25 | Excellent | All scripts are shellcheck-clean (0 warnings). Every function uses `local` variables and accepts parameters. Meaningful exit codes (0 = success, 1 = general, 2 = config, 3 = dependency) with errors written to stderr. Timestamped log file with `[INFO]` / `[WARN]` / `[ERROR]` prefixes. Color-coded console output. At least 4 well-named functions. Scripts do not require root where avoidable. |
| 18–22 | Good | Shellcheck-clean or 1–2 minor warnings. Good function structure with local variables. Error handling present and mostly correct. Basic logging present. Reliable for all documented use cases. |
| 12–17 | Fair | Multiple shellcheck warnings or 1–2 errors. Some functions but inconsistent local variable use. Basic error handling with gaps on edge cases. Limited or absent logging. Works on the happy path but fails on edge cases. |
| 0–11 | Needs Work | Many shellcheck errors. No functions or no local variables. No meaningful error handling. No logging. Scripts unreliable or non-functional. |

---

## Category 2: Python Component (25 points)

Evaluates the quality of all Python scripting in the project.

| Points | Level | Description |
| --- | --- | --- |
| 23–25 | Excellent | All functions have type hints and comprehensive docstrings (args, returns, raises). `argparse` CLI with helpful `--help` output. `pylint` score ≥ 7.0 and `black`-formatted. Custom exception types used where appropriate. `logging` module throughout (no bare `print` statements for program output). Python stdlib used for core logic with justified third-party dependencies. |
| 18–22 | Good | Most functions have type hints and docstrings. `argparse` present. `pylint` score ≥ 6.0. Code mostly `black`-formatted. `logging` module used. Minor style issues. |
| 12–17 | Fair | Some type hints and docstrings. Basic `argparse` or `sys.argv`. `pylint` score 4.0–6.0. Mixed `print`/`logging`. Multiple style issues. |
| 0–11 | Needs Work | Missing type hints and docstrings. No argument parsing or hard-coded values. Low pylint score. `print()` instead of `logging`. Code hard to read or understand. |

---

## Category 3: Integration Component (20 points)

Evaluates the best third technology domain beyond Bash and Python. If your
project integrates multiple additional domains, you are graded on the
highest-quality one. A fourth domain in good shape can earn bonus points.

Choose the sub-option that matches your project:

---

### Sub-option A: Docker Integration

| Points | Level | Description |
| --- | --- | --- |
| 18–20 | Excellent | Multi-stage `Dockerfile` producing a final image ≤ 300 MB. Non-root user configured. `HEALTHCHECK` instruction present. `docker-compose.yml` with named volumes and a custom network. Bash orchestrator calls Docker correctly with proper volume mounts and environment variable passing. Full end-to-end workflow runs via `docker compose up`. |
| 13–17 | Good | Functional `Dockerfile` (single- or multi-stage). Non-root user present. `docker-compose.yml` mostly configured. Integration between Bash and Docker works for documented use cases. |
| 8–12 | Fair | `Dockerfile` present but with notable issues (runs as root, no health check, or bloated image). `docker-compose.yml` incomplete. Integration partially working. |
| 0–7 | Needs Work | `Dockerfile` non-functional or missing. `docker-compose.yml` missing or broken. Integration does not work. |

---

### Sub-option B: CI/CD (GitHub Actions)

| Points | Level | Description |
| --- | --- | --- |
| 18–20 | Excellent | Workflow with at least 3 jobs using `needs:` for sequencing. Matrix build (e.g., Python 3.11 + 3.12). Artifact upload in the build or test job. Quality gates enforced (shellcheck, pylint ≥ 7.0, pytest coverage ≥ 70%). `workflow_dispatch` trigger. All jobs currently passing on `main`. |
| 13–17 | Good | Workflow with 2–3 jobs. Basic quality gates. Artifact upload present. Jobs passing on `main`. |
| 8–12 | Fair | Workflow with 1–2 jobs. Missing quality gates or artifact management. Some jobs failing or intermittent. |
| 0–7 | Needs Work | Workflow missing, broken, or has never passed. |

---

### Sub-option C: Logging, Archiving, and Security

| Points | Level | Description |
| --- | --- | --- |
| 18–20 | Excellent | Structured JSON logging in Python with ISO 8601 timestamps. Correlation IDs generated at script start and passed through all components. Audit log entries following WHO/WHAT/WHEN/WHERE pattern. Bash log format consistent with Python format. Log rotation with gzip compression and retention enforcement (age and count). File permissions enforced (600 for config, 644 for logs, 700 for scripts). Path traversal prevention (`..` patterns rejected). No hardcoded credentials. |
| 13–17 | Good | Structured logging in Python. Some correlation ID usage. Basic audit log. Rotation present. File permissions mostly correct. No credentials in code. |
| 8–12 | Fair | Basic logging without structured format. No correlation IDs. Limited audit log. Rotation incomplete. Permission issues present. |
| 0–7 | Needs Work | No structured logging. No audit trail. No rotation. Security issues present (hardcoded credentials, wrong permissions, no path validation). |

---

## Category 4: Testing and Quality Gates (20 points)

| Points | Level | Description |
| --- | --- | --- |
| 18–20 | Excellent | `pytest` suite with ≥70% coverage verified via `pytest-cov`. Tests cover at least one integration scenario (not only unit tests). At least one test for an error or edge case. All tests passing. `commit-msg` hook installed and blocking non-conventional commits. shellcheck and pylint run in CI and enforced as quality gates. |
| 13–17 | Good | `pytest` suite with ≥50% coverage. Tests mostly passing. `commit-msg` hook present. CI quality checks present with minor gaps. |
| 8–12 | Fair | Some pytest tests but coverage < 50% or multiple failures. Hook present but not enforced. CI has checks but they are not gating (workflow continues on failure). |
| 0–7 | Needs Work | Fewer than 5 tests or tests do not run. No hooks. No CI quality gates. |

---

## Category 5: Documentation (20 points)

| Points | Level | Description |
| --- | --- | --- |
| 18–20 | Excellent | `README.md` serves as the project's **landing page** — a grader or new user can understand, set up, and run the tool from it alone. Contains all required sections: clear description (2–3 sentences), architecture diagram, tested step-by-step setup, example commands with expected output, how to run tests, known limitations, and a thoughtful reflection paragraph. No placeholder or TODO text remains. All Python functions have complete docstrings. All Bash functions have header comments explaining purpose and parameters. Proposal deviations documented. |
| 14–17 | Good | `README.md` covers most required sections with real content (not placeholder text). Most Python functions have docstrings. Most Bash functions have header comments. Minor gaps. |
| 9–13 | Fair | `README.md` present but missing multiple required sections, retains placeholder text, or setup instructions have not been tested. Docstrings and comments sparse. |
| 0–8 | Needs Work | `README.md` is minimal or still looks like the starter template. Setup instructions missing or broken. No docstrings or comments. |

---

## Category 6: Git Workflow and Collaboration (20 points)

| Points | Level | Description |
| --- | --- | --- |
| 18–20 | Excellent | 5+ feature branches with descriptive names (e.g., `feature/bash-monitor`, `feature/log-parser`). 3+ merged PRs; for teams, at least 1 PR reviewed and approved by the other member with review comments visible. 15+ commits with conventional format (`feat:` `fix:` `docs:` `test:` `chore:`). Regular commit cadence — commits spread across the 10-day implementation window with no large dump commits. 1+ documented merge conflict (resolved and noted in PR description or commit message). `git log --graph` shows clean branching history. |
| 13–17 | Good | 5+ branches. 3+ PRs. 12–14 commits with mostly conventional format. Regular cadence. 1 conflict resolved. Readable history. |
| 8–12 | Fair | 3–4 branches. 2 PRs. 8–11 commits with inconsistent format. Some large dump commits. Conflict resolved but not documented. |
| 0–7 | Needs Work | Fewer than 3 branches. 0–1 PRs. Fewer than 8 commits or all commits on `main`. No merge conflict evidence. |

> **Teams:** If one member has zero commits, the team receives **0 points** in
> this category regardless of total commit count.

---

## Category 7: Video Demo / Presentation (30 points)

This is a professional deliverable. Students are encouraged to treat it as
something they could show a potential employer — it should demonstrate not
only that the tool works, but that the team understands why it was built, how
it is designed, and what they learned from building it.

**For teams: every member must appear on screen and present a substantive
portion of the video.** A video where one member does all the talking scores
in the Fair range at best, regardless of technical quality.

| Points | Level | Description |
| --- | --- | --- |
| 27–30 | Excellent | 10–15 minute video. All team members appear on screen and each presents a clearly owned section. Opens with a compelling problem statement — explains the pain point and why automation solves it. Live end-to-end demo with real (non-trivial) data producing meaningful output. Walks through every integrated component (Bash, Python, and the chosen third domain) with code visible on screen. Architecture diagram referenced during the walkthrough. Code deep-dive into at least one complex function per language. Git branch graph shown (`git log --graph --oneline`) with a PR and the merge conflict resolution explained. Closes with a genuine reflection: what worked, what broke, what each member would do differently. Clear audio, readable screen, and professional enough to share with a recruiter. |
| 20–26 | Good | Video within the time range. All or most team members present. Problem statement explained. Demo shows the tool working end-to-end. All major components covered. Code walkthrough present. Git workflow shown. Reflection included. Minor gaps in depth or polish. |
| 10–19 | Fair | Video present but missing 1–2 required sections, or only one team member presents the entire video. Demo partially works or skips components. Architecture surface-level. Git workflow absent or superficial. Reflection missing or one sentence. |
| 0–9 | Needs Work | Video shorter than 5 minutes, missing, or so incomplete that it does not demonstrate the project. No real demo. No architecture explanation. No Git discussion. |

---

## Bonus Points (up to +15)

Awarded at the instructor's discretion for work that is genuinely exceptional.
No partial credit within bonus categories.

| Bonus | Points | Criteria |
| --- | --- | --- |
| Extra domain | +5 | Integrates a 4th technology domain at the same quality level as the three primary ones |
| Advanced CI | +5 | GitHub Actions workflow includes a scheduled (cron) trigger, real deployment step, or external API integration beyond the GitHub Checks API |
| Security excellence | +5 | Implements secret scanning (gitleaks or detect-secrets) in CI, enforces signed commits, or achieves pylint ≥ 9.0 across the entire codebase |

---

## Score Summary

| Category | Max Points |
| --- | --- |
| Bash Component | 25 |
| Python Component | 25 |
| Integration Component | 20 |
| Testing and Quality Gates | 20 |
| Documentation | 20 |
| Git Workflow and Collaboration | 20 |
| Video Demo / Presentation | 30 |
| **Base Total** | **160** |
| **Instructor Bonus** | **up to +15** |
| **Canvas Assignment Total** | **175** |
