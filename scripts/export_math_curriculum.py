"""Export the reviewable IPST placement of every registered math problem set."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from otk.core import catalog


FIELDS = (
    "key", "display_name", "course_type", "level", "legacy_level", "strand_code",
    "strand", "standard_code", "indicator_codes", "unit", "topic",
    "mapping_status", "curriculum_node_id", "curriculum_version",
    "learning_stage", "learning_stage_key", "learning_stage_label", "source_key",
)


def export(output: Path) -> int:
    rows = [row for row in catalog() if row["subject"] == "คณิตศาสตร์"]
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            exported = dict(row)
            exported["indicator_codes"] = "; ".join(row["indicator_codes"])
            writer.writerow(exported)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o", "--output", type=Path,
        default=Path("docs/for_admin/math_ipst_mapping.csv"),
    )
    args = parser.parse_args()
    count = export(args.output)
    print(f"Exported {count} math problem sets to {args.output}")


if __name__ == "__main__":
    main()
