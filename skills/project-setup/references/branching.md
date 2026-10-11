## 6. Branching model

Two long-lived branches, plus short-lived module branches:

- **`dev`** — integration branch. Every module PR merges here; this is where the app actually gets built up.
- **`main`** — deployed/stable. Only advances via a separate, deliberate `dev`→`main` **promotion PR**, decided independently of any individual module merge. Any deploy/publish CI (image builds, store uploads) should trigger on `main` only — merging a module into `dev` shouldn't itself trigger a production deploy. This decoupling is the entire reason for the two-branch split; don't collapse it back to one branch even for a small project.
- **Module branches** — one branch per candidate per module (see step 7's `module/<id>-a` / `-b` / `-tests` naming), forked from `dev`, deleted once synthesis picks a direction and merges.

Neither `dev` nor `main` should accept direct pushes — enforced via the local `pre-push` hook in step 8, since GitHub's native branch protection is usually plan-gated on a private repo.

## Optional: epic branches (Full tier, opt-in)

Use when a feature is not usable until several stories land (e.g. a reading library = import + reader + lookup popup). Skip for Solo/Small tiers — there, one PR per module into `dev` is simpler and integrates earlier.

Vocabulary: an **epic** is one feature/phase worth of work; a **story** is one numbered roadmap row inside it. (Without epics, a story is just called a module.)

```
main  ←(promotion PR)—  dev  ←(epic PR)—  epic/<name>  ←(story PRs)—  module/<id>-*
```

- **`epic/<name>`** — forked from `dev` when the epic starts. Every story PR merges here, each approved by the user. Never receives direct pushes (extend the `pre-push` hook to block `refs/heads/epic/*`).
- **Story branches** — `module/<id>-a`, `-b`, `-tests`, forked from the **epic branch**, not `dev`. Same dual-builder pipeline.
- **Epic PR** — when all stories are merged and the epic's test plan is green, open one PR `epic/<name>` → `dev`. The user's approval is the gate; deleting the epic branch afterwards.
- **Keep epics short-lived**: merge `dev` into the epic branch whenever `dev` moves (at least before each story PR) to avoid a big conflict at the end. Prefer epics of ≤8 stories.
- Per-story review is of the small diff; per-epic review is of the whole feature against its feature doc — don't re-review every line twice.
- `ROADMAP.md`: mark epic phases with `Epic branch: epic/<name>`, and `Current status` must name the active epic and which stories are merged into it.
- Alternative without extra branches: merge stories straight into `dev` behind a feature flag.
