---
description: Check the epic completion gate — may the next epic start? Lists exactly what is still missing
argument-hint: "[epic number to start]"
---

Run the epic gate for this repo (use the project's own copy under `scripts/` if the scaffold vendored it, otherwise the plugin's `skills/project-setup/scripts/epic-gate.py`):

`python3 <skill dir>/scripts/epic-gate.py . --start <N>` where N = $ARGUMENTS, or the epic after the current one if no argument. Run `gh pr list` as well if the script says it could not verify PRs.

- **Gate open (exit 0):** say so in one line, then wait for the user to say go. Never start the next epic on your own.
- **Gate closed (exit 1):** print a clear WARNING, then spell out every missing item from the script grouped by epic (stories not done, caveats on "done" stories, unchecked items, feature docs not marked Done, leftover branches, open PRs, epic PR not merged, unresolved open questions). Offer the shortest path to close each. Do not start any story of the later epic.
- Only the user can override the gate. If they do, record the override and the items skipped in `docs/DECISIONS.md` before proceeding.
