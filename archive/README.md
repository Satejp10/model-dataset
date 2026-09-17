# Archive

Frozen copies of the dataset. **Never edit these files.** They are a fixed
reference point, not a working copy — nothing in the repo reads from them, and the
scripts in `logs/` never write to them.

## `2026-09-17-baseline/`

A frozen copy taken before weekly automation started, so there is always a known-good
state to fall back to. Source commit `f2795b5`, 403 models.

| File | Taken from |
|---|---|
| `Pruned AI Models_Table.xlsx` | the repo root |
| `latest.json` | `logs/snapshots/latest.json` |
| `CHANGELOG.md` | `logs/CHANGELOG.md` |

**To restore.** Copy the workbook back to the repo root, then run the logging routine in
[`logs/README.md`](../logs/README.md) — `diff_dataset.py` will diff it against whatever
the current snapshot holds and log the delta, and `build_constellation.py` rebuilds
`dist/`:

```bash
cp "archive/2026-09-17-baseline/Pruned AI Models_Table.xlsx" .
```

**To rebuild the old `dist/`** without touching anything in the repo:

```bash
python logs/build_constellation.py \
  --snapshot archive/2026-09-17-baseline/latest.json \
  --out /tmp/old-dist
```

## Earlier states

Git history has them — no need to freeze a copy of everything:

| Commit | State |
|---|---|
| `f83a3e8` | before the Sep 16 fixes |
| `7538005` | the original 401-model upload |

```bash
git show 7538005:"Pruned AI Models_Table.xlsx" > /tmp/original.xlsx
```
