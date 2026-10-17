"""The cevians through the extouch points meet at the Nagel point."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2556, ข้อ 12",)
)


def nagel_quantity(asked: str, a: int, b: int, c: int) -> Fraction:
    """A, the antipode P of the touch point D, and M are collinear (the
    homothety at A taking the incircle to the A-excircle), so BM = CD = s − c.
    CN = AE = s − a puts N at the B-extouch point. R is the Nagel point, with
    barycentrics (s − a : s − b : s − c), so AR/RM = a/(s − a)."""
    s = Fraction(a + b + c, 2)
    if asked == "BM":
        return s - c
    if asked == "AN":
        return s - c
    if asked == "AR:RM":
        return a / (s - a)
    raise ValueError(asked)


TRIANGLES = tuple(
    (a, b, c)
    for a in range(4, 16) for b in range(4, 16) for c in range(4, 16)
    if a < b + c and b < a + c and c < a + b and b != c
)


def _num(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


@question_type(
    "math.nagel_cevian_ratios_olympiad",
    display_name={"th": "เส้นจากจุดยอดผ่านจุดสัมผัสวงกลมแนบนอก (จุดนาเกล)"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมแนบใน",
)
class NagelCevianRatios(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.choice(TRIANGLES)
        asked = rng.choice(("BM", "AN", "AR:RM"))
        answer = nagel_quantity(asked, a, b, c)
        s = Fraction(a + b + c, 2)
        candidates = [s - b, s - a, Fraction(a, 2), s, (s - a) / a, Fraction(b + c, a), a / (s - b)]
        wrong = [_num(v) for v in dict.fromkeys(candidates) if v != answer and v > 0]
        label = {"BM": "ความยาว BM", "AN": "ความยาว AN", "AR:RM": "อัตราส่วน AR/RM"}[asked]
        return MathDraw(
            rf"BC={a},\ CA={b},\ AB={c}",
            _num(answer),
            prompt=(
                "วงกลมแนบใน ω ของรูปสามเหลี่ยม ABC สัมผัส BC, CA ที่ D, E ลากเส้นตั้งฉากกับ BC ที่ D ตัด ω อีกครั้งที่ P "
                "เส้นตรง AP ตัด BC ที่ M จุด N บน AC ทำให้ AE = CN และ BN ตัด AM ที่ R "
                f"จงหา{label}"
            ),
            hint="P เป็นจุดตรงข้าม D บนวงกลมแนบใน การขยายที่ A ส่งวงกลมแนบในไปวงกลมแนบนอก จึง M เป็นจุดสัมผัสของวงกลมแนบนอก",
            distractors=wrong,
            variant=asked,
        )
