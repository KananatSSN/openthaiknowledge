"""การเปลี่ยนแปลงแทนที่ของระบบนิเวศ

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.1 ม.4/2

Sets moved here from: science_wave_b33.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b19 import UPPER_FOUR, Fact, _fact_question
from otk.sets._support.science_wave_b31 import ECOLOGY_TOPIC
from otk.sets._support.science_wave_b33 import SUCCESSION_SCENARIOS

PROVENANCE = Provenance("original")


PRIMARY = "ปฐมภูมิ"


SECONDARY = "ทุติยภูมิ"


class Succession(NamedTuple):
    """A case of succession and which kind it is."""
    case: str
    kind: str


SUCCESSIONS = (
    Succession("ลาวาจากภูเขาไฟเย็นตัวเป็นพื้นหินใหม่ แล้วค่อย ๆ มีสิ่งมีชีวิตเข้ามาอาศัย",
               PRIMARY),
    Succession("เกาะที่เกิดใหม่จากภูเขาไฟใต้ทะเลค่อย ๆ มีพืชขึ้นปกคลุม", PRIMARY),
    Succession("พื้นหินเปล่าที่ธารน้ำแข็งละลายถอยร่นไปค่อย ๆ มีไลเคนและมอสขึ้น",
               PRIMARY),
    Succession("เนินทรายชายฝั่งที่เกิดขึ้นใหม่ค่อย ๆ มีพืชคลุมดินขึ้น", PRIMARY),
    Succession("ไร่ข้าวโพดที่ถูกทิ้งร้างค่อย ๆ มีหญ้าและไม้พุ่มขึ้นจนกลายเป็นป่าละเมาะ",
               SECONDARY),
    Succession("ป่าที่ถูกไฟไหม้ค่อย ๆ มีพืชงอกขึ้นใหม่จากดินและเมล็ดที่เหลืออยู่",
               SECONDARY),
    Succession("ป่าที่ถูกตัดโค่นค่อย ๆ มีต้นไม้ขึ้นทดแทนจนกลับเป็นป่าอีกครั้ง", SECONDARY),
    Succession("ทุ่งหญ้าหลังน้ำท่วมใหญ่ค่อย ๆ มีพืชขึ้นใหม่บนดินเดิม", SECONDARY),
)


# Changes that come and go with the seasons or the day. None replaces one
# community with another, so none is succession.
NOT_SUCCESSION = (
    "ใบไม้ในป่าผลัดใบเปลี่ยนสีและร่วงในฤดูหนาว แล้วแตกใบใหม่ในฤดูใบไม้ผลิ",
    "นกอพยพบินมาอาศัยในบึงช่วงฤดูหนาว แล้วบินกลับเมื่ออากาศอุ่นขึ้น",
    "ดอกบัวในสระบานตอนเช้าและหุบตอนเย็นทุกวัน",
    "ยุงในหมู่บ้านเพิ่มจำนวนในฤดูฝนและลดลงในฤดูแล้งทุกปี",
)


KIND_VERDICTS = {
    PRIMARY: "แบบปฐมภูมิ เพราะเริ่มต้นบนพื้นที่ที่ไม่เคยมีดินหรือสิ่งมีชีวิตมาก่อน",
    SECONDARY: "แบบทุติยภูมิ เพราะเริ่มต้นบนพื้นที่ที่ยังมีดิน เมล็ด หรือรากของพืชเดิมเหลืออยู่",
}


WRONG_VERDICTS = (
    "แบบปฐมภูมิ เพราะเป็นการเปลี่ยนแปลงครั้งแรกหลังจากมนุษย์เข้าไปรบกวน",
    "ไม่ใช่การเปลี่ยนแปลงแทนที่ เพราะสิ่งมีชีวิตกลับมาเหมือนเดิมทุกปี",
)


SUCCESSION_ORDER = ("ไลเคน", "มอส", "พืชล้มลุกและหญ้า", "ไม้พุ่ม", "ไม้ยืนต้น")


CAUSE_FACTS = (
    Fact("เหตุใดไลเคนจึงเป็นสิ่งมีชีวิตกลุ่มแรกที่ขึ้นบนพื้นหินเปล่าได้",
         "ไลเคนทนความแห้งแล้งได้ดีและไม่ต้องอาศัยดิน "
         "อีกทั้งปล่อยสารที่ช่วยให้หินผุกร่อน"),
    Fact("เหตุใดมอสจึงเข้ามาแทนที่ไลเคนได้",
         "หินที่ผุผสมกับซากไลเคนเกิดเป็นดินชั้นบาง ๆ ที่อุ้มน้ำได้พอให้มอสขึ้น"),
    Fact("เหตุใดสิ่งมีชีวิตที่ขึ้นก่อนจึงมักถูกสิ่งมีชีวิตที่ขึ้นทีหลังแทนที่",
         "สิ่งมีชีวิตที่ขึ้นก่อนเปลี่ยนสภาพแวดล้อม เช่น เพิ่มดินและร่มเงา "
         "จนเหมาะกับชนิดใหม่มากกว่าตัวเอง"),
    Fact("เหตุใดการเปลี่ยนแปลงแทนที่แบบทุติยภูมิจึงดำเนินไปเร็วกว่าแบบปฐมภูมิ",
         "เพราะมีดิน เมล็ด และรากเดิมเหลืออยู่ ไม่ต้องรอให้เกิดดินขึ้นใหม่"),
    Fact("สาเหตุจากธรรมชาติที่ทำให้เกิดการเปลี่ยนแปลงแทนที่มีอะไรบ้าง",
         "ภูเขาไฟระเบิด ไฟป่าจากฟ้าผ่า น้ำท่วมใหญ่ และดินถล่ม"),
    Fact("สาเหตุจากการกระทำของมนุษย์ที่ทำให้เกิดการเปลี่ยนแปลงแทนที่มีอะไรบ้าง",
         "การตัดไม้ทำลายป่า การเปิดพื้นที่ทำไร่แล้วทิ้งร้าง และการจุดไฟเผาป่า"),
    Fact("เหตุใดชนิดของสิ่งมีชีวิตจึงมักเพิ่มขึ้นเมื่อการเปลี่ยนแปลงแทนที่ดำเนินไป",
         "ดินหนาขึ้นและพืชมีหลายชั้นมากขึ้น จึงเกิดที่อยู่และแหล่งอาหารหลายแบบ"),
)


@question_type(
    "ecology.succession_foundation",
    display_name={"th": "ตัวอย่างการเปลี่ยนแปลงแทนที่"},
    level=UPPER_FOUR, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class SuccessionFoundation(QuestionType):
    """Recognise examples of succession, and of each of its two kinds."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "ถามว่าพื้นที่นั้นมีดินอยู่ก่อนหรือไม่ และสิ่งมีชีวิตชุดเดิมถูกแทนที่จริงหรือไม่"
        branch = rng.random()
        if branch < 0.35:
            kind = rng.choice((PRIMARY, SECONDARY))
            item = rng.choice([one for one in SUCCESSIONS if one.kind == kind])
            others = [one.case for one in SUCCESSIONS if one.kind != kind]
            rng.shuffle(others)
            return _labelled(
                stem=f"ข้อใดเป็นตัวอย่างของการเปลี่ยนแปลงแทนที่แบบ{kind}",
                correct=item.case, wrongs=tuple(others[:3]), hint=hint,
                topic=ECOLOGY_TOPIC,
            )
        if branch < 0.6:
            item = rng.choice(SUCCESSIONS)
            others = list(NOT_SUCCESSION)
            rng.shuffle(others)
            return _labelled(
                stem="ข้อใดเป็นตัวอย่างของการเปลี่ยนแปลงแทนที่ของระบบนิเวศ",
                correct=item.case, wrongs=tuple(others[:3]), hint=hint,
                topic=ECOLOGY_TOPIC,
            )
        item = rng.choice(SUCCESSIONS)
        other = PRIMARY if item.kind == SECONDARY else SECONDARY
        return _labelled(
            stem=f"“{item.case}” เป็นการเปลี่ยนแปลงแทนที่แบบใด",
            correct=KIND_VERDICTS[item.kind],
            wrongs=(KIND_VERDICTS[other], *WRONG_VERDICTS),
            hint=hint, topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.succession_fluency",
    display_name={"th": "อภิปรายสาเหตุของการเปลี่ยนแปลงแทนที่"},
    level=UPPER_FOUR, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class SuccessionFluency(QuestionType):
    """Discuss what causes succession and what drives each replacement."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            return _fact_question(
                rng, CAUSE_FACTS, topic=ECOLOGY_TOPIC,
                hint="สิ่งมีชีวิตแต่ละกลุ่มเปลี่ยนสภาพแวดล้อมรอบตัว "
                     "จนเปิดทางให้กลุ่มถัดไป",
            )
        index = rng.randrange(len(SUCCESSION_ORDER) - 1)
        current = SUCCESSION_ORDER[index]
        answer = SUCCESSION_ORDER[index + 1]
        wrongs = tuple(stage for stage in SUCCESSION_ORDER
                       if stage not in (current, answer))
        return _labelled(
            stem="ในการเปลี่ยนแปลงแทนที่แบบปฐมภูมิบนพื้นหินเปล่า "
                 f"สิ่งมีชีวิตกลุ่มใดเข้ามาแทนที่ถัดจาก “{current}”",
            correct=answer, wrongs=wrongs,
            hint="กลุ่มถัดไปต้องการดินและน้ำมากกว่ากลุ่มเดิมเล็กน้อย "
                 "ซึ่งกลุ่มเดิมเป็นผู้สร้างไว้ให้",
            topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.succession_application",
    display_name={"th": "วิเคราะห์การเปลี่ยนแปลงแทนที่ของระบบนิเวศ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class SuccessionApplication(QuestionType):
    """Compare two recoveries, or predict where one is heading."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SUCCESSION_SCENARIOS,
            hint="ถามว่าจุดเริ่มต้นมีดินหรือไม่ และมีสิ่งใดรบกวนซ้ำระหว่างทาง",
        ), ECOLOGY_TOPIC)
