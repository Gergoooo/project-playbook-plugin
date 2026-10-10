#!/usr/bin/env python3
"""LLM-judged content rubric. Usage: judge.py <root> <brief.md> [--ref <ref_root>] > result.json
Runs `claude -p` (no plugin loaded) with a bundle of the generated docs and a fixed rubric; prints JSON."""
import json, os, re, subprocess, sys

root = os.path.abspath(sys.argv[1]); brief = open(sys.argv[2]).read()
ref = os.path.abspath(sys.argv[sys.argv.index("--ref") + 1]) if "--ref" in sys.argv else None

def bundle(r, cap_file=14000, cap_total=150000):
    out, total = [], 0
    for dp, dn, fn in os.walk(r):
        dn[:] = sorted(d for d in dn if d not in (".git", "node_modules", ".venv", "skills", "__pycache__", ".pytest_cache", "app", "tests", "JapaneseApp", "JapaneseAppTests"))
        for f in sorted(fn):
            p = os.path.join(dp, f); rel = os.path.relpath(p, r)
            if not (f.endswith((".md", ".yml", ".toml")) or rel.startswith(".githooks")): continue
            t = open(p, errors="ignore").read()[:cap_file]
            if total + len(t) > cap_total: continue
            total += len(t); out.append(f"\n=== FILE: {rel} ===\n{t}")
    return "".join(out)

RUBRIC = """
Score each item 1 (clearly met) or 0 (not met / weak). Be strict; cite one short reason.
GENERIC (all projects):
G1 review-auth: DECISIONS addresses auth exposure (or n/a with reason)
G2 review-spend: spend caps / cost exposure of paid services (or n/a)
G3 review-licensing: third-party data/content licensing + attribution (or n/a)
G4 review-legal: ToS/legal risk of scraped or third-party content (or n/a)
G5 review-backup: backup/sync of user data / loss-on-reset (or n/a)
G6 review-secrets: how secrets reach the runtime without being committed (or n/a)
G7 review-distribution: distribution scope (store/public/personal) stated (or n/a)
G8 review-accounts: third-party account prerequisites noted inline on the roadmap rows that need them (or n/a)
G9 features-covered: every feature in the brief has at least one roadmap module and a feature doc
G10 modules-sound: each module has concrete Scope paths, Depends-on with no forward/circular deps, and a real Test plan; modules within a group have non-overlapping scope
G11 phase0: Phase 0 has skeleton + CI (+ hosting/secrets/auth when the project is hosted)
G12 specific: docs contain project-specific content (real names, components, endpoints/commands), not generic filler or leftover <placeholders>
G13 architecture: ARCHITECTURE has a component diagram/overview consistent with the chosen stack
G14 testing: TESTING names tests and tooling appropriate to the project's stack and risks
G15 decisions-quality: DECISIONS entries have real Context/Decision/Why with tradeoffs (not restating)
G16 claude-md: CLAUDE.md has the Resume protocol, standing rules, stack, and hook setup
G17 agents: builder/tester/verifier agents exist for the actual stack (or omitted for a solo-script tier) with no template leftovers
G18 right-sized: process weight (tier, number of docs/modules/agents) is appropriate for the project's size
G19 consistent: names, endpoints, tables and module ids agree across docs
G20 gates: user-merge gate, dev/main model, and ask-before-gitignore rule are carried into WORKFLOW/CLAUDE.md
"""
REFRUBRIC = """
REFERENCE COMPARISON (only when a reference project is provided; compare generated vs reference):
R1 same capability areas: generated roadmap covers the same feature areas as the reference roadmap
R2 module granularity: total module count within +-35% of the reference and similarly scoped
R3 phase0 parity: Phase 0 covers the same foundations as the reference (shells for each repo, CI for each, hosting, ingress, auth gate, secrets)
R4 decisions parity: DECISIONS covers the same risk topics as the reference (auth despite 'single-user', no store distribution, local-data backup, ToS-safe approach to scraped sites, LLM provider cost, licensing)
R5 doc-set parity: same kinds of docs as the reference (architecture, api, data model, testing, workflow, attributions, deployment, features/)
R6 agents parity: builder+tester per stack plus verifier, with equivalent rules
R7 overall: a maintainer would call the generated setup substantially equivalent in rigor and usefulness to the reference
"""
prompt = f"""You are a strict reviewer grading an auto-generated project scaffold.

PROJECT BRIEF (what the user asked for):
{brief}

GENERATED PROJECT FILES:
{bundle(root)}
"""
if ref:
    prompt += f"\nREFERENCE PROJECT FILES (hand-built gold standard):\n{bundle(ref, 9000, 120000)}\n"
prompt += f"""
RUBRIC:
{RUBRIC}{REFRUBRIC if ref else ''}
Output ONLY JSON: {{"items":[{{"id":"G1","pass":1,"reason":"..."}}, ...]}} covering every item listed."""
r = subprocess.run(["claude", "-p", prompt, "--output-format", "text"], capture_output=True, text=True, cwd="/private/tmp")
txt = r.stdout
m = re.search(r"\{.*\}", txt, re.S)
try:
    data = json.loads(m.group(0))
    items = data["items"]
    got = sum(int(i["pass"]) for i in items)
    print(json.dumps({"score": round(got / len(items), 4), "n": len(items), "items": items}, indent=1))
except Exception as e:
    print(json.dumps({"error": str(e), "raw": txt[:2000]}))
