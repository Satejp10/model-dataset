# Constellation build report

- Snapshot: `Pruned AI Models_Table.xlsx` captured `2026-09-04`
- Records in snapshot: **403**
- Parsed: **403** · skipped: **0** · filtered out: **0** · emitted: **403**

- Year range: **2017–2026**
- Month range: **2017-06 → 2026-09**

## Coverage

| Field | Records with a value |
|---|---:|
| link (Paper / Repo) | 403 / 403 |
| playground | 314 / 403 |
| alscore | 402 / 403 |
| paramsB | 402 / 403 |
| paramsActiveB | 164 / 403 |
| tokensB | 401 / 403 |
| mmlu | 133 / 403 |
| mmluPro | 102 / 403 |
| gpqa | 153 / 403 |
| hle | 78 / 403 |
| desc (Notes) | 403 / 403 |
| arch | 402 / 403 |
| disclosure | 401 / 403 |
| family | 13 / 403 |
| tags (non-empty) | 177 / 403 |

## Records per lab

| Lab | Records |
|---|---:|
| Google DeepMind | 95 |
| Microsoft | 45 |
| NVIDIA | 42 |
| OpenAI | 40 |
| Alibaba | 39 |
| Meta AI | 37 |
| Mistral | 26 |
| DeepSeek-AI | 21 |
| Anthropic | 20 |
| Moonshot AI | 12 |
| xAI | 12 |
| MiniMax | 7 |
| Z.AI | 7 |

## Horizon

`DATASET.horizon` = **2026-09** — the newest month among records that carry a primary-source link.
Records dated after the horizon: **0**.

## Scores

`score` and `scoreSrc` are **null on every record**. The snapshot carries no Artificial Analysis index, and none was derived: ALScore is emitted verbatim in `alscore` and was not rescaled, normalised, or back-extrapolated, and no score was inferred from MMLU/GPQA/HLE.

## Families formed

6 family/families, from the fixed variant-token allowlist only (no fuzzy matching, no edit distance, no inference from Notes). The consumer draws a family only when its members also share a month.

| Lab | Family | Members |
|---|---|---|
| Google DeepMind | Gemini 1.5 | Gemini 1.5 Flash, Gemini 1.5 Pro |
| Google DeepMind | Gemini 3 | Gemini 3 Flash, Gemini 3 Pro |
| Microsoft | phi-3 | phi-3-medium, phi-3-mini |
| Mistral | Mistral | Mistral Large, Mistral Small, Mistral-medium |
| NVIDIA | Cosmos 3 | Cosmos 3 Edge, Cosmos 3 Super |
| OpenAI | GPT-4 | GPT-4 Turbo, gpt-4-turbo-2024-04-09 |

## Id collisions

| Base slug | Records |
|---|---|
| `flame` | `FLAME` → `flame`; `FLAMe` → `flame-2` |

## Skipped records

None. Every snapshot record had a usable `Announced` date.

## Warnings

8 warning(s). These do not fail the build.

- `Engram` — unrecognised Public? value '🟡' - defaulted released=true
- `HOPE` — unrecognised Public? value '🟡' - defaulted released=true
- `LearnLM` — unrecognised Public? value '🟡' - defaulted released=true
- `Audio Flamingo` — unrecognised Public? value '🟡' - defaulted released=true
- `MedLM` — unrecognised Public? value '🟡' - defaulted released=true
- `Orca 2` — unrecognised Public? value '🟡' - defaulted released=true
- `Orca` — unrecognised Public? value '🟡' - defaulted released=true
- `LaMDA 2` — unrecognised Public? value '🟡' - defaulted released=true

## Judgments made

- **`desc` truncation.** The 240-char rule engages only when `Notes` actually exceeds 240 characters; a note that already fits is emitted whole with no ellipsis, since appending one would signal an elision that did not happen. Longer notes are cut at the last `.`/`?`/`!` within the first 240 characters, or at the last word boundary plus `…` when there is none. Text is always a verbatim prefix.
- **Id stability.** Ids are assigned over every parsed record *before* `--labs` / `--since` filtering, so a filtered run produces the same ids as a full run.
- **Families and horizon** are computed on the records actually emitted (after filtering), so neither can point at a record that was filtered away.
- **`--labs`** matches a record's aliased `lab` or its original `labRaw`, case-insensitively.
- **Filtered-out records** are counted, not listed individually; only records dropped for unusable data are listed under Skipped records.
