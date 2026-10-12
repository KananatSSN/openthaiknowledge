"""ระบบสมการ

คณิตศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ค 1.3 ม.3/3

Sets moved here from: math, math_algebra, math_m3.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem, poly_tex
from otk.sets._support.math_algebra import _nonzero
from otk.sets._support.math_m3 import LEGACY
from otk.sets._support.math_p2 import _maths

PROVENANCE = Provenance("original")


@question_type("math.simultaneous_2var",
               display_name={"th": "ระบบสมการสองตัวแปร"}, level={"th": "ม.2"},
               topic="ระบบสมการ")
class Simultaneous2Var(MathType):
    def expr(self, rng: Random, aligned: int = 1):
        x, y = rng.randint(-6, 6), rng.randint(-6, 6)
        if aligned:
            b = rng.randint(1, 4)
            a1, a2 = rng.sample(range(1, 10), 2)
            b1 = b2 = b
        else:
            while True:
                a1, b1, a2, b2 = (rng.choice([1, -1]) * rng.randint(1, 5)
                                  for _ in range(4))
                if a1 * b2 - a2 * b1 != 0:
                    break
        e1 = rf"{poly_tex((a1, 'x'), (b1, 'y'))} = {a1 * x + b1 * y}"
        e2 = rf"{poly_tex((a2, 'x'), (b2, 'y'))} = {a2 * x + b2 * y}"
        return MathDraw(rf"{e1}, \;\; {e2}", rf"(x, y) = ({x}, {y})",
                        prompt="จงแก้ระบบสมการ")


@question_type("math.system_substitution", display_name={"th": "ระบบสมการ (แทนค่า)"},
               level={"th": "ม.2"}, topic="ระบบสมการ")
class SystemSubstitution(MathType):
    def expr(self, rng: Random, root_hi: int = 8, coef_hi: int = 6):
        x, y = (_nonzero(rng, -root_hi, root_hi) for _ in range(2))
        a, b = rng.randint(1, coef_hi), rng.randint(1, coef_hi)
        c, d = rng.randint(1, coef_hi), -rng.randint(1, coef_hi)
        if a * d - b * c == 0:                     # keep the system independent
            d -= 1
        e, f = a * x + b * y, c * x + d * y
        return MathDraw(
            rf"\begin{{cases}} {poly_tex((a, 'x'), (b, 'y'))} = {e} \\ "
            rf"{poly_tex((c, 'x'), (d, 'y'))} = {f} \end{{cases}}",
            f"({x}, {y})", prompt="จงหาคำตอบของระบบสมการ",
            distractors=[f"({y}, {x})", f"({-x}, {-y})", f"({x}, {-y})"])


@question_type("math.system_setup_m3",
               display_name={"th": "เขียนระบบสมการจากโจทย์ปัญหา"},
               level=LEGACY, topic="ระบบสมการ")
class SystemSetupM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(6)
        if kind == 3:
            ad, ch = rng.randint(2, 40), rng.randint(2, 40)
            pa, pc = rng.choice(((120, 60), (100, 50), (150, 80), (80, 40)))
            money = pa * ad + pc * ch
            story = (f"ขายบัตรเข้าชมได้ {ad + ch} ใบ เป็นเงิน {money} บาท บัตรผู้ใหญ่ราคา {pa} บาท "
                     f"บัตรเด็กราคา {pc} บาท ให้ x แทนจำนวนบัตรผู้ใหญ่ และ y แทนจำนวนบัตรเด็ก")
            right = rf"x + y = {ad + ch},\quad {pa}x + {pc}y = {money}"
            wrongs = [rf"x + y = {ad + ch},\quad {pc}x + {pa}y = {money}",
                      rf"x + y = {money},\quad {pa}x + {pc}y = {ad + ch}",
                      rf"{pa}x + {pc}y = {ad + ch},\quad x - y = {money}"]
        elif kind == 4:
            child = rng.randint(5, 15)
            times = rng.choice((3, 4, 5))
            story = (f"ผลบวกของอายุพ่อกับอายุลูกเท่ากับ {child * (times + 1)} ปี อายุพ่อเป็น {times} เท่า"
                     f"ของอายุลูก ให้ x แทนอายุพ่อ และ y แทนอายุลูก")
            right = rf"x + y = {child * (times + 1)},\quad x = {times}y"
            wrongs = [rf"x + y = {child * (times + 1)},\quad y = {times}x",
                      rf"x - y = {child * (times + 1)},\quad x = {times}y",
                      rf"x + y = {child * (times + 1)},\quad x = y + {times}"]
        elif kind == 5:
            w, extra = rng.randint(4, 20), rng.randint(2, 12)
            per = 2 * (2 * w + extra)
            story = (f"รูปสี่เหลี่ยมผืนผ้ายาวรอบรูป {per} เซนติเมตร ด้านยาวยาวกว่าด้านกว้าง {extra} เซนติเมตร "
                     f"ให้ x แทนความยาว และ y แทนความกว้าง")
            right = rf"2x + 2y = {per},\quad x - y = {extra}"
            wrongs = [rf"x + y = {per},\quad x - y = {extra}",
                      rf"2x + 2y = {per},\quad y - x = {extra}",
                      rf"xy = {per},\quad x - y = {extra}"]
        elif kind == 0:
            x, y = rng.randint(5, 30), rng.randint(5, 30)
            story = (f"ในฟาร์มมีไก่และกระต่ายรวมกัน {x + y} ตัว นับขาได้ {2 * x + 4 * y} ขา "
                     f"ให้ x แทนจำนวนไก่ และ y แทนจำนวนกระต่าย")
            right = rf"x + y = {x + y},\quad 2x + 4y = {2 * x + 4 * y}"
            wrongs = [rf"x + y = {x + y},\quad 4x + 2y = {2 * x + 4 * y}",
                      rf"2x + 4y = {x + y},\quad x + y = {2 * x + 4 * y}",
                      rf"x + y = {x + y},\quad x + 4y = {2 * x + 4 * y}"]
        elif kind == 1:
            a, b = rng.randint(10, 60), rng.randint(5, 50)
            big, small = max(a, b), min(a, b)
            if big == small:
                big += 3
            story = (f"จำนวนสองจำนวนมีผลบวกเท่ากับ {big + small} และผลต่างเท่ากับ {big - small} "
                     f"ให้ x แทนจำนวนที่มากกว่า และ y แทนจำนวนที่น้อยกว่า")
            right = rf"x + y = {big + small},\quad x - y = {big - small}"
            wrongs = [rf"x + y = {big + small},\quad y - x = {big - small}",
                      rf"x - y = {big + small},\quad x + y = {big - small}",
                      rf"xy = {big + small},\quad x - y = {big - small}"]
        else:
            n5, n10 = rng.randint(3, 20), rng.randint(3, 20)
            story = (f"กระปุกมีเหรียญห้าบาทและเหรียญสิบบาทรวม {n5 + n10} เหรียญ คิดเป็นเงิน {5 * n5 + 10 * n10} บาท "
                     f"ให้ x แทนจำนวนเหรียญห้าบาท และ y แทนจำนวนเหรียญสิบบาท")
            right = rf"x + y = {n5 + n10},\quad 5x + 10y = {5 * n5 + 10 * n10}"
            wrongs = [rf"x + y = {n5 + n10},\quad 10x + 5y = {5 * n5 + 10 * n10}",
                      rf"5x + 10y = {n5 + n10},\quad x + y = {5 * n5 + 10 * n10}",
                      rf"x + y = {5 * n5 + 10 * n10},\quad 5x + 10y = {n5 + n10}"]
        return _maths([text(story), text("ระบบสมการใดแสดงความสัมพันธ์ในโจทย์นี้")], right, wrongs,
                      self.topic)


@question_type("math.system_word_problem", display_name={"th": "โจทย์ปัญหาระบบสมการ"},
               level={"th": "ม.2"}, topic="ระบบสมการ")
class SystemWordProblem(WordProblem):
    def expr(self, rng: Random, count_lo: int = 3, count_hi: int = 20):
        x = rng.randint(count_lo, count_hi)
        y = rng.randint(count_lo, count_hi)
        kind = rng.randrange(4)
        if kind == 0:
            adult_price = rng.randrange(40, 121, 10)
            child_price = rng.randrange(10, adult_price, 10)
            prompt = (f"ผู้ใหญ่และเด็กรวม {x + y} คน เข้าชมนิทรรศการ "
                      f"ค่าเข้าชมผู้ใหญ่คนละ {adult_price} บาท เด็กคนละ "
                      f"{child_price} บาท รวมเป็นเงิน {x * adult_price + y * child_price} บาท "
                      "มีผู้ใหญ่กี่คน")
        elif kind == 1:
            prompt = (f"ในฟาร์มมีไก่และกระต่ายรวมกัน {x + y} ตัว นับขาได้ {2 * y + 4 * x} ขา "
                      "มีกระต่ายกี่ตัว")
        elif kind == 2:
            prompt = (f"กระปุกมีเหรียญสิบบาทและเหรียญห้าบาทรวม {x + y} เหรียญ คิดเป็นเงิน "
                      f"{10 * x + 5 * y} บาท มีเหรียญสิบบาทกี่เหรียญ")
        else:
            if x == y:
                y += 1
            x, y = max(x, y), min(x, y)
            prompt = (f"จำนวนสองจำนวนมีผลบวกเท่ากับ {x + y} และผลต่างเท่ากับ {x - y} "
                      "จำนวนที่มากกว่าคือจำนวนใด")
        # The other unknown, the total, and the difference of the two.
        return MathDraw("", str(x), prompt=prompt,
                        distractors=[str(v) for v in dict.fromkeys((y, x + y, abs(x - y) or x + 1,
                                                                    x + 1)) if v != x])
