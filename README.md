# project-playbook

Claude Code plugin: a docs-first project setup playbook.

- Skill `project-setup` — the playbook, split into on-demand reference files, plus templates (CLAUDE.md with Resume protocol, ROADMAP/WORKFLOW/DECISIONS, git hooks, verifier agent).
- `/project-playbook:new-project [idea]` — scaffold a new project, stopping at every human gate.
- `/project-playbook:resume` — report last merged / in flight / next up.

## Install
```
/plugin marketplace add Gergoooo/project-playbook-plugin
/plugin install project-playbook@project-setup-playbook
```
Local dev: `claude --plugin-dir /path/to/project-playbook-plugin`.
