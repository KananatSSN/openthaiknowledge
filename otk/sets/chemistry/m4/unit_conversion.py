"""หน่วยวัดและการเปลี่ยนหน่วยด้วยแฟกเตอร์เปลี่ยนหน่วย

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 3 ม.4/4

Sets moved here from: science_wave_f41.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f41 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_UNITS = "หน่วยวัดและการเปลี่ยนหน่วยด้วยแฟกเตอร์เปลี่ยนหน่วย"


# (from unit, to unit, factor to multiply by, quantity)
CONVERSIONS = (
    ("cm³", "dm³", Fraction(1, 1000), "ปริมาตร"), ("dm³", "cm³", Fraction(1000), "ปริมาตร"),
    ("mL", "L", Fraction(1, 1000), "ปริมาตร"), ("dm³", "m³", Fraction(1, 1000), "ปริมาตร"),
    ("g", "kg", Fraction(1, 1000), "มวล"), ("mg", "g", Fraction(1, 1000), "มวล"), ("kg", "g", Fraction(1000), "มวล"),
    ("atm", "mmHg", Fraction(760), "ความดัน"), ("mmHg", "atm", Fraction(1, 760), "ความดัน"),
    ("kPa", "Pa", Fraction(1000), "ความดัน"), ("nm", "m", Fraction(1, 10 ** 9), "ความยาว"),
    ("pm", "m", Fraction(1, 10 ** 12), "ความยาว"), ("kJ", "J", Fraction(1000), "พลังงาน"),
    ("min", "s", Fraction(60), "เวลา"), ("h", "s", Fraction(3600), "เวลา"),
)


SI_BASE = (("มวล", "กิโลกรัม (kg)"), ("ปริมาณสาร", "โมล (mol)"), ("อุณหภูมิ", "เคลวิน (K)"), ("ความยาว", "เมตร (m)"),
           ("เวลา", "วินาที (s)"), ("กระแสไฟฟ้า", "แอมแปร์ (A)"))


PREFIXES = (("กิโล (k)", "10³"), ("เซนติ (c)", "10⁻²"), ("มิลลิ (m)", "10⁻³"), ("ไมโคร (μ)", "10⁻⁶"),
            ("นาโน (n)", "10⁻⁹"), ("เมกะ (M)", "10⁶"))


@question_type(
    "chem.unit_conversion_foundation",
    display_name={"th": "หน่วยฐานเอสไอและคำนำหน้าหน่วย"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_UNITS,
)
class UnitConversionFoundation(QuestionType):
    """The seven base units, and what each prefix multiplies by."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            quantity, unit = rng.choice(SI_BASE)
            others = [u for q, u in SI_BASE if q != quantity] + ["ลิตร (L)", "องศาเซลเซียส (°C)", "กรัม (g)"]
            return _labelled(stem=f"หน่วยฐานเอสไอของ{quantity}คือข้อใด", correct=unit, wrongs=tuple(others),
                             topic=TOPIC_UNITS, hint="มวลใช้กิโลกรัม อุณหภูมิใช้เคลวิน ปริมาณสารใช้โมล")
        prefix, factor = rng.choice(PREFIXES)
        others = [f for p, f in PREFIXES if p != prefix]
        return _labelled(stem=f"คำนำหน้าหน่วย {prefix} มีค่าเท่าใด", correct=factor, wrongs=tuple(others),
                         topic=TOPIC_UNITS, hint="กิโล 10³ เซนติ 10⁻² มิลลิ 10⁻³ ไมโคร 10⁻⁶ นาโน 10⁻⁹")


@question_type(
    "chem.unit_conversion_fluency",
    display_name={"th": "เปลี่ยนหน่วยด้วยแฟกเตอร์เปลี่ยนหน่วย"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_UNITS,
)
class UnitConversionFluency(QuestionType):
    """Multiply by a factor whose top and bottom are equal amounts."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            src, dst, factor, _ = rng.choice([c for c in CONVERSIONS if c[2] >= Fraction(1, 1000)])
            value = Fraction(rng.randrange(1, 2000), rng.choice((1, 2, 4, 10)))
            answer = value * factor
            return (src, dst, factor, value, answer) if exact(answer) and exact(value) else None

        src, dst, factor, value, answer = _find(rng, draw)
        return numeric(stem=f"{show(value)} {src} เท่ากับกี่ {dst}", answer=answer,
                       wrongs=[value / factor if exact(value / factor) else answer * 10, answer * 10, answer / 10 if exact(answer / 10) else answer + 1],
                       unit=dst, topic=TOPIC_UNITS,
                       hint="คูณด้วยแฟกเตอร์เปลี่ยนหน่วยที่ให้หน่วยเดิมตัดกันเหลือหน่วยที่ต้องการ เช่น 1 dm³ / 1000 cm³")


@question_type(
    "chem.unit_conversion_application",
    display_name={"th": "เปลี่ยนหน่วยหลายขั้นและเปลี่ยนอุณหภูมิเป็นเคลวิน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_UNITS,
)
class UnitConversionApplication(QuestionType):
    """Chain factors, and K = °C + 273."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            c = rng.randrange(-50, 301)
            if rng.random() < 0.5:
                return numeric(stem=f"อุณหภูมิ {c} °C เท่ากับกี่เคลวิน", answer=c + 273, wrongs=[c - 273 if c - 273 > 0 else c + 300, c, c + 100],
                               unit="K", topic=TOPIC_UNITS, allow_negative=True, hint="K = °C + 273")
            k = c + 273
            return numeric(stem=f"อุณหภูมิ {k} K เท่ากับกี่องศาเซลเซียส", answer=c, wrongs=[k + 273, k, c + 10],
                           unit="°C", topic=TOPIC_UNITS, allow_negative=True, hint="°C = K − 273")
        if kind == 1:
            conc = Fraction(rng.randrange(1, 200), 10)
            answer = conc * 1000
            return numeric(stem=f"ความหนาแน่น {show(conc)} g/cm³ เท่ากับกี่ kg/m³", answer=answer,
                           wrongs=[conc / 1000 if exact(conc / 1000) else conc * 10, conc * 100, conc], unit="kg/m³",
                           topic=TOPIC_UNITS, hint="g/cm³ × (1 kg/1000 g) × (10⁶ cm³/1 m³) = × 1000")
        speed = rng.choice((18, 36, 54, 72, 90, 108, 144))
        return numeric(stem=f"อัตราการไหลของแก๊ส {speed} dm³/h เท่ากับกี่ cm³/s", answer=Fraction(speed * 1000, 3600),
                       wrongs=[Fraction(speed, 3600) * 100, speed * 1000, Fraction(speed, 60)], unit="cm³/s",
                       topic=TOPIC_UNITS, hint="dm³ → cm³ คูณ 1000 และ h → s หาร 3600")
