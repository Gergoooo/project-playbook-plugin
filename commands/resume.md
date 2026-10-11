---
description: Report where this project left off and what's next (Resume protocol)
---

Read `docs/ROADMAP.md` → `## Current status`. Cross-check against reality with `gh pr list`, `git branch -r`, and `git status`. If they disagree, say so and trust the git/GitHub state.

Also run the epic gate (`epic-gate.py . --epic <current>`) and include whether the current epic is complete and what's missing.

Report in ≤5 lines: last merged module, in-flight work (name the active epic branch and merged stories if the roadmap uses epics), **Next up**. Then wait for the user — never auto-start the next module.
