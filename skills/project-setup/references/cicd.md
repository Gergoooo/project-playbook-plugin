# CI/CD

Goal: every PR is checked by real commands; nothing reaches `main` untested; publishing and deploying are separate, gated steps. Applies to any stack — pick the template, fill in the real commands from `docs/TESTING.md`.

## Pick templates (`templates/github-workflows/`)
| Need | Template |
|---|---|
| CI for the stack | `ci-node` · `ci-python` · `ci-go` · `ci-rust` · `ci-jvm` · `ci-swift` · `ci-terraform` · `ci-generic` (copy as `.github/workflows/ci.yml`) |
| Build + push a container | `publish-docker.yml` (calls ci.yml first; main only) |
| Roll out to a host | `deploy-ssh.yml` (manual, smoke test, rollback) |
| Tagged releases | `release.yml` |
| Dependency updates | `github/dependabot.yml` (set the real ecosystem) |
| Playbook enforcement | `github/playbook-checks.yml` + `scripts/playbook-expect.txt` (the `--expect` list used when the scaffold was generated) |

## Rules every workflow follows
- CI triggers on PRs into `dev`, `main`, **and `epic/**`/`phase/**`** (story PRs go there), plus `workflow_call` so publish can reuse it, and `workflow_dispatch`.
- `permissions:` declared per workflow (read-only by default; widen per job), `timeout-minutes` on every job, `concurrency` to cancel superseded runs, dependency caching on.
- Lint + type-check + tests run in CI; if the project has no linter yet, add one in Phase 0 rather than leaving the gate empty. Never leave a placeholder step — `verify.py` fails scaffolds that do.
- Publish/deploy trigger on `main` only (or manual), never on PRs or `dev`, and depend on green tests (`needs: test` / reusable CI). Deploy keeps secrets in GitHub encrypted secrets or an environment, writes the host `.env` at deploy time, runs a smoke test, and rolls back on failure.
- Pin third-party actions to a commit SHA before the repo goes public; Dependabot keeps them updated. Prefer OIDC to cloud providers over static keys.
- Lint every workflow with `actionlint` before committing (`verify.py` runs it when installed).

## Limits to state in DECISIONS
- Without branch protection (private repo on a free plan) these checks can't block merges — the local hooks and the user's merge gate are the real enforcement. Record that, and revisit if the plan changes.
- `gitleaks-action` needs a license for organization accounts; personal accounts are free.
- Apple-platform builds need macOS runners (minutes cost more).
