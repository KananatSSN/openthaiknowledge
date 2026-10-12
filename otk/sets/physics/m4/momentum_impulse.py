"""โมเมนตัม การดล และแรงดล

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/14

Sets moved here from: science_wave_f5.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f5 import SUBJECT, UPPER_FOUR, _exact

PROVENANCE = Provenance("original")


TOPIC_MOMENTUM = "โมเมนตัม การดล และแรงดล"


MOMENTUM_FACTS = (
    ("โมเมนตัมของวัตถุคือปริมาณใด", "ผลคูณของมวลกับความเร็ว เป็นปริมาณเวกเตอร์",
     ("ผลคูณของมวลกับความเร่ง เป็นปริมาณสเกลาร์", "ผลคูณของแรงกับระยะทาง", "ครึ่งหนึ่งของมวลคูณอัตราเร็วกำลังสอง")),
    ("การดลของแรงที่กระทำต่อวัตถุเท่ากับปริมาณใด", "โมเมนตัมที่เปลี่ยนไปของวัตถุ",
     ("พลังงานจลน์ที่เปลี่ยนไปของวัตถุ", "งานที่แรงทำ", "โมเมนตัมสุดท้ายของวัตถุเสมอ")),
    ("พื้นที่ใต้กราฟแรงกับเวลาบอกปริมาณใด", "การดล",
     ("งาน", "กำลัง", "ความเร่ง")),
    ("หน่วยของการดลคือข้อใด", "N·s ซึ่งเท่ากับ kg·m/s",
     ("N·m ซึ่งเท่ากับ J", "N/s", "kg·m/s²")),
    ("แรงดลคือแรงแบบใด", "แรงที่กระทำต่อวัตถุในช่วงเวลาสั้น ๆ ทำให้โมเมนตัมเปลี่ยน",
     ("แรงคงตัวที่กระทำตลอดเวลา", "แรงที่ไม่ทำให้โมเมนตัมเปลี่ยน", "แรงโน้มถ่วงที่กระทำต่อวัตถุ")),
)


CUSHIONS = (
    "ถุงลมนิรภัยในรถยนต์", "การย่อเข่าเมื่อกระโดดลงถึงพื้น", "บ่อทรายที่รองรับนักกีฬากระโดดไกล",
    "เบาะรองรับนักกีฬากระโดดสูง", "การเลื่อนมือตามลูกบอลขณะรับลูก", "โฟมกันกระแทกในหมวกกันน็อก",
    "กันชนรถยนต์ที่ยุบตัวได้", "ยางรถที่แขวนไว้ข้างท่าเรือ",
)


@question_type(
    "phys.momentum_impulse_foundation",
    display_name={"th": "โมเมนตัม p = mv และความหมายของการดล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MOMENTUM,
)
class MomentumImpulseFoundation(QuestionType):
    """p = mv, in kilograms and in grams, and what impulse means."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        hint = "โมเมนตัม p = mv (มวลเป็นกิโลกรัม ความเร็วเป็นเมตรต่อวินาที) การดลเท่ากับโมเมนตัมที่เปลี่ยนไป"
        if shape == 0:
            stem, correct, wrongs = rng.choice(MOMENTUM_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_MOMENTUM, hint=hint)
        if shape == 1:
            what, low, high, step = rng.choice((("รถยนต์", 16, 40, 50), ("รถจักรยานยนต์", 10, 30, 10),
                                                ("นักวิ่ง", 8, 16, 5), ("รถเข็น", 1, 30, 2)))
            m = rng.randint(low, high) * step
            v = rng.randint(2, 30)
            return numeric(stem=f"{what}มวล {m:,} kg เคลื่อนที่ด้วยความเร็ว {v} m/s มีโมเมนตัมเท่าใด",
                           answer=m * v, wrongs=[Fraction(m * v * v, 2), Fraction(m, v), m + v],
                           unit="kg·m/s", topic=TOPIC_MOMENTUM, hint=hint)
        grams = rng.choice((50, 100, 150, 200, 250, 400, 500))
        v = rng.randint(2, 40)
        return numeric(stem=f"ลูกบอลมวล {grams} g เคลื่อนที่ด้วยความเร็ว {v} m/s มีโมเมนตัมเท่าใด",
                       answer=Fraction(grams * v, 1000), wrongs=[grams * v, Fraction(grams * v, 100),
                                                                 Fraction(grams * v * v, 2000)],
                       unit="kg·m/s", topic=TOPIC_MOMENTUM, hint=hint)


@question_type(
    "phys.momentum_impulse_fluency",
    display_name={"th": "คำนวณการดลจากสมการและพื้นที่ใต้กราฟแรงกับเวลา"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MOMENTUM,
)
class MomentumImpulseFluency(QuestionType):
    """Impulse as the area under F-t, and as Δp when a ball bounces back."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(4)
        hint = "การดล = FΔt = พื้นที่ใต้กราฟแรงกับเวลา = mv − mu (ต้องคิดทิศของความเร็วด้วย)"
        if shape == 0:
            f = rng.randint(2, 40) * 10
            t = Fraction(rng.randint(1, 20), 100)
            peak = rng.random() < 0.5
            curve = (f"แรงเพิ่มจาก 0 เป็น {f} N แล้วลดกลับเป็น 0 เป็นเส้นตรง ในเวลารวม {show(t)} s" if peak
                     else f"แรงคงที่ {f} N เป็นเวลา {show(t)} s")
            answer = f * t / 2 if peak else f * t
            return numeric(stem=f"กราฟแรงกับเวลาที่กระทำต่อวัตถุ: {curve} การดลของแรงนี้เท่าใด",
                           answer=answer, wrongs=[f * t * 2 if not peak else f * t, f * t / 4, f * t * 10],
                           unit="N·s", topic=TOPIC_MOMENTUM, hint=hint)
        if shape == 1:
            f = rng.randint(2, 20) * 50
            t1, t2, t3 = (Fraction(rng.randint(1, 5), 100) for _ in range(3))
            return numeric(
                stem=(f"กราฟแรงกับเวลา: แรงเพิ่มจาก 0 เป็น {f} N ในเวลา {show(t1)} s คงที่อีก {show(t2)} s "
                      f"แล้วลดเป็น 0 ในเวลา {show(t3)} s การดลทั้งหมดเท่าใด"),
                answer=f * (t2 + (t1 + t3) / 2), wrongs=[f * (t1 + t2 + t3), f * t2, f * (t1 + t2 + t3) / 2],
                unit="N·s", topic=TOPIC_MOMENTUM,
                hint="พื้นที่ใต้กราฟเป็นรูปสี่เหลี่ยมคางหมู: สามเหลี่ยมสองข้างรวมกับสี่เหลี่ยมตรงกลาง")
        if shape == 2:
            m = Fraction(rng.choice((1, 2, 4, 5, 6, 8)), 10)
            u = rng.randint(4, 30)
            v = rng.randint(2, u)
            return numeric(
                stem=(f"ลูกบอลมวล {show(m)} kg พุ่งชนกำแพงในแนวตั้งฉากด้วยอัตราเร็ว {u} m/s "
                      f"แล้วกระดอนกลับในแนวเดิมด้วยอัตราเร็ว {v} m/s การดลที่กำแพงให้ลูกบอลมีขนาดเท่าใด"),
                answer=m * (u + v), wrongs=[m * (u - v), m * u, m * v] if u != v else [m * u, m * u * 4, m],
                unit="N·s", topic=TOPIC_MOMENTUM,
                hint="ความเร็วกลับทิศ: Δp = m(v − (−u)) = m(u + v) ไม่ใช่ m(u − v)")
        m = rng.randint(1, 20) * 5
        u = rng.randint(0, 10)
        impulse = m * rng.randint(1, 10)
        return numeric(
            stem=(f"วัตถุมวล {m} kg เคลื่อนที่ด้วยความเร็ว {u} m/s ได้รับการดลขนาด {impulse} N·s "
                  "ในทิศเดียวกับการเคลื่อนที่ ความเร็วของวัตถุหลังได้รับการดลเท่าใด"),
            answer=u + Fraction(impulse, m), wrongs=[Fraction(impulse, m), u + impulse, Fraction(impulse, m) - u],
            unit="m/s", topic=TOPIC_MOMENTUM, hint="mv = mu + การดล ดังนั้น v = u + การดล ÷ m")


@question_type(
    "phys.momentum_impulse_application",
    display_name={"th": "แรงดลเฉลี่ยและการลดแรงดลในชีวิตประจำวัน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MOMENTUM,
)
class MomentumImpulseApplication(QuestionType):
    """F = Δp ÷ Δt: a crash, a kicked ball, and a longer stop that softens the blow."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(4)
        hint = "แรงดลเฉลี่ย = โมเมนตัมที่เปลี่ยนไป ÷ เวลาที่ใช้ เพิ่มเวลาแรงดลก็ลดลง"
        if shape == 0:
            item = rng.choice(CUSHIONS)
            return _labelled(
                stem=f"{item}ช่วยลดอันตรายจากการกระแทกได้เพราะเหตุใด",
                correct="เพิ่มเวลาในการเปลี่ยนโมเมนตัม แรงดลเฉลี่ยจึงลดลง",
                wrongs=("ลดโมเมนตัมที่เปลี่ยนไปให้เป็นศูนย์", "เพิ่มแรงดลให้หยุดเร็วขึ้น",
                        "ลดเวลาในการเปลี่ยนโมเมนตัม แรงดลเฉลี่ยจึงลดลง"),
                topic=TOPIC_MOMENTUM, hint=hint)
        if shape == 1:
            m = rng.randint(8, 20) * 100
            v = rng.choice((10, 15, 20, 25, 30))
            dt = rng.choice([x for x in (Fraction(1, 10), Fraction(1, 5), Fraction(1, 2), Fraction(1), Fraction(2))
                             if _exact(m * v / x)])
            return numeric(
                stem=f"รถยนต์มวล {m:,} kg วิ่งด้วยความเร็ว {v} m/s ชนกำแพงแล้วหยุดในเวลา {show(dt)} s แรงดลเฉลี่ยมีขนาดเท่าใด",
                answer=m * v / dt, wrongs=[m * v, m * v * dt, Fraction(m * v * v, 2) / dt], unit="N",
                topic=TOPIC_MOMENTUM, hint=hint)
        if shape == 2:
            grams = rng.choice((100, 200, 400, 500))
            u = rng.randint(0, 10)
            v = rng.randint(10, 30)
            ms = rng.choice([x for x in (2, 4, 5, 8, 10, 20, 25, 50) if _exact(Fraction(grams * (u + v), x))])
            m = Fraction(grams, 1000)
            dt = Fraction(ms, 1000)
            return numeric(
                stem=(f"ลูกฟุตบอลมวล {grams} g เคลื่อนที่เข้าหาผู้เล่นด้วยอัตราเร็ว {u} m/s ถูกเตะกลับในแนวเดิม"
                      f"ด้วยอัตราเร็ว {v} m/s เท้าสัมผัสลูกนาน {ms} ms แรงดลเฉลี่ยที่เท้ากระทำมีขนาดเท่าใด"),
                answer=m * (u + v) / dt, wrongs=[m * abs(v - u) / dt, m * v / dt, m * (u + v) / dt / 10],
                unit="N", topic=TOPIC_MOMENTUM, hint="เมื่อลูกกลับทิศ Δp = m(u + v) แล้วหารด้วยเวลาที่สัมผัส (1 ms = 0.001 s)")
        t1 = Fraction(rng.choice((1, 2, 5)), 100)
        k = rng.choice((2, 4, 5, 10))
        f1 = rng.randint(2, 30) * 1000
        return numeric(
            stem=(f"ผู้ขับขี่ชนแล้วหยุดในเวลา {show(t1)} s ได้รับแรงดลเฉลี่ย {f1:,} N ถ้ามีถุงลมนิรภัยทำให้ใช้เวลาหยุด "
                  f"{show(t1 * k)} s โดยโมเมนตัมที่เปลี่ยนไปเท่าเดิม แรงดลเฉลี่ยจะเหลือเท่าใด"),
            answer=Fraction(f1, k), wrongs=[f1 * k, f1, Fraction(f1, 2 * k)], unit="N",
            topic=TOPIC_MOMENTUM, hint="FΔt คงตัว เวลาเพิ่มขึ้นกี่เท่า แรงดลเฉลี่ยก็ลดลงเท่านั้น")
