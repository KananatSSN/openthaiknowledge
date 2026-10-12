"""การเขียนโปรแกรมภาษาไพทอน

วิทยาการคำนวณ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 4.2 ม.1/2

Sets moved here from: technology_t4.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t4 import M1, _fix_question, _lines, _numbers, _question

PROVENANCE = Provenance("original")


TRACE_TOPIC = "การเขียนโปรแกรมภาษาไพทอน"


TRACE_HINT = ("ไล่โปรแกรมทีละบรรทัดจากบนลงล่าง จดค่าของตัวแปรทุกครั้งที่เปลี่ยน "
              "เครื่องหมาย = หมายถึงนำค่าทางขวาไปเก็บในตัวแปรทางซ้าย")


LOOP_HINT = ("range(n) ให้ค่า 0, 1, ..., n - 1 และ range(a, b) ให้ค่า a ถึง b - 1 "
             "คำสั่งที่เยื้องเข้าไปใต้ for จะทำซ้ำทุกรอบ")


def _sequence(rng: Random):
    """(program, answer, slips): assignments and arithmetic, no loop."""
    kind = rng.randrange(4)
    if kind == 0:
        a, b, c = rng.randint(2, 9), rng.randint(2, 9), rng.randint(2, 5)
        op1, op2 = rng.choice("+*-"), rng.choice("+*")
        if op1 == "-":
            a, b = max(a, b), min(a, b)
        first = {"+": a + b, "-": a - b, "*": a * b}[op1]
        answer = first + c if op2 == "+" else first * c
        return (_lines(f"a = {a}", f"b = {b}", f"c = a {op1} b", f"c = c {op2} {c}", "print(c)"),
                answer, (first, a + b + c, answer + c))
    if kind == 1:
        speed, time = rng.randint(3, 20), rng.randint(2, 12)
        return (_lines(f"speed = {speed}", f"time = {time}", "distance = speed * time", "print(distance)"),
                speed * time, (speed + time, speed, time * 2))
    if kind == 2:
        a, b = rng.randint(2, 30), rng.randint(2, 30)
        return (_lines(f"x = {a}", f"y = {b}", "x = x + y", "y = x - y", "print(y)"),
                a, (b, a + b, a - b if a > b else b - a))
    price, count = rng.randint(5, 25), rng.randint(2, 6)
    paid = (price * count // 50 + 1) * 50
    return (_lines(f"price = {price}", f"count = {count}", f"paid = {paid}", "total = price * count",
                   "change = paid - total", "print(change)"),
            paid - price * count, (price * count, paid - price, paid - price - count))


def _loop(rng: Random):
    """(program, answer, slips): one ``for`` loop."""
    kind = rng.randrange(5)
    if kind == 0:
        n, k = rng.randint(3, 8), rng.randint(2, 9)
        return (_lines("total = 0", f"for i in range({n}):", f"    total = total + {k}", "print(total)"),
                n * k, ((n - 1) * k, (n + 1) * k, n + k))
    if kind == 1:
        n = rng.randint(4, 9)
        return (_lines("total = 0", f"for i in range(1, {n}):", "    total = total + i", "print(total)"),
                n * (n - 1) // 2, (n * (n + 1) // 2, n, (n - 1) * (n - 2) // 2))
    if kind == 2:
        a, b = rng.randint(1, 6), rng.randint(9, 20)
        return (_lines("count = 0", f"for i in range({a}, {b}):", "    count = count + 1", "print(count)"),
                b - a, (b - a + 1, b - a - 1, b))
    if kind == 3:
        height, days, growth = rng.randint(2, 15), rng.randint(3, 7), rng.randint(2, 5)
        return (_lines(f"height = {height}", f"for day in range({days}):", f"    height = height + {growth}",
                       "print(height)"),
                height + days * growth, (days * growth, height + (days - 1) * growth, height + growth))
    n = rng.randint(2, 6)
    return (_lines("x = 1", f"for i in range({n}):", "    x = x * 2", "print(x)"),
            2 ** n, (2 ** (n - 1), 2 ** (n + 1), 2 * n))


def _area(rng: Random):
    w, h = rng.randint(3, 9), rng.randint(3, 9)
    return (f"หาพื้นที่ของรูปสี่เหลี่ยมผืนผ้ากว้าง {w} หน่วย ยาว {h} หน่วย",
            _lines(f"width = {w}", f"height = {h}", "area = width * height", "print(area)"))


def _perimeter(rng: Random):
    w, h = rng.randint(3, 9), rng.randint(3, 9)
    return (f"หาความยาวรอบรูปของรูปสี่เหลี่ยมผืนผ้ากว้าง {w} หน่วย ยาว {h} หน่วย",
            _lines(f"width = {w}", f"height = {h}", "perimeter = 2 * (width + height)", "print(perimeter)"))


def _distance(rng: Random):
    s, t = rng.randint(3, 15), rng.randint(2, 10)
    return (f"หาระยะทางที่รถวิ่งได้ด้วยอัตราเร็ว {s} เมตรต่อวินาที เป็นเวลา {t} วินาที",
            _lines(f"speed = {s}", f"time = {t}", "distance = speed * time", "print(distance)"))


def _change(rng: Random):
    price, count = rng.randint(5, 25), rng.randint(2, 6)
    paid = (price * count // 50 + 1) * 50
    return (f"หาเงินทอนเมื่อซื้อสมุด {count} เล่ม เล่มละ {price} บาท แล้วจ่ายเงิน {paid} บาท",
            _lines(f"price = {price}", f"count = {count}", f"paid = {paid}", "total = price * count",
                   "change = paid - total", "print(change)"))


def _warming(rng: Random):
    start = rng.randint(20, 30)
    end = start + rng.randint(3, 12)
    return (f"หาว่าอุณหภูมิของน้ำเพิ่มขึ้นกี่องศาเซลเซียส เมื่อเปลี่ยนจาก {start} เป็น {end} องศาเซลเซียส",
            _lines(f"start = {start}", f"end = {end}", "rise = end - start", "print(rise)"))


def _sum_to(rng: Random):
    n = rng.randint(4, 10)
    return (f"หาผลบวกของจำนวนนับตั้งแต่ 1 ถึง {n}",
            _lines(f"n = {n}", "total = 0", "for i in range(1, n + 1):", "    total = total + i", "print(total)"))


M1_FIXES = (_area, _perimeter, _distance, _change, _warming, _sum_to)


@question_type(
    "comp.code_trace_foundation",
    display_name={"th": "ไล่โปรแกรมที่มีการกำหนดค่าและคำนวณ"},
    level=M1, subject=SUBJECT, topic=TRACE_TOPIC,
)
class CodeTraceFoundation(QuestionType):
    def build(self, rng: Random, **params):
        program, answer, slips = _sequence(rng)
        return _question("โปรแกรมภาษาไพทอนต่อไปนี้แสดงผลเป็นเท่าใด", program, str(answer),
                         _numbers(rng, answer, slips), TRACE_HINT, TRACE_TOPIC)


@question_type(
    "comp.code_trace_fluency",
    display_name={"th": "ไล่โปรแกรมที่มีการวนซ้ำด้วย for"},
    level=M1, subject=SUBJECT, topic=TRACE_TOPIC,
)
class CodeTraceFluency(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random, **params):
        program, answer, slips = _loop(rng)
        return _question("โปรแกรมภาษาไพทอนต่อไปนี้แสดงผลเป็นเท่าใด", program, str(answer),
                         _numbers(rng, answer, slips), LOOP_HINT, TRACE_TOPIC)


@question_type(
    "comp.code_trace_application",
    display_name={"th": "แก้โปรแกรมคณิตศาสตร์และวิทยาศาสตร์ให้ถูกต้อง"},
    level=M1, subject=SUBJECT, topic=TRACE_TOPIC,
)
class CodeTraceApplication(QuestionType):
    def build(self, rng: Random, **params):
        return _fix_question(rng, M1_FIXES, TRACE_TOPIC)
