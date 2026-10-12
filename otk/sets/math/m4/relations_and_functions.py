"""ความสัมพันธ์และฟังก์ชัน

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 2 ม.4/2

Sets moved here from: math, math_algebra, math_bank_functions, math_gaps_indicators, math_m4.
"""

from __future__ import annotations

import math
from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import ChoiceType, MathDraw, MathType, WordProblem, frac_tex, poly_tex
from otk.sets._support.math_algebra import _nonzero
from otk.sets._support.math_bank_functions import M4, _frac_q, _minus, _tex_q
from otk.sets._support.math_gaps_indicators import M4 as M4_math_gaps_indicators
from otk.sets._support.math_gaps_indicators import _nz
from otk.sets._support.math_m4 import M4 as M4_math_m4
from otk.sets._support.math_m4 import maths
from otk.sets._support.math_m4 import maths as _num_maths

RELATION = "ความสัมพันธ์และฟังก์ชัน"


def _rational_sqrt(q: Fraction):
    n, d = math.isqrt(q.numerator), math.isqrt(q.denominator)
    if n * n == q.numerator and d * d == q.denominator:
        return Fraction(n, d)
    return None


class Piecewise:
    """f(x) = m·x + p for x < c, and a·(x − c)² + d for x ≥ c."""

    def __init__(self, m: int, p: int, c: int, a: int, d: int):
        self.m, self.p, self.c, self.a, self.d = m, p, c, a, d

    def __call__(self, x) -> Fraction:
        x = Fraction(x)
        if x < self.c:
            return self.m * x + self.p
        return self.a * (x - self.c) ** 2 + self.d

    def solve(self, k) -> list[Fraction]:
        """Every real x with f(x) = k, piece by piece, kept only inside its piece."""
        k = Fraction(k)
        out = []
        if self.m:
            x = (k - self.p) / self.m
            if x < self.c:
                out.append(x)
        sq = (k - self.d) / self.a
        if sq >= 0:
            r = _rational_sqrt(sq)
            if r is not None:
                for x in {self.c + r, self.c - r}:
                    if x >= self.c:
                        out.append(x)
        return sorted(set(out))

    def tex(self) -> str:
        left = poly_tex((self.m, "x"), (self.p, ""))
        square = "x^{2}" if self.c == 0 else \
            rf"(x {'-' if self.c > 0 else '+'} {abs(self.c)})^{{2}}"
        right = f"{'' if self.a == 1 else self.a}{square}"
        right += f" {'+' if self.d >= 0 else '-'} {abs(self.d)}" if self.d else ""
        return (rf"f(x) = \begin{{cases}} {left} & , x < {self.c} \\ "
                rf"{right} & , x \ge {self.c} \end{{cases}}")


def _random_piecewise(rng: Random) -> Piecewise:
    return Piecewise(rng.choice((1, 2, -1, 3)), rng.randint(-3, 6), rng.randint(-1, 3),
                     rng.choice((1, 2, 4)), rng.randint(-2, 5))


def line_over_abs(k: int, p: int, q: int) -> tuple[Fraction, Fraction]:
    """(a, b) with |x| + k ≤ ax + b exactly on [p, q], p < 0 < q: both ends are
    intersection points, so −p + k = ap + b and q + k = aq + b."""
    a = Fraction(q + p, q - p)
    return a, q + k - a * q


def parabolas_meeting(h: int, top: int, s: int) -> tuple[Fraction, Fraction]:
    """(α, β) for f = αx² (vertex at the origin) and g = β(x − h)² + top, with
    f ≤ g exactly on [0, s]: g(0) = 0 fixes β, and f(s) = g(s) fixes α."""
    beta = Fraction(-top, h * h)
    alpha = (beta * (s - h) ** 2 + top) / (s * s)
    return alpha, beta


def count_relation(lo: int, hi: int, shift: int, div: int) -> int:
    """|{(x, y) ∈ A × A | y = (x − shift)/div}| for A = {lo, …, hi}."""
    A = range(lo, hi + 1)
    return sum(1 for x in A if (x - shift) % div == 0 and lo <= (x - shift) // div <= hi)


_FN_TOPIC = "ความสัมพันธ์และฟังก์ชัน"


@question_type("math.is_function", display_name={"th": "ความสัมพันธ์ใดเป็นฟังก์ชัน"},
               level={"th": "ม.4"}, topic="ความสัมพันธ์และฟังก์ชัน")
class IsFunction(ChoiceType):
    def compose(self, rng: Random):
        xs = rng.sample(range(1, 9), 3)
        ys = [rng.randint(1, 9) for _ in range(3)]
        good = "{" + ", ".join(f"({x}, {y})" for x, y in zip(xs, ys)) + "}"
        # One x repeated with two different images breaks the definition.
        bad = ("{" + f"({xs[0]}, {ys[0]}), ({xs[0]}, {ys[0] + 1}), "
               f"({xs[1]}, {ys[1]})" + "}")
        if rng.random() < 0.5:
            return (f"ความสัมพันธ์ {good} เป็นฟังก์ชันหรือไม่", "เป็นฟังก์ชัน เพราะไม่มีโดเมนซ้ำ",
                    ["ไม่เป็นฟังก์ชัน เพราะมีโดเมนซ้ำ",
                     "ไม่เป็นฟังก์ชัน เพราะมีเรนจ์ซ้ำ",
                     "ไม่เป็นฟังก์ชัน เพราะมีสมาชิกไม่ครบ"])
        return (f"ความสัมพันธ์ {bad} เป็นฟังก์ชันหรือไม่",
                "ไม่เป็นฟังก์ชัน เพราะมีโดเมนซ้ำ",
                ["เป็นฟังก์ชัน เพราะไม่มีโดเมนซ้ำ", "ไม่เป็นฟังก์ชัน เพราะมีเรนจ์ซ้ำ",
                 "ไม่เป็นฟังก์ชัน เพราะมีสมาชิกไม่ครบ"])
IsFunction.PROVENANCE = Provenance("original")


@question_type("math.function_domain",
               display_name={"th": "โดเมนของฟังก์ชัน"}, level={"th": "ม.4"},
               topic="ความสัมพันธ์และฟังก์ชัน")
class FunctionDomain(MathType):
    def expr(self, rng: Random):
        a = rng.choice([n for n in range(-6, 7) if n])
        sign = "-" if a >= 0 else "+"
        if rng.random() < 0.5:
            fx = rf"f(x) = \frac{{1}}{{x {sign} {abs(a)}}}"
            ans, wrong = rf"x \neq {a}", [rf"x = {a}", rf"x > {a}", rf"x < {a}"]
        else:
            fx = rf"f(x) = \sqrt{{x {sign} {abs(a)}}}"
            ans, wrong = rf"x \geq {a}", [rf"x > {a}", rf"x \leq {a}", rf"x < {a}"]
        return MathDraw(fx, ans, prompt="โดเมนของฟังก์ชันนี้คือข้อใด",
                        distractors=wrong)
FunctionDomain.PROVENANCE = Provenance("original")


@question_type("math.piecewise_function_m4",
               display_name={"th": "ฟังก์ชันที่นิยามเป็นช่วงและฟังก์ชันขั้นบันได"},
               level=M4, topic=RELATION)
class PiecewiseFunctionM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(5)
        if kind in (0, 1, 2):
            while True:
                f = _random_piecewise(rng)
                if kind == 0:
                    u, v = f.c - rng.randint(1, 6), f.c + rng.randint(0, 4)
                    right = f(u) + f(v)
                    ask = rf"f({u}) + f({v})"
                    # Each value through the other piece.
                    swapped = (f.a * (u - f.c) ** 2 + f.d) + (f.m * v + f.p)
                    named = [swapped, f(u) - f(v), 2 * f(v)]
                    stem = [text("กำหนดให้"), content_math(f.tex()), text("ค่าของ"),
                            content_math(ask), text("เท่ากับเท่าใด")]
                    return _frac_q(stem, right, named, self.topic)
                if kind == 1:
                    k = rng.randint(f.d + 1, f.d + 40)
                    sols = f.solve(k)
                    if len(sols) == 2:
                        right = sum(sols)
                        # Keeping every root of both pieces, not just those in range.
                        every = [(Fraction(k) - f.p) / f.m] if f.m else []
                        r = _rational_sqrt((Fraction(k) - f.d) / f.a)
                        every += [f.c + r, f.c - r] if r is not None else []
                        named = [sum(every), max(sols), min(sols)]
                        stem = [text("กำหนดให้"), content_math(f.tex()),
                                text(f"ถ้า S = {{ a | f(a) = {_minus(k)} }} แล้วผลบวกของสมาชิกทั้งหมดใน S เท่ากับเท่าใด")]
                        return _frac_q(stem, right, named, self.topic)
                    continue
                # f(f(t)) = k with exactly one t.
                t = Fraction(rng.randint(-6, 6))
                k = f(f(t))
                inner = f.solve(k)
                ts = sorted({s for u in inner for s in f.solve(u)})
                if ts == [t]:
                    stem = [text("กำหนดให้"), content_math(f.tex()),
                            text(f"ถ้า f(f(c)) = {_minus(k)} แล้ว c มีค่าเท่าใด")]
                    # Solving f(c) = k (one layer only); the inner value; its sign flipped.
                    one = f.solve(k)
                    named = [one[0] if one else -t, inner[0], -t]
                    return _frac_q(stem, t, named, self.topic)
        if kind == 3:
            # Tiered pricing applied to the whole purchase.
            p1, p2 = rng.choice(((200, 150), (120, 100), (90, 75), (60, 50)))
            limit = rng.choice((50, 100, 120))
            n1, n2 = rng.randint(10, limit), rng.randint(limit + 1, limit + 80)
            right = p1 * n1 + p2 * n2
            stem = [text(f"ร้านค้าแห่งหนึ่งขายเสื้อตามฟังก์ชัน f(x) = {p1}x เมื่อ x ≤ {limit} "
                         f"และ f(x) = {p2}x เมื่อ x > {limit} (บาท) เมื่อ x คือจำนวนเสื้อที่ซื้อในครั้งเดียว "
                         f"ถ้าซื้อครั้งแรก {n1} ตัว และครั้งที่สอง {n2} ตัว จ่ายเงินทั้งหมดกี่บาท")]
            # One price for the combined purchase; each purchase at the other price.
            total = n1 + n2
            named = [p2 * total, p1 * total, p2 * n1 + p1 * n2]
            return _num_maths(stem, str(right), [str(w) for w in named if w != right], self.topic)
        # A step function: the first h hours cost X; each further hour started costs Y.
        h, first, extra = rng.choice((1, 2, 3)), rng.choice((20, 30, 40)), rng.choice((10, 15, 20))
        t = Fraction(rng.randint(h * 2 + 1, h * 2 + 18), 2)                  # half hours
        right = first + extra * math.ceil(t - h) if t > h else first
        stem = [text(f"อาคารจอดรถคิดค่าบริการ {h} ชั่วโมงแรก {first} บาท ชั่วโมงต่อไปคิดชั่วโมงละ {extra} บาท "
                     f"(เศษของชั่วโมงคิดเป็นหนึ่งชั่วโมง) ถ้าจอดรถนาน {frac_tex(t) if t.denominator == 1 else str(float(t))} ชั่วโมง "
                     f"ต้องจ่ายค่าจอดรถกี่บาท")]
        # Rounding down; charging every hour at the extra rate; forgetting the first block.
        named = [first + extra * math.floor(t - h), extra * math.ceil(t), extra * math.ceil(t - h)]
        return _num_maths(stem, str(right), [str(w) for w in named if w != right], self.topic)
PiecewiseFunctionM4.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/4 ฟังก์ชัน',))


@question_type("math.relation_pairs_m4",
               display_name={"th": "ความสัมพันธ์ในรูปเซตของคู่อันดับและบริเวณบนระนาบ"},
               level=M4, topic=RELATION)
class RelationPairsM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            while True:
                lo, hi = rng.randint(1, 6), rng.randint(12, 20)
                shift, div = rng.randint(0, 3), rng.choice((2, 3))
                right = count_relation(lo, hi, shift, div)
                if right >= 1:
                    break
            stem = [text(f"ถ้า A = {{{lo}, {lo + 1}, …, {hi}}} และ"),
                    content_math(rf"r = \{{ (x, y) \in A \times A \mid y = \frac{{x - {shift}}}{{{div}}} \}}"
                                 if shift else rf"r = \{{ (x, y) \in A \times A \mid y = \frac{{x}}{{{div}}} \}}"),
                    text("แล้ว r มีสมาชิกทั้งหมดกี่ตัว")]
            # Forgetting y must be in A; counting every x in A; forgetting y must be whole.
            whole = sum(1 for x in range(lo, hi + 1) if (x - shift) % div == 0)
            return _num_maths(stem, str(right),
                              [str(w) for w in (whole, hi - lo + 1, right + 1) if w != right], self.topic)
        if kind == 1:
            k = rng.choice((2, 3))
            a = rng.choice([v for v in range(-4, 5) if v not in (0, 1, -1)])
            right = (k * a, a * a)
            # Forgetting the factor k; squaring the first entry; swapping; halving the square.
            candidates = [(a, a * a), (k * a, k * a * a), (a * a, k * a), (k * a, a), (-k * a, -a * a),
                          (k * a, a * a + 1)]
            member = lambda pr: Fraction(pr[1]) == Fraction(pr[0], k) ** 2
            wrongs = [w for w in dict.fromkeys(candidates) if not member(w)][:3]
            fmt = lambda pr: f"({pr[0]}, {pr[1]})"
            stem = [text("กำหนดให้"), content_math(rf"r = \{{ ({k}a, a^{{2}}) \mid a \in \mathbb{{R}} \}}"),
                    text("คู่อันดับในข้อใดเป็นสมาชิกของ r")]
            return _tex_q(stem, fmt(right), [fmt(w) for w in wrongs], self.topic)
        # s ≥ u + v + 3 keeps a lattice point (u + 1, v + 1) inside the region.
        u, v = rng.randint(0, 2), rng.randint(0, 2)
        s = rng.randint(u + v + 3, u + v + 6)
        inside = lambda x, y: x + y < s and x > u and y > v
        while True:
            pts = [(rng.randint(-1, 7), rng.randint(-1, 7)) for _ in range(12)]
            good = [p for p in pts if inside(*p)]
            bad = list(dict.fromkeys(p for p in pts if not inside(*p)))
            if good and len(bad) >= 3:
                break
        stem = [text("กำหนดให้"),
                content_math(rf"r = \{{ (x, y) \mid x + y < {s},\ x > {u},\ y > {v} \}}"),
                text("จุดในข้อใดอยู่ในความสัมพันธ์ r")]
        fmt = lambda p: f"({p[0]}, {p[1]})"
        return _tex_q(stem, fmt(good[0]), [fmt(p) for p in bad[:3]], self.topic)
RelationPairsM4.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/4 ฟังก์ชัน',))


@question_type("math.function_arithmetic_m4", display_name={"th": "การบวก ลบ คูณ และหารฟังก์ชัน"},
               level=M4_math_gaps_indicators, topic="ความสัมพันธ์และฟังก์ชัน")
class FunctionArithmeticM4(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, b = _nz(rng, -5, 5), rng.randint(-9, 9)
        c, d = _nz(rng, -3, 3), rng.randint(-9, 9)
        f = lambda x: a * x + b          # noqa: E731
        g = lambda x: c * x * x + d      # noqa: E731
        while True:
            k = rng.randint(-4, 4)
            if g(k) and f(k) and f(k) != g(k):
                break
        op = rng.choice(("+", "-", r"\cdot", "/"))
        fk, gk = f(k), g(k)
        if op == "+":
            right, name = Fraction(fk + gk), "(f + g)"
            wrongs = [Fraction(fk - gk), Fraction(fk * gk), Fraction(f(gk))]
        elif op == "-":
            right, name = Fraction(fk - gk), "(f - g)"
            wrongs = [Fraction(gk - fk), Fraction(fk + gk), Fraction(f(gk))]
        elif op == r"\cdot":
            # f(g(k)) is the composite, the mistake this set is here to catch.
            right, name = Fraction(fk * gk), r"(f \cdot g)"
            wrongs = [Fraction(f(gk)), Fraction(fk + gk), Fraction(g(fk))]
        else:
            right, name = Fraction(fk, gk), r"\left(\frac{f}{g}\right)"
            wrongs = [Fraction(gk, fk), Fraction(f(gk)), Fraction(fk - gk)]
        stem = [text("กำหนดให้"), content_math(rf"f(x) = {poly_tex((a, 'x'), (b, ''))}"), text("และ"),
                content_math(rf"g(x) = {poly_tex((c, 'x^{2}'), (d, ''))}"), text("จงหาค่าของ"),
                content_math(rf"{name}({k})")]
        wrongs += [-right, right + 1, right - 1]
        return maths(stem, frac_tex(right), [frac_tex(w) for w in wrongs], self.topic)
FunctionArithmeticM4.PROVENANCE = Provenance("original")


@question_type("math.exponential_function_m4",
               display_name={"th": "ฟังก์ชันเอกซ์โพเนนเชียล: ค่า การเพิ่ม และการลด"},
               level=M4_math_m4, topic=_FN_TOPIC)
class ExponentialFunctionM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            a, b, x = rng.randint(1, 5), rng.choice((2, 3, 4, 5)), rng.randint(0, 4)
            v = a * b ** x
            return maths([text(f"จงหาค่าของ f({x})"),
                           content_math(rf"f(x) = {a} \cdot {b}^{{x}}")], str(v),
                          [str(a * b * x), str((a * b) ** x), str(a + b ** x), str(v * b),
                           str(v + a), str(v + 1)],
                          self.topic)
        if kind == 1:
            inc = [r"y = 3^{x}", r"y = \left(\tfrac{5}{2}\right)^{x}", r"y = 2^{x}", r"y = (1.5)^{x}"]
            dec = [r"y = \left(\tfrac{1}{2}\right)^{x}", r"y = (0.8)^{x}", r"y = \left(\tfrac{2}{3}\right)^{x}",
                   r"y = 3^{-x}"]
            want_inc = rng.random() < 0.5
            good, bad = (inc, dec) if want_inc else (dec, inc)
            return maths([text(f"ฟังก์ชันใดเป็นฟังก์ชัน{'เพิ่ม' if want_inc else 'ลด'}")],
                          rng.choice(good), rng.sample(bad, 3), self.topic)
        b = rng.choice((2, 3, 4, 5, 9, 10))
        return maths([text("กราฟของฟังก์ชันนี้ตัดแกน Y ที่จุดใด"), content_math(rf"y = {b}^{{x}}")],
                      "(0, 1)", ["(0, 0)", f"(0, {b})", f"(1, {b})", "(1, 0)"], self.topic)
ExponentialFunctionM4.PROVENANCE = Provenance("original")


@question_type("math.function_range_linear",
               display_name={"th": "เรนจ์ของฟังก์ชันเชิงเส้นบนช่วงปิด"},
               level={"th": "ม.4"}, topic="ความสัมพันธ์และฟังก์ชัน")
class FunctionRangeLinear(MathType):
    def expr(self, rng: Random, slope_hi: int = 6, bound_hi: int = 8):
        m = _nonzero(rng, -slope_hi, slope_hi)
        b = rng.randint(-10, 10)
        lo, hi = sorted(rng.sample(range(-bound_hi, bound_hi + 1), 2))
        ends = sorted((m * lo + b, m * hi + b))
        return MathDraw(
            rf"f(x) = {poly_tex((m, 'x'), (b, ''))}, \quad {lo} \le x \le {hi}",
            f"[{ends[0]}, {ends[1]}]", prompt="จงหาเรนจ์ของฟังก์ชัน",
            # A negative slope reverses the endpoints — the trap here.
            distractors=[f"[{m * lo + b}, {m * hi + b}]", f"[{lo}, {hi}]",
                         f"[{ends[0] - 1}, {ends[1] + 1}]"])
FunctionRangeLinear.PROVENANCE = Provenance("original")


@question_type("math.graph_inequality_parameters_m4",
               display_name={"th": "หาค่าคงตัวจากเซตคำตอบของ f(x) ≤ g(x)"},
               level=M4, topic=RELATION)
class GraphInequalityParametersM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.55:
            while True:
                k, p, q = rng.randint(1, 9), -rng.randint(2, 12), rng.randint(2, 16)
                if p + q != 0:
                    break
            a, b = line_over_abs(k, p, q)
            right = a + b
            stem = [text("กำหนดให้"), content_math(rf"f(x) = |x| + {k}"), text("และ"),
                    content_math(r"g(x) = ax + b"),
                    text("เมื่อ a, b เป็นจำนวนจริง ถ้าเซตคำตอบของอสมการ f(x) ≤ g(x) คือช่วงปิด"),
                    content_math(f"[{p}, {q}]"), text("แล้ว a + b เท่ากับเท่าใด")]
            # Using −p as if |p| were p; slope as (q − p)/(q + p); b alone.
            a_wrong = Fraction(q - p, q + p) if q + p else a + 1
            named = [a_wrong + (q + k - a_wrong * q), b, a + b + k]
            return _frac_q(stem, right, named, self.topic)
        while True:
            h, top, s = rng.choice((1, 2)), rng.randint(2, 8), rng.choice((1, 2, 3))
            alpha, beta = parabolas_meeting(h, top, s)
            if alpha > 0 and alpha > beta:          # f − g opens upward: f ≤ g between the roots
                break
        t = rng.choice((-2, -1, 1, 2)) if s > 1 else rng.choice((-2, -1, 2))
        f_t, g_t = alpha * t * t, beta * (t - h) ** 2 + top
        right = f_t + g_t
        stem = [text(f"กำหนดให้กราฟของ y = f(x) เป็นพาราโบลาที่มีจุดยอดที่ (0, 0) และกราฟของ y = g(x) "
                     f"เป็นพาราโบลาที่มีจุดยอดที่ ({h}, {top}) ถ้าเซตคำตอบของอสมการ f(x) ≤ g(x) คือช่วงปิด "
                     f"[0, {s}] แล้ว f({_minus(t)}) + g({_minus(t)}) มีค่าเท่ากับเท่าใด")]
        named = [f_t - g_t, g_t, alpha * t * t + beta * (t + h) ** 2 + top]
        return _frac_q(stem, right, named, self.topic)
GraphInequalityParametersM4.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/4 ฟังก์ชัน',))


@question_type("math.cost_revenue_function_m4",
               display_name={"th": "ฟังก์ชันเชิงเส้นในชีวิตจริง: ต้นทุน รายได้ กำไร"},
               level=M4_math_m4, topic=_FN_TOPIC)
class CostRevenueFunctionM4(WordProblem):
    _GOODS = ("เสื้อยืดสกรีนลาย", "ขนมปังโฮมเมด", "สบู่ทำมือ", "พวงกุญแจ", "กระเป๋าผ้า")

    def expr(self, rng: Random):
        goods = rng.choice(self._GOODS)
        v = rng.randint(10, 60)
        p = v + rng.randint(5, 40)
        q = rng.randint(20, 300)
        fixed = (p - v) * q
        head = (f"ร้านหนึ่งผลิต{goods} มีต้นทุนคงที่ {fixed:,} บาท และต้นทุนชิ้นละ {v} บาท "
                f"ขายชิ้นละ {p} บาท")
        kind = rng.randrange(3)
        if kind == 0:
            return MathDraw("", str(q), prompt=f"{head} ต้องขายกี่ชิ้นจึงจะคุ้มทุนพอดี",
                            # Dividing by the price, or by the cost, instead of the margin.
                            distractors=_story.keep(fixed // p if fixed % p == 0 else q - 1,
                                                    fixed // v if fixed % v == 0 else q + 10,
                                                    q + 1, answer=q, lo=1))
        sold = q + rng.randint(10, 200)
        profit = (p - v) * sold - fixed
        if kind == 1:
            return MathDraw("", f"{profit:,}".replace(",", "{,}"),
                            prompt=f"{head} ถ้าขายได้ {sold} ชิ้น จะได้กำไรกี่บาท",
                            distractors=[f"{(p - v) * sold:,}".replace(",", "{,}"),
                                         f"{p * sold - fixed:,}".replace(",", "{,}"),
                                         f"{profit + fixed // 2:,}".replace(",", "{,}")])
        rule = rf"P(x) = {p - v}x - {fixed}"
        return MathDraw(rule, str(q), prompt=f"กำไร (บาท) จากการขาย{goods} x ชิ้น เป็นไปตามฟังก์ชันนี้ "
                                              f"ต้องขายอย่างน้อยกี่ชิ้นจึงจะไม่ขาดทุน",
                        distractors=_story.keep(q - 1, q + 1, fixed, answer=q, lo=1))
CostRevenueFunctionM4.PROVENANCE = Provenance("original")
