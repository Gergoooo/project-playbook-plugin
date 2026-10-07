# Right-size the process

Pick a tier at step 0 and record it in `docs/DECISIONS.md`. Re-tier if the project grows. Skipping a step is fine; skipping it silently is not — note what was skipped and why.

| Tier | Fits | Keep | Skip |
|---|---|---|---|
| **Solo script / weekend** | one file or small tool, nobody depends on it | README, `CLAUDE.md` with Resume protocol, `.gitignore`, gitleaks hook | roadmap modules, `dev` branch, subagent pipeline, review pass beyond secrets |
| **Small app** | one deployable, solo, real users or real data | all of the above + ARCHITECTURE, ROADMAP with `Current status`, DECISIONS, TESTING, review pass (§4), `dev`/`main`, one PR per module | dual builders (use one builder + tester + verifier), per-feature docs unless complex |
| **Full pipeline** | multi-component or multi-repo, long-lived, spend/legal/security exposure | everything: docs, review pass, module groups, dual builders + tester + verifier, hooks, memory | nothing |

Rules of thumb:
- Dual builders cost ~2–3× tokens per module. Use them when the module has real design choices (data model, auth, sync), not for mechanical work.
- The review pass (§4) is cheap and catches expensive mistakes — keep it for anything that touches users, money or third-party data, whatever the tier.
- The Resume protocol and "user merges every PR" gate apply at every tier.
- Ask the user which tier they want when it isn't obvious; recommend one with the reason.

## Platform assumptions (adapt if different)
- **GitHub + `gh` CLI** (steps in `repo-setup.md`, `branching.md`, `failsafes.md`, `subagents.md`). On GitLab/other, substitute the equivalent CLI for PRs/branch protection; the workflow itself is unchanged.
- **git worktrees** for parallel builders (`subagents.md`).
- **Claude Code** features: subagents, `.claude/agents/`, plan mode, memory.
