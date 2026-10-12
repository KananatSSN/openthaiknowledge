"""ความชื้นสัมพัทธ์ของอากาศ

ธรณีวิทยา · ม.1 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.1/2

Sets moved here from: science_wave_g2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b2 import LEVEL as MIDDLE_ONE
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import SUBJECT as GEO_SUBJECT
from otk.sets._support.science_wave_g2 import HUMIDITY_SCENARIOS

PROVENANCE = Provenance("original")


HUMIDITY_TOPIC = "ความชื้นสัมพัทธ์ของอากาศ"


# Wrong meanings, three drawn per question.
HUMIDITY_DECOYS = (
    "ปริมาณไอน้ำทั้งหมดที่มีอยู่ในอากาศ วัดเป็นกรัมต่อลูกบาศก์เมตร โดยไม่เทียบกับค่าใด",
    "ปริมาณน้ำฝนที่ตกลงมาในหนึ่งวัน คิดเป็นร้อยละของปริมาณน้ำฝนทั้งปี",
    "อัตราส่วนของอุณหภูมิอากาศเทียบกับอุณหภูมิของน้ำในแหล่งน้ำใกล้เคียง",
    "ร้อยละของเวลาในหนึ่งวันที่ท้องฟ้ามีเมฆปกคลุม เทียบกับเวลาที่ท้องฟ้าโปร่ง",
    "ปริมาณไอน้ำที่มากที่สุดที่อากาศรับไว้ได้ โดยไม่เทียบกับไอน้ำที่มีอยู่จริง",
    "อัตราส่วนของแก๊สออกซิเจนเทียบกับไอน้ำในอากาศ คิดเป็นร้อยละ",
    "น้ำหนักของอากาศที่กดลงบนพื้นที่หนึ่งตารางเมตร วัดเป็นหน่วยปาสกาล",
    "ไอน้ำมากที่สุดที่อากาศรับได้ เทียบกับไอน้ำที่มีจริงในอากาศ คิดเป็นเท่า",
    "ความเร็วที่น้ำระเหยกลายเป็นไอน้ำจากผิวน้ำ วัดเป็นมิลลิเมตรต่อวัน",
)


# Each case: what changes, and what happens to ความชื้นสัมพัทธ์ because of it.
# The temperature cases are the ones learners get wrong — the amount of water
# vapour has not changed at all, only how much the air *could* hold.
HUMIDITY_CASES = (
    ("อุณหภูมิของอากาศสูงขึ้น โดยปริมาณไอน้ำในอากาศเท่าเดิม",
     "ความชื้นสัมพัทธ์ลดลง เพราะอากาศที่ร้อนขึ้นรับไอน้ำได้มากขึ้น ไอน้ำเท่าเดิมจึงคิดเป็นสัดส่วนที่น้อยลง"),
    ("อุณหภูมิของอากาศลดลง โดยปริมาณไอน้ำในอากาศเท่าเดิม",
     "ความชื้นสัมพัทธ์เพิ่มขึ้น เพราะอากาศที่เย็นลงรับไอน้ำได้น้อยลง ไอน้ำเท่าเดิมจึงคิดเป็นสัดส่วนที่มากขึ้น"),
    ("มีไอน้ำระเหยเข้าสู่อากาศเพิ่มขึ้น โดยอุณหภูมิของอากาศเท่าเดิม",
     "ความชื้นสัมพัทธ์เพิ่มขึ้น เพราะปริมาณไอน้ำที่มีอยู่จริงมากขึ้น ขณะที่ปริมาณสูงสุดที่รับได้เท่าเดิม"),
    ("ความชื้นสัมพัทธ์ของอากาศมีค่าถึงร้อยละ 100",
     "อากาศรับไอน้ำไว้ได้เต็มที่แล้ว ไอน้ำส่วนเกินจะควบแน่นเป็นหยดน้ำ เกิดเป็นเมฆ หมอก หรือน้ำค้าง"),
    ("ไอน้ำในอากาศลดลงเพราะควบแน่นไปเกาะบนผิวที่เย็น โดยอุณหภูมิของอากาศเท่าเดิม",
     "ความชื้นสัมพัทธ์ลดลง เพราะปริมาณไอน้ำที่มีอยู่จริงน้อยลง ขณะที่ปริมาณสูงสุดที่รับได้เท่าเดิม"),
    ("อุณหภูมิสูงขึ้น และมีไอน้ำระเหยเพิ่มเข้ามาในสัดส่วนเดียวกับที่อากาศรับได้มากขึ้น",
     "ความชื้นสัมพัทธ์เท่าเดิม เพราะไอน้ำที่มีอยู่จริงและปริมาณสูงสุดที่รับได้เพิ่มขึ้นในสัดส่วนเท่ากัน"),
)


@question_type(
    "geo.humidity_foundation",
    display_name={"th": "บอกความหมายของความชื้นสัมพัทธ์"},
    level=MIDDLE_ONE, subject=GEO_SUBJECT, topic=HUMIDITY_TOPIC,
)
class HumidityFoundation(QuestionType):
    """A ratio, not an amount — the distinction the whole idea turns on."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _labelled(
            stem=rng.choice(("ความชื้นสัมพัทธ์ของอากาศหมายถึงอะไร",
                             "ข้อใดบอกความหมายของความชื้นสัมพัทธ์ของอากาศได้ถูกต้อง")),
            correct="ไอน้ำที่มีจริงในอากาศ เทียบกับไอน้ำมากที่สุดที่อากาศรับได้ คิดเป็นร้อยละ",
            wrongs=tuple(HUMIDITY_DECOYS),
            hint="คำว่าสัมพัทธ์แปลว่าเทียบกับสิ่งอื่น ในที่นี้คือเทียบกับปริมาณไอน้ำมากที่สุดที่อากาศรับไว้ได้",
            topic=HUMIDITY_TOPIC,
        )


@question_type(
    "geo.humidity_fluency",
    display_name={"th": "บอกผลต่อความชื้นสัมพัทธ์เมื่ออุณหภูมิหรือไอน้ำเปลี่ยนไป"},
    level=MIDDLE_ONE, subject=GEO_SUBJECT, topic=HUMIDITY_TOPIC,
)
class HumidityFluency(QuestionType):
    """One thing changes; what the relative humidity does."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(HUMIDITY_CASES))
        change, correct = HUMIDITY_CASES[index]
        others = [c for i, (_, c) in enumerate(HUMIDITY_CASES) if i != index]
        return _labelled(
            stem=f"เมื่อ{change} ความชื้นสัมพัทธ์ของอากาศจะเปลี่ยนแปลงอย่างไร",
            correct=correct,
            wrongs=tuple(others),
            hint=("ความชื้นสัมพัทธ์เป็นสัดส่วน จึงเปลี่ยนได้ทั้งเมื่อไอน้ำที่มีอยู่จริงเปลี่ยน "
                  "และเมื่อปริมาณสูงสุดที่อากาศรับได้เปลี่ยนตามอุณหภูมิ"),
            topic=HUMIDITY_TOPIC,
        )


@question_type(
    "geo.humidity_application",
    display_name={"th": "ใช้ความชื้นสัมพัทธ์อธิบายสถานการณ์ในชีวิตประจำวัน"},
    level=MIDDLE_ONE, subject=GEO_SUBJECT, topic=HUMIDITY_TOPIC,
)
class HumidityApplication(QuestionType):
    """Morning fog burning off, sticky heat, and a document store."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, HUMIDITY_SCENARIOS,
            hint="ถามว่าอากาศรับไอน้ำได้อีกเท่าใด ไม่ใช่ว่ามีไอน้ำอยู่เท่าใด",
        ), HUMIDITY_TOPIC)
