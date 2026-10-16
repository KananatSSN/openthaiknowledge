"""ลอการิทึม

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 2 ม.4/3, ค เพิ่มเติม จำนวนและพีชคณิต 3 ม.4/4

Sets moved here from: math, math_algebra, math_bank_logs, math_chapters, math_m4, math_pictures_add.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import image, text
from otk.core.content import math as content_math
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex, poly_tex
from otk.sets._support.math_chapters import _lin
from otk.sets._support.math_m4 import maths
from otk.sets._support.math_m4 import maths as _num_maths
from otk.sets._support.math_p2 import _maths
from otk.sets._support.math_pictures_add import EXP_LOG_GRAPHS, _plus, _q

M5 = {"th": "ม.5"}


TOPIC = "ลอการิทึม"


def _tex_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    """Named mistakes first; duplicates and the answer itself dropped; three kept."""
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right][:3]
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


def _frac_q(stem: list, right: Fraction, named: list, topic: str) -> GeneratedQuestion:
    out: list[str] = []
    for w in [*named, right + 1, right - 1, right * 2, right / 2]:
        t = frac_tex(Fraction(w))
        if t != frac_tex(right) and t not in out:
            out.append(t)
        if len(out) == 3:
            break
    return _tex_q(stem, frac_tex(right), out, topic)


def difference_with_squared_base(p: int, k: int, c: int) -> int:
    """log_p(pᵏ·c) − log_(p²)(c²) = k: the second term is log_p c."""
    return k


def reciprocal_sum(a: int, b: int, q: int) -> Fraction:
    """1/log_a N + 1/log_b N with N = (ab)^q: log_N(ab) = 1/q."""
    return Fraction(1, q)


def swapped_power_bases(m: int, n: int, v: int) -> Fraction:
    """log_(bⁿ) a when log_(aᵐ) b = v: log_a b = mv, so the answer is 1/(n·m·v)."""
    return Fraction(1, n * m * v)


def power_of_ten_solutions(m: int, n: int) -> list[int]:
    """x with 9^(log x) − (3^m + 3^n)·3^(log x) + 3^(m+n) = 0: log x ∈ {m, n}."""
    return sorted({10 ** m, 10 ** n})


def self_power_product(b: int, k: int, j: int) -> Fraction:
    """Product of the solutions of x^(log_b x) = bᵏ·xʲ: t² − jt − k = 0, so bᵗ¹·bᵗ² = bʲ."""
    return Fraction(b) ** j


def same_argument_inequality(base_below_one: bool, c: int) -> tuple[Fraction, Fraction | None]:
    """log_a(x − c) < log_(aᵏ)(x − c), k > 1: with t = log_a(x − c), t < t/k ⇔ t < 0.

    t < 0 means x − c > 1 when a < 1, and 0 < x − c < 1 when a > 1.
    Returns (low, high) of the open solution interval, high None for ∞.
    """
    if base_below_one:
        return Fraction(c + 1), None
    return Fraction(c), Fraction(c + 1)


def linear_log_inequality(a: Fraction, p: int, q: int, r: int, s: int
                          ) -> tuple[Fraction, Fraction | None] | None:
    """log_a(px + q) > log_a(rx + s) with p, r > 0: the open interval of solutions, or None.

    Domain: x > −q/p and x > −s/r. Compare px + q with rx + s, flipping for a < 1.
    """
    lo = max(Fraction(-q, p), Fraction(-s, r))
    if p == r:
        holds = q > s if a > 1 else q < s          # equal arguments never satisfy ">"
        return (lo, None) if holds else None
    t = Fraction(s - q, p - r)
    upward = (p - r > 0) == (a > 1)                  # px + q > rx + s ⇔ x > t (after any flips)
    if upward:
        return (max(lo, t), None)
    return (lo, t) if t > lo else None


def interval_tex(iv: tuple[Fraction, Fraction | None]) -> str:
    lo, hi = iv
    return rf"({frac_tex(lo)}, \infty)" if hi is None else rf"({frac_tex(lo)}, {frac_tex(hi)})"


_DECREASING = (r"y = \left(\frac{1}{2}\right)^{x}", r"y = \left(\frac{2}{3}\right)^{x}", r"y = (0.4)^{x}",
               r"y = \log_{\frac{1}{2}} x", r"y = \log_{0.1} x")


_INCREASING = (r"y = 2^{x}", r"y = \left(\frac{3}{2}\right)^{x}", r"y = 10^{x}", r"y = \log_{3} x",
               r"y = \log x", r"y = \log_{5} x")


EXP_ALT = "กราฟเส้นโค้งบนระนาบพิกัดฉากที่มีเส้นตาราง มีจุดทึบบนกราฟ"


def _base_tex(b: Fraction) -> str:
    return str(b.numerator) if b.denominator == 1 else rf"\frac{{1}}{{{b.denominator}}}"


def _exp_log_tex(kind: str, b: Fraction, k: int) -> str:
    if kind == "exp":
        power = f"{b.numerator}^{{x}}" if b.denominator == 1 else rf"\left(\frac{{1}}{{{b.denominator}}}\right)^{{x}}"
        return f"y = {power}{_plus(k)}"
    return rf"y = \log_{{{_base_tex(b)}}} x{_plus(k)}"


@question_type("math.logarithm",
               display_name={"th": "ลอการิทึม: หาค่า / แก้สมการ"}, level={"th": "ม.5"}, topic="ลอการิทึม")
class Logarithm(MathType):
    def expr(self, rng: Random):
        b = rng.choice([2, 3, 5, 10])
        k = rng.randint(0, 5 if b == 2 else 3)
        if rng.random() < 0.5:
            return MathDraw(rf"\log_{{{b}}} {b ** k}", rf"{k}",
                            hint=rf"{b ** k} = {b}^{{{k}}}", topic="ลอการิทึม",
                            prompt="จงหาค่า")
        k = max(1, k)
        c = rng.randint(-5, 5)
        x = b ** k - c
        arg = "x" if c == 0 else f"x {'+' if c > 0 else '-'} {abs(c)}"
        hint = (rf"x {'+' if c > 0 else '-'} {abs(c)} = {b}^{{{k}}}" if c
                else rf"x = {b}^{{{k}}}")
        return MathDraw(rf"\log_{{{b}}}({arg}) = {k}", rf"x = {x}", hint=hint,
                        topic="สมการลอการิทึม", prompt="จงแก้สมการ")
Logarithm.PROVENANCE = Provenance("original")


@question_type("math.log_change_of_base", display_name={"th": "ลอการิทึม: หาค่าโดยตรง"},
               level={"th": "ม.5"}, topic="ลอการิทึม")
class LogDirect(MathType):
    def expr(self, rng: Random, base_lo: int = 2, base_hi: int = 6,
             exp_hi: int = 5):
        b = rng.randint(base_lo, base_hi)
        e = rng.randint(1, exp_hi)
        return MathDraw(
            rf"\log_{{{b}}} {b ** e}", str(e), prompt="จงหาค่า",
            distractors=[str(b ** e), str(b * e), str(e + 1)])
LogDirect.PROVENANCE = Provenance("original")


@question_type("math.log_laws", display_name={"th": "กฎของลอการิทึม"},
               level={"th": "ม.5"}, topic="ลอการิทึม")
class LogLaws(MathType):
    """log turns products into sums — the property the whole tool exists for."""

    def expr(self, rng: Random, base_lo: int = 2, base_hi: int = 5,
             exp_hi: int = 5):
        b = rng.randint(base_lo, base_hi)
        m, n = rng.randint(1, exp_hi), rng.randint(1, exp_hi)
        if rng.random() < 0.5:
            shown = rf"\log_{{{b}}}({b ** m} \cdot {b ** n})"
            answer, wrong = m + n, [m * n, abs(m - n), b ** (m + n)]
        else:
            shown = rf"\log_{{{b}}}\left(\frac{{{b ** (m + n)}}}{{{b ** n}}}\right)"
            answer, wrong = m, [m + n, n, Fraction(m + n, n)]
        return MathDraw(shown, str(answer), prompt="จงหาค่า",
                        distractors=[str(w) for w in wrong])
LogLaws.PROVENANCE = Provenance("original")


@question_type("math.log_mixed_bases_m5",
               display_name={"th": "ค่าของนิพจน์ลอการิทึมต่างฐาน"},
               level=M5, topic=TOPIC)
class LogMixedBasesM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        if kind == 0:
            p, k = rng.choice((2, 3)), rng.randint(1, 4)
            c = rng.choice([v for v in (5, 7, 10, 11) if v % p])
            right = Fraction(difference_with_squared_base(p, k, c))
            stem = [text("ค่าของ"),
                    content_math(rf"\log_{{{p}}} {p ** k * c} - \log_{{{p * p}}} {c * c}"),
                    text("เท่ากับเท่าใด")]
            # Near misses around the power: log_(p²) read as log_p takes one too many off;
            # halving everything; one too many.
            named = [Fraction(k - 1), Fraction(k, 2), Fraction(k + 1)]
            return _frac_q(stem, right, named, self.topic)
        if kind == 1:
            a, b = rng.sample((2, 3, 5, 7), 2)
            q = rng.choice((1, 2, 3))
            N = (a * b) ** q
            right = reciprocal_sum(a, b, q)
            stem = [text("ค่าของ"),
                    content_math(rf"\frac{{1}}{{\log_{{{a}}} {N}}} + \frac{{1}}{{\log_{{{b}}} {N}}}"),
                    text("เท่ากับเท่าใด")]
            # log_(ab) N instead of its reciprocal; a + b over N; 1/(2q).
            named = [Fraction(q), Fraction(a + b, N), Fraction(1, 2 * q)]
            return _frac_q(stem, right, named, self.topic)
        if kind == 2:
            m, n, v = rng.choice((2, 3)), rng.choice((2, 3)), rng.randint(2, 6)
            right = swapped_power_bases(m, n, v)
            stem = [text("กำหนดให้ a และ b เป็นจำนวนจริงบวกที่ไม่เท่ากับ 1 ถ้า"),
                    content_math(rf"\log_{{a^{{{m}}}}} b = {v}"),
                    text("แล้ว"), content_math(rf"\log_{{b^{{{n}}}}} a"), text("เท่ากับเท่าใด")]
            # Forgetting one exponent; multiplying instead of dividing; the plain reciprocal.
            named = [Fraction(1, m * v), Fraction(n, m * v), Fraction(1, v)]
            return _frac_q(stem, right, named, self.topic)
        # log(log bᵏ) − log(log bʲ) = log x → x = k / j.
        b, j = rng.choice((2, 3, 5)), rng.randint(1, 3)
        k = j * rng.randint(2, 5)
        right = Fraction(k, j)
        stem = [text("ถ้า"), content_math(rf"\log(\log {b ** k}) - \log(\log {b ** j}) = \log x"),
                text("แล้ว x เท่ากับเท่าใด")]
        # Subtracting inside (log bᵏ − log bʲ); k − j; the powers' ratio.
        named = [Fraction(k - j), Fraction(k - j, j), Fraction(b ** (k - j))]
        return _frac_q(stem, right, named, self.topic)
LogMixedBasesM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/6 เอกโพเนนเชียล และ ลอการิทึม',))


@question_type("math.exp_log_graph_m4",
               display_name={"th": "กราฟของฟังก์ชันเอกซ์โพเนนเชียลและฟังก์ชันลอการิทึม"},
               level=M5, topic="ลอการิทึม")
class ExpLogGraphM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(5)
        a = rng.choice((2, 3, 4, 5))
        k = rng.choice([v for v in range(-5, 6) if v not in (0, -1)])
        tail = f" + {k}" if k > 0 else f" - {-k}"
        if kind == 0:
            right = f"(0, {1 + k})"
            # a⁰ taken as 0, as a, and the point put on the x-axis.
            wrongs = [f"(0, {k})", f"(0, {a + k})", f"({1 + k}, 0)"]
            return _maths([text("กราฟของ"), content_math(f"y = {a}^{{x}}{tail}"), text("ตัดแกน Y ที่จุดใด")],
                          right, wrongs, self.topic)
        if kind == 1:
            right = f"y = {k}"
            wrongs = ["y = 0", f"x = {k}", f"y = {1 + k}"]
            return _maths([text("เส้นกำกับแนวนอนของกราฟ"), content_math(f"y = {a}^{{x}}{tail}"),
                           text("คือเส้นใด")], right, wrongs, self.topic)
        if kind == 2:
            if rng.random() < 0.5:
                right, wrongs, ask = rng.choice(_DECREASING), rng.sample(_INCREASING, 3), "ฟังก์ชันลด"
            else:
                right, wrongs, ask = rng.choice(_INCREASING), rng.sample(_DECREASING, 3), "ฟังก์ชันเพิ่ม"
            return _maths([text(f"ฟังก์ชันใดเป็น{ask}")], right, wrongs, self.topic)
        if kind == 3:
            h = rng.choice([v for v in range(-6, 7) if v])
            right = rf"({h}, \infty)"
            wrongs = [rf"[{h}, \infty)", rf"({-h}, \infty)", rf"(-\infty, {h})"]
            return _maths([text("โดเมนของฟังก์ชัน"), content_math(rf"y = \log_{{{a}}} ({_lin(1, -h)})"),
                           text("คือช่วงใด")], right, wrongs, self.topic)
        a, k = rng.choice(((2, 3), (2, 4), (3, 2), (3, 3), (5, 2), (10, 2), (10, 3)))
        right = f"({a ** k}, {k})"
        # The point of the exponential graph instead, a·k for aᵏ, one too high.
        wrongs = [f"({k}, {a ** k})", f"({a * k}, {k})", f"({a ** k}, {k + 1})"]
        log = r"\log x" if a == 10 else rf"\log_{{{a}}} x"
        return _maths([text("จุดใดอยู่บนกราฟของ"), content_math(f"y = {log}")], right, wrongs, self.topic)
ExpLogGraphM4.PROVENANCE = Provenance("original")


@question_type("math.exp_log_graph_picture_m4",
               display_name={"th": "ระบุฟังก์ชันเอกซ์โพเนนเชียลหรือลอการิทึมจากกราฟ"},
               level={"th": "ม.4"}, topic="ลอการิทึม")
class ExpLogGraphPictureM4(QuestionType):
    break_convergence = True  # one-part slips cluster round the answer
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(EXP_LOG_GRAPHS)
        other = "log" if s.kind == "exp" else "exp"
        wrongs = [_exp_log_tex(other, s.base, -s.k if s.k else 1),
                  _exp_log_tex(s.kind, 1 / s.base, s.k), _exp_log_tex(other, s.base, s.k),
                  _exp_log_tex(s.kind, s.base, -s.k if s.k else 1),
                  _exp_log_tex(other, 1 / s.base, s.k),
                  _exp_log_tex(s.kind, 1 / s.base, -s.k if s.k else 1)]
        wrongs = [w for w in dict.fromkeys(wrongs) if w != _exp_log_tex(*s)]
        return _q([text("กราฟในภาพเป็นกราฟของฟังก์ชันใด"), image(s.asset_id, alt=EXP_ALT)],
                  _exp_log_tex(*s), wrongs, self.topic, [])
ExpLogGraphPictureM4.PROVENANCE = Provenance("original")


@question_type("math.log_equation", display_name={"th": "สมการลอการิทึม"},
               level={"th": "ม.5"}, topic="ลอการิทึม")
class LogEquation(MathType):
    def expr(self, rng: Random, base_lo: int = 2, base_hi: int = 5,
             exp_hi: int = 4):
        b = rng.randint(base_lo, base_hi)
        e = rng.randint(1, exp_hi)
        c = rng.randint(-8, 8)
        # log_b(x + c) = e  ⟹  x = b^e − c
        x = b ** e - c
        return MathDraw(
            rf"\log_{{{b}}}({poly_tex((1, 'x'), (c, ''))}) = {e}", f"x = {x}",
            prompt="จงแก้สมการ",
            distractors=[f"x = {b ** e + c}", f"x = {b * e - c}",
                         f"x = {e - c}"])
LogEquation.PROVENANCE = Provenance("original")


@question_type("math.log_equation_advanced_m5",
               display_name={"th": "สมการลอการิทึมรูปแบบซับซ้อน"},
               level=M5, topic=TOPIC)
class LogEquationAdvancedM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            m, n = sorted(rng.sample(range(0, 4), 2))
            sols = power_of_ten_solutions(m, n)
            right = sum(sols)
            stem = [text("ผลบวกของคำตอบของสมการ"),
                    content_math(rf"9^{{\log x}} - {3 ** m + 3 ** n}\left(3^{{\log x}}\right) + {3 ** (m + n)} = 0"),
                    text("เท่ากับเท่าใด")]
            # Stopping at log x (m + n); stopping at 3^(log x); 10^(m + n).
            return _num_maths(stem, str(right), [str(m + n), str(3 ** m + 3 ** n), str(10 ** (m + n))],
                              self.topic)
        if kind == 1:
            # (log x)² − s·log x + p = 0 with integer roots r1, r2.
            r1, r2 = sorted(rng.sample(range(-2, 4), 2))
            s, p = r1 + r2, r1 * r2
            right = Fraction(10) ** r1 + Fraction(10) ** r2
            lin = f"{'-' if s > 0 else '+'} {'' if abs(s) == 1 else abs(s)}\\log x" if s else ""
            const = f"{'+' if p >= 0 else '-'} {abs(p)}" if p else ""
            stem = [text("ผลบวกของคำตอบทั้งหมดของสมการ"),
                    content_math(rf"(\log x)^{{2}} {lin} {const} = 0".replace("  ", " ")),
                    text("เท่ากับเท่าใด")]
            # The sum of log x; 10^(sum); the product of the solutions.
            named = [Fraction(s), Fraction(10) ** s, Fraction(10) ** (r1 + r2)]
            return _frac_q(stem, right, named, self.topic)
        b = rng.choice((2, 3, 5))
        while True:
            j, k = rng.randint(1, 4), rng.randint(1, 8)
            if j * j + 4 * k > 0:
                break
        right = self_power_product(b, k, j)
        stem = [text("กำหนดให้ x > 0 และ x ≠ 1 ผลคูณของคำตอบทั้งหมดของสมการ"),
                content_math(rf"x^{{\log_{{{b}}} x}} = {b ** k} x^{{{j}}}"), text("เท่ากับเท่าใด")]
        # b^k (the constant); b^(−k); b^(j + k).
        named = [Fraction(b) ** k, Fraction(b) ** -k, Fraction(b) ** (j + k)]
        return _frac_q(stem, right, named, self.topic)
LogEquationAdvancedM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/6 เอกโพเนนเชียล และ ลอการิทึม',))


@question_type("math.log_inequality_m5",
               display_name={"th": "อสมการลอการิทึม"},
               level=M5, topic=TOPIC)
class LogInequalityM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.5:
            below = rng.random() < 0.5
            c = rng.randint(-3, 5)
            base, k = rng.choice(((Fraction(1, 10), 2), (Fraction(1, 2), 3), (Fraction(1, 3), 2))) if below \
                else rng.choice(((Fraction(2), 3), (Fraction(3), 2), (Fraction(10), 2)))
            iv = same_argument_inequality(below, c)
            other = same_argument_inequality(not below, c)
            arg = f"x {'-' if c >= 0 else '+'} {abs(c)}" if c else "x"
            b1, b2 = base, base ** k
            stem = [text("เซตคำตอบของอสมการ"),
                    content_math(rf"\log_{{{frac_tex(b1)}}}({arg}) < \log_{{{frac_tex(b2)}}}({arg})"),
                    text("คือเซตในข้อใด")]
            # The base's side flipped; forgetting the domain x > c; the reversed half.
            wrongs = [interval_tex(other), interval_tex((Fraction(c - 1), None)),
                      rf"(-\infty, {frac_tex(Fraction(c + 1))})"]
            return _tex_q(stem, interval_tex(iv), wrongs, self.topic)
        while True:
            a = rng.choice((Fraction(2), Fraction(3), Fraction(1, 2), Fraction(1, 3)))
            p, r = rng.randint(1, 4), rng.randint(1, 4)
            q, s = rng.randint(-6, 6), rng.randint(-6, 6)
            iv = linear_log_inequality(a, p, q, r, s)
            flipped = linear_log_inequality(1 / a, p, q, r, s)
            if iv is not None and flipped is not None and iv != flipped and p != r:
                break
        lin = lambda k, c: f"{'' if k == 1 else k}x {'+' if c >= 0 else '-'} {abs(c)}" if c else \
            f"{'' if k == 1 else k}x"
        stem = [text("เซตคำตอบของอสมการ"),
                content_math(rf"\log_{{{frac_tex(a)}}}({lin(p, q)}) > \log_{{{frac_tex(a)}}}({lin(r, s)})"),
                text("คือเซตในข้อใด")]
        t = Fraction(s - q, p - r)
        # The inequality not flipped (or wrongly flipped); ignoring the domain.
        lo = max(Fraction(-q, p), Fraction(-s, r))
        wrongs = [interval_tex(flipped), rf"({frac_tex(t)}, \infty)", rf"(-\infty, {frac_tex(t)})",
                  rf"({frac_tex(lo)}, \infty)", rf"({frac_tex(t - 1)}, \infty)", rf"(-\infty, {frac_tex(lo)})"]
        return _tex_q(stem, interval_tex(iv), wrongs, self.topic)
LogInequalityM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/6 เอกโพเนนเชียล และ ลอการิทึม',))


@question_type("math.logarithm_application_m4",
               display_name={"th": "การประยุกต์ลอการิทึม (pH เดซิเบล ขนาดแผ่นดินไหว)"},
               level=M5, topic="ลอการิทึม")
class LogarithmApplicationM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        if kind == 0:
            k = rng.randint(2, 12)
            return maths([text("สารละลายมีความเข้มข้นของไฮโดรเจนไอออน"),
                           content_math(rf"[H^{{+}}] = 10^{{-{k}}}"),
                           text("โมลต่อลิตร ถ้า"), content_math(r"\text{pH} = -\log [H^{+}]"),
                           text("สารละลายนี้มี pH เท่าใด")], str(k),
                          [str(-k), str(10 - k) if 10 - k != k else str(k + 1), str(k + 1), str(14 - k)
                           if 14 - k != k else str(k - 1)], self.topic)
        if kind == 1:
            d = rng.randint(1, 4)
            return maths([text(f"แผ่นดินไหวครั้งแรกมีขนาด {5 + d} ริกเตอร์ ครั้งที่สองมีขนาด 5 ริกเตอร์ "
                                f"ถ้าขนาดเพิ่มขึ้น 1 ริกเตอร์ แอมพลิจูดเพิ่มขึ้น 10 เท่า ครั้งแรกมีแอมพลิจูดกี่เท่า"
                                f"ของครั้งที่สอง")], f"{10 ** d:,}".replace(",", "{,}"),
                          [str(10 * d), str(d + 1), f"{10 ** (d + 1):,}".replace(",", "{,}"), str(d)],
                          self.topic)
        if kind == 2:
            k = rng.randint(2, 9)
            return maths([text("เสียงมีความเข้มเป็น"), content_math(rf"\frac{{I}}{{I_0}} = 10^{{{k}}}"),
                           text("ถ้าระดับเสียง"), content_math(r"\beta = 10 \log \frac{I}{I_0}"),
                           text("เดซิเบล เสียงนี้ดังกี่เดซิเบล")], str(10 * k),
                          [str(k), str(10 ** k) if k < 4 else str(100 * k), str(10 * k + 10),
                           str(10 + k)], self.topic)
        r = rng.choice((2, 3, 5))
        n = rng.randint(2, 6)
        big = r ** n
        return maths([text(f"เงินฝากเพิ่มเป็น {r} เท่าทุก 10 ปี ต้องใช้เวลากี่ปีเงินจึงเพิ่มเป็น {big:,} เท่า"),
                       content_math(rf"\log_{{{r}}} {big} = {n}")], str(10 * n),
                      [str(n), str(10 * big // r), str(10 * (n + 1)), str(big)], self.topic)
LogarithmApplicationM4.PROVENANCE = Provenance("original")
