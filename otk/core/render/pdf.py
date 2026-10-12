"""Render a worksheet to an A4 PDF (drill-sheet layout) with matplotlib.

Consumes the block model: each problem's stem is a list of blocks (a Thai prompt,
a math expression, and/or an image with arrow markers), and the answer key
renders each question's correct choice. matplotlib is *not* thread-safe — callers
serialize rendering (the API holds a lock).

Three extra modes layer on the same drawing code:
* **Images** — pass an ``asset_resolver`` (id -> file path) and image questions
  render the diagram + arrow markers instead of alt text.
* **Choices** — ``Worksheet.show_choices`` prints each question's options under
  its stem, which is what makes a multiple-choice type answerable on paper.
* **Edit mode** — ``render_edit_preview`` returns page-1 PNG plus clickable
  ``regions`` (page-fraction rectangles for each editable header field), which
  the web builder overlays as hotspots.

Prompts and options are wrapped to their column: Thai runs long, and an
unwrapped stem used to cross into the next column and off the page.
"""

from __future__ import annotations

import datetime
import io
import math
from functools import lru_cache
from pathlib import Path
from typing import Callable, Optional

import matplotlib

matplotlib.use("Agg")
matplotlib.rcParams["mathtext.fontset"] = "cm"

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.figure import Figure
from matplotlib.patches import FancyBboxPatch, Rectangle

from ..question import Question
from ..worksheet import Worksheet

A4 = (8.27, 11.69)

MARGIN_L = 0.08
MARGIN_R = 0.92
GRID_BOTTOM = 0.075
FOOTER_Y = 0.035

INK = "#1a1a1a"
FAINT = "#999999"
RULE = "#444444"
ANSWER_LINE = "#555555"
KEY_INK = "#20601f"
ARROW = "#b00000"
PLACEHOLDER = "#b9c2cc"          # gray "click to fill" hints in edit mode

_KEY_ROWS_PER_COL = 25

# Thai option labels, the convention on a Thai multiple-choice sheet.
_CHOICE_LABELS = "กขคงจฉชฌ"
_CHOICE_FONTSIZE = 9.0

# What a diagram is given in the flow layout, where height is measured up front
# rather than divided out of a fixed cell.
_FLOW_IMAGE_H = 0.085
_PROMPT_FONTSIZE = 8.5

# Thai stacks vowels and tone marks on the preceding consonant. Breaking a long
# run between a base character and its mark would strand the mark on the next
# line, so character-level wrapping steps back past these.
_THAI_COMBINING = set("ัิีึืฺุู"
                      "็่้๊๋์ํ๎")

# id -> file path (or None). Lets the renderer resolve ImageBlock.asset_id
# without knowing about the API's data dir.
AssetResolver = Callable[[str], Optional[Path]]

# Thai placeholders for empty header fields, shown only in edit mode.
_PLACEHOLDERS = {
    "school_name": "+ ชื่อโรงเรียน",
    "title": "หัวข้อชีท",
    "subtitle": "+ คำอธิบายใต้ชื่อ",
    "level": "ระดับ",
    "instructions": "+ คำสั่ง",
}


# ── Block → renderable ───────────────────────────────────────────────────────

def _stem_parts(q: Question) -> tuple[str, str]:
    """(prompt text, math tex) for the non-image path (image alt as a fallback)."""
    prompt = " ".join(b.text for b in q.stem if b.kind == "text")
    mathtex = " ".join(b.tex for b in q.stem if b.kind == "math")
    if not prompt:
        prompt = " ".join(b.alt for b in q.stem if b.kind == "image" and b.alt)
    return prompt, mathtex


def _code_lines(q: Question) -> list[str]:
    """Every line of the stem's code blocks, exactly as written."""
    return [line for b in q.stem if b.kind == "code" for line in b.code.split("\n")]


_CODE_FONTSIZE = 8.0
_CODE_PAD = 0.006


def _code_h(lines: list[str]) -> float:
    # 1.2 line spacing, as drawn; the last line needs its descent as well.
    return (len(lines) * 1.2 + 0.3) * _CODE_FONTSIZE / (A4[1] * 72) + 2 * _CODE_PAD


def _draw_code(ax, lines: list[str], x: float, y_top: float, width: float) -> float:
    """A program on a pale panel in a monospace font, spaces kept; return its height.

    Code is never wrapped: a broken line would change what the program means.
    """
    height = _code_h(lines)
    ax.add_patch(plt.Rectangle((x, y_top - height), width, height, facecolor="#f3f5f8",
                               edgecolor="#c9d0da", linewidth=0.6))
    ax.text(x + _CODE_PAD, y_top - _CODE_PAD, "\n".join(lines), family="monospace",
            fontsize=_CODE_FONTSIZE, color=INK, ha="left", va="top", linespacing=1.2)
    return height


def _content_str(content) -> tuple[bool, str]:
    """(is_math, string) for a choice's content — used by the answer key."""
    if content and all(b.kind == "math" for b in content):
        return True, " ".join(b.tex for b in content)
    parts = [b.tex if b.kind == "math" else getattr(b, "text", getattr(b, "code", ""))
             for b in content]
    return False, " ".join(parts)


# ── Header / footer ──────────────────────────────────────────────────────────

def _apply_font(config: Worksheet) -> None:
    if config.font_family:
        base = matplotlib.rcParams["font.sans-serif"]
        matplotlib.rcParams["font.sans-serif"] = (
            [config.font_family] + [f for f in base if f != config.font_family])


def _draw_header(fig, ax, config: Worksheet, page: int,
                 regions: list | None = None) -> float:
    """Draw the header; return the y where problems may start. When ``regions``
    is a list, run in edit mode: append a hotspot rect per editable field and
    show gray placeholders for empty ones."""
    editing = regions is not None

    def mark(key: str, x0: float, y_bot: float, x1: float, y_top: float) -> None:
        if editing:
            regions.append({"key": key, "x": round(x0, 4), "y": round(1 - y_top, 4),
                            "w": round(x1 - x0, 4), "h": round(y_top - y_bot, 4)})

    y = 0.965
    text_x = MARGIN_L
    box_h = 0.055

    logo = Path(config.logo) if config.logo else None
    if logo is not None and logo.exists():
        img = plt.imread(str(logo))
        box_w = box_h * (img.shape[1] / img.shape[0]) * (A4[1] / A4[0])
        ax_logo = fig.add_axes([MARGIN_L, y - box_h + 0.005, box_w, box_h])
        ax_logo.imshow(img)
        ax_logo.set_axis_off()
        text_x = MARGIN_L + box_w + 0.02

    if config.school_name or editing:
        ax.text(text_x, y, config.school_name or _PLACEHOLDERS["school_name"],
                fontsize=9, color=FAINT if config.school_name else PLACEHOLDER,
                va="top", ha="left")
        mark("school_name", text_x, y - 0.013, MARGIN_R - 0.11, y)
        y -= 0.016

    ax.text(text_x, y, config.title or _PLACEHOLDERS["title"], fontsize=17,
            fontweight="bold", color=INK if config.title else PLACEHOLDER,
            va="top", ha="left")
    mark("title", text_x, y - 0.026, MARGIN_R - 0.11, y)
    y -= 0.028

    if config.subtitle or editing:
        ax.text(text_x, y, config.subtitle or _PLACEHOLDERS["subtitle"],
                fontsize=10, color="#555555" if config.subtitle else PLACEHOLDER,
                va="top", ha="left")
        mark("subtitle", text_x, y - 0.016, MARGIN_R - 0.11, y)
        y -= 0.018

    if config.level or editing:
        badge = FancyBboxPatch(
            (MARGIN_R - 0.09, 0.925), 0.09, 0.042, boxstyle="round,pad=0.006",
            facecolor="#f2f2f2" if config.level else "none",
            edgecolor=INK if config.level else PLACEHOLDER, linewidth=1.2,
            transform=ax.transAxes)
        if not config.level:
            badge.set_linestyle((0, (4, 3)))
        ax.add_patch(badge)
        ax.text(MARGIN_R - 0.045, 0.946, config.level or _PLACEHOLDERS["level"],
                fontsize=13 if config.level else 8,
                fontweight="bold" if config.level else "normal",
                ha="center", va="center", color=INK if config.level else PLACEHOLDER)
        mark("level", MARGIN_R - 0.096, 0.919, MARGIN_R + 0.006, 0.973)

    if page == 1 and (config.instructions or editing):
        ax.text(MARGIN_L, y, config.instructions or _PLACEHOLDERS["instructions"],
                fontsize=10, color=INK if config.instructions else PLACEHOLDER,
                va="top", ha="left")
        mark("instructions", MARGIN_L, y - 0.016, MARGIN_R, y)
        y -= 0.020

    if config.show_name_date:
        y -= 0.012
        line_y = y - 0.012
        x = MARGIN_L
        for label, width in zip(config.field_labels, [0.26, 0.14, 0.10, 0.10]):
            ax.text(x, line_y, label, fontsize=10, color=INK, va="bottom")
            lx0 = x + 0.012 * len(label) + 0.008
            ax.plot([lx0, x + width], [line_y - 0.002, line_y - 0.002],
                    color=INK, linewidth=0.8)
            x += width + 0.03
        y = line_y - 0.014

    ax.plot([MARGIN_L, MARGIN_R], [y, y], color=RULE, linewidth=1.4)
    return y - 0.012


def _draw_footer(ax, config: Worksheet, page: int, total: int) -> None:
    ax.plot([MARGIN_L, MARGIN_R], [GRID_BOTTOM - 0.01, GRID_BOTTOM - 0.01],
            color=RULE, linewidth=0.8)
    if config.school_name:
        ax.text(MARGIN_L, FOOTER_Y, config.school_name, fontsize=8, color=FAINT,
                ha="left", va="center")
    ax.text(0.5, FOOTER_Y, f"{page} / {total}", fontsize=9, color=FAINT,
            ha="center", va="center")
    ax.text(MARGIN_R, FOOTER_Y, datetime.date.today().isoformat(), fontsize=8,
            color=FAINT, ha="right", va="center")


# ── Problem cells ────────────────────────────────────────────────────────────

def _number_offset(last_number: int) -> float:
    return 0.013 + 0.008 * (2 + len(str(last_number)))


@lru_cache(maxsize=1)
def _measure_fig():
    """A throwaway A4 figure used only to measure text. Widths are returned as
    a fraction of the page, which is dpi-independent, so one figure serves both
    the PDF and PNG paths."""
    fig = Figure(figsize=A4)
    FigureCanvasAgg(fig)
    return fig


@lru_cache(maxsize=8192)
def _text_w(text: str, fontsize: float, font: str) -> float:
    """Rendered width of ``text``, as a fraction of the page width.

    ``font`` is part of the key rather than the computation: the active font is
    an rcParam, so two worksheets in one process would otherwise share a
    measurement taken under the wrong typeface.
    """
    fig = _measure_fig()
    artist = fig.text(0, 0, text, fontsize=fontsize)
    width = artist.get_window_extent(fig.canvas.get_renderer()).width / fig.bbox.width
    artist.remove()
    return width


def _break_point(text: str, fontsize: float, font: str, max_w: float) -> int:
    """How many characters of ``text`` fit in ``max_w`` (at least one)."""
    lo, hi = 1, len(text)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if _text_w(text[:mid], fontsize, font) <= max_w:
            lo = mid
        else:
            hi = mid - 1
    while lo < len(text) and text[lo] in _THAI_COMBINING:
        lo -= 1
    return max(lo, 1)


def _wrap(text: str, fontsize: float, max_w: float, font: str) -> list[str]:
    """Split ``text`` into lines no wider than ``max_w`` (a page fraction).

    Thai does not put spaces between words, so spaces are preferred break
    points but not the only ones: a run with none is cut by character.
    """
    if not text or max_w <= 0:
        return [text] if text else []
    if _text_w(text, fontsize, font) <= max_w:
        return [text]

    lines: list[str] = []
    current = ""
    for word in text.split(" "):
        candidate = f"{current} {word}" if current else word
        if current and _text_w(candidate, fontsize, font) > max_w:
            lines.append(current)
            current = word
        else:
            current = candidate
        while _text_w(current, fontsize, font) > max_w and len(current) > 1:
            cut = _break_point(current, fontsize, font, max_w)
            lines.append(current[:cut])
            current = current[cut:]
    if current:
        lines.append(current)
    return lines


def _one_line(text: str, fontsize: float, max_w: float, font: str) -> str:
    """``text`` cut to a single line of ``max_w``, with an ellipsis if cut."""
    if not text or _text_w(text, fontsize, font) <= max_w:
        return text
    cut = _break_point(text, fontsize, font, max_w - _text_w("…", fontsize, font))
    return text[:cut].rstrip() + "…"


def _draw_wrapped(fig, ax, text: str, x: float, y_top: float, max_w: float,
                  fontsize: float, color: str, config: Worksheet) -> float:
    """Draw ``text`` wrapped to ``max_w`` from ``y_top`` down; return its height."""
    lines = _wrap(text, fontsize, max_w, config.font_family)
    artist = ax.text(x, y_top, "\n".join(lines), fontsize=fontsize, color=color,
                     ha="left", va="top", linespacing=1.4)
    return max(len(lines) * _line_h(fontsize), _drawn_h(fig, artist))


def _line_h(fontsize: float) -> float:
    """One line of text at ``fontsize``, as a fraction of the page height."""
    return fontsize * 1.35 / (A4[1] * 72)


def _drawn_h(fig, artist) -> float:
    """The rendered height of ``artist``, as a fraction of the page height.

    Thai fonts stack vowels and tone marks above and below the line, so Loma
    and Garuda run taller than the 1.35 line that fits Latin text.
    """
    return artist.get_window_extent(fig.canvas.get_renderer()).height / fig.bbox.height


def _draw_answer_space(ax, x0: float, y_mid: float, cell_w: float, cell_h: float,
                       config: Worksheet, x_from: float) -> None:
    x1 = x0 + cell_w * 0.94
    if config.answer_style == "none" or x_from >= x1:
        return
    if config.answer_style == "line":
        ax.plot([x_from, x1], [y_mid - 0.008, y_mid - 0.008],
                color=ANSWER_LINE, linewidth=0.9)
    elif config.answer_style == "box":
        bh = min(cell_h * 0.62, 0.045)
        ax.add_patch(Rectangle((x_from, y_mid - bh / 2), x1 - x_from, bh,
                               facecolor="none", edgecolor=ANSWER_LINE, linewidth=0.9))


# ── Choices ──────────────────────────────────────────────────────────────────

_CHOICE_INDENT = 0.022
_CHOICE_GAP = 0.004


def _choice_lines(q: Question, avail_w: float, config: Worksheet) -> list[list[str]]:
    """The wrapped lines of every option, in order. Math options are left on one
    line: a TeX string has no sensible break points."""
    out: list[list[str]] = []
    for choice in q.choices:
        is_math, text = _content_str(choice.content)
        if is_math:
            out.append([f"${text}$"])
        else:
            out.append(_wrap(text, _CHOICE_FONTSIZE,
                             avail_w - _CHOICE_INDENT, config.font_family))
    return out


def _choices_h(q: Question, avail_w: float, config: Worksheet) -> float:
    """Height the printed options will need, for laying out what sits above."""
    lines = sum(len(ls) for ls in _choice_lines(q, avail_w, config))
    return lines * _line_h(_CHOICE_FONTSIZE) * 1.4 + len(q.choices) * _CHOICE_GAP


def _draw_choices(fig, ax, q: Question, x: float, y_top: float, avail_w: float,
                  config: Worksheet) -> None:
    """Print ``ก. … ข. …`` under the stem so the question can be answered on
    paper. The options replace the answer blank — the student rings a letter."""
    y = y_top
    for i, lines in enumerate(_choice_lines(q, avail_w, config)):
        label = f"{_CHOICE_LABELS[i]}." if i < len(_CHOICE_LABELS) else f"{i + 1}."
        ax.text(x, y, label, fontsize=_CHOICE_FONTSIZE, color=INK,
                ha="left", va="top")
        artist = ax.text(x + _CHOICE_INDENT, y, "\n".join(lines),
                         fontsize=_CHOICE_FONTSIZE, color=INK, ha="left",
                         va="top", linespacing=1.4)
        y -= max(len(lines) * _line_h(_CHOICE_FONTSIZE) * 1.4,
                 _drawn_h(fig, artist)) + _CHOICE_GAP


def _image_dims(img_path: Path, cell_w: float, target_h: float) -> tuple[float, float]:
    """(width, height) for a diagram at ``target_h``, capped to half the column."""
    img = plt.imread(str(img_path))
    aspect = (img.shape[1] / img.shape[0]) * (A4[1] / A4[0])
    height, width = target_h, target_h * aspect
    if width > cell_w * 0.5:
        width = cell_w * 0.5
        height = width / aspect
    return width, height


def _draw_image_problem(fig, ax, q: Question, block, img_path: Path,
                        x0: float, y_top: float, y_mid: float,
                        cell_w: float, cell_h: float, body_x: float,
                        config: Worksheet, avail_w: float,
                        fixed_h: float | None = None) -> float:
    """Draw an image question; return the y below the picture.

    ``fixed_h`` is the flow layout's pre-measured diagram height. Without it
    the picture is centred in whatever the fixed cell has left, as the
    drill-sheet layout has always done.
    """
    # Only a real text prompt is printed; the image's alt is for screen readers,
    # and the arrow + answer line already imply "name the marked part".
    prompt = " ".join(b.text for b in q.stem if b.kind == "text")

    # The prompt takes a line across the top of the cell and the picture gets
    # what is left below it. Both used to be placed from the cell's midpoint,
    # which drew the image straight over the words.
    # Padding is kept tight here, unlike the text-only cell: the prompt line has
    # to come out of the same cell, and on a dense sheet that is most of it.
    top = y_top - cell_h * 0.05
    if prompt:
        top -= _draw_wrapped(fig, ax, prompt, body_x, top, avail_w,
                             _PROMPT_FONTSIZE, "#444444", config)
        # Loma and Garuda hang their lower vowels a little below the measured
        # box; a quarter line keeps the picture clear of them.
        top -= _line_h(_PROMPT_FONTSIZE) * 0.25
    if fixed_h is not None:
        width, height = _image_dims(img_path, cell_w, fixed_h)
        y_bottom = top - height
    else:
        bottom = y_top - cell_h * 0.97
        # The picture gets what the prompt left of the cell, however little: a
        # floor here pushed it over the prompt above or into the cell below.
        band = max(top - bottom, 0.004)
        width, height = _image_dims(img_path, cell_w, min(band * 0.98, 0.10))
        y_bottom = (top + bottom) / 2 - height / 2

    ax_in = fig.add_axes([body_x, y_bottom, width, height])
    ax_in.imshow(plt.imread(str(img_path)))
    ax_in.set_axis_off()
    for m in block.markers:
        ax_in.annotate("", xy=(m.x, 1 - m.y), xytext=(m.x + 0.16, 1 - m.y + 0.16),
                       xycoords="axes fraction", annotation_clip=False,
                       arrowprops=dict(arrowstyle="-|>", color=ARROW, lw=1.4))

    if fixed_h is None:
        _draw_answer_space(ax, x0, y_bottom + height / 2, cell_w, cell_h, config,
                           x_from=body_x + width + 0.02)
    return y_bottom


def _cell_pads(config: Worksheet, cell_h: float) -> tuple[float, float]:
    """(padding above the stem, gap between stacked parts) for a cell.

    The drill grid scales its padding with the cell; the flow layout cannot —
    there the cell *is* the content, so a proportional pad would grow with the
    very thing it surrounds.
    """
    if config.show_choices:
        return 0.010, 0.007
    return cell_h * 0.05, cell_h * 0.04


def _prompt_h(prompt: str, avail_w: float, config: Worksheet) -> float:
    lines = _wrap(prompt, _PROMPT_FONTSIZE, avail_w, config.font_family)
    return len(lines) * _line_h(_PROMPT_FONTSIZE) * 1.4


def _question_h(q: Question, cell_w: float, body_offset: float,
                config: Worksheet, asset_resolver: AssetResolver | None) -> float:
    """Height a flow-laid-out question needs, measured the way it is drawn."""
    avail_w = cell_w * 0.94 - body_offset
    pad, gap = _cell_pads(config, 0.0)
    height = pad

    images = [b for b in q.stem if b.kind == "image"]
    img_path = asset_resolver(images[0].asset_id) if images and asset_resolver else None
    if img_path is not None:
        prompt = " ".join(b.text for b in q.stem if b.kind == "text")
        if prompt:
            height += _prompt_h(prompt, avail_w, config)
        height += _image_dims(img_path, cell_w, _FLOW_IMAGE_H)[1] + gap
    else:
        prompt, mathtex = _stem_parts(q)
        if prompt:
            height += _prompt_h(prompt, avail_w, config) + gap
        if _code_lines(q):
            height += _code_h(_code_lines(q)) + gap
        if mathtex:
            height += _line_h(config.problem_fontsize) * 1.3 + gap
    return height + _choices_h(q, avail_w, config) + gap


def _draw_problem(fig, ax, q: Question, number: int, x0: float, y_top: float,
                  cell_w: float, cell_h: float, config: Worksheet,
                  body_offset: float, asset_resolver: AssetResolver | None) -> None:
    y_mid = y_top - cell_h * 0.5
    body_x = x0 + body_offset
    avail_w = cell_w * 0.94 - body_offset
    pad, gap = _cell_pads(config, cell_h)
    top = y_top - pad

    images = [b for b in q.stem if b.kind == "image"]
    img_path = asset_resolver(images[0].asset_id) if images and asset_resolver else None
    if img_path is not None:
        _draw_number(ax, number, x0, top if config.show_choices else y_mid,
                     from_top=config.show_choices)
        below = _draw_image_problem(
            fig, ax, q, images[0], img_path, x0, y_top, y_mid, cell_w, cell_h,
            body_x, config, avail_w,
            fixed_h=_FLOW_IMAGE_H if config.show_choices else None)
        if config.show_choices:
            _draw_choices(fig, ax, q, body_x, below - gap, avail_w, config)
        return

    prompt, mathtex = _stem_parts(q)

    # A wrapped prompt or a list of options grows downward, so those cells are
    # laid out from the top. A bare expression keeps the vertically centred
    # drill layout it has always had.
    code_lines = _code_lines(q)
    from_top = bool(prompt) or bool(code_lines) or config.show_choices
    _draw_number(ax, number, x0, top if from_top else y_mid, from_top=from_top)

    if prompt:
        top -= _draw_wrapped(fig, ax, prompt, body_x, top, avail_w,
                             _PROMPT_FONTSIZE, "#666666", config) + gap
    if code_lines:
        top -= _draw_code(ax, code_lines, body_x, top, avail_w * 0.9) + gap
    if mathtex:
        add_eq = (config.answer_style != "none" and "=" not in mathtex
                  and not prompt and not config.show_choices)
        eq = r"\ =" if add_eq else ""
        artist = ax.text(body_x, top if from_top else y_mid, f"${mathtex}{eq}$",
                         fontsize=config.problem_fontsize, color=INK, ha="left",
                         va="top" if from_top else "center")
        if from_top:
            top -= _drawn_h(fig, artist) + gap

    if config.show_choices:
        _draw_choices(fig, ax, q, body_x, top, avail_w, config)
        return
    _draw_answer_space(ax, x0, y_mid if not prompt else top + cell_h * 0.02,
                       cell_w, cell_h, config, x_from=x0 + cell_w * 0.58)


def _draw_number(ax, number: int, x0: float, y: float, from_top: bool) -> None:
    ax.text(x0, y, f"({number})", fontsize=11, fontweight="bold", color=INK,
            ha="left", va="top" if from_top else "center")


# ── Pages ────────────────────────────────────────────────────────────────────

def _new_page(figs: list):
    fig = plt.figure(figsize=A4)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_axis_off()
    figs.append(fig)
    return fig, ax


def _draw_problem_grid(fig, ax, chunk: list[Question], config: Worksheet,
                       grid_top: float, start_number: int,
                       asset_resolver: AssetResolver | None) -> int:
    rows = math.ceil(config.problems_per_page / config.columns)
    cell_h = (grid_top - GRID_BOTTOM) / rows
    cell_w = (MARGIN_R - MARGIN_L) / config.columns
    body_offset = _number_offset(start_number + len(chunk))
    number = start_number
    for i, q in enumerate(chunk):
        number += 1
        col, row = i // rows, i % rows              # fill down, then across
        x0 = MARGIN_L + col * cell_w
        y_top = grid_top - row * cell_h
        _draw_problem(fig, ax, q, number, x0, y_top, cell_w, cell_h, config,
                      body_offset, asset_resolver)
    return number


# ── Flow layout (printed choices) ────────────────────────────────────────────
#
# A grid of equal cells works for drills, where every problem is one line. Once
# the options are printed each question is a different height, so the page is
# packed by measured height instead and ``problems_per_page`` stops applying.

def _grid_tops(config: Worksheet) -> tuple[float, float]:
    """Where problems may start on (page 1, later pages) — page 1 also carries
    the instructions, so it starts lower."""
    tops = []
    for page in (1, 2):
        fig, ax = _new_page([])
        tops.append(_draw_header(fig, ax, config, page))
        plt.close(fig)
    return tops[0], tops[1]


def _paginate_flow(config: Worksheet, questions: list[Question],
                   asset_resolver: AssetResolver | None,
                   first_top: float | None = None) -> list[list[tuple]]:
    """Pack questions into pages as ``(index, column, y_top, height)``.

    ``first_top`` overrides where page 1 starts, for the edit preview: its
    header is taller, because empty fields still show a placeholder.
    """
    cell_w = (MARGIN_R - MARGIN_L) / config.columns
    body_offset = _number_offset(len(questions))
    heights = [_question_h(q, cell_w, body_offset, config, asset_resolver)
               for q in questions]

    measured_first, later_top = _grid_tops(config)
    first_top = measured_first if first_top is None else first_top
    pages: list[list[tuple]] = []
    i = 0
    while i < len(questions):
        grid_top = first_top if not pages else later_top
        page: list[tuple] = []
        for col in range(config.columns):
            y = grid_top
            while i < len(questions) and y - heights[i] >= GRID_BOTTOM:
                page.append((i, col, y, heights[i]))
                y -= heights[i]
                i += 1
        if not page:                    # one question taller than a whole page
            page.append((i, 0, grid_top, heights[i]))
            i += 1
        pages.append(page)
    return pages


def _draw_flow_page(fig, ax, page: list[tuple], questions: list[Question],
                    config: Worksheet,
                    asset_resolver: AssetResolver | None) -> None:
    cell_w = (MARGIN_R - MARGIN_L) / config.columns
    body_offset = _number_offset(len(questions))
    for index, col, y_top, height in page:
        _draw_problem(fig, ax, questions[index], index + 1,
                      MARGIN_L + col * cell_w, y_top, cell_w, height, config,
                      body_offset, asset_resolver)


def _answers_per_key_page(config: Worksheet) -> int:
    return config.answer_key_columns * _KEY_ROWS_PER_COL


def _render_answer_key(figs, config: Worksheet, questions: list[Question],
                       page_start: int, total_pages: int) -> None:
    per_page = _answers_per_key_page(config)
    chunks = [questions[i:i + per_page] for i in range(0, len(questions), per_page)]
    numbering = 0
    for ci, chunk in enumerate(chunks):
        fig, ax = _new_page(figs)
        title = config.answer_key_title or f"{config.title} — เฉลย"
        ax.text(MARGIN_L, 0.955, title, fontsize=15, fontweight="bold",
                color=INK, va="top")
        ax.plot([MARGIN_L, MARGIN_R], [0.925, 0.925], color=RULE, linewidth=1.2)
        rows = _KEY_ROWS_PER_COL
        grid_top = 0.905
        cell_h = (grid_top - GRID_BOTTOM) / rows
        cell_w = (MARGIN_R - MARGIN_L) / config.answer_key_columns
        body_offset = _number_offset(numbering + len(chunk))
        for i, q in enumerate(chunk):
            numbering += 1
            col, row = i // rows, i % rows
            x0 = MARGIN_L + col * cell_w
            y_mid = grid_top - row * cell_h - cell_h / 2
            ax.text(x0, y_mid, f"({numbering})", fontsize=10, fontweight="bold",
                    color=INK, ha="left", va="center")
            is_math, s = _content_str(q.choices[q.answer].content)
            text_x = x0 + body_offset
            # With the options printed on the sheet the pupil writes a letter,
            # so the key leads with the letter. The wording then only has to
            # identify the option while marking, and is cut to the column
            # rather than sprawling across the neighbouring ones.
            if config.show_choices and q.answer < len(_CHOICE_LABELS):
                ax.text(text_x, y_mid, f"{_CHOICE_LABELS[q.answer]}.", fontsize=11,
                        fontweight="bold", color=KEY_INK, ha="left", va="center")
                text_x += 0.022
                if not is_math:
                    s = _one_line(s, 10, x0 + cell_w * 0.94 - text_x,
                                  config.font_family)
            ax.text(text_x, y_mid, f"${s}$" if is_math else s,
                    fontsize=10 if config.show_choices else 11,
                    color=KEY_INK, ha="left", va="center")
        _draw_footer(ax, config, page_start + ci, total_pages)


def _build_figures(config: Worksheet, questions: list[Question],
                   asset_resolver: AssetResolver | None = None) -> list:
    _apply_font(config)
    flow = _paginate_flow(config, questions, asset_resolver) if config.show_choices else None
    per_page = config.problems_per_page
    chunks = ([[questions[i] for i, *_ in page] for page in flow] if flow
              else [questions[i:i + per_page]
                    for i in range(0, len(questions), per_page)])
    n_key = (math.ceil(len(questions) / _answers_per_key_page(config))
             if config.answer_key and questions else 0)
    total_pages = len(chunks) + n_key

    figs: list = []
    number = 0
    for page_i, chunk in enumerate(chunks, start=1):
        fig, ax = _new_page(figs)
        grid_top = _draw_header(fig, ax, config, page_i)
        _draw_footer(ax, config, page_i, total_pages)
        if flow:
            _draw_flow_page(fig, ax, flow[page_i - 1], questions, config,
                            asset_resolver)
        else:
            number = _draw_problem_grid(fig, ax, chunk, config, grid_top, number,
                                        asset_resolver)
    if config.answer_key and questions:
        _render_answer_key(figs, config, questions, len(chunks) + 1, total_pages)
    return figs


def render_pdf(config: Worksheet, questions: list[Question], out,
               asset_resolver: AssetResolver | None = None) -> None:
    """Write a multi-page PDF to a path or a writable binary file object."""
    if not hasattr(out, "write"):
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
    figs = _build_figures(config, questions, asset_resolver)
    with PdfPages(out) as pdf:
        for fig in figs:
            pdf.savefig(fig)
            plt.close(fig)


def render_page_png(config: Worksheet, questions: list[Question], page: int = 0,
                    dpi: int = 90, asset_resolver: AssetResolver | None = None) -> bytes:
    """Render one page as PNG bytes."""
    figs = _build_figures(config, questions, asset_resolver)
    buf = io.BytesIO()
    figs[min(page, len(figs) - 1)].savefig(buf, format="png", dpi=dpi,
                                           facecolor="white")
    for fig in figs:
        plt.close(fig)
    return buf.getvalue()


def render_edit_preview(config: Worksheet, questions: list[Question],
                        asset_resolver: AssetResolver | None = None,
                        dpi: int = 100) -> tuple[bytes, list]:
    """Page-1 PNG plus clickable header ``regions`` for the web builder. Tolerates
    an empty question list (header-only page)."""
    _apply_font(config)
    figs: list = []
    fig, ax = _new_page(figs)
    regions: list = []
    grid_top = _draw_header(fig, ax, config, page=1, regions=regions)
    per_page = config.problems_per_page
    if config.show_choices and questions:
        pages = _paginate_flow(config, questions, asset_resolver,
                               first_top=grid_top)
        _draw_footer(ax, config, 1, len(pages))
        _draw_flow_page(fig, ax, pages[0], questions, config, asset_resolver)
    else:
        n_sheet = math.ceil(len(questions) / per_page) if questions else 1
        _draw_footer(ax, config, 1, n_sheet)
        _draw_problem_grid(fig, ax, questions[:per_page], config, grid_top, 0,
                           asset_resolver)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=dpi, facecolor="white")
    plt.close(fig)
    return buf.getvalue(), regions
