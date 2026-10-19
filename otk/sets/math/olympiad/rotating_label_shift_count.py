"""Label 3m chairs with three grades, m each, so that some rotation shifts every grade by one."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2554, ข้อ 12",)
)


def shift_labelling_count(m: int) -> int:
    """A rotation by k with f(a + k) ≡ f(a) − 1 is the condition
    f(a + d) ≡ f(a) + s with d = gcd(k, 3m) | m and s ∈ {1, 2}. When 3 ∤ m,
    every such set lies in one of the two disjoint sets for d = m, each of
    size 3^m, so the count is 2·3^m. (The official key's 3² + 3¹²⁷⁷ + 3²⁵⁵⁴
    for m = 2554 counts one sign per period only.)"""
    if m % 3 == 0:
        raise ValueError("this closed form needs 3 ∤ m")
    return 2 * 3**m


def _divisor_sum_tex(m: int) -> str:
    return "+".join(rf"3^{{{d}}}" for d in range(2, m + 1) if m % d == 0)


@question_type(
    "math.rotating_label_shift_count_olympiad",
    display_name={"th": "จำนวนวิธีติดป้ายที่การหมุนเลื่อนทุกระดับชั้นไปหนึ่ง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การจัดหมู่",
)
class RotatingLabelShiftCount(WordProblem):
    def expr(self, rng: Random):
        m = rng.choice([v for v in range(4, 61) if v % 3])
        answer = rf"2\cdot 3^{{{m}}}"
        candidates = [rf"3^{{{m}}}", rf"2\cdot 3^{{{m - 1}}}", rf"6^{{{m}}}", rf"3^{{{3 * m}}}", _divisor_sum_tex(m)]
        wrong = [t for t in dict.fromkeys(candidates) if t != answer]
        return MathDraw(
            rf"n={3 * m},\quad m={m}",
            answer,
            prompt=(
                f"เก้าอี้ {3 * m} ตัววางเป็นวงกลม ติดป้ายระดับชั้น ม.1, ม.2, ม.3 อย่างละ {m} ตัว นักเรียนถือบอลประจำชั้นของตน "
                "และทุกสัญญาณส่งบอลไปทางซ้ายพร้อมกัน การติดป้ายแบบหลินปิงคือแบบที่หลังจากส่งไปจำนวนครั้งหนึ่ง "
                "ม.1 ทุกคนถือบอลของ ม.3, ม.2 ถือของ ม.1 และ ม.3 ถือของ ม.2 มีการติดป้ายแบบหลินปิงกี่วิธี"
            ),
            hint="การส่ง k ครั้งให้เงื่อนไข f(a + k) ≡ f(a) − 1 พิจารณา d = ห.ร.ม.(k, 3m) และทิศทางทั้งสองของการเลื่อน",
            distractors=wrong,
        )
