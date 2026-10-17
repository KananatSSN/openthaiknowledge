"""Roots u³, v³, w³: e₁′ = e₁³ − 3e₁e₂ + 3e₃, e₂′ = e₂³ − 3e₁e₂e₃ + 3e₃², e₃′ = e₃³."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2547, วันแรก ข้อ 3",))


def cubed_coefficients(e1: int, e2: int, e3: int) -> tuple[int, int, int]:
    """Power sum p₃ and the same identity for the pairwise products uv, vw, wu
    (whose elementary sums are e₂, e₁e₃, e₃²) (source: 5, 4, 3 →
    x³ − 74x² − 89x − 27)."""
    return e1**3 - 3 * e1 * e2 + 3 * e3, e2**3 - 3 * e1 * e2 * e3 + 3 * e3 * e3, e3**3


def cubic_tex(a: int, b: int, c: int) -> str:
    def term(coef: int, body: str) -> str:
        if coef == 0:
            return ""
        mag = "" if abs(coef) == 1 and body else str(abs(coef))
        return ("-" if coef < 0 else "+") + mag + body

    return "x^3" + term(-a, "x^2") + term(b, "x") + term(-c, "") + "=0"


@question_type(
    "math.cubed_roots_polynomial_olympiad",
    display_name={"th": "สมการพหุนามที่มีรากเป็นกำลังสามของรากเดิม"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="พหุนามสมมาตร",
)
class CubedRootsPolynomial(WordProblem):
    def expr(self, rng: Random):
        e1, e2, e3 = rng.randint(1, 9), rng.randint(-6, 9), rng.randint(1, 5)
        a, b, c = cubed_coefficients(e1, e2, e3)
        answer = cubic_tex(a, b, c)
        wrong = [t for t in dict.fromkeys([cubic_tex(e1**3, e2**3, e3**3), cubic_tex(e1**3 - 3 * e1 * e2, b, c), cubic_tex(a, e2**3 - 3 * e1 * e2 * e3, c), cubic_tex(a, b, 3 * e3), cubic_tex(-a, b, -c)]) if t != answer]
        return MathDraw(
            cubic_tex(e1, e2, e3).replace("x", "t"),
            answer,
            prompt="ให้ u, v, w เป็นรากของสมการต่อไปนี้ (ในตัวแปร t) จงหาสมการพหุนามกำลังสามโมนิกในตัวแปร x ที่มี u³, v³, w³ เป็นราก",
            hint="ใช้ u³ + v³ + w³ = e₁³ − 3e₁e₂ + 3e₃ และใช้เอกลักษณ์เดียวกันกับ uv, vw, wu ซึ่งมีผลบวกสมมาตรเป็น e₂, e₁e₃, e₃²",
            distractors=wrong,
        )
