"""EF meets the median CM at G: EG : GF = k·BC : AC when CE = k·CF."""

from __future__ import annotations

from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 4",))


def segment_ratio(ac: int, bc: int, k: int) -> tuple[int, int]:
    """With C the origin, E = (CE/AC)·a and F = (CF/BC)·b; G on EF is a multiple
    of a + b, which gives EG : GF = k·BC : AC (source: 36 : 16 = 9 : 4)."""
    p, q = k * bc, ac
    g = gcd(p, q)
    return p // g, q // g


@question_type(
    "math.cevian_segment_ratio_olympiad",
    display_name={"th": "อัตราส่วนที่เส้นมัธยฐานแบ่งส่วนของเส้นตรง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: สามเหลี่ยมและเส้นมัธยฐาน",
)
class CevianSegmentRatio(WordProblem):
    def expr(self, rng: Random):
        ac, bc, k = rng.randint(5, 30), rng.randint(5, 30), rng.randint(2, 5)
        p, q = segment_ratio(ac, bc, k)
        answer = f"{p}:{q}"
        wrong = [t for t in dict.fromkeys([f"{q}:{p}", ":".join(map(str, segment_ratio(bc, ac, k))), ":".join(map(str, segment_ratio(ac, bc, 1))), f"{k}:1", f"{p + q}:{q}"]) if t != answer]
        return MathDraw(
            rf"AC={ac},\quad BC={bc},\quad CE={k}\,CF",
            answer,
            prompt="E อยู่บน AC, F อยู่บน BC และ M เป็นจุดกึ่งกลาง AB เส้น EF ตัด CM ที่ G จงหา EG : GF",
            hint="ใช้เวกเตอร์จาก C: จุดบน CM เป็นพหุคูณของ CA + CB",
            distractors=wrong,
        )
