"""Export sample questions from the สสวท. math enrichment for a teacher to review.

Three differently worded samples per set, with the answer and the choices, and
two empty columns for the reviewer. Open the CSV in a spreadsheet; mathematics
is written as TeX between square brackets, and a drawing is named by its asset
id (the PNG is in otk/pictures/).
"""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from random import Random

from otk.core import REGISTRY, generate
from otk.core.curriculum import placement_for
from otk.kit.math_problems import WordProblem

# Modules written for the enrichment, and the older modules whose word
# problems were given several situations.
ENRICHMENT = tuple(f".math_{m}" for m in (
    "p1", "p2", "p3", "p4", "p5", "p6", "m1", "m2", "m3", "m4", "m5", "m6",
    "diagrams", "diagrams_hi", "diagrams_geo", "chapters", "thin_topics"))
STORY_MODULES = (".math", ".math_geometry", ".math_number", ".math_data")
SAMPLES = 3

FIELDS = ("key", "ชั้น", "หัวข้อ", "ชื่อชุดโจทย์", "ตัวอย่างที่", "โจทย์", "รูป", "คำตอบ", "ตัวเลือก",
          "ภาษาถูกต้องและเป็นธรรมชาติ (ใช่/ไม่)", "ข้อเสนอแนะ")


def _in_scope(spec) -> bool:
    module = type(spec).__module__
    return (module.endswith(ENRICHMENT)
            or (module.endswith(STORY_MODULES) and isinstance(spec, WordProblem)))


def _block(b) -> str:
    if getattr(b, "kind", "") == "image":
        return ""
    return getattr(b, "text", None) or (f"[{b.tex}]" if getattr(b, "tex", "") else "")


def _samples(key: str):
    seen: set[str] = set()
    for seed in range(200):
        q = generate(key, Random(seed))
        stem = " ".join(filter(None, (_block(b) for b in q.stem)))
        shape = re.sub(r"\[.*?\]", "", re.sub(r"\d[\d,.]*", "#", stem))
        if shape in seen:
            continue
        seen.add(shape)
        yield q, stem
        if len(seen) == SAMPLES:
            return


def export(output: Path) -> int:
    rows = []
    for key, spec in REGISTRY.items():
        if not key.startswith("math.") or key.startswith("math.ipst.") or not _in_scope(spec):
            continue
        place = placement_for(key=spec.curriculum_key or key, subject=spec.subject,
                              level=spec.level_for(), topic=spec.topic)
        for n, (q, stem) in enumerate(_samples(key), 1):
            choices = [" ".join(filter(None, (_block(b) for b in c.content))) for c in q.choices]
            images = [b.asset_id for b in q.stem if getattr(b, "kind", "") == "image"]
            rows.append({
                "key": key, "ชั้น": place.level, "หัวข้อ": spec.topic,
                "ชื่อชุดโจทย์": spec.display_name.get("th", ""), "ตัวอย่างที่": n,
                "โจทย์": stem, "รูป": " ".join(images), "คำตอบ": choices[q.answer],
                "ตัวเลือก": " | ".join(choices),
            })
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    return len(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-o", "--output", type=Path,
                        default=Path("docs/for_admin/math_thai_review_sheet.csv"))
    args = parser.parse_args()
    count = export(args.output)
    print(f"Exported {count} sample questions to {args.output}")


if __name__ == "__main__":
    main()
