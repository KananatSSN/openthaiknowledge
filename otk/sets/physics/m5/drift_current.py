"""กระแสไฟฟ้าในลวดตัวนำและความเร็วลอยเลื่อนของอิเล็กตรอน

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.5/7

Sets moved here from: science_wave_f11.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f11 import SUBJECT, UPPER_FIVE, _exact

PROVENANCE = Provenance("original")


TOPIC_DRIFT = "กระแสไฟฟ้าในลวดตัวนำและความเร็วลอยเลื่อนของอิเล็กตรอน"


SUPERSCRIPT = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def _sci(mantissa, exponent: int) -> str:
    return f"{show(mantissa)} × 10{str(exponent).translate(SUPERSCRIPT)}"


DRIFT_FACTS = (
    ("อิเล็กตรอนอิสระในลวดโลหะที่ไม่มีกระแสไฟฟ้าเคลื่อนที่อย่างไร", "เคลื่อนที่แบบสุ่มทุกทิศทาง ความเร็วเฉลี่ยเป็นศูนย์",
     ("อยู่นิ่งกับที่", "เคลื่อนที่ไปทางเดียวกันทั้งหมด", "หมุนรอบนิวเคลียสเท่านั้น")),
    ("เมื่อต่อลวดกับแบตเตอรี่ อิเล็กตรอนอิสระเคลื่อนที่ไปทางใดโดยเฉลี่ย", "สวนทิศกับสนามไฟฟ้า ไปทางขั้วบวก",
     ("ทิศเดียวกับสนามไฟฟ้า ไปทางขั้วลบ", "ตั้งฉากกับลวด", "ไม่เคลื่อนที่")),
    ("ความเร็วลอยเลื่อนของอิเล็กตรอนในลวดมีค่าประมาณเท่าใด", "น้อยมาก ประมาณเศษส่วนของมิลลิเมตรต่อวินาที",
     ("ใกล้เคียงความเร็วแสง", "ประมาณ 340 m/s", "ประมาณ 1 km/s")),
    ("ความเร็วลอยเลื่อนช้ามาก แต่เปิดสวิตช์แล้วหลอดไฟสว่างทันที เพราะเหตุใด",
     "สนามไฟฟ้าเกิดตลอดลวดเกือบทันที อิเล็กตรอนทุกตัวในลวดจึงเริ่มเลื่อนพร้อมกัน",
     ("อิเล็กตรอนจากสวิตช์วิ่งไปถึงหลอดด้วยความเร็วแสง", "หลอดไฟมีอิเล็กตรอนสำรองอยู่แล้ว", "กระแสไฟฟ้าไม่ต้องใช้อิเล็กตรอน")),
    ("ทิศของกระแสไฟฟ้าสัมพันธ์กับทิศการเคลื่อนที่ของอิเล็กตรอนอย่างไร", "ตรงข้ามกัน",
     ("ทิศเดียวกัน", "ตั้งฉากกัน", "ไม่เกี่ยวข้องกัน")),
)


@question_type(
    "phys.drift_current_foundation",
    display_name={"th": "การเคลื่อนที่ของอิเล็กตรอนอิสระและกระแสไฟฟ้า I = Q/t"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_DRIFT,
)
class DriftCurrentFoundation(QuestionType):
    """Electrons wander and drift; current is charge per second."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            stem, correct, wrongs = rng.choice(DRIFT_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_DRIFT,
                             hint="อิเล็กตรอนเคลื่อนที่สุ่มอยู่แล้ว สนามไฟฟ้าทำให้เลื่อนไปทางหนึ่งอย่างช้า ๆ")
        if shape == 1:
            q = rng.randint(1, 60) * 5
            t = rng.choice([x for x in (2, 4, 5, 10, 20, 25, 50, 60) if _exact(Fraction(q, x))])
            return numeric(stem=f"ประจุ {q} C ผ่านภาคตัดขวางของลวดในเวลา {t} s กระแสไฟฟ้าเท่าใด",
                           answer=Fraction(q, t), wrongs=[q * t, Fraction(t, q), q], unit="A", topic=TOPIC_DRIFT,
                           hint="I = Q/t")
        k = rng.randint(1, 9)
        exponent = rng.randint(18, 20)
        current = Fraction(16 * k, 10) * Fraction(10) ** (exponent - 19)
        return _labelled(
            stem=f"ลวดมีกระแสไฟฟ้า {show(current)} A มีอิเล็กตรอนผ่านภาคตัดขวางกี่ตัวในหนึ่งวินาที (e = 1.6 × 10⁻¹⁹ C)",
            correct=f"{_sci(k, exponent)} ตัว",
            wrongs=(f"{_sci(k, exponent - 1)} ตัว", f"{_sci(Fraction(16 * k, 10), exponent)} ตัว", f"{_sci(k, -exponent)} ตัว"),
            topic=TOPIC_DRIFT, hint="จำนวนอิเล็กตรอนต่อวินาที = I ÷ e")


@question_type(
    "phys.drift_current_fluency",
    display_name={"th": "คำนวณความเร็วลอยเลื่อนจาก I = nevA"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_DRIFT,
)
class DriftCurrentFluency(QuestionType):
    """v = I/(neA) with n = 5 × 10²⁸ m⁻³, and the current back from a drift speed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        area = rng.choice((Fraction(1, 2), 1, 2, Fraction(5, 2), 4, 5))
        speed = rng.choice([x for x in (Fraction(1, 20), Fraction(1, 10), Fraction(1, 5), Fraction(1, 4),
                                        Fraction(1, 2), Fraction(3, 4), 1, 2) if _exact(8 * area * x)])
        current = 8 * area * speed
        given = "(n = 5 × 10²⁸ ต่อลูกบาศก์เมตร, e = 1.6 × 10⁻¹⁹ C)"
        if rng.random() < 0.6:
            return numeric(
                stem=(f"ลวดทองแดงพื้นที่หน้าตัด {show(area)} mm² มีกระแสไฟฟ้า {show(current)} A "
                      f"ความเร็วลอยเลื่อนของอิเล็กตรอนกี่มิลลิเมตรต่อวินาที {given}"),
                answer=speed, wrongs=[speed * 10, speed * 1000, current / area], unit="mm/s", topic=TOPIC_DRIFT,
                hint="v = I/(neA) โดย A เป็นตารางเมตร (1 mm² = 10⁻⁶ m²) แล้วแปลงเป็นมิลลิเมตรต่อวินาที")
        return numeric(
            stem=(f"อิเล็กตรอนในลวดพื้นที่หน้าตัด {show(area)} mm² มีความเร็วลอยเลื่อน {show(speed)} mm/s "
                  f"ลวดมีกระแสไฟฟ้าเท่าใด {given}"),
            answer=current, wrongs=[current * 10, current / 10, current * 1000], unit="A", topic=TOPIC_DRIFT,
            hint="I = nevA ระวังหน่วย mm/s และ mm²")


@question_type(
    "phys.drift_current_application",
    display_name={"th": "ความเร็วลอยเลื่อนเมื่อพื้นที่หน้าตัดหรือกระแสไฟฟ้าเปลี่ยน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_DRIFT,
)
class DriftCurrentApplication(QuestionType):
    """Same current through a thinner section drifts faster; more current drifts faster."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        v = rng.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 4), Fraction(1, 2), 1, 2, 3, 4))
        if rng.random() < 0.5:
            a1, a2 = rng.choice([p for p in ((2, 1), (4, 1), (3, 1), (4, 2), (5, 1), (6, 2), (1, 2), (2, 4), (1, 4))
                                 if _exact(v * p[0] / p[1])])
            return numeric(
                stem=(f"ลวดโลหะชนิดเดียวกันสองช่วงต่ออนุกรมกัน ช่วงแรกพื้นที่หน้าตัด {a1} mm² อิเล็กตรอนมีความเร็วลอยเลื่อน "
                      f"{show(v)} mm/s ช่วงที่สองพื้นที่หน้าตัด {a2} mm² ความเร็วลอยเลื่อนในช่วงที่สองเท่าใด"),
                answer=v * a1 / a2, wrongs=[v * a2 / a1, v, v * a1 * a2], unit="mm/s", topic=TOPIC_DRIFT,
                hint="ต่ออนุกรมกระแสเท่ากัน I = nevA คงตัว ความเร็วลอยเลื่อนแปรผกผันกับพื้นที่หน้าตัด")
        factor = rng.choice([f for f in (2, 3, 4, Fraction(1, 2)) if _exact(v * f)])
        change = f"เพิ่มเป็น {factor} เท่า" if factor > 1 else "ลดลงครึ่งหนึ่ง"
        return numeric(
            stem=(f"อิเล็กตรอนในลวดเส้นหนึ่งมีความเร็วลอยเลื่อน {show(v)} mm/s ถ้ากระแสไฟฟ้าในลวดเส้นเดิม{change} "
                  "ความเร็วลอยเลื่อนเป็นเท่าใด"),
            answer=v * factor, wrongs=[v / factor, v, v * factor * factor], unit="mm/s", topic=TOPIC_DRIFT,
            hint="ลวดเส้นเดิม n, e, A คงตัว ความเร็วลอยเลื่อนแปรผันตรงกับกระแสไฟฟ้า")
