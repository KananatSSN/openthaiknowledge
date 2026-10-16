"""ทักษะกระบวนการทางวิทยาศาสตร์ ป.5

วิทยาศาสตร์ทั่วไป · ป.5 · เสริมทักษะ
Indicators: —

Filed like the ม.1 and ป.4 units (บทนำ, no ตัวชี้วัด). ป.5 practises the skills
that work with numbers: measuring with the right tool and unit, reading data a
class has recorded in a table, and predicting the next value from a pattern.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_g4 import SUBJECT

PROVENANCE = Provenance("original")


PRIMARY_FIVE = {"th": "ป.5"}


PROCESS_SKILL_TOPIC = "ทักษะกระบวนการทางวิทยาศาสตร์"


class Quantity(NamedTuple):
    """One kind of quantity, the tool a ป.5 class uses for it, and its unit."""
    tool: str
    unit: str
    things: tuple[str, ...]


QUANTITIES = (
    Quantity("ไม้บรรทัด", "เซนติเมตร",
             ("ความยาวของดินสอ", "ความกว้างของใบไม้", "ความยาวของหนอนผีเสื้อ")),
    Quantity("เทอร์มอมิเตอร์", "องศาเซลเซียส",
             ("อุณหภูมิของน้ำในแก้ว", "อุณหภูมิของอากาศในห้องเรียน", "อุณหภูมิของน้ำแข็งที่กำลังละลาย")),
    Quantity("เครื่องชั่ง", "กรัม",
             ("มวลของผลส้ม", "มวลของก้อนหิน", "มวลของดินในกระถาง")),
    Quantity("กระบอกตวง", "มิลลิลิตร",
             ("ปริมาตรของน้ำในขวด", "ปริมาตรของนมในกล่อง", "ปริมาตรของน้ำฝนที่รองได้ในหนึ่งวัน")),
    Quantity("นาฬิกาจับเวลา", "วินาที",
             ("เวลาที่ลูกบอลกลิ้งลงพื้นเอียง", "เวลาที่น้ำแข็งก้อนเล็กละลายหมด", "เวลาที่ใช้วิ่งรอบสนาม")),
    Quantity("เครื่องชั่งสปริง", "นิวตัน",
             ("แรงที่ใช้ดึงกล่องบนพื้น", "น้ำหนักของถุงทราย", "แรงที่ใช้ยกถังน้ำ")),
    Quantity("ตลับเมตร", "เมตร",
             ("ความยาวของห้องเรียน", "ความสูงของเสาธง", "ความยาวของสนามฟุตบอล")),
)


def _pair(tool: str, unit: str) -> str:
    return f"ใช้{tool} และบอกหน่วยเป็น{unit}"


@question_type(
    "sci.process_skill_p5_foundation",
    display_name={"th": "เลือกเครื่องมือและหน่วยในการวัด"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillP5Foundation(QuestionType):
    """The tool and the unit together; a wrong choice gets one or both wrong."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        quantity = rng.choice(QUANTITIES)
        thing = rng.choice(quantity.things)
        others = [q for q in QUANTITIES if q.tool != quantity.tool]
        rng.shuffle(others)
        return _labelled(
            stem=f"นักเรียนต้องการวัด{thing} ควรใช้เครื่องมือใด และบอกหน่วยอย่างไร",
            correct=_pair(quantity.tool, quantity.unit),
            # Right tool with a wrong unit, a wrong tool with the right unit,
            # and a whole wrong pair.
            wrongs=(_pair(quantity.tool, others[0].unit),
                    _pair(others[1].tool, quantity.unit),
                    _pair(others[2].tool, others[2].unit),
                    _pair(quantity.tool, others[3].unit)),
            hint="ถามก่อนว่าต้องการรู้ความยาว อุณหภูมิ มวล ปริมาตร เวลา หรือแรง แล้วจึงเลือกเครื่องมือและหน่วยของสิ่งนั้น",
            topic=PROCESS_SKILL_TOPIC,
        )


TIMES = ("08.00 น.", "10.00 น.", "12.00 น.", "14.00 น.", "16.00 น.")


def temperature_record(rng: Random) -> list[int]:
    """A day's air temperatures that rise to one peak and fall, all distinct."""
    peak = rng.randrange(1, 4)
    base = rng.randint(24, 28)
    values = [base]
    for i in range(1, len(TIMES)):
        step = rng.randint(1, 3)
        values.append(values[-1] + step if i <= peak else values[-1] - step)
    if len(set(values)) < len(values):
        return temperature_record(rng)
    return values


@question_type(
    "sci.process_skill_p5_fluency",
    display_name={"th": "อ่านข้อมูลจากตารางบันทึกผล"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillP5Fluency(QuestionType):
    """A recorded table of air temperature through one day, read three ways."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        values = temperature_record(rng)
        table = " / ".join(f"{t} {v} องศาเซลเซียส" for t, v in zip(TIMES, values))
        stem = f"นักเรียนวัดอุณหภูมิของอากาศหน้าห้องเรียนในวันหนึ่ง บันทึกได้ดังนี้ {table} "
        kind = rng.randrange(3)
        if kind < 2:
            pick = max if kind == 0 else min
            word = "สูงที่สุด" if kind == 0 else "ต่ำที่สุด"
            target = TIMES[values.index(pick(values))]
            return _labelled(
                stem=stem + f"จากตาราง อุณหภูมิ{word}ในเวลาใด",
                correct=target,
                wrongs=tuple(t for t in TIMES if t != target),
                hint="อ่านตัวเลขทุกช่องในตาราง แล้วเทียบกันทีละค่า",
                topic=PROCESS_SKILL_TOPIC,
            )
        i, j = sorted(rng.sample(range(len(TIMES)), 2))
        high, low = max(values[i], values[j]), min(values[i], values[j])
        return numeric(
            stem=stem + f"จากตาราง อุณหภูมิเวลา {TIMES[i]} กับเวลา {TIMES[j]} ต่างกันกี่องศาเซลเซียส",
            answer=high - low,
            # Reading one of the two values instead of the difference, or adding them.
            wrongs=(high, low, high + low),
            unit="องศาเซลเซียส",
            hint="หาค่าของทั้งสองเวลาก่อน แล้วนำค่ามากลบด้วยค่าน้อย",
            topic=PROCESS_SKILL_TOPIC,
        )


class Pattern(NamedTuple):
    """Something that changes by the same amount each step, and how it is said."""
    what: str
    unit: str
    step_word: str
    start: tuple[int, int]
    change: tuple[int, int]
    rising: bool


PATTERNS = (
    Pattern("ความสูงของต้นถั่ว", "เซนติเมตร", "วันที่", (3, 8), (1, 4), True),
    Pattern("จำนวนเมล็ดที่งอกรวมทั้งหมด", "เมล็ด", "วันที่", (2, 6), (2, 5), True),
    Pattern("มวลของน้ำแข็งที่เหลืออยู่", "กรัม", "นาทีที่", (90, 120), (5, 9), False),
    Pattern("ความสูงที่ลูกบอลกระดอนขึ้น", "เซนติเมตร", "ครั้งที่", (80, 100), (8, 12), False),
)


@question_type(
    "sci.process_skill_p5_application",
    display_name={"th": "พยากรณ์จากแบบรูปของข้อมูล"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillP5Application(QuestionType):
    """Four recorded values change by a fixed amount; predict a later one."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        pattern = rng.choice(PATTERNS)
        start = rng.randint(*pattern.start)
        step = rng.randint(*pattern.change) * (1 if pattern.rising else -1)
        values = [start + step * i for i in range(4)]
        ahead = rng.choice((2, 3))
        target = 4 + ahead
        answer = start + step * (target - 1)
        table = " / ".join(f"{pattern.step_word} {i + 1}: {v} {pattern.unit}" for i, v in enumerate(values))
        return numeric(
            stem=(f"นักเรียนบันทึก{pattern.what}ได้ดังนี้ {table} "
                  f"ถ้าแบบรูปนี้ยังคงเดิม {pattern.step_word} {target} จะมีค่าเท่าใด"),
            answer=answer,
            # The next value only, one step too many, and the change taken the wrong way.
            wrongs=(values[-1] + step, answer + step, values[-1] - step * ahead),
            unit=pattern.unit,
            hint="หาก่อนว่าค่าเปลี่ยนไปเท่าใดในแต่ละช่วง แล้วนับว่าต้องเปลี่ยนต่ออีกกี่ช่วงจึงถึงค่าที่ถาม",
            topic=PROCESS_SKILL_TOPIC,
        )
