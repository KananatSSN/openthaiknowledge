"""แรงแม่เหล็กต่ออนุภาคที่มีประจุ ลวดที่มีกระแส และหลักการทำงานของมอเตอร์

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.5/8

Sets moved here from: science_wave_e12.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e12 import (
    DIRECTION,
    SUBJECT,
    UPPER_FIVE,
    Vec,
    _direction_choices,
    _labelled,
    cross,
    neg,
)

PROVENANCE = Provenance("original")


TOPIC_FORCE = "แรงแม่เหล็กต่ออนุภาคที่มีประจุ ลวดที่มีกระแส และหลักการทำงานของมอเตอร์"


ZERO_FORCE = "ไม่มีแรงกระทำ"


MOTOR_PARTS = (
    ("ขดลวดอาร์เมเจอร์", "เป็นขดลวดที่มีกระแสผ่าน จึงถูกแรงแม่เหล็กกระทำจนหมุน"),
    ("แม่เหล็กถาวร", "ให้สนามแม่เหล็กที่ขดลวดวางอยู่"),
    ("คอมมิวเทเตอร์", "กลับทิศกระแสในขดลวดทุกครึ่งรอบ ขดลวดจึงหมุนไปทางเดิมต่อเนื่อง"),
    ("แปรงถ่าน", "สัมผัสคอมมิวเทเตอร์เพื่อนำกระแสจากแหล่งจ่ายเข้าสู่ขดลวดที่กำลังหมุน"),
)


MOTOR_FACTS = (
    ("มอเตอร์ไฟฟ้าเปลี่ยนพลังงานรูปใดเป็นรูปใด", "พลังงานไฟฟ้าเป็นพลังงานกล",
     ("พลังงานกลเป็นพลังงานไฟฟ้า", "พลังงานความร้อนเป็นพลังงานไฟฟ้า", "พลังงานแสงเป็นพลังงานกล")),
    ("มอเตอร์ไฟฟ้าทำงานได้โดยอาศัยหลักการใด",
     "ลวดที่มีกระแสไฟฟ้าผ่านและวางอยู่ในสนามแม่เหล็กจะถูกแรงแม่เหล็กกระทำ",
     ("การเปลี่ยนสนามแม่เหล็กผ่านขดลวดทำให้เกิดกระแสไฟฟ้า", "ประจุไฟฟ้าสถิตผลักกัน",
      "ความร้อนทำให้ลวดขยายตัวจนหมุน")),
)


MOTOR_DEVICES = ("พัดลมไฟฟ้า", "เครื่องปั่นน้ำผลไม้", "สว่านไฟฟ้า", "เครื่องดูดฝุ่น",
                 "รถยนต์ไฟฟ้า", "เครื่องซักผ้า", "แปรงสีฟันไฟฟ้า")


NOT_MOTOR_DEVICES = ("เตารีดไฟฟ้า", "หลอดไฟ LED", "กาต้มน้ำไฟฟ้า", "เครื่องคิดเลข",
                     "หม้อหุงข้าวไฟฟ้า", "ถ่านไฟฉาย")


MOTOR_TRUE = (
    "ขดลวดหมุนได้เพราะด้านทั้งสองของขดลวดถูกแรงแม่เหล็กในทิศตรงข้ามกัน",
    "คอมมิวเทเตอร์ทำให้กระแสในขดลวดกลับทิศทุกครึ่งรอบ ขดลวดจึงหมุนทางเดียวต่อเนื่อง",
    "ถ้าไม่มีกระแสไฟฟ้าผ่านขดลวด ขดลวดจะไม่ถูกแรงแม่เหล็กและไม่หมุน",
    "มอเตอร์เปลี่ยนพลังงานไฟฟ้าเป็นพลังงานกล",
)


MOTOR_FALSE = (
    "ขดลวดหมุนเพราะแม่เหล็กถาวรหมุนรอบขดลวด",
    "คอมมิวเทเตอร์ทำหน้าที่เพิ่มกระแสไฟฟ้าให้ขดลวด",
    "มอเตอร์เปลี่ยนพลังงานกลเป็นพลังงานไฟฟ้า",
    "ถ้าไม่มีคอมมิวเทเตอร์ ขดลวดจะหมุนเร็วขึ้นในทิศเดิม",
    "แปรงถ่านทำให้เกิดสนามแม่เหล็กในมอเตอร์",
)


def particle_force(velocity: Vec, field: Vec, charge: int) -> Vec:
    """F = q v × B, with the sign of q only."""
    f = cross(velocity, field)
    return f if charge > 0 else neg(f)


@question_type(
    "phys.magnetic_force_foundation",
    display_name={"th": "ส่วนประกอบและหลักการทำงานของมอเตอร์ไฟฟ้า"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FORCE,
)
class MagneticForceFoundation(QuestionType):
    """The second outcome, อธิบายหลักการทำงานของมอเตอร์: its parts and principle."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "มอเตอร์ใช้แรงแม่เหล็กที่กระทำต่อขดลวดที่มีกระแส และใช้คอมมิวเทเตอร์กลับทิศกระแสทุกครึ่งรอบ"
        shape = rng.random()
        if shape < 0.15:
            stem, correct, wrongs = rng.choice(MOTOR_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_FORCE, hint=hint)
        if shape < 0.3:
            return _labelled(stem="เครื่องใช้ไฟฟ้าใดมีมอเตอร์ไฟฟ้าเป็นส่วนประกอบหลัก",
                             correct=rng.choice(MOTOR_DEVICES),
                             wrongs=tuple(NOT_MOTOR_DEVICES),
                             topic=TOPIC_FORCE,
                             hint="มอเตอร์ทำให้ส่วนหนึ่งของเครื่องหมุน มองหาเครื่องที่มีการหมุน")
        if shape < 0.5:
            return _labelled(stem="ข้อใดอธิบายการทำงานของมอเตอร์ไฟฟ้ากระแสตรงได้ถูกต้อง",
                             correct=rng.choice(MOTOR_TRUE), wrongs=tuple(MOTOR_FALSE),
                             topic=TOPIC_FORCE, hint=hint)
        part, job = rng.choice(MOTOR_PARTS)
        if shape < 0.75:
            return _labelled(
                stem=f"ในมอเตอร์ไฟฟ้ากระแสตรง {part}ทำหน้าที่ใด",
                correct=job, wrongs=tuple(j for p, j in MOTOR_PARTS if p != part),
                topic=TOPIC_FORCE, hint=hint)
        return _labelled(
            stem=f"ในมอเตอร์ไฟฟ้ากระแสตรง ส่วนประกอบใด{job.split(' ')[0]}",
            correct=part, wrongs=tuple(p for p, _ in MOTOR_PARTS if p != part),
            topic=TOPIC_FORCE, hint=hint)


@question_type(
    "phys.magnetic_force_fluency",
    display_name={"th": "หาทิศของแรงแม่เหล็กต่ออนุภาคที่มีประจุและลวดที่มีกระแส"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FORCE,
)
class MagneticForceFluency(QuestionType):
    """The first outcome across both of its objects: a moving charge and a current-carrying wire."""

    PARTICLES = (("โปรตอน", 1), ("อิเล็กตรอน", -1), ("อนุภาคแอลฟา", 1))

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = ("ใช้มือขวา: นิ้วทั้งสี่ชี้ตามความเร็ว (หรือกระแส) แล้วงอเข้าหาทิศสนามแม่เหล็ก "
                "นิ้วหัวแม่มือคือทิศของแรงต่อประจุบวก ถ้าเป็นประจุลบแรงมีทิศตรงข้าม")
        shape = rng.random()
        field = rng.choice(list(DIRECTION))
        if shape < 0.15:
            name, _ = rng.choice(self.PARTICLES)
            parallel = rng.random() < 0.5
            motion = (f"เคลื่อนที่{DIRECTION[field]}ในแนวเดียวกับสนามแม่เหล็ก" if parallel
                      else "หยุดนิ่งอยู่")
            return _labelled(
                stem=(f"{name}{motion} ในบริเวณที่มีสนามแม่เหล็กสม่ำเสมอมีทิศ{DIRECTION[field]} "
                      "แรงแม่เหล็กที่กระทำต่ออนุภาคเป็นอย่างไร"),
                correct=ZERO_FORCE,
                wrongs=(DIRECTION[field], *[DIRECTION[v] for v in DIRECTION
                                            if cross(v, field) != (0, 0, 0)][:2]),
                topic=TOPIC_FORCE,
                hint="แรงแม่เหล็กเกิดเมื่อประจุเคลื่อนที่ตัดสนามแม่เหล็กเท่านั้น")
        velocity = rng.choice([v for v in DIRECTION if cross(v, field) != (0, 0, 0)])
        if shape < 0.6:
            name, charge = rng.choice(self.PARTICLES)
            force = particle_force(velocity, field, charge)
            stem = (f"{name}เคลื่อนที่{DIRECTION[velocity]} เข้าไปในสนามแม่เหล็กสม่ำเสมอที่มีทิศ"
                    f"{DIRECTION[field]} แรงแม่เหล็กที่กระทำต่อ{name}มีทิศใด")
        else:
            force = cross(velocity, field)
            stem = (f"ลวดตรงมีกระแสไฟฟ้าไหล{DIRECTION[velocity]} วางอยู่ในสนามแม่เหล็กสม่ำเสมอที่มีทิศ"
                    f"{DIRECTION[field]} แรงแม่เหล็กที่กระทำต่อลวดมีทิศใด")
        return _labelled(
            stem=stem, correct=DIRECTION[force],
            wrongs=tuple(_direction_choices(force, velocity, field)),
            topic=TOPIC_FORCE, hint=hint)


@question_type(
    "phys.magnetic_force_application",
    display_name={"th": "คำนวณแรงแม่เหล็กต่อลวดและปรับการทำงานของมอเตอร์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FORCE,
)
class MagneticForceApplication(QuestionType):
    """F = BIL with numbers, and what changes a motor's speed or direction."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            b = Fraction(rng.choice((1, 2, 3, 4, 5)), 10)
            i = rng.randint(1, 10)
            length = Fraction(rng.choice((10, 20, 25, 50, 100)), 100)
            f = b * i * length

            def n(x):
                v = float(x)
                return f"{v:g}"
            wrongs = [b * i, i * length, f * 10, f * 2, b * length]
            seen = [f]
            for w in wrongs:
                if w not in seen:
                    seen.append(w)
            return GeneratedQuestion(
                stem=[text(f"ลวดยาว {n(length)} เมตรมีกระแสไฟฟ้า {i} แอมแปร์ วางตั้งฉากกับสนามแม่เหล็ก "
                           f"{n(b)} เทสลา แรงแม่เหล็กที่กระทำต่อลวดมีขนาดเท่าใด")],
                correct=[text(f"{n(f)} นิวตัน")],
                distractors=fixed(*[[text(f"{n(w)} นิวตัน")] for w in seen[1:]]),
                topic=TOPIC_FORCE,
                hint=[text("แรงแม่เหล็กต่อลวดที่วางตั้งฉากกับสนาม F = BIL")])
        goal = rng.choice(("หมุนเร็วขึ้น", "หมุนกลับทิศ"))
        if goal == "หมุนเร็วขึ้น":
            correct = rng.choice(("เพิ่มกระแสไฟฟ้าที่ผ่านขดลวด", "ใช้แม่เหล็กที่มีสนามแม่เหล็กแรงขึ้น",
                                  "เพิ่มจำนวนรอบของขดลวดอาร์เมเจอร์"))
            wrongs = ("กลับขั้วแบตเตอรี่", "สลับขั้วของแม่เหล็กถาวร", "ถอดคอมมิวเทเตอร์ออก")
        else:
            correct = rng.choice(("กลับขั้วแบตเตอรี่", "สลับขั้วของแม่เหล็กถาวร"))
            wrongs = ("เพิ่มกระแสไฟฟ้าที่ผ่านขดลวด", "เพิ่มจำนวนรอบของขดลวดอาร์เมเจอร์",
                      "กลับขั้วแบตเตอรี่และสลับขั้วแม่เหล็กพร้อมกัน")
        return _labelled(
            stem=f"ต้องการให้มอเตอร์ไฟฟ้ากระแสตรง{goal} ควรทำอย่างไร",
            correct=correct, wrongs=wrongs, topic=TOPIC_FORCE,
            hint="ขนาดของแรงขึ้นกับกระแส สนาม และจำนวนรอบ ส่วนทิศของแรงกลับเมื่อกลับทิศกระแสหรือทิศสนามอย่างใดอย่างหนึ่ง")
