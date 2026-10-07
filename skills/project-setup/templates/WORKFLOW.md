# Workflow

## Modules
Each module has **Scope** (files/dirs it owns, no overlap within a group), **Depends on**, **Group** (batch; batches run in sequence), **Test plan**.

**Each module ships as one PR into `dev`. The human's PR approval is the decision gate** — nothing auto-proceeds to the next module, group, or phase. Every module PR also updates `ROADMAP.md`'s `## Current status`.

## Branches
- `dev` — integration; all module PRs merge here.
- `main` — stable/deployed; moves only via a deliberate `dev`→`main` promotion PR. Deploy CI triggers on `main` only.
- Module branches: `module/<id>-a`, `-b`, `-tests`, forked from `dev`, deleted after merge.
- No direct pushes to `main`/`dev` (local `pre-push` hook).

## Per-module pipeline
1. Dispatch in parallel, each in its own worktree: Builder-A, Builder-B (same brief, independent), Tester (spec only, never reads builders' code). None open a PR.
2. Orchestrating session synthesizes: read both diffs + rationale, run tester's suite on each, pick/merge, state reasoning.
3. `module-verifier` re-runs the suite on the synthesized branch (no Write/Edit).
4. Present both candidates' differences, synthesis reasoning, verifier output. Open the one PR into `dev`.
5. After merge: delete candidate/tests/synthesis branches (remote + local), remove worktrees.
