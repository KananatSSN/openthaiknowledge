"""เซลล์ปฐมภูมิและเซลล์ทุติยภูมิ

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/30

Sets moved here from: science_wave_f40.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f40 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_BATTERY = "เซลล์ปฐมภูมิและเซลล์ทุติยภูมิ"


PRIMARY, SECONDARY = "เซลล์ปฐมภูมิ (ใช้แล้วทิ้ง)", "เซลล์ทุติยภูมิ (ประจุไฟใหม่ได้)"


# (cell, kind, anode, cathode, electrolyte)
CELLS = (
    ("เซลล์ถ่านไฟฉาย (เซลล์เลอคลังเช)", PRIMARY, "Zn", "แท่งแกรไฟต์กับ MnO₂", "NH₄Cl และ ZnCl₂ ชื้น"),
    ("เซลล์แอลคาไลน์", PRIMARY, "Zn", "MnO₂", "KOH"),
    ("เซลล์กระดุมซิลเวอร์ออกไซด์", PRIMARY, "Zn", "Ag₂O", "KOH"),
    ("เซลล์ลิเทียมแบบกระดุม", PRIMARY, "Li", "MnO₂", "เกลือลิเทียมในตัวทำละลายอินทรีย์"),
    ("แบตเตอรี่ตะกั่ว-กรด (แบตเตอรี่รถยนต์)", SECONDARY, "Pb", "PbO₂", "H₂SO₄"),
    ("แบตเตอรี่นิกเกิล-แคดเมียม", SECONDARY, "Cd", "NiO(OH)", "KOH"),
    ("แบตเตอรี่ลิเทียมไอออน", SECONDARY, "แกรไฟต์ที่มีลิเทียมแทรก", "LiCoO₂", "เกลือลิเทียมในตัวทำละลายอินทรีย์"),
    ("แบตเตอรี่นิกเกิล-โลหะไฮไดรด์", SECONDARY, "โลหะผสมที่เก็บไฮโดรเจน", "NiO(OH)", "KOH"),
)


LEAD_ACID = (
    ("ขณะแบตเตอรี่ตะกั่ว-กรดจ่ายไฟ ความเข้มข้นของ H₂SO₄ เปลี่ยนอย่างไร", "ลดลง เพราะ H₂SO₄ ถูกใช้ไปเกิด PbSO₄ และน้ำ",
     ("เพิ่มขึ้น เพราะ PbSO₄ ละลายกลับเป็น H₂SO₄", "ไม่เปลี่ยน เพราะ H₂SO₄ เป็นเพียงตัวเร่งปฏิกิริยา", "ลดลง เพราะ H₂SO₄ ระเหยออกไป")),
    ("ขณะประจุไฟแบตเตอรี่ตะกั่ว-กรด เกิดอะไรขึ้น", "PbSO₄ ที่ขั้วทั้งสองเปลี่ยนกลับเป็น Pb และ PbO₂ โดยใช้ไฟฟ้าจากภายนอก",
     ("Pb และ PbO₂ ที่ขั้วทั้งสองเปลี่ยนเป็น PbSO₄ โดยปล่อยไฟฟ้าออกมา", "น้ำกลั่นเปลี่ยนเป็น H₂SO₄ โดยไม่ใช้ไฟฟ้า", "แบตเตอรี่ทำหน้าที่เป็นเซลล์กัลวานิก จ่ายไฟฟ้าออกไปใช้ภายนอก")),
    ("ปฏิกิริยารวมขณะแบตเตอรี่ตะกั่ว-กรดจ่ายไฟคือข้อใด", "Pb + PbO₂ + 2H₂SO₄ → 2PbSO₄ + 2H₂O",
     ("2PbSO₄ + 2H₂O → Pb + PbO₂ + 2H₂SO₄", "Pb + 2H₂SO₄ → PbO₂ + 2H₂O", "PbSO₄ + H₂O → PbO₂ + H₂SO₄")),
    ("เหตุใดเซลล์ทุติยภูมิจึงประจุไฟใหม่ได้", "ปฏิกิริยาที่ขั้วผันกลับได้เมื่อให้ไฟฟ้าย้อนทิศ",
     ("สารในเซลล์ไม่ทำปฏิกิริยาเลยขณะจ่ายไฟฟ้า", "เซลล์ดูดพลังงานจากอากาศมาสร้างสารตั้งต้นใหม่", "อิเล็กโทรไลต์ระเหยกลับมาเอง")),
)


@question_type(
    "chem.battery_type_foundation",
    display_name={"th": "เซลล์ปฐมภูมิและเซลล์ทุติยภูมิ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_BATTERY,
)
class BatteryTypeFoundation(QuestionType):
    """Primary cells are used once; secondary cells recharge."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cell, kind, *_ = rng.choice(CELLS)
        if rng.random() < 0.5:
            other = SECONDARY if kind == PRIMARY else PRIMARY
            return _labelled(stem=f"{cell} จัดเป็นเซลล์ประเภทใด", correct=kind,
                             wrongs=(other, "เซลล์อิเล็กโทรไลต์", "เซลล์เชื้อเพลิง"), topic=TOPIC_BATTERY,
                             hint="เซลล์ปฐมภูมิปฏิกิริยาผันกลับไม่ได้ ใช้แล้วทิ้ง เซลล์ทุติยภูมิประจุไฟใหม่ได้")
        others = [c[0] for c in CELLS if c[1] != kind]
        return _labelled(stem=f"ข้อใดเป็น{kind.split(' ')[0]}", correct=cell, wrongs=tuple(others),
                         topic=TOPIC_BATTERY, hint="แบตเตอรี่ที่ชาร์จได้เป็นเซลล์ทุติยภูมิ ถ่านไฟฉายทั่วไปเป็นเซลล์ปฐมภูมิ")


@question_type(
    "chem.battery_type_fluency",
    display_name={"th": "ขั้วและอิเล็กโทรไลต์ของเซลล์ชนิดต่าง ๆ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_BATTERY,
)
class BatteryTypeFluency(QuestionType):
    """Name the anode, the cathode or the electrolyte of a named cell."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cell, _, anode, cathode, electrolyte = rng.choice(CELLS)
        part, index = rng.choice((("แอโนด (ขั้วลบ)", 2), ("แคโทด (ขั้วบวก)", 3), ("อิเล็กโทรไลต์", 4)))
        right = (anode, cathode, electrolyte)[index - 2]
        pool = sorted({c[i] for c in CELLS for i in (2, 3, 4)} - {right})
        near = [x for x in (anode, cathode, electrolyte) if x != right]
        return _labelled(stem=f"{cell} มีอะไรเป็น{part}", correct=right,
                         wrongs=(*near, rng.choice([p for p in pool if p not in near])), topic=TOPIC_BATTERY,
                         hint="แอโนดคือโลหะที่ถูกออกซิไดส์ แคโทดคือสารที่ถูกรีดิวซ์ อิเล็กโทรไลต์ให้ไอออนเคลื่อนที่")


@question_type(
    "chem.battery_type_application",
    display_name={"th": "การจ่ายไฟและการประจุไฟของแบตเตอรี่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_BATTERY,
)
class BatteryTypeApplication(QuestionType):
    """Discharging is galvanic; charging runs it backwards as an electrolytic cell."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, right, wrongs = rng.choice(LEAD_ACID)
            return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_BATTERY,
                             hint="จ่ายไฟ: Pb และ PbO₂ ใช้ H₂SO₄ ได้ PbSO₄ ประจุไฟ: ปฏิกิริยาย้อนกลับโดยใช้ไฟฟ้า")
        uses = (("รีโมตโทรทัศน์ที่ใช้ไฟน้อยนาน ๆ", PRIMARY), ("ไฟฉายที่ใช้เป็นครั้งคราว", PRIMARY),
                ("นาฬิกาข้อมือ", PRIMARY), ("โทรศัพท์มือถือ", SECONDARY), ("รถยนต์ไฟฟ้า", SECONDARY),
                ("สตาร์ตเครื่องยนต์รถยนต์", SECONDARY))
        use, kind = rng.choice(uses)
        cells = [c[0] for c in CELLS if c[1] == kind]
        others = [c[0] for c in CELLS if c[1] != kind]
        return _labelled(stem=f"{use} เหมาะจะใช้เซลล์ใดมากที่สุด", correct=rng.choice(cells),
                         wrongs=tuple(others), topic=TOPIC_BATTERY,
                         hint="อุปกรณ์ที่ใช้ไฟมากและต้องชาร์จบ่อยใช้เซลล์ทุติยภูมิ อุปกรณ์ใช้ไฟน้อยใช้เซลล์ปฐมภูมิได้คุ้ม")
