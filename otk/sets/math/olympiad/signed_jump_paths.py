"""Count integer jump paths of a fixed total length, exactly or modulo 2."""

from __future__ import annotations

from math import comb
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2562, ข้อ 4",)
)


def jump_paths(total: int, end: int) -> int:
    """Sequences of nonzero integer jumps with Σ|jump| = total, ending at end."""
    counts = [{0: 1}]
    for length in range(1, total + 1):
        row: dict[int, int] = {}
        for jump in range(1, length + 1):
            for position, ways in counts[length - jump].items():
                for target in (position + jump, position - jump):
                    row[target] = row.get(target, 0) + ways
        counts.append(row)
    return counts[total].get(end, 0)


def odd_endpoints(total: int) -> tuple[int, ...]:
    """End points with an odd number of paths.

    Modulo 2 the generating function 1/(1 − Σ tʲ(xʲ + x⁻ʲ)) is
    1 + t(x + 1/x)/(1 + t²), so only ±1 for an odd total and none for even.
    """
    return (-1, 1) if total % 2 else ()


def _set_tex(values) -> str:
    if not values:
        return r"\varnothing"
    return r"\{" + ",\\,".join(str(v) for v in sorted(values)) + r"\}"


@question_type(
    "math.signed_jump_paths_olympiad",
    display_name={"th": "จำนวนวิธีกระโดดบนเส้นจำนวนตามระยะทางรวม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class SignedJumpPaths(WordProblem):
    def expr(self, rng: Random):
        setup = (
            "กระต่ายเริ่มที่ 0 บนเส้นจำนวน แต่ละครั้งกระโดดไปยังจำนวนเต็มอื่นใดก็ได้ "
            "(ไม่อยู่กับที่) ให้ N(a) เป็นจำนวนลำดับการกระโดดที่ระยะทางรวมเท่ากับ "
        )
        if rng.randrange(2):
            total = rng.randint(3, 6)
            end = rng.choice(range(-total + 2, total + 1, 2))
            answer = jump_paths(total, end)
            wrong = []
            for value in (
                2 ** (total - 1),  # compositions of the total, signs ignored
                comb(total, (total + end) // 2),  # unit steps only
                2 ** total,
                answer + 2,
                answer - 2,
                2 * answer,
            ):
                if value > 0 and value != answer and value not in wrong:
                    wrong.append(value)
            return MathDraw(
                rf"N({end})",
                str(answer),
                prompt=setup + f"{total} หน่วยและจบที่ a จงหาค่าต่อไปนี้",
                hint="แยกกรณีตามการกระโดดครั้งแรก ยาว j หน่วยไปทางซ้ายหรือขวา แล้วนับระยะทางที่เหลือ n − j แบบเดียวกัน",
                distractors=[str(value) for value in wrong],
                variant="count",
            )
        total = rng.randint(50, 2030)
        answer = odd_endpoints(total)
        options = [
            odd_endpoints(total + 1),  # the other parity's answer
            (-total, total),  # only the single-jump paths
            (0,),
            (-total, -1, 1, total),
            (1,),
        ]
        return MathDraw(
            "",
            _set_tex(answer),
            prompt=setup + f"{total} หน่วยและจบที่ a เซตของจำนวนเต็ม a ทั้งหมดที่ N(a) เป็นจำนวนคี่คือข้อใด",
            hint="จับคู่ลำดับการกระโดดที่สะท้อนกันได้ หรือคิดฟังก์ชันก่อกำเนิดมอดุโล 2 ซึ่งลดรูปเหลือ 1 + t(x + 1/x)/(1 + t²)",
            distractors=[_set_tex(o) for o in options if o != answer],
            variant="parity",
        )
