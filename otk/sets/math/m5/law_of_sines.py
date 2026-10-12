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
from otk.sets._support.math_p2 import _maths

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
