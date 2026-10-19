"""In a round robin without draws, Σ wins² = Σ losses²."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2553, วันแรก ข้อ 5",)
)


def square_sums(wins: list[int]) -> dict[str, int]:
    """aᵢ + bᵢ = n − 1 and Σaᵢ = Σbᵢ, so Σaᵢ² − Σbᵢ² = (n − 1)(Σaᵢ − Σbᵢ) = 0."""
    n = len(wins)
    losses = [n - 1 - w for w in wins]
    return {
        "losses": sum(b * b for b in losses),
        "products": sum(w * b for w, b in zip(wins, losses)),
    }


def random_scores(n: int, rng: Random) -> list[int]:
    wins = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            wins[i if rng.randrange(2) else j] += 1
    return sorted(wins, reverse=True)


@question_type(
    "math.tournament_square_sums_olympiad",
    display_name={"th": "ผลบวกกำลังสองของจำนวนครั้งชนะและแพ้ในการแข่งขันพบกันหมด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การจัดหมู่",
)
class TournamentSquareSums(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(5, 9)
        wins = random_scores(n, rng)
        values = square_sums(wins)
        asked = rng.choice(("losses", "products"))
        answer = values[asked]
        squares = sum(w * w for w in wins)
        wrong = [v for v in dict.fromkeys([
            values["products"] if asked == "losses" else values["losses"],
            (n - 1) ** 2 * n - squares,
            n * (n - 1) // 2,
            answer + n - 1,
            answer - 2,
        ]) if v != answer and v >= 0]
        label = "Σ bᵢ² (ผลบวกกำลังสองของจำนวนครั้งที่แพ้)" if asked == "losses" else "Σ aᵢbᵢ"
        return MathDraw(
            rf"(a_1,\ldots,a_{{{n}}})=({','.join(map(str, wins))})",
            str(answer),
            prompt=(
                f"นักกีฬา {n} คนแข่งพบกันหมด ผลมีเพียงชนะหรือแพ้ aᵢ คือจำนวนครั้งที่ชนะและ bᵢ คือจำนวนครั้งที่แพ้ของคนที่ i "
                f"จงหา {label}"
            ),
            hint="aᵢ + bᵢ = n − 1 และ Σaᵢ = Σbᵢ = จำนวนคู่ทั้งหมด",
            distractors=[str(v) for v in wrong],
            variant=asked,
        )
