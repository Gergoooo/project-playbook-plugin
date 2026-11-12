# Security policy

## Reporting a vulnerability
Do **not** open a public issue. Report privately via GitHub: **Security → Report a vulnerability** on this repo<, or email <security contact>>.

Include: what you found, steps to reproduce, affected version/commit, and impact. Expect an acknowledgement within <N> days.

## Supported versions
<only the latest release / `main` is supported | table of supported versions>

## Scope
<what counts: the app, the API, the deploy config. What does not: third-party services, social engineering>

## Handling secrets
Never commit credentials. The repo runs `gitleaks` in a pre-commit hook and in CI. If a secret leaks, rotate it first, then remove it from history.
