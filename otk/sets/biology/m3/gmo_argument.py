"""การโต้แย้งทางวิทยาศาสตร์และการเผยแพร่ความรู้

ชีวะ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.3/8

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
from otk.sets._support.science_wave_b19 import Fact, _fact_question
from otk.sets._support.science_wave_b25 import MIDDLE_THREE
from otk.sets._support.science_wave_b27 import ARGUMENT_SCENARIOS, GMO_TOPIC

PROVENANCE = Provenance("original")


ARGUMENT_FACTS = (
    Fact("การโต้แย้งทางวิทยาศาสตร์ต่างจากการเถียงกันทั่วไปอย่างไร",
         "การโต้แย้งทางวิทยาศาสตร์ต้องมีข้อกล่าวอ้าง หลักฐานที่ตรวจสอบได้ "
         "และการให้เหตุผลที่เชื่อมหลักฐานเข้ากับข้อกล่าวอ้างนั้น"),
    Fact("ข้อกล่าวอ้างที่ดีในการโต้แย้งทางวิทยาศาสตร์ควรเป็นอย่างไร",
         "ควรเป็นข้อความที่ชัดเจนพอจะถูกตรวจสอบด้วยหลักฐานได้ว่าจริงหรือเท็จ"),
    Fact("หลักฐานที่ใช้สนับสนุนข้อกล่าวอ้างควรมีลักษณะใด",
         "ควรเป็นข้อมูลที่เก็บมาอย่างเป็นระบบ ระบุแหล่งที่มาได้ "
         "และผู้อื่นตรวจสอบซ้ำได้"),
    Fact("เหตุใดการอ้างว่า “คนส่วนใหญ่เชื่อแบบนี้” จึงไม่ใช่หลักฐานทางวิทยาศาสตร์",
         "เพราะจำนวนคนที่เชื่อไม่ได้บอกว่าข้อกล่าวอ้างนั้นจริงหรือไม่ "
         "ต้องอาศัยข้อมูลจากการสังเกตหรือการทดลองแทน"),
    Fact("เมื่อพบข้อมูลที่ขัดกับข้อกล่าวอ้างของตนเอง ควรทำอย่างไร",
         "ควรนำข้อมูลนั้นมาพิจารณาด้วย แล้วปรับหรือละทิ้งข้อกล่าวอ้างเดิม"
         "ถ้าหลักฐานไม่สนับสนุน"),
    Fact("การเผยแพร่ความรู้เรื่องสิ่งมีชีวิตดัดแปรพันธุกรรมควรทำอย่างไร",
         "ควรนำเสนอทั้งประโยชน์และผลกระทบพร้อมแหล่งข้อมูลที่อ้างอิงได้ "
         "ไม่ใช่เลือกเฉพาะด้านที่สนับสนุนความเห็นของตน"),
)


ARGUMENT_FACTS += (
    Fact('การอ้างอิงแหล่งข้อมูลในการโต้แย้งมีประโยชน์อย่างไร',
         'ทำให้ผู้อื่นตรวจสอบย้อนกลับได้ว่าหลักฐานมาจากไหน และน่าเชื่อถือเพียงใด'),
    Fact('เหตุผลที่เชื่อมหลักฐานกับข้อกล่าวอ้างมีบทบาทอย่างไร',
         'อธิบายว่าหลักฐานนั้นสนับสนุนข้อกล่าวอ้างได้อย่างไร ผู้ฟังจึงเห็นความเชื่อมโยงชัดเจน'),
    Fact('การโจมตีตัวผู้พูดแทนการพิจารณาหลักฐานเป็นการโต้แย้งที่ดีหรือไม่',
         'ไม่ดี เพราะลักษณะของผู้พูดไม่ได้ทำให้ข้อกล่าวอ้างจริงหรือเท็จ ต้องพิจารณาที่หลักฐาน'),
    Fact('การยอมรับข้อจำกัดของหลักฐานของตนเองช่วยการโต้แย้งอย่างไร',
         'ทำให้การโต้แย้งน่าเชื่อถือขึ้น เพราะแสดงว่าพิจารณาหลักฐานรอบด้าน ไม่ได้เลือกเฉพาะส่วนที่สนับสนุน'),
)


class Claim(NamedTuple):
    """A statement about GMOs, and the verdict on it as evidence."""
    statement: str
    verdict: str


CLAIMS = (
    Claim("“จากการทดลองภาคสนามสามปี แปลงข้าวโพดต้านแมลงใช้สารกำจัดแมลง"
          "น้อยกว่าแปลงควบคุมร้อยละ 40”",
          "เป็นข้อความที่มีข้อมูลสนับสนุน เพราะระบุวิธีเก็บข้อมูล ระยะเวลา "
          "และตัวเลขที่ตรวจสอบซ้ำได้"),
    Claim("“ฉันรู้สึกว่าอาหารดัดแปรพันธุกรรมไม่เป็นธรรมชาติ จึงต้องไม่ปลอดภัย”",
          "เป็นความเห็นส่วนตัว เพราะความรู้สึกว่าไม่เป็นธรรมชาติ"
          "ไม่ใช่ข้อมูลที่ตรวจสอบได้ว่าปลอดภัยหรือไม่"),
    Claim("“เพื่อนบอกว่ากินข้าวโพดดัดแปรพันธุกรรมแล้วปวดท้อง จึงสรุปว่า"
          "ข้าวโพดชนิดนี้เป็นอันตราย”",
          "เป็นการสรุปจากกรณีเดียวโดยไม่มีกลุ่มเปรียบเทียบ "
          "จึงยังแยกไม่ได้ว่าอาการนั้นเกิดจากข้าวโพดหรือจากสาเหตุอื่น"),
    Claim("“ผลสำรวจพบว่าคนร้อยละ 70 ไม่อยากกินอาหารดัดแปรพันธุกรรม "
          "จึงสรุปว่าอาหารนี้เป็นอันตราย”",
          "เป็นการนำความคิดเห็นของคนหมู่มากมาสรุปเรื่องความปลอดภัย "
          "ซึ่งเป็นคนละเรื่องกัน ต้องใช้ผลการทดสอบความปลอดภัยแทน"),
    Claim("“รายงานการตรวจติดตามสิบปีพบว่ายีนต้านทานแพร่ไปยังมะละกอพื้นเมือง"
          "ในรัศมี 400 เมตร”",
          "เป็นข้อความที่มีข้อมูลสนับสนุน เพราะมีการตรวจติดตามอย่างเป็นระบบ "
          "และระบุขอบเขตของผลที่พบไว้ชัดเจน"),
    Claim("“บริษัทผู้ผลิตบอกว่าผลิตภัณฑ์ของตนปลอดภัย จึงเชื่อได้ทันที”",
          "ยังสรุปไม่ได้ เพราะผู้ให้ข้อมูลมีส่วนได้ส่วนเสีย "
          "ควรตรวจสอบกับผลการทดสอบจากหน่วยงานที่เป็นอิสระด้วย"),
)


@question_type(
    "life.gmo_argument_foundation",
    display_name={"th": "องค์ประกอบของการโต้แย้งทางวิทยาศาสตร์"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=GMO_TOPIC,
)
class GmoArgumentFoundation(QuestionType):
    """What makes an argument scientific rather than merely loud."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, ARGUMENT_FACTS, topic=GMO_TOPIC,
            hint="ตรวจสามอย่างเสมอ คือข้อกล่าวอ้าง หลักฐาน "
                 "และเหตุผลที่เชื่อมสองสิ่งนี้เข้าด้วยกัน",
        )


@question_type(
    "life.gmo_argument_fluency",
    display_name={"th": "แยกข้อความที่มีข้อมูลสนับสนุนออกจากความเห็น"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=GMO_TOPIC,
)
class GmoArgumentFluency(QuestionType):
    """Judge one statement as evidence.

    ``ม.3/8``'s evidence clause is ``โดยการเผยแพร่ความรู้`` — an act. No item can
    observe it, so this set is ``standard_scope``; weighing what is worth
    publishing is as close as an item gets.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(CLAIMS)
        others = [other.verdict for other in CLAIMS
                  if other.verdict != item.verdict]
        rng.shuffle(others)
        return _labelled(
            stem=f"{item.statement} ข้อใดประเมินข้อความนี้ได้เหมาะสมที่สุด",
            correct=item.verdict, wrongs=tuple(others[:3]),
            hint="ถามว่ามีข้อมูลที่เก็บมาอย่างเป็นระบบรองรับหรือไม่ "
                 "และข้อมูลนั้นตอบคำถามที่ตั้งไว้ตรงหรือเปล่า",
            topic=GMO_TOPIC,
        )


@question_type(
    "life.gmo_argument_application",
    display_name={"th": "วิเคราะห์การโต้แย้งและการเผยแพร่ความรู้"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=GMO_TOPIC,
)
class GmoArgumentApplication(QuestionType):
    """Judge how an argument or a piece of outreach uses its evidence."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, ARGUMENT_SCENARIOS,
            hint="แยกข้อกล่าวอ้างออกจากหลักฐาน แล้วถามว่าหลักฐานนั้น"
                 "ตอบคำถามที่กำลังโต้แย้งกันอยู่จริงหรือไม่",
        ), GMO_TOPIC)
