"""การสื่อสารด้วยคลื่นแม่เหล็กไฟฟ้า และสัญญาณแอนะล็อกกับสัญญาณดิจิทัล

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.5/12

Sets moved here from: science_wave_e15.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e15 import SUBJECT, UPPER_FIVE, _labelled, _numeric

PROVENANCE = Provenance("original")


TOPIC_EM_COMMS = "การสื่อสารด้วยคลื่นแม่เหล็กไฟฟ้า และสัญญาณแอนะล็อกกับสัญญาณดิจิทัล"


COMMS_WAYS = (
    ("วิทยุ AM", "ข้อมูลเสียงถูกผสมไปกับคลื่นพาหะโดยเปลี่ยนแอมพลิจูดของคลื่นพาหะ"),
    ("วิทยุ FM", "ข้อมูลเสียงถูกผสมไปกับคลื่นพาหะโดยเปลี่ยนความถี่ของคลื่นพาหะ"),
    ("โทรศัพท์เคลื่อนที่", "ส่งข้อมูลด้วยไมโครเวฟระหว่างโทรศัพท์กับเสาส่งสัญญาณที่อยู่ใกล้ที่สุด"),
    ("ดาวเทียมสื่อสาร", "รับไมโครเวฟจากสถานีภาคพื้นดิน แล้วส่งต่อไปยังสถานีที่อยู่ไกลออกไป"),
    ("เส้นใยนำแสง", "ส่งข้อมูลเป็นจังหวะของแสงที่สะท้อนกลับหมดภายในเส้นใยแก้ว"),
    ("ไวไฟ (Wi-Fi)", "ส่งข้อมูลดิจิทัลด้วยไมโครเวฟระหว่างอุปกรณ์กับเราเตอร์ในระยะใกล้"),
)


ANALOG, DIGITAL = "สัญญาณแอนะล็อก", "สัญญาณดิจิทัล"


SIGNAL_FACTS = (
    ("มีค่าต่อเนื่อง เปลี่ยนแปลงได้ทุกค่าตามข้อมูลต้นฉบับ", ANALOG),
    ("มีค่าไม่ต่อเนื่อง แทนด้วยรหัส 0 และ 1", DIGITAL),
    ("เมื่อมีสัญญาณรบกวนปนเข้ามา แยกสัญญาณรบกวนออกได้ยาก คุณภาพจึงลดลงเมื่อส่งไกล", ANALOG),
    ("ทนต่อสัญญาณรบกวนได้ดี เพราะเครื่องรับเพียงแยกให้ได้ว่าเป็น 0 หรือ 1", DIGITAL),
    ("บีบอัดข้อมูลและเข้ารหัสเพื่อความปลอดภัยได้ง่าย", DIGITAL),
    ("เป็นรูปแบบของสัญญาณที่ใช้ในวิทยุ AM และ FM แบบดั้งเดิม", ANALOG),
    ("คัดลอกได้หลายครั้งโดยคุณภาพไม่ลดลง", DIGITAL),
    ("ตรวจพบและแก้ไขข้อผิดพลาดที่เกิดระหว่างการส่งได้", DIGITAL),
    ("เป็นรูปแบบของข้อมูลในแผ่นซีดีและไฟล์เพลงบนโทรศัพท์", DIGITAL),
    ("เป็นรูปแบบของข้อมูลในแผ่นเสียงไวนิลและเทปคาสเซ็ต", ANALOG),
    ("เมื่อคัดลอกต่อกันหลายทอด เสียงรบกวนสะสมจนคุณภาพลดลง", ANALOG),
)


@question_type(
    "phys.em_comms_foundation",
    display_name={"th": "อธิบายการสื่อสารโดยอาศัยคลื่นแม่เหล็กไฟฟ้า"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EM_COMMS,
)
class EmCommsFoundation(QuestionType):
    """The first free verb, อธิบาย: how each technology carries information."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        way, how = rng.choice(COMMS_WAYS)
        if rng.random() < 0.6:
            return _labelled(
                stem=f"{way}ส่งผ่านสารสนเทศด้วยคลื่นแม่เหล็กไฟฟ้าอย่างไร",
                correct=how, wrongs=tuple([h for w, h in COMMS_WAYS if w != way]),
                topic=TOPIC_EM_COMMS,
                hint="ข้อมูลถูกผสมไปกับคลื่นพาหะ (AM เปลี่ยนแอมพลิจูด FM เปลี่ยนความถี่) หรือส่งเป็นจังหวะของคลื่นผ่านเสา ดาวเทียม หรือเส้นใยนำแสง")
        return _labelled(
            stem=f"\"{how}\" เป็นหลักการของการสื่อสารแบบใด",
            correct=way, wrongs=tuple([w for w, h in COMMS_WAYS if w != way]),
            topic=TOPIC_EM_COMMS,
            hint="ดูว่าข้อมูลเดินทางด้วยคลื่นช่วงใด และผ่านอะไร: อากาศ เสาส่ง ดาวเทียม หรือเส้นใยแก้ว")


@question_type(
    "phys.em_comms_fluency",
    display_name={"th": "เปรียบเทียบสัญญาณแอนะล็อกกับสัญญาณดิจิทัล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EM_COMMS,
)
class EmCommsFluency(QuestionType):
    """The second free verb, เปรียบเทียบ: analogue against digital."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        fact, kind = rng.choice(SIGNAL_FACTS)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"\"{fact}\" เป็นลักษณะของสัญญาณแบบใด",
                correct=kind,
                wrongs=(DIGITAL if kind == ANALOG else ANALOG, "เป็นลักษณะของทั้งสองแบบเท่ากัน",
                        "ไม่ใช่ลักษณะของสัญญาณแบบใดเลย"),
                topic=TOPIC_EM_COMMS,
                hint="แอนะล็อกมีค่าต่อเนื่องและไวต่อสัญญาณรบกวน ดิจิทัลเป็น 0 กับ 1 จึงทนสัญญาณรบกวนและคัดลอกได้ไม่เสียคุณภาพ")
        other = DIGITAL if kind == ANALOG else ANALOG
        mine = [f for f, k in SIGNAL_FACTS if k == kind]
        theirs = [f for f, k in SIGNAL_FACTS if k == other]
        return _labelled(
            stem=f"ข้อใดเป็นลักษณะของ{kind} ไม่ใช่ของ{other}",
            correct=rng.choice(mine), wrongs=tuple(theirs),
            topic=TOPIC_EM_COMMS,
            hint="แอนะล็อกมีค่าต่อเนื่องและไวต่อสัญญาณรบกวน ดิจิทัลเป็น 0 กับ 1 จึงทนสัญญาณรบกวนและคัดลอกได้ไม่เสียคุณภาพ")


@question_type(
    "phys.em_comms_application",
    display_name={"th": "คำนวณระดับสัญญาณดิจิทัลและเวลาส่งข้อมูล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EM_COMMS,
)
class EmCommsApplication(QuestionType):
    """Bits to levels, and a file's size to the time it takes to send."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            bits = rng.randint(2, 10)
            return _numeric(
                stem=f"สัญญาณดิจิทัลที่ใช้รหัส {bits} บิตต่อหนึ่งค่า แทนค่าที่ต่างกันได้ทั้งหมดกี่ค่า",
                answer=2 ** bits, wrongs=[2 * bits, bits * bits, 10 * bits],
                unit="ค่า", topic=TOPIC_EM_COMMS,
                hint="แต่ละบิตเป็นได้ 2 แบบ (0 หรือ 1) รหัส n บิตจึงแทนค่าได้ 2ⁿ ค่า")
        if shape == 1:
            rate = rng.choice((5, 10, 20, 25, 40, 50, 100))
            megabytes = rng.choice([m for m in (5, 10, 25, 50, 100, 125, 250, 500) if (m * 8) % rate == 0])
            seconds = Fraction(megabytes * 8, rate)
            return _numeric(
                stem=(f"ส่งไฟล์ขนาด {megabytes} เมกะไบต์ ผ่านอินเทอร์เน็ตไร้สายที่มีอัตราการส่งข้อมูล "
                      f"{rate} เมกะบิตต่อวินาที ต้องใช้เวลากี่วินาที (1 ไบต์ = 8 บิต)"),
                answer=seconds, wrongs=[Fraction(megabytes, rate), seconds * 8, Fraction(rate * 8, megabytes)],
                unit="วินาที", topic=TOPIC_EM_COMMS,
                hint="แปลงเมกะไบต์เป็นเมกะบิต (คูณ 8) แล้วหารด้วยอัตราการส่งข้อมูล")
        noise = rng.choice(("ส่งสัญญาณผ่านระยะทางไกลมาก", "มีสัญญาณรบกวนจากเครื่องใช้ไฟฟ้า",
                            "ต้องคัดลอกข้อมูลต่อกันหลายทอด"))
        return _labelled(
            stem=f"ถ้า{noise} การส่งข้อมูลแบบใดจะรักษาคุณภาพของข้อมูลได้ดีกว่า และเพราะเหตุใด",
            correct="สัญญาณดิจิทัล เพราะเครื่องรับเพียงแยก 0 กับ 1 จึงสร้างสัญญาณเดิมกลับได้แม้มีสัญญาณรบกวน",
            wrongs=("สัญญาณแอนะล็อก เพราะมีค่าต่อเนื่องจึงไม่เกิดสัญญาณรบกวน",
                    "สัญญาณแอนะล็อก เพราะคัดลอกได้โดยคุณภาพไม่ลดลง",
                    "ทั้งสองแบบเท่ากัน เพราะเป็นคลื่นแม่เหล็กไฟฟ้าเหมือนกัน"),
            topic=TOPIC_EM_COMMS,
            hint="สัญญาณรบกวนทำให้ค่าของสัญญาณเพี้ยน สัญญาณแบบใดแก้กลับได้ง่ายกว่า")
