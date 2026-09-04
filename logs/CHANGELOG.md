# Changelog — Pruned AI Models_Table.xlsx

All notable changes to the model dataset are recorded here, newest first.

The **Current dataset specs** block and each dated entry under **Change history**
are written by `logs/diff_dataset.py` (see `logs/README.md`). You can also add or
edit entries by hand — just keep the two marker comments in place.

---

## Current dataset specs

<!-- SPECS:START -->
_Snapshot as of 2026-09-04_

| Property | Value |
|---|---|
| File | `Pruned AI Models_Table.xlsx` |
| Sheet | `Models` |
| Header row | Row 2 |
| Number of models | **403** |
| Number of distinct labs (as-written) | **15** |
| Columns (named) | **20** |

### Columns

| # | Column |
|---|---|
| 1 | Model |
| 2 | Lab |
| 3 | Params (total, B) |
| 4 | Params (active, B) |
| 5 | Announced |
| 6 | Arch |
| 7 | Tokens trained (B) |
| 8 | ALScore |
| 9 | MMLU |
| 10 | MMLU-Pro |
| 11 | GPQA |
| 12 | HLE |
| 13 | Training dataset |
| 14 | Public? |
| 15 | Disclosure score |
| 16 | Paper / Repo |
| 17 | Tags |
| 18 | Notes |
| 19 | Count (rough) |
| 20 | Playground |

### Models per lab

| Lab | Models |
|---|---:|
| Google DeepMind | 57 |
| Microsoft | 45 |
| NVIDIA | 42 |
| OpenAI | 40 |
| Alibaba | 39 |
| Meta AI | 37 |
| Google | 31 |
| Mistral | 26 |
| DeepSeek-AI | 21 |
| Anthropic | 20 |
| Moonshot AI | 12 |
| xAI | 12 |
| DeepMind | 7 |
| MiniMax | 7 |
| Z.AI | 7 |

> Note: `Google DeepMind`, `Google`, and `DeepMind` are recorded as separate
> labels. If treated as one organisation, subtract 2 from the distinct-lab count.
<!-- SPECS:END -->

---

## Change history

<!-- CHANGES:START -->

### 2026-09-04 — Update (+2 / -0 / ~0)

Source export: `Pruned AI Models_Table.xlsx` · models 401 → 403 · labs 15 → 15 · columns 20 → 20

**Models added (2):**
- GPT-6 Astra — OpenAI
- Claude Fable 5.1 — Anthropic

**Models removed (0):**
- none

**Models changed (0):**
- none


### 2026-09-01 — Baseline snapshot
- Established this logs folder.
- Recorded initial dataset specs: 401 models across 15 lab labels, 20 named columns.
- No changes made to the dataset itself in this entry.
