"""Geometry and chart sets read off a drawing (math_diagrams_geo): every spec
has its PNG, and every answer is re-derived from the figure's geometry rather
than from the helper that picked it."""

from __future__ import annotations

from otk.tests._origins import keys_from

import math
import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, generate
from otk.core.render.assets import is_diagram
from otk.sets._support import math_diagrams_geo as geo
from otk.sets._support.math_diagrams_hi import BOX_PLOTS
from otk.sets.math.p5.parallel_lines import RELATIONS, relation
from otk.sets.math.m2.geometric_transformations import transform_name

SEEDS = range(300)
KEYS = keys_from("math_diagrams_geo")
BY_ID = {s.asset_id: s for s in geo.ALL_GEO_DIAGRAMS}
BOX_BY_ID = {b.asset_id: b for b in BOX_PLOTS}


def _b(block) -> str:
    return getattr(block, "text", None) or getattr(block, "tex", "") or ""


def _choices(q) -> list[str]:
    return [" ".join(_b(b) for b in c.content) for c in q.choices]


def _answer(q) -> str:
    return _choices(q)[q.answer]


def _stem(q) -> str:
    return " ".join(_b(b) for b in q.stem)


def _each(key):
    for seed in SEEDS:
        q = generate(key, Random(seed))
        img = next(b for b in q.stem if b.kind == "image")
        yield q, BY_ID.get(img.asset_id) or BOX_BY_ID[img.asset_id], img


def test_fourteen_sets_and_every_spec_has_a_png():
    assert len(KEYS) == 14
    assert len(BY_ID) == len(geo.ALL_GEO_DIAGRAMS)
    missing = [s.asset_id for s in geo.ALL_GEO_DIAGRAMS if not is_diagram(s.asset_id)]
    assert not missing


@pytest.mark.parametrize("key", KEYS)
def test_four_distinct_choices(key):
    for q, _, _ in _each(key):
        assert len(q.choices) == REGISTRY[key].max_choices and len(set(_choices(q))) == REGISTRY[key].max_choices, (key, _stem(q))


@pytest.mark.parametrize("key", ["math.line_ray_picture_p4", "math.parallel_pair_picture_p5",
                                 "math.transformation_picture_m2", "math.symmetry_picture_p3",
                                 "math.conic_graph_picture_m4"])
def test_naming_sets_keep_the_answer_out_of_the_alt_text(key):
    assert len({img.alt for _, _, img in _each(key)}) == 1


# ── Lines and rays ───────────────────────────────────────────────────────────

def test_line_ray_names_start_at_the_endpoint():
    for q, f, _ in _each("math.line_ray_picture_p4"):
        a, b = f.names
        want = {"segment": f"ส่วนของเส้นตรง {a}{b}",
                "ray": f"รังสี {a}{b}",          # starts at A, passes B
                "ray_back": f"รังสี {b}{a}",     # starts at B, passes A
                "line": f"เส้นตรง {a}{b}"}[f.kind]
        assert _answer(q) == want


# ── Parallel lines ───────────────────────────────────────────────────────────

def _size(theta: int, pos: int) -> int:
    """Measure the corner from the directions of its two arms."""
    arms = [0, theta, 180, 180 + theta, 360]
    k = (pos - 1) % 4
    return arms[k + 1] - arms[k]


def test_parallel_angle():
    for q, p, _ in _each("math.parallel_angle_picture_p5"):
        (g, lab), (x, _) = p.marks
        assert int(lab) == _size(p.theta, g)
        assert int(_answer(q)) == _size(p.theta, x)


def test_parallel_pairs_name_the_book_relations():
    for q, p, _ in _each("math.parallel_pair_picture_p5"):
        (a, _), (b, _) = p.marks
        rel = relation(a, b)
        equal = _size(p.theta, a) == _size(p.theta, b)
        assert rel is not None
        assert equal == (rel in ("corresponding", "alternate", "vertical"))
        if "เป็นมุมคู่ใด" in _stem(q):
            assert _answer(q) == RELATIONS[rel]
        else:
            assert ("เท่ากัน" in _answer(q)) == equal


def test_transversal_two_unknowns():
    for q, p, _ in _each("math.transversal_picture_m2"):
        (g, lab), (xp, _), (yp, _) = p.marks
        assert int(lab) == _size(p.theta, g)
        x, y = _size(p.theta, xp), _size(p.theta, yp)
        ask = q.stem[1].tex
        assert int(_answer(q)) == {"x + y": x + y, "x - y": x - y, "y": y}[ask]


# ── Triangles ────────────────────────────────────────────────────────────────

def test_triangle_specs_are_triangles():
    for t in geo.TRI_ANGLES:
        assert sum(t.angles) == 180 and min(t.angles) > 0
    for t in geo.TRI_SIDES:
        a, b, c = sorted(t.sides)
        assert a + b > c


def _by_angle_from_sides(sides) -> str:
    a, b, c = sorted(sides)
    d = a * a + b * b - c * c
    return "รูปสามเหลี่ยมมุมแหลม" if d > 0 else "รูปสามเหลี่ยมมุมฉาก" if d == 0 else "รูปสามเหลี่ยมมุมป้าน"


def test_triangle_type():
    for q, t, _ in _each("math.triangle_type_picture_p6"):
        a = _answer(q)
        if t.sides:
            n = len(set(t.sides))
            assert a == {1: "รูปสามเหลี่ยมด้านเท่า", 2: "รูปสามเหลี่ยมหน้าจั่ว", 3: "รูปสามเหลี่ยมด้านไม่เท่า"}[n]
        elif a.isdigit():
            assert int(a) == 180 - t.angles[0] - t.angles[1]
        else:
            top = max(t.angles)
            assert ("แหลม" in a, "ฉาก" in a, "ป้าน" in a) == (top < 90, top == 90, top > 90)
    # The side triples classify by angle the same way the law of cosines does.
    assert _by_angle_from_sides((6, 8, 10)) == "รูปสามเหลี่ยมมุมฉาก"


# ── Pie charts and box plots ─────────────────────────────────────────────────

def test_pie_chart():
    for p in geo.PIE_CHARTS:
        assert sum(p.percents) == 100
    for q, p, _ in _each("math.pie_chart_picture_p6"):
        s = _stem(q)
        pct = dict(zip("ABCD", p.percents))
        parts = re.findall(r"ส่วน ([ABCD])", s)
        ans = int(_answer(q))
        if "มุมที่จุดศูนย์กลาง" in s:
            assert ans == pct[parts[0]] * 360 // 100
            continue
        total = int(re.search(r"ทั้งหมด ([\d,]+)", s).group(1).replace(",", ""))
        if "ต่างกัน" in s:
            assert ans == total * abs(pct[parts[0]] - pct[parts[1]]) // 100
        else:
            assert ans == total * pct[parts[0]] // 100


def test_box_plot_m2():
    for q, b, _ in _each("math.box_plot_picture_m2"):
        s, ans = _stem(q), int(_answer(q))
        if "ค่าต่ำสุด" in s:
            assert ans == b.lo
        elif "ควอร์ไทล์ที่ 1 เท่ากับ" in s:
            assert ans == b.q1
        elif "ร้อยละ" in s:
            assert ans == 50
        else:
            assert ans == b.hi - b.med


# ── Transformations ──────────────────────────────────────────────────────────

def _moved(move: str, x: int, y: int) -> tuple[int, int]:
    if move.startswith("t_"):
        _, dx, dy = move.split("_")
        return x + int(dx), y + int(dy)
    # Reflection in an axis flips one coordinate; a quarter turn anticlockwise
    # sends (1, 0) to (0, 1) and (0, 1) to (-1, 0).
    return {"rx": (x, -y), "ry": (-x, y), "r180": (-x, -y), "r90": (-y, x)}[move]


def test_transformations():
    for t in geo.TRANSFORMS:
        assert all(-6 <= v <= 6 for p in t.tri + t.image() for v in p)
    for q, t, _ in _each("math.transformation_picture_m2"):
        s = _stem(q)
        if "มีพิกัด" in s:
            i = "ABC".index(re.search(r"จุด ([ABC])'", s).group(1))
            assert _answer(q) == "({}, {})".format(*_moved(t.move, *t.tri[i]))
        else:
            assert _answer(q) == transform_name(t.move)


# ── Angles in a circle, from coordinates ─────────────────────────────────────

def _on(deg):
    return math.cos(math.radians(deg)), math.sin(math.radians(deg))


def _angle(v, p, q) -> float:
    a = (p[0] - v[0], p[1] - v[1])
    b = (q[0] - v[0], q[1] - v[1])
    return math.degrees(math.acos((a[0] * b[0] + a[1] * b[1]) / (math.hypot(*a) * math.hypot(*b))))


def test_circle_angles_measured_on_the_drawing():
    for q, c, _ in _each("math.circle_angle_picture_m3"):
        ans = int(_answer(q))
        origin = (0.0, 0.0)
        if c.kind in ("central", "inscribed"):
            cen = c.value if c.kind == "central" else 2 * c.value
            A, B, C = _on(-90 - cen / 2), _on(-90 + cen / 2), _on(90)
            x = _angle(C, A, B) if c.kind == "central" else _angle(origin, A, B)
        elif c.kind == "semi":
            A, B, C = _on(180), _on(0), _on(2 * c.value)
            assert round(_angle(A, B, C)) == c.value
            x = _angle(B, A, C)
        else:
            A, B, C, D = _on(180), _on(c.value + 20), _on(0), _on(20 - c.value)
            assert round(_angle(A, B, D)) == c.value
            x = _angle(C, B, D)
        assert round(x) == ans, c


# ── Similar triangles ────────────────────────────────────────────────────────

def test_similar_triangles():
    for q, s, img in _each("math.similar_triangle_picture_m3"):
        nums = re.findall(r"ยาว (\S+) (\S+) (\S+) หน่วย", img.alt)
        small, large = nums
        i = s.unknown % 3
        j = (i + 1) % 3
        # The scale factor from a pair of corresponding sides both shown.
        k = int(large[j]) / int(small[j])
        want = int(small[i]) * k if s.unknown < 3 else int(large[i]) / k
        assert int(_answer(q)) == want


# ── Symmetry and tangents ────────────────────────────────────────────────────

def test_symmetry_axes_by_shape():
    # A regular n-gon has n axes; the rest are counted by hand from the drawing.
    regular = {"equilateral": 3, "square": 4, "pentagon": 5, "hexagon": 6, "octagon": 8}
    for q, s, _ in _each("math.symmetry_picture_p3"):
        want = regular.get(s.name, {"rectangle": 2, "rhombus": 2, "cross": 4, "isosceles": 1, "kite": 1,
                                    "trapezoid": 1, "arrow": 1, "scalene": 0, "parallelogram": 0}.get(s.name))
        assert int(_answer(q)) == want


def test_tangents_meet_the_radius_at_a_right_angle():
    for q, t, img in _each("math.tangent_picture_m3"):
        ans = int(_answer(q))
        if t.kind == "pt":
            assert t.a ** 2 + ans ** 2 == t.b ** 2
        elif t.kind == "op":
            assert t.a ** 2 + t.b ** 2 == ans ** 2
        elif t.kind == "two":
            assert ans == t.a                       # tangents from one point are equal
        else:
            assert ans + t.a == 180                 # OAPB has two right angles


# ── Conic sections and the right-triangle figure ─────────────────────────────

def _conic_value(eq: str, x: float, y: float) -> float:
    """lhs − rhs of an equation as the conic set prints it."""
    m = re.fullmatch(r"([xy])\^\{2\} = (-?\d+)([xy])", eq)
    if m:
        sq, k, lin = m.groups()
        v = {"x": x, "y": y}
        return v[sq] ** 2 - int(k) * v[lin]
    m = re.fullmatch(r"\\frac\{([xy])\^\{2\}\}\{(\d+)\} ([+-]) \\frac\{([xy])\^\{2\}\}\{(\d+)\} = 1", eq)
    v1, d1, sign, v2, d2 = m.groups()
    v = {"x": x, "y": y}
    return v[v1] ** 2 / int(d1) + (1 if sign == "+" else -1) * v[v2] ** 2 / int(d2) - 1


def _conic_points(g) -> list[tuple[float, float]]:
    """Points read off the drawing, independent of the set's helpers."""
    if g.kind == "par":
        pt = (2 * abs(g.a), g.a) if g.vertical else (g.a, 2 * abs(g.a))
        mirror = (-pt[0], pt[1]) if g.vertical else (pt[0], -pt[1])
        return [(0, 0), pt, mirror]
    if g.kind == "ell":
        return [(g.a, 0), (-g.a, 0), (0, g.b), (0, -g.b)]
    u = 1.0
    if g.vertical:
        return [(0, g.a), (g.b * math.sinh(u), g.a * math.cosh(u))]
    return [(g.a, 0), (g.a * math.cosh(u), g.b * math.sinh(u))]


def test_conic_graph():
    for q, g, _ in _each("math.conic_graph_picture_m4"):
        s, a = _stem(q), _answer(q)
        if "สมการใด" in s:
            on = lambda eq: all(abs(_conic_value(eq, x, y)) < 1e-9 for x, y in _conic_points(g))
            assert on(a), (g, a)
            assert not any(on(w) for i, w in enumerate(_choices(q)) if i != q.answer)
        elif "โฟกัส" in s:
            # y² = 4px: the labelled point (p, 2p) gives 4p² = 4p·p.
            p = g.a
            assert a == (f"(0, {p})" if g.vertical else f"({p}, 0)")
        elif "แกนเอก" in s:
            assert int(a) == 2 * max(g.a, g.b)
        else:
            assert a == (rf"(0, \pm {g.a})" if g.vertical else rf"(\pm {g.a}, 0)")


def test_right_triangle_ratio():
    for q, r, _ in _each("math.right_triangle_ratio_picture_m5"):
        assert r.opp ** 2 + r.adj ** 2 == r.hyp ** 2
        fn = q.stem[1].tex
        want = {r"\sin\theta": Fraction(r.opp, r.hyp), r"\cos\theta": Fraction(r.adj, r.hyp),
                r"\tan\theta": Fraction(r.opp, r.adj)}[fn]
        m = re.fullmatch(r"\\frac\{(\d+)\}\{(\d+)\}", _answer(q))
        assert Fraction(int(m.group(1)), int(m.group(2))) == want
