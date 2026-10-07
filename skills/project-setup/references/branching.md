## 6. Branching model

Two long-lived branches, plus short-lived module branches:

- **`dev`** — integration branch. Every module PR merges here; this is where the app actually gets built up.
- **`main`** — deployed/stable. Only advances via a separate, deliberate `dev`→`main` **promotion PR**, decided independently of any individual module merge. Any deploy/publish CI (image builds, store uploads) should trigger on `main` only — merging a module into `dev` shouldn't itself trigger a production deploy. This decoupling is the entire reason for the two-branch split; don't collapse it back to one branch even for a small project.
- **Module branches** — one branch per candidate per module (see step 7's `module/<id>-a` / `-b` / `-tests` naming), forked from `dev`, deleted once synthesis picks a direction and merges.

Neither `dev` nor `main` should accept direct pushes — enforced via the local `pre-push` hook in step 8, since GitHub's native branch protection is usually plan-gated on a private repo.
