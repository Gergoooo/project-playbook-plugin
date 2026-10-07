## 4. Full review pass — do this before writing code, not after

Go through the plan looking specifically for:

- **Auth exposure**: does anything become reachable from the public internet (tunnel, deployed API) that was scoped as "no auth needed" under a "local only" assumption? If so, that assumption just broke — add an auth gate.
- **Spend caps**: any paid API in the loop (LLM, third-party service) — set usage/budget caps on the provider's dashboard, independent of app-level auth, as a second line of defense against bugs or abuse.
- **Data licensing**: third-party datasets/content — check the actual license (CC BY-SA requires attribution, some require share-alike, some forbid commercial use). Add to `ATTRIBUTIONS.md` and plan an in-app credits screen if it ships publicly.
- **ToS/legal risk for scraped content**: if the plan involves pulling content from a site that isn't explicitly public-domain/licensed for reuse, don't scrape/store it — consider a WebView/embed approach that reads live instead of copying, or drop the source.
- **Backup/sync for user data**: anything stored only on one device or machine — is losing it on reinstall acceptable? If not, plan a sync mechanism (e.g. the platform's cloud sync, or a server-side store) early, not as an afterthought.
- **Secrets-to-host deployment**: if there's a deploy target (VM, server), how do secrets actually get there without being committed? Decide this explicitly (CI secrets + deploy-time env write, typically), don't leave it implicit.
- **Distribution scope**: is this actually going to a public app store / production users right now, or is it personal-use/dev for now? Compliance work (store review guidelines, privacy policy hosting, paid developer accounts) should match the actual current goal — don't front-load work for a launch that isn't planned yet, but write down what would need to be revisited if that changes.
- **Account prerequisites**: list what third-party accounts each later module will need (cloud hosting, DNS/tunnel provider, paid APIs), but don't set any of them up now — note them inline on the relevant `ROADMAP.md` row and sort each out just-in-time when that module actually starts. A separate "accounts to create" checklist doc tends to go stale.
