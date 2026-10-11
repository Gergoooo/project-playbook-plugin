# Workflow: Modules, Parallel Subagents, Testing, Decisions

How each phase in [ROADMAP.md](ROADMAP.md) gets built.

## Principles
1. **Modules, not phases, are the unit of work.** Each module is small enough for one subagent, scoped to files/directories no concurrent module touches.
2. **Parallel groups.** Modules in a group are independent and dispatch together; groups run in sequence.
3. **Isolated work.** Every builder/tester works in its own git worktree/branch within its module's scope.
4. **Test before done.** A module is complete when its test plan (from [TESTING.md](TESTING.md)) is green, confirmed by an independent re-run (`module-verifier`), not the builder's own claim.
5. **User decides, every time.** After a module's tests pass it is presented, not merged or built on. Nothing proceeds automatically — at module level or phase level.
6. **Each module is one PR against `dev`, not `main`.** CI must pass before it's presentable. The user's PR approval and merge is the decision gate. Every module PR also updates `ROADMAP.md`'s `## Current status`.

7. **Epic completion gate.** The next epic (phase) only starts when every earlier required epic is complete: all stories merged and marked ✅ with no unresolved caveats, the epic's test plan green, its feature doc marked `**Status**: Done`, no leftover `module/*` branches or open PRs, the epic PR merged into `dev` (if an epic branch is used), and no open question in DECISIONS that mentions its stories. Check with `/project-playbook:next-epic` (or `scripts/epic-gate.py`). If anything is missing, warn and list it; don't start the next epic. Only the user can override, and the override is logged in DECISIONS. Mark optional/stretch phases `(optional)` in their heading so they don't block.

## Branching model
- **`dev`** — integration branch; every module PR merges here.
- **`main`** — stable/deployed; advances only via a deliberate `dev`→`main` promotion PR, decided independently of any module. Publish/deploy workflows trigger on `main` only.
- **Module branches** — `module/<id>-a`, `module/<id>-b`, `module/<id>-tests`, forked from `dev` (or from the epic branch), deleted after merge.
- **Epic branches (optional, Full tier)** — `epic/<name>`, forked from `dev` for a phase whose stories aren't usable until all land. Story PRs merge into the epic branch (user approves each); one final `epic/<name>` → `dev` PR (user approves) when the epic's test plan is green. Merge `dev` into the epic branch regularly. Phases using one are marked `Epic branch: epic/<name>` in ROADMAP. Terms: epic = one feature/phase; story = one roadmap row inside it.
- No direct pushes to `main`, `dev` or `epic/*` — enforced by the local `pre-push` hook (see `CLAUDE.md`) when GitHub branch protection is unavailable.

## Module entry format
**Scope** (files/dirs owned) · **Depends on** · **Group** · **Test plan** · **Status**.

## Agent roster
Custom subagents in `.claude/agents/`. None get `AskUserQuestion`/`Agent` — if a subagent needs a user decision it stops and reports to the orchestrating session, the single point of user contact.

| Agent | Role | Tools |
|---|---|---|
| `<stack>-module-builder` (dispatched twice) | Implements one module candidate within scope | Read, Write, Edit, Bash, Grep, Glob |
| `<stack>-tester` | Writes tests from the spec only, never reads a builder's code | Read, Write, Edit, Bash, Grep, Glob |
| `module-verifier` | Independently re-runs the suite on the synthesized branch; reports with evidence | Read, Bash, Grep, Glob (no Write/Edit) |

## Per-module pipeline
1. **Dispatch in parallel**, each in its own worktree: Builder-A (`module/<id>-a`), Builder-B (`module/<id>-b`) — same brief, independent, each ending with 2–5 sentences of design rationale — and Tester (`module/<id>-tests`, spec only). None open a PR.
2. **Synthesis** (orchestrating session, not delegated): read both diffs + rationale, run the tester's suite on each, pick or merge; state the reasoning.
3. **`module-verifier`** runs against the synthesized branch for an independent pass/fail with real output.
4. **Present to the user**: key differences, synthesis reasoning, verifier results. Open the one PR into `dev`. After merge, delete candidate/tests/synthesis branches (remote + local) and any worktrees.

_Right-size note: record the chosen tier in DECISIONS. Smaller tiers use one builder instead of two._

## Known issues
- **`isolation: "worktree"` pins to the session's primary working directory**, not the target repo. In a multi-repo project, run `cd "<repo>" && git status` right before dispatching and confirm the primary directory flipped; keep batches per-repo. Fallback: `git worktree add -b module/<id>-a .worktrees/<id>-a dev` manually and tell each subagent to `cd` there.
- **Custom agent types may not be selectable by name** — fall back to `general-purpose` with the agent file's role inlined in the prompt.
- **Missing tooling in the sandbox** (Docker, SDKs): say so, use the closest proxy, carry the caveat into the PR and flag the module in ROADMAP as unverified.
