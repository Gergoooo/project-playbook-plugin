# Roadmap

Living checklist, split into parallel-safe modules — see [WORKFLOW.md](WORKFLOW.md). Check items off as they land.

## Current status
- **Last merged:** <module id + PR link, or "none yet">
- **In flight:** <module / branch / PR, or "none"> (if epics are used: active epic branch + which stories are merged into it)
- **Next up:** <module, Group, blockers / open decisions>

> Update this block in every module PR.

## Phase -1 — Docs first
- [ ] README.md
- [ ] docs/ARCHITECTURE.md · API.md · DATA_MODEL.md (where applicable)
- [ ] docs/ROADMAP.md · DECISIONS.md · TESTING.md · WORKFLOW.md
- [ ] docs/features/ — one doc per feature, linked from the phase it belongs to
- [ ] Repo(s) created (private), hooks active, `.gitignore` secret patterns confirmed with user

## Phase 0 — Foundations
_Feature doc: n/a_

### Group A (independent, start immediately)
| Module | Scope | Depends on | Test plan |
|---|---|---|---|
| 0.1 <skeleton / app shell> | <dirs> | — | <builds + one trivial test> |
| 0.2 <CI> | `.github/workflows/ci.yml` | 0.1 | CI green on a trivial PR |

### Group B (depends on Group A)
| Module | Scope | Depends on | Test plan |
|---|---|---|---|

## Phase 1 — <first user-visible capability>
<!-- Optional (Full tier): Epic branch: epic/<name> -->
_Feature doc: [<feature>.md](features/<feature>.md)_

### Group A
| Module | Scope | Depends on | Test plan |
|---|---|---|---|

<!-- Add phases until every feature from scoping has modules. Note account prerequisites inline on the row that needs them. -->
