"""Stage 1 — PDF in, readable artifacts out.

Thai exam PDFs are typeset, not scanned, so the text layer is usually good; what
it *cannot* carry is the figures, and on an olympiad sheet a third of the
questions live in their figures. So this module does three things:

* :func:`page_texts` / :func:`split_items` — text, then cut into numbered items.
* :func:`render_pages` / :func:`figure_pages` — PNGs of the pages that have
  artwork, for a human or a vision model to actually look at.
* :func:`read_cell_grid` / :func:`read_table_layout` — the two figure kinds that
  recur on Thai maths sheets and *must* be read exactly rather than eyeballed: a
  filled-cell grid (ตาราง with ช่องสีดำ) and a labelled table (ผัง with letters
  and icons). Getting one cell wrong here silently poisons every downstream
  answer, so both return data you can print and diff against the render.

Requires PyMuPDF (``fitz``); it is imported lazily so the rest of the pipeline —
and the generators, which never touch a PDF — work without it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


def _fitz():
    try:
        import fitz
    except ImportError as exc:                                # pragma: no cover
        raise RuntimeError(
            "sheetpipe extraction needs PyMuPDF: pip install pymupdf") from exc
    return fitz


# ── Text ─────────────────────────────────────────────────────────────────────

def page_texts(pdf: str | Path) -> list[str]:
    """Text of every page, in order, with Thai font damage repaired.

    See :mod:`.fontfix`. A clean PDF comes back as plain ``get_text()``.
    """
    from .fontfix import page_texts as repaired

    with _fitz().open(str(pdf)) as doc:
        return repaired(doc)


# A question opens with its number at the very start of a line: "12." / "12)".
_ITEM_HEAD = re.compile(r"^\s*(\d{1,2})[.)]\s*$|^\s*(\d{1,2})[.)]\s+(?=\S)",
                        re.MULTILINE)


def _ascending_runs(hits: list[tuple[int, object]]) -> list[list[tuple]]:
    """Every way to read ``hits`` as a run 1, 2, 3, … — one run per "1." found.

    ``hits`` is ``(number, position)`` in reading order; ``position`` only has to
    be orderable, so this serves both the text offsets of :func:`split_items` and
    the ``(page, y)`` coordinates of :func:`item_anchors`.

    From each candidate start, walk forward taking only the next number due, so
    a "3." inside a bulleted list is skipped because it is not what comes next.
    """
    runs: list[list[tuple]] = []
    for i, (num, start) in enumerate(hits):
        if num != 1:
            continue
        run, want = [(1, start)], 2
        for later_num, later_start in hits[i + 1:]:
            if later_num == want:
                run.append((later_num, later_start))
                want += 1
        runs.append(run)
    return runs


def _best_run(runs: list[list[tuple]], expect: int = 0) -> list[tuple]:
    """Pick the reading that is actually the questions.

    Matching ``expect`` wins first, then the longest run, then — the tie-break
    that matters — the one starting *later* in the document, since an exam's
    numbered instructions always precede the questions they describe.
    """
    return max(runs, key=lambda r: (expect and len(r) == expect, len(r), r[0][1]),
               default=[])


def split_items(pages: list[str], expect: int = 0) -> dict[int, str]:
    """Cut the page text into ``{question number: text}``.

    Numbers must run 1, 2, 3, … — that single rule handles the usual false
    positives (prices, years, sub-conditions) without a parser. But it is not
    enough on its own, because an exam's คำชี้แจง is itself a numbered list:
    on the POSN 2568 sheet the instructions run 1–8, so reading greedily from
    the first "1." consumed the instructions and then resumed at question 9 —
    and since 8 instructions + questions 9–30 is also 30 items, even the count
    check waved it through.

    So every possible run is built (:func:`_ascending_runs`) and the best one
    chosen: matching ``expect`` first, then the longest, then — the tie-break
    that separates the two 30-item readings above — the one starting *later* in
    the document, since instructions always precede the questions they describe.

    ``expect`` is the printed question count (from คำชี้แจง); when given, a
    mismatch raises rather than silently digesting 28 of 30 questions.
    """
    body = "\n".join(pages)
    hits = [(int(m.group(1) or m.group(2)), m.start())
            for m in _ITEM_HEAD.finditer(body)]
    best = _best_run(_ascending_runs(hits), expect)
    out: dict[int, str] = {}
    for i, (num, start) in enumerate(best):
        end = best[i + 1][1] if i + 1 < len(best) else len(body)
        out[num] = body[start:end].strip()
    if expect and len(out) != expect:
        raise ValueError(
            f"split_items found {len(out)} items, sheet declares {expect}; "
            f"missing {sorted(set(range(1, expect + 1)) - set(out))}")
    return out


def declared_item_count(pages: list[str]) -> int:
    """The question count the sheet states in its คำชี้แจง, or 0."""
    m = re.search(r"จำนวน\s*(\d+)\s*ข้อ", "\n".join(pages[:2]))
    return int(m.group(1)) if m else 0


# ── Figures ──────────────────────────────────────────────────────────────────

def figure_pages(pdf: str | Path, vector_min: int = 20) -> list[int]:
    """1-based numbers of pages carrying artwork — the pages to go look at.

    An embedded image is a reliable signal; a *few* vector paths are not, since
    fraction bars, header rules and table borders all show up as drawings. So
    vector-only pages count as figured once they pass ``vector_min`` paths. Err
    towards including a page: a false positive costs one glance, a false
    negative silently drops a question's geometry.
    """
    with _fitz().open(str(pdf)) as doc:
        return [i + 1 for i, p in enumerate(doc)
                if p.get_images() or len(p.get_drawings()) > vector_min]


def render_pages(pdf: str | Path, out_dir: str | Path,
                 pages: list[int] | None = None, dpi: int = 130) -> list[Path]:
    """Render pages to PNG for visual reading. ``pages`` is 1-based."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    written = []
    with _fitz().open(str(pdf)) as doc:
        for n in pages or range(1, doc.page_count + 1):
            path = out / f"p{n:02d}.png"
            doc[n - 1].get_pixmap(dpi=dpi).save(str(path))
            written.append(path)
    return written


def image_boxes(pdf: str | Path, page: int) -> list[tuple[float, ...]]:
    """Bounding boxes of the embedded images on a 1-based page.

    Icon-per-cell figures (the ผัง in §30 of the POSN sheet) are read from these
    boxes plus :func:`word_boxes`, not from pixels — the icons are separate
    images, so their centres *are* the cell centres.
    """
    with _fitz().open(str(pdf)) as doc:
        return [tuple(round(v, 2) for v in im["bbox"])
                for im in doc[page - 1].get_image_info()]


def word_rects(pdf: str | Path, page: int) -> list[tuple[float, float, float,
                                                          float, str]]:
    """``(x0, y0, x1, y1, word)`` for every word on a 1-based page."""
    with _fitz().open(str(pdf)) as doc:
        return [(w[0], w[1], w[2], w[3], w[4])
                for w in doc[page - 1].get_text("words")]


def word_boxes(pdf: str | Path, page: int) -> list[tuple[float, float, str]]:
    """``(x_centre, y_centre, word)`` for every word on a 1-based page."""
    return [((x0 + x1) / 2, (y0 + y1) / 2, w)
            for x0, y0, x1, y1, w in word_rects(pdf, page)]


# ── Per-item figures ─────────────────────────────────────────────────────────
#
# A figure question is not digested until its picture is, and a picture the
# reader never sees is a question with a hole in it. So the figures are cut out
# of the PDF as PNGs and tied to the question they belong to, which is what lets
# a generated item show the same diagram the sheet showed.
#
# Two facts make this tractable on a typeset Thai exam. Artwork is graphics —
# embedded images and vector paths — and never overlaps the text column, so
# clustering the graphics boxes finds the figures. And a figure always sits
# below the number of the question it illustrates, so the item numbers' own
# positions assign it.

#: A crop is padded by this many PDF points so nothing is clipped at the edge.
FIGURE_PAD = 6.0


@dataclass
class Figure:
    """One piece of artwork, tied to the question it illustrates."""

    item: int                                  # question number, 0 if unclaimed
    page: int                                  # 1-based
    box: tuple[float, float, float, float]     # PDF points, x0 y0 x1 y1
    words: list[str]                           # text printed inside the figure

    @property
    def numeric(self) -> bool:
        """Does the figure print a *quantity*?

        This is the question that decides whether the crop can be reused as-is.
        A lettered configuration diagram illustrates the *arrangement*, which
        every draw shares — so one crop serves them all. A figure with ``12``
        written on it illustrates one particular draw, and reusing it would put
        a number on screen that contradicts the stem.

        A digit only counts when the word opens with one: ``12``, ``12cm`` and
        ``3.5`` are measurements, while ``l₁``, ``A2`` and ``P₀`` are names that
        happen to contain a digit, and renaming a line is not a redraw.
        """
        return any(w[:1].isdigit() for w in self.words)


def _graphic_boxes(pdf: str | Path, page: int) -> list[tuple[float, ...]]:
    """Bounding boxes of everything drawn (not typeset) on a 1-based page."""
    with _fitz().open(str(pdf)) as doc:
        p = doc[page - 1]
        boxes = [tuple(im["bbox"]) for im in p.get_image_info()]
        boxes += [tuple(d["rect"]) for d in p.get_drawings()]
    return boxes


def _cluster(boxes: list[tuple[float, ...]], gap: float) -> list[tuple[float, ...]]:
    """Union boxes that touch when inflated by ``gap``, until nothing merges."""
    out = [tuple(float(v) for v in b) for b in boxes]
    merged = True
    while merged:
        merged = False
        for i in range(len(out)):
            for j in range(len(out) - 1, i, -1):
                a, b = out[i], out[j]
                if (a[0] - gap <= b[2] and b[0] - gap <= a[2]
                        and a[1] - gap <= b[3] and b[1] - gap <= a[3]):
                    out[i] = (min(a[0], b[0]), min(a[1], b[1]),
                              max(a[2], b[2]), max(a[3], b[3]))
                    out.pop(j)
                    merged = True
    return out


def figure_regions(pdf: str | Path, page: int, gap: float = 18.0,
                   min_side: float = 24.0) -> list[tuple[float, ...]]:
    """Bounding boxes of the figures on a 1-based page, top to bottom.

    ``gap`` is how far apart two pieces of one drawing may be and still count as
    one figure — 18 points holds a label to its arrow and the 128 separate paths
    of a ruled ผัง together. ``min_side`` then drops what is graphics but not a
    figure: a header rule is 400 points wide and half a point tall.
    """
    clusters = _cluster(_graphic_boxes(pdf, page), gap)
    return sorted((tuple(round(v, 2) for v in c) for c in clusters
                   if c[2] - c[0] >= min_side and c[3] - c[1] >= min_side),
                  key=lambda b: b[1])


# An item number opening a line: "12." / "12)".
_ANCHOR = re.compile(r"^(\d{1,2})[.)]$")


def item_anchors(pdf: str | Path, expect: int = 0) -> dict[int, tuple[int, float]]:
    """``{question number: (page, y)}`` — where each question starts on the page.

    Only line-opening numbers are candidates, and they are then filtered by the
    same ascending-run rule :func:`split_items` uses, so a numbered คำชี้แจง
    cannot hijack the numbering here either.
    """
    hits: list[tuple[int, tuple[int, float]]] = []
    with _fitz().open(str(pdf)) as doc:
        for pno, p in enumerate(doc, start=1):
            for w in p.get_text("words"):
                # words are (x0, y0, x1, y1, text, block, line, word_index)
                if w[7] != 0:
                    continue
                m = _ANCHOR.match(w[4])
                if m:
                    hits.append((int(m.group(1)), (pno, round(w[1], 2))))
    return dict(_best_run(_ascending_runs(hits), expect))


def figures(pdf: str | Path, expect: int = 0, **kwargs) -> list[Figure]:
    """Every figure on the sheet, each assigned to a question.

    A figure belongs to the last question that started at or above it — the
    reading order a person uses. One that precedes question 1 (a cover logo)
    gets ``item = 0`` and is dropped by :func:`extract_figures`.
    """
    anchors = item_anchors(pdf, expect)
    starts = sorted((pos, n) for n, pos in anchors.items())
    with _fitz().open(str(pdf)) as doc:
        page_count = doc.page_count
    out = []
    for page in range(1, page_count + 1):
        for box in figure_regions(pdf, page, **kwargs):
            above = [n for pos, n in starts if pos <= (page, box[1])]
            out.append(Figure(item=above[-1] if above else 0, page=page,
                              box=box, words=_words_in(pdf, page, box)))
    return out


def _words_in(pdf: str | Path, page: int, box: tuple[float, ...]) -> list[str]:
    """Text printed inside a box — the labels a figure carries."""
    x0, y0, x1, y1 = box
    return [w for x, y, w in word_boxes(pdf, page)
            if x0 <= x <= x1 and y0 <= y <= y1]


def crop_box(pdf: str | Path, fig: Figure,
             pad: float = FIGURE_PAD) -> tuple[float, float, float, float]:
    """The figure's box, padded — but pulled back off any neighbouring text.

    The pad exists so a label or an arrowhead is not shaved off at the edge. On
    a tight page it also reaches into the line above, and a crop that carries a
    sliver of the question's own text is a crop that shows numbers from the
    sheet's draw. So every word lying outside the figure clamps the pad back.

    A word that *straddles* the figure's own top or bottom edge clamps it too: a
    stray path — the tail of a dashed rule, an underline — can push the cluster
    a few points into the paragraph below, and a half-height line of Thai is the
    tell. An interior label never straddles the boundary, so it is left alone.
    """
    x0, y0, x1, y1 = fig.box
    r = [x0 - pad, y0 - pad, x1 + pad, y1 + pad]
    for wx0, wy0, wx1, wy1, _ in word_rects(pdf, fig.page):
        if wx1 > r[0] and wx0 < r[2]:                # vertically in the way
            if wy1 <= y0 or (wy0 < y0 < wy1):
                r[1] = max(r[1], wy1)
            elif wy0 >= y1 or (wy0 < y1 < wy1):
                r[3] = min(r[3], wy0)
        if wy1 > r[1] and wy0 < r[3]:                # horizontally in the way
            if wx1 <= x0:
                r[0] = max(r[0], wx1)
            elif wx0 >= x1:
                r[2] = min(r[2], wx0)
    return (r[0], r[1], r[2], r[3])


def crop_figure(pdf: str | Path, fig: Figure, dest: str | Path,
                dpi: int = 300, pad: float = FIGURE_PAD) -> Path:
    """Render one figure to its own PNG."""
    fitz = _fitz()
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with fitz.open(str(pdf)) as doc:
        clip = fitz.Rect(*crop_box(pdf, fig, pad))
        doc[fig.page - 1].get_pixmap(dpi=dpi, clip=clip).save(str(dest))
    return dest


def extract_figures(pdf: str | Path, out_dir: str | Path, expect: int = 0,
                    dpi: int = 300) -> list[Figure]:
    """Crop every question's figure to ``out_dir/itemNN.png``.

    Questions with more than one figure keep the largest — a second cluster on
    the same question is nearly always a stray mark, and if it is not, the
    manifest says so and the crop can be redone by hand.
    """
    out = Path(out_dir)
    best: dict[int, Figure] = {}
    for fig in figures(pdf, expect):
        if fig.item == 0:
            continue
        area = (fig.box[2] - fig.box[0]) * (fig.box[3] - fig.box[1])
        kept = best.get(fig.item)
        if kept is None or area > ((kept.box[2] - kept.box[0])
                                   * (kept.box[3] - kept.box[1])):
            best[fig.item] = fig
    for n, fig in sorted(best.items()):
        crop_figure(pdf, fig, out / f"item{n:02d}.png", dpi=dpi)
    return [best[n] for n in sorted(best)]


@dataclass
class CellGrid:
    """A ruled grid figure, read cell by cell."""

    rows: int
    cols: int
    filled: list[tuple[int, int]]        # (row, col), origin top-left

    def render(self) -> str:
        """ASCII art — print this and diff it against the page image."""
        f = set(self.filled)
        return "\n".join("".join("#" if (r, c) in f else "."
                                 for c in range(self.cols))
                         for r in range(self.rows))


def read_cell_grid(pdf: str | Path, page: int, clip: tuple[float, ...],
                   dpi: int = 400, line_frac: float = 0.85,
                   fill_frac: float = 0.7, inset: int = 15) -> CellGrid:
    """Read a ruled grid with solid-filled cells (ตารางที่มีช่องสีดำ).

    Finds the rules by looking for near-fully-dark pixel rows/columns, then
    samples the interior of each cell. ``clip`` is the figure's PDF-point
    bounding box, from :func:`image_boxes`.

    Always eyeball :meth:`CellGrid.render` against the page render before
    trusting it — one misread cell changes the answer and nothing downstream
    can notice.
    """
    import numpy as np

    fitz = _fitz()
    with fitz.open(str(pdf)) as doc:
        pix = doc[page - 1].get_pixmap(dpi=dpi, clip=fitz.Rect(*clip))
        arr = np.frombuffer(pix.samples, dtype=np.uint8)
        arr = arr.reshape(pix.height, pix.width, pix.n)
    dark = arr[:, :, :3].mean(axis=2) < 140
    rs, cs = np.where(dark.any(axis=1))[0], np.where(dark.any(axis=0))[0]
    sub = dark[rs.min():rs.max() + 1, cs.min():cs.max() + 1]

    def rules(profile) -> list[int]:
        """Collapse runs of adjacent near-solid lines to one index each."""
        idx = [i for i, v in enumerate(profile) if v > line_frac]
        out: list[int] = []
        for i in idx:
            if not out or i > out[-1] + 3:
                out.append(i)
        return out

    rl, cl = rules(sub.mean(axis=1)), rules(sub.mean(axis=0))
    if len(rl) < 2 or len(cl) < 2:
        raise ValueError(f"no grid rules found on page {page} at {clip}")
    filled = [(r, c)
              for r in range(len(rl) - 1) for c in range(len(cl) - 1)
              if sub[rl[r] + inset:rl[r + 1] - inset,
                     cl[c] + inset:cl[c + 1] - inset].mean() > fill_frac]
    return CellGrid(rows=len(rl) - 1, cols=len(cl) - 1, filled=filled)


def read_table_layout(pdf: str | Path, page: int, x_centres: list[float],
                      y_centres: list[float], tol: float = 12.0,
                      icon: str = "H") -> list[list[str]]:
    """Read a labelled table figure (ผัง) into a grid of cell contents.

    Cells are snapped to the given column/row centre coordinates: a word lands
    in the nearest cell, an embedded image becomes ``icon``. Blank stays ``""``.
    Get the centres from :func:`word_boxes` and :func:`image_boxes` — they are
    evenly spaced, so the two lists are obvious once printed.
    """
    grid = [["" for _ in x_centres] for _ in y_centres]

    def cell(x: float, y: float) -> tuple[int, int] | None:
        cs = [i for i, v in enumerate(x_centres) if abs(v - x) <= tol]
        rs = [i for i, v in enumerate(y_centres) if abs(v - y) <= tol]
        return (rs[0], cs[0]) if cs and rs else None

    for x0, y0, x1, y1 in image_boxes(pdf, page):
        at = cell((x0 + x1) / 2, (y0 + y1) / 2)
        if at:
            grid[at[0]][at[1]] = icon
    for x, y, word in word_boxes(pdf, page):
        at = cell(x, y)
        if at:
            grid[at[0]][at[1]] = (grid[at[0]][at[1]] + word).strip()
    return grid
