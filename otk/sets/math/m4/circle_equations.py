"""สมการวงกลม

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม การวัดและเรขาคณิต 1 ม.4/1

Sets moved here from: math, math_bank_conics, math_geometry, math_pictures_add.
"""

from __future__ import annotations

import math
from fractions import Fraction
from random import Random

from otk.core.content import image, text
from otk.core.content import math as content_math
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex
from otk.sets._support.math_bank_conics import M4, _tex_q, line_tex, pt, shifted
from otk.sets._support.math_geometry import _TRIPLES
from otk.sets._support.math_pictures_add import CIRCLE_GRIDS, _plus, _q, _shift

_NORMALS = ((3, 4, 5), (4, 3, 5), (5, 12, 13), (12, 5, 13))


def radius_tangent_to_axes_and_line(a: int, b: int, c: int) -> list[Fraction]:
    """r > 0 with centre (r, r) at distance r from ax + by + c = 0 (n = √(a² + b²) integer)."""
    n = math.isqrt(a * a + b * b)
    out = []
    for sign in (1, -1):                                  # (a + b)r + c = ±n·r
        denom = sign * n - (a + b)
        if denom:
            r = Fraction(c, denom)
            if r > 0:
                out.append(r)
    return sorted(set(out))


def radius_tangent_at_point(u: int, v: int, w: int, t: int) -> Fraction:
    """Circle above the x-axis tangent to the line through the origin with direction
    (u, v) at the point t·(u, v), and tangent to the Y axis: its centre is
    t(u, v) + r(−v, u)/w, and the Y-axis condition makes its x-coordinate r."""
    return Fraction(t * u * w, w + v)


def tangent_slope_from_origin(r: int, k: int) -> Fraction:
    """For (x − r)² + (y − k)² = r² (tangent to the Y axis), the other tangent
    through the origin y = mx: (mr − k)² = r²(1 + m²) gives m = (k² − r²)/(2rk)."""
    return Fraction(k * k - r * r, 2 * r * k)


CIRCLE_ALT = "วงกลมบนระนาบพิกัดฉากที่มีเส้นตาราง จุดศูนย์กลางมีจุดทึบ"


def _std(h: int, k: int, rhs: int) -> str:
    return f"({_shift(h)})^{{2}} + ({_shift(k, 'y')})^{{2}} = {rhs}"


def _term(c: int, var: str) -> str:
    """ + 4x / - x / nothing, for a linear term."""
    if c == 0:
        return ""
    mag = "" if abs(c) == 1 else str(abs(c))
    return f" {'+' if c > 0 else '-'} {mag}{var}"


def _general(d: int, e: int, f: int) -> str:
    return f"x^{{2}} + y^{{2}}{_term(d, 'x')}{_term(e, 'y')}{_plus(f)} = 0"


@question_type("math.circle_centre_radius",
               display_name={"th": "จุดศูนย์กลางและรัศมีของวงกลม"},
               level={"th": "ม.5"}, topic="สมการวงกลม")
class CircleCentreRadius(MathType):
    def expr(self, rng: Random, coord_hi: int = 9, radius_hi: int = 10):
        h, k = rng.randint(-coord_hi, coord_hi), rng.randint(-coord_hi, coord_hi)
        r = rng.randint(2, radius_hi)
        sx = f"x {'-' if h >= 0 else '+'} {abs(h)}" if h else "x"
        sy = f"y {'-' if k >= 0 else '+'} {abs(k)}" if k else "y"
        return MathDraw(
            rf"({sx})^2 + ({sy})^2 = {r * r}", f"({h}, {k})",
            prompt="วงกลมนี้มีจุดศูนย์กลางอยู่ที่จุดใด",
            # The sign flip inside the bracket is the whole difficulty.
            distractors=[f"({-h}, {-k})", f"({k}, {h})", f"({h}, {-k})"])
CircleCentreRadius.PROVENANCE = Provenance("original")


@question_type("math.circle_equation",
               display_name={"th": "สมการวงกลม"}, level={"th": "ม.5"},
               topic="สมการวงกลม")
class CircleEquation(MathType):
    def expr(self, rng: Random):
        a, b = rng.randint(-4, 4), rng.randint(-4, 4)
        r = rng.randint(1, 6)
        eq = (rf"(x {'-' if a >= 0 else '+'} {abs(a)})^{{2}} + "
              rf"(y {'-' if b >= 0 else '+'} {abs(b)})^{{2}} = {r * r}")
        if rng.random() < 0.5:
            return MathDraw(rf"C({a}, {b}), \;\; r = {r}", eq, prompt="จงหาสมการวงกลม")
        return MathDraw(eq, rf"C({a}, {b}), \;\; r = {r}",
                        prompt="จงหาจุดศูนย์กลางและรัศมี")
CircleEquation.PROVENANCE = Provenance("original")


@question_type("math.circle_graph_picture_m4",
               display_name={"th": "สมการวงกลมจากภาพบนระนาบพิกัด"},
               level={"th": "ม.4"}, topic="สมการวงกลม")
class CircleGraphPictureM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(CIRCLE_GRIDS)
        img = image(s.asset_id, alt=CIRCLE_ALT)
        h, k, r = s
        if rng.random() < 0.5:
            return _q([text("วงกลมในภาพมีสมการตรงกับข้อใด"), img], _std(h, k, r * r),
                      [_std(-h, -k, r * r), _std(h, k, r), _std(-h, -k, r), _std(k, h, r * r)],
                      self.topic, [])
        f = h * h + k * k - r * r
        return _q([text("เขียนสมการวงกลมในภาพให้อยู่ในรูปทั่วไป จะได้ข้อใด"), img],
                  _general(-2 * h, -2 * k, f),
                  [_general(2 * h, 2 * k, f), _general(-2 * h, -2 * k, h * h + k * k + r * r),
                   _general(-h, -k, f), _general(2 * h, 2 * k, h * h + k * k + r * r)],
                  self.topic, [])
CircleGraphPictureM4.PROVENANCE = Provenance("original")


@question_type("math.circle_tangency_m4",
               display_name={"th": "วงกลมที่สัมผัสเส้นตรงและแกน"},
               level=M4, topic="สมการวงกลม")
class CircleTangencyM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            while True:
                a, b, n = rng.choice(_NORMALS)
                a *= rng.choice((1, -1))
                r_true = rng.randint(2, 9)
                c = rng.choice((1, -1)) * n * r_true - (a + b) * r_true
                roots = radius_tangent_to_axes_and_line(a, b, c)
                if roots == [Fraction(r_true)]:           # exactly one circle fits
                    break
            line = line_tex(a, b, c)
            # The line through the centre and the tangency point runs along the normal (a, b).
            right = line_tex(b, -a, -(b - a) * r_true)
            wrongs = [line_tex(a, b, -(a + b) * r_true),              # parallel to ℓ, not perpendicular
                      line_tex(b, -a, (b - a) * r_true),              # the constant's sign
                      line_tex(b, -a, -(b - a) * (r_true + 1)),       # the centre one step off
                      line_tex(b, a, -(b + a) * r_true)]
            stem = [text("ให้ s เป็นวงกลมในจตุภาคที่ 1 ซึ่งสัมผัสแกน X แกน Y และเส้นตรง"), content_math(line),
                    text("ถ้า C เป็นจุดศูนย์กลางของ s และ P เป็นจุดที่ s สัมผัสเส้นตรงนี้ "
                         "แล้วสมการเส้นตรงที่ผ่าน C และ P คือข้อใด")]
            return _tex_q(stem, right, wrongs, self.topic)
        if kind == 1:
            u, v, w = rng.choice(((4, 3, 5), (3, 4, 5), (12, 5, 13), (5, 12, 13)))
            t = rng.randint(1, 3)
            r = radius_tangent_at_point(u, v, w, t)
            line = rf"{u}y = {v}x"
            stem = [text("วงกลมที่อยู่เหนือแกน X ซึ่งสัมผัสเส้นตรง"), content_math(line),
                    text(f"ที่จุด {pt(t * u, t * v)} และสัมผัสแกน Y มีรัศมีเท่ากับเท่าใด")]
            # w + v flipped to w − v; the tangency point's x; half the distance to the origin.
            wrong = [Fraction(t * u * w, w - v), Fraction(t * u), Fraction(t * w, 2)]
            return _tex_q(stem, frac_tex(r), [frac_tex(x) for x in wrong if x != r]
                          + [frac_tex(r + 1)], self.topic)
        while True:
            r, k = rng.randint(1, 4), rng.randint(1, 6)
            if k != r:
                break
        m = tangent_slope_from_origin(r, k)
        circle = rf"{shifted('x', r)}^{{2}} + {shifted('y', k)}^{{2}} = {r * r}"
        stem = [text("วงกลม"), content_math(circle),
                text("มีเส้นสัมผัสที่ผ่านจุดกำเนิดสองเส้น คือแกน Y และเส้นตรง L ความชันของเส้นตรง L เท่ากับเท่าใด")]
        # The slope to the centre; its reciprocal; the sign flipped.
        wrong = [Fraction(k, r), Fraction(r, k), -m]
        return _tex_q(stem, frac_tex(m), [frac_tex(x) for x in wrong if x != m] + [frac_tex(m + 1)],
                      self.topic)
CircleTangencyM4.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/7 เรขาคณิตวิเคราะห์ และภาคตัดกรวย',))


@question_type("math.circle_from_centre_point",
               display_name={"th": "รัศมีจากจุดศูนย์กลางและจุดบนวงกลม"},
               level={"th": "ม.5"}, topic="สมการวงกลม")
class CircleFromCentrePoint(MathType):
    def expr(self, rng: Random, k_lo: int = 1, k_hi: int = 4):
        a, b, c = rng.choice(_TRIPLES)
        k = rng.randint(k_lo, k_hi)
        h, v = rng.randint(-8, 8), rng.randint(-8, 8)
        px, py = h + a * k, v + b * k
        return MathDraw(
            f"C({h}, {v}), \\; P({px}, {py})", str(c * k),
            prompt="วงกลมมีจุดศูนย์กลาง C และผ่านจุด P จงหารัศมี",
            distractors=[str((c * k) ** 2), str(a * k + b * k), str(c * k * 2)])
CircleFromCentrePoint.PROVENANCE = Provenance("original")

from math import isqrt  # noqa: E402

from otk.core.content import math as _math_block  # noqa: E402
from otk.core.content import text as _text_block  # noqa: E402
from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType  # noqa: E402
from otk.kit.math_problems import poly_tex, sqrt_tex  # noqa: E402
from otk.sets._support.math_m4 import M4 as LEVEL  # noqa: E402
from otk.sets._support.math_p2 import _texts as _fixed_texts  # noqa: E402


def _nz4(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk4(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk4(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk4(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt4(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk4(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk4(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))

# ── More circle equations (2026-11): the centre from the general form, the radius from the general form, a
# point inside or outside, a circle from a diameter's ends, and a circle touching the x-axis ──


def _sq4(sym: str, h: int) -> str:
    return f"({sym} {'-' if h > 0 else '+'} {abs(h)})^{{2}}" if h else f"{sym}^{{2}}"


def _general4(h: int, k: int, r2: int) -> str:
    return f"{poly_tex((1, 'x^{2}'), (1, 'y^{2}'), (-2 * h, 'x'), (-2 * k, 'y'), (h * h + k * k - r2, ''))} = 0"


@question_type("math.circle_centre_general_m4", display_name={"th": "จุดศูนย์กลางจากสมการวงกลมรูปทั่วไป"}, level=LEVEL,
               topic="สมการวงกลม")
class CircleCentreGeneralM4(MathType):
    def expr(self, rng: Random):
        h, k = _nz4(rng, 1, 8), _nz4(rng, 1, 8)
        r = rng.randint(1, 9)
        right = _pt4(h, k)
        wrongs = [_pt4(-h, -k), _pt4(2 * h, 2 * k), _pt4(-2 * h, -2 * k), _pt4(k, h)]
        return MathDraw(_general4(h, k, r * r), right, prompt="วงกลมนี้มีจุดศูนย์กลางที่จุดใด", distractors=_tk4(*wrongs, answer=right))


@question_type("math.circle_radius_general_m4", display_name={"th": "รัศมีจากสมการวงกลมรูปทั่วไป"}, level=LEVEL,
               topic="สมการวงกลม")
class CircleRadiusGeneralM4(MathType):
    def expr(self, rng: Random):
        h, k = _nz4(rng, 1, 8), _nz4(rng, 1, 8)
        r = rng.randint(1, 9)
        f = h * h + k * k - r * r
        # The constant read as r²; r² not rooted; h + k.
        wrongs = [sqrt_tex(abs(f)) if f else "1", str(r * r), str(abs(h) + abs(k)), str(r + 1)]
        return MathDraw(_general4(h, k, r * r), str(r), prompt="วงกลมนี้มีรัศมียาวกี่หน่วย", distractors=_tk4(*wrongs, answer=str(r)))


@question_type("math.point_vs_circle_m4", display_name={"th": "จุดอยู่ภายใน บน หรือภายนอกวงกลม"}, level=LEVEL,
               topic="สมการวงกลม")
class PointVsCircleM4(QuestionType):
    _OPTIONS = ("อยู่ภายในวงกลม", "อยู่บนวงกลม", "อยู่ภายนอกวงกลม", "บอกไม่ได้")

    def build(self, rng: Random, **params):
        h, k = rng.randint(-5, 5), rng.randint(-5, 5)
        r = rng.randint(3, 8)
        kind = rng.randrange(3)
        dx = rng.randint(0, r - 1) if kind == 0 else r if kind == 1 else r + rng.randint(1, 3)
        x, y = h + dx, k
        if kind == 1 and rng.random() < 0.5:
            x, y = h, k + r
        stem = [_text_block(f"จุด ({x}, {y}) อยู่ที่ใดเมื่อเทียบกับวงกลม"), _math_block(f"{_sq4('x', h)} + {_sq4('y', k)} = {r * r}")]
        right = self._OPTIONS[kind]
        return _fixed_texts(stem, right, [o for o in self._OPTIONS if o != right], self.topic)


@question_type("math.circle_from_diameter_m4", display_name={"th": "สมการวงกลมจากปลายเส้นผ่านศูนย์กลาง"}, level=LEVEL,
               topic="สมการวงกลม")
class CircleFromDiameterM4(MathType):
    def expr(self, rng: Random):
        h, k = rng.randint(-6, 6), rng.randint(-6, 6)
        a, b = rng.choice(((3, 4), (4, 3), (5, 12), (12, 5), (6, 8), (8, 6), (0, 5), (5, 0)))
        r2 = a * a + b * b
        p, q = (h - a, k - b), (h + a, k + b)
        right = f"{_sq4('x', h)} + {_sq4('y', k)} = {r2}"
        # The diameter squared; the centre's signs flipped; the radius not squared.
        wrongs = [f"{_sq4('x', h)} + {_sq4('y', k)} = {4 * r2}", f"{_sq4('x', -h)} + {_sq4('y', -k)} = {r2}",
                  f"{_sq4('x', h)} + {_sq4('y', k)} = {isqrt(r2)}"]
        return MathDraw(rf"A{_pt4(*p)}, \; B{_pt4(*q)}", right, prompt="AB เป็นเส้นผ่านศูนย์กลางของวงกลม สมการวงกลมคือข้อใด",
                        distractors=_tk4(*wrongs, answer=right))


@question_type("math.circle_touching_x_axis_m4", display_name={"th": "วงกลมที่สัมผัสแกน x"}, level=LEVEL, topic="สมการวงกลม")
class CircleTouchingXAxisM4(MathType):
    def expr(self, rng: Random):
        h, k = rng.randint(-8, 8), _nz4(rng, 1, 8)
        right = f"{_sq4('x', h)} + {_sq4('y', k)} = {k * k}"
        # The radius from h; the radius not squared; h² + k².
        wrongs = [f"{_sq4('x', h)} + {_sq4('y', k)} = {h * h if h else 1}", f"{_sq4('x', h)} + {_sq4('y', k)} = {abs(k)}",
                  f"{_sq4('x', h)} + {_sq4('y', k)} = {h * h + k * k}"]
        return MathDraw(rf"C({h}, {k})", right, prompt="วงกลมมีจุดศูนย์กลางที่ C และสัมผัสแกน x สมการวงกลมคือข้อใด",
                        distractors=_tk4(*wrongs, answer=right))


CircleCentreGeneralM4.PROVENANCE = Provenance("original")
CircleRadiusGeneralM4.PROVENANCE = Provenance("original")
PointVsCircleM4.PROVENANCE = Provenance("original")
CircleFromDiameterM4.PROVENANCE = Provenance("original")
CircleTouchingXAxisM4.PROVENANCE = Provenance("original")
