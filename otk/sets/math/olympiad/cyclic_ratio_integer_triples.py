"""a/b + b/c + c/a an integer forces abc to be a cube; count small triples."""

from __future__ import annotations

from fractions import Fraction
from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2555, ข้อ 12",)
)


def _search(limit: int) -> list[tuple[int, int, int]]:
    """For a prime p with exponents α, β, γ in a, b, c, a²c + b²a + c²b ≡ 0
    (mod abc) forces the two smallest of 2α + γ, 2β + α, 2γ + β to be equal,
    which gives α + β + γ ≡ 0 (mod 3): abc is a cube."""
    found = []
    for a in range(1, limit + 1):
        for b in range(1, limit + 1):
            for c in range(1, limit + 1):
                if gcd(gcd(a, b), c) == 1 and (a * a * c + b * b * a + c * c * b) % (a * b * c) == 0:
                    found.append((a, b, c))
    return found


_ALL = tuple(_search(30))


def integer_triples(limit: int) -> list[tuple[int, int, int]]:
    """Triples with entries ≤ limit (≤ 30), from one cached search."""
    if limit > 30:
        return _search(limit)
    return [t for t in _ALL if max(t) <= limit]


@question_type(
    "math.cyclic_ratio_integer_triples_olympiad",
    display_name={"th": "สามสิ่งอันดับที่ a/b + b/c + c/a เป็นจำนวนเต็ม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="ทฤษฎีจำนวนเชิงพีชคณิต",
)
class CyclicRatioIntegerTriples(WordProblem):
    def expr(self, rng: Random):
        limit = rng.randint(4, 30)
        triples = integer_triples(limit)
        if rng.randrange(2):
            answer = len(triples)
            wrong = [v for v in dict.fromkeys([answer - 1, answer + 3, answer // 3 or 2, 3 * answer, answer + 1]) if v != answer and v > 0]
            return MathDraw(
                rf"1\le a,b,c\le {limit},\quad \gcd(a,b,c)=1",
                str(answer),
                prompt="มีสามสิ่งอันดับ (a, b, c) ของจำนวนเต็มบวกกี่ชุดที่ทำให้ a/b + b/c + c/a เป็นจำนวนเต็ม",
                hint="ทุกชุดที่ได้มี abc เป็นกำลังสามสมบูรณ์ ลองพิจารณาเลขชี้กำลังของจำนวนเฉพาะแต่ละตัว",
                distractors=[str(v) for v in wrong],
                variant="count",
            )
        a, b, c = rng.choice([t for t in triples if t != (1, 1, 1)] or [(1, 2, 4)])
        value = Fraction(a, b) + Fraction(b, c) + Fraction(c, a)
        answer = int(value)
        wrong = [v for v in dict.fromkeys([answer + 1, answer - 1, a + b + c, round((a * b * c) ** (1 / 3)), 3]) if v != answer and v > 0]
        return MathDraw(
            rf"\frac{{{a}}}{{{b}}}+\frac{{{b}}}{{{c}}}+\frac{{{c}}}{{{a}}}",
            str(answer),
            prompt="จงหาค่าของผลบวกต่อไปนี้ (ซึ่งเป็นจำนวนเต็ม)",
            hint="หาตัวส่วนร่วม abc แล้วตรวจว่า a²c + b²a + c²b หาร abc ลงตัว",
            distractors=[str(v) for v in wrong],
            variant="value",
        )
