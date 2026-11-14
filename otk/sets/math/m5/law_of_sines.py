"""กฎของไซน์

คณิตศาสตร์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 3 ม.5/2

Sets moved here from: math_chapters.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import redraw_until_full
from otk.core.mistakes import named
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.math_chapters import (
    _SIN,
    M5,
    _deg,
    _distinct,
    _div,
    _mul,
    _surd_bump,
    _surd_tex,
)
from otk.sets._support.math_p2 import _maths, _texts

PROVENANCE = Provenance("original")


_SINE_TOPIC = "กฎของไซน์"


def _two_angles(rng: Random) -> tuple[int, int]:
    while True:
        a, b = rng.sample(sorted(_SIN), 2)
        if a + b < 180:
            return a, b


@question_type("math.triangle_area_sine_m5", display_name={"th": "พื้นที่รูปสามเหลี่ยม ½ab sin C"},
               level=M5, topic=_SINE_TOPIC)
class TriangleAreaSineM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        C = rng.choice(sorted(_SIN))
        a, b = rng.randint(2, 12), rng.randint(2, 12)
        half = (Fraction(a * b, 2), 1)
        area = _mul(half, _SIN[C])
        right = _surd_tex(area)
        # No ½, no sine, and sin mistaken for cos (30° ↔ 60°).
        swap = {30: 60, 60: 30, 150: 60, 120: 30}.get(C, 30)
        wrongs = _distinct(right, _surd_tex(_mul((Fraction(a * b), 1), _SIN[C])), _surd_tex(half),
                           _surd_tex(_mul(half, _SIN[swap])), _surd_bump(area))
        stem = rng.choice((
            f"รูปสามเหลี่ยม ABC มี a = {a} หน่วย, b = {b} หน่วย และ ∠C = {C}° "
            f"จงหาพื้นที่ของรูปสามเหลี่ยม (ตารางหน่วย)",
            f"ที่ดินรูปสามเหลี่ยมมีด้าน a = {a} เมตร และ b = {b} เมตร ทำมุมกัน ∠C = {C}° "
            f"ที่ดินแปลงนี้มีพื้นที่กี่ตารางเมตร",
            f"แผ่นป้ายรูปสามเหลี่ยมมีด้านสองด้านยาว a = {a} เดซิเมตร และ b = {b} เดซิเมตร "
            f"มุมระหว่างสองด้านนี้ ∠C = {C}° ต้องใช้สีทาป้ายด้านหน้ากี่ตารางเดซิเมตร",
        ))
        return _maths([text(stem)], right, wrongs[:3], self.topic)


@question_type("math.sine_rule_side_m5", display_name={"th": "กฎของไซน์: หาความยาวด้าน"},
               level=M5, topic=_SINE_TOPIC)
class SineRuleSideM5(QuestionType):
    @redraw_until_full()
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            A, B = _two_angles(rng)
            a = rng.randint(2, 20)
            b = _mul((Fraction(a), 1), _div(_SIN[B], _SIN[A]))
            if b[0].denominator == 1:
                break
        right = _surd_tex(b)
        # The ratio upside down, and a·sin B without dividing by sin A.
        wrongs = _distinct(right, _surd_tex(_mul((Fraction(a), 1), _div(_SIN[A], _SIN[B]))),
                           _surd_tex(_mul((Fraction(a), 1), _SIN[B])),
                           _surd_tex(_div((Fraction(a), 1), _SIN[B])), _surd_bump(b),
                           _surd_tex(_mul((Fraction(2), 1), b)), str(a))
        stem = rng.choice((
            f"รูปสามเหลี่ยม ABC มี ∠A = {A}°, ∠B = {B}° และ a = {a} หน่วย จงหาความยาวของด้าน b",
            f"ผู้สำรวจวัดที่ดินรูปสามเหลี่ยม ABC ได้ ∠A = {A}°, ∠B = {B}° และด้าน a = {a} เมตร "
            f"(a คือด้าน BC) ด้าน b (ด้าน CA) ยาวกี่เมตร",
            f"เรือสองลำอยู่ที่จุด A และ B มองเห็นประภาคารที่จุด C โดย ∠A = {A}°, ∠B = {B}° "
            f"และระยะ a = {a} กิโลเมตร (a คือระยะ BC) เรือที่จุด A อยู่ห่างจากประภาคารกี่กิโลเมตร",
        ))
        return _maths([text(stem)], right, wrongs[:3], self.topic)


@question_type("math.sine_rule_angle_m5", display_name={"th": "กฎของไซน์: หาขนาดของมุม"},
               level=M5, topic=_SINE_TOPIC)
class SineRuleAngleM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            A, B = _two_angles(rng)
            if B == 90:              # "if ∠B is a right angle" would give it away
                continue
            a = rng.randint(2, 12)
            b = _mul((Fraction(a), 1), _div(_SIN[B], _SIN[A]))
            if b[0].denominator == 1:
                break
        which = "มุมแหลม" if B < 90 else "มุมป้าน" if B > 90 else "มุมฉาก"
        # The other angle with the same sine, ∠A, ∠C, then the books' other angles.
        wrongs = _distinct(_deg(B), *[_deg(v) for v in (180 - B, A, 180 - A - B, *sorted(_SIN))])
        return _maths([text("รูปสามเหลี่ยม ABC มี"), content_math(rf"\angle A = {_deg(A)},\ a = {a},\ "
                                                                 rf"b = {_surd_tex(b)}"),
                       text(f"ถ้า ∠B เป็น{which} จงหาขนาดของ ∠B")], _deg(B), wrongs[:3], self.topic)


def _circumradius_parameters(rng: Random) -> tuple[int, int]:
    return rng.choice(sorted(_SIN)), rng.randint(3, 30)


@question_type("math.sine_rule_circumradius_m5",
               display_name={"th": "รัศมีวงกลมล้อมรอบรูปสามเหลี่ยมจากกฎของไซน์"},
               level=M5, topic=_SINE_TOPIC)
class SineRuleCircumradiusM5(QuestionType):
    @redraw_until_full()
    def build(self, rng: Random) -> GeneratedQuestion:
        angle, side = _circumradius_parameters(rng)
        radius = _div((Fraction(side, 2), 1), _SIN[angle])
        right = _surd_tex(radius)
        wrongs = _distinct(
            right,
            _surd_tex(_div((Fraction(side), 1), _SIN[angle])),
            _surd_tex((Fraction(side, 2), 1)),
            _surd_tex(_mul((Fraction(side, 2), 1), _SIN[angle])),
            _surd_bump(radius), str(side),
        )
        diameter = _surd_tex(_div((Fraction(side), 1), _SIN[angle]))
        if diameter in wrongs:
            named("steps.missed_a_step", diameter)
        return _maths([text(
            f"รูปสามเหลี่ยม ABC มี ∠A = {angle}° และด้าน a (ตรงข้ามมุม A) ยาว {side} เซนติเมตร "
            "รัศมีของวงกลมที่ล้อมรอบรูปสามเหลี่ยมนี้ยาวกี่เซนติเมตร"
        )], right, wrongs[:3], self.topic)


_AREA_ANGLES = tuple((a, b, 180 - a - b) for a in sorted(_SIN) for b in sorted(_SIN)
                     if 0 < 180 - a - b in _SIN)


def _area_from_angles_parameters(rng: Random) -> tuple[int, int, int, int]:
    A, B, C = rng.choice(_AREA_ANGLES)
    return A, B, C, rng.randint(3, 24)


@question_type("math.sine_rule_area_from_angles_m5",
               display_name={"th": "พื้นที่สามเหลี่ยมจากด้านหนึ่งและสองมุม"},
               level=M5, topic=_SINE_TOPIC)
class SineRuleAreaFromAnglesM5(QuestionType):
    @redraw_until_full()
    def build(self, rng: Random) -> GeneratedQuestion:
        A, B, C, a = _area_from_angles_parameters(rng)
        half_square = (Fraction(a * a, 2), 1)
        area = _mul(_mul(half_square, _SIN[B]), _div(_SIN[C], _SIN[A]))
        right = _surd_tex(area)
        no_half = _surd_tex(_mul((Fraction(a * a), 1), _div(_mul(_SIN[B], _SIN[C]), _SIN[A])))
        wrongs = _distinct(
            right, no_half,
            _surd_tex(_mul(half_square, _SIN[A])),
            _surd_tex(_mul(half_square, _mul(_SIN[B], _SIN[C]))),
            _surd_tex(_mul(half_square, _div(_SIN[A], _mul(_SIN[B], _SIN[C])))),
            _surd_bump(area),
        )
        if no_half in wrongs:
            named("steps.missed_a_step", no_half)
        return _maths([text(
            f"รูปสามเหลี่ยม ABC มี ∠A = {A}°, ∠B = {B}° และด้าน a (ตรงข้ามมุม A) "
            f"ยาว {a} เซนติเมตร พื้นที่ของรูปสามเหลี่ยมนี้กี่ตารางเซนติเมตร"
        )], right, wrongs[:3], self.topic)


_SSA_LABELS = (
    "ไม่มีรูปสามเหลี่ยม",
    "มีรูปสามเหลี่ยม 1 รูป โดยมุม B เป็นมุมแหลม",
    "มีรูปสามเหลี่ยม 1 รูป โดยมุม B เป็นมุมฉาก",
    "มีรูปสามเหลี่ยม 2 รูป",
)


def _ssa_parameters(rng: Random) -> tuple[int, int, int, int]:
    """Choose a feasible example of each SSA outcome, including the tangent case."""
    target = rng.randrange(4)
    if target == 2:
        blue = 2 * rng.randint(3, 12)
        return 30, blue // 2, blue, target
    while True:
        angle = rng.choice((30, 45, 60))
        opposite_a, opposite_b = rng.randint(2, 24), rng.randint(3, 28)
        sin4 = {30: 1, 45: 2, 60: 3}[angle]
        height_comparison = 4 * opposite_a * opposite_a - sin4 * opposite_b * opposite_b
        if height_comparison < 0:
            outcome = 0
        elif height_comparison == 0:
            outcome = 2
        elif opposite_a < opposite_b and height_comparison > 0:
            outcome = 3
        else:
            outcome = 1
        if outcome == target:
            return angle, opposite_a, opposite_b, outcome


@question_type("math.sine_rule_ambiguous_case_m5",
               display_name={"th": "กรณีกำกวมของกฎของไซน์"},
               level=M5, topic=_SINE_TOPIC)
class SineRuleAmbiguousCaseM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        angle, a, b, outcome = _ssa_parameters(rng)
        right = _SSA_LABELS[outcome]
        wrongs = [label for label in _SSA_LABELS if label != right]
        if outcome == 3:
            named("trig.ambiguous_second_angle", _SSA_LABELS[1])
        elif outcome == 0:
            named("trig.ignored_height", _SSA_LABELS[1])
        elif outcome == 2:
            named("trig.ambiguous_second_angle", _SSA_LABELS[3])
        else:
            named("trig.ambiguous_second_angle", _SSA_LABELS[3])
        return _texts([text(
            f"กำหนดรูปสามเหลี่ยม ABC โดย ∠A = {angle}°, ด้าน a (ตรงข้ามมุม A) ยาว {a} หน่วย "
            f"และด้าน b (ตรงข้ามมุม B) ยาว {b} หน่วย ข้อมูลนี้สร้างรูปสามเหลี่ยมได้กี่รูป"
        )], right, wrongs, self.topic)


from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import MathDraw, WordProblem  # noqa: E402
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

# ── More law of sines (2026-11): a side from the circumradius, an area with a 30° or 150° angle, side ratios
# of special triangles, and a side from two angles ──


@question_type("math.side_from_circumradius_m5", display_name={"th": "หาความยาวด้านจากรัศมีวงกลมล้อมรอบ"}, level=LEVEL,
               topic="กฎของไซน์")
class SideFromCircumradiusM5(WordProblem):
    def expr(self, rng: Random):
        r = rng.randint(2, 20)
        angle = rng.choice((30, 90, 150))
        right = 2 * r if angle == 90 else r
        prompt = f"รูปสามเหลี่ยม ABC แนบในวงกลมรัศมี {r} เซนติเมตร ถ้ามุม A มีขนาด {angle} องศา ด้าน a (ตรงข้ามมุม A) ยาวกี่เซนติเมตร"
        # The radius doubled or halved; the sine forgotten.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk5(r if angle == 90 else 2 * r, 4 * r, r // 2 if r > 3 else r + 3, right + 1, answer=right, lo=1))


@question_type("math.area_with_thirty_degrees_m5", display_name={"th": "พื้นที่รูปสามเหลี่ยมเมื่อมุมระหว่างด้านเป็น 30° หรือ 150°"},
               level=LEVEL, topic="กฎของไซน์")
class AreaWithThirtyDegreesM5(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.randint(1, 10) * 4, rng.randint(2, 20)
        angle = rng.choice((30, 150, 90))
        right = a * b // 4 if angle != 90 else a * b // 2
        prompt = f"รูปสามเหลี่ยมมีด้านสองด้านยาว {a} และ {b} เซนติเมตร มุมระหว่างสองด้านนี้ {angle} องศา มีพื้นที่กี่ตารางเซนติเมตร"
        # The sine left out; the product; the right-angle formula for every angle.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk5(a * b // 2 if angle != 90 else a * b // 4, a * b, a + b, right + a, answer=right, lo=1))


@question_type("math.special_triangle_side_ratio_m5", display_name={"th": "อัตราส่วนความยาวด้านของรูปสามเหลี่ยมมุมพิเศษ"},
               level=LEVEL, topic="กฎของไซน์")
class SpecialTriangleSideRatioM5(ConceptBankType):
    ITEMS = [
        Concept("รูปสามเหลี่ยมที่มีมุม 30°, 60°, 90° มีอัตราส่วนด้านตรงข้ามมุมเหล่านั้นเป็นเท่าใด", "1 : √3 : 2",
                ("1 : 2 : 3", "1 : 2 : √3", "√3 : 1 : 2")),
        Concept("รูปสามเหลี่ยมที่มีมุม 45°, 45°, 90° มีอัตราส่วนด้านตรงข้ามมุมเหล่านั้นเป็นเท่าใด", "1 : 1 : √2",
                ("1 : 1 : 2", "1 : 2 : √2", "√2 : √2 : 1")),
        Concept("รูปสามเหลี่ยมที่มีมุม 30°, 30°, 120° มีอัตราส่วนด้านตรงข้ามมุมเหล่านั้นเป็นเท่าใด", "1 : 1 : √3",
                ("1 : 1 : 4", "1 : 1 : 2", "1 : 1 : 3")),
        Concept("รูปสามเหลี่ยมที่มีมุมทั้งสามเท่ากัน มีอัตราส่วนความยาวด้านเป็นเท่าใด", "1 : 1 : 1",
                ("1 : 2 : 3", "1 : √3 : 2", "1 : 1 : √2")),
    ]


@question_type("math.side_from_two_angles_m5", display_name={"th": "หาความยาวด้านจากมุมสองมุมและด้านหนึ่ง"}, level=LEVEL,
               topic="กฎของไซน์")
class SideFromTwoAnglesM5(WordProblem):
    def expr(self, rng: Random):
        k = rng.randint(2, 20)
        case = rng.randrange(3)
        if case == 0:
            angles, right, wrongs = (30, 45), rf"{k}\sqrt{{2}}", (rf"\frac{{{k}\sqrt{{2}}}}{{2}}", str(2 * k), rf"{k}\sqrt{{3}}")
        elif case == 1:
            angles, right, wrongs = (30, 60), rf"{k}\sqrt{{3}}", (rf"\frac{{{k}\sqrt{{3}}}}{{3}}", str(2 * k), rf"{k}\sqrt{{2}}")
        else:
            angles, right, wrongs = (45, 90), rf"{k}\sqrt{{2}}", (rf"\frac{{{k}\sqrt{{2}}}}{{2}}", str(2 * k), str(k))
        prompt = (f"รูปสามเหลี่ยม ABC มีมุม A = {angles[0]}° มุม B = {angles[1]}° และด้าน a (ตรงข้ามมุม A) ยาว {k} หน่วย "
                  "ด้าน b (ตรงข้ามมุม B) ยาวกี่หน่วย")
        return MathDraw("", right, prompt=prompt, distractors=_tk5(*wrongs, answer=right))
