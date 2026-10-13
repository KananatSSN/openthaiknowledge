"""Index the geography (ส 5) indicators of the 2560 standards book.

``scripts/curriculum_index.py`` reads the science and maths books, which print
indicators in a ชั้น | ตัวชี้วัด | สาระ table. The geography pages print one
column per grade instead, so they get this reader of the tracked Markdown copy
of that book (``_ทั่วไป/มาตรฐานการเรียนรู้และตัวชี้วัด_คณิต_วิทย์_ภูมิศาสตร์_2560.md``).

In that copy the columns come out one after another, ป.1 first, each item
starting "๑.", "๒.", … and the numbering restarting at the next grade. The
grades and their item counts are fixed below from the printed pages, and the
reader fails if the text does not split into exactly those counts.

Rewrites the ``"subject": "geography"`` rows of
``docs/curriculum_sources/_md/indicators.jsonl`` and leaves the rest alone.

    python scripts/geography_indicators.py
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

MD = Path(__file__).resolve().parents[1] / "docs/curriculum_sources/_md"
REL = "_ทั่วไป/มาตรฐานการเรียนรู้และตัวชี้วัด_คณิต_วิทย์_ภูมิศาสตร์_2560"
INDEX = MD / "indicators.jsonl"
GRADES = ("ป.1", "ป.2", "ป.3", "ป.4", "ป.5", "ป.6", "ม.1", "ม.2", "ม.3", "ม.4-6")
# Items per grade, counted on the printed pages (book pages 89-92).
COUNTS = {
    "ส 5.1": (4, 3, 2, 3, 2, 2, 3, 3, 2, 3),
    "ส 5.2": (3, 4, 6, 3, 3, 3, 4, 4, 5, 4),
}
THAI_DIGITS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")
ITEM = re.compile(r"^\s*([๑-๙])\s*\.\s*(\S.*)$")
PAGE = re.compile(r"<!-- page (\d+) -->")
# Lines that are page furniture or headings, never part of an indicator.
FURNITURE = re.compile(
    r"^(สาระที่|มาตรฐาน|ตัวชี้วัด|[ปม]\. ?[๑-๖]|\d+$|\(ต่อ\)|<!--|#)")


def join(lines: list[str]) -> str:
    """Thai wraps between words with no space, so a Thai-to-Thai break joins tight."""
    out = ""
    for ln in (x.strip() for x in lines):
        tight = re.search(r"[฀-๿]$", out) and not out.endswith("ๆ") and re.match(r"[฀-๿]", ln)
        if out and not tight:
            out += " "
        out += ln
    return re.sub(r"\s+", " ", out).strip()


def read() -> list[dict]:
    lines = (MD / f"{REL}.md").read_text("utf-8").splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith("### สาระภูมิศาสตร์"))
    page = 0
    for ln in lines[:start]:
        if m := PAGE.search(ln):
            page = int(m.group(1))
    rows: list[dict] = []
    order = [(std, grade, n) for std, counts in COUNTS.items()
             for grade, count in zip(GRADES, counts) for n in range(1, count + 1)]
    current: dict | None = None
    started = False
    for ln in lines[start:]:
        if m := PAGE.search(ln):
            page = int(m.group(1))
        stripped = ln.strip()
        if stripped.startswith("ตัวชี้วัดชั้นปี"):
            started = True
        if not started or not stripped:
            continue
        if m := ITEM.match(ln):
            if len(rows) == len(order):
                break
            std, grade, n = order[len(rows)]
            got = int(m.group(1).translate(THAI_DIGITS))
            if got != n:
                raise SystemExit(f"{std} {grade}: expected item {n}, read {got}: {stripped}")
            current = {"code": f"{std} {grade}/{n}", "subject": "geography", "kind": "core",
                       "standard": std, "level": grade, "number": n, "lines": [m.group(2)],
                       "official_code": True, "formula_fix": None,
                       "source": f"{REL}.pdf", "page": page}
            rows.append(current)
        elif FURNITURE.match(stripped):
            # A heading ends the item before it, and what follows it (a
            # standard's wrapped lines) belongs to no item until the next "๑.".
            current = None
        elif current is not None:
            current["lines"].append(stripped)
    if len(rows) != len(order):
        raise SystemExit(f"read {len(rows)} indicators, expected {len(order)}")
    out = []
    for row in rows:
        text = join(row.pop("lines"))
        out.append({"code": row["code"], "subject": row["subject"], "kind": row["kind"],
                    "standard": row["standard"], "level": row["level"], "number": row["number"],
                    "text": text, "official_code": row["official_code"],
                    "formula_fix": row["formula_fix"], "source": row["source"], "page": row["page"]})
    return out


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    rows = read()
    kept = [ln for ln in INDEX.read_text("utf-8").splitlines()
            if ln.strip() and json.loads(ln)["subject"] != "geography"]
    with INDEX.open("w", encoding="utf-8", newline="\n") as fh:
        for ln in kept:
            fh.write(ln + "\n")
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"geography: {len(rows)} indicators")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
