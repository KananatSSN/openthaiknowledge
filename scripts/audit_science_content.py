"""Sample the 95-set science baseline and export Phase 2 audit evidence.

This is an automated integrity pass, not a substitute for scientific review. It
checks that deterministic samples generate successfully, retain their approved
catalog placement, and expose non-empty, distinct multiple-choice content.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from random import Random

from otk.core import REGISTRY, catalog, generate
from otk.core.curriculum_science import SCIENCE_BASELINE_KEYS
from otk.sets._support.science_stages import REVIEWED_SCIENCE_STAGES


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs/for_admin/science_content_audit.csv"
MAPPING_FILE = ROOT / "docs/for_admin/science_ipst_mapping.csv"
FIELDS = (
    "key", "subject", "mapped_level", "legacy_level", "curriculum_topic",
    "mapping_status", "sampled_items", "unique_stems", "min_choices",
    "max_choices", "generation_failures", "metadata_failures",
    "distinct_choice_failures", "automated_status", "manual_review",
    "review_note", "failure_notes",
)


def _signature(value: object) -> str:
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        default=lambda item: item.model_dump(mode="json"),
    )


def audit(*, seeds: int) -> list[dict]:
    if seeds < 1:
        raise ValueError("seeds must be at least 1")

    by_key = {
        row["key"]: row for row in catalog()
        if row["key"] in SCIENCE_BASELINE_KEYS
    }
    with MAPPING_FILE.open(encoding="utf-8", newline="") as handle:
        mapping = {row["key"]: row for row in csv.DictReader(handle)}

    rows: list[dict] = []
    for key in sorted(SCIENCE_BASELINE_KEYS):
        entry = by_key[key]
        spec = REGISTRY[key]
        unique_stems: set[str] = set()
        choice_counts: list[int] = []
        generation_failures = 0
        metadata_failures = 0
        distinct_choice_failures = 0
        failure_notes: list[str] = []

        for seed in range(seeds):
            try:
                question = generate(key, Random(seed))
            except Exception as exc:  # the report must retain every failing key
                generation_failures += 1
                if len(failure_notes) < 3:
                    failure_notes.append(f"seed {seed}: {type(exc).__name__}: {exc}")
                continue

            unique_stems.add(_signature(question.stem))
            choice_counts.append(len(question.choices))
            choices = [_signature(choice.content) for choice in question.choices]
            if len(choices) < 2 or len(choices) != len(set(choices)):
                distinct_choice_failures += 1
                if len(failure_notes) < 3:
                    failure_notes.append(f"seed {seed}: fewer than two distinct choices")
            if not question.stem or not all(choice.content for choice in question.choices):
                metadata_failures += 1
                if len(failure_notes) < 3:
                    failure_notes.append(f"seed {seed}: empty stem or choice content")
            if (question.type != key or question.level != entry["level"]
                    or question.topic != spec.topic):
                metadata_failures += 1
                if len(failure_notes) < 3:
                    failure_notes.append(f"seed {seed}: generated identity/placement mismatch")

        failures = generation_failures + metadata_failures + distinct_choice_failures
        source = mapping[key]
        rows.append({
            "key": key,
            "subject": entry["subject"],
            "mapped_level": entry["level"],
            "legacy_level": entry["legacy_level"],
            "curriculum_topic": entry["unit"],
            "mapping_status": entry["mapping_status"],
            "sampled_items": seeds,
            "unique_stems": len(unique_stems),
            "min_choices": min(choice_counts, default=0),
            "max_choices": max(choice_counts, default=0),
            "generation_failures": generation_failures,
            "metadata_failures": metadata_failures,
            "distinct_choice_failures": distinct_choice_failures,
            "automated_status": "pass" if failures == 0 else "fail",
            "manual_review": (
                "complete" if key in REVIEWED_SCIENCE_STAGES
                else "required" if entry["mapping_status"] == "needs_review"
                else "pending"
            ),
            "review_note": source["review_note"],
            "failure_notes": " | ".join(failure_notes),
        })
    return rows


def validate(rows: list[dict], *, seeds: int) -> None:
    if (len(rows) != len(SCIENCE_BASELINE_KEYS)
            or {row["key"] for row in rows} != set(SCIENCE_BASELINE_KEYS)):
        raise ValueError("audit does not contain exactly the 95-key science baseline")
    failed = [row["key"] for row in rows if row["automated_status"] != "pass"]
    wrong_counts = [row["key"] for row in rows if row["sampled_items"] != seeds]
    if failed or wrong_counts:
        raise ValueError(f"science audit failed: failed={failed}, wrong_counts={wrong_counts}")


def write(rows: list[dict], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", type=int, default=200)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true",
                        help="run and validate the audit without writing the CSV")
    args = parser.parse_args()
    rows = audit(seeds=args.seeds)
    validate(rows, seeds=args.seeds)
    if not args.check:
        write(rows, args.output)
    print(
        f"Audited {len(rows)} science sets x {args.seeds} seeds; "
        f"automated failures: 0; manual review pending: "
        f"{sum(row['manual_review'] != 'complete' for row in rows)}"
    )


if __name__ == "__main__":
    main()
