#!/usr/bin/env bash
# shellcheck disable=SC2016  # backticks in fixture text are literal
# Usage: run_adopt.sh <runs_dir>
# Builds a messy existing project, runs `/project-playbook:adopt --auto` on a copy, then checks nothing was clobbered.
# Manual (needs the `claude` CLI, costs tokens); the checker itself is unit-tested in CI.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; PLUGIN="$(dirname "$HERE")"
RUNS="$(mkdir -p "$1" && cd "$1" && pwd)"; OUT="$RUNS/adopt"; rm -rf "$OUT"; mkdir -p "$OUT/before"; cd "$OUT/before" || exit 1
git init -q -b main; git config user.email t@example.com; git config user.name t
mkdir -p src tests .github/workflows
printf '# Notes app\n\nSmall CLI for notes.\n\n## Usage\nrun `python -m notes add "text"`\n' > README.md
printf 'import sys\n\ndef add(t):\n    print("added", t)\n\nif __name__ == "__main__":\n    add(" ".join(sys.argv[1:]))\n' > src/notes.py
printf 'from src.notes import add\n\ndef test_add(capsys):\n    add("x")\n    assert "added" in capsys.readouterr().out\n' > tests/test_notes.py
printf '__pycache__/\n.venv/\n' > .gitignore
printf '# CLAUDE.md\n\nUse 4-space indents. Run `pytest` before committing.\n' > CLAUDE.md
printf '# TODO\n- [x] add command\n- [ ] list command\n- [ ] delete command\n' > TODO.md
printf 'name: ci\non: [push]\njobs:\n  t:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@v4\n      - run: pip install pytest && pytest\n' > .github/workflows/ci.yml
git add -A; git commit -q -m "add command"; echo "# changelog" > CHANGELOG.md; git add -A; git commit -q -m "changelog"
cp -R "$OUT/before" "$OUT/after"; cd "$OUT/after" || exit 1
claude --plugin-dir "$PLUGIN" -p "/project-playbook:adopt --auto" \
  --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "Bash(git:*)" "Bash(mkdir:*)" "Bash(chmod:*)" "Bash(cp:*)" "Bash(ls:*)" "Bash(cat:*)" "Bash(python3:*)" "Bash(test:*)" "Bash(find:*)" \
  > "$OUT/transcript.txt" 2>&1
python3 "$HERE/adopt_check.py" "$OUT/before" "$OUT/after" | tee "$OUT/check.json"
python3 "$PLUGIN/skills/project-setup/scripts/verify.py" "$OUT/after" --expect ci | python3 -c "import json,sys; d=json.load(sys.stdin); print('verify score', d['score'], 'failing', [i['name'] for i in d['items'] if not i['pass']])"
