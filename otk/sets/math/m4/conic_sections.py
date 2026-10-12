"""ภาคตัดกรวย

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม การวัดและเรขาคณิต 1 ม.4/1

Sets moved here from: math_bank_conics, math_diagrams_geo, math_m4.
"""

from __future__ import annotations

import math
from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed, redraw_until_full
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import frac_tex, poly_tex
from otk.sets._support.math_bank_conics import M4, _tex_q, pt, shifted
from otk.sets._support.math_diagrams import _img, _math_q
from otk.sets._support.math_diagrams_geo import CONIC_GRAPHS, ConicGraph
from otk.sets._support.math_m4 import _TRIPLES, _sgn, maths

CONICS = "ภาคตัดกรวย"


#: (a, b, c) with a² = b² + c² — an ellipse with semi-axes a > b and focal distance c.
ELLIPSE = ((5, 4, 3), (5, 3, 4), (13, 12, 5), (10, 8, 6), (10, 6, 8), (13, 5, 12))


#: (a, b, c) with c² = a² + b² — a hyperbola.
HYPERBOLA = ((3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13), (6, 8, 10), (8, 6, 10))


def _text_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right][:3]
    return GeneratedQuestion(stem=stem, correct=[text(right)],
                             distractors=fixed(*[[text(w)] for w in wrongs]), topic=topic)


def standard_tex(kind: str, h: int, k: int, a: int, b: int, horizontal: bool) -> str:
    """(x − h)²/A ± (y − k)²/B = 1 with the major (transverse) axis as asked."""
    X, Y = shifted("x", h), shifted("y", k)
    if kind == "ellipse":
        dx, dy = (a * a, b * b) if horizontal else (b * b, a * a)
        return rf"\frac{{{X}^{{2}}}}{{{dx}}} + \frac{{{Y}^{{2}}}}{{{dy}}} = 1"
    if horizontal:
        return rf"\frac{{{X}^{{2}}}}{{{a * a}}} - \frac{{{Y}^{{2}}}}{{{b * b}}} = 1"
    return rf"\frac{{{Y}^{{2}}}}{{{a * a}}} - \frac{{{X}^{{2}}}}{{{b * b}}} = 1"


def general_coefficients(kind: str, h: int, k: int, a: int, b: int, horizontal: bool):
    """(A, B, D, E, F) with Ax² + By² + Dx + Ey + F = 0 for the standard form above."""
    if kind == "ellipse":
        p, q = (a * a, b * b) if horizontal else (b * b, a * a)    # (x−h)²/p + (y−k)²/q = 1
        A, B, rhs = q, p, p * q
    elif horizontal:
        A, B, rhs = b * b, -a * a, a * a * b * b                   # b²(x−h)² − a²(y−k)² = a²b²
    else:
        A, B, rhs = -a * a, b * b, a * a * b * b                   # b²(y−k)² − a²(x−h)² = a²b²
    return A, B, -2 * A * h, -2 * B * k, A * h * h + B * k * k - rhs


def vertices(h: int, k: int, a: int, horizontal: bool):
    return ((h - a, k), (h + a, k)) if horizontal else ((h, k - a), (h, k + a))


def ellipse_foci_distance(sum_of_distances: int, d: int) -> tuple[int, int]:
    """2c as k·√m for an ellipse with PF₁ + PF₂ = 2a and one semi-axis d:
    the other semi-axis is a (the major one), and c = √(a² − d²)."""
    a = sum_of_distances // 2
    c2 = a * a - d * d
    k = max(v for v in range(1, math.isqrt(c2) + 1) if c2 % (v * v) == 0)
    return 2 * k, c2 // (k * k)


def _radical(k: int, m: int) -> str:
    if m == 1:
        return str(k)
    return rf"{'' if k == 1 else k}\sqrt{{{m}}}"


def _simplify_root(n: int) -> tuple[int, int]:
    k = max(v for v in range(1, math.isqrt(n) + 1) if n % (v * v) == 0)
    return k, n // (k * k)


CONIC_ALT = "กราฟภาคตัดกรวยที่มีจุดศูนย์กลางหรือจุดยอดอยู่ที่จุดกำเนิด บนระนาบพิกัดที่มีเส้นตารางช่องละ 1 หน่วย"


def conic_equation(g: ConicGraph) -> str:
    if g.kind == "par":
        return rf"x^{{2}} = {4 * g.a}y" if g.vertical else rf"y^{{2}} = {4 * g.a}x"
    x2, y2 = rf"\frac{{x^{{2}}}}{{{g.a * g.a}}}", rf"\frac{{y^{{2}}}}{{{g.b * g.b}}}"
    if g.kind == "ell":
        return rf"{x2} + {y2} = 1"
    if g.vertical:
        return rf"\frac{{y^{{2}}}}{{{g.a * g.a}}} - \frac{{x^{{2}}}}{{{g.b * g.b}}} = 1"
    return rf"{x2} - {y2} = 1"


_CONIC_TOPIC = "ภาคตัดกรวย"


def _ellipse_triples():
    # (a, b, c) with a² = b² + c², so foci and axes are whole.
    return ((5, 4, 3), (5, 3, 4), (13, 12, 5), (13, 5, 12), (10, 8, 6), (10, 6, 8), (17, 15, 8),
            (25, 24, 7))


@question_type("math.conic_graph_picture_m4", display_name={"th": "อ่านสมการภาคตัดกรวยจากกราฟ"},
               level={"th": "ม.4"}, topic="ภาคตัดกรวย")
class ConicGraphPictureM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        g = rng.choice(CONIC_GRAPHS)
        img = _img(g.asset_id, CONIC_ALT)
        right = conic_equation(g)
        if rng.random() < 0.55:
            if g.kind == "par":
                # The wrong axis, the wrong sign, and 2p for 4p.
                wrongs = [conic_equation(g._replace(vertical=not g.vertical)), conic_equation(g._replace(a=-g.a)),
                          rf"x^{{2}} = {2 * g.a}y" if g.vertical else rf"y^{{2}} = {2 * g.a}x"]
            elif g.kind == "ell":
                wrongs = [conic_equation(g._replace(a=g.b, b=g.a)),
                          rf"\frac{{x^{{2}}}}{{{g.a}}} + \frac{{y^{{2}}}}{{{g.b}}} = 1",
                          right.replace("+", "-")]
            else:
                wrongs = [conic_equation(g._replace(vertical=not g.vertical)), right.replace("-", "+"),
                          conic_equation(g._replace(a=g.b, b=g.a))]
            return _math_q([text("กราฟนี้เป็นกราฟของสมการใด"), img], right, wrongs, self.topic)
        if g.kind == "par":
            p = g.a
            focus = f"(0, {p})" if g.vertical else f"({p}, 0)"
            wrongs = [f"({p}, 0)" if g.vertical else f"(0, {p})", f"(0, {4 * p})" if g.vertical else f"({4 * p}, 0)",
                      f"(0, {-p})" if g.vertical else f"({-p}, 0)"]
            return _math_q([text("พาราโบลาในรูปมีจุดยอดที่จุดกำเนิด โฟกัสของพาราโบลาคือจุดใด"), img], focus, wrongs,
                           self.topic)
        if g.kind == "ell":
            big, small = max(g.a, g.b), min(g.a, g.b)
            return _math_q([text("แกนเอกของวงรีในรูปยาวกี่หน่วย"), img], str(2 * big),
                           [str(big), str(2 * small), str(g.a + g.b)], self.topic)
        vert = rf"(0, \pm {g.a})" if g.vertical else rf"(\pm {g.a}, 0)"
        wrongs = [rf"(\pm {g.b}, 0)" if not g.vertical else rf"(0, \pm {g.b})",
                  rf"(\pm {g.a}, 0)" if g.vertical else rf"(0, \pm {g.a})",
                  rf"(\pm {g.a * g.a}, 0)" if not g.vertical else rf"(0, \pm {g.a * g.a})"]
        return _math_q([text("จุดยอดของไฮเพอร์โบลาในรูปคือจุดใด"), img], vert, wrongs, self.topic)
ConicGraphPictureM4.PROVENANCE = Provenance("original")


@question_type("math.conic_general_form_m4",
               display_name={"th": "ภาคตัดกรวยจากสมการรูปทั่วไป"},
               level=M4, topic=CONICS)
class ConicGeneralFormM4(QuestionType):
    @redraw_until_full()
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.choice(("ellipse", "hyperbola"))
        a, b, c = rng.choice(ELLIPSE if kind == "ellipse" else HYPERBOLA)
        h, k = rng.randint(-5, 5), rng.randint(-5, 5)
        horizontal = rng.random() < 0.5
        A, B, D, E, F = general_coefficients(kind, h, k, a, b, horizontal)
        g = math.gcd(math.gcd(A, B), math.gcd(math.gcd(D, E), F))
        sign = -1 if A < 0 else 1                         # lead with a positive x² term
        A, B, D, E, F = (sign * v // g for v in (A, B, D, E, F))
        general = poly_tex((A, "x^{2}"), (B, "y^{2}"), (D, "x"), (E, "y"), (F, "")) + " = 0"
        name = "วงรี" if kind == "ellipse" else "ไฮเพอร์โบลา"
        ask = rng.choice(("vertices", "foci"))
        dist = a if ask == "vertices" else c
        both = lambda d, hor: " และ ".join(pt(*p) for p in vertices(h, k, d, hor))
        right = both(dist, horizontal)
        # The other axis; using b (or a) instead; the centre's signs flipped.
        wrongs = [both(dist, not horizontal), both(b if ask == "vertices" else a, horizontal),
                  " และ ".join(pt(*p) for p in vertices(-h, -k, dist, horizontal))]
        what = "จุดยอด" if ask == "vertices" else "โฟกัส"
        stem = [text("กราฟของสมการ"), content_math(general),
                text(f"เป็น{name} {what}ของ{name}นี้คือข้อใด")]
        return _text_q(stem, right, wrongs, self.topic)
ConicGeneralFormM4.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/7 เรขาคณิตวิเคราะห์ และภาคตัดกรวย',))


@question_type("math.parabola_conic_m4",
               display_name={"th": "พาราโบลา: จุดยอด โฟกัส และไดเรกตริกซ์"},
               level=M4, topic=_CONIC_TOPIC)
class ParabolaConicM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice([v for v in range(-5, 6) if v])
        h, k = rng.randint(-4, 4), rng.randint(-4, 4)
        vertical = rng.random() < 0.5            # (x − h)² = 4p(y − k): opens up/down
        xh = f"(x {_sgn(-h)})" if h else "x"
        yk = f"(y {_sgn(-k)})" if k else "y"
        eq = (rf"{xh}^{{2}} = {4 * p}{yk}" if vertical else rf"{yk}^{{2}} = {4 * p}{xh}")
        focus = (h, k + p) if vertical else (h + p, k)
        pt = lambda a: f"({a[0]}, {a[1]})"
        kind = rng.randrange(3)
        if kind == 0:
            wrongs = [pt((h, k + 4 * p)) if vertical else pt((h + 4 * p, k)),
                      pt((h + p, k)) if vertical else pt((h, k + p)),
                      pt((h, k - p)) if vertical else pt((h - p, k)), pt((h, k))]
            return maths([text("จงหาโฟกัสของพาราโบลา"), content_math(eq)], pt(focus), wrongs, self.topic)
        if kind == 1:
            right = f"y = {k - p}" if vertical else f"x = {h - p}"
            wrongs = ([f"y = {k + p}", f"x = {h - p}", f"y = {k - 4 * p}"] if vertical
                      else [f"x = {h + p}", f"y = {k - p}", f"x = {h - 4 * p}"])
            return maths([text("จงหาสมการไดเรกตริกซ์ของพาราโบลา"), content_math(eq)], right, wrongs,
                          self.topic)
        return maths([text("จงหาจุดยอดของพาราโบลา"), content_math(eq)], pt((h, k)),
                      [pt((-h, -k)), pt((k, h)) if (k, h) != (h, k) else pt((h + 1, k)), pt(focus),
                       pt((h, -k)) if k else pt((h, k + 1))], self.topic)
ParabolaConicM4.PROVENANCE = Provenance("original")


@question_type("math.ellipse_m4", display_name={"th": "วงรี: แกนเอก แกนโท และโฟกัส"},
               level=M4, topic=_CONIC_TOPIC)
class EllipseM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        a, b, c = rng.choice(_ellipse_triples())
        horizontal = rng.random() < 0.5
        eq = (rf"\frac{{x^{{2}}}}{{{a * a}}} + \frac{{y^{{2}}}}{{{b * b}}} = 1" if horizontal
              else rf"\frac{{x^{{2}}}}{{{b * b}}} + \frac{{y^{{2}}}}{{{a * a}}} = 1")
        kind = rng.randrange(3)
        if kind == 0:
            right = f"(\\pm {c}, 0)" if horizontal else f"(0, \\pm {c})"
            wrongs = [f"(\\pm {a}, 0)" if horizontal else f"(0, \\pm {a})",
                      f"(0, \\pm {c})" if horizontal else f"(\\pm {c}, 0)",
                      f"(\\pm {b}, 0)" if horizontal else f"(0, \\pm {b})",
                      f"(\\pm {a * a - b * b}, 0)" if horizontal else f"(0, \\pm {a * a - b * b})"]
            return maths([text("จงหาโฟกัสของวงรี"), content_math(eq)], right, wrongs, self.topic)
        if kind == 1:
            return maths([text("แกนเอกของวงรีนี้ยาวกี่หน่วย"), content_math(eq)], str(2 * a),
                          [str(a), str(2 * b), str(a * a), str(2 * c)], self.topic)
        return maths([text("แกนโทของวงรีนี้ยาวกี่หน่วย"), content_math(eq)], str(2 * b),
                      [str(b), str(2 * a), str(b * b), str(2 * c)], self.topic)
EllipseM4.PROVENANCE = Provenance("original")


@question_type("math.conic_focal_definition_m4",
               display_name={"th": "สมการวงรีและไฮเพอร์โบลาจากโฟกัส"},
               level=M4, topic=CONICS)
class ConicFocalDefinitionM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.65:
            kind = rng.choice(("ellipse", "hyperbola"))
            a, b, c = rng.choice(ELLIPSE if kind == "ellipse" else HYPERBOLA)
            h, k = rng.randint(-4, 4), rng.randint(-4, 4)
            horizontal = rng.random() < 0.5
            f1, f2 = vertices(h, k, c, horizontal)
            if kind == "ellipse":
                d1 = rng.randint(a - c + 1, a + c - 1) if a - c + 1 <= a + c - 1 else a
                d2 = 2 * a - d1
                given = f"PF₁ = {d1} และ PF₂ = {d2}"
            else:
                d2 = rng.randint(c - a + 1, c + a + 6)
                d1 = d2 + 2 * a
                given = f"PF₁ = {d1} และ PF₂ = {d2}"
            name = "วงรี" if kind == "ellipse" else "ไฮเพอร์โบลา"
            right = standard_tex(kind, h, k, a, b, horizontal)
            # c² in place of b²; the axes swapped; a in place of a².
            # (For an ellipse, swapping a and b is the same as swapping the axes, hence
            # the extra candidates: the centre's signs flipped, and c with a.)
            wrongs = [standard_tex(kind, h, k, a, c, horizontal),
                      standard_tex(kind, h, k, a, b, not horizontal),
                      standard_tex(kind, h, k, b, a, horizontal),
                      standard_tex(kind, -h, -k, a, b, horizontal) if (h, k) != (0, 0)
                      else standard_tex(kind, h, k, c, b, horizontal),
                      standard_tex(kind, h, k, c, a, horizontal)]
            stem = [text(f"ให้ P เป็นจุดบน{name}ซึ่งมีโฟกัสอยู่ที่ F₁{pt(*f1)} และ F₂{pt(*f2)} "
                         f"ถ้า {given} แล้วสมการ{name}คือข้อใด")]
            return _tex_q(stem, right, wrongs, self.topic)
        # The distance between the foci, from PF₁ + PF₂ and one semi-axis.
        while True:
            d, a = rng.randint(2, 6), rng.randint(3, 9)
            if a > d:
                break
        h, k = rng.randint(-4, 4), rng.randint(-4, 4)
        kk, m = ellipse_foci_distance(2 * a, d)
        right = _radical(kk, m)
        X, Y = shifted("x", h), shifted("y", k)
        stem = [text(f"ให้ r และ s เป็นจำนวนจริงบวก ถ้า P{pt(h + d, k)} เป็นจุดบนวงรี"),
                content_math(rf"\frac{{{X}^{{2}}}}{{r^{{2}}}} + \frac{{{Y}^{{2}}}}{{s^{{2}}}} = 1"),
                text(f"ซึ่งมีโฟกัส F₁ และ F₂ และ PF₁ + PF₂ = {2 * a} แล้วระยะระหว่าง F₁ และ F₂ เท่ากับเท่าใด")]
        # c instead of 2c; a² + d² under the root (the hyperbola's rule); 2a.
        wrongs = [_radical(kk // 2, m), _radical(*_simplify_root(4 * (a * a + d * d))), str(2 * a),
                  str(2 * d)]
        return _tex_q(stem, right, wrongs, self.topic)
ConicFocalDefinitionM4.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/7 เรขาคณิตวิเคราะห์ และภาคตัดกรวย',))


@question_type("math.hyperbola_m4", display_name={"th": "ไฮเพอร์โบลา: โฟกัส จุดยอด และเส้นกำกับ"},
               level=M4, topic=_CONIC_TOPIC)
class HyperbolaM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        a, b, c = rng.choice(_TRIPLES[:6])
        if rng.random() < 0.5:
            a, b = b, a
        eq = rf"\frac{{x^{{2}}}}{{{a * a}}} - \frac{{y^{{2}}}}{{{b * b}}} = 1"
        kind = rng.randrange(3)
        if kind == 0:
            return maths([text("จงหาโฟกัสของไฮเพอร์โบลา"), content_math(eq)], f"(\\pm {c}, 0)",
                          [f"(\\pm {a}, 0)", f"(0, \\pm {c})", f"(\\pm {abs(a * a - b * b)}, 0)"
                           if a != b else "(\\pm 1, 0)", f"(\\pm {b}, 0)"], self.topic)
        if kind == 1:
            return maths([text("จงหาจุดยอดของไฮเพอร์โบลา"), content_math(eq)], f"(\\pm {a}, 0)",
                          [f"(\\pm {c}, 0)", f"(0, \\pm {b})", f"(\\pm {b}, 0)", f"(\\pm {a * a}, 0)"],
                          self.topic)
        slope = Fraction(b, a)
        right = rf"y = \pm {frac_tex(slope)}x"
        return maths([text("จงหาสมการเส้นกำกับของไฮเพอร์โบลา"), content_math(eq)], right,
                      [rf"y = \pm {frac_tex(1 / slope)}x", rf"y = \pm {frac_tex(slope * slope)}x",
                       rf"y = \pm {frac_tex(Fraction(c, a))}x", rf"y = \pm {frac_tex(Fraction(b * b, a * a) + 1)}x"],
                      self.topic)
HyperbolaM4.PROVENANCE = Provenance("original")
