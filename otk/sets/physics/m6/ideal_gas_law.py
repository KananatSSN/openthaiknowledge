"""กฎของแก๊สอุดมคติ

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/7

Sets moved here from: science_wave_f16.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_f16 import SUBJECT, UPPER_SIX, _exact

PROVENANCE = Provenance("original")


TOPIC_GAS = "กฎของแก๊สอุดมคติ"


R_GAS = Fraction(831, 100)


@question_type(
    "phys.ideal_gas_law_foundation",
    display_name={"th": "อุณหภูมิเคลวินและกฎของบอยล์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GAS,
)
class IdealGasLawFoundation(QuestionType):
    """T(K) = T(°C) + 273, and P₁V₁ = P₂V₂ at constant temperature."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            c = rng.randint(-50, 200)
            return numeric(stem=f"แก๊สมีอุณหภูมิ {c} °C คิดเป็นอุณหภูมิกี่เคลวิน", answer=c + 273,
                           wrongs=[c - 273 if c > 273 else 273 - c, c + 100, c + 373], unit="K", topic=TOPIC_GAS,
                           hint="T(K) = T(°C) + 273 กฎของแก๊สต้องใช้อุณหภูมิเคลวินเสมอ")
        p1 = rng.randint(1, 10) * 50
        v1 = rng.randint(1, 20)
        v2 = rng.choice([x for x in range(1, 41) if x != v1 and _exact(Fraction(p1 * v1, x))])
        return numeric(
            stem=f"แก๊สในกระบอกสูบมีความดัน {p1} kPa ปริมาตร {v1} L อัดหรือขยายให้ปริมาตรเป็น {v2} L โดยอุณหภูมิคงตัว ความดันใหม่เท่าใด",
            answer=Fraction(p1 * v1, v2), wrongs=[Fraction(p1 * v2, v1), p1, Fraction(p1 * v1, v2) * 2], unit="kPa",
            topic=TOPIC_GAS, hint="กฎของบอยล์: อุณหภูมิคงตัว P₁V₁ = P₂V₂")


@question_type(
    "phys.ideal_gas_law_fluency",
    display_name={"th": "กฎของชาร์ลและกฎของเกย์-ลูสแซก"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GAS,
)
class IdealGasLawFluency(QuestionType):
    """V/T and P/T constant, with temperatures given in °C to convert."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        t1c, t2c = rng.sample([k - 273 for k in range(250, 601, 25)], 2)
        t1, t2 = t1c + 273, t2c + 273
        if rng.random() < 0.5:
            v1 = rng.choice([x for x in range(1, 41) if _exact(Fraction(x * t2, t1))])
            return numeric(
                stem=f"แก๊สปริมาตร {v1} L ที่ {t1c} °C เปลี่ยนอุณหภูมิเป็น {t2c} °C โดยความดันคงตัว ปริมาตรใหม่กี่ลิตร",
                answer=Fraction(v1 * t2, t1), wrongs=[Fraction(v1 * t2c, t1c) if t1c and _exact(Fraction(v1 * t2c, t1c)) else v1 * 2,
                                                      Fraction(v1 * t1, t2), v1],
                unit="L", topic=TOPIC_GAS, hint="กฎของชาร์ล V₁/T₁ = V₂/T₂ โดย T เป็นเคลวิน (บวก 273 ก่อน)")
        p1 = rng.choice([x for x in range(50, 501, 10) if _exact(Fraction(x * t2, t1))])
        return numeric(
            stem=f"ถังปิดบรรจุแก๊สความดัน {p1} kPa ที่ {t1c} °C เมื่ออุณหภูมิเปลี่ยนเป็น {t2c} °C ความดันเป็นกี่กิโลพาสคัล",
            answer=Fraction(p1 * t2, t1), wrongs=[Fraction(p1 * t1, t2), p1, Fraction(p1 * t2, t1) + 100], unit="kPa",
            topic=TOPIC_GAS, hint="ปริมาตรคงตัว P₁/T₁ = P₂/T₂ โดย T เป็นเคลวิน")


@question_type(
    "phys.ideal_gas_law_application",
    display_name={"th": "กฎรวมของแก๊สและสมการ PV = nRT"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GAS,
)
class IdealGasLawApplication(QuestionType):
    """P₁V₁/T₁ = P₂V₂/T₂, and PV = nRT with R = 8.31."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            n = rng.choice((Fraction(1, 2), 1, 2, 3, 4, 5))
            t = rng.choice((200, 250, 300, 400, 500, 600))
            v = rng.choice([x for x in (Fraction(1, 100), Fraction(1, 50), Fraction(1, 20), Fraction(1, 10), Fraction(1, 5), 1)
                            if _exact(n * R_GAS * t / x)])
            pressure = n * R_GAS * t / v
            return numeric(
                stem=f"แก๊สอุดมคติ {show(n)} โมล อุณหภูมิ {t} K บรรจุในภาชนะปริมาตร {show(v)} m³ มีความดันกี่ปาสคัล (R = 8.31 J/mol·K)",
                answer=pressure, wrongs=[pressure / 1000, n * R_GAS * t, pressure * 2], unit="Pa", topic=TOPIC_GAS,
                hint="PV = nRT ดังนั้น P = nRT/V")
        p1, v1, t1, p2, t2 = rng.choice([(p1, v1, t1, p2, t2) for p1 in (100, 150, 200, 300) for v1 in (2, 3, 4, 6, 10)
                                         for t1 in (250, 300, 400) for p2 in (100, 200, 250, 400, 500) for t2 in (300, 350, 400, 600)
                                         if p1 != p2 and _exact(Fraction(p1 * v1 * t2, t1 * p2))])
        v2 = Fraction(p1 * v1 * t2, t1 * p2)
        return numeric(
            stem=(f"แก๊สมีความดัน {p1} kPa ปริมาตร {v1} L อุณหภูมิ {t1} K เปลี่ยนเป็นความดัน {p2} kPa อุณหภูมิ {t2} K "
                  "ปริมาตรใหม่กี่ลิตร"),
            answer=v2, wrongs=[Fraction(p1 * v1, p2), Fraction(v1 * t2, t1), Fraction(p2 * v1 * t1, p1 * t2)
                               if _exact(Fraction(p2 * v1 * t1, p1 * t2)) else v2 * 2],
            unit="L", topic=TOPIC_GAS, hint="กฎรวมของแก๊ส P₁V₁/T₁ = P₂V₂/T₂")
