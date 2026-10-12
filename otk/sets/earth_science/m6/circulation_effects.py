"""ผลของการหมุนเวียนของอากาศและน้ำในมหาสมุทร

ธรณีวิทยา · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.6/12

Sets moved here from: science_wave_c25.
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
from otk.sets._support.science_wave_c24 import MORE_PART_FALSES, parts_item
from otk.sets._support.science_wave_c25 import (
    EFFECTS,
    EFFECTS_SCENARIOS,
    EL_NINO,
    GULF_STREAM,
    LA_NINA,
)

PROVENANCE = Provenance("original")


EFFECTS_TOPIC = "ผลของการหมุนเวียนของอากาศและน้ำในมหาสมุทร"


ASPECTS = ("ภูมิอากาศ", "ลมฟ้าอากาศ", "สิ่งมีชีวิต", "สิ่งแวดล้อม")


PHENOMENA = {
    EL_NINO: "เอลนีโญ ซึ่งลมค้าอ่อนกำลังลงและน้ำอุ่นผิวหน้าไหลไปสะสมทางฝั่งตะวันออกของมหาสมุทรแปซิฟิก",
    LA_NINA: "ลานีญา ซึ่งลมค้ามีกำลังแรงขึ้นและน้ำอุ่นผิวหน้าถูกพัดไปสะสมทางฝั่งตะวันตกของมหาสมุทรแปซิฟิกมากกว่าปกติ",
    GULF_STREAM: "กระแสน้ำกัลฟ์สตรีมและกระแสน้ำแอตแลนติกเหนือ ซึ่งพาน้ำอุ่นจากเขตร้อนไปยังชายฝั่งยุโรปตะวันตก",
}


@question_type(
    "geo.circulation_effects_foundation",
    display_name={"th": "ระบุผลของการหมุนเวียนของอากาศและน้ำทีละด้าน"},
    level=UPPER_SIX, subject=SUBJECT, topic=EFFECTS_TOPIC,
)
class CirculationEffectsFoundation(QuestionType):
    """One circulation and one aspect; wrongs are its own falsehood and other circulations' effects."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        phenomenon = rng.choice(tuple(PHENOMENA))
        aspect = rng.randrange(len(ASPECTS))
        part = EFFECTS[phenomenon][aspect]
        # El Niño and La Niña mirror each other, so one's truth can be the other's
        # falsehood; candidates are deduplicated and never repeat the answer.
        candidates = [part.false,
                      *(EFFECTS[other][aspect].true for other in PHENOMENA if other != phenomenon),
                      *(EFFECTS[other][aspect].false for other in PHENOMENA if other != phenomenon)]
        candidates += list(MORE_PART_FALSES.get(part.false, ()))
        pool = [text for text in dict.fromkeys(candidates) if text != part.true]
        wrongs = rng.sample(pool, 3)
        return _labelled(
            stem=f"ข้อใดเป็นผลของ{PHENOMENA[phenomenon]} ต่อ{ASPECTS[aspect]}",
            correct=part.true,
            wrongs=tuple(wrongs),
            hint="ระบุก่อนว่าน้ำอุ่นไปสะสมที่ใด บริเวณนั้นอากาศลอยตัวขึ้นและฝนตกมาก",
            topic=EFFECTS_TOPIC,
        )


@question_type(
    "geo.circulation_effects_fluency",
    display_name={"th": "อธิบายผลของการหมุนเวียนของอากาศและน้ำต่อภูมิอากาศ ลมฟ้าอากาศ สิ่งมีชีวิต และสิ่งแวดล้อม"},
    level=UPPER_SIX, subject=SUBJECT, topic=EFFECTS_TOPIC,
)
class CirculationEffectsFluency(QuestionType):
    """All four effects of one circulation; each wrong choice falsifies one."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        phenomenon = rng.choice(tuple(PHENOMENA))
        return parts_item(
            rng, EFFECTS[phenomenon],
            stem=(f"ข้อใดอธิบายผลของ{PHENOMENA[phenomenon]} "
                  "ต่อภูมิอากาศ ลมฟ้าอากาศ สิ่งมีชีวิต และสิ่งแวดล้อมได้ถูกต้องทั้งหมด"),
            hint="ตรวจทีละด้าน ข้อที่ผิดจะผิดอย่างน้อยหนึ่งด้าน",
            topic=EFFECTS_TOPIC,
        )


@question_type(
    "geo.circulation_effects_application",
    display_name={"th": "วิเคราะห์ผลของเอลนีโญ ปะการังฟอกขาว และกระแสน้ำอุ่น"},
    level=UPPER_SIX, subject=SUBJECT, topic=EFFECTS_TOPIC,
)
class CirculationEffectsApplication(QuestionType):
    """Farming through El Niño, bleached reefs, and London's mild winters."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, EFFECTS_SCENARIOS,
            hint="ตามว่าอากาศและน้ำอุ่นเคลื่อนไปที่ใด แล้วนึกถึงผลต่อฝน อุณหภูมิ และสิ่งมีชีวิตบริเวณนั้น",
        ), EFFECTS_TOPIC)
