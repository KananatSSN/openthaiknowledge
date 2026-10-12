"""สมบัติของดินและการใช้ประโยชน์

ธรณีวิทยา · ม.2 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.2/7

Sets moved here from: science_wave_c21.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b8 import LEVEL as MIDDLE_TWO
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c21 import SOIL_USE_SCENARIOS

PROVENANCE = Provenance("original")


SOIL_USE_TOPIC = "สมบัติของดินและการใช้ประโยชน์"


class Tool(NamedTuple):
    """A soil property and the instrument or test suited to measuring it."""
    property: str
    tool: str


TOOLS = (
    Tool("ความเป็นกรด-เบสของดิน", "ชุดตรวจ pH ของดินหรือกระดาษยูนิเวอร์ซัลอินดิเคเตอร์"),
    Tool("เนื้อดิน", "การปั้นดินที่พรมน้ำเป็นเส้นแล้วสังเกตการจับตัว"),
    Tool("ความชื้นในดิน", "เครื่องวัดความชื้นดิน หรือการชั่งดินก่อนและหลังอบแห้ง"),
    Tool("การระบายน้ำของดิน", "การเทน้ำปริมาณเท่ากันผ่านดินในกรวย แล้วจับเวลาที่น้ำไหลผ่าน"),
    Tool("สีของดิน", "การเทียบดินกับแผ่นเทียบสีดินในที่ที่มีแสงสว่างพอ"),
    Tool("ความแน่นของดิน", "การกดแท่งเหล็กปลายแหลมลงในดินด้วยแรงเท่ากัน แล้ววัดความลึกที่กดลงไปได้"),
)


class Profile(NamedTuple):
    """A soil test result pattern and the use it supports."""
    name: str
    ph: tuple[float, float]
    texture: str
    drainage: str
    use: str


# Each profile differs on pH band or texture, so a record matches one profile.
PROFILES = (
    Profile("ดินกรดจัด", (4.0, 4.9), "ดินร่วน", "ระบายน้ำปานกลาง",
            "ใส่ปูนขาวหรือโดโลไมต์เพื่อปรับความเป็นกรดก่อนปลูกพืช"),
    Profile("ดินร่วนเป็นกลาง", (6.2, 7.2), "ดินร่วน", "ระบายน้ำปานกลาง",
            "ปลูกผักและไม้ผลได้ทันที โดยใส่ปุ๋ยอินทรีย์รักษาความสมบูรณ์"),
    Profile("ดินเหนียวระบายน้ำยาก", (5.8, 7.0), "ดินเหนียว", "ระบายน้ำช้ามาก",
            "ทำนาข้าวซึ่งต้องการน้ำขัง หรือใช้ปั้นอิฐและภาชนะดินเผา"),
    Profile("ดินทรายระบายน้ำเร็ว", (5.8, 7.0), "ดินทราย", "ระบายน้ำเร็วมาก",
            "ผสมปุ๋ยหมักเพิ่มการอุ้มน้ำ และปลูกพืชทนแล้ง เช่น มันสำปะหลัง"),
)


def soil_record(rng: Random) -> tuple[Profile, str]:
    profile = rng.choice(PROFILES)
    ph = round(rng.uniform(*profile.ph), 1)
    record = (f"pH {ph} / เนื้อดิน: {profile.texture} / การระบายน้ำ: {profile.drainage}")
    return profile, record


@question_type(
    "geo.soil_property_foundation",
    display_name={"th": "เครื่องมือตรวจวัดสมบัติของดิน"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=SOIL_USE_TOPIC,
)
class SoilPropertyFoundation(QuestionType):
    """Choose the instrument for a soil property, in either direction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(TOOLS)
        others = [other for other in TOOLS if other.property != item.property]
        if rng.random() < 0.5:
            return _labelled(
                stem=f"ถ้าต้องการตรวจวัด{item.property} ควรใช้เครื่องมือหรือวิธีใดจึงเหมาะสมที่สุด",
                correct=item.tool,
                wrongs=tuple(other.tool for other in others),
                hint="นึกว่าสมบัตินั้นวัดเป็นตัวเลข สังเกตด้วยมือ หรือจับเวลา",
                topic=SOIL_USE_TOPIC,
            )
        return _labelled(
            stem=f"“{item.tool}” ใช้ตรวจวัดสมบัติใดของดิน",
            correct=item.property,
            wrongs=tuple(other.property for other in others),
            hint="นึกว่าเครื่องมือนั้นวัดอะไรได้โดยตรง",
            topic=SOIL_USE_TOPIC,
        )


@question_type(
    "geo.soil_property_fluency",
    display_name={"th": "เสนอแนวทางใช้ประโยชน์ดินจากข้อมูลสมบัติของดิน"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=SOIL_USE_TOPIC,
)
class SoilPropertyFluency(QuestionType):
    """Propose the use a soil test record supports — the assessable second verb."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        profile, record = soil_record(rng)
        return _labelled(
            stem=f"นักเรียนตรวจวัดสมบัติของดินในแปลงหนึ่งได้ผลดังนี้ — {record} "
                 "จากข้อมูลนี้ ควรเสนอแนวทางใช้ประโยชน์ดินแปลงนี้อย่างไรจึงเหมาะสมที่สุด",
            correct=profile.use,
            wrongs=tuple(other.use for other in PROFILES if other.name != profile.name),
            hint="ดูค่า pH ก่อนว่าเป็นกรดจัดหรือไม่ แล้วดูเนื้อดินกับการระบายน้ำ",
            topic=SOIL_USE_TOPIC,
        )


@question_type(
    "geo.soil_property_application",
    display_name={"th": "วางแผนตรวจและปรับปรุงดินเพื่อการใช้ประโยชน์"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=SOIL_USE_TOPIC,
)
class SoilPropertyApplication(QuestionType):
    """Sample a plot fairly, check a lime treatment, and fix compacted soil."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SOIL_USE_SCENARIOS,
            hint="ใช้ข้อมูลสมบัติของดินตัดสินใจ และตรวจซ้ำเพื่อดูผลของการปรับปรุง",
        ), SOIL_USE_TOPIC)
