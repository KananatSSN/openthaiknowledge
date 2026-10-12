"""การใช้เหตุผลเชิงตรรกะ

วิทยาการคำนวณ · ป.4 · สสวท. พื้นฐาน
Indicators: ว 4.2 ป.4/1

Sets moved here from: technology_t1s5.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t1s4 import _near
from otk.sets._support.technology_t1s5 import FOURTH, NAMES

PROVENANCE = Provenance("original")


LOGIC_TOPIC = "การใช้เหตุผลเชิงตรรกะ"


#: (condition, its negation, what happens if it holds, what happens if not).
RULES = (
    ("ฝนตก", "ฝนไม่ตก", "แม่นำร่มไปทำงาน", "แม่นำหมวกไปทำงาน"),
    ("ไฟจราจรเป็นสีแดง", "ไฟจราจรเป็นสีเขียว", "รถหยุดรอ", "รถเคลื่อนที่ต่อไป"),
    ("น้ำในแก้วหมด", "น้ำในแก้วยังไม่หมด", "ต้นเติมน้ำใหม่", "ต้นดื่มน้ำในแก้วต่อ"),
    ("ทำการบ้านเสร็จ", "ทำการบ้านยังไม่เสร็จ", "แพรได้ดูการ์ตูน", "แพรทำการบ้านต่อ"),
    ("ถังขยะเต็ม", "ถังขยะยังไม่เต็ม", "บอยนำขยะไปทิ้งที่จุดรวมขยะ", "บอยทิ้งขยะลงถังตามปกติ"),
    ("แบตเตอรี่แท็บเล็ตเหลือไม่ถึงครึ่ง", "แบตเตอรี่แท็บเล็ตเหลือมากกว่าครึ่ง",
     "มิ้นเสียบสายชาร์จ", "มิ้นใช้แท็บเล็ตต่อ"),
    ("อากาศหนาว", "อากาศร้อน", "น้ำสวมเสื้อกันหนาว", "น้ำสวมเสื้อยืด"),
    ("ประตูห้องปิดอยู่", "ประตูห้องเปิดอยู่", "ภูมิเคาะประตูก่อนเข้า", "ภูมิเดินเข้าห้องได้เลย"),
)


PET_SETS = (("แมว", "สุนัข", "กระต่าย", "ปลา"), ("สีแดง", "สีฟ้า", "สีเขียว", "สีเหลือง"))


NOT_ENOUGH = "ข้อมูลไม่พอที่จะบอกได้"


#: (what to do to an even number, to an odd one).
MACHINES = (
    (("หารด้วย 2", lambda n: n // 2), ("บวก 1", lambda n: n + 1)),
    (("บวก 3", lambda n: n + 3), ("ลบ 1", lambda n: n - 1)),
    (("หารด้วย 2", lambda n: n // 2), ("บวก 3", lambda n: n + 3)),
)


def run_machine(machine, start: int, rounds: int) -> int:
    (_, even), (_, odd) = machine
    n = start
    for _ in range(rounds):
        n = even(n) if n % 2 == 0 else odd(n)
    return n


@question_type(
    "comp.logic_rule_foundation",
    display_name={"th": "คาดการณ์ผลลัพธ์จากเงื่อนไข ถ้า…ถ้าไม่…"},
    level=FOURTH, subject=SUBJECT, topic=LOGIC_TOPIC,
)
class LogicRuleFoundation(QuestionType):
    def build(self, rng: Random, **params):
        index = rng.randrange(len(RULES))
        condition, negation, yes, no = RULES[index]
        holds = rng.random() < 0.5
        others = [row for i, row in enumerate(RULES) if i != index]
        decoys = [rng.choice(row[2:]) for row in rng.sample(others, 2)]
        return _labelled(
            stem=(f"กติกาคือ ถ้า{condition} {yes} ถ้าไม่เป็นเช่นนั้น {no} "
                  f"ถ้าตอนนี้{condition if holds else negation} จะเกิดอะไรขึ้น"),
            correct=yes if holds else no, wrongs=(no if holds else yes, *decoys),
            hint="ตรวจว่าเงื่อนไขหลังคำว่า ถ้า เป็นจริงหรือไม่ แล้วเลือกผลลัพธ์ของกรณีนั้น",
            topic=LOGIC_TOPIC,
        )


@question_type(
    "comp.logic_rule_fluency",
    display_name={"th": "ใช้เหตุผลตัดตัวเลือกเพื่อหาคำตอบ"},
    level=FOURTH, subject=SUBJECT, topic=LOGIC_TOPIC,
)
class LogicRuleFluency(QuestionType):
    """Three people, three things, two clues: who has which."""

    def build(self, rng: Random, **params):
        a, b, c = rng.sample(NAMES, 3)
        pets = rng.random() < 0.5
        things = rng.sample(PET_SETS[0] if pets else PET_SETS[1], 3)
        owner = dict(zip((a, b, c), things))
        if pets:
            intro = f"{a} {b} และ{c} เลี้ยงสัตว์คนละชนิด คือ {' '.join(sorted(things))}"
            has, has_not, ask = "เลี้ยง", "ไม่ได้เลี้ยง", "เลี้ยงสัตว์ใด"
        else:
            intro = f"{a} {b} และ{c} ใส่เสื้อคนละสี คือ {' '.join(sorted(things))}"
            has, has_not, ask = "ใส่เสื้อ", "ไม่ได้ใส่เสื้อ", "ใส่เสื้อสีใด"
        target = rng.choice((a, c))
        return _labelled(
            stem=(f"{intro} {b}{has}{owner[b]} และ{a}{has_not}{owner[c]} {target}{ask}"),
            correct=owner[target],
            wrongs=(*[t for t in things if t != owner[target]], NOT_ENOUGH),
            hint="ตัดสิ่งที่รู้แน่แล้วว่าเป็นของใครออกทีละข้อ สิ่งที่เหลือเพียงอย่างเดียวคือคำตอบ",
            topic=LOGIC_TOPIC,
        )


@question_type(
    "comp.logic_rule_application",
    display_name={"th": "คาดการณ์ผลลัพธ์ของเครื่องจักรตัวเลขที่มีเงื่อนไข"},
    level=FOURTH, subject=SUBJECT, topic=LOGIC_TOPIC,
)
class LogicRuleApplication(QuestionType):
    def build(self, rng: Random, **params):
        index = rng.randrange(len(MACHINES))
        machine = MACHINES[index]
        (even_text, _), (odd_text, _) = machine
        start, rounds = rng.randint(3, 30), rng.randint(2, 3)
        answer = run_machine(machine, start, rounds)
        wrongs = _near(answer, (run_machine(machine, start, rounds - 1),
                                run_machine(machine, start, rounds + 1),
                                run_machine(((odd_text, machine[1][1]), (even_text, machine[0][1])),
                                            start, rounds)))
        return _labelled(
            stem=(f"เครื่องจักรตัวเลขทำงานดังนี้ ถ้าตัวเลขเป็นจำนวนคู่ ให้{even_text} "
                  f"ถ้าเป็นจำนวนคี่ ให้{odd_text} ใส่เลข {start} แล้วให้เครื่องทำงาน {rounds} ครั้งต่อกัน "
                  f"โดยนำผลแต่ละครั้งเข้าเครื่องอีก ผลลัพธ์สุดท้ายคือเท่าใด"),
            correct=str(answer), wrongs=tuple(str(w) for w in rng.sample(wrongs, 3)),
            hint="ทำทีละครั้ง ดูว่าตัวเลขตอนนั้นเป็นคู่หรือคี่ก่อนเลือกคำสั่ง แล้วนำผลไปทำครั้งถัดไป",
            topic=LOGIC_TOPIC,
        )
