"""การเคลื่อนที่แบบวงกลมและการโคจรของดาวเทียม

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/17

Sets moved here from: science_wave_f6.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import G, _labelled, numeric, show
from otk.sets._support.science_wave_f6 import ORBITS, SUBJECT, UPPER_FOUR, _exact

PROVENANCE = Provenance("original")


TOPIC_CIRCULAR = "การเคลื่อนที่แบบวงกลมและการโคจรของดาวเทียม"


CIRCULAR_FACTS = (
    ("วัตถุเคลื่อนที่เป็นวงกลมด้วยอัตราเร็วคงตัว ความเร็วมีทิศใด", "ทิศสัมผัสวงกลม ณ ตำแหน่งนั้น",
     ("ทิศเข้าสู่ศูนย์กลาง", "ทิศออกจากศูนย์กลาง", "ทิศคงตัวตลอดการเคลื่อนที่")),
    ("แรงสู่ศูนย์กลางมีทิศใด", "เข้าหาศูนย์กลางของวงกลมเสมอ",
     ("ออกจากศูนย์กลางของวงกลม", "ตามทิศความเร็ว", "สวนทิศความเร็ว")),
    ("แกว่งจุกยางผูกเชือกเป็นวงกลมในระนาบระดับ แล้วเชือกขาด จุกยางจะเคลื่อนที่อย่างไร", "ออกไปตามแนวเส้นสัมผัสวงกลม ณ ตำแหน่งที่เชือกขาด",
     ("พุ่งออกในแนวรัศมีจากศูนย์กลาง", "พุ่งเข้าหาศูนย์กลาง", "ยังคงเคลื่อนที่เป็นวงกลมต่อไป")),
    ("วัตถุเคลื่อนที่เป็นวงกลมด้วยอัตราเร็วคงตัว มีความเร่งหรือไม่", "มี เพราะทิศของความเร็วเปลี่ยนตลอดเวลา",
     ("ไม่มี เพราะอัตราเร็วคงตัว", "มี เพราะอัตราเร็วเพิ่มขึ้น", "ไม่มี เพราะแรงลัพธ์เป็นศูนย์")),
    ("รถยนต์เลี้ยวโค้งบนถนนราบ แรงใดทำหน้าที่เป็นแรงสู่ศูนย์กลาง", "แรงเสียดทานระหว่างยางกับถนน",
     ("น้ำหนักของรถ", "แรงที่ถนนดันรถในแนวดิ่ง", "แรงขับของเครื่องยนต์")),
    ("ดาวเทียมโคจรรอบโลกเป็นวงกลม แรงใดทำหน้าที่เป็นแรงสู่ศูนย์กลาง", "แรงดึงดูดระหว่างโลกกับดาวเทียม",
     ("แรงขับของจรวดตลอดเวลา", "แรงต้านอากาศ", "แรงหนีศูนย์กลางของดาวเทียม")),
    ("ดาวเทียมค้างฟ้าโคจรรอบโลกด้วยคาบเท่าใด", "ประมาณ 24 ชั่วโมง เท่ากับคาบการหมุนรอบตัวเองของโลก",
     ("ประมาณ 90 นาที", "ประมาณ 1 เดือน", "ประมาณ 1 ปี")),
    ("ดาวเทียมที่โคจรเป็นวงกลมสูงจากโลกมากขึ้น มีอัตราเร็วในวงโคจรเป็นอย่างไร", "น้อยลง",
     ("มากขึ้น", "เท่าเดิมทุกความสูง", "เป็นศูนย์")),
)


@question_type(
    "phys.circular_motion_foundation",
    display_name={"th": "ความเร็ว แรงสู่ศูนย์กลาง คาบ และอัตราเร็วเชิงมุมในการเคลื่อนที่แบบวงกลม"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CIRCULAR,
)
class CircularMotionFoundation(QuestionType):
    """Directions in circular motion, and period, frequency and v = ωr."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            stem, correct, wrongs = rng.choice(CIRCULAR_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_CIRCULAR,
                             hint="ความเร็วมีทิศสัมผัสวงกลม ส่วนแรงและความเร่งมีทิศเข้าสู่ศูนย์กลาง")
        if shape == 1:
            n = rng.choice((2, 4, 5, 10, 20, 25, 50))
            t = rng.choice([x for x in (1, 2, 4, 5, 10, 20) if _exact(Fraction(x, n)) and _exact(Fraction(n, x))])
            period = rng.random() < 0.5
            return numeric(
                stem=f"วัตถุเคลื่อนที่เป็นวงกลมครบ {n} รอบในเวลา {t} s {'คาบ' if period else 'ความถี่'}ของการเคลื่อนที่เท่าใด",
                answer=Fraction(t, n) if period else Fraction(n, t),
                wrongs=[Fraction(n, t), n * t, Fraction(t, 2 * n)] if period else [Fraction(t, n), n * t, Fraction(2 * n, t)],
                unit="s" if period else "Hz", topic=TOPIC_CIRCULAR,
                hint="คาบ T = เวลาที่ใช้ต่อหนึ่งรอบ ความถี่ f = จำนวนรอบต่อวินาที = 1/T")
        w = rng.randint(2, 20)
        r = Fraction(rng.randint(1, 30), 10)
        return numeric(
            stem=f"วัตถุเคลื่อนที่เป็นวงกลมรัศมี {show(r)} m ด้วยอัตราเร็วเชิงมุม {w} rad/s มีอัตราเร็วเชิงเส้นเท่าใด",
            answer=w * r, wrongs=[Fraction(w) / r, w * r * r, w * r * 2], unit="m/s", topic=TOPIC_CIRCULAR,
            hint="v = ωr")


@question_type(
    "phys.circular_motion_fluency",
    display_name={"th": "คำนวณแรงสู่ศูนย์กลางและความเร่งสู่ศูนย์กลาง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CIRCULAR,
)
class CircularMotionFluency(QuestionType):
    """F = mv²/r, a = v²/r, F = mω²r, and the speed a given force allows."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(4)
        hint = "แรงสู่ศูนย์กลาง F = mv²/r = mω²r และความเร่งสู่ศูนย์กลาง a = v²/r"
        if shape == 0:
            m = Fraction(rng.choice((1, 2, 4, 5, 10, 20)), 10)
            v = rng.randint(2, 12)
            r = rng.choice([x for x in (Fraction(1, 2), 1, 2, Fraction(5, 2), 4, 5) if _exact(m * v * v / x)])
            return numeric(
                stem=f"จุกยางมวล {show(m)} kg ผูกเชือกแกว่งเป็นวงกลมรัศมี {show(r)} m ในระนาบระดับด้วยอัตราเร็ว {v} m/s แรงสู่ศูนย์กลางเท่าใด",
                answer=m * v * v / r, wrongs=[m * v / r, m * v * v * r, m * v * v / r / 2], unit="N",
                topic=TOPIC_CIRCULAR, hint=hint)
        if shape == 1:
            v = rng.randint(2, 30)
            r = rng.choice([x for x in (1, 2, 4, 5, 10, 20, 25, 50, 100) if _exact(Fraction(v * v, x))])
            return numeric(
                stem=f"รถวิ่งรอบวงเวียนรัศมี {r} m ด้วยอัตราเร็วคงตัว {v} m/s มีความเร่งสู่ศูนย์กลางเท่าใด",
                answer=Fraction(v * v, r), wrongs=[Fraction(v, r), Fraction(v * v, 2 * r), v * v * r], unit="m/s²",
                topic=TOPIC_CIRCULAR, hint=hint)
        if shape == 2:
            m = rng.randint(1, 10)
            w = rng.randint(2, 10)
            r = Fraction(rng.randint(1, 20), 10)
            return numeric(
                stem=f"วัตถุมวล {m} kg เคลื่อนที่เป็นวงกลมรัศมี {show(r)} m ด้วยอัตราเร็วเชิงมุม {w} rad/s แรงสู่ศูนย์กลางเท่าใด",
                answer=m * w * w * r, wrongs=[m * w * r, m * w * w / r, m * w * r * r], unit="N",
                topic=TOPIC_CIRCULAR, hint=hint)
        m, v, r = rng.choice([(a, b, c) for a in range(1, 11) for b in range(2, 13) for c in range(1, 6)
                              if (a * b * b) % c == 0])
        return numeric(
            stem=(f"เชือกเส้นหนึ่งทนแรงดึงได้มากที่สุด {m * v * v // r} N "
                  f"ใช้ผูกวัตถุมวล {m} kg แกว่งเป็นวงกลมรัศมี {r} m ในระนาบระดับบนพื้นลื่น "
                  "อัตราเร็วมากที่สุดที่เชือกยังไม่ขาดเท่าใด"),
            answer=v, wrongs=[v * v, v * 2, v + 2], unit="m/s", topic=TOPIC_CIRCULAR,
            hint="แรงตึงเชือกเป็นแรงสู่ศูนย์กลาง: T = mv²/r แล้วแก้หา v")


@question_type(
    "phys.circular_motion_application",
    display_name={"th": "การเลี้ยวโค้งบนถนนราบและการโคจรของดาวเทียม"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CIRCULAR,
)
class CircularMotionApplication(QuestionType):
    """Friction around a bend, a satellite held by gravity, and how F scales."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(4)
        car = rng.randint(16, 40) * 50
        if shape == 3:
            v = rng.randint(5, 25)
            r = rng.choice([x for x in (10, 20, 25, 40, 50, 80, 100, 125, 200) if _exact(Fraction(car * v * v, x))])
            return numeric(
                stem=(f"รถยนต์มวล {car:,} kg เลี้ยวโค้งบนถนนราบรัศมีความโค้ง {r} m ด้วยอัตราเร็วคงตัว {v} m/s "
                      "ต้องมีแรงเสียดทานระหว่างยางกับถนนเท่าใดเป็นแรงสู่ศูนย์กลาง"),
                answer=Fraction(car * v * v, r), wrongs=[Fraction(car * v, r), Fraction(car * v * v, 2 * r), car * G],
                unit="N", topic=TOPIC_CIRCULAR, hint="แรงเสียดทานทำหน้าที่เป็นแรงสู่ศูนย์กลาง: f = mv²/r")
        if shape == 0:
            mu, r, v = rng.choice([(m, Fraction(s * s, G) / m, s) for m in (Fraction(1, 5), Fraction(2, 5), Fraction(1, 2),
                                                                             Fraction(4, 5), 1)
                                   for s in range(5, 31) if (Fraction(s * s, G) / m).denominator == 1])
            return numeric(
                stem=(f"รถยนต์มวล {car:,} kg เลี้ยวโค้งบนถนนราบรัศมีความโค้ง {show(r)} m สัมประสิทธิ์ความเสียดทานสถิตระหว่างยางกับถนน "
                      f"{show(mu)} รถเลี้ยวได้ด้วยอัตราเร็วมากที่สุดเท่าใดโดยไม่ไถลออกนอกโค้ง (g = 10 m/s²)"),
                answer=v, wrongs=[mu * G * r, v * 2, Fraction(v, 2)], unit="m/s", topic=TOPIC_CIRCULAR,
                hint="แรงเสียดทานสถิตสูงสุด μmg เป็นแรงสู่ศูนย์กลาง: μmg = mv²/r ดังนั้น v = √(μgr) ไม่ขึ้นกับมวล")
        if shape == 1:
            r, g, v = rng.choice(ORBITS)
            return numeric(
                stem=(f"ดาวเทียมโคจรรอบโลกเป็นวงกลมรัศมี {r:,} km (วัดจากศูนย์กลางโลก) ซึ่งความเร่งโน้มถ่วงที่ระดับนั้น"
                      f"เท่ากับ {show(g)} m/s² ดาวเทียมมีอัตราเร็วในวงโคจรเท่าใด"),
                answer=v, wrongs=[g * r * 1000, v * 2, Fraction(v, 2)], unit="m/s", topic=TOPIC_CIRCULAR,
                hint="แรงโน้มถ่วง mg' ทำหน้าที่เป็นแรงสู่ศูนย์กลาง: mg' = mv²/r ดังนั้น v = √(g'r) และต้องแปลง km เป็น m")
        speed = rng.choice((1, 2, 3, 4))
        radius = rng.choice((Fraction(1, 2), 1, 2, 4))
        if speed == 1 and radius == 1:
            speed = 2
        factor = Fraction(speed * speed) / radius
        change = [f"อัตราเร็วเพิ่มเป็น {speed} เท่า" if speed != 1 else "อัตราเร็วเท่าเดิม",
                  "รัศมีเท่าเดิม" if radius == 1 else
                  f"รัศมี{'ลดลงเหลือครึ่งหนึ่ง' if radius == Fraction(1, 2) else f'เพิ่มเป็น {radius} เท่า'}"]
        return numeric(
            stem=(f"วัตถุเคลื่อนที่เป็นวงกลมด้วยแรงสู่ศูนย์กลาง F ถ้ามวลเท่าเดิม {change[0]} และ{change[1]} "
                  "แรงสู่ศูนย์กลางจะเป็นกี่เท่าของเดิม"),
            answer=factor, wrongs=[Fraction(speed) / radius, speed * speed * radius, Fraction(speed) * radius],
            unit="เท่า", topic=TOPIC_CIRCULAR, hint="F = mv²/r: แรงแปรผันตรงกับอัตราเร็วกำลังสอง และผกผันกับรัศมี")
