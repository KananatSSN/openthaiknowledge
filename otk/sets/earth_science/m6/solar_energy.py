"""การได้รับพลังงานจากดวงอาทิตย์

ธรณีวิทยา · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.6/7

Sets moved here from: science_wave_c24.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c24 import SOLAR_FACTORS, SOLAR_SCENARIOS, parts_item

PROVENANCE = Provenance("original")


SOLAR_TOPIC = "การได้รับพลังงานจากดวงอาทิตย์"


SOLAR_LABELS = tuple(part.label for part in SOLAR_FACTORS)


# Each case holds the other three factors equal, so only one explains it.
SOLAR_CASES = {
    "ละติจูด": (
        "ในวันเดียวกันซึ่งท้องฟ้าแจ่มใสทั้งสองแห่ง พื้นที่โล่งในเมืองใกล้เส้นศูนย์สูตรได้รับพลังงานต่อพื้นที่มากกว่าพื้นที่โล่งแบบเดียวกันในเมืองที่ละติจูดสูง",
        "แผงรับแสงรุ่นเดียวกันวางราบบนลานคอนกรีตในวันที่ท้องฟ้าแจ่มใสเหมือนกัน แผงที่จังหวัดนราธิวาสผลิตไฟฟ้าต่อตารางเมตรได้มากกว่าแผงเดียวกันในประเทศนอร์เวย์",
    ),
    "ฤดูกาล": (
        "ลานคอนกรีตแห่งเดียวกันในเมืองซีกโลกเหนือได้รับพลังงานจากดวงอาทิตย์ในเดือนมิถุนายนมากกว่าเดือนธันวาคม ทั้งที่ท้องฟ้าแจ่มใสทั้งสองช่วง",
        "สถานีวัดแสงแห่งเดียวกันในประเทศญี่ปุ่นบันทึกพลังงานรวมต่อวันในฤดูร้อนได้มากกว่าฤดูหนาว ในวันที่ไม่มีเมฆเหมือนกัน",
    ),
    "เมฆและละอองในอากาศ": (
        "สองอำเภอที่อยู่ติดกัน วันเดียวกัน อำเภอหนึ่งมีเมฆหนาปกคลุมทั้งวัน อีกอำเภอหนึ่งท้องฟ้าแจ่มใส ทุ่งหญ้าในอำเภอที่ท้องฟ้าแจ่มใสได้รับพลังงานมากกว่า",
        "ทุ่งนาแปลงเดียวกันได้รับพลังงานจากดวงอาทิตย์ในวันที่มีหมอกควันหนาแน่นน้อยกว่าในวันถัดมาที่อากาศสะอาด ทั้งสองวันอยู่ในสัปดาห์เดียวกัน",
    ),
    "ลักษณะพื้นผิว": (
        "ในวันเดียวกันที่มีแดดเท่ากัน ลานน้ำแข็งกับผืนป่าที่อยู่ติดกันได้รับแสงเท่ากัน แต่ผืนป่าดูดกลืนพลังงานไว้มากกว่า",
        "ในวันที่มีแดดเท่ากัน พื้นที่ที่หิมะเพิ่งละลายเผยดินสีเข้มดูดกลืนพลังงานไว้มากกว่าพื้นที่ข้าง ๆ ที่ยังมีหิมะปกคลุม",
    ),
}


# Factors that do not explain the regional differences asked about.
SOLAR_DECOYS = ("ระยะห่างระหว่างโลกกับดวงอาทิตย์ในวันนั้น", "ความเร็วลมบริเวณนั้น")


@question_type(
    "geo.solar_energy_foundation",
    display_name={"th": "ระบุปัจจัยที่ทำให้บริเวณต่าง ๆ ได้รับพลังงานจากดวงอาทิตย์ต่างกัน"},
    level=UPPER_SIX, subject=SUBJECT, topic=SOLAR_TOPIC,
)
class SolarEnergyFoundation(QuestionType):
    """One case, with the other factors held equal; name the factor at work."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        factor = rng.choice(SOLAR_LABELS)
        return _labelled(
            stem=f"{rng.choice(SOLAR_CASES[factor])} ปัจจัยใดทำให้เกิดความแตกต่างนี้",
            correct=factor,
            wrongs=tuple([label for label in SOLAR_LABELS if label != factor]
                                    + list(SOLAR_DECOYS)),
            hint="ดูว่าเรื่องนี้กำหนดให้อะไรเหมือนกันแล้ว ปัจจัยที่ยังต่างกันคือคำตอบ",
            topic=SOLAR_TOPIC,
        )


SOLAR_ASK = "ข้อใดอธิบายปัจจัยที่ทำให้แต่ละบริเวณของโลกได้รับพลังงานจากดวงอาทิตย์แตกต่างกันได้ถูกต้องทั้งหมด"


# What the question opens on. Each ends where ``SOLAR_ASK`` begins, and none
# changes which statement of a factor is true.
SOLAR_LEADS = (
    "",
    "ในวันเดียวกัน เทอร์โมมิเตอร์ที่เขตศูนย์สูตรอ่านค่าได้สูงกว่าที่เขตขั้วโลกมาก ",
    "นักเรียนส่องไฟฉายตั้งฉากกับกระดาษ แล้วเอียงไฟฉาย พบว่าวงแสงกว้างขึ้นแต่สลัวลง ",
    "ภาพถ่ายดาวเทียมแสดงว่าพื้นที่ปกคลุมด้วยหิมะดูขาวสว่าง ส่วนป่าและมหาสมุทรดูเข้ม ",
    "ในเมืองเดียวกัน วันที่ฟ้าโปร่งร้อนกว่าวันที่มีเมฆหนาปกคลุมตลอดวัน ",
)


@question_type(
    "geo.solar_energy_fluency",
    display_name={"th": "อธิบายปัจจัยที่มีผลต่อการได้รับพลังงานจากดวงอาทิตย์"},
    level=UPPER_SIX, subject=SUBJECT, topic=SOLAR_TOPIC,
)
class SolarEnergyFluency(QuestionType):
    """All four factors explained; each wrong choice makes one false."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return parts_item(
            rng, SOLAR_FACTORS,
            stem=rng.choice(SOLAR_LEADS) + SOLAR_ASK,
            hint="ตรวจทีละปัจจัย ข้อที่ผิดจะผิดอย่างน้อยหนึ่งปัจจัย",
            topic=SOLAR_TOPIC,
        )


@question_type(
    "geo.solar_energy_application",
    display_name={"th": "วิเคราะห์พลังงานจากดวงอาทิตย์ในสถานการณ์จริง"},
    level=UPPER_SIX, subject=SUBJECT, topic=SOLAR_TOPIC,
)
class SolarEnergyApplication(QuestionType):
    """Cold summer poles, melting sea ice, and tilting a solar panel."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SOLAR_SCENARIOS,
            hint="นึกถึงมุมตกกระทบของแสงและพื้นผิวที่รับแสงไว้หรือสะท้อนออกไป",
        ), SOLAR_TOPIC)
