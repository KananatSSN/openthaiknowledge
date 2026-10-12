"""กล้องจุลทรรศน์ใช้แสง

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 1 ม.4/10

Sets moved here from: science_wave_f46.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f46 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_SCOPE = "กล้องจุลทรรศน์ใช้แสง"


PARTS = (
    ("เลนส์ใกล้ตา", "ขยายภาพจากเลนส์ใกล้วัตถุอีกครั้งก่อนเข้าตา"), ("เลนส์ใกล้วัตถุ", "ขยายภาพของวัตถุเป็นครั้งแรก"),
    ("ปุ่มปรับภาพหยาบ", "เลื่อนลำกล้องหรือแท่นวางวัตถุขึ้นลงมาก ใช้หาภาพที่กำลังขยายต่ำ"),
    ("ปุ่มปรับภาพละเอียด", "ปรับภาพให้ชัดเล็กน้อย ใช้กับกำลังขยายสูง"),
    ("ไดอะแฟรม", "ปรับปริมาณแสงที่ผ่านเข้าสู่วัตถุ"), ("เลนส์รวมแสง", "รวมแสงให้เข้มขึ้นก่อนผ่านวัตถุ"),
    ("แท่นวางวัตถุ", "วางสไลด์ตัวอย่าง"),
)


CARE = (
    ("การยกกล้องจุลทรรศน์ที่ถูกต้องคือข้อใด", "จับแขนกล้องด้วยมือหนึ่งและรองฐานด้วยอีกมือหนึ่ง",
     ("จับที่ลำกล้องมือเดียว", "จับที่เลนส์ใกล้ตา", "ยกที่แท่นวางวัตถุ")),
    ("ควรเริ่มหาภาพด้วยเลนส์ใกล้วัตถุกำลังขยายเท่าใด", "กำลังขยายต่ำสุดก่อน", ("กำลังขยายสูงสุดก่อน",
                                                                             "กำลังขยายใดก็ได้", "ไม่ต้องใช้เลนส์ใกล้วัตถุ")),
    ("ทำความสะอาดเลนส์ด้วยอะไร", "กระดาษเช็ดเลนส์", ("กระดาษทิชชูทั่วไป", "ผ้าเช็ดหน้า", "นิ้วมือ")),
    ("เมื่อใช้เลนส์ใกล้วัตถุกำลังขยายสูง ควรปรับภาพด้วยปุ่มใด", "ปุ่มปรับภาพละเอียดเท่านั้น",
     ("ปุ่มปรับภาพหยาบ", "ไดอะแฟรม", "ปุ่มหมุนเลนส์ใกล้ตา")),
    ("ภาพที่เห็นในกล้องจุลทรรศน์ใช้แสงเทียบกับวัตถุจริงเป็นอย่างไร", "ภาพเสมือนหัวกลับและกลับซ้ายขวา",
     ("ภาพจริงหัวตั้ง", "ภาพเสมือนหัวตั้งไม่กลับซ้ายขวา", "ภาพจริงขนาดเท่าวัตถุ")),
)


@question_type(
    "biology.microscope_foundation",
    display_name={"th": "ส่วนประกอบและการดูแลรักษากล้องจุลทรรศน์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_SCOPE,
)
class MicroscopeFoundation(QuestionType):
    """Each part's job, and the right way to handle the microscope."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            part, role = rng.choice(PARTS)
            others = [p for p in PARTS if p[0] != part]
            if rng.random() < 0.5:
                return _labelled(stem=f"{part}มีหน้าที่อะไร", correct=role, wrongs=tuple(p[1] for p in rng.sample(others, 3)),
                                 topic=TOPIC_SCOPE, hint="เลนส์ขยายภาพ ปุ่มปรับภาพทำให้ชัด ไดอะแฟรมและเลนส์รวมแสงคุมแสง")
            return _labelled(stem=f"ส่วนใดของกล้องทำหน้าที่{role}", correct=part, wrongs=tuple(p[0] for p in rng.sample(others, 3)),
                             topic=TOPIC_SCOPE, hint="เลนส์ขยายภาพ ปุ่มปรับภาพทำให้ชัด ไดอะแฟรมและเลนส์รวมแสงคุมแสง")
        stem, right, wrongs = rng.choice(CARE)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_SCOPE,
                         hint="เริ่มที่กำลังขยายต่ำ ใช้ปุ่มปรับละเอียดที่กำลังขยายสูง และถือกล้องด้วยสองมือ")


@question_type(
    "biology.microscope_fluency",
    display_name={"th": "กำลังขยายและขนาดจริงของวัตถุ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_SCOPE,
)
class MicroscopeFluency(QuestionType):
    """Total magnification = eyepiece × objective; real size = image size ÷ magnification."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eyepiece = rng.choice((5, 10, 15))
        objective = rng.choice((4, 10, 40, 100))
        total = eyepiece * objective
        if rng.random() < 0.5:
            return numeric(stem=f"ใช้เลนส์ใกล้ตากำลังขยาย {eyepiece}X กับเลนส์ใกล้วัตถุ {objective}X กำลังขยายรวมเท่าใด",
                           answer=total, wrongs=[eyepiece + objective, total * 10, objective], unit="เท่า", topic=TOPIC_SCOPE,
                           hint="กำลังขยายรวม = กำลังขยายเลนส์ใกล้ตา × กำลังขยายเลนส์ใกล้วัตถุ")
        real = rng.choice((2, 4, 5, 8, 10, 12, 20, 25, 40, 50))
        image_mm = Fraction(real * total, 1000)
        return numeric(stem=f"ส่องเซลล์ด้วยกำลังขยายรวม {total} เท่า (เลนส์ใกล้ตา {eyepiece}X เลนส์ใกล้วัตถุ {objective}X) "
                            f"วัดภาพได้ยาว {show(image_mm)} mm เซลล์จริงยาวกี่ไมโครเมตร (1 mm = 1000 μm)",
                       answer=real, wrongs=[real * 1000 if real * 1000 < 10 ** 6 else real * 10, image_mm * 1000, real * 10],
                       unit="μm", topic=TOPIC_SCOPE, hint="ขนาดจริง = ขนาดภาพ ÷ กำลังขยาย แล้วเปลี่ยน mm เป็น μm")


@question_type(
    "biology.microscope_application",
    display_name={"th": "ประมาณขนาดเซลล์จากเส้นผ่านศูนย์กลางของขอบเขตภาพ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_SCOPE,
)
class MicroscopeApplication(QuestionType):
    """Field diameter shrinks as magnification grows; cells across the field give each cell's size."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        low_mag = rng.choice((40, 50, 100))
        field_low = rng.choice((2, 4, 5))
        high_mag = low_mag * rng.choice((2, 4, 5, 10))
        field_high = Fraction(field_low * low_mag, high_mag)
        if rng.random() < 0.5:
            return numeric(stem=f"ที่กำลังขยาย {low_mag} เท่า ขอบเขตภาพมีเส้นผ่านศูนย์กลาง {field_low} mm ถ้าเปลี่ยนเป็นกำลังขยาย "
                                f"{high_mag} เท่า ขอบเขตภาพมีเส้นผ่านศูนย์กลางกี่ mm",
                           answer=field_high, wrongs=[Fraction(field_low * high_mag, low_mag), field_low, field_high * 2],
                           unit="mm", topic=TOPIC_SCOPE,
                           hint="เส้นผ่านศูนย์กลางขอบเขตภาพแปรผกผันกับกำลังขยาย: D₂ = D₁ × M₁ ÷ M₂")
        cells = rng.choice((4, 5, 8, 10, 20, 25))
        field_um = field_high * 1000
        size = field_um / cells
        return numeric(stem=f"ที่กำลังขยาย {high_mag} เท่า ขอบเขตภาพกว้าง {show(field_high)} mm เรียงเซลล์ได้เต็มแนวเส้นผ่านศูนย์กลาง "
                            f"{cells} เซลล์ เซลล์หนึ่งยาวประมาณกี่ไมโครเมตร",
                       answer=size, wrongs=[field_um * cells if field_um * cells < 10 ** 6 else size * 2, field_high / cells if (field_high / cells * 100).denominator == 1 else size + 1, size * 10],
                       unit="μm", topic=TOPIC_SCOPE, hint="ขนาดเซลล์ = เส้นผ่านศูนย์กลางขอบเขตภาพ (μm) ÷ จำนวนเซลล์ที่เรียงได้")
