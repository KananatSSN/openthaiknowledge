"""การใช้ประโยชน์และผลกระทบของสิ่งมีชีวิตดัดแปรพันธุกรรม

ชีวะ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.3/7

Sets moved here from: science_wave_b27.
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
from otk.sets._support.science_wave_b25 import MIDDLE_THREE
from otk.sets._support.science_wave_b27 import GMO_SCENARIOS, GMO_TOPIC

PROVENANCE = Provenance("original")


class Gmo(NamedTuple):
    """One GMO, what it was modified for, and the concern raised about it."""
    name: str
    benefit: str
    impact: str


GMOS = (
    Gmo("ข้าวโพดต้านแมลง",
        "ได้รับยีนที่สร้างโปรตีนซึ่งเป็นพิษต่อหนอนเจาะลำต้น "
        "เกษตรกรจึงใช้สารกำจัดแมลงน้อยลงและได้ผลผลิตมากขึ้น",
        "แมลงศัตรูอาจปรับตัวจนทนต่อโปรตีนนั้นได้ในระยะยาว "
        "และโปรตีนอาจมีผลต่อแมลงชนิดอื่นที่ไม่ใช่ศัตรูพืช"),
    Gmo("ถั่วเหลืองทนสารกำจัดวัชพืช",
        "ทนต่อสารกำจัดวัชพืชชนิดหนึ่งได้ เกษตรกรจึงกำจัดวัชพืชได้สะดวก"
        "โดยไม่ทำอันตรายต่อต้นถั่ว",
        "อาจทำให้มีการใช้สารกำจัดวัชพืชมากขึ้นจนตกค้างในดินและแหล่งน้ำ "
        "และวัชพืชอาจทนต่อสารนั้นตามไปด้วย"),
    Gmo("ข้าวสีทอง",
        "ได้รับยีนที่ทำให้เมล็ดสร้างสารตั้งต้นของวิตามินเอ "
        "ช่วยลดภาวะขาดวิตามินเอในพื้นที่ที่กินข้าวเป็นอาหารหลัก",
        "ยังมีข้อถกเถียงเรื่องปริมาณที่ได้รับจริงเมื่อกินตามปกติ "
        "และเรื่องการเข้าถึงเมล็ดพันธุ์ของเกษตรกรรายย่อย"),
    Gmo("แบคทีเรียผลิตอินซูลิน",
        "ได้รับยีนอินซูลินของมนุษย์ จึงผลิตอินซูลินได้ในปริมาณมาก "
        "ผู้ป่วยเบาหวานจึงเข้าถึงยาได้มากขึ้นและปลอดภัยกว่าการสกัดจากสัตว์",
        "ต้องควบคุมไม่ให้แบคทีเรียดัดแปรพันธุกรรมหลุดออกจากระบบผลิต"
        "สู่สิ่งแวดล้อม"),
    Gmo("มะละกอต้านไวรัสใบด่างวงแหวน",
        "ได้รับยีนของไวรัสบางส่วนจึงต้านทานโรคใบด่างวงแหวนได้ "
        "ช่วยรักษาผลผลิตในพื้นที่ที่โรคนี้ระบาด",
        "อาจถ่ายเรณูไปยังมะละกอพันธุ์พื้นเมืองที่ปลูกใกล้เคียง "
        "ทำให้ยีนดัดแปรกระจายออกไปโดยไม่ตั้งใจ"),
    Gmo("ปลาแซลมอนโตเร็ว",
        "ได้รับยีนที่ทำให้สร้างฮอร์โมนการเจริญเติบโตได้ตลอดปี "
        "จึงโตถึงขนาดที่ขายได้ในเวลาสั้นลงราวครึ่งหนึ่ง",
        "หากหลุดออกสู่แหล่งน้ำธรรมชาติ อาจแย่งอาหารและผสมพันธุ์"
        "กับปลาพันธุ์ดั้งเดิมจนกระทบประชากรเดิม"),
)


GMOS += (
    Gmo('มะเขือเทศสุกช้า',
        'ได้รับยีนที่ชะลอการนิ่มของผล จึงเก็บรักษาและขนส่งได้นานขึ้นโดยไม่เน่าเสีย',
        'ผู้บริโภคบางส่วนกังวลเรื่องความปลอดภัย และต้องการให้ติดฉลากเพื่อใช้ประกอบการเลือกซื้อ'),
    Gmo('ยีสต์ผลิตวัคซีนตับอักเสบบี',
        'ได้รับยีนสร้างโปรตีนผิวของไวรัส จึงผลิตวัคซีนที่ไม่มีตัวไวรัสก่อโรคได้ในปริมาณมาก',
        'ต้องผลิตในโรงงานที่ควบคุมมาตรฐาน และตรวจความบริสุทธิ์ของวัคซีนอย่างเข้มงวดก่อนนำไปใช้'),
    Gmo('ข้าวโพดทนแล้ง',
        'ได้รับยีนที่ช่วยให้ทนต่อการขาดน้ำ จึงให้ผลผลิตได้แม้ในปีที่ฝนตกน้อย',
        'ยีนทนแล้งอาจถ่ายไปยังข้าวโพดพันธุ์อื่นที่ปลูกใกล้กัน และต้นทุนเมล็ดพันธุ์อาจสูงสำหรับเกษตรกรรายย่อย'),
)


@question_type(
    "life.gmo_use_foundation",
    display_name={"th": "การใช้ประโยชน์จากสิ่งมีชีวิตดัดแปรพันธุกรรม"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=GMO_TOPIC,
)
class GmoUseFoundation(QuestionType):
    """What each GMO was made to do."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(GMOS)
        others = [other for other in GMOS if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.name}” ถูกดัดแปรพันธุกรรมเพื่อประโยชน์ใด",
                correct=item.benefit,
                wrongs=tuple(other.benefit for other in others[:3]),
                hint="ถามว่ายีนที่ใส่เข้าไปทำให้สิ่งมีชีวิตนั้นทำอะไรได้เพิ่มขึ้น",
                topic=GMO_TOPIC,
            )
        return _labelled(
            stem=f"สิ่งมีชีวิตดัดแปรพันธุกรรมชนิดใดถูกสร้างขึ้นโดย{item.benefit}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="อ่านประโยชน์ให้จบก่อน แล้วจึงเลือกสิ่งมีชีวิตที่ตรงกับประโยชน์นั้น",
            topic=GMO_TOPIC,
        )


@question_type(
    "life.gmo_use_fluency",
    display_name={"th": "ผลกระทบของสิ่งมีชีวิตดัดแปรพันธุกรรม"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=GMO_TOPIC,
)
class GmoUseFluency(QuestionType):
    """Name the concern that actually attaches to a given GMO.

    ``ม.3/7`` names ``ผลกระทบที่อาจมีต่อมนุษย์และสิ่งแวดล้อม`` alongside the uses,
    so this half is asked in its own right rather than folded into the benefits.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(GMOS)
        others = [other.impact for other in GMOS if other.impact != item.impact]
        rng.shuffle(others)
        return _labelled(
            stem=f"“{item.name}” มีผลกระทบที่ต้องเฝ้าระวังในเรื่องใด",
            correct=item.impact, wrongs=tuple(others[:3]),
            hint="ผลกระทบที่ถูกต้องต้องตามมาจากยีนที่ใส่เข้าไปในสิ่งมีชีวิตนั้นจริง ๆ",
            topic=GMO_TOPIC,
        )


@question_type(
    "life.gmo_use_application",
    display_name={"th": "วิเคราะห์ประโยชน์และผลกระทบของสิ่งมีชีวิตดัดแปรพันธุกรรม"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=GMO_TOPIC,
)
class GmoUseApplication(QuestionType):
    """Weigh a benefit against the concern that actually follows from it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, GMO_SCENARIOS,
            hint="ตามผลจากยีนที่ใส่เข้าไปเป็นลูกโซ่ "
                 "และแยกข้อกังวลที่มีข้อมูลรองรับออกจากข้อกังวลที่ไม่มี",
        ), GMO_TOPIC)
