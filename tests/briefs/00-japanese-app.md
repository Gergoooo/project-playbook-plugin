---
id: 00-japanese-app
tier: full
repos: 2
expect: [api, data_model, attributions, deployment, ci, features]
---
I want to build an iPhone app for learning Japanese, for myself (solo, personal use only, not planning an App Store release for now). Features I want:
- A 3-way English / Hungarian / Japanese dictionary with kanji breakdown and example sentences.
- A translator (EN/HU <-> JP) and a grammar checker that explains mistakes, both AI-powered.
- Anki-style spaced-repetition flashcards, with preset decks (professions, keigo, casual speech) and my own cards.
- A reading library: classic Japanese literature, NHK Easy news, modern web novels (Syosetu/Kakuyomu), and files I import; tap/long-press any kanji to look it up, toggleable furigana.
- Stretch: AI conversation practice.
Constraints: budget as close to free as possible (paid LLM APIs only if cheap), self-host the backend myself, native feel on iPhone, my data should survive losing the phone, and I want Claude Code to build it module by module with me approving every PR.
