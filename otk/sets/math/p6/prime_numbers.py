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

from fractions import Fraction  # noqa: E402

from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit import story as _story  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathType, WordProblem  # noqa: E402
from otk.sets._support.math_p4 import as_mixed  # noqa: E402
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


# ── More prime numbers (2026-11): a prime factorisation, the largest prime factor, the sum of primes in a
# range, the next prime, and how many factors ──


def _is_prime6(n: int) -> bool:
    return n > 1 and all(n % k for k in range(2, int(n ** 0.5) + 1))


def _prime_factors6(n: int) -> list[int]:
    out, k = [], 2
    while n > 1:
        while n % k == 0:
            out.append(k)
            n //= k
        k += 1
    return out


@question_type("math.prime_factorisation_p6", display_name={"th": "แยกตัวประกอบ"},
               level=LEVEL, topic="จำนวนเฉพาะ")
class PrimeFactorisationP6(ChoiceType):
    def compose(self, rng: Random):
        while True:
            n = rng.randint(24, 200)
            fs = _prime_factors6(n)
            if len(fs) >= 3 and len(set(fs)) >= 2:
                break
        right = " × ".join(str(f) for f in fs)
        # A composite factor kept; one prime left out; one prime doubled.
        merged = [fs[0] * fs[1], *fs[2:]]
        wrongs = [" × ".join(str(f) for f in merged), " × ".join(str(f) for f in fs[1:]),
                  " × ".join(str(f) for f in [*fs, fs[-1]])]
        return f"ข้อใดเป็นการแยกตัวประกอบของ {n}", right, [w for w in dict.fromkeys(wrongs) if w != right]


@question_type("math.largest_prime_factor_p6", display_name={"th": "ตัวประกอบเฉพาะที่มากที่สุด"},
               level=LEVEL, topic="จำนวนเฉพาะ")
class LargestPrimeFactorP6(WordProblem):
    def expr(self, rng: Random):
        while True:
            n = rng.randint(30, 300)
            fs = _prime_factors6(n)
            if len(set(fs)) >= 2 and not _is_prime6(n):
                break
        right = max(fs)
        # The smallest; the number halved; the largest factor that is not prime.
        return MathDraw("", str(right), prompt=f"ตัวประกอบเฉพาะที่มากที่สุดของ {n} คือจำนวนใด",
                        distractors=_story.keep(min(fs), n // min(fs), sorted(set(fs))[-2], right + 2,
                                                answer=right, lo=2))


@question_type("math.sum_of_primes_p6", display_name={"th": "ผลบวกของจำนวนเฉพาะในช่วงที่กำหนด"},
               level=LEVEL, topic="จำนวนเฉพาะ")
class SumOfPrimesP6(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(1, 40)
        b = a + rng.randint(8, 16)
        primes = [k for k in range(a, b + 1) if _is_prime6(k)]
        while len(primes) < 2:
            b += 3
            primes = [k for k in range(a, b + 1) if _is_prime6(k)]
        right = sum(primes)
        odd = sum(k for k in range(a, b + 1) if k % 2 and k > 1)
        prompt = f"ผลบวกของจำนวนเฉพาะทุกจำนวนตั้งแต่ {a} ถึง {b} เท่ากับเท่าใด"
        # Every odd number; one prime left out; the count instead of the sum.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(odd, right - primes[-1], right - primes[0], right + 9,
                                                answer=right, lo=1))


@question_type("math.next_prime_p6", display_name={"th": "จำนวนเฉพาะที่อยู่ถัดไป"},
               level=LEVEL, topic="จำนวนเฉพาะ")
class NextPrimeP6(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(10, 120)
        right = next(k for k in range(n + 1, n + 100) if _is_prime6(k))
        odd = next(k for k in range(n + 1, n + 100) if k % 2 and not _is_prime6(k))
        prompt = f"จำนวนเฉพาะที่น้อยที่สุดที่มากกว่า {n} คือจำนวนใด"
        # The next odd number that is not prime; the prime after; one more.
        after = next(k for k in range(right + 1, right + 100) if _is_prime6(k))
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(odd, after, n + 1, right + 1, answer=right, lo=2))


@question_type("math.count_factors_p6", display_name={"th": "นับตัวประกอบทั้งหมด"},
               level=LEVEL, topic="จำนวนเฉพาะ")
class CountFactorsP6(WordProblem):
    def expr(self, rng: Random):
        n = rng.choice((12, 16, 18, 20, 24, 28, 30, 32, 36, 40, 42, 45, 48, 50, 54, 60, 64, 72, 80, 84, 90, 96, 100))
        right = sum(1 for k in range(1, n + 1) if n % k == 0)
        # 1 and the number left out; only the prime factors; one off.
        return MathDraw("", str(right), prompt=f"{n} มีตัวประกอบทั้งหมดกี่จำนวน",
                        distractors=_story.keep(right - 2, len(set(_prime_factors6(n))), right + 1, right - 1,
                                                answer=right, lo=1))
