"""แยกตัวประกอบ

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 3 ม.4/1

Sets moved here from: math, math_algebra.
"""

from __future__ import annotations

import math as _math
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, binomial_tex, poly_tex
from otk.sets._support.math_algebra import _nonzero, _signed

PROVENANCE = Provenance("original")


@question_type("math.factor_by_grouping", display_name={"th": "แยกตัวประกอบโดยจัดกลุ่ม"},
               level={"th": "ม.4"}, topic="แยกตัวประกอบ")
class FactorByGrouping(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, coef_hi: int = 6):
        # gcd(a, b) = 1, or (ax + b) still has a common factor to pull out and
        # the "fully factored" answer would not be fully factored.
        while True:
            a, b = rng.randint(1, coef_hi), _nonzero(rng, -coef_hi, coef_hi)
            if _math.gcd(a, abs(b)) == 1:
                break
        c = _nonzero(rng, -coef_hi, coef_hi)
        # (ax + b)(x^2 + c) = ax^3 + bx^2 + acx + bc
        shown = poly_tex((a, "x^3"), (b, "x^2"), (a * c, "x"), (b * c, ""))
        answer = rf"({poly_tex((a, 'x'), (b, ''))})(x^2{_signed(c)})"
        return MathDraw(
            shown, answer, prompt="จงแยกตัวประกอบโดยการจัดกลุ่ม",
            distractors=[rf"({poly_tex((a, 'x'), (-b, ''))})(x^2{_signed(c)})",
                         rf"({poly_tex((a, 'x'), (b, ''))})(x^2{_signed(-c)})",
                         rf"(x^2{_signed(c)})({poly_tex((b, 'x'), (a, ''))})"])


@question_type("math.factor_cubes", display_name={"th": "ผลบวก/ผลต่างกำลังสาม"},
               level={"th": "ม.4"}, topic="แยกตัวประกอบ")
class FactorCubes(MathType):
    def expr(self, rng: Random, a_hi: int = 4, b_hi: int = 5):
        a = rng.randint(1, a_hi)
        b = rng.randint(1, b_hi)
        ax = "x" if a == 1 else f"{a}x"
        if rng.random() < 0.5:
            shown = poly_tex((a ** 3, "x^3"), (b ** 3, ""))
            answer = (rf"({ax} + {b})({poly_tex((a * a, 'x^2'), (-a * b, 'x'), (b * b, ''))})")
            wrong = [rf"({ax} + {b})({poly_tex((a * a, 'x^2'), (a * b, 'x'), (b * b, ''))})",
                     rf"({ax} - {b})({poly_tex((a * a, 'x^2'), (a * b, 'x'), (b * b, ''))})",
                     rf"({ax} + {b})^3"]
        else:
            shown = poly_tex((a ** 3, "x^3"), (-(b ** 3), ""))
            answer = (rf"({ax} - {b})({poly_tex((a * a, 'x^2'), (a * b, 'x'), (b * b, ''))})")
            wrong = [rf"({ax} - {b})({poly_tex((a * a, 'x^2'), (-a * b, 'x'), (b * b, ''))})",
                     rf"({ax} + {b})({poly_tex((a * a, 'x^2'), (-a * b, 'x'), (b * b, ''))})",
                     rf"({ax} - {b})^3"]
        return MathDraw(shown, answer, prompt="จงแยกตัวประกอบ", distractors=wrong)


@question_type("math.factor_advanced",
               display_name={"th": "แยกตัวประกอบขั้นสูง (จัดกลุ่ม, กำลังสาม)"},
               level={"th": "ม.4"}, topic="แยกตัวประกอบ")
class FactorAdvanced(MathType):
    def expr(self, rng: Random):
        kind = rng.choice(["group", "cubes", "biquad"])
        if kind == "group":
            a = rng.choice([1, -1]) * rng.randint(1, 5)
            b = rng.randint(2, 9)
            tex = poly_tex((1, "x^{3}"), (a, "x^{2}"), (b, "x"), (a * b, ""))
            return MathDraw(tex, rf"{binomial_tex(a)}(x^{{2}} + {b})",
                            hint=r"\text{group in pairs}", prompt="จงแยกตัวประกอบ")
        if kind == "cubes":
            a = rng.randint(1, 5)
            if rng.random() < 0.5:
                return MathDraw(
                    rf"x^{{3}} + {a ** 3}",
                    rf"(x + {a})({poly_tex((1, 'x^{2}'), (-a, 'x'), (a * a, ''))})",
                    hint=r"a^3 + b^3 = (a+b)(a^2 - ab + b^2)", prompt="จงแยกตัวประกอบ")
            return MathDraw(
                rf"x^{{3}} - {a ** 3}",
                rf"(x - {a})({poly_tex((1, 'x^{2}'), (a, 'x'), (a * a, ''))})",
                hint=r"a^3 - b^3 = (a-b)(a^2 + ab + b^2)", prompt="จงแยกตัวประกอบ")
        a, b = rng.sample(range(1, 5), 2)
        a, b = min(a, b), max(a, b)
        tex = poly_tex((1, "x^{4}"), (-(a * a + b * b), "x^{2}"), (a * a * b * b, ""))
        return MathDraw(
            tex,
            rf"{binomial_tex(a)}{binomial_tex(-a)}{binomial_tex(b)}{binomial_tex(-b)}",
            hint=r"\text{treat } x^2 \text{ as the variable}",
            prompt="จงแยกตัวประกอบให้สมบูรณ์")

from fractions import Fraction  # noqa: E402

from otk.core.content import math as _math_block  # noqa: E402
from otk.core.content import text as _text_block  # noqa: E402
from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m4 import M4 as LEVEL  # noqa: E402
from otk.sets._support.math_p2 import _maths as _fixed_maths  # noqa: E402


def _nz4(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk4(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk4(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk4(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt4(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk4(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk4(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))

# ── More factorising (2026-11): a sum of cubes, a common factor then a difference of squares, which binomial
# is a factor, a biquadratic, x³ + y³ from the sum and product, a cubic with three whole roots, and four
# terms in pairs ──


def _bin4(r: int, sym: str = "x") -> str:
    return binomial_tex(r, sym)


@question_type("math.sum_of_cubes_m4", display_name={"th": "แยกตัวประกอบผลบวกกำลังสาม"}, level=LEVEL, topic="แยกตัวประกอบ")
class SumOfCubesM4(MathType):
    def expr(self, rng: Random):
        a = rng.randint(1, 6)
        right = rf"(x + {a})(x^{{2}} - {a}x + {a * a})".replace(" 1x", " x")
        # The middle sign wrong; the middle term doubled; a difference of cubes pattern.
        wrongs = [rf"(x + {a})(x^{{2}} + {a}x + {a * a})", rf"(x + {a})(x^{{2}} - {2 * a}x + {a * a})",
                  rf"(x - {a})(x^{{2}} + {a}x + {a * a})"]
        wrongs = [w.replace(" 1x", " x") for w in wrongs]
        return MathDraw(f"x^{{3}} + {a ** 3}", right, prompt="จงแยกตัวประกอบ", distractors=_tk4(*wrongs, answer=right))


@question_type("math.common_then_squares_m4", display_name={"th": "ดึงตัวร่วมแล้วแยกผลต่างกำลังสอง"}, level=LEVEL,
               topic="แยกตัวประกอบ")
class CommonThenSquaresM4(MathType):
    def expr(self, rng: Random):
        a = rng.randint(1, 9)
        right = f"x{_bin4(a)}{_bin4(-a)}"
        # The x left out; squared bracket; the common factor kept squared.
        wrongs = [f"{_bin4(a)}{_bin4(-a)}", f"x{_bin4(-a)}^{{2}}", f"x^{{2}}{_bin4(-a)}", f"x(x^{{2}} - {a})"]
        return MathDraw(poly_tex((1, "x^{3}"), (-a * a, "x")), right, prompt="จงแยกตัวประกอบให้สมบูรณ์",
                        distractors=_tk4(*wrongs, answer=right))


@question_type("math.cubic_factor_test_m4", display_name={"th": "ข้อใดเป็นตัวประกอบของพหุนามดีกรีสาม"}, level=LEVEL,
               topic="แยกตัวประกอบ")
class CubicFactorTestM4(QuestionType):
    """Fixed choices: a binomial from another draw could also be a factor."""

    def build(self, rng: Random, **params):
        roots = rng.sample([r for r in range(-5, 6) if r], 3)
        a, b, c = roots
        poly = poly_tex((1, "x^{3}"), (-(a + b + c), "x^{2}"), (a * b + b * c + a * c, "x"), (-a * b * c, ""))
        right = _bin4(-a)
        bad = [r for r in range(-6, 7) if r and r not in roots]
        wrongs = [_bin4(a)] if -a not in roots else []
        wrongs += [_bin4(-r) for r in rng.sample(bad, 3)]
        return _fixed_maths([_text_block("ข้อใดเป็นตัวประกอบของ"), _math_block(poly)], right,
                            _tk4(*wrongs, answer=right)[:3], self.topic)


@question_type("math.biquadratic_m4", display_name={"th": "แยกตัวประกอบพหุนามดีกรีสี่ที่มีแต่กำลังคู่"}, level=LEVEL,
               topic="แยกตัวประกอบ")
class BiquadraticM4(MathType):
    def expr(self, rng: Random):
        a, b = sorted(rng.sample(range(1, 7), 2))
        right = f"{_bin4(-a)}{_bin4(a)}{_bin4(-b)}{_bin4(b)}"
        # One square's sign flipped; one pair's signs both minus; the numbers not square-rooted.
        wrongs = [f"(x^{{2}} - {a * a})(x^{{2}} + {b * b})", f"{_bin4(-a)}^{{2}}{_bin4(-b)}{_bin4(b)}",
                  f"{_bin4(-a * a)}{_bin4(a * a)}{_bin4(-b * b)}{_bin4(b * b)}"]
        return MathDraw(poly_tex((1, "x^{4}"), (-(a * a + b * b), "x^{2}"), (a * a * b * b, "")), right,
                        prompt="จงแยกตัวประกอบให้สมบูรณ์", distractors=_tk4(*wrongs, answer=right))


@question_type("math.cube_sum_from_sum_product_m4", display_name={"th": "หาค่า x³ + y³ จากผลบวกและผลคูณ"}, level=LEVEL,
               topic="แยกตัวประกอบ")
class CubeSumFromSumProductM4(MathType):
    def expr(self, rng: Random):
        s, p = rng.randint(2, 9), _nz4(rng, 1, 12)
        right = s ** 3 - 3 * s * p
        # The 3sp term added; only s cubed; p cubed taken away.
        return MathDraw(rf"x + y = {s}, \; xy = {p}", str(right), prompt="จงหาค่าของ x³ + y³",
                        distractors=_nk4(s ** 3 + 3 * s * p, s ** 3, s ** 3 - p ** 3, s ** 3 - 3 * p, answer=right))


@question_type("math.cubic_three_roots_m4", display_name={"th": "แยกตัวประกอบพหุนามดีกรีสามที่มีรากเป็นจำนวนเต็ม"},
               level=LEVEL, topic="แยกตัวประกอบ")
class CubicThreeRootsM4(MathType):
    def expr(self, rng: Random):
        a, b, c = sorted(rng.sample([r for r in range(-5, 6) if r], 3))
        poly = poly_tex((1, "x^{3}"), (-(a + b + c), "x^{2}"), (a * b + b * c + a * c, "x"), (-a * b * c, ""))
        right = f"{_bin4(-a)}{_bin4(-b)}{_bin4(-c)}"
        # Every sign flipped; one sign flipped; one root replaced by the constant.
        wrongs = [f"{_bin4(a)}{_bin4(b)}{_bin4(c)}", f"{_bin4(a)}{_bin4(-b)}{_bin4(-c)}",
                  f"{_bin4(-a)}{_bin4(-b)}{_bin4(c)}"]
        return MathDraw(poly, right, prompt="จงแยกตัวประกอบให้สมบูรณ์", distractors=_tk4(*wrongs, answer=right))


@question_type("math.four_terms_pairs_m4", display_name={"th": "แยกตัวประกอบโดยจับคู่สี่พจน์"}, level=LEVEL,
               topic="แยกตัวประกอบ")
class FourTermsPairsM4(MathType):
    def expr(self, rng: Random):
        a, b = _nz4(rng, 1, 9), _nz4(rng, 1, 9)
        poly = poly_tex((1, "xy"), (a, "y"), (b, "x"), (a * b, ""))
        right = f"{_bin4(a)}{_bin4(b, 'y')}"
        # The numbers swapped between brackets; both signs flipped; x and y in one bracket.
        wrongs = [f"{_bin4(b)}{_bin4(a, 'y')}", f"{_bin4(-a)}{_bin4(-b, 'y')}", f"(x + y){_bin4(a * b)}"]
        return MathDraw(poly, right, prompt="จงแยกตัวประกอบ", distractors=_tk4(*wrongs, answer=right))
