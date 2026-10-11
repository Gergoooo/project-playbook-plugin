#!/usr/bin/env python3
"""Epic completion gate. Usage: epic-gate.py <repo root> [--start N] [--epic N] [--no-gh]
  --start N : may work on phase/epic N begin? Checks every earlier non-optional phase (>=0) is complete.
  --epic N  : report only on epic N.
  (neither) : report every phase, and which one is current.
Exit 0 = ready / gate open, 1 = something missing (list printed)."""
import json, os, re, subprocess, sys

root = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else "."
args = sys.argv[2:]
def opt(name):
    return int(args[args.index(name) + 1]) if name in args else None
start, only = opt("--start"), opt("--epic")
use_gh = "--no-gh" not in args

def read(p):
    try: return open(p, errors="ignore").read()
    except Exception: return ""
def sh(*a):
    try:
        r = subprocess.run(a, cwd=root, capture_output=True, text=True, timeout=30)
        return r.stdout if r.returncode == 0 else None
    except Exception: return None

rp = next((p for p in (f"{root}/docs/ROADMAP.md", f"{root}/ROADMAP.md") if os.path.isfile(p)), None)
if not rp: print("No ROADMAP.md found."); sys.exit(1)
rm = read(rp)
dec = read(os.path.join(os.path.dirname(rp), "DECISIONS.md"))

# split into phases
parts = re.split(r"(?m)^(?=##\s+Phase\s+-?\d+)", rm)
phases = []
for part in parts:
    m = re.match(r"##\s+Phase\s+(-?\d+)\s*[—–-]?\s*(.*)", part)
    if not m: continue
    num, title = int(m.group(1)), m.group(2).strip()
    rows = re.findall(r"(?m)^\|\s*(\d+\.\d+)\s+([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|", part)
    phases.append({"num": num, "title": title, "text": part, "rows": rows,
                   "optional": bool(re.search(r"(?i)optional|stretch", title)),
                   "epic": (re.search(r"Epic branch:\s*`?(epic/[\w./-]+)", part) or [None, None])[1],
                   "features": re.findall(r"features/([\w.-]+\.md)", part)})

branches = sh("git", "branch", "-a", "--format=%(refname:short)") or ""
branches = [b.strip() for b in branches.splitlines()]
prs = None
if use_gh:
    out = sh("gh", "pr", "list", "--state", "open", "--json", "number,title,headRefName")
    prs = json.loads(out) if out else None

def check(ph):
    miss = []
    ids = [r[0] for r in ph["rows"]]
    if not ids and ph["num"] >= 0: miss.append("no stories/modules listed for this epic in ROADMAP")
    for sid, name, scope, dep, test in ph["rows"]:
        label = f"{sid} {name.replace('✅','').strip()}"
        if "✅" not in name and "[x]" not in name.lower():
            miss.append(f"story not done: {label}")
        elif re.search(r"(?i)unverified|TBD|not yet|follow-?up", name + test):
            miss.append(f"story marked done but has a caveat to resolve: {label} ({(re.search(r'(?i)unverified|TBD|not yet|follow-?up', name + test)).group(0)})")
    for line in re.findall(r"(?m)^- \[ \] .+", ph["text"]):
        miss.append(f"unchecked item: {line[6:].strip()[:100]}")
    for f in ph["features"]:
        fp = os.path.join(os.path.dirname(rp), "features", f)
        t = read(fp)
        if t and not re.search(r"(?i)\*{0,2}Status\*{0,2}:\s*\*{0,2}\s*(done|complete|shipped)", t):
            miss.append(f"feature doc not marked Done: features/{f}")
    for b in branches:
        for sid in ids:
            if re.match(rf"(origin/)?module/{re.escape(sid)}-", b): miss.append(f"leftover branch not cleaned up: {b}")
    if ph["epic"]:
        local = ph["epic"] in branches or f"origin/{ph['epic']}" in branches
        if local:
            nm = sh("git", "branch", "-a", "--no-merged", "dev", "--format=%(refname:short)")
            if nm is not None and any(x.strip().endswith(ph["epic"]) for x in nm.splitlines()):
                miss.append(f"epic branch {ph['epic']} not merged into dev (epic PR still open or not created)")
    if prs:
        for pr in prs:
            hb = pr["headRefName"]
            if any(hb.startswith(f"module/{sid}-") for sid in ids) or (ph["epic"] and hb == ph["epic"]):
                miss.append(f"open PR #{pr['number']}: {pr['title']}")
    oq = re.search(r"(?ms)^##\s*Open questions(.*?)(?=^##\s|\Z)", dec)
    if oq:
        for sid in ids:
            for line in oq.group(1).splitlines():
                if re.search(rf"\b{re.escape(sid)}\b", line): miss.append(f"unresolved open question mentions {sid}: {line.strip()[:100]}")
    return miss

real = [p for p in phases if p["num"] >= 0]
results = {p["num"]: check(p) for p in real}
def show(p):
    m = results[p["num"]]
    print(f"Epic {p['num']} — {p['title']}: " + ("COMPLETE" if not m else f"NOT COMPLETE ({len(m)} open)"))
    for x in m: print(f"   - {x}")
    if p["optional"] and m: print("   (optional epic — does not block the next one)")

rc = 0
if only is not None:
    for p in real:
        if p["num"] == only: show(p); rc = 1 if results[p["num"]] else 0
elif start is not None:
    blockers = [p for p in real if p["num"] < start and not p["optional"] and results[p["num"]]]
    if blockers:
        print(f"WARNING: cannot start Epic {start} — earlier epic(s) are not complete:\n")
        for p in blockers: show(p)
        print("\nFinish (or explicitly descope, recording it in DECISIONS) the items above first. Only the user can override this gate.")
        rc = 1
    else:
        print(f"Gate open: all earlier epics are complete. Epic {start} may start (after the user says go).")
else:
    cur = next((p for p in real if not p["optional"] and results[p["num"]]), None)
    for p in real: show(p)
    print("\nCurrent epic:", f"Epic {cur['num']} — {cur['title']}" if cur else "none (all required epics complete)")
if prs is None and use_gh: print("\n(note: could not verify open PRs via gh — check `gh pr list` manually)")
sys.exit(rc)
