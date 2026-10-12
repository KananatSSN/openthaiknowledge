"""ทัศนอุปกรณ์และการมองเห็น

ฟิสิกส์ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.3/17, ว 2.3 ม.3/18

Sets moved here from: physics, science_wave_a4.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.physics import SUBJECT, TOPIC
from otk.sets._support.science_wave_a4 import (
    IMAGE_REAL_LARGER,
    IMAGE_REAL_SMALLER,
    IMAGE_VIRTUAL_LARGER,
    IMAGE_VIRTUAL_SMALLER,
    PHYSICS,
    WAVES,
    _distinct,
    _image_wrongs,
    _question,
)

PROVENANCE = Provenance("original")


# (ทัศนอุปกรณ์, ชิ้นส่วนหลัก, ลักษณะภาพที่ใช้งาน)
DEVICE_FACTS = (
    ("แว่นขยาย", "เลนส์นูน", IMAGE_VIRTUAL_LARGER),
    ("กล้องถ่ายรูป", "เลนส์นูน", IMAGE_REAL_SMALLER),
    ("เครื่องฉายภาพนิ่ง", "เลนส์นูน", IMAGE_REAL_LARGER),
    ("กระจกมองหลังรถยนต์", "กระจกนูน", IMAGE_VIRTUAL_SMALLER),
    ("กระจกส่องฟันของทันตแพทย์", "กระจกเว้า", IMAGE_VIRTUAL_LARGER),
    ("กล้องโทรทรรศน์ชนิดสะท้อนแสง", "กระจกเว้า", IMAGE_REAL_SMALLER),
)


OPTICAL_ELEMENTS = ("เลนส์นูน", "เลนส์เว้า", "กระจกนูน", "กระจกเว้า")


# (ปรากฏการณ์, สมบัติของแสงที่เป็นสาเหตุหลัก)
LIGHT_PHENOMENA = (
    ("การเกิดรุ้งกินน้ำหลังฝนตก",
     "การหักเหและการกระจายของแสงขาวในหยดน้ำ"),
    ("การมองเห็นเหมือนมีน้ำอยู่บนถนนในวันที่แดดจัด",
     "การหักเหของแสงในอากาศที่มีอุณหภูมิต่างกันจนเกิดการสะท้อนกลับหมด"),
    ("การเห็นเหรียญที่ก้นแก้วน้ำอยู่ตื้นกว่าความเป็นจริง",
     "การหักเหของแสงเมื่อเดินทางจากน้ำออกสู่อากาศ"),
    ("การส่งสัญญาณผ่านเส้นใยแก้วนำแสง",
     "การสะท้อนกลับหมดของแสงภายในตัวกลางที่มีดัชนีหักเหมากกว่า"),
    ("การมองเห็นภาพของตนเองในกระจกเงาราบ",
     "การสะท้อนของแสงที่ผิวเรียบของกระจก"),
    ("การเห็นท้องฟ้าเป็นสีน้ำเงินในเวลากลางวัน",
     "การกระเจิงของแสงโดยโมเลกุลของอากาศ"),
    ("การเห็นหลอดดูดน้ำในแก้วน้ำดูเหมือนหักงอตรงผิวน้ำ",
     "การหักเหของแสงเมื่อเดินทางจากน้ำออกสู่อากาศ"),
    ("การเห็นแสงขาวแยกเป็นแถบสีเมื่อผ่านปริซึม",
     "การหักเหและการกระจายของแสงขาวในหยดน้ำ"),
    ("การเห็นท้องฟ้าเป็นสีส้มแดงตอนดวงอาทิตย์ตก",
     "การกระเจิงของแสงโดยโมเลกุลของอากาศ"),
    ("การมองเห็นภาพสะท้อนของต้นไม้บนผิวน้ำนิ่ง",
     "การสะท้อนของแสงที่ผิวเรียบของกระจก"),
    ("การเห็นเพชรที่เจียระไนแล้วแวววาวมาก",
     "การสะท้อนกลับหมดของแสงภายในตัวกลางที่มีดัชนีหักเหมากกว่า"),
    ("การเห็นสระว่ายน้ำตื้นกว่าความลึกจริงเมื่อมองจากขอบสระ",
     "การหักเหของแสงเมื่อเดินทางจากน้ำออกสู่อากาศ"),
)


PHENOMENON_CAUSES = tuple(cause for _, cause in LIGHT_PHENOMENA)


# (ภาวะสายตา, อาการ, เลนส์ที่ใช้แก้ไข, เหตุผล)
VISION_DEFECTS = (
    ("สายตาสั้น", "มองวัตถุที่อยู่ไกลไม่ชัด เพราะภาพไปตกก่อนถึงจอตา",
     "เลนส์เว้า", "ช่วยกระจายแสงให้ภาพเลื่อนไปตกบนจอตาพอดี"),
    ("สายตายาว", "มองวัตถุที่อยู่ใกล้ไม่ชัด เพราะภาพไปตกเลยจอตา",
     "เลนส์นูน", "ช่วยรวมแสงให้ภาพเลื่อนเข้ามาตกบนจอตาพอดี"),
)


@question_type("phys.optics",
               display_name={"th": "ทัศนอุปกรณ์ (เลนส์และกระจก)"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class OpticalDevices(ClassifyType):
    """จำแนกทัศนอุปกรณ์ตามหน้าที่ รวมแสง (นูน/เว้า) หรือ กระจายแสง (เว้า/นูน)."""

    CLASSIFY_STEM = "“{member}” ทำหน้าที่แบบใด"
    PICK_STEM = "ทัศนอุปกรณ์ในข้อใดทำหน้าที่{category}"

    CATEGORIES = [
        Category("รวมแสง (Converging)",
                 ("เลนส์นูน (Convex Lens)", "กระจกเว้า (Concave Mirror)",
                  "เลนส์ของแว่นขยาย", "เลนส์แว่นตาของคนสายตายาว", "กระจกส่องฟันของทันตแพทย์",
                  "แผ่นสะท้อนแสงด้านหลังหลอดไฟฉาย", "เลนส์แก้วตาของมนุษย์", "จานรับสัญญาณดาวเทียม")),
        Category("กระจายแสง (Diverging)",
                 ("เลนส์เว้า (Concave Lens)", "กระจกนูน (Convex Mirror)",
                  "เลนส์แว่นตาของคนสายตาสั้น", "กระจกมองข้างรถยนต์", "กระจกโค้งที่ติดตรงทางแยก",
                  "กระจกโค้งมุมห้องในร้านสะดวกซื้อ")),
    ]


@question_type(
    "phys.optics_fluency",
    display_name={"th": "ทัศนอุปกรณ์: ชิ้นส่วนหลักและลักษณะภาพที่ใช้งาน"},
    level={"th": "ม.3"}, subject=PHYSICS, topic=WAVES,
)
class OpticalDeviceFluency(QuestionType):
    """Read one device off the table: which element it uses, or which image it forms."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        device, element, image = rng.choice(DEVICE_FACTS)
        if rng.random() < 0.5:
            wrongs = _distinct(element, [value for value in OPTICAL_ELEMENTS])
            assert wrongs is not None
            return _question(
                stem=f"{device}ใช้ชิ้นส่วนใดต่อไปนี้เป็นตัวสร้างภาพ",
                correct=element,
                wrongs=wrongs,
                hint="แยกก่อนว่าอุปกรณ์นั้นทำงานด้วยการหักเหของแสง (เลนส์) หรือการสะท้อนของแสง (กระจก)",
            )
        return _question(
            stem=f"ภาพที่ {device} สร้างขึ้นเพื่อการใช้งานตามปกติมีลักษณะอย่างไร",
            correct=image,
            wrongs=_image_wrongs(image, rng),
            hint="ถามตัวเองว่าภาพนั้นต้องรับบนฉากหรือเซนเซอร์หรือไม่ และต้องใหญ่ขึ้นหรือเล็กลง",
        )


@question_type(
    "phys.optics_application",
    display_name={"th": "ทัศนอุปกรณ์และปรากฏการณ์ของแสง: อธิบายและเลือกวิธีแก้ไข"},
    level={"th": "ม.3"}, subject=PHYSICS, topic=WAVES,
)
class OpticalDeviceApplication(QuestionType):
    """Explain a light phenomenon, or choose the lens that corrects a vision defect."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            phenomenon, cause = rng.choice(LIGHT_PHENOMENA)
            wrongs = _distinct(
                cause, rng.sample([value for value in PHENOMENON_CAUSES if value != cause],
                                  len([value for value in PHENOMENON_CAUSES if value != cause])),
            )
            assert wrongs is not None
            return _question(
                stem=f"{phenomenon} เกิดจากสมบัติใดของแสงเป็นหลัก",
                correct=cause,
                wrongs=wrongs,
                hint="ดูว่าแสงเปลี่ยนตัวกลางหรือไม่ ถ้าเปลี่ยนให้คิดถึงการหักเห ถ้าไม่เปลี่ยนให้คิดถึงการสะท้อน",
            )
        name, symptom, lens, reason = rng.choice(VISION_DEFECTS)
        other = next(row for row in VISION_DEFECTS if row[0] != name)
        return _question(
            stem=f"ผู้ที่มีภาวะ{name} ({symptom}) ควรแก้ไขด้วยเลนส์ชนิดใด เพราะเหตุใด",
            correct=f"{lens} เพราะ{reason}",
            wrongs=(
                f"{other[2]} เพราะ{other[3]}",
                f"{other[2]} เพราะ{reason}",
                f"{lens} เพราะ{other[3]}",
            ),
            hint="ถ้าภาพตกก่อนถึงจอตาต้องดึงภาพให้ถอยออกไป ถ้าภาพตกเลยจอตาต้องดึงภาพให้เข้ามา",
        )
