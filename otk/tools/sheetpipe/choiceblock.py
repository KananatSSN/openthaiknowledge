"""Split a question-bank sheet into questions by the labels in its margin.

This is the layout of the rathcenter compilations, 203 files in the bank.
Each question is a stem, the exam it came from as a tag
(``[O-NET (มี.ค. 2561/31)]``), and usually choices ``1.``–``5.``. Two things
make the running-number reading of :func:`extract.split_items` useless here:

* **The question numbers are margin labels, not text.** Each is its own small
  block (``1.``, ``2.``, …) placed at the height of the question's first line,
  and the text layer emits them at the *end* of the page. The page's reading
  order is not the question's either: a stem's set definitions can come after
  its source tag. So questions are cut by **geometry**. Every block belongs to
  the label above it, and a question's blocks are read top to bottom.
* **Each file holds the questions twice.** The labels run 1…n over the
  question pages, then 1…n again over the worked solutions, where each
  question is repeated with ``ตอบ N`` and the working. The second run gives the
  answer key.

Text comes through :mod:`.fontfix`, so the font damage in these files is
already repaired.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from pathlib import Path

from .extract import _ascending_runs, _fitz
from .fontfix import Block, page_blocks, repair_for

LABEL = re.compile(r"^\s*(\d{1,3})\.\s*$")
LABEL_MAX_WIDTH = 20        # a margin label is a few points wide
LABEL_SLACK = 6             # a question's first block may start just above its label
SOURCE_TAG = re.compile(r"\[(?=[^\]\n]*[A-Za-zก-ฮ]{2})(?=[^\]\n]*\d{2})[^\]\n]{4,60}\]")
CHOICE = re.compile(r"^\s*([1-5])\.\s*(.*?)\s*$")
STACK_MAX = 4               # lines a stacked-math choice may take
ANSWER = re.compile(r"ตอบ\s*[:：]?\s*(.+?)\s*$", re.MULTILINE)

# Page furniture: the bank's running header and the page-edge ruler.
FURNITURE = ("คลังโจทย์", ".0123456789")
MARGIN = 60                 # pt from the top/bottom edge that holds furniture only


@dataclass
class Item:
    number: int
    stem: str
    choices: dict[int, str] = field(default_factory=dict)
    tag: str = ""                       # the exam it came from, without brackets
    pages: list[int] = field(default_factory=list)
    figure: bool = False                # an image or a vector drawing in its band
    answer: str = ""                    # from the solutions run: "3", "1, 2", "−7"
    solution: str = ""
    section: str = ""                   # answer-key splitter: "<section title> <item>.<sub>"

    def to_json(self) -> dict:
        d = asdict(self)
        if not d["section"]:
            del d["section"]            # choice-block digests stay as they were
        d["choices"] = {str(k): v for k, v in self.choices.items()}
        return d


@dataclass
class Segment:
    number: int
    blocks: list[Block] = field(default_factory=list)
    figure: bool = False

    @property
    def text(self) -> str:
        ordered = sorted((b for b in self.blocks if not b.image),
                         key=lambda b: (b.page, round(b.y0), b.bbox[0]))
        lines = [ln.rstrip() for b in ordered for ln in b.text.splitlines()]
        return "\n".join(ln for ln in lines if ln.strip())

    @property
    def pages(self) -> list[int]:
        return sorted({b.page for b in self.blocks})


def _is_label(b: Block) -> bool:
    return (not b.image and bool(LABEL.match(b.text))
            and b.bbox[2] - b.bbox[0] <= LABEL_MAX_WIDTH)


def _is_furniture(b: Block, height: float) -> bool:
    if b.image:
        return b.bbox[3] < MARGIN
    if any(f in b.text for f in FURNITURE):
        return True
    # The page number: a lone short numeral in the top or bottom margin.
    return (b.bbox[3] < MARGIN or b.bbox[1] > height - 20) and len(b.text.strip()) <= 3


def _figure_bands(page) -> list[tuple[float, float]]:
    """Vertical extents of the page's vector drawings, minus rules and furniture."""
    bands = []
    for d in page.get_drawings():
        r = d["rect"]
        if r.y1 < MARGIN or r.y0 > page.rect.height - MARGIN:
            continue
        if r.width > 5 and r.height > 5:        # skip hairline rules and fraction bars
            bands.append((r.y0, r.y1))
    return bands


Page = tuple[list[Block], list[tuple[float, float]]]     # (blocks, drawing bands)


def read_pages(pdf: str | Path) -> list[Page]:
    """Every page's blocks (font-repaired, furniture dropped) and drawing bands."""
    with _fitz().open(str(pdf)) as doc:
        repair = repair_for(doc)
        return [([b for b in page_blocks(page, repair)
                  if not _is_furniture(b, page.rect.height)], _figure_bands(page))
                for page in doc]


def segments(pdf: str | Path) -> list[list[Segment]]:
    """The label runs of ``pdf``, each cut into one segment per label."""
    return assign(read_pages(pdf))


def assign(pages: list[Page]) -> list[list[Segment]]:
    """Cut pages into label runs, and each run into one segment per label."""
    labels = [(int(LABEL.match(b.text).group(1)), (b.page, b.y0))
              for blocks, _ in pages for b in blocks if _is_label(b)]
    runs = _ascending_runs(labels)
    # Keep runs that do not overlap an earlier-starting one: questions, then solutions.
    chosen: list[list[tuple]] = []
    for run in sorted(runs, key=lambda r: r[0][1]):
        if not chosen or run[0][1] > chosen[-1][-1][1]:
            chosen.append(run)
    if not chosen:
        return []

    # Every label start, in document order, tagged with its run.
    starts = [(pos, ri, num) for ri, run in enumerate(chosen) for num, pos in run]
    starts.sort()
    out: list[list[Segment]] = [[Segment(num) for num, _ in run] for run in chosen]
    index = {(ri, num): seg for ri, run in enumerate(out) for seg in run
             for num in [seg.number]}

    def owner(page: int, y: float):
        """The segment whose label is the last one at or above ``(page, y)``."""
        found = None
        for (lp, ly), ri, num in starts:
            if (lp, ly - LABEL_SLACK) <= (page, y):
                found = index[(ri, num)]
            else:
                break
        return found

    for blocks, bands in pages:
        for b in blocks:
            if _is_label(b):
                continue
            seg = owner(b.page, b.y0)
            if seg is None:
                continue
            seg.blocks.append(b)
            seg.figure |= b.image
        if blocks:
            pno = blocks[0].page
            for y0, _ in bands:
                seg = owner(pno, y0)
                if seg is not None:
                    seg.figure = True

    if len(out) == 1:
        # Some files label only the questions. Their solutions start on the
        # first later page that has a ตอบ; move those pages into their own run.
        last = chosen[0][-1][1][0]
        sol_page = next((blocks[0].page for blocks, _ in pages
                         if blocks and blocks[0].page > last
                         and any(ANSWER.search(b.text) for b in blocks)), None)
        if sol_page is not None:
            tail = Segment(0)
            for seg in out[0]:
                tail.blocks += [b for b in seg.blocks if b.page >= sol_page]
                seg.blocks = [b for b in seg.blocks if b.page < sol_page]
            out.append([tail])
    return out


def parse_question(seg: Segment) -> Item:
    text = seg.text
    tags = SOURCE_TAG.findall(text)
    tag = tags[-1][1:-1].strip() if tags else ""
    body = SOURCE_TAG.sub("", text)

    lines = body.splitlines()
    # The choices are the last run 1., 2., 3., … of lines, in order. A choice
    # whose label stands alone on its line is typeset math, a stacked fraction
    # most often, and its lines follow: "1." / "1" / "5" is 1/5.
    choices: dict[int, str] = {}
    first = len(lines)
    want = 1
    open_choice = 0                         # the choice still taking lines
    for i, ln in enumerate(lines):
        m = CHOICE.match(ln)
        if m and int(m.group(1)) in (want, 1):
            if int(m.group(1)) == 1:
                choices, first, want = {}, i, 1
            choices[want] = m.group(2)
            open_choice = want if not m.group(2) else 0
            want += 1
        elif open_choice and len(choices[open_choice].splitlines()) < STACK_MAX:
            choices[open_choice] = (choices[open_choice] + "\n" + ln.strip()).strip()
        else:
            open_choice = 0
    if len(choices) < 4:                    # an open-answer question
        choices, first = {}, len(lines)
    stem = "\n".join(ln.strip() for ln in lines[:first] if ln.strip())
    return Item(seg.number, stem, choices, tag, seg.pages, seg.figure)


def parse_solution(text: str) -> tuple[str, str]:
    """``(answer, working)`` from one question's stretch of the solutions."""
    m = ANSWER.search(text)
    if not m:
        return "", ""
    return m.group(1).strip(), text[m.end():].strip()


def _chunks_by_tag(items: list[Item], text: str) -> dict[int, str]:
    """Each tagged question's stretch of the solutions text.

    The solutions run sometimes drops a margin label, and then one label's
    segment holds two solutions. Every solution repeats its question, tag
    included, so the tag is the more reliable anchor. A chunk runs from a
    question's tag to where the next question's repeated stem begins.
    """
    out: dict[int, str] = {}
    pos = 0
    tagged = [it for it in items if it.tag]
    for i, it in enumerate(tagged):
        start = text.find(f"[{it.tag}", pos)
        if start < 0:
            continue
        end = len(text)
        if i + 1 < len(tagged):
            nxt = tagged[i + 1]
            tag_at = text.find(f"[{nxt.tag}", start + 1)
            bound = tag_at if tag_at >= 0 else len(text)
            # The next stem is looked for only after this question's ตอบ: a
            # stem opening like กำหนดให้ also turns up inside the working.
            ans = ANSWER.search(text, start, bound)
            head = next((ln.strip()[:25] for ln in nxt.stem.splitlines() if ln.strip()), "")
            stem_at = text.find(head, ans.end(), bound) if (ans and head) else -1
            end = stem_at if stem_at >= 0 else bound
        out[it.number] = text[start:end]
        pos = start + 1
    return out


def split(pdf: str | Path) -> list[Item]:
    """The questions of a choice-block sheet, with answers where the file has them."""
    return items_from(segments(pdf))


def items_from(runs: list[list[Segment]]) -> list[Item]:
    if not runs:
        return []
    items = [parse_question(s) for s in runs[0]]
    if len(runs) > 1:
        by_tag = _chunks_by_tag(items, "\n".join(s.text for s in runs[1]))
        by_label = {s.number: s.text for s in runs[1]}
        for it in items:
            it.answer, it.solution = parse_solution(by_tag.get(it.number, ""))
            if not it.answer:
                it.answer, it.solution = parse_solution(by_label.get(it.number, ""))
    return items
