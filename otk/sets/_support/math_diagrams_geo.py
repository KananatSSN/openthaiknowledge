"""Geometry and chart sets read off a drawing: points, lines and rays; parallel
lines cut by a transversal; triangles with their angles or sides marked; pie
charts; box plots at ม.2; transformations on a grid; angles in a circle; and
similar triangles.

Same contract as :mod:`.math_diagrams`: each family is a finite tuple of specs,
``otk/pictures/math_diagrams.py`` draws one PNG per spec,
and a question computes its answer from the spec it shows. Labels in the
drawings are numbers and ASCII letters. Where the marked data is not itself
the answer, the alt text reads it out; where naming the figure *is* the
question, the alt text is the same for every item of the set.
"""

from __future__ import annotations

import math
from typing import NamedTuple

from otk.sets._support.math_diagrams import _neg

# ══ Points, lines and rays (ป.4) ═════════════════════════════════════════════

class LineFigure(NamedTuple):
    kind: str        # "segment" | "ray" | "ray_back" | "line"
    names: str       # two letters, left to right: "AB"
    tilt: int        # degrees

    @property
    def asset_id(self) -> str:
        return f"mlray_{self.kind}_{self.names}_{self.tilt}"


LINE_FIGURES = tuple(LineFigure(k, n, t) for k in ("segment", "ray", "ray_back", "line")
                     for n, t in (("AB", 0), ("PQ", 20), ("MN", -15)))


# ══ Parallel lines cut by a transversal (ป.5, ม.2) ═══════════════════════════

# The transversal crosses the upper line at P and the lower line at Q. At each
# crossing the four angles are numbered anticlockwise from the upper right:
# P: 1 UR, 2 UL, 3 LL, 4 LR;  Q: 5 UR, 6 UL, 7 LL, 8 LR.

class ParallelCut(NamedTuple):
    theta: int                         # the acute angle at each upper right
    marks: tuple[tuple[int, str], ...]  # (angle number, label): "65", "x", "a"

    @property
    def asset_id(self) -> str:
        return f"mpar_{self.theta}_" + "_".join(f"{p}{length}" for p, length in self.marks)


def angle_at(theta: int, pos: int) -> int:
    """The size of angle ``pos``: upper right and lower left are θ."""
    return theta if (pos - 1) % 4 in (0, 2) else 180 - theta


_FIND_PAIRS = ((1, 5), (2, 6), (3, 7), (4, 8), (3, 5), (4, 6), (4, 5), (3, 6), (1, 3), (6, 8))
PARALLEL_FIND = tuple(ParallelCut(t, ((g, str(angle_at(t, g))), (x, "x")))
                      for i, (a, b) in enumerate(_FIND_PAIRS)
                      for t, (g, x) in ((50 + 5 * (i % 5), (a, b)), (65 + 5 * (i % 3), (b, a))))
PARALLEL_NAME = tuple(ParallelCut(t, ((a, "a"), (b, "b")))
                      for t in (60, 70)
                      for a, b in ((1, 5), (2, 6), (3, 5), (4, 6), (4, 5), (3, 6), (4, 8), (1, 3)))
_TWO = ((1, 6, 7), (4, 5, 8), (2, 3, 8), (5, 4, 2), (6, 3, 1), (8, 3, 6), (7, 1, 4), (3, 7, 5))
PARALLEL_TWO = tuple(ParallelCut(t, ((g, str(angle_at(t, g))), (x, "x"), (y, "y")))
                     for t in (55, 70) for g, x, y in _TWO)


def parallel_alt(p: ParallelCut) -> str:
    """The marked sizes are data, so they are read out; positions are named by
    the crossing and the corner."""
    where = {1: "บนขวา", 2: "บนซ้าย", 3: "ล่างซ้าย", 4: "ล่างขวา"}
    parts = [f"มุม{where[(pos - 1) % 4 + 1]}ที่จุดตัด{'บน' if pos <= 4 else 'ล่าง'}กำกับ "
             f"{lab + ' องศา' if lab.isdigit() else lab}" for pos, lab in p.marks]
    return "เส้นตรงสองเส้นที่ขนานกันถูกตัดด้วยเส้นตัด " + " ".join(parts)


# ══ Triangles with angles or sides marked (ป.6) ══════════════════════════════

class MarkedTriangle(NamedTuple):
    angles: tuple[int, int, int]      # at A, B, C
    shown: str                        # "abc": all marked; "ab": C drawn as x
    sides: tuple[int, int, int] = ()  # when set, sides are marked instead (cm)

    @property
    def asset_id(self) -> str:
        if self.sides:
            return "mtri_s_" + "_".join(map(str, self.sides))
        return "mtri_a_" + "_".join(map(str, self.angles)) + f"_{self.shown}"


_ANGLE_TRIPLES = ((50, 60, 70), (40, 65, 75), (30, 60, 90), (45, 45, 90), (35, 55, 90), (30, 40, 110),
                  (25, 35, 120), (20, 60, 100), (60, 60, 60), (70, 70, 40), (50, 50, 80), (30, 30, 120))
TRI_ANGLES = tuple(MarkedTriangle(t, s) for t in _ANGLE_TRIPLES for s in ("abc", "ab"))
# (AB, BC, CA): each triangle is drawn from its sides.
_SIDE_TRIPLES = ((5, 5, 5), (6, 6, 6), (5, 5, 8), (7, 4, 7), (6, 9, 9), (4, 5, 6), (5, 7, 9), (6, 8, 10))
TRI_SIDES = tuple(MarkedTriangle((0, 0, 0), "", s) for s in _SIDE_TRIPLES)


# ══ Pie charts (ป.6) ═════════════════════════════════════════════════════════

class PieChart(NamedTuple):
    percents: tuple[int, int, int, int]     # sectors A, B, C, D

    @property
    def asset_id(self) -> str:
        return "mpie_" + "_".join(map(str, self.percents))


PIE_CHARTS = tuple(PieChart(p) for p in (
    (40, 25, 20, 15), (35, 30, 25, 10), (50, 20, 15, 15), (30, 30, 25, 15), (45, 25, 20, 10),
    (25, 25, 30, 20), (40, 30, 10, 20), (20, 35, 30, 15), (55, 15, 20, 10), (30, 40, 20, 10)))


# ══ Transformations on a grid (ม.2) ══════════════════════════════════════════

class Transform(NamedTuple):
    tri: tuple[tuple[int, int], ...]   # A, B, C
    move: str                          # "t_dx_dy" | "rx" | "ry" | "r180" | "r90"

    @property
    def asset_id(self) -> str:
        pts = "_".join(f"{_neg(x)}.{_neg(y)}" for x, y in self.tri)
        return f"mtrans_{self.move.replace('-', 'n')}_{pts}"

    def image(self) -> tuple[tuple[int, int], ...]:
        return tuple(move_point(self.move, p) for p in self.tri)


def move_point(move: str, p: tuple[int, int]) -> tuple[int, int]:
    x, y = p
    if move.startswith("t_"):
        _, dx, dy = move.split("_")
        return x + int(dx), y + int(dy)
    return {"rx": (x, -y), "ry": (-x, y), "r180": (-x, -y), "r90": (-y, x)}[move]


TRANSFORMS = tuple(Transform(t, m) for t, m in (
    (((1, 1), (4, 1), (2, 3)), "rx"), (((-4, 2), (-1, 2), (-2, 4)), "rx"),
    (((1, 1), (3, 1), (3, 4)), "ry"), (((2, -1), (5, -1), (4, -3)), "ry"),
    (((1, 1), (4, 1), (1, 3)), "r180"), (((-3, 1), (-1, 1), (-1, 4)), "r180"),
    (((1, 1), (4, 1), (4, 3)), "r90"), (((2, 1), (4, 2), (2, 4)), "r90"),
    (((-5, 1), (-3, 1), (-4, 3)), "t_6_2"), (((1, 2), (3, 2), (1, 5)), "t_-5_-4"),
    (((-4, -4), (-1, -4), (-2, -2)), "t_3_5"), (((2, 3), (5, 3), (3, 5)), "t_-6_-1"),
))


# ══ Angles in a circle (ม.3) ═════════════════════════════════════════════════

class CircleAngle(NamedTuple):
    kind: str      # "central" (∠AOB given) | "inscribed" (∠ACB given) | "semi" | "cyclic"
    value: int     # the marked angle

    @property
    def asset_id(self) -> str:
        return f"mcirc_{self.kind}_{self.value}"

    @property
    def answer(self) -> int:
        return {"central": self.value // 2, "inscribed": 2 * self.value,
                "semi": 90 - self.value, "cyclic": 180 - self.value}[self.kind]


CIRCLE_ANGLES = (tuple(CircleAngle("central", v) for v in (60, 80, 100, 120, 140))
                 + tuple(CircleAngle("inscribed", v) for v in (25, 35, 40, 55, 65))
                 + tuple(CircleAngle("semi", v) for v in (25, 35, 50, 62))
                 + tuple(CircleAngle("cyclic", v) for v in (70, 85, 100, 115)))


# ══ Similar triangles (ม.3) ══════════════════════════════════════════════════

class SimilarPair(NamedTuple):
    small: tuple[int, int, int]     # AB, BC, CA
    k: int                          # the large triangle's sides are k times
    unknown: int                    # 0–2: side of the large triangle drawn as x;
                                    # 3–5: side of the small one

    @property
    def asset_id(self) -> str:
        return "msim_" + "_".join(map(str, self.small)) + f"_{self.k}_{self.unknown}"

    @property
    def answer(self) -> int:
        i = self.unknown % 3
        return self.small[i] * self.k if self.unknown < 3 else self.small[i]


SIMILAR_PAIRS = tuple(SimilarPair(s, k, u) for s, k, u in (
    ((3, 4, 5), 2, 0), ((3, 4, 5), 3, 1), ((4, 6, 5), 2, 2), ((4, 6, 5), 3, 4),
    ((5, 7, 6), 2, 1), ((5, 7, 6), 2, 3), ((6, 8, 7), 3, 2), ((2, 3, 4), 4, 0),
    ((2, 3, 4), 3, 5), ((4, 5, 7), 2, 4), ((6, 5, 4), 3, 0), ((3, 5, 7), 2, 5),
))


# ══ Lines of symmetry (ป.3) ══════════════════════════════════════════════════

class SymmetryShape(NamedTuple):
    name: str
    axes: int

    @property
    def asset_id(self) -> str:
        return f"msym_{self.name}"


SYMMETRY_SHAPES = tuple(SymmetryShape(n, a) for n, a in (
    ("square", 4), ("rectangle", 2), ("equilateral", 3), ("isosceles", 1), ("scalene", 0),
    ("pentagon", 5), ("hexagon", 6), ("rhombus", 2), ("kite", 1), ("parallelogram", 0),
    ("trapezoid", 1), ("arrow", 1), ("cross", 4), ("octagon", 8)))


# ══ Tangents to a circle (ม.3) ═══════════════════════════════════════════════

class Tangent(NamedTuple):
    kind: str      # "pt": find PT from r and OP; "op": find OP from r and PT;
                   # "two": PA given, find PB; "angle": ∠APB given, find ∠AOB
    a: int
    b: int

    @property
    def asset_id(self) -> str:
        return f"mtan_{self.kind}_{self.a}_{self.b}"

    @property
    def answer(self) -> int:
        if self.kind == "pt":
            return math.isqrt(self.b ** 2 - self.a ** 2)
        if self.kind == "op":
            return math.isqrt(self.a ** 2 + self.b ** 2)
        return self.a if self.kind == "two" else 180 - self.a


# (radius, tangent length, OP) from Pythagorean triples.
TANGENTS = (tuple(Tangent("pt", r, d) for r, d in ((3, 5), (5, 13), (8, 17), (6, 10), (7, 25), (9, 15)))
            + tuple(Tangent("op", r, t) for r, t in ((3, 4), (5, 12), (8, 15), (6, 8), (9, 12)))
            + tuple(Tangent("two", t, 0) for t in (6, 9, 11))
            + tuple(Tangent("angle", v, 0) for v in (40, 50, 64, 76)))


# ══ Conic sections on a grid (ม.4 เพิ่มเติม) ═════════════════════════════════

class ConicGraph(NamedTuple):
    kind: str       # "par": y² = 4px (or x² = 4py); "ell": x²/a² + y²/b² = 1; "hyp": ±(x²/a² − y²/b²) = 1
    a: int          # p for a parabola
    b: int
    vertical: bool  # parabola opens up/down; hyperbola opens up/down

    @property
    def asset_id(self) -> str:
        return f"mconic_{self.kind}_{_neg(self.a)}_{self.b}_{'v' if self.vertical else 'h'}"


CONIC_GRAPHS = (tuple(ConicGraph("par", p, 0, v) for p in (1, 2, -1, -2) for v in (False, True))
                + tuple(ConicGraph("ell", a, b, False) for a, b in ((5, 3), (4, 2), (6, 4), (5, 4), (3, 2), (6, 3),
                                                                     (3, 5), (2, 4), (4, 6)))
                + tuple(ConicGraph("hyp", a, b, v) for a, b, v in ((2, 1, False), (3, 2, False), (4, 3, False),
                                                                   (2, 3, False), (3, 4, False), (2, 1, True),
                                                                   (3, 2, True), (4, 3, True))))


# ══ A right triangle with an angle θ (ม.5 อัตราส่วนตรีโกณมิติ) ════════════════

class RightTriangle(NamedTuple):
    opp: int        # side facing θ
    adj: int        # side next to θ
    hyp: int
    shown: str      # the two sides written on the drawing: "oa" | "oh" | "ah"

    @property
    def asset_id(self) -> str:
        return f"mrtri_{self.opp}_{self.adj}_{self.hyp}_{self.shown}"


RIGHT_TRIANGLES = tuple(RightTriangle(o, a, h, s)
                        for t in ((3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25))
                        for o, a, h in ((t[0], t[1], t[2]), (t[1], t[0], t[2]))
                        for s in ("oa", "oh", "ah"))


ALL_GEO_DIAGRAMS = (LINE_FIGURES + PARALLEL_FIND + PARALLEL_NAME + PARALLEL_TWO + TRI_ANGLES + TRI_SIDES
                    + PIE_CHARTS + TRANSFORMS + CIRCLE_ANGLES + SIMILAR_PAIRS + SYMMETRY_SHAPES + TANGENTS
                    + CONIC_GRAPHS + RIGHT_TRIANGLES)


# ══ Sets ═════════════════════════════════════════════════════════════════════


