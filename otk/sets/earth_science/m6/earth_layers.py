"""การแบ่งชั้นและสมบัติของโครงสร้างโลก

ธรณีวิทยา · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.6/1

Sets moved here from: science_wave_c22.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c22 import STRUCTURE_SCENARIOS, SUPPORTING_DATA, _matching_item

PROVENANCE = Provenance("original")


STRUCTURE_TOPIC = "การแบ่งชั้นและสมบัติของโครงสร้างโลก"


class PhysicalLayer(NamedTuple):
    """A layer of the Earth by physical property."""
    name: str
    property: str


PHYSICAL_LAYERS = (
    PhysicalLayer("ธรณีภาค", "ชั้นนอกสุดที่เป็นของแข็งแกร่ง ประกอบด้วยเปลือกโลกและเนื้อโลกส่วนบนสุด แตกเป็นแผ่นธรณี"),
    PhysicalLayer("ฐานธรณีภาค", "ชั้นเนื้อโลกที่ร้อนจนหินบางส่วนหลอมเหลว จึงอ่อนและไหลได้ช้า ๆ รองรับแผ่นธรณี"),
    PhysicalLayer("มีโซสเฟียร์", "ชั้นเนื้อโลกตอนล่างที่เป็นของแข็งเพราะความดันสูงมาก"),
    PhysicalLayer("แก่นโลกชั้นนอก", "ชั้นที่เป็นของเหลว ประกอบด้วยเหล็กและนิกเกิลหลอมเหลว คลื่นทุติยภูมิผ่านไม่ได้"),
    PhysicalLayer("แก่นโลกชั้นใน", "ชั้นในสุดที่เป็นของแข็ง ประกอบด้วยเหล็กและนิกเกิล มีความดันและอุณหภูมิสูงที่สุด"),
)


@question_type(
    "geo.earth_layers_foundation",
    display_name={"th": "ข้อมูลที่สนับสนุนการแบ่งชั้นของโลก"},
    level=UPPER_SIX, subject=SUBJECT, topic=STRUCTURE_TOPIC,
)
class EarthLayersFoundation(QuestionType):
    """Give the data that supports a claim about the interior — the free verb ยกตัวอย่าง."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SUPPORTING_DATA,
            hint="ภายในโลกศึกษาจากคลื่นไหวสะเทือน ความหนาแน่น และอุกกาบาต",
        ), STRUCTURE_TOPIC)


@question_type(
    "geo.earth_layers_fluency",
    display_name={"th": "อธิบายการแบ่งชั้นและสมบัติของโครงสร้างโลก"},
    level=UPPER_SIX, subject=SUBJECT, topic=STRUCTURE_TOPIC,
)
class EarthLayersFluency(QuestionType):
    """Place all five physical layers against their properties; each wrong choice swaps two."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _matching_item(
            rng, [layer.name for layer in PHYSICAL_LAYERS], [layer.property for layer in PHYSICAL_LAYERS],
            intro="สมบัติของโครงสร้างโลก 5 ชั้น เมื่อแบ่งตามสมบัติเชิงกล",
            question="ข้อใดจับคู่ธรณีภาค ฐานธรณีภาค มีโซสเฟียร์ แก่นโลกชั้นนอก และแก่นโลกชั้นใน กับสมบัติได้ถูกต้องทั้งหมด",
            hint="เรียงจากนอกเข้าใน: แข็งแกร่ง อ่อนไหลได้ แข็งเพราะความดัน ของเหลว และของแข็งในสุด",
            topic=STRUCTURE_TOPIC,
        )


@question_type(
    "geo.earth_layers_application",
    display_name={"th": "วิเคราะห์โครงสร้างโลกจากหลักฐาน"},
    level=UPPER_SIX, subject=SUBJECT, topic=STRUCTURE_TOPIC,
)
class EarthLayersApplication(QuestionType):
    """A solid inner core, why plates move, and reasoning from a counterfactual wave."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, STRUCTURE_SCENARIOS,
            hint="เชื่อมสมบัติของแต่ละชั้นกับความดัน อุณหภูมิ และพฤติกรรมของคลื่นไหวสะเทือน",
        ), STRUCTURE_TOPIC)
