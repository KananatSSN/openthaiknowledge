"""ประวัติและพัฒนาการของความรู้ทางฟิสิกส์

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/1

Sets moved here from: science_wave_f6.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f6 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_HISTORY = "ประวัติและพัฒนาการของความรู้ทางฟิสิกส์"


SCIENTISTS = (
    ("กาลิเลโอ กาลิเลอี", "ทดลองการเคลื่อนที่ของวัตถุบนพื้นเอียงและการตก แสดงว่าวัตถุตกด้วยความเร่งเท่ากัน"),
    ("ไอแซก นิวตัน", "เสนอกฎการเคลื่อนที่สามข้อและกฎความโน้มถ่วงสากล"),
    ("โยฮันเนส เคปเลอร์", "เสนอกฎการเคลื่อนที่ของดาวเคราะห์ที่โคจรเป็นวงรีรอบดวงอาทิตย์"),
    ("อาร์คิมีดีส", "อธิบายแรงลอยตัวของวัตถุในของเหลว"),
    ("ไมเคิล ฟาราเดย์", "ค้นพบการเหนี่ยวนำแม่เหล็กไฟฟ้า"),
    ("เจมส์ เคลิร์ก แมกซ์เวลล์", "สร้างทฤษฎีคลื่นแม่เหล็กไฟฟ้าและทำนายว่าแสงเป็นคลื่นแม่เหล็กไฟฟ้า"),
    ("ไฮน์ริช เฮิรตซ์", "ทดลองสร้างและตรวจจับคลื่นแม่เหล็กไฟฟ้าได้เป็นคนแรก"),
    ("อัลเบิร์ต ไอน์สไตน์", "เสนอทฤษฎีสัมพัทธภาพและอธิบายปรากฏการณ์โฟโตอิเล็กทริก"),
    ("เออร์เนสต์ รัทเทอร์ฟอร์ด", "ยิงอนุภาคแอลฟาผ่านแผ่นทองคำบางแล้วเสนอว่าอะตอมมีนิวเคลียส"),
    ("มารี กูรี", "ค้นพบธาตุกัมมันตรังสีพอโลเนียมและเรเดียม"),
    ("เจ. เจ. ทอมสัน", "ค้นพบอิเล็กตรอนจากการทดลองหลอดรังสีแคโทด"),
    ("วิลเฮล์ม เรินต์เกน", "ค้นพบรังสีเอกซ์"),
    ("เบลส ปาสกาล", "เสนอหลักว่าความดันที่เพิ่มให้ของเหลวในภาชนะปิดส่งผ่านไปทุกจุดเท่ากัน"),
    ("เจมส์ จูล", "ทดลองแสดงว่างานเปลี่ยนเป็นความร้อนได้ในอัตราส่วนคงตัว"),
    ("โรเบิร์ต ฮุก", "พบว่าแรงที่ดึงสปริงแปรผันตรงกับระยะที่สปริงยืด"),
)


TECHNOLOGY = (
    ("เครื่องกำเนิดไฟฟ้าและหม้อแปลงไฟฟ้า", "การเหนี่ยวนำแม่เหล็กไฟฟ้า"),
    ("วิทยุ โทรทัศน์ และโทรศัพท์เคลื่อนที่", "คลื่นแม่เหล็กไฟฟ้า"),
    ("เซลล์สุริยะ", "ปรากฏการณ์โฟโตอิเล็กทริก"),
    ("การส่งดาวเทียมขึ้นสู่วงโคจร", "กฎการเคลื่อนที่และกฎความโน้มถ่วงสากลของนิวตัน"),
    ("โรงไฟฟ้านิวเคลียร์", "ปฏิกิริยานิวเคลียร์ฟิชชัน"),
    ("การถ่ายภาพกระดูกในโรงพยาบาล", "รังสีเอกซ์"),
    ("ลิฟต์ยกรถในอู่ซ่อมรถและเบรกรถยนต์แบบไฮดรอลิก", "หลักของปาสกาล"),
    ("เรือและเรือดำน้ำ", "แรงลอยตัวตามหลักของอาร์คิมีดีส"),
    ("การแก้เวลาของนาฬิกาบนดาวเทียมระบบ GPS", "ทฤษฎีสัมพัทธภาพ"),
    ("ตาชั่งสปริง", "กฎของฮุก"),
)


PROCESS_FACTS = (
    ("กาลิเลโอหักล้างแนวคิดของอริสโตเติลที่ว่าวัตถุหนักตกเร็วกว่าวัตถุเบาได้อย่างไร",
     "ใช้การทดลองและการวัดมาตรวจสอบแนวคิด",
     ("ใช้การโต้แย้งด้วยเหตุผลเพียงอย่างเดียว", "อ้างอิงคำสอนของนักปราชญ์รุ่นก่อน", "ใช้การทายผลโดยไม่ทดลอง")),
    ("ข้อใดกล่าวถึงความรู้ทางฟิสิกส์ได้ถูกต้อง", "ความรู้อาจเปลี่ยนแปลงหรือขยายได้เมื่อมีหลักฐานใหม่",
     ("ความรู้ที่ได้แล้วไม่มีวันเปลี่ยนแปลง", "ความรู้ได้จากความเชื่อของนักวิทยาศาสตร์คนเดียว", "ความรู้ไม่ต้องตรวจสอบซ้ำ")),
    ("กฎของนิวตันยังใช้ได้ดีหลังมีทฤษฎีสัมพัทธภาพ ในกรณีใด", "วัตถุเคลื่อนที่ด้วยอัตราเร็วน้อยกว่าอัตราเร็วแสงมาก",
     ("วัตถุเคลื่อนที่ใกล้อัตราเร็วแสง", "อนุภาคที่เล็กกว่าอะตอมเท่านั้น", "ไม่มีกรณีใดใช้ได้อีก")),
    ("ฟิสิกส์เป็นวิทยาศาสตร์ที่ศึกษาเรื่องใด", "สสาร พลังงาน และอันตรกิริยาระหว่างสสารกับพลังงาน",
     ("องค์ประกอบของสิ่งมีชีวิตเท่านั้น", "สมบัติและการเปลี่ยนแปลงของสารเคมีเท่านั้น", "ประวัติของโลกและหิน")),
)


@question_type(
    "phys.physics_history_foundation",
    display_name={"th": "นักฟิสิกส์และผลงานที่สำคัญ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_HISTORY,
)
class PhysicsHistoryFoundation(QuestionType):
    """Which physicist did what."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = rng.sample(SCIENTISTS, 4)
        name, work = chosen[0]
        return _labelled(stem=f"นักวิทยาศาสตร์คนใด{work}", correct=name,
                         wrongs=tuple(n for n, _ in chosen[1:]), topic=TOPIC_HISTORY,
                         hint="จับคู่นักวิทยาศาสตร์กับการค้นพบ: ใครทดลองหรือเสนอแนวคิดนั้นเป็นคนแรก")


@question_type(
    "phys.physics_history_fluency",
    display_name={"th": "ผลงานของนักฟิสิกส์กับการพัฒนาแนวคิดทางฟิสิกส์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_HISTORY,
)
class PhysicsHistoryFluency(QuestionType):
    """A physicist's work, and how physics checks and grows its ideas."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            stem, correct, wrongs = rng.choice(PROCESS_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_HISTORY,
                             hint="ความรู้ทางฟิสิกส์ได้จากการสังเกต ทดลอง และตรวจสอบซ้ำ และปรับเปลี่ยนได้เมื่อมีหลักฐานใหม่")
        chosen = rng.sample(SCIENTISTS, 4)
        name, work = chosen[0]
        return _labelled(stem=f"ผลงานที่สำคัญของ{name}คือข้อใด", correct=work,
                         wrongs=tuple(w for _, w in chosen[1:]), topic=TOPIC_HISTORY,
                         hint="นึกถึงการทดลองหรือกฎที่ตั้งชื่อตามนักวิทยาศาสตร์คนนั้น")


@question_type(
    "phys.physics_history_application",
    display_name={"th": "ความรู้ทางฟิสิกส์ที่นำไปสู่การพัฒนาเทคโนโลยี"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_HISTORY,
)
class PhysicsHistoryApplication(QuestionType):
    """Which piece of physics a technology grew out of, either way round."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = rng.sample(TECHNOLOGY, 4)
        tech, idea = chosen[0]
        hint = "เทคโนโลยีพัฒนาจากความรู้ทางฟิสิกส์ ให้คิดว่าเครื่องมือนั้นทำงานด้วยหลักการใด"
        if rng.random() < 0.5:
            joint = " " if tech[-1].isascii() else ""
            return _labelled(stem=f"{tech}{joint}พัฒนาขึ้นจากความรู้ทางฟิสิกส์เรื่องใด", correct=idea,
                             wrongs=tuple(i for _, i in chosen[1:]), topic=TOPIC_HISTORY, hint=hint)
        return _labelled(stem=f"เทคโนโลยีใดพัฒนาขึ้นจากความรู้เรื่อง{idea}", correct=tech,
                         wrongs=tuple(t for t, _ in chosen[1:]), topic=TOPIC_HISTORY, hint=hint)
