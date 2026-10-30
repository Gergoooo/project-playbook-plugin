#!/usr/bin/env python3
"""Self-verification for a scaffolded project. Usage: verify.py <root> --expect a,b,c [--ci  (skip local-only checks: hooksPath, branches)] (add tier:solo for solo tier)
Root may be one repo or a folder holding several repos. Prints JSON {items:[{name,weight,pass,detail}], score}."""
import json, os, re, subprocess, sys

root = os.path.abspath(sys.argv[1])
expect = set()
if "--expect" in sys.argv:
    expect = set(x for x in sys.argv[sys.argv.index("--expect") + 1].split(",") if x)

def repos():
    out = []
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in ("node_modules", ".venv", "venv", "__pycache__", "worktrees", ".worktrees")]
        if ".git" in dn or ".git" in fn:
            out.append(dp)
            dn[:] = [d for d in dn if d != ".git"]
    return out or [root]

R = repos()
def read(p):
    try: return open(p, errors="ignore").read()
    except Exception: return ""
def find_doc(name):
    for r in R:
        for base in ("docs", "."):
            p = os.path.join(r, base, name)
            if os.path.isfile(p): return p
    return None
def git(r, *a):
    try: return subprocess.run(["git", "-C", r, *a], capture_output=True, text=True).stdout
    except Exception: return ""

items = []
def add(name, weight, ok, detail=""):
    items.append({"name": name, "weight": weight, "pass": bool(ok), "detail": detail})

def per_repo(name, weight, fn):
    res = [fn(r) for r in R]
    ok = sum(1 for x in res if x)
    add(name, weight, ok == len(res), f"{ok}/{len(res)} repos")

# --- docs (any repo) ---
for doc, w in [("README.md", 1), ("ARCHITECTURE.md", 1), ("ROADMAP.md", 2), ("DECISIONS.md", 2), ("TESTING.md", 1), ("WORKFLOW.md", 2)]:
    add(f"doc:{doc}", w, find_doc(doc) is not None)
for doc, key in [("API.md", "api"), ("DATA_MODEL.md", "data_model"), ("ATTRIBUTIONS.md", "attributions"), ("DEPLOYMENT.md", "deployment")]:
    if key in expect: add(f"doc:{doc}", 1, find_doc(doc) is not None)
    else: add(f"no-filler:{doc}", 0.5, True if find_doc(doc) is None else len(read(find_doc(doc)).strip()) > 400, "present docs must be real")
if "features" in expect:
    fd = None
    for r in R:
        if os.path.isdir(os.path.join(r, "docs/features")): fd = os.path.join(r, "docs/features")
    n = len([f for f in os.listdir(fd) if f.endswith(".md") and f not in ("README.md",) and not f.startswith("_")]) if fd else 0
    add("features:index+docs", 2, bool(fd) and os.path.isfile(os.path.join(fd, "README.md")) and n >= 1, f"{n} feature docs")

# --- roadmap quality ---
rp = find_doc("ROADMAP.md"); rd = read(rp) if rp else ""
add("roadmap:current-status", 2, re.search(r"##\s*Current status", rd) and all(k in rd for k in ("Last merged", "In flight", "Next up")))
add("roadmap:phase-1-docs", 0.5, re.search(r"Phase -1", rd) is not None)
phases = re.findall(r"(?m)^##\s*Phase\s+\d+", rd)
groups = re.findall(r"(?m)^###\s*Group\s+[A-Z]", rd)
mods = re.findall(r"(?m)^\|\s*\d+\.\d+\b[^|]*\|[^|]+\|[^|]+\|[^|]+\|", rd)
add("roadmap:phases>=2", 1, len(phases) >= 2, f"{len(phases)} phases")
add("roadmap:groups", 1, len(groups) >= 2, f"{len(groups)} groups")
add("roadmap:modules>=8", 1, len(mods) >= 8 or ("tier:solo" in expect), f"{len(mods)} modules")
add("roadmap:table-columns", 1, all(c in rd for c in ("Scope", "Depends on", "Test plan")))
add("roadmap:phase0", 1, re.search(r"Phase 0", rd) is not None)
add("roadmap:no-placeholders", 1, not re.search(r"<(module|feature|name|skeleton|dirs|stack)[^>]*>", rd), "template markers left")

# --- decisions quality ---
dp = find_doc("DECISIONS.md"); dd = read(dp) if dp else ""
entries = re.findall(r"(?m)^##\s+(?!Open|Assumptions).+", dd)
add("decisions:entries>=3", 1, len(entries) >= 3, f"{len(entries)} entries")
add("decisions:review-pass", 1, re.search(r"(?mi)^##\s*Review pass", dd) is not None)
add("decisions:context-decision-why", 1, all(k in dd for k in ("Context", "Decision", "Why")))
add("decisions:open-questions", 1, re.search(r"(?mi)^##\s*Open questions", dd) is not None)

# --- per-repo hygiene ---
per_repo("claude-md:resume-protocol", 2, lambda r: "On session start" in read(f"{r}/CLAUDE.md") and "ROADMAP" in read(f"{r}/CLAUDE.md"))
per_repo("claude-md:no-placeholders", 1, lambda r: os.path.isfile(f"{r}/CLAUDE.md") and not re.search(r"<(stack|stack and one-line|project)[^>]*>", read(f"{r}/CLAUDE.md")))
per_repo("gitignore", 1, lambda r: os.path.isfile(f"{r}/.gitignore"))
per_repo("hooks:pre-push-exec", 1, lambda r: os.access(f"{r}/.githooks/pre-push", os.X_OK))
per_repo("hooks:pre-commit-exec", 1, lambda r: os.access(f"{r}/.githooks/pre-commit", os.X_OK))
per_repo("hooks:gitleaks.toml", 0.5, lambda r: os.path.isfile(f"{r}/.gitleaks.toml"))
if "--ci" not in sys.argv: per_repo("hooks:core.hooksPath", 1, lambda r: git(r, "config", "core.hooksPath").strip() == ".githooks")
if "--ci" not in sys.argv: per_repo("git:main+dev", 1, lambda r: {"main", "dev"} <= set(b.strip("* ").strip() for b in git(r, "branch", "--list").split("\n") if b.strip()))
per_repo("git:has-commit", 0.5, lambda r: bool(git(r, "log", "-1", "--format=%H").strip()))
if "ci" in expect: per_repo("ci:workflow", 1, lambda r: os.path.isdir(f"{r}/.github/workflows") and bool(os.listdir(f"{r}/.github/workflows")))
if "tier:solo" not in expect:
    allagents = {}
    for r in R:
        for sub in (".claude/agents", "agents-pending"):  # headless runs can't write .claude/; fallback dir accepted
            d = f"{r}/{sub}"
            if os.path.isdir(d): allagents.setdefault(r, []).extend(os.path.join(sub, x) for x in os.listdir(d))
    names = [a for v in allagents.values() for a in v]
    add("agents:builder", 1, any("builder" in n for n in names))
    add("agents:tester", 1, any("tester" in n for n in names))
    add("agents:verifier", 1, any("verifier" in n for n in names))
    add("agents:no-placeholders", 1, names and all(not re.search(r"<stack>", read(f"{r}/{n}")) for r, v in allagents.items() for n in v))

# --- CI/CD workflow quality ---
def wf_files(r):
    d = f"{r}/.github/workflows"
    return [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith((".yml", ".yaml"))] if os.path.isdir(d) else []
if "ci" in expect:
    allwf = [f for r in R for f in wf_files(r)]
    texts = {f: re.sub(r"(?m)^\s*#.*$", "", read(f)) for f in allwf}
    add("cicd:no-stub-steps", 2, bool(texts) and not any(re.search(r"TODO replace|replace with the real|<setup-|<install deps>", t) for t in texts.values()), "CI must run real commands")
    ci_files = [t for f, t in texts.items() if re.search(r"(?m)^name:\s*(iOS )?CI\b", t)]
    add("cicd:ci-covers-epic-branches", 1, bool(ci_files) and all(("epic/**" in t or "phase/**" in t or "'**'" in t) for t in ci_files) if "epics" in expect else True, "ci.yml must trigger on epic/** PRs when epics are used")
    add("cicd:least-privilege", 1, all(re.search(r"(?m)^permissions:", t) for t in texts.values()) if texts else False, "every workflow declares permissions")
    add("cicd:timeouts", 0.5, all("timeout-minutes" in t for t in texts.values()) if texts else False)
    pub = [t for t in texts.values() if re.search(r"(?m)^name:\s*(Publish|Deploy|Release)", t)]
    add("cicd:publish-only-from-main", 1, all(("branches: [main]" in t or "branches:\n      - main" in t or "tags:" in t or "workflow_dispatch" in t) and "pull_request" not in t.split("jobs:")[0] for t in pub) if pub else True)
    add("cicd:publish-needs-tests", 1, all(re.search(r"needs:\s*\[?test|workflow_run|uses:\s*\./\.github/workflows/ci", t) or "workflow_dispatch" in t for t in pub) if pub else True)
    try:
        r = subprocess.run(["actionlint"] + allwf, capture_output=True, text=True, timeout=60)
        add("cicd:actionlint", 1, r.returncode == 0, r.stdout[:200]) if allwf else None
    except FileNotFoundError:
        pass  # actionlint not installed: skipped, not failed

tot = sum(i["weight"] for i in items); got = sum(i["weight"] for i in items if i["pass"])
print(json.dumps({"root": root, "repos": R, "score": round(got / tot, 4), "items": items}, indent=1))
