"""การจัดการขยะ

ภูมิศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: ส 5.2 ป.2/4
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.geography import P2, SUBJECT, choices, stage

PROVENANCE = Provenance("original")


TOPIC = "การจัดการขยะ"


@question_type(
    "geog.waste_bin_p2",
    display_name={"th": "แยกขยะลงถังตามสีที่กำหนด"},
    level=P2, subject=SUBJECT, topic=TOPIC,
)
@stage(1)
class WasteBin(ClassifyType):
    # The bin colours of กรมควบคุมมลพิษ: green for waste that rots, yellow for
    # recyclables, red for hazardous waste, blue for general waste. Items that
    # schools sort differently (tissue, foam boxes) are left out.
    CLASSIFY_STEM = "“{member}” ควรทิ้งลงถังขยะสีใด"
    PICK_STEM = "ข้อใดควรทิ้งลง{category}"
    CATEGORIES = [
        Category("ถังสีเขียว (ขยะย่อยสลายได้)", ("เปลือกกล้วย", "เศษผักจากครัว", "ข้าวที่กินเหลือ",
                                                 "ใบไม้แห้ง")),
        Category("ถังสีเหลือง (ขยะรีไซเคิล)", ("ขวดพลาสติกใส", "กระป๋องอะลูมิเนียม", "ขวดแก้ว",
                                               "กล่องกระดาษลัง")),
        Category("ถังสีแดง (ขยะอันตราย)", ("ถ่านไฟฉายที่ใช้แล้ว", "หลอดไฟที่เสีย", "กระป๋องสเปรย์ฉีดยุง",
                                           "ขวดยาฆ่าแมลง")),
        Category("ถังสีน้ำเงิน (ขยะทั่วไป)", ("ซองขนมที่เปื้อนน้ำมัน", "ถุงพลาสติกเปื้อนอาหาร",
                                              "หลอดดูดพลาสติกที่ใช้แล้ว")),
    ]


@question_type(
    "geog.three_r_p2",
    display_name={"th": "จำแนกการลดใช้ การใช้ซ้ำ และการนำกลับมาใช้ใหม่"},
    level=P2, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class ThreeR(ClassifyType):
    ASKS = ("pick",)           # three groups: a classify question would offer three choices
    PICK_STEM = "ข้อใดเป็นการ{category}"
    CATEGORIES = [
        Category("ลดการใช้ (Reduce)", ("พกถุงผ้าไปตลาดแทนการรับถุงพลาสติก",
                                       "พกขวดน้ำส่วนตัวแทนการซื้อน้ำขวดใหม่",
                                       "ปฏิเสธหลอดพลาสติกเมื่อซื้อน้ำดื่ม")),
        Category("ใช้ซ้ำ (Reuse)", ("ใช้ขวดน้ำพลาสติกเก่าเป็นกระถางปลูกต้นไม้",
                                    "นำกระดาษที่ใช้หน้าเดียวมาเขียนอีกหน้า",
                                    "ใช้กล่องรองเท้าเก่าเป็นกล่องเก็บของ")),
        Category("นำกลับมาใช้ใหม่ (Recycle)", ("ส่งกระป๋องเข้าโรงงานหลอมทำเป็นกระป๋องใหม่",
                                               "ขายขวดพลาสติกให้ร้านรับซื้อของเก่าไปแปรรูป",
                                               "นำกระดาษเก่าไปผ่านกระบวนการผลิตกระดาษใหม่")),
    ]


# Items for a clean-up count, by the bin they go in (as WasteBin files them).
BIN_ITEMS = {c.label: c.members for c in WasteBin.CATEGORIES}
UNITS = {"เปลือกกล้วย": "ชิ้น", "เศษผักจากครัว": "ถุง", "ข้าวที่กินเหลือ": "จาน", "ใบไม้แห้ง": "ถุง",
         "ขวดพลาสติกใส": "ขวด", "กระป๋องอะลูมิเนียม": "ใบ", "ขวดแก้ว": "ขวด", "กล่องกระดาษลัง": "กล่อง",
         "ถ่านไฟฉายที่ใช้แล้ว": "ก้อน", "หลอดไฟที่เสีย": "หลอด", "กระป๋องสเปรย์ฉีดยุง": "ใบ",
         "ขวดยาฆ่าแมลง": "ขวด", "ซองขนมที่เปื้อนน้ำมัน": "ซอง", "ถุงพลาสติกเปื้อนอาหาร": "ใบ",
         "หลอดดูดพลาสติกที่ใช้แล้ว": "อัน"}


@question_type(
    "geog.waste_count_p2",
    display_name={"th": "นับจำนวนขยะที่ต้องทิ้งลงถังแต่ละสี"},
    level=P2, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class WasteCount(QuestionType):
    def build(self, rng: Random, **params):
        bins = list(BIN_ITEMS)
        found = []                                   # (item, count, bin)
        for label in bins:
            for item in rng.sample(BIN_ITEMS[label], rng.randint(1, 2)):
                found.append((item, rng.randint(1, 5), label))
        rng.shuffle(found)
        asked = rng.choice(bins)
        total = sum(n for _, n, b in found if b == asked)
        listed = " ".join(f"{item} {n} {UNITS[item]}" for item, n, _ in found)
        everything = sum(n for _, n, _ in found)
        others = [sum(n for _, n, b in found if b == label) for label in bins if label != asked]
        colour = asked.split(" (")[0]
        return choices(
            stem=f"หลังทำความสะอาดห้องเรียน เก็บขยะได้ดังนี้: {listed} ขยะที่ต้องทิ้งลง{colour}มีทั้งหมดกี่ชิ้น",
            correct=f"{total} ชิ้น",
            wrongs=[*(f"{n} ชิ้น" for n in others), f"{everything} ชิ้น",
                    f"{total + 1} ชิ้น", f"{total + 2} ชิ้น", f"{max(total - 1, 1)} ชิ้น"],
            hint="แยกขยะแต่ละอย่างตามถังก่อน แล้วรวมจำนวนเฉพาะขยะที่ต้องทิ้งลงถังที่ถาม",
            topic=TOPIC)
