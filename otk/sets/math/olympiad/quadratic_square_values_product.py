"""n² + bn + c = m² factors as (2n + b − 2m)(2n + b + 2m) = b² − 4c."""

from __future__ import annotations

from math import isqrt, prod
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 17",))


def square_solutions(b: int, c: int) -> list[int]:
    """4(n² + bn + c) = 4m² gives (2n + b − 2m)(2n + b + 2m) = D = b² − 4c.
    Each factor pair e·f = D with f ≥ e and f − e ≡ 0 (mod 4) gives
    2n + b = (e + f)/2 (source: b = 59, c = 881, D = −43: n = −19, −40)."""
    d = b * b - 4 * c
    found = set()
    for e in range(1, abs(d) + 1):
        if d % e:
            continue
        for x in (e, -e):
            y = d // x
            if y >= x and (y - x) % 4 == 0 and (x + y) % 2 == 0 and ((x + y) // 2 - b) % 2 == 0:
                found.add(((x + y) // 2 - b) // 2)
    return sorted(found)


def _cases():
    out = []
    for b in range(11, 100, 2):
        for c in range(b * b // 4 - 60, b * b // 4 + 60):
            d = b * b - 4 * c
            if c <= 0 or d == 0 or isqrt(c) ** 2 == c:
                continue
            q = abs(d)
            if q > 2 and all(q % f for f in range(2, isqrt(q) + 1)):
                sols = square_solutions(b, c)
                if len(sols) == 2 and 0 not in sols:
                    out.append((b, c))
    return tuple(out)


CASES = _cases()


@question_type(
    "math.quadratic_square_values_product_olympiad",
    display_name={"th": "ผลคูณของจำนวนเต็มที่ทำให้พหุนามกำลังสองเป็นกำลังสองสมบูรณ์"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="กำลังสองสมบูรณ์",
)
class QuadraticSquareValuesProduct(WordProblem):
    def expr(self, rng: Random):
        b, c = rng.choice(CASES)
        sols = square_solutions(b, c)
        answer = prod(sols)
        roots = prod(isqrt(n * n + b * n + c) for n in sols)
        wrong = [v for v in dict.fromkeys([sum(sols), -answer, c, roots, max(sols, key=abs)]) if v != answer]
        return MathDraw(
            rf"n^2+{b}n+{c}",
            str(answer),
            prompt="จงหาผลคูณของจำนวนเต็ม n ทั้งหมดที่ทำให้นิพจน์ต่อไปนี้เป็นกำลังสองสมบูรณ์",
            hint="ให้ n² + bn + c = m² คูณด้วย 4 แล้วเขียนเป็นผลต่างกำลังสอง (2n + b)² − (2m)² = b² − 4c",
            distractors=[str(v) for v in wrong],
        )
