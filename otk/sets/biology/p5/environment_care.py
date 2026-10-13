"""การมีส่วนร่วมดูแลรักษาสิ่งแวดล้อม

ชีวะ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 1.1 ป.5/4

Sets moved here from: science_wave_b32.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, Care, Need, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b24 import PRIMARY_FIVE
from otk.sets._support.science_wave_b31 import ECOLOGY_TOPIC
from otk.sets._support.science_wave_b32 import CARE_SCENARIOS

PROVENANCE = Provenance("original")


ENVIRONMENT_CARE = (
    Care("ไม่ทิ้งขยะและไม่เทน้ำเสียลงแม่น้ำลำคลอง",
         "น้ำที่สะอาดเป็นที่อยู่ของปลาและพืชน้ำ และเป็นแหล่งน้ำที่คนและสัตว์ใช้"),
    Care("ช่วยกันปลูกต้นไม้และไม่ตัดต้นไม้โดยไม่จำเป็น",
         "ต้นไม้เป็นที่อยู่และแหล่งอาหารของสัตว์ และรากช่วยยึดดินไม่ให้พังทลาย"),
    Care("ไม่จับสัตว์น้ำในช่วงฤดูวางไข่",
         "สัตว์น้ำได้ขยายพันธุ์ ประชากรจึงไม่ลดลงจนหมดไป"),
    Care("ไม่เผาขยะหรือเศษใบไม้ในที่โล่ง",
         "ควันจากการเผาทำให้อากาศเสีย ส่งผลต่อการหายใจของคนและสัตว์"),
    Care("คัดแยกขยะและนำขวดพลาสติกไปรีไซเคิล",
         "ลดขยะพลาสติกที่หลุดรอดลงสู่ทะเลและทำอันตรายต่อสัตว์ทะเล"),
    Care("นำเศษอาหารไปทำปุ๋ยหมักใส่แปลงผัก",
         "ดินร่วนซุยและมีธาตุอาหารเพิ่มขึ้น สิ่งมีชีวิตในดินเช่นไส้เดือนดินจึงอยู่ได้"),
)


ENVIRONMENT_NEEDS = (
    Need("นักเรียนเห็นคนเทน้ำมันเครื่องที่ใช้แล้วลงคลองหลังบ้าน "
         "ควรปฏิบัติตามแนวทางใด",
         "ไม่ทิ้งขยะและไม่เทน้ำเสียลงแม่น้ำลำคลอง"),
    Need("ตลิ่งริมลำธารในหมู่บ้านพังทลายทุกฤดูฝน หลังจากต้นไม้ริมตลิ่งถูกตัดไป "
         "ควรปฏิบัติตามแนวทางใด",
         "ช่วยกันปลูกต้นไม้และไม่ตัดต้นไม้โดยไม่จำเป็น"),
    Need("ชาวบ้านจับปลาที่มีไข่เต็มท้องได้จำนวนมากในช่วงต้นฤดูฝนทุกปี "
         "และปลาก็น้อยลงทุกปี ควรปฏิบัติตามแนวทางใด",
         "ไม่จับสัตว์น้ำในช่วงฤดูวางไข่"),
    Need("ทุกเย็นเพื่อนบ้านกวาดใบไม้มากองแล้วจุดไฟ ทำให้เด็กในบ้านไอบ่อย "
         "ควรปฏิบัติตามแนวทางใด",
         "ไม่เผาขยะหรือเศษใบไม้ในที่โล่ง"),
    Need("ถังขยะของโรงเรียนเต็มเร็วมาก และมีขวดพลาสติกปนอยู่กับขยะอื่นจำนวนมาก "
         "ควรปฏิบัติตามแนวทางใด",
         "คัดแยกขยะและนำขวดพลาสติกไปรีไซเคิล"),
    Need("โรงอาหารมีเศษผักและเศษอาหารเหลือทุกวัน ส่วนแปลงผักของโรงเรียนดินแข็ง"
         "และไม่พบไส้เดือนดินเลย ควรปฏิบัติตามแนวทางใด",
         "นำเศษอาหารไปทำปุ๋ยหมักใส่แปลงผัก"),
)


@question_type(
    "ecology.environment_care_foundation",
    display_name={"th": "คุณค่าของสิ่งแวดล้อมต่อสิ่งมีชีวิต"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class EnvironmentCareFoundation(QuestionType):
    """Match a way of caring for the environment to what it keeps alive."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(ENVIRONMENT_CARE)
        others = [other for other in ENVIRONMENT_CARE if other.practice != item.practice]
        rng.shuffle(others)
        hint = "โยงกลับไปว่าการกระทำนั้นช่วยรักษาสิ่งใดที่สิ่งมีชีวิตต้องใช้"
        if rng.random() < 0.5:
            return _labelled(
                stem=f"การ “{item.practice}” ช่วยให้สิ่งมีชีวิตดำรงชีวิตได้อย่างไร",
                correct=item.reason,
                wrongs=tuple(other.reason for other in others[:3]),
                hint=hint, topic=ECOLOGY_TOPIC,
            )
        return _labelled(
            stem=f"การดูแลสิ่งแวดล้อมแบบใดอาศัยเหตุผลที่ว่า {item.reason}",
            correct=item.practice,
            wrongs=tuple(other.practice for other in others[:3]),
            hint=hint, topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.environment_care_fluency",
    display_name={"th": "เลือกแนวทางดูแลรักษาสิ่งแวดล้อม"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class EnvironmentCareFluency(QuestionType):
    """Choose the practice that fits the situation.

    ``ป.5/4``'s evidence clause is ``โดยมีส่วนร่วมในการดูแลรักษา`` — conduct, so
    this set is ``standard_scope`` even though it states a แนวทาง.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        need = rng.choice(ENVIRONMENT_NEEDS)
        others = [care.practice for care in ENVIRONMENT_CARE
                  if care.practice != need.practice]
        rng.shuffle(others)
        return _labelled(
            stem=need.situation, correct=need.practice, wrongs=tuple(others[:3]),
            hint="เลือกแนวทางที่แก้ปัญหาที่โจทย์บรรยายไว้โดยตรง",
            topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.environment_care_application",
    display_name={"th": "วิเคราะห์การมีส่วนร่วมดูแลสิ่งแวดล้อม"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class EnvironmentCareApplication(QuestionType):
    """Judge whether an action helps the environment or only looks like it does."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, CARE_SCENARIOS,
            hint="ถามว่าการกระทำนั้นแก้ที่ต้นเหตุหรือไม่ และทำต่อเนื่องได้หรือเปล่า",
        ), ECOLOGY_TOPIC)


# More practices, each with its own reason and the one situation it answers,
# so every practice still answers exactly one situation.
ENVIRONMENT_CARE += (
    Care('ปิดไฟและเครื่องใช้ไฟฟ้าเมื่อไม่ใช้งาน',
         'ลดการใช้เชื้อเพลิงในการผลิตไฟฟ้า จึงลดควันพิษและแก๊สที่ปล่อยสู่อากาศ'),
    Care('พกถุงผ้าไปซื้อของแทนการรับถุงพลาสติก',
         'ลดจำนวนถุงพลาสติกที่ใช้แล้วทิ้ง ซึ่งย่อยสลายยากและตกค้างในสิ่งแวดล้อม'),
)
ENVIRONMENT_NEEDS += (
    Need('นักเรียนออกจากห้องเรียนไปพักกลางวันโดยเปิดพัดลมและไฟทิ้งไว้ทุกวัน ควรทำอย่างไร',
         'ปิดไฟและเครื่องใช้ไฟฟ้าเมื่อไม่ใช้งาน'),
    Need('นักเรียนไปตลาดกับแม่ทุกเช้า และรับถุงพลาสติกใบใหม่มาหลายใบทุกครั้ง ควรทำอย่างไร',
         'พกถุงผ้าไปซื้อของแทนการรับถุงพลาสติก'),
)
