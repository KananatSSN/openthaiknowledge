"""โครงสร้างและหน้าที่ของเซลล์ประสาท

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/2

Sets moved here from: science_wave_f65.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f65 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_NEURON = "โครงสร้างและหน้าที่ของเซลล์ประสาท"


PARTS = (
    ("เดนไดรต์", "รับกระแสประสาทเข้าสู่ตัวเซลล์"),
    ("แอกซอน", "นำกระแสประสาทออกจากตัวเซลล์"),
    ("ตัวเซลล์", "มีนิวเคลียสและออร์แกเนลล์ส่วนใหญ่"),
    ("เยื่อไมอีลิน", "เป็นฉนวนหุ้มแอกซอนทำให้กระแสประสาทเคลื่อนที่เร็วขึ้น"),
    ("โนดออฟแรนเวียร์", "ช่วงของแอกซอนที่ไม่มีเยื่อไมอีลินหุ้ม ทำให้กระแสประสาทกระโดดข้าม"),
    ("ปลายแอกซอน", "หลั่งสารสื่อประสาทที่ไซแนปส์"),
)


TYPES = (
    ("เซลล์ประสาทรับความรู้สึก", "นำกระแสประสาทจากหน่วยรับความรู้สึกเข้าสู่ระบบประสาทส่วนกลาง"),
    ("เซลล์ประสาทสั่งการ", "นำกระแสประสาทจากระบบประสาทส่วนกลางไปยังหน่วยปฏิบัติงาน เช่น กล้ามเนื้อ"),
    ("เซลล์ประสาทประสานงาน", "เชื่อมต่อระหว่างเซลล์ประสาทภายในสมองและไขสันหลัง"),
)


SHAPES = (("เซลล์ประสาทขั้วเดียว", "มีแขนงยื่นออกจากตัวเซลล์ 1 แขนงแล้วแยกเป็นสองทาง พบในเซลล์ประสาทรับความรู้สึก"),
          ("เซลล์ประสาทสองขั้ว", "มีแขนงออกจากตัวเซลล์ 2 แขนง พบในเรตินา"),
          ("เซลล์ประสาทหลายขั้ว", "มีเดนไดรต์หลายแขนงและแอกซอน 1 แขนง พบในเซลล์ประสาทสั่งการ"))


NEURON_HINT = ("เดนไดรต์รับกระแสประสาท แอกซอนส่งออก เยื่อไมอีลินเป็นฉนวน เซลล์ประสาทรับความรู้สึกนำเข้า "
               "เซลล์ประสาทสั่งการนำออก เซลล์ประสาทประสานงานเชื่อมต่อในสมองและไขสันหลัง")


@question_type(
    "biology.neuron_foundation",
    display_name={"th": "ส่วนประกอบของเซลล์ประสาทและหน้าที่"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_NEURON,
)
class NeuronFoundation(QuestionType):
    """Dendrite, axon, myelin, nodes, terminals."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        part, role = rng.choice(PARTS)
        others = rng.sample([p for p in PARTS if p[0] != part], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{part}ของเซลล์ประสาทมีหน้าที่อย่างไร", correct=role, wrongs=tuple(p[1] for p in others), topic=TOPIC_NEURON,
                             hint=NEURON_HINT)
        return _labelled(stem=f"ส่วนใดของเซลล์ประสาท{role}", correct=part, wrongs=tuple(p[0] for p in others), topic=TOPIC_NEURON,
                         hint=NEURON_HINT)


@question_type(
    "biology.neuron_fluency",
    display_name={"th": "ชนิดของเซลล์ประสาทตามหน้าที่และรูปร่าง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_NEURON,
)
class NeuronFluency(QuestionType):
    """Sensory, motor and interneurons; one, two or many poles."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        pool = TYPES if rng.random() < 0.55 else SHAPES
        name, what = rng.choice(pool)
        others = [p for p in pool if p[0] != name]
        extra_names = ("เซลล์ชวันน์", "เซลล์เกลีย", "เซลล์กล้ามเนื้อลาย")
        extra_whats = ("สร้างเยื่อไมอีลินหุ้มแอกซอน", "สร้างแอนติบอดีต่อต้านเชื้อโรค", "ลำเลียงออกซิเจนในเลือด")
        if rng.random() < 0.5:
            return _labelled(stem=f"เซลล์ประสาทชนิดใด{what}", correct=name, wrongs=(*(o[0] for o in others), rng.choice(extra_names)),
                             topic=TOPIC_NEURON, hint=NEURON_HINT)
        return _labelled(stem=f"{name}มีลักษณะหรือหน้าที่อย่างไร", correct=what, wrongs=(*(o[1] for o in others), rng.choice(extra_whats)),
                         topic=TOPIC_NEURON, hint=NEURON_HINT)


@question_type(
    "biology.neuron_application",
    display_name={"th": "คำนวณเวลาและอัตราเร็วของกระแสประสาท"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_NEURON,
)
class NeuronApplication(QuestionType):
    """Myelinated fibres carry impulses far faster than bare ones."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        speed = rng.choice((1, 2, 5, 10, 20, 25, 50, 100, 120))
        length = Fraction(rng.choice((50, 60, 80, 100, 120, 150, 200)), 100)
        ms = length / speed * 1000
        if (ms * 100).denominator != 1:
            speed, ms = 100, length * 10
        fibre = "มีเยื่อไมอีลิน" if speed >= 20 else "ไม่มีเยื่อไมอีลิน"
        if rng.random() < 0.6:
            return numeric(stem=f"กระแสประสาทเคลื่อนที่ในใยประสาทที่{fibre}ด้วยอัตราเร็ว {speed} m/s ระยะทาง {show(length)} m ใช้เวลากี่มิลลิวินาที",
                           answer=ms, wrongs=[ms / 1000 if (ms / 1000 * 100).denominator == 1 else ms * 10, length * speed, ms * 2],
                           unit="ms", topic=TOPIC_NEURON, hint="เวลา = ระยะทาง ÷ อัตราเร็ว แล้วคูณ 1,000 เพื่อเปลี่ยนเป็นมิลลิวินาที")
        return numeric(stem=f"กระแสประสาทเคลื่อนที่ได้ {show(length)} m ในเวลา {show(ms)} ms อัตราเร็วเป็นกี่เมตรต่อวินาที", answer=speed,
                       wrongs=[length * ms if (length * ms * 100).denominator == 1 else speed * 10, speed * 1000, ms], unit="m/s",
                       topic=TOPIC_NEURON, hint="อัตราเร็ว = ระยะทาง ÷ เวลา (แปลง ms เป็น s ก่อน)")
