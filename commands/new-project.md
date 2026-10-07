---
description: Scaffold a new project using the docs-first playbook (scoping → docs → repo hygiene → module pipeline)
argument-hint: "[short project idea]"
---

Use the `project-setup` skill to set up a new project: $ARGUMENTS

Work through the skill's steps in order, reading only the reference file for the current step.

1. **Scope (step 0):** enter plan mode, interrogate the idea, ask which tier (see `references/right-size.md`) and skip steps accordingly, give recommendations with tradeoffs, record constraints (budget, privacy, solo/team, timeline).
2. **Docs (step 1):** create the docs from `templates/` (ROADMAP with `## Current status`, WORKFLOW, DECISIONS, plus README/ARCHITECTURE/DATA_MODEL/TESTING and `API.md` if client/server). No application code yet.
3. **Repo (steps 2–3, 6):** confirm repo layout and names with the user before `git init`/`gh repo create`. Create `dev`. Propose exact `.gitignore` secret patterns and **wait for explicit confirmation**; add plain build-noise without asking.
4. **Review pass (step 4)** against the checklist; write findings into DECISIONS.
5. **Modules (step 5):** break ROADMAP into modules with Scope / Depends on / Group / Test plan.
6. **Failsafes (step 9):** copy `templates/CLAUDE.md` (fill the stack), `templates/githooks/*` to `.githooks/`, `gitleaks.toml` to `.gitleaks.toml`; run `git config core.hooksPath .githooks`; test that a direct push to `main`/`dev` is blocked.
7. **Agents (step 7):** copy `templates/agents/module-verifier.md`; write stack-specific builder and tester agents.

Stop and ask at each of: repo creation/push, `.gitignore` secret patterns, and the end of every step that changes remote state. Never start a module — that is the user's decision after the setup PR merges.
