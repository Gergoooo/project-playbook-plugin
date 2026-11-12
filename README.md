# project-playbook

Claude Code plugin: a docs-first project setup playbook. It takes a project from first idea to "modules landing through a dual-builder PR pipeline", and makes any fresh session resume where the last one stopped.

## What it gives you
- **Skill `project-setup`**: the playbook, split into on-demand reference files, plus templates (docs, `CLAUDE.md` with the Resume protocol, git hooks, per-stack CI/CD, PR/issue templates, agents) and two scripts (`epic-gate.py`, `verify.py`).
- **Agent `module-verifier`**: independent test re-runner with no Write/Edit access (also available as a template to copy into a project).
- **SessionStart hook**: in any repo that has `docs/ROADMAP.md`, injects the *Current status* block, git state and epic-gate result at session start. Silent in other repos.

## Commands
| Command | Does |
|---|---|
| `/project-playbook:new-project <idea> [--auto]` | Scaffold a new project: scope, tier, docs, repo + hooks, roadmap modules, CI, agents. Stops at every human gate. `--auto` is local-only (no `gh`, no push). |
| `/project-playbook:adopt [--auto]` | Retrofit the playbook onto an existing repo without overwriting anything (works on a branch `docs/adopt-playbook`). |
| `/project-playbook:resume` | Report last merged / in flight / next up, cross-checked against git and GitHub. |
| `/project-playbook:start-module <id>` | Run the per-module pipeline (gate check, sizing S/M/L, builders, tester, synthesis, verifier). Stops at the PR; never merges. |
| `/project-playbook:next-epic [N]` | Run the epic completion gate and list exactly what is missing before the next epic may start. |
| `/project-playbook:retro [N]` | Record an epic retrospective in `docs/DECISIONS.md` and propose process changes. |

## Install
```
/plugin marketplace add Gergoooo/project-playbook-plugin
/plugin install project-playbook@project-setup-playbook
```
From a local clone: `/plugin marketplace add /path/to/project-playbook-plugin`, or for development `claude --plugin-dir /path/to/project-playbook-plugin`. Restart the session after installing.

## Requirements
Claude Code, `git`, Python 3. GitHub + `gh` for the PR flow (the playbook itself is platform-neutral; GitLab/Bitbucket equivalents are described in `references/right-size.md`). Optional: `gitleaks`, `actionlint`, `shellcheck`.

## Tests
```
python3 -m unittest discover -s tests -v      # scripts, hooks, templates, manifests (runs in CI)
tests/run.sh tests/briefs/00-japanese-app.md /tmp/runs   # LLM scaffold run + judge (manual, needs `claude`)
tests/run_adopt.sh /tmp/runs                  # LLM `adopt` no-clobber run (manual, needs `claude`)
```

## License
MIT — see `LICENSE`. Changes: `CHANGELOG.md`.
