"""การคำนวณอัตราการเกิดปฏิกิริยาเคมี

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/2

Sets moved here from: science_wave_f32.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f32 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_CALC = "การคำนวณอัตราการเกิดปฏิกิริยาเคมี"


# (equation, species with coefficient, which are products)
RATE_EQUATIONS = (
    ("2H₂O₂ → 2H₂O + O₂", {"H₂O₂": 2, "H₂O": 2, "O₂": 1}, {"H₂O", "O₂"}),
    ("N₂ + 3H₂ → 2NH₃", {"N₂": 1, "H₂": 3, "NH₃": 2}, {"NH₃"}),
    ("2SO₂ + O₂ → 2SO₃", {"SO₂": 2, "O₂": 1, "SO₃": 2}, {"SO₃"}),
    ("2N₂O₅ → 4NO₂ + O₂", {"N₂O₅": 2, "NO₂": 4, "O₂": 1}, {"NO₂", "O₂"}),
    ("2NO + O₂ → 2NO₂", {"NO": 2, "O₂": 1, "NO₂": 2}, {"NO₂"}),
    ("H₂ + I₂ → 2HI", {"H₂": 1, "I₂": 1, "HI": 2}, {"HI"}),
    ("4NH₃ + 5O₂ → 4NO + 6H₂O", {"NH₃": 4, "O₂": 5, "NO": 4, "H₂O": 6}, {"NO", "H₂O"}),
    ("2HI → H₂ + I₂", {"HI": 2, "H₂": 1, "I₂": 1}, {"H₂", "I₂"}),
)


# (reaction, what is measured, unit of the amount)
MEASURED = (
    ("Mg(s) + 2HCl(aq) → MgCl₂(aq) + H₂(g)", "ปริมาตรแก๊ส H₂ ที่เกิดขึ้น", "cm³"),
    ("CaCO₃(s) + 2HCl(aq) → CaCl₂(aq) + H₂O(l) + CO₂(g)", "ปริมาตรแก๊ส CO₂ ที่เกิดขึ้น", "cm³"),
    ("2H₂O₂(aq) → 2H₂O(l) + O₂(g)", "ปริมาตรแก๊ส O₂ ที่เกิดขึ้น", "cm³"),
    ("CaCO₃(s) + 2HCl(aq) → CaCl₂(aq) + H₂O(l) + CO₂(g)", "มวลของระบบที่ลดลงเพราะ CO₂ หนีออกไป", "g"),
    ("Zn(s) + 2HCl(aq) → ZnCl₂(aq) + H₂(g)", "ปริมาตรแก๊ส H₂ ที่เกิดขึ้น", "cm³"),
)


@question_type(
    "chem.rate_calc_foundation",
    display_name={"th": "อัตราการเกิดปฏิกิริยาเฉลี่ยจากข้อมูลการทดลอง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CALC,
)
class RateCalcFoundation(QuestionType):
    """Average rate = change in amount ÷ time taken."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            reaction, what, unit = rng.choice(MEASURED)
            t1 = rng.choice((0, 0, 10, 20, 30, 60))
            span = rng.choice((10, 20, 30, 40, 50, 60, 90, 120))
            if unit == "cm³":
                a1 = 0 if t1 == 0 else rng.randrange(5, 60, 5)
                change = rng.randrange(5, 121, 5)
            else:
                a1 = 0 if t1 == 0 else Fraction(rng.randrange(1, 30), 10)
                change = Fraction(rng.randrange(1, 60), 10)
            rate = Fraction(change) / span
            return (reaction, what, unit, t1, span, a1, change, rate) if exact(rate) else None

        reaction, what, unit, t1, span, a1, change, rate = _find(rng, draw)
        t2, a2 = t1 + span, a1 + change
        return numeric(stem=f"ปฏิกิริยา {reaction} วัด{what}: ที่เวลา {t1} s ได้ {show(a1)} {unit} ที่เวลา {t2} s ได้ "
                            f"{show(a2)} {unit} อัตราการเกิดปฏิกิริยาเฉลี่ยในช่วงนี้เท่าใด",
                       answer=rate, wrongs=[Fraction(a2) / t2 if t2 and exact(Fraction(a2) / t2) and a1 else rate * 2,
                                            Fraction(span) / change if exact(Fraction(span) / change) else rate + 1,
                                            rate * 10], unit=f"{unit}/s", topic=TOPIC_CALC,
                       hint="อัตราเฉลี่ย = ปริมาณที่เปลี่ยนไป ÷ เวลาที่ใช้ = (ค่าหลัง − ค่าก่อน) ÷ (t₂ − t₁)")


@question_type(
    "chem.rate_calc_fluency",
    display_name={"th": "อัตราการเปลี่ยนแปลงของสารอื่นจากสัมประสิทธิ์ในสมการ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CALC,
)
class RateCalcFluency(QuestionType):
    """Rates of different substances stand in the ratio of their coefficients."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            eq, coef, products = rng.choice(RATE_EQUATIONS)
            a, b = rng.sample(sorted(coef), 2)
            rate_a = Fraction(rng.randrange(1, 60), 100)
            rate_b = rate_a * coef[b] / coef[a]
            return (eq, coef, products, a, b, rate_a, rate_b) if exact(rate_b) else None

        eq, coef, products, a, b, rate_a, rate_b = _find(rng, draw)
        verb = lambda x: "เกิด" if x in products else "ลดลง"
        return numeric(stem=f"ปฏิกิริยา {eq} ถ้า {a} {verb(a)}ด้วยอัตรา {show(rate_a)} mol/dm³·s "
                            f"{b} จะ{verb(b)}ด้วยอัตราเท่าใด",
                       answer=rate_b, wrongs=[rate_a, rate_a * coef[a] / coef[b] if exact(rate_a * coef[a] / coef[b]) else rate_b * 2,
                                              rate_b * 2 if rate_b * 2 != rate_a else rate_b + 1], unit="mol/dm³·s",
                       topic=TOPIC_CALC,
                       hint="อัตราของแต่ละสารเป็นสัดส่วนกับสัมประสิทธิ์: อัตราของ B = อัตราของ A × (b ÷ a)")


@question_type(
    "chem.rate_calc_application",
    display_name={"th": "ปริมาณสารที่ไม่ได้วัดในปฏิกิริยา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CALC,
)
class RateCalcApplication(QuestionType):
    """What happened to the substance nobody measured, from the one that was."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            eq, coef, products = rng.choice(RATE_EQUATIONS)
            a, b = rng.sample(sorted(coef), 2)
            start = Fraction(rng.randrange(10, 201, 5), 100)
            change = Fraction(rng.randrange(5, int(start * 100) + 1, 5), 100) if a not in products else \
                Fraction(rng.randrange(5, 101, 5), 100)
            change_b = change * coef[b] / coef[a]
            seconds = rng.choice((10, 20, 25, 30, 40, 50, 60, 100))
            return (eq, coef, products, a, b, change, change_b, seconds) if exact(change_b) else None

        eq, coef, products, a, b, change, change_b, seconds = _find(rng, draw)
        a_dir = "เพิ่มขึ้น" if a in products else "ลดลง"
        b_dir = "เพิ่มขึ้น" if b in products else "ลดลง"
        if rng.random() < 0.5:
            return numeric(stem=f"ปฏิกิริยา {eq} ในเวลา {seconds} s ความเข้มข้นของ {a} {a_dir} {show(change)} mol/dm³ "
                                f"ในช่วงเดียวกันความเข้มข้นของ {b} {b_dir}กี่ mol/dm³",
                           answer=change_b, wrongs=[change, change * coef[a] / coef[b] if exact(change * coef[a] / coef[b]) else change_b * 2,
                                                    change_b / seconds if exact(change_b / seconds) and change_b / seconds else change_b + 1],
                           unit="mol/dm³", topic=TOPIC_CALC,
                           hint="ความเข้มข้นที่เปลี่ยนไปเป็นสัดส่วนกับสัมประสิทธิ์ในสมการ")
        right = f"ความเข้มข้นของ {b} {b_dir} เร็วในช่วงแรกแล้วช้าลงจนคงที่"
        wrong_dir = "ลดลง" if b_dir == "เพิ่มขึ้น" else "เพิ่มขึ้น"
        return _labelled(stem=f"ปฏิกิริยา {eq} วัดได้ว่าความเข้มข้นของ {a} {a_dir}เร็วในช่วงแรกแล้วช้าลงเรื่อย ๆ "
                              f"กราฟความเข้มข้นของ {b} (ไม่ได้วัด) กับเวลามีลักษณะอย่างไร",
                         correct=right,
                         wrongs=(f"ความเข้มข้นของ {b} {wrong_dir} เร็วในช่วงแรกแล้วช้าลงจนคงที่",
                                 f"ความเข้มข้นของ {b} {b_dir}ด้วยอัตราคงที่ตลอดเป็นเส้นตรง",
                                 f"ความเข้มข้นของ {b} ไม่เปลี่ยนแปลง"),
                         topic=TOPIC_CALC,
                         hint="สารตั้งต้นลดลง ผลิตภัณฑ์เพิ่มขึ้น และอัตราช้าลงเมื่อสารตั้งต้นเหลือน้อย กราฟจึงค่อย ๆ ราบ")
