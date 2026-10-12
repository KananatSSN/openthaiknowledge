"""ผลของความเร่งต่อการเคลื่อนที่แนวตรง โพรเจกไทล์ วงกลม และการสั่น

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.5/5

Sets moved here from: science_wave_e11.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e11 import SUBJECT, UPPER_FIVE, G, _labelled, _numeric

PROVENANCE = Provenance("original")


TOPIC_MOTIONS = "ผลของความเร่งต่อการเคลื่อนที่แนวตรง โพรเจกไทล์ วงกลม และการสั่น"


STRAIGHT, PROJECTILE, CIRCLE, SWING = (
    "การเคลื่อนที่แนวตรง", "การเคลื่อนที่แบบโพรเจกไทล์", "การเคลื่อนที่แบบวงกลม", "การเคลื่อนที่แบบสั่น")


MOTIONS = (STRAIGHT, PROJECTILE, CIRCLE, SWING)


ACCELERATION_OF = {
    STRAIGHT: "ความเร่งอยู่ในแนวเดียวกับความเร็ว ทำให้วัตถุเร็วขึ้นหรือช้าลงโดยไม่เปลี่ยนแนว",
    PROJECTILE: "ความเร่งคงตัวเท่ากับความเร่งโน้มถ่วง มีทิศลงในแนวดิ่งตลอดการเคลื่อนที่",
    CIRCLE: "ความเร่งมีทิศเข้าสู่ศูนย์กลางของวงกลมตลอดเวลา ทำให้ทิศของความเร็วเปลี่ยน",
    SWING: "ความเร่งมีทิศเข้าหาตำแหน่งสมดุลเสมอ และมีขนาดมากที่สุดที่ตำแหน่งปลายสุด",
}


MOTION_EXAMPLES = (
    ("ผลมะพร้าวหล่นจากต้นลงสู่พื้นตรง ๆ", STRAIGHT),
    ("รถยนต์เบรกจนหยุดบนถนนตรง", STRAIGHT),
    ("รถไฟเร่งความเร็วออกจากสถานีบนรางตรง", STRAIGHT),
    ("ลูกบาสเกตบอลที่ถูกโยนเป็นแนวโค้งลงห่วง", PROJECTILE),
    ("น้ำที่พุ่งออกจากสายยางในแนวเฉียงขึ้น", PROJECTILE),
    ("ลูกบอลที่กลิ้งตกจากขอบโต๊ะ", PROJECTILE),
    ("รถยนต์วิ่งรอบวงเวียนด้วยอัตราเร็วคงตัว", CIRCLE),
    ("ก้อนหินผูกเชือกแกว่งเป็นวงกลมในแนวระดับ", CIRCLE),
    ("ดาวเทียมโคจรรอบโลกเป็นวงกลม", CIRCLE),
    ("ลูกตุ้มนาฬิกาแกว่งไปมา", SWING),
    ("มวลที่ติดปลายสปริงสั่นขึ้นลง", SWING),
    ("เด็กนั่งชิงช้าแกว่งไปมา", SWING),
    ("ลิฟต์เริ่มเคลื่อนที่ขึ้นจากชั้นล่างในแนวดิ่ง", STRAIGHT),
    ("ลูกบอลกลิ้งลงตามรางเอียงที่ตรง", STRAIGHT),
    ("เครื่องบินเร่งความเร็วบนทางวิ่งก่อนขึ้นบิน", STRAIGHT),
    ("ลูกกอล์ฟที่ถูกตีลอยโค้งไปตกบนสนาม", PROJECTILE),
    ("ลูกเทนนิสที่ถูกตีข้ามเน็ตเป็นแนวโค้ง", PROJECTILE),
    ("ลูกดอกที่ถูกขว้างเป็นแนวโค้งไปปักเป้า", PROJECTILE),
    ("รถไฟเหาะวิ่งรอบวงแหวนแนวดิ่งด้วยอัตราเร็วคงตัว", CIRCLE),
    ("เสื้อผ้าหมุนเป็นวงกลมในถังปั่นแห้งของเครื่องซักผ้า", CIRCLE),
    ("ใบพัดลมหมุนด้วยอัตราเร็วคงตัว", CIRCLE),
    ("เข็มนาฬิกาแบบลูกตุ้มแกว่งกลับไปกลับมาผ่านจุดต่ำสุด", SWING),
    ("ไม้บรรทัดที่ถูกกดปลายแล้วปล่อยให้สั่นขึ้นลง", SWING),
    ("รถจักรยานยนต์ชะลอความเร็วจนหยุดบนถนนตรง", STRAIGHT),
    ("ลูกธนูที่ยิงเฉียงขึ้นแล้วโค้งลงสู่เป้า", PROJECTILE),
    ("กล่องเสบียงที่ปล่อยจากเครื่องบินซึ่งบินในแนวระดับ", PROJECTILE),
    ("เด็กนั่งม้าหมุนที่หมุนด้วยอัตราเร็วคงตัว", CIRCLE),
    ("เสื้อผ้าในถังปั่นแห้งของเครื่องซักผ้า", CIRCLE),
    ("อิเล็กตรอนเคลื่อนที่เป็นวงกลมในสนามแม่เหล็ก", CIRCLE),
    ("สายกีตาร์ที่ถูกดีดสั่นไปมา", SWING),
    ("ไม้บรรทัดที่กดปลายไว้กับขอบโต๊ะแล้วดีดให้สั่น", SWING),
    ("ทุ่นลอยน้ำที่กระเพื่อมขึ้นลงเมื่อถูกกดแล้วปล่อย", SWING),
)


@question_type(
    "phys.accelerated_motion_foundation",
    display_name={"th": "ลักษณะความเร่งของการเคลื่อนที่แต่ละแบบ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_MOTIONS,
)
class AcceleratedMotionFoundation(QuestionType):
    """Name the motion from an example, before explaining its acceleration."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        example, motion = rng.choice(MOTION_EXAMPLES)
        return _labelled(
            stem=f"\"{example}\" เป็นการเคลื่อนที่แบบใด",
            correct=motion, wrongs=tuple(m for m in MOTIONS if m != motion),
            topic=TOPIC_MOTIONS,
            hint="ดูรูปร่างเส้นทาง: เส้นตรง เส้นโค้งพาราโบลา วงกลม หรือกลับไปกลับมาผ่านจุดเดิม",
        )


@question_type(
    "phys.accelerated_motion_fluency",
    display_name={"th": "อธิบายความเร่งในการเคลื่อนที่แนวตรง โพรเจกไทล์ วงกลม และการสั่น"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_MOTIONS,
)
class AcceleratedMotionFluency(QuestionType):
    """The indicator across all four motions: what the acceleration does in each."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        example, motion = rng.choice(MOTION_EXAMPLES)
        if rng.random() < 0.6:
            return _labelled(
                stem=f"\"{example}\" ข้อใดอธิบายความเร่งของวัตถุได้ถูกต้อง",
                correct=ACCELERATION_OF[motion],
                wrongs=tuple(ACCELERATION_OF[m] for m in MOTIONS if m != motion),
                topic=TOPIC_MOTIONS,
                hint="ความเร่งไม่จำเป็นต้องอยู่ในทิศของความเร็ว ให้ดูว่าความเร่งทำให้ขนาดหรือทิศของความเร็วเปลี่ยน",
            )
        if rng.random() < 0.5:
            # Reverse: from the acceleration to an example of it.
            motion = rng.choice(MOTIONS)
            mine = [e for e, m in MOTION_EXAMPLES if m == motion]
            others = rng.sample([m for m in MOTIONS if m != motion], 3)
            return _labelled(
                stem=f"วัตถุในข้อใดมีลักษณะความเร่งดังนี้: \"{ACCELERATION_OF[motion]}\"",
                correct=rng.choice(mine),
                wrongs=tuple(rng.choice([e for e, m in MOTION_EXAMPLES if m == o]) for o in others),
                topic=TOPIC_MOTIONS,
                hint="นึกภาพเส้นทางของวัตถุแต่ละข้อ แล้วถามว่าแรงลัพธ์ชี้ไปทางใด",
            )
        motion = rng.choice(MOTIONS)
        return _labelled(
            stem=f"ข้อใดอธิบายความเร่งของ{motion}ได้ถูกต้อง",
            correct=ACCELERATION_OF[motion],
            wrongs=tuple(ACCELERATION_OF[m] for m in MOTIONS if m != motion),
            topic=TOPIC_MOTIONS,
            hint="นึกถึงตัวอย่างของการเคลื่อนที่นั้น แล้วถามว่าแรงลัพธ์ (และความเร่ง) ชี้ไปทางใด",
        )


@question_type(
    "phys.accelerated_motion_application",
    display_name={"th": "คำนวณการตกอิสระ โพรเจกไทล์แนวระดับ และความเร่งสู่ศูนย์กลาง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_MOTIONS,
)
class AcceleratedMotionApplication(QuestionType):
    """The accelerations put to numbers, with g = 10 m/s²."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(4)
        if shape == 0:
            t = rng.randint(1, 5)
            if rng.random() < 0.5:
                return _numeric(
                    stem=(f"ปล่อยก้อนหินจากที่สูงให้ตกอิสระ (g = 10 m/s²) เมื่อเวลาผ่านไป {t} วินาที "
                          "ก้อนหินมีความเร็วเท่าใด"),
                    answer=G * t, wrongs=[5 * t * t, G, G * t * t], unit="m/s",
                    topic=TOPIC_MOTIONS, hint="การตกอิสระมีความเร่ง g คงตัว: v = gt")
            return _numeric(
                stem=(f"ปล่อยก้อนหินจากที่สูงให้ตกอิสระ (g = 10 m/s²) ใน {t} วินาทีแรก "
                      "ก้อนหินตกลงมาได้ระยะทางเท่าใด"),
                answer=5 * t * t, wrongs=[G * t, G * t * t, 5 * t], unit="เมตร",
                topic=TOPIC_MOTIONS, hint="ระยะทางของการตกอิสระจากหยุดนิ่ง: s = ½gt²")
        if shape == 1:
            t = rng.randint(1, 4)
            h = 5 * t * t
            u = rng.randint(2, 15)
            return _numeric(
                stem=(f"ลูกบอลกลิ้งตกจากขอบโต๊ะสูง {h} เมตรด้วยความเร็วแนวระดับ {u} m/s "
                      "(g = 10 m/s² ไม่คิดแรงต้านอากาศ) ลูกบอลตกห่างจากขอบโต๊ะในแนวระดับเท่าใด"),
                answer=u * t, wrongs=[u * h, u, u * t * 2, h], unit="เมตร",
                topic=TOPIC_MOTIONS,
                hint="หาเวลาตกจากแนวดิ่งก่อน (h = ½gt²) แล้วคูณด้วยความเร็วแนวระดับที่คงตัว")
        if shape == 2:
            v = rng.choice((2, 3, 4, 5, 6, 8, 10, 12))
            r = rng.choice([d for d in range(1, 51) if (v * v) % d == 0 and d != v])
            return _numeric(
                stem=(f"วัตถุเคลื่อนที่เป็นวงกลมรัศมี {r} เมตรด้วยอัตราเร็วคงตัว {v} m/s "
                      "ความเร่งสู่ศูนย์กลางมีขนาดเท่าใด"),
                answer=Fraction(v * v, r), wrongs=[Fraction(v, r), v * r, Fraction(v * v, 2 * r)],
                unit="m/s²", topic=TOPIC_MOTIONS,
                hint="ความเร่งสู่ศูนย์กลาง a = v²/r")
        where = rng.choice(("ตำแหน่งปลายสุด", "ตำแหน่งสมดุล"))
        correct = ("ความเร่งมีขนาดมากที่สุด แต่อัตราเร็วเป็นศูนย์" if where == "ตำแหน่งปลายสุด"
                   else "ความเร่งเป็นศูนย์ แต่อัตราเร็วมากที่สุด")
        return _labelled(
            stem=f"มวลติดปลายสปริงสั่นกลับไปกลับมา ขณะมวลอยู่ที่{where} ข้อใดถูกต้อง",
            correct=correct,
            wrongs=tuple(w for w in ("ความเร่งมีขนาดมากที่สุด แต่อัตราเร็วเป็นศูนย์",
                                     "ความเร่งเป็นศูนย์ แต่อัตราเร็วมากที่สุด",
                                     "ทั้งความเร่งและอัตราเร็วมีค่ามากที่สุด",
                                     "ทั้งความเร่งและอัตราเร็วเป็นศูนย์") if w != correct),
            topic=TOPIC_MOTIONS,
            hint="แรงดึงกลับของสปริงมากที่สุดเมื่อยืดหรือหดมากที่สุด และเป็นศูนย์ที่ตำแหน่งสมดุล",
        )
