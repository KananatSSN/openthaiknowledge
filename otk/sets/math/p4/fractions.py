"""เศษส่วน

คณิตศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.4/*

Sets moved here from: math_gaps_primary, math_p4, math_pictures_extra.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import image, text
from otk.core.content import math as content_math
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_p2 import _maths
from otk.sets._support.math_p4 import LEVEL, _not_equal, as_mixed, fr, mixed
from otk.sets._support.math_pictures_extra import BARS, _fr

PROVENANCE = Provenance("original")


def _frac_tex(f: Fraction) -> str:
    whole, rest = divmod(f.numerator, f.denominator)
    if rest == 0:
        return str(whole)
    return (f"{whole}" if whole else "") + rf"\frac{{{rest}}}{{{f.denominator}}}"


_FR_TOPIC = "เศษส่วน"


def _mixed(w: int, n: int, d: int) -> str:
    if n == 0:
        return str(w)
    return rf"{w}\frac{{{n}}}{{{d}}}" if w else _fr(n, d)


BARS_ALT = "ภาพแถบที่แบ่งเป็นส่วนเท่า ๆ กัน บางส่วนแรเงา"


@question_type("math.fraction_kinds_p4",
               display_name={"th": "เศษส่วนแท้ เศษส่วนเกิน และจำนวนคละ"},
               level=LEVEL, topic=_FR_TOPIC)
class FractionKindsP4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        d = rng.randint(3, 9)
        proper = fr(rng.randint(1, d - 1), d)
        improper = fr(rng.randint(d + 1, 3 * d), d)
        mixed_n = mixed(rng.randint(1, 5), rng.randint(1, d - 1), d)
        whole_like = fr(d, d)
        kind = rng.randrange(3)
        if kind == 0:
            return _maths([text("ข้อใดเป็นเศษส่วนแท้")], proper,
                          [improper, whole_like, mixed_n], self.topic)
        if kind == 1:
            # d/d is เศษส่วนเกิน too, so it is never a wrong choice here.
            return _maths([text("ข้อใดเป็นเศษส่วนเกิน")], improper,
                          [proper, mixed_n, fr(rng.randint(1, d - 1), d + 1)], self.topic)
        others = [improper, proper, fr(d + rng.randint(1, d - 1), d),
                  fr(rng.randint(1, d), d + 1), whole_like]
        return _maths([text("ข้อใดเป็นจำนวนคละ")], mixed_n,
                      [w for w in dict.fromkeys(others)], self.topic)


@question_type("math.improper_mixed_p4",
               display_name={"th": "เขียนเศษส่วนเกินเป็นจำนวนคละ และจำนวนคละเป็นเศษส่วนเกิน"},
               level=LEVEL, topic=_FR_TOPIC)
class ImproperMixedP4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        d = rng.randint(3, 9)
        whole, n = rng.randint(1, 6), rng.randint(1, d - 1)
        top = whole * d + n
        if rng.random() < 0.5:
            # Quotient and remainder swapped, the remainder over the numerator.
            wrongs = [mixed(n, whole, d) if whole < d else mixed(whole + 1, n, d),
                      mixed(whole, n, top), mixed(whole + 1, n, d),
                      mixed(whole - 1 or whole + 2, n, d), mixed(whole, d - n, d)]
            return _maths([text("เขียนเศษส่วนเกินนี้เป็นจำนวนคละ"), content_math(fr(top, d))],
                          mixed(whole, n, d), [w for w in dict.fromkeys(wrongs)
                                               if w != mixed(whole, n, d)], self.topic)
        # whole × n, whole + n, and forgetting to add the numerator.
        wrongs = [fr(whole * n, d), fr(whole + n, d), fr(whole * d, d), fr(top, d * whole)
                  if whole > 1 else fr(top + d, d), fr(top + 1, d), fr(top - 1, d)]
        return _maths([text("เขียนจำนวนคละนี้เป็นเศษส่วนเกิน"), content_math(mixed(whole, n, d))],
                      fr(top, d), [w for w in dict.fromkeys(wrongs) if w != fr(top, d)],
                      self.topic)


@question_type("math.fraction_bars_p4", display_name={"th": "จำนวนคละและเศษเกินจากภาพแถบ"},
               level={"th": "ป.4"}, topic="เศษส่วน")
class FractionBarsP4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        b = rng.choice(BARS)
        w, p, d = b.wholes, b.part, b.d
        img = image(b.asset_id, alt=BARS_ALT)
        lead = text("แต่ละแถบแทน 1 ส่วนที่แรเงาแทนจำนวนใด")
        if rng.random() < 0.5:
            # The unshaded part; the bars counted as the whole; the last bar alone.
            wrongs = [_mixed(w, d - p, d), _fr(w * d + p, (w + 1) * d), _mixed(w + 1, p, d), _fr(p, d)]
            return _math_q([lead, text("(ตอบเป็นจำนวนคละ)"), img], _mixed(w, p, d), wrongs, self.topic)
        n = w * d + p
        wrongs = [_fr(n, (w + 1) * d), _fr(w + p, d), _fr(n + d, d), _fr(n - 1, d)]
        return _math_q([lead, text("(ตอบเป็นเศษเกิน)"), img], _fr(n, d), wrongs, self.topic)


@question_type("math.compare_fractions_multiple_p4",
               display_name={"th": "เปรียบเทียบเศษส่วนและจำนวนคละที่ตัวส่วนเป็นพหุคูณกัน"},
               level={"th": "ป.4"}, topic="เศษส่วน")
class CompareFractionsMultipleP4(WordProblem):
    """Four numbers, one denominator a multiple of the other. Every choice is
    one of the four numbers shown."""

    def expr(self, rng: Random):
        while True:
            d, m = rng.choice((2, 3, 4, 5)), rng.choice((2, 3, 4))
            big = d * m
            fs = [Fraction(rng.randint(1, d - 1), d)] + [
                Fraction(rng.randint(1, big - 1), big) for _ in range(3)]
            if rng.random() < 0.4:      # make one a mixed number
                fs[rng.randrange(4)] += rng.randint(1, 2)
            # Lowest terms can break the multiple (5/15 is 1/3 next to fifths),
            # so check the denominators as they will be shown.
            dens = sorted({f.denominator for f in fs if f.denominator > 1})
            chain = all(b % a == 0 for a in dens for b in dens if b >= a)
            if len(set(fs)) == 4 and chain:
                break
        most = rng.random() < 0.5
        target = max(fs) if most else min(fs)
        return MathDraw(r",\ ".join(_frac_tex(f) for f in fs), _frac_tex(target),
                        prompt=f"จำนวนใดมีค่า{'มากที่สุด' if most else 'น้อยที่สุด'}",
                        distractors=[_frac_tex(f) for f in fs if f != target])


@question_type("math.fraction_addsub_multiple_p4",
               display_name={"th": "บวกลบเศษส่วนที่ตัวส่วนตัวหนึ่งเป็นพหุคูณของอีกตัวหนึ่ง"},
               level=LEVEL, topic=_FR_TOPIC)
class FractionAddSubMultipleP4(QuestionType):
    """a/d ± b/(dk): the answer is written over dk, the books' common
    denominator, as a proper fraction or จำนวนคละ."""

    def build(self, rng: Random) -> GeneratedQuestion:
        d, k = rng.randint(2, 6), rng.randint(2, 4)
        big = d * k
        a, b = rng.randint(1, d - 1), rng.randint(1, big - 1)
        while a * k == b:
            b = rng.randint(1, big - 1)
        add = rng.random() < 0.5
        if add:
            terms = [fr(a, d), fr(b, big)]
            rng.shuffle(terms)
            num = a * k + b
        elif a * k > b:
            terms, num = [fr(a, d), fr(b, big)], a * k - b
        else:
            terms, num = [fr(b, big), fr(a, d)], b - a * k
        whole, rem = divmod(num, big)
        answer = mixed(whole, rem, big) if whole else fr(rem, big)
        value = Fraction(num, big)
        # Adding tops and bottoms; not converting a/d; one sixth-of-a-step off.
        raw = a + b if add else abs(a - b)
        wrongs = [fr(raw, d + big), fr(raw, big), fr(num + 1, big), fr(num - 1, big)
                  if num > 1 else fr(num + 2, big), fr(raw, d), fr(num + 2, big),
                  fr(num + big, big)]
        return _maths([text("จงหาผลลัพธ์"),
                       content_math(f" {'+' if add else '-'} ".join(terms))],
                      answer, _not_equal(value, wrongs, answer), self.topic)


@question_type("math.fraction_word_problem_p4",
               display_name={"th": "โจทย์ปัญหาการบวกลบเศษส่วนและจำนวนคละ"},
               level=LEVEL, topic=_FR_TOPIC)
class FractionWordProblemP4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(_story.NAMES)
        d = rng.choice((2, 3, 4))
        big = d * rng.choice((2, 3))
        while True:
            x = Fraction(rng.randint(1, d - 1), d) + rng.randint(0, 2)
            y = Fraction(rng.randint(1, big - 1), big) + rng.randint(0, 2)
            if x != y:
                break
        kind = rng.randrange(6)
        takes = kind in (1, 3, 4)          # the situations that subtract
        if takes and x < y:
            x, y = y, x
        tx, ty = as_mixed(x), as_mixed(y)
        if kind == 0:
            stem = [text(f"{p}ใช้แป้งทำขนมครั้งแรก"), content_math(tx),
                    text("ถ้วยตวง ครั้งที่สอง"), content_math(ty),
                    text("ถ้วยตวง ใช้แป้งทั้งหมดกี่ถ้วยตวง")]
            value = x + y
        elif kind == 1:
            stem = [text(f"{p}มีเชือกยาว"), content_math(tx), text("เมตร ตัดไปใช้"),
                    content_math(ty), text("เมตร เหลือเชือกยาวกี่เมตร")]
            value = x - y
        elif kind == 2:
            stem = [text(f"{p}วิ่งวันแรก"), content_math(tx), text("กิโลเมตร วันที่สองวิ่ง"),
                    content_math(ty), text("กิโลเมตร สองวันวิ่งได้รวมกี่กิโลเมตร")]
            value = x + y
        elif kind == 3:
            stem = [text(f"{p}มีน้ำ"), content_math(tx), text("ลิตร ดื่มไป"),
                    content_math(ty), text("ลิตร เหลือน้ำกี่ลิตร")]
            value = x - y
        elif kind == 4:
            stem = [text("ถนนสายหนึ่งยาว"), content_math(tx), text("กิโลเมตร ซ่อมแล้ว"),
                    content_math(ty), text("กิโลเมตร ยังไม่ได้ซ่อมอีกกี่กิโลเมตร")]
            value = x - y
        else:
            stem = [text(f"{p}อ่านหนังสือวันเสาร์"), content_math(tx), text("ชั่วโมง วันอาทิตย์"),
                    content_math(ty), text("ชั่วโมง สองวันอ่านหนังสือรวมกี่ชั่วโมง")]
            value = x + y
        answer = as_mixed(value)
        step = Fraction(1, big)
        wrongs = [as_mixed(abs(x - y)) if not takes else as_mixed(x + y),
                  as_mixed(value + step), as_mixed(value + 1),
                  as_mixed(value - step) if value > step else as_mixed(value + 2)]
        return _maths(stem, answer, _not_equal(value, wrongs, answer), self.topic)
