#!/usr/bin/env bash
# Usage: run.sh <brief.md> <runs_dir> [--ref <ref_root>]
# Generates a scaffold from the brief in <runs_dir>/<id>/gen with the plugin (auto mode), then scores it.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; PLUGIN="$(dirname "$HERE")"
BRIEF="$(cd "$(dirname "$1")" && pwd)/$(basename "$1")"; RUNS="$(mkdir -p "$2" && cd "$2" && pwd)"; shift 2
ID=$(basename "$BRIEF" .md)
OUT="$RUNS/$ID"; rm -rf "$OUT"; mkdir -p "$OUT/gen"
IDEA=$(awk 'BEGIN{n=0} /^---$/{n++; next} n>=2' "$BRIEF")
EXPECT=$(sed -n 's/^expect: \[\(.*\)\]/\1/p' "$BRIEF" | tr -d ' ')
TIER=$(sed -n 's/^tier: *//p' "$BRIEF")
[ "$TIER" = "solo" ] && EXPECT="$EXPECT,tier:solo"
cd "$OUT/gen"
claude --plugin-dir "$PLUGIN" -p "/project-playbook:new-project $IDEA --auto" \
  --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "Bash(git:*)" "Bash(mkdir:*)" "Bash(chmod:*)" "Bash(cp:*)" "Bash(ls:*)" "Bash(cat:*)" "Bash(sed:*)" "Bash(touch:*)" "Bash(mv:*)" "Bash(rm:*)" "Bash(test:*)" "Bash(printf:*)" "Bash(echo:*)" "Bash(find:*)" "Bash(wc:*)" "Bash(head:*)" "Bash(tail:*)" \
  > "$OUT/transcript.txt" 2>&1
python3 "$HERE/check.py" "$OUT/gen" --expect "$EXPECT" > "$OUT/check.json"
python3 "$HERE/judge.py" "$OUT/gen" "$BRIEF" "$@" > "$OUT/judge.json"
python3 - "$OUT" <<'PY'
import json,sys
o=sys.argv[1]; c=json.load(open(o+"/check.json")); j=json.load(open(o+"/judge.json"))
js=j.get("score"); s=c["score"]
tot=round(0.5*s+0.5*js,4) if js is not None else None
json.dump({"structural":s,"judge":js,"total":tot},open(o+"/score.json","w"))
print(o.split("/")[-1], "structural",s,"judge",js,"total",tot)
PY
