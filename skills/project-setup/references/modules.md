## 5. Break the roadmap into modules

- Each phase → small modules, each scoped to specific files/directories with no overlap against modules in the same batch — so they're safe to work in parallel (by subagents or otherwise).
- Group modules into dependency-ordered batches (Group A/B/C...); batches run in sequence, modules within a batch don't depend on each other and dispatch together.
- Every module needs: **Scope** (files/dirs it owns), **Depends on** (modules that must land first), **Group** (which batch), and a **Test plan** (what kind of test proves it's done).
- Every module PR also updates `ROADMAP.md`'s `## Current status` block (last merged, in-flight, next up) — part of the module's definition of done, so status never goes stale.
- Write this into `docs/WORKFLOW.md`: the module format, and the rule that **each module ships as one PR, and the human's PR approval is the decision gate** — nothing auto-proceeds to the next module or phase, and finishing a group's modules doesn't imply starting the next group either.

## Scope self-check (do before finishing the roadmap)
- No file or directory is owned by two modules in the same group. A shared file (router, config, workflow, schema) gets one owner module in an earlier group; later modules extend it only via that module's declared extension point.
- Every `Depends on` points to an earlier group (no forward or circular deps).
- Every feature from scoping has at least one module and a feature doc.
- Every module's Test plan names a concrete check, not "tests".
