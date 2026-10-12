"""การเคลื่อนที่ของสัตว์

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/9

Sets moved here from: science_wave_f67.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f67 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_MOVE = "การเคลื่อนที่ของสัตว์"


MOVERS = (
    ("แมงกะพรุน", "หดตัวของเซลล์กล้ามเนื้อรอบร่มพ่นน้ำออก ทำให้ตัวเคลื่อนที่ไปในทิศตรงข้าม"),
    ("หมึก", "หดกล้ามเนื้อแมนเทิลพ่นน้ำออกทางไซฟอนอย่างแรง"),
    ("ดาวทะเล", "ใช้ระบบท่อน้ำดันทิวบ์ฟีตยืดหดและยึดเกาะ"),
    ("ไส้เดือนดิน", "กล้ามเนื้อวงและกล้ามเนื้อตามยาวทำงานสลับกัน ร่วมกับเดือยช่วยยึดดิน"),
    ("แมลง", "กล้ามเนื้อยึดอยู่ภายในโครงร่างแข็งภายนอก ขยับขาและปีก"),
    ("ปลา", "กล้ามเนื้อสองข้างลำตัวหดสลับกันเป็นรูปตัว S และใช้ครีบช่วยบังคับทิศ"),
    ("นก", "กล้ามเนื้อหน้าอกขนาดใหญ่กระพือปีก กระดูกกลวงทำให้ตัวเบา"),
)


MOVE_HINT = ("แมงกะพรุนและหมึกพ่นน้ำ ดาวทะเลใช้ระบบท่อน้ำและทิวบ์ฟีต ไส้เดือนใช้กล้ามเนื้อวงกับตามยาวสลับกัน "
             "แมลงมีกล้ามเนื้อในโครงร่างภายนอก ปลาหดกล้ามเนื้อเป็นรูปตัว S นกใช้กล้ามเนื้ออกกระพือปีก")


MOVE_FACTS = (
    ("เมื่อกล้ามเนื้อวงของไส้เดือนดินหดตัว ลำตัวส่วนนั้นเป็นอย่างไร", "ยืดยาวและเรียวเล็กลง",
     ("หดสั้นและอ้วนขึ้น", "ยืดยาวและอ้วนขึ้น", "หดสั้นและเรียวเล็กลง", "งอเป็นรูปตัว S")),
    ("เมื่อกล้ามเนื้อตามยาวของไส้เดือนดินหดตัว ลำตัวส่วนนั้นเป็นอย่างไร", "หดสั้นและอ้วนขึ้น",
     ("ยืดยาวและเรียวเล็กลง", "ยืดยาวและอ้วนขึ้น", "หดสั้นและเรียวเล็กลง", "งอเป็นรูปตัว S")),
    ("กล้ามเนื้อสองชุดที่ทำงานตรงข้ามกันเรียกว่าอะไร", "กล้ามเนื้อแอนทาโกนิซึม", ("กล้ามเนื้อหัวใจ", "กล้ามเนื้อเรียบ", "กล้ามเนื้อลายเส้นเดียว", "กล้ามเนื้อทำงานพร้อมกัน")),
    ("กล้ามเนื้อของแมลงยึดติดกับส่วนใด", "ผนังด้านในของโครงร่างแข็งภายนอก", ("กระดูกภายใน", "ผิวด้านนอกของโครงร่างแข็งภายนอก", "ระบบท่อน้ำ", "กระดูกภายในที่อยู่ใต้ผิวหนัง")),
    ("ถุงลมและกระดูกกลวงของนกช่วยการบินอย่างไร", "ทำให้น้ำหนักตัวเบา", ("ทำให้กล้ามเนื้อใหญ่ขึ้น", "ทำให้ขนยาวขึ้น",
                                                                 "ทำให้กระดูกหนักขึ้นเพื่อทรงตัว", "ทำให้ไม่ต้องใช้กล้ามเนื้อ")),
    ("ทิวบ์ฟีตของดาวทะเลยืดออกได้เพราะเหตุใด", "น้ำในระบบท่อน้ำถูกดันเข้าไป", ("กล้ามเนื้อหัวใจบีบ", "อากาศจากเหงือกถูกดันเข้าไป",
                                                                      "กระดูกภายในยืดตัว", "เลือดจากหัวใจถูกสูบเข้าไป")),
    ("หมึกเคลื่อนที่ถอยหลังอย่างรวดเร็วได้เพราะเหตุใด", "พ่นน้ำออกทางไซฟอนอย่างแรงไปทางด้านหน้า",
     ("กระพือครีบข้างลำตัวเท่านั้น", "ดูดน้ำเข้าทางไซฟอนแล้วลอยตัวขึ้นไป", "ใช้ขาเป็นข้อปล้อง", "ใช้หนวดยึดพื้นแล้วดึงตัวไปข้างหน้า")),
    ("ครีบหางของปลาทำหน้าที่ใดเป็นหลัก", "ช่วยผลักน้ำให้ตัวเคลื่อนที่ไปข้างหน้าและเปลี่ยนทิศทาง",
     ("ช่วยให้ปลาหายใจได้ โดยโบกน้ำผ่านเหงือกตลอดเวลา", "ใช้กินอาหาร", "ช่วยรับรู้การสั่นสะเทือนของน้ำ เพื่อหาทิศทางของอาหาร", "ใช้เก็บอาหาร")),
)


@question_type(
    "biology.animal_locomotion_foundation",
    display_name={"th": "วิธีการเคลื่อนที่ของสัตว์ต่าง ๆ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MOVE,
)
class AnimalLocomotionFoundation(QuestionType):
    """Each animal and its way of moving."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        animal, how = rng.choice(MOVERS)
        others = rng.sample([m for m in MOVERS if m[0] != animal], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{animal}เคลื่อนที่อย่างไร", correct=how, wrongs=tuple(m[1] for m in others), topic=TOPIC_MOVE, hint=MOVE_HINT)
        return _labelled(stem=f"สัตว์ใดเคลื่อนที่โดย{how}", correct=animal, wrongs=tuple(m[0] for m in others), topic=TOPIC_MOVE,
                         hint=MOVE_HINT)


@question_type(
    "biology.animal_locomotion_fluency",
    display_name={"th": "การทำงานของกล้ามเนื้อและโครงร่างในการเคลื่อนที่ของสัตว์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MOVE,
)
class AnimalLocomotionFluency(QuestionType):
    """Antagonistic muscles, exoskeletons and light bones."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(MOVE_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_MOVE, hint=MOVE_HINT)


@question_type(
    "biology.animal_locomotion_application",
    display_name={"th": "เปรียบเทียบการเคลื่อนที่ของสัตว์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MOVE,
)
class AnimalLocomotionApplication(QuestionType):
    """Which animals share a way of moving."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        groups = {"อาศัยการพ่นน้ำ": ("แมงกะพรุน", "หมึก"),
                  "มีโครงร่างแข็งภายนอกให้กล้ามเนื้อยึด": ("แมลง", "กุ้ง", "แมงมุม"),
                  "มีโครงร่างแข็งภายในให้กล้ามเนื้อยึด": ("ปลา", "นก", "คน", "กบ"),
                  "ใช้แรงดันของของเหลวในลำตัวร่วมกับกล้ามเนื้อ": ("ไส้เดือนดิน", "ดาวทะเล")}
        label = rng.choice(sorted(groups))
        others = [a for k, v in groups.items() if k != label for a in v]
        return _labelled(stem=f"สัตว์ใดเคลื่อนที่โดย{label}", correct=rng.choice(groups[label]), wrongs=tuple(others),
                         topic=TOPIC_MOVE, hint=MOVE_HINT)
