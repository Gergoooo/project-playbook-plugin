# Threat model

Short and honest beats thorough and stale. Revisit when a new entry point, data type or integration is added.

## Assets
<what is worth protecting: user data, credentials, money-moving actions, API quota, signing keys>

## Entry points
| Entry point | Who can reach it | Auth |
|---|---|---|
| <endpoint / CLI flag / webhook / file input> | <anonymous / user / admin / internal> | <how> |

## Threats and mitigations
| Threat | Entry point / asset | Mitigation | Status |
|---|---|---|---|
| <e.g. unauthenticated access once exposed publicly> | <...> | <auth gate in module X.Y> | <planned / done / accepted> |

## Out of scope / accepted risks
<each with the reason, and what would make it in scope>
