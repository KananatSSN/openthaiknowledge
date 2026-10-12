"""แยกตัวประกอบ

คณิตศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ค 1.2 ม.3/*

Sets moved here from: math, math_algebra, math_gaps_secondary.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import (
    MathDraw,
    MathType,
    WordProblem,
    binomial_tex,
    mono_tex,
    poly_tex,
)
from otk.sets._support.math_algebra import _nonzero
from otk.sets._support.math_gaps_secondary import _nz, _quad

PROVENANCE = Provenance("original")


@question_type("math.factor_special",
               display_name={"th": "แยกตัวประกอบ: ผลต่างกำลังสอง / ตัวประกอบร่วม"},
               level={"th": "ม.3"}, topic="แยกตัวประกอบ")
class FactorSpecial(MathType):
    def expr(self, rng: Random):
        if rng.random() < 0.5:
            k = rng.choice([1, 2, 3])
            a = rng.randint(1, 9 if k == 1 else 5)
            lead = "x^{2}" if k == 1 else rf"{k * k}x^{{2}}"
            return MathDraw(
                rf"{lead} - {(k * a) ** 2}",
                rf"({mono_tex(k, 1, 0)} + {a})({mono_tex(k, 1, 0)} - {a})",
                hint=r"a^2 - b^2 = (a+b)(a-b)", prompt="จงแยกตัวประกอบ")
        c = rng.randint(2, 5)
        r = rng.choice([1, -1]) * rng.randint(1, 6)
        return MathDraw(
            poly_tex((c, "x^{2}"), (c * r, "x")), rf"{c}x{binomial_tex(r)}",
            hint=r"\text{take out the common factor}", prompt="จงแยกตัวประกอบ")


@question_type("math.factor_quadratic",
               display_name={"th": "แยกตัวประกอบพหุนามกำลังสอง"}, level={"th": "ม.3"},
               topic="แยกตัวประกอบ")
class FactorQuadratic(MathType):
    def expr(self, rng: Random, root_hi: int = 9):
        while True:
            a = rng.choice([1, -1]) * rng.randint(1, root_hi)
            b = rng.choice([1, -1]) * rng.randint(1, root_hi)
            if a + b != 0:
                break
        if a < b:
            a, b = b, a
        factored = rf"{binomial_tex(a)}^{{2}}" if a == b \
            else rf"{binomial_tex(a)}{binomial_tex(b)}"
        return MathDraw(
            poly_tex((1, "x^{2}"), (a + b, "x"), (a * b, "")), factored,
            hint=r"x^2 + (a{+}b)x + ab = (x+a)(x+b)", prompt="จงแยกตัวประกอบ")


@question_type("math.factor_cubic_common_m3", display_name={"th": "แยกตัวประกอบพหุนามดีกรีสาม (ดึงตัวร่วมก่อน)"},
               level={"th": "ม.3"}, topic="แยกตัวประกอบ")
class FactorCubicCommonM3(WordProblem):
    """x³ + bx² + cx = x(x + p)(x + q), or ax³ − ab²x = ax(x − b)(x + b)."""
    break_convergence = True  # one-part slips cluster round the answer

    def expr(self, rng: Random):
        if rng.random() < 0.5:
            while True:
                p, q = _nz(rng, -7, 7), _nz(rng, -7, 7)
                if p != q and p + q:
                    break
            expanded = poly_tex((1, "x^{3}"), (p + q, "x^{2}"), (p * q, "x"))
            right = f"x{binomial_tex(p)}{binomial_tex(q)}"
            wrongs = [f"x({_quad(1, p + q, p * q)})", f"x{binomial_tex(-p)}{binomial_tex(-q)}",
                      f"{binomial_tex(p)}{binomial_tex(q)}"]
        else:
            a, b = rng.randint(2, 5), rng.randint(2, 6)
            expanded = poly_tex((a, "x^{3}"), (-a * b * b, "x"))
            right = f"{a}x{binomial_tex(-b)}{binomial_tex(b)}"
            wrongs = [f"{a}x({_quad(1, 0, -b * b)})", f"{a}x{binomial_tex(-b)}^{{2}}",
                      f"x{binomial_tex(-a * b)}{binomial_tex(a * b)}"]
        return MathDraw(expanded, right, prompt="จงแยกตัวประกอบให้สมบูรณ์", distractors=wrongs)


@question_type("math.factor_common_then_quadratic",
               display_name={"th": "ดึงตัวประกอบร่วมแล้วแยกต่อ"},
               level={"th": "ม.3"}, topic="แยกตัวประกอบ")
class FactorCommonThenQuadratic(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, common_hi: int = 6, root_hi: int = 8):
        k = rng.randint(2, common_hi)
        r1, r2 = (_nonzero(rng, -root_hi, root_hi) for _ in range(2))
        # k(x − r1)(x − r2)
        b, c = -(r1 + r2), r1 * r2
        shown = poly_tex((k, "x^2"), (k * b, "x"), (k * c, ""))
        answer = f"{k}{binomial_tex(-r1)}{binomial_tex(-r2)}"
        return MathDraw(
            shown, answer, prompt="จงแยกตัวประกอบ",
            distractors=[f"{binomial_tex(-r1)}{binomial_tex(-r2)}",
                         f"{k}{binomial_tex(r1)}{binomial_tex(r2)}",
                         f"{k}{binomial_tex(-r1)}{binomial_tex(r2)}",
                         # k dropped and a sign flipped.
                         f"{binomial_tex(r1)}{binomial_tex(r2)}",
                         f"{binomial_tex(-r1)}{binomial_tex(r2)}"])


@question_type("math.factor_cubic_grouping_m3", display_name={"th": "แยกตัวประกอบพหุนามดีกรีสามโดยจัดกลุ่ม"},
               level={"th": "ม.3"}, topic="แยกตัวประกอบ")
class FactorCubicGroupingM3(WordProblem):
    """x³ + ax² − b²x − ab² = (x + a)(x² − b²) = (x + a)(x − b)(x + b)."""
    break_convergence = True  # one-part slips cluster round the answer

    def expr(self, rng: Random):
        while True:
            a, b = _nz(rng, -6, 6), rng.randint(1, 6)
            if abs(a) != b:
                break
        expanded = poly_tex((1, "x^{3}"), (a, "x^{2}"), (-b * b, "x"), (-a * b * b, ""))
        right = f"{binomial_tex(a)}{binomial_tex(-b)}{binomial_tex(b)}"
        # Stopping at the grouping, and sign slips in the grouping.
        wrongs = [f"{binomial_tex(a)}({_quad(1, 0, -b * b)})",
                  f"{binomial_tex(-a)}{binomial_tex(-b)}{binomial_tex(b)}",
                  f"{binomial_tex(a)}{binomial_tex(b)}^{{2}}"]
        return MathDraw(expanded, right, prompt="จงแยกตัวประกอบให้สมบูรณ์", distractors=wrongs)
