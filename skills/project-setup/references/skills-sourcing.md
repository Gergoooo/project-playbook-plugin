## 10. Sourcing skills/plugins, if using them

- Prefer content you can read directly (a single `SKILL.md` or similar) over installing an opaque plugin bundle.
- **Don't trust star counts** — the ecosystem has bot-farmed/bought stars (check: does watcher count and repo age make the star count plausible? A repo with 100k+ stars and single-digit-percent watchers, or explosive growth in a few months, is suspect). Verify via `gh api orgs/<name>` (`is_verified`) and by reading the actual content instead.
- Watch for "toolkit export" bundles (vs a single skill's plain-file download) — these can carry live API tokens (check any `.mcp.json` or config file for `Authorization`/`token` fields) and hooks that phone home on session start or tool use. Extract just the actual content you want; don't install the surrounding plugin machinery unless you've read exactly what it does.
- Any bundled script (not just markdown) gets read before trusting it — check for `subprocess`/`eval`/`exec`/network calls that go beyond what the skill claims to do.
