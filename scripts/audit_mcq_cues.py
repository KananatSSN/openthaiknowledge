"""Audit every set for answer cues a student can use without the subject.

Per set, over ``--samples`` seeded draws:

- ``longest``   share of draws where the correct choice is visibly the longest
  (see :func:`stands_out`)
- ``shortest``  share where it is visibly the shortest
- ``rank_mode`` for numeric choices, share of the commonest sorted position of
  the correct value ("it is always the smallest")
- ``convergent`` share where the correct choice is uniquely the most similar to
  the others (each distractor changes one part of the answer)
- ``answers``   distinct correct answers seen, a memorisation signal

The tracker is docs/for_admin/MCQ_GUESSABILITY.md.

Examples::

    python -X utf8 scripts/audit_mcq_cues.py
    python -X utf8 scripts/audit_mcq_cues.py --samples 60 --csv docs/for_admin/mcq_cue_audit.csv
    python -X utf8 scripts/audit_mcq_cues.py --only math.polygon_sides --show 5
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from difflib import SequenceMatcher
from pathlib import Path
from random import Random

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# A cue is flagged when following it beats these rates. Chance is 1/n, so a
# length cue must also beat chance by CUE_MARGIN: in a two-choice set the
# shorter choice is right half the time with no cue at all.
LONGEST_LIMIT = 0.45
SHORTEST_LIMIT = 0.45
CUE_MARGIN = 0.20
RANK_LIMIT = 0.60
CONVERGENT_LIMIT = 0.60
MIN_NUMERIC = 20          # numeric draws needed before rank_mode is judged


def _unique_index(values, pick):
    best = pick(values)
    return values.index(best) if values.count(best) == 1 else None


def stands_out(sizes: list[int], answer: int) -> str:
    """``"longest"`` / ``"shortest"`` when the answer's length is visibly apart
    from every distractor's: by 10% of its length and at least 3 characters.
    A 119-against-121 difference is not a cue anyone can see."""
    from otk.core.distractors import _length_gap
    size = sizes[answer]
    others = sizes[:answer] + sizes[answer + 1:]
    gap = _length_gap(size)
    if others and size - max(others) >= gap:
        return "longest"
    if others and min(others) - size >= gap:
        return "shortest"
    return ""


def measure(key: str, samples: int) -> dict:
    from otk.core import generate
    from otk.core.distractors import _plain_number, visible_length
    from scripts.audit_answer_length import visible_text

    counts: Counter = Counter()
    ranks: Counter = Counter()
    answers: set[str] = set()
    for sample in range(samples):
        q = generate(key, rng=Random(7919 * sample + 17))
        texts = [visible_text(c.content) for c in q.choices]
        a = q.answer
        counts["n"] += 1
        counts["chance"] += 1 / len(q.choices)
        answers.add(texts[a])
        cue = stands_out([visible_length(c.content) for c in q.choices], a)
        counts["longest"] += cue == "longest"
        counts["shortest"] += cue == "shortest"
        if len(texts) > 2:
            similarity = [round(sum(SequenceMatcher(None, t, u).ratio()
                                    for j, u in enumerate(texts) if j != i), 6)
                          for i, t in enumerate(texts)]
            counts["convergent"] += _unique_index(similarity, max) == a
        numbers = [_plain_number(c.content) for c in q.choices]
        if (len(numbers) >= 3 and None not in numbers
                and len({v[0] for v in numbers}) == len(numbers)
                and len({v[3] for v in numbers}) == 1):
            order = sorted(range(len(numbers)), key=lambda i: numbers[i][0])
            ranks[order.index(a)] += 1
    n = counts["n"]
    numeric = sum(ranks.values())
    return {
        "key": key,
        "longest": counts["longest"] / n,
        "shortest": counts["shortest"] / n,
        "convergent": counts["convergent"] / n,
        "numeric": numeric,
        "rank_mode": max(ranks.values()) / numeric if numeric else 0.0,
        "answers": len(answers),
        "chance": counts["chance"] / n,
    }


def _measure(args):
    return measure(*args)


def flags(row: dict) -> list[str]:
    out = []
    bar = max(LONGEST_LIMIT, row.get("chance", 0.25) + CUE_MARGIN)
    if row["longest"] >= bar:
        out.append("longest")
    if row["shortest"] >= max(SHORTEST_LIMIT, row.get("chance", 0.25) + CUE_MARGIN):
        out.append("shortest")
    if row["numeric"] >= MIN_NUMERIC and row["rank_mode"] >= RANK_LIMIT:
        out.append("rank")
    if row["convergent"] >= CONVERGENT_LIMIT:
        out.append("convergent")
    return out


def show(key: str, count: int) -> None:
    from otk.core import generate
    from scripts.audit_answer_length import visible_text
    for sample in range(count):
        q = generate(key, rng=Random(7919 * sample + 17))
        print("Q:", visible_text(q.stem)[:160])
        for i, c in enumerate(q.choices):
            print("  ", "*" if i == q.answer else " ", visible_text(c.content)[:120])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--samples", type=int, default=60)
    parser.add_argument("--csv", help="write every set's measures here")
    parser.add_argument("--only", nargs="*", help="audit just these keys")
    parser.add_argument("--show", type=int, default=0, help="print N draws of each --only key")
    args = parser.parse_args()

    from otk.core import catalog
    rows = {r["key"]: r for r in catalog()}
    keys = args.only or list(rows)
    if args.show:
        for key in keys:
            print("=====", key)
            show(key, args.show)
        return
    with ProcessPoolExecutor() as pool:
        results = list(pool.map(_measure, [(k, args.samples) for k in keys], chunksize=8))

    by_flag: Counter = Counter()
    by_subject: Counter = Counter()
    for r in results:
        r["subject"] = rows[r["key"]]["subject"]
        r["level"] = rows[r["key"]]["level"]
        r["flags"] = " ".join(flags(r))
        for f in flags(r):
            by_flag[f] += 1
            by_subject[(f, r["subject"])] += 1
    print(f"Audited {len(results)} sets x {args.samples} draws")
    for f in ("longest", "shortest", "rank", "convergent"):
        subjects = {s: n for (g, s), n in by_subject.items() if g == f}
        print(f"  {f:11} {by_flag[f]:4}  {subjects}")
    if args.only:
        for r in results:
            print(f"  {r['key']}: longest {r['longest']:.2f} shortest {r['shortest']:.2f} "
                  f"rank {r['rank_mode']:.2f}/{r['numeric']} convergent {r['convergent']:.2f} "
                  f"answers {r['answers']} [{r['flags']}]")
    if args.csv:
        fields = ["key", "subject", "level", "flags", "longest", "shortest",
                  "rank_mode", "numeric", "convergent", "answers"]
        with open(args.csv, "w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
            writer.writeheader()
            for r in sorted(results, key=lambda r: (r["flags"] == "", r["subject"], r["key"])):
                writer.writerow({**r, **{k: f"{r[k]:.2f}" for k in
                                         ("longest", "shortest", "rank_mode", "convergent")}})


if __name__ == "__main__":
    main()
