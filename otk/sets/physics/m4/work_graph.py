"""งานของแรงคงตัวและกำลังเฉลี่ย

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/10

Sets moved here from: science_wave_f3.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import SUBJECT, UPPER_FOUR, G, _labelled, numeric

PROVENANCE = Provenance("original")


TOPIC_WORK = "งานของแรงคงตัวและกำลังเฉลี่ย"


@question_type(
    "phys.work_graph_foundation",
    display_name={"th": "งานของแรงคงตัว W = Fs cos θ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_WORK,
)
class WorkGraphFoundation(QuestionType):
    """Work along the motion, against it, and at right angles to it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        f = rng.randint(2, 20) * 5
        s = rng.randint(2, 12)
        shape = rng.randrange(4)
        hint = "W = Fs cos θ: แรงตามทิศการเคลื่อนที่ให้งานบวก สวนทางให้งานลบ ตั้งฉากไม่ทำงาน"
        if shape == 0:
            return numeric(stem=f"ออกแรง {f} N ลากกล่องไปตามแนวแรงได้ระยะ {s} m งานของแรงนี้เท่าใด",
                           answer=f * s, wrongs=[f + s, Fraction(f, s), f * s * 2], unit="J", topic=TOPIC_WORK,
                           hint=hint)
        if shape == 1:
            return numeric(stem=f"แรงเสียดทาน {f} N ต้านกล่องที่ไถลไปได้ระยะ {s} m งานของแรงเสียดทานเท่าใด",
                           answer=-f * s, wrongs=[f * s, -f - s, 0], unit="J", topic=TOPIC_WORK, hint=hint,
                           allow_negative=True)
        if shape == 2:
            return _labelled(
                stem=f"นักเรียนถือกระเป๋าหนัก {f} N เดินไปตามพื้นราบได้ระยะ {s} m งานที่แรงยกกระเป๋าทำเท่าใด",
                correct="0 J", wrongs=(f"{f * s} J", f"{f + s} J", f"{-f * s} J"), topic=TOPIC_WORK,
                hint="แรงยกมีทิศขึ้น แต่การกระจัดอยู่ในแนวระดับ ตั้งฉากกันจึงไม่มีงาน")
        angle = rng.choice((37, 53))
        cos = Fraction(4, 5) if angle == 37 else Fraction(3, 5)
        sin = Fraction(3, 5) if angle == 37 else Fraction(4, 5)
        return numeric(
            stem=(f"ดึงกล่องด้วยแรง {f} N ในแนวทำมุม {angle}° กับพื้น ลากไปตามพื้นได้ระยะ {s} m "
                  "งานของแรงดึงเท่าใด (sin 37° = 0.6, cos 37° = 0.8)"),
            # Ignoring the angle, and using sin for cos.
            answer=f * s * cos, wrongs=[f * s, f * s * sin, f * s * Fraction(1, 2)],
            unit="J", topic=TOPIC_WORK, hint=hint)


@question_type(
    "phys.work_graph_fluency",
    display_name={"th": "งานจากพื้นที่ใต้กราฟแรงกับตำแหน่ง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_WORK,
)
class WorkGraphFluency(QuestionType):
    """The area under a force-position graph: rectangle, triangle, and both."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        f = rng.randint(2, 12) * 5
        x1 = rng.randint(2, 8)
        x2 = x1 + rng.choice((2, 4, 6))
        shape = rng.randrange(3)
        hint = "งานเท่ากับพื้นที่ใต้กราฟแรงกับตำแหน่ง แบ่งเป็นสี่เหลี่ยมและสามเหลี่ยมแล้วรวมกัน"
        if shape == 0:
            return numeric(
                stem=f"กราฟแรงกับตำแหน่ง: แรงคงที่ {f} N ตั้งแต่ x = 0 ถึง x = {x1} m งานของแรงนี้เท่าใด",
                answer=f * x1, wrongs=[Fraction(f * x1, 2), f + x1, f * x1 * 2], unit="J", topic=TOPIC_WORK,
                hint=hint)
        if shape == 1:
            return numeric(
                stem=(f"กราฟแรงกับตำแหน่ง: แรงเพิ่มจาก 0 เป็น {f} N อย่างสม่ำเสมอ ตั้งแต่ x = 0 ถึง x = {x1} m "
                      "งานของแรงนี้เท่าใด"),
                answer=Fraction(f * x1, 2), wrongs=[f * x1, f + x1, Fraction(f * x1, 4)], unit="J", topic=TOPIC_WORK,
                hint=hint)
        work = f * x1 + Fraction(f * (x2 - x1), 2)
        return numeric(
            stem=(f"กราฟแรงกับตำแหน่ง: แรงคงที่ {f} N ตั้งแต่ x = 0 ถึง x = {x1} m แล้วลดลงเป็นเส้นตรงจนเป็นศูนย์"
                  f"ที่ x = {x2} m งานทั้งหมดเท่าใด"),
            answer=work, wrongs=[f * x2, f * x1, Fraction(f * x2, 2)], unit="J", topic=TOPIC_WORK, hint=hint)


@question_type(
    "phys.work_graph_application",
    display_name={"th": "คำนวณกำลังเฉลี่ยจากงานและเวลา"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_WORK,
)
class WorkGraphApplication(QuestionType):
    """Average power: lifting, climbing, and P = Fv."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        hint = "กำลังเฉลี่ย = งาน ÷ เวลา และเมื่อแรงคงตัวดันวัตถุด้วยความเร็วคงตัว P = Fv"
        if shape == 0:
            m = rng.randint(1, 20) * 5
            h = rng.randint(2, 12)
            t = rng.choice([x for x in (2, 4, 5, 8, 10, 20) if (m * G * h) % x == 0])
            return numeric(
                stem=f"เครนยกวัตถุมวล {m} kg ขึ้นสูง {h} m ด้วยความเร็วคงตัวในเวลา {t} s กำลังเฉลี่ยของเครนเท่าใด (g = 10 m/s²)",
                answer=Fraction(m * G * h, t), wrongs=[m * G * h, Fraction(m * h, t), Fraction(m * G, t)],
                unit="W", topic=TOPIC_WORK, hint=hint)
        if shape == 1:
            m = rng.randint(8, 16) * 5
            h = rng.randint(2, 6) * 3
            t = rng.choice([x for x in (5, 10, 15, 20, 30) if (m * G * h) % x == 0])
            return numeric(
                stem=f"นักเรียนมวล {m} kg วิ่งขึ้นบันไดสูง {h} m ในเวลา {t} s มีกำลังเฉลี่ยเท่าใด (g = 10 m/s²)",
                answer=Fraction(m * G * h, t), wrongs=[m * G * h, Fraction(m * h, t), Fraction(m * G * t, h)],
                unit="W", topic=TOPIC_WORK, hint=hint)
        f = rng.randint(2, 20) * 100
        v = rng.randint(2, 30)
        return numeric(
            stem=f"รถยนต์วิ่งด้วยความเร็วคงตัว {v} m/s โดยเครื่องยนต์ออกแรงขับ {f:,} N กำลังของเครื่องยนต์เท่าใด",
            answer=f * v, wrongs=[Fraction(f, v), f + v, f * v * 2], unit="W", topic=TOPIC_WORK, hint=hint)
