"""ประโยชน์ของดวงอาทิตย์ต่อสิ่งมีชีวิต

ดาราศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 3.1 ป.3/3

Sets moved here from: science_wave_c2.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import PRIMARY_THREE, _retopic
from otk.sets._support.science_wave_c1 import SKY_TOPIC, SUBJECT
from otk.sets._support.science_wave_c2 import SUN_BENEFIT_SCENARIOS

PROVENANCE = Provenance("original")


class Benefit(NamedTuple):
    """One thing the sun gives, who it reaches, and what would happen without it."""
    gift: str
    who: str
    because: str
    without: str


# The four gifts are distinct in kind — food, warmth, light to see by, and the
# water cycle — so no two rows share a ``because`` or a ``without``.
BENEFITS = (
    Benefit("แสงสำหรับสร้างอาหาร", "พืช",
            "พืชใช้แสงจากดวงอาทิตย์สร้างอาหารที่ใบ",
            "พืชสร้างอาหารไม่ได้ แล้วสัตว์ที่กินพืชก็ขาดอาหารตามไปด้วย"),
    Benefit("ความอบอุ่น", "สัตว์และมนุษย์",
            "ความร้อนจากดวงอาทิตย์ทำให้อากาศและพื้นดินอุ่นพอที่สิ่งมีชีวิตจะอยู่ได้",
            "โลกจะหนาวเย็นจัดจนสิ่งมีชีวิตส่วนใหญ่อยู่ไม่ได้"),
    Benefit("แสงสว่างสำหรับมองเห็น", "สัตว์และมนุษย์",
            "แสงในเวลากลางวันทำให้มองเห็นอาหาร ทาง และอันตรายได้",
            "กลางวันจะมืดจนหาอาหารและเดินทางได้ยาก"),
    Benefit("ความร้อนที่ทำให้น้ำระเหย", "สิ่งมีชีวิตทุกชนิด",
            "ความร้อนทำให้น้ำระเหยขึ้นไปเป็นเมฆแล้วตกกลับลงมาเป็นฝน",
            "วัฏจักรน้ำจะหยุดลง ฝนไม่ตก และแหล่งน้ำจืดจะหมดไป"),
    Benefit("การบอกเวลาและทิศ", "มนุษย์",
            "การขึ้นและตกซ้ำเป็นแบบรูปเดิมทุกวันใช้บอกช่วงเวลาและทิศได้",
            "การนัดหมายเวลากลางวันและการหาทิศจากท้องฟ้าจะทำได้ยาก"),
    Benefit("ความร้อนที่ใช้ตากสิ่งของ", "มนุษย์",
            "แดดทำให้ผ้า ข้าวเปลือก และปลาแห้งได้โดยไม่ต้องใช้เชื้อเพลิง",
            "ต้องหาวิธีอื่นมาทำให้ของแห้ง ซึ่งสิ้นเปลืองกว่า"),
)


@question_type(
    "astro.sun_benefits_foundation",
    display_name={"th": "ดวงอาทิตย์ให้อะไรแก่สิ่งมีชีวิต"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=SKY_TOPIC,
)
class SunBenefitsFoundation(QuestionType):
    """Match a gift of the sun to who receives it, in either direction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(BENEFITS)
        others = [other for other in BENEFITS if other.gift != item.gift]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"ดวงอาทิตย์ให้ “{item.gift}” แก่สิ่งมีชีวิตอย่างไร",
                correct=item.because,
                wrongs=tuple(other.because for other in others[:3]),
                hint="นึกว่าสิ่งนั้นช่วยให้สิ่งมีชีวิตทำอะไรได้",
                topic=SKY_TOPIC,
            )
        return _labelled(
            stem=f"ข้อใดคือประโยชน์ของดวงอาทิตย์ที่ทำให้ “{item.because}”",
            correct=item.gift,
            wrongs=tuple(other.gift for other in others[:3]),
            hint="อ่านคำอธิบายแล้วเลือกชื่อของประโยชน์ที่ตรงกัน",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.sun_benefits_fluency",
    display_name={"th": "บรรยายประโยชน์ของดวงอาทิตย์ต่อสิ่งมีชีวิต"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=SKY_TOPIC,
)
class SunBenefitsFluency(QuestionType):
    """Describe what the sun does for living things, and what its loss would cost.

    ``ตระหนัก`` is evidenced here by ``โดยบรรยายประโยชน์``, which a learner can be
    asked to do on paper, so this is the one ``exact`` set of the indicator.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(BENEFITS)
        others = [other for other in BENEFITS if other.gift != item.gift]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"ถ้าไม่มี “{item.gift}” จากดวงอาทิตย์ จะเกิดผลต่อสิ่งมีชีวิตอย่างไร",
                correct=item.without,
                wrongs=tuple(other.without for other in others[:3]),
                hint="นึกว่าสิ่งมีชีวิตใช้สิ่งนั้นทำอะไร แล้วสิ่งนั้นจะขาดไป",
                topic=SKY_TOPIC,
            )
        return _labelled(
            stem=f"ดวงอาทิตย์มีความสำคัญต่อ “{item.who}” อย่างไร "
                 f"เมื่อพิจารณาเรื่อง{item.gift}",
            correct=item.because,
            wrongs=tuple(other.because for other in others[:3]),
            hint="บรรยายว่าสิ่งมีชีวิตกลุ่มนั้นได้ประโยชน์จากดวงอาทิตย์ในเรื่องใด",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.sun_benefits_application",
    display_name={"th": "วิเคราะห์ความสำคัญของดวงอาทิตย์"},
    level=PRIMARY_THREE, subject=SUBJECT, topic=SKY_TOPIC,
)
class SunBenefitsApplication(QuestionType):
    """Trace the sun's importance through a dark room, a cave, and a solar panel."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SUN_BENEFIT_SCENARIOS,
            hint="ถามว่าสิ่งมีชีวิตในสถานการณ์นั้นใช้อะไรจากดวงอาทิตย์ แล้วสิ่งนั้นขาดไปหรือไม่",
        ), SKY_TOPIC)
