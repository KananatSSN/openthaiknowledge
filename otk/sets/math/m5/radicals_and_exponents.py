"""จำนวนจริงในรูปกรณฑ์และเลขยกกำลัง

คณิตศาสตร์ · ม.5 · สสวท. พื้นฐาน
Indicators: ค 1.1 ม.5/1

Sets moved here from: math_apply_stage, math_bank_powers, math_gaps_secondary.
"""

from __future__ import annotations

import math
from fractions import Fraction
from itertools import permutations
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sets._support.math_apply_stage import (
    _n,
    _nums,
    _split_square,
)
from otk.sets._support.math_apply_stage import (
    _surd as _surd_math_apply_stage,
)
from otk.sets._support.math_bank_powers import _ROOT_FACTS, M5, _tex_q
from otk.sets._support.math_gaps_secondary import _distinct, _num
from otk.sets._support.math_m4 import maths

POWERS = "จำนวนจริงในรูปกรณฑ์และเลขยกกำลัง"


def _frac_q(stem: list, right: Fraction, named: list, topic: str) -> GeneratedQuestion:
    out: list[str] = []
    for w in [*named, right + 1, right - 1, right * 2, -right]:
        t = frac_tex(Fraction(w))
        if t != frac_tex(right) and t not in out:
            out.append(t)
        if len(out) == 3:
            break
    return _tex_q(stem, frac_tex(right), out, topic)


def _pow_tex(base: int, e) -> str:
    return f"{base}^{{{e}}}"


def rational_power(sign: int, p: int, q: int, n: int, m: int) -> Fraction:
    """(sign·(p/q)ⁿ)^(m/n) — the real value, n odd when sign is negative."""
    assert sign > 0 or n % 2 == 1
    return Fraction(sign * p, q) ** m


_NAMES = ("a", "b", "c")


def order_tex(values: list[int]) -> str:
    """'c < b < a' style ordering of three distinct values named a, b, c."""
    ranked = sorted(range(3), key=lambda i: values[i])
    return " < ".join(_NAMES[i] for i in ranked)


_REAL_TOPIC = "จำนวนจริงในรูปกรณฑ์และเลขยกกำลัง"


def _surd(k: int, n: int) -> str:
    """k√n with square factors already out and 1 not written."""
    if n == 1:
        return str(k)
    return (str(k) if k != 1 else "") + rf"\sqrt{{{n}}}"


def _ftex(f: Fraction) -> str:
    return str(f.numerator) if f.denominator == 1 else rf"\frac{{{f.numerator}}}{{{f.denominator}}}"


def _xpow(f: Fraction) -> str:
    return "x" if f == 1 else rf"x^{{{_ftex(f)}}}"


@question_type("math.rational_power_evaluate_m5",
               display_name={"th": "ค่าของเลขยกกำลังตรรกยะที่มีฐานเป็นจำนวนลบหรือเศษส่วน"},
               level=M5, topic=POWERS)
class RationalPowerEvaluateM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            n = rng.choice((2, 3, 5))
            sign = -1 if n % 2 and rng.random() < 0.5 else 1
            p, q = rng.choice(((1, 2), (1, 3), (2, 3), (1, 5), (2, 1), (3, 1), (1, 4)))
            m = rng.choice([v for v in range(-3, 4) if v and v % n])
            big_p, big_q = p ** n, q ** n
            if big_p < 1000 and big_q < 1000:
                break
        right = rational_power(sign, p, q, n, m)
        base = Fraction(sign * big_p, big_q)
        base_tex = frac_tex(base) if base.denominator == 1 and base > 0 else rf"\left({frac_tex(base)}\right)"
        exp_tex = frac_tex(Fraction(m, n))
        stem = [text("ค่าของ"), content_math(rf"{base_tex}^{{{exp_tex}}}"), text("เท่ากับเท่าใด")]
        # The sign dropped; the reciprocal (negative exponent ignored); the exponent's numerator only.
        named = [abs(right), 1 / right if right else 0, Fraction(sign * p, q) ** abs(m) * (1 if m > 0 else -1)]
        return _frac_q(stem, right, named, self.topic)
RationalPowerEvaluateM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/5 เลขยกกำลัง',))


@question_type("math.radical_to_power_m5", display_name={"th": "กรณฑ์และเลขยกกำลังที่มีเลขชี้กำลังเป็นจำนวนตรรกยะ"},
               level={"th": "ม.5"}, topic=_REAL_TOPIC)
class RadicalToPowerM5(WordProblem):
    def expr(self, rng: Random):
        n = rng.choice((2, 3, 4))
        base = rng.choice((2, 3)) if n == 4 else rng.choice((2, 3, 5))
        m = rng.choice([m for m in range(1, n + 3) if math.gcd(m, n) == 1])
        a = base ** n
        value = base ** m
        if rng.random() < 0.5:
            # a^{m/n} = (ⁿ√a)^m; the slips multiply by the exponent instead.
            return MathDraw(rf"{a}^{{\frac{{{m}}}{{{n}}}}}", _num(value), prompt="จงหาค่า",
                            distractors=[_num(int(v)) for v in _story.keep(
                                a * m // n if a * m % n == 0 else a * m, a // n if a % n == 0 else a,
                                base * m, value * base, a, value + 1, value + 2, answer=value, lo=1)[:3]])
        root = r"\sqrt" + (f"[{n}]" if n != 2 else "")
        inside = f"{a}^{{{m}}}" if m > 1 else str(a)
        right = rf"{a}^{{{_ftex(Fraction(m, n))}}}"
        return MathDraw(rf"{root}{{{inside}}}", right,
                        prompt="เขียนในรูปเลขยกกำลังที่มีเลขชี้กำลังเป็นจำนวนตรรกยะ",
                        distractors=_distinct(right, rf"{a}^{{{_ftex(Fraction(n, m))}}}", rf"{a}^{{{m * n}}}",
                                              rf"{a}^{{{m + n}}}", rf"{a}^{{{m - n}}}"))
RadicalToPowerM5.PROVENANCE = Provenance("original")


@question_type("math.root_sign_properties_m5",
               display_name={"th": "เครื่องหมายของรากและรากของจำนวนลบ"},
               level=M5, topic=POWERS)
class RootSignPropertiesM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        premise, claims = rng.choice(_ROOT_FACTS)
        true = [c for c, v in claims if v]
        false = [c for c, v in claims if not v]
        ask_true = rng.random() < 0.6
        pool_right, pool_wrong = (true, false) if ask_true else (false, true)
        right = rng.choice(pool_right)
        wrongs = rng.sample(pool_wrong, 3)
        ask = "ข้อใดถูกต้อง" if ask_true else "ข้อใดไม่ถูกต้อง"
        stem = [text(f"กำหนดให้ {premise} {ask}")]
        return _tex_q(stem, right, wrongs, self.topic)
RootSignPropertiesM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/5 เลขยกกำลัง',))


@question_type("math.simplify_radicals_m5", display_name={"th": "จัดรูปจำนวนจริงในรูปกรณฑ์"},
               level={"th": "ม.5"}, topic=_REAL_TOPIC)
class SimplifyRadicalsM5(WordProblem):
    def expr(self, rng: Random):
        n = rng.choice((2, 3, 5, 6, 7))
        kind = rng.randrange(3)
        if kind == 0:        # √(k²n) = k√n
            k = rng.randint(2, 6)
            # Leaving k² outside, pulling out k without squaring, swapping k and n.
            return MathDraw(rf"\sqrt{{{k * k * n}}}", _surd(k, n), prompt="จงเขียนในรูปอย่างง่าย",
                            distractors=_distinct(_surd(k, n), _surd(k * k, n), _surd(k, k * n), _surd(n, k),
                                                  _surd(k + 1, n)))
        if kind == 1:        # a√m + b√m after simplifying each
            k1, k2 = rng.sample(range(1, 5), 2)
            tex = rf"\sqrt{{{k1 * k1 * n}}} + \sqrt{{{k2 * k2 * n}}}"
            return MathDraw(tex, _surd(k1 + k2, n), prompt="จงหาผลบวกในรูปอย่างง่าย",
                            distractors=[_surd(1, (k1 * k1 + k2 * k2) * n), _surd(k1 * k2, n),
                                         _surd(k1 + k2, 2 * n)])
        a, b = rng.randint(2, 6), n
        value = a * a - b
        return MathDraw(rf"({a} + \sqrt{{{b}}})({a} - \sqrt{{{b}}})", str(value), prompt="จงหาค่า",
                        distractors=_story.keep(a * a + b, a * a - b * b, a * a, 2 * a - b, a * a - 2 * b,
                                                answer=value, lo=-99)[:3])
SimplifyRadicalsM5.PROVENANCE = Provenance("original")


@question_type("math.rational_power_context_m5", display_name={"th": "กรณฑ์และเลขยกกำลังในสถานการณ์"},
               level={"th": "ม.5"}, topic="จำนวนจริงในรูปกรณฑ์และเลขยกกำลัง")
class RationalPowerContextM5(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            side = rng.randint(2, 12)
            vol = side ** 3
            stem = f"กล่องลูกบาศก์มีปริมาตร {_n(vol).replace('{,}', ',')} ลูกบาศก์เซนติเมตร กล่องยาวด้านละกี่เซนติเมตร (ใช้ V^(1/3))"
            return maths([text(stem)], str(side), _nums(side, vol // 3, side * side, side + 1, lo=1), self.topic)
        if kind == 1:
            m, h = rng.choice(((2, 3), (3, 2), (2, 4), (3, 3), (4, 2), (5, 2), (2, 5)))
            total = m ** h
            stem = (f"แบคทีเรียเพิ่มจำนวนเป็น {total} เท่าทุก {h} ชั่วโมง ในอัตราคงที่ "
                    f"ในหนึ่งชั่วโมงเพิ่มเป็นกี่เท่า (คือ {total}^(1/{h}))")
            return maths([text(stem)], str(m), _nums(m, round(total / h), total, m + 1, lo=1),
                         self.topic)
        while True:
            area = rng.randint(8, 200)
            k, s = _split_square(area)
            if k > 1 and s > 1:
                break
        stem = f"สนามรูปสี่เหลี่ยมจัตุรัสมีพื้นที่ {area} ตารางเมตร ยาวด้านละกี่เมตร (เขียนในรูปอย่างง่าย)"
        return maths([text(stem)], _surd_math_apply_stage(k, s), [_surd_math_apply_stage(s, k) if k != s else _surd_math_apply_stage(k + 1, s), rf"\sqrt{{{area // 2}}}",
                                                 _surd_math_apply_stage(k * k, s), str(area // 4)], self.topic)
RationalPowerContextM5.PROVENANCE = Provenance("original")


@question_type("math.power_compare_m5",
               display_name={"th": "เปรียบเทียบเลขยกกำลังที่มีค่ามาก"},
               level=M5, topic=POWERS)
class PowerCompareM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            if rng.random() < 0.6:
                g = rng.choice((5, 10, 12, 15, 20))
                picks = rng.sample(((2, 5), (3, 3), (5, 2), (2, 4), (3, 2), (7, 2), (2, 6), (11, 1),
                                    (6, 2), (4, 3), (10, 1)), 3)
                if len({b for b, _ in picks}) < 3:
                    continue                      # same base twice makes the comparison trivial
                values = [b ** (k * g) for b, k in picks]
                shown = [_pow_tex(b, k * g) for b, k in picks]
            else:
                exps = [(rng.randint(5, 15), rng.randint(5, 15)) for _ in range(3)]
                values = [2 ** x * 3 ** y for x, y in exps]
                shown = [rf"2^{{{x}}} \times 3^{{{y}}}" if x != y else _pow_tex(6, x) for x, y in exps]
            if len(set(values)) == 3:
                break
        right = order_tex(values)
        orders = [" < ".join(p) for p in permutations(_NAMES)]
        # The reversed order first (comparing bases or exponents alone often flips it).
        reverse = " < ".join(reversed(right.split(" < ")))
        rest = [o for o in orders if o not in (right, reverse)]
        rng.shuffle(rest)
        wrongs = [reverse] + rest
        stem = [text("กำหนดให้"),
                content_math(rf"a = {shown[0]},\quad b = {shown[1]},\quad c = {shown[2]}"),
                text("ข้อใดต่อไปนี้ถูกต้อง")]
        return _tex_q(stem, right, wrongs[:3], self.topic)
PowerCompareM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/5 เลขยกกำลัง',))


@question_type("math.power_laws_rational_m5", display_name={"th": "สมบัติของเลขยกกำลังที่มีเลขชี้กำลังเป็นจำนวนตรรกยะ"},
               level={"th": "ม.5"}, topic=_REAL_TOPIC)
class PowerLawsRationalM5(WordProblem):
    def expr(self, rng: Random):
        p = Fraction(rng.choice((1, 3, 5)), 2) if rng.random() < 0.5 else Fraction(rng.choice((1, 2, 4)), 3)
        q = Fraction(rng.choice((1, 2, 4, 5)), 3) if rng.random() < 0.5 else Fraction(rng.choice((1, 3, 5)), 4)
        if rng.random() < 0.5:
            value = p + q
            tex = rf"x^{{{_ftex(p)}}} \cdot x^{{{_ftex(q)}}}"
            wrongs = [p * q, p + q + 1, abs(p - q) or p + 2 * q]
        else:
            value = p * q
            tex = rf"\left(x^{{{_ftex(p)}}}\right)^{{{_ftex(q)}}}"
            wrongs = [p + q, p / q, p * q + 1]
        return MathDraw(tex, _xpow(value), prompt="จงเขียนในรูปเลขยกกำลังของ x (x > 0)",
                        distractors=[_xpow(w) for w in dict.fromkeys(wrongs) if w != value])
PowerLawsRationalM5.PROVENANCE = Provenance("original")
