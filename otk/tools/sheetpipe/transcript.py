"""Sheets read by eye: a hand transcript in, digest items out.

The ``(สสวท)`` textbook files and the scans in the bank print their maths as
pictures. Neither the text layer nor OCR recovers it, so a person (or a model
in a session) reads the rendered pages and writes a transcript to
``sheet_database/_transcribed/<bank path>.md``. ``convert`` prefers a
transcript to any splitter, needs no PDF to do so, and marks the digest
``"transcribed": true``.

The format, one line per thing::

    # แบบฝึกหัด 3.3                      a section title: numbering restarts under it
    > จงหาเซตคำตอบของอสมการต่อไปนี้        a lead, put in front of every item of the section
    @p2                                  the page the following items are on
    1. ให้ p(x) = 3x⁴ + 2x² − ax + 3 ...  an item; [O-NET 61/3] at the end is its tag
       จงหา a, b และ c                    an indented line continues the stem
       = a = 5, b = 3, c = 0              the answer of the item above
    2. ให้ p(x) = x² − 1 จงหา
       1) p(x) + q(x)                     a sub-item, numbered k)
          = 2x² − 2x + 2                  the answer of the sub-item
       (1) 5   (2) 6                       choices (one per line or several)
    {figure}                             anywhere in a stem: the item has a picture

Each sub-item becomes its own question, with the parent's stem in front and
``section`` ``"<title> <n>.<k>"`` (an item without subs gets ``"<title> <n>"``).
That is the answer-key splitter's convention, so a knowledge unit can name a
whole section as its source.

Maths is written in plain Unicode: ``x²``, ``√(x+1)``, ``π``, ``−``, and
fractions as ``a/b`` with brackets where they are needed.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from . import bank as bk
from .choiceblock import Item

ROOT = bk.DEFAULT_ROOT / "_transcribed"

TITLE = re.compile(r"^#\s+(.+?)\s*$")
LEAD = re.compile(r"^>\s*(.*)$")
PAGE = re.compile(r"^@p(\d+)\s*$")
ITEM = re.compile(r"^(\d{1,3})\.\s+(.*)$")
SUB = re.compile(r"^(\d{1,2})\)\s+(.*)$")
ANSWER = re.compile(r"^=\s*(.*)$")
CHOICE = re.compile(r"\((\d)\)\s*(.*?)(?=\s+\(\d\)\s|$)")
TAG = re.compile(r"[ \t]*\[([^\]\n]*(?:[ก-๙]|[A-Z]{2})[^\]\n]*)\][ \t]*$", re.MULTILINE)
FIGURE = "{figure}"


def path_for(bank_path: str) -> Path:
    return (ROOT / bank_path).with_suffix(".md")


@dataclass
class _Node:
    number: int
    lines: list[str] = field(default_factory=list)
    answer: list[str] = field(default_factory=list)
    choices: dict[int, str] = field(default_factory=dict)
    page: int = 0
    subs: list["_Node"] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "\n".join(self.lines)


class TranscriptError(ValueError):
    pass


def parse(text: str) -> list[Item]:
    """Transcript text → digest items, in order."""
    sections: list[tuple[str, list[_Node], list[str]]] = [("", [], [])]
    page = 0
    item: _Node | None = None
    node: _Node | None = None             # the item or sub-item lines now belong to
    for n, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("<!--"):
            continue
        indented = raw[:1].isspace()
        if (m := TITLE.match(line)) and not indented:
            sections.append((m.group(1), [], []))
            item = node = None
        elif (m := LEAD.match(line)) and not indented and item is None:
            sections[-1][2].append(m.group(1))
        elif m := PAGE.match(line):
            page = int(m.group(1))
        elif (m := ITEM.match(line)) and not indented:
            item = node = _Node(int(m.group(1)), [m.group(2)], page=page)
            sections[-1][1].append(item)
        elif node is None:
            raise TranscriptError(f"line {n}: text before the first item: {line!r}")
        elif m := ANSWER.match(line):
            node.answer.append(m.group(1))
        elif line.startswith("(") and CHOICE.match(line):
            for k, v in CHOICE.findall(line):
                node.choices[int(k)] = v.strip()
        elif (m := SUB.match(line)) and item is not None:
            node = _Node(int(m.group(1)), [m.group(2)], page=page)
            item.subs.append(node)
        else:
            node.lines.append(line)
    return _items(sections)


def _item(number: int, stem: str, node: _Node, section: str, page: int) -> Item:
    tag = ""
    if m := TAG.search(stem):
        tag, stem = m.group(1).strip(), stem[:m.start()] + stem[m.end():]
    figure = FIGURE in stem
    stem = re.sub(r"\s*\{figure\}\s*", " ", stem).strip()
    return Item(number=number, stem=stem, choices=dict(node.choices), tag=tag,
                pages=[page] if page else [], figure=figure,
                answer="; ".join(node.answer), section=section)


def _items(sections) -> list[Item]:
    out: list[Item] = []
    for title, nodes, lead in sections:
        if not nodes:
            continue
        prefix = f"{title} " if title else ""
        for it in nodes:
            head = "\n".join([*lead, it.text])
            if not it.subs:
                out.append(_item(len(out) + 1, head, it, f"{prefix}{it.number}", it.page))
                continue
            for sub in it.subs:
                stem = f"{head}\n{sub.text}"
                out.append(_item(len(out) + 1, stem, sub, f"{prefix}{it.number}.{sub.number}",
                                 sub.page or it.page))
    return out


def split(bank_path: str) -> list[Item]:
    return parse(path_for(bank_path).read_text("utf-8"))


# ── Tooling for the person (or subagent) doing the reading ──────────────────

#: Layouts whose maths is printed as pictures: these need a transcript.
PICTURE_LAYOUTS = ("numbered", "scan")
TEXT_FLOOR = 50            # a page with fewer extracted characters is a photo


def page_kinds(pdf: Path) -> list[bool]:
    """Per page, whether it is a photo (no usable text layer). In the (สสวท)
    files the photos are the textbook exercises and the text pages are the
    teacher's-manual answers."""
    from .extract import _fitz
    with _fitz().open(pdf) as doc:
        return [len(page.get_text().strip()) < TEXT_FLOOR for page in doc]


def render_pages(pdf: Path, out: Path, zoom: float = 1.5,
                 pages: list[int] | None = None) -> list[Path]:
    """Render 1-based ``pages`` (default all) to ``out/pNN.png``."""
    from .extract import _fitz
    fitz = _fitz()
    out.mkdir(parents=True, exist_ok=True)
    done = []
    with fitz.open(pdf) as doc:
        for n in pages or range(1, doc.page_count + 1):
            target = out / f"p{n:02d}.png"
            doc[n - 1].get_pixmap(matrix=fitz.Matrix(zoom, zoom)).save(target)
            done.append(target)
    return done


def todo(bank: dict[str, "bk.BankEntry"]) -> list["bk.BankEntry"]:
    """Exam files that need a transcript and have none yet, in path order.
    A file that serves as another sheet's answer key is not on the list."""
    keys = {e.answer_key for e in bank.values() if e.answer_key and e.answer_key != e.path}
    return sorted((e for e in bank.values()
                   if e.kind == "exam" and e.layout in PICTURE_LAYOUTS
                   and e.stage in ("new", "converted") and e.path not in keys
                   and not path_for(e.path).is_file()),
                  key=lambda e: e.path)


def check(bank_path: str) -> tuple[int, int]:
    """(questions, answered) of a transcript; raises TranscriptError if malformed."""
    items = split(bank_path)
    if not items:
        raise TranscriptError(f"{bank_path}: no items")
    return len(items), sum(bool(it.answer) for it in items)
