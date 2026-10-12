"""การนำความรู้เกี่ยวกับเสียงไปใช้ประโยชน์ในชีวิตประจำวัน

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.5/8

Sets moved here from: science_wave_e15.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e15 import SUBJECT, UPPER_FIVE, _labelled, _numeric

PROVENANCE = Provenance("original")


TOPIC_SOUND_USE = "การนำความรู้เกี่ยวกับเสียงไปใช้ประโยชน์ในชีวิตประจำวัน"


REFLECTION, DOPPLER, SUPERPOSITION, ULTRASOUND_ENERGY, ABSORPTION, RESONANCE = (
    "การสะท้อนของเสียง", "ปรากฏการณ์ดอปเพลอร์", "การรวมคลื่นเสียง (การแทรกสอด)",
    "พลังงานของคลื่นเหนือเสียง", "การดูดกลืนเสียงของวัสดุ", "การสั่นพ้องของเสียง")


PRINCIPLES = (REFLECTION, DOPPLER, SUPERPOSITION, ULTRASOUND_ENERGY, ABSORPTION, RESONANCE)


SOUND_USES = (
    ("การตรวจดูทารกในครรภ์ด้วยเครื่องอัลตราซาวนด์", REFLECTION),
    ("โซนาร์วัดความลึกของทะเลและหาฝูงปลา", REFLECTION),
    ("การตรวจหารอยร้าวภายในชิ้นโลหะด้วยคลื่นเหนือเสียง", REFLECTION),
    ("เซนเซอร์ถอยจอดรถที่ส่งเสียงเตือนเมื่อใกล้สิ่งกีดขวาง", REFLECTION),
    ("การตรวจวัดความเร็วของเลือดที่ไหลในหลอดเลือดด้วยคลื่นเหนือเสียง", DOPPLER),
    ("การวัดความเร็วของลูกเบสบอลหรือรถด้วยการเปลี่ยนความถี่ของคลื่นที่สะท้อนกลับ", DOPPLER),
    ("หูฟังตัดเสียงรบกวนแบบแอกทีฟ", SUPERPOSITION),
    ("การตั้งเสียงเครื่องดนตรีโดยฟังเสียงบีตเทียบกับส้อมเสียง", SUPERPOSITION),
    ("เครื่องล้างแว่นตาและเครื่องประดับด้วยคลื่นเหนือเสียง", ULTRASOUND_ENERGY),
    ("การสลายนิ่วในไตด้วยคลื่นเสียงพลังงานสูง", ULTRASOUND_ENERGY),
    ("การบุผนังห้องบันทึกเสียงด้วยแผ่นฟองน้ำ", ABSORPTION),
    ("การติดตั้งกำแพงกันเสียงริมทางด่วน", ABSORPTION),
    ("กล่องเสียงกลวงของกีตาร์และไวโอลินที่ทำให้เสียงดังขึ้น", RESONANCE),
    ("การเป่าขลุ่ยโดยปิดเปิดรูเพื่อเปลี่ยนความยาวลำอากาศ", RESONANCE),
)


@question_type(
    "phys.sound_use_foundation",
    display_name={"th": "หลักการของเสียงที่อยู่เบื้องหลังเทคโนโลยี"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SOUND_USE,
)
class SoundUseFoundation(QuestionType):
    """Name the principle a use of sound relies on."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        use, principle = rng.choice(SOUND_USES)
        return _labelled(
            stem=f"\"{use}\" อาศัยความรู้เรื่องใดของเสียงเป็นหลัก",
            correct=principle,
            wrongs=tuple([p for p in PRINCIPLES if p != principle]),
            topic=TOPIC_SOUND_USE,
            hint="ถามว่าเทคโนโลยีนี้ฟังเสียงที่ย้อนกลับมา วัดความถี่ที่เปลี่ยน ใช้เสียงหักล้างกัน ใช้พลังงานของเสียง ดูดกลืนเสียง หรือทำให้เสียงดังขึ้น")


@question_type(
    "phys.sound_use_fluency",
    display_name={"th": "ยกตัวอย่างการนำความรู้เกี่ยวกับเสียงไปใช้ประโยชน์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SOUND_USE,
)
class SoundUseFluency(QuestionType):
    """The indicator's ยกตัวอย่าง: pick the use that rests on a named principle."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        principle = rng.choice(PRINCIPLES)
        mine = [u for u, p in SOUND_USES if p == principle]
        others = [u for u, p in SOUND_USES if p != principle]
        return _labelled(
            stem=f"ข้อใดเป็นตัวอย่างการนำความรู้เรื่อง{principle}ไปใช้ประโยชน์",
            correct=rng.choice(mine), wrongs=tuple(others),
            topic=TOPIC_SOUND_USE,
            hint="อ่านแต่ละตัวอย่างแล้วถามว่าเสียงทำอะไรในเทคโนโลยีนั้น")


@question_type(
    "phys.sound_use_application",
    display_name={"th": "เลือกและใช้เทคโนโลยีด้านเสียงแก้ปัญหา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SOUND_USE,
)
class SoundUseApplication(QuestionType):
    """A problem to fix with sound, and the numbers behind a car's parking sensor."""

    PROBLEMS = (
        ("ต้องการทราบความลึกของแม่น้ำโดยไม่ต้องดำลงไป", "ส่งคลื่นเสียงลงไปแล้วจับเวลาที่เสียงสะท้อนกลับขึ้นมา"),
        ("ห้องประชุมมีเสียงก้องจนฟังผู้พูดไม่ชัด", "บุผนังและเพดานด้วยวัสดุที่ดูดกลืนเสียง"),
        ("ต้องการตรวจอวัยวะภายในของผู้ป่วยโดยไม่ใช้รังสี", "ใช้คลื่นเหนือเสียงแล้วสร้างภาพจากคลื่นที่สะท้อนกลับ"),
        ("คนงานได้ยินเสียงเครื่องยนต์ดังตลอดเวลาในห้องโดยสาร", "ใช้หูฟังที่สร้างเสียงหักล้างกับเสียงรบกวน"),
        ("ต้องการทราบว่ารถคันหนึ่งวิ่งเร็วเกินกำหนดหรือไม่", "ส่งคลื่นไปกระทบรถแล้ววัดการเปลี่ยนความถี่ของคลื่นที่สะท้อนกลับ"),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            problem, fix = rng.choice(self.PROBLEMS)
            return _labelled(
                stem=f"\"{problem}\" ควรใช้ความรู้เรื่องเสียงแก้ปัญหาอย่างไร",
                correct=fix,
                wrongs=tuple([f for p, f in self.PROBLEMS if f != fix]),
                topic=TOPIC_SOUND_USE,
                hint="จับคู่ปัญหากับสิ่งที่เสียงทำได้: สะท้อนกลับ ถูกดูดกลืน หักล้างกัน หรือเปลี่ยนความถี่เมื่อแหล่งเคลื่อนที่")
        ms = rng.randint(2, 30)
        distance = Fraction(340 * ms, 2000)
        return _numeric(
            stem=(f"เซนเซอร์ถอยจอดรถส่งคลื่นเสียงออกไป และรับเสียงสะท้อนจากกำแพงกลับมาใน {ms} มิลลิวินาที "
                  "ถ้าอัตราเร็วเสียง 340 m/s ท้ายรถอยู่ห่างจากกำแพงกี่เซนติเมตร"),
            answer=distance * 100, wrongs=[distance * 200, Fraction(340 * ms, 1000) * 1000, distance * 10],
            unit="เซนติเมตร", topic=TOPIC_SOUND_USE,
            hint="เสียงเดินทางไปและกลับ ระยะ = อัตราเร็ว × เวลา ÷ 2 และ 1 มิลลิวินาที = 0.001 วินาที")
