"""การเกิดระบบสุริยะและเขตเอื้อต่อชีวิต

ดาราศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.1 ม.6/8

Sets moved here from: science_wave_c8.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c1 import SUBJECT
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c8 import HABITABLE_FACTS, ORIGIN_SCENARIOS

PROVENANCE = Provenance("original")


ORIGIN_TOPIC = "การเกิดระบบสุริยะและเขตเอื้อต่อชีวิต"


class Zone(NamedTuple):
    """One zone of the sun's family, and what the nebula left there."""
    name: str
    where: str
    members: str
    why: str


ZONES = (
    Zone("เขตดาวเคราะห์ชั้นใน",
         "ระหว่างดวงอาทิตย์กับแถบดาวเคราะห์น้อย",
         "ดาวพุธ ดาวศุกร์ โลก และดาวอังคาร ซึ่งเป็นดาวเคราะห์หินขนาดเล็กและมีความหนาแน่นสูง",
         "บริเวณนั้นร้อนเกินกว่าน้ำแข็งและแก๊สเบาจะควบแน่นอยู่ได้ เหลือเพียงหินและโลหะ"),
    Zone("แถบดาวเคราะห์น้อย",
         "ระหว่างวงโคจรของดาวอังคารกับดาวพฤหัสบดี",
         "เศษหินและโลหะจำนวนมากที่ไม่ได้รวมตัวกันเป็นดาวเคราะห์",
         "แรงโน้มถ่วงของดาวพฤหัสบดีรบกวนจนเศษวัตถุรวมตัวกันเป็นดาวเคราะห์ไม่ได้"),
    Zone("เขตดาวเคราะห์ชั้นนอก",
         "ถัดจากแถบดาวเคราะห์น้อยออกไปจนถึงวงโคจรของดาวเนปจูน",
         "ดาวพฤหัสบดี ดาวเสาร์ ดาวยูเรนัส และดาวเนปจูน ซึ่งเป็นดาวเคราะห์แก๊สและน้ำแข็งขนาดใหญ่",
         "บริเวณนั้นเย็นพอให้น้ำแข็งควบแน่นได้ แกนจึงโตเร็วและดึงแก๊สเข้ามาห่อหุ้มไว้ได้มาก"),
    Zone("แถบไคเปอร์และบริเวณถัดออกไป",
         "พ้นวงโคจรของดาวเนปจูนออกไป",
         "ดาวเคราะห์แคระอย่างพลูโต และวัตถุน้ำแข็งจำนวนมากซึ่งเป็นต้นกำเนิดของดาวหาง",
         "อยู่ไกลและเบาบางเกินกว่าที่วัตถุจะรวมตัวกันเป็นดาวเคราะห์ขนาดใหญ่ได้"),
)


FORMATION = "กระบวนการเกิดระบบสุริยะ"


ZONING = "การแบ่งเขตบริวารของดวงอาทิตย์"


HABITABLE = "ลักษณะของดาวเคราะห์ที่เอื้อต่อการดำรงชีวิต"


# The one answer that carries all three objects the indicator names. They are
# causally linked: the collapse sets the temperature gradient, the gradient sets
# the zones, and the zones set which distances can hold liquid water.
ORIGIN_SPANNING = (
    "ระบบสุริยะเกิดจากเนบิวลาที่ยุบตัวเป็นจานหมุน ใจกลางที่ร้อนทำให้เขตชั้นในเหลือหินและโลหะ "
    "ส่วนเขตชั้นนอกมีน้ำแข็งและแก๊ส "
    "ดาวเคราะห์ที่เอื้อต่อชีวิตจึงอยู่ในระยะที่น้ำเป็นของเหลวได้")


ORIGIN_SPANNING_WRONGS = (
    "ระบบสุริยะเกิดจากเนบิวลาที่ยุบตัว "
    "ความร้อนที่ลดหลั่นออกไปทำให้เขตชั้นในเป็นแก๊สและเขตชั้นนอกเป็นหิน "
    "ดาวเคราะห์ที่เอื้อต่อชีวิตจึงต้องอยู่ไกลจากดวงอาทิตย์ที่สุด",
    "ระบบสุริยะเกิดจากการที่ดวงอาทิตย์จับดาวเคราะห์ที่ผ่านมาเข้าสู่วงโคจร "
    "เขตชั้นในและชั้นนอกจึงไม่ต่างกันอย่างมีแบบแผน "
    "และดาวเคราะห์ใดก็เอื้อต่อชีวิตได้เท่ากัน",
    "ระบบสุริยะเกิดจากเนบิวลาที่ยุบตัว "
    "แต่ดาวเคราะห์ทุกดวงมีองค์ประกอบของหิน โลหะ น้ำแข็ง และแก๊สเหมือนกันหมด "
    "ดาวเคราะห์ที่เอื้อต่อชีวิตจึงขึ้นกับขนาดเพียงอย่างเดียว",
)


MORE_ORIGIN_WRONGS = (
    "ระบบสุริยะเกิดจากเนบิวลาที่ยุบตัว เขตชั้นในเย็นที่สุดจึงเป็นน้ำแข็ง "
    "และดาวเคราะห์ที่เอื้อต่อชีวิตต้องอยู่ใกล้ดวงอาทิตย์ที่สุดเพื่อให้ได้รับความร้อนมากพอจะละลายน้ำแข็ง",
    "ระบบสุริยะเกิดจากดวงอาทิตย์ระเบิดออกเป็นชิ้น ๆ แล้วชิ้นส่วนเย็นตัวลงเป็นดาวเคราะห์ เขตทั้งหมดจึงเป็นหินร้อน "
    "และไม่มีดาวเคราะห์ใดเอื้อต่อชีวิตได้",
)


# Three ways to ask for the one answer that links all three objects.
ORIGIN_STEMS = (
    f"ข้อใดอธิบาย{FORMATION} {ZONING} และ{HABITABLE}ได้ถูกต้องและเชื่อมโยงกัน",
    "นักเรียนเขียนสรุปหนึ่งย่อหน้าว่าระบบสุริยะเกิดขึ้นอย่างไร เหตุใดบริวารจึงแบ่งเป็นเขต "
    "และดาวเคราะห์แบบใดเอื้อต่อชีวิต ข้อใดเป็นข้อสรุปที่ถูกต้อง",
    "เหตุใดโลกจึงเป็นดาวเคราะห์หินที่มีน้ำเป็นของเหลว ขณะที่ดาวเคราะห์ชั้นนอกเป็นแก๊สและน้ำแข็ง "
    "ข้อใดอธิบายโดยเริ่มจากการเกิดระบบสุริยะได้ถูกต้อง",
)


ZONE_WHY_DECOYS = ("บริเวณนั้นได้รับวัตถุจากกาแล็กซีอื่นมากที่สุด",
                   "บริเวณนั้นมีดาวฤกษ์ดวงอื่นช่วยให้ความร้อน")


ZONE_MEMBER_DECOYS = ("ดาวฤกษ์ขนาดเล็กหลายดวงที่โคจรรอบดวงอาทิตย์",
                      "ดวงจันทร์ของโลกเพียงดวงเดียว")


ZONE_NAME_DECOYS = ("แถบดาวฤกษ์คู่", "เขตหลุมดำ")


@question_type(
    "astro.solar_system_origin_foundation",
    display_name={"th": "เขตบริวารของดวงอาทิตย์และเขตเอื้อต่อชีวิต"},
    level=UPPER_SIX, subject=SUBJECT, topic=ORIGIN_TOPIC,
)
class SolarSystemOriginFoundation(QuestionType):
    """Know the zones and what makes a planet habitable, one at a time."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            return _retopic(scenario_question(
                rng, HABITABLE_FACTS,
                hint="นึกว่าอุณหภูมิที่ลดหลั่นจากใจกลางออกไปกำหนดว่าอะไรควบแน่นได้ที่ระยะใด",
            ), ORIGIN_TOPIC)
        zone = rng.choice(ZONES)
        others = [other for other in ZONES if other.name != zone.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{zone.name}” มีสมาชิกเป็นอะไร",
                correct=zone.members,
                wrongs=tuple([other.members for other in others[:3]]
                                        + list(ZONE_MEMBER_DECOYS)),
                hint="นึกลำดับจากดวงอาทิตย์ออกไปจนพ้นวงโคจรของดาวเนปจูน",
                topic=ORIGIN_TOPIC,
            )
        return _labelled(
            stem=f"เขตใดของระบบสุริยะอยู่{zone.where}",
            correct=zone.name,
            wrongs=tuple([other.name for other in others[:3]] + list(ZONE_NAME_DECOYS)),
            hint="นึกลำดับจากดวงอาทิตย์ออกไปจนพ้นวงโคจรของดาวเนปจูน",
            topic=ORIGIN_TOPIC,
        )


@question_type(
    "astro.solar_system_origin_fluency",
    display_name={"th": "เชื่อมการเกิดระบบสุริยะกับเขตและการเอื้อต่อชีวิต"},
    level=UPPER_SIX, subject=SUBJECT, topic=ORIGIN_TOPIC,
)
class SolarSystemOriginFluency(QuestionType):
    """Reach the formation, the zoning and habitability in one answer.

    The indicator names all three under a single verb, so by the multi-object
    rule only an answer holding all three is a defensible match.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            return _labelled(
                stem=rng.choice(ORIGIN_STEMS),
                correct=ORIGIN_SPANNING,
                wrongs=tuple(ORIGIN_SPANNING_WRONGS + MORE_ORIGIN_WRONGS),
                hint="ตอบให้ครบทั้งสามเรื่อง แล้วตรวจว่าเขตชั้นในกับชั้นนอกสลับกันหรือไม่",
                topic=ORIGIN_TOPIC,
            )
        zone = rng.choice(ZONES)
        others = [other for other in ZONES if other.name != zone.name]
        rng.shuffle(others)
        return _labelled(
            stem=rng.choice((f"เหตุใด “{zone.name}” จึงมีสมาชิกเป็น{zone.members}",
                             f"เหตุใดบริเวณ{zone.where}จึงมีสมาชิกเป็น{zone.members}")),
            correct=zone.why,
            wrongs=tuple([other.why for other in others[:3]] + list(ZONE_WHY_DECOYS)),
            hint="ย้อนกลับไปที่อุณหภูมิและแรงโน้มถ่วงในจานเนบิวลาขณะที่ระบบสุริยะก่อตัว",
            topic=ORIGIN_TOPIC,
        )


@question_type(
    "astro.solar_system_origin_application",
    display_name={"th": "วิเคราะห์การเกิดระบบสุริยะและการเอื้อต่อชีวิต"},
    level=UPPER_SIX, subject=SUBJECT, topic=ORIGIN_TOPIC,
)
class SolarSystemOriginApplication(QuestionType):
    """Judge a habitable-zone claim, Mars's lost water, and the asteroid belt."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, ORIGIN_SCENARIOS,
            hint="ถามว่าอุณหภูมิ มวล และบรรยากาศของดาวดวงนั้นเอื้อให้มีน้ำของเหลวหรือไม่",
        ), ORIGIN_TOPIC)
