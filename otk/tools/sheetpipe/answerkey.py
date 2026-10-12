"""Split an exercise file whose answers live in a separate answer-key file.

The rathcenter ``(rath)`` trigonometry notes end each topic with a
``แบบฝึกหัด`` block of open-response exercises; ``(rath) เฉลย.pdf`` holds the
answers for every file, grouped under the same section titles::

    exercise file                       answer key
    ─────────────                       ──────────
    สูตรผลบวกผลต่างมุม  (heading)         สูตรผลบวกผลต่างมุม
    แบบฝึกหัด                            1. 1. −7/25      ← item 1, sub 1
    1. กำหนดให้ sin A = 4/5 …            2. −1            ← sub 2
       1. sin(A + B)                    …
       2. sin(A − B) …                  2. 1. 17/6       ← item 2, sub 1

Both sides number sub-items from 1 again under every item, so ``2.`` alone is
ambiguous. ``align`` settles it with a small dynamic programme. It labels
each numbered line of the exercise as an item, a sub-item, a choice (under a
question that asks ``ข้อใด`` or cites an exam) or noise (a worked example's
own numbered steps). The labelling it keeps is the one whose implied tokens
(item ``t`` with ``k`` sub-items prints ``t. 1.``, ``2.``, …, ``k.``; an item
without sub-items prints ``t.``) best match the key. The Thai heuristic (an
item's own line is a Thai instruction) only breaks ties.

A key section answers one or more exercise blocks. Sub-item 1 always prints
as ``t. 1.``, so a token numbered 1 can only start a new block, and
``key_chunks`` cuts the section there.

Sections are matched by title: a key title is a short Thai line followed by a
``1.`` line, and an exercise block belongs to the last key title seen above
it. Running page headers (the chapter name and page number at the top of a
page) are stripped first, because the chapter name is also a section title.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import fitz

from .choiceblock import Item
from .fontfix import page_texts

NUM = re.compile(r"^(\d{1,2})\.(?!\d)\s*(?:(\d{1,2})\.(?!\d)\s*)?(.*)$")
THAI = re.compile(r"[ก-๛]")
EXERCISE = "แบบฝึกหัด"
#: Words that make a line a question, when its Thai starts after the maths.
ASKS = re.compile(r"เท่ากับ|ข้อใด|จงหา|จงแก้|จงพิสูจน์|พิจารณา|กำหนดให้")


@dataclass
class Token:
    a: int                           # the first number on the line
    b: int | None                    # a second number (``2. 1.``), if any
    text: str = ""

    def add(self, line: str) -> None:
        self.text = f"{self.text} {line}".strip() if self.text else line


@dataclass
class Exercise:
    number: int
    stem: str
    subs: list[str] = field(default_factory=list)
    choices: list[str] = field(default_factory=list)

    @property
    def tag(self) -> str:
        """The exam an item was taken from, when the notes cite one: ``[PAT 1 (ต.ค. 55)/9]``."""
        m = TAG.search(self.stem)
        return m[1].strip() if m else ""


#: An exam citation such as [PAT 1 (ต.ค. 55)/9] or [A-NET 49/1-7] — named, so an
#: interval like [0 , 3π/2] is not taken for one.
TAG = re.compile(r"\[([^\[\]]*(?:[A-Z]{2,}|[ก-๛])[^\[\]]*\d[^\[\]]*)\]")


def clean_pages(texts: list[str]) -> list[list[str]]:
    """Each page's non-blank lines, with the running header removed.

    The header is the page number plus the most common short Thai line among
    the first three lines of the pages (the chapter name).
    """
    pages = [[ln.strip() for ln in t.splitlines() if ln.strip()] for t in texts]
    heads = Counter(re.sub(r"^\d+\s+|\s+\d+$", "", ln) for p in pages for ln in p[:3]
                    if THAI.search(ln) and len(ln) < 60)
    running = heads.most_common(1)[0][0] if heads else ""
    out = []
    for p in pages:
        # At most one title line and one page number: a section heading that
        # repeats the chapter name can sit right under the header.
        seen_title = seen_number = False
        i = 0
        while i < min(3, len(p)):
            if p[i].isdigit() and not seen_number:
                seen_number = True
            elif re.sub(r"^\d+\s+|\s+\d+$", "", p[i]) == running and not seen_title:
                seen_title = True
                seen_number = seen_number or p[i] != running          # "26    ฟังก์ชัน…"
            else:
                break
            i += 1
        out.append(p[i:])
    return out


def lines_of(pdf: str | Path) -> list[str]:
    with fitz.open(str(pdf)) as doc:
        return [ln for page in clean_pages(page_texts(doc)) for ln in page]


# ── The key ──────────────────────────────────────────────────────────────────

def _is_title(lines: list[str], i: int) -> bool:
    ln = lines[i]
    if NUM.match(ln) or not THAI.search(ln) or len(ln) > 40 or re.match(r"^[\d\-−(]", ln):
        return False
    nxt = lines[i + 1] if i + 1 < len(lines) else ""
    return bool(re.match(r"^1\.(?!\d)", nxt))


def key_sections(lines: list[str]) -> dict[str, list[Token]]:
    """Answer tokens under each section title, in order. Continuation lines
    (stacked fractions, working) are joined onto the token above them."""
    out: dict[str, list[Token]] = {}
    current: list[Token] | None = None
    for i, ln in enumerate(lines):
        if _is_title(lines, i):
            current = out.setdefault(ln, [])
            continue
        if current is None:
            continue
        m = NUM.match(ln)
        if m:
            current.append(Token(int(m[1]), int(m[2]) if m[2] else None, m[3].strip()))
        elif current:
            current[-1].add(ln)
    return out


# ── The exercise file ────────────────────────────────────────────────────────

def exercise_blocks(lines: list[str], titles: set[str]) -> list[tuple[str, list[str]]]:
    """``(section title, lines)`` for every ``แบบฝึกหัด`` block."""
    blocks: list[tuple[str, list[str]]] = []
    title, body = "", None
    for ln in lines:
        if ln in titles:
            title = ln
            if body is not None:
                body = None                      # a new section ends the block
            continue
        if ln.startswith(EXERCISE):
            body = []
            blocks.append((title, body))
            continue
        if body is not None:
            body.append(ln)
    return blocks


@dataclass
class Seg:
    """A numbered line of an exercise block with the unnumbered lines under it."""

    n: int | None                    # None: text before the first number, or a "1. 2." line
    text: str
    instruction: bool = False        # reads like an item: see ``_is_instruction``
    mcq: bool = False                # asks "ข้อใด" or cites an exam: its sub-lines may be choices


def _is_instruction(first: str, text: str) -> bool:
    # Thai on the numbered line itself, or a bare number whose text follows;
    # a sidebar note under a maths sub-item must not promote it.
    return (bool(THAI.search(first)) or (not first and bool(THAI.search(text)))
            or bool(TAG.search(text)) or bool(ASKS.search(text)))


def segments(lines: list[str]) -> list[Seg]:
    raw: list[tuple[re.Match | None, list[str]]] = []
    for ln in lines:
        m = NUM.match(ln)
        if m or not raw:
            raw.append((m, [m[3].strip() if m and not m[2] else ln] if m else [ln]))
        else:
            raw[-1][1].append(ln)
    out = []
    for m, body in raw:
        text = " ".join(t for t in body if t)
        if m is None or m[2]:
            out.append(Seg(None, text))
            continue
        first = body[0] if body else ""
        out.append(Seg(int(m[1]), text, _is_instruction(first, text),
                       bool(TAG.search(text)) or "ข้อใด" in text))
    return out


# Alignment costs. A key token matched costs nothing; one missed or invented
# costs 1. The Thai heuristic only breaks ties between structures the key
# accepts equally well, and dropping a numbered line (a sidebar's own steps)
# costs a little more than a heuristic disagreement.
MISS, NOISE, AGAINST_TOP, AGAINST_SUB, CHOICE = 1.0, 0.6, 0.3, 0.2, 0.05


def align(segs: list[Seg], toks: list[Token]) -> list[tuple[str, int | None]]:
    """Label every segment ``top``, ``sub``, ``choice``, ``noise`` or ``text``,
    with the key token each top or sub takes (``None`` if unmatched).

    Tops are numbered 1, 2, …; a top's subs 1, 2, …; a top with subs takes
    ``t. 1.`` then ``2.``, ``3.`` …; a top without subs takes ``t.`` (its
    choices, if it is a choice question, take nothing). The labelling that
    agrees best with ``toks`` wins.
    """
    import sys
    from functools import lru_cache

    sys.setrecursionlimit(max(10000, sys.getrecursionlimit()))
    n_seg, n_tok = len(segs), len(toks)

    def emit(j: int, want: tuple[int, int | None]) -> tuple[float, int, int | None]:
        """Cost, next key index, matched token for emitting ``want`` at ``j``.
        With no key at all there is no evidence either way: the heuristic decides."""
        if j < n_tok and (toks[j].a, toks[j].b) == want:
            return 0.0, j + 1, j
        return (MISS if n_tok else 0.0), j, None

    @lru_cache(maxsize=None)
    def best(i: int, t: int, s: int, c: int, mcq: bool, j: int) -> tuple[float, tuple]:
        # Closing the current top without subs emits "t." for it.
        def close(j_: int) -> tuple[float, int, int | None]:
            return emit(j_, (t, None)) if t and not s else (0.0, j_, None)

        if i == n_seg:
            cost, j2, got = close(j)
            return cost + MISS * (n_tok - j2), (("close", got),)
        seg = segs[i]
        options: list[tuple[float, tuple]] = []
        # A key token with no line here (a sub the notes print as a picture).
        if j < n_tok:
            cost, path = best(i, t, s, c, mcq, j + 1)
            options.append((cost + MISS, (("skip", None),) + path))
        if seg.n is None:
            cost, path = best(i + 1, t, s, c, mcq, j)
            return min(options + [(cost, (("text", None),) + path)], key=lambda o: o[0])
        n = seg.n
        if n == t + 1:
            c1, j1, got = close(j)
            cost, path = best(i + 1, n, 0, 0, seg.mcq, j1)
            options.append((c1 + cost + (0 if seg.instruction else AGAINST_TOP),
                            (("top", got),) + path))
        if t and not c and n == s + 1:
            c1, j1, got = emit(j, (t, 1) if s == 0 else (n, None))
            cost, path = best(i + 1, t, n, 0, mcq, j1)
            options.append((c1 + cost + (AGAINST_SUB if seg.instruction else 0), (("sub", got),) + path))
        if t and mcq and not s and n == c + 1 and c < 5:
            cost, path = best(i + 1, t, 0, n, mcq, j)
            options.append((cost + CHOICE, (("choice", None),) + path))
        cost, path = best(i + 1, t, s, c, mcq, j)
        options.append((cost + NOISE, (("noise", None),) + path))
        return min(options, key=lambda o: o[0])

    path = best(0, 0, 0, 0, False, 0)[1]
    best.cache_clear()
    # Fold the path back onto segments: a top's own token arrives when it closes.
    labels: list[tuple[str, int | None]] = []
    open_top: int | None = None
    for step, got in path:
        if step == "skip":
            continue
        if step in ("top", "close") and open_top is not None and got is not None:
            labels[open_top] = ("top", got)
        if step == "close":
            break
        labels.append((step, None if step == "top" else got))
        if step == "top":
            open_top = len(labels) - 1
    return labels


def exercises(lines: list[str], toks: list[Token] | None = None
              ) -> tuple[list[Exercise], list[list[str]]]:
    """Items, their sub-items, and the answers each takes from ``toks``.

    Without ``toks`` the structure comes from the Thai heuristic alone."""
    segs = segments(lines)
    labels = align(segs, toks or [])
    out: list[Exercise] = []
    answers: list[list[str]] = []
    for seg, (label, got) in zip(segs, labels):
        ans = toks[got].text if toks and got is not None else ""
        if label == "top":
            out.append(Exercise(seg.n, seg.text))
            answers.append([ans])
        elif label == "sub" and out:
            out[-1].subs.append(seg.text)
            if len(out[-1].subs) == 1:
                answers[-1] = [ans]
            else:
                answers[-1].append(ans)
        elif label == "choice" and out:
            out[-1].choices.append(seg.text)
        elif out:
            _append(out[-1], seg.text)
    return out, answers


def _append(ex: Exercise, text: str) -> None:
    for part in (ex.choices, ex.subs):
        if part:
            part[-1] = f"{part[-1]} {text}".strip()
            return
    ex.stem = f"{ex.stem} {text}".strip()


def key_chunks(tokens: list[Token]) -> list[list[Token]]:
    """A key section cut into one chunk per exercise block. Sub-item 1 always
    prints as ``t. 1.``, so a token numbered 1 can only start a new block."""
    chunks: list[list[Token]] = []
    for tok in tokens:
        if tok.a == 1 or not chunks:
            chunks.append([])
        chunks[-1].append(tok)
    return chunks


def split(pdf: str | Path, key_pdf: str | Path) -> list[Item]:
    """Every exercise sub-item of ``pdf``, answered from ``key_pdf``.

    ``key_pdf`` may be ``pdf`` itself: the 🍰 lecture books bind the notes and
    their key together, the key after the last ``แบบฝึกหัด``. Its titles
    are then kept only if they also head a section of the notes, so a
    stray Thai line in the last exercise cannot end a block early.
    """
    lines = lines_of(pdf)
    if Path(key_pdf) == Path(pdf):
        starts = [i for i, ln in enumerate(lines) if ln.startswith(EXERCISE)]
        cut = starts[-1] + 1 if starts else len(lines)
        headings = set(lines[:cut])
        keys = {t: v for t, v in key_sections(lines[cut:]).items() if t in headings}
    else:
        keys = key_sections(lines_of(key_pdf))
    items: list[Item] = []
    # Several blocks can share a title; the key answers them in order, one chunk each.
    chunks = {t: iter(key_chunks(v)) for t, v in keys.items()}
    for title, body in exercise_blocks(lines, set(keys)):
        exs, answers = exercises(body, next(chunks.get(title, iter(())), []))
        for ex, row in zip(exs, answers):
            if ex.choices:
                stem = TAG.sub("", ex.stem).strip()
                items.append(Item(len(items) + 1, stem, choices=dict(enumerate(ex.choices, start=1)),
                                  tag=ex.tag, answer=row[0], section=f"{title} {ex.number}".strip()))
                continue
            parts = ex.subs or [""]
            for s, (sub, ans) in enumerate(zip(parts, row), start=1):
                stem = ex.stem if not sub else f"{ex.stem}\n{sub}"
                label = f"{ex.number}" if not ex.subs else f"{ex.number}.{s}"
                items.append(Item(len(items) + 1, stem, answer=ans, section=f"{title} {label}".strip()))
    return items
