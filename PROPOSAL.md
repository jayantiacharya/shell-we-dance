# Final Capstone Proposal

**CS 3030 - Scripting Languages**
**Team Members:** [Name 1] (A#######) | [Name 2] (A#######)
**Date:** YYYY-MM-DD

> **Instructions:** Fill in every section below. Delete all instruction
> comments (lines starting with `>`). Commit this file on a feature branch,
> open a PR, merge it into `main`, and submit the GitHub link on Canvas.
> Do not begin implementation until your instructor approves this proposal.
> This file is intentionally both the editable template and the final submitted
> proposal. Edit it directly.

---

## Section 1: Problem Statement

### What problem does your tool solve?
<!-- 2-4 sentences. Be specific. "Automate X because Y is currently painful/manual/error-prone." -->

### Who would use this tool and how?
<!-- Describe a realistic user and a typical workflow scenario. -->

### Why is automation the right solution here?
<!-- Explain why a script/pipeline beats a manual process or a GUI tool. -->

---

## Section 2: Technical Design

### Core Components

<!-- List each component, its technology, and its responsibility.
     You must use at least 3 technology domains. -->

| Component | Technology | Responsibility |
| --- | --- | --- |
| e.g. `monitor.sh` | Bash | Watches directory, triggers pipeline |
| e.g. `analyzer.py` | Python | Parses logs, generates JSON report |
| e.g. `Dockerfile` | Docker | Containerizes the Python analyzer |
| e.g. `ci.yml` | GitHub Actions | Runs pipeline on push, uploads artifact |

### Technology Domains Used

<!-- Check all that apply. You must check at least 3. -->

- [ ] Bash scripting (file operations, error handling, functions)
- [ ] Python scripting (data processing, pytest, argparse)
- [ ] Docker / container orchestration
- [ ] CI/CD pipelines / GitHub Actions
- [ ] Logging, archiving, and security best practices

### Data Flow Diagram

<!-- ASCII diagram or written description showing how data moves through your system. -->

```text
[input source] --> [component A] --> [component B] --> [output artifact]
```

### External Dependencies

<!-- List pip packages, Docker base images, GitHub APIs, or third-party services you plan to use. -->

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
