"""การคำนวณปริมาณสารในปฏิกิริยาเคมีที่เกี่ยวข้องกับมวล

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.4/2

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
    SUBJECT,
    UPPER_FOUR,
    equation_text,
    mass_of,
    species,
    verb,
)

PROVENANCE = Provenance("original")


TOPIC_MASS = "การคำนวณปริมาณสารในปฏิกิริยาเคมีที่เกี่ยวข้องกับมวล"


def _pair(rng: Random, eqs=EQUATIONS):
    """An equation and two different species in it."""
    eq = rng.choice(eqs)
    a, b = rng.sample(species(eq), 2)
    return eq, a, b


@question_type(
    "chem.stoich_mass_foundation",
    display_name={"th": "จำนวนโมลของสารในปฏิกิริยาจากอัตราส่วนในสมการ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MASS,
)
class StoichMassFoundation(QuestionType):
    """mol B = mol A × (coefficient of B ÷ coefficient of A)."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            eq, a, b = _pair(rng)
            n_a = rng.choice([Fraction(k, 4) for k in range(1, 41)])
            n_b = n_a * b[0] / a[0]
            return (eq, a, b, n_a, n_b) if exact(n_b) else None

        eq, a, b, n_a, n_b = _find(rng, draw)
        return numeric(stem=f"จากสมการ {equation_text(eq)} ถ้า {a[1]} {verb(eq, a[1])} {show(n_a)} โมล "
                            f"{b[1]} จะ{verb(eq, b[1])}กี่โมล",
                       answer=n_b, wrongs=[n_a, n_a * a[0] / b[0] if exact(n_a * a[0] / b[0]) else n_a * 2, n_a * b[0]],
                       unit="โมล", topic=TOPIC_MASS, hint="ใช้อัตราส่วนสัมประสิทธิ์ในสมการที่ดุลแล้ว: n_B = n_A × (b ÷ a)")


@question_type(
    "chem.stoich_mass_fluency",
    display_name={"th": "คำนวณมวลของสารในปฏิกิริยาจากมวลของอีกสารหนึ่ง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MASS,
)
class StoichMassFluency(QuestionType):
    """mass A → mol A → mol B → mass B."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            eq, a, b = _pair(rng)
            extent = rng.choice([Fraction(k, 4) for k in range(1, 41)])
            m_a, m_b = extent * a[0] * mass_of(a[1]), extent * b[0] * mass_of(b[1])
            return (eq, a, b, m_a, m_b) if exact(m_a) and exact(m_b) else None

        eq, a, b, m_a, m_b = _find(rng, draw)
        masses = ", ".join(f"{f} = {show(mass_of(f))}" for f in dict.fromkeys((a[1], b[1])))
        return numeric(stem=f"จากสมการ {equation_text(eq)} ถ้า {a[1]} {verb(eq, a[1])} {show(m_a)} กรัม "
                            f"{b[1]} จะ{verb(eq, b[1])}กี่กรัม (มวลต่อโมล {masses})",
                       answer=m_b, wrongs=[m_a * mass_of(b[1]) / mass_of(a[1]), m_a, m_b * 2], unit="กรัม",
                       topic=TOPIC_MASS, hint="เปลี่ยนมวลเป็นโมล ใช้อัตราส่วนโมลจากสมการ แล้วเปลี่ยนโมลกลับเป็นมวล")


@question_type(
    "chem.stoich_mass_application",
    display_name={"th": "กฎทรงมวลและมวลสารตั้งต้นที่ต้องใช้"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MASS,
)
class StoichMassApplication(QuestionType):
    """Mass is conserved; and how much of a reactant a given product needs."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            def draw():
                eq = rng.choice([e for e in EQUATIONS if len(species(e)) >= 3])
                extent = rng.choice([Fraction(k, 4) for k in range(1, 21)])
                grams = {f: extent * c * mass_of(f) for c, f, _ in species(eq)}
                return (eq, grams) if all(exact(g) for g in grams.values()) else None

            eq, grams = _find(rng, draw)
            hidden = rng.choice([f for _, f, _ in species(eq)])
            known = ", ".join(f"{f} {show(g)} กรัม" for f, g in grams.items() if f != hidden)
            return numeric(stem=f"ปฏิกิริยา {equation_text(eq)} เกิดพอดี โดยมี {known} มี {hidden} {verb(eq, hidden)}กี่กรัม",
                           answer=grams[hidden], wrongs=[sum(grams.values()) - grams[hidden], grams[hidden] * 2,
                                                         grams[hidden] + 1], unit="กรัม", topic=TOPIC_MASS,
                           hint="กฎทรงมวล: มวลสารตั้งต้นรวม = มวลผลิตภัณฑ์รวม")

        def draw():
            eq = rng.choice(EQUATIONS)
            product = rng.choice(eq[1])
            reactant = rng.choice(eq[0])
            extent = rng.choice([Fraction(k, 4) for k in range(1, 41)])
            m_p, m_r = extent * product[0] * mass_of(product[1]), extent * reactant[0] * mass_of(reactant[1])
            return (eq, product, reactant, m_p, m_r) if exact(m_p) and exact(m_r) else None

        eq, product, reactant, m_p, m_r = _find(rng, draw)
        return numeric(stem=f"ต้องการเตรียม {product[1]} {show(m_p)} กรัม จากปฏิกิริยา {equation_text(eq)} "
                            f"ต้องใช้ {reactant[1]} อย่างน้อยกี่กรัม (มวลต่อโมล {product[1]} = {show(mass_of(product[1]))}, "
                            f"{reactant[1]} = {show(mass_of(reactant[1]))})",
                       answer=m_r, wrongs=[m_p, m_r * 2, m_p * mass_of(reactant[1]) / mass_of(product[1])],
                       unit="กรัม", topic=TOPIC_MASS, hint="โมลผลิตภัณฑ์ → โมลสารตั้งต้นด้วยอัตราส่วนในสมการ → มวล")
