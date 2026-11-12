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

from fractions import Fraction  # noqa: E402

from otk.core.content import math as _math_block  # noqa: E402
from otk.core.content import text as _text_block  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit import story as _story  # noqa: E402
from otk.kit.math_problems import MathType, WordProblem  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m3 import LEVEL  # noqa: E402
from otk.sets._support.math_p2 import _maths as _fixed_maths  # noqa: E402


def _fk3(*values: Fraction, answer: Fraction, lo: Fraction | None = None) -> list[str]:
    """Distinct fraction distractors as TeX, the answer (and values below lo) left out."""
    out: list[str] = []
    for v in values:
        v = Fraction(v)
        if v == answer or (lo is not None and v < lo) or frac_tex(v) in out:
            continue
        out.append(frac_tex(v))
    return out


def _tk3(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _roots3(a: int, b: int) -> str:
    lo, hi = sorted((a, b))
    return rf"x = {lo}, \; {hi}"


def _g3(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572."""
    return f"{n:,}".replace(",", "{,}")


def _gk3(*values: int, answer: int, lo: int = 0) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g3(int(v)) for v in _story.keep(*values, answer=answer, lo=lo)]


# ── More factorising (2026-11): a difference of squares, a perfect square, a leading coefficient of two, two
# variables, and which binomial is a factor ──


def _lin3(a: int, b: int, sym: str = "x") -> str:
    return f"({poly_tex((a, sym), (b, ''))})"


@question_type("math.factor_difference_of_squares_m3", display_name={"th": "แยกตัวประกอบผลต่างกำลังสอง"},
               level=LEVEL, topic="แยกตัวประกอบ")
class FactorDifferenceOfSquaresM3(MathType):
    def expr(self, rng: Random):
        a, b = rng.randint(1, 9), rng.randint(1, 12)
        right = f"{_lin3(a, b)}{_lin3(a, -b)}"
        # Both signs the same; not square-rooted; the first term not rooted.
        wrongs = [f"{_lin3(a, b)}{_lin3(a, b)}", f"{_lin3(a, -b)}^{{2}}", f"{_lin3(a * a, b)}{_lin3(1, -b)}"]
        return MathDraw(poly_tex((a * a, "x^{2}"), (-b * b, "")), right, prompt="จงแยกตัวประกอบ",
                        distractors=_tk3(*wrongs, answer=right))


@question_type("math.factor_perfect_square_m3", display_name={"th": "แยกตัวประกอบกำลังสองสมบูรณ์"},
               level=LEVEL, topic="แยกตัวประกอบ")
class FactorPerfectSquareM3(MathType):
    def expr(self, rng: Random):
        a = rng.choice((1, -1)) * rng.randint(1, 12)
        right = f"{binomial_tex(a)}^{{2}}"
        # The sign of a flipped; a difference of squares; the middle coefficient as the root.
        wrongs = [f"{binomial_tex(-a)}^{{2}}", f"{binomial_tex(a)}{binomial_tex(-a)}", f"{binomial_tex(2 * a)}^{{2}}"]
        return MathDraw(poly_tex((1, "x^{2}"), (2 * a, "x"), (a * a, "")), right, prompt="จงแยกตัวประกอบ",
                        distractors=_tk3(*wrongs, answer=right))


@question_type("math.factor_leading_two_m3", display_name={"th": "แยกตัวประกอบเมื่อสัมประสิทธิ์ของ x² เป็น 2"},
               level=LEVEL, topic="แยกตัวประกอบ")
class FactorLeadingTwoM3(MathType):
    def expr(self, rng: Random):
        while True:
            p = rng.choice((1, -1)) * rng.choice((1, 3, 5, 7, 9))
            q = rng.choice((1, -1)) * rng.randint(1, 9)
            if p + 2 * q != 0 and p != 2 * q:
                break
        right = f"{_lin3(2, p)}{_lin3(1, q)}"
        # The constants swapped; both signs flipped; the 2 on the other bracket.
        wrongs = [f"{_lin3(2, q)}{_lin3(1, p)}", f"{_lin3(2, -p)}{_lin3(1, -q)}", f"{_lin3(1, p)}{_lin3(2, -q)}"]
        return MathDraw(poly_tex((2, "x^{2}"), (p + 2 * q, "x"), (p * q, "")), right, prompt="จงแยกตัวประกอบ",
                        distractors=_tk3(*wrongs, answer=right))


@question_type("math.factor_two_variables_m3", display_name={"th": "แยกตัวประกอบพหุนามสองตัวแปร"},
               level=LEVEL, topic="แยกตัวประกอบ")
class FactorTwoVariablesM3(MathType):
    def expr(self, rng: Random):
        while True:
            a, b = rng.choice((1, -1)) * rng.randint(1, 7), rng.choice((1, -1)) * rng.randint(1, 7)
            if a + b != 0 and a != b:
                break
        right = f"({poly_tex((1, 'x'), (a, 'y'))})({poly_tex((1, 'x'), (b, 'y'))})"
        # Both signs flipped; the y left off one bracket; one sign flipped.
        wrongs = [f"({poly_tex((1, 'x'), (-a, 'y'))})({poly_tex((1, 'x'), (-b, 'y'))})",
                  f"({poly_tex((1, 'x'), (a, 'y'))})({poly_tex((1, 'x'), (b, ''))})",
                  f"({poly_tex((1, 'x'), (a, 'y'))})({poly_tex((1, 'x'), (-b, 'y'))})"]
        return MathDraw(poly_tex((1, "x^{2}"), (a + b, "xy"), (a * b, "y^{2}")), right, prompt="จงแยกตัวประกอบ",
                        distractors=_tk3(*wrongs, answer=right))


@question_type("math.which_factor_m3", display_name={"th": "ข้อใดเป็นตัวประกอบของพหุนาม"},
               level=LEVEL, topic="แยกตัวประกอบ")
class WhichFactorM3(QuestionType):
    """Fixed choices: a binomial from another draw could also be a factor."""

    def build(self, rng: Random, **params):
        while True:
            a, b = rng.choice((1, -1)) * rng.randint(1, 9), rng.choice((1, -1)) * rng.randint(1, 9)
            if a != b and a != -b:
                break
        poly = poly_tex((1, "x^{2}"), (a + b, "x"), (a * b, ""))
        right = binomial_tex(a)
        # This factor's sign flipped; the other's sign flipped; the product or sum as the constant.
        third = next(r for r in (a * b, a + b, -(a + b), a - b, 2 * a + 1) if r and abs(r) not in (abs(a), abs(b)))
        wrongs = [binomial_tex(-a), binomial_tex(-b), binomial_tex(third)]
        return _fixed_maths([_text_block("ข้อใดเป็นตัวประกอบของ"), _math_block(poly)], right,
                            _tk3(*wrongs, answer=right), self.topic)

