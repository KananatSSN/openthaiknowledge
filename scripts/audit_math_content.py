"""Sample every math problem set and export variety and learning-curve evidence.

Each set is drawn ``--samples`` times from a fixed seed. A *shape* is a stem
with its numbers, Thai number words, and the shared story names and colours
masked, so two items that differ only in their numbers or in who is buying
share a shape. ``distinct_items`` counts whole items (stem and choices), which
exposes small finite banks. The rest are proxies for difficulty and support:
stem length, the median of the largest number in the stem, picture use and
hints. It is evidence for a human review, not a verdict.

    python -X utf8 scripts/audit_math_content.py
"""

from __future__ import annotations

import argparse
import csv
import re
import statistics
from collections import Counter
from pathlib import Path
from random import Random

from otk.core import catalog, generate
from otk.kit import story

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "docs/for_admin/math_content_audit.csv"
FIELDS = (
    "key", "display_name", "course_type", "level", "topic", "learning_stage",
    "mapping_status", "shapes", "top_shape_share", "distinct_items", "choices",
    "stem_chars", "max_number_median", "picture_share", "hint_share",
    "context", "example_shape",
)
# A thousands separator is "," in text and "{,}" in TeX: 45{,}327 is one number.
NUMBER = re.compile(r"[0-9๐-๙]+(?:(?:[.,]|\{,\})[0-9๐-๙]+)*")
NUMBER_WORDS = re.compile("(?:ศูนย์|หนึ่ง|เอ็ด|ยี่|สอง|สาม|สี่|ห้า|หก|เจ็ด|แปด|เก้า|สิบ|ร้อย|พัน|หมื่น|แสน|ล้าน)+")
THAI_DIGITS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")


def _words(values) -> set[str]:
    out: set[str] = set()
    for value in values:
        if isinstance(value, str):
            out.add(value)
        elif isinstance(value, (tuple, list)):
            out |= _words(value)
    return out


_NAMES = sorted(_words(story.NAMES) | _words(story.GIVERS) | _words(story.COLOURS),
                key=len, reverse=True)
NAME = re.compile("|".join(map(re.escape, _NAMES)))


def text_of(blocks: list[dict], assets: bool = False) -> str:
    """Blocks as text; ``assets`` names each picture, so two items that differ
    only in their figure count as two items."""
    parts = []
    for block in blocks:
        kind = block.get("kind")
        if kind == "text":
            parts.append(block.get("text", ""))
        elif kind == "math":
            parts.append(f"${block.get('tex', '')}$")
        elif assets and block.get("asset_id"):
            parts.append(f"[{kind}:{block['asset_id']}]")
        else:
            parts.append(f"[{kind}]")
    return " ".join(parts)


def shape(stem: str) -> str:
    stem = NAME.sub("@", NUMBER.sub("#", stem))
    return re.sub(r"\s+", " ", NUMBER_WORDS.sub("~", stem)).strip()


def largest_number(stem: str) -> float | None:
    values = []
    for match in NUMBER.finditer(stem.translate(THAI_DIGITS)):
        try:
            values.append(abs(float(match.group().replace("{,}", "").replace(",", ""))))
        except ValueError:
            pass
    return max(values) if values else None


def audit(row: dict, samples: int) -> dict:
    rng = Random(20260925)
    shapes: Counter = Counter()
    items, choices, lengths, largest = set(), Counter(), [], []
    pictures = hints = 0
    for _ in range(samples):
        question = generate(row["key"], rng=rng).model_dump(mode="json")
        stem = text_of(question["stem"])
        options = [text_of(choice["content"]) for choice in question["choices"]]
        shapes[shape(stem)] += 1
        items.add(text_of(question["stem"], assets=True) + "||" + "|".join(sorted(options)))
        choices[len(options)] += 1
        lengths.append(len(stem))
        if (value := largest_number(stem)) is not None:
            largest.append(value)
        pictures += any(b.get("kind") not in ("text", "math") for b in question["stem"])
        hints += bool(question.get("hint"))
    example = shapes.most_common(1)[0][0]
    return {
        **{field: row[field] for field in (
            "key", "display_name", "course_type", "level", "topic",
            "learning_stage", "mapping_status")},
        "shapes": len(shapes),
        "top_shape_share": round(shapes.most_common(1)[0][1] / samples, 2),
        "distinct_items": len(items),
        "choices": "/".join(str(n) for n in sorted(choices)),
        "stem_chars": round(statistics.mean(lengths)),
        "max_number_median": statistics.median(largest) if largest else "",
        "picture_share": round(pictures / samples, 2),
        "hint_share": round(hints / samples, 2),
        # A stem with a sentence of Thai around its numbers is set in a situation.
        "context": len(re.findall(r"[ก-ฮ]", example)) >= 25,
        "example_shape": example[:200],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=300)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    rows = [row for row in catalog() if row["subject"] == "คณิตศาสตร์"]
    with args.output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(audit(row, args.samples))
    print(f"Audited {len(rows)} math sets into {args.output}")


if __name__ == "__main__":
    main()
