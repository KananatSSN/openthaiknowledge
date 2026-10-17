"""Circle on diameter CP in a right triangle: AP·PR = BP·PC and AC·CQ = BC·PC."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2555, ข้อ 1",)
)


def chord_products(bp: int, pc: int) -> dict[str, int]:
    """∠CQP = 90° gives CQ = CP·cos C, so AC·CQ = CP·BC. The power of A
    is AP·AR = AQ·AC, so AP·PR = AQ·AC − AP² = BP·PC, and subtracting gives
    the source identity CP² = AC·CQ − AP·PR."""
    bc = bp + pc
    return {"AC·CQ": bc * pc, "AP·PR": bp * pc, "CP²": pc * pc}


@question_type(
    "math.right_triangle_diameter_circle_olympiad",
    display_name={"th": "ผลคูณส่วนของเส้นในวงกลมที่มี CP เป็นเส้นผ่านศูนย์กลาง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: กำลังของจุด",
)
class RightTriangleDiameterCircle(WordProblem):
    def expr(self, rng: Random):
        ab = rng.randint(2, 12)
        bp = rng.randint(1, 9)
        pc = rng.randint(1, 9)
        asked = rng.choice(("AC·CQ", "AP·PR"))
        values = chord_products(bp, pc)
        answer = values[asked]
        other = "AP·PR" if asked == "AC·CQ" else "AC·CQ"
        wrong = [v for v in dict.fromkeys([
            values[other],
            values["CP²"],
            bp * (bp + pc),
            ab * ab + bp * bp,  # AP²
            (bp + pc) ** 2,
            answer + pc,
        ]) if v != answer]
        return MathDraw(
            rf"AB={ab},\quad BP={bp},\quad PC={pc}",
            str(answer),
            prompt=(
                "รูปสามเหลี่ยม ABC มีมุม B เป็นมุมฉาก P อยู่บนด้าน BC วงกลม ω มี CP เป็นเส้นผ่านศูนย์กลาง "
                f"ตัด AC ที่ Q และเส้นตรง AP ตัด ω อีกครั้งที่ R จงหา {asked}"
            ),
            hint="∠CQP = 90° จึง CQ = CP·cos C และใช้กำลังของจุด A เทียบกับ ω: AP·AR = AQ·AC",
            distractors=[str(v) for v in wrong],
            variant=asked,
        )
