"""Values on every axis cross (x ± t, y), (x, y ± t) sum to K: f is the constant K/4."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2553, วันที่สอง ข้อ 5",)
)


def frac_tex(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}"


def cross_value(total: int, dimension: int) -> Fraction:
    """In one dimension f(x − t) + f(x + t) = K for all x and t ≠ 0 means
    f(p) + f(q) = K for all p ≠ q, so f is constant. In the plane the four
    points are the corners of a square in the rotated coordinates (x + y,
    x − y); the constant K/4 is the solution (uniqueness is sketched in the
    private note). In d dimensions the 2d points give K/(2d)."""
    return Fraction(total, 2 * dimension)


@question_type(
    "math.diamond_sum_functional_olympiad",
    display_name={"th": "สมการเชิงฟังก์ชันจากผลบวกค่าที่จุดสี่จุดรอบจุดหนึ่ง"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class DiamondSumFunctional(WordProblem):
    def expr(self, rng: Random):
        dimension = rng.choice((1, 2, 3))
        total = rng.randint(10, 3000)
        answer = cross_value(total, dimension)
        wrong = [frac_tex(v) for v in dict.fromkeys([Fraction(total, dimension), Fraction(total), Fraction(total, 4 * dimension), Fraction(total, 2 * dimension + 1), Fraction(total, 2)]) if v != answer]
        terms = {
            1: r"f(x-t)+f(x+t)",
            2: r"f(x-t,y)+f(x+t,y)+f(x,y-t)+f(x,y+t)",
            3: r"\sum_{\pm}\big(f(x\pm t,y,z)+f(x,y\pm t,z)+f(x,y,z\pm t)\big)",
        }[dimension]
        point = {1: "f(7)", 2: "f(3, −2)", 3: "f(1, 2, 3)"}[dimension]
        return MathDraw(
            rf"{terms}={total}",
            frac_tex(answer),
            prompt=f"f สอดคล้องสมการต่อไปนี้ทุกจุดและทุก t ≠ 0 จงหา {point}",
            hint="เริ่มจากกรณีหนึ่งมิติ: f(p) + f(q) เท่ากันทุก p ≠ q บังคับให้ f คงตัว",
            distractors=wrong,
            variant=str(dimension),
        )
