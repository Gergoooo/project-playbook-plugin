## 9. Failsafes for continuity and safety

- **`CLAUDE.md` with a Resume protocol** in each repo (and the parent folder, if sibling repos share one). Point any future session at `docs/ROADMAP.md` first (live status), then `docs/WORKFLOW.md`/`docs/DECISIONS.md`, and include this block verbatim near the top:

  > **On session start (and after `/init`):** read `docs/ROADMAP.md` → `## Current status`. Report in ≤5 lines: last merged module, in-flight work (verify with `gh pr list`, `git branch -r`, `git status`), and **Next up**. Then wait — never auto-start the next module; the user's PR merge is the gate.

  Using `/init` so a new session knows where you left off:
  - `/init` alone can't know status — it infers from code, and early on there's barely any. Status comes from `ROADMAP.md`'s `Current status`; the Resume protocol is what makes every session read and report it.
  - Run `/init` inside each repo (not a non-git parent folder). Run it once after the docs exist, and again after the first code module merges so it picks up real build/test/lint commands.
  - If `CLAUDE.md` already exists, `/init` should improve it, not replace it: keep the Resume protocol block and doc pointers verbatim, add only commands/architecture not already in docs, reject any status it guesses.
  - Don't make a project command named `init` (collides with the built-in). For an explicit re-check mid-session, add `.claude/commands/resume.md` containing the Resume protocol prompt and invoke `/resume`.
  - `CLAUDE.md` changes go through the normal docs PR into `dev`, not a direct push.
- **Branch protection**: check if it's actually available (`gh api repos/<owner>/<repo>/branches/main/protection` — private repos on a free GitHub plan often return "Upgrade to Pro"). If unavailable, use a local `pre-push` git hook (tracked in `.githooks/`, activated via `git config core.hooksPath .githooks`) that blocks direct pushes to `main` **and `dev`** (see step 6), forcing the branch+PR flow for real.
- **Secret scanning**: same plan-gating issue often applies (GitHub Advanced Security). Add a local `pre-commit` hook running `gitleaks protect --staged` (`brew install gitleaks`) as a backstop, with a `.gitleaks.toml` allowlist for confirmed false positives (document *why* each one is safe, don't blanket-suppress). Note: gitleaks 8.30+ wants the singular `[allowlist]` table, not `[[allowlist]]` array syntax.
- Test the hooks actually work (commit a trivial change, attempt a direct push to `main`/`dev`, confirm it's blocked) before trusting them.
