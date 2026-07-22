# CS 3030 — Final Capstone Project

Weber State University | Scripting Languages

---

## Welcome

This is your starter repository for the CS 3030 Final Capstone Project. You
will design and build an original automation tool that integrates at least
**three** technology domains you have learned this semester: Bash scripting,
Python scripting, Docker, CI/CD pipelines, and logging/security practices.

The project has three graded parts:

| Part | What | Points | First step |
| --- | --- | --- | --- |
| **Part 1 — Proposal** | Define what you will build | 15 pts | Fill in `PROPOSAL.md` |
| **Part 2 — Implementation** | Build and demo it | 175 pts | Start after proposal is approved |
| **Part 3 — Reflection** | Complete the feedback quiz | 30 pts | After Part 2 submission |
| | | **220 pts total** | |

Read the full instructions for each part in the course project folder before
you begin.

---

## Team Setup

Teams of `2 or 3` ARE required. Solo students are NOT allowed.

**If you are working as a team:**

1. Your professor will create the repo and send invitation for all team members. 
3. All members should clone the repository and confirm they can push.
4. All members must appear as commit authors in the Git history.

---

## Part 1: Proposal

**Due before you write any implementation code.**

1. Open `PROPOSAL.md` in this repository and edit it in place.
2. Fill in every section. Delete all instruction comments.
3. Commit and push your changes on a feature branch.
4. Open a pull request and merge it into `main`.
5. Submit the GitHub repository link on Canvas.

Your instructor will review the proposal and provide approval feedback on
Canvas. **Do not begin Part 2 until you receive approval.**

---

## Part 2: Implementation

**Begins after proposal approval and runs across a 10-day build window.**

Build the tool you proposed. As you work, maintain the Git workflow below.

### Git Workflow Requirements

| Requirement | Minimum |
| --- | --- |
| Feature branches | 5 with descriptive names |
| Merged pull requests | 3 (teams: ≥1 reviewed by partner) |
| Conventional commits | 15 (`feat:` `fix:` `docs:` `test:` `chore:`) |
| Commit cadence | Spread across the 10-day implementation window |
| Merge conflict resolved | 1, documented in PR or commit message |

Install the commit-msg hook now so conventional commits are enforced from
the start:

```bash
bash scripts/setup-hooks.sh
```

### What to Build

Your `src/` directory is empty — structure it however your tool requires.
Common layouts:

```text
src/
├── monitor.sh          # Bash orchestrator
├── analyzer.py         # Python processor
├── Dockerfile
├── docker-compose.yml
└── tests/
    └── test_analyzer.py
```

### README as Your Project Landing Page (20 points)

Your `README.md` is your project's front door — treat it as a sales pitch and
setup guide rolled into one. A grader or new user must be able to understand,
install, and run your tool using only this file. It is graded under the
Documentation category (20 points) and is one of the highest-leverage things
you can polish before submission.

By submission time your `README.md` **must** replace all placeholder text and
include:

- **What your tool does** — 2–3 sentences that make the purpose and value
  immediately clear to someone who has never seen the project
- **Architecture diagram** — even a simple ASCII diagram showing how Bash,
  Python, Docker, and/or CI/CD components connect
- **Step-by-step setup and run instructions** — tested on a clean machine;
  every command shown should actually work
- **Example commands with expected output** — show what success looks like
- **How to run the tests** — exact command, expected coverage output
- **Known limitations** — be honest about what the tool does not handle
- **Reflection paragraph** — what worked, what you would change, what you
  learned (this is separate from the Canvas reflection quiz)

Delete every line that still says "TODO" or looks like starter-template
boilerplate before you submit.

### CI Workflow

A starter GitHub Actions workflow is in `.github/workflows/ci.yml`. Update
it as you add code — at minimum it must have two passing jobs on `main` by
submission time.

---

## Submission

### Part 1 — Proposal
Submit the GitHub repository link on Canvas after merging `PROPOSAL.md` to
`main`. Wait for instructor approval before beginning Part 2.

### Part 2 — Implementation
When your project is complete:

1. Confirm all items in the submission checklist (see the full project
   instructions) are checked off.
2. Ensure your `README.md` is polished and complete (see above — it is graded).
3. Record your 10–15 minute video demo (all team members must appear and present).
4. Submit on Canvas with:
   - The GitHub repository URL
   - The video link (YouTube/Vimeo/Loom — unlisted)

### Part 3 — Reflection Quiz
After submitting Part 2, complete the **Capstone Reflection Quiz** on Canvas.

- The quiz is **individual** — each team member submits their own responses.
- It asks what worked well, what you would change, what you learned, and a
  self-assessment of your contribution.
- Worth **30 points**. Submit before the Canvas deadline; no extensions.
- The quiz closes automatically — do not wait until the last minute.

---

## Quick Reference

```bash
# Install git hooks (run once after cloning)
bash scripts/setup-hooks.sh

# Run Python tests with coverage
pytest src/ --cov=src --cov-report=term-missing

# Lint Bash files
shellcheck src/*.sh

# Lint Python files
pylint src/*.py
black --check src/

# Check CI workflow locally (optional, requires act)
act push
```
