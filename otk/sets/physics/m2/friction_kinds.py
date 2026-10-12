"""แรงเสียดทานสถิตและแรงเสียดทานจลน์

ฟิสิกส์ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.2/6

Sets moved here from: science_wave_d19.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c23 import Part
from otk.sets._support.science_wave_c24 import parts_item
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d18 import SECONDARY_TWO
from otk.sets._support.science_wave_d19 import _facts

PROVENANCE = Provenance("original")


FRICTION_KINDS_TOPIC = "แรงเสียดทานสถิตและแรงเสียดทานจลน์"


def friction_record(rng: Random) -> tuple[list[tuple[str, int, str]], int, int]:
    """Pull readings as they rise; the block starts sliding at the peak."""
    peak = rng.randint(6, 12)
    kinetic = rng.randint(3, peak - 2)
    low = rng.randint(1, kinetic - 1) if kinetic > 2 else 1
    mid = rng.randint(low + 1, peak - 1)
    rows = [
        ("ครั้งที่ 1", low, "กล่องอยู่นิ่ง"),
        ("ครั้งที่ 2", mid, "กล่องอยู่นิ่ง"),
        ("ครั้งที่ 3", peak, "กล่องเริ่มเคลื่อนที่"),
        ("ขณะลากต่อด้วยความเร็วคงที่", kinetic, "กล่องเคลื่อนที่"),
    ]
    return rows, peak, kinetic


def friction_parts(low: int, peak: int, kinetic: int) -> tuple[Part, ...]:
    return (
        Part("ขณะกล่องอยู่นิ่ง", f"เกิดแรงเสียดทานสถิตเท่ากับแรงดึง เช่น เมื่อดึง {low} นิวตัน แรงเสียดทานสถิตก็เป็น {low} นิวตัน",
             f"ไม่มีแรงเสียดทาน เพราะกล่องยังไม่เคลื่อนที่ แม้จะดึงด้วยแรง {low} นิวตัน"),
        Part("แรงเสียดทานสถิตสูงสุด", f"มีค่า {peak} นิวตัน ซึ่งเป็นแรงดึงขณะกล่องเริ่มเคลื่อนที่",
             f"มีค่า {kinetic} นิวตัน ซึ่งเป็นแรงดึงขณะกล่องเคลื่อนที่ไปแล้ว"),
        Part("ขณะกล่องเคลื่อนที่", f"เกิดแรงเสียดทานจลน์ {kinetic} นิวตัน ซึ่งน้อยกว่าแรงเสียดทานสถิตสูงสุด",
             f"เกิดแรงเสียดทานจลน์ {kinetic} นิวตัน ซึ่งมากกว่าแรงเสียดทานสถิตสูงสุด"),
    )


FRICTION_KINDS_HINT = "วัตถุยังไม่ขยับคือแรงเสียดทานสถิต ซึ่งเพิ่มตามแรงที่กระทำจนถึงค่าสูงสุด วัตถุไถลอยู่คือแรงเสียดทานจลน์"


FRICTION_KINDS_FACTS = (
    ("แรงเสียดทานสถิตเกิดขึ้นเมื่อใด", "เมื่อมีแรงกระทำแต่วัตถุยังไม่เคลื่อนที่เทียบกับผิวสัมผัส",
     ("เมื่อวัตถุกำลังไถลไปบนพื้น", "เมื่อไม่มีแรงใดกระทำต่อวัตถุ", "เมื่อวัตถุลอยอยู่กลางอากาศ",
      "เมื่อวัตถุตกอย่างอิสระ", "เมื่อวัตถุหมุนอยู่กับที่ในอากาศ")),
    ("แรงเสียดทานจลน์เกิดขึ้นเมื่อใด", "เมื่อวัตถุกำลังเคลื่อนที่เทียบกับผิวสัมผัส",
     ("เมื่อวัตถุอยู่นิ่งบนพื้นและไม่มีแรงกระทำ", "เมื่อผลักวัตถุแต่วัตถุยังไม่ขยับ", "เมื่อวัตถุลอยอยู่ในอวกาศ",
      "เมื่อวัตถุถูกแขวนนิ่งด้วยเชือก", "เมื่อวัตถุวางนิ่งบนโต๊ะ")),
    ("โดยทั่วไป แรงเสียดทานสถิตสูงสุดเทียบกับแรงเสียดทานจลน์บนผิวคู่เดียวกันเป็นอย่างไร", "แรงเสียดทานสถิตสูงสุดมากกว่า",
     ("แรงเสียดทานจลน์มากกว่า", "เท่ากันเสมอ", "แรงเสียดทานสถิตสูงสุดเป็นศูนย์", "แรงเสียดทานจลน์เป็นสองเท่า",
      "เปรียบเทียบไม่ได้")),
    ("ผลักกล่องด้วยแรง 4 นิวตันแล้วกล่องยังไม่ขยับ แรงเสียดทานสถิตขณะนั้นเป็นเท่าใด", "4 นิวตัน เท่ากับแรงผลัก",
     ("0 นิวตัน เพราะกล่องไม่เคลื่อนที่", "มากกว่า 4 นิวตัน", "น้อยกว่า 4 นิวตัน", "8 นิวตัน", "เท่ากับน้ำหนักของกล่อง")),
    ("เมื่อค่อย ๆ เพิ่มแรงดึงกล่องที่อยู่นิ่ง แรงเสียดทานสถิตเปลี่ยนไปอย่างไร", "เพิ่มขึ้นตามแรงดึงจนถึงค่าสูงสุด แล้วกล่องจึงเริ่มเคลื่อนที่",
     ("คงที่ตลอดตั้งแต่เริ่มดึง", "ลดลงเมื่อดึงแรงขึ้น", "เป็นศูนย์จนกว่ากล่องจะเคลื่อนที่", "เพิ่มขึ้นโดยไม่มีค่าสูงสุด",
      "มีค่าเท่าน้ำหนักของกล่องเสมอ")),
)


FRICTION_KINDS_SCENARIOS = (
    ("เหตุใดการเริ่มผลักตู้หนักให้ขยับจึงยากกว่าการผลักตู้ที่ไถลอยู่แล้ว",
     "แรงเสียดทานสถิตสูงสุดมีค่ามากกว่าแรงเสียดทานจลน์",
     ("แรงเสียดทานจลน์มีค่ามากกว่าแรงเสียดทานสถิต", "ตู้หนักขึ้นเมื่ออยู่นิ่ง", "ขณะไถลไม่มีแรงเสียดทาน")),
    ("กล่องมีแรงเสียดทานสถิตสูงสุด 15 นิวตัน ถ้าผลักด้วยแรง 10 นิวตัน กล่องจะเป็นอย่างไร และแรงเสียดทานเป็นเท่าใด",
     "กล่องอยู่นิ่ง แรงเสียดทานสถิตเท่ากับ 10 นิวตัน",
     ("กล่องเคลื่อนที่ แรงเสียดทานจลน์เท่ากับ 15 นิวตัน", "กล่องอยู่นิ่ง แรงเสียดทานสถิตเท่ากับ 15 นิวตัน", "กล่องอยู่นิ่ง เพราะไม่มีแรงเสียดทานเลย")),
    ("ระบบเบรกป้องกันล้อล็อก (ABS) ช่วยให้รถหยุดได้ดีขึ้นบนถนนลื่นอย่างไร",
     "ไม่ให้ล้อไถล ล้อจึงยังได้แรงเสียดทานสถิตซึ่งมากกว่าแรงเสียดทานจลน์",
     ("ทำให้ล้อไถลเร็วขึ้นเพื่อเพิ่มแรงเสียดทานจลน์ให้มากกว่าแรงเสียดทานสถิต", "ลดแรงเสียดทานทั้งหมดให้เป็นศูนย์ รถจึงหยุดได้ทันที",
      "ทำให้รถหนักขึ้นจนแรงเสียดทานจลน์มากกว่าแรงเสียดทานสถิต")),
)


@question_type(
    "phys.friction_kinds_foundation",
    display_name={"th": "จำแนกแรงเสียดทานสถิตและแรงเสียดทานจลน์"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FRICTION_KINDS_TOPIC,
)
class FrictionKindsFoundation(QuestionType):
    """A situation; static or kinetic friction."""

    CASES = (
        ("ผลักตู้หนักแต่ตู้ยังไม่ขยับ", True),
        ("รถยนต์จอดนิ่งบนทางลาดโดยไม่ไถลลง", True),
        ("หนังสือวางนิ่งบนโต๊ะที่เอียงเล็กน้อย", True),
        ("ลากกล่องไถลไปบนพื้น", False),
        ("นักสกีไถลลงเนินหิมะ", False),
        ("ลูกฮอกกี้ไถลบนลานน้ำแข็งจนช้าลง", False),
        ("กล่องวางนิ่งบนกระบะรถที่กำลังออกตัวโดยไม่ไถล", True),
        ("ดึงเชือกลากโต๊ะหนักแต่โต๊ะยังไม่เลื่อน", True),
        ("รองเท้าที่ยืนนิ่งบนทางลาดชันโดยไม่ลื่น", True),
        ("ยางลบวางนิ่งบนหนังสือที่ยกเอียงขึ้นเล็กน้อย", True),
        ("แก้วน้ำวางนิ่งบนถาดที่ถูกยกเดิน", True),
        ("ตะปูที่ตอกอยู่ในเนื้อไม้โดยไม่หลุดออก", True),
        ("เด็กไถลลงจากกระดานลื่น", False),
        ("ถูพื้นด้วยไม้ถูพื้นไปมา", False),
        ("ยางรถที่ล้อล็อกไถลบนถนนขณะเบรกกะทันหัน", False),
        ("ใช้ยางลบถูกระดาษเพื่อลบรอยดินสอ", False),
        ("เลื่อนตู้เย็นไปตามพื้นห้องครัว", False),
        ("ขัดเงาโต๊ะด้วยผ้า", False),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _facts(rng, FRICTION_KINDS_FACTS, hint=FRICTION_KINDS_HINT, topic=FRICTION_KINDS_TOPIC)
        case, static = rng.choice(self.CASES)
        s = "แรงเสียดทานสถิต เพราะวัตถุยังไม่เคลื่อนที่เทียบกับผิวสัมผัส"
        k = "แรงเสียดทานจลน์ เพราะวัตถุกำลังเคลื่อนที่เทียบกับผิวสัมผัส"
        return _labelled(
            stem=f"\"{case}\" เกิดแรงเสียดทานชนิดใด",
            correct=s if static else k,
            wrongs=(k if static else s,
                    "แรงเสียดทานสถิต เพราะวัตถุกำลังเคลื่อนที่เทียบกับผิวสัมผัส" if static
                    else "แรงเสียดทานจลน์ เพราะวัตถุยังไม่เคลื่อนที่เทียบกับผิวสัมผัส",
                    "ไม่มีแรงเสียดทาน เพราะไม่มีใครออกแรง"),
            hint="วัตถุยังไม่ขยับคือแรงเสียดทานสถิต วัตถุไถลอยู่คือแรงเสียดทานจลน์",
            topic=FRICTION_KINDS_TOPIC,
        )


@question_type(
    "phys.friction_kinds_fluency",
    display_name={"th": "อธิบายแรงเสียดทานสถิตและแรงเสียดทานจลน์จากผลการทดลอง"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FRICTION_KINDS_TOPIC,
)
class FrictionKindsFluency(QuestionType):
    """Spring-scale readings as a box starts to slide; both kinds of friction together."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rows, peak, kinetic = friction_record(rng)
        record = " / ".join(f"{label}: อ่านได้ {value} นิวตัน {state}" for label, value, state in rows)
        return parts_item(
            rng, friction_parts(rows[0][1], peak, kinetic),
            stem=(f"นักเรียนใช้เครื่องชั่งสปริงดึงกล่องบนพื้นโดยค่อย ๆ เพิ่มแรง ได้ผลดังนี้ — {record} "
                  "จากหลักฐานนี้ ข้อใดอธิบายแรงเสียดทานได้ถูกต้องทั้งหมด"),
            hint="ก่อนเคลื่อนที่ แรงเสียดทานสถิตเท่ากับแรงดึง ค่าสูงสุดคือแรงขณะเริ่มเคลื่อนที่ หลังจากนั้นเป็นแรงเสียดทานจลน์",
            topic=FRICTION_KINDS_TOPIC,
        )


@question_type(
    "phys.friction_kinds_application",
    display_name={"th": "ใช้แรงเสียดทานสถิตและจลน์อธิบายสถานการณ์"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FRICTION_KINDS_TOPIC,
)
class FrictionKindsApplication(QuestionType):
    """Authored cases, and a push against a known largest static friction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.65:
            thing = rng.choice(("กล่อง", "ตู้", "โต๊ะ", "ลังผลไม้", "เครื่องซักผ้า"))
            peak = rng.randrange(10, 81, 5)
            push = rng.choice((rng.randrange(5, peak, 5), rng.randrange(peak + 5, peak + 31, 5)))
            if push < peak:
                answer = f"{thing}อยู่นิ่ง แรงเสียดทานสถิตเท่ากับ {push} นิวตัน"
                wrongs = (f"{thing}เคลื่อนที่ แรงเสียดทานจลน์เท่ากับ {peak} นิวตัน", f"{thing}อยู่นิ่ง แรงเสียดทานสถิตเท่ากับ {peak} นิวตัน",
                          f"{thing}อยู่นิ่ง เพราะไม่มีแรงเสียดทานเลย")
            else:
                answer = f"{thing}เริ่มเคลื่อนที่ เพราะแรงผลักเกินแรงเสียดทานสถิตสูงสุด"
                wrongs = (f"{thing}อยู่นิ่ง แรงเสียดทานสถิตเท่ากับ {push} นิวตัน",
                          f"{thing}อยู่นิ่ง เพราะแรงเสียดทานสถิตเพิ่มตามแรงผลักได้ไม่จำกัด",
                          f"{thing}เริ่มเคลื่อนที่ เพราะแรงเสียดทานกลายเป็นศูนย์")
            return _labelled(
                stem=(f"{thing}บนพื้นมีแรงเสียดทานสถิตสูงสุด {peak} นิวตัน ถ้าผลักด้วยแรง {push} นิวตัน "
                      f"{thing}จะเป็นอย่างไร และแรงเสียดทานเป็นอย่างไร"),
                correct=answer, wrongs=wrongs,
                hint="ถ้าแรงผลักไม่เกินแรงเสียดทานสถิตสูงสุด วัตถุอยู่นิ่งและแรงเสียดทานเท่ากับแรงผลัก ถ้าเกินวัตถุจึงเริ่มเคลื่อนที่",
                topic=FRICTION_KINDS_TOPIC,
            )
        return _retopic(scenario_question(
            rng, FRICTION_KINDS_SCENARIOS,
            hint="แรงเสียดทานสถิตปรับตามแรงที่กระทำจนถึงค่าสูงสุด เมื่อไถลแล้วแรงเสียดทานจลน์มีค่าน้อยกว่า",
        ), FRICTION_KINDS_TOPIC)
