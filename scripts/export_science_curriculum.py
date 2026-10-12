"""Export and validate approved IPST placement of registered science sets."""

from __future__ import annotations

import argparse
import csv
import re
from collections import defaultdict
from pathlib import Path

from otk.core import REGISTRY, catalog
from otk.core.curriculum import ADDITIONAL, BASIC
from otk.core.curriculum_science import SCIENCE_KEYS


FIELDS = (
    "key", "display_name", "subject", "course_type", "level", "legacy_level",
    "strand_code", "strand", "standard_code", "indicator_codes", "unit", "topic",
    "mapping_status", "curriculum_node_id", "curriculum_version",
    "learning_stage", "learning_stage_key", "learning_stage_label", "source_key",
)
VALID_STATUSES = {
    "exact", "standard_scope", "additional_outcome", "outside_scope", "needs_review",
}
CORE_CODE = re.compile(r"^ว [1-4]\.\d [ปม]\.\d/\d+$")
ADDITIONAL_CODE = re.compile(r"^(?:เคมี|ฟิสิกส์|ชีววิทยา|โลก ดาราศาสตร์ และอวกาศ)เพิ่มเติม [1-6] ม\.[456]/\d+$")


def science_rows() -> list[dict]:
    return [row for row in catalog() if row["key"] in SCIENCE_KEYS]


def validate(rows: list[dict]) -> None:
    """Reject unknown keys, unstable IDs, collisions, and malformed curriculum codes."""
    keys = [row["key"] for row in rows]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate science keys in catalog export")
    unknown = set(keys) - set(REGISTRY)
    missing = set(SCIENCE_KEYS) - set(keys)
    if unknown or missing:
        raise ValueError(f"science key mismatch: unknown={sorted(unknown)}, missing={sorted(missing)}")

    nodes: dict[str, set[tuple]] = defaultdict(set)
    for row in rows:
        if row["mapping_status"] not in VALID_STATUSES:
            raise ValueError(f"invalid mapping status for {row['key']}: {row['mapping_status']}")
        node_id = row["curriculum_node_id"]
        if not node_id.startswith("th-sci-2560-"):
            raise ValueError(f"invalid science node ID for {row['key']}: {node_id}")
        nodes[node_id].add((
            row["course_type"], row["level"], row["strand_code"],
            row["standard_code"], row["unit"],
        ))
        matcher = CORE_CODE if row["course_type"] == BASIC else ADDITIONAL_CODE
        if row["course_type"] in {BASIC, ADDITIONAL}:
            if not row["indicator_codes"]:
                raise ValueError(f"missing curriculum outcome for {row['key']}")
            invalid = [code for code in row["indicator_codes"] if not matcher.fullmatch(code)]
            if invalid:
                raise ValueError(f"invalid curriculum outcome for {row['key']}: {invalid}")

    collisions = {node_id: values for node_id, values in nodes.items() if len(values) > 1}
    if collisions:
        raise ValueError(f"science node ID collisions: {collisions}")


def export(output: Path) -> int:
    rows = science_rows()
    validate(rows)
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
        default=Path("docs/for_admin/science_ipst_catalog.csv"),
    )
    parser.add_argument(
        "--check", action="store_true",
        help="validate the in-memory catalog without writing an export",
    )
    args = parser.parse_args()
    if args.check:
        rows = science_rows()
        validate(rows)
        print(f"Validated {len(rows)} science problem sets")
        return
    count = export(args.output)
    print(f"Exported {count} science problem sets to {args.output}")


if __name__ == "__main__":
    main()
