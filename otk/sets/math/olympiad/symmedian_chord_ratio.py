"""Through the pole P of AC, line PQ is the Q-symmedian of QAC: AB/BC = (QA/QC)² = (AR/RC)²."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันที่สอง ข้อ 2",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def segment_ab(length: int, p: int, q: int) -> Fraction:
    """PA, PC tangent: P is the pole of AC, so QP is the symmedian of triangle
    QAC and AB : BC = QA² : QC². The bisector gives AR : RC = QA : QC, which
    is the source's AB/BC = (AR/RC)²."""
    return Fraction(length * p * p, p * p + q * q)


@question_type(
    "math.symmedian_chord_ratio_olympiad",
    display_name={"th": "อัตราส่วนที่เส้นจากจุดตัดเส้นสัมผัสแบ่งคอร์ด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: เส้นสัมผัสวงกลม",
)
class SymmedianChordRatio(WordProblem):
    def expr(self, rng: Random):
        while True:
            length, p, q = rng.randint(4, 40), rng.randint(1, 9), rng.randint(1, 9)
            if p != q:
                break
        answer = segment_ab(length, p, q)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(length * p, p + q), segment_ab(length, q, p), Fraction(length * p * p, (p + q) ** 2), Fraction(length, 2), Fraction(length * p**3, p**3 + q**3)]) if v != answer]
        return MathDraw(
            rf"AC={length},\quad AR:RC={p}:{q}",
            frac_tex(answer),
            prompt="P เป็นจุดภายนอกวงกลม ลากเส้นจาก P สัมผัสวงกลมที่ A และ C ให้ B อยู่บน AC และ PB ตัดวงกลมที่ Q เส้นแบ่งครึ่งมุม AQC ตัด AC ที่ R จงหา AB",
            hint="เส้นแบ่งครึ่งมุมให้ AR : RC = QA : QC และ QP เป็นเส้นซิมมีเดียนของสามเหลี่ยม QAC จึง AB : BC = QA² : QC²",
            distractors=wrong,
        )
