"""ยีน การสังเคราะห์โปรตีน และลักษณะทางพันธุกรรม

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.3 ม.4/1

Sets moved here from: science_wave_b29.
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
from otk.sets._support.science_wave_b19 import UPPER_FOUR, Fact, _fact_question
from otk.sets._support.science_wave_b29 import PROTEIN_SCENARIOS

PROVENANCE = Provenance("original")


PROTEIN_TOPIC = "ยีนกับการสังเคราะห์โปรตีน"


PROTEIN_FACTS = (
    Fact("ยีนควบคุมลักษณะทางพันธุกรรมได้อย่างไร",
         "ยีนเก็บลำดับนิวคลีโอไทด์ที่กำหนดลำดับกรดแอมิโนของโปรตีน "
         "โปรตีนที่ได้ทำหน้าที่ของมันแล้วจึงปรากฏออกมาเป็นลักษณะที่สังเกตได้"),
    Fact("การถอดรหัสคือขั้นตอนใด",
         "การสร้างสาย mRNA ขึ้นโดยใช้สายดีเอ็นเอสายหนึ่งของยีนเป็นแม่แบบ"),
    Fact("การแปลรหัสคือขั้นตอนใด",
         "การที่ไรโบโซมอ่านรหัสทีละสามเบสบน mRNA "
         "แล้วนำกรดแอมิโนที่ tRNA พามาต่อกันเป็นสายพอลิเพปไทด์"),
    Fact("โคดอนคืออะไร",
         "ลำดับนิวคลีโอไทด์สามตัวบน mRNA ที่กำหนดกรดแอมิโนหนึ่งตัว "
         "หรือกำหนดให้หยุดการสร้างสายพอลิเพปไทด์"),
    Fact("tRNA ทำหน้าที่ใดในการสังเคราะห์โปรตีน",
         "นำกรดแอมิโนที่ตรงกับโคดอนมาส่งที่ไรโบโซม "
         "โดยใช้แอนติโคดอนของตนจับคู่กับโคดอนบน mRNA"),
    Fact("เหตุใดลำดับของกรดแอมิโนจึงสำคัญต่อหน้าที่ของโปรตีน",
         "เพราะลำดับกรดแอมิโนกำหนดการพับตัวเป็นรูปร่างสามมิติ "
         "และรูปร่างนั้นเองที่กำหนดว่าโปรตีนจะทำหน้าที่ใดได้"),
    Fact("เหตุใดเซลล์ต่างชนิดในร่างกายเดียวกันจึงทำหน้าที่ต่างกัน "
         "ทั้งที่มียีนชุดเดียวกัน",
         "เพราะเซลล์แต่ละชนิดแสดงออกของยีนไม่เหมือนกัน "
         "จึงสร้างโปรตีนคนละชุดและทำหน้าที่ต่างกัน"),
)


class Chain(NamedTuple):
    """One gene, the protein it specifies, and the trait that results."""
    gene: str
    protein: str
    trait: str


CHAINS = (
    Chain("ยีนที่ควบคุมการสร้างเม็ดสีเมลานิน",
          "เอนไซม์ที่ใช้ในการสร้างเม็ดสีเมลานิน",
          "สีของผิวหนัง เส้นผม และม่านตา"),
    Chain("ยีนที่ควบคุมการสร้างฮีโมโกลบิน",
          "สายโปรตีนโกลบินที่ประกอบขึ้นเป็นฮีโมโกลบิน",
          "ความสามารถของเม็ดเลือดแดงในการลำเลียงแก๊สออกซิเจน"),
    Chain("ยีนที่ควบคุมการสร้างสารรับแสงในจอตา",
          "โปรตีนรับแสงในเซลล์รูปกรวยของจอตา",
          "ความสามารถในการแยกสีที่มองเห็น"),
    Chain("ยีนที่ควบคุมการสร้างปัจจัยการแข็งตัวของเลือด",
          "โปรตีนที่ทำให้เลือดแข็งตัวเมื่อมีบาดแผล",
          "ระยะเวลาที่เลือดหยุดไหลหลังได้รับบาดเจ็บ"),
    Chain("ยีนที่ควบคุมการสร้างเอนไซม์ย่อยน้ำตาลแล็กโทส",
          "เอนไซม์ที่ผนังลำไส้เล็กซึ่งย่อยน้ำตาลในนม",
          "ความสามารถในการดื่มนมโดยไม่เกิดอาการท้องอืด"),
    Chain("ยีนที่ควบคุมการสร้างเคราตินของเส้นผม",
          "โปรตีนเคราตินที่เรียงตัวอยู่ในเส้นผม",
          "ลักษณะของเส้นผมว่าตรงหรือหยิก"),
)


CHAINS += (
    Chain('ยีนที่ควบคุมการสร้างอินซูลิน',
        'ฮอร์โมนอินซูลินที่สร้างจากตับอ่อน',
        'การควบคุมระดับน้ำตาลกลูโคสในเลือด'),
    Chain('ยีนที่ควบคุมการสร้างคอลลาเจน',
        'โปรตีนคอลลาเจนในผิวหนังและเส้นเอ็น',
        'ความยืดหยุ่นและความแข็งแรงของผิวหนังและข้อต่อ'),
    Chain('ยีนที่ควบคุมการสร้างแอนติเจนบนผิวเม็ดเลือดแดง',
        'เอนไซม์ที่เติมน้ำตาลบางชนิดลงบนผิวเซลล์เม็ดเลือดแดง',
        'หมู่เลือดในระบบ ABO'),
)


@question_type(
    "cell.protein_synthesis_foundation",
    display_name={"th": "ยีนกับการสังเคราะห์โปรตีน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=PROTEIN_TOPIC,
)
class ProteinSynthesisFoundation(QuestionType):
    """The steps from a gene to a working protein."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, PROTEIN_FACTS, topic=PROTEIN_TOPIC,
            hint="เรียงลำดับให้ได้ก่อนว่า ดีเอ็นเอ ถูกถอดรหัสเป็น mRNA "
                 "แล้วจึงถูกแปลรหัสเป็นสายกรดแอมิโน",
        )


@question_type(
    "cell.protein_synthesis_fluency",
    display_name={"th": "จากยีนสู่โปรตีนสู่ลักษณะ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=PROTEIN_TOPIC,
)
class ProteinSynthesisFluency(QuestionType):
    """Carry the whole chain — a protein alone does not answer this indicator."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(CHAINS)
        others = [f"กำหนดให้สร้าง{other.protein} ซึ่งทำให้เกิด{other.trait}"
                  for other in CHAINS if other.gene != item.gene]
        rng.shuffle(others)
        return _labelled(
            stem=f"“{item.gene}” ทำให้เกิดลักษณะทางพันธุกรรมได้อย่างไร",
            correct=f"กำหนดให้สร้าง{item.protein} ซึ่งทำให้เกิด{item.trait}",
            wrongs=tuple(others[:3]),
            hint="ตัวเลือกที่ถูกต้องต้องถูกทั้งโปรตีนที่สร้างขึ้น "
                 "และลักษณะที่ปรากฏออกมาจากโปรตีนนั้น",
            topic=PROTEIN_TOPIC,
        )


@question_type(
    "cell.protein_synthesis_application",
    display_name={"th": "วิเคราะห์ความสัมพันธ์ของยีน โปรตีน และลักษณะ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=PROTEIN_TOPIC,
)
class ProteinSynthesisApplication(QuestionType):
    """Trace a trait back through its protein to the gene behind it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, PROTEIN_SCENARIOS,
            hint="เดินตามลูกโซ่ให้ครบสามขั้นเสมอ คือยีน โปรตีน แล้วจึงลักษณะ",
        ), PROTEIN_TOPIC)
