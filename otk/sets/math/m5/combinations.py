"""การจัดหมู่

คณิตศาสตร์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม สถิติและความน่าจะเป็น 1 ม.5/1

Sets moved here from: math, math_bank_counting, math_data, math_formats_hi, math_m5.
"""

from __future__ import annotations

import math
import math as _math
from math import comb, factorial, perm
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_bank_counting import M5, _num_q, num
from otk.sets._support.math_diagrams import _text_q
from otk.sets._support.math_m5 import M6

COMBINATION = "การจัดหมู่"


def _tex_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right][:3]
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


def multinomial(sizes: list[int]) -> int:
    out, left = 1, sum(sizes)
    for s in sizes:
        out *= comb(left, s)
        left -= s
    return out


def two_baskets(n: int, a: int, b: int) -> int:
    """a items to basket 1 and b to basket 2 from n distinct items, the rest left out."""
    return comb(n, a) * comb(n - a, b)


_ORDERED = (
    "เลือกประธานและรองประธานจากนักเรียน 10 คน",
    "นำหนังสือ 5 เล่มที่ต่างกันมาเรียงบนชั้น",
    "ตั้งรหัสผ่าน 4 หลักจากเลขโดดที่ไม่ซ้ำกัน",
    "จัดนักวิ่ง 8 คนให้ได้ที่ 1 ที่ 2 และที่ 3",
    "จัดคน 6 คนนั่งเรียงแถวบนม้านั่งยาว",
    "เลือกนักเรียน 3 คนมาเป็นหัวหน้า รองหัวหน้า และเหรัญญิก",
)


_UNORDERED = (
    "เลือกกรรมการ 3 คนจากนักเรียน 10 คน",
    "เลือกผลไม้ 2 ชนิดจากผลไม้ 6 ชนิดใส่ตะกร้า",
    "คน 8 คนจับมือกันคนละหนึ่งครั้ง",
    "เลือกนักกีฬา 5 คนจาก 12 คนเข้าทีม",
    "ลากส่วนของเส้นตรงเชื่อมจุด 2 จุดจากจุด 7 จุดบนวงกลม",
    "เลือกหนังสือ 3 เล่มจาก 8 เล่มไปอ่านช่วงปิดเทอม",
)


@question_type("math.combinations",
               display_name={"th": "การจัดหมู่ (nCr)"}, level={"th": "ม.6"},
               topic="การจัดหมู่")
class Combinations(MathType):
    def expr(self, rng: Random):
        n = rng.randint(5, 10)
        r = rng.randint(2, min(4, n - 1))
        return MathDraw(rf"\binom{{{n}}}{{{r}}}", rf"{math.comb(n, r)}",
                        hint=r"\binom{n}{r} = \frac{n!}{r!(n-r)!}")
Combinations.PROVENANCE = Provenance("original")


@question_type("math.order_matters_m5", display_name={"th": "สถานการณ์ใดคำนึงถึงลำดับ"},
               level={"th": "ม.5"}, topic="การจัดหมู่")
class OrderMattersM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.5:
            right = rng.choice(_UNORDERED)
            wrongs = rng.sample(_ORDERED, 3)
            ask = "สถานการณ์ใดเป็นการจัดหมู่ (ไม่คำนึงถึงลำดับ)"
        else:
            right = rng.choice(_ORDERED)
            wrongs = rng.sample(_UNORDERED, 3)
            ask = "สถานการณ์ใดเป็นการเรียงสับเปลี่ยน (คำนึงถึงลำดับ)"
        return _text_q([text(ask)], right, wrongs, self.topic)
OrderMattersM5.PROVENANCE = Provenance("original")


@question_type("math.combination_identity", display_name={"th": "สมบัติของ nCr"},
               level={"th": "ม.6"}, topic="การจัดหมู่")
class CombinationIdentity(MathType):
    """C(n, r) = C(n, n − r) — the reason you never compute C(20, 18) directly."""
    break_convergence = True  # one-part slips cluster round the answer

    def expr(self, rng: Random, n_lo: int = 6, n_hi: int = 20):
        n = rng.randint(n_lo, n_hi)
        # r = n/2 would make the answer the expression shown.
        r = rng.choice([k for k in range(2, n - 1) if 2 * k != n])
        return MathDraw(
            rf"\binom{{{n}}}{{{r}}}", rf"\binom{{{n}}}{{{n - r}}}",
            prompt="ข้อใดมีค่าเท่ากับนิพจน์นี้",
            distractors=[rf"\binom{{{n}}}{{{r + 1}}}",
                         rf"\binom{{{n - r}}}{{{r}}}",
                         rf"\binom{{{n + r}}}{{{r}}}"])
CombinationIdentity.PROVENANCE = Provenance("original")


@question_type("math.combination_word_m5",
               display_name={"th": "โจทย์ปัญหาการจัดหมู่ (จับมือ เส้นตรง เส้นทแยงมุม)"},
               level=M6, topic="การจัดหมู่")
class CombinationWordM5(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(5, 15)
        kind = rng.randrange(4)
        if kind == 0:
            ans = math.comb(n, 2)
            return MathDraw("", str(ans),
                            prompt=f"ในงานเลี้ยงมีคน {n} คน ทุกคนจับมือกันคนละหนึ่งครั้ง มีการจับมือทั้งหมดกี่ครั้ง",
                            # Counting each handshake twice.
                            distractors=_story.keep(n * (n - 1), n * n, math.comb(n, 3), answer=ans))
        if kind == 1:
            ans = math.comb(n, 2) - n
            return MathDraw("", str(ans),
                            prompt=f"รูป {n} เหลี่ยมมีเส้นทแยงมุมทั้งหมดกี่เส้น",
                            distractors=_story.keep(math.comb(n, 2), n * (n - 3), n * (n - 3) // 2 + n,
                                                    answer=ans))
        if kind == 2:
            ans = math.comb(n, 3)
            return MathDraw("", str(ans),
                            prompt=(f"มีจุด {n} จุดบนระนาบ โดยไม่มีสามจุดใดอยู่บนเส้นตรงเดียวกัน "
                                    f"สร้างรูปสามเหลี่ยมที่มีจุดยอดเป็นจุดเหล่านี้ได้กี่รูป"),
                            distractors=_story.keep(math.perm(n, 3), math.comb(n, 2), n * 3, answer=ans))
        k = rng.randint(2, 4)
        ans = math.comb(n, k)
        return MathDraw("", str(ans),
                        prompt=f"ร้านพิซซ่ามีหน้าพิซซ่า {n} ชนิด ต้องการเลือก {k} ชนิดโดยไม่สนใจลำดับ เลือกได้กี่แบบ",
                        distractors=_story.keep(math.perm(n, k), n * k, math.comb(n, k - 1), answer=ans))
CombinationWordM5.PROVENANCE = Provenance("original")


@question_type("math.distribute_to_groups_m5",
               display_name={"th": "แบ่งของที่ต่างกันให้กลุ่มที่ต่างกัน"},
               level=M5, topic=COMBINATION)
class DistributeToGroupsM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            r, s = rng.randint(2, 4), rng.randint(2, 3)
            sizes = [s] * r
            n = r * s
            right = multinomial(sizes)
            stem = [text(f"คุณแม่ซื้อโดนัทมา {n} ชิ้น แต่ละชิ้นหน้าตาต่างกัน ต้องการแบ่งให้ลูก {r} คน คนละ {s} ชิ้น "
                         "จะแบ่งได้ทั้งหมดกี่วิธี")]
            # The children treated as interchangeable; only the first child's choice; n!.
            return _num_q(stem, right, [right // factorial(r), comb(n, s), factorial(n)], self.topic)
        if kind == 1:
            n = rng.randint(6, 9)
            a = rng.randint(2, n // 2)
            b = rng.randint(2, n - a - 1)
            stem = [text(f"มีผลไม้ต่างชนิดกัน {n} ผล นำมาจัดลงตะกร้า 2 ใบที่แตกต่างกัน โดยใบแรกใส่ {a} ผล "
                         f"และใบที่สองใส่ {b} ผล ที่เหลือไม่ได้จัดลงตะกร้า จำนวนวิธีจัดเท่ากับเท่าใด")]
            # Both baskets chosen from all n; adding instead of multiplying; ordering inside baskets.
            right = two_baskets(n, a, b)
            return _num_q(stem, right, [comb(n, a) * comb(n, b), comb(n, a) + comb(n, b),
                                        perm(n, a) * perm(n - a, b)], self.topic)
        n = rng.choice((49, 59, 99, 199))
        right = rf"{num(comb(n + 1, 2))} \cdot {n}!"
        stem = [text(f"ในการจัดคน {n + 1} คนเข้าห้องพัก {n} ห้อง โดยแต่ละคนต้องถูกจัดเข้าห้องใดห้องหนึ่ง "
                     "และทุกห้องต้องมีคนพัก จะจัดได้ทั้งหมดกี่วิธี")]
        # The shared room's pair not chosen (only who is extra); the pair ordered; n·n!.
        wrongs = [rf"{n + 1} \cdot {n}!", rf"{num((n + 1) * n)} \cdot {n}!", rf"{n} \cdot {n}!"]
        return _tex_q(stem, right, wrongs, self.topic)
DistributeToGroupsM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/12 หลักการนับ',))


@question_type("math.combination_committee",
               display_name={"th": "การจัดหมู่: เลือกคณะกรรมการ"},
               level={"th": "ม.6"}, topic="การจัดหมู่")
class CombinationCommittee(WordProblem):
    def expr(self, rng: Random, men_lo: int = 4, men_hi: int = 9,
             women_lo: int = 4, women_hi: int = 9):
        men = rng.randint(men_lo, men_hi)
        women = rng.randint(women_lo, women_hi)
        pick_m = rng.randint(1, min(3, men))
        pick_w = rng.randint(1, min(3, women))
        kind = rng.randrange(3)
        if kind == 0:
            count = _math.comb(men, pick_m) * _math.comb(women, pick_w)
            return MathDraw(
                "", str(count),
                prompt=(f"จากชาย {men} คนและหญิง {women} คน ต้องการเลือกกรรมการ "
                        f"ชาย {pick_m} คนและหญิง {pick_w} คน เลือกได้กี่วิธี"),
                distractors=[str(_math.comb(men + women, pick_m + pick_w)),
                             str(_math.comb(men, pick_m) + _math.comb(women, pick_w)),
                             str(_math.perm(men, pick_m) * _math.perm(women, pick_w))])
        k = pick_m + pick_w
        if kind == 1:
            # At least one woman: everything minus the all-men choices.
            count = _math.comb(men + women, k) - _math.comb(men, k)
            return MathDraw(
                "", str(count),
                prompt=(f"จากชาย {men} คนและหญิง {women} คน เลือกกรรมการ {k} คน "
                        f"โดยต้องมีผู้หญิงอย่างน้อย 1 คน เลือกได้กี่วิธี"),
                distractors=[str(_math.comb(men + women, k)), str(women * _math.comb(men + women - 1, k - 1)),
                             str(_math.comb(women, k))])
        # A named person must be on it.
        n = men + women
        count = _math.comb(n - 1, k - 1)
        return MathDraw(
            "", str(count),
            prompt=(f"จากนักเรียน {n} คน ต้องการเลือกตัวแทน {k} คน โดยประธานนักเรียนต้องได้รับเลือกด้วย "
                    f"เลือกได้กี่วิธี"),
            distractors=[str(_math.comb(n, k)), str(_math.comb(n - 1, k)), str(_math.perm(n - 1, k - 1))])
CombinationCommittee.PROVENANCE = Provenance("original")
