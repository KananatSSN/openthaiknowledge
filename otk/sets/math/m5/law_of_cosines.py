"""กฎของโคไซน์

คณิตศาสตร์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 3 ม.5/2

Sets moved here from: math, math_apply_add, math_bank_trig, math_geometry, math_pictures_add.
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
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem, sqrt_tex
from otk.sets._support.math_apply_add import M5, _c, _root
from otk.sets._support.math_bank_trig import M5 as M5_math_bank_trig
from otk.sets._support.math_bank_trig import TRIPLES, _int_q, _tex_q
from otk.sets._support.math_pictures_add import COS_TRIANGLES, _fr, _q, _sqrt

# (p, q, angle, d): sides p and q with the angle between them, and the third side.
_COS_TRIPLES = ((3, 8, 60, 7), (5, 8, 60, 7), (7, 15, 60, 13), (8, 15, 60, 13), (5, 21, 60, 19),
                (16, 21, 60, 19), (3, 5, 120, 7), (7, 8, 120, 13), (5, 16, 120, 19),
                (11, 24, 120, 31), (6, 10, 120, 14))


COSINE_RULE = "กฎของโคไซน์"


def triangle_kind(a: int, b: int, c: int) -> str:
    a, b, c = sorted((a, b, c))
    if a + b <= c:
        return "none"
    d = a * a + b * b - c * c
    return "right" if d == 0 else ("obtuse" if d < 0 else "acute")


def obtuse_third_sides(a: int, b: int) -> int:
    """#integers x making a, b, x an obtuse triangle (a ≤ b): the obtuse angle faces x or faces b."""
    hyp = a * a + b * b
    facing_x = (a + b - 1) - math.isqrt(hyp)                    # √(a² + b²) < x < a + b
    leg = b * b - a * a
    top = math.isqrt(leg - 1) if leg > 0 else 0                 # b − a < x < √(b² − a²)
    facing_b = max(0, top - (b - a))
    return facing_x + facing_b


KIND_TH = {"obtuse": "มุมป้าน", "right": "มุมฉาก", "acute": "มุมแหลม"}


def _sides_of(rng: Random, kind: str) -> tuple[int, int, int]:
    if kind == "right":
        p, q, r = rng.choice(TRIPLES[:4])
        k = rng.randint(1, 2)
        return tuple(sorted((k * p, k * q, k * r)))
    while True:           # every kind has many triples with sides up to 12
        a, b, c = sorted(rng.sample(range(1, 13), 3))
        if triangle_kind(a, b, c) == kind:
            return a, b, c


COS_ALT = "รูปสามเหลี่ยม ABC กำกับความยาวด้านและมุมที่จุดยอด A"


@question_type("math.cosine_rule_side", display_name={"th": "กฎของโคไซน์: หาด้าน"},
               level={"th": "ม.5"}, topic="กฎของโคไซน์")
class CosineRuleSide(MathType):
    def expr(self, rng: Random, side_lo: int = 3, side_hi: int = 12):
        angle = rng.choice([60, 120])
        a, b = rng.randint(side_lo, side_hi), rng.randint(side_lo, side_hi)
        c2 = a * a + b * b + (-a * b if angle == 60 else a * b)
        return MathDraw(
            rf"a = {a}, \; b = {b}, \; C = {angle}^\circ", sqrt_tex(c2),
            prompt="จงหาความยาวของด้าน c",
            hint=r"c^2 = a^2 + b^2 - 2ab\cos C",
            # Forgetting the cosine term, and getting its sign backwards.
            distractors=[sqrt_tex(a * a + b * b),
                         sqrt_tex(a * a + b * b + (a * b if angle == 60 else -a * b)),
                         str(a + b)])
CosineRuleSide.PROVENANCE = Provenance("original")


@question_type("math.cosine_rule",
               display_name={"th": "กฎของโคไซน์"}, level={"th": "ม.5"},
               topic="กฎของโคไซน์")
class CosineRule(MathType):
    def expr(self, rng: Random):
        b, c = rng.randint(2, 8), rng.randint(2, 8)
        deg = rng.choice([60, 120])
        a2 = b * b + c * c - b * c if deg == 60 else b * b + c * c + b * c
        return MathDraw(rf"b = {b}, \; c = {c}, \; A = {deg}^{{\circ}}",
                        rf"a = {sqrt_tex(a2)}", hint=r"a^2 = b^2 + c^2 - 2bc\cos A",
                        prompt="จงหาความยาวด้าน a")
CosineRule.PROVENANCE = Provenance("original")


@question_type("math.cosine_rule_picture_m5",
               display_name={"th": "ใช้กฎของโคไซน์กับรูปสามเหลี่ยมในภาพ"},
               level={"th": "ม.5"}, topic="กฎของโคไซน์")
class CosineRulePictureM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(COS_TRIANGLES)
        img = image(s.asset_id, alt=COS_ALT)
        b2c2, bc = s.b * s.b + s.c * s.c, s.b * s.c
        if s.hide:
            other = b2c2 + bc if s.cos_a > 0 else b2c2 - bc   # the other sign of cos A
            return _q([text("จากภาพ จงหาความยาว x"), img], str(s.a),
                      [_sqrt(b2c2), _sqrt(other), str(s.b + s.c - s.a if s.b + s.c - s.a != s.a else s.a + 1)],
                      self.topic, [str(s.a + 1), str(s.a - 1)])
        if s.cos_a.denominator == 2 and abs(s.cos_a.numerator) == 1 and rng.random() < 0.5:
            deg = 60 if s.cos_a > 0 else 120
            return _q([text("จากภาพ มุม θ มีขนาดกี่องศา"), img], f"{deg}^\\circ",
                      [f"{180 - deg}^\\circ", "30^\\circ", "150^\\circ"], self.topic, [])
        c = s.cos_a
        return _q([text("จากภาพ จงหาค่าของ"), content_math(r"\cos \theta"), img], _fr(c),
                  [_fr(-c), _fr(2 * c), _fr(c / 2)], self.topic, [_fr(c + Fraction(1, 2 * bc)), _fr(c - Fraction(1, bc))])
CosineRulePictureM5.PROVENANCE = Provenance("original")


@question_type("math.cosine_rule_distance_m5",
               display_name={"th": "โจทย์ปัญหาระยะทางด้วยกฎของโคไซน์"},
               level=M5, topic="กฎของโคไซน์")
class CosineRuleDistanceM5(WordProblem):
    def expr(self, rng: Random):
        p, q, ang, d = rng.choice(_COS_TRIPLES)
        other = p * p + q * q + (p * q if ang == 60 else -p * q)   # the other sign of cos
        flat = [_root(p * p + q * q), _root(other)]
        kind = rng.randrange(5)
        if kind == 0:
            t = rng.choice((2, 3, 4))
            return MathDraw("", str(d * t),
                            prompt=(f"เรือสองลำออกจากท่าพร้อมกัน แล่นเป็นเส้นตรงทำมุมกัน {ang} องศา "
                                    f"ลำหนึ่งแล่นด้วยอัตราเร็ว {p} กิโลเมตรต่อชั่วโมง อีกลำ {q} กิโลเมตรต่อชั่วโมง "
                                    f"เมื่อผ่านไป {t} ชั่วโมง เรือทั้งสองอยู่ห่างกันกี่กิโลเมตร"),
                            distractors=[str(d), str((p + q) * t)] + flat)
        k = rng.choice((10, 20, 50))
        if kind == 1:
            return MathDraw("", str(d * k),
                            prompt=(f"ผู้สำรวจยืนที่จุด P ห่างจากจุด A ริมบึง {_c(p * k)} เมตร และห่างจากจุด B "
                                    f"อีกฝั่งหนึ่ง {_c(q * k)} เมตร มุม APB กาง {ang} องศา "
                                    f"ระยะจาก A ถึง B ยาวกี่เมตร"),
                            distractors=[str((p + q) * k), str(abs(q - p) * k),
                                         _root(k * k * (p * p + q * q))])
        if kind == 2:
            saved = (p + q - d) * k
            return MathDraw("", str(saved),
                            prompt=(f"ทางเดินในสวนจาก A ไป P ยาว {p * k} เมตร และจาก P ไป B ยาว {q * k} เมตร "
                                    f"โดยมุม APB กาง {ang} องศา ถ้าตัดทางเดินตรงจาก A ไป B "
                                    f"จะเดินสั้นลงกี่เมตร"),
                            distractors=_story.keep(d * k, (p + q) * k, abs(q - p) * k, saved + k,
                                                    answer=saved, lo=1))
        if kind == 3:
            return MathDraw("", str(d),
                            prompt=(f"โดรนบินจากจุดปล่อยเป็นเส้นตรง {p} กิโลเมตร แล้วเปลี่ยนทิศบินต่ออีก "
                                    f"{q} กิโลเมตร โดยเส้นทางทั้งสองช่วงทำมุมกัน {ang} องศาที่จุดเปลี่ยนทิศ "
                                    f"ขณะนั้นโดรนอยู่ห่างจากจุดปล่อยกี่กิโลเมตร"),
                            distractors=[str(p + q), str(abs(q - p))] + flat)
        cost = rng.choice((150, 200, 250))
        total = (p + q + d) * k * cost
        return MathDraw("", _c(total),
                        prompt=(f"ที่ดินรูปสามเหลี่ยมมีด้านสองด้านยาว {p * k} เมตร และ {q * k} เมตร "
                                f"มุมระหว่างสองด้านนี้กาง {ang} องศา ถ้าล้อมรั้วรอบที่ดิน ราคาเมตรละ {cost} บาท "
                                f"ต้องจ่ายค่ารั้วกี่บาท"),
                        distractors=[_c((p + q) * k * cost), _c(d * k * cost),
                                     _c((p + q + d) * k * cost + d * k * cost)])
CosineRuleDistanceM5.PROVENANCE = Provenance("original")


@question_type("math.triangle_side_type_m5",
               display_name={"th": "ชนิดของรูปสามเหลี่ยมจากความยาวด้าน"},
               level=M5_math_bank_trig, topic=COSINE_RULE)
class TriangleSideTypeM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.5:
            target = rng.choice(("obtuse", "right", "acute"))
            fmt = lambda s: rf"\{{{s[0]}, {s[1]}, {s[2]}\}}"
            right = _sides_of(rng, target)
            # One of each other kind, and three lengths that make no triangle at all.
            others = [k for k in ("obtuse", "right", "acute", "none") if k != target]
            rng.shuffle(others)
            wrongs = [fmt(_sides_of(rng, k)) for k in others]
            stem = [text("เซตของจำนวนเต็มสามจำนวนในข้อใดต่อไปนี้ เป็นความยาวด้านทั้งสามของรูปสามเหลี่ยม"
                         f"{KIND_TH[target]}ได้")]
            return _tex_q(stem, fmt(right), wrongs, self.topic)
        a = rng.randint(2, 8)
        b = rng.randint(a, 12)
        right = obtuse_third_sides(a, b)
        stem = [text(f"รูปสามเหลี่ยมรูปหนึ่งมีด้านยาว {a} หน่วย {b} หน่วย และ x หน่วย โดยที่ x "
                     "เป็นจำนวนเต็มบวก มีค่า x ทั้งหมดกี่ค่าที่ทำให้รูปสามเหลี่ยมนี้เป็นรูปสามเหลี่ยมมุมป้าน")]
        facing_x = (a + b - 1) - math.isqrt(a * a + b * b)
        # Only the obtuse angle opposite x; every x that makes a triangle; one more.
        return _int_q(stem, right, [facing_x, 2 * a - 1, right + 1, right - 1], self.topic)
TriangleSideTypeM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/8 ตรีโกณมิติ',))


@question_type("math.cosine_rule_angle", display_name={"th": "กฎของโคไซน์: หามุม"},
               level={"th": "ม.5"}, topic="กฎของโคไซน์")
class CosineRuleAngle(MathType):
    """Run the law backwards: three sides give cos C, hence the angle. The sides
    are built from a known angle so the answer is exact."""

    def expr(self, rng: Random, side_lo: int = 3, side_hi: int = 12):
        angle = rng.choice([60, 120])
        a, b = rng.randint(side_lo, side_hi), rng.randint(side_lo, side_hi)
        # c² = a² + b² − 2ab·cos C, and cos 60° = ½, cos 120° = −½.
        c2 = a * a + b * b + (-a * b if angle == 60 else a * b)
        return MathDraw(
            rf"a = {a}, \; b = {b}, \; c = \sqrt{{{c2}}}", rf"{angle}^\circ",
            prompt="จงหาขนาดของมุม C ที่อยู่ตรงข้ามด้าน c",
            hint=r"c^2 = a^2 + b^2 - 2ab\cos C",
            distractors=[rf"{180 - angle}^\circ", r"90^\circ", r"45^\circ"])
CosineRuleAngle.PROVENANCE = Provenance("original")


from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType, WordProblem  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m5 import M5 as LEVEL  # noqa: E402


def _nz5(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk5(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk5(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk5(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt5(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk5(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk5(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))


def _g5(n: int) -> str:
    """A whole number in TeX with grouped thousands."""
    return f"{n:,}".replace(",", "{,}")


def _gk5(*values: int, answer: int, lo: int = 1) -> list[str]:
    return _tk5(*(_g5(int(v)) for v in values if v >= lo), answer=_g5(answer))


def _deg5(*angles: int) -> str:
    return "x = " + ", ".join(f"{a}^{{\\circ}}" for a in angles)

# ── More law of cosines (2026-11): cos C from three sides, a side with a 120° angle, a side with a 60° angle,
# and a parallelogram's long diagonal ──

_COS120 = ((3, 5, 7), (7, 8, 13), (5, 16, 19), (6, 10, 14), (9, 15, 21), (5, 3, 7), (8, 7, 13))
_COS60 = ((5, 8, 7), (3, 8, 7), (7, 15, 13), (5, 21, 19), (8, 15, 13), (8, 5, 7), (8, 3, 7))


@question_type("math.cos_from_three_sides_m5", display_name={"th": "หาค่า cos ของมุมจากความยาวด้านทั้งสาม"}, level=LEVEL,
               topic="กฎของโคไซน์")
class CosFromThreeSidesM5(MathType):
    def expr(self, rng: Random):
        while True:
            a, b, c = rng.randint(3, 12), rng.randint(3, 12), rng.randint(3, 12)
            if a + b > c and a + c > b and b + c > a and a * a + b * b != c * c:
                break
        right = Fraction(a * a + b * b - c * c, 2 * a * b)
        return MathDraw(rf"a = {a}, \quad b = {b}, \quad c = {c}", frac_tex(right), prompt="จงหาค่าของ cos C (C อยู่ตรงข้ามด้าน c)",
                        distractors=_fk5(Fraction(a * a + b * b + c * c, 2 * a * b), Fraction(a * a + b * b - c * c, a * b),
                                         -right, right + Fraction(1, 2 * a * b), answer=right))


@question_type("math.side_with_120_m5", display_name={"th": "หาด้านที่สามเมื่อมุมระหว่างเป็น 120°"}, level=LEVEL, topic="กฎของโคไซน์")
class SideWith120M5(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.choice(_COS120)
        k = rng.randint(1, 3)
        a, b, c = a * k, b * k, c * k
        prompt = f"รูปสามเหลี่ยมมีด้านยาว {a} และ {b} หน่วย มุมระหว่างสองด้านนี้ 120 องศา ด้านที่สามยาวกี่หน่วย"
        # Taken as 60°; the sides added; Pythagoras.
        sixty = a * a + b * b - a * b
        return MathDraw("", str(c), prompt=prompt,
                        distractors=_tk5(sqrt_tex(sixty), str(a + b), sqrt_tex(a * a + b * b), str(c + 1), answer=str(c)))


@question_type("math.side_with_60_m5", display_name={"th": "หาด้านที่สามเมื่อมุมระหว่างเป็น 60°"}, level=LEVEL, topic="กฎของโคไซน์")
class SideWith60M5(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.choice(_COS60)
        k = rng.randint(1, 3)
        a, b, c = a * k, b * k, c * k
        prompt = f"รูปสามเหลี่ยมมีด้านยาว {a} และ {b} หน่วย มุมระหว่างสองด้านนี้ 60 องศา ด้านที่สามยาวกี่หน่วย"
        wide = a * a + b * b + a * b
        return MathDraw("", str(c), prompt=prompt,
                        distractors=_tk5(sqrt_tex(wide), str(abs(a - b)), sqrt_tex(a * a + b * b), str(c + 1), answer=str(c)))


@question_type("math.parallelogram_long_diagonal_m5", display_name={"th": "เส้นทแยงมุมยาวของรูปสี่เหลี่ยมด้านขนาน"}, level=LEVEL,
               topic="กฎของโคไซน์")
class ParallelogramLongDiagonalM5(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.choice(_COS120)
        k = rng.randint(1, 3)
        a, b, c = a * k, b * k, c * k
        prompt = f"รูปสี่เหลี่ยมด้านขนานมีด้านยาว {a} และ {b} เซนติเมตร มุมแหลมขนาด 60 องศา เส้นทแยงมุมเส้นที่ยาวกว่ายาวกี่เซนติเมตร"
        short = a * a + b * b - a * b
        return MathDraw("", str(c), prompt=prompt,
                        distractors=_tk5(sqrt_tex(short), str(a + b), sqrt_tex(a * a + b * b), str(2 * max(a, b)), answer=str(c)))


CosFromThreeSidesM5.PROVENANCE = Provenance("original")
SideWith120M5.PROVENANCE = Provenance("original")
SideWith60M5.PROVENANCE = Provenance("original")
ParallelogramLongDiagonalM5.PROVENANCE = Provenance("original")
