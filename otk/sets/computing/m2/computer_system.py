"""ระบบคอมพิวเตอร์และเทคโนโลยีการสื่อสาร

วิทยาการคำนวณ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 4.2 ม.2/3

Sets moved here from: technology_t1s7.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t1s4 import _near
from otk.sets._support.technology_t1s7 import M2

PROVENANCE = Provenance("original")


SYSTEM_TOPIC = "ระบบคอมพิวเตอร์และเทคโนโลยีการสื่อสาร"


INPUT, CPU, MAIN, SECONDARY, OUTPUT = (
    "หน่วยรับเข้า", "หน่วยประมวลผลกลาง", "หน่วยความจำหลัก", "หน่วยความจำรอง", "หน่วยส่งออก")


UNITS = (INPUT, CPU, MAIN, SECONDARY, OUTPUT)


DEVICES = (
    ("แป้นพิมพ์", INPUT), ("เมาส์", INPUT), ("ไมโครโฟน", INPUT), ("สแกนเนอร์", INPUT),
    ("ซีพียู", CPU),
    ("แรม (RAM)", MAIN),
    ("ฮาร์ดดิสก์", SECONDARY), ("เอสเอสดี (SSD)", SECONDARY), ("แฟลชไดรฟ์", SECONDARY),
    ("จอภาพ", OUTPUT), ("ลำโพง", OUTPUT), ("เครื่องพิมพ์", OUTPUT),
)


UNITS_HINT = ("หน่วยรับเข้ารับข้อมูลจากผู้ใช้ หน่วยประมวลผลกลางคำนวณและควบคุม หน่วยความจำหลัก เช่น แรม "
              "เก็บข้อมูลที่กำลังใช้งาน หน่วยความจำรองเก็บข้อมูลไว้ใช้ภายหลังแม้ปิดเครื่อง หน่วยส่งออกแสดงผล")


SENDER, RECEIVER, MESSAGE, MEDIUM, PROTOCOL = (
    "ผู้ส่ง", "ผู้รับ", "ข้อมูลหรือข่าวสาร", "สื่อกลาง", "โพรโทคอล")


PARTS = (SENDER, RECEIVER, MESSAGE, MEDIUM, PROTOCOL)


LINKS = (
    ("แพรส่งข้อความผ่านแอปแชตจากโทรศัพท์ของตนถึงโทรศัพท์ของต้น ผ่านเครือข่าย Wi-Fi",
     {SENDER: "โทรศัพท์ของแพร", RECEIVER: "โทรศัพท์ของต้น", MESSAGE: "ข้อความที่แพรพิมพ์",
      MEDIUM: "คลื่นสัญญาณ Wi-Fi", PROTOCOL: "ข้อตกลงรูปแบบการรับส่งข้อมูลที่แอปแชตทั้งสองเครื่องใช้ร่วมกัน"}),
    ("ครูสั่งพิมพ์เอกสารจากคอมพิวเตอร์ไปยังเครื่องพิมพ์ ผ่านสาย USB",
     {SENDER: "คอมพิวเตอร์ของครู", RECEIVER: "เครื่องพิมพ์", MESSAGE: "ไฟล์เอกสารที่สั่งพิมพ์",
      MEDIUM: "สาย USB", PROTOCOL: "มาตรฐาน USB ที่กำหนดวิธีรับส่งข้อมูลระหว่างสองอุปกรณ์"}),
    ("สถานีโทรทัศน์ส่งภาพข่าวไปยังโทรทัศน์ที่บ้าน ผ่านดาวเทียม",
     {SENDER: "สถานีโทรทัศน์", RECEIVER: "โทรทัศน์ที่บ้าน", MESSAGE: "ภาพและเสียงของข่าว",
      MEDIUM: "คลื่นไมโครเวฟที่ส่งผ่านดาวเทียม",
      PROTOCOL: "มาตรฐานการออกอากาศที่สถานีและเครื่องรับใช้ร่วมกัน"}),
    ("บอยส่งอีเมลแนบรูปภาพจากคอมพิวเตอร์ที่บ้านถึงครู ผ่านอินเทอร์เน็ตบ้านที่ใช้สายใยแก้วนำแสง",
     {SENDER: "คอมพิวเตอร์ของบอย", RECEIVER: "คอมพิวเตอร์ที่ครูใช้เปิดอ่านอีเมล",
      MESSAGE: "อีเมลและรูปภาพที่แนบ", MEDIUM: "สายใยแก้วนำแสง",
      PROTOCOL: "โพรโทคอลอีเมลที่กำหนดวิธีส่งและรับอีเมล"}),
)


@question_type(
    "comp.computer_system_foundation",
    display_name={"th": "ระบุองค์ประกอบของระบบคอมพิวเตอร์"},
    level=M2, subject=SUBJECT, topic=SYSTEM_TOPIC,
)
class ComputerSystemFoundation(QuestionType):
    def build(self, rng: Random, **params):
        device, unit = rng.choice(DEVICES)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"{device}จัดเป็นองค์ประกอบใดของคอมพิวเตอร์",
                correct=unit, wrongs=tuple([u for u in UNITS if u != unit]),
                hint=UNITS_HINT, topic=SYSTEM_TOPIC,
            )
        others = [d for d, u in DEVICES if u != unit]
        return _labelled(
            stem=f"ข้อใดจัดเป็น{unit}ของคอมพิวเตอร์",
            correct=device, wrongs=tuple(others),
            hint=UNITS_HINT, topic=SYSTEM_TOPIC,
        )


@question_type(
    "comp.computer_system_fluency",
    display_name={"th": "คำนวณขนาดข้อมูลและเวลาในการส่งข้อมูล"},
    level=M2, subject=SUBJECT, topic=SYSTEM_TOPIC,
)
class ComputerSystemFluency(QuestionType):
    """Bytes to bits, and how long a file takes at a stated speed."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params):
        if rng.random() < 0.4:
            size = rng.randint(3, 60)
            answer = size * 8
            return _labelled(
                stem=f"ไฟล์ขนาด {size} เมกะไบต์ มีขนาดเท่ากับกี่เมกะบิต (1 ไบต์ = 8 บิต)",
                correct=f"{answer} เมกะบิต",
                wrongs=tuple(f"{w} เมกะบิต" for w in rng.sample(
                    _near(answer, (size, size * 1024, size + 8, size * 10)), 3)),
                hint="1 ไบต์มี 8 บิต จึงนำจำนวนเมกะไบต์คูณด้วย 8",
                topic=SYSTEM_TOPIC,
            )
        speed = rng.choice((4, 8, 10, 16, 20, 40, 50, 100))
        seconds = rng.randint(2, 30)
        size = speed * seconds // 8
        while size * 8 != speed * seconds or size == 0:
            seconds += 1
            size = speed * seconds // 8
        return _labelled(
            stem=(f"ส่งไฟล์ขนาด {size} เมกะไบต์ ผ่านเครือข่ายความเร็ว {speed} เมกะบิตต่อวินาที "
                  f"ถ้าส่งได้เต็มความเร็วตลอดเวลา จะใช้เวลากี่วินาที"),
            correct=f"{seconds} วินาที",
            wrongs=tuple(f"{w} วินาที" for w in rng.sample(
                _near(seconds, (size // speed if size >= speed else seconds * 8,
                                seconds * 8, seconds // 2 if seconds > 1 else seconds + 2)), 3)),
            hint="ความเร็วบอกเป็นบิตต่อวินาที จึงแปลงขนาดไฟล์เป็นเมกะบิตก่อน (คูณ 8) แล้วหารด้วยความเร็ว",
            topic=SYSTEM_TOPIC,
        )


@question_type(
    "comp.computer_system_application",
    display_name={"th": "วิเคราะห์องค์ประกอบของการสื่อสารข้อมูล"},
    level=M2, subject=SUBJECT, topic=SYSTEM_TOPIC,
)
class ComputerSystemApplication(QuestionType):
    def build(self, rng: Random, **params):
        story, parts = rng.choice(LINKS)
        part = rng.choice(PARTS)
        hint = ("การสื่อสารข้อมูลมีห้าองค์ประกอบ ผู้ส่ง ผู้รับ ข้อมูลหรือข่าวสาร สื่อกลางที่ข้อมูลเดินทางผ่าน "
                "และโพรโทคอลซึ่งเป็นข้อตกลงที่ทำให้ผู้ส่งและผู้รับเข้าใจกัน")
        if rng.random() < 0.5:
            return _labelled(
                stem=f"{story} “{parts[part]}” เป็นองค์ประกอบใดของการสื่อสารข้อมูล",
                correct=part, wrongs=tuple([p for p in PARTS if p != part]),
                hint=hint, topic=SYSTEM_TOPIC,
            )
        return _labelled(
            stem=f"{story} ข้อใดเป็น{part}ของการสื่อสารครั้งนี้",
            correct=parts[part], wrongs=tuple([t for p, t in parts.items() if p != part]),
            hint=hint, topic=SYSTEM_TOPIC,
        )
