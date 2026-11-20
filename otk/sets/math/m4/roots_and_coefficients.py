"""ความสัมพันธ์ราก-สัมประสิทธิ์

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 3 ม.4/1

Sets moved here from: math, math_algebra.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex, poly_tex
from otk.sets._support.math_algebra import _nonzero

PROVENANCE = Provenance("original")


@question_type("math.vieta",
               display_name={"th": "ความสัมพันธ์ราก-สัมประสิทธิ์"}, level={"th": "ม.4"},
               topic="ความสัมพันธ์ราก-สัมประสิทธิ์")
class Vieta(MathType):
    def expr(self, rng: Random):
        p = rng.choice([n for n in range(-6, 7) if n])
        q = rng.choice([n for n in range(-8, 9) if n])
        eq = poly_tex((1, "x^{2}"), (-p, "x"), (q, ""))
        kind = rng.choice(["sumsq", "diffsq", "prodsum", "recip"])
        if kind == "sumsq":
            expr, val = r"\alpha^{2} + \beta^{2}", rf"{p * p - 2 * q}"
        elif kind == "diffsq":
            expr, val = r"(\alpha - \beta)^{2}", rf"{p * p - 4 * q}"
        elif kind == "prodsum":
            expr, val = r"\alpha^{2}\beta + \alpha\beta^{2}", rf"{p * q}"
        else:
            expr, val = r"\frac{1}{\alpha} + \frac{1}{\beta}", frac_tex(Fraction(p, q))
        return MathDraw(rf"{eq} = 0: \quad {expr}", val,
                        hint=rf"\alpha + \beta = {p}, \; \alpha\beta = {q}",
                        prompt="ให้แอลฟาและเบตาเป็นรากของสมการ จงหาค่า")


@question_type("math.vieta_build", display_name={"th": "หาสัมประสิทธิ์จากผลบวก/ผลคูณของราก"},
               level={"th": "ม.4"}, topic="ความสัมพันธ์ราก-สัมประสิทธิ์")
class VietaBuild(MathType):
    def expr(self, rng: Random, sum_hi: int = 12, product_hi: int = 20):
        s = rng.randint(-sum_hi, sum_hi)
        p = _nonzero(rng, -product_hi, product_hi)
        return MathDraw(
            rf"r_1 + r_2 = {s}, \quad r_1 r_2 = {p}",
            poly_tex((1, "x^2"), (-s, "x"), (p, "")) + " = 0",
            prompt="สมการกำลังสองใดมีรากตามเงื่อนไขนี้",
            distractors=[poly_tex((1, "x^2"), (s, "x"), (p, "")) + " = 0",
                         poly_tex((1, "x^2"), (-s, "x"), (-p, "")) + " = 0",
                         poly_tex((1, "x^2"), (s, "x"), (-p, "")) + " = 0"])


@question_type("math.vieta_expressions",
               display_name={"th": "ค่าของนิพจน์จากผลบวกและผลคูณของราก"},
               level={"th": "ม.4"}, topic="ความสัมพันธ์ราก-สัมประสิทธิ์")
class VietaExpressions(MathType):
    """The point of Vieta: symmetric expressions in the roots, without the roots."""

    def expr(self, rng: Random, coef_hi: int = 9):
        b = _nonzero(rng, -coef_hi, coef_hi)
        c = _nonzero(rng, -coef_hi, coef_hi)
        s, p = -b, c                              # r1 + r2, r1·r2
        kind = rng.choice(["squares", "reciprocals"])
        if kind == "squares":
            ask, value = r"r_1^2 + r_2^2", s * s - 2 * p
            wrong = [str(s * s), str(s * s + 2 * p), str(s * s - p)]
        else:
            ask = r"\frac{1}{r_1} + \frac{1}{r_2}"
            value_f = Fraction(s, p)
            ask_value = frac_tex(value_f)
            return MathDraw(
                poly_tex((1, "x^2"), (b, "x"), (c, "")) + " = 0", ask_value,
                prompt=f"ถ้า r₁ และ r₂ เป็นรากของสมการนี้ จงหาค่าของ {ask}",
                distractors=[frac_tex(Fraction(p, s)), frac_tex(-value_f),
                             frac_tex(Fraction(1, p))])
        return MathDraw(
            poly_tex((1, "x^2"), (b, "x"), (c, "")) + " = 0", str(value),
            prompt=f"ถ้า r₁ และ r₂ เป็นรากของสมการนี้ จงหาค่าของ {ask}",
            distractors=wrong)


from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import question_type  # noqa: E402
from otk.kit.math_problems import MathType  # noqa: E402
from otk.sets._support.math_m4 import M4 as LEVEL  # noqa: E402


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

# ── More roots and coefficients (2026-11): the sum, the sum of squares, the gap between the roots, the other
# root, an equation with doubled roots, the sum of cubes, and α/β + β/α ──


def _sp4(rng: Random):
    s = _nz4(rng, 1, 9)
    p = _nz4(rng, 1, 15)
    return s, p, f"{poly_tex((1, 'x^{2}'), (-s, 'x'), (p, ''))} = 0"


@question_type("math.vieta_sum_m4", display_name={"th": "ผลบวกของรากจากสัมประสิทธิ์"}, level=LEVEL,
               topic="ความสัมพันธ์ราก-สัมประสิทธิ์")
class VietaSumM4(MathType):
    def expr(self, rng: Random):
        a = rng.randint(1, 4)
        b, c = rng.randint(-12, 12), _nz4(rng, 1, 12)
        right = Fraction(-b, a)
        # The sign kept; the product; b over c.
        return MathDraw(f"{poly_tex((a, 'x^{2}'), (b, 'x'), (c, ''))} = 0", frac_tex(right), prompt="ผลบวกของรากทั้งสองเท่ากับเท่าใด",
                        distractors=_fk4(Fraction(b, a), Fraction(c, a), Fraction(-c, a), right + 1, answer=right))


@question_type("math.vieta_sum_of_squares_m4", display_name={"th": "ผลบวกกำลังสองของราก"}, level=LEVEL,
               topic="ความสัมพันธ์ราก-สัมประสิทธิ์")
class VietaSumOfSquaresM4(MathType):
    def expr(self, rng: Random):
        s, p, eq = _sp4(rng)
        right = s * s - 2 * p
        # 2p added; only s squared; p taken once.
        return MathDraw(eq, str(right), prompt="ถ้า α และ β เป็นรากของสมการนี้ จงหาค่าของ α² + β²",
                        distractors=_nk4(s * s + 2 * p, s * s, s * s - p, s * s - 4 * p, answer=right))


@question_type("math.vieta_root_gap_m4", display_name={"th": "ผลต่างของรากทั้งสอง"}, level=LEVEL,
               topic="ความสัมพันธ์ราก-สัมประสิทธิ์")
class VietaRootGapM4(MathType):
    def expr(self, rng: Random):
        r1, r2 = rng.sample(range(-8, 9), 2)
        s, p = r1 + r2, r1 * r2
        right = abs(r1 - r2)
        # The square of the gap; the sum; the gap with 2p.
        return MathDraw(f"{poly_tex((1, 'x^{2}'), (-s, 'x'), (p, ''))} = 0", str(right),
                        prompt="ถ้า α และ β เป็นรากของสมการนี้ จงหาค่าของ |α − β|",
                        distractors=_nk4(right * right, abs(s), right + 2, abs(s) + right, answer=right, lo=0))


@question_type("math.vieta_other_root_m4", display_name={"th": "หารากอีกรากเมื่อรู้รากหนึ่ง"}, level=LEVEL,
               topic="ความสัมพันธ์ราก-สัมประสิทธิ์")
class VietaOtherRootM4(MathType):
    def expr(self, rng: Random):
        r1, r2 = _nz4(rng, 1, 9), _nz4(rng, 1, 9)
        p = r1 * r2
        # The sign flipped; the product; the given root.
        return MathDraw(f"x^{{2}} + bx {'+' if p > 0 else '-'} {abs(p)} = 0", str(r2),
                        prompt=f"ถ้า {r1} เป็นรากหนึ่งของสมการนี้ รากอีกรากหนึ่งเท่ากับเท่าใด",
                        distractors=_nk4(-r2, p, r1, r2 + 1, answer=r2))


@question_type("math.vieta_doubled_roots_m4", display_name={"th": "สมการที่มีรากเป็นสองเท่าของรากเดิม"}, level=LEVEL,
               topic="ความสัมพันธ์ราก-สัมประสิทธิ์")
class VietaDoubledRootsM4(MathType):
    def expr(self, rng: Random):
        s, p, eq = _sp4(rng)
        right = f"{poly_tex((1, 'x^{2}'), (-2 * s, 'x'), (4 * p, ''))} = 0"
        # The product only doubled; nothing changed; the sum's sign flipped.
        wrongs = [f"{poly_tex((1, 'x^{2}'), (-2 * s, 'x'), (2 * p, ''))} = 0", f"{poly_tex((2, 'x^{2}'), (-2 * s, 'x'), (2 * p, ''))} = 0",
                  f"{poly_tex((1, 'x^{2}'), (2 * s, 'x'), (4 * p, ''))} = 0"]
        return MathDraw(eq, right, prompt="สมการใดมีรากเป็นสองเท่าของรากของสมการนี้", distractors=_tk4(*wrongs, answer=right))


@question_type("math.vieta_sum_of_cubes_m4", display_name={"th": "ผลบวกกำลังสามของราก"}, level=LEVEL,
               topic="ความสัมพันธ์ราก-สัมประสิทธิ์")
class VietaSumOfCubesM4(MathType):
    def expr(self, rng: Random):
        s, p, eq = _sp4(rng)
        right = s ** 3 - 3 * s * p
        return MathDraw(eq, str(right), prompt="ถ้า α และ β เป็นรากของสมการนี้ จงหาค่าของ α³ + β³",
                        distractors=_nk4(s ** 3 + 3 * s * p, s ** 3, s ** 3 - p ** 3, s ** 3 - 3 * p, answer=right))


@question_type("math.vieta_ratio_sum_m4", display_name={"th": "หาค่า α/β + β/α"}, level=LEVEL,
               topic="ความสัมพันธ์ราก-สัมประสิทธิ์")
class VietaRatioSumM4(MathType):
    def expr(self, rng: Random):
        s, p, eq = _sp4(rng)
        right = Fraction(s * s - 2 * p, p)
        # The 2p left out; the product on top; one over the sum.
        return MathDraw(eq, frac_tex(right), prompt="ถ้า α และ β เป็นรากของสมการนี้ จงหาค่าของ α/β + β/α",
                        distractors=_fk4(Fraction(s * s, p), Fraction(s * s + 2 * p, p), Fraction(p, s * s - 2 * p) if s * s != 2 * p else Fraction(1, p),
                                         Fraction(s, p), answer=right))
