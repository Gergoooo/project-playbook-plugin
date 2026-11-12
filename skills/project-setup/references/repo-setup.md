## 2. Repo setup

- Decide monorepo vs polyrepo based on how independently the pieces deploy/release (e.g. a client and a backend that release separately → separate repos; one deployable → one repo).
- License file per `licensing.md` (fetch text with `gh api licenses/<spdx>`), if the decision is to have one.
- `git init`, set local `user.name`/`user.email` if not already configured globally — prefer a GitHub noreply email (`<id>+<username>@users.noreply.github.com`) over a personal email, even for private repos.
- Check `gh auth status`; if not authenticated, have the user run `gh auth login` themselves (browser-based OAuth) rather than pasting a token into chat. Follow with `gh auth setup-git` so pushes don't hit credential prompts.
- `gh repo create <name> --private --source=. --remote=origin --push` per repo.
- **Grant the `workflow` OAuth scope up front** if the plan involves GitHub Actions (it almost always will): `gh auth refresh -h github.com -s workflow`. Without it, `git push` silently rejects *any* change touching `.github/workflows/*.yml` — even a file that just lives in that directory without being a workflow itself — with `refusing to allow an OAuth App to create or update workflow ... without workflow scope`. Easy to not notice until a CI-authoring module is already dispatched and blocked.

## 3. `.gitignore` — ask before adding secrets

- Standard build-artifact hygiene (`.DS_Store`, language build/cache dirs like `node_modules`, `__pycache__`, `target/`, `build/`, etc.) — add without asking, it's not a judgment call.
- Anything that could hold a secret (`.env`, `*.pem`, `*.key`, credentials files, signing certs) — **propose the specific patterns and get explicit confirmation before adding them**, per-repo. Don't assume what "secret" means for an unfamiliar stack.
