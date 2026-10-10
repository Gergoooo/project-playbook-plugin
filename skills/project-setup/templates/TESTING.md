# Testing Strategy

| Type | Scope | Tooling | When it runs |
|---|---|---|---|
| Unit | <pure logic> | <runner> | Every PR |
| Integration | <components together / real dependencies> | <runner> | Every PR |
| Contract | <API/schema agreement between components> | <tool> | Every PR |
| E2E / UI | <critical user flows> | <tool> | Every PR or nightly |
| Data validation | <imports/ETL/migrations, counts + spot checks> | <runner> | On each run |
| Scheduled / smoke | <paid or flaky external deps; kept out of PR CI> | <runner> | Nightly |
| Manual QA | <what can't be automated> | checklist below | Before each release |

_Delete rows that don't apply; add rows the project needs. Name the real test commands once Phase 0 lands — the verifier agent runs them._

## CI gates
- PRs blocked on: <tests, lint, type-check>.
- Nightly/periodic jobs report, they don't block merges.

## Manual QA checklist
- [ ] <flow>
