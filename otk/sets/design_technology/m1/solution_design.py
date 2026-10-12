"""การออกแบบวิธีการแก้ปัญหา

การออกแบบและเทคโนโลยี · ม.1 · สสวท. พื้นฐาน
Indicators: ว 4.1 ม.1/3

Sets moved here from: technology_t2s1.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1 import SUBJECT
from otk.sets._support.technology_t2s1 import LABELS, M1

PROVENANCE = Provenance("original")


DESIGN_TOPIC = "การออกแบบวิธีการแก้ปัญหา"


#: (thing designed, what the measure is, its unit, the measure's range).
CONTEXTS = (
    ("ชั้นวางรองเท้า", "วางรองเท้าได้", "คู่", (8, 30)),
    ("ถังเก็บน้ำฝนสำหรับรดน้ำต้นไม้", "เก็บน้ำได้", "ลิตร", (20, 80)),
    ("ที่วางโทรศัพท์", "รับน้ำหนักได้", "กรัม", (200, 600)),
)


PLANS = {
    "ทำที่วางโทรศัพท์จากไม้": ("ร่างแบบและกำหนดขนาดของชิ้นส่วน", "วัดและตัดไม้ตามแบบ",
                              "ประกอบชิ้นส่วนด้วยกาวและตะปู", "ขัดผิวแล้วทดลองวางโทรศัพท์"),
    "ทำที่แยกขยะจากกล่องกระดาษ": ("กำหนดประเภทขยะที่จะแยก", "ตัดกล่องให้ได้ขนาดตามแบบ",
                                 "ติดป้ายและสีบอกประเภทขยะ", "นำไปวางทดลองใช้ในโรงอาหาร"),
    "ทำกล่องแยกยาเจ็ดวัน": ("กำหนดจำนวนช่องตามวันและมื้อ", "ตัดแผ่นพลาสติกทำผนังกั้นช่อง",
                           "เขียนชื่อวันและมื้อตัวใหญ่ที่แต่ละช่อง", "ให้คุณยายทดลองใส่และหยิบยา"),
    "ทำที่ม้วนเก็บสายชาร์จ": ("นับจำนวนสายและวัดความยาว", "ออกแบบช่องม้วนสายให้พอดีกับความยาว",
                             "ตัดและประกอบวัสดุตามแบบ", "ทดลองม้วนเก็บและดึงสายออก"),
    "ทำระบบรดน้ำด้วยขวดพลาสติก": ("คำนวณปริมาณน้ำที่ต้นไม้ต้องใช้", "เจาะรูที่ฝาขวดให้น้ำหยดช้า ๆ",
                                 "คว่ำขวดปักลงในดินในกระถาง", "สังเกตว่าดินชื้นพอตลอดหลายวันหรือไม่"),
}


PLAN_HINT = "ต้องรู้ขนาดและรายละเอียดก่อนจึงตัดวัสดุได้ ต้องมีชิ้นส่วนก่อนจึงประกอบได้ และต้องประกอบเสร็จก่อนจึงทดสอบได้"


PRESENTATIONS = (
    ("ต้องการบอกผู้สร้างว่าชิ้นงานมีขนาดและส่วนประกอบอย่างไร",
     "ภาพร่างที่ระบุขนาดและชื่อส่วนประกอบ",
     ("ภาพระบายสีสวยงามที่ไม่บอกขนาด",
      "คำอธิบายด้วยคำพูดโดยไม่มีภาพ",
      "ภาพถ่ายวัสดุที่ยังไม่ได้ตัดเป็นชิ้น",
      "ใบเสร็จค่าวัสดุที่ซื้อมาทั้งหมด",
      "คลิปสาธิตการใช้งานชิ้นงานจริง")),
    ("ต้องการให้เพื่อนเข้าใจลำดับการทำงานของชิ้นงาน",
     "ผังงานหรือแผนภาพแสดงขั้นตอนการทำงานทีละขั้น",
     ("ภาพร่างที่ระบุเฉพาะขนาดของชิ้นงานแต่ละส่วน",
      "ภาพถ่ายชิ้นงานที่เสร็จแล้วจากมุมเดียว",
      "ตารางรายชื่อเครื่องมือที่ใช้สร้างชิ้นงาน",
      "ตารางราคาวัสดุที่ใช้ในแต่ละขั้นตอน",
      "ภาพร่างสามมิติที่ระบายสีสวยงามทุกด้าน")),
    ("ต้องการเปรียบเทียบข้อดีข้อเสียของแนวคิดหลายแบบก่อนเลือก",
     "ตารางเปรียบเทียบแต่ละแนวคิดตามเกณฑ์เดียวกัน",
     ("ภาพร่างของแนวคิดที่ชอบที่สุดเพียงแบบเดียว",
      "คลิปสาธิตการใช้ชิ้นงานที่สร้างเสร็จแล้ว",
      "รายการวัสดุของแนวคิดแรกที่คิดได้",
      "ผังงานการทำงานของแนวคิดสุดท้าย",
      "ภาพถ่ายของผู้ใช้งานขณะใช้ชิ้นงานต้นแบบ")),
    ("ต้องการแสดงผลการทดสอบความแข็งแรงหลายครั้ง",
     "ตารางหรือกราฟแสดงผลการทดสอบแต่ละครั้ง",
     ("คำบอกเล่าเฉพาะครั้งที่ได้ผลดีที่สุด",
      "ภาพร่างของชิ้นงานก่อนเริ่มสร้าง",
      "คำบรรยายความรู้สึกของผู้สร้างชิ้นงาน",
      "ภาพถ่ายวัสดุที่ซื้อมาใช้ทดสอบ",
      "รายชื่อผู้ทดสอบและวันที่ทดสอบทุกครั้ง")),
    ("ต้องการให้ผู้ใช้เห็นว่าชิ้นงานใช้งานจริงอย่างไร",
     "สาธิตการใช้ชิ้นงานจริง หรือคลิปวิดีโอสั้นขณะใช้งาน",
     ("ภาพร่างแนวคิดแรกของชิ้นงานที่ไม่ได้นำมาใช้สร้าง",
      "ผลการสำรวจข้อมูลความต้องการก่อนเริ่มออกแบบ",
      "ตารางราคาวัสดุและรายชื่อเครื่องมือที่ใช้สร้าง",
      "ภาพถ่ายกล่องบรรจุวัสดุก่อนนำมาสร้างชิ้นงาน",
      "ตารางเปรียบเทียบแนวคิดทั้งหมดที่เคยคิดก่อนสร้างชิ้นงาน")),
    ("ต้องการบอกค่าใช้จ่ายของการสร้างชิ้นงาน",
     "ตารางรายการวัสดุ จำนวน และราคา",
     ("ภาพร่างสามมิติของชิ้นงานทั้งชิ้น",
      "ผังงานการทำงานของชิ้นงาน",
      "คลิปการทดสอบชิ้นงานจริงทุกครั้ง",
      "ภาพถ่ายชิ้นงานที่เสร็จแล้ว",
      "รายชื่อผู้ใช้งานชิ้นงาน")),
)


@question_type(
    "tech.solution_design_foundation",
    display_name={"th": "เลือกแนวทางแก้ปัญหาที่ตรงตามความต้องการ"},
    level=M1, subject=SUBJECT, topic=DESIGN_TOPIC,
)
class SolutionDesignFoundation(QuestionType):
    """Four options, a price cap and a minimum; exactly one meets both."""

    def build(self, rng: Random, **params):
        thing, measure, unit, (low, high) = rng.choice(CONTEXTS)
        cap = rng.randrange(150, 401, 10)
        need = rng.randint(low + 2, high - 2)
        good = (rng.randrange(cap - 60, cap + 1, 10), rng.randint(need, high))
        pricey = (rng.randrange(cap + 10, cap + 101, 10), rng.randint(need, high))
        weak = (rng.randrange(cap - 80, cap + 1, 10), rng.randint(low, need - 1))
        both = (rng.randrange(cap + 10, cap + 101, 10), rng.randint(low, need - 1))
        options = [good, pricey, weak, both]
        rng.shuffle(options)
        listed = " ".join(f"แบบ {label} ราคา {price} บาท {measure} {amount} {unit}"
                          for label, (price, amount) in zip(LABELS, options))
        answer = LABELS[options.index(good)]
        return _labelled(
            stem=(f"ต้องการ{thing}ที่ราคาไม่เกิน {cap} บาท และ{measure}อย่างน้อย {need} {unit} "
                  f"มีแนวทางให้เลือกดังนี้ {listed} ควรเลือกแบบใด"),
            correct=f"แบบ {answer}", wrongs=tuple(f"แบบ {ell}" for ell in LABELS if ell != answer),
            hint="ตรวจทุกแบบกับเงื่อนไขทีละข้อ แบบที่เลือกต้องผ่านทั้งเรื่องราคาและเรื่องความสามารถ",
            topic=DESIGN_TOPIC,
        )


@question_type(
    "tech.solution_design_fluency",
    display_name={"th": "วางแผนลำดับขั้นตอนการสร้างชิ้นงาน"},
    level=M1, subject=SUBJECT, topic=DESIGN_TOPIC,
)
class SolutionDesignFluency(QuestionType):
    def build(self, rng: Random, **params):
        task = rng.choice(list(PLANS))
        steps = list(PLANS[task])
        if rng.random() < 0.5:
            shown = steps[:]
            while shown == steps:
                rng.shuffle(shown)
            label = {s: LABELS[i] for i, s in enumerate(shown)}
            correct = " → ".join(label[s] for s in steps)
            wrongs: list[str] = []
            while len(wrongs) < 3:
                candidate = steps[:]
                rng.shuffle(candidate)
                text = " → ".join(label[s] for s in candidate)
                if text != correct and text not in wrongs:
                    wrongs.append(text)
            listed = " ".join(f"({label[s]}) {s}" for s in shown)
            return _labelled(
                stem=f"แผนการ{task}ถูกสลับลำดับ {listed} ลำดับที่ถูกต้องคือข้อใด",
                correct=correct, wrongs=tuple(wrongs), hint=PLAN_HINT, topic=DESIGN_TOPIC,
            )
        gap = rng.randrange(4)
        shown = " → ".join("____" if i == gap else s for i, s in enumerate(steps))
        others = [s for t, ss in PLANS.items() if t != task for s in ss]
        return _labelled(
            stem=f"แผนการ{task}คือ {shown} ขั้นตอนที่หายไปคือข้อใด",
            correct=steps[gap], wrongs=tuple(others),
            hint=PLAN_HINT, topic=DESIGN_TOPIC,
        )


@question_type(
    "tech.solution_design_application",
    display_name={"th": "เลือกวิธีนำเสนอแนวทางการแก้ปัญหาให้ผู้อื่นเข้าใจ"},
    level=M1, subject=SUBJECT, topic=DESIGN_TOPIC,
)
class SolutionDesignApplication(QuestionType):
    def build(self, rng: Random, **params):
        purpose, best, wrongs = rng.choice(PRESENTATIONS)
        return _labelled(
            stem=f"{purpose} ควรนำเสนอด้วยวิธีใดจึงเหมาะสมที่สุด",
            correct=best, wrongs=tuple(wrongs),
            hint="เลือกรูปแบบที่บอกสิ่งที่ผู้ฟังต้องรู้ได้ชัดที่สุด ขนาดใช้ภาพร่าง ลำดับใช้ผังงาน ตัวเลขใช้ตารางหรือกราฟ",
            topic=DESIGN_TOPIC,
        )
