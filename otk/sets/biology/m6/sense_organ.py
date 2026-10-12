"""อวัยวะรับความรู้สึก

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/7

Sets moved here from: science_wave_f67.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f67 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_SENSE = "อวัยวะรับความรู้สึก"


SENSE_PARTS = (
    ("กระจกตา", "ตา", "ด่านแรกที่หักเหแสงเข้าสู่ตา"),
    ("ม่านตา", "ตา", "ปรับขนาดรูม่านตาเพื่อควบคุมปริมาณแสง"),
    ("เลนส์ตา", "ตา", "ปรับความโค้งเพื่อโฟกัสภาพให้ตกบนเรตินา"),
    ("เซลล์รูปแท่ง", "ตา", "รับแสงสลัวและเห็นเป็นขาวดำ"),
    ("เซลล์รูปกรวย", "ตา", "รับแสงสว่างและแยกสี"),
    ("เยื่อแก้วหู", "หู", "สั่นตามคลื่นเสียงและส่งต่อไปยังกระดูกหู"),
    ("กระดูกค้อน ทั่ง โกลน", "หู", "ขยายการสั่นส่งต่อไปยังหูชั้นใน"),
    ("คอเคลีย", "หู", "เปลี่ยนการสั่นเป็นกระแสประสาทการได้ยิน"),
    ("ช่องครึ่งวงกลม", "หู", "รับรู้การเคลื่อนไหวและการทรงตัวของศีรษะ"),
    ("ท่อยูสเตเชียน", "หู", "ปรับความดันอากาศในหูชั้นกลางให้เท่ากับภายนอก"),
    ("เซลล์รับกลิ่น", "จมูก", "รับสารเคมีที่ละลายในเมือกของโพรงจมูก"),
    ("ตุ่มรับรส", "ลิ้น", "รับรสหวาน เค็ม เปรี้ยว ขม และอูมามิ"),
)


DISORDERS = (
    ("สายตาสั้น", "ภาพตกก่อนถึงเรตินา แก้ไขด้วยเลนส์เว้า"),
    ("สายตายาว", "ภาพตกเลยเรตินา แก้ไขด้วยเลนส์นูน"),
    ("สายตาเอียง", "กระจกตาหรือเลนส์โค้งไม่เท่ากันทุกแนว แก้ไขด้วยเลนส์ทรงกระบอก"),
    ("ต้อกระจก", "เลนส์ตาขุ่น แก้ไขโดยผ่าตัดเปลี่ยนเลนส์"),
    ("ต้อหิน", "ความดันในลูกตาสูงจนทำลายเส้นประสาทตา"),
    ("หูชั้นกลางอักเสบ", "ติดเชื้อที่หูชั้นกลาง มักลุกลามมาจากคอผ่านท่อยูสเตเชียน"),
)


SENSE_HINT = ("กระจกตาและเลนส์หักเหแสง ม่านตาคุมแสง เซลล์รูปแท่งรับแสงสลัว เซลล์รูปกรวยแยกสี เยื่อแก้วหูและกระดูกหูส่งการสั่น "
              "คอเคลียรับเสียง ช่องครึ่งวงกลมรับการทรงตัว สายตาสั้นใช้เลนส์เว้า สายตายาวใช้เลนส์นูน")


CARE = (
    ("การอ่านหนังสือในที่แสงสว่างเพียงพอและพักสายตาเป็นระยะ", "ถนอมสายตา"),
    ("หลีกเลี่ยงการฟังเสียงดังมากเป็นเวลานาน และใช้ที่อุดหูในที่เสียงดัง", "ป้องกันการเสื่อมของการได้ยิน"),
    ("ไม่ใช้ของแข็งแคะหู", "ป้องกันเยื่อแก้วหูทะลุ"),
    ("สวมแว่นกันแดดเมื่ออยู่กลางแดดจัด", "ลดความเสี่ยงต้อกระจกจากรังสีอัลตราไวโอเลต"),
    ("ทาครีมกันแดดและหลีกเลี่ยงแดดจัด", "ลดความเสี่ยงมะเร็งผิวหนัง"),
)


SCENES = (
    ("ขณะเครื่องบินลดระดับ รู้สึกหูอื้อ การกลืนน้ำลายช่วยได้เพราะเหตุใด", "ท่อยูสเตเชียนเปิด ทำให้ความดันในหูชั้นกลางเท่ากับภายนอก",
     ("ทำให้เยื่อแก้วหูหนาขึ้น", "ทำให้คอเคลียหยุดทำงาน", "ท่อยูสเตเชียนปิด ทำให้ความดันในหูชั้นกลางสูงกว่าภายนอก", "เยื่อแก้วหูหนาขึ้น ทำให้ความดันในหูชั้นในเท่ากับภายนอก")),
    ("เมื่อเดินจากที่สว่างเข้าห้องมืด ระยะแรกมองไม่เห็น แล้วค่อย ๆ มองเห็นเพราะเหตุใด", "รูม่านตาขยายและเซลล์รูปแท่งปรับตัวไวต่อแสงสลัวขึ้น",
     ("รูม่านตาหรี่ลงและเซลล์รูปกรวยปรับตัวไวต่อแสงสลัวขึ้น", "เซลล์รูปกรวยทำงานมากขึ้นในที่มืด", "เลนส์ตาหยุดทำงาน", "กระจกตาขุ่นขึ้นชั่วคราว")),
    ("เมื่อเป็นหวัดคัดจมูก มักรับรสอาหารได้น้อยลงเพราะเหตุใด", "กลิ่นอาหารช่วยในการรับรส เมื่อรับกลิ่นไม่ได้จึงรับรสได้ไม่ชัด",
     ("ตุ่มรับรสถูกทำลายถาวร", "น้ำมูกไปเคลือบตุ่มรับรส ตุ่มรับรสจึงรับรสไม่ได้ชั่วคราว", "ไข้หวัดทำลายตุ่มรับรสบนลิ้นอย่างถาวร จึงรับรสได้ไม่ชัด", "เซลล์รับกลิ่นกลายเป็นตุ่มรับรส")),
    ("หมุนตัวหลายรอบแล้วหยุด รู้สึกเวียนศีรษะเพราะเหตุใด", "ของเหลวในช่องครึ่งวงกลมยังเคลื่อนที่อยู่ กระตุ้นเซลล์รับการทรงตัว",
     ("คอเคลียหยุดทำงาน", "เยื่อแก้วหูยังสั่นอยู่ กระตุ้นเซลล์ขนในคอเคลียที่ใช้ทรงตัว", "ท่อยูสเตเชียนปิด ความดันในหูชั้นกลางจึงสูงจนเสียการทรงตัว", "เลนส์ตาเปลี่ยนความโค้ง")),
)


@question_type(
    "biology.sense_organ_foundation",
    display_name={"th": "โครงสร้างและหน้าที่ของตา หู จมูก และลิ้น"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SENSE,
)
class SenseOrganFoundation(QuestionType):
    """Each part of each sense organ and what it does."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        part, organ, job = rng.choice(SENSE_PARTS)
        others = rng.sample([p for p in SENSE_PARTS if p[0] != part], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{part}ของ{organ}ทำหน้าที่อะไร", correct=job, wrongs=tuple(p[2] for p in others), topic=TOPIC_SENSE,
                             hint=SENSE_HINT)
        return _labelled(stem=f"ส่วนใด{job}", correct=part, wrongs=tuple(p[0] for p in others), topic=TOPIC_SENSE, hint=SENSE_HINT)


@question_type(
    "biology.sense_organ_fluency",
    display_name={"th": "ความผิดปกติของตาและหูและการแก้ไข"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SENSE,
)
class SenseOrganFluency(QuestionType):
    """Short and long sight, astigmatism, cataract, glaucoma, ear infection."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, what = rng.choice(DISORDERS)
        others = rng.sample([d for d in DISORDERS if d[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}เกิดจากอะไรและแก้ไขหรือเกิดผลอย่างไร", correct=what, wrongs=tuple(d[1] for d in others),
                             topic=TOPIC_SENSE, hint=SENSE_HINT)
        return _labelled(stem=f"\"{what}\" เป็นลักษณะของความผิดปกติใด", correct=name, wrongs=tuple(d[0] for d in others), topic=TOPIC_SENSE,
                         hint=SENSE_HINT)


@question_type(
    "biology.sense_organ_application",
    display_name={"th": "การดูแลอวัยวะรับความรู้สึกและอธิบายปรากฏการณ์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SENSE,
)
class SenseOrganApplication(QuestionType):
    """Care habits, and everyday effects explained."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            habit, why = rng.choice(CARE)
            others = rng.sample([c for c in CARE if c[0] != habit], 3)
            return _labelled(stem=f"\"{habit}\" ช่วยดูแลสุขภาพอย่างไร", correct=why, wrongs=tuple(c[1] for c in others), topic=TOPIC_SENSE,
                             hint=SENSE_HINT)
        stem, right, wrongs = rng.choice(SCENES)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_SENSE, hint=SENSE_HINT)
