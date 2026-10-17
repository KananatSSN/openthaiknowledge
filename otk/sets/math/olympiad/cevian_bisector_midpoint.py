"""Concurrent cevians in a right triangle with RP bisecting ∠BRC: MR = MC = PQ/2."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2554, ข้อ 3",)
)

PAIRS = ((3, 4), (6, 8), (5, 12), (8, 15), (9, 12), (12, 16), (7, 24), (15, 20), (20, 21))


def midpoint_distance(cp: int, cq: int) -> Fraction:
    """With concurrent cevians, RC and RP are harmonic conjugates of RA, RB,
    so RP bisecting ∠BRC makes RQ bisect ∠CRA and ∠PRQ = 90°. With ∠PCQ = 90°
    too, R and C lie on the circle with diameter PQ: MR = MC = PQ/2."""
    hyp_sq = cp * cp + cq * cq
    root = int(round(hyp_sq**0.5))
    assert root * root == hyp_sq
    return Fraction(root, 2)


def _tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


@question_type(
    "math.cevian_bisector_midpoint_olympiad",
    display_name={"th": "ระยะจากจุดกึ่งกลาง PQ เมื่อเส้นตรงจากจุดตัดแบ่งครึ่งมุม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: สามเหลี่ยมมุมฉาก",
)
class CevianBisectorMidpoint(WordProblem):
    def expr(self, rng: Random):
        cp, cq = rng.choice(PAIRS)
        if rng.randrange(2):
            cp, cq = cq, cp
        answer = midpoint_distance(cp, cq)
        hyp = 2 * answer
        wrong = [_tex(v) for v in dict.fromkeys([
            hyp,  # the whole of PQ
            Fraction(cp + cq, 2),
            Fraction(cp * cq, int(hyp)),  # the altitude from C onto PQ
            Fraction(max(cp, cq), 2),
            answer + 1,
        ]) if v != answer]
        return MathDraw(
            rf"CP={cp},\quad CQ={cq}",
            _tex(answer),
            prompt=(
                "รูปสามเหลี่ยม ABC มีมุม C ฉาก จุด D ภายในทำให้ AD, BD, CD ตัด BC, CA, AB ที่ P, Q, R "
                "และ ∠BRP = ∠PRC ให้ M เป็นจุดกึ่งกลาง PQ จงหา MR"
            ),
            hint="แสดงว่า ∠PRQ = 90° แล้ว R และ C อยู่บนวงกลมที่มี PQ เป็นเส้นผ่านศูนย์กลาง",
            distractors=wrong,
        )
