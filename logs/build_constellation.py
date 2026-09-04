#!/usr/bin/env python3
"""
build_constellation.py — emit constellation data from the committed snapshot.

Step 5 of the routine in logs/README.md. Reads logs/snapshots/latest.json (the diff
baseline written by diff_dataset.py: records keyed by model name, every value a string,
"" for missing) and writes into dist/:

  constellation-data.json  — the records as pure JSON (2-space indent, sorted keys)
  constellation-data.js    — the same data as three browser globals
  REPORT.md                — what was emitted, what was skipped, every judgment made

Reads nothing else and changes nothing else. Standard library only; no network.

  python logs/build_constellation.py                    # build into dist/
  python logs/build_constellation.py --check            # validate + report, write nothing
  python logs/build_constellation.py --labs "OpenAI,Anthropic" --since 2024-01

Determinism: two runs on the same snapshot produce byte-identical output. The only date
anywhere is the snapshot's own `captured` field.
"""

from __future__ import annotations

import argparse
import collections
import json
import math
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SNAPSHOT = REPO_ROOT / "logs" / "snapshots" / "latest.json"
DEFAULT_OUT = REPO_ROOT / "dist"

DESC_LIMIT = 240

# Labels that refer to the same organisation. The changelog already calls out this merge.
# Edit here to add more; nothing else clusters labs, and nothing matches by similarity.
LAB_ALIASES = {
    "Google": "Google DeepMind",
    "DeepMind": "Google DeepMind",
}

# The only tokens that may end a sibling variant name. Nothing else forms a family.
VARIANT_TOKENS = [
    "Pro", "Flash", "Flash-Lite", "Mini", "Nano", "Micro", "Lite", "Small", "Medium",
    "Large", "Instant", "Turbo", "Fast", "Heavy", "Thinking", "Reasoning", "Edge",
    "Super", "Base", "Chat", "Instruct",
]

METRICS = [
    {"id": "alscore", "name": "ALScore", "scale": "linear", "unit": "",
     "caption": "Radius = ALScore, as published"},
    {"id": "paramsB", "name": "Parameters", "scale": "log", "unit": "B",
     "caption": "Radius = total parameters, log scale"},
    {"id": "tokensB", "name": "Tokens", "scale": "log", "unit": "B",
     "caption": "Radius = training tokens, log scale"},
    {"id": None, "name": "Uniform", "scale": "none", "unit": "",
     "caption": "Radius fixed · time and lab only"},
]

# Source columns, as cleaned by diff_dataset.py.
C_MODEL = "Model"
C_LAB = "Lab"
C_PARAMS = "Params (total, B)"
C_PARAMS_ACTIVE = "Params (active, B)"
C_ANNOUNCED = "Announced"
C_ARCH = "Arch"
C_TOKENS = "Tokens trained (B)"
C_ALSCORE = "ALScore"
C_MMLU = "MMLU"
C_MMLU_PRO = "MMLU-Pro"
C_GPQA = "GPQA"
C_HLE = "HLE"
C_TRAINING = "Training dataset"
C_PUBLIC = "Public?"
C_DISCLOSURE = "Disclosure score"
C_PAPER = "Paper / Repo"
C_TAGS = "Tags"
C_NOTES = "Notes"
C_PLAYGROUND = "Playground"

DATE_FULL_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DATE_MONTH_RE = re.compile(r"^\d{4}-\d{2}$")
BENCHMARK_FIELDS = ("mmlu", "mmluPro", "gpqa", "hle")
NUMERIC_FIELDS = ("alscore", "paramsB", "paramsActiveB", "tokensB") + BENCHMARK_FIELDS

# Trailing date/version suffixes stripped before looking for a variant token.
SUFFIX_RES = [
    re.compile(r"\s*\([^)]*\)\s*$"),            # (new), (preview)
    re.compile(r"[\s\-]+\d{4}-\d{2}-\d{2}\s*$"),  # -2024-11-20
    re.compile(r"[\s\-]+\d{2}-\d{2}\s*$"),        # 06-05
]
TOKEN_RE = re.compile(
    r"^(?P<stem>.+?)[\s\-]+(?P<token>"
    + "|".join(re.escape(t) for t in sorted(VARIANT_TOKENS, key=len, reverse=True))
    + r")$",
    re.IGNORECASE,
)


# --------------------------------------------------------------------------- #
# Field helpers
# --------------------------------------------------------------------------- #
def slugify(text: str) -> str:
    """Lowercase, non-alphanumerics to '-', collapse runs, trim."""
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parse_number(raw: str, field: str, key: str, errors: list[str]):
    """Empty -> None. Present but not a finite number >= 0 -> hard error."""
    if raw is None or raw == "":
        return None
    try:
        value = float(raw)
    except (TypeError, ValueError):
        errors.append(f"{key}: {field} is present but not numeric: {raw!r}")
        return None
    if not math.isfinite(value) or value < 0:
        errors.append(f"{key}: {field} is present but not a finite number >= 0: {raw!r}")
        return None
    return value


def clean_url(raw: str):
    raw = (raw or "").strip()
    return raw if raw.startswith(("http://", "https://")) else None


def text_or_none(raw: str):
    raw = (raw or "").strip()
    return raw or None


def split_tags(raw: str) -> list[str]:
    return [t.strip() for t in (raw or "").split(",") if t.strip()]


def truncate_notes(raw: str):
    """
    Verbatim prefix of Notes, never paraphrased.

    Judgment: the 240-char rule only engages when Notes actually exceeds 240 chars.
    A note that already fits is emitted whole, with no ellipsis - appending one would
    signal an elision that did not happen, and cutting a fitting note at its first
    sentence end would drop text the source did include.
    """
    text = (raw or "").strip()
    if not text:
        return None
    if len(text) <= DESC_LIMIT:
        return text
    window = text[:DESC_LIMIT]
    cut = max(window.rfind("."), window.rfind("?"), window.rfind("!"))
    if cut != -1:
        return text[: cut + 1]
    space = window.rfind(" ")
    if space == -1:
        return window.rstrip() + "…"
    return text[:space].rstrip() + "…"


def strip_variant_suffix(name: str) -> str:
    previous, current = None, name.strip()
    while previous != current:
        previous = current
        for rx in SUFFIX_RES:
            current = rx.sub("", current).strip()
    return current


def variant_stem(name: str):
    """Stem if the name ends with an allowlisted variant token, else None."""
    match = TOKEN_RE.match(strip_variant_suffix(name))
    if not match:
        return None
    stem = match.group("stem").strip(" -")
    return stem if len(stem) >= 2 else None


# --------------------------------------------------------------------------- #
# Build
# --------------------------------------------------------------------------- #
def build_records(snapshot: dict, errors: list[str], warnings: list[tuple[str, str]],
                  skipped: list[tuple[str, str]]) -> list[dict]:
    """Parse every snapshot row into a record. Rows with an unusable date are skipped."""
    models = snapshot.get("models", {})
    order = [k for k in snapshot.get("order", []) if k in models]
    order += [k for k in sorted(models) if k not in set(order)]

    records = []
    for key in order:
        row = models[key]
        announced = (row.get(C_ANNOUNCED) or "").strip()
        if not DATE_FULL_RE.match(announced):
            reason = "empty Announced" if not announced else f"Announced not YYYY-MM-DD: {announced!r}"
            skipped.append((key, reason))
            continue

        lab_raw = (row.get(C_LAB) or "").strip()
        public = (row.get(C_PUBLIC) or "").strip()
        if public == "\U0001F7E2":
            released = True
        elif public == "\U0001F534":
            released = False
        else:
            released = True
            warnings.append(
                (key, f"unrecognised Public? value {public!r} - defaulted released=true")
            )

        link = clean_url(row.get(C_PAPER))
        notes = truncate_notes(row.get(C_NOTES))
        if notes is None:
            warnings.append((key, "missing Notes - desc is null"))
        if link is None:
            warnings.append((key, "missing primary-source link - estimated=true"))

        records.append({
            "_key": key,
            "id": None,
            "name": (row.get(C_MODEL) or "").strip(),
            "lab": LAB_ALIASES.get(lab_raw, lab_raw),
            "labRaw": lab_raw,
            "date": announced[:7],
            # The snapshot carries no Artificial Analysis index. alscore carries the
            # published number; score stays null rather than being invented.
            "score": None,
            "scoreSrc": None,
            "alscore": None,
            "mmlu": parse_number(row.get(C_MMLU), C_MMLU, key, errors),
            "mmluPro": parse_number(row.get(C_MMLU_PRO), C_MMLU_PRO, key, errors),
            "gpqa": parse_number(row.get(C_GPQA), C_GPQA, key, errors),
            "hle": parse_number(row.get(C_HLE), C_HLE, key, errors),
            "paramsB": parse_number(row.get(C_PARAMS), C_PARAMS, key, errors),
            "paramsActiveB": parse_number(row.get(C_PARAMS_ACTIVE), C_PARAMS_ACTIVE, key, errors),
            "tokensB": parse_number(row.get(C_TOKENS), C_TOKENS, key, errors),
            "arch": text_or_none(row.get(C_ARCH)),
            "family": None,
            "released": released,
            "estimated": link is None,
            "disclosure": text_or_none(row.get(C_DISCLOSURE)),
            "trainingSet": text_or_none(row.get(C_TRAINING)),
            "tags": split_tags(row.get(C_TAGS)),
            "desc": notes,
            "link": link,
            "playground": clean_url(row.get(C_PLAYGROUND)),
        })

        alscore = parse_number(row.get(C_ALSCORE), C_ALSCORE, key, errors)
        records[-1]["alscore"] = None if alscore is None else round(alscore, 2)

    return records


def assign_ids(records: list[dict]) -> list[tuple[str, list[tuple[str, str]]]]:
    """
    Ids are slugs of the snapshot key, so 'GPT-Red <OpenAI>' keeps its lab.

    Assigned over every parsed record before --labs/--since filtering, so an id never
    changes just because a run was filtered. Collisions take -2, -3 in sorted key order.
    """
    by_slug: dict[str, list[dict]] = collections.defaultdict(list)
    for rec in records:
        by_slug[slugify(rec["_key"])].append(rec)

    collisions = []
    for slug in sorted(by_slug):
        group = sorted(by_slug[slug], key=lambda r: r["_key"])
        for index, rec in enumerate(group):
            rec["id"] = slug if index == 0 else f"{slug}-{index + 1}"
        if len(group) > 1:
            collisions.append((slug, [(r["_key"], r["id"]) for r in group]))
    return collisions


def assign_families(records: list[dict]) -> list[tuple[str, str, list[str]]]:
    """
    Group sibling variants that share a lab and a stem. Computed on the records actually
    emitted, so a family never points at a record the filters removed.
    """
    groups: dict[tuple[str, str], list[dict]] = collections.defaultdict(list)
    for rec in records:
        stem = variant_stem(rec["name"])
        if stem:
            groups[(rec["lab"], stem.lower())].append(rec)

    families = []
    for (lab, _stem_key), members in sorted(groups.items()):
        if len(members) < 2:
            continue
        members.sort(key=lambda r: r["name"])
        stem = variant_stem(members[0]["name"])
        for rec in members:
            rec["family"] = stem
        families.append((lab, stem, [r["name"] for r in members]))
    return families


def validate(records: list[dict], errors: list[str]) -> None:
    seen: dict[str, str] = {}
    for rec in records:
        label = rec["_key"]
        for field in ("id", "name", "lab"):
            if not rec.get(field):
                errors.append(f"{label}: missing {field}")
        rid = rec.get("id")
        if rid:
            if rid in seen:
                errors.append(f"duplicate id {rid!r}: {seen[rid]!r} and {label!r}")
            else:
                seen[rid] = label
        if not DATE_MONTH_RE.match(rec.get("date") or ""):
            errors.append(f"{label}: date is not YYYY-MM: {rec.get('date')!r}")
        for field in NUMERIC_FIELDS:
            value = rec.get(field)
            if value is None:
                continue
            if not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
                errors.append(f"{label}: {field} is not a finite number >= 0: {value!r}")

    for metric in METRICS:
        mid = metric["id"]
        if mid is None:
            continue
        if not any(rec.get(mid) is not None for rec in records):
            errors.append(f"METRICS id {mid!r} is carried by no record")


# --------------------------------------------------------------------------- #
# Render
# --------------------------------------------------------------------------- #
def public_record(rec: dict) -> dict:
    return {k: v for k, v in rec.items() if not k.startswith("_")}


def build_dataset_header(snapshot: dict, horizon) -> dict:
    captured = snapshot.get("captured", "")
    return {
        "version": f"lifearchitect-{captured}",
        "updated": captured,
        "scoreMetric": "LifeArchitect ALScore",
        "scoreNote": "ALScore as published in the Models Table. Not an Artificial Analysis index.",
        "horizon": horizon,
        "palette": "signal",
    }


def render_js(dataset: dict, records: list[dict]) -> str:
    # Keys stay in their documented order here (the sorted-key requirement is for the
    # .json diff). ensure_ascii keeps U+2028/U+2029 escaped, which raw JS cannot carry.
    def dump(obj):
        return json.dumps(obj, ensure_ascii=True, separators=(",", ":"))

    return (
        "// Generated by logs/build_constellation.py from logs/snapshots/latest.json.\n"
        "// Do not edit by hand - re-run the generator instead.\n"
        f"window.DATASET = {dump(dataset)};\n"
        f"window.METRICS = {dump(METRICS)};\n"
        f"window.MODELS = {dump([public_record(r) for r in records])};\n"
    )


def render_json(dataset: dict, records: list[dict]) -> str:
    payload = {
        "dataset": dataset,
        "metrics": METRICS,
        "models": [public_record(r) for r in records],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def render_report(snapshot, records, total_parsed, skipped, filtered_out, collisions,
                  families, horizon, after_horizon, warnings, filters) -> str:
    lines = ["# Constellation build report", ""]
    lines += [
        f"- Snapshot: `{snapshot.get('source_file', '?')}` captured `{snapshot.get('captured', '?')}`",
        f"- Records in snapshot: **{len(snapshot.get('models', {}))}**",
        f"- Parsed: **{total_parsed}** · skipped: **{len(skipped)}** · "
        f"filtered out: **{filtered_out}** · emitted: **{len(records)}**",
    ]
    if filters:
        lines.append(f"- Filters applied: {filters}")
    lines.append("")

    if records:
        years = sorted({r["date"][:4] for r in records})
        lines += [f"- Year range: **{years[0]}–{years[-1]}**",
                  f"- Month range: **{min(r['date'] for r in records)} → "
                  f"{max(r['date'] for r in records)}**", ""]

    lines += ["## Coverage", "", "| Field | Records with a value |", "|---|---:|"]
    for label, field in [("link (Paper / Repo)", "link"), ("playground", "playground"),
                         ("alscore", "alscore"), ("paramsB", "paramsB"),
                         ("paramsActiveB", "paramsActiveB"), ("tokensB", "tokensB"),
                         ("mmlu", "mmlu"), ("mmluPro", "mmluPro"), ("gpqa", "gpqa"),
                         ("hle", "hle"), ("desc (Notes)", "desc"), ("arch", "arch"),
                         ("disclosure", "disclosure"), ("family", "family")]:
        count = sum(1 for r in records if r.get(field) is not None)
        lines.append(f"| {label} | {count} / {len(records)} |")
    tagged = sum(1 for r in records if r["tags"])
    lines += [f"| tags (non-empty) | {tagged} / {len(records)} |", ""]

    lines += ["## Records per lab", "", "| Lab | Records |", "|---|---:|"]
    per_lab = collections.Counter(r["lab"] for r in records)
    for lab, count in sorted(per_lab.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"| {lab} | {count} |")
    lines.append("")

    lines += ["## Horizon", "",
              f"`DATASET.horizon` = **{horizon}** — the newest month among records that "
              "carry a primary-source link.",
              f"Records dated after the horizon: **{after_horizon}**.", ""]

    lines += ["## Scores", "",
              "`score` and `scoreSrc` are **null on every record**. The snapshot carries no "
              "Artificial Analysis index, and none was derived: ALScore is emitted verbatim "
              "in `alscore` and was not rescaled, normalised, or back-extrapolated, and no "
              "score was inferred from MMLU/GPQA/HLE.", ""]

    lines += ["## Families formed", ""]
    if families:
        lines.append(f"{len(families)} family/families, from the fixed variant-token "
                     "allowlist only (no fuzzy matching, no edit distance, no inference "
                     "from Notes). The consumer draws a family only when its members also "
                     "share a month.")
        lines.append("")
        lines += ["| Lab | Family | Members |", "|---|---|---|"]
        for lab, stem, members in families:
            lines.append(f"| {lab} | {stem} | {', '.join(members)} |")
    else:
        lines.append("None. No record ended with an allowlisted variant token while sharing "
                     "its stem with another record from the same lab.")
    lines.append("")

    lines += ["## Id collisions", ""]
    if collisions:
        lines += ["| Base slug | Records |", "|---|---|"]
        for slug, members in collisions:
            rendered = "; ".join(f"`{key}` → `{rid}`" for key, rid in members)
            lines.append(f"| `{slug}` | {rendered} |")
    else:
        lines.append("None. Every record slugged to a unique id.")
    lines.append("")

    lines += ["## Skipped records", ""]
    if skipped:
        lines += ["| Record | Reason |", "|---|---|"]
        for key, reason in skipped:
            lines.append(f"| `{key}` | {reason} |")
    else:
        lines.append("None. Every snapshot record had a usable `Announced` date.")
    lines.append("")

    lines += ["## Warnings", ""]
    if warnings:
        lines.append(f"{len(warnings)} warning(s). These do not fail the build.")
        lines.append("")
        for key, message in warnings:
            lines.append(f"- `{key}` — {message}")
    else:
        lines.append("None.")
    lines.append("")

    lines += [
        "## Judgments made", "",
        "- **`desc` truncation.** The 240-char rule engages only when `Notes` actually "
        "exceeds 240 characters; a note that already fits is emitted whole with no "
        "ellipsis, since appending one would signal an elision that did not happen. "
        "Longer notes are cut at the last `.`/`?`/`!` within the first 240 characters, or "
        "at the last word boundary plus `…` when there is none. Text is always a verbatim "
        "prefix.",
        "- **Id stability.** Ids are assigned over every parsed record *before* `--labs` / "
        "`--since` filtering, so a filtered run produces the same ids as a full run.",
        "- **Families and horizon** are computed on the records actually emitted (after "
        "filtering), so neither can point at a record that was filtered away.",
        "- **`--labs`** matches a record's aliased `lab` or its original `labRaw`, "
        "case-insensitively.",
        "- **Filtered-out records** are counted, not listed individually; only records "
        "dropped for unusable data are listed under Skipped records.",
        "",
    ]
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def main() -> None:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--snapshot", type=Path, default=DEFAULT_SNAPSHOT,
                    help="snapshot to read (default: logs/snapshots/latest.json)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT,
                    help="output directory (default: dist)")
    ap.add_argument("--labs", default="",
                    help='comma-separated labs to keep, e.g. "OpenAI,Anthropic"')
    ap.add_argument("--since", default="", help="keep records dated YYYY-MM or later")
    ap.add_argument("--check", action="store_true",
                    help="validate and report without writing anything")
    args = ap.parse_args()

    if not args.snapshot.exists():
        sys.exit(f"Snapshot not found: {args.snapshot}")
    if args.since and not DATE_MONTH_RE.match(args.since):
        sys.exit(f"--since must be YYYY-MM, got {args.since!r}")

    snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))

    errors: list[str] = []
    warnings: list[str] = []
    skipped: list[tuple[str, str]] = []

    records = build_records(snapshot, errors, warnings, skipped)
    total_parsed = len(records)
    collisions = assign_ids(records)

    wanted = {lab.strip().lower() for lab in args.labs.split(",") if lab.strip()}
    if wanted:
        records = [r for r in records
                   if r["lab"].lower() in wanted or r["labRaw"].lower() in wanted]
    if args.since:
        records = [r for r in records if r["date"] >= args.since]
    filtered_out = total_parsed - len(records)

    records.sort(key=lambda r: (r["date"], r["lab"], r["name"]))
    families = assign_families(records)

    # Keep only warnings about records that actually survived filtering, so the report
    # never flags a row it did not emit.
    emitted_keys = {r["_key"] for r in records}
    warnings = [(key, message) for key, message in warnings if key in emitted_keys]

    linked = [r["date"] for r in records if r["link"]]
    horizon = max(linked) if linked else (max((r["date"] for r in records), default=None))
    after_horizon = sum(1 for r in records if horizon and r["date"] > horizon)
    if not linked and records:
        warnings.append(("(dataset)", "no record carries a link; horizon fell back to the newest month"))

    validate(records, errors)
    if not records:
        errors.append("no records to emit (check --labs / --since)")

    if errors:
        print(f"BUILD FAILED - {len(errors)} problem(s), nothing written:", file=sys.stderr)
        for problem in errors:
            print(f"  - {problem}", file=sys.stderr)
        sys.exit(1)

    filters = ", ".join(
        part for part in (
            f"--labs {args.labs!r}" if args.labs else "",
            f"--since {args.since}" if args.since else "",
        ) if part
    )
    report = render_report(snapshot, records, total_parsed, skipped, filtered_out,
                           collisions, families, horizon, after_horizon, warnings, filters)
    dataset = build_dataset_header(snapshot, horizon)

    if args.check:
        print(report)
        print(f"OK - {len(records)} record(s) would be emitted. Nothing written (--check).")
        return

    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "constellation-data.json").write_text(render_json(dataset, records), encoding="utf-8")
    (args.out / "constellation-data.js").write_text(render_js(dataset, records), encoding="utf-8")
    (args.out / "REPORT.md").write_text(report, encoding="utf-8")

    rel = args.out.relative_to(REPO_ROOT) if args.out.is_relative_to(REPO_ROOT) else args.out
    print(f"Wrote {len(records)} record(s) to {rel}/constellation-data.json, "
          f"{rel}/constellation-data.js, {rel}/REPORT.md")
    if warnings:
        print(f"{len(warnings)} warning(s) - see {rel}/REPORT.md")


if __name__ == "__main__":
    main()
