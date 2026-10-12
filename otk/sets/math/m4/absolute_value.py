"""ค่าสัมบูรณ์

คณิตศาสตร์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 1 ม.4/3, ค เพิ่มเติม จำนวนและพีชคณิต 3 ม.4/3

Sets moved here from: math, math_algebra, math_bank_real, math_bank_textbook_real, math_pictures_add.
"""

from __future__ import annotations

import math
from fractions import Fraction
from functools import lru_cache
from random import Random

from otk.core.content import image, text
from otk.core.content import math as content_math
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex, poly_tex
from otk.sets._support.math_algebra import _nonzero, _signed
from otk.sets._support.math_bank_real import M4, SCAN, _agree, _count_q, _tex_q, count_integers
from otk.sets._support.math_bank_textbook_real import M4 as M4_math_bank_textbook_real
from otk.sets._support.math_bank_textbook_real import _q
from otk.sets._support.math_pictures_add import (
    ABS_GRAPHS,
    _plus,
    _shift,
)
from otk.sets._support.math_pictures_add import (
    _q as _q_math_pictures_add,
)


def _frac_q(stem: list, right: Fraction, named: list[Fraction], topic: str) -> GeneratedQuestion:
    """A rational answer with its named mistakes, padded by ±1, ±2 when they collide."""
    wrongs: list[str] = []
    for w in [*named, right + 1, right - 1, right + 2, right - 2]:
        t = frac_tex(Fraction(w))
        if t != frac_tex(right) and t not in wrongs:
            wrongs.append(t)
        if len(wrongs) == 3:
            break
    return _tex_q(stem, frac_tex(right), wrongs, topic)


def solve_abs_linear(terms: list[tuple[Fraction, Fraction, Fraction]], const: Fraction,
                     rhs: Fraction) -> list[Fraction] | None:
    """Real solutions of Σ w·|m·x + c| + const = rhs, each term (w, m, c), m ≠ 0.

    Exact: split at every breakpoint −c/m, solve the linear equation on each
    piece, keep solutions that lie in their piece. None when a whole piece
    solves it (infinitely many solutions).
    """
    cuts = sorted({-c / m for _, m, c in terms})
    pieces = [(None, cuts[0])] + list(zip(cuts, cuts[1:])) + [(cuts[-1], None)]
    found: set[Fraction] = set()
    for lo, hi in pieces:
        probe = hi - 1 if lo is None else lo + 1 if hi is None else (lo + hi) / 2
        signs = [1 if m * probe + c >= 0 else -1 for _, m, c in terms]
        slope = sum(w * m * s for (w, m, _), s in zip(terms, signs))
        inter = sum(w * c * s for (w, _, c), s in zip(terms, signs)) + const
        if slope == 0:
            if inter == rhs:
                return None
            continue
        x = (rhs - inter) / slope
        if (lo is None or x >= lo) and (hi is None or x <= hi):
            found.add(x)
    return sorted(found)


def _fmt(v: Fraction) -> str:
    return frac_tex(v)


def solve_abs_via_square(n: int) -> list[Fraction]:
    """Solutions of |x² − n| = x (x ≥ 0), from the two quadratics x² ∓ x − n = 0."""
    out = set()
    for s in (1, -1):
        disc = 1 + 4 * n
        r = math.isqrt(disc)
        if r * r != disc:
            continue
        for sign in (1, -1):
            x = Fraction(s + sign * r, 2)
            if x >= 0 and abs(x * x - n) == x:
                out.add(x)
    return sorted(out)


def _abs_family(rng: Random):
    """Like :func:`_ineq_family`, for absolute-value inequalities; None to redraw."""
    kind = rng.randrange(3)
    if kind == 0:
        k, a, m = rng.randint(2, 7), rng.randint(1, 6), rng.randint(2, 7)
        if m == k:
            return None
        tex = rf"{k}|x - {a}| < {m}x"
        pred = lambda x: k * abs(x - a) < m * x
        # Dropping the absolute value.
        mistake = lambda x: k * (x - a) < m * x and x > 0
        return tex, pred, mistake, f"{k}*Abs(x - {a}) < {m}*x"
    if kind == 1:
        a, c = rng.randint(-5, 8), rng.choice((6, 12, 20, 30, 42))
        inner = poly_tex((1, "x"), (-a, ""))
        tex = rf"({inner})^{{2}} - |{inner}| < {c}"
        pred = lambda x: (x - a) ** 2 - abs(x - a) < c
        # Treating |x − a| as x − a.
        mistake = lambda x: (x - a) ** 2 - (x - a) < c
        return tex, pred, mistake, f"(x - ({a}))**2 - Abs(x - ({a})) < {c}"
    a, b = rng.choice((2, 3)), rng.randint(-9, 9)
    c = rng.randint(3, 15)
    rel = rng.choice(("<", r"\le"))
    tex = rf"|{poly_tex((a, 'x'), (-b, ''))}| {rel} {c}"
    strict = rel == "<"
    pred = (lambda x: abs(a * x - b) < c) if strict else (lambda x: abs(a * x - b) <= c)
    # The other strictness: the endpoints wrongly kept or dropped.
    mistake = (lambda x: abs(a * x - b) <= c) if strict else (lambda x: abs(a * x - b) < c)
    return tex, pred, mistake, f"Abs({a}*x - ({b})) {'<' if strict else '<='} {c}"


_GRID = [Fraction(n, 2) for n in range(-12, 13)]


_PREMISES = (
    ("", lambda a, b: True),
    (r"ab > 0", lambda a, b: a * b > 0),
    (r"ab < 0", lambda a, b: a * b < 0),
    (r"a < 0", lambda a, b: a < 0),
)


_CLAIMS = (
    (r"|ab| = |a||b|", lambda a, b: abs(a * b) == abs(a) * abs(b)),
    (r"|a|^{2} = a^{2}", lambda a, b: abs(a) ** 2 == a * a),
    (r"|-a| = |a|", lambda a, b: abs(-a) == abs(a)),
    (r"|a + b| \le |a| + |b|", lambda a, b: abs(a + b) <= abs(a) + abs(b)),
    (r"|a - b| \ge \bigl||a| - |b|\bigr|", lambda a, b: abs(a - b) >= abs(abs(a) - abs(b))),
    (r"|a + b| = |a| + |b|", lambda a, b: abs(a + b) == abs(a) + abs(b)),
    (r"|a + b| < |a| + |b|", lambda a, b: abs(a + b) < abs(a) + abs(b)),
    (r"|a - b| \le |a| - |b|", lambda a, b: abs(a - b) <= abs(a) - abs(b)),
    (r"|a| = a", lambda a, b: abs(a) == a),
    (r"|a| = -a", lambda a, b: abs(a) == -a),
    (r"|-a|^{2} = -(a^{2})", lambda a, b: abs(-a) ** 2 == -(a * a)),
    (r"|a - b| = |b - a|", lambda a, b: abs(a - b) == abs(b - a)),
    (r"|a + b| = |a| - |b|", lambda a, b: abs(a + b) == abs(a) - abs(b)),
)


def always(premise, claim) -> bool:
    """No counterexample on a grid of halves from −6 to 6 (zero included)."""
    return all(claim(a, b) for a in _GRID for b in _GRID if premise(a, b))


@lru_cache(maxsize=None)
def _split(premise_index: int) -> tuple[list[str], list[str]]:
    """The claims that always hold under a premise, and those that may fail."""
    prem = _PREMISES[premise_index][1]
    verdict = [(t, always(prem, c)) for t, c in _CLAIMS]
    return [t for t, ok in verdict if ok], [t for t, ok in verdict if not ok]


ABS_ALT = "กราฟรูปตัววีบนระนาบพิกัดฉากที่มีเส้นตาราง"


def _abs_tex(a: int, h: int, k: int) -> str:
    coef = {1: "", -1: "-"}.get(a, str(a))
    return rf"y = {coef}\left|{_shift(h)}\right|{_plus(k)}"


@question_type("math.absolute_value_evaluate",
               display_name={"th": "ค่าของนิพจน์ที่มีค่าสัมบูรณ์"},
               level={"th": "ม.4"}, topic="ค่าสัมบูรณ์")
class AbsoluteValueEvaluate(MathType):
    def expr(self, rng: Random, value_hi: int = 12, coef_hi: int = 5):
        x = _nonzero(rng, -value_hi, value_hi)
        a, b = _nonzero(rng, -coef_hi, coef_hi), rng.randint(-9, 9)
        c = _nonzero(rng, -coef_hi, coef_hi)
        value = abs(a * x + b) + c * x
        shown = rf"\left|{poly_tex((a, 'x'), (b, ''))}\right|{_signed(c)}x"
        return MathDraw(
            shown, str(value), prompt=f"จงหาค่าของนิพจน์ เมื่อ x = {x}",
            # Dropping the bars, and taking the absolute value of the whole thing.
            distractors=[str(a * x + b + c * x), str(abs(a * x + b + c * x)),
                         str(abs(a * x) + b + c * x)])
AbsoluteValueEvaluate.PROVENANCE = Provenance("original")


@question_type("math.absolute_value_equation",
               display_name={"th": "สมการค่าสัมบูรณ์"}, level={"th": "ม.4"},
               topic="ค่าสัมบูรณ์")
class AbsoluteValueEquation(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        a, b = rng.randint(1, 10), rng.randint(1, 10)
        return MathDraw(
            rf"|x - {a}| = {b}", rf"x = {a - b},\ {a + b}", prompt="จงแก้สมการ",
            distractors=[rf"x = {a + b}", rf"x = {b - a}", rf"x = {a},\ {b}"])
AbsoluteValueEquation.PROVENANCE = Provenance("original")


@question_type("math.absolute_value_multi_equation_m4",
               display_name={"th": "สมการที่มีค่าสัมบูรณ์หลายตัว"},
               level=M4, topic="ค่าสัมบูรณ์")
class AbsoluteValueMultiEquationM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            # (|x − a| − p)(|kx − b| − q) = 0 → a ± p and (b ± q)/k.
            a, p = rng.randint(-5, 6), rng.randint(1, 4)
            k, b, q = rng.choice((1, 2, 3)), rng.randint(-4, 6), rng.randint(1, 4)
            sols = sorted({Fraction(a + p), Fraction(a - p), Fraction(b + q, k), Fraction(b - q, k)})
            right = sum(sols)
            tex = rf"(|{poly_tex((1, 'x'), (-a, ''))}| - {p})(|{poly_tex((k, 'x'), (-b, ''))}| - {q}) = 0"
            ask = "ผลบวกของคำตอบทั้งหมดของสมการ"
            # Counting only one factor's roots; the sum of the centres; one root per factor.
            wrongs = [Fraction(2 * a), Fraction(2 * a) + Fraction(2 * b, k),
                      Fraction(a + p) + Fraction(b + q, k)]
        elif kind == 1:
            # |x² − m(m + 1)| = x: only x ≥ 0 can work; the roots are m + 1 and m.
            m = rng.randint(3, 12)
            n = m * (m + 1)
            right = Fraction(2 * m + 1)
            tex = rf"|x^{{2}} - {n}| = x"
            ask = "ผลบวกของคำตอบทั้งหมดของสมการ"
            _agree(sum(solve_abs_via_square(n)), right)
            # Keeping the negative roots (they cancel to 0); one branch only (either one).
            wrongs = [Fraction(0), Fraction(m + 1), Fraction(m)]
        else:
            # |x − a| + |kx − b| = c, with a condition that keeps exactly one solution.
            while True:
                a, k, b = rng.randint(-3, 9), rng.choice((2, 3, 4)), rng.randint(1, 9)
                c = rng.randint(8, 24)
                terms = [(Fraction(1), Fraction(1), Fraction(-a)), (Fraction(1), Fraction(k), Fraction(-b))]
                sols = solve_abs_linear(terms, Fraction(0), Fraction(c))
                if sols is not None and len(sols) == 2:
                    break
            s0, s1 = sols
            between = [t for t in range(math.ceil(s0), math.floor(s1) + 1) if s0 < t < s1]
            cut = Fraction(between[len(between) // 2]) if between else (s0 + s1) / 2
            pick = rng.randrange(2)
            right = sols[pick]
            cond = rf"x < {_fmt(cut)}" if pick == 0 else rf"x > {_fmt(cut)}"
            tex = rf"|{poly_tex((1, 'x'), (-a, ''))}| + |{poly_tex((k, 'x'), (-b, ''))}| = {c}"
            # The other solution (ignoring the condition); a sign slip; the breakpoint.
            wrongs = [sols[1 - pick], -right, Fraction(b, k)]
            stem = [text("ถ้า"), content_math(cond), text("แล้วคำตอบของสมการ"), content_math(tex),
                    text("เท่ากับเท่าใด")]
            return _frac_q(stem, right, wrongs, self.topic)
        stem = [text(ask), content_math(tex), text("เท่ากับเท่าใด")]
        return _frac_q(stem, right, wrongs, self.topic)
AbsoluteValueMultiEquationM4.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/3 จำนวนจริง',))


@question_type("math.absolute_value_graph_m4",
               display_name={"th": "สมการและคำตอบจากกราฟค่าสัมบูรณ์"},
               level={"th": "ม.4"}, topic="ค่าสัมบูรณ์")
class AbsoluteValueGraphM4(QuestionType):
    break_convergence = True  # one-part slips cluster round the answer
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(ABS_GRAPHS)
        img = image(s.asset_id, alt=ABS_ALT)
        if abs(s.a) == 1 and rng.random() < 0.5:
            # Solve f(x) = c where the horizontal line meets both arms on the grid.
            d = rng.choice([d for d in (1, 2, 3) if abs(s.k + s.a * d) <= 5])
            c = s.k + s.a * d
            correct = f"x = {s.h - d} \\;,\\; x = {s.h + d}"
            wrongs = [f"x = {-s.h - d - 1} \\;,\\; x = {-s.h + d + 1}",
                      f"x = {-s.h - d} \\;,\\; x = {-s.h + d}", f"x = {s.h + d}",
                      f"x = {s.h - d - 1} \\;,\\; x = {s.h + d + 1}"]
            wrongs = [w for w in dict.fromkeys(wrongs) if w != correct]
            return _q_math_pictures_add([text("จากกราฟของ y = f(x) ในภาพ จงหาคำตอบของสมการ"),
                       content_math(f"f(x) = {c}"), img], correct, wrongs, self.topic, [])
        right = _abs_tex(s.a, s.h, s.k)
        # A two-slip wrong leads: with one-slip copies alone the answer is the
        # equation they all resemble.
        wrongs = [_abs_tex(-s.a, -s.h, s.k), _abs_tex(s.a, -s.h, s.k), _abs_tex(s.a, s.h, -s.k),
                  _abs_tex(-s.a, s.h, s.k), _abs_tex(s.a, -s.h, -s.k), _abs_tex(-s.a, s.h, -s.k)]
        return _q_math_pictures_add([text("กราฟในภาพเป็นกราฟของสมการใด"), img], right,
                  [w for w in dict.fromkeys(wrongs) if w != right], self.topic, [])
AbsoluteValueGraphM4.PROVENANCE = Provenance("original")


@question_type("math.absolute_value_inequality",
               display_name={"th": "อสมการค่าสัมบูรณ์"},
               level={"th": "ม.4"}, topic="ค่าสัมบูรณ์")
class AbsoluteValueInequality(MathType):
    def expr(self, rng: Random, shift_hi: int = 9, bound_hi: int = 12):
        b = rng.randint(-shift_hi, shift_hi)
        c = rng.randint(1, bound_hi)
        inner = poly_tex((1, "x"), (b, ""))
        if rng.random() < 0.5:
            # |x + b| < c  ⟺  −c − b < x < c − b
            return MathDraw(
                rf"\left|{inner}\right| < {c}", f"{-c - b} < x < {c - b}",
                prompt="จงหาคำตอบของอสมการ",
                distractors=[f"{c - b} < x < {-c - b}", f"x < {c - b}",
                             f"{-c + b} < x < {c + b}"])
        # |x + b| > c  ⟺  x < −c − b  or  x > c − b
        return MathDraw(
            rf"\left|{inner}\right| > {c}",
            f"x < {-c - b} \\;\\vee\\; x > {c - b}",
            prompt="จงหาคำตอบของอสมการ",
            distractors=[f"{-c - b} < x < {c - b}",
                         f"x > {c - b}",
                         f"x < {c - b} \\;\\vee\\; x > {-c - b}"])
AbsoluteValueInequality.PROVENANCE = Provenance("original")


@question_type("math.absolute_value_integer_count_m4",
               display_name={"th": "จำนวนเต็มที่สอดคล้องกับอสมการค่าสัมบูรณ์"},
               level=M4, topic="ค่าสัมบูรณ์")
class AbsoluteValueIntegerCountM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            family = _abs_family(rng)
            if family is None:
                continue
            tex, pred, mistake, _ = family
            right = count_integers(pred)
            if 2 <= right <= 60 and max(abs(x) for x in SCAN if pred(x)) < 300:
                break
        wrongs = [count_integers(mistake), right + 1, right - 1]
        stem = [text("จำนวนเต็ม x ที่สอดคล้องกับอสมการ"), content_math(tex), text("มีทั้งหมดกี่จำนวน")]
        return _count_q(stem, right, wrongs, self.topic)
AbsoluteValueIntegerCountM4.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/3 จำนวนจริง',))


@question_type("math.absolute_value_properties_m4",
               display_name={"th": "สมบัติของค่าสัมบูรณ์"},
               level=M4_math_bank_textbook_real, topic="ค่าสัมบูรณ์")
class AbsoluteValuePropertiesM4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            i = rng.randrange(len(_PREMISES))
            cond = _PREMISES[i][0]
            true, false = _split(i)
            ask_true = rng.random() < 0.6
            pool_right, pool_wrong = (list(true), list(false)) if ask_true else (list(false), list(true))
            if pool_right and len(pool_wrong) >= 3:
                break
        right = rng.choice(pool_right)
        rng.shuffle(pool_wrong)
        stem = [text("กำหนดให้ a และ b เป็นจำนวนจริง")]
        if cond:
            stem += [text("โดยที่"), content_math(cond)]
        stem.append(text("ข้อใดเป็นจริงเสมอ" if ask_true else "ข้อใดไม่จำเป็นต้องเป็นจริง"))
        return _q(stem, right, pool_wrong[:3], self.topic)
AbsoluteValuePropertiesM4.PROVENANCE = Provenance("original")
