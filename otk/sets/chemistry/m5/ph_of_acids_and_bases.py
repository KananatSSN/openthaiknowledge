"""pH ของสารละลายกรดและเบส

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/17

Sets moved here from: science_wave_f36.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric
from otk.sets._support.science_wave_f24 import _find
from otk.sets._support.science_wave_f36 import (
    LOGS,
    SUBJECT,
    UPPER_FIVE,
    log_note,
    ph_of,
    sci,
    sci_text,
    tabled,
)

PROVENANCE = Provenance("original")


TOPIC_PH = "pH ของสารละลายกรดและเบส"


def tabled_conc(rng: Random, low: int = 1, high: int = 6) -> Fraction:
    return Fraction(rng.choice(sorted(LOGS))) / Fraction(10) ** rng.randint(low, high)


@question_type(
    "chem.ph_calc_foundation",
    display_name={"th": "คำนวณ pH จาก [H₃O⁺] หรือ [OH⁻]"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_PH,
)
class PhCalcFoundation(QuestionType):
    """pH = −log[H₃O⁺]; pOH = −log[OH⁻]; pH + pOH = 14 at 25 °C."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        conc = tabled_conc(rng)
        value = ph_of(conc)
        if rng.random() < 0.5:
            return numeric(stem=f"สารละลายมี [H₃O⁺] = {sci_text(conc)} mol/dm³ มี pH เท่าใด{log_note(conc)}",
                           answer=value, wrongs=[14 - value, value + LOGS[int(sci(conc)[0])] * 2 or value + 1, value + 2],
                           unit="", topic=TOPIC_PH, hint="pH = −log[H₃O⁺] = n − log a เมื่อ [H₃O⁺] = a × 10⁻ⁿ")
        return numeric(stem=f"สารละลายมี [OH⁻] = {sci_text(conc)} mol/dm³ ที่ 25 °C มี pH เท่าใด{log_note(conc)}",
                       answer=14 - value, wrongs=[value, 14 - value + 1, 14 - (value + 1) if value + 1 < 14 else value + 2],
                       unit="", topic=TOPIC_PH, hint="pOH = −log[OH⁻] แล้ว pH = 14 − pOH")


@question_type(
    "chem.ph_calc_fluency",
    display_name={"th": "pH ของสารละลายกรดแก่และเบสแก่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_PH,
)
class PhCalcFluency(QuestionType):
    """Strong acids and bases ionise fully; H₂SO₄ and Ca(OH)₂ give two per formula."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            name, per, base = rng.choice((("HCl", 1, False), ("HNO₃", 1, False), ("H₂SO₄", 2, False), ("NaOH", 1, True),
                                          ("KOH", 1, True), ("Ca(OH)₂", 2, True), ("Ba(OH)₂", 2, True)))
            c = Fraction(rng.choice((1, 2, 3, 4, 5))) / Fraction(10) ** rng.randint(1, 4)
            ion = c * per
            return (name, per, base, c, ion) if tabled(ion) and ion < 1 else None

        name, per, base, c, ion = _find(rng, draw)
        p = ph_of(ion)
        value = 14 - p if base else p
        wrong_single = 14 - ph_of(c) if base else ph_of(c) if tabled(c) else value + 1
        return numeric(stem=f"สารละลาย {name} เข้มข้น {sci_text(c)} mol/dm³ มี pH เท่าใด{log_note(ion)}",
                       answer=value, wrongs=[wrong_single if wrong_single != value else value + 1, 14 - value,
                                             value + 1 if value + 1 <= 14 else value - 2],
                       unit="", topic=TOPIC_PH,
                       hint="กรดแก่ [H₃O⁺] = C × จำนวน H⁺ ต่อโมเลกุล เบสแก่ [OH⁻] = C × จำนวน OH⁻ แล้วหา pH (เบสใช้ pH = 14 − pOH)")


@question_type(
    "chem.ph_calc_application",
    display_name={"th": "ความเข้มข้นของไอออนจาก pH และการเจือจาง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_PH,
)
class PhCalcApplication(QuestionType):
    """From pH back to the ions, and pH after diluting a strong acid or base."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            ph = rng.randint(1, 13)
            ion, sign = rng.choice((("H₃O⁺", ph), ("OH⁻", 14 - ph)))
            return numeric(stem=f"สารละลายมี pH = {ph} ที่ 25 °C [{ion}] = 1 × 10⁻ⁿ mol/dm³ ค่า n เท่าใด",
                           answer=sign, wrongs=[14 - sign, sign + 1, sign - 1 if sign > 1 else sign + 2], unit="",
                           topic=TOPIC_PH, hint="[H₃O⁺] = 10⁻ᵖᴴ และ [OH⁻] = 10⁻⁽¹⁴⁻ᵖᴴ⁾")
        if kind == 1:
            ph = rng.randint(1, 4)
            times = rng.choice((10, 100, 1000))
            steps = {10: 1, 100: 2, 1000: 3}[times]
            return numeric(stem=f"สารละลาย HCl มี pH = {ph} เจือจางด้วยน้ำจนมีปริมาตรเพิ่มเป็น {times} เท่า pH ใหม่เท่าใด",
                           answer=ph + steps, wrongs=[ph, ph * times if ph * times <= 14 else ph + steps + 1, ph - steps if ph > steps else ph + steps + 2],
                           unit="", topic=TOPIC_PH, hint="เจือจาง 10 เท่า [H₃O⁺] ลดลง 10 เท่า pH เพิ่มขึ้น 1")
        ph = rng.randint(10, 13)
        times = rng.choice((10, 100))
        steps = {10: 1, 100: 2}[times]
        return numeric(stem=f"สารละลาย NaOH มี pH = {ph} เจือจางด้วยน้ำจนมีปริมาตรเพิ่มเป็น {times} เท่า pH ใหม่เท่าใด",
                       answer=ph - steps, wrongs=[ph, ph + steps if ph + steps <= 14 else ph - steps - 1, 14 - ph],
                       unit="", topic=TOPIC_PH, hint="เจือจางเบส [OH⁻] ลดลง pOH เพิ่มขึ้น pH จึงลดลง (เข้าใกล้ 7)")
