# Constellation build report

- Snapshot: `Pruned AI Models_Table.xlsx` captured `2026-09-23`
- Data: Dr Alan D. Thompson, LifeArchitect.ai Models Table (Sep/2026). Carried into `DATASET.source`.
- Records in snapshot: **488**
- Parsed: **488** · skipped: **0** · filtered out: **0** · emitted: **488**

- Year range: **2017–2026**
- Month range: **2017-06 → 2026-09**

## Coverage

| Field | Records with a value |
|---|---:|
| link (Paper / Repo) | 488 / 488 |
| playground | 389 / 488 |
| alscore | 408 / 488 |
| paramsB | 422 / 488 |
| paramsActiveB | 175 / 488 |
| tokensB | 409 / 488 |
| mmlu | 137 / 488 |
| mmluPro | 105 / 488 |
| gpqa | 157 / 488 |
| hle | 83 / 488 |
| desc (Notes) | 488 / 488 |
| arch | 416 / 488 |
| disclosure | 401 / 488 |
| family | 25 / 488 |
| tags (non-empty) | 249 / 488 |

## Records per lab

| Lab | Records |
|---|---:|
| Google DeepMind | 108 |
| Microsoft | 54 |
| OpenAI | 51 |
| Alibaba | 46 |
| NVIDIA | 45 |
| Meta AI | 41 |
| Mistral | 27 |
| DeepSeek-AI | 24 |
| Anthropic | 22 |
| xAI | 16 |
| Moonshot AI | 12 |
| Xiaomi | 11 |
| Z.AI | 11 |
| MiniMax | 7 |
| ByteDance | 5 |
| Black Forest Labs | 4 |
| Midjourney | 4 |

## Access

From the source `Public?` column, on LifeArchitect's legend: 🟢 publicly accessible, 🟡 video or scripted demo only, 🔴 held in the lab and never released. `released` is true for 🟢 alone — a 🟡 demo is something you cannot use — and `access` is what tells a demo apart from a lab model.

| `access` | Legend | `released` | Records |
|---|---|---|---:|
| `public` | 🟢 | `true` | 408 |
| `demo` | 🟡 | `false` | 8 |
| `unreleased` | 🔴 | `false` | 72 |

## Horizon

`DATASET.horizon` = **2026-09** — the newest month among records that carry a primary-source link.
Records dated after the horizon: **0**.

## Scores

`score` and `scoreSrc` are **null on every record**. The snapshot carries no Artificial Analysis index, and none was derived: ALScore is emitted verbatim in `alscore` and was not rescaled, normalised, or back-extrapolated, and no score was inferred from MMLU/GPQA/HLE.

## Families formed

12 family/families, from the fixed variant-token allowlist only (no fuzzy matching, no edit distance, no inference from Notes). The consumer draws a family only when its members also share a month.

| Lab | Family | Members |
|---|---|---|
| ByteDance | Seedream 5.0 | Seedream 5.0 Lite, Seedream 5.0 Pro |
| DeepSeek-AI | DeepSeek-V4 | DeepSeek-V4-Flash, DeepSeek-V4-Pro |
| Google DeepMind | Gemini 1.5 | Gemini 1.5 Flash, Gemini 1.5 Pro |
| Google DeepMind | Gemini 3 | Gemini 3 Flash, Gemini 3 Pro |
| Google DeepMind | Gemini 3.5 | Gemini 3.5 Flash, Gemini 3.5 Flash-Lite |
| Microsoft | MAI-Image-2.5 | MAI-Image-2.5-Flash, MAI-Image-2.5-Pro |
| Microsoft | phi-3 | phi-3-medium, phi-3-mini |
| Mistral | Mistral | Mistral Large, Mistral Small, Mistral-medium |
| NVIDIA | Cosmos 3 | Cosmos 3 Edge, Cosmos 3 Super |
| OpenAI | GPT-4 | GPT-4 Turbo, gpt-4-turbo-2024-04-09 |
| Xiaomi | MiMo-V2 | MiMo-V2-Flash, MiMo-V2-Pro |
| Xiaomi | MiMo-V2.6 | MiMo-V2.6-Flash, MiMo-V2.6-Pro |

## Id collisions

| Base slug | Records |
|---|---|
| `flame` | `FLAME` → `flame`; `FLAMe` → `flame-2` |

## Skipped records

None. Every snapshot record had a usable `Announced` date.

## Warnings

2 warning(s). These do not fail the build.

- `MAI-Cyber-1-Flash` — unrecognised Public? value '' - defaulted released=true, access='public'
- `Robostral Navigate` — unrecognised Public? value '' - defaulted released=true, access='public'

## Judgments made

- **`desc` truncation.** The 240-char rule engages only when `Notes` actually exceeds 240 characters; a note that already fits is emitted whole with no ellipsis, since appending one would signal an elision that did not happen. Longer notes are cut at the last `.`/`?`/`!` within the first 240 characters, or at the last word boundary plus `…` when there is none. Text is always a verbatim prefix.
- **🟡 is not released.** A model shown only in a video or a scripted demo is `released: false`, alongside 🔴. The two are still distinguishable: `access` is `"demo"` for 🟡 and `"unreleased"` for 🔴. A `Public?` glyph outside the legend falls back to `released: true` / `access: "public"` and is listed under Warnings; `released == (access == "public")` holds on every record either way.
- **Id stability.** Ids are assigned over every parsed record *before* `--labs` / `--since` filtering, so a filtered run produces the same ids as a full run.
- **Families and horizon** are computed on the records actually emitted (after filtering), so neither can point at a record that was filtered away.
- **`--labs`** matches a record's aliased `lab` or its original `labRaw`, case-insensitively.
- **Filtered-out records** are counted, not listed individually; only records dropped for unusable data are listed under Skipped records.
