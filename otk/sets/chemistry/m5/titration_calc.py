"""การคำนวณจากการไทเทรตกรด-เบส

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/21

Sets moved here from: science_wave_f37.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f37 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_CALC = "การคำนวณจากการไทเทรตกรด-เบส"


# (acid, H⁺ per formula, base, OH⁻ per formula)
PAIRS = (("HCl", 1, "NaOH", 1), ("HNO₃", 1, "KOH", 1), ("H₂SO₄", 2, "NaOH", 1), ("HCl", 1, "Ca(OH)₂", 2),
         ("CH₃COOH", 1, "NaOH", 1), ("H₂SO₄", 2, "KOH", 1), ("HCl", 1, "Ba(OH)₂", 2), ("H₂C₂O₄", 2, "NaOH", 1))


MOLARITY = tuple(Fraction(x, 100) for x in (5, 10, 20, 25, 40, 50, 100))


VOLUME = (10, 20, 25, 40, 50)


def titre_case(rng: Random):
    def draw():
        acid, a, base, b = rng.choice(PAIRS)
        ca, va, cb = rng.choice(MOLARITY), rng.choice(VOLUME), rng.choice(MOLARITY)
        vb = ca * va * a / (cb * b)
        return (acid, a, base, b, ca, va, cb, vb) if exact(vb) and 5 <= vb <= 60 else None
    return _find(rng, draw)


@question_type(
    "chem.titration_calc_foundation",
    display_name={"th": "ปริมาตรที่ใช้ในการไทเทรตถึงจุดสมมูล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CALC,
)
class TitrationCalcFoundation(QuestionType):
    """mol H⁺ = mol OH⁻ at the equivalence point."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        acid, a, base, b, ca, va, cb, vb = titre_case(rng)
        return numeric(stem=f"ไทเทรต {acid} {show(ca)} mol/dm³ ปริมาตร {va} cm³ ด้วย {base} {show(cb)} mol/dm³ "
                            f"ต้องใช้ {base} กี่ cm³ จึงถึงจุดสมมูล",
                       answer=vb, wrongs=[ca * va / cb if ca * va / cb != vb else vb * 2, va, vb * 2 if vb * 2 != va else vb / 2],
                       unit="cm³", topic=TOPIC_CALC,
                       hint="ที่จุดสมมูล โมล H⁺ จากกรด = โมล OH⁻ จากเบส: C₁V₁ × (H⁺ ต่อโมเลกุล) = C₂V₂ × (OH⁻ ต่อโมเลกุล)")


@question_type(
    "chem.titration_calc_fluency",
    display_name={"th": "ความเข้มข้นของสารละลายจากการไทเทรต"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CALC,
)
class TitrationCalcFluency(QuestionType):
    """Solve the same balance for the unknown concentration."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        acid, a, base, b, ca, va, cb, vb = titre_case(rng)
        if rng.random() < 0.5:
            return numeric(stem=f"ไทเทรตสารละลาย {acid} ปริมาตร {va} cm³ ด้วย {base} {show(cb)} mol/dm³ ใช้ไป {show(vb)} cm³ "
                                f"สารละลาย {acid} เข้มข้นกี่ mol/dm³",
                           answer=ca, wrongs=[cb * vb / va if cb * vb / va != ca else ca * 2, ca * 2, cb], unit="mol/dm³",
                           topic=TOPIC_CALC, hint="C_กรด = C_เบส × V_เบส × (OH⁻ ต่อโมเลกุล) ÷ (V_กรด × H⁺ ต่อโมเลกุล)")
        return numeric(stem=f"ไทเทรตสารละลาย {base} ปริมาตร {show(vb)} cm³ ด้วย {acid} {show(ca)} mol/dm³ ใช้ไป {va} cm³ "
                            f"สารละลาย {base} เข้มข้นกี่ mol/dm³",
                       answer=cb, wrongs=[ca * va / vb if ca * va / vb != cb else cb * 2, cb * 2, ca], unit="mol/dm³",
                       topic=TOPIC_CALC, hint="C_เบส = C_กรด × V_กรด × (H⁺ ต่อโมเลกุล) ÷ (V_เบส × OH⁻ ต่อโมเลกุล)")


@question_type(
    "chem.titration_calc_application",
    display_name={"th": "ปริมาณกรดแอซีติกในน้ำส้มสายชูจากการไทเทรต"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CALC,
)
class TitrationCalcApplication(QuestionType):
    """Moles of CH₃COOH from the NaOH used, then grams and percent by mass per volume."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            sample = rng.choice((5, 10, 20, 25))
            cb = rng.choice(MOLARITY)
            vb = rng.choice(range(5, 61))
            moles = cb * vb / 1000
            grams = moles * 60
            percent = grams / sample * 100
            return (sample, cb, vb, moles, grams, percent) if exact(grams) and exact(percent) else None

        sample, cb, vb, moles, grams, percent = _find(rng, draw)
        stem = (f"ไทเทรตน้ำส้มสายชู {sample} cm³ ด้วย NaOH {show(cb)} mol/dm³ ใช้ไป {vb} cm³ "
                "(CH₃COOH + NaOH → CH₃COONa + H₂O, มวลโมเลกุล CH₃COOH = 60)")
        if rng.random() < 0.5:
            return numeric(stem=f"{stem} น้ำส้มสายชูนี้มีกรดแอซีติกกี่กรัม", answer=grams,
                           wrongs=[grams * 1000, moles * 1000 if exact(moles * 1000) else grams * 2, grams * 2], unit="กรัม",
                           topic=TOPIC_CALC, hint="โมล CH₃COOH = โมล NaOH ที่ใช้ แล้วคูณมวลโมเลกุล 60")
        return numeric(stem=f"{stem} น้ำส้มสายชูนี้มีกรดแอซีติกร้อยละโดยมวลต่อปริมาตรเท่าใด", answer=percent,
                       wrongs=[grams, percent * 10, percent / 10 if exact(percent / 10) else percent + 1], unit="% w/v",
                       topic=TOPIC_CALC, hint="ร้อยละโดยมวลต่อปริมาตร = มวลกรด (g) ÷ ปริมาตรตัวอย่าง (cm³) × 100")
