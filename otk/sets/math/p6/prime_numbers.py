"""จำนวนเฉพาะ

คณิตศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.6/*

Sets moved here from: math, math_apply_stage, math_formats, math_number.
"""

from __future__ import annotations

import math
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import ChoiceType, MathDraw, MathType
from otk.sets._support.math_apply_stage import _nums
from otk.sets._support.math_diagrams import _math_q, _text_q
from otk.sets._support.math_gaps_shape_data import _choices
from otk.sets._support.math_m4 import maths

PROVENANCE = Provenance("original")


def _is_prime(n: int) -> bool:
    return n > 1 and all(n % d for d in range(2, math.isqrt(n) + 1))


def _factors(n: int) -> list[int]:
    return [d for d in range(1, n + 1) if n % d == 0]


_RICH = tuple(n for n in range(12, 101) if len(_factors(n)) >= 6)


@question_type("math.prime_or_composite",
               display_name={"th": "จำแนกจำนวนเฉพาะ/จำนวนประกอบ"}, level={"th": "ป.6"},
               topic="จำนวนเฉพาะ")
class PrimeOrComposite(ChoiceType):
    @staticmethod
    def _is_prime(n: int) -> bool:
        if n < 2:
            return False
        return all(n % k for k in range(2, int(n ** 0.5) + 1))

    def compose(self, rng: Random):
        n = rng.randint(2, 100)
        label = "จำนวนเฉพาะ" if self._is_prime(n) else "จำนวนประกอบ"
        other = "จำนวนประกอบ" if label == "จำนวนเฉพาะ" else "จำนวนเฉพาะ"
        return f"{n} เป็นจำนวนใด?", label, [other]


@question_type("math.factors_p6", display_name={"th": "ตัวประกอบของจำนวนนับ"},
               level={"th": "ป.6"}, topic="จำนวนเฉพาะ")
class FactorsP6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        n = rng.choice(_RICH)
        fs = _factors(n)
        if rng.random() < 0.5:
            def show(xs):
                return ", ".join(str(x) for x in xs)
            inner = fs[1:-1]
            near = next(x for x in range(2, n) if n % x and x not in fs)
            wrongs = [show(fs[:-1]),                                   # dropping n itself
                      show([x for x in fs if x != rng.choice(inner)]),  # missing one
                      show(sorted(fs + [near])),                        # one that does not divide
                      show([x for x in fs if x in (2, 3, 5, 7)])]       # primes only
            return _text_q([text(f"ข้อใดเป็นตัวประกอบทั้งหมดของ {n}")], show(fs), wrongs, self.topic)
        non = [x for x in range(2, n) if n % x]
        odd = rng.choice([x for x in non if x <= 12] or non)
        right = rng.sample([x for x in fs if 1 < x < n], 3)
        return _math_q([text(f"จำนวนใดไม่เป็นตัวประกอบของ {n}")], str(odd),
                       [str(x) for x in right], self.topic)


@question_type("math.pick_prime",
               display_name={"th": "เลือกจำนวนเฉพาะ"}, level={"th": "ป.6"},
               topic="จำนวนเฉพาะ")
class PickPrime(QuestionType):
    _PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
    _COMPOSITES = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25]

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        prime = rng.choice(self._PRIMES)
        wrong = rng.sample(self._COMPOSITES, 3)
        return GeneratedQuestion(
            stem=[text("จำนวนใดเป็นจำนวนเฉพาะ?")],
            correct=[content_math(str(prime))],
            distractors=fixed(*[[content_math(str(w))] for w in wrong]),
            topic=self.topic,
        )


@question_type("math.prime_word_p6", display_name={"th": "จำนวนเฉพาะในการจัดแถวและการนับ"},
               level={"th": "ป.6"}, topic="จำนวนเฉพาะ")
class PrimeWordP6(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            n = rng.randint(12, 60)
            ways = sum(1 for d in range(2, n) if n % d == 0)
            stem = (f"จัดเก้าอี้ {n} ตัวเป็นแถว แถวละเท่า ๆ กัน โดยมีอย่างน้อย 2 แถว และแถวละอย่างน้อย 2 ตัว "
                    f"จัดได้กี่แบบ (2 แถว แถวละ 3 ตัว ถือว่าต่างจาก 3 แถว แถวละ 2 ตัว)")
            divisors = sum(1 for d in range(1, n + 1) if n % d == 0)
            return maths([text(stem)], str(ways), _nums(ways, divisors, ways // 2 or ways + 2, ways + 1, lo=0),
                         self.topic)
        if kind == 1:
            primes = [p for p in range(11, 60) if _is_prime(p)]
            right = rng.choice(primes)
            others = rng.sample([n for n in range(12, 60) if not _is_prime(n) and n % 2], 3)
            return _choices([text("ครูมีลูกอมจำนวนหนึ่ง ต้องการแบ่งให้นักเรียนมากกว่า 1 คน คนละเท่า ๆ กัน "
                                  "และแต่ละคนได้มากกว่า 1 เม็ด จำนวนลูกอมในข้อใดแบ่งแบบนี้ไม่ได้")],
                            f"{right} เม็ด", [f"{o} เม็ด" for o in others], self.topic)
        a = rng.randint(10, 70)
        b = a + rng.randint(10, 20)
        count = sum(_is_prime(n) for n in range(a, b + 1))
        return maths([text(f"จำนวนเฉพาะที่อยู่ระหว่าง {a} ถึง {b} มีกี่จำนวน")], str(count),
                     _nums(count, count + 1, count - 1, (b - a) // 2, lo=0), self.topic)


@question_type("math.smallest_prime_factor",
               display_name={"th": "ตัวประกอบเฉพาะที่น้อยที่สุด"},
               level={"th": "ป.6"}, topic="จำนวนเฉพาะ")
class SmallestPrimeFactor(MathType):
    def expr(self, rng: Random, lo: int = 20, hi: int = 200):
        # Odd composites only: for an even number the answer is always 2, which
        # makes the item answerable without looking at it. Squares of a prime are
        # excluded too — there n // smallest *is* the answer, so the cofactor
        # distractor would be a second correct choice.
        n = rng.choice([m for m in range(lo | 1, hi, 2)
                        if any(m % k == 0 for k in range(3, int(m ** 0.5) + 1))
                        and int(m ** 0.5) ** 2 != m])
        smallest = next(k for k in range(3, n + 1) if n % k == 0)
        return MathDraw(str(n), str(smallest),
                        prompt="ตัวประกอบเฉพาะที่น้อยที่สุดของจำนวนนี้คือเท่าใด",
                        distractors=[str(n // smallest), str(n), "2"])
