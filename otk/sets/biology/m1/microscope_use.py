"""การใช้กล้องจุลทรรศน์ใช้แสง

ชีวะ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.1/2

Sets moved here from: science_wave_i1.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_i1 import BIOLOGY, LOWER_ONE, _others

PROVENANCE = Provenance("original")


TOPIC_CELL = "เซลล์และการดำรงชีวิต"


MICROSCOPE_PARTS = {
    "เลนส์ใกล้ตา": "ขยายภาพที่ได้จากเลนส์ใกล้วัตถุอีกครั้ง เป็นเลนส์ที่ตามองผ่าน",
    "เลนส์ใกล้วัตถุ": "ขยายภาพของวัตถุบนแท่นวางสไลด์เป็นครั้งแรก",
    "จานหมุน": "หมุนเพื่อเปลี่ยนเลนส์ใกล้วัตถุที่มีกำลังขยายต่างกัน",
    "ปุ่มปรับภาพหยาบ": "เลื่อนลำกล้องหรือแท่นวางสไลด์ขึ้นลงมาก ๆ เพื่อหาภาพครั้งแรก",
    "ปุ่มปรับภาพละเอียด": "เลื่อนขึ้นลงทีละน้อยเพื่อปรับภาพให้คมชัด",
    "ที่หนีบสไลด์": "ยึดสไลด์ไว้บนแท่นวางสไลด์ไม่ให้เลื่อน",
    "ไดอะแฟรม": "ปรับปริมาณแสงที่ผ่านไปยังวัตถุ",
    "เลนส์รวมแสง": "รวมแสงให้เข้มขึ้นก่อนส่องผ่านวัตถุ",
    "แขน": "ส่วนที่ใช้จับเมื่อยกกล้อง โดยใช้อีกมือรองที่ฐาน",
}


# (situation, the right step, wrong steps)
MICROSCOPE_STEPS = (
    ("เมื่อเริ่มส่องสไลด์ ควรใช้เลนส์ใกล้วัตถุแบบใดก่อน",
     "เลนส์ใกล้วัตถุที่มีกำลังขยายต่ำสุด",
     ("เลนส์ใกล้วัตถุที่มีกำลังขยายสูงสุด", "เลนส์ใดก็ได้ เพราะภาพเหมือนกัน",
      "ไม่ต้องใช้เลนส์ใกล้วัตถุ ใช้เลนส์ใกล้ตาอย่างเดียว")),
    ("เมื่อเปลี่ยนจากเลนส์ใกล้วัตถุกำลังขยายต่ำเป็นกำลังขยายสูงแล้ว ควรปรับภาพด้วยปุ่มใด",
     "ปุ่มปรับภาพละเอียดเท่านั้น",
     ("ปุ่มปรับภาพหยาบเท่านั้น", "ปุ่มปรับภาพหยาบก่อน แล้วจึงปรับละเอียด", "ไม่ต้องปรับภาพอีก")),
    ("ขั้นตอนใดเรียงลำดับการหาภาพได้ถูกต้อง",
     "วางสไลด์และหนีบ → ใช้เลนส์กำลังขยายต่ำ → ปรับภาพหยาบ → ปรับภาพละเอียด",
     ("วางสไลด์และหนีบ → ใช้เลนส์กำลังขยายสูง → ปรับภาพหยาบ → ปรับภาพละเอียด",
      "ใช้เลนส์กำลังขยายต่ำ → ปรับภาพละเอียด → ปรับภาพหยาบ → วางสไลด์",
      "ปรับภาพหยาบ → วางสไลด์ → ใช้เลนส์กำลังขยายสูง → ปรับภาพละเอียด")),
    ("ขณะลดลำกล้องด้วยปุ่มปรับภาพหยาบ ควรทำอย่างไรเพื่อไม่ให้เลนส์กระแทกสไลด์",
     "มองด้านข้างกล้องจนเลนส์ใกล้วัตถุอยู่ใกล้สไลด์ แล้วจึงมองผ่านเลนส์ใกล้ตาและหมุนให้ห่างออก",
     ("มองผ่านเลนส์ใกล้ตาและหมุนลงจนกว่าจะเห็นภาพ", "ใช้เลนส์กำลังขยายสูงสุดก่อนเสมอ",
      "เปิดไดอะแฟรมให้กว้างที่สุดก่อนหมุน")),
)


EYEPIECES = (5, 10, 15)


OBJECTIVES = (4, 10, 40, 100)


# The image is upside down and reversed left to right, so it moves opposite to
# the slide: to bring something into the centre, move the slide toward the side
# where the image of it appears.
DIRECTIONS = {"ซ้าย": "ขวา", "ขวา": "ซ้าย", "ด้านบน": "ด้านล่าง", "ด้านล่าง": "ด้านบน"}


MAGNIFY_EFFECTS = (
    "ภาพใหญ่ขึ้น เห็นเซลล์น้อยลง และภาพมืดลง",
    ("ภาพเล็กลง เห็นเซลล์มากขึ้น และภาพสว่างขึ้น", "ภาพใหญ่ขึ้น เห็นเซลล์มากขึ้น และภาพสว่างขึ้น",
     "ภาพขนาดเท่าเดิม แต่คมชัดขึ้นเท่านั้น"),
)


@question_type(
    "cell.microscope_use_foundation",
    display_name={"th": "ส่วนประกอบและหน้าที่ของกล้องจุลทรรศน์ใช้แสง"},
    level=LOWER_ONE, subject=BIOLOGY, topic=TOPIC_CELL,
)
class MicroscopeUseFoundation(QuestionType):
    """Name a part's job, or the part that does a job."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        part = rng.choice(sorted(MICROSCOPE_PARTS))
        hint = "นึกถึงทางเดินของแสง: แหล่งแสง → เลนส์รวมแสง → วัตถุ → เลนส์ใกล้วัตถุ → เลนส์ใกล้ตา"
        if rng.random() < 0.5:
            return _labelled(stem=f"{part}ของกล้องจุลทรรศน์ใช้แสงมีหน้าที่อย่างไร",
                             correct=MICROSCOPE_PARTS[part], wrongs=_others(MICROSCOPE_PARTS, part),
                             topic=TOPIC_CELL, hint=hint)
        return _labelled(stem=f"ส่วนใดของกล้องจุลทรรศน์ใช้แสงทำหน้าที่{MICROSCOPE_PARTS[part]}",
                         correct=part, wrongs=tuple(p for p in MICROSCOPE_PARTS if p != part),
                         topic=TOPIC_CELL, hint=hint)


@question_type(
    "cell.microscope_use_fluency",
    display_name={"th": "กำลังขยายของกล้องจุลทรรศน์และขั้นตอนการใช้"},
    level=LOWER_ONE, subject=BIOLOGY, topic=TOPIC_CELL,
)
class MicroscopeUseFluency(QuestionType):
    """Total magnification is the product of the two lenses; and the steps in order."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "กำลังขยายทั้งหมด = กำลังขยายของเลนส์ใกล้ตา × กำลังขยายของเลนส์ใกล้วัตถุ"
        kind = rng.randrange(3)
        eye, obj = rng.choice(EYEPIECES), rng.choice(OBJECTIVES)
        if kind == 0:
            return numeric(stem=f"ใช้เลนส์ใกล้ตากำลังขยาย {eye} เท่า และเลนส์ใกล้วัตถุกำลังขยาย {obj} เท่า "
                                "ภาพที่เห็นมีกำลังขยายทั้งหมดกี่เท่า",
                           answer=eye * obj, wrongs=[eye + obj, obj, eye * obj * 10], unit="เท่า",
                           topic=TOPIC_CELL, hint=hint)
        if kind == 1:
            return numeric(stem=f"ต้องการให้ภาพมีกำลังขยายทั้งหมด {eye * obj} เท่า โดยใช้เลนส์ใกล้ตากำลังขยาย "
                                f"{eye} เท่า ต้องใช้เลนส์ใกล้วัตถุกำลังขยายกี่เท่า",
                           answer=obj, wrongs=[eye * obj - eye, eye * obj, obj * 10], unit="เท่า",
                           topic=TOPIC_CELL, hint=hint)
        stem, right, wrongs = rng.choice(MICROSCOPE_STEPS)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_CELL,
                         hint="เริ่มที่กำลังขยายต่ำและปรับหยาบ แล้วจึงปรับละเอียด เมื่อใช้กำลังขยายสูงปรับละเอียดเท่านั้น")


@question_type(
    "cell.microscope_use_application",
    display_name={"th": "ทิศทางของภาพและผลของการเพิ่มกำลังขยาย"},
    level=LOWER_ONE, subject=BIOLOGY, topic=TOPIC_CELL,
)
class MicroscopeUseApplication(QuestionType):
    """Where to move the slide, and what a higher power does to the view."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(4)
        if kind == 0:
            seen = rng.choice(sorted(DIRECTIONS))
            return _labelled(stem=f"ส่องกล้องจุลทรรศน์แล้วเห็นเซลล์ที่ต้องการอยู่ทาง{seen}ของภาพ "
                                  "ถ้าต้องการให้เซลล์นั้นมาอยู่กลางภาพ ต้องเลื่อนสไลด์ไปทางใด",
                             correct=f"ไปทาง{seen}", wrongs=tuple(f"ไปทาง{d}" for d in DIRECTIONS if d != seen),
                             topic=TOPIC_CELL,
                             hint="ภาพกลับหัวและกลับซ้ายขวา ภาพจึงเคลื่อนสวนทางกับสไลด์: เลื่อนสไลด์ไปทางเดียวกับที่เห็นภาพ")
        if kind == 1:
            moved = rng.choice(sorted(DIRECTIONS))
            return _labelled(stem=f"ขณะส่องกล้องจุลทรรศน์ ถ้าเลื่อนสไลด์ไปทาง{moved} ภาพที่เห็นจะเคลื่อนไปทางใด",
                             correct=f"ไปทาง{DIRECTIONS[moved]}",
                             wrongs=tuple(f"ไปทาง{d}" for d in DIRECTIONS if d != DIRECTIONS[moved]),
                             topic=TOPIC_CELL, hint="ภาพจากกล้องจุลทรรศน์ใช้แสงกลับหัวและกลับซ้ายขวา จึงเคลื่อนสวนทางกับสไลด์")
        if kind == 2:
            right, wrongs = MAGNIFY_EFFECTS
            low, high = rng.choice(((4, 10), (10, 40), (4, 40)))
            return _labelled(stem=f"เมื่อเปลี่ยนเลนส์ใกล้วัตถุจาก {low} เท่า เป็น {high} เท่า โดยไม่ปรับแสง "
                                  "ภาพที่เห็นจะเปลี่ยนไปอย่างไร",
                             correct=right, wrongs=wrongs, topic=TOPIC_CELL,
                             hint="กำลังขยายสูงขึ้น ขอบเขตภาพแคบลง แสงที่เข้าตาจึงน้อยลง")
        # Cells counted across the field shrink with the magnification; cells
        # filling it shrink with its square.
        factor = rng.choice((2, 4))
        low = rng.choice((40, 100))
        if rng.random() < 0.5:
            across = factor * rng.randrange(2, 9)
            return numeric(stem=f"ที่กำลังขยาย {low} เท่า เห็นเซลล์เรียงเป็นแถวตามเส้นผ่านศูนย์กลางของภาพ {across} เซลล์ "
                                f"ถ้าเปลี่ยนเป็นกำลังขยาย {low * factor} เท่า จะเห็นเซลล์ในแถวนั้นกี่เซลล์",
                           answer=Fraction(across, factor), wrongs=[across * factor, Fraction(across, factor * factor)
                                                                    if across % (factor * factor) == 0 else across - factor],
                           unit="เซลล์", topic=TOPIC_CELL,
                           hint="กำลังขยายเพิ่ม n เท่า เส้นผ่านศูนย์กลางของขอบเขตภาพลดลง n เท่า")
        filled = factor * factor * rng.randrange(1, 9)
        return numeric(stem=f"ที่กำลังขยาย {low} เท่า เห็นเซลล์เต็มขอบเขตภาพ {filled} เซลล์ "
                            f"ถ้าเปลี่ยนเป็นกำลังขยาย {low * factor} เท่า จะเห็นเซลล์ประมาณกี่เซลล์",
                       answer=Fraction(filled, factor * factor), wrongs=[Fraction(filled, factor), filled * factor],
                       unit="เซลล์", topic=TOPIC_CELL,
                       hint="กำลังขยายเพิ่ม n เท่า พื้นที่ของขอบเขตภาพลดลง n² เท่า")
