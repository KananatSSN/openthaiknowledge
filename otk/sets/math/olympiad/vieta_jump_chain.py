"""(m − n)² = kmn + m + n: Vieta jumping from (k + 3, 1) gives infinitely many pairs."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2552, วันที่สอง ข้อ 4",))


def next_pair(k: int, m: int, n: int) -> tuple[int, int]:
    """As a quadratic in its larger entry, m² − ((k + 2)n + 1)m + n² − n = 0,
    so (m, n) → ((k + 2)m + 1 − n, m) is another solution."""
    return (k + 2) * m + 1 - n, m


def chain(k: int, length: int) -> list[tuple[int, int]]:
    pairs = [(k + 3, 1)]
    while len(pairs) < length:
        pairs.append(next_pair(k, *pairs[-1]))
    return pairs


@question_type(
    "math.vieta_jump_chain_olympiad",
    display_name={"th": "การกระโดดแบบเวียตาในสมการ (m − n)² = kmn + m + n"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวนเชิงพีชคณิต",
)
class VietaJumpChain(WordProblem):
    def expr(self, rng: Random):
        k = rng.randint(1, 6)
        pairs = chain(k, rng.randint(2, 4))
        m, n = pairs[-1]
        answer = next_pair(k, m, n)[0]
        wrong = [v for v in dict.fromkeys([(k + 2) * m - n, (k + 2) * m + 1 + n, (k + 1) * m + 1 - n, k * m + 1, answer + 1]) if v != answer and v > m]
        return MathDraw(
            rf"(m-n)^2={k if k > 1 else ''}mn+m+n,\quad (m,n)=({m},{n})",
            str(answer),
            prompt="คู่ (m, n) ต่อไปนี้สอดคล้องสมการ จงหาค่า M > m ที่ทำให้ (M, m) สอดคล้องสมการด้วย",
            hint="มองเป็นสมการกำลังสองในตัวแปรตัวใหญ่ ผลบวกรากเท่ากับ (k + 2)n + 1",
            distractors=[str(v) for v in wrong],
        )
