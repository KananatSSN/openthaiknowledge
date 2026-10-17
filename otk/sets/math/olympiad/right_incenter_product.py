"""In a right triangle with hypotenuse a and inradius r, ∠BOC = 135° and BO·OC = √2·r·a."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันแรก ข้อ 4",))


TRIPLES = ((3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25), (20, 21, 29), (9, 40, 41), (12, 35, 37))


def product_coefficient(b: int, c: int, a: int) -> int:
    """r = (b + c − a)/2; triangle BOC has height r on BC and ∠BOC = 135°,
    so ra/2 = BO·OC·sin 135°/2 and BO·OC = √2·ra (source: 3, 4, 5 → 5√2)."""
    return (b + c - a) // 2 * a


@question_type(
    "math.right_incenter_product_olympiad",
    display_name={"th": "ผลคูณระยะจากจุดศูนย์กลางวงกลมแนบในถึงจุดยอด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: วงกลมแนบใน",
)
class RightIncenterProduct(WordProblem):
    def expr(self, rng: Random):
        b, c, a = rng.choice(TRIPLES)
        scale = rng.randint(1, 4)
        b, c, a = b * scale, c * scale, a * scale
        coef = product_coefficient(b, c, a)
        answer = rf"{coef}\sqrt{{2}}"
        r = (b + c - a) // 2
        wrong = [t for t in dict.fromkeys([str(coef), rf"{2 * coef}\sqrt{{2}}", rf"{coef}\sqrt{{3}}", rf"\frac{{{coef}\sqrt{{2}}}}{{2}}" if coef % 2 else rf"{coef // 2}\sqrt{{2}}", str(b * c // r if r else b * c)]) if t != answer]
        return MathDraw(
            rf"AB={b},\quad AC={c}",
            answer,
            prompt="ABC เป็นรูปสามเหลี่ยมแนบในวงกลมซึ่งมี BC เป็นเส้นผ่านศูนย์กลาง และ O เป็นจุดศูนย์กลางของวงกลมแนบในรูปสามเหลี่ยม ABC จงหาค่าของ BO·OC",
            hint="มุม A ฉาก จึง ∠BOC = 90° + A/2 = 135° พื้นที่สามเหลี่ยม BOC = r·BC/2 = BO·OC·sin 135°/2",
            distractors=wrong,
        )
