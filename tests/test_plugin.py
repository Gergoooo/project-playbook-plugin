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

if __name__ == "__main__":
    unittest.main()
