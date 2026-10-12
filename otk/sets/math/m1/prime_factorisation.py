"""แยกตัวประกอบเฉพาะ

คณิตศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: —

Sets moved here from: math, math_apply_stage, math_formats_hi, math_number.
"""

from __future__ import annotations

import math
from collections import Counter
from random import Random
from typing import NamedTuple

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType
from otk.sets._support.math_apply_stage import _nums
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_m4 import maths

PROVENANCE = Provenance("original")


def _factorise(n: int) -> Counter:
    out, d = Counter(), 2
    while d * d <= n:
        while n % d == 0:
            out[d] += 1
            n //= d
        d += 1
    if n > 1:
        out[n] += 1
    return out


def _split(n: int) -> tuple[int, int] | None:
    """Two factors as close to √n as possible, or None for a prime."""
    for a in range(int(math.isqrt(n)), 1, -1):
        if n % a == 0:
            return a, n // a
    return None


class Node(NamedTuple):
    value: int
    children: tuple["Node", ...]


def _tree(n: int) -> Node:
    pair = _split(n)
    return Node(n, () if pair is None else (_tree(pair[0]), _tree(pair[1])))


def _nodes(t: Node) -> list[Node]:
    return [t] + [x for c in t.children for x in _nodes(c)]


class FactorTree(NamedTuple):
    n: int
    hidden: int          # index into the tree's nodes in pre-order; 0 = nothing hidden

    @property
    def asset_id(self) -> str:
        return f"mftree_{self.n}_{self.hidden}"

    @property
    def tree(self) -> Node:
        return _tree(self.n)


_TREE_NUMBERS = (24, 30, 36, 40, 45, 48, 54, 56, 60, 72, 84, 90, 96, 100, 108, 120, 126,
                 132, 150, 168, 180, 196, 210, 225)


def _factor_trees() -> tuple[FactorTree, ...]:
    out = []
    for i, n in enumerate(_TREE_NUMBERS):
        count = len(_nodes(_tree(n)))
        out.append(FactorTree(n, 0))
        out.append(FactorTree(n, 1 + i % (count - 1)))
        out.append(FactorTree(n, 1 + (i * 5 + 2) % (count - 1)))
    return tuple(dict.fromkeys(out))


FACTOR_TREES = _factor_trees()


TREE_ALT = "แผนภาพต้นไม้แสดงการแยกตัวประกอบ"


def _prime_power_tex(n: int) -> str:
    parts, p, m = [], 2, n
    while m > 1:
        k = 0
        while m % p == 0:
            m //= p
            k += 1
        if k:
            parts.append(f"{p}^{{{k}}}" if k > 1 else str(p))
        p += 1
    return r" \times ".join(parts)


@question_type("math.prime_factorization",
               display_name={"th": "แยกตัวประกอบเฉพาะ"}, level={"th": "ม.1"},
               topic="แยกตัวประกอบเฉพาะ")
class PrimeFactorization(MathType):
    _CANDIDATES = [
        12, 18, 20, 24, 28, 30, 36, 40, 42, 45,
        48, 50, 54, 56, 60, 63, 70, 72, 75, 80,
        84, 90, 96, 100, 108, 120, 126, 132, 140, 144,
        150, 180, 200, 210, 216, 240, 252, 270, 300, 360,
    ]

    def expr(self, rng: Random):
        n = rng.choice(self._CANDIDATES)
        temp, factors, d = n, {}, 2
        while d * d <= temp:
            while temp % d == 0:
                factors[d] = factors.get(d, 0) + 1
                temp //= d
            d += 1
        if temp > 1:
            factors[temp] = factors.get(temp, 0) + 1
        parts = [str(p) if e == 1 else rf"{p}^{{{e}}}"
                 for p, e in sorted(factors.items())]
        return MathDraw(rf"{n}", r" \cdot ".join(parts),
                        hint=r"\text{divide by smallest prime repeatedly}",
                        prompt="จงเขียนเป็นผลคูณของจำนวนเฉพาะ")


@question_type("math.factor_tree_m1", display_name={"th": "แผนภาพต้นไม้แยกตัวประกอบ"},
               level={"th": "ม.1"}, topic="แยกตัวประกอบเฉพาะ")
class FactorTreeM1(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random) -> GeneratedQuestion:
        t = rng.choice(FACTOR_TREES)
        img = image(t.asset_id, alt=TREE_ALT)
        if t.hidden:
            node = _nodes(t.tree)[t.hidden]
            v = node.value
            return _math_q([text("จากแผนภาพต้นไม้ จำนวนที่แทน ? คือจำนวนใด"), img],
                           str(v), [str(v * 2), str(v + 2), str(max(v - 2, 1)), str(v * 3)],
                           self.topic)
        n = t.n
        right = _prime_power_tex(n)
        # A composite factor left in; one prime too few or too many.
        pair = _split(n)
        wrongs = [rf"{pair[0]} \times {pair[1]}", _prime_power_tex(n * 2), _prime_power_tex(n // 2 * 3)
                  if n % 2 == 0 else _prime_power_tex(n * 3), _prime_power_tex(n + 2 if n % 4 else n + 4)]
        return _math_q([text(f"จากแผนภาพต้นไม้ {n} เขียนเป็นผลคูณของจำนวนเฉพาะได้อย่างไร"), img],
                       right, [w for w in wrongs if w != right], self.topic)


@question_type("math.count_divisors", display_name={"th": "จำนวนตัวประกอบทั้งหมด"},
               level={"th": "ม.1"}, topic="แยกตัวประกอบเฉพาะ")
class CountDivisors(MathType):
    """Why prime factorization is worth doing: the exponents give the count
    directly, as (e₁+1)(e₂+1)…, without listing anything."""

    def expr(self, rng: Random, lo: int = 12, hi: int = 200):
        # Composites only: a prime always has exactly 2, so those items are
        # answerable without factorizing anything.
        n = rng.choice([m for m in range(lo, hi)
                        if any(m % k == 0 for k in range(2, int(m ** 0.5) + 1))])
        count = sum(1 for d in range(1, n + 1) if n % d == 0)
        return MathDraw(str(n), str(count),
                        prompt="จำนวนนี้มีตัวประกอบทั้งหมดกี่จำนวน",
                        # Counting only the *prime* factors, and forgetting that
                        # 1 and n are themselves divisors.
                        distractors=[str(count - 2), str(count - 1),
                                     str(count + 2)])


@question_type("math.prime_factor_word_m1", display_name={"th": "นำการแยกตัวประกอบเฉพาะไปใช้"},
               level={"th": "ม.1"}, topic="แยกตัวประกอบเฉพาะ")
class PrimeFactorWordM1(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            while True:
                n = rng.randint(12, 300)
                f = _factorise(n)
                k = math.prod(p for p, e in f.items() if e % 2)
                if 1 < k < n:
                    break
            stem = (f"ต้องการจัดกระเบื้องแผ่นสี่เหลี่ยมจัตุรัสเป็นรูปสี่เหลี่ยมจัตุรัสรูปใหญ่ มีกระเบื้องชุดละ {n} แผ่น "
                    f"ต้องใช้กระเบื้องอย่างน้อยกี่ชุด (จำนวนชุดที่น้อยที่สุดที่ทำให้ {n} × จำนวนชุด เป็นกำลังสองสมบูรณ์)")
            wrong = max(f)
            return maths([text(stem)], str(k), _nums(k, wrong, n, k * 2, lo=1), self.topic)
        if kind == 1:
            n = rng.choice([m for m in range(24, 200) if len(_factorise(m)) >= 2])
            f = _factorise(n)
            divisors = math.prod(e + 1 for e in f.values())
            stem = (f"จัดนักเรียน {n} คนเป็นแถว แถวละเท่า ๆ กัน (จัดเป็นแถวเดียวก็ได้) จัดได้กี่แบบ")
            return maths([text(stem)], str(divisors),
                         _nums(divisors, sum(f.values()), math.prod(f.values()), divisors // 2, divisors - 2, lo=1),
                         self.topic)
        while True:
            a, b = rng.sample(range(12, 90), 2)
            g = math.gcd(a, b)
            if 1 < g < min(a, b):
                break
        stem = (f"มีไม้ยาว {a} เซนติเมตร และ {b} เซนติเมตร ตัดทั้งสองท่อนเป็นท่อนสั้นยาวเท่ากันให้ยาวที่สุด "
                f"โดยไม่เหลือเศษ จะได้ไม้ท่อนสั้นทั้งหมดกี่ท่อน")
        pieces = a // g + b // g
        return maths([text(stem)], str(pieces), _nums(pieces, g, a * b // g, pieces + 1, lo=1), self.topic)


@question_type("math.largest_prime_factor",
               display_name={"th": "ตัวประกอบเฉพาะที่มากที่สุด"},
               level={"th": "ม.1"}, topic="แยกตัวประกอบเฉพาะ")
class LargestPrimeFactor(MathType):
    def expr(self, rng: Random, lo: int = 30, hi: int = 400):
        def largest_factor(m: int) -> int:
            out, k = 1, 2
            while k * k <= m:
                while m % k == 0:
                    out, m = k, m // k
                k += 1
            return m if m > 1 else out

        # Composites only — for a prime the answer is the number itself, which
        # asks nothing, and the cofactor distractor would be 1.
        n = rng.choice([m for m in range(lo, hi)
                        if any(m % k == 0 for k in range(2, int(m ** 0.5) + 1))])
        largest = largest_factor(n)
        return MathDraw(str(n), str(largest),
                        prompt="ตัวประกอบเฉพาะที่มากที่สุดของจำนวนนี้คือเท่าใด",
                        distractors=[str(n // largest), str(n),
                                     str(largest_factor(n // largest))])
