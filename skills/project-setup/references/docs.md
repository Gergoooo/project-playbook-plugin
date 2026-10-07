## 1. Docs before code

Write these before any application code exists, in the actual repo(s):

- `README.md` — what it is, stack, how to run it (fill in "TBD" for parts that don't exist yet)
- `docs/ARCHITECTURE.md` — components, how they talk to each other, a diagram if it helps
- `docs/API.md` — endpoint contract, if there's a client/server split (write it before implementing)
- `docs/DATA_MODEL.md` — schema sketch
- `docs/ROADMAP.md` — phased delivery plan (see step 5 for the module breakdown). **Must open with a `## Current status` block**: last merged module (+ PR link), in-flight module/branch/PR, and **Next up** (module, group, blockers/open decisions). This block is what lets a fresh session resume — see step 9.
- `docs/DECISIONS.md` — lightweight ADR log: one entry per non-obvious choice, **Context / Decision / Why**, newest first, plus an **Open questions** section for things not yet decided
- `docs/TESTING.md` — test types, tooling, when each runs in CI
- `docs/features/` — one file per feature, linked from a `README.md` index and from `ROADMAP.md`'s phases
- `docs/ATTRIBUTIONS.md` — if using any third-party data/content under a license requiring credit (CC BY, CC BY-SA, etc.) — check this explicitly, don't assume "free" means "no attribution needed"

Why: keeps the plan concrete, reviewable, and durable independent of implementation — and gives something concrete to build against instead of discovering the shape of things ad hoc.
