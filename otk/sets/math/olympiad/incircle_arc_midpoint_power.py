"""K, D, M collinear: the chord through the incircle touch point."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2562, ข้อ 8",)
)


def touch_chord_product(a: int, b: int, c: int) -> Fraction:
    """KD·DM: K, D, M lie on one chord, so it is D's power BD·DC."""
    s = Fraction(a + b + c, 2)
    return (s - b) * (s - c)


def _triangles():
    for a in range(4, 21):
        for b in range(3, 21):
            for c in range(3, 21):
                if b != c and a < b + c and b < a + c and c < a + b and (a + b + c) % 2 == 0:
                    yield a, b, c


TRIANGLES = tuple(_triangles())


@question_type(
    "math.incircle_arc_midpoint_power_olympiad",
    display_name={"th": "ผลคูณส่วนของคอร์ดผ่านจุดสัมผัสวงกลมแนบใน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมแนบใน",
)
class IncircleArcMidpointPower(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.choice(TRIANGLES)
        s = (a + b + c) // 2
        answer = int(touch_chord_product(a, b, c))
        wrong = []
        for value in (
            (s - a) * (s - b),  # wrong pair of tangent lengths
            (s - a) * (s - c),
            Fraction(a * a, 4),  # treat D as the midpoint of BC
            s * (s - a),
            b * c - answer,
            answer + s - a,
        ):
            if value != answer and value > 0 and value not in wrong:
                wrong.append(value)
        return MathDraw(
            rf"BC={a},\ CA={b},\ AB={c}",
            str(answer),
            prompt=(
                "ในรูปสามเหลี่ยม ABC วงกลมแนบในมีจุดศูนย์กลาง I สัมผัส BC ที่ D "
                "วงกลมที่มี AI เป็นเส้นผ่านศูนย์กลางตัดวงกลมล้อมรอบอีกครั้งที่ K "
                "และเส้นตรง AI ตัดวงกลมล้อมรอบอีกครั้งที่ M จงหา KD · DM"
            ),
            hint="แสดงว่า K, D, M อยู่บนเส้นตรงเดียวกัน แล้วใช้กำลังของจุด D: KD · DM = BD · DC",
            distractors=[
                str(v) if not isinstance(v, Fraction) or v.denominator == 1
                else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"
                for v in wrong
            ],
        )
