# Pinned for a later run

Models someone asked for that are not in the sheet yet, and suggested fixes to existing
rows that nobody has applied yet. Read this before a model-update run. Delete a model
once its row is in, and a fix once it's applied or rejected.

| Model | Lab | Released | Primary source | Pinned |
|---|---|---|---|---|
| Gemini 4 Pro | Google DeepMind | Not yet | None yet. On 2026-09-24 DeepMind's Koray Kavukcuoglu said Gemini 4 is in post-training and will ship "as soon as possible" ([9to5Google](https://9to5google.com/2026/09/24/google-says-gemini-4-release-is-coming-as-soon-as-possible/)). | 2026-09-29 |

**Gemini 4 Pro:** Google hasn't named a "Pro" model or opened any beta. The only sightings
are anonymous test checkpoints that developers found. Add the row once Google announces
it. Use 🟢 if anyone can use it, or 🔴 if access is limited to vetted testers.

## Suggested fixes to existing rows

Not applied. A weekly run only adds rows, so it copies these into its PR body instead.
Apply one only when the user asks for it, then delete it here.

| Model | Field | Now | Suggested | Source | Pinned |
|---|---|---|---|---|---|
| Claude Opus 5 | HLE | blank | 63.6 (with tools; 56.6 without goes in Notes, as on the other Anthropic rows) | Table 8.1.A of the [Claude Opus 5.5 system card](https://www.anthropic.com/claude-opus-5-5-system-card) | 2026-09-30 |
| Chameleon | Tags | blank | `Image` (it generates images as well as text) | [arXiv 2405.09818](https://arxiv.org/abs/2405.09818) | 2026-09-30 |

## Image models

Image models went in on 2026-09-23: 41 rows from Jan 2025 on, tagged **`Image`**, plus
**`Video`** for models that also generate video. The `weekly-model-update` skill now
tracks them. Video-only and music models are still left out.
