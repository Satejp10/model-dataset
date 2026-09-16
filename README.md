# model-dataset

A pruned copy of the [LifeArchitect.ai Models Table](https://lifearchitect.ai/models-table/),
kept as `Pruned AI Models_Table.xlsx` — 403 frontier and near-frontier models from 15 labs,
with parameters, training tokens, benchmarks, release status and a primary-source link each.
Small Python scripts in `logs/` diff a fresh export against the last snapshot, record the
delta in a changelog, and build browser-ready JSON/JS into `dist/`.

See [`logs/README.md`](logs/README.md) for the update routine and the scripts.

Data: Dr Alan D. Thompson, LifeArchitect.ai Models Table (Sep/2026).
