"""การรวบรวม ประมวลผล และนำเสนอข้อมูล

วิทยาการคำนวณ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 4.2 ป.3/4

Sets moved here from: technology_t3s4.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t1s4 import _near
from otk.sets._support.technology_t2s3 import _bank
from otk.sets._support.technology_t3s4 import P3

PROVENANCE = Provenance("original")


PRESENT_TOPIC = "การรวบรวม ประมวลผล และนำเสนอข้อมูล"


SOFTWARE = (
    ("พิมพ์รายงานเรื่องต้นไม้ในโรงเรียน", "โปรแกรมประมวลผลคำ"),
    ("บันทึกคะแนนสอบของเพื่อนทั้งห้องและหาผลรวม", "โปรแกรมตารางทำการ"),
    ("ทำสไลด์นำเสนอผลการสำรวจหน้าชั้นเรียน", "โปรแกรมนำเสนอ"),
    ("วาดภาพประกอบโปสเตอร์รณรงค์", "โปรแกรมวาดภาพ"),
    ("ทำแผนภูมิแท่งจากตารางคะแนน", "โปรแกรมตารางทำการ"),
    ("ตัดต่อคลิปการทดลองพร้อมเสียงบรรยาย", "โปรแกรมตัดต่อวิดีโอ"),
    ("เขียนจดหมายเชิญผู้ปกครองมาร่วมงาน", "โปรแกรมประมวลผลคำ"),
    ("อัดเสียงรายงานข่าวประจำวัน", "โปรแกรมบันทึกเสียง"),
)


SOFTWARE_KINDS = ("โปรแกรมประมวลผลคำ", "โปรแกรมตารางทำการ", "โปรแกรมนำเสนอ", "โปรแกรมวาดภาพ",
                  "โปรแกรมตัดต่อวิดีโอ", "โปรแกรมบันทึกเสียง")


SURVEYS = (
    ("ผลไม้ที่ชอบ", ("มะม่วง", "กล้วย", "ส้ม", "แตงโม")),
    ("สัตว์เลี้ยงที่มีที่บ้าน", ("แมว", "สุนัข", "ปลา", "นก")),
    ("กีฬาที่ชอบ", ("ฟุตบอล", "ว่ายน้ำ", "แบดมินตัน", "วิ่ง")),
    ("วิธีเดินทางมาโรงเรียน", ("เดิน", "จักรยาน", "รถยนต์", "รถโดยสาร")),
    ("สีที่ชอบ", ("แดง", "ฟ้า", "เขียว", "เหลือง")),
)


PRESENTATIONS = (
    ("เปรียบเทียบจำนวนนักเรียนที่ชอบผลไม้แต่ละชนิดให้เห็นได้ชัดในทันที", "แผนภูมิแท่ง",
     ("ข้อความยาวหนึ่งหน้า", "เสียงอ่านรายชื่อนักเรียน", "ภาพถ่ายผลไม้หนึ่งภาพ", "รายชื่อนักเรียนเรียงตามตัวอักษร")),
    ("แสดงคะแนนของนักเรียนแต่ละคนอย่างละเอียดเพื่อให้ครูตรวจ", "ตาราง",
     ("ภาพวาดการ์ตูน", "แผนภูมิแท่งที่ไม่มีตัวเลข", "เพลงประกอบ", "คำบรรยายสั้น ๆ หนึ่งประโยค")),
    ("นำเสนอผลการสำรวจหน้าชั้นเรียนพร้อมภาพประกอบทีละหัวข้อ", "สไลด์นำเสนอ",
     ("ตารางตัวเลขเพียงอย่างเดียว", "ไฟล์เสียงที่ไม่มีภาพ", "ข้อความยาวบนกระดาษแผ่นเดียว", "รายชื่อไฟล์ในโฟลเดอร์")),
    ("แสดงจำนวนสัตว์เลี้ยงของเพื่อนด้วยรูปภาพให้น้อง ป.1 เข้าใจง่าย", "แผนภูมิรูปภาพ",
     ("ตารางตัวเลขละเอียด", "ข้อความยาวหลายหน้า", "สูตรคำนวณ", "รายชื่อเว็บไซต์")),
    ("บอกเล่าผลการสำรวจให้เพื่อนที่มองไม่เห็นฟัง", "เสียงบรรยายผลการสำรวจ",
     ("แผนภูมิแท่งไม่มีคำอธิบาย", "ภาพถ่ายไม่มีเสียง", "ตารางบนกระดาษ", "สไลด์ที่มีแต่ภาพ")),
    ("ติดประกาศผลการสำรวจไว้ที่บอร์ดหน้าห้องให้ทุกคนอ่านได้ตลอดวัน", "โปสเตอร์ที่มีแผนภูมิและคำอธิบายสั้น ๆ",
     ("เสียงประกาศครั้งเดียว", "ไฟล์ที่เก็บไว้ในเครื่องของครู", "คลิปวิดีโอในโทรศัพท์ของเพื่อน", "การเล่าปากเปล่า")),
)


STEPS = ("รวบรวมข้อมูล", "ประมวลผลข้อมูล", "นำเสนอข้อมูล")


STEP_EXAMPLES = (
    ("ถามเพื่อนแต่ละคนว่าชอบผลไม้อะไร", "รวบรวมข้อมูล"),
    ("จดคำตอบของเพื่อนลงในแบบบันทึก", "รวบรวมข้อมูล"),
    ("นับจำนวนเพื่อนที่ชอบผลไม้แต่ละชนิด", "ประมวลผลข้อมูล"),
    ("หาผลรวมของคะแนนด้วยโปรแกรมตารางทำการ", "ประมวลผลข้อมูล"),
    ("ทำแผนภูมิแท่งแสดงผลให้เพื่อนดู", "นำเสนอข้อมูล"),
    ("ออกไปเล่าผลการสำรวจหน้าชั้นเรียนด้วยสไลด์", "นำเสนอข้อมูล"),
    ("ชั่งน้ำหนักกระเป๋าของเพื่อนแต่ละคนแล้วจดไว้", "รวบรวมข้อมูล"),
    ("เรียงชื่อเพื่อนตามน้ำหนักกระเป๋าจากมากไปน้อย", "ประมวลผลข้อมูล"),
    ("ติดโปสเตอร์ผลการสำรวจไว้ที่บอร์ดหน้าห้อง", "นำเสนอข้อมูล"),
)


@question_type(
    "comp.data_present_foundation",
    display_name={"th": "เลือกซอฟต์แวร์ให้เหมาะกับงาน"},
    level=P3, subject=SUBJECT, topic=PRESENT_TOPIC,
)
class DataPresentFoundation(QuestionType):
    def build(self, rng: Random, **params):
        job, kind = rng.choice(SOFTWARE)
        return _labelled(stem=f"ถ้าต้องการ{job} ควรใช้ซอฟต์แวร์ใด", correct=kind,
                         wrongs=tuple([k for k in SOFTWARE_KINDS if k != kind]),
                         hint="ประมวลผลคำใช้พิมพ์เอกสาร ตารางทำการใช้คำนวณและทำแผนภูมิ นำเสนอใช้ทำสไลด์",
                         topic=PRESENT_TOPIC)


@question_type(
    "comp.data_present_fluency",
    display_name={"th": "อ่านผลการสำรวจที่ประมวลผลแล้ว"},
    level=P3, subject=SUBJECT, topic=PRESENT_TOPIC,
)
class DataPresentFluency(QuestionType):
    """A tallied survey: the most or least popular, a total, or a difference."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params):
        subject, items = rng.choice(SURVEYS)
        counts = rng.sample(range(2, 13), len(items))
        table = " ".join(f"{i} {c} คน" for i, c in zip(items, counts))
        lead = f"นักเรียนสำรวจ{subject}ของเพื่อนในห้อง แล้วใช้ซอฟต์แวร์นับจำนวนได้ดังนี้ {table}"
        ask = rng.choice(("most", "least", "total", "difference"))
        hint = "อ่านจำนวนของแต่ละรายการจากผลการสำรวจ แล้วเปรียบเทียบ รวม หรือหาผลต่างตามที่ถาม"
        if ask in ("most", "least"):
            pick = max if ask == "most" else min
            answer = items[counts.index(pick(counts))]
            return _labelled(stem=f"{lead} {subject}ใดมีผู้เลือก{'มากที่สุด' if ask == 'most' else 'น้อยที่สุด'}",
                             correct=answer, wrongs=tuple(i for i in items if i != answer),
                             hint=hint, topic=PRESENT_TOPIC)
        if ask == "total":
            total = sum(counts)
            wrongs = _near(total, (total - counts[0], total + counts[-1], max(counts) * len(counts)))
            return _labelled(stem=f"{lead} นักเรียนที่ตอบแบบสำรวจมีทั้งหมดกี่คน", correct=f"{total} คน",
                             wrongs=tuple(f"{w} คน" for w in rng.sample(wrongs[:4], 3)),
                             hint=hint, topic=PRESENT_TOPIC)
        a, b = rng.sample(range(len(items)), 2)
        gap = abs(counts[a] - counts[b])
        wrongs = _near(gap, (counts[a] + counts[b], max(counts[a], counts[b]), gap + 2))
        return _labelled(stem=f"{lead} ผู้ที่เลือก{items[a]}กับผู้ที่เลือก{items[b]}ต่างกันกี่คน",
                         correct=f"{gap} คน", wrongs=tuple(f"{w} คน" for w in rng.sample(wrongs[:4], 3)),
                         hint=hint, topic=PRESENT_TOPIC)


@question_type(
    "comp.data_present_application",
    display_name={"th": "เลือกวิธีนำเสนอและขั้นตอนการจัดการข้อมูล"},
    level=P3, subject=SUBJECT, topic=PRESENT_TOPIC,
)
class DataPresentApplication(QuestionType):
    def build(self, rng: Random, **params):
        if rng.random() < 0.5:
            return _bank(rng, PRESENTATIONS, "ถ้าต้องการ{} ควรนำเสนอข้อมูลแบบใด",
                         hint="แผนภูมิช่วยเปรียบเทียบ ตารางแสดงตัวเลขละเอียด สไลด์ใช้นำเสนอทีละหัวข้อ",
                         topic=PRESENT_TOPIC)
        action, step = rng.choice(STEP_EXAMPLES)
        return _labelled(stem=f"การ{action} เป็นขั้นตอนใดของการจัดการข้อมูล", correct=step,
                         wrongs=tuple(s for s in STEPS if s != step) + ("ลบข้อมูล",),
                         hint="ขั้นตอนเรียงเป็น รวบรวมข้อมูล แล้วประมวลผล เช่น นับหรือคำนวณ แล้วจึงนำเสนอ",
                         topic=PRESENT_TOPIC)
