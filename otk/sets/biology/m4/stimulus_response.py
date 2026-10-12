"""การตอบสนองของพืชต่อสิ่งเร้า

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.4/12

Sets moved here from: science_wave_b22.
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
from otk.sets._support.science_wave_b19 import UPPER_FOUR
from otk.sets._support.science_wave_b22 import GROWTH_TOPIC, RESPONSE_SCENARIOS

PROVENANCE = Provenance("original")


class Response(NamedTuple):
    """One plant response: the stimulus, how it works, a case, and its benefit."""
    name: str
    description: str
    example: str
    benefit: str


RESPONSES = (
    Response("โฟโตทรอปิซึม",
             "ปลายยอดเจริญโค้งเข้าหาแสง เพราะออกซินสะสมทางด้านที่ไม่ได้รับแสง"
             "มากกว่า เซลล์ด้านนั้นจึงยืดตัวมากกว่า",
             "ต้นไม้ในกระถางที่วางไว้ริมหน้าต่างเอนยอดเข้าหาหน้าต่าง",
             "ใบได้รับแสงมากขึ้น พืชจึงสังเคราะห์ด้วยแสงได้มากขึ้น"),
    Response("จีโอทรอปิซึม",
             "รากเจริญไปตามแรงโน้มถ่วงลงสู่ดิน ส่วนยอดเจริญขึ้นในทิศตรงกันข้าม",
             "เมล็ดที่วางกลับหัวไว้ก็ยังงอกรากลงดินและชูยอดขึ้นข้างบน",
             "รากหยั่งลงไปหาน้ำและธาตุอาหารพร้อมกับยึดลำต้นไว้ "
             "ส่วนยอดขึ้นไปรับแสงได้"),
    Response("ไฮโดรทรอปิซึม",
             "รากเจริญโค้งไปทางบริเวณที่มีความชื้นมากกว่า",
             "รากไม้ใหญ่ชอนไชไปทางท่อน้ำที่รั่วซึมใต้ดิน",
             "รากไปถึงแหล่งน้ำได้แม้น้ำในดินจะกระจายอยู่ไม่สม่ำเสมอ"),
    Response("ทิกมอทรอปิซึม",
             "มือเกาะหรือลำต้นเจริญพันรอบสิ่งที่สัมผัส "
             "โดยด้านที่สัมผัสยืดตัวน้อยกว่าด้านตรงข้าม",
             "เถาตำลึงพันรอบรั้วและไต่ขึ้นไปด้านบน",
             "พืชเลื้อยพยุงตัวขึ้นสู่ที่สูงเพื่อรับแสง "
             "โดยไม่ต้องลงทุนสร้างลำต้นที่แข็งแรง"),
    Response("การตอบสนองแบบนาสติก",
             "ส่วนของพืชเคลื่อนไหวโดยทิศทางไม่ขึ้นกับทิศของสิ่งเร้า "
             "เกิดจากการเปลี่ยนแรงดันเต่งของเซลล์อย่างรวดเร็ว",
             "ใบไมยราบหุบลงทันทีเมื่อถูกสัมผัส",
             "ลดโอกาสถูกสัตว์กินและลดการสูญเสียน้ำเมื่อถูกรบกวน"),
    Response("การตอบสนองต่อช่วงแสง",
             "พืชออกดอกเมื่อความยาวของช่วงมืดในรอบวันถึงระดับที่พืชชนิดนั้นต้องการ",
             "เบญจมาศออกดอกในช่วงที่กลางคืนยาวกว่ากลางวัน",
             "พืชออกดอกในฤดูที่เหมาะสมต่อการถ่ายเรณูและการติดผล"),
)


@question_type(
    "plant.stimulus_response_foundation",
    display_name={"th": "รูปแบบการตอบสนองของพืชต่อสิ่งเร้า"},
    level=UPPER_FOUR, subject=SUBJECT, topic=GROWTH_TOPIC,
)
class StimulusResponseFoundation(QuestionType):
    """Explain each form of response — the ``อธิบาย`` half of ``ม.4/12``."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(RESPONSES)
        others = [other for other in RESPONSES if other.name != item.name]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.name}” คือการตอบสนองของพืชในลักษณะใด",
                correct=item.description,
                wrongs=tuple(other.description for other in others[:3]),
                hint="ถามว่าสิ่งเร้าคืออะไร และทิศทางการตอบสนองขึ้นกับทิศของ"
                     "สิ่งเร้านั้นหรือไม่",
                topic=GROWTH_TOPIC,
            )
        return _labelled(
            stem=f"การตอบสนองรูปแบบใดของพืชมีลักษณะว่า {item.description}",
            correct=item.name,
            wrongs=tuple(other.name for other in others[:3]),
            hint="จับที่สิ่งเร้าเป็นหลัก คือแสง แรงโน้มถ่วง ความชื้น การสัมผัส "
                 "หรือความยาวของช่วงมืด",
            topic=GROWTH_TOPIC,
        )


@question_type(
    "plant.stimulus_response_fluency",
    display_name={"th": "การตอบสนองของพืชกับการดำรงชีวิต"},
    level=UPPER_FOUR, subject=SUBJECT, topic=GROWTH_TOPIC,
)
class StimulusResponseFluency(QuestionType):
    """Name the response a case shows, and say what it does for the plant."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(RESPONSES)
        others = [f"{other.name} ซึ่งทำให้{other.benefit}" for other in RESPONSES
                  if other.name != item.name]
        rng.shuffle(others)
        return _labelled(
            stem=f"“{item.example}” เป็นการตอบสนองรูปแบบใด "
                 f"และมีผลต่อการดำรงชีวิตของพืชอย่างไร",
            correct=f"{item.name} ซึ่งทำให้{item.benefit}",
            wrongs=tuple(others[:3]),
            hint="ตัวเลือกที่ถูกต้องต้องถูกทั้งชื่อของการตอบสนอง "
                 "และประโยชน์ที่พืชได้รับจากการตอบสนองนั้น",
            topic=GROWTH_TOPIC,
        )


@question_type(
    "plant.stimulus_response_application",
    display_name={"th": "วิเคราะห์การตอบสนองของพืชต่อสิ่งเร้า"},
    level=UPPER_FOUR, subject=SUBJECT, topic=GROWTH_TOPIC,
)
class StimulusResponseApplication(QuestionType):
    """Read an observed plant movement back to the stimulus and mechanism."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, RESPONSE_SCENARIOS,
            hint="ระบุสิ่งเร้าก่อน แล้วจึงถามว่าการตอบสนองเกิดจากการเจริญเติบโต"
                 "ที่ไม่เท่ากัน หรือจากการเปลี่ยนแรงดันเต่งของเซลล์",
        ), GROWTH_TOPIC)
