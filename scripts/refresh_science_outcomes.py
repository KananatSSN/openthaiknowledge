"""Rewrite the outcome matrix's coverage columns from the approved placements.

``current_set_keys``, ``current_set_count`` and ``coverage_state`` are derived
facts: they say which registered sets claim an outcome and whether those sets
carry it through all three learning stages. Deriving them here keeps them from
drifting away from ``curriculum_science.py`` as each slice lands. Everything
else in the file — the official text, its page, the wave it belongs to — is
reviewed by hand and is left untouched.
"""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path

from otk.core import catalog


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_FILE = ROOT / "docs/for_admin/science_ipst_outcomes.csv"
DERIVED = ("current_set_keys", "current_set_count", "coverage_state")


def coverage() -> dict[str, tuple[set[str], set[int]]]:
    """Keys and learning stages claiming each outcome code."""
    found: dict[str, tuple[set[str], set[int]]] = defaultdict(
        lambda: (set(), set()))
    for row in catalog():
        for code in row["indicator_codes"] or ():
            keys, stages = found[code]
            keys.add(row["key"])
            stages.add(row["learning_stage"])
    return found


def state(keys: set[str], stages: set[int]) -> str:
    if not keys:
        return "missing"
    # An outcome is only complete once a learner can go Foundation → Fluency →
    # Application on it. Sets alone are not coverage.
    return "complete" if stages == {1, 2, 3} else "partial"


def refresh(path: Path, *, check: bool) -> int:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fields = list(reader.fieldnames or ())
        rows = list(reader)
    found = coverage()
    changed = 0
    for row in rows:
        keys, stages = found.get(row["outcome_code"], (set(), set()))
        updated = {
            "current_set_keys": "; ".join(sorted(keys)),
            "current_set_count": str(len(keys)),
            "coverage_state": state(keys, stages),
        }
        if any(row[field] != updated[field] for field in DERIVED):
            changed += 1
            print(f"{row['outcome_code']}: {row['coverage_state']} -> "
                  f"{updated['coverage_state']} ({len(keys)} sets)")
        row.update(updated)
    if not check:
        with path.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file", type=Path, default=DEFAULT_FILE)
    parser.add_argument("--check", action="store_true",
                        help="report drift without rewriting the file")
    args = parser.parse_args()
    changed = refresh(args.file, check=args.check)
    print(f"{changed} outcome row(s) {'drifted' if args.check else 'refreshed'}")
    return 1 if args.check and changed else 0


if __name__ == "__main__":
    raise SystemExit(main())
