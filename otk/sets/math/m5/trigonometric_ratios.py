"""อัตราส่วนตรีโกณมิติ

คณิตศาสตร์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 2 ม.5/1

Sets moved here from: math, math_apply_add, math_bank_trig, math_diagrams_geo, math_thin_topics.
"""

from __future__ import annotations

import math
from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_tex
from otk.sets._support.math_apply_add import M5 as M5_math_apply_add
from otk.sets._support.math_apply_add import _c
from otk.sets._support.math_bank_trig import (
    M5 as M5_math_bank_trig,
)
from otk.sets._support.math_bank_trig import (
    TRIPLES,
    _frac_q,
    _tex_q,
    simplify_root,
    surd_tex,
)
from otk.sets._support.math_chapters import _SIN, _distinct, _div, _mul, _surd_tex
from otk.sets._support.math_diagrams import _img, _math_q
from otk.sets._support.math_diagrams_geo import RIGHT_TRIANGLES, RightTriangle
from otk.sets._support.math_p2 import _maths
from otk.sets._support.math_thin_topics import M5

_TRIG_RATIOS = [
    (r"\sin", 0, "0"), (r"\sin", 30, r"\frac{1}{2}"),
    (r"\sin", 45, r"\frac{\sqrt{2}}{2}"), (r"\sin", 60, r"\frac{\sqrt{3}}{2}"),
    (r"\sin", 90, "1"),
    (r"\cos", 0, "1"), (r"\cos", 30, r"\frac{\sqrt{3}}{2}"),
    (r"\cos", 45, r"\frac{\sqrt{2}}{2}"), (r"\cos", 60, r"\frac{1}{2}"),
    (r"\cos", 90, "0"),
    (r"\tan", 0, "0"), (r"\tan", 30, r"\frac{\sqrt{3}}{3}"),
    (r"\tan", 45, "1"), (r"\tan", 60, r"\sqrt{3}"),
]


def _sqrt3(k: Fraction) -> str:
    """k·√3 with k rational."""
    if k.denominator == 1:
        return ("" if k == 1 else str(k.numerator)) + r"\sqrt{3}"
    return rf"\frac{{{k.numerator}\sqrt{{3}}}}{{{k.denominator}}}"


RATIOS = "อัตราส่วนตรีโกณมิติ"


def area_from_hypotenuse_and_tan(c: int, p: int, q: int) -> Fraction:
    """C = 90°, AB = c, tan A = p/q: a = cp/√(p² + q²), b = cq/√(p² + q²), area ½ab."""
    return Fraction(c * c * p * q, 2 * (p * p + q * q))


def sine_sum_from_area(c: int, area: Fraction) -> Fraction:
    """sin A + sin B = (a + b)/c with (a + b)² = c² + 4·area; returned exact when a perfect square."""
    s2 = c * c + 4 * Fraction(area)
    root = math.isqrt(s2.numerator)
    assert s2.denominator == 1 and root * root == s2.numerator
    return Fraction(root, c)


def area_from_scaled_sines(u: Fraction, v: Fraction) -> Fraction:
    """c² sin A = u, c² sin B = v: c⁴ = u² + v², area = ½(c sin A)(c sin B) = uv / (2c²).

    Returns the area's square, so an irrational v (like k√3) can be passed as v².
    """
    return (u * u) * v / (4 * (u * u + v))


#: Allowed (p, q) for tan A = p/q and the hypotenuses that give a whole-number area.
TAN_HYPOTENUSE = {(p, q): [c for c in range(2, 21) if area_from_hypotenuse_and_tan(c, p, q).denominator == 1]
                  for p, q in ((1, 2), (1, 3), (2, 3), (3, 4), (1, 4), (1, 1), (2, 1), (3, 1))}


def right_triangle_alt(r: RightTriangle) -> str:
    sides = {"o": f"ด้านตรงข้ามมุม θ ยาว {r.opp} หน่วย", "a": f"ด้านประชิดมุม θ ยาว {r.adj} หน่วย",
             "h": f"ด้านตรงข้ามมุมฉากยาว {r.hyp} หน่วย"}
    return "รูปสามเหลี่ยมมุมฉากมีมุม θ " + " ".join(sides[c] for c in r.shown)


_TRIPLES = ((3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29))


_TAN = {30: (Fraction(1, 3), 3), 45: (Fraction(1), 1), 60: (Fraction(1), 3)}


@question_type("math.trig_ratio",
               display_name={"th": "ค่าตรีโกณมิติของมุมพิเศษ"}, level={"th": "ม.5"},
               topic="อัตราส่วนตรีโกณมิติ")
class TrigRatio(MathType):
    def expr(self, rng: Random):
        fn, deg, val = rng.choice(_TRIG_RATIOS)
        return MathDraw(rf"{fn} {deg}^{{\circ}}", val, prompt="จงหาค่าแบบแม่นตรง")
TrigRatio.PROVENANCE = Provenance("original")


@question_type("math.right_triangle_ratio_picture_m5", display_name={"th": "อัตราส่วนตรีโกณมิติจากรูปสามเหลี่ยมมุมฉาก"},
               level={"th": "ม.5"}, topic="อัตราส่วนตรีโกณมิติ")
class RightTriangleRatioPictureM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        r = rng.choice(RIGHT_TRIANGLES)
        o, a, h = r.opp, r.adj, r.hyp
        ratios = {r"\sin\theta": Fraction(o, h), r"\cos\theta": Fraction(a, h), r"\tan\theta": Fraction(o, a)}
        ask = rng.choice(sorted(ratios))
        right = ratios[ask]
        # The other two ratios, and each one upside down.
        pool = [frac_tex(v) for v in ratios.values()] + [frac_tex(1 / v) for v in ratios.values()]
        wrongs = [w for w in dict.fromkeys(pool) if w != frac_tex(right)]
        rng.shuffle(wrongs)
        return _math_q([text("จากรูป จงหาค่าของ"), content_math(ask),
                        _img(r.asset_id, right_triangle_alt(r))], frac_tex(right), wrongs[:3], self.topic)
RightTriangleRatioPictureM5.PROVENANCE = Provenance("original")


@question_type("math.right_triangle_relations_m5",
               display_name={"th": "ความสัมพันธ์ของด้านและมุมในรูปสามเหลี่ยมมุมฉาก"},
               level=M5_math_bank_trig, topic=RATIOS)
class RightTriangleRelationsM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        given = [text("กำหนดให้ ABC เป็นรูปสามเหลี่ยมที่มีมุม C เป็นมุมฉาก")]
        if kind == 0:
            p, q = rng.choice(list(TAN_HYPOTENUSE))
            c = rng.choice(TAN_HYPOTENUSE[(p, q)])
            right = area_from_hypotenuse_and_tan(c, p, q)
            stem = [*given, text(f"ถ้าด้าน AB ยาว {c} หน่วย และ"), content_math(rf"\tan A = {frac_tex(Fraction(p, q))}"),
                    text("แล้วพื้นที่ของรูปสามเหลี่ยม ABC เท่ากับกี่ตารางหน่วย")]
            # AB taken as the leg next to A (½·c·c tan A); forgetting ½; AB as the leg opposite A.
            named = [Fraction(c * c * p, 2 * q), 2 * right, Fraction(c * c * q, 2 * p)]
            return _frac_q(stem, right, named, self.topic)
        if kind == 1:
            p, q, r = rng.choice(TRIPLES)
            k = rng.randint(1, 3)
            c, area = k * r, Fraction(k * k * p * q, 2)
            right = sine_sum_from_area(c, area)
            stem = [*given, text(f"ถ้าด้าน AB ยาว {c} หน่วย และพื้นที่ของรูปสามเหลี่ยมเท่ากับ "
                                 f"{area} ตารางหน่วย แล้ว"),
                    content_math(r"\sin A + \sin B"), text("เท่ากับเท่าใด")]
            # sin A · sin B; 2·area/c; the reciprocal; |sin A − sin B|.
            named = [Fraction(2 * area, c * c), Fraction(2 * area, c), 1 / right, Fraction(abs(p - q), r)]
            return _frac_q(stem, right, named, self.topic)
        if kind == 2:
            p, q = rng.choice(((1, 3), (1, 2), (2, 3), (1, 4), (3, 4), (2, 5), (3, 5), (5, 13)))
            k, m = simplify_root(q * q - p * p)
            if rng.random() < 0.5:
                stem = [*given, text("ถ้า"), content_math(rf"\sin A = {frac_tex(Fraction(p, q))}"), text("แล้ว"),
                        content_math(r"\sin B"), text("เท่ากับเท่าใด")]
                # sin B = sin A; 1 − sin A; cot A; tan A.
                wrongs = [frac_tex(Fraction(p, q)), frac_tex(Fraction(q - p, q)), surd_tex(Fraction(k, p), m),
                          surd_tex(Fraction(p, k * m), m)]
                return _tex_q(stem, surd_tex(Fraction(k, q), m), wrongs, self.topic)
            cot = surd_tex(Fraction(k, p), m)
            tan = surd_tex(Fraction(p, k * m), m)
            stem = [*given, text("มี a, b และ c เป็นความยาวด้านตรงข้ามมุม A, B และ C ตามลำดับ ถ้า"),
                    content_math(rf"\sin A = {frac_tex(Fraction(p, q))}"), text("แล้วข้อใดถูกต้อง")]
            coef = lambda t: "" if t == "1" else t
            # b and a swapped; the hypotenuse ratio; the plain sine ratio.
            wrongs = [rf"a = {coef(cot)}b", rf"b = {coef(tan)}a", rf"b = {coef(str(q) if p == 1 else frac_tex(Fraction(q, p)))}a",
                      rf"a = {coef(frac_tex(Fraction(q, p)))}b"]
            return _tex_q(stem, rf"b = {coef(cot)}a", wrongs, self.topic)
        stem_u = lambda u, v: [*given, text("มี a, b และ c เป็นความยาวด้านตรงข้ามมุม A, B และ C ตามลำดับ ถ้า"),
                               content_math(rf"c^{{2}}\sin A = {u}"), text("และ"),
                               content_math(rf"c^{{2}}\sin B = {v}"),
                               text("แล้วพื้นที่ของรูปสามเหลี่ยม ABC เท่ากับกี่ตารางหน่วย")]
        if rng.random() < 0.5:
            p, q, r = rng.choice(TRIPLES[:6])
            k = rng.randint(1, 4)
            u, v = k * p, k * q
            right = Fraction(u * v, 2 * k * r)
            assert right * right == area_from_scaled_sines(Fraction(u), Fraction(v * v))
            # Forgetting ½; uv/2 (c² dropped); dividing by c⁴ instead of c².
            named = [2 * right, Fraction(u * v, 2), Fraction(u * v, 2 * k * k * r * r)]
            return _frac_q(stem_u(u, v), right, named, self.topic)
        k = rng.randint(1, 6)
        # u = k, v = k√3: c² = 2k, area = k√3/4.
        right = surd_tex(Fraction(k, 4), 3)
        wrongs = [surd_tex(Fraction(k, 2), 3), frac_tex(Fraction(3 * k, 4)), surd_tex(Fraction(k * k, 2), 3),
                  surd_tex(Fraction(k, 8), 3)]
        return _tex_q(stem_u(str(k), surd_tex(Fraction(k), 3)), right, wrongs, self.topic)
RightTriangleRelationsM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/8 ตรีโกณมิติ',))


@question_type("math.trig_ratio_triangle_m5", display_name={"th": "อัตราส่วนตรีโกณมิติจากรูปสามเหลี่ยมมุมฉาก"},
               level=M5, topic="อัตราส่วนตรีโกณมิติ")
class TrigRatioTriangleM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        a, b, c = rng.choice(_TRIPLES)
        if rng.random() < 0.5:
            a, b = b, a
        # C is the right angle: BC = a faces A, AC = b faces B, AB = c.
        given = rng.choice((("AB", c, "BC", a), ("AB", c, "AC", b), ("BC", a, "AC", b)))
        ratios = {r"\sin A": Fraction(a, c), r"\cos A": Fraction(b, c), r"\tan A": Fraction(a, b),
                  r"\sin B": Fraction(b, c), r"\cos B": Fraction(a, c), r"\tan B": Fraction(b, a)}
        ask = rng.choice(sorted(ratios))
        right = ratios[ask]
        wrongs = _distinct(frac_tex(right), *[frac_tex(v) for v in ratios.values()], frac_tex(1 / right))
        return _maths([text(f"รูปสามเหลี่ยม ABC มีมุม C เป็นมุมฉาก {given[0]} = {given[1]} และ "
                            f"{given[2]} = {given[3]} จงหาค่าของ"), content_math(ask)],
                      frac_tex(right), wrongs[:3], self.topic)
TrigRatioTriangleM5.PROVENANCE = Provenance("original")


@question_type("math.two_angle_height_m5",
               display_name={"th": "มุมเงยสองมุมและมุมก้ม: หาความสูงและระยะทาง"},
               level=M5_math_apply_add, topic="อัตราส่วนตรีโกณมิติ")
class TwoAngleHeightM5(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(5)
        if kind == 0:
            d = 2 * rng.randint(5, 30)
            h = Fraction(d, 2)                       # h = d·√3/2
            return MathDraw("", _sqrt3(h),
                            prompt=(f"ยืนที่จุด A มองยอดเสาธงเป็นมุมเงย 30 องศา เดินตรงเข้าหาเสาอีก {d} เมตร "
                                    f"ถึงจุด B มองยอดเสาเป็นมุมเงย 60 องศา เสาธงสูงกี่เมตร"),
                            distractors=[_sqrt3(h * 2), str(d), _sqrt3(h / 3), str(d // 2)])
        if kind == 1:
            d = 2 * rng.randint(5, 30)
            return MathDraw("", str(d // 2),
                            prompt=(f"ยืนริมแม่น้ำมองยอดต้นไม้ที่อีกฝั่งเป็นมุมเงย 60 องศา เมื่อถอยหลังออกมาตรง ๆ "
                                    f"อีก {d} เมตร มองยอดต้นไม้เดิมเป็นมุมเงย 30 องศา แม่น้ำกว้างกี่เมตร"),
                            distractors=_story.keep(d, 2 * d, d // 3 if d % 3 == 0 else d + d // 2,
                                                    answer=d // 2, lo=1)
                            + [_sqrt3(Fraction(d, 2))])
        if kind == 2:
            h = 3 * rng.randint(4, 20)
            gap = Fraction(2 * h, 3)                 # h√3 − h/√3 = 2h√3/3
            return MathDraw("", _sqrt3(gap),
                            prompt=(f"จากยอดประภาคารสูง {h} เมตร มองเรือสองลำที่อยู่ในแนวเดียวกันกับฐานประภาคาร "
                                    f"เป็นมุมก้ม 60 องศา และ 30 องศา เรือทั้งสองลำอยู่ห่างกันกี่เมตร"),
                            distractors=[_sqrt3(Fraction(h)), _sqrt3(Fraction(h, 3)), _sqrt3(gap * 2), str(h)])
        if kind == 3:
            H = 3 * rng.randint(3, 15)
            tower = H + H // 3                       # gap = H/√3, rise = gap/√3 = H/3
            return MathDraw("", str(tower),
                            prompt=(f"จากดาดฟ้าตึกสูง {H} เมตร มองยอดหอคอยที่อยู่ตรงข้ามเป็นมุมเงย 30 องศา "
                                    f"และมองฐานหอคอยเป็นมุมก้ม 60 องศา หอคอยสูงกี่เมตร"),
                            distractors=_story.keep(H + H, H + 3 * H, H // 3, H + H // 3 * 2,
                                                    answer=tower, lo=1))
        m, t = rng.randint(2, 12), rng.choice((5, 10, 20))
        h = 3 * t * m                                 # speed = 2h/(√3·t) = 2m√3
        return MathDraw("", _sqrt3(Fraction(2 * m)),
                        prompt=(f"เครื่องบินบินในแนวระดับที่ความสูง {_c(h)} เมตร ผู้สังเกตบนพื้นมองเห็นเครื่องบินเป็นมุมเงย "
                                f"60 องศา อีก {t} วินาทีต่อมามองเห็นเป็นมุมเงย 30 องศา "
                                f"เครื่องบินบินด้วยอัตราเร็วกี่เมตรต่อวินาที"),
                        distractors=[_sqrt3(Fraction(m)), _sqrt3(Fraction(4 * m)), _sqrt3(Fraction(2 * m, 3)),
                                     str(2 * m)])
TwoAngleHeightM5.PROVENANCE = Provenance("original")


@question_type("math.angle_of_elevation_m5", display_name={"th": "มุมเงยและระยะทาง"},
               level=M5, topic="อัตราส่วนตรีโกณมิติ")
class AngleOfElevationM5(WordProblem):
    def expr(self, rng: Random):
        theta = rng.choice((30, 45, 60))
        n = rng.choice((6, 10, 12, 20, 24, 30))
        whole = (Fraction(n), 1)
        if rng.random() < 0.55:
            h = _mul(whole, _TAN[theta])
            thing = rng.choice(("เสาธง", "ต้นไม้", "ตึก"))
            right = _surd_tex(h)
            # sin or cos in place of tan, and tan of the other angle.
            wrongs = _distinct(right, _surd_tex(_mul(whole, _SIN[theta])), _surd_tex(_mul(whole, _SIN[90 - theta])),
                               _surd_tex(_mul(whole, _TAN[90 - theta])), str(n + 1))
            return MathDraw("", right,
                            prompt=(f"ยืนห่างจากโคน{thing} {n} เมตร มองเห็นยอด{thing}เป็นมุมเงย {theta} องศา "
                                    f"{thing}สูงกี่เมตร (ไม่คิดความสูงของผู้มอง)"),
                            distractors=wrongs[:3])
        h = _mul(whole, _SIN[theta])
        right = _surd_tex(h)
        wrongs = _distinct(right, _surd_tex(_mul(whole, _SIN[90 - theta])), _surd_tex(_mul(whole, _TAN[theta])),
                           _surd_tex(_div(whole, _SIN[theta])), str(n))
        return MathDraw("", right,
                        prompt=(f"บันไดยาว {n} เมตร พาดกำแพงโดยทำมุม {theta} องศากับพื้น "
                                f"ปลายบันไดอยู่สูงจากพื้นกี่เมตร"),
                        distractors=wrongs[:3])
AngleOfElevationM5.PROVENANCE = Provenance("original")
