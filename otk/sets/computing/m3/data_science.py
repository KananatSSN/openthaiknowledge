"""วิทยาการข้อมูลเบื้องต้น

วิทยาการคำนวณ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 4.2 ม.3/2

Sets moved here from: technology_t3s6.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t1s6 import _pair_either_way
from otk.sets._support.technology_t3s6 import M3

PROVENANCE = Provenance("original")


SCIENCE_TOPIC = "วิทยาการข้อมูลเบื้องต้น"


STAGES = (
    ("กำหนดว่าอยากรู้ว่านักเรียนใช้เวลากับโทรศัพท์วันละกี่ชั่วโมง", "ตั้งคำถามหรือกำหนดปัญหา"),
    ("แจกแบบสอบถามออนไลน์ให้นักเรียนทุกห้องตอบ", "เก็บรวบรวมข้อมูล"),
    ("ลบคำตอบที่ซ้ำและคำตอบที่เป็นไปไม่ได้ เช่น 30 ชั่วโมงต่อวัน", "เตรียมและทำความสะอาดข้อมูล"),
    ("หาค่าเฉลี่ยและเปรียบเทียบเวลาของแต่ละระดับชั้น", "วิเคราะห์ข้อมูล"),
    ("ทำกราฟและอินโฟกราฟิกสรุปผลให้ผู้บริหารโรงเรียน", "นำเสนอผลและสื่อสาร"),
)


CHARTS = (
    ("แสดงการเปลี่ยนแปลงของอุณหภูมิในแต่ละเดือนตลอดปี", "กราฟเส้น"),
    ("แสดงสัดส่วนค่าใช้จ่ายแต่ละประเภทเมื่อเทียบกับค่าใช้จ่ายทั้งหมด", "แผนภูมิวงกลม"),
    ("เปรียบเทียบจำนวนนักเรียนที่ชอบกีฬาแต่ละชนิด", "แผนภูมิแท่ง"),
    ("แสดงความสัมพันธ์ระหว่างเวลาอ่านหนังสือกับคะแนนสอบของนักเรียนแต่ละคน", "แผนภาพการกระจาย"),
    ("แสดงค่าที่แน่นอนของคะแนนนักเรียนทุกคนในทุกวิชา", "ตาราง"),
)


MONTHS = ("ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.")


@question_type(
    "comp.data_science_foundation",
    display_name={"th": "ระบุขั้นตอนของกระบวนการวิทยาการข้อมูล"},
    level=M3, subject=SUBJECT, topic=SCIENCE_TOPIC,
)
class DataScienceFoundation(QuestionType):
    def build(self, rng: Random, **params):
        return _pair_either_way(rng, STAGES, forward="การ{} เป็นขั้นตอนใดของกระบวนการวิทยาการข้อมูล",
                                backward="ข้อใดเป็นการทำงานในขั้น{}",
                                hint="กระบวนการวิทยาการข้อมูลเรียงเป็น ตั้งคำถาม เก็บรวบรวมข้อมูล เตรียมข้อมูล วิเคราะห์ และนำเสนอผล",
                                topic=SCIENCE_TOPIC)


@question_type(
    "comp.data_science_fluency",
    display_name={"th": "เลือกแผนภูมิให้เหมาะกับการนำเสนอข้อมูล"},
    level=M3, subject=SUBJECT, topic=SCIENCE_TOPIC,
)
class DataScienceFluency(QuestionType):
    def build(self, rng: Random, **params):
        return _pair_either_way(rng, CHARTS, forward="ถ้าต้องการ{} ควรนำเสนอด้วยข้อใด",
                                backward="{}เหมาะกับการนำเสนอข้อมูลแบบใดมากที่สุด",
                                hint="กราฟเส้นแสดงแนวโน้มตามเวลา แผนภูมิวงกลมแสดงส่วนของทั้งหมด แผนภูมิแท่งเปรียบเทียบกลุ่ม "
                                     "แผนภาพการกระจายแสดงความสัมพันธ์ของสองตัวแปร ตารางแสดงค่าที่แน่นอน",
                                topic=SCIENCE_TOPIC)


@question_type(
    "comp.data_science_application",
    display_name={"th": "สรุปผลที่ข้อมูลสนับสนุน"},
    level=M3, subject=SUBJECT, topic=SCIENCE_TOPIC,
)
class DataScienceApplication(QuestionType):
    """Six months of sales; exactly one of four statements is borne out."""

    def build(self, rng: Random, **params):
        while True:
            sales = [rng.randint(8, 30) * 10 for _ in MONTHS]
            if len(set(sales)) == 6 and sales != sorted(sales):
                break
        top = MONTHS[sales.index(max(sales))]
        total = sum(sales)
        a, b = rng.sample(range(6), 2)
        higher, lower = (a, b) if sales[a] > sales[b] else (b, a)

        def claim(kind: str, true: bool) -> str:
            if kind == "top":
                month = top if true else rng.choice([m for m in MONTHS if m != top])
                return f"เดือนที่ขายได้มากที่สุดคือ {month}"
            if kind == "total":
                return f"ยอดขายรวม 6 เดือนเท่ากับ {total if true else total + rng.choice((-100, -50, 50, 100))} ชิ้น"
            if kind == "compare":
                first, second = (higher, lower) if true else (lower, higher)
                return f"เดือน {MONTHS[first]} ขายได้มากกว่าเดือน {MONTHS[second]}"
            return "ยอดขายเพิ่มขึ้นทุกเดือน"          # never true: the data are not sorted

        kinds = ["top", "total", "compare", "rising"]
        true_kind = rng.choice(kinds[:3])
        table = " ".join(f"{m} {s}" for m, s in zip(MONTHS, sales))
        return _labelled(
            stem=f"ร้านค้าบันทึกยอดขายสินค้า (ชิ้น) 6 เดือนได้ดังนี้ {table} ข้อสรุปใดถูกต้องตามข้อมูล",
            correct=claim(true_kind, True),
            wrongs=tuple(claim(k, False) for k in kinds if k != true_kind),
            hint="ตรวจแต่ละข้อสรุปกับตัวเลขในข้อมูลทีละข้อ ข้อสรุปที่ถูกต้องต้องเป็นจริงตามข้อมูลทุกประการ",
            topic=SCIENCE_TOPIC)
