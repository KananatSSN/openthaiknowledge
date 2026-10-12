"""ปฏิกิริยาสะเทิน

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/18

Sets moved here from: science_wave_f36.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find
from otk.sets._support.science_wave_f36 import (
    ACIDIC,
    BASIC,
    NEUTRAL,
    SUBJECT,
    UPPER_FIVE,
    log_note,
    ph_of,
    tabled,
)

PROVENANCE = Provenance("original")


TOPIC_NEUTRAL = "ปฏิกิริยาสะเทิน"


# (acid, base, salt, acid strong, base strong)
NEUTRALISATIONS = (
    ("HCl", "NaOH", "NaCl", True, True), ("HNO₃", "KOH", "KNO₃", True, True), ("HCl", "KOH", "KCl", True, True),
    ("HNO₃", "NaOH", "NaNO₃", True, True), ("CH₃COOH", "NaOH", "CH₃COONa", False, True),
    ("HF", "KOH", "KF", False, True), ("HCOOH", "NaOH", "HCOONa", False, True), ("HCl", "NH₃", "NH₄Cl", True, False),
    ("HNO₃", "NH₃", "NH₄NO₃", True, False), ("HCN", "NaOH", "NaCN", False, True),
)


def at_equivalence(acid_strong: bool, base_strong: bool) -> str:
    if acid_strong and base_strong:
        return NEUTRAL
    return BASIC if base_strong else ACIDIC


@question_type(
    "chem.neutralization_foundation",
    display_name={"th": "ผลิตภัณฑ์และสมการของปฏิกิริยาสะเทิน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NEUTRAL,
)
class NeutralizationFoundation(QuestionType):
    """Acid + base → salt + water; the net ionic equation is H₃O⁺ + OH⁻ → 2H₂O."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        acid, base, salt, strong_a, strong_b = rng.choice(NEUTRALISATIONS)
        if rng.random() < 0.4 and strong_a and strong_b:
            return _labelled(stem=f"สมการไอออนิกสุทธิของปฏิกิริยาสะเทินระหว่าง {acid} กับ {base} คือข้อใด",
                             correct="H₃O⁺(aq) + OH⁻(aq) → 2H₂O(l)",
                             wrongs=(f"{acid}(aq) + {base}(aq) → {salt}(aq) + H₂O(l)", "Na⁺(aq) + Cl⁻(aq) → NaCl(s)",
                                     "H₂O(l) → H₃O⁺(aq) + OH⁻(aq)"),
                             topic=TOPIC_NEUTRAL, hint="กรดแก่และเบสแก่แตกตัวหมด ไอออนที่ไม่ได้ทำปฏิกิริยาตัดออกได้")
        others = sorted({n[2] for n in NEUTRALISATIONS} - {salt})
        return _labelled(stem=f"{acid} ทำปฏิกิริยาสะเทินกับ {base} ได้เกลือใด", correct=salt,
                         wrongs=tuple(others), topic=TOPIC_NEUTRAL,
                         hint="เกลือประกอบด้วยไอออนบวกจากเบส และไอออนลบจากกรด")


@question_type(
    "chem.neutralization_fluency",
    display_name={"th": "ความเป็นกรด-เบสของสารละลายหลังการสะเทิน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NEUTRAL,
)
class NeutralizationFluency(QuestionType):
    """Compare moles; at exact equivalence the weak partner decides."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        acid, base, salt, strong_a, strong_b = rng.choice(NEUTRALISATIONS)
        c_a, c_b = rng.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 2))), rng.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 2)))
        v_a = rng.choice((20, 25, 40, 50))
        equal = rng.random() < 0.5
        v_b = c_a * v_a / c_b if equal else rng.choice((10, 20, 25, 40, 50, 60))
        n_a, n_b = c_a * v_a, c_b * v_b
        if n_a > n_b:
            right = ACIDIC
        elif n_b > n_a:
            right = BASIC
        else:
            right = at_equivalence(strong_a, strong_b)
        return _labelled(stem=f"ผสม {acid} {show(c_a)} mol/dm³ ปริมาตร {v_a} cm³ กับ {base} {show(c_b)} mol/dm³ ปริมาตร "
                              f"{show(v_b)} cm³ สารละลายที่ได้มีสมบัติอย่างไร",
                         correct=right, wrongs=tuple(x for x in (ACIDIC, BASIC, NEUTRAL, "บอกไม่ได้") if x != right),
                         topic=TOPIC_NEUTRAL,
                         hint="เทียบโมลกรดกับโมลเบส ถ้าเท่ากันพอดี กรดแก่+เบสแก่เป็นกลาง กรดอ่อน+เบสแก่เป็นเบส "
                              "กรดแก่+เบสอ่อนเป็นกรด")


@question_type(
    "chem.neutralization_application",
    display_name={"th": "pH ของสารละลายหลังผสมกรดแก่กับเบสแก่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NEUTRAL,
)
class NeutralizationApplication(QuestionType):
    """Excess moles over the combined volume set the pH."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            c_a, c_b = rng.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 2), Fraction(1))), \
                rng.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 2), Fraction(1)))
            v_a, v_b = rng.choice((10, 20, 25, 40, 50, 60, 75, 100)), rng.choice((10, 20, 25, 40, 50, 60, 75, 100))
            excess = c_a * v_a - c_b * v_b
            if excess == 0:
                return None
            conc = abs(excess) / (v_a + v_b)
            return (c_a, v_a, c_b, v_b, excess, conc) if tabled(conc) else None

        c_a, v_a, c_b, v_b, excess, conc = _find(rng, draw)
        p = ph_of(conc)
        value = p if excess > 0 else 14 - p
        return numeric(stem=f"ผสม HCl {show(c_a)} mol/dm³ ปริมาตร {v_a} cm³ กับ NaOH {show(c_b)} mol/dm³ ปริมาตร {v_b} cm³ "
                            f"สารละลายที่ได้มี pH เท่าใด{log_note(conc)}",
                       answer=value, wrongs=[14 - value, 7, value + 1 if value + 1 < 14 else value - 1], unit="",
                       topic=TOPIC_NEUTRAL,
                       hint="หาโมลที่เหลือของสารที่มากเกินพอ หารด้วยปริมาตรรวม (dm³) แล้วคำนวณ pH")
