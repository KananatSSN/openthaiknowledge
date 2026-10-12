"""การคำนวณปริมาณสารในปฏิกิริยาเคมีที่เกี่ยวข้องกับปริมาตรแก๊ส

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.4/4

Sets moved here from: science_wave_f30.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f30 import (
    EQUATIONS,
    STP,
    SUBJECT,
    UPPER_FOUR,
    equation_text,
    mass_of,
    species,
    verb,
)

PROVENANCE = Provenance("original")


TOPIC_GAS = "การคำนวณปริมาณสารในปฏิกิริยาเคมีที่เกี่ยวข้องกับปริมาตรแก๊ส"


GAS_EQUATIONS = tuple(e for e in EQUATIONS if any(st == "g" for _, _, st in e[1]))


ALL_GAS = tuple(e for e in EQUATIONS if all(st == "g" for _, _, st in species(e)))


@question_type(
    "chem.stoich_gas_foundation",
    display_name={"th": "ปริมาตรแก๊สที่ STP จากจำนวนโมล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_GAS,
)
class StoichGasFoundation(QuestionType):
    """1 mol of any gas at STP takes 22.4 dm³."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            eq = rng.choice(GAS_EQUATIONS)
            gas = rng.choice([x for x in eq[1] if x[2] == "g"])
            other = rng.choice([x for x in species(eq) if x is not gas])
            n_other = rng.choice([Fraction(k, 4) for k in range(1, 21)])
            volume = n_other * gas[0] / other[0] * STP
            return (eq, gas, other, n_other, volume) if exact(volume) else None

        eq, gas, other, n_other, volume = _find(rng, draw)
        return numeric(stem=f"จากสมการ {equation_text(eq)} ถ้า {other[1]} {verb(eq, other[1])} {show(n_other)} โมล "
                            f"จะเกิดแก๊ส {gas[1]} กี่ dm³ ที่ STP",
                       answer=volume, wrongs=[n_other * STP, volume * 2, n_other * gas[0] / other[0] * Fraction(245, 10)],
                       unit="dm³", topic=TOPIC_GAS,
                       hint="โมลแก๊สจากอัตราส่วนในสมการ แล้ว × 22.4 dm³/mol ที่ STP")


@question_type(
    "chem.stoich_gas_fluency",
    display_name={"th": "ปริมาตรแก๊สที่ STP จากมวลสารตั้งต้น"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_GAS,
)
class StoichGasFluency(QuestionType):
    """mass → mol → mol of gas → dm³ at STP, or back to mass."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            eq = rng.choice(GAS_EQUATIONS)
            gas = rng.choice([x for x in eq[1] if x[2] == "g"])
            solid = rng.choice([x for x in eq[0] if x[1] != gas[1]])
            extent = rng.choice([Fraction(k, 4) for k in range(1, 21)])
            grams = extent * solid[0] * mass_of(solid[1])
            volume = extent * gas[0] * STP
            return (eq, gas, solid, grams, volume) if exact(grams) and exact(volume) else None

        eq, gas, solid, grams, volume = _find(rng, draw)
        mass_text = f"(มวลต่อโมล {solid[1]} = {show(mass_of(solid[1]))})"
        hint = "มวล ÷ มวลต่อโมล = โมล ใช้อัตราส่วนในสมการ แล้ว × 22.4 dm³ ที่ STP"
        if rng.random() < 0.5:
            return numeric(stem=f"จากสมการ {equation_text(eq)} ใช้ {solid[1]} {show(grams)} กรัม จะเกิดแก๊ส {gas[1]} "
                                f"กี่ dm³ ที่ STP {mass_text}",
                           answer=volume, wrongs=[grams / mass_of(solid[1]) * STP, volume * 2, grams * STP / 100],
                           unit="dm³", topic=TOPIC_GAS, hint=hint)
        return numeric(stem=f"จากสมการ {equation_text(eq)} ต้องการแก๊ส {gas[1]} {show(volume)} dm³ ที่ STP ต้องใช้ "
                            f"{solid[1]} กี่กรัม {mass_text}",
                       answer=grams, wrongs=[volume / STP * mass_of(solid[1]), grams * 2, volume],
                       unit="กรัม", topic=TOPIC_GAS, hint=hint)


@question_type(
    "chem.stoich_gas_application",
    display_name={"th": "อัตราส่วนปริมาตรของแก๊สในปฏิกิริยา"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_GAS,
)
class StoichGasApplication(QuestionType):
    """At the same temperature and pressure, gas volumes react in the ratio of their coefficients."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            eq = rng.choice(ALL_GAS + tuple(e for e in EQUATIONS if sum(st == "g" for _, _, st in species(e)) >= 2))
            gases = [x for x in species(eq) if x[2] == "g"]
            a, b = rng.sample(gases, 2)
            va = rng.randrange(10, 301, 10)
            vb = Fraction(va * b[0], a[0])
            return (eq, a, b, va, vb) if exact(vb) else None

        eq, a, b, va, vb = _find(rng, draw)
        return numeric(stem=f"จากสมการ {equation_text(eq, states=True)} ที่อุณหภูมิและความดันเดียวกัน ถ้าแก๊ส {a[1]} "
                            f"{verb(eq, a[1])} {va} cm³ แก๊ส {b[1]} จะ{verb(eq, b[1])}กี่ cm³",
                       answer=vb, wrongs=[va, Fraction(va * a[0], b[0]) if exact(Fraction(va * a[0], b[0])) else va * 2,
                                          vb * 2], unit="cm³", topic=TOPIC_GAS,
                       hint="กฎของเกย์-ลูสแซกเรื่องปริมาตรแก๊สที่รวมกัน: อัตราส่วนปริมาตรแก๊ส = อัตราส่วนสัมประสิทธิ์")
