"""Boys and girls round robin with asymmetric points: top score 4n − 1 forces ties."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2555, ข้อ 8",)
)


def draw_fraction(n: int) -> Fraction:
    """Every game hands out at least 2 points, so the 4n players average at
    least 4n − 1; a top score of 4n − 1 forces equality: same-sex games are
    all draws, and each girl draws n boys and loses to n. Draws:
    2n(2n − 1) + 2n² out of C(4n, 2)."""
    draws = 2 * n * (2 * n - 1) + 2 * n * n
    games = 4 * n * (4 * n - 1) // 2
    return Fraction(draws, games)


def _tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


@question_type(
    "math.tie_heavy_round_robin_olympiad",
    display_name={"th": "สัดส่วนคู่ที่เสมอเมื่อคะแนนสูงสุดถูกจำกัด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การจัดหมู่",
)
class TieHeavyRoundRobin(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(2, 30)
        answer = draw_fraction(n)
        wrong = [_tex(v) for v in dict.fromkeys([
            Fraction(2 * n - 1, 4 * n - 1),  # same-sex draws only
            Fraction(1, 2),
            Fraction(3, 4),  # the large-n limit
            Fraction(3 * n, 4 * n - 1),
            Fraction(3 * n - 1, 4 * n),
        ]) if v != answer]
        return MathDraw(
            rf"n={n},\quad 4n-1={4 * n - 1}",
            _tex(answer),
            prompt=(
                "นักเรียนชาย 2n คนและหญิง 2n คนแข่งพบกันหมด เพศเดียวกัน: ชนะ 3 แพ้ 0 เสมอคนละ 1 "
                "ต่างเพศ: หญิงชนะได้ 3 เสมอได้ 2 แพ้ได้ 0 ส่วนชายชนะได้ 2 แพ้หรือเสมอได้ 0 "
                "ถ้าคะแนนรวมสูงสุดเท่ากับ 4n − 1 สัดส่วนของคู่ที่เสมอต่อคู่ทั้งหมดคือเท่าใด"
            ),
            hint="ทุกคู่ให้คะแนนรวมอย่างน้อย 2 คะแนน เทียบค่าเฉลี่ยกับคะแนนสูงสุด",
            distractors=wrong,
        )
