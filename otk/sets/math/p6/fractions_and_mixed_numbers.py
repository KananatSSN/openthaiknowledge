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
