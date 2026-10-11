---
description: After an epic, record what slowed it down and propose improvements to the playbook and this project's process
argument-hint: "[epic number]"
---

Run a short retrospective for epic $ARGUMENTS (default: the most recently completed epic).

1. **Gather facts** (read-only): `python3 scripts/epic-gate.py . --epic <N> --no-gh`, `git log` and merged PRs for the epic's stories (`gh pr list --state merged` if available), the ROADMAP rows, and any "unverified"/caveat notes. If PR descriptions record agent counts or slice use, tally them.
2. **Write a retro entry** at the top of `docs/DECISIONS.md` (Context / Decision / Why format, titled `Retro — Epic N`): what went well, what caused rework (failed verifier runs, scope overlaps, re-slicing, unclear specs), where agent cost was not worth it, surprises, and process changes to adopt. Keep it under 25 lines.
3. **Propose process changes** as concrete diffs to this project's `docs/WORKFLOW.md`, `docs/TESTING.md`, agent files or hooks — show them, apply only what the user approves.
4. **Playbook feedback:** list lessons that generalise beyond this project and offer to add them to the plugin's `references/` (or the user's `project-setup-playbook.md`). Do not edit the plugin without the user's go.
5. Never start the next epic; remind the user to run `/project-playbook:next-epic`.
