"""เทคโนโลยีที่เกี่ยวข้องกับเซลล์เคมีไฟฟ้า

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/32

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


TOPIC_TECH = "เทคโนโลยีที่เกี่ยวข้องกับเซลล์เคมีไฟฟ้า"


TECH = (
    ("เซลล์เชื้อเพลิงไฮโดรเจน", "ใช้ H₂ และ O₂ ผลิตไฟฟ้าต่อเนื่องตราบที่ป้อนเชื้อเพลิง ได้น้ำเป็นผลิตภัณฑ์",
     "รถยนต์และรถบัสเซลล์เชื้อเพลิง"),
    ("แบตเตอรี่ลิเทียมไอออน", "ลิเทียมไอออนเคลื่อนระหว่างขั้วเมื่อชาร์จและจ่ายไฟ น้ำหนักเบา เก็บพลังงานได้มาก",
     "โทรศัพท์มือถือและรถยนต์ไฟฟ้า"),
    ("แบตเตอรี่สังกะสี-อากาศ", "ใช้ออกซิเจนจากอากาศเป็นสารที่ถูกรีดิวซ์ ให้พลังงานสูงในขนาดเล็ก", "เครื่องช่วยฟัง"),
    ("แบตเตอรี่รีดอกซ์โฟลว์", "เก็บพลังงานในสารละลายที่สูบผ่านเซลล์ ขยายความจุได้ด้วยถังที่ใหญ่ขึ้น",
     "กักเก็บพลังงานจากโซลาร์ฟาร์มและกังหันลม"),
    ("แบตเตอรี่โซเดียมไอออน", "ใช้โซเดียมซึ่งหาง่ายและราคาถูกกว่าลิเทียม", "ระบบกักเก็บพลังงานขนาดใหญ่ราคาประหยัด"),
    ("เซลล์ลิเทียมแบบกระดุม", "ขนาดเล็ก ศักย์สูง ใช้ได้นานโดยไม่ต้องชาร์จ", "เครื่องกระตุ้นหัวใจและเมนบอร์ดคอมพิวเตอร์"),
)


@question_type(
    "chem.cell_technology_foundation",
    display_name={"th": "เซลล์เคมีไฟฟ้าในเทคโนโลยีสมัยใหม่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_TECH,
)
class CellTechnologyFoundation(QuestionType):
    """Match a technology to how it works."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, how, _ = rng.choice(TECH)
        others = [t for t in TECH if t[0] != name]
        if rng.random() < 0.5:
            return _labelled(stem=f"{name} มีหลักการหรือจุดเด่นตามข้อใด", correct=how,
                             wrongs=tuple(t[1] for t in rng.sample(others, 3)), topic=TOPIC_TECH,
                             hint="นึกถึงสารที่ใช้ในเซลล์และสิ่งที่ทำให้เซลล์นั้นต่างจากเซลล์อื่น")
        return _labelled(stem=f"\"{how}\" เป็นจุดเด่นของเทคโนโลยีใด", correct=name,
                         wrongs=tuple(t[0] for t in rng.sample(others, 3)), topic=TOPIC_TECH,
                         hint="นึกถึงสารที่ใช้ในเซลล์และสิ่งที่ทำให้เซลล์นั้นต่างจากเซลล์อื่น")


@question_type(
    "chem.cell_technology_fluency",
    display_name={"th": "เลือกเทคโนโลยีเซลล์ให้เหมาะกับการใช้งาน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_TECH,
)
class CellTechnologyFluency(QuestionType):
    """The job points to the cell."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, _, use = rng.choice(TECH)
        others = [t[0] for t in TECH if t[0] != name]
        return _labelled(stem=f"{use} นิยมใช้เทคโนโลยีเซลล์ใด", correct=name, wrongs=tuple(others),
                         topic=TOPIC_TECH, hint="ดูว่างานต้องการน้ำหนักเบา ขนาดเล็ก ความจุมาก หรือเชื้อเพลิงต่อเนื่อง")


@question_type(
    "chem.cell_technology_application",
    display_name={"th": "ปฏิกิริยาและผลกระทบของเซลล์เชื้อเพลิงและแบตเตอรี่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_TECH,
)
class CellTechnologyApplication(QuestionType):
    """Fuel-cell half-reactions, and the trade-offs of new cells."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        facts = (
            ("ปฏิกิริยาที่แอโนดของเซลล์เชื้อเพลิงไฮโดรเจน (อิเล็กโทรไลต์เป็นกรด) คือข้อใด", "H₂ → 2H⁺ + 2e⁻",
             ("O₂ + 4H⁺ + 4e⁻ → 2H₂O", "2H₂O → O₂ + 4H⁺ + 4e⁻", "2H⁺ + 2e⁻ → H₂")),
            ("ปฏิกิริยาที่แคโทดของเซลล์เชื้อเพลิงไฮโดรเจน (อิเล็กโทรไลต์เป็นกรด) คือข้อใด", "O₂ + 4H⁺ + 4e⁻ → 2H₂O",
             ("H₂ → 2H⁺ + 2e⁻", "2H₂O → O₂ + 4H⁺ + 4e⁻", "O₂ + 2H₂ → 2H₂O + 4e⁻")),
            ("ปฏิกิริยารวมของเซลล์เชื้อเพลิงไฮโดรเจนคือข้อใด", "2H₂ + O₂ → 2H₂O",
             ("2H₂O → 2H₂ + O₂", "H₂ + O₂ → H₂O₂", "CH₄ + 2O₂ → CO₂ + 2H₂O")),
            ("ข้อใดเป็นข้อดีของเซลล์เชื้อเพลิงไฮโดรเจนเมื่อเทียบกับเครื่องยนต์เผาไหม้", "ไม่ปล่อย CO₂ ขณะใช้งาน ได้เพียงน้ำ",
             ("ไม่ต้องใช้เชื้อเพลิงใด ๆ ขณะใช้งาน", "ได้แก๊ส CO₂ ที่นำไปใช้ต่อได้", "ไม่มีปฏิกิริยาเคมีเกิดขึ้นในเซลล์")),
            ("ข้อใดเป็นข้อควรระวังในการใช้แบตเตอรี่ลิเทียมไอออน", "ถ้าร้อนเกินหรือเสียหายอาจลุกไหม้ ควรใช้ที่ชาร์จที่ถูกต้อง",
             ("ห้ามชาร์จซ้ำ เพราะเป็นเซลล์ปฐมภูมิที่ใช้ได้เพียงครั้งเดียว", "ต้องเติมน้ำกลั่นเป็นประจำ เพื่อไม่ให้อิเล็กโทรไลต์แห้ง", "ต้องเติมกรดกำมะถันเมื่อไฟอ่อน")),
            ("เหตุใดจึงต้องแยกทิ้งแบตเตอรี่ใช้แล้ว ไม่ทิ้งรวมกับขยะทั่วไป", "มีโลหะหนักและสารเคมีที่เป็นพิษ และนำโลหะกลับมาใช้ใหม่ได้",
             ("เพราะแบตเตอรี่ย่อยสลายได้เร็วจนปนกับขยะอื่นไม่ได้", "เพราะแบตเตอรี่ใช้แล้วไม่มีสารเคมีเหลือ จึงรีไซเคิลได้ง่าย", "เพราะแบตเตอรี่ทุกชนิดประจุไฟใหม่ได้")),
        )
        stem, right, wrongs = rng.choice(facts)
        wrongs = tuple(wrongs)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_TECH,
                         hint="เซลล์เชื้อเพลิง: H₂ ถูกออกซิไดส์ที่แอโนด O₂ ถูกรีดิวซ์ที่แคโทด ได้น้ำ")
