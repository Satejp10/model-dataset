# Pinned for a later run

Models someone asked for that are not in the sheet yet. Read this before a model-update
run, and delete an entry once its row is in.

## Image models

The sheet holds no image-generation models, and the `weekly-model-update` skill skips
image, video and music generators. So these go in only when someone asks for them by
name, or once that skip rule changes.

When they go in, tag them **`Image`** in the `Tags` column, plus **`Video`** for a model
that also generates video. The tag keeps them out of any view that should only show
language models. No new column is needed: `Tags` is free text and already carries
`Reasoning`, `Diffusion` and `SOTA`.

| Model | Lab | Released | Primary source | Pinned |
|---|---|---|---|---|
| GPT Image 2 (`gpt-image-2`) | OpenAI | 2026-04-21 | https://developers.openai.com/api/docs/models/gpt-image-2 | 2026-09-23 |
| Grok Imagine Image 2.0 | xAI | 2026-08-07 | https://x.ai/news/grok-imagine-image-2 | 2026-09-23 |

Also seen during the 2026-09-23 run but not requested. Check each against a primary
source before adding it:

- MAI-Image-2.5-Pro (Jul 2026) and MAI-Image-2.6 (Microsoft), https://microsoft.ai/news/
- Muse Image and Muse Video (Meta AI, Jul 2026), https://ai.meta.com/blog/introducing-muse-image-muse-video-msl/
- Qwen-Image-2.1 (Alibaba, Sep 2026), https://huggingface.co/Qwen/Qwen-Image-2.1
- Grok Imagine Video 1.5 (xAI), https://docs.x.ai/developers/release-notes
- ChatGPT Images 2.5 (OpenAI, Sep 2026). Only press coverage seen so far.
