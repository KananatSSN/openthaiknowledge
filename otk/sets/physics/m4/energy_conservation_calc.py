"""กฎการอนุรักษ์พลังงานกล

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/12

Sets moved here from: science_wave_f4.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import G, numeric, show
from otk.sets._support.science_wave_f4 import DROPS, SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_CONSERVE = "กฎการอนุรักษ์พลังงานกล"


@question_type(
    "phys.energy_conservation_calc_foundation",
    display_name={"th": "พลังงานกลในการเคลื่อนที่ที่ไม่มีแรงต้าน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CONSERVE,
)
class EnergyConservationCalcFoundation(QuestionType):
    """Mechanical energy as a total that stays put while its parts trade."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        m = rng.randint(1, 10)
        h = rng.randint(2, 20)
        top = m * G * h
        if rng.random() < 0.5:
            where = rng.choice(("กึ่งกลางทาง", "จุดต่ำสุด", "ความสูงหนึ่งในสี่ของความสูงเดิม"))
            return numeric(
                stem=(f"ปล่อยวัตถุมวล {m} kg จากความสูง {h} m ให้ตกอิสระโดยไม่มีแรงต้าน พลังงานกลของวัตถุ"
                      f"ที่{where}เท่าใด (g = 10 m/s²)"),
                answer=top, wrongs=[Fraction(top, 2), 0, Fraction(top, 4)], unit="J", topic=TOPIC_CONSERVE,
                hint="เมื่อไม่มีแรงต้าน พลังงานกลคงตัวทุกตำแหน่ง")
        frac = rng.choice((Fraction(1, 2), Fraction(1, 4), Fraction(3, 4)))
        return numeric(
            stem=(f"ปล่อยวัตถุมวล {m} kg จากความสูง {h} m โดยไม่มีแรงต้าน เมื่อตกลงมาได้ {show(frac * 100)}% "
                  "ของความสูงเดิม วัตถุมีพลังงานจลน์เท่าใด (g = 10 m/s²)"),
            answer=top * frac, wrongs=[top * (1 - frac), top, top * frac / 2], unit="J", topic=TOPIC_CONSERVE,
            hint="พลังงานจลน์ที่ได้เท่ากับพลังงานศักย์ที่ลดลง คือ mg × ระยะที่ตกลงมา")


@question_type(
    "phys.energy_conservation_calc_fluency",
    display_name={"th": "ใช้กฎการอนุรักษ์พลังงานกลหาความเร็วและความสูง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CONSERVE,
)
class EnergyConservationCalcFluency(QuestionType):
    """mgh = ½mv², forwards and backwards, and a spring's launch."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        h, v = rng.choice(DROPS)
        what = rng.choice(("ลูกตุ้มแกว่งจากจุดสูงสุด", "เด็กไถลลงสไลเดอร์ลื่น", "รถรางเลื่อนลงจากยอดราง"))
        if shape == 0:
            return numeric(
                stem=(f"{what}ซึ่งสูงกว่าจุดต่ำสุด {show(h)} m เริ่มจากหยุดนิ่ง เมื่อถึงจุดต่ำสุดมีอัตราเร็วเท่าใด "
                      "(g = 10 m/s² ไม่คิดแรงต้าน)"),
                answer=v, wrongs=[2 * G * h, G * h, v * 2], unit="m/s", topic=TOPIC_CONSERVE,
                hint="mgh = ½mv² ดังนั้น v = √(2gh) ไม่ขึ้นกับมวล")
        if shape == 1:
            return numeric(
                stem=f"โยนลูกบอลขึ้นในแนวดิ่งด้วยอัตราเร็ว {v} m/s ลูกบอลขึ้นไปได้สูงสุดเท่าใด (g = 10 m/s² ไม่คิดแรงต้าน)",
                answer=h, wrongs=[h * 2, Fraction(v, G), Fraction(v * v, G)], unit="m", topic=TOPIC_CONSERVE,
                hint="½mv² = mgh ดังนั้น h = v²/2g")
        # Only launches whose height is exact to the centimetre.
        m, k, x = rng.choice([(Fraction(mm, 10), kk, Fraction(xx, 10))
                              for mm in (1, 2, 5) for kk in (100, 200, 250, 400, 500, 1000)
                              for xx in range(1, 11)
                              if (Fraction(kk * xx * xx, 200) / (Fraction(mm, 10) * G) * 100).denominator == 1])
        height = k * x * x / 2 / (m * G)
        return numeric(
            stem=(f"สปริงค่านิจ {k} N/m ถูกอัดเข้าไป {show(x)} m แล้วดีดลูกบอลมวล {show(m)} kg ขึ้นในแนวดิ่ง "
                  "ลูกบอลขึ้นไปได้สูงเท่าใด (g = 10 m/s² ไม่คิดแรงต้าน)"),
            answer=height, wrongs=[k * x * x / (m * G), k * x / (m * G), height * 10], unit="m",
            topic=TOPIC_CONSERVE, hint="พลังงานศักย์ยืดหยุ่นกลายเป็นพลังงานศักย์โน้มถ่วง: ½kx² = mgh")


@question_type(
    "phys.energy_conservation_calc_application",
    display_name={"th": "พลังงานกลที่หายไปเมื่อมีแรงเสียดทาน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CONSERVE,
)
class EnergyConservationCalcApplication(QuestionType):
    """Where the conservation law stops holding: friction takes a measured share."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        m = rng.randint(2, 10) * 5
        h, v_ideal = rng.choice(DROPS[3:])
        v = rng.choice([x for x in range(2, v_ideal) if x % 2 == 0] or [2])
        lost = m * G * h - Fraction(m * v * v, 2)
        if rng.random() < 0.5:
            return numeric(
                stem=(f"เด็กมวล {m} kg ไถลลงสไลเดอร์สูง {show(h)} m จากหยุดนิ่ง ถึงปลายล่างด้วยอัตราเร็ว {v} m/s "
                      "พลังงานที่สูญเสียไปกับแรงเสียดทานเท่าใด (g = 10 m/s²)"),
                answer=lost, wrongs=[m * G * h, Fraction(m * v * v, 2), m * G * h + Fraction(m * v * v, 2)],
                unit="J", topic=TOPIC_CONSERVE,
                hint="พลังงานที่สูญเสีย = พลังงานศักย์ที่ปลายบน − พลังงานจลน์ที่ปลายล่าง")
        length = rng.choice([x for x in (2, 4, 5, 8, 10, 20) if lost % x == 0] or [1])
        return numeric(
            stem=(f"เด็กมวล {m} kg ไถลลงสไลเดอร์สูง {show(h)} m ยาว {length} m จากหยุดนิ่ง ถึงปลายล่างด้วย"
                  f"อัตราเร็ว {v} m/s แรงเสียดทานเฉลี่ยตลอดทางเท่าใด (g = 10 m/s²)"),
            answer=lost / length, wrongs=[lost, m * G * h / length, Fraction(m * v * v, 2) / length],
            unit="N", topic=TOPIC_CONSERVE,
            hint="งานของแรงเสียดทาน = พลังงานกลที่หายไป แล้วหารด้วยระยะทางที่ไถล")
