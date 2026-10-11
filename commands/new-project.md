---
description: Scaffold any new project with the docs-first playbook (scoping → docs → repo hygiene → roadmap modules → agents/hooks)
argument-hint: "<project idea> [--auto]"
---

Use the `project-setup` skill to set up a new project: $ARGUMENTS

Works for any kind of project (app, service, CLI, library, data/ML, game, embedded, infra). Do not assume a stack — derive everything from the idea and the user's answers. Read `references/adapt.md` first, then only the reference file for the step you are on.

## Modes
- **Interactive (default):** enter plan mode for step 0, ask the user (AskUserQuestion) for the decisions that are genuinely theirs, recommend one option with the tradeoff, and stop at each human gate below.
- **`--auto`:** no questions. Take your own recommendation for every decision and record each as an assumption in `docs/DECISIONS.md` under "Assumptions (auto mode)". Work in the current directory (create the repo dir(s) as subdirectories). **Local only**: `git init` yes; never run `gh repo create`, never add a remote, never push. Secret-related `.gitignore` patterns are still written but listed in DECISIONS as "proposed — needs user confirmation". Used for dry runs and tests.

## Steps
1. **Scope (step 0):** restate the idea, list features, constraints (budget, privacy/legal, solo/team, timeline, distribution), pick the **tier** (`references/right-size.md`) and **project type** (`references/adapt.md`). Decide repo count/layout.
2. **Docs (step 1):** from `templates/`, create the docs the project type needs — README, ARCHITECTURE, ROADMAP (with `## Current status`), DECISIONS (Context/Decision/Why, newest first + Open questions), TESTING, WORKFLOW, `features/` (README + one doc per feature), and conditionally API, DATA_MODEL, ATTRIBUTIONS, DEPLOYMENT. Fill them with real, project-specific content — no leftover `<placeholders>`. No application code.
3. **Repo (steps 2–3, 6):** `git init`, create `dev` branch, local identity if unset. Write `.gitignore` (stack build-noise freely; secret patterns confirmed with the user or flagged in auto mode). Interactive: confirm names, then create private repo(s) with `gh`.
4. **Review pass (step 4):** go through every checklist item in `references/review-pass.md`; each becomes a DECISIONS entry or an explicit "n/a — reason". Open questions go in DECISIONS' Open questions.
5. **Modules (step 5):** write ROADMAP phases → groups → module tables with Scope / Depends on / Test plan columns. For the Full tier, ask (or in auto mode decide and record) whether any phase should use an epic branch — recommend it only for phases whose stories are unusable until all land (see `references/branching.md`); mark those phases `Epic branch: epic/<name>`. Phase 0 = skeleton, CI, and (if hosted) hosting + secrets + auth. Every feature gets modules. Link each phase to its feature doc. Note account prerequisites inline on the row that needs them.
6. **Failsafes (step 9):** `CLAUDE.md` from the template (stack filled in, Resume protocol verbatim, local setup), `.githooks/pre-push` + `pre-commit` (executable), `.gitleaks.toml`, `git config core.hooksPath .githooks`, CI workflow from `templates/github-workflows/ci.yml` with the real toolchain. Verify a direct push to `main`/`dev` is blocked (local test against a bare temp remote is fine).
7. **Agents (step 7):** `.claude/agents/` (if writes to `.claude/` are denied in a non-interactive session, write them to `agents-pending/` and say so in the final report — never skip them) — instantiate builder + tester per stack from the templates, plus `module-verifier`. Tier "Solo script" skips agents.
8. **Consistency + self-verify:** re-read the docs once for agreement (names, endpoints, tables, module ids, tier). Then run `python3 <skill dir>/scripts/verify.py <project root> --expect <docs you decided to include, e.g. api,data_model,ci,features; add tier:solo for the solo tier>` and fix every failing item, then re-run until it passes or the failure is a deliberate omission you record in DECISIONS.
9. **Commit** the scaffold on a docs branch (not `main`/`dev` directly if a remote exists); in auto mode commit locally.

## Gates (interactive mode)
Stop and ask before: repo creation/push, `.gitignore` secret patterns, anything outside the project directory. Never start a module — that is the user's decision after the setup PR merges.

## Final report
List: project type + tier chosen, files created, assumptions made (auto), open questions, and the first module that would be next.
