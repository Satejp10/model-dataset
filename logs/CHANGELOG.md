# Changelog — Pruned AI Models_Table.xlsx

All notable changes to the model dataset are recorded here, newest first.

The **Current dataset specs** block and each dated entry under **Change history**
are written by `logs/diff_dataset.py` (see `logs/README.md`). You can also add or
edit entries by hand — just keep the two marker comments in place.

---

## Current dataset specs

<!-- SPECS:START -->
_Snapshot as of 2026-09-23_

| Property | Value |
|---|---|
| File | `Pruned AI Models_Table.xlsx` |
| Sheet | `Models` |
| Header row | Row 2 |
| Number of models | **488** |
| Number of distinct labs (as-written) | **19** |
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
| Google DeepMind | 70 |
| Microsoft | 54 |
| OpenAI | 51 |
| Alibaba | 46 |
| NVIDIA | 45 |
| Meta AI | 41 |
| Google | 31 |
| Mistral | 27 |
| DeepSeek-AI | 24 |
| Anthropic | 22 |
| xAI | 16 |
| Moonshot AI | 12 |
| Xiaomi | 11 |
| Z.AI | 11 |
| DeepMind | 7 |
| MiniMax | 7 |
| ByteDance | 5 |
| Black Forest Labs | 4 |
| Midjourney | 4 |

> Note: `Google DeepMind`, `Google`, and `DeepMind` are recorded as separate
> labels. If treated as one organisation, subtract 2 from the distinct-lab count.
<!-- SPECS:END -->

---

## Change history

<!-- CHANGES:START -->

### 2026-09-23 — Update (+41 / -0 / ~0)

Source export: `Pruned AI Models_Table.xlsx` · models 447 → 488 · labs 16 → 19 · columns 20 → 20

**Models added (41):**
- GPT-Image-2.5 Sunburst — OpenAI
- GPT-Image-2.5 Flare — OpenAI
- MAI-Image-2.6-Flash — Microsoft
- Qwen-Image-2.1 — Alibaba
- Grok Imagine Image 2.0 — xAI
- MAI-Image-2.6 — Microsoft
- Seedream 5.0 Pro — ByteDance
- MAI-Image-2.5-Pro — Microsoft
- Muse Image — Meta AI
- Qwen-Image-3.0 — Alibaba
- FLUX 3 — Black Forest Labs
- Midjourney V8.2 — Midjourney
- Gemini 3.1 Flash-Lite Image (Nano Banana 2 Lite) — Google DeepMind
- MAI-Image-2.5 — Microsoft
- MAI-Image-2.5-Flash — Microsoft
- GPT-Image-2 — OpenAI
- Midjourney V8.1 — Midjourney
- MAI-Image-2 — Microsoft
- Midjourney V8 — Midjourney
- Gemini 3.1 Flash Image (Nano Banana 2) — Google DeepMind
- Seedream 5.0 Lite — ByteDance
- Qwen-Image-2.0 — Alibaba
- Grok Imagine — xAI
- GLM-Image — Z.AI
- FLUX.2 [klein] — Black Forest Labs
- GPT-Image-1.5 — OpenAI
- Seedream 4.5 — ByteDance
- Gemini 3 Pro Image (Nano Banana Pro) — Google DeepMind
- FLUX.2 — Black Forest Labs
- GPT-Image-1 Mini — OpenAI
- MAI-Image-1 — Microsoft
- Seedream 4.0 — ByteDance
- Gemini 2.5 Flash Image (Nano Banana) — Google DeepMind
- Qwen-Image — Alibaba
- Imagen 4 — Google DeepMind
- FLUX.1 Kontext — Black Forest Labs
- GPT-Image-1 — OpenAI
- Seedream 3.0 — ByteDance
- Midjourney V7 — Midjourney
- CogView4-6B — Z.AI
- Janus-Pro-7B — DeepSeek-AI

**Models removed (0):**
- none

**Models changed (0):**
- none


### 2026-09-23 — Update (+25 / -0 / ~0)

Source export: `Pruned AI Models_Table.xlsx` · models 422 → 447 · labs 15 → 16 · columns 20 → 20

**Models added (25):**
- Claude Opus 5.5 — Anthropic
- GPT-6 Sol — OpenAI
- GPT-6 Luna — OpenAI
- Gemini 3.8 Live — Google DeepMind
- Gemini 3.8 Live Extended Thinking — Google DeepMind
- Grok 4.7 — xAI
- Muse Spark 1.3 — Meta AI
- Nemotron-3-Labs-Ultra-Math — NVIDIA
- MiMo-V2.6-Pro — Xiaomi
- MiMo-V2.6-Flash — Xiaomi
- Muse Spark 1.2 — Meta AI
- Muse Glimmer — Meta AI
- MAI-Cyber-1-Flash — Microsoft
- NVIDIA-NemotronLabs-VoiceChat-11B — NVIDIA
- Nemotron 3.5 Lightning — NVIDIA
- Mage-VL — Microsoft
- MiMo-V2.5 — Xiaomi
- MiMo-V2.5-Pro — Xiaomi
- MiMo-V2-Pro — Xiaomi
- MiMo-V2-Omni — Xiaomi
- MiMo-V2-Flash — Xiaomi
- MiMo-Embodied-7B — Xiaomi
- MiMo-Audio-7B — Xiaomi
- MiMo-VL-7B — Xiaomi
- MiMo-7B — Xiaomi

**Models removed (0):**
- none

**Models changed (0):**
- none


### 2026-09-17 — Update (+19 / -0 / ~0)

Source export: `Pruned AI Models_Table.xlsx` · models 403 → 422 · labs 15 → 15 · columns 20 → 20

**Models added (19):**
- Gemini 3.8 Flash — Google DeepMind
- Gemini 3.8 Flash Cyber — Google DeepMind
- DeepSeek-V4.1-Flash — DeepSeek-AI
- Grok 4.6 — xAI
- Gemini 3.7 Flash — Google DeepMind
- Qwen3.8-2.4T-A95B — Alibaba
- Qwen3.8-27B — Alibaba
- Qwen3.8-Flash-Next — Alibaba
- GLM-5.3 — Z.AI
- GLM-5.3-Flash — Z.AI
- Claude Opus 5 — Anthropic
- GPT-5.6 Terra — OpenAI
- GPT-5.6 Luna — OpenAI
- GPT-Live-1 — OpenAI
- Gemini 3.6 Flash — Google DeepMind
- Gemini 3.5 Flash-Lite — Google DeepMind
- Gemini 3.5 Flash Cyber — Google DeepMind
- DeepSeek-V4-Flash — DeepSeek-AI
- Robostral Navigate — Mistral

**Models removed (0):**
- none

**Models changed (0):**
- none


### 2026-09-16 — Update (+0 / -0 / ~2)

Source export: `Pruned AI Models_Table.xlsx` · models 403 → 403 · labs 15 → 15 · columns 20 → 20

**Models added (0):**
- none

**Models removed (0):**
- none

**Models changed (2):**
- GPT-6 Astra — OpenAI
  - Paper / Repo: `https://developers.openai.com/api/docs/models/gpt-6-astra` → `https://deploymentsafety.openai.com/gpt-6-astra/gpt-6-astra.pdf`
- Claude Fable 5.1 — Anthropic
  - Tokens trained (B): `∅` → `250000`


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
