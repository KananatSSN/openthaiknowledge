"""เซนเซอร์ ตัวควบคุม และอุปกรณ์ขับเคลื่อน

การออกแบบและเทคโนโลยี · ม.4 · สสวท. พื้นฐาน
Indicators: ว 4.1 ม.4/5

Sets moved here from: technology_t2s4.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1 import SUBJECT
from otk.sets._support.technology_t2s3 import _bank, _pair_either_way
from otk.sets._support.technology_t2s4 import M4

PROVENANCE = Provenance("original")


SYSTEM_TOPIC = "เซนเซอร์ ตัวควบคุม และอุปกรณ์ขับเคลื่อน"


SENSORS = (
    ("เซนเซอร์อัลตราโซนิก", "ระยะห่างจากวัตถุ"),
    ("เซนเซอร์ตรวจจับความเคลื่อนไหวแบบอินฟราเรด (PIR)", "การเคลื่อนไหวของคนหรือสัตว์"),
    ("เซนเซอร์วัดความชื้นในดิน", "ปริมาณความชื้นในดิน"),
    ("ตัวต้านทานไวแสง (LDR)", "ความเข้มของแสง"),
    ("เซนเซอร์วัดอุณหภูมิ", "ความร้อนหรือความเย็นของสิ่งแวดล้อม"),
    ("เซนเซอร์วัดความเร่งและการเอียง", "การเอียงหรือการสั่นของอุปกรณ์"),
)


INPUT, CONTROL, OUTPUT, POWER = ("อุปกรณ์รับเข้า (อินพุต)", "ตัวควบคุม",
                                 "อุปกรณ์ส่งออกหรือขับเคลื่อน (เอาต์พุต)", "แหล่งจ่ายพลังงาน")


ROLES = (INPUT, CONTROL, OUTPUT, POWER)


SYSTEM_PARTS = (
    ("เซนเซอร์อัลตราโซนิก", INPUT), ("ปุ่มกด", INPUT), ("เซนเซอร์วัดความชื้นในดิน", INPUT),
    ("บอร์ดไมโครคอนโทรลเลอร์", CONTROL),
    ("มอเตอร์เซอร์โว", OUTPUT), ("ปั๊มน้ำขนาดเล็ก", OUTPUT), ("จอแสดงผลแอลซีดี", OUTPUT), ("ลำโพง", OUTPUT),
    ("แบตเตอรี่", POWER), ("แผงเซลล์สุริยะ", POWER),
)


AUTOMATIONS = (
    ("ระบบรดน้ำที่ทำงานเมื่อดินแห้ง", "เซนเซอร์วัดความชื้นในดิน → ปั๊มน้ำ",
     ("เซนเซอร์อัลตราโซนิก → ลำโพง", "ตัวต้านทานไวแสง → มอเตอร์เซอร์โว", "ปุ่มกด → จอแสดงผลแอลซีดี",
      "เซนเซอร์วัดอุณหภูมิ → ลำโพง", "เซนเซอร์ตรวจจับความเคลื่อนไหว → ปั๊มน้ำ")),
    ("ถังขยะที่เปิดฝาเองเมื่อมีมือยื่นเข้าใกล้", "เซนเซอร์อัลตราโซนิก → มอเตอร์เซอร์โว",
     ("เซนเซอร์วัดความชื้นในดิน → ลำโพง", "ตัวต้านทานไวแสง → ปั๊มน้ำ", "เซนเซอร์วัดอุณหภูมิ → จอแสดงผลแอลซีดี",
      "ปุ่มกด → ปั๊มน้ำ", "เซนเซอร์วัดความเร่ง → ปั๊มน้ำ")),
    ("ไฟทางเดินที่เปิดเมื่อมีคนเดินผ่านในเวลากลางคืน", "เซนเซอร์ตรวจจับความเคลื่อนไหวและตัวต้านทานไวแสง → หลอดไฟ LED",
     ("เซนเซอร์วัดความชื้นในดิน → หลอดไฟ LED", "เซนเซอร์วัดอุณหภูมิ → ปั๊มน้ำ", "ปุ่มกด → มอเตอร์เซอร์โว",
      "เซนเซอร์อัลตราโซนิก → ปั๊มน้ำ", "เซนเซอร์วัดความเร่ง → ลำโพง")),
    ("พัดลมที่เปิดเองเมื่อห้องร้อน", "เซนเซอร์วัดอุณหภูมิ → มอเตอร์ของพัดลม",
     ("ตัวต้านทานไวแสง → ปั๊มน้ำ", "เซนเซอร์วัดความชื้นในดิน → มอเตอร์ของพัดลม", "ปุ่มกด → ลำโพง",
      "เซนเซอร์อัลตราโซนิก → จอแสดงผลแอลซีดี", "เซนเซอร์วัดความเร่ง → ปั๊มน้ำ")),
    ("เซนเซอร์ถอยหลังรถที่ส่งเสียงเตือนเมื่อใกล้สิ่งกีดขวาง", "เซนเซอร์อัลตราโซนิก → ลำโพงหรือออด",
     ("เซนเซอร์วัดความชื้นในดิน → ลำโพง", "ตัวต้านทานไวแสง → ปั๊มน้ำ", "เซนเซอร์วัดอุณหภูมิ → มอเตอร์เซอร์โว",
      "ปุ่มกด → ปั๊มน้ำ", "แผงเซลล์สุริยะ → จอแสดงผลแอลซีดี")),
    ("อุปกรณ์แจ้งเตือนเมื่อผู้สูงอายุหกล้ม", "เซนเซอร์วัดความเร่งและการเอียง → ส่งข้อความแจ้งเตือนไปยังโทรศัพท์ของผู้ดูแล",
     ("เซนเซอร์วัดความชื้นในดิน → ปั๊มน้ำ", "ตัวต้านทานไวแสง → หลอดไฟ LED", "เซนเซอร์วัดอุณหภูมิ → พัดลม",
      "ปุ่มกด → มอเตอร์เซอร์โว", "เซนเซอร์อัลตราโซนิก → ปั๊มน้ำ")),
)


@question_type(
    "tech.control_system_foundation",
    display_name={"th": "บอกสิ่งที่เซนเซอร์แต่ละชนิดตรวจวัด"},
    level=M4, subject=SUBJECT, topic=SYSTEM_TOPIC,
)
class ControlSystemFoundation(QuestionType):
    def build(self, rng: Random, **params):
        return _pair_either_way(rng, SENSORS,
                                forward="{}ตรวจวัดสิ่งใด",
                                backward="ถ้าต้องการตรวจวัด{} ควรใช้เซนเซอร์ใด",
                                hint="เซนเซอร์เปลี่ยนสิ่งที่ตรวจวัด เช่น ระยะ แสง ความชื้น หรือการเคลื่อนไหว ให้เป็นสัญญาณไฟฟ้า",
                                topic=SYSTEM_TOPIC)


@question_type(
    "tech.control_system_fluency",
    display_name={"th": "จำแนกองค์ประกอบของระบบควบคุมอัตโนมัติ"},
    level=M4, subject=SUBJECT, topic=SYSTEM_TOPIC,
)
class ControlSystemFluency(QuestionType):
    def build(self, rng: Random, **params):
        part, role = rng.choice(SYSTEM_PARTS)
        hint = ("อินพุตรับรู้สิ่งแวดล้อมหรือคำสั่ง ตัวควบคุมประมวลผลและตัดสินใจ "
                "เอาต์พุตทำงานออกมา และแหล่งจ่ายพลังงานให้ไฟฟ้าแก่ทั้งระบบ")
        if rng.random() < 0.5:
            return _labelled(stem=f"ในระบบควบคุมอัตโนมัติ {part}ทำหน้าที่เป็นองค์ประกอบใด",
                             correct=role, wrongs=tuple(r for r in ROLES if r != role), hint=hint, topic=SYSTEM_TOPIC)
        others = [p for p, r in SYSTEM_PARTS if r != role]
        return _labelled(stem=f"ข้อใดทำหน้าที่เป็น{role}ในระบบควบคุมอัตโนมัติ",
                         correct=part, wrongs=tuple(others), hint=hint, topic=SYSTEM_TOPIC)


@question_type(
    "tech.control_system_application",
    display_name={"th": "ออกแบบระบบอัตโนมัติด้วยเซนเซอร์และอุปกรณ์ขับเคลื่อน"},
    level=M4, subject=SUBJECT, topic=SYSTEM_TOPIC,
)
class ControlSystemApplication(QuestionType):
    def build(self, rng: Random, **params):
        return _bank(rng, AUTOMATIONS, "ต้องการสร้าง{} ควรใช้เซนเซอร์และอุปกรณ์ขับเคลื่อนคู่ใด โดยมีไมโครคอนโทรลเลอร์เป็นตัวควบคุม",
                     hint="เลือกเซนเซอร์ที่ตรวจสิ่งที่เป็นเงื่อนไขของงาน และอุปกรณ์ขับเคลื่อนที่ให้ผลที่ต้องการ",
                     topic=SYSTEM_TOPIC)
