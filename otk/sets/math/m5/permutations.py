"""การเรียงสับเปลี่ยน

คณิตศาสตร์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม สถิติและความน่าจะเป็น 1 ม.5/1

Sets moved here from: math, math_bank_counting, math_data, math_m5.
"""

from __future__ import annotations

import math
import math as _math
from math import comb, factorial, perm
from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_bank_counting import M5, _num_q
from otk.sets._support.math_m5 import M6

PERMUTATION = "การเรียงสับเปลี่ยน"


def blocks(sizes: list[int]) -> int:
    """Arrangements where each group stays together: g!·Π sᵢ!."""
    out = factorial(len(sizes))
    for s in sizes:
        out *= factorial(s)
    return out


def alternating(a: int, b: int) -> int:
    """Rows of a + b people from two groups with no two of the same group adjacent."""
    if abs(a - b) > 1:
        return 0
    return factorial(a) * factorial(b) * (2 if a == b else 1)


def no_two_adjacent_seats(n: int, p: int) -> int:
    """Seat p distinct people on n chairs in a row with no two in neighbouring chairs: C(n − p + 1, p)·p!."""
    return comb(n - p + 1, p) * factorial(p)


@question_type("math.permutations",
               display_name={"th": "การเรียงสับเปลี่ยน (nPr, วงกลม)"}, level={"th": "ม.6"}, topic="การเรียงสับเปลี่ยน")
class Permutations(MathType):
    def expr(self, rng: Random):
        kind = rng.choice(["npr", "fact", "circle"])
        if kind == "npr":
            n = rng.randint(5, 8)
            r = rng.randint(2, 4)
            return MathDraw(rf"{{}}_{{{n}}}P_{{{r}}}", rf"{math.perm(n, r)}",
                            topic="การเรียงสับเปลี่ยน",
                            hint=r"{}_{n}P_{r} = \frac{n!}{(n-r)!}")
        if kind == "fact":
            n = rng.randint(4, 7)
            return MathDraw(rf"{n}!", rf"{math.factorial(n)}", topic="แฟกทอเรียล")
        n = rng.randint(4, 7)
        return MathDraw(rf"n = {n}", rf"{math.factorial(n - 1)}", hint=r"(n-1)!",
                        topic="การเรียงสับเปลี่ยนเชิงวงกลม",
                        prompt=f"มีกี่วิธีที่คน {n} คนจะนั่งรอบโต๊ะกลม")
Permutations.PROVENANCE = Provenance("original")


@question_type("math.permutation_nPr", display_name={"th": "ค่าของ nPr"},
               level={"th": "ม.6"}, topic="การเรียงสับเปลี่ยน")
class PermutationNPr(MathType):
    def expr(self, rng: Random, n_lo: int = 4, n_hi: int = 10):
        n = rng.randint(n_lo, n_hi)
        r = rng.randint(2, min(4, n))
        return MathDraw(
            f"P({n}, {r})", str(_math.perm(n, r)), prompt="จงหาค่า",
            distractors=[str(_math.comb(n, r)), str(n ** r),
                         str(_math.factorial(n) // _math.factorial(r))])
PermutationNPr.PROVENANCE = Provenance("original")


@question_type("math.permutation_with_repetition",
               display_name={"th": "การเรียงสับเปลี่ยนของสิ่งที่ซ้ำกัน"},
               level={"th": "ม.6"}, topic="การเรียงสับเปลี่ยน")
class PermutationWithRepetition(WordProblem):
    WORDS = [("BANANA", [3, 2, 1]), ("LEVEL", [2, 2, 1]),
             ("SUCCESS", [3, 2, 1, 1]), ("MAMMAL", [3, 2, 1]),
             ("PEPPER", [3, 2, 1]), ("COFFEE", [2, 2, 1, 1])]

    def expr(self, rng: Random):
        word, counts = rng.choice(self.WORDS)
        n = len(word)
        total = _math.factorial(n)
        for c in counts:
            total //= _math.factorial(c)
        return MathDraw(
            "", str(total),
            prompt=f"นำตัวอักษรของคำว่า {word} มาเรียงสับเปลี่ยนได้กี่วิธี",
            # Forgetting to divide out the repeats.
            distractors=[str(_math.factorial(n)), str(total * 2),
                         str(_math.factorial(n - 1))])
PermutationWithRepetition.PROVENANCE = Provenance("original")


@question_type("math.permutation_identical_m5",
               display_name={"th": "การเรียงสับเปลี่ยนสิ่งของที่ซ้ำกัน"},
               level=M6, topic="การเรียงสับเปลี่ยน")
class PermutationIdenticalM5(WordProblem):
    _WORDS = ("BANANA", "LETTER", "COFFEE", "SCHOOL", "PEPPER", "BALLOON", "SUCCESS", "COOKBOOK")

    def expr(self, rng: Random):
        if rng.random() < 0.5:
            w = rng.choice(self._WORDS)
            counts = {c: w.count(c) for c in set(w)}
            ans = math.factorial(len(w))
            for c in counts.values():
                ans //= math.factorial(c)
            return MathDraw("", f"{ans:,}".replace(",", "{,}"),
                            prompt=f"นำตัวอักษรของคำ {w} มาเรียงสับเปลี่ยนทั้งหมด ได้กี่แบบ",
                            distractors=[f"{math.factorial(len(w)):,}".replace(",", "{,}"),
                                         f"{ans * 2:,}".replace(",", "{,}"), f"{math.factorial(len(counts)):,}"
                                         .replace(",", "{,}")])
        r, w = rng.randint(2, 4), rng.randint(2, 4)
        ans = math.comb(r + w, r)
        return MathDraw("", str(ans),
                        prompt=(f"มีธงสีแดง {r} ผืน และธงสีขาว {w} ผืน (ธงสีเดียวกันเหมือนกันทุกผืน) "
                                f"นำมาเรียงเป็นแถวได้กี่แบบ"),
                        distractors=_story.keep(math.factorial(r + w), math.factorial(r) * math.factorial(w),
                                                r * w, answer=ans))
PermutationIdenticalM5.PROVENANCE = Provenance("original")


@question_type("math.arrangement_blocks_gaps_m5",
               display_name={"th": "จัดเรียงให้ติดกันเป็นกลุ่ม สลับกลุ่ม หรือเว้นช่องไม่ให้ติดกัน"},
               level=M5, topic=PERMUTATION)
class ArrangementBlocksGapsM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            sizes = [rng.randint(2, 4) for _ in range(rng.randint(2, 3))]
            names = ("ภาษาไทย", "ภาษาอังกฤษ", "คณิตศาสตร์")[:len(sizes)]
            books = " ".join(f"{nm}ต่างกัน {s} เล่ม" for nm, s in zip(names, sizes))
            stem = [text(f"มีหนังสือ{books} ถ้าจะวางหนังสือทั้งหมดเรียงบนชั้นเดียวกัน "
                         "จำนวนวิธีจัดวางให้หนังสือวิชาเดียวกันอยู่ติดกันทั้งหมดเท่ากับเท่าใด")]
            inner = blocks(sizes) // factorial(len(sizes))
            # Only the inside of each block; only the blocks; adding the insides.
            return _num_q(stem, blocks(sizes), [inner, factorial(len(sizes)) * sum(factorial(s) for s in sizes),
                                                factorial(sum(sizes)) // inner], self.topic)
        if kind == 1:
            a = rng.randint(2, 5)
            b = a + rng.choice((0, 1))
            right = alternating(a, b)
            stem = [text(f"นักเรียนกลุ่มที่หนึ่ง {a} คน และกลุ่มที่สอง {b} คน ต้องการยืนเรียงแถวหน้ากระดานทั้ง "
                         f"{a + b} คน โดยนักเรียนกลุ่มเดียวกันไม่ยืนติดกัน จะจัดได้ทั้งหมดกี่วิธี")]
            # The factor 2 wrong way round; one group's order ignored; everyone arranged freely.
            other = factorial(a) * factorial(b) * (1 if a == b else 2)
            return _num_q(stem, right, [other, factorial(b) * (2 if a == b else 1), factorial(a + b)], self.topic)
        p = rng.randint(3, 5)
        n = rng.randint(2 * p, 2 * p + 3)
        right = no_two_adjacent_seats(n, p)
        stem = [text(f"มีเก้าอี้ {n} ตัววางเรียงเป็นแถวหน้ากระดาน ต้องการจัดที่นั่งให้คน {p} คน "
                     "โดยไม่ให้มีใครนั่งเก้าอี้ติดกัน จะจัดได้ทั้งหมดกี่วิธี")]
        # The chairs chosen but the people not ordered; any seats; n − p gaps instead of n − p + 1.
        return _num_q(stem, right, [comb(n - p + 1, p), perm(n, p), comb(n - p, p) * factorial(p)], self.topic)
ArrangementBlocksGapsM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/12 หลักการนับ',))


@question_type("math.circular_permutation_m5",
               display_name={"th": "การเรียงสับเปลี่ยนเชิงวงกลม"},
               level=M6, topic="การเรียงสับเปลี่ยน")
class CircularPermutationM5(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(4, 8)
        if rng.random() < 0.6:
            ans = math.factorial(n - 1)
            prompt = rng.choice((
                f"จัดคน {n} คนนั่งรอบโต๊ะกลม จัดได้กี่วิธี",
                f"ให้เด็ก {n} คนยืนจับมือกันเป็นวงกลมเพื่อเล่นเกม จัดได้กี่วิธี",
                f"จัดแจกันดอกไม้ {n} แจกันที่ต่างกันวางรอบโต๊ะกลม จัดได้กี่วิธี",
            ))
            return MathDraw("", str(ans), prompt=prompt,
                            # Treating the table as a row.
                            distractors=_story.keep(math.factorial(n), math.factorial(n - 2), n * n,
                                                    answer=ans))
        ans = 2 * math.factorial(n - 2)
        prompt = rng.choice((
            f"จัดคน {n} คนนั่งรอบโต๊ะกลม โดยให้สองคนที่กำหนดนั่งติดกันเสมอ จัดได้กี่วิธี",
            f"ครอบครัวหนึ่งมี {n} คนนั่งรับประทานอาหารรอบโต๊ะกลม โดยพ่อกับแม่นั่งติดกันเสมอ จัดได้กี่วิธี",
        ))
        return MathDraw("", str(ans), prompt=prompt,
                        # Forgetting the pair can swap, or treating it as a row.
                        distractors=_story.keep(math.factorial(n - 2), 2 * math.factorial(n - 1),
                                                math.factorial(n - 1), answer=ans))
CircularPermutationM5.PROVENANCE = Provenance("original")


@question_type("math.permutation_conditions_m5",
               display_name={"th": "การเรียงสับเปลี่ยนแบบมีเงื่อนไข"},
               level=M6, topic="การเรียงสับเปลี่ยน")
class PermutationConditionsM5(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(4, 7)
        f = math.factorial
        kind = rng.randrange(3)
        if kind == 0:
            ans = 2 * f(n - 1)
            return MathDraw("", str(ans),
                            prompt=f"จัดคน {n} คนยืนเรียงแถว โดยให้สองคนที่กำหนดยืนติดกันเสมอ จัดได้กี่วิธี",
                            distractors=_story.keep(f(n - 1), f(n), 2 * f(n - 2), answer=ans))
        if kind == 1:
            ans = f(n) - 2 * f(n - 1)
            return MathDraw("", str(ans),
                            prompt=f"จัดคน {n} คนยืนเรียงแถว โดยให้สองคนที่กำหนดไม่ยืนติดกัน จัดได้กี่วิธี",
                            # Everything, and everything minus the unswapped pair.
                            distractors=_story.keep(f(n), f(n) - f(n - 1), 2 * f(n - 1), answer=ans))
        ans = 2 * f(n - 2)
        return MathDraw("", str(ans),
                        prompt=(f"จัดคน {n} คนยืนเรียงแถว โดยให้สองคนที่กำหนดยืนหัวแถวและท้ายแถว "
                                f"จัดได้กี่วิธี"),
                        distractors=_story.keep(f(n - 2), f(n), 2 * f(n - 1), answer=ans))
PermutationConditionsM5.PROVENANCE = Provenance("original")
