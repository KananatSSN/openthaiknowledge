"""กระจายทวินาม

คณิตศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ค 1.2 ม.3/*

Sets moved here from: math, math_algebra.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, binomial_tex, poly_tex
from otk.sets._support.math_algebra import _nonzero

PROVENANCE = Provenance("original")


@question_type("math.expand_binomials",
               display_name={"th": "กระจายทวินาม"}, level={"th": "ม.3"},
               topic="กระจายทวินาม")
class ExpandBinomials(MathType):
    def expr(self, rng: Random, root_hi: int = 9):
        a = rng.choice([1, -1]) * rng.randint(1, root_hi)
        b = rng.choice([1, -1]) * rng.randint(1, root_hi)
        return MathDraw(
            rf"{binomial_tex(a)}{binomial_tex(b)}",
            poly_tex((1, "x^{2}"), (a + b, "x"), (a * b, "")),
            prompt="จงกระจาย")


@question_type("math.expand_formula",
               display_name={"th": "กระจายด้วยสูตร"}, level={"th": "ม.3"},
               topic="กระจายทวินาม")
class ExpandFormula(MathType):
    def expr(self, rng: Random, a_hi: int = 9):
        a = rng.randint(1, a_hi)
        kind = rng.choice(["sq+", "sq-", "diff"])
        if kind == "sq+":
            return MathDraw(rf"(x + {a})^{{2}}",
                            poly_tex((1, "x^{2}"), (2 * a, "x"), (a * a, "")),
                            hint=r"(a+b)^2 = a^2 + 2ab + b^2", prompt="จงกระจาย")
        if kind == "sq-":
            return MathDraw(rf"(x - {a})^{{2}}",
                            poly_tex((1, "x^{2}"), (-2 * a, "x"), (a * a, "")),
                            hint=r"(a-b)^2 = a^2 - 2ab + b^2", prompt="จงกระจาย")
        return MathDraw(rf"(x + {a})(x - {a})",
                        poly_tex((1, "x^{2}"), (-a * a, "")),
                        hint=r"(a+b)(a-b) = a^2 - b^2", prompt="จงกระจาย")


@question_type("math.expand_three_terms", display_name={"th": "กระจายพหุนามสองวงเล็บ"},
               level={"th": "ม.3"}, topic="กระจายทวินาม")
class ExpandThreeTerms(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, coef_hi: int = 5, const_hi: int = 9):
        a, b = rng.randint(1, coef_hi), _nonzero(rng, -const_hi, const_hi)
        c, d = rng.randint(1, coef_hi), _nonzero(rng, -const_hi, const_hi)
        # (ax + b)(cx + d)
        p, q, r = a * c, a * d + b * c, b * d
        shown = (rf"({poly_tex((a, 'x'), (b, ''))})"
                 rf"({poly_tex((c, 'x'), (d, ''))})")
        return MathDraw(
            shown, poly_tex((p, "x^2"), (q, "x"), (r, "")),
            prompt="จงกระจายและจัดรูป",
            # Multiplying only the matching terms — the "FOIL without the OI" slip.
            distractors=[poly_tex((p, "x^2"), (r, "")),
                         poly_tex((p, "x^2"), (a * d - b * c, "x"), (r, "")),
                         poly_tex((p, "x^2"), (q, "x"), (-r, ""))])

from fractions import Fraction  # noqa: E402

from otk.core.registry import question_type  # noqa: E402
from otk.kit import story as _story  # noqa: E402
from otk.kit.math_problems import MathType  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m3 import LEVEL  # noqa: E402


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


# ── More binomial expansion (2026-11): one coefficient, (ax + b)², (ax + b)(ax − b), two variables, a product
# less a square, and squares and products done in the head ──


def _nz3(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


@question_type("math.binomial_x_coefficient_m3", display_name={"th": "สัมประสิทธิ์ของ x หลังกระจาย"},
               level=LEVEL, topic="กระจายทวินาม")
class BinomialXCoefficientM3(MathType):
    def expr(self, rng: Random):
        a, c = rng.randint(1, 5), rng.randint(1, 5)
        b, d = _nz3(rng, 1, 9), _nz3(rng, 1, 9)
        right = a * d + b * c
        left = f"({poly_tex((a, 'x'), (b, ''))})({poly_tex((c, 'x'), (d, ''))})"
        # The outer pair only; the inner pair only; the two constants multiplied.
        return MathDraw(left, str(right), prompt="เมื่อกระจายแล้ว สัมประสิทธิ์ของ x เท่ากับเท่าใด",
                        distractors=_tk3(str(a * d), str(b * c), str(b * d), str(a * c), str(right + 1), answer=str(right)))


@question_type("math.square_of_ax_plus_b_m3", display_name={"th": "กำลังสองของ (ax + b)"},
               level=LEVEL, topic="กระจายทวินาม")
class SquareOfAxPlusBM3(MathType):
    def expr(self, rng: Random):
        a = rng.randint(2, 6)
        b = _nz3(rng, 1, 9)
        right = poly_tex((a * a, "x^{2}"), (2 * a * b, "x"), (b * b, ""))
        # The middle term left out; the middle term not doubled; the first term not squared.
        wrongs = [poly_tex((a * a, "x^{2}"), (b * b, "")), poly_tex((a * a, "x^{2}"), (a * b, "x"), (b * b, "")),
                  poly_tex((a, "x^{2}"), (2 * a * b, "x"), (b * b, ""))]
        return MathDraw(f"({poly_tex((a, 'x'), (b, ''))})^{{2}}", right, prompt="จงกระจาย",
                        distractors=_tk3(*wrongs, answer=right))


@question_type("math.difference_of_squares_ax_m3", display_name={"th": "ผลคูณ (ax + b)(ax − b)"},
               level=LEVEL, topic="กระจายทวินาม")
class DifferenceOfSquaresAxM3(MathType):
    def expr(self, rng: Random):
        a, b = rng.randint(2, 9), rng.randint(1, 12)
        right = poly_tex((a * a, "x^{2}"), (-b * b, ""))
        # Added instead of taken away; not squared; a middle term kept.
        wrongs = [poly_tex((a * a, "x^{2}"), (b * b, "")), poly_tex((a, "x^{2}"), (-b, "")),
                  poly_tex((a * a, "x^{2}"), (-2 * a * b, "x"), (-b * b, ""))]
        return MathDraw(f"({a}x + {b})({a}x - {b})", right, prompt="จงกระจาย", distractors=_tk3(*wrongs, answer=right))


@question_type("math.expand_two_variables_m3", display_name={"th": "กระจายทวินามที่มีสองตัวแปร"},
               level=LEVEL, topic="กระจายทวินาม")
class ExpandTwoVariablesM3(MathType):
    def expr(self, rng: Random):
        a, b = _nz3(rng, 1, 7), _nz3(rng, 1, 7)
        right = poly_tex((1, "x^{2}"), (a + b, "xy"), (a * b, "y^{2}"))
        # The middle term from the product; the constants added for the last; the cross term dropped.
        wrongs = [poly_tex((1, "x^{2}"), (a * b, "xy"), (a + b, "y^{2}")), poly_tex((1, "x^{2}"), (a * b, "y^{2}")),
                  poly_tex((1, "x^{2}"), (a + b, "xy"), (a * b, "y"))]
        return MathDraw(f"({poly_tex((1, 'x'), (a, 'y'))})({poly_tex((1, 'x'), (b, 'y'))})", right, prompt="จงกระจาย",
                        distractors=_tk3(*wrongs, answer=right))


@question_type("math.product_minus_square_m3", display_name={"th": "กระจายแล้วจัดรูปให้อย่างง่าย"},
               level=LEVEL, topic="กระจายทวินาม")
class ProductMinusSquareM3(MathType):
    def expr(self, rng: Random):
        a, b = _nz3(rng, 1, 9), _nz3(rng, 1, 9)
        while a + b == 0:
            b = _nz3(rng, 1, 9)
        right = poly_tex((a + b, "x"), (a * b, ""))
        # The square kept; the constant's sign lost; the x terms not combined.
        wrongs = [poly_tex((1, "x^{2}"), (a + b, "x"), (a * b, "")), poly_tex((a + b, "x"), (-a * b, "")),
                  poly_tex((a * b, "x"), (a + b, ""))]
        return MathDraw(f"{binomial_tex(a)}{binomial_tex(b)} - x^{{2}}", right, prompt="จงกระจายและจัดรูปให้อย่างง่าย",
                        distractors=_tk3(*wrongs, answer=right))


@question_type("math.mental_square_m3", display_name={"th": "หากำลังสองด้วยการกระจาย"},
               level=LEVEL, topic="กระจายทวินาม")
class MentalSquareM3(MathType):
    def expr(self, rng: Random):
        base = rng.choice((20, 30, 40, 50, 60, 70, 80, 90, 100))
        d = _nz3(rng, 1, 4)
        n = base + d
        right = n * n
        # The middle term forgotten; the middle term not doubled; d squared with the wrong sign.
        return MathDraw(f"{n}^{{2}}", f"{right:,}".replace(",", "{,}"), prompt="จงหาค่า (ใช้การกระจายกำลังสองของทวินาม)",
                        distractors=[f"{int(v):,}".replace(",", "{,}")
                                     for v in _story.keep(base * base + d * d, base * base + base * d + d * d,
                                                          base * base + 2 * base * d - d * d, right + 10, answer=right, lo=1)])


@question_type("math.mental_product_m3", display_name={"th": "หาผลคูณด้วยผลต่างกำลังสอง"},
               level=LEVEL, topic="กระจายทวินาม")
class MentalProductM3(MathType):
    def expr(self, rng: Random):
        base = rng.choice((20, 30, 40, 50, 60, 70, 80, 90, 100))
        d = rng.randint(1, 5)
        right = base * base - d * d
        # Added instead of taken away; d not squared; the square of the base alone.
        return MathDraw(f"{base - d} \\times {base + d}", f"{right:,}".replace(",", "{,}"),
                        prompt="จงหาค่า (ใช้ผลต่างกำลังสอง)",
                        distractors=[f"{int(v):,}".replace(",", "{,}")
                                     for v in _story.keep(base * base + d * d, base * base - d, base * base,
                                                          base * base - 2 * d * d, answer=right, lo=1)])
