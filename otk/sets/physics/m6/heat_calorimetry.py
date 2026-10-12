"""ความร้อนกับการเปลี่ยนอุณหภูมิและสถานะของสสาร

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/1

Sets moved here from: science_wave_f14.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_f14 import SUBJECT, UPPER_SIX, _exact

PROVENANCE = Provenance("original")


TOPIC_HEAT = "ความร้อนกับการเปลี่ยนอุณหภูมิและสถานะของสสาร"


WATER_C = 4200


ICE_L = 336000


STEAM_L = 2260000


@question_type(
    "phys.heat_calorimetry_foundation",
    display_name={"th": "ความร้อนที่ทำให้สสารเปลี่ยนอุณหภูมิ Q = mcΔT"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HEAT,
)
class HeatCalorimetryFoundation(QuestionType):
    """Q = mcΔT for water and for a metal whose c is stated."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            m = Fraction(rng.randint(1, 20), 10)
            t1 = rng.randint(10, 40)
            t2 = t1 + rng.randint(5, 60)
            q = m * WATER_C * (t2 - t1)
            return numeric(
                stem=f"ต้มน้ำมวล {show(m)} kg จาก {t1} °C เป็น {t2} °C ต้องใช้ความร้อนกี่จูล (c ของน้ำ = 4,200 J/kg·K)",
                answer=q, wrongs=[m * WATER_C * t2, q / 1000, m * (t2 - t1)], unit="J", topic=TOPIC_HEAT,
                hint="Q = mcΔT โดย ΔT = อุณหภูมิสุดท้าย − อุณหภูมิเริ่มต้น")
        metal, c = rng.choice((("อะลูมิเนียม", 900), ("ทองแดง", 390), ("เหล็ก", 450), ("ตะกั่ว", 130)))
        m = Fraction(rng.randint(1, 20), 10)
        dt = rng.randint(2, 20) * 5
        q = m * c * dt
        return numeric(
            stem=f"ก้อน{metal}มวล {show(m)} kg ได้รับความร้อน {show(q)} J อุณหภูมิเพิ่มขึ้นกี่เคลวิน (c ของ{metal} = {c} J/kg·K)",
            answer=dt, wrongs=[dt * 2, Fraction(dt, 2), q / c], unit="K", topic=TOPIC_HEAT,
            hint="ΔT = Q ÷ (mc)")


@question_type(
    "phys.heat_calorimetry_fluency",
    display_name={"th": "ความร้อนแฝงและความร้อนที่ใช้เปลี่ยนทั้งอุณหภูมิและสถานะ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HEAT,
)
class HeatCalorimetryFluency(QuestionType):
    """Q = mL, and melting ice then warming the water."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        m = Fraction(rng.randint(1, 20), 20)
        if rng.random() < 0.4:
            boil = rng.random() < 0.5
            latent = STEAM_L if boil else ICE_L
            what = "เปลี่ยนน้ำที่ 100 °C เป็นไอน้ำที่ 100 °C" if boil else "หลอมน้ำแข็งที่ 0 °C เป็นน้ำที่ 0 °C"
            name = "ความร้อนแฝงของการกลายเป็นไอ 2,260,000 J/kg" if boil else "ความร้อนแฝงของการหลอมเหลว 336,000 J/kg"
            return numeric(
                stem=f"{what} มวล {show(m)} kg ต้องใช้ความร้อนกี่จูล ({name})",
                answer=m * latent, wrongs=[m * latent / 1000, latent, m * WATER_C * 100], unit="J", topic=TOPIC_HEAT,
                hint="ขณะเปลี่ยนสถานะอุณหภูมิคงตัว Q = mL")
        t = rng.randint(1, 20) * 5
        q = m * ICE_L + m * WATER_C * t
        return numeric(
            stem=(f"น้ำแข็งมวล {show(m)} kg ที่ 0 °C ได้รับความร้อนจนกลายเป็นน้ำที่ {t} °C ต้องใช้ความร้อนทั้งหมดกี่จูล "
                  "(ความร้อนแฝงของการหลอมเหลว 336,000 J/kg, c ของน้ำ = 4,200 J/kg·K)"),
            answer=q, wrongs=[m * ICE_L, m * WATER_C * t, m * ICE_L - m * WATER_C * t], unit="J", topic=TOPIC_HEAT,
            hint="แบ่งเป็นสองช่วง: หลอมเหลว mL แล้วเพิ่มอุณหภูมิ mcΔT นำมารวมกัน")


@question_type(
    "phys.heat_calorimetry_application",
    display_name={"th": "การถ่ายโอนความร้อนตามกฎการอนุรักษ์พลังงาน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HEAT,
)
class HeatCalorimetryApplication(QuestionType):
    """Heat lost = heat gained: mixing water, and a hot metal dropped in water."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            m1, t1, m2, t2 = rng.choice([(a, x, b, y) for a in (1, 2, 3, 4, 5) for b in (1, 2, 3, 4, 5)
                                         for x in range(60, 101, 10) for y in range(10, 41, 10)
                                         if _exact(Fraction(a * x + b * y, a + b))])
            final = Fraction(m1 * t1 + m2 * t2, m1 + m2)
            return numeric(
                stem=(f"ผสมน้ำร้อน {show(Fraction(m1, 10))} kg อุณหภูมิ {t1} °C กับน้ำเย็น {show(Fraction(m2, 10))} kg "
                      f"อุณหภูมิ {t2} °C ในภาชนะที่ไม่รับความร้อน อุณหภูมิสุดท้ายเท่าใด"),
                answer=final, wrongs=[Fraction(t1 + t2, 2), Fraction(t1 - t2, 2), final + 10], unit="°C", topic=TOPIC_HEAT,
                hint="ความร้อนที่น้ำร้อนให้ = ความร้อนที่น้ำเย็นรับ: m₁c(T₁ − T) = m₂c(T − T₂)")
        metal, c = rng.choice((("อะลูมิเนียม", 900), ("ทองแดง", 390), ("เหล็ก", 450)))
        mm, tm, mw, tw, final = rng.choice(
            [(Fraction(a, 10), x, Fraction(b, 10), y, f) for a in (1, 2, 4, 5) for b in (1, 2, 4, 5, 10)
             for x in (100, 150, 200) for y in (20, 25, 30) for f in range(y + 1, 60)
             if Fraction(a, 10) * c * (x - f) == Fraction(b, 10) * WATER_C * (f - y)])
        return numeric(
            stem=(f"นำก้อน{metal}มวล {show(mm)} kg อุณหภูมิ {tm} °C ใส่ลงในน้ำ {show(mw)} kg อุณหภูมิ {tw} °C "
                  f"อุณหภูมิสุดท้ายของน้ำเท่าใด (c ของ{metal} = {c} J/kg·K, c ของน้ำ = 4,200 J/kg·K ไม่คิดความร้อนที่ภาชนะรับ)"),
            answer=final, wrongs=[Fraction(tm + tw, 2), final + 5, tw + (tm - tw) * Fraction(c, WATER_C)],
            unit="°C", topic=TOPIC_HEAT, hint="m_โลหะ c_โลหะ (T_โลหะ − T) = m_น้ำ c_น้ำ (T − T_น้ำ)")
