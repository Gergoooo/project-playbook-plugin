---
description: Run the per-module pipeline for one story (gate check, sizing, builders, tester, synthesis, verifier) and stop at the user's PR gate
argument-hint: "<module id, e.g. 1.4>"
---

Run the playbook's per-module pipeline for module $ARGUMENTS. Read `docs/WORKFLOW.md`, `CLAUDE.md`, and the module's ROADMAP row first. You are the orchestrator; the user is the only decision-maker.

## 0. Preconditions (stop and report if any fails)
- Run `python3 scripts/epic-gate.py . --start <epic of this module>` — if earlier epics are incomplete, show the warning + missing list and stop (only the user can override).
- The module's `Depends on` are all ✅ and merged. Working tree clean, on `dev` (or the epic branch if the phase has `Epic branch:`), up to date. `core.hooksPath` set.
- Run a Bash command with `cwd` in the target repo before dispatching (worktree gotcha, see WORKFLOW "Known issues").

## 1. Size the story (S / M / L) — rules in `references/subagents.md` "Scaling agents to task size"
Tell the user the size and agent count you chose and why, in one line; the tier caps it.

## 2. Dispatch (parallel, each in its own worktree, none opens a PR)
- **S:** 1 builder + tester. **M:** Builder-A, Builder-B, tester. **L:** write the slicing plan + slice contract on `module/<id>-int` first, then one builder per slice (+ tester(s)). Use the project's `.claude/agents/*` definitions; if named dispatch isn't available use `general-purpose` with the agent file inlined. Give each only the module scope and linked docs, never the whole roadmap.
- Builders end with 2–5 sentences of design rationale. Tester works from the spec only and never reads a builder's code.

## 3. Synthesis (you, not delegated)
Read the diffs and rationale, run the tester's suite on each candidate (or merge slices into `module/<id>-int` in dependency order), pick/merge, and state the reasoning. Re-run tests yourself; don't relay builder claims.

## 4. Verify
Dispatch `module-verifier` on the synthesized branch (no Write/Edit). Include its real output.

## 5. Prepare the PR — do not merge
Update ROADMAP: mark the story ✅ (only if verifier passed; otherwise note the caveat) and refresh `## Current status`. Open one PR into `dev` (or the epic branch) from the synthesized branch with: both candidates' key differences / slice summary, synthesis reasoning, verifier results, agent count, any unverified caveats. Delete losing candidate branches and worktrees only after the PR is merged.

## 6. Stop
Report PR link and a ≤5-line summary. Never start the next module, never merge, never push to `main`/`dev`.
