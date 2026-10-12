"""List the bank rows behind a set's ``longest`` / ``shortest`` flag.

Draws each set many times and prints every distinct item whose correct
choice is uniquely the longest (or shortest), with the choices, so the row
can be found in the source by its correct text and rewritten.

    python -X utf8 scripts/list_length_leaks.py --keys geo.drift_evidence_fluency
    python -X utf8 scripts/list_length_leaks.py --flagged docs/for_admin/mcq_cue_audit.csv --summary
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path
from random import Random

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from otk.core import generate  # noqa: E402
from otk.core.distractors import visible_length  # noqa: E402
from scripts.audit_answer_length import visible_text  # noqa: E402
from scripts.audit_mcq_cues import stands_out  # noqa: E402


def leaks(key: str, draws: int = 200) -> dict[str, tuple]:
    """Distinct leaking items: correct text -> (stem, choices, kind)."""
    out: dict[str, tuple] = {}
    for seed in range(draws):
        q = generate(key, Random(seed))
        sizes = [visible_length(c.content) for c in q.choices]
        a = q.answer
        kind = stands_out(sizes, a)
        if kind:
            texts = [visible_text(c.content) for c in q.choices]
            out.setdefault(texts[a], (visible_text(q.stem), texts, kind, sizes))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--keys", nargs="*", default=[])
    parser.add_argument("--flagged", help="audit CSV; take every longest/shortest-flagged set")
    parser.add_argument("--summary", action="store_true", help="counts only")
    parser.add_argument("--draws", type=int, default=200)
    args = parser.parse_args()
    keys = list(args.keys)
    if args.flagged:
        with open(args.flagged, encoding="utf-8") as handle:
            keys += [r["key"] for r in csv.DictReader(handle)
                     if {"longest", "shortest"} & set(r["flags"].split())]
    total = 0
    for key in keys:
        found = leaks(key, args.draws)
        total += len(found)
        if args.summary:
            print(f"{len(found):4}  {key}")
            continue
        print(f"===== {key}  ({len(found)} leaking items)")
        for correct, (stem, texts, kind, sizes) in found.items():
            print(f"  [{kind}] {stem[:150]}")
            for t, n in zip(texts, sizes):
                print(f"    {'*' if t == correct else ' '} {n:3} {t}")
    print(f"total leaking items: {total} across {len(keys)} sets")


if __name__ == "__main__":
    main()
