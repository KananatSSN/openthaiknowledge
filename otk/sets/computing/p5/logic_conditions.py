"""เหตุผลเชิงตรรกะกับเงื่อนไขหลายข้อ

วิทยาการคำนวณ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 4.2 ป.5/1

Sets moved here from: technology_t1s5.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t1s4 import _near
from otk.sets._support.technology_t1s5 import FIFTH, NAMES

PROVENANCE = Provenance("original")


CONDITIONS_TOPIC = "เหตุผลเชิงตรรกะกับเงื่อนไขหลายข้อ"


@question_type(
    "comp.logic_conditions_foundation",
    display_name={"th": "นับผลลัพธ์ของการทำซ้ำที่มีเงื่อนไข"},
    level=FIFTH, subject=SUBJECT, topic=CONDITIONS_TOPIC,
)
class LogicConditionsFoundation(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random, **params):
        n, d = rng.randint(10, 30), rng.randint(2, 5)
        hits = n // d
        clap_on_multiples = rng.random() < 0.5
        answer = hits if clap_on_multiples else n - hits
        rule = "หารด้วย {d} ลงตัว" if clap_on_multiples else "หารด้วย {d} ไม่ลงตัว"
        return _labelled(
            stem=(f"นับเลขตั้งแต่ 1 ถึง {n} ทีละหนึ่ง ถ้าเลขใด{rule.format(d=d)} ให้ปรบมือ 1 ครั้ง "
                  f"เมื่อนับครบ จะปรบมือทั้งหมดกี่ครั้ง"),
            correct=f"{answer} ครั้ง",
            wrongs=tuple(f"{w} ครั้ง" for w in rng.sample(
                _near(answer, (n - answer, answer + 1, answer - 1, d)), 3)),
            hint=f"เลขที่หารด้วย {d} ลงตัวคือ {d}, {2 * d}, {3 * d}, … ไปจนไม่เกิน {n} ให้นับว่ามีกี่ตัว",
            topic=CONDITIONS_TOPIC,
        )


@question_type(
    "comp.logic_conditions_fluency",
    display_name={"th": "ตัดสินด้วยเงื่อนไขที่เชื่อมด้วย และ หรือ หรือ"},
    level=FIFTH, subject=SUBJECT, topic=CONDITIONS_TOPIC,
)
class LogicConditionsFluency(QuestionType):
    """Count who meets two conditions joined by และ, or by หรือ."""

    def build(self, rng: Random, **params):
        people = rng.sample(NAMES, 5)
        heights = {p: rng.randrange(110, 146, 5) for p in people}
        ages = {p: rng.randint(6, 11) for p in people}
        min_height, min_age = rng.choice((120, 125, 130)), rng.choice((8, 9))
        tall = {p for p in people if heights[p] >= min_height}
        old = {p for p in people if ages[p] >= min_age}
        both = rng.random() < 0.5
        joined = "และ" if both else "หรือ"
        answer = len(tall & old) if both else len(tall | old)
        other = len(tall | old) if both else len(tall & old)
        listed = " ".join(f"{p} สูง {heights[p]} ซม. อายุ {ages[p]} ปี" for p in people)
        return _labelled(
            stem=(f"เด็กห้าคน ได้แก่ {listed} กติกาคือ เล่นเครื่องเล่นได้ถ้าสูงอย่างน้อย {min_height} ซม. "
                  f"{joined}อายุอย่างน้อย {min_age} ปี มีเด็กที่เล่นได้กี่คน"),
            correct=f"{answer} คน",
            wrongs=tuple(f"{w} คน" for w in rng.sample(
                _near(answer, (other, len(tall), len(old))), 3)),
            hint=("เงื่อนไขที่เชื่อมด้วย และ ต้องเป็นจริงทั้งสองข้อ "
                  "ส่วนเงื่อนไขที่เชื่อมด้วย หรือ เป็นจริงเพียงข้อเดียวก็พอ"),
            topic=CONDITIONS_TOPIC,
        )


@question_type(
    "comp.logic_conditions_application",
    display_name={"th": "เรียงลำดับด้วยเหตุผลเชิงตรรกะจากข้อมูลที่กำหนด"},
    level=FIFTH, subject=SUBJECT, topic=CONDITIONS_TOPIC,
)
class LogicConditionsApplication(QuestionType):
    """Four people, three 'taller than' clues in shuffled order."""

    def build(self, rng: Random, **params):
        order = rng.sample(NAMES, 4)          # tallest first
        clues = [f"{order[i]}สูงกว่า{order[i + 1]}" for i in range(3)]
        rng.shuffle(clues)
        kind = rng.randrange(3)
        question, answer = (("ใครสูงที่สุด", order[0]), ("ใครเตี้ยที่สุด", order[-1]),
                            ("ใครสูงเป็นอันดับสอง", order[1]))[kind]
        return _labelled(
            stem=f"{' '.join(clues)} {question}",
            correct=answer, wrongs=tuple(p for p in order if p != answer),
            hint="เรียงชื่อจากข้อมูลทีละคู่ให้ต่อกันเป็นแถวเดียว จากสูงที่สุดไปเตี้ยที่สุด",
            topic=CONDITIONS_TOPIC,
        )
