#!/usr/bin/env python3
"""No-clobber checker for `/project-playbook:adopt`.
Usage: adopt_check.py <before_dir> <after_dir>   (before = pristine copy of the project, after = project after adopt --auto)
Prints JSON {pass, problems}. Rules:
  - every file that existed before still exists
  - text/config files (.md .yml .yaml .toml .txt, dotfiles, .githooks/, .husky/): every original non-blank line is still present, in order (merge, not overwrite)
  - everything else (application code, data, binaries): byte-identical
  - after is on branch docs/adopt-playbook and its remotes are unchanged
"""
import json, os, subprocess, sys

SKIP = {".git", "node_modules", ".venv", "venv", "__pycache__", "worktrees", ".worktrees"}
MERGE_EXT = {".md", ".yml", ".yaml", ".toml", ".txt"}

def files(root):
    for dp, dn, fn in os.walk(root):
        dn[:] = [d for d in dn if d not in SKIP]
        for f in fn:
            p = os.path.join(dp, f)
            yield os.path.relpath(p, root)

def mergeable(rel):
    base = os.path.basename(rel)
    return (os.path.splitext(base)[1] in MERGE_EXT or base.startswith(".")
            or rel.startswith((".githooks/", ".husky/")))

def lines(b):
    return [l.strip() for l in b.decode("utf-8", "replace").splitlines() if l.strip()]

def is_subsequence(needle, hay):
    it = iter(hay)
    return all(any(n == h for h in it) for n in needle)

def git(d, *a):
    r = subprocess.run(["git", "-C", d, *a], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None

def check(before, after):
    problems = []
    for rel in sorted(files(before)):
        pa, pb = os.path.join(after, rel), os.path.join(before, rel)
        if not os.path.isfile(pa):
            problems.append(f"deleted: {rel}"); continue
        ob, oa = open(pb, "rb").read(), open(pa, "rb").read()
        if ob == oa: continue
        if mergeable(rel):
            if not is_subsequence(lines(ob), lines(oa)):
                problems.append(f"overwritten (original lines lost/reordered): {rel}")
        else:
            problems.append(f"modified non-doc file: {rel}")
    if git(after, "rev-parse", "--git-dir") is not None:
        br = git(after, "branch", "--show-current")
        if br != "docs/adopt-playbook": problems.append(f"expected branch docs/adopt-playbook, on {br!r}")
        if git(before, "rev-parse", "--git-dir") is not None and git(before, "remote", "-v") != git(after, "remote", "-v"):
            problems.append("git remotes changed")
    return {"pass": not problems, "problems": problems}

if __name__ == "__main__":
    res = check(os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]))
    print(json.dumps(res, indent=1)); sys.exit(0 if res["pass"] else 1)
