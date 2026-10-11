## 7. Define subagents for module implementation

For any module big enough to be worth automating (most of them), don't hand-implement or single-shot it — dispatch a small pipeline of subagents per module and have the orchestrating conversation (you, talking to the user) synthesize and present the result. This produced noticeably more robust output in practice (see the worked example below) at the cost of more tokens/time per module — that tradeoff is worth stating explicitly to the user and letting them choose, rather than assuming.

**Roster** (adapt per stack — this shape worked for a two-repo client + server project; collapse to one builder pass for small work, see right-size.md):

| Agent | Role | Tools |
|---|---|---|
| `<stack>-module-builder` (dispatched twice per module, independently) | Implements one module candidate end-to-end within its declared scope | Read, Write, Edit, Bash, Grep, Glob |
| `<stack>-tester` | Writes the test suite for a module from its spec alone — **never reads either builder's implementation** | Read, Write, Edit, Bash, Grep, Glob |
| `module-verifier` (shared across stacks) | Independently re-runs a module's test suite against the synthesized implementation, reports pass/fail with real evidence | Read, Bash, Grep, Glob — **no Write/Edit**, so it can't "fix" what it's checking |

Define these as `.claude/agents/*.md` files (frontmatter: `name`/`description`/`tools`; each agent's body should point it at `CLAUDE.md` → the module's `ROADMAP.md` row → any feature doc → relevant architecture/decision docs → project skills, in that order) so the pattern is documented and repeatable, not just something you remember to do manually.

**Per-module pipeline:**

1. **Dispatch three subagents in parallel**, each in its own git worktree/branch:
   - Builder-A on `module/<id>-a`, Builder-B on `module/<id>-b` — same brief, dispatched independently, told not to coordinate or look at each other's work. Each ends its report with a few sentences of *design rationale* (what it chose between and why), not just "done."
   - Tester on `module/<id>-tests` — works from the module's scope/spec only, never reads either builder's branch. Its tests won't run meaningfully yet (no implementation merged) — that's expected.
   - None of the three open a PR. They push their branch and report back.
2. **Synthesis** (done by the orchestrating conversation, not delegated): read both builders' diffs and rationale, apply the tester's suite to each candidate, and pick a winner or merge the stronger parts of both into a fresh branch. State the reasoning — this is a real editorial call, not a mechanical vote.
3. **Dispatch `module-verifier`** against the synthesized branch for an independent test re-run with real command output, not a paraphrase.
4. **Present to the user**: both candidates' key differences, the synthesis reasoning, the verifier's results. Open the one PR into `dev` (or into the epic branch when the phase uses one — see branching.md) at this point — the user's review/merge of *that* PR is the actual decision gate.

Document this whole flow in `docs/WORKFLOW.md` so a future session (after `/clear`/`/compact`, or a fresh window) can pick it back up without re-deriving it.

## 8. Environment gotchas when actually dispatching subagents

Things that didn't show up until subagents were dispatched for real — check for these rather than assuming a clean run:

- **Custom agent types may not be selectable.** Defining `.claude/agents/<name>.md` doesn't guarantee the `Agent` tool's type list will include it by name in every environment — it may only ever offer built-ins (`general-purpose`, etc.). Workaround: dispatch `general-purpose` and inline the custom agent's role/rules directly into the prompt ("Act as this project's `<agent-name>` agent, defined in `.claude/agents/<name>.md` — read it for full rules. You are Builder-A..."). Check which situation you're in before assuming named dispatch will work.
- **`isolation: "worktree"` ties to the orchestrating session's *current primary working directory*, not the target repo.** In a multi-repo project, dispatching a subagent for repo B while the session's primary directory is still pointed at repo A silently pins that subagent to a worktree of the *wrong* repo — it'll correctly refuse to touch repo B rather than corrupt anything, but the dispatch is wasted. Fix: run a Bash command with `cwd` in the target repo (e.g. `cd "<repo>" && git status`) immediately before dispatching, which flips the primary directory — confirm it actually flipped before dispatching, especially in a batch mixing modules from more than one repo. (Batches should generally be per-repo for this reason — don't mix repos in one parallel dispatch.) Fallback if that's ever unreliable: manually `git worktree add -b module/<id>-a .worktrees/<id>-a dev` yourself, then dispatch subagents *without* `isolation: "worktree"`, telling each to `cd` into its pre-made path.
- **Tooling the agent assumes exists may not be installed in its sandbox** (Docker, a project generator or SDK, a specific interpreter version). Instruct agents explicitly: if a required tool is missing, say so plainly and use the closest available proxy to still validate what you can (e.g. run the containerized app's exact install/serve commands directly, outside Docker, if Docker itself isn't available) — never claim a result you didn't actually get. Carry that caveat through to synthesis and the PR description rather than losing it; flag the module in `ROADMAP.md` (e.g. "merged but unverified against real Docker — confirm before relying on it") until someone actually runs the real check.
- **Verify claims yourself at synthesis time, don't just relay them.** A builder or tester reporting "tests passed" is a claim, not proof — re-run the test suite yourself (or via `module-verifier`) against the synthesized branch before presenting it to the user. This caught nothing dramatic in practice, but it's the actual point of having a separate verification step at all.
- **Clean up after merge, on both remote and local.** Losing candidate branches, the tester's standalone branch, and the synthesis branch all need deleting after the PR merges (`git push origin --delete <branch>`, then locally `git branch -D <branch>` — plus `git worktree remove --force` for any manually-created worktrees). Easy to let these pile up across several modules; do a `gh pr list --state all` + `git branch -r` sweep periodically to catch what got missed.

## Scaling agents to task size (slices)

Don't use the same agent set for every module. The orchestrator sizes each story when it is dispatched (or the roadmap row carries `Size: S/M/L`):

| Size | Signal | Agents |
|---|---|---|
| **S** | ≤3 files, one concern, mechanical | 1 builder + tester + verifier |
| **M** | one layer/dir, real design choices | 2 competing builders + tester + verifier (the standard pipeline) |
| **L** | >~8 files, or spans layers/dirs, or expected >~600 changed lines | split into **slices**: 2–5 builders in parallel, each owning a disjoint part of the module's scope |

**Slicing rules (L stories)**
1. The orchestrator writes the slicing plan *before* dispatching: slice id (`s1`…`sk`), the exact files/dirs each owns (no overlap), and a short **slice contract** — the interfaces, types, endpoints or file formats slices share — committed first on `module/<id>-int` so every slice builds against the same contract.
2. One builder per slice on `module/<id>-s<k>`, forked from the integration branch. In the Full tier a slice may still get two competing builders if it contains a real design decision (data model, auth, sync); otherwise one.
3. Tester: one per slice if slices have separate specs, otherwise one tester for the whole module writing contract-level tests from the spec only.
4. The orchestrator merges slices into `module/<id>-int` in dependency order, resolves seams, and runs the tester's suite; then `module-verifier` runs on the integrated branch. One PR from the integration branch — the user's approval is still the gate.
5. Cap parallelism at ~6 agents at once; queue the rest. Report agent count and slices in the PR so the cost is visible.
6. If a slice needs a file outside its scope, it stops and reports; the orchestrator re-slices — never let slices edit each other's files.
