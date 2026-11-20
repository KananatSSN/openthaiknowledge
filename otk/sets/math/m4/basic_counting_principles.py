"""หลักการนับเบื้องต้น

คณิตศาสตร์ · ม.4 · สสวท. พื้นฐาน
Indicators: ค 3.2 ม.4/1

Sets moved here from: math_gaps_secondary.
"""

from __future__ import annotations

import math
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_gaps_secondary import _num

PROVENANCE = Provenance("original")


_COUNT_TOPIC = "หลักการนับเบื้องต้น"


@question_type("math.add_or_multiply_m4", display_name={"th": "หลักการบวกและหลักการคูณ"},
               level={"th": "ม.4"}, topic=_COUNT_TOPIC)
class AddOrMultiplyM4(WordProblem):
    """The same numbers, told once as a choice between ways (add) and once as
    one step after another (multiply). Mixing the two is the mistake."""

    def expr(self, rng: Random):
        m, n = rng.randint(2, 7), rng.randint(2, 7)
        kind = rng.randrange(4)
        if kind == 0:
            return MathDraw("", str(m + n), prompt=(
                f"การเดินทางจากเมือง A ไปเมือง B ไปได้โดยรถโดยสาร {m} เส้นทาง หรือโดยรถไฟ {n} เส้นทาง "
                f"จะเดินทางจาก A ไป B ได้กี่วิธี"),
                distractors=_story.keep(m * n, m + n + 1, max(m, n), answer=m + n, lo=1))
        if kind == 1:
            return MathDraw("", str(m * n), prompt=(
                f"จากเมือง A ไปเมือง B มีถนน {m} สาย และจากเมือง B ไปเมือง C มีถนน {n} สาย "
                f"เดินทางจาก A ไป C โดยผ่าน B ได้กี่วิธี"),
                distractors=_story.keep(m + n, m * n + m, m * n - 1, answer=m * n, lo=1))
        if kind == 2:
            k = rng.randint(2, 5)
            return MathDraw("", str(m * n * k), prompt=(
                f"ร้านอาหารมีข้าว {m} แบบ กับข้าว {n} แบบ และเครื่องดื่ม {k} แบบ "
                f"ถ้าสั่งอย่างละหนึ่ง จะสั่งอาหารได้กี่ชุด"),
                distractors=_story.keep(m + n + k, m * n + k, m * n, answer=m * n * k, lo=1))
        digits = rng.randint(3, 4)
        choices = rng.randint(5, 9)
        value = math.perm(choices, digits)
        return MathDraw("", _num(value), prompt=(
            f"มีบัตรตัวเลข {choices} ใบ เขียนเลขโดดต่างกันใบละหนึ่งตัว (ไม่มี 0) "
            f"นำมาเรียงเป็นจำนวน {digits} หลักโดยไม่ใช้บัตรซ้ำ ได้กี่จำนวน"),
            distractors=[_num(int(v)) for v in
                         _story.keep(choices ** digits, choices * digits, math.comb(choices, digits),
                                     answer=value, lo=1)])


@question_type("math.arrange_in_row_m4", display_name={"th": "การจัดเรียงสิ่งของที่แตกต่างกันเป็นแถว"},
               level={"th": "ม.4"}, topic=_COUNT_TOPIC)
class ArrangeInRowM4(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(4, 7)
        kind = rng.randrange(3)
        things = rng.choice(("นักเรียน", "หนังสือ", "ตุ๊กตา", "รถของเล่น"))
        if kind == 0:
            value = math.factorial(n)
            prompt = f"จัด{things}ที่แตกต่างกัน {n} ชิ้นเรียงเป็นแถวได้กี่แบบ" if things != "นักเรียน" \
                else f"จัดนักเรียน {n} คนยืนเรียงแถวถ่ายรูปได้กี่แบบ"
            wrongs = [n * n, math.factorial(n - 1), n * (n - 1)]
        elif kind == 1:
            value = math.factorial(n - 1)
            prompt = f"จัดนักเรียน {n} คนยืนเรียงแถว โดยให้หัวหน้าห้องยืนหัวแถวเสมอ ได้กี่แบบ"
            wrongs = [math.factorial(n), n * (n - 1), math.factorial(n) - 1]
        else:
            r = rng.randint(2, n - 1)
            value = math.perm(n, r)
            prompt = f"เลือกนักเรียน 2 คนจาก {n} คน มาเป็นประธานและรองประธาน ได้กี่แบบ" \
                if r == 2 else f"เลือกนักเรียน {r} คนจาก {n} คน มายืนเรียงแถวหน้ากระดาน ได้กี่แบบ"
            wrongs = [math.comb(n, r), n ** r, math.factorial(n)]
        return MathDraw("", _num(value), prompt=prompt,
                        distractors=[_num(int(v)) for v in _story.keep(*wrongs, answer=value, lo=1)])


@question_type("math.choose_group_m4", display_name={"th": "การเลือกสิ่งของโดยไม่คำนึงถึงลำดับ"},
               level={"th": "ม.4"}, topic=_COUNT_TOPIC)
class ChooseGroupM4(WordProblem):
    def expr(self, rng: Random):
        n, r = rng.randint(5, 10), rng.randint(2, 4)
        if rng.random() < 0.5:
            value = math.comb(n, r)
            prompt = rng.choice((
                f"เลือกตัวแทน {r} คนจากนักเรียน {n} คน ไปแข่งขันเป็นทีม ได้กี่วิธี",
                f"มีหนังสือต่างกัน {n} เล่ม เลือกยืม {r} เล่ม ได้กี่วิธี",
                f"ร้านมีท็อปปิงไอศกรีม {n} ชนิด เลือกใส่ {r} ชนิดที่ต่างกัน ได้กี่แบบ",
                f"มีจุด {n} จุดบนวงกลม เลือก {r} จุดมาเป็นจุดยอดของรูปหลายเหลี่ยม ได้กี่รูป"
                if r >= 3 else f"มีจุด {n} จุดบนวงกลม ลากส่วนของเส้นตรงเชื่อมจุดทีละ 2 จุด ได้กี่เส้น",
            ))
            wrongs = [math.perm(n, r), n * r, math.comb(n, r - 1)]
        else:
            value = math.comb(n - 1, r - 1)
            prompt = f"เลือกตัวแทน {r} คนจากนักเรียน {n} คน โดยต้องมีหัวหน้าห้องอยู่ในทีมด้วย ได้กี่วิธี"
            wrongs = [math.comb(n, r), math.comb(n - 1, r), math.perm(n - 1, r - 1)]
        return MathDraw("", str(value), prompt=prompt,
                        distractors=_story.keep(*wrongs, answer=value, lo=1))

from fractions import Fraction  # noqa: E402
from math import comb, factorial  # noqa: E402

from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import question_type  # noqa: E402
from otk.kit.math_problems import WordProblem  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m4 import M4 as LEVEL  # noqa: E402


def _nz4(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk4(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk4(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk4(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt4(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk4(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk4(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))

# ── More counting (2026-11): outfits, codes with repeats, numbers with no repeated digit, even numbers,
# handshakes, a round trip on different roads, and two people side by side ──


@question_type("math.outfits_m4", display_name={"th": "แต่งตัวได้กี่แบบ"}, level=LEVEL, topic="หลักการนับเบื้องต้น")
class OutfitsM4(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.randint(2, 6), rng.randint(2, 6), rng.randint(2, 5)
        right = a * b * c
        prompt = f"มีเสื้อ {a} ตัว กางเกง {b} ตัว และรองเท้า {c} คู่ แต่งตัวโดยใส่อย่างละหนึ่งชิ้นได้กี่แบบ"
        # Added instead of multiplied; two kinds only.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk4(a + b + c, a * b, a * b + c, right + a, answer=right, lo=1))


@question_type("math.codes_with_repeats_m4", display_name={"th": "รหัสที่ใช้ตัวเลขซ้ำได้"}, level=LEVEL,
               topic="หลักการนับเบื้องต้น")
class CodesWithRepeatsM4(WordProblem):
    def expr(self, rng: Random):
        k = rng.randint(2, 4)
        repeat = rng.random() < 0.5
        right = 10 ** k if repeat else factorial(10) // factorial(10 - k)
        rule = "ใช้เลขโดดซ้ำกันได้" if repeat else "ไม่ใช้เลขโดดซ้ำกัน"
        prompt = f"สร้างรหัสผ่าน {k} หลักจากเลขโดด 0 ถึง 9 โดย{rule} ได้ทั้งหมดกี่รหัส"
        other = factorial(10) // factorial(10 - k) if repeat else 10 ** k
        # The other rule; ten times the length; choosing without order.
        return MathDraw("", f"{right:,}".replace(",", "{,}"), prompt=prompt,
                        distractors=[f"{v:,}".replace(",", "{,}") for v in dict.fromkeys((other, 10 * k, comb(10, k), 9 ** k))
                                     if v != right])


@question_type("math.numbers_no_repeat_m4", display_name={"th": "จำนวนที่สร้างจากเลขโดดไม่ซ้ำกัน (มี 0)"},
               level=LEVEL, topic="หลักการนับเบื้องต้น")
class NumbersNoRepeatM4(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(4, 8)
        k = rng.choice((3, 4)) if n >= 5 else 3
        digits = ", ".join(str(d) for d in range(n + 1))
        right = n * factorial(n) // factorial(n - k + 1)
        prompt = f"ใช้เลขโดด {digits} สร้างจำนวน {k} หลักที่เลขโดดไม่ซ้ำกัน ได้กี่จำนวน"
        # 0 allowed in front; digits allowed to repeat; one fewer digit.
        return MathDraw("", f"{right:,}".replace(",", "{,}"), prompt=prompt,
                        distractors=[f"{v:,}".replace(",", "{,}")
                                     for v in dict.fromkeys((factorial(n + 1) // factorial(n + 1 - k), n * (n + 1) ** (k - 1),
                                                             factorial(n) // factorial(n - k), right + n)) if v != right])


@question_type("math.even_numbers_count_m4", display_name={"th": "นับจำนวนคู่ที่สร้างจากเลขโดดไม่ซ้ำกัน"},
               level=LEVEL, topic="หลักการนับเบื้องต้น")
class EvenNumbersCountM4(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(5, 9)
        evens = n // 2
        right = evens * (n - 1) * (n - 2)
        digits = ", ".join(str(d) for d in range(1, n + 1))
        prompt = f"ใช้เลขโดด {digits} สร้างจำนวนคู่สามหลักที่เลขโดดไม่ซ้ำกัน ได้กี่จำนวน"
        # Any number at all; repeats allowed in the front two; odd numbers instead.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk4(n * (n - 1) * (n - 2), evens * n * n, (n - evens) * (n - 1) * (n - 2),
                                         right + evens, answer=right, lo=1))


@question_type("math.handshakes_m4", display_name={"th": "จับมือกันทุกคู่ได้กี่ครั้ง"}, level=LEVEL,
               topic="หลักการนับเบื้องต้น")
class HandshakesM4(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(4, 25)
        right = n * (n - 1) // 2
        prompt = f"มีคน {n} คน ทุกคนจับมือกับคนอื่นคนละหนึ่งครั้ง จะมีการจับมือทั้งหมดกี่ครั้ง"
        # Each handshake counted twice; n squared; n times n less one... less one.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk4(n * (n - 1), n * n, (n - 1) * (n - 2) // 2, right + n, answer=right, lo=1))


@question_type("math.round_trip_routes_m4", display_name={"th": "ไปกลับโดยไม่ใช้ทางเดิม"}, level=LEVEL,
               topic="หลักการนับเบื้องต้น")
class RoundTripRoutesM4(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.randint(2, 5), rng.randint(2, 5)
        right = a * b * (a - 1) * (b - 1)
        prompt = (f"จากเมือง A ไปเมือง B มีถนน {a} สาย จากเมือง B ไปเมือง C มีถนน {b} สาย "
                  "เดินทางจาก A ไป C แล้วกลับมา A โดยไม่ใช้ถนนสายเดิมเลย ได้กี่วิธี")
        # One way only; the roads reused; added instead.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk4(a * b, (a * b) ** 2, a + b, a * b * (a + b - 2), answer=right, lo=1))


@question_type("math.side_by_side_m4", display_name={"th": "นั่งเรียงแถวโดยสองคนนั่งติดกัน"}, level=LEVEL,
               topic="หลักการนับเบื้องต้น")
class SideBySideM4(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(4, 7)
        right = 2 * factorial(n - 1)
        p, q = _story.names(rng)
        prompt = f"คน {n} คนรวมทั้ง{p}และ{q} นั่งเรียงแถวหน้ากระดาน โดย{p}กับ{q}ต้องนั่งติดกัน จัดได้กี่แบบ"
        # The pair not swapped; everyone free; the pair kept apart.
        return MathDraw("", f"{right:,}".replace(",", "{,}"), prompt=prompt,
                        distractors=[f"{v:,}".replace(",", "{,}") for v in
                                     dict.fromkeys((factorial(n - 1), factorial(n), factorial(n) - right, 2 * factorial(n - 2)))
                                     if v != right])
