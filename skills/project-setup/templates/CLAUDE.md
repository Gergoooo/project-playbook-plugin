# Working in this repo

**Before doing anything else, read [`docs/ROADMAP.md`](docs/ROADMAP.md)** — the `## Current status` block is the live source of truth. Then, as relevant: [`docs/WORKFLOW.md`](docs/WORKFLOW.md) (read before starting or resuming any module), [`docs/DECISIONS.md`](docs/DECISIONS.md), [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

## Resume protocol

> **On session start (and after `/init`):** read `docs/ROADMAP.md` → `## Current status`. Report in ≤5 lines: last merged module, in-flight work (verify with `gh pr list`, `git branch -r`, `git status`), and **Next up**. Then wait — never auto-start the next module; the user's PR merge is the gate.

## Standing rules
- **User decides at every module/phase boundary.** Never auto-proceed past one without explicit sign-off.
- **Ask before adding anything to `.gitignore`** that isn't obviously build-noise — secret-related patterns need explicit confirmation.
- Do not push directly to `main` or `dev`. Modules → PR into `dev`; `dev` → `main` only via a deliberate promotion PR.

## Stack
<stack and one-line rationale; details in docs/DECISIONS.md>

## Local setup (one-time per clone)
```
git config core.hooksPath .githooks
```
Activates `pre-push` (blocks direct pushes to `main`/`dev`; override only if intentional: `ALLOW_MAIN_PUSH=1 git push`) and `pre-commit` (`gitleaks protect --staged`; `brew install gitleaks`; false positives go in `.gitleaks.toml`, not `--no-verify`).
