## 11. Save durable lessons as you go

"Where we left off" lives in `ROADMAP.md`'s `Current status` (see step 9), not in memory — memory is for the durable lessons below.

If working with Claude Code's memory system, prompt it (or let it prompt itself) to save:
- Non-obvious decisions and their *why* (so future sessions don't re-litigate them)
- Corrections to Claude's approach ("don't do X because Y")
- Confirmed-good approaches ("yes, that was the right call")
- Environment-specific pitfalls hit while dispatching subagents (see step 8) — these are easy to rediscover the hard way in a later session if they're not written down somewhere durable

This is what makes the next session actually pick up where the last one left off, instead of re-deriving context from scratch. And when a lesson is general enough to apply beyond the current project (like everything in step 8), fold it back into *this* playbook, not just the project's own memory — that's the point of keeping it outside any one repo.
