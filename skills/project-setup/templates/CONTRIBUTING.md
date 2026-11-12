# Contributing

Read [`docs/WORKFLOW.md`](docs/WORKFLOW.md) and [`docs/ROADMAP.md`](docs/ROADMAP.md) first: work is organized into modules, each landing as one PR.

## Setup
```
git config core.hooksPath .githooks     # blocks direct pushes to main/dev, scans staged files for secrets
<install + run commands, see README and docs/TESTING.md>
```

## Flow
1. Pick a module from the ROADMAP (or open an issue first for anything else).
2. Branch from `dev` (or the phase's `epic/<name>` branch): `module/<id>-<slug>`.
3. Keep the change inside the module's declared Scope. Update `docs/ROADMAP.md` (`Current status` and the story ✅) in the same PR.
4. Run the tests named in the module's Test plan; paste results in the PR.
5. Open a PR into `dev` using the template. A maintainer merges; nobody pushes to `main`, `dev` or `epic/*` directly.

## Conventions
<commit message style, formatting/lint command, test naming>
