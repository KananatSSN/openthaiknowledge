"""Math sets that are read off a drawing: clocks, protractors, shaded fractions,
labelled figures, charts, graphs, solids and nets.

Until this module no ป.1–ม.3 set showed a picture. Clocks were described in
words ("เข็มสั้นอยู่ระหว่างเลข 9 กับ 10"), charts were rows of ●, and a
rectangle's sides were stated in the sentence. Each family below is a finite
tuple of specs; ``otk/pictures/math_diagrams.py`` draws one
PNG per spec, and a question draws a spec, shows its PNG and computes the answer
from the same spec — so the picture and the answer cannot disagree.

As in ``ms1_diagrams``, nothing Thai is drawn into a PNG (the bundled font has
none): labels are numbers, ASCII units ("cm", "m") and letters (A–E, x, y).
Category names for charts are given in the stem against the letters. Alt text
describes the drawing without the value being asked for, so a screen reader —
or an image that fails to load — never answers the question.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import image as content_image
from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.question import GeneratedQuestion
from otk.kit import story as _story


def _img(asset: str, alt: str):
    return content_image(asset, alt=alt)


def _neg(n: int) -> str:
    """-3 -> n3, for asset ids (letters, digits, _ . - only)."""
    return f"n{-n}" if n < 0 else str(n)


def _math_q(stem: list, correct: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    wrongs = [w for w in dict.fromkeys(wrongs) if w != correct]
    # Two named mistakes can coincide for some specs; a whole-number answer is
    # then topped up with its neighbours so the item still offers four.
    if correct.lstrip("-").isdigit():
        n = int(correct)
        for d in (1, -1, 2, -2, 3, 5):
            if len(wrongs) >= 3:
                break
            if str(n + d) not in wrongs:
                wrongs.append(str(n + d))
    return GeneratedQuestion(stem=stem, correct=[content_math(correct)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


def _text_q(stem: list, correct: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    wrongs = [w for w in dict.fromkeys(wrongs) if w != correct]
    return GeneratedQuestion(stem=stem, correct=[text(correct)],
                             distractors=fixed(*[[text(w)] for w in wrongs]), topic=topic)


def _nums(*values: int, answer: int, lo: int = 0) -> list[str]:
    return _story.keep(*values, answer=answer, lo=lo)


# ══ Specs ════════════════════════════════════════════════════════════════════

# ── รูปเรขาคณิตสองมิติและสามมิติ ──────────────────────────────────────────────

class Shape2D(NamedTuple):
    name: str
    thai: str

    @property
    def asset_id(self) -> str:
        return f"mshape2d_{self.name}"


SHAPES_2D = (Shape2D("triangle", "รูปสามเหลี่ยม"), Shape2D("square", "รูปสี่เหลี่ยมจัตุรัส"),
             Shape2D("rectangle", "รูปสี่เหลี่ยมผืนผ้า"), Shape2D("circle", "รูปวงกลม"),
             Shape2D("ellipse", "รูปวงรี"), Shape2D("pentagon", "รูปห้าเหลี่ยม"),
             Shape2D("hexagon", "รูปหกเหลี่ยม"))


class Solid(NamedTuple):
    name: str
    thai: str
    faces: int
    edges: int
    vertices: int

    @property
    def asset_id(self) -> str:
        return f"msolid_{self.name}"


SOLIDS = (Solid("cube", "ทรงลูกบาศก์", 6, 12, 8),
          Solid("cuboid", "ทรงสี่เหลี่ยมมุมฉาก", 6, 12, 8),
          Solid("tri_prism", "ปริซึมสามเหลี่ยม", 5, 9, 6),
          Solid("pent_prism", "ปริซึมห้าเหลี่ยม", 7, 15, 10),
          Solid("sq_pyramid", "พีระมิดฐานสี่เหลี่ยม", 5, 8, 5),
          Solid("tri_pyramid", "พีระมิดฐานสามเหลี่ยม", 4, 6, 4),
          Solid("cylinder", "ทรงกระบอก", 0, 0, 0),
          Solid("cone", "กรวย", 0, 0, 0),
          Solid("sphere", "ทรงกลม", 0, 0, 0))


class Net(NamedTuple):
    name: str
    thai: str

    @property
    def asset_id(self) -> str:
        return f"mnet_{self.name}"


NETS = (Net("cube", "ทรงลูกบาศก์"), Net("cuboid", "ทรงสี่เหลี่ยมมุมฉาก"),
        Net("tri_prism", "ปริซึมสามเหลี่ยม"), Net("sq_pyramid", "พีระมิดฐานสี่เหลี่ยม"),
        Net("cylinder", "ทรงกระบอก"), Net("cone", "กรวย"))


# ── นาฬิกา ────────────────────────────────────────────────────────────────────

class ClockSpec(NamedTuple):
    h: int      # 1..12
    m: int      # 0..55, five-minute steps

    @property
    def asset_id(self) -> str:
        return f"mclock_{self.h}_{self.m:02d}"


CLOCKS = tuple(ClockSpec(h, m) for h in range(1, 13) for m in range(0, 60, 5))
CLOCK_ALT = "หน้าปัดนาฬิกาที่มีตัวเลข 1 ถึง 12 พร้อมเข็มสั้นและเข็มยาว"


# ── มุม ──────────────────────────────────────────────────────────────────────

class AngleSpec(NamedTuple):
    deg: int
    protractor: bool

    @property
    def asset_id(self) -> str:
        return f"mangle_{self.deg}_{'p' if self.protractor else 'n'}"


PROTRACTOR_ANGLES = tuple(AngleSpec(d, True) for d in range(10, 180, 5))
KIND_ANGLES = tuple(AngleSpec(d, False) for d in (20, 35, 50, 65, 80, 90, 100, 115, 130, 145,
                                                  160, 180, 210, 240, 270, 300))


# ── เศษส่วนจากรูป ─────────────────────────────────────────────────────────────

class FractionPicture(NamedTuple):
    n: int
    d: int
    shape: str          # "bar" | "pie"

    @property
    def asset_id(self) -> str:
        return f"mfrac_{self.shape}_{self.n}_{self.d}"


FRACTION_PICTURES = (tuple(FractionPicture(n, d, "bar") for d in range(2, 11) for n in range(1, d))
                     + tuple(FractionPicture(n, d, "pie") for d in range(2, 9) for n in range(1, d)))


# ── รูปที่มีความยาวกำกับ ──────────────────────────────────────────────────────

class Figure(NamedTuple):
    """A figure with its measurements written on it.

    ``kind`` and ``dims``:
      rect   (width, length)              square (side,)
      para   (base, height, slant)        trap   (top, bottom, height)
      tri    (base, height, apex_at)      apex_at is where the top sits along
                                          the base, in tenths (0 = right angle)
      lshape (width, height, cut_w, cut_h) the cut is taken from the top right
      rtri   (a, b, c)                    legs a, b; hypotenuse c
    ``unknown`` (rtri only) is the side drawn as x.
    """
    kind: str
    dims: tuple[int, ...]
    unit: str = "cm"
    unknown: str = ""

    @property
    def asset_id(self) -> str:
        tail = f"_{self.unknown}" if self.unknown else ""
        return f"mfig_{self.kind}_{'_'.join(map(str, self.dims))}_{self.unit}{tail}"


RECT_FIGURES = tuple(Figure("rect", d, u) for d, u in (
    ((4, 7), "cm"), ((5, 9), "cm"), ((6, 11), "cm"), ((3, 12), "cm"), ((8, 13), "cm"),
    ((7, 15), "cm"), ((9, 14), "cm"), ((12, 20), "m"), ((15, 25), "m"), ((10, 18), "m"),
    ((6, 16), "m"), ((14, 30), "m"), ((5, 8), "m"), ((11, 17), "cm"), ((13, 22), "m"))) + tuple(
    Figure("square", (s,), u) for s, u in ((5, "cm"), (8, "cm"), (12, "cm"), (15, "m"), (20, "m")))

QUAD_FIGURES = tuple(Figure("para", d) for d in (
    (8, 5, 6), (10, 6, 7), (12, 7, 8), (9, 4, 5), (14, 8, 10), (15, 6, 7), (11, 9, 10),
    (16, 5, 6))) + tuple(Figure("trap", d) for d in (
    (6, 10, 5), (4, 12, 6), (8, 14, 7), (5, 9, 4), (7, 15, 8), (10, 16, 6), (3, 11, 5),
    (9, 13, 10)))

TRIANGLE_FIGURES = tuple(Figure("tri", d) for d in (
    (10, 6, 3), (12, 8, 5), (8, 7, 0), (14, 9, 6), (16, 5, 4), (9, 8, 0), (18, 10, 7),
    (20, 7, 5), (11, 6, 4), (15, 12, 0), (13, 10, 6), (24, 9, 3)))

L_FIGURES = tuple(Figure("lshape", d) for d in (
    (10, 8, 4, 3), (12, 9, 5, 4), (14, 10, 6, 5), (9, 7, 4, 3), (16, 12, 7, 5),
    (11, 8, 5, 2), (13, 11, 6, 4), (15, 9, 8, 3), (18, 14, 10, 6), (10, 10, 4, 4)))

_TRIPLES = ((3, 4, 5), (6, 8, 10), (9, 12, 15), (12, 16, 20), (5, 12, 13), (10, 24, 26),
            (8, 15, 17), (7, 24, 25), (20, 21, 29))
RIGHT_TRIANGLE_FIGURES = tuple(Figure("rtri", t, "cm", u) for t in _TRIPLES for u in ("a", "b", "c"))


def figure_alt(f: Figure) -> str:
    """The measurements on the drawing, which are the question's data."""
    u = "ซม." if f.unit == "cm" else "ม."
    if f.kind == "rect":
        return f"รูปสี่เหลี่ยมผืนผ้า ด้านกว้างกำกับ {f.dims[0]} {u} ด้านยาวกำกับ {f.dims[1]} {u}"
    if f.kind == "square":
        return f"รูปสี่เหลี่ยมจัตุรัส ด้านกำกับ {f.dims[0]} {u}"
    if f.kind == "para":
        b, h, s = f.dims
        return f"รูปสี่เหลี่ยมด้านขนาน ฐาน {b} {u} ความสูง {h} {u} (เส้นประ) ด้านเอียง {s} {u}"
    if f.kind == "trap":
        a, b, h = f.dims
        return f"รูปสี่เหลี่ยมคางหมู ด้านคู่ขนานยาว {a} {u} และ {b} {u} ความสูง {h} {u} (เส้นประ)"
    if f.kind == "tri":
        return f"รูปสามเหลี่ยม ฐาน {f.dims[0]} {u} ความสูง {f.dims[1]} {u} (เส้นประ)"
    if f.kind == "lshape":
        w, h, cw, ch = f.dims
        return (f"รูปหกเหลี่ยมรูปตัวแอล ด้านล่างยาว {w} {u} ด้านซ้ายสูง {h} {u} ด้านบนยาว {w - cw} {u} "
                f"ด้านขวาสูง {h - ch} {u}")
    a, b, c = f.dims
    shown = {"a": a, "b": b, "c": c}
    parts = [f"{'x' if k == f.unknown else v} {u}" for k, v in shown.items()]
    return f"รูปสามเหลี่ยมมุมฉาก ด้านประกอบมุมฉาก {parts[0]} และ {parts[1]} ด้านตรงข้ามมุมฉาก {parts[2]}"


# ── แผนภูมิแท่งและกราฟเส้น ────────────────────────────────────────────────────

class BarChart(NamedTuple):
    values: tuple[int, ...]
    scale: int

    @property
    def asset_id(self) -> str:
        return f"mbar_{self.scale}_{'_'.join(map(str, self.values))}"


class LineGraph(NamedTuple):
    values: tuple[int, ...]
    step: int

    @property
    def asset_id(self) -> str:
        return f"mline_{self.step}_{'_'.join(map(str, self.values))}"


def _bar_charts() -> tuple[BarChart, ...]:
    # Fixed seed: the tuple is part of the shipped content and must not move.
    rng = Random(20260923)
    out = []
    for scale in (1, 2, 5, 10, 20, 50):
        for _ in range(3):
            n = rng.choice((4, 5))
            counts = rng.sample(range(1, 11), n)
            out.append(BarChart(tuple(c * scale for c in counts), scale))
    return tuple(out)


def _line_graphs() -> tuple[LineGraph, ...]:
    rng = Random(20260924)
    out = []
    for step in (1, 2, 5, 10):
        for _ in range(4):
            vals = [rng.randint(2, 9)]
            for _ in range(5):
                vals.append(min(10, max(0, vals[-1] + rng.choice((-3, -2, -1, 1, 2, 3)))))
            out.append(LineGraph(tuple(v * step for v in vals), step))
    return tuple(out)


BAR_CHARTS = _bar_charts()
LINE_GRAPHS = _line_graphs()


# ── เส้นจำนวนและกราฟบนระนาบพิกัดฉาก ──────────────────────────────────────────

class NumberLine(NamedTuple):
    p: int

    @property
    def asset_id(self) -> str:
        return f"mnumline_{_neg(self.p)}"


NUMBER_LINES = tuple(NumberLine(p) for p in range(-9, 10) if p not in (0, 5, -5))


class LineFn(NamedTuple):
    m: int
    c: int

    @property
    def asset_id(self) -> str:
        return f"mlinefn_{_neg(self.m)}_{_neg(self.c)}"


LINE_FNS = tuple(LineFn(m, c) for m, c in (
    (1, 2), (1, -3), (2, 1), (2, -2), (3, -4), (-1, 3), (-1, -2), (-2, 4), (-2, 0),
    (1, 0), (3, 1), (-3, 2), (2, 3), (-1, 5), (1, -1), (-2, -3), (2, -4), (-1, 1)))
LINE_FN_ALT = "กราฟเส้นตรงบนระนาบพิกัดฉากที่มีเส้นตาราง แกน X และแกน Y กำกับทุก 1 หน่วย"


class Parabola(NamedTuple):
    a: int      # 1 or -1
    h: int
    k: int

    @property
    def asset_id(self) -> str:
        return f"mparab_{_neg(self.a)}_{_neg(self.h)}_{_neg(self.k)}"


PARABOLAS = tuple(Parabola(a, h, k) for a, h, k in (
    (1, 0, -3), (1, 1, -4), (1, -2, -1), (1, 2, 0), (1, -1, 2), (1, 3, -2), (1, -3, 1),
    (1, 0, 1), (1, 2, -4), (-1, 0, 3), (-1, 1, 4), (-1, -2, 1), (-1, 2, 0), (-1, -1, -1),
    (-1, 3, 2), (-1, 0, 5), (-1, -3, 4), (-1, 1, -2)))


ALL_MATH_DIAGRAMS = (SHAPES_2D + SOLIDS + NETS + CLOCKS + PROTRACTOR_ANGLES + KIND_ANGLES
                     + FRACTION_PICTURES + RECT_FIGURES + QUAD_FIGURES + TRIANGLE_FIGURES
                     + L_FIGURES + RIGHT_TRIANGLE_FIGURES + BAR_CHARTS + LINE_GRAPHS + NUMBER_LINES
                     + LINE_FNS + PARABOLAS)


# ══ Sets ═════════════════════════════════════════════════════════════════════

# ── ป.1 รูปเรขาคณิต ───────────────────────────────────────────────────────────


# ── ป.2–ป.3 นาฬิกา ────────────────────────────────────────────────────────────


# ── ป.3 เศษส่วนจากรูป ─────────────────────────────────────────────────────────


# ── ป.4 มุม ──────────────────────────────────────────────────────────────────


# ── ป.4–ป.6 รูปที่มีความยาวกำกับ ──────────────────────────────────────────────


# ── ป.6–ม.1 รูปเรขาคณิตสามมิติและรูปคลี่ ──────────────────────────────────────


# ── ป.4–ป.5 แผนภูมิแท่งและกราฟเส้น ────────────────────────────────────────────


# ── ม.1–ม.3 เส้นจำนวนและกราฟ ──────────────────────────────────────────────────


