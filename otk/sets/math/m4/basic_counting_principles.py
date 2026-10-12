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
