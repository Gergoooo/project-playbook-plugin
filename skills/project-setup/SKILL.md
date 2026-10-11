---
name: project-setup
description: Docs-first process for bootstrapping a new software project with Claude Code — scoping, docs, repo + hooks setup, module/PR pipeline with dual builders and a verifier, and a Resume protocol. Use when the user starts a new project, asks to set up a repo/docs/workflow, or wants to resume one built this way.
---

# Project setup playbook

Process for going from first conversation to "modules landing via a dual-builder pipeline." Follow roughly in order; skip steps that don't apply. Read only the reference file for the step you are on.

**Not every project needs every step.** Choose Solo / Small app / Full pipeline first (`references/right-size.md`); it says which steps to skip. Assumes GitHub + `gh` and Claude Code.

## Standing rules (always)
- **Docs before code.** No application code until the docs in `references/docs.md` exist.
- **Epic gate:** the next epic starts only when the current one is fully done; otherwise warn and list what's missing (`/project-playbook:next-epic`).
- **User decides at every module/phase boundary.** Each module = one PR into `dev`; the user's merge is the gate. Never auto-proceed.
- **Ask before adding anything secret-related to `.gitignore`** — propose exact patterns, get confirmation.
- Verify subagent claims yourself (or via `module-verifier`); never relay "tests passed" unchecked.
- Don't trust GitHub star counts; read skill/plugin content directly before installing.

## Steps
| # | Step | Read |
|---|---|---|
| 0 | Scope the idea (plan mode) **and pick a tier** | `references/scoping.md`, `references/right-size.md` |
| 1 | Docs before code (+ `Current status` block in ROADMAP) | `references/docs.md` |
| 2–3 | Repo setup, `.gitignore` | `references/repo-setup.md` |
| 4 | Full review pass before code | `references/review-pass.md` |
| 5 | Break roadmap into modules | `references/modules.md` |
| 6 | Branching model (`dev` / `main`) | `references/branching.md` |
| 7–8 | Subagent pipeline + gotchas | `references/subagents.md` |
| 9 | Failsafes: CLAUDE.md Resume protocol, hooks | `references/failsafes.md` |
| 10 | Sourcing skills/plugins | `references/skills-sourcing.md` |
| 11 | Save durable lessons | `references/memory.md` |

Start with `references/adapt.md` (fit the scaffold to the project type) and `references/right-size.md`.

## Templates (`templates/`)
- Docs: `README.md`, `ARCHITECTURE.md`, `API.md`*, `DATA_MODEL.md`*, `ROADMAP.md`, `DECISIONS.md`, `TESTING.md`, `WORKFLOW.md`, `ATTRIBUTIONS.md`*, `DEPLOYMENT.md`*, `features/` (*conditional on project type)
- `CLAUDE.md` — repo CLAUDE.md with the Resume protocol block
- `github/pull_request_template.md`, `github/playbook-checks.yml` (CI enforcement)
- `githooks/pre-push`, `githooks/pre-commit`, `gitleaks.toml`, `gitignore.base`, `github-workflows/ci.yml`
- `agents/module-builder.md`, `module-tester.md` (instantiate per stack), `module-verifier.md`

Replace every `<placeholder>` when copying. Commands: `/project-playbook:new-project [--auto]` scaffolds; `/project-playbook:resume` reports status; `/project-playbook:next-epic [N]` runs the epic completion gate (`scripts/epic-gate.py`); `/project-playbook:adopt` retrofits an existing repo; `/project-playbook:start-module <id>` runs the per-module pipeline; `/project-playbook:retro [N]` records an epic retrospective.
