# Changelog — Pruned AI Models_Table.xlsx

All notable changes to the model dataset are recorded here, newest first.

---

## Current dataset specs

_Snapshot as of 2026-09-01_

| Property | Value |
|---|---|
| File | `Pruned AI Models_Table.xlsx` |
| Sheet | `Models` |
| Header row | Row 2 |
| Data rows | Rows 3–403 |
| Number of models | **401** |
| Number of distinct labs | **15** |
| Columns (populated) | **20** |
| Sheet extent | 1000 rows × 21 columns (rows 404–1000 empty; col 8 is a blank spacer) |

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
| 8 | _(blank spacer)_ |
| 9 | ALScore |
| 10 | MMLU |
| 11 | MMLU-Pro |
| 12 | GPQA |
| 13 | HLE |
| 14 | Training dataset |
| 15 | Public? |
| 16 | Disclosure score |
| 17 | Paper / Repo |
| 18 | Tags |
| 19 | Notes |
| 20 | Count (rough) |
| 21 | Playground |

### Models per lab

| Lab | Models |
|---|---:|
| Google DeepMind | 57 |
| Microsoft | 45 |
| NVIDIA | 42 |
| OpenAI | 39 |
| Alibaba | 39 |
| Meta AI | 37 |
| Google | 31 |
| Mistral | 26 |
| DeepSeek-AI | 21 |
| Anthropic | 19 |
| Moonshot AI | 12 |
| xAI | 12 |
| Z.AI | 7 |
| MiniMax | 7 |
| DeepMind | 7 |

> Note: `Google DeepMind`, `Google`, and `DeepMind` are recorded as separate lab
> labels. If treated as one organization, the distinct-lab count is **13**.

---

## Change history

### 2026-09-01 — Baseline snapshot
- Established this logs folder.
- Recorded initial dataset specs above: 401 models across 15 lab labels, 20 populated columns.
- No changes made to the dataset itself in this entry.
