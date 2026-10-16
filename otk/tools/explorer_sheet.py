"""The explorer's download sheet: one page of problems that uses the page, and one of answers.

Laid out for a single problem set, apart from the general worksheet renderer
(``otk.core.render.pdf``, which the CLI uses):

* a slim header, so the page is mostly problems;
* formulas kept inside their sentence, wrapped with it;
* the options set four across, or two by two, whenever they fit on the line;
* two columns whenever every question fits in one.

Each question is measured by drawing it on a scratch page, so the page is
filled as far as the questions really reach, in whatever Thai font is
installed. Questions are drawn until the page is full, and a repeat of one
already on the sheet is drawn again.
"""

from __future__ import annotations

import io
import json
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path
from random import Random
from typing import Callable, Optional

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
from matplotlib.font_manager import FontProperties
from matplotlib.mathtext import MathTextParser
from matplotlib.patches import Rectangle
from matplotlib.textpath import TextPath

from otk.core.question import Question
from otk.core.render.pdf import (_CHOICE_LABELS, _THAI_COMBINING, A4, ARROW, INK, KEY_INK,
                                 _measure_fig, _new_page, _one_line, _text_w)

AssetResolver = Callable[[str], Optional[Path]]

# Page geometry, as fractions of the A4 page (y runs up from the bottom).
LEFT, RIGHT = 0.06, 0.94
TOP = 0.962
BOTTOM = 0.05
FOOTER_Y = 0.03
GUTTER = 0.04
QUESTION_GAP = 0.016
PART_GAP = 0.004
ROW_GAP = 0.003
LOGO_H = 0.034
IMAGE_H = 0.12                      # a diagram's height, before it is narrowed to its column

TITLE_PT = 13
META_PT = 8
FIELD_PT = 9
NUMBER_PT = 9.5
TEXT_PT = 9.5
MATH_ONLY_PT = 11.5                 # a stem that is nothing but a formula
CHOICE_PT = 9
CODE_PT = 8
KEY_PT = 9
LINESPACING = 1.3

#: Bundled with matplotlib; draws the symbols a Thai font lacks.
_FALLBACK_FONT = "DejaVu Sans"

GRAY = "#555555"
FAINT = "#999999"
RULE = "#444444"
CODE_FILL, CODE_EDGE = "#f3f5f8", "#c9d0da"

#: Questions drawn before the column count is chosen: all of them must fit a column.
PROBE = 6
#: The most questions one page takes, and the draws tried once a column is full.
MAX_QUESTIONS = 40
MAX_MISSES = 4
#: Draws in a row that may repeat a question already on the sheet before giving up.
REPEAT_TRIES = 5


@dataclass(frozen=True)
class SheetInfo:
    """What the header and footer say."""
    title: str
    meta: str                       # the subject and unit, under the title
    level: str                      # the corner badge, e.g. "ม.3"
    key: str                        # the set's key, in the footer
    instructions: str
    logo: Path | None = None
    font: str = ""


@dataclass(frozen=True)
class Placement:
    index: int                      # into ``Plan.questions``
    column: int
    x: float
    y_top: float
    height: float


@dataclass
class Plan:
    """Which questions go on the page, and where."""
    columns: int
    width: float                    # of one column
    top: float                      # where the first question starts
    questions: list[Question] = field(default_factory=list)
    placements: list[Placement] = field(default_factory=list)


# ── Drawing surface ──────────────────────────────────────────────────────────

class _Canvas:
    """The page being drawn, or a scratch page that only measures.

    Every drawing call reports the height it took, and the canvas remembers the
    furthest right anything reached: that is how a question is found too wide
    for a column. A measuring canvas (``measure=True``) works lines and
    pictures out from their metrics and draws nothing, which is most of what
    makes a sheet quick: drawing a formula means parsing it again.
    """

    def __init__(self, fig, ax, font: str = "", measure: bool = False) -> None:
        self.fig, self.ax = fig, ax
        self.font, self.measure = font, measure
        # The Thai font first, then one with the symbols it lacks (∠, ⊕, ①).
        self.family = [font, _FALLBACK_FONT] if font else None
        self.renderer = fig.canvas.get_renderer()
        self.artists: list = []
        self.image_axes: list = []
        self.right = 0.0

    def text(self, x: float, y: float, s: str, size: float, *, color: str = INK,
             bold: bool = False, family: str | None = None, ha: str = "left",
             linespacing: float = LINESPACING, **extra) -> float:
        """Draw ``s`` hanging from ``y``; return its height."""
        if family or self.family:
            extra["family"] = family or self.family
        artist = self.ax.text(x, y, s, fontsize=size, color=color, ha=ha, va="top",
                              fontweight="bold" if bold else "normal",
                              linespacing=linespacing, **extra)
        self.artists.append(artist)
        box = artist.get_window_extent(self.renderer)
        self.right = max(self.right, box.x1 / self.fig.bbox.width)
        return box.height / self.fig.bbox.height

    def lines(self, x: float, y: float, lines: list[str], size: float, *,
              color: str = INK, bold: bool = False, mono: bool = False,
              ascent: float = 0.0) -> float:
        """Draw ``lines`` hanging from ``y``, each on its own baseline; return the height.

        The baselines are placed here, from point sizes, rather than by
        matplotlib's multi-line layout: that sizes each line by its own glyphs,
        and differently at the 100 dpi a page is measured at and the 72 of the
        PDF, so a long Thai paragraph drew a line taller than it measured.
        ``ascent`` (points) raises the first line's room, to share a baseline
        with a taller neighbour.
        """
        extra = ({"family": "monospace"} if mono
                 else {"family": self.family} if self.family else {})
        baseline, below = y, 0.0
        for i, line in enumerate(lines):
            up, down = _line_metrics(line, size, mono)
            if i == 0:
                up = max(up, ascent)
                baseline = y - up * _PT
            else:
                baseline -= (below + up + _LEADING * size) * _PT
            below = down
            if self.measure:
                width = _mono_w(line, size) if mono else _seg_w(line, size, self.font)
                self.right = max(self.right, x + width * (1.08 if bold else 1.0))
                continue
            self.artists.append(self.ax.text(x, baseline, line, fontsize=size, color=color,
                                             ha="left", va="baseline",
                                             fontweight="bold" if bold else "normal", **extra))
        return (y - baseline) + below * _PT if lines else 0.0

    def patch(self, patch):
        self.ax.add_patch(patch)
        self.artists.append(patch)
        return patch

    def line(self, x0: float, x1: float, y: float, width: float, color: str = RULE) -> None:
        self.artists.extend(self.ax.plot([x0, x1], [y, y], color=color, linewidth=width))

    def picture(self, x: float, y_bottom: float, w: float, h: float):
        """Axes to draw a picture in, or None on a measuring canvas."""
        self.right = max(self.right, x + w)
        if self.measure:
            return None
        axes = self.fig.add_axes([x, y_bottom, w, h])
        axes.set_axis_off()
        self.image_axes.append(axes)
        return axes

    def clear(self) -> None:
        for artist in self.artists:
            artist.remove()
        for axes in self.image_axes:
            self.fig.delaxes(axes)
        self.artists, self.image_axes, self.right = [], [], 0.0


def _scratch(font: str) -> _Canvas:
    fig = Figure(figsize=A4)
    FigureCanvasAgg(fig)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()
    return _Canvas(fig, ax, font, measure=True)


def _use_font(font: str) -> None:
    if font:
        names = matplotlib.rcParams["font.sans-serif"]
        matplotlib.rcParams["font.sans-serif"] = [font] + [n for n in names if n != font]


@lru_cache(maxsize=16)
def _image(path: str):
    """A picture, decoded once for measuring and again for drawing.

    Kept as 8-bit (a quarter of matplotlib's float decoding) and only a sheet's
    worth at a time: a generated diagram is a new file with each draw, so a
    larger cache would only fill with pictures that never come back.
    """
    img = plt.imread(path)
    return (img * 255).round().astype("uint8") if img.dtype.kind == "f" else img


# ── Line metrics, in points, the same in every backend ───────────────────────

_PT = 1 / (A4[1] * 72)              # one point, as a fraction of the page height
_LEADING = 0.25                     # em, between one line's lowest mark and the next's highest
_MATH = re.compile(r"(?<!\\)\$(.+?)(?<!\\)\$")
_MATH_PARSER = MathTextParser("path")

# Thai stacks a vowel and a tone mark above a consonant, and a vowel below it.
# The tallest stacks and the deepest marks, measured from the glyph outlines.
_THAI_EXTREMES = ("ปั้ปิ๊ฝี่ฟื้ฬั๋ ปิ่น", "ฎุฏูญุฐู ฤๅ", "Agjy()")
_MONO_EXTREMES = ("Agjy()[]{}|",)


@lru_cache(maxsize=16)
def _font_metrics(family: tuple[str, ...], mono: bool) -> tuple[float, float]:
    """(ascent, descent) in em of the font that draws, for the tallest and deepest marks.

    Read from glyph outlines, so they hold in every backend; ``family`` is the
    active ``font.sans-serif`` list, which picks the font.
    """
    prop = FontProperties(family="monospace" if mono else "sans-serif", size=100)
    paths = [TextPath((0, 0), s, prop=prop).get_extents()
             for s in (_MONO_EXTREMES if mono else _THAI_EXTREMES)]
    return max(p.y1 for p in paths) / 100, -min(p.y0 for p in paths) / 100


@lru_cache(maxsize=4096)
def _math_box(tex: str, size: float) -> tuple[float, float, float]:
    """(width, ascent, descent) of a formula in points: one parse gives all three."""
    try:
        parsed = _MATH_PARSER.parse(f"${tex}$", dpi=720, prop=FontProperties(size=size))
    except ValueError:              # a formula mathtext cannot set: assume a tall one
        return 0.6 * size * len(tex), 1.6 * size, 0.6 * size
    width, height, depth = (float(v) / 10 for v in (parsed.width, parsed.height, parsed.depth))
    return width, height - depth, depth


def _math_metrics(tex: str, size: float) -> tuple[float, float]:
    """(ascent, descent) of a formula in points, from mathtext's own layout."""
    return _math_box(tex, size)[1:]


_PT_W = 1 / (A4[0] * 72)            # one point, as a fraction of the page width


@lru_cache(maxsize=16384)
def _plain_w(text: str, size: float, font: str) -> float:
    """Width of text with no formula in it, spaces at either end included."""
    return _text_w(f"|{text}|", size, font) - _text_w("||", size, font)


@lru_cache(maxsize=16384)
def _seg_w(text: str, size: float, font: str) -> float:
    """Width of a piece or a line, as a fraction of the page: the plain text
    between formulas plus each formula's own width, each measured once."""
    width, pos = 0.0, 0
    for m in _MATH.finditer(text):
        if m.start() > pos:
            width += _plain_w(text[pos:m.start()], size, font)
        width += _math_box(m.group(1), size)[0] * _PT_W
        pos = m.end()
    if pos < len(text):
        width += _plain_w(text[pos:], size, font)
    return width


def _mono_text_w(text: str, size: float) -> float:
    fig = _measure_fig()
    artist = fig.text(0, 0, text, fontsize=size, family="monospace")
    width = artist.get_window_extent(fig.canvas.get_renderer()).width / fig.bbox.width
    artist.remove()
    return width


@lru_cache(maxsize=4096)
def _mono_w(line: str, size: float) -> float:
    """Width of a line of code (monospace), as a fraction of the page."""
    return _mono_text_w(f"|{line}|", size) - _mono_text_w("||", size)


def _line_metrics(line: str, size: float, mono: bool) -> tuple[float, float]:
    """(ascent, descent) of one line in points: the font's, or a taller formula's."""
    return _line_metrics_in(tuple(matplotlib.rcParams["font.sans-serif"][:4]), line, size, mono)


@lru_cache(maxsize=8192)
def _line_metrics_in(family: tuple[str, ...], line: str, size: float,
                     mono: bool) -> tuple[float, float]:
    em_up, em_down = _font_metrics(family, mono)
    up, down = em_up * size, em_down * size
    if mono:
        return up, down
    for tex in _MATH.findall(line):
        m_up, m_down = _math_metrics(tex, size)
        up, down = max(up, m_up + 0.1 * size), max(down, m_down + 0.1 * size)
    return up, down


def _first_ascent(lines: list[str], size: float) -> float:
    return _line_metrics(lines[0], size, False)[0] if lines else 0.0


# ── Text: sentences with formulas in them ────────────────────────────────────

def _escape(text: str) -> str:
    """Plain text for matplotlib: a ``$`` would otherwise open a formula."""
    return text.replace("$", r"\$")


# KaTeX spellings that matplotlib's mathtext knows by another name.
_TEX_ALIASES = [(re.compile(rf"\\{old}(?![A-Za-z])"), new) for old, new in (
    ("ge", r"\\geq"), ("le", r"\\leq"), ("ne", r"\\neq"), ("dfrac", r"\\frac"),
    ("tfrac", r"\\frac"), ("text", r"\\mathrm"), ("textrm", r"\\mathrm"),
    ("operatorname", r"\\mathrm"), ("lbrace", r"\\{"), ("rbrace", r"\\}"),
    ("dots", r"\\ldots"), ("implies", r"\\Rightarrow"), ("iff", r"\\Leftrightarrow"))]


@lru_cache(maxsize=4096)
def _mathtext(tex: str) -> str | None:
    """``tex`` as mathtext can set it, or None when it cannot (an array, say)."""
    for pattern, new in _TEX_ALIASES:
        tex = pattern.sub(new, tex)
    try:
        _MATH_PARSER.parse(f"${tex}$", dpi=72, prop=FontProperties(size=10))
    except ValueError:
        return None
    return tex


def _pieces(runs: list[tuple[str, str]]) -> list[tuple[str, bool]]:
    """``(piece, breakable)``: words, spaces and line breaks of the text, each formula
    whole. A formula mathtext cannot set is printed as its TeX, rather than failing."""
    out: list[tuple[str, bool]] = []
    for kind, value in runs:
        if kind == "math":
            tex = _mathtext(value)
            out.append((f"${tex}$" if tex is not None else _escape(value), False))
        else:
            out.extend((part, True) for part in re.split(r"( |\n)", _escape(value)) if part)
    return out


def _fit(used: float, word: str, size: float, width: float, font: str) -> int:
    """How many characters of ``word`` still fit after ``used`` of the line; never
    before a Thai mark."""
    lo, hi = 0, len(word)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if used + _seg_w(word[:mid], size, font) <= width:
            lo = mid
        else:
            hi = mid - 1
    while 0 < lo < len(word) and word[lo] in _THAI_COMBINING:
        lo -= 1
    return lo


def _wrap(runs: list[tuple[str, str]], size: float, width: float, font: str) -> list[str]:
    """Lines no wider than ``width``. Spaces are the preferred breaks; Thai, which has
    none between words, is cut by character; a formula is never cut. Each piece is
    measured once and the line's width kept as a running sum."""
    lines: list[str] = []
    line, used = "", 0.0

    def flush() -> None:
        nonlocal line, used
        if line.strip():
            lines.append(line.rstrip())
        line, used = "", 0.0

    for piece, breakable in _pieces(runs):
        if piece == "\n":          # the text's own line break
            flush()
            continue
        if piece == " " and not line:
            continue
        w = _seg_w(piece, size, font)
        if used + w <= width:
            line, used = line + piece, used + w
            continue
        if piece == " ":
            flush()
            continue
        if not breakable or w <= width:
            flush()
            line, used = piece, w
            continue
        while piece:                # a long run of Thai: fill the line, then the next
            cut = _fit(used, piece, size, width, font)
            if cut == 0:
                if line:
                    flush()
                    continue
                cut = 1
            line, used = line + piece[:cut], used + _seg_w(piece[:cut], size, font)
            piece = piece[cut:]
            if piece:
                flush()
    flush()
    return lines


def _one_string(runs: list[tuple[str, str]]) -> str:
    """The runs on one line: a line break inside an option becomes a space."""
    return "".join(" " if piece == "\n" else piece for piece, _ in _pieces(runs))


def _runs(content) -> list[tuple[str, str]]:
    return [("math", b.tex) if b.kind == "math"
            else ("text", getattr(b, "text", "") or getattr(b, "code", "")) for b in content]


def _stem_parts(q: Question) -> list[tuple[str, object]]:
    """The stem as paragraphs (runs of text and formulas, in order) and the code
    and pictures that stand on their own lines."""
    parts: list[tuple[str, object]] = []
    runs: list[tuple[str, str]] = []
    for block in q.stem:
        if block.kind in ("text", "math"):
            runs.append(("math", block.tex) if block.kind == "math" else ("text", block.text))
            continue
        if runs:
            parts.append(("para", runs))
            runs = []
        parts.append((block.kind, block))
    if runs:
        parts.append(("para", runs))
    return parts


# ── One question ─────────────────────────────────────────────────────────────

def _draw_code(c: _Canvas, code: str, x: float, y: float, width: float) -> float:
    pad = 0.005
    h = c.lines(x + pad, y - pad, code.split("\n"), CODE_PT, mono=True)
    c.patch(Rectangle((x, y - h - 2 * pad), width, h + 2 * pad, facecolor=CODE_FILL,
                      edgecolor=CODE_EDGE, linewidth=0.6, zorder=0))
    return h + 2 * pad


def _image_size(path: Path, width: float) -> tuple[float, float]:
    """(width, height) of a diagram: ``IMAGE_H`` tall, narrowed to ``width`` if wider."""
    img = _image(str(path))
    aspect = (img.shape[1] / img.shape[0]) * (A4[1] / A4[0])   # page width per page height
    w, h = IMAGE_H * aspect, IMAGE_H
    return (width, width / aspect) if w > width else (w, h)


def _draw_image(c: _Canvas, block, path: Path, x: float, y: float, width: float) -> float:
    img = _image(str(path))
    w, h = _image_size(path, width)
    axes = c.picture(x, y - h, w, h)
    if axes is None:                # measuring: the size is all that counts
        return h
    axes.imshow(img)
    for m in block.markers:
        if m.style == "dot":
            axes.plot([m.x * img.shape[1]], [m.y * img.shape[0]], "o", color=ARROW, markersize=4)
        else:
            axes.annotate("", xy=(m.x, 1 - m.y), xytext=(m.x + 0.16, 1 - m.y + 0.16),
                          xycoords="axes fraction", annotation_clip=False,
                          arrowprops=dict(arrowstyle="-|>", color=ARROW, lw=1.4))
    return h


def _choices_per_row(rows: list[list[tuple[str, str]]], width: float,
                     label_w: float, font: str) -> int:
    """All the options on one line, else two to a line, else one: the most that fit."""
    n = len(rows)
    widths = [_seg_w(_one_string(r), CHOICE_PT, font) for r in rows]
    for per_row in ([n] if n <= 4 else []) + ([2] if n > 2 else []):
        if all(label_w + w + 0.012 <= width / per_row for w in widths):
            return per_row
    return 1


def _draw_choices(c: _Canvas, q: Question, x: float, y: float, width: float,
                  font: str) -> float:
    """``ก. … ข. …`` under the stem; the student rings a letter."""
    rows = [_runs(choice.content) for choice in q.choices]
    label_w = _text_w("ก.", CHOICE_PT, font) + 0.007
    per_row = _choices_per_row(rows, width, label_w, font)
    slot = width / per_row
    top = y
    for start in range(0, len(rows), per_row):
        bodies = [[_one_string(runs)] if per_row > 1
                  else _wrap(runs, CHOICE_PT, width - label_w, font)
                  for runs in rows[start:start + per_row]]
        # One baseline across the row, however tall a formula in it stands.
        ascent = max(_first_ascent(lines, CHOICE_PT) for lines in bodies)
        tallest = 0.0
        for j, lines in enumerate(bodies):
            i = start + j
            sx = x + j * slot
            label = f"{_CHOICE_LABELS[i]}." if i < len(_CHOICE_LABELS) else f"{i + 1}."
            c.lines(sx, y, [label], CHOICE_PT, ascent=ascent)
            tallest = max(tallest, c.lines(sx + label_w, y, lines, CHOICE_PT, ascent=ascent))
        y -= tallest + ROW_GAP
    return top - y


def _draw_question(c: _Canvas, q: Question, number: int, x: float, y: float, width: float,
                   number_w: float, font: str, resolver: AssetResolver | None) -> float:
    """Draw one question hanging from ``y``; return the height it took."""
    top = y
    bx, bw = x + number_w, width - number_w
    parts = _stem_parts(q)

    # One narrow picture stands on the right, and the words and options run
    # down beside it: a diagram the width of half the column would otherwise
    # leave the other half empty.
    pictures = [part for kind, part in parts if kind == "image"]
    path = resolver(pictures[0].asset_id) if len(pictures) == 1 and resolver else None
    beside = 0.0
    if path is not None:
        w, _ = _image_size(path, bw)
        if w <= bw * 0.5:
            beside = _draw_image(c, pictures[0], path, bx + bw - w, y, w)
            bw -= w + 0.015
            parts = [(kind, part) for kind, part in parts if kind != "image"]

    # The number shares the first line's baseline.
    first = parts[0] if parts else None
    number_ascent = 0.0
    for i, (kind, part) in enumerate(parts):
        if kind == "para":
            size = MATH_ONLY_PT if all(k == "math" for k, _ in part) else TEXT_PT
            lines = _wrap(part, size, bw, font)
            if i == 0:
                number_ascent = _first_ascent(lines, size)
            y -= c.lines(bx, y, lines, size, ascent=_first_ascent([f"{number}."], NUMBER_PT)
                         if i == 0 else 0.0) + PART_GAP
        elif kind == "code":
            y -= _draw_code(c, part.code, bx, y, bw) + PART_GAP
        elif kind == "image":
            path = resolver(part.asset_id) if resolver else None
            if path is not None:
                y -= _draw_image(c, part, path, bx, y, bw) + PART_GAP
            elif part.alt:
                y -= c.lines(bx, y, _wrap([("text", part.alt)], TEXT_PT, bw, font),
                             TEXT_PT, color=GRAY) + PART_GAP
    c.lines(x, top, [f"{number}."], NUMBER_PT, bold=True,
            ascent=number_ascent if first and first[0] == "para" else 0.0)
    y -= _draw_choices(c, q, bx, y, bw, font)
    return max(top - y, beside)


# ── Header, footer and the answer page ───────────────────────────────────────

def _draw_header(c: _Canvas, info: SheetInfo, title: str, count: int | None) -> float:
    """Logo, title, subject and level, then (on the problem page) the instructions and
    the name, date and score fields. Return where the questions start."""
    y = TOP
    x = LEFT
    logo_h = 0.0
    if info.logo is not None and info.logo.exists():
        img = _image(str(info.logo))
        w = LOGO_H * (img.shape[1] / img.shape[0]) * (A4[1] / A4[0])
        axes = c.picture(LEFT, y - LOGO_H, w, LOGO_H)
        if axes is not None:
            axes.imshow(img)
        x, logo_h = LEFT + w + 0.012, LOGO_H
    if info.level:
        c.text(RIGHT - 0.004, y - 0.002, info.level, 12, bold=True, ha="right",
               bbox=dict(boxstyle="round,pad=0.35", facecolor="#f2f2f2",
                         edgecolor=INK, linewidth=1))
    text_h = c.text(x, y, title, TITLE_PT, bold=True)
    if info.meta:
        text_h += 0.003 + c.text(x, y - text_h - 0.003, info.meta, META_PT, color=GRAY)
    y -= max(logo_h, text_h) + 0.010

    if count is not None:
        row = 0.0
        if info.instructions:
            row = c.text(LEFT, y, info.instructions, FIELD_PT)
        fields = [("ชื่อ", 0.24, ""), ("วันที่", 0.11, ""), ("คะแนน", 0.05, f"/ {count}")]
        widths = [_text_w(label, FIELD_PT, info.font) + 0.006 + line + 0.006
                  + (_text_w(after, FIELD_PT, info.font) if after else 0) for label, line, after in fields]
        fx = RIGHT - sum(widths) - 0.02 * (len(fields) - 1)
        for (label, line, after), w in zip(fields, widths):
            row = max(row, c.text(fx, y, label, FIELD_PT))
            lx = fx + _text_w(label, FIELD_PT, info.font) + 0.006
            c.line(lx, lx + line, y - row + 0.002, 0.7, INK)
            if after:
                c.text(lx + line + 0.006, y, after, FIELD_PT)
            fx += w + 0.02
        y -= row + 0.008
    c.line(LEFT, RIGHT, y, 1.2)
    return y - 0.012


def _draw_footer(c: _Canvas, info: SheetInfo, page: int, pages: int) -> None:
    c.text(LEFT, FOOTER_Y, f"OpenThaiKnowledge · {info.key}", 7, color=FAINT)
    c.text(RIGHT, FOOTER_Y, f"{page} / {pages}", 7, color=FAINT, ha="right")


def _draw_answers(c: _Canvas, info: SheetInfo, questions: list[Question]) -> None:
    top = _draw_header(c, info, f"เฉลย · {info.title}", None)
    columns = 2 if len(questions) > 12 else 1
    width = (RIGHT - LEFT - GUTTER * (columns - 1)) / columns
    number_w = _text_w("88.", KEY_PT, info.font) * 1.15 + 0.006
    label_w = _text_w("ก.", KEY_PT, info.font) + 0.01
    per_column = -(-len(questions) // columns)
    y = top
    for i, q in enumerate(questions):
        col, row = divmod(i, per_column)
        if row == 0:
            y = top
        x = LEFT + col * (width + GUTTER)
        h = c.text(x, y, f"{i + 1}.", KEY_PT, bold=True)
        label = _CHOICE_LABELS[q.answer] if q.answer < len(_CHOICE_LABELS) else str(q.answer + 1)
        c.text(x + number_w, y, f"{label}.", KEY_PT, bold=True, color=KEY_INK)
        answer = _one_string(_runs(q.choices[q.answer].content))
        if "$" not in answer:
            answer = _one_line(answer, KEY_PT, width - number_w - label_w, info.font)
        h = max(h, c.text(x + number_w + label_w, y, answer, KEY_PT, color=KEY_INK))
        y -= h + 0.006


# ── The page ─────────────────────────────────────────────────────────────────

def unique_draws(generate: Callable[[Random], Question], rng: Random) -> Callable[[], Optional[Question]]:
    """Draws from ``generate``, skipping any question whose stem is already on the
    sheet (the same question with its options reordered is still a repeat); None
    once ``REPEAT_TRIES`` draws in a row were all repeats (a set with few questions)."""
    seen: set[str] = set()

    def draw() -> Optional[Question]:
        for _ in range(REPEAT_TRIES):
            q = generate(rng)
            fingerprint = json.dumps(q.model_dump(mode="json", include={"stem"}),
                                     sort_keys=True, ensure_ascii=False)
            if fingerprint not in seen:
                seen.add(fingerprint)
                return q
        return None

    return draw


def plan_page(info: SheetInfo, draw: Callable[[], Optional[Question]],
              resolver: AssetResolver | None) -> Plan:
    """Fill one page: two columns if every probed question fits in one, else one."""
    _use_font(info.font)
    c = _scratch(info.font)
    top = _draw_header(c, info, info.title, 0)
    c.clear()
    number_w = _text_w("88.", NUMBER_PT, info.font) * 1.15 + 0.006

    def measure(q: Question, width: float) -> tuple[float, bool]:
        height = _draw_question(c, q, 88, LEFT, top, width, number_w, info.font, resolver)
        fits = c.right <= LEFT + width + 0.002
        c.clear()
        return height, fits

    probe = [q for q in (draw() for _ in range(PROBE)) if q is not None]
    half = (RIGHT - LEFT - GUTTER) / 2
    measured = [measure(q, half) for q in probe]
    columns = 2 if measured and all(fits for _, fits in measured) else 1
    width = half if columns == 2 else RIGHT - LEFT
    if columns == 1:
        measured = [measure(q, width) for q in probe]
    pending = [(q, h) for q, (h, _) in zip(probe, measured)]

    plan = Plan(columns=columns, width=width, top=top)
    column, y, misses = 0, top, 0
    while len(plan.questions) < MAX_QUESTIONS and misses < MAX_MISSES:
        if pending:
            q, h = pending.pop(0)
        else:
            q = draw()
            if q is None:
                break
            h = measure(q, width)[0]
        if y - h < BOTTOM and column + 1 < columns and y < top:
            column, y = column + 1, top
        if y - h < BOTTOM and plan.questions:
            misses += 1             # taller than what is left: try another question
            continue
        x = LEFT + column * (width + GUTTER)
        plan.placements.append(Placement(len(plan.questions), column, x, y, h))
        plan.questions.append(q)
        y -= h + QUESTION_GAP
    return plan


def render_sheet(info: SheetInfo, plan: Plan, resolver: AssetResolver | None) -> bytes:
    """The PDF: the planned page of problems, then their answers."""
    _use_font(info.font)
    figs: list = []
    try:
        fig, ax = _new_page(figs)
        page = _Canvas(fig, ax, info.font)
        _draw_header(page, info, info.title, len(plan.questions))
        number_w = _text_w("88.", NUMBER_PT, info.font) * 1.15 + 0.006
        for p in plan.placements:
            _draw_question(page, plan.questions[p.index], p.index + 1, p.x, p.y_top,
                           plan.width, number_w, info.font, resolver)
        _draw_footer(page, info, 1, 2)

        fig, ax = _new_page(figs)
        answers = _Canvas(fig, ax, info.font)
        _draw_answers(answers, info, plan.questions)
        _draw_footer(answers, info, 2, 2)

        buffer = io.BytesIO()
        with PdfPages(buffer) as pdf:
            for f in figs:
                pdf.savefig(f)
        return buffer.getvalue()
    finally:
        for f in figs:
            plt.close(f)
