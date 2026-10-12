"""เอกโซไซโทซิสและเอนโดไซโทซิส

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 1 ม.4/15

Sets moved here from: science_wave_f47.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f47 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_BULK = "เอกโซไซโทซิสและเอนโดไซโทซิส"


BULK = (
    ("เอกโซไซโทซิส", "ถุงที่บรรจุสารรวมกับเยื่อหุ้มเซลล์แล้วปล่อยสารออกนอกเซลล์"),
    ("ฟาโกไซโทซิส", "เซลล์ยื่นเยื่อหุ้มล้อมอนุภาคขนาดใหญ่แล้วนำเข้าเซลล์เป็นถุง"),
    ("พิโนไซโทซิส", "เยื่อหุ้มเซลล์เว้าเข้านำของเหลวและสารละลายเข้าเซลล์เป็นถุงเล็ก"),
    ("การนำสารเข้าสู่เซลล์โดยอาศัยตัวรับ", "สารจับกับโปรตีนตัวรับที่เยื่อหุ้มเซลล์ก่อนถูกนำเข้าเซลล์เป็นถุง"),
)


BULK_EXAMPLES = (
    ("เซลล์ตับอ่อนหลั่งเอนไซม์และอินซูลิน", "เอกโซไซโทซิส"), ("เซลล์ประสาทหลั่งสารสื่อประสาท", "เอกโซไซโทซิส"),
    ("เซลล์พืชส่งสารสร้างผนังเซลล์ออกนอกเซลล์", "เอกโซไซโทซิส"),
    ("เซลล์เม็ดเลือดขาวกินแบคทีเรีย", "ฟาโกไซโทซิส"), ("อะมีบากินอาหาร", "ฟาโกไซโทซิส"),
    ("เซลล์บุผนังหลอดเลือดนำของเหลวจากเลือดเข้าเซลล์", "พิโนไซโทซิส"),
    ("เซลล์นำคอเลสเตอรอลใน LDL เข้าเซลล์", "การนำสารเข้าสู่เซลล์โดยอาศัยตัวรับ"),
    ("เซลล์ไข่นำโปรตีนไข่แดงที่จับกับตัวรับเข้าเซลล์", "การนำสารเข้าสู่เซลล์โดยอาศัยตัวรับ"),
)


@question_type(
    "biology.bulk_transport_foundation",
    display_name={"th": "ลักษณะของเอกโซไซโทซิสและเอนโดไซโทซิสแบบต่าง ๆ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_BULK,
)
class BulkTransportFoundation(QuestionType):
    """Out in vesicles, or in by eating, drinking, or through receptors."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, how = rng.choice(BULK)
        others = [b for b in BULK if b[0] != name]
        if rng.random() < 0.4:
            match = [e[0] for e in BULK_EXAMPLES if e[1] == name]
            rest = [e[0] for e in BULK_EXAMPLES if e[1] != name]
            return _labelled(stem=f"ข้อใดเป็นตัวอย่างของ{name}", correct=rng.choice(match), wrongs=tuple(rest),
                             topic=TOPIC_BULK, hint="ส่งสารออกคือเอกโซไซโทซิส กินอนุภาคใหญ่คือฟาโกไซโทซิส นำของเหลวเข้าคือพิโนไซโทซิส")
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}เกิดขึ้นอย่างไร", correct=how, wrongs=tuple(b[1] for b in others), topic=TOPIC_BULK,
                             hint="เอกโซไซโทซิสนำสารออก ฟาโกไซโทซิสกินอนุภาคใหญ่ พิโนไซโทซิสนำของเหลวเข้า และแบบอาศัยตัวรับจำเพาะสาร")
        return _labelled(stem=f"กระบวนการใดที่{how}", correct=name, wrongs=tuple(b[0] for b in others), topic=TOPIC_BULK,
                         hint="เอกโซไซโทซิสนำสารออก ฟาโกไซโทซิสกินอนุภาคใหญ่ พิโนไซโทซิสนำของเหลวเข้า และแบบอาศัยตัวรับจำเพาะสาร")


@question_type(
    "biology.bulk_transport_fluency",
    display_name={"th": "ระบุการลำเลียงสารโมเลกุลใหญ่จากตัวอย่าง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_BULK,
)
class BulkTransportFluency(QuestionType):
    """Name the process behind a cell's action."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        case, right = rng.choice(BULK_EXAMPLES)
        if rng.random() < 0.5:
            outward = right == "เอกโซไซโทซิส"
            match = [e[0] for e in BULK_EXAMPLES if (e[1] == "เอกโซไซโทซิส") == outward]
            rest = [e[0] for e in BULK_EXAMPLES if (e[1] == "เอกโซไซโทซิส") != outward]
            return _labelled(stem=f"ข้อใดเป็นการลำเลียงสารโมเลกุลใหญ่{'ออกนอกเซลล์' if outward else 'เข้าสู่เซลล์'}",
                             correct=rng.choice(match), wrongs=tuple(rest), topic=TOPIC_BULK,
                             hint="เอกโซไซโทซิสส่งสารออก เอนโดไซโทซิสทุกแบบนำสารเข้า")
        return _labelled(stem=f"\"{case}\" เป็นการลำเลียงสารแบบใด", correct=right,
                         wrongs=tuple(b[0] for b in BULK if b[0] != right), topic=TOPIC_BULK,
                         hint="ส่งสารออกนอกเซลล์คือเอกโซไซโทซิส นำเข้าเซลล์คือเอนโดไซโทซิสแบบต่าง ๆ")


@question_type(
    "biology.bulk_transport_application",
    display_name={"th": "ลำดับขั้นและพลังงานในการลำเลียงสารโมเลกุลใหญ่"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_BULK,
)
class BulkTransportApplication(QuestionType):
    """Vesicles, the Golgi route out, and the energy it all takes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        facts = (
            ("เส้นทางของโปรตีนที่เซลล์สร้างเพื่อหลั่งออกนอกเซลล์คือข้อใด",
             "ไรโบโซมบน ER ผิวขรุขระ → กอลจิคอมเพล็กซ์ → ถุงลำเลียง → เยื่อหุ้มเซลล์",
             ("นิวเคลียส → ไลโซโซม → ถุงลำเลียง → เยื่อหุ้มเซลล์", "ไมโทคอนเดรีย → กอลจิคอมเพล็กซ์ → ถุงลำเลียง → นิวเคลียส",
              "เยื่อหุ้มเซลล์ → ER ผิวเรียบ → กอลจิคอมเพล็กซ์ → นิวเคลียส",
              "ไรโบโซมอิสระในไซโทซอล → ไลโซโซม → ถุงลำเลียง → เยื่อหุ้มเซลล์")),
            ("การลำเลียงสารแบบเอกโซไซโทซิสและเอนโดไซโทซิสต้องใช้พลังงานหรือไม่", "ใช้พลังงานจาก ATP",
             ("ไม่ใช้พลังงานเลย", "ใช้พลังงานแสงโดยตรง", "ใช้เฉพาะเอนโดไซโทซิส", "ใช้พลังงานจากการแพร่")),
            ("เพราะเหตุใดโปรตีนและแบคทีเรียจึงเข้าเซลล์ด้วยการแพร่ไม่ได้", "มีขนาดใหญ่เกินกว่าจะผ่านชั้นฟอสโฟลิพิดหรือโปรตีนตัวพา",
             ("มีขนาดเล็กเกินไปจนหลุดผ่านช่องของโปรตีนตัวพาออกไป", "ไม่มีความเข้มข้นต่างกันระหว่างภายในและภายนอกเซลล์",
              "ละลายในลิพิดได้ดีเกินไปจนติดค้างอยู่ในชั้นฟอสโฟลิพิด", "มีประจุมากเกินไปจนเยื่อหุ้มเซลล์ผลักออก")),
            ("หลังฟาโกไซโทซิส ถุงอาหารในเซลล์เม็ดเลือดขาวจะรวมกับออร์แกเนลล์ใดเพื่อย่อยเชื้อโรค", "ไลโซโซม",
             ("ไรโบโซม", "คลอโรพลาสต์", "นิวคลีโอลัส", "แวคิวโอล")),
            ("เมื่อเซลล์ทำเอกโซไซโทซิสบ่อย ๆ พื้นที่เยื่อหุ้มเซลล์เป็นอย่างไร", "เพิ่มขึ้น เพราะเยื่อของถุงรวมเข้ากับเยื่อหุ้มเซลล์",
             ("ลดลง เพราะเยื่อหุ้มเซลล์ถูกใช้สร้างถุงลำเลียง", "ไม่เปลี่ยนแปลง เพราะถุงไม่ได้รวมกับเยื่อหุ้มเซลล์",
              "หายไปทั้งหมดเพราะเซลล์ปล่อยเยื่อออกไปพร้อมสาร", "เพิ่มขึ้น เพราะเซลล์สร้างผนังเซลล์ใหม่ขึ้นมาแทน")),
        )
        stem, right, wrongs = rng.choice(facts)
        # The row's own wrong readings only: another row's answer is off topic here.
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_BULK,
                         hint="สารโมเลกุลใหญ่เคลื่อนที่ในถุงเยื่อ ต้องใช้พลังงาน และมักผ่านกอลจิหรือไปรวมกับไลโซโซม")
