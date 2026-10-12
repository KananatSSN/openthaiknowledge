"""สภาพยืดหยุ่น ความเค้น ความเครียด และมอดุลัสของยัง

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/2

Sets moved here from: science_wave_f15.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f15 import SUBJECT, UPPER_SIX, _exact

PROVENANCE = Provenance("original")


TOPIC_ELASTIC = "สภาพยืดหยุ่น ความเค้น ความเครียด และมอดุลัสของยัง"


ELASTIC_FACTS = (
    ("ในช่วงที่แรงดึงไม่เกินขีดจำกัดการแปรผันตรง ความยาวที่เพิ่มขึ้นของแท่งวัสดุเป็นอย่างไร", "แปรผันตรงกับแรงดึง",
     ("แปรผกผันกับแรงดึง", "คงตัวไม่ว่าแรงเท่าใด", "เพิ่มแบบก้าวกระโดด")),
    ("ถ้าดึงแท่งวัสดุเกินขีดจำกัดสภาพยืดหยุ่นแล้วปล่อย จะเกิดอะไรขึ้น", "แท่งวัสดุไม่กลับสู่ความยาวเดิม",
     ("แท่งวัสดุกลับสู่ความยาวเดิมทันที", "แท่งวัสดุหดสั้นกว่าเดิม", "มอดุลัสของยังเพิ่มขึ้น")),
    ("มอดุลัสของยังขึ้นกับอะไร", "ชนิดของวัสดุ",
     ("ความยาวของแท่งวัสดุ", "แรงที่ใช้ดึง", "พื้นที่หน้าตัดของแท่งวัสดุ")),
    ("ความเค้นตามยาวคืออะไร", "แรงดึงต่อพื้นที่หน้าตัดของแท่งวัสดุ",
     ("ความยาวที่เปลี่ยนไปต่อความยาวเดิม", "แรงดึงคูณความยาว", "พื้นที่หน้าตัดต่อแรงดึง")),
    ("ความเครียดตามยาวมีหน่วยเป็นอะไร", "ไม่มีหน่วย เพราะเป็นอัตราส่วนของความยาว",
     ("นิวตันต่อตารางเมตร", "นิวตัน", "เมตร")),
    ("การออกแบบสายเคเบิลลิฟต์ให้ปลอดภัย ต้องเลือกให้ความเค้นที่ใช้งานเป็นอย่างไร", "ต่ำกว่าขีดจำกัดสภาพยืดหยุ่นมาก",
     ("เท่ากับความเค้นที่จุดแตกหัก", "สูงกว่าขีดจำกัดสภาพยืดหยุ่นเล็กน้อย", "ไม่ต้องคำนึงถึงความเค้น")),
)


@question_type(
    "phys.elasticity_modulus_foundation",
    display_name={"th": "สภาพยืดหยุ่นและความเค้นตามยาว"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ELASTIC,
)
class ElasticityModulusFoundation(QuestionType):
    """How a rod stretches, and stress = F/A."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            stem, correct, wrongs = rng.choice(ELASTIC_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_ELASTIC,
                             hint="ในช่วงสภาพยืดหยุ่น ความเค้นแปรผันตรงกับความเครียด อัตราส่วนคือมอดุลัสของยัง")
        area = rng.choice((1, 2, 4, 5, 8, 10, 20, 25, 50))
        force = area * rng.randint(1, 40) * 10
        return numeric(
            stem=f"แขวนน้ำหนัก {force:,} N ที่ปลายลวดพื้นที่หน้าตัด {area} mm² ความเค้นตามยาวในลวดกี่เมกะพาสคัล",
            answer=Fraction(force, area), wrongs=[force * area, Fraction(area, force) * 1000, Fraction(force, area) * 10],
            unit="MPa", topic=TOPIC_ELASTIC, hint="ความเค้น = F/A และ 1 N/mm² = 10⁶ Pa = 1 MPa")


@question_type(
    "phys.elasticity_modulus_fluency",
    display_name={"th": "คำนวณความเครียดตามยาวและมอดุลัสของยัง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ELASTIC,
)
class ElasticityModulusFluency(QuestionType):
    """Strain = ΔL/L, and Y = stress/strain."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        length = rng.choice((1, 2, Fraction(5, 2), 4, 5))
        stretch = Fraction(rng.randint(1, 20), 10)
        strain = stretch / length
        if rng.random() < 0.5 and _exact(strain):
            return numeric(
                stem=f"ลวดยาว {show(length)} m ยืดออก {show(stretch)} mm ความเครียดตามยาวเท่าใด (ตอบในหน่วย × 10⁻³)",
                answer=strain, wrongs=[strain * 1000, Fraction(length) / stretch, strain * 10], unit="× 10⁻³",
                topic=TOPIC_ELASTIC, hint="ความเครียด = ΔL/L ใช้หน่วยเดียวกัน (1 mm ÷ 1 m = 10⁻³)")
        stress, strain = rng.choice([(s, e) for s in (50, 100, 150, 200, 250, 300, 400) for e in (Fraction(1, 2), 1, 2, Fraction(5, 2), 4, 5)
                                     if _exact(Fraction(s) / e)])
        return numeric(
            stem=f"ลวดโลหะมีความเค้น {stress} MPa และความเครียด {show(strain)} × 10⁻³ มอดุลัสของยังของลวดกี่จิกะพาสคัล",
            answer=Fraction(stress) / strain, wrongs=[stress * strain, Fraction(stress) / strain * 1000, Fraction(strain) / stress * 1000],
            unit="GPa", topic=TOPIC_ELASTIC, hint="Y = ความเค้น/ความเครียด: MPa ÷ 10⁻³ = GPa")


@question_type(
    "phys.elasticity_modulus_application",
    display_name={"th": "ใช้มอดุลัสของยังหาความยาวที่ยืดของลวดและเส้นเคเบิล"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ELASTIC,
)
class ElasticityModulusApplication(QuestionType):
    """ΔL = FL/(AY), and Y from a whole loading experiment."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        metal, y = rng.choice((("เหล็กกล้า", 200), ("ทองแดง", 100), ("อะลูมิเนียม", 70), ("ทองเหลือง", 100)))
        force, area, length = rng.choice([(f, a, ell) for f in range(100, 5001, 100) for a in (1, 2, 4, 5, 10) for ell in (1, 2, 3, 4, 5)
                                          if _exact(Fraction(f * ell, a * y))])
        stretch = Fraction(force * length, area * y)  # mm, since N/mm² ÷ GPa × m gives mm
        if rng.random() < 0.5:
            return numeric(
                stem=(f"ลวด{metal}ยาว {length} m พื้นที่หน้าตัด {area} mm² รับแรงดึง {force:,} N ลวดยืดออกกี่มิลลิเมตร "
                      f"(มอดุลัสของยังของ{metal} = {y} GPa)"),
                answer=stretch, wrongs=[stretch * 1000, Fraction(force, area * y), stretch * 2], unit="mm",
                topic=TOPIC_ELASTIC, hint="ΔL = FL/(AY) ระวังหน่วย: N/mm² = MPa, GPa = 1,000 MPa")
        return numeric(
            stem=(f"ดึงลวดยาว {length} m พื้นที่หน้าตัด {area} mm² ด้วยแรง {force:,} N ลวดยืดออก {show(stretch)} mm "
                  "มอดุลัสของยังของลวดกี่จิกะพาสคัล"),
            answer=y, wrongs=[y * 1000, Fraction(y, 10), y * 2], unit="GPa", topic=TOPIC_ELASTIC,
            hint="หาความเค้น F/A และความเครียด ΔL/L แล้ว Y = ความเค้น/ความเครียด")
