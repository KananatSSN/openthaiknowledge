"""การหารพหุนาม

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 3 ม.4/1

Sets moved here from: math, math_algebra, math_bank_real, math_bank_textbook_real, math_gaps_indicators.
"""

from __future__ import annotations

import math
from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import combine, fixed, sibling_answers
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, binomial_tex, poly_tex
from otk.sets._support.math_algebra import _nonzero
from otk.sets._support.math_bank_real import M4, _agree, _count_q
from otk.sets._support.math_bank_textbook_real import (
    M4 as M4_math_bank_textbook_real,
)
from otk.sets._support.math_bank_textbook_real import (
    _q,
    ptex,
    trim,
)
from otk.sets._support.math_gaps_indicators import M4 as M4_math_gaps_indicators
from otk.sets._support.math_m4 import maths
from otk.sets._support.math_m4 import maths as _num_maths


def _minus(n: int) -> str:
    """A number for Thai text, with a true minus sign rather than a hyphen."""
    return str(n).replace("-", "−")


def _eval(coeffs: list[int], x) -> Fraction:
    """coeffs highest degree first."""
    v = Fraction(0)
    for c in coeffs:
        v = v * x + c
    return v


def _ptex(coeffs: list[int]) -> str:
    deg = len(coeffs) - 1
    syms = [f"x^{{{deg - i}}}" if deg - i > 1 else ("x" if deg - i == 1 else "") for i in range(deg + 1)]
    return poly_tex(*zip(coeffs, syms))


def solve_sum_from_roots(lead: int, roots: list[int]) -> int:
    """a + b + c for lead·x³ + ax² + bx + c with the given roots: P(1) − lead."""
    return lead * math.prod(1 - r for r in roots) - lead


def solve_odd_remainder(r_at_1: int, r_at_0: int) -> int:
    """P(−1) for P(x) = ax⁵ + bx³ + cx + d, from P(1) and P(0) = d."""
    return 2 * r_at_0 - r_at_1


def solve_quadratic_factor(s: int, t: int, k: int) -> tuple[int, int]:
    """(a, b) when x² − sx + t divides x³ + ax² + bx + k: the cofactor is x + k/t."""
    m = Fraction(k, t)
    return int(m - s), int(t - s * m)


def factorial_sum_mod(n: int, m: int, power: int = 1) -> int:
    """(1! + 2! + ⋯ + n!)^power mod m, reducing each k! mod m (k! ≡ 0 once m | k!)."""
    total, f = 0, 1
    for k in range(1, n + 1):
        f = f * k % m
        total = (total + f) % m
    return pow(total, power, m)


def power_cycle(a: int, m: int) -> list[int]:
    """Remainders a¹, a², … mod m until they first repeat: the cycle aⁿ mod m runs through."""
    seen, out, r = {}, [], a % m
    while r not in seen:
        seen[r] = len(out)
        out.append(r)
        r = r * a % m
    return out


def combined_remainder(ra: int, rb: int, rc: int, m: int) -> int:
    """a ≡ ra, b ≡ rb, c ≡ rc (mod m): the remainder of a²b + c."""
    return (ra * ra * rb + rc) % m


def padd(p: list, q: list) -> list:
    n = max(len(p), len(q))
    p, q = [0] * (n - len(p)) + list(p), [0] * (n - len(q)) + list(q)
    return trim([a + b for a, b in zip(p, q)])


def pmul(p: list, q: list) -> list:
    out = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            out[i + j] += a * b
    return trim(out)


def pdivmod(a: list, b: list) -> tuple[list, list]:
    """Long division: (q, r) with a = b·q + r and deg r < deg b."""
    a, b = [Fraction(c) for c in trim(a)], [Fraction(c) for c in trim(b)]
    if len(a) < len(b):
        return [0], trim(a)
    q = [Fraction(0)] * (len(a) - len(b) + 1)
    r = list(a)
    for i in range(len(q)):
        c = r[i] / b[0]
        q[i] = c
        for j, bj in enumerate(b):
            r[i + j] -= c * bj
    rest = trim(r[len(q):]) if len(b) > 1 else [Fraction(0)]
    norm = lambda p: [int(c) if c.denominator == 1 else c for c in p]
    return norm(trim(q)), norm(rest)


def _set(values) -> str:
    return r"\{" + ", ".join(map(str, sorted(values))) + r"\}"


@question_type("math.remainder_theorem",
               display_name={"th": "ทฤษฎีบทเศษเหลือ"}, level={"th": "ม.4"},
               topic="การหารพหุนาม")
class RemainderTheorem(MathType):
    def expr(self, rng: Random):
        a = rng.choice([n for n in range(-3, 4) if n])
        c3 = rng.randint(1, 2)
        c2, c1, c0 = (rng.randint(-5, 5) for _ in range(3))
        poly = poly_tex((c3, "x^{3}"), (c2, "x^{2}"), (c1, "x"), (c0, ""))
        rem = ((c3 * a + c2) * a + c1) * a + c0
        return MathDraw(poly, rf"{rem}", hint=rf"\text{{remainder}} = P({a})",
                        prompt=f"จงหาเศษเหลือเมื่อหารด้วย (x {'-' if a > 0 else '+'} {abs(a)})")
RemainderTheorem.PROVENANCE = Provenance("original")


@question_type("math.polynomial_division",
               display_name={"th": "การหารพหุนาม"}, level={"th": "ม.4"},
               topic="การหารพหุนาม")
class PolynomialDivision(MathType):
    """Answers read ผลหาร … เศษ …. The wrong answers flip the sign of the
    divisor's root (dividing by x − a instead of x + a), flip the remainder's
    sign, or take the last row of synthetic division without the remainder."""

    def expr(self, rng: Random):
        a = rng.choice([1, -1]) * rng.randint(1, 4)
        r = rng.choice([n for n in range(-6, 7) if n])
        if rng.random() < 0.5:
            b, c = rng.randint(-4, 4), rng.randint(-5, 5)
            coeffs = (1, a + b, a * b + c, a * c + r)
        else:
            b = rng.randint(-5, 5)
            coeffs = (1, a + b, a * b + r)
        return a, coeffs

    @staticmethod
    def _synthetic(coeffs, root):
        row = [coeffs[0]]
        for k in coeffs[1:]:
            row.append(k + row[-1] * root)
        return row[:-1], row[-1]

    @staticmethod
    def _poly(cs) -> str:
        return poly_tex(*zip(cs, ["x^{2}", "x", ""][-len(cs):]))

    def _choice(self, quotient, remainder) -> list:
        return [text("ผลหาร "), content_math(self._poly(quotient)),
                text(" เศษ "), content_math(str(remainder))]

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, coeffs = self.expr(rng)
        q, r = self._synthetic(coeffs, -a)
        q_wrong, r_wrong = self._synthetic(coeffs, a)
        wrongs = [(q_wrong, r_wrong), (q, -r), (q, 0)]

        def sample():
            a2, c2 = self.expr(rng)
            return self._choice(*self._synthetic(c2, -a2))

        dividend = poly_tex(*zip(coeffs, ["x^{3}", "x^{2}", "x", ""][-len(coeffs):]))
        return GeneratedQuestion(
            stem=[text("จงหาผลหารและเศษ"),
                  content_math(rf"({dividend}) \div {binomial_tex(a)}")],
            correct=self._choice(q, r),
            distractors=combine(fixed(*[self._choice(*w) for w in wrongs]),
                                sibling_answers(sample)),
            topic=self.topic,
        )
PolynomialDivision.PROVENANCE = Provenance("original")


@question_type("math.synthetic_division", display_name={"th": "หารสังเคราะห์"},
               level={"th": "ม.4"}, topic="การหารพหุนาม")
class SyntheticDivision(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, coef_hi: int = 6, root_hi: int = 5):
        a, b, c = (_nonzero(rng, -coef_hi, coef_hi) for _ in range(3))
        r = _nonzero(rng, -root_hi, root_hi)
        # (x − r)(ax² + bx + c) = ax³ + (b−ar)x² + (c−br)x − cr
        shown = poly_tex((a, "x^3"), (b - a * r, "x^2"), (c - b * r, "x"), (-c * r, ""))
        quotient = poly_tex((a, "x^2"), (b, "x"), (c, ""))
        return MathDraw(
            rf"\frac{{{shown}}}{{{poly_tex((1, 'x'), (-r, ''))}}}", quotient,
            prompt="จงหาผลหาร",
            distractors=[poly_tex((a, "x^2"), (-b, "x"), (c, "")),
                         poly_tex((a, "x^2"), (b, "x"), (-c, "")),
                         poly_tex((a, "x^2"), (b - a * r, "x"), (c, ""))])
SyntheticDivision.PROVENANCE = Provenance("original")


@question_type("math.polynomial_unknown_coefficients_m4",
               display_name={"th": "หาสัมประสิทธิ์ที่ไม่รู้จากเศษเหลือหรือตัวประกอบ"},
               level=M4, topic="การหารพหุนาม")
class PolynomialUnknownCoefficientsM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            lead = rng.choice((1, 2, 3))
            roots = rng.sample(range(-5, 6), 3)
            coeffs = [lead, -lead * sum(roots), lead * (roots[0] * roots[1] + roots[1] * roots[2]
                                                        + roots[0] * roots[2]), -lead * math.prod(roots)]
            right = _agree(solve_sum_from_roots(lead, roots), sum(coeffs[1:]))
            factors = ", ".join(binomial_tex(-r) for r in roots)
            stem = [text("กำหนดให้"), content_math(rf"P(x) = {lead if lead != 1 else ''}x^{{3}} + ax^{{2}} + bx + c"),
                    text("เมื่อ a, b, c เป็นจำนวนจริง ถ้า"), content_math(factors),
                    text("เป็นตัวประกอบของ P(x) แล้ว a + b + c เท่ากับเท่าใด")]
            # P(1) without subtracting the leading coefficient; P(−1) − lead; the product of roots.
            wrongs = [right + lead, int(_eval(coeffs, -1)) - lead, -math.prod(roots)]
        elif kind == 1:
            a, b, c, d = (rng.randint(-5, 5) for _ in range(4))
            coeffs = [a, 0, b, 0, c, d]
            r1, r0 = int(_eval(coeffs, 1)), d
            right = _agree(solve_odd_remainder(r1, r0), int(_eval(coeffs, -1)))
            stem = [text("กำหนดให้"), content_math(r"P(x) = ax^{5} + bx^{3} + cx + d"),
                    text(f"เมื่อ a, b, c, d เป็นค่าคงตัว ถ้า x − 1 หาร P(x) เหลือเศษ {_minus(r1)} "
                         f"และ x หาร P(x) เหลือเศษ {_minus(r0)} แล้ว x + 1 หาร P(x) เหลือเศษเท่ากับเท่าใด")]
            # −P(1) (odd without the constant); P(1) itself; ignoring d twice.
            wrongs = [-r1, r1, r0 - r1]
        else:
            s, t = rng.randint(-6, 6), rng.randint(2, 9)
            m = rng.choice([v for v in range(-6, 7) if v])
            k = t * m
            a_true, b_true = m - s, t - s * m
            a, b = _agree(solve_quadratic_factor(s, t, k), (a_true, b_true))
            right = a + b
            quad = _ptex([1, -s, t])
            stem = [text("ถ้า"), content_math(quad), text("เป็นตัวประกอบของ"),
                    content_math(rf"x^{{3}} + ax^{{2}} + bx {'+' if k >= 0 else '-'} {abs(k)}"),
                    text("โดยที่ a และ b เป็นจำนวนจริง แล้ว a + b เท่ากับเท่าใด")]
            # The cofactor's sign flipped; a − b; b alone.
            wrongs = [(-m - s) + (t + s * m), a - b, b]
        return _num_maths(stem, str(right), [str(w) for w in wrongs if w != right], self.topic)
PolynomialUnknownCoefficientsM4.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/3 จำนวนจริง',))


@question_type("math.remainder_arithmetic_m4",
               display_name={"th": "เศษเหลือจากการหารผลบวก ผลคูณ และเลขยกกำลัง"},
               level=M4, topic="การหารพหุนาม")
class RemainderArithmeticM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            m = rng.choice((5, 6, 7, 8, 9))
            n = rng.randint(m + 2, 30)
            power = rng.choice((1, 2))
            right = factorial_sum_mod(n, m, power)
            body = rf"\sum_{{k=1}}^{{{n}}} k!" if power == 1 else rf"\left(\sum_{{k=1}}^{{{n}}} k!\right)^{{2}}"
            stem = [text("เศษเหลือจากการหาร"), content_math(body), text(f"ด้วย {m} เท่ากับเท่าใด")]
            # The square forgotten (or added); only 1! + 2! + 3! kept; n itself reduced.
            wrongs = [factorial_sum_mod(n, m, 3 - power), factorial_sum_mod(3, m, power), n % m,
                      (right + 1) % m, (right + 2) % m]
            return _count_q(stem, right, wrongs, self.topic)
        if kind == 1:
            m = rng.choice((5, 7, 9, 10, 11, 13))
            a = rng.choice([x for x in range(2, 14) if math.gcd(x, m) == 1 and x % m != 1])
            n = rng.randint(50, 2030)
            cyc = power_cycle(a, m)
            right = cyc[(n - 1) % len(cyc)]
            stem = [text("เศษเหลือจากการหาร"), content_math(f"{a}^{{{n}}}"), text(f"ด้วย {m} เท่ากับเท่าใด")]
            # Counted from a⁰ instead of a¹; the exponent reduced mod m; a·n mod m.
            wrongs = [cyc[n % len(cyc)], pow(a, n % m, m), a * n % m, cyc[(n - 2) % len(cyc)]]
            return _count_q(stem, right, wrongs, self.topic)
        m = rng.choice((5, 6, 7, 8, 9, 11))
        ra, rb, rc = (rng.randint(1, m - 1) for _ in range(3))
        right = combined_remainder(ra, rb, rc, m)
        stem = [text(f"ถ้า a, b และ c เป็นจำนวนเต็มบวก ซึ่งเมื่อหารด้วย {m} เหลือเศษ {ra}, {rb} และ {rc} ตามลำดับ "
                     "แล้วเศษเหลือจากการหาร"), content_math("a^{2}b + c"), text(f"ด้วย {m} เท่ากับเท่าใด")]
        # a not squared; the sum not reduced (when it differs); c dropped.
        wrongs = [(ra * rb + rc) % m, ra * ra * rb + rc, (ra * ra * rb) % m, (right + 1) % m]
        return _count_q(stem, right, wrongs, self.topic)
RemainderArithmeticM4.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/3 จำนวนจริง',))


@question_type("math.polynomial_long_division_m4",
               display_name={"th": "หารยาวพหุนามด้วยพหุนามดีกรีสอง"},
               level=M4_math_bank_textbook_real, topic="การหารพหุนาม")
class PolynomialLongDivisionM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        while True:
            b = [1, rng.choice([v for v in range(-4, 5) if v]), rng.choice([v for v in range(-5, 6) if v])]
            q = [rng.choice((1, 2, 3))] + [rng.randint(-4, 4) for _ in range(rng.choice((1, 2)))]
            r = [rng.randint(-6, 6), rng.randint(-9, 9)]
            a = padd(pmul(b, q), r)
            if trim(r) == [0] or 0 not in a[1:]:
                continue                 # the dropped-terms mistake needs a missing term
            if pdivmod(a, b) != (trim(q), trim(r)):     # pragma: no cover
                raise AssertionError("long division disagrees with the construction")
            # Real divisions that a slip produces: the missing terms dropped from
            # the dividend; the divisor's lower signs flipped (adding instead of
            # subtracting); the divisor's constant term forgotten.
            slips = [pdivmod([c for c in a if c], b), pdivmod(a, [b[0], -b[1], -b[2]]),
                     pdivmod(a, [b[0], b[1], 0])]
            part = 0 if kind == 0 else 1
            answer = (q, r)[part]
            wrongs = [ptex(s[part]) for s in slips]
            if kind == 2 or len({*wrongs} - {ptex(answer)}) == 3:
                break
        a_t, b_t = ptex(a), ptex(b)
        if kind < 2:
            ask = "ผลหาร" if kind == 0 else "เศษเหลือ"
            stem = [text(f"{ask}จากการหาร"), content_math(a_t), text("ด้วย"), content_math(b_t),
                    text("คือข้อใด")]
            right = ptex(answer)
        else:
            stem = [text("พหุนามที่หารด้วย"), content_math(b_t), text("แล้วได้ผลหาร"), content_math(ptex(q)),
                    text("และเศษเหลือ"), content_math(ptex(r)), text("คือข้อใด")]
            right = a_t
            # b·q − r; b·q alone; b·r + q (the roles swapped).
            wrongs = [ptex(padd(pmul(b, q), [-c for c in r])), ptex(pmul(b, q)), ptex(padd(pmul(b, r), q))]
        return _q(stem, right, wrongs, self.topic)
PolynomialLongDivisionM4.PROVENANCE = Provenance("original")


@question_type("math.polynomial_equation_m4", display_name={"th": "แก้สมการพหุนามดีกรีสามและดีกรีสี่"},
               level=M4_math_gaps_indicators, topic="การหารพหุนาม")
class PolynomialEquationM4(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            # (x − p)(x − q)(x − r) expanded: guess a root from the factors of
            # the constant, divide, and factor the quadratic left over.
            p, q, r = rng.sample([n for n in range(-5, 6) if n], 3)
            poly = poly_tex((1, "x^{3}"), (-(p + q + r), "x^{2}"), (p * q + q * r + r * p, "x"), (-p * q * r, ""))
            roots = {p, q, r}
            wrongs = [_set({-p, -q, -r}), _set({p, q}), _set({-p, q, r}), _set({p, -q, -r}),
                      _set({p, -q, r}), _set({p, q, -r}), _set({q, r}), _set({p, r})]
        else:
            # x⁴ − (a² + b²)x² + a²b² = (x² − a²)(x² − b²): four roots ±a, ±b.
            a, b = rng.sample(range(1, 6), 2)
            poly = poly_tex((1, "x^{4}"), (-(a * a + b * b), "x^{2}"), (a * a * b * b, ""))
            roots = {a, -a, b, -b}
            wrongs = [_set({a, b}), _set({a * a, b * b}), _set({-a, -b}), _set({a * a, -a * a, b * b, -b * b})]
        return maths([text("จงหาเซตคำตอบของสมการ"), content_math(f"{poly} = 0")], _set(roots), wrongs, self.topic)
PolynomialEquationM4.PROVENANCE = Provenance("original")


@question_type("math.polynomial_inequality_m4", display_name={"th": "แก้อสมการพหุนามดีกรีสาม"},
               level=M4_math_gaps_indicators, topic="การหารพหุนาม")
class PolynomialInequalityM4(QuestionType):
    """(x − p)(x − q)(x − r) compared with 0: the sign changes at each root,
    and is positive to the right of the largest."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        p, q, r = sorted(rng.sample(range(-6, 7), 3))
        op = rng.choice((">", "<", r"\geq", r"\leq"))
        closed = op in (r"\geq", r"\leq")
        up = op in (">", r"\geq")

        def region(positive: bool, shut: bool) -> str:
            lo, hi = ("[", "]") if shut else ("(", ")")
            if positive:
                return rf"{lo}{p}, {q}{hi} \cup {lo}{r}, \infty)"
            return rf"(-\infty, {p}{hi} \cup {lo}{q}, {r}{hi}"

        right = region(up, closed)
        lo, hi = ("[", "]") if closed else ("(", ")")
        # The other sign; the roots kept or dropped wrongly; and the quadratic
        # habit of reading only the outer roots.
        wrongs = [region(not up, closed), region(up, not closed),
                  rf"{lo}{p}, {r}{hi}" if not up else rf"(-\infty, {p}{hi} \cup {lo}{r}, \infty)"]
        factors = "".join(binomial_tex(-n) if n else "x" for n in (p, q, r))
        return maths([text("จงหาเซตคำตอบของอสมการ"), content_math(f"{factors} {op} 0")], right,
                     [w for w in wrongs if w != right], self.topic)
PolynomialInequalityM4.PROVENANCE = Provenance("original")
