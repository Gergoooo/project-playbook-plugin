# License decision

Ask at scoping; record the answer (or "none — private/proprietary, reason") in `docs/DECISIONS.md`. Without a license file, others have no right to use the code even if the repo is public.

| Situation | Default suggestion |
|---|---|
| Private, personal or client work, never shared | no license file; note "all rights reserved" in README |
| Open source, want max adoption | MIT (or Apache-2.0 if patent grant matters) |
| Open source, want improvements shared back | GPL-3.0 (apps) / AGPL-3.0 (network services) / MPL-2.0 (libraries, file-level copyleft) |
| Bundles third-party data/assets/models | license must be compatible; list credit-required items in `ATTRIBUTIONS.md` |

Get the exact text from GitHub rather than writing it: `gh api licenses/mit --jq .body > LICENSE` (replace the year and holder), or `gh repo create --license mit`. Never pick a license for the user without asking; recommend one with the tradeoff.

Companion files (copy from `templates/` when the project is public or has collaborators): `SECURITY.md`, `CONTRIBUTING.md`, `github/CODEOWNERS`, `github/ISSUE_TEMPLATE/`. A private solo project can skip them (note the skip). Add `THREAT_MODEL.md` when the project is reachable from the network, handles user data, money or credentials, or runs untrusted input.
