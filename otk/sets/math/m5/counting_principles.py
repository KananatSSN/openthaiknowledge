"""หลักการนับ

คณิตศาสตร์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม สถิติและความน่าจะเป็น 1 ม.5/1

Sets moved here from: math, math_bank_counting, math_bank_notes, math_data.
"""

from __future__ import annotations

import math as _math
from math import comb, perm
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_bank_counting import M5, _num_q, num
from otk.sets._support.math_bank_notes import M5 as M5_math_bank_notes
from otk.sets._support.math_bank_notes import _q

COUNTING = "หลักการนับ"


def at_least_one(d: int, n: int) -> int:
    """n-long strings over d symbols containing a given symbol at least once: dⁿ − (d − 1)ⁿ."""
    return d ** n - (d - 1) ** n


def above_power_of_ten(b: int, n: int) -> int:
    """n-digit numbers from digits 0, …, b − 1 (repeats allowed) that are greater than 10…0."""
    return (b - 1) * b ** (n - 1) - 1


#: name → (Thai description of which parts touch, edges, closed form in k). A path of n parts has no
#: description (the stem says "in a row") and its edges come from path_edges(n).
LAYOUTS = {
    "path": ("", None, lambda k, n: k * (k - 1) ** (n - 1)),
    "triangle_plus": ("ส่วน A, B และ C ติดกันทุกคู่ และส่วน D ติดกับ B และ C เท่านั้น",
                      ((0, 1), (0, 2), (1, 2), (1, 3), (2, 3)), lambda k, n: k * (k - 1) * (k - 2) ** 2),
    "cycle": ("ส่วน A, B, C และ D เรียงเป็นวง A ติดกับ B, B ติดกับ C, C ติดกับ D และ D ติดกับ A",
              ((0, 1), (1, 2), (2, 3), (0, 3)), lambda k, n: (k - 1) ** 4 + (k - 1)),
    "all": ("ส่วน A, B, C และ D ติดกันทุกคู่", ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)),
            lambda k, n: k * (k - 1) * (k - 2) * (k - 3)),
    "triangle_tail": ("ส่วน A, B และ C ติดกันทุกคู่ และส่วน D ติดกับ C เท่านั้น",
                      ((0, 1), (0, 2), (1, 2), (2, 3)), lambda k, n: k * (k - 1) * (k - 2) * (k - 1)),
}


def colourings(layout: str, k: int, n: int = 4) -> int:
    return LAYOUTS[layout][2](k, n)


def distributions(n: int, k: int, at_least: int = 0) -> int:
    """Ways to give n identical things to k distinct groups, each at least ``at_least``."""
    rest = n - k * at_least
    return comb(rest + k - 1, k - 1) if rest >= 0 else 0


@question_type("math.multiplication_principle",
               display_name={"th": "หลักการคูณ"}, level={"th": "ม.5"}, topic="หลักการนับ")
class MultiplicationPrinciple(WordProblem):
    def expr(self, rng: Random):
        m, n = rng.randint(2, 6), rng.randint(2, 6)
        prompt = rng.choice((
            f"เลือกเสื้อ {m} แบบ และกางเกง {n} แบบ จับคู่ได้กี่แบบ?",
            f"เดินทางจากเมือง A ไปเมือง B ได้ {m} เส้นทาง และจาก B ไป C ได้ {n} เส้นทาง "
            f"เดินทางจาก A ไป C ผ่าน B ได้กี่เส้นทาง",
            f"ร้านไอศกรีมมีไอศกรีม {m} รส และท็อปปิ้ง {n} ชนิด เลือกไอศกรีม 1 รสกับท็อปปิ้ง 1 ชนิด"
            f"ได้กี่แบบ",
            f"ห้องเรียนมีนักเรียนชาย {m} คน นักเรียนหญิง {n} คน ต้องการเลือกหัวหน้าชายหนึ่งคน"
            f"และรองหัวหน้าหญิงหนึ่งคน ได้กี่วิธี",
        ))
        return MathDraw("", str(m * n), prompt=prompt,
                        # Adding the choices, and one choice raised to the other.
                        distractors=[str(m + n), str(m ** n), str(m * n - 1)])
MultiplicationPrinciple.PROVENANCE = Provenance("original")


@question_type("math.counting_complement_m5",
               display_name={"th": "นับแบบตรงข้าม: มีอย่างน้อยหนึ่ง"},
               level=M5, topic=COUNTING)
class CountingComplementM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        if kind == 0:
            d, n = rng.randint(3, 6), rng.randint(3, 4)
            x = rng.randint(1, d)
            digits = ", ".join(str(v) for v in range(1, d + 1))
            stem = [text(f"กำหนดให้ S คือเซตของจำนวนนับ {n} หลักที่ประกอบขึ้นจากเลขโดด {digits} "
                         f"(ใช้ซ้ำได้) จำนวนสมาชิกของ S ที่มีเลขโดด {x} ปรากฏอยู่อย่างน้อยหนึ่งหลักเท่ากับเท่าใด")]
            # Exactly one x; forgetting to subtract; the complement itself.
            return _num_q(stem, at_least_one(d, n), [n * (d - 1) ** (n - 1), d ** n, (d - 1) ** n], self.topic)
        if kind == 1:
            n, x = rng.randint(2, 4), rng.randint(1, 9)
            stem = [text(f"จำนวนเต็มบวก {n} หลักซึ่งไม่มีเลขโดด 0 อยู่เลย แต่มีเลขโดด {x} "
                         "อย่างน้อยหนึ่งตัว มีทั้งหมดกี่จำนวน")]
            # Including 0 in the complement; exactly one x; 10 digits in the total.
            return _num_q(stem, at_least_one(9, n),
                          [9 ** n - 9 * 8 ** (n - 1), n * 8 ** (n - 1), 9 ** n - 8 ** (n - 1)], self.topic)
        if kind == 2:
            m, k = rng.randint(3, 6), rng.randint(3, 5)
            colours = ("สีฟ้า", "สีแดง", "สีเขียว", "สีเหลือง", "สีม่วง")[:k]
            stem = [text(f"ต้องการระบายสีรูป {m} รูปที่ต่างกัน รูปละ 1 สี จากสี {k} สี คือ {' '.join(colours)} "
                         "โดยจะใช้สีซ้ำหรือไม่ก็ได้ แต่ต้องมีรูปสีฟ้าอย่างน้อยหนึ่งรูป จำนวนวิธีระบายสีเท่ากับเท่าใด")]
            # Exactly one blue; all colourings; fixing one shape blue and colouring the rest freely.
            return _num_q(stem, at_least_one(k, m), [m * (k - 1) ** (m - 1), k ** m, k ** (m - 1)], self.topic)
        b, n = rng.randint(2, 4), rng.randint(3, 5)
        digits = ", ".join(str(v) for v in range(b))
        floor = "1" + "0" * (n - 1)
        stem = [text(f"ต้องการสร้างจำนวนที่มี {n} หลักจากเลขโดด {digits} (ใช้ซ้ำได้) "
                     "โดยจำนวนที่สร้างขึ้นมีค่ามากกว่า"), content_math(num(int(floor))),
                text("จะสร้างได้ทั้งหมดกี่จำนวน")]
        right = above_power_of_ten(b, n)
        # Allowing a leading 0; not removing 10…0 itself; bⁿ⁻¹.
        return _num_q(stem, right, [b ** n - 1, right + 1, b ** (n - 1)], self.topic)
CountingComplementM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/12 หลักการนับ',))


@question_type("math.counting_menu", display_name={"th": "หลักการคูณ: การเลือกชุดอาหาร"},
               level={"th": "ม.5"}, topic="หลักการนับ")
class CountingMenu(WordProblem):
    def expr(self, rng: Random, lo: int = 2, hi: int = 8):
        a, b, c = (rng.randint(lo, hi) for _ in range(3))
        prompt = rng.choice((
            f"ร้านอาหารมีอาหารจานหลัก {a} อย่าง เครื่องดื่ม {b} อย่าง และของหวาน {c} อย่าง "
            f"เลือกอย่างละหนึ่งได้กี่วิธี",
            f"ร้านกาแฟมีกาแฟ {a} ชนิด ขนาดแก้ว {b} ขนาด และระดับความหวาน {c} ระดับ "
            f"สั่งกาแฟหนึ่งแก้วได้กี่แบบ",
            f"รหัสผ่านประกอบด้วยตัวอักษร 1 ตัวจาก {a} ตัว ตามด้วยตัวเลข 1 ตัวจาก {b} ตัว "
            f"และสัญลักษณ์ 1 ตัวจาก {c} ตัว ตั้งรหัสผ่านได้กี่แบบ",
            f"นักเรียนต้องเลือกวิชาเลือกเสรีจากกลุ่มแรก {a} วิชา กลุ่มที่สอง {b} วิชา "
            f"และกลุ่มที่สาม {c} วิชา กลุ่มละหนึ่งวิชา เลือกได้กี่วิธี",
        ))
        return MathDraw("", str(a * b * c), prompt=prompt,
                        distractors=[str(a + b + c), str(a * b), str(a * b * c * 2)])
CountingMenu.PROVENANCE = Provenance("original")


@question_type("math.coloring_regions_m5",
               display_name={"th": "ระบายสีบริเวณที่ติดกันไม่ให้สีซ้ำ"},
               level=M5, topic=COUNTING)
class ColoringRegionsM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            n, k = rng.randint(4, 6), rng.randint(3, 5)
            stem = [text(f"มีรูปหกเหลี่ยม {n} รูปเรียงต่อกันเป็นแถว และมีสี {k} สีที่แตกต่างกัน "
                         "ต้องการระบายสีทุกรูป รูปละ 1 สี โดยรูปที่อยู่ติดกันต้องใช้สีต่างกัน จะระบายได้ทั้งหมดกี่วิธี")]
            # All colourings; every hexagon a different colour (when possible); one fewer factor.
            return _num_q(stem, colourings("path", k, n),
                          [k ** n, perm(k, n) if k >= n else k * (k - 1) * (k - 2) ** (n - 2),
                           (k - 1) ** n], self.topic)
        if kind == 1:
            n, k = rng.randint(3, 5), rng.randint(6, 10)
            stem = [text(f"ต้องการระบายสีภาพที่แบ่งออกเป็น {n} ส่วน ด้วยสีที่ต่างกัน {k} สี "
                         "โดยเลือกสีไประบายส่วนละหนึ่งสีจนครบทุกส่วนและไม่ใช้สีซ้ำกัน จำนวนวิธีระบายสีมีทั้งหมดกี่วิธี")]
            # Choosing without order; repeats allowed; nᵏ.
            return _num_q(stem, perm(k, n), [comb(k, n), k ** n, n ** k if n ** k < 10 ** 7 else k ** (n - 1)],
                          self.topic)
        layout = rng.choice(["triangle_plus", "cycle", "all", "triangle_tail"])
        k = rng.randint(4, 7)
        right = colourings(layout, k)
        stem = [text(f"รูปหนึ่งแบ่งออกเป็น 4 ส่วน คือ A, B, C และ D โดย{LAYOUTS[layout][0]} "
                     f"ถ้ามีสี {k} สี และต้องการระบายสีทุกส่วน ส่วนละหนึ่งสี "
                     "โดยส่วนที่ติดกันต้องใช้สีต่างกัน จะระบายได้ทั้งหมดกี่วิธี")]
        # Treating the parts as a row; every part a different colour; k(k − 1)³ for a cycle as if open.
        named = [colourings("path", k, 4), perm(k, 4), colourings("triangle_plus", k), colourings("cycle", k)]
        return _num_q(stem, right, [v for v in named if v != right], self.topic)
ColoringRegionsM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/12 หลักการนับ',))


@question_type("math.stars_bars_m5",
               display_name={"th": "แบ่งของที่เหมือนกันให้กลุ่มที่ต่างกัน (สตาร์แอนด์บาร์)"},
               level=M5_math_bank_notes, topic="หลักการนับ")
class StarsBarsM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        k = rng.randint(3, 5)
        n = rng.randint(k + 2, 14)
        kind = rng.randrange(3)
        if kind == 0:
            stem = [text(f"มีลูกอมที่เหมือนกันทุกเม็ด {n} เม็ด แจกให้เด็ก {k} คน โดยบางคนอาจไม่ได้เลย "
                         "จะแจกได้ทั้งหมดกี่วิธี")]
            right = distributions(n, k)
        elif kind == 1:
            stem = [text(f"มีลูกอมที่เหมือนกันทุกเม็ด {n} เม็ด แจกให้เด็ก {k} คน โดยทุกคนได้อย่างน้อย 1 เม็ด "
                         "จะแจกได้ทั้งหมดกี่วิธี")]
            right = distributions(n, k, 1)
        else:
            vars_ = " + ".join(f"x_{{{i}}}" for i in range(1, k + 1))
            stem = [text("จำนวนคำตอบที่เป็นจำนวนเต็มไม่เป็นลบของสมการ"), content_math(f"{vars_} = {n}"),
                    text("เท่ากับเท่าใด")]
            right = distributions(n, k)
        # kⁿ (distinct things); C(n + k, k); C(n + k − 1, k) (bars and stars swapped by one); the other rule.
        other = distributions(n, k, 1) if kind != 1 else distributions(n, k)
        return _q(stem, right, [comb(n + k - 1, k), other, comb(n + k, k), k ** n], self.topic)
StarsBarsM5.PROVENANCE = Provenance("original")


@question_type("math.counting_with_restriction",
               display_name={"th": "หลักการนับที่มีเงื่อนไข"},
               level={"th": "ม.5"}, topic="หลักการนับ")
class CountingWithRestriction(WordProblem):
    """Digits without repetition, and the conditions that change the count:
    no leading zero, an even last digit, a fixed first letter."""

    def expr(self, rng: Random, digits_lo: int = 3, digits_hi: int = 5,
             pool_lo: int = 5, pool_hi: int = 9):
        pool = rng.randint(pool_lo, pool_hi)
        length = rng.randint(digits_lo, min(digits_hi, pool))
        kind = rng.randrange(3)
        if kind == 0:
            count = _math.perm(pool, length)
            return MathDraw(
                "", str(count),
                prompt=(f"มีเลขโดด {pool} ตัวที่ต่างกันและไม่มี 0 ต้องการสร้างจำนวน {length} "
                        "หลักโดยใช้เลขโดดไม่ซ้ำกัน จะสร้างได้กี่จำนวน"),
                distractors=[str(pool ** length), str(_math.comb(pool, length)),
                             str(pool * length)])
        if kind == 1:
            # 0–(pool−1) with 0 not allowed first.
            count = (pool - 1) * _math.perm(pool - 1, length - 1)
            return MathDraw(
                "", str(count),
                prompt=(f"ใช้เลขโดด 0, 1, 2, …, {pool - 1} สร้างจำนวน {length} หลักที่เลขโดดไม่ซ้ำกัน "
                        "(หลักแรกห้ามเป็น 0) ได้กี่จำนวน"),
                distractors=[str(_math.perm(pool, length)), str(pool ** length),
                             str(_math.perm(pool - 1, length))])
        # Digits 1..pool, even numbers: choose the last digit first.
        evens = pool // 2
        count = evens * _math.perm(pool - 1, length - 1)
        return MathDraw(
            "", str(count),
            prompt=(f"ใช้เลขโดด 1 ถึง {pool} สร้างจำนวนคู่ {length} หลักที่เลขโดดไม่ซ้ำกัน ได้กี่จำนวน"),
            distractors=[str(_math.perm(pool, length) // 2), str(_math.perm(pool, length)),
                         str(evens * pool ** (length - 1))])
CountingWithRestriction.PROVENANCE = Provenance("original")
