"""ผลได้ร้อยละ

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.4/7

Sets moved here from: science_wave_f31.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f30 import EQUATIONS, equation_text, mass_of
from otk.sets._support.science_wave_f31 import QUARTERS, SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_YIELD = "ผลได้ร้อยละ"


PERCENTS = (40, 50, 60, 64, 75, 80, 85, 90, 92, 95)


def yield_case(rng: Random):
    def draw():
        eq = rng.choice(EQUATIONS)
        reactant = rng.choice(eq[0])
        product = rng.choice(eq[1])
        extent = rng.choice(QUARTERS)
        m_r = extent * reactant[0] * mass_of(reactant[1])
        theory = extent * product[0] * mass_of(product[1])
        percent = rng.choice(PERCENTS)
        actual = theory * percent / 100
        ok = all(exact(x) for x in (m_r, theory, actual))
        return (eq, reactant, product, m_r, theory, actual, percent) if ok else None
    return _find(rng, draw)


@question_type(
    "chem.percent_yield_foundation",
    display_name={"th": "คำนวณผลได้ร้อยละจากผลได้จริงและผลได้ตามทฤษฎี"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_YIELD,
)
class PercentYieldFoundation(QuestionType):
    """% yield = actual ÷ theoretical × 100."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq, _, product, _, theory, actual, percent = yield_case(rng)
        if rng.random() < 0.5:
            return numeric(stem=f"ปฏิกิริยาหนึ่งควรได้ {product[1]} ตามทฤษฎี {show(theory)} กรัม แต่ทดลองได้จริง "
                                f"{show(actual)} กรัม ผลได้ร้อยละเท่าใด",
                           answer=percent, wrongs=[100 - percent, theory / actual * 100 if exact(theory / actual * 100) else percent + 5,
                                                   percent + 10 if percent <= 90 else percent - 20], unit="%",
                           topic=TOPIC_YIELD, hint="ผลได้ร้อยละ = (ผลได้จริง ÷ ผลได้ตามทฤษฎี) × 100")
        return numeric(stem=f"ปฏิกิริยาหนึ่งควรได้ {product[1]} ตามทฤษฎี {show(theory)} กรัม ถ้าผลได้ร้อยละเท่ากับ "
                            f"{percent}% จะได้ {product[1]} จริงกี่กรัม",
                       answer=actual, wrongs=[theory, theory - actual, actual * 2], unit="กรัม", topic=TOPIC_YIELD,
                       hint="ผลได้จริง = ผลได้ตามทฤษฎี × ร้อยละ ÷ 100")


@question_type(
    "chem.percent_yield_fluency",
    display_name={"th": "ผลได้ร้อยละจากมวลสารตั้งต้น"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_YIELD,
)
class PercentYieldFluency(QuestionType):
    """Theoretical yield from the reactant first, then compare with what was collected."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq, reactant, product, m_r, theory, actual, percent = yield_case(rng)
        masses = f"(มวลต่อโมล {reactant[1]} = {show(mass_of(reactant[1]))}, {product[1]} = {show(mass_of(product[1]))})"
        return numeric(stem=f"ใช้ {reactant[1]} {show(m_r)} กรัม ทำปฏิกิริยาตามสมการ {equation_text(eq)} "
                            f"(สารอื่นมากเกินพอ) ได้ {product[1]} จริง {show(actual)} กรัม ผลได้ร้อยละเท่าใด {masses}",
                       answer=percent, wrongs=[actual / m_r * 100 if exact(actual / m_r * 100) and actual / m_r * 100 != percent else 100 - percent,
                                               percent + 5 if percent <= 95 else percent - 10, 100], unit="%",
                       topic=TOPIC_YIELD,
                       hint="คำนวณผลได้ตามทฤษฎีจากมวลสารตั้งต้นก่อน แล้วผลได้ร้อยละ = ผลได้จริง ÷ ผลได้ตามทฤษฎี × 100")


@question_type(
    "chem.percent_yield_application",
    display_name={"th": "มวลสารตั้งต้นที่ต้องใช้เมื่อทราบผลได้ร้อยละ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_YIELD,
)
class PercentYieldApplication(QuestionType):
    """To collect a target, aim for target ÷ (% ÷ 100) in theory, then work back to the reactant."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq, reactant, product, m_r, theory, actual, percent = yield_case(rng)
        masses = f"(มวลต่อโมล {reactant[1]} = {show(mass_of(reactant[1]))}, {product[1]} = {show(mass_of(product[1]))})"
        if rng.random() < 0.5:
            return numeric(stem=f"ต้องการ {product[1]} จริง {show(actual)} กรัม จากปฏิกิริยา {equation_text(eq)} "
                                f"ซึ่งมีผลได้ร้อยละ {percent}% ต้องใช้ {reactant[1]} กี่กรัม (สารอื่นมากเกินพอ) {masses}",
                           answer=m_r, wrongs=[m_r * percent / 100 if exact(m_r * percent / 100) else m_r / 2,
                                               theory, m_r * 2], unit="กรัม", topic=TOPIC_YIELD,
                           hint="ผลได้ตามทฤษฎีที่ต้องการ = ผลได้จริง × 100 ÷ ร้อยละ แล้วคำนวณย้อนหามวลสารตั้งต้น")
        return numeric(stem=f"ใช้ {reactant[1]} {show(m_r)} กรัม ทำปฏิกิริยาตามสมการ {equation_text(eq)} "
                            f"(สารอื่นมากเกินพอ) ถ้าผลได้ร้อยละเท่ากับ {percent}% จะได้ {product[1]} จริงกี่กรัม {masses}",
                       answer=actual, wrongs=[theory, m_r * percent / 100 if exact(m_r * percent / 100) else actual * 2,
                                              theory - actual], unit="กรัม", topic=TOPIC_YIELD,
                       hint="หาผลได้ตามทฤษฎีจากมวลสารตั้งต้น แล้วคูณด้วยร้อยละ ÷ 100")
