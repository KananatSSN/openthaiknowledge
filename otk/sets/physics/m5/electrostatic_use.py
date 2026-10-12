"""การนำความรู้เรื่องไฟฟ้าสถิตไปใช้

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.5/6

Sets moved here from: science_wave_f11.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f11 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_STATIC = "การนำความรู้เรื่องไฟฟ้าสถิตไปใช้"


DEVICES = (
    ("เครื่องถ่ายเอกสาร", "ดรัมที่มีประจุดูดผงหมึกที่มีประจุตรงข้ามไปติดตามรูปภาพ แล้วถ่ายลงกระดาษ"),
    ("เครื่องกำจัดฝุ่นในปล่องควันโรงงาน", "ทำให้อนุภาคฝุ่นมีประจุ แล้วใช้แผ่นโลหะที่มีประจุตรงข้ามดูดฝุ่นไว้"),
    ("การพ่นสีรถยนต์แบบไฟฟ้าสถิต", "ละอองสีมีประจุ ถูกดูดไปเกาะชิ้นงานที่มีประจุตรงข้ามอย่างทั่วถึง"),
    ("สายล่อฟ้า", "ปลายแหลมของตัวนำต่อลงดิน ช่วยถ่ายเทประจุระหว่างเมฆกับพื้นดินอย่างปลอดภัย"),
    ("โซ่ลากพื้นท้ายรถบรรทุกน้ำมัน", "ถ่ายเทประจุที่สะสมจากการเสียดสีลงดิน ป้องกันประกายไฟ"),
    ("สายรัดข้อมือต่อลงดินของช่างซ่อมคอมพิวเตอร์", "ระบายประจุจากร่างกายลงดิน ไม่ให้ประกายไฟทำลายวงจร"),
    ("เครื่องพิมพ์เลเซอร์", "ใช้แสงเลเซอร์ลบประจุบนดรัมเป็นรูปภาพ แล้วดรัมดูดผงหมึกเฉพาะส่วนที่มีประจุ"),
)


EVENTS = (
    ("หลังเดินบนพรมแล้วจับลูกบิดประตูโลหะ รู้สึกเหมือนถูกไฟดูด",
     "ร่างกายสะสมประจุจากการเสียดสีกับพรม แล้วประจุถ่ายเทสู่ลูกบิดโลหะ"),
    ("หวีผมแล้วนำหวีเข้าใกล้เศษกระดาษ เศษกระดาษถูกดูดติดหวี",
     "หวีมีประจุจากการขัดสี แล้วเหนี่ยวนำให้เศษกระดาษด้านใกล้มีประจุตรงข้าม"),
    ("ถอดเสื้อไหมพรมในห้องมืดแล้วเห็นประกายไฟเล็ก ๆ",
     "เสื้อกับร่างกายเสียดสีจนมีประจุต่างกัน แล้วประจุกระโดดข้ามช่องว่าง"),
    ("ช่วงอากาศแห้งถูกไฟฟ้าสถิตช็อตบ่อยกว่าช่วงอากาศชื้น",
     "อากาศชื้นมีไอน้ำช่วยถ่ายเทประจุออกจากวัตถุ ประจุจึงสะสมได้น้อย"),
    ("ฟ้าผ่าลงยอดต้นไม้สูงกลางทุ่ง",
     "เมฆที่มีประจุเหนี่ยวนำพื้นดินให้มีประจุตรงข้าม แล้วประจุถ่ายเทผ่านอากาศมาทางจุดที่สูง"),
    ("ลูกโป่งที่ถูกับผมแล้วติดผนังได้",
     "ลูกโป่งมีประจุเหนี่ยวนำให้ผิวผนังด้านใกล้มีประจุตรงข้าม จึงดูดกัน"),
)


SAFETY = (
    ("ขณะเติมน้ำมันที่ปั๊ม ไม่ควรกลับเข้าไปนั่งในรถแล้วออกมาจับหัวจ่ายอีก เพราะเหตุใด",
     "การเสียดสีกับเบาะทำให้ร่างกายมีประจุ อาจเกิดประกายไฟจุดไอน้ำมันได้"),
    ("ระหว่างฝนฟ้าคะนองกลางทุ่งโล่ง ควรทำอย่างไร", "นั่งยอง ๆ ให้ตัวต่ำ ไม่ยืนใต้ต้นไม้สูงโดดเดี่ยว"),
    ("ช่างซ่อมคอมพิวเตอร์ควรทำอย่างไรก่อนจับแผงวงจร", "สวมสายรัดข้อมือต่อลงดินเพื่อระบายประจุจากร่างกาย"),
    ("อาคารสูงควรติดตั้งอุปกรณ์ใดเพื่อป้องกันฟ้าผ่า", "สายล่อฟ้าที่มีปลายแหลมและต่อสายลงดิน"),
    ("ห้องผ่าตัดที่มีแก๊สไวไฟควรควบคุมอย่างไร", "รักษาความชื้นในอากาศและใช้พื้นที่นำไฟฟ้าต่อลงดิน"),
    ("ก่อนถ่ายน้ำมันจากรถบรรทุกลงถังใต้ดิน ต้องทำอย่างไรก่อน", "ต่อสายดินระหว่างรถกับถัง ให้ประจุที่สะสมไหลลงดินก่อน"),
    ("โรงงานบดแป้งหรือผงไม้ต้องระวังไฟฟ้าสถิตเป็นพิเศษ เพราะเหตุใด", "ประกายไฟจากประจุสะสมอาจจุดฝุ่นผงที่ฟุ้งในอากาศให้ระเบิดได้"),
    ("เมื่ออยู่ในรถยนต์ขณะเกิดฟ้าผ่า ควรทำอย่างไร", "อยู่ในรถที่ปิดกระจก ไม่จับชิ้นส่วนโลหะ เพราะประจุไหลไปตามผิวนอกของตัวถัง"),
)


@question_type(
    "phys.electrostatic_use_foundation",
    display_name={"th": "หลักการทำงานของอุปกรณ์ที่ใช้ไฟฟ้าสถิต"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_STATIC,
)
class ElectrostaticUseFoundation(QuestionType):
    """Each device and the static trick it relies on."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = rng.sample(DEVICES, 4)
        device, how = chosen[0]
        hint = "อุปกรณ์เหล่านี้ใช้ประจุต่างชนิดดูดกัน หรือใช้ตัวนำต่อลงดินระบายประจุ"
        if rng.random() < 0.5:
            return _labelled(stem=f"{device}ทำงานโดยอาศัยหลักการใด", correct=how,
                             wrongs=tuple(h for _, h in chosen[1:]), topic=TOPIC_STATIC, hint=hint)
        return _labelled(stem=f"อุปกรณ์ใดทำงานโดย{how}", correct=device,
                         wrongs=tuple(d for d, _ in chosen[1:]), topic=TOPIC_STATIC, hint=hint)


@question_type(
    "phys.electrostatic_use_fluency",
    display_name={"th": "อธิบายปรากฏการณ์ไฟฟ้าสถิตในชีวิตประจำวัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_STATIC,
)
class ElectrostaticUseFluency(QuestionType):
    """An everyday spark or cling, and the charge story behind it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = rng.sample(EVENTS, 4)
        event, why = chosen[0]
        return _labelled(stem=f"{event} อธิบายได้ด้วยข้อใด", correct=why, wrongs=tuple(w for _, w in chosen[1:]),
                         topic=TOPIC_STATIC, hint="ถามตัวเองว่าประจุมาจากไหน (ขัดสีหรือเหนี่ยวนำ) และถ่ายเทไปทางใด")


@question_type(
    "phys.electrostatic_use_application",
    display_name={"th": "ความปลอดภัยจากไฟฟ้าสถิตและฟ้าผ่า"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_STATIC,
)
class ElectrostaticUseApplication(QuestionType):
    """Where static is a hazard, and what drains it away."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = rng.sample(SAFETY, 4)
        situation, action = chosen[0]
        return _labelled(stem=situation, correct=action, wrongs=tuple(a for _, a in chosen[1:]),
                         topic=TOPIC_STATIC, hint="ป้องกันอันตรายจากไฟฟ้าสถิตโดยไม่ให้ประจุสะสม หรือระบายประจุลงดินอย่างปลอดภัย")
