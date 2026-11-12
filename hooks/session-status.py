#!/usr/bin/env python3
"""SessionStart hook: in a playbook project (docs/ROADMAP.md present) print the Resume-protocol facts
so the session starts informed. Silent (exit 0, no output) everywhere else. Never fails the session."""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(HERE, "..", "skills", "project-setup", "scripts", "epic-gate.py")

def cwd():
    try:
        if sys.stdin.isatty(): return os.getcwd()
        d = json.load(sys.stdin).get("cwd")
        if d and os.path.isdir(d): return d
    except Exception: pass
    return os.getcwd()

def sh(root, *a):
    try:
        r = subprocess.run(a, cwd=root, capture_output=True, text=True, timeout=10)
        return (r.stdout or "").strip() if r.returncode == 0 else ""
    except Exception: return ""

def status_block(text):
    m = re.search(r"(?ms)^##\s*Current status\s*\n(.*?)(?=^##\s|\Z)", text)
    if not m: return ""
    return "\n".join(l for l in m.group(1).strip().splitlines() if l.strip() and not l.startswith(">"))

def main():
    root = cwd()
    rp = next((p for p in (f"{root}/docs/ROADMAP.md", f"{root}/ROADMAP.md") if os.path.isfile(p)), None)
    if not rp: return
    try: block = status_block(open(rp, errors="ignore").read())
    except Exception: return
    if not block: return
    out = ["[project-playbook] Resume protocol (auto-injected at session start)",
           f"From {os.path.relpath(rp, root)} -> Current status:", block]
    branch = sh(root, "git", "rev-parse", "--abbrev-ref", "HEAD")
    if branch:
        dirty = sh(root, "git", "status", "--porcelain")
        out.append(f"Git: branch `{branch}`, {len(dirty.splitlines())} uncommitted change(s).")
    gate = sh(root, sys.executable, GATE, root, "--no-gh")
    if gate: out += ["Epic gate (local check, PRs not verified):"] + gate.splitlines()[:20]
    out.append("Report this to the user in <=5 lines (last merged, in flight, epic gate state, Next up), cross-check with "
               "`gh pr list` / `git branch -r`, then wait. Never auto-start the next module.")
    print("\n".join(out))

try: main()
except Exception: pass
sys.exit(0)
