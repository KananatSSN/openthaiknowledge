"""a z^(n+1) − z^n − 1 = 0 has a root on the unit circle iff n ≡ −2 (mod 2m), where a = 2cos(π/m)."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2550, วันแรก ข้อ 10",))


COEFFICIENTS = ((3, "1"), (4, r"\sqrt{2}"), (5, r"\frac{1+\sqrt{5}}{2}"), (6, r"\sqrt{3}"))


def smallest_index(m: int, above: int) -> int:
    """|z| = 1 and z^n(az − 1) = 1 force |az − 1| = 1, so cos θ = a/2 and
    z = e^{±iπ/m}. Then az − 1 = e^{±2iπ/m}, so z^n = e^{∓2iπ/m}: n ≡ −2
    (mod 2m). Returns the least such n greater than `above` (source: √3, n = 10)."""
    return least_congruent(-2, 2 * m, above)


def least_congruent(residue: int, modulus: int, above: int) -> int:
    n = residue % modulus or modulus
    while n <= above:
        n += modulus
    return n


@question_type(
    "math.unit_root_power_index_olympiad",
    display_name={"th": "เลขชี้กำลังที่ทำให้สมการมีรากขนาดหนึ่งหน่วย"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="รากของพหุนาม",
)
class UnitRootPowerIndex(WordProblem):
    def expr(self, rng: Random):
        m, coef = rng.choice(COEFFICIENTS)
        above = rng.choice([0, 0, rng.randint(5, 60)])
        answer = smallest_index(m, above)
        wrong = [v for v in dict.fromkeys([least_congruent(2, 2 * m, above), least_congruent(-2, m, above), least_congruent(-1, 2 * m, above), least_congruent(0, 2 * m, above), answer + 2 * m]) if v != answer]
        lead = "" if coef == "1" else coef
        condition = "" if above == 0 else f" และ n > {above}"
        return MathDraw(
            rf"{lead}\,z^{{n+1}}-z^{{n}}-1=0",
            str(answer),
            prompt=f"จงหาจำนวนเต็มบวก n ที่น้อยที่สุด{condition} ที่ทำให้สมการต่อไปนี้มีรากที่มีขนาดหนึ่งหน่วย",
            hint="ถ้า |z| = 1 แล้ว |az − 1| = |z⁻ⁿ| = 1 หา z ก่อน แล้วแก้ zⁿ = 1/(az − 1)",
            distractors=[str(v) for v in wrong],
        )
