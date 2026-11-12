# Adapt the scaffold to the project

The templates are a superset. Fit them to the project — don't emit docs that have nothing to say.

## 1. Classify the project (record in DECISIONS)
| Type | Typical shape | Docs to keep | Docs to drop/shrink |
|---|---|---|---|
| Client + server app (mobile/web + API) | 1–2 repos | all of them | — |
| Backend service / API | 1 repo | API, DATA_MODEL, DEPLOYMENT | UI-specific testing rows |
| Web app (full-stack single repo) | 1 repo | ARCHITECTURE, API, DATA_MODEL | — |
| Mobile/desktop app, local-only | 1 repo | ARCHITECTURE, DATA_MODEL (local store), TESTING | API, DEPLOYMENT |
| CLI tool / script | 1 repo | README, ARCHITECTURE (short), TESTING | API (unless a flag/config contract matters), DATA_MODEL, DEPLOYMENT |
| Library / SDK | 1 repo | API (public surface = the contract), TESTING, ATTRIBUTIONS if bundling | DEPLOYMENT, DATA_MODEL |
| Data / ML / analytics pipeline | 1 repo | ARCHITECTURE, DATA_MODEL (datasets), ATTRIBUTIONS (datasets/models), TESTING (data validation) | API |
| Game | 1 repo | ARCHITECTURE, features/ (per mechanic), ATTRIBUTIONS (assets) | API, DEPLOYMENT unless multiplayer |
| Embedded / hardware | 1 repo | ARCHITECTURE (hardware + firmware), TESTING (hardware-in-loop vs sim) | API, DEPLOYMENT |
| Infra / automation / IaC | 1 repo | ARCHITECTURE, DEPLOYMENT, TESTING (plan/dry-run) | API, DATA_MODEL, features/ |

Repo count: one deployable → one repo; client and server that release separately → two. Ask when unclear.

## 2. Conditional docs
- `API.md` — only with a service/library/CLI contract. `DATA_MODEL.md` — only if data persists. `DEPLOYMENT.md` — only if hosted. `ATTRIBUTIONS.md` — only if third-party data/content/assets need credit. `THREAT_MODEL.md` — only if networked / user data / money / untrusted input. `LICENSE` — per the license decision (`licensing.md`). `SECURITY.md`, `CONTRIBUTING.md`, `CODEOWNERS`, issue templates — public or multi-contributor repos only.
- `features/` — one file per feature; skip for tier "Solo script".

## 3. Stack-specific pieces (generate, don't copy)
- **Builder/tester agents**: instantiate `templates/agents/module-builder.md` and `module-tester.md` once per stack/repo, replacing `<stack>`, the skills list, and the runner's collect-only command. Always add `module-verifier` (copy the template into `.claude/agents/`; the plugin also ships it as `project-playbook:module-verifier` for sessions where the copy is missing).
- **CI/CD** (`references/cicd.md`): pick `ci-<stack>.yml`, replace every command with the real one; add publish/deploy/release/dependabot only when they apply.
- **`.gitignore`**: build-noise for the stack added freely; secret patterns proposed and confirmed.
- **TESTING.md**: keep only test types that apply; name real commands.
- **Phase 0 modules**: skeleton/shell, CI, and (if hosted) hosting + secrets + auth gate — before any feature phase.

## 4. Review pass (references/review-pass.md) — outcomes become DECISIONS entries
Every item must be addressed or explicitly marked n/a with a reason: auth exposure, spend caps, data licensing, ToS/legal for scraped content, backup/sync of user data, secrets-to-host, distribution scope, account prerequisites.

## 5. Right-size
Apply the tier from `references/right-size.md`. Smaller tier → fewer docs and single-builder pipeline, but the Resume protocol, user-merge gate, gitignore-ask rule and hooks always stay.
