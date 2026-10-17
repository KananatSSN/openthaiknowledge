"""Every k-group has a champion and a loser ⇒ distinct scores, once n ≥ 2k − 3."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2555, ข้อ 6",)
)


def threshold(group: int) -> int:
    """A draw u–v: fewer than k − 2 others may fail to beat both (else that
    k-group has no champion), so ≥ n − k + 1 beat both and ≥ n − k + 1 lose to
    both, forcing n ≤ 2k − 4. A 3-cycle likewise forces n ≤ 2k − 5. With
    n ≥ 2k − 3 the results are transitive without draws, so scores differ;
    a draw with k − 3 players above and k − 3 below shows 2k − 4 is not enough."""
    return 2 * group - 3


@question_type(
    "math.tournament_top_bottom_threshold_olympiad",
    display_name={"th": "จำนวนผู้เล่นที่บังคับให้คะแนนแตกต่างกันในการแข่งขันพบกันหมด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การจัดหมู่",
)
class TournamentTopBottomThreshold(WordProblem):
    def expr(self, rng: Random):
        k = rng.randint(5, 200)
        answer = threshold(k)
        wrong = [v for v in dict.fromkeys([2 * k - 4, 2 * k - 5, 2 * k - 2, k + 1, 2 * k, k]) if v != answer]
        return MathDraw(
            rf"k={k}",
            str(answer),
            prompt=(
                "ผู้เล่น n คน (n ≥ k) แข่งแบบพบกันหมดคู่ละหนึ่งครั้ง ชนะได้ 2 แพ้ได้ 0 เสมอได้คนละ 1 คะแนน "
                "ถ้าผู้เล่น k คนกลุ่มใด ๆ มีคนหนึ่งชนะอีก k − 1 คน และมีคนหนึ่งแพ้อีก k − 1 คนเสมอ "
                "ค่า n ที่น้อยที่สุดที่รับประกันว่าผู้เล่นทุกคนได้คะแนนรวมต่างกันคือเท่าใด"
            ),
            hint="ถ้ามีคู่ที่เสมอกัน นับผู้ที่ชนะทั้งสองคนและผู้ที่แพ้ทั้งสองคน แล้วสร้างตัวอย่างค้านที่มีผู้เล่น 2k − 4 คน",
            distractors=[str(v) for v in wrong],
        )
