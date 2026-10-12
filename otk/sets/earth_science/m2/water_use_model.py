"""การใช้น้ำอย่างยั่งยืน

ธรณีวิทยา · ม.2 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.2/9

Sets moved here from: science_wave_c21.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b8 import LEVEL as MIDDLE_TWO
from otk.sets._support.science_wave_b9 import Care, Need, care_fluency, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c21 import AGRICULTURE, WATER_USE_SCENARIOS

PROVENANCE = Provenance("original")


WATER_USE_TOPIC = "การใช้น้ำอย่างยั่งยืน"


# Parts of 20 glasses per use. Agriculture is always the largest by a wide
# margin, as it is in Thailand; the smaller uses are redrawn until all four
# differ, so the second-largest use varies and every rank has one answer.
BANDS = {
    AGRICULTURE: (11, 13),
    "การอุปโภคบริโภคในครัวเรือน": (2, 5),
    "อุตสาหกรรม": (1, 3),
}


def water_model(rng: Random) -> dict[str, int]:
    while True:
        parts = {use: rng.randint(*band) for use, band in BANDS.items()}
        parts["การรักษาระบบนิเวศของแหล่งน้ำ"] = 20 - sum(parts.values())
        if min(parts.values()) >= 1 and len(set(parts.values())) == len(parts):
            return parts


WATER_CARE = (
    Care("เปลี่ยนการให้น้ำแปลงผักจากการปล่อยน้ำท่วมแปลงเป็นระบบน้ำหยด",
         "น้ำหยดส่งน้ำถึงรากพืชโดยตรง น้ำระเหยและไหลทิ้งน้อยกว่ามาก"),
    Care("ติดตั้งถังรองรับน้ำฝนจากหลังคาไว้ใช้รดน้ำและทำความสะอาด",
         "น้ำฝนที่เก็บไว้ช่วยลดการสูบน้ำจากแหล่งน้ำและน้ำประปาในฤดูแล้ง"),
    Care("บำบัดน้ำเสียจากโรงงานแล้วนำกลับมาใช้ในกระบวนการผลิต",
         "น้ำถูกใช้ซ้ำหลายรอบ จึงดึงน้ำใหม่จากแหล่งน้ำน้อยลงและไม่ทำให้แหล่งน้ำเสีย"),
    Care("ขุดลอกและดูแลแหล่งกักเก็บน้ำของชุมชนร่วมกัน",
         "แหล่งน้ำที่ไม่ตื้นเขินเก็บน้ำฝนไว้ใช้ในฤดูแล้งได้มากขึ้น"),
    Care("ซ่อมท่อประปาที่รั่วในชุมชนและตรวจมาตรวัดน้ำเป็นประจำ",
         "น้ำประปาที่รั่วไหลทิ้งทั้งวันทั้งคืนรวมกันเป็นน้ำจำนวนมากที่ไม่ได้ใช้ประโยชน์"),
    Care("นำน้ำที่ใช้ล้างผักและซักผ้าครั้งสุดท้ายไปรดต้นไม้หรือราดพื้น",
         "น้ำที่ใช้แล้วแต่ยังไม่สกปรกมากถูกใช้ซ้ำ จึงใช้น้ำสะอาดน้อยลง"),
)


WATER_NEEDS = (
    Need("เกษตรกรในหมู่บ้านปล่อยน้ำท่วมแปลงผักทุกวัน จนน้ำในบ่อหมดก่อนสิ้นฤดูแล้ง "
         "ควรเสนอแนวทางการใช้น้ำอย่างยั่งยืนใดที่ตรงกับท้องถิ่นนี้ที่สุด",
         "เปลี่ยนการให้น้ำแปลงผักจากการปล่อยน้ำท่วมแปลงเป็นระบบน้ำหยด"),
    Need("บ้านเรือนในชุมชนมีหลังคากว้าง ฝนตกชุกช่วงฤดูฝน แต่ขาดน้ำใช้ในบ้านช่วงฤดูแล้ง "
         "ควรเสนอแนวทางการใช้น้ำอย่างยั่งยืนใดที่ตรงกับท้องถิ่นนี้ที่สุด",
         "ติดตั้งถังรองรับน้ำฝนจากหลังคาไว้ใช้รดน้ำและทำความสะอาด"),
    Need("โรงงานในพื้นที่สูบน้ำจากแม่น้ำใช้ครั้งเดียวแล้วปล่อยทิ้ง ขณะที่ชุมชนท้ายน้ำขาดน้ำ "
         "ควรเสนอแนวทางการใช้น้ำอย่างยั่งยืนใดที่ตรงกับท้องถิ่นนี้ที่สุด",
         "บำบัดน้ำเสียจากโรงงานแล้วนำกลับมาใช้ในกระบวนการผลิต"),
    Need("หนองน้ำสาธารณะของหมู่บ้านตื้นเขินจนเก็บน้ำฝนได้น้อยลงทุกปี "
         "ควรเสนอแนวทางการใช้น้ำอย่างยั่งยืนใดที่ตรงกับท้องถิ่นนี้ที่สุด",
         "ขุดลอกและดูแลแหล่งกักเก็บน้ำของชุมชนร่วมกัน"),
    Need("ถนนในหมู่บ้านมีน้ำประปาซึมออกมาจากท่อหลายจุดตลอดเวลา และบ้านหลายหลังค่าน้ำสูงผิดปกติ "
         "ควรเสนอแนวทางการใช้น้ำอย่างยั่งยืนใดที่ตรงกับท้องถิ่นนี้ที่สุด",
         "ซ่อมท่อประปาที่รั่วในชุมชนและตรวจมาตรวัดน้ำเป็นประจำ"),
    Need("บ้านในชุมชนเทน้ำล้างผักและน้ำซักผ้าทิ้งลงท่อทุกวัน แต่ใช้น้ำประปาใหม่รดต้นไม้หน้าบ้าน "
         "ควรเสนอแนวทางการใช้น้ำอย่างยั่งยืนใดที่ตรงกับท้องถิ่นนี้ที่สุด",
         "นำน้ำที่ใช้ล้างผักและซักผ้าครั้งสุดท้ายไปรดต้นไม้หรือราดพื้น"),
)


@question_type(
    "geo.water_use_model_foundation",
    display_name={"th": "อธิบายการใช้น้ำจากแบบจำลอง"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=WATER_USE_TOPIC,
)
class WaterUseModelFoundation(QuestionType):
    """Read a water-use model and explain what it shows — the first free verb."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        parts = water_model(rng)
        model = " / ".join(f"{use} {count} แก้ว" for use, count in parts.items())
        ranked = sorted(parts, key=parts.get, reverse=True)
        stem = ("แบบจำลองแบ่งน้ำที่ชุมชนหนึ่งใช้ใน 1 ปีเป็นน้ำ 20 แก้ว ดังนี้ — "
                f"{model} จากแบบจำลองนี้ ข้อใดอธิบายการใช้น้ำของชุมชนได้ถูกต้อง")
        if rng.random() < 0.5:
            return _labelled(
                stem=stem,
                correct=f"{ranked[0]}ใช้น้ำมากที่สุด การใช้น้ำอย่างประหยัดใน{ranked[0]}จึงช่วยลดการใช้น้ำของชุมชนได้มากที่สุด",
                wrongs=tuple(f"{use}ใช้น้ำมากที่สุด การใช้น้ำอย่างประหยัดใน{use}จึงช่วยลดการใช้น้ำของชุมชนได้มากที่สุด"
                             for use in ranked[1:]),
                hint="นับแก้วของการใช้น้ำแต่ละด้าน แล้วหาด้านที่มากที่สุด",
                topic=WATER_USE_TOPIC,
            )
        return _labelled(
            stem=stem,
            correct=f"{ranked[1]}ใช้น้ำมากเป็นอันดับสอง รองจาก{ranked[0]}",
            wrongs=tuple(f"{use}ใช้น้ำมากเป็นอันดับสอง รองจาก{ranked[0]}"
                         for use in (ranked[2], ranked[3]))
                   + (f"{ranked[0]}ใช้น้ำมากเป็นอันดับสอง รองจาก{ranked[1]}",),
            hint="เรียงจำนวนแก้วจากมากไปน้อย แล้วดูลำดับที่สอง",
            topic=WATER_USE_TOPIC,
        )


@question_type(
    "geo.water_use_model_fluency",
    display_name={"th": "เสนอแนวทางการใช้น้ำอย่างยั่งยืนในท้องถิ่น"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=WATER_USE_TOPIC,
)
class WaterUseModelFluency(QuestionType):
    """Put forward the sustainable practice that fits a local case — the second free verb."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(care_fluency(
            rng, needs=WATER_NEEDS, cares=WATER_CARE,
            hint="หาว่าน้ำในท้องถิ่นนี้สูญเสียหรือขาดแคลนเพราะอะไร แล้วเลือกแนวทางที่แก้สาเหตุนั้น",
        ), WATER_USE_TOPIC)


@question_type(
    "geo.water_use_model_application",
    display_name={"th": "วางแผนการใช้น้ำอย่างยั่งยืนจากข้อมูล"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=WATER_USE_TOPIC,
)
class WaterUseModelApplication(QuestionType):
    """Water for ecosystems, targeting the biggest use, and building a fair model."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, WATER_USE_SCENARIOS,
            hint="นึกว่าน้ำถูกใช้ไปในด้านใดมาก และแนวทางใดทำให้ยังมีน้ำใช้ได้ในระยะยาว",
        ), WATER_USE_TOPIC)
