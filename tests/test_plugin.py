import glob, json, os, shutil, subprocess, sys, tempfile, unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SK = os.path.join(ROOT, "skills", "project-setup")
GATE = os.path.join(SK, "scripts", "epic-gate.py")
VERIFY = os.path.join(SK, "scripts", "verify.py")
HOOK = os.path.join(SK, "templates", "githooks", "pre-push")

ROADMAP = """## Phase 0 — Foundations
| Module | Scope | Depends on | Test plan |
|---|---|---|---|
| 0.1 shell ✅ | app/ | — | builds |
## Phase 1 — Search
_Feature doc: [search.md](features/search.md)_
| Module | Scope | Depends on | Test plan |
|---|---|---|---|
| 1.1 index | src/ | 0.1 | t |
## Phase 2 — More
| Module | Scope | Depends on | Test plan |
|---|---|---|---|
| 2.1 x | y/ | 1.1 | t |
"""

def run(*a, **k):
    return subprocess.run(a, capture_output=True, text=True, **k)

def edit(path, old, new):
    t = open(path).read()
    open(path, "w").write(t.replace(old, new))

class EpicGate(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp(); os.makedirs(f"{self.d}/docs/features")
        open(f"{self.d}/docs/ROADMAP.md", "w").write(ROADMAP)
        open(f"{self.d}/docs/DECISIONS.md", "w").write("# D\n")
        open(f"{self.d}/docs/features/search.md", "w").write("**Status**: Done\n")
    def tearDown(self): shutil.rmtree(self.d)
    def test_blocks_when_story_missing(self):
        r = run(sys.executable, GATE, self.d, "--start", "2", "--no-gh")
        self.assertEqual(r.returncode, 1); self.assertIn("story not done: 1.1", r.stdout)
    def test_opens_when_all_done(self):
        edit(f"{self.d}/docs/ROADMAP.md", "1.1 index |", "1.1 index ✅ |")
        r = run(sys.executable, GATE, self.d, "--start", "2", "--no-gh")
        self.assertEqual(r.returncode, 0, r.stdout)
    def test_caveat_blocks(self):
        edit(f"{self.d}/docs/ROADMAP.md", "1.1 index |", "1.1 index ✅ unverified |")
        self.assertEqual(run(sys.executable, GATE, self.d, "--start", "2", "--no-gh").returncode, 1)
    def test_feature_doc_must_be_done(self):
        open(f"{self.d}/docs/features/search.md", "w").write("**Status**: Not started\n")
        edit(f"{self.d}/docs/ROADMAP.md", "1.1 index |", "1.1 index ✅ |")
        self.assertIn("feature doc not marked Done", run(sys.executable, GATE, self.d, "--epic", "1", "--no-gh").stdout)
    def test_optional_epic_does_not_block(self):
        edit(f"{self.d}/docs/ROADMAP.md", "Phase 1 — Search", "Phase 1 — Search (optional)")
        self.assertEqual(run(sys.executable, GATE, self.d, "--start", "2", "--no-gh").returncode, 0)

class PrePushHook(unittest.TestCase):
    def test_protected_branches(self):
        t = tempfile.mkdtemp()
        try:
            run("git", "init", "-q", "--bare", f"{t}/r.git")
            run("git", "init", "-q", f"{t}/w")
            for k, v in (("user.email", "a@b.c"), ("user.name", "t"), ("core.hooksPath", os.path.dirname(HOOK))):
                run("git", "-C", f"{t}/w", "config", k, v)
            run("git", "-C", f"{t}/w", "commit", "-q", "--allow-empty", "-m", "x")
            run("git", "-C", f"{t}/w", "remote", "add", "origin", f"{t}/r.git")
            for b, blocked in (("main", 1), ("dev", 1), ("epic/foo", 1), ("feature/x", 0)):
                r = run("git", "-C", f"{t}/w", "push", "-q", "origin", f"HEAD:refs/heads/{b}")
                self.assertEqual(r.returncode != 0, bool(blocked), f"{b}: {r.stderr}")
        finally: shutil.rmtree(t)

class Templates(unittest.TestCase):
    def test_manifests(self):
        for f in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json"):
            json.load(open(os.path.join(ROOT, f)))
    def test_commands_have_frontmatter(self):
        for f in glob.glob(f"{ROOT}/commands/*.md"):
            self.assertTrue(open(f).read().startswith("---\ndescription:"), f)
    def test_hooks_shellcheck(self):
        if not shutil.which("shellcheck"): self.skipTest("shellcheck missing")
        for h in glob.glob(f"{SK}/templates/githooks/*"):
            self.assertEqual(run("shellcheck", h).returncode, 0, h)
    def test_workflows_actionlint(self):
        if not shutil.which("actionlint"): self.skipTest("actionlint missing")
        # lint inside a project-shaped dir so publish-docker's reusable `./.github/workflows/ci.yml` resolves
        d = tempfile.mkdtemp()
        try:
            wf = f"{d}/.github/workflows"; os.makedirs(wf)
            for f in glob.glob(f"{SK}/templates/github-workflows/*.yml") + glob.glob(f"{SK}/templates/github/*.yml"):
                if not f.endswith("dependabot.yml"): shutil.copy(f, wf)
            shutil.copy(f"{SK}/templates/github-workflows/ci-node.yml", f"{wf}/ci.yml")
            run("git", "init", "-q", d)
            r = run("actionlint", cwd=d); self.assertEqual(r.returncode, 0, r.stdout)
        finally: shutil.rmtree(d)
    def test_ci_templates_trigger_on_epic_branches(self):
        for f in glob.glob(f"{SK}/templates/github-workflows/ci-*.yml"):
            t = open(f).read(); self.assertIn("epic/**", t, f); self.assertIn("workflow_call", t, f); self.assertIn("permissions:", t, f)

class Verify(unittest.TestCase):
    def test_stub_ci_fails_and_real_passes(self):
        d = tempfile.mkdtemp()
        try:
            run("git", "init", "-q", "-b", "main", d); os.makedirs(f"{d}/.github/workflows")
            shutil.copy(f"{SK}/templates/github-workflows/ci-generic.yml", f"{d}/.github/workflows/ci.yml")
            out = json.loads(run(sys.executable, VERIFY, d, "--ci", "--expect", "ci").stdout)
            self.assertFalse(next(i for i in out["items"] if i["name"] == "cicd:no-stub-steps")["pass"])
            shutil.copy(f"{SK}/templates/github-workflows/ci-node.yml", f"{d}/.github/workflows/ci.yml")
            out = json.loads(run(sys.executable, VERIFY, d, "--ci", "--expect", "ci,epics").stdout)
            ok = {i["name"]: i["pass"] for i in out["items"]}
            for k in ("cicd:no-stub-steps", "cicd:ci-covers-epic-branches", "cicd:least-privilege", "cicd:timeouts"): self.assertTrue(ok[k], k)
        finally: shutil.rmtree(d)

HOOKS = os.path.join(ROOT, "hooks")
SESSION = os.path.join(HOOKS, "session-status.py")
sys.path.insert(0, os.path.dirname(__file__))
import adopt_check

def commands():
    return sorted(os.path.splitext(os.path.basename(f))[0] for f in glob.glob(f"{ROOT}/commands/*.md"))

class SessionHook(unittest.TestCase):
    def test_hooks_json_points_at_existing_script(self):
        h = json.load(open(os.path.join(HOOKS, "hooks.json")))
        cmd = h["hooks"]["SessionStart"][0]["hooks"][0]["command"]
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/hooks/session-status.py", cmd)
        self.assertTrue(os.path.isfile(SESSION))
    def test_silent_outside_playbook_project(self):
        d = tempfile.mkdtemp()
        try:
            r = subprocess.run([sys.executable, SESSION], input="", capture_output=True, text=True, cwd=d)
            self.assertEqual((r.returncode, r.stdout), (0, ""))
        finally: shutil.rmtree(d)
    def test_prints_status_and_gate(self):
        d = tempfile.mkdtemp()
        try:
            os.makedirs(f"{d}/docs")
            open(f"{d}/docs/ROADMAP.md", "w").write(ROADMAP.replace("## Phase 0", "## Current status\n- **Last merged:** 0.1\n- **Next up:** 1.1\n\n## Phase 0", 1))
            run("git", "init", "-q", d)
            r = subprocess.run([sys.executable, SESSION], input=json.dumps({"cwd": d}), capture_output=True, text=True)
            self.assertEqual(r.returncode, 0)
            for s in ("Last merged:** 0.1", "Next up:** 1.1", "Epic gate", "Never auto-start"): self.assertIn(s, r.stdout)
        finally: shutil.rmtree(d)
    def test_never_fails_on_garbage_input(self):
        r = subprocess.run([sys.executable, SESSION], input="not json", capture_output=True, text=True, cwd=tempfile.gettempdir())
        self.assertEqual(r.returncode, 0)

class Consistency(unittest.TestCase):
    def test_every_command_documented_in_readme_and_skill(self):
        readme, skill = open(f"{ROOT}/README.md").read(), open(f"{SK}/SKILL.md").read()
        for c in commands():
            self.assertIn(f"/project-playbook:{c}", readme, f"README missing {c}")
            self.assertIn(f"/project-playbook:{c}", skill, f"SKILL.md missing {c}")
    def test_docs_do_not_mention_unknown_commands(self):
        import re
        known = set(commands())
        for f in (f"{ROOT}/README.md", f"{SK}/SKILL.md", *glob.glob(f"{ROOT}/commands/*.md")):
            for c in re.findall(r"/project-playbook:([a-z-]+)", open(f).read()):
                self.assertIn(c, known, f"{f} mentions unknown command {c}")
    def test_commands_use_plugin_root_not_placeholders(self):
        import re
        for f in glob.glob(f"{ROOT}/commands/*.md"):
            t = open(f).read()
            self.assertNotIn("<skill dir>", t, f)
            self.assertNotRegex(t, r"python3 scripts/", f)
            for rel in re.findall(r"\$\{CLAUDE_PLUGIN_ROOT\}/([\w./-]+\.py)", t):
                self.assertTrue(os.path.isfile(os.path.join(ROOT, rel)), f"{f}: {rel} missing")
    def test_versions_and_metadata_agree(self):
        pj = json.load(open(f"{ROOT}/.claude-plugin/plugin.json")); mj = json.load(open(f"{ROOT}/.claude-plugin/marketplace.json"))
        self.assertEqual(pj["version"], mj["plugins"][0]["version"])
        self.assertEqual(pj["license"], "MIT"); self.assertTrue(os.path.isfile(f"{ROOT}/LICENSE"))
        self.assertIn(f"## {pj['version']}", open(f"{ROOT}/CHANGELOG.md").read())
    def test_skill_template_paths_exist(self):
        import re
        skill = open(f"{SK}/SKILL.md").read()
        for ref in re.findall(r"`(references/[\w.-]+\.md)`", skill):
            self.assertTrue(os.path.isfile(f"{SK}/{ref}"), ref)
        for tpl in ("SECURITY.md", "CONTRIBUTING.md", "THREAT_MODEL.md", "github/CODEOWNERS", "github/ISSUE_TEMPLATE/bug_report.md",
                    "github/ISSUE_TEMPLATE/feature_request.md", "github/ISSUE_TEMPLATE/config.yml"):
            self.assertTrue(os.path.isfile(f"{SK}/templates/{tpl}"), tpl)
    def test_shipped_verifier_agent_matches_template(self):
        a, b = open(f"{ROOT}/agents/module-verifier.md").read(), open(f"{SK}/templates/agents/module-verifier.md").read()
        self.assertEqual(a, b, "agents/module-verifier.md drifted from templates/agents/module-verifier.md")
        self.assertTrue(a.startswith("---\nname: module-verifier\n"))
        self.assertNotRegex(a.split("---")[1], r"Write|Edit")

class VerifyNewKeys(unittest.TestCase):
    def check(self, d, expect):
        out = json.loads(run(sys.executable, VERIFY, d, "--ci", "--expect", expect).stdout)
        return {i["name"]: i["pass"] for i in out["items"]}
    def test_license_community_threat(self):
        d = tempfile.mkdtemp()
        try:
            run("git", "init", "-q", "-b", "main", d); os.makedirs(f"{d}/docs")
            r = self.check(d, "license,community,threat_model")
            self.assertFalse(r["license:file"]); self.assertFalse(r["community:files"]); self.assertFalse(r["doc:THREAT_MODEL.md"])
            open(f"{d}/LICENSE", "w").write("MIT License\n" + "x" * 300)
            for f in ("SECURITY.md", "CONTRIBUTING.md"): open(f"{d}/{f}", "w").write("real text")
            os.makedirs(f"{d}/.github/ISSUE_TEMPLATE"); open(f"{d}/.github/CODEOWNERS", "w").write("* @someone\n")
            shutil.copy(f"{SK}/templates/THREAT_MODEL.md", f"{d}/docs/THREAT_MODEL.md")
            r = self.check(d, "license,community,threat_model")
            self.assertTrue(r["license:file"]); self.assertTrue(r["community:files"])
            self.assertFalse(r["doc:THREAT_MODEL.md"], "unfilled template must fail")
            open(f"{d}/.github/CODEOWNERS", "w").write("* @<github-username>\n")
            self.assertFalse(self.check(d, "community")["community:files"], "placeholder owner must fail")
        finally: shutil.rmtree(d)

class AdoptNoClobber(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.mkdtemp(); self.b, self.a = f"{self.t}/b", f"{self.t}/a"
        os.makedirs(f"{self.b}/src")
        open(f"{self.b}/README.md", "w").write("# App\n\nusage line\n"); open(f"{self.b}/src/app.py", "w").write("print(1)\n")
        open(f"{self.b}/.gitignore", "w").write("a/\nb/\n")
        run("git", "init", "-q", "-b", "main", self.b)
        shutil.copytree(self.b, self.a); run("git", "-C", self.a, "checkout", "-q", "-b", "docs/adopt-playbook")
    def tearDown(self): shutil.rmtree(self.t)
    def test_additive_changes_pass(self):
        open(f"{self.a}/README.md", "w").write("# App\n\nnew intro\n\nusage line\n\n## Docs\n")
        open(f"{self.a}/.gitignore", "a").write(".env\n")
        os.makedirs(f"{self.a}/docs"); open(f"{self.a}/docs/ROADMAP.md", "w").write("# R\n")
        r = adopt_check.check(self.b, self.a); self.assertTrue(r["pass"], r)
    def test_detects_overwrite_delete_code_edit_wrong_branch(self):
        open(f"{self.a}/README.md", "w").write("# Totally new\n")
        os.remove(f"{self.a}/.gitignore"); open(f"{self.a}/src/app.py", "w").write("print(2)\n")
        run("git", "-C", self.a, "checkout", "-q", "-b", "other")
        p = " | ".join(adopt_check.check(self.b, self.a)["problems"])
        for s in ("overwritten", "README.md", "deleted: .gitignore", "modified non-doc file: src/app.py", "expected branch"): self.assertIn(s, p)
    def test_detects_changed_remote(self):
        run("git", "-C", self.a, "remote", "add", "origin", "https://example.com/x.git")
        self.assertIn("git remotes changed", " ".join(adopt_check.check(self.b, self.a)["problems"]))

if __name__ == "__main__":
    unittest.main()
