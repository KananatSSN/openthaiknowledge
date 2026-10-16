"""How much of each set's question wording also appears in its sources.

Evidence for the publication review (docs/for_admin/PUBLICATION_REVIEW.md): a
set that reproduces a copyrighted question's wording is a copy with new
numbers, whatever its provenance says. For each set, the stems of three draws
are cut into 12-character pieces (whitespace removed); pieces that more than
three sets share are dropped as stock phrasing ("จงหาค่าของ…"); the score is
the share of the remaining pieces found in the source text.

Sources compared:

* a digested paper's set → its item's original text (``sheet.json`` ``source``);
* a module that cites ``openthaiknowledge-bank/<folder>`` → that folder's digests;
* every other set → all digests and transcripts (should be near zero).

    python scripts/source_overlap.py               # summary per family
    python scripts/source_overlap.py --sets 0.5    # also list sets scoring >= 0.5

Needs ``openthaiknowledge-bank/_digest`` and ``_transcribed`` (in this repository).
Scores are a screening signal for a human reviewer, not a legal test.
"""

from __future__ import annotations

import argparse
import collections
import json
import re
from pathlib import Path
from random import Random

from otk.api import REGISTRY, provenance
from otk.sheets import SHEETS_DIR

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "openthaiknowledge-bank"
PIECE = 12
SEEDS = (1, 2, 3)
STOCK = 3          # pieces shared by more sets than this are stock phrasing
MIN_PIECES = 15    # stems shorter than this (after dropping stock) are not scored


def _pieces(text: str) -> set[int]:
    flat = re.sub(r"\s+", "", text)
    return {hash(flat[i:i + PIECE]) for i in range(max(0, len(flat) - PIECE + 1))}


def _corpus(paths) -> set[int]:
    out: set[int] = set()
    for path in paths:
        out |= _pieces(path.read_text(encoding="utf-8", errors="ignore"))
    return out


def _stems(key: str) -> list[str]:
    return ["".join(b.text for b in REGISTRY[key].generate(Random(seed)).stem
                    if getattr(b, "kind", "") == "text") for seed in SEEDS]


def scores() -> list[dict]:
    stems = {key: _stems(key) for key in REGISTRY}
    shared = collections.Counter()
    for texts in stems.values():
        shared.update(set().union(*map(_pieces, texts)))

    paper_text = {}
    for sheet in sorted(SHEETS_DIR.iterdir()):
        meta = sheet / "sheet.json"
        if meta.exists():
            for item in json.loads(meta.read_text("utf-8"))["items"]:
                if item.get("generator"):
                    paper_text[item["generator"]] = (sheet.name, item.get("source", ""))

    everything = _corpus([*(BANK / "_digest").rglob("*.md"), *(BANK / "_transcribed").rglob("*.*")])
    folders: dict[tuple, set[int]] = {}
    rows = []
    for key, texts in stems.items():
        origin = provenance(key)
        if key in paper_text:
            family, source = f"paper {paper_text[key][0]}", _pieces(paper_text[key][1])
        elif origin.kind == "adapted":
            family = f"module {type(REGISTRY[key]).__module__.rsplit('.', 1)[-1]}"
            cited = origin.sources
            if cited not in folders:
                folders[cited] = _corpus(p for c in cited
                                         for p in (BANK / "_digest" / c.removeprefix("openthaiknowledge-bank/")).rglob("*.md"))
            source = folders[cited]
        else:
            family, source = "original", everything
        best, scored = 0.0, False
        for text in texts:
            mine = {p for p in _pieces(text) if shared[p] <= STOCK}
            if len(mine) >= MIN_PIECES:
                scored = True
                best = max(best, len(mine & source) / len(mine))
        rows.append({"key": key, "family": family, "score": round(best, 2),
                     "scored": scored, "source_text": bool(source)})
    return rows


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--sets", type=float, metavar="MIN", help="list sets scoring at least MIN")
    args = parser.parse_args(argv)
    rows = scores()
    families = collections.defaultdict(list)
    for row in rows:
        families[row["family"]].append(row)
    print(f"{'family':40} {'sets':>5} {'scored':>6} {'median':>6} {'>=0.5':>5}")
    for family, members in sorted(families.items()):
        values = sorted(r["score"] for r in members if r["scored"])
        median = f"{values[len(values) // 2]:.2f}" if values else "-"
        note = "" if any(r["source_text"] for r in members) else "  (no source text)"
        print(f"{family:40} {len(members):5} {len(values):6} {median:>6} "
              f"{sum(v >= .5 for v in values):5}{note}")
    if args.sets is not None:
        for row in sorted(rows, key=lambda r: -r["score"]):
            if row["score"] >= args.sets:
                print(f"{row['score']:.2f}  {row['family']:30} {row['key']}")


if __name__ == "__main__":
    main()
