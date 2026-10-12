"""ตรรกะและฟังก์ชันในโปรแกรม

วิทยาการคำนวณ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 4.2 ม.2/2

Sets moved here from: technology_t4.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t4 import M2, _fix_question, _lines, _numbers, _question

PROVENANCE = Provenance("original")


LOGIC_TOPIC = "ตรรกะและฟังก์ชันในโปรแกรม"


IF_HINT = ("ตรวจเงื่อนไขจากบนลงล่าง ทำเฉพาะส่วนของเงื่อนไขแรกที่เป็นจริง ถ้าไม่มีเงื่อนไขใดจริงจึงทำส่วน else "
           "ระวัง >= และ <= ซึ่งรวมกรณีที่เท่ากัน")


FUNC_HINT = ("เมื่อเรียกฟังก์ชัน ค่าในวงเล็บจะถูกส่งไปแทนพารามิเตอร์ตามลำดับ "
             "แล้ว return ส่งผลลัพธ์กลับมาแทนที่การเรียกฟังก์ชันนั้น")


GRADES = (("score", (80, 70, 60), ("A", "B", "C", "F")),
          ("temp", (35, 25, 15), ("hot", "warm", "cool", "cold")))


def _function(rng: Random):
    """(program, answer, slips): a function defined, then called."""
    kind = rng.randrange(5)
    if kind == 0:
        a, b, c, d = (rng.randint(2, 9) for _ in range(4))
        return (_lines("def area(w, h):", "    return w * h", "", f"print(area({a}, {b}) + area({c}, {d}))"),
                a * b + c * d, (a * b, a + b + c + d, (a + c) * (b + d)))
    if kind == 1:
        m, k, a = rng.randint(2, 3), rng.randint(1, 5), rng.randint(1, 6)
        once = a * m + k
        return (_lines("def f(x):", f"    return x * {m} + {k}", "", f"print(f(f({a})))"),
                once * m + k, (once, once * m, once + k))
    if kind == 2:
        x, y = rng.sample(range(2, 20), 2)
        return (_lines("def bigger(a, b):", "    if a > b:", "        return a", "    return b", "",
                       f"print(bigger({x}, {y}) * 2)"),
                max(x, y) * 2, (min(x, y) * 2, max(x, y), x + y))
    if kind == 3:
        h, m = rng.randint(1, 4), rng.randint(5, 55)
        return (_lines("def to_minutes(hours, minutes):", "    return hours * 60 + minutes", "",
                       f"print(to_minutes({h}, {m}))"),
                h * 60 + m, (h + m, h * 100 + m, h * 60))
    n = rng.randint(5, 15)
    return (_lines("def count_even(n):", "    count = 0", "    for i in range(1, n + 1):",
                   "        if i % 2 == 0:", "            count = count + 1", "    return count", "",
                   f"print(count_even({n}))"),
            n // 2, (n - n // 2, n, n // 2 + 1))


def _parity(rng: Random):
    n = rng.randint(3, 40)
    return (f"บอกว่า {n} เป็นจำนวนคู่ (even) หรือจำนวนคี่ (odd)",
            _lines(f"n = {n}", "if n % 2 == 0:", '    print("even")', "else:", '    print("odd")'))


def _pass_mark(rng: Random):
    score = rng.choice((49, 50, 50, 51, rng.randint(30, 80)))
    return (f"ตัดสินผลสอบของผู้ที่ได้ {score} คะแนน โดยได้ตั้งแต่ 50 คะแนนขึ้นไปถือว่าผ่าน (pass) ไม่ถึงถือว่าไม่ผ่าน (fail)",
            _lines(f"score = {score}", "if score >= 50:", '    print("pass")', "else:", '    print("fail")'))


def _ticket(rng: Random):
    age = rng.choice((11, 12, 12, 13, rng.randint(5, 40)))
    return (f"หาค่าเข้าชมของผู้ที่อายุ {age} ปี โดยผู้ที่อายุต่ำกว่า 12 ปีจ่าย 20 บาท ผู้อื่นจ่าย 50 บาท",
            _lines(f"age = {age}", "if age < 12:", "    price = 20", "else:", "    price = 50", "print(price)"))


def _bigger(rng: Random):
    x, y = rng.sample(range(2, 30), 2)
    return (f"หาจำนวนที่มากกว่าระหว่าง {x} กับ {y} ด้วยฟังก์ชัน",
            _lines("def bigger(a, b):", "    if a > b:", "        return a", "    return b", "",
                   f"print(bigger({x}, {y}))"))


def _multiples(rng: Random):
    n = rng.randint(7, 20)
    return (f"นับจำนวนนับตั้งแต่ 1 ถึง {n} ที่หารด้วย 3 ลงตัว",
            _lines(f"n = {n}", "count = 0", "for i in range(1, n + 1):", "    if i % 3 == 0:",
                   "        count = count + 1", "print(count)"))


def _rooms(rng: Random):
    a, b, c, d = (rng.randint(2, 9) for _ in range(4))
    return (f"หาพื้นที่รวมของห้องขนาด {a} × {b} เมตร และห้องขนาด {c} × {d} เมตร ด้วยฟังก์ชัน",
            _lines("def area(w, h):", "    return w * h", "", f"print(area({a}, {b}) + area({c}, {d}))"))


M2_FIXES = (_parity, _pass_mark, _ticket, _bigger, _multiples, _rooms)


@question_type(
    "comp.code_logic_foundation",
    display_name={"th": "ไล่โปรแกรมที่มีเงื่อนไข if elif else"},
    level=M2, subject=SUBJECT, topic=LOGIC_TOPIC,
)
class CodeLogicFoundation(QuestionType):
    """An if/elif/else ladder, often right on a boundary; or a condition joined by and/or."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params):
        if rng.random() < 0.6:
            name, cuts, labels = rng.choice(GRADES)
            sign = rng.choice((">=", ">"))
            value = rng.choice(cuts) + rng.choice((-1, 0, 0, 1))
            program = _lines(f"{name} = {value}",
                             f"if {name} {sign} {cuts[0]}:", f'    print("{labels[0]}")',
                             f"elif {name} {sign} {cuts[1]}:", f'    print("{labels[1]}")',
                             f"elif {name} {sign} {cuts[2]}:", f'    print("{labels[2]}")',
                             "else:", f'    print("{labels[3]}")')
            passes = [value >= c if sign == ">=" else value > c for c in cuts]
            answer = labels[passes.index(True)] if any(passes) else labels[3]
            return _question("โปรแกรมภาษาไพทอนต่อไปนี้แสดงผลเป็นข้อใด", program, answer,
                             [label for label in labels if label != answer], IF_HINT, LOGIC_TOPIC)
        x = rng.randint(4, 20)
        limit = rng.randint(6, 14)
        joint = rng.choice(("and", "or"))
        times, add = rng.randint(2, 3), rng.randint(3, 9)
        program = _lines(f"x = {x}", f"if x % 2 == 0 {joint} x > {limit}:", f"    x = x * {times}",
                         "else:", f"    x = x + {add}", "print(x)")
        even, big = x % 2 == 0, x > limit
        taken = (even and big) if joint == "and" else (even or big)
        answer = x * times if taken else x + add
        other = x + add if taken else x * times
        return _question("โปรแกรมภาษาไพทอนต่อไปนี้แสดงผลเป็นเท่าใด", program, str(answer),
                         _numbers(rng, answer, (other, x, answer + 1)), IF_HINT, LOGIC_TOPIC)


@question_type(
    "comp.code_logic_fluency",
    display_name={"th": "ไล่โปรแกรมที่เรียกใช้ฟังก์ชัน"},
    level=M2, subject=SUBJECT, topic=LOGIC_TOPIC,
)
class CodeLogicFluency(QuestionType):
    def build(self, rng: Random, **params):
        program, answer, slips = _function(rng)
        return _question("โปรแกรมภาษาไพทอนต่อไปนี้แสดงผลเป็นเท่าใด", program, str(answer),
                         _numbers(rng, answer, slips), FUNC_HINT, LOGIC_TOPIC)


@question_type(
    "comp.code_logic_application",
    display_name={"th": "แก้ตรรกะหรือฟังก์ชันในโปรแกรมให้ถูกต้อง"},
    level=M2, subject=SUBJECT, topic=LOGIC_TOPIC,
)
class CodeLogicApplication(QuestionType):
    def build(self, rng: Random, **params):
        return _fix_question(rng, M2_FIXES, LOGIC_TOPIC)
