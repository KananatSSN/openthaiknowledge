"""ทฤษฎีจลน์ของแก๊สและอัตราเร็วอาร์เอ็มเอส

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/8

Sets moved here from: science_wave_f16.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f16 import PRESSURE_DENSITY, SUBJECT, UPPER_SIX, _exact, _sci

PROVENANCE = Provenance("original")


TOPIC_KINETIC = "ทฤษฎีจลน์ของแก๊สและอัตราเร็วอาร์เอ็มเอส"


KINETIC_FACTS = (
    ("ข้อใดเป็นสมมติฐานของแบบจำลองแก๊สอุดมคติ", "โมเลกุลเคลื่อนที่แบบสุ่ม ชนกันแบบยืดหยุ่น และไม่มีแรงกระทำต่อกันยกเว้นขณะชน",
     ("โมเลกุลอยู่นิ่งและดึงดูดกันตลอดเวลา", "โมเลกุลมีขนาดใหญ่เทียบกับระยะห่าง", "โมเลกุลชนกันแบบไม่ยืดหยุ่นเสมอ")),
    ("ความดันของแก๊สในภาชนะเกิดจากอะไร", "โมเลกุลของแก๊สชนผนังภาชนะแล้วเปลี่ยนโมเมนตัม",
     ("น้ำหนักของโมเลกุลกดก้นภาชนะเท่านั้น", "โมเลกุลดึงดูดผนังภาชนะ", "ความร้อนจากผนังภาชนะ")),
    ("พลังงานจลน์เฉลี่ยของโมเลกุลแก๊สขึ้นกับปริมาณใด", "อุณหภูมิเคลวินของแก๊สเท่านั้น",
     ("ชนิดของแก๊สเท่านั้น", "ปริมาตรของภาชนะ", "จำนวนโมเลกุล")),
    ("แก๊สสองชนิดที่อุณหภูมิเท่ากัน โมเลกุลของแก๊สชนิดใดมีอัตราเร็วอาร์เอ็มเอสมากกว่า", "แก๊สที่มีมวลโมเลกุลน้อยกว่า",
     ("แก๊สที่มีมวลโมเลกุลมากกว่า", "มีอัตราเร็วเท่ากัน", "แก๊สที่อยู่ในภาชนะใหญ่กว่า")),
)


@question_type(
    "phys.kinetic_gas_foundation",
    display_name={"th": "แบบจำลองแก๊สอุดมคติและพลังงานจลน์เฉลี่ยของโมเลกุล"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_KINETIC,
)
class KineticGasFoundation(QuestionType):
    """The model's assumptions, and Ē = (3/2)kT."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            stem, correct, wrongs = rng.choice(KINETIC_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_KINETIC,
                             hint="แก๊สอุดมคติ: โมเลกุลเล็กมาก เคลื่อนที่สุ่ม ชนแบบยืดหยุ่น พลังงานจลน์เฉลี่ยขึ้นกับอุณหภูมิเท่านั้น")
        if rng.random() < 0.5:
            t1, t2 = rng.sample(range(100, 1001, 100), 2)
            e1 = Fraction(207, 100) * t1 / 100
            return numeric(
                stem=(f"โมเลกุลแก๊สที่ {t1} K มีพลังงานจลน์เฉลี่ย {show(e1)} × 10⁻²¹ J ที่อุณหภูมิ {t2} K "
                      "พลังงานจลน์เฉลี่ยเท่าใด (ตอบในหน่วย × 10⁻²¹ J)"),
                answer=e1 * t2 / t1, wrongs=[e1 * t1 / t2, e1, e1 * t2 / t1 * 2], unit="× 10⁻²¹ J", topic=TOPIC_KINETIC,
                hint="Ē = (3/2)kT แปรผันตรงกับอุณหภูมิเคลวิน")
        t = rng.choice((100, 200, 300, 400))
        mantissa = Fraction(207, 100) * t / 100
        return _labelled(
            stem=f"แก๊สอุณหภูมิ {t} K พลังงานจลน์เฉลี่ยต่อโมเลกุลเท่าใด (k = 1.38 × 10⁻²³ J/K)",
            correct=f"{_sci(mantissa, -21)} J",
            wrongs=(f"{_sci(mantissa * 2 / 3, -21)} J", f"{_sci(mantissa, -23)} J", f"{_sci(mantissa * 2, -21)} J"),
            topic=TOPIC_KINETIC, hint="Ē = (3/2)kT")


@question_type(
    "phys.kinetic_gas_fluency",
    display_name={"th": "พลังงานจลน์เฉลี่ยและอัตราเร็วอาร์เอ็มเอสเมื่ออุณหภูมิหรือมวลโมเลกุลเปลี่ยน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_KINETIC,
)
class KineticGasFluency(QuestionType):
    """Ē ∝ T; v_rms ∝ √(T/M)."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            t1 = rng.choice((100, 150, 200, 250, 300, 400))
            factor = rng.choice((2, 3, 4, Fraction(1, 2)))
            return numeric(
                stem=f"แก๊สที่ {t1} K เพิ่มอุณหภูมิเป็น {show(t1 * factor)} K พลังงานจลน์เฉลี่ยของโมเลกุลเป็นกี่เท่าของเดิม",
                answer=factor, wrongs=[factor * factor, 1 / Fraction(factor) if factor != 1 else 2, factor + 1],
                unit="เท่า", topic=TOPIC_KINETIC, hint="Ē = (3/2)kT แปรผันตรงกับอุณหภูมิเคลวิน")
        if shape == 1:
            k = rng.choice((2, 3, 4))
            t1 = rng.choice((100, 200, 300))
            v1 = rng.randint(2, 10) * 50
            return numeric(
                stem=f"โมเลกุลแก๊สที่ {t1} K มีอัตราเร็วอาร์เอ็มเอส {v1} m/s ถ้าอุณหภูมิเป็น {t1 * k * k} K อัตราเร็วอาร์เอ็มเอสเท่าใด",
                answer=v1 * k, wrongs=[v1 * k * k, v1, v1 * k * 2], unit="m/s", topic=TOPIC_KINETIC,
                hint="v_rms = √(3kT/m) แปรผันตรงกับรากที่สองของอุณหภูมิ")
        # Only pairs whose mass ratio is a perfect square.
        gas_a, m_a, gas_b, m_b, ratio = rng.choice((("ไฮโดรเจน", 2, "ออกซิเจน", 32, 4), ("ฮีเลียม", 4, "มีเทน", 16, 2),
                                                    ("มีเทน", 16, "ซัลเฟอร์ไดออกไซด์", 64, 2),
                                                    ("ฮีเลียม", 4, "ซัลเฟอร์ไดออกไซด์", 64, 4)))
        assert m_b == m_a * ratio * ratio
        return numeric(
            stem=(f"ที่อุณหภูมิเดียวกัน อัตราเร็วอาร์เอ็มเอสของโมเลกุล{gas_a} (มวลโมเลกุล {m_a}) เป็นกี่เท่าของ{gas_b} "
                  f"(มวลโมเลกุล {m_b})"),
            answer=ratio, wrongs=[ratio * ratio, Fraction(1, ratio), ratio * 2], unit="เท่า", topic=TOPIC_KINETIC,
            hint="v_rms แปรผกผันกับรากที่สองของมวลโมเลกุล: v_A/v_B = √(M_B/M_A)")


@question_type(
    "phys.kinetic_gas_application",
    display_name={"th": "คำนวณอัตราเร็วอาร์เอ็มเอสจากความดันและความหนาแน่นของแก๊ส"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_KINETIC,
)
class KineticGasApplication(QuestionType):
    """v_rms = √(3P/ρ), and the density back from a measured speed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            rho, v = rng.choice([(Fraction(k, 10), m * 100) for k in range(1, 51) for m in range(1, 11)
                                 if _exact(Fraction(k, 10) * (m * 100) ** 2 / 3 / 1000)])
            pressure = rho * v * v / 3 / 1000
            return numeric(
                stem=f"แก๊สมีความหนาแน่น {show(rho)} kg/m³ โมเลกุลมีอัตราเร็วอาร์เอ็มเอส {v} m/s แก๊สมีความดันกี่กิโลพาสคัล",
                answer=pressure, wrongs=[pressure * 3, pressure * 1000, rho * v / 3], unit="kPa", topic=TOPIC_KINETIC,
                hint="P = (1/3)ρv²_rms แล้วแปลงปาสคัลเป็นกิโลพาสคัล")
        p, rho, v = rng.choice(PRESSURE_DENSITY)
        if rng.random() < 0.6:
            return numeric(
                stem=f"แก๊สมีความดัน {p} kPa และความหนาแน่น {show(rho)} kg/m³ อัตราเร็วอาร์เอ็มเอสของโมเลกุลเท่าใด",
                answer=v, wrongs=[v * v, v * 2, Fraction(v, 2)], unit="m/s", topic=TOPIC_KINETIC,
                hint="จาก P = (1/3)ρv²_rms จะได้ v_rms = √(3P/ρ) (P เป็นปาสคัล)")
        return numeric(
            stem=f"โมเลกุลแก๊สที่ความดัน {p} kPa มีอัตราเร็วอาร์เอ็มเอส {v} m/s แก๊สมีความหนาแน่นกี่กิโลกรัมต่อลูกบาศก์เมตร",
            answer=rho, wrongs=[rho * 3, rho / 3, rho * 10], unit="kg/m³", topic=TOPIC_KINETIC,
            hint="ρ = 3P/v²_rms")
