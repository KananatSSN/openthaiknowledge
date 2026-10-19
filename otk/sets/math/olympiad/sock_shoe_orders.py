"""k feet, sock before shoe on each: (2k)!/2^k orders."""

from __future__ import annotations

from math import factorial
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 12",))


def dressing_orders(feet: int) -> int:
    """2k distinct actions in any order, and on each foot exactly half the
    orders put the sock first: (2k)!/2^k (source: 4 feet, 8!/16 = 2520)."""
    return factorial(2 * feet) // 2 ** feet


@question_type(
    "math.sock_shoe_orders_olympiad",
    display_name={"th": "จำนวนลำดับการใส่ถุงเท้าและรองเท้า"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class SockShoeOrders(WordProblem):
    def expr(self, rng: Random):
        feet = rng.randint(2, 7)
        answer = dressing_orders(feet)
        wrong = [v for v in dict.fromkeys([factorial(2 * feet), factorial(feet) ** 2, factorial(2 * feet) // factorial(feet), answer // factorial(feet), factorial(2 * feet) // 2]) if v != answer]
        return MathDraw(
            rf"k={feet}",
            str(answer),
            prompt="สิ่งมีชีวิตตัวหนึ่งมี k เท้า ต้องใส่ถุงเท้าและรองเท้าให้ครบทุกเท้า โดยแต่ละเท้าต้องใส่ถุงเท้าก่อนรองเท้า จะมีลำดับการใส่ได้กี่วิธี",
            hint="มีการกระทำ 2k อย่างที่ต่างกัน ในแต่ละเท้าลำดับครึ่งหนึ่งเท่านั้นที่ใส่ถุงเท้าก่อน",
            distractors=[str(v) for v in wrong],
        )
