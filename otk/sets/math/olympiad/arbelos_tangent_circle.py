"""In the semicircle of radius R: the inner circle has radius R/2, the side semicircle R/3 at distance 2R/3, the fourth circle R/6."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันที่สอง ข้อ 4",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


QUANTITIES = ("O1O3", "r3", "r", "O1P")


def lengths(ab: int) -> dict[str, Fraction]:
    """R = AB/2, O₂ = (0, R/2) with radius R/2. O₃ = (d, 0), radius ρ:
    d + ρ = R and √(d² + R²/4) = R/2 + ρ give d = 2R/3, ρ = R/3. P = (2R/3,
    R/2) has O₁P = 5R/6, O₂P = 2R/3, O₃P = R/2, so the circle at P of
    radius R/6 touches all three."""
    r = Fraction(ab, 2)
    return {"O1O3": 2 * r / 3, "r3": r / 3, "r": r / 6, "O1P": 5 * r / 6}


@question_type(
    "math.arbelos_tangent_circle_olympiad",
    display_name={"th": "วงกลมที่สัมผัสสามวงในครึ่งวงกลม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมสัมผัสกัน",
)
class ArbelosTangentCircle(WordProblem):
    def expr(self, rng: Random):
        ab = rng.randint(4, 60)
        values = lengths(ab)
        key = rng.choice(QUANTITIES)
        answer = values[key]
        r = Fraction(ab, 2)
        wrong = [frac_tex(v) for v in dict.fromkeys([*values.values(), r / 4, r / 2, 3 * r / 4]) if v != answer]
        ask = {"O1O3": "O₁O₃", "r3": "รัศมีของครึ่งวงกลม O₃", "r": "รัศมีของวงกลมที่มีจุดศูนย์กลาง P ซึ่งสัมผัสทั้งสามวง", "O1P": "O₁P"}[key]
        return MathDraw(
            rf"AB={ab}",
            frac_tex(answer),
            prompt=f"O₁ เป็นจุดศูนย์กลางครึ่งวงกลมที่มี AB เป็นเส้นผ่านศูนย์กลาง O₂ เป็นจุดศูนย์กลางวงกลมที่แนบในครึ่งวงกลมแรกและสัมผัส AB ที่ O₁ O₃ อยู่บน AB เป็นจุดศูนย์กลางครึ่งวงกลมที่สัมผัสสองวงแรก P เป็นจุดตัดของเส้นตั้งฉากกับ AB ที่ O₃ กับเส้นผ่าน O₂ ที่ขนานกับ AB จงหา {ask}",
            hint="ใช้พิกัด O₁ = (0, 0) รัศมีครึ่งวงกลม R แล้ว O₂ = (0, R/2) เงื่อนไขสัมผัสคือระยะระหว่างจุดศูนย์กลางเท่ากับผลบวกหรือผลต่างของรัศมี",
            distractors=wrong,
        )
