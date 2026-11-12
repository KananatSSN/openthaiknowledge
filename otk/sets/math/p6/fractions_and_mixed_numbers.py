"""เศษส่วนและจำนวนคละ

คณิตศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.6/1, ค 1.1 ป.6/7, ค 1.1 ป.6/8

Sets moved here from: math_gaps_shape_data.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_p4 import as_mixed

PROVENANCE = Provenance("original")


def _rand_frac(rng: Random, whole_hi: int = 2) -> Fraction:
    d = rng.choice((2, 3, 4, 5, 6, 8, 10, 12))
    return Fraction(rng.randint(1, d - 1), d) + rng.randint(0, whole_hi)


@question_type("math.order_mixed_numbers_p6", display_name={"th": "เปรียบเทียบและเรียงลำดับเศษส่วนและจำนวนคละ"},
               level={"th": "ป.6"}, topic="เศษส่วนและจำนวนคละ")
class OrderMixedNumbersP6(WordProblem):
    def expr(self, rng: Random):
        while True:
            fs = [_rand_frac(rng) for _ in range(3)]
            dens = {f.denominator for f in fs}
            if len(set(fs)) == 3 and len(dens) >= 2:
                break
        asc = rng.random() < 0.5
        ordered = sorted(fs, reverse=not asc)
        while fs == ordered:        # never show them already in order
            fs = rng.sample(fs, 3)
        tex = lambda seq: r",\ ".join(as_mixed(f) for f in seq)
        # Ordering by numerators alone, and the reverse order.
        by_num = sorted(fs, key=lambda f: (f.numerator % f.denominator, f), reverse=not asc)
        return MathDraw(tex(fs), tex(ordered),
                        prompt=f"จงเรียงลำดับ{'จากน้อยไปมาก' if asc else 'จากมากไปน้อย'}",
                        distractors=[tex(w) for w in ([ordered[::-1], by_num,
                                                       [ordered[1], ordered[0], ordered[2]],
                                                       [ordered[0], ordered[2], ordered[1]]])
                                     if w != ordered])


@question_type("math.mixed_number_ops_p6", display_name={"th": "บวก ลบ คูณ หารระคนของเศษส่วนและจำนวนคละ"},
               level={"th": "ป.6"}, topic="เศษส่วนและจำนวนคละ")
class MixedNumberOpsP6(WordProblem):
    """a ∘ b ∗ c with ∗ a product or quotient, so the order of operations
    matters. Working left to right is the mistake named first."""

    def expr(self, rng: Random):
        while True:
            a, b, c = _rand_frac(rng, 2), _rand_frac(rng, 1), _rand_frac(rng, 1)
            plus = rng.random() < 0.5
            times = rng.random() < 0.5
            bc = b * c if times else b / c
            value = a + bc if plus else a - bc
            left_to_right = ((a + b) if plus else (a - b)) * c if times else ((a + b) if plus else (a - b)) / c
            if value > 0 and left_to_right > 0 and value != left_to_right and value.denominator <= 60:
                break
        op1, op2 = ("+" if plus else "-"), (r"\times" if times else r"\div")
        tex = rf"{as_mixed(a)} {op1} {as_mixed(b)} {op2} {as_mixed(c)}"
        # Multiplying or dividing whole and fraction parts separately.
        w = lambda f: f.numerator // f.denominator
        parts = Fraction(w(b) * w(c)) + (b - w(b)) * (c - w(c)) if times else None
        slip = (a + parts if plus else a - parts) if times else a + (b * c if plus else -b * c)
        wrongs = [left_to_right, slip, value + 1]
        return MathDraw(tex, as_mixed(value), prompt="จงหาผลลัพธ์",
                        distractors=[as_mixed(x) for x in dict.fromkeys(wrongs) if x != value and x > 0])


@question_type("math.fraction_multistep_word_p6",
               display_name={"th": "โจทย์ปัญหาเศษส่วนและจำนวนคละ 2–3 ขั้นตอน"},
               level={"th": "ป.6"}, topic="เศษส่วนและจำนวนคละ")
class FractionMultistepWordP6(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        p = rng.choice(_story.NAMES)
        m = lambda f: content_math(as_mixed(f))
        kind = rng.randrange(3)
        if kind == 0:
            each = Fraction(rng.randint(1, 3), 4) + 1
            n = rng.randint(2, 4)
            cloth = each * n + Fraction(rng.randint(1, 7), 8) + rng.randint(0, 1)
            value = cloth - each * n
            stem = [text(f"{p}มีผ้ายาว"), m(cloth), text(f"เมตร ตัดไปทำกระเป๋า {n} ใบ ใบละ"), m(each),
                    text("เมตร เหลือผ้ายาวกี่เมตร")]
            wrongs = [cloth - each, cloth - each - n, each * n]
        elif kind == 1:
            bag = rng.choice((Fraction(1, 2), Fraction(3, 4), Fraction(3, 2), Fraction(5, 4)))
            bags = rng.randint(6, 16)
            total = bag * bags
            sold = rng.randint(2, bags - 2)
            value = Fraction(bags - sold)
            stem = [text("ร้านค้ามีน้ำตาล"), m(total), text("กิโลกรัม แบ่งใส่ถุง ถุงละ"), m(bag),
                    text(f"กิโลกรัม แล้วขายไป {sold} ถุง เหลือน้ำตาลกี่ถุง")]
            wrongs = [Fraction(bags), total - sold, total * bag - sold]
        else:
            a, b = _rand_frac(rng, 1) + 1, _rand_frac(rng, 1)
            share = rng.randint(2, 4)
            value = (a + b) / share
            stem = [text(f"{p}เก็บผลไม้วันแรกได้"), m(a), text("กิโลกรัม วันที่สองได้"), m(b),
                    text(f"กิโลกรัม แบ่งให้เพื่อน {share} คนเท่า ๆ กัน ได้คนละกี่กิโลกรัม")]
            wrongs = [a + b / share, (a + b) * share, a + b]
        # Backups keep four choices when two of the mistakes coincide.
        wrongs += [value + Fraction(1, 2), value * 2, value + 1, value + Fraction(1, 4)]
        wrongs = [as_mixed(x) for x in dict.fromkeys(wrongs) if x != value and x > 0][:3]
        return GeneratedQuestion(stem=stem, correct=[content_math(as_mixed(value))],
                                 distractors=fixed(*[[content_math(w)] for w in wrongs]),
                                 topic=self.topic)


from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathType, WordProblem  # noqa: E402
from otk.sets._support.math_p6 import LEVEL  # noqa: E402


def _g6(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk6(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g6(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _d6(value: int, places: int) -> str:
    """An integer count of 10**-places as a decimal, trailing zeros dropped: (2350, 3) -> 2.35."""
    sign = "-" if value < 0 else ""
    whole, frac = divmod(abs(value), 10 ** places)
    digits = str(frac).rjust(places, "0").rstrip("0") if places else ""
    return f"{sign}{whole}.{digits}" if digits else f"{sign}{whole}"


def _dk6(*values: int, answer: int, places: int, lo: int = 0) -> list[str]:
    """``story.keep`` for decimals held as integer counts of 10**-places."""
    return [_d6(int(v), places) for v in _story.keep(*values, answer=answer, lo=lo)]


def _fk6(*values: Fraction, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer and non-positive values left out."""
    out: list[str] = []
    for v in values:
        if v > 0 and v != answer and as_mixed(v) not in out:
            out.append(as_mixed(v))
    return out


# ── More fractions and mixed numbers (2026-11): a mixed number times or divided by a whole number, a part of
# a part, the largest of four, a reciprocal, a missing factor, and a mixed number as an improper fraction ──


def _plain6(value: Fraction) -> str:
    """A fraction for Thai prompt text, outside TeX: 2 1/3, 3/4, or 5."""
    whole, rem = divmod(value.numerator, value.denominator)
    if not rem:
        return str(whole)
    return f"{whole} {rem}/{value.denominator}" if whole else f"{rem}/{value.denominator}"


def _mixed6(rng: Random) -> Fraction:
    d = rng.randint(2, 9)
    return rng.randint(1, 5) + Fraction(rng.randint(1, d - 1), d)


@question_type("math.mixed_times_whole_p6", display_name={"th": "จำนวนคละคูณจำนวนนับ"},
               level=LEVEL, topic="เศษส่วนและจำนวนคละ")
class MixedTimesWholeP6(MathType):
    def expr(self, rng: Random):
        m = _mixed6(rng)
        k = rng.randint(2, 9)
        right = m * k
        whole = m.numerator // m.denominator
        part = m - whole
        # Only the whole part multiplied; only the fraction; the whole number added.
        return MathDraw(f"{as_mixed(m)} \\times {k}", as_mixed(right), prompt="จงหาผลคูณ",
                        distractors=_fk6(whole * k + part, part * k + whole, m + k, right + 1, answer=right))


@question_type("math.mixed_divide_whole_p6", display_name={"th": "จำนวนคละหารด้วยจำนวนนับ"},
               level=LEVEL, topic="เศษส่วนและจำนวนคละ")
class MixedDivideWholeP6(MathType):
    def expr(self, rng: Random):
        m = _mixed6(rng)
        k = rng.randint(2, 6)
        right = m / k
        # Multiplied instead; the divisor upside down on the wrong side; the whole part alone divided.
        whole = m.numerator // m.denominator
        return MathDraw(f"{as_mixed(m)} \\div {k}", as_mixed(right), prompt="จงหาผลหาร",
                        distractors=_fk6(m * k, k / m, Fraction(whole, k) + (m - whole), right + Fraction(1, k),
                                         answer=right))


@question_type("math.part_of_part_p6", display_name={"th": "เศษส่วนของเศษส่วน"},
               level=LEVEL, topic="เศษส่วนและจำนวนคละ")
class PartOfPartP6(WordProblem):
    def expr(self, rng: Random):
        d1, d2 = rng.randint(2, 6), rng.randint(2, 6)
        f1, f2 = Fraction(rng.randint(1, d1 - 1), d1), Fraction(rng.randint(1, d2 - 1), d2)
        right = f1 * f2
        prompt = (f"สวนแห่งหนึ่งปลูกผัก {_plain6(f1)} ของพื้นที่ทั้งหมด และ {_plain6(f2)} ของพื้นที่ปลูกผักเป็นผักบุ้ง "
                  "ผักบุ้งคิดเป็นเศษส่วนเท่าใดของพื้นที่ทั้งหมด")
        # Added instead; the part left of the vegetables; the first fraction alone.
        return MathDraw("", as_mixed(right), prompt=prompt,
                        distractors=_fk6(f1 + f2, f1 * (1 - f2), f1, abs(f1 - f2), answer=right))


@question_type("math.largest_fraction_p6", display_name={"th": "เศษส่วนที่มากที่สุดหรือน้อยที่สุด"},
               level=LEVEL, topic="เศษส่วนและจำนวนคละ")
class LargestFractionP6(ChoiceType):
    def compose(self, rng: Random):
        while True:
            fs = []
            for _ in range(4):
                d = rng.randint(3, 12)
                fs.append(Fraction(rng.randint(1, d - 1), d))
            if len(set(fs)) == 4:
                break
        most = rng.random() < 0.5
        right = max(fs) if most else min(fs)
        return (f"เศษส่วนใด{'มากที่สุด' if most else 'น้อยที่สุด'}", as_mixed(right),
                [as_mixed(f) for f in fs if f != right])


@question_type("math.reciprocal_p6", display_name={"th": "ส่วนกลับของเศษส่วนและจำนวนคละ"},
               level=LEVEL, topic="เศษส่วนและจำนวนคละ")
class ReciprocalP6(MathType):
    def expr(self, rng: Random):
        m = _mixed6(rng) if rng.random() < 0.5 else Fraction(rng.randint(2, 11), rng.randint(2, 12))
        while m.denominator == 1 or m.numerator == 1:
            m = _mixed6(rng)
        right = f"\\frac{{{m.denominator}}}{{{m.numerator}}}"
        whole, rem = divmod(m.numerator, m.denominator)
        # The fraction part flipped with the whole kept; the number itself; its whole part over one.
        wrongs = [f"{whole}\\frac{{{m.denominator}}}{{{rem}}}" if whole else f"\\frac{{{m.numerator}}}{{{m.denominator + 1}}}",
                  as_mixed(m), f"\\frac{{{m.numerator}}}{{{m.denominator}}}" if whole else f"\\frac{{1}}{{{m.numerator}}}"]
        return MathDraw(as_mixed(m), right, prompt="ส่วนกลับของจำนวนนี้คือข้อใด",
                        distractors=[w for w in dict.fromkeys(wrongs) if w != right])


@question_type("math.fraction_missing_factor_p6", display_name={"th": "หาตัวคูณที่หายไป (เศษส่วน)"},
               level=LEVEL, topic="เศษส่วนและจำนวนคละ")
class FractionMissingFactorP6(MathType):
    def expr(self, rng: Random):
        d = rng.randint(2, 9)
        f = Fraction(rng.randint(1, d - 1), d)
        right = Fraction(rng.randint(2, 9), rng.choice((1, 1, 2, 3)))
        product = f * right
        # The product multiplied instead of divided; the factor upside down; the product itself.
        return MathDraw(f"{as_mixed(f)} \\times \\square = {as_mixed(product)}", as_mixed(right),
                        prompt="จำนวนใดเติมใน □ แล้วทำให้ประโยคเป็นจริง",
                        distractors=_fk6(product * f, 1 / right, product, right + 1, answer=right))


@question_type("math.mixed_to_improper_p6", display_name={"th": "เขียนจำนวนคละเป็นเศษเกิน"},
               level=LEVEL, topic="เศษส่วนและจำนวนคละ")
class MixedToImproperP6(MathType):
    def expr(self, rng: Random):
        d = rng.randint(2, 9)
        whole, rem = rng.randint(1, 9), rng.randint(1, d - 1)
        top = whole * d + rem
        right = f"\\frac{{{top}}}{{{d}}}"
        # The whole times the top; the whole and top added; the whole times the bottom alone.
        wrongs = [f"\\frac{{{whole * rem + d}}}{{{d}}}", f"\\frac{{{whole + rem}}}{{{d}}}", f"\\frac{{{whole * d}}}{{{d}}}",
                  f"\\frac{{{top}}}{{{d + whole}}}"]
        return MathDraw(f"{whole}\\frac{{{rem}}}{{{d}}}", right, prompt="เขียนจำนวนคละนี้เป็นเศษเกิน",
                        distractors=[w for w in dict.fromkeys(wrongs) if w != right])
