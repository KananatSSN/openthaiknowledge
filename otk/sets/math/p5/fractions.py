"""เศษส่วน

คณิตศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.5/*

Sets moved here from: math, math_apply_basic, math_number.
"""

from __future__ import annotations

import math
import math as _math
from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import REGISTRY, question_type
from otk.kit import story as _story
from otk.kit.math_problems import (
    MathDraw,
    MathType,
    WordProblem,
    _as_draw,
    frac_answer_tex,
    frac_tex,
    proper,
    rand_proper,
)
from otk.sets._support.math_apply_add import _c, _fr

PROVENANCE = Provenance("original")


_SIMPLE_FRACTIONS = [
    (1, 2), (1, 3), (2, 3), (1, 4), (3, 4),
    (1, 5), (2, 5), (3, 5), (4, 5), (1, 6), (5, 6),
    (1, 7), (2, 7), (3, 7), (4, 7), (1, 8), (3, 8), (5, 8), (7, 8),
    (1, 9), (2, 9), (4, 9), (5, 9), (7, 9),
]


@question_type("math.reduce_fraction",
               display_name={"th": "เศษส่วนอย่างต่ำ"}, level={"th": "ป.5"},
               topic="เศษส่วน")
class ReduceFraction(MathType):
    def expr(self, rng: Random, k_lo: int = 2, k_hi: int = 8):
        p, q = rng.choice(_SIMPLE_FRACTIONS)
        k = rng.randint(k_lo, k_hi)
        return MathDraw(rf"\frac{{{p * k}}}{{{q * k}}}", rf"\frac{{{p}}}{{{q}}}",
                        hint=rf"\text{{GCD}} = {k}", prompt="จงทำให้เป็นรูปอย่างง่าย")


@question_type("math.order_fractions",
               display_name={"th": "เรียงลำดับเศษส่วน"}, level={"th": "ป.5"},
               topic="เศษส่วน")
class OrderFractions(MathType):
    def expr(self, rng: Random):
        while True:
            fs = [Fraction(rng.randint(1, 5), rng.randint(2, 6)) for _ in range(3)]
            if len(set(fs)) == 3:
                break
        asc = rng.random() < 0.5
        mode = "จากน้อยไปมาก" if asc else "จากมากไปน้อย"
        ordered = sorted(fs, reverse=not asc)
        # Never show the fractions already in the order asked for.
        while fs == ordered:
            fs = rng.sample(fs, 3)
        tex = lambda seq: r",\ ".join(frac_tex(f) for f in seq)
        distractors = [
            tex(sorted(fs, reverse=asc)),
            tex([ordered[1], ordered[0], ordered[2]]),
            tex([ordered[0], ordered[2], ordered[1]]),
        ]
        return MathDraw(tex(fs), tex(ordered), prompt=f"จงเรียง{mode}",
                        distractors=distractors)


@question_type("math.improper_to_mixed", display_name={"th": "เศษเกินเป็นจำนวนคละ"},
               level={"th": "ป.5"}, topic="เศษส่วน")
class ImproperToMixed(MathType):
    def expr(self, rng: Random, whole_hi: int = 6, den_hi: int = 9):
        q = rng.randint(2, den_hi)
        whole = rng.randint(1, whole_hi)
        # The หัวข้อ is เศษส่วนอย่างต่ำ, so the fractional part must already be in
        # lowest terms — otherwise the "answer" needs another step to be right.
        r = rng.choice([k for k in range(1, q) if _math.gcd(k, q) == 1])
        p = whole * q + r
        return MathDraw(rf"\frac{{{p}}}{{{q}}}",
                        rf"{whole}\frac{{{r}}}{{{q}}}",
                        prompt="เขียนเศษเกินนี้ในรูปจำนวนคละ",
                        distractors=[rf"{r}\frac{{{whole}}}{{{q}}}",
                                     rf"{whole + 1}\frac{{{r}}}{{{q}}}",
                                     rf"{whole}\frac{{{q - r}}}{{{q}}}"])


@question_type("math.add_fractions",
               display_name={"th": "บวกเศษส่วน"}, level={"th": "ป.5"},
               topic="เศษส่วน")
class AddFractions(MathType):
    def expr(self, rng: Random, den_hi: int = 20, like: int = 0):
        den_hi = max(3, int(den_hi))
        while True:
            f1 = rand_proper(rng, 2, den_hi)
            f2 = proper(rng, f1.denominator) if like else rand_proper(rng, 2, den_hi)
            lcd = math.lcm(f1.denominator, f2.denominator)
            if like or (f1.denominator != f2.denominator and lcd <= 48):
                break
        return MathDraw(rf"{frac_tex(f1)} + {frac_tex(f2)}",
                        frac_answer_tex(f1 + f2), hint=rf"\text{{LCD}} = {lcd}")


@question_type("math.sub_fractions",
               display_name={"th": "ลบเศษส่วน"}, level={"th": "ป.5"},
               topic="เศษส่วน")
class SubFractions(MathType):
    def expr(self, rng: Random, den_hi: int = 20):
        den_hi = max(3, int(den_hi))
        while True:
            f1, f2 = rand_proper(rng, 2, den_hi), rand_proper(rng, 2, den_hi)
            lcd = math.lcm(f1.denominator, f2.denominator)
            if f1 != f2 and f1.denominator != f2.denominator and lcd <= 48:
                break
        if f1 < f2:
            f1, f2 = f2, f1
        return MathDraw(rf"{frac_tex(f1)} - {frac_tex(f2)}",
                        frac_answer_tex(f1 - f2), hint=rf"\text{{LCD}} = {lcd}")


@question_type("math.add_mixed_numbers", display_name={"th": "บวกจำนวนคละ"},
               level={"th": "ป.5"}, topic="เศษส่วน")
class AddMixedNumbers(MathType):
    def expr(self, rng: Random, whole_hi: int = 5, den_hi: int = 8):
        qa, qb = rng.randint(2, den_hi), rng.randint(2, den_hi)
        wa, wb = rng.randint(1, whole_hi), rng.randint(1, whole_hi)
        fa = Fraction(rng.randint(1, qa - 1), qa)
        fb = Fraction(rng.randint(1, qb - 1), qb)
        a, b = wa + fa, wb + fb
        total = a + b
        whole, rem = divmod(total.numerator, total.denominator)
        answer = (str(whole) if rem == 0
                  else rf"{whole}\frac{{{rem}}}{{{total.denominator}}}")
        shown = (rf"{wa}\frac{{{fa.numerator}}}{{{fa.denominator}}} + "
                 rf"{wb}\frac{{{fb.numerator}}}{{{fb.denominator}}}")
        # The classic slip: add the wholes, then add numerators and denominators.
        slip = Fraction(fa.numerator + fb.numerator, fa.denominator + fb.denominator)
        return MathDraw(shown, answer, prompt="จงหาผลบวก",
                        distractors=[rf"{wa + wb}\frac{{{slip.numerator}}}"
                                     rf"{{{slip.denominator}}}",
                                     frac_tex(total),
                                     rf"{wa + wb}\frac{{{fa.numerator}}}"
                                     rf"{{{fa.denominator}}}"])


@question_type("math.mul_fractions",
               display_name={"th": "คูณเศษส่วน"}, level={"th": "ป.5"},
               topic="เศษส่วน")
class MulFractions(MathType):
    def expr(self, rng: Random, cancel: int = 1):
        while True:
            a, b = rng.randint(1, 9), rng.randint(2, 12)
            c, d = rng.randint(1, 9), rng.randint(2, 12)
            if a >= b or c >= d:
                continue
            if math.gcd(a, b) != 1 or math.gcd(c, d) != 1:
                continue
            if cancel and math.gcd(a, d) == 1 and math.gcd(c, b) == 1:
                continue
            result = Fraction(a, b) * Fraction(c, d)
            if result.denominator <= 30:
                break
        return MathDraw(rf"\frac{{{a}}}{{{b}}} \times \frac{{{c}}}{{{d}}}",
                        frac_answer_tex(result),
                        hint=r"\text{cancel before multiplying}")


@question_type("math.div_fractions",
               display_name={"th": "หารเศษส่วน"}, level={"th": "ป.5"},
               topic="เศษส่วน")
class DivFractions(MathType):
    def expr(self, rng: Random, den_hi: int = 9):
        while True:
            f1, f2 = rand_proper(rng, 2, den_hi), rand_proper(rng, 2, den_hi)
            result = f1 / f2
            if f1 != f2 and result.denominator <= 24 and abs(result.numerator) <= 24:
                break
        return MathDraw(rf"{frac_tex(f1)} \div {frac_tex(f2)}",
                        frac_answer_tex(result),
                        hint=r"\div \tfrac{a}{b} \;=\; \times \tfrac{b}{a}")


@question_type("math.mixed_fractions",
               display_name={"th": "เศษส่วน: สี่การดำเนินการ (สุ่ม)"},
               level={"th": "ป.5"}, topic="เศษส่วน")
class MixedFractionOps(MathType):
    def expr(self, rng: Random, den_hi: int = 12):
        make = rng.choice([
            lambda: REGISTRY["math.add_fractions"].expr(rng, den_hi=den_hi),
            lambda: REGISTRY["math.sub_fractions"].expr(rng, den_hi=den_hi),
            lambda: REGISTRY["math.mul_fractions"].expr(rng),
            lambda: REGISTRY["math.div_fractions"].expr(rng),
        ])
        d = _as_draw(make())
        return MathDraw(d.problem_tex, d.answer_tex, topic="เศษส่วนระคน", hint=d.hint)


@question_type("math.fraction_remaining_p5",
               display_name={"th": "โจทย์ปัญหาเศษส่วนของส่วนที่เหลือ"},
               level={"th": "ป.5"}, topic="เศษส่วน")
class FractionRemainingP5(WordProblem):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        kind = rng.randrange(5)
        a, b = rng.choice(((3, 2), (4, 3), (5, 2), (3, 4), (4, 5), (5, 3)))
        if kind == 0:
            m = a * b * rng.randint(2, 12) * 10
            after = m - m // a
            left = after - after // b
            return MathDraw("", _c(left),
                            prompt=(f"{p}มีเงิน {_c(m)} บาท ใช้ซื้อหนังสือ 1/{a} ของเงินที่มี แล้วใช้ซื้อขนม "
                                    f"1/{b} ของเงินที่เหลือ {p}เหลือเงินกี่บาท"),
                            distractors=[_c(m - m // a - m // b), _c(after), _c(m // a + m // b)])
        if kind == 1:
            L = 5 * 2 * rng.randint(2, 15)
            rest = L - 2 * L // 5
            left = rest // 2
            return MathDraw("", str(left),
                            prompt=(f"เชือกยาว {L} เมตร ตัดออกไป 2/5 ของความยาวทั้งหมด แล้วตัดออกอีกครึ่งหนึ่งของส่วนที่เหลือ "
                                    f"เชือกเหลือยาวกี่เมตร"),
                            distractors=_story.keep(L - 2 * L // 5 - L // 2, rest, L // 10, answer=left, lo=1))
        if kind == 2:
            n, m = rng.choice(((4, 6), (4, 10), (6, 9), (8, 12), (6, 15)))
            num, den = rng.choice(((3, 4), (2, 3), (1, 2), (5, 6)))
            need = Fraction(num, den) * m / n
            return MathDraw("", _fr(need),
                            prompt=(f"สูตรขนมสำหรับ {n} คน ใช้แป้ง {num}/{den} ถ้วย ถ้าทำให้ {m} คน ต้องใช้แป้งกี่ถ้วย"),
                            distractors=[_fr(Fraction(num, den) * n / m), _fr(Fraction(num * m, den)),
                                         _fr(Fraction(num, den) + m - n)])
        if kind == 3:
            cap = 12 * rng.randint(5, 40)
            water = cap * 3 // 4
            left = water - water * 2 // 3
            return MathDraw("", str(left),
                            prompt=(f"ถังน้ำจุ {cap} ลิตร มีน้ำอยู่ 3/4 ของถัง ใช้น้ำไป 2/3 ของน้ำที่มีอยู่ "
                                    f"เหลือน้ำในถังกี่ลิตร"),
                            distractors=_story.keep(cap - cap * 2 // 3, water * 2 // 3, cap // 12, water - cap * 2 // 3,
                                                    answer=left, lo=1))
        dist = a * b * rng.randint(1, 6)
        walked = Fraction(dist, a)
        second = (dist - walked) / b
        todo = dist - walked - second
        return MathDraw("", _fr(todo),
                        prompt=(f"เส้นทางเดินป่ายาว {dist} กิโลเมตร ช่วงเช้าเดินได้ 1/{a} ของระยะทาง ช่วงบ่ายเดินได้ "
                                f"1/{b} ของระยะทางที่เหลือ ยังต้องเดินอีกกี่กิโลเมตร"),
                        distractors=[_fr(dist - walked - Fraction(dist, b)), _fr(walked + second), _fr(dist - walked)])
