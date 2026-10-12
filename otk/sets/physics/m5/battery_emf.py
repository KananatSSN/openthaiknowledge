"""อีเอ็มเอฟสมมูลและวงจรไฟฟ้ากระแสตรง

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.5/10

Sets moved here from: science_wave_f12.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_f12 import SUBJECT, UPPER_FIVE, _exact

PROVENANCE = Provenance("original")


TOPIC_EMF = "อีเอ็มเอฟสมมูลและวงจรไฟฟ้ากระแสตรง"


@question_type(
    "phys.battery_emf_foundation",
    display_name={"th": "อีเอ็มเอฟและความต้านทานภายในสมมูลของแบตเตอรี่ที่ต่อแบบอนุกรมและขนาน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EMF,
)
class BatteryEmfFoundation(QuestionType):
    """n identical cells: in series emf and r both add; in parallel emf stays, r divides."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        e = rng.choice((Fraction(3, 2), 2, 3, Fraction(9, 2), 6, 9, 12))
        r = rng.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 4), Fraction(1, 2), 1, 2))
        n = rng.choice([x for x in (2, 3, 4, 5, 6) if _exact(r / x)])
        series = rng.random() < 0.5
        cells = f"แบตเตอรี่เหมือนกัน {n} ก้อน แต่ละก้อนมีอีเอ็มเอฟ {show(e)} V ความต้านทานภายใน {show(r)} Ω ต่อแบบ{'อนุกรม' if series else 'ขนาน'}"
        hint = "อนุกรม: E รวม = nE, r รวม = nr   ขนาน (ก้อนเหมือนกัน): E รวม = E, r รวม = r/n"
        if rng.random() < 0.5:
            return numeric(stem=f"{cells} อีเอ็มเอฟสมมูลเท่าใด", answer=n * e if series else e,
                           wrongs=[e if series else n * e, e / n, n * e + 1], unit="V", topic=TOPIC_EMF, hint=hint)
        return numeric(stem=f"{cells} ความต้านทานภายในสมมูลเท่าใด", answer=n * r if series else r / n,
                       wrongs=[r / n if series else n * r, r, r * n * n], unit="Ω", topic=TOPIC_EMF, hint=hint)


@question_type(
    "phys.battery_emf_fluency",
    display_name={"th": "คำนวณกระแสไฟฟ้าและความต่างศักย์ที่ขั้วของแบตเตอรี่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EMF,
)
class BatteryEmfFluency(QuestionType):
    """I = E/(R + r), and the terminal voltage V = E − Ir."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        e, big_r, r = rng.choice([(e, R, r) for e in (3, 6, 9, 12, 24) for R in (1, 2, 3, 4, 5, 8, 10, 11, 20)
                                  for r in (Fraction(1, 2), 1, 2) if _exact(e / (R + r))])
        i = e / (big_r + r)
        given = f"แบตเตอรี่อีเอ็มเอฟ {e} V ความต้านทานภายใน {show(r)} Ω ต่อกับตัวต้านทาน {big_r} Ω"
        if rng.random() < 0.5:
            return numeric(stem=f"{given} กระแสไฟฟ้าในวงจรเท่าใด", answer=i,
                           wrongs=[Fraction(e, big_r), e / r, e / (big_r + r) * 2], unit="A", topic=TOPIC_EMF,
                           hint="I = E/(R + r) ความต้านทานภายในรวมอยู่ในวงจรด้วย")
        return numeric(stem=f"{given} ความต่างศักย์ระหว่างขั้วแบตเตอรี่เท่าใด", answer=e - i * r,
                       wrongs=[e, i * r, e + i * r], unit="V", topic=TOPIC_EMF,
                       hint="ความต่างศักย์ที่ขั้ว V = E − Ir = IR")


@question_type(
    "phys.battery_emf_application",
    display_name={"th": "กระแสไฟฟ้าในวงจรที่มีแบตเตอรี่หลายก้อนและตัวต้านทาน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EMF,
)
class BatteryEmfApplication(QuestionType):
    """Combine the cells first, then the whole loop: I = E_eq/(R + r_eq)."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        e, r, n, big_r, series = rng.choice(
            [(e, r, n, R, s) for e in (Fraction(3, 2), 2, 3, 6) for r in (Fraction(1, 2), 1, 2) for n in (2, 3, 4)
             for R in (1, 2, 3, 4, 5, 6, 9, 10) for s in (True, False)
             if _exact((n * e if s else e) / (R + (n * r if s else r / n))) and _exact(r / n)])
        e_eq, r_eq = (n * e, n * r) if series else (e, r / n)
        i = e_eq / (big_r + r_eq)
        return numeric(
            stem=(f"แบตเตอรี่เหมือนกัน {n} ก้อน แต่ละก้อนมีอีเอ็มเอฟ {show(e)} V ความต้านทานภายใน {show(r)} Ω "
                  f"ต่อแบบ{'อนุกรม' if series else 'ขนาน'} แล้วต่อกับตัวต้านทาน {big_r} Ω กระแสไฟฟ้าผ่านตัวต้านทานเท่าใด"),
            answer=i, wrongs=[e_eq / big_r, (e if series else n * e) / (big_r + (r if series else n * r)),
                              e / (big_r + r)],
            unit="A", topic=TOPIC_EMF, hint="หา E และ r สมมูลของแบตเตอรี่ก่อน แล้ว I = E_รวม ÷ (R + r_รวม)")
