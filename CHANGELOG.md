# Changelog

## 0.2.0
- README documents every command; added `LICENSE` (MIT) and full plugin metadata.
- Commands call scripts via `${CLAUDE_PLUGIN_ROOT}` instead of a guessed `<skill dir>`; they work in projects that never vendored `scripts/`.
- `SessionStart` hook (`hooks/session-status.py`) injects ROADMAP Current status + git state + epic gate automatically in playbook projects. Silent elsewhere.
- Ships `module-verifier` as a plugin agent (`agents/module-verifier.md`); the template stays canonical and a test keeps them identical.
- New scaffold templates: `LICENSE` guidance, `SECURITY.md`, `CODEOWNERS`, `CONTRIBUTING.md`, issue templates, `THREAT_MODEL.md` (conditional). `verify.py` checks them when listed in `--expect`.
- Scoping/review pass now include a license decision and a threat-model prompt.
- Plugin CI pins actions to commit SHAs and actionlint to a release.
- New tests: SessionStart hook, README/command consistency, agent sync, `adopt` no-clobber checker (+ manual `tests/run_adopt.sh`).

## 0.1.0
- Initial release: `new-project`, `resume`, `adopt`, `start-module`, `next-epic`, `retro`; templates, epic gate, verify, per-stack CI.
