"""Index every official indicator and learning outcome in the IPST 2560 books.

The books print indicators in a three-column table — ชั้น | ตัวชี้วัด (or
ผลการเรียนรู้) | สาระการเรียนรู้ — under a standard or learning-area heading,
and never print the full code. This script splits each text line into those
columns by x position, tracks the heading, grade and item number, and writes
one JSON object per indicator to docs/curriculum_sources/_md/indicators.jsonl:

    {"code": "ว 1.1 ป.1/1", "subject": "science", "kind": "core",
     "standard": "ว 1.1", "level": "ป.1", "number": 1,
     "text": "ระบุชื่อพืชและ...", "source": "_ทั่วไป/...pdf", "page": 20}

Codes use Arabic digits, as the repo does; ``page`` is the PDF page.

    python scripts/curriculum_index.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

import pymupdf

sys.path.insert(0, str(Path(__file__).resolve().parent))
from curriculum_sources_to_md import (  # noqa: E402
    OUT, SOURCES, GlyphFixer, repair, symbol_chars,
)

BOOKS = (
    ("science", "_ทั่วไป/ตัวชี้วัดและสาระการเรียนรู้แกนกลาง_วิทยาศาสตร์_2560.pdf"),
    ("math", "คณิตศาสตร์_ประถมศึกษา/ตัวชี้วัดและสาระการเรียนรู้แกนกลาง_คณิตศาสตร์_2560.pdf"),
)
THAI_DIGITS = str.maketrans("๐๑๒๓๔๕๖๗๘๙", "0123456789")
GRADE = re.compile(r"^\s*([ปม])\s*\.\s*([๑-๖1-6])(?:\s*[-–]\s*([๑-๖1-6]))?\s*(?:\(ต่อ\))?\s*$")
ITEM = re.compile(r"^\s*([๐-๙0-9]{1,2})\s*\.\s*(?=\S)")
STANDARD = re.compile(r"มาตรฐาน\s+([วค])\s*([๑-๙1-9])\s*\.\s*([๑-๙1-9])")
ADD_SUBJECT = re.compile(r"^\s*สาระ(ชีววิทยา|เคมี|ฟิสิกส์|โลก ดาราศาสตร์ และอวกาศ)\s*$")
ADD_GROUP = re.compile(r"^\s*([๑-๙1-9])\s*\.\s+\S")
ADD_COURSE = {
    "ชีววิทยา": "ชีววิทยาเพิ่มเติม", "เคมี": "เคมีเพิ่มเติม",
    "ฟิสิกส์": "ฟิสิกส์เพิ่มเติม",
    "โลก ดาราศาสตร์ และอวกาศ": "โลก ดาราศาสตร์ และอวกาศเพิ่มเติม",
}
MATH_ADD = re.compile(r"^\s*สาระ(จำนวนและพีชคณิต|การวัดและเรขาคณิต|สถิติและความน่าจะเป็น|แคลคูลัส)\s*$")
# Formulas set as fractions, vectors or subscripts do not survive text
# extraction. Each fix was checked against the rendered PDF page.
FORMULA_FIXES = {
    "ว 2.2 ม.2/14": ("v = s t และ v = s t", "v = s/t และ v⃗ = s⃗/t"),
    "ว 2.3 ม.1/1": ("เปลี่ยนสถานะ Q = mc∆t Q = mL โดยใช้สมการ และ",
                    "เปลี่ยนสถานะ โดยใช้สมการ Q = mcΔt และ Q = mL"),
    "ว 2.3 ม.2/1": ("P = W t", "P = W/t"),
    "ว 3.1 ม.3/1": ("F = (Gm1m2)/r2", "F = (Gm₁m₂)/r²"),
    "ชีววิทยาเพิ่มเติม 2 ม.4/2": ("F1 และ F2", "F₁ และ F₂"),
}
INDICATOR_HEAD = ("ตัวชี้วัด", "ผลการเรียนรู้")
CONTENT_HEAD = ("สาระการเรียนรู้แกนกลาง", "สาระการเรียนรู้เพิ่มเติม")


def arabic(s: str) -> str:
    return s.translate(THAI_DIGITS)


@dataclass
class Indicator:
    code: str
    subject: str
    kind: str
    standard: str
    level: str
    number: int
    text: str
    official_code: bool
    formula_fix: str | None
    source: str
    page: int
    lines: list[str] = field(default_factory=list, repr=False)


def page_lines(page: pymupdf.Page, fixer: GlyphFixer, doc_id: str):
    """Yield (x0, y0, text-with-positions) per line: a list of (x, char)."""
    by_pos = fixer.page_map(page, doc_id)
    raw = page.get_text("rawdict", flags=pymupdf.TEXTFLAGS_TEXT)
    for block in raw["blocks"]:
        for line in block.get("lines", ()):
            chars = []
            size = max((sp["size"] for sp in line["spans"] if sp["chars"]), default=0)
            for span in line["spans"]:
                sym = "symbol" in span["font"].lower()
                for ch in span["chars"]:
                    c = fixer.fix(by_pos, ch)
                    if sym or 0xF020 <= ord(c) <= 0xF0FF:
                        c = symbol_chars(c)
                    chars.append((ch["bbox"][0], c))
            if chars:
                yield line["bbox"], chars, size


def text_of(chars) -> str:
    return repair("".join(c for _, c in chars))


def book_columns(doc: pymupdf.Document) -> list[float]:
    """Left edges of the ชั้น, indicator and content columns.

    The layout is fixed within a book, so take the most common edges among
    the tables that look like indicator tables; find_tables misses some pages
    and sees the page frame as a table on others.
    """
    seen: Counter = Counter()
    for page in doc:
        for t in page.find_tables().tables:
            xs = sorted({round(c[0]) for c in t.cells if c})[:3]
            if (t.col_count >= 3 and len(xs) == 3 and xs[0] > 30
                    and xs[1] - xs[0] >= 20 and xs[2] - xs[1] >= 100):
                seen[tuple(xs)] += 1
    return list(seen.most_common(1)[0][0])


RUNNING = re.compile(r"^(ตัวชี้วัดและสาระการเรียนรู้แกนกลาง กลุ่มสาระ|ตามหลักสูตรแกนกลาง|[0-9๐-๙]+$)")


def split(chars, xs):
    cols: list[list] = [[], [], []]
    for x, c in chars:
        i = 2 if x >= xs[2] - 2 else 1 if x >= xs[1] - 2 else 0
        cols[i].append((x, c))
    return tuple(text_of(col) for col in cols)


def join(lines: list[str]) -> str:
    """Join wrapped lines. Thai wraps between words without a space, so a line
    break becomes a space only where the line itself ended with one."""
    out = ""
    for ln in lines:
        if out and not out.endswith(" ") and not ln.startswith(" "):
            thai_break = re.search(r"[฀-๿]$", out) and re.match(r"[฀-๿]", ln)
            out += "" if thai_break else " "
        out += ln
    return re.sub(r"\s+", " ", out).strip()


def build(subject: str, rel: str, fixer: GlyphFixer) -> list[Indicator]:
    path = SOURCES / rel
    doc = pymupdf.open(path)
    found: list[Indicator] = []
    standard = kind = course = group = level = None
    current: Indicator | None = None

    def close():
        nonlocal current
        if current is not None:
            current.text = join(current.lines)
            fix = FORMULA_FIXES.get(current.code)
            if fix:
                if fix[0] not in current.text:
                    raise SystemExit(f"{current.code}: formula fix no longer matches: {current.text}")
                current.text = current.text.replace(*fix)
                current.formula_fix = "checked against the page image"
            found.append(current)
        current = None

    xs = book_columns(doc)
    for pno, page in enumerate(doc, 1):
        events = []
        for bbox, chars, size in page_lines(page, fixer, path.name):
            g, ind, _content = split(chars, xs)
            # A grade token leads any item that starts on the same row.
            lead = GRADE.match(g) is not None
            events.append((bbox[1] - (4 if lead else 0), bbox, chars, g, ind, size))
        sizes = sorted(e[5] for e in events)
        body = sizes[len(sizes) // 2] if sizes else 0
        events.sort(key=lambda e: (e[0], e[1][0]))
        for _, bbox, chars, g, ind, size in events:
            full = text_of(chars)
            stripped = full.strip()
            if not stripped or RUNNING.match(stripped):
                continue
            m = STANDARD.search(full)
            if m and bbox[0] < xs[1]:
                close()
                standard = f"{m.group(1)} {arabic(m.group(2))}.{arabic(m.group(3))}"
                kind, level = "core", None
                continue
            m = ADD_SUBJECT.match(full)
            if m:
                close()
                course, kind, group, level = ADD_COURSE[m.group(1)], "additional", None, None
                continue
            m = MATH_ADD.match(full)
            if m and subject == "math":
                close()
                course, kind, group, level = f"ค เพิ่มเติม {m.group(1)}", "additional", None, None
                continue
            m = ADD_GROUP.match(full)
            # A learning-area heading starts in the grade column (maths) or
            # runs across the content column (science); items do neither.
            if kind == "additional" and m and (bbox[0] < xs[1] - 2 or (
                    bbox[2] > xs[2] + 50 and bbox[0] > xs[1] + 15)):
                close()
                group, level = arabic(m.group(1)), None
                continue
            if kind is None or stripped in ("ชั้น", *INDICATOR_HEAD, *CONTENT_HEAD):
                continue
            gm = GRADE.match(g)
            if gm:
                close()
                level = f"{gm.group(1)}.{arabic(gm.group(2))}"
                if gm.group(3):
                    level += f"-{arabic(gm.group(3))}"
            elif g.strip():
                # Prose running from the first column into the second ends
                # the table; stray glyphs and footers do not.
                if (len(re.findall("[ก-ฮ]", g)) >= 3 and ind.strip()
                        and bbox[1] < 0.8 * page.rect.height):
                    close()
                    level = None
                continue
            if not ind.strip() or level is None:
                continue
            if size > 1.25 * body or (bbox[0] > xs[1] + 15 and bbox[2] > xs[2] + 30):
                # A heading or paragraph across both columns: the table ended.
                close()
                level = None
                continue
            im = ITEM.match(ind)
            if im:
                close()
                n = int(arabic(im.group(1)))
                lv = level.split("-")[0]
                std = standard if kind == "core" else f"{course} {group}"
                # The maths book prints no codes for its additional course;
                # its codes here follow the science pattern and are ours.
                code, official = f"{std} {lv}/{n}", not std.startswith("ค เพิ่มเติม")
                current = Indicator(
                    code=code, subject=subject, kind=kind, standard=std,
                    level=level, number=n, text="", official_code=official, formula_fix=None,
                    source=rel, page=pno, lines=[ind[im.end():]],
                )
            elif current is not None and ind.strip() not in ("-", "–"):
                current.lines.append(ind)
    close()
    return found


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    fixer = GlyphFixer()
    rows: list[Indicator] = []
    for subject, rel in BOOKS:
        got = build(subject, rel, fixer)
        print(f"{subject}: {len(got)} indicators from {rel}")
        rows += got
    dest = OUT / "indicators.jsonl"
    # Rows other readers wrote (scripts/geography_indicators.py) stay as they are.
    built = {subject for subject, _ in BOOKS}
    others = [ln for ln in dest.read_text("utf-8").splitlines()
              if ln.strip() and json.loads(ln)["subject"] not in built] if dest.exists() else []
    with dest.open("w", encoding="utf-8", newline="\n") as fh:
        for r in rows:
            d = asdict(r)
            d.pop("lines")
            fh.write(json.dumps(d, ensure_ascii=False) + "\n")
        for ln in others:
            fh.write(ln + "\n")
    dupes = {r.code for r in rows if sum(x.code == r.code for x in rows) > 1}
    if dupes:
        print("duplicate codes:", sorted(dupes)[:20])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
