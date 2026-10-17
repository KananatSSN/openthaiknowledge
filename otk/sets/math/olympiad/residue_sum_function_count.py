"""Count maps {1..N} → {u, v, w} with Σ f(k) ≡ t (mod 3) by the residue transfer."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 11",))


PATTERNS = ((0, 0, 1), (0, 0, 2), (1, 1, 2), (1, 1, 0), (2, 2, 0), (2, 2, 1), (0, 1, 2))


def residue_counts(values: tuple[int, ...], n: int) -> list[int]:
    """counts[r] = number of maps {1..n} → values whose sum is ≡ r (mod 3),
    built one argument at a time (source: residues 1, 2, 0 give 3^2549)."""
    counts = [1, 0, 0]
    for _ in range(n):
        new = [0, 0, 0]
        for r, c in enumerate(counts):
            for v in values:
                new[(r + v) % 3] += c
        counts = new
    return counts


def pick_values(rng: Random, pattern: tuple[int, ...]) -> tuple[int, ...]:
    values: list[int] = []
    for r in pattern:
        while True:
            v = 3 * rng.randint(4, 33) + r
            if v not in values:
                values.append(v)
                break
    return tuple(sorted(values))


@question_type(
    "math.residue_sum_function_count_olympiad",
    display_name={"th": "จำนวนฟังก์ชันที่ผลบวกค่าหารด้วย 3 ลงตัว"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="การนับเชิงการจัด",
)
class ResidueSumFunctionCount(WordProblem):
    def expr(self, rng: Random):
        pattern = rng.choice(PATTERNS)
        values = pick_values(rng, pattern)
        n = rng.randint(4, 12)
        target = rng.randint(0, 2)
        counts = residue_counts(values, n)
        answer = counts[target]
        wrong = [v for v in dict.fromkeys([counts[(target + 1) % 3], counts[(target + 2) % 3], 3 ** (n - 1), 3 ** n - answer, answer + 3 ** (n - 2)]) if v != answer]
        rest = "หารด้วย 3 ลงตัว" if target == 0 else f"หารด้วย 3 เหลือเศษ {target}"
        return MathDraw(
            rf"f:\{{1,2,\ldots,{n}\}}\to\{{{values[0]},{values[1]},{values[2]}\}}",
            str(answer),
            prompt=f"จงหาจำนวนฟังก์ชัน f ซึ่ง f(1) + f(2) + … + f({n}) {rest}",
            hint="ดูเฉพาะเศษจากการหารด้วย 3 ของค่าแต่ละตัว แล้วนับทีละตำแหน่งตามเศษของผลบวกสะสม",
            distractors=[str(v) for v in wrong],
        )
