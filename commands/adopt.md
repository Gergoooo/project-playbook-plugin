---
description: Retrofit the playbook onto an existing project (adds Current status, Resume protocol, hooks, epic gate, missing docs) without overwriting anything
argument-hint: "[--auto]"
---

Use the `project-setup` skill to adopt the playbook in the **current repo**, which already has code and/or docs. Never overwrite or delete existing content — merge into it. Skill files (`references/`, `templates/`, `scripts/`) live in `${CLAUDE_PLUGIN_ROOT}/skills/project-setup/`. Read `references/adapt.md` and `references/right-size.md` first.

## Modes
- **Interactive (default):** show the audit and the proposed change list, and wait for the user's go before writing.
- **`--auto`:** no questions; apply the plan, but work only on a new branch `docs/adopt-playbook`, never push, never create PRs. Used for dry runs on copies.

## Steps
1. **Audit (read-only).** Run `python3 "${CLAUDE_PLUGIN_ROOT}/skills/project-setup/scripts/verify.py" . --expect <docs that apply>` to see what's missing; read the existing README, docs/, CLAUDE.md, ROADMAP/TODO files, CI config, `.githooks`/`.husky`, `.gitignore`, and `git log -20`, `git branch -a`, `gh pr list --state all --limit 20` (if `gh` works). Classify the project type and tier (`adapt.md`, `right-size.md`).
2. **Reconstruct real status.** From git history, open PRs, branches, tests and the existing roadmap (or TODOs), work out what is done, in flight and next. Do not invent: mark unknowns as "unknown — confirm with user".
3. **Plan the change list** (additions only): missing docs from `templates/` filled with content derived from the real code, not placeholders; `## Current status` block in ROADMAP (create ROADMAP from existing plans/issues if none); Resume protocol + standing rules appended to an existing CLAUDE.md (keep everything already there; if none, create from template); `dev`/`main` branches if missing (ask before creating on a remote); hooks in `.githooks/` (pre-push, pre-commit) and `.gitleaks.toml` — if the project already has a hook manager (husky, pre-commit framework, lefthook) integrate with it instead of replacing it; copies of the plugin's `epic-gate.py` + `verify.py` in the project's `scripts/` (from `${CLAUDE_PLUGIN_ROOT}/skills/project-setup/scripts/`); PR template and `playbook-checks.yml` workflow (`templates/github/`); `.claude/agents/` per stack if the project will use the module pipeline (skip for solo tier); mark existing finished work with ✅ in the roadmap so the epic gate is meaningful.
4. **Show the list and wait** (interactive). Anything touching `.gitignore` secret patterns, existing CI, existing hooks or remote branches needs explicit confirmation.
5. **Apply on a branch** `docs/adopt-playbook` forked from `dev` (or the default branch). Do not touch application code. Commit.
6. **Self-verify:** run `verify.py` and `epic-gate.py --no-gh`; fix gaps. Open the PR into `dev` only after the user says so (interactive).

## Final report
What was added, what was merged into existing files, what was left alone, reconstructed status with its confidence, and open questions for the user. Never start a module.
