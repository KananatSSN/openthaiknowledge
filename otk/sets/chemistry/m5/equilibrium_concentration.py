"""การคำนวณความเข้มข้นของสารที่ภาวะสมดุล

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/10

Sets moved here from: science_wave_f34.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f34 import (
    CONCS,
    K_SYSTEMS,
    SUBJECT,
    UPPER_FIVE,
    conc_text,
    counted,
    k_case,
    k_value,
)

PROVENANCE = Provenance("original")


TOPIC_CONC = "การคำนวณความเข้มข้นของสารที่ภาวะสมดุล"


@question_type(
    "chem.equilibrium_concentration_foundation",
    display_name={"th": "หาความเข้มข้นที่ภาวะสมดุลเมื่อทราบค่า K"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CONC,
)
class EquilibriumConcentrationFoundation(QuestionType):
    """Rearrange K for the one unknown concentration."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            system, conc, k = k_case(rng)
            # Only species that enter K to the first power, so no roots are needed.
            singles = [f for f, c, _ in counted(system[1]) + counted(system[2]) if c == 1]
            if not singles:
                return None
            return system, conc, k, rng.choice(singles)

        system, conc, k, hidden = _find(rng, draw)
        known = {f: v for f, v in conc.items() if f != hidden}
        return numeric(stem=f"ปฏิกิริยา {system[0]} มีค่า K = {show(k)} ที่ภาวะสมดุลมี {conc_text(known)} mol/dm³ "
                            f"[{hidden}] ที่ภาวะสมดุลเท่าใด",
                       answer=conc[hidden], wrongs=[conc[hidden] * 2, conc[hidden] / 2 if exact(conc[hidden] / 2) else conc[hidden] + 1,
                                                    k if k != conc[hidden] else k + 1],
                       unit="mol/dm³", topic=TOPIC_CONC, hint="เขียนนิพจน์ K แทนค่าที่รู้ แล้วแก้สมการหาความเข้มข้นที่ไม่รู้")


@question_type(
    "chem.equilibrium_concentration_fluency",
    display_name={"th": "ตาราง ICE: ความเข้มข้นเริ่มต้น เปลี่ยนแปลง และที่ภาวะสมดุล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CONC,
)
class EquilibriumConcentrationFluency(QuestionType):
    """Initial − change = equilibrium, with changes in the ratio of the coefficients."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        gas = [s for s in K_SYSTEMS if len(counted(s[1])) == len(s[1]) and len(counted(s[2])) == len(s[2])]

        def draw():
            system = rng.choice(gas)
            _, reactants, products = system
            start = {f: rng.choice(CONCS[3:]) for f, _, _ in reactants}
            x = Fraction(rng.randrange(5, 101, 5), 100)
            eq = {f: start[f] - c * x for f, c, _ in reactants}
            eq.update({f: c * x for f, c, _ in products})
            if any(v <= 0 for v in eq.values()):
                return None
            k = k_value(system, eq)
            return (system, start, eq, k) if exact(k) and k <= 10000 else None

        system, start, eq, k = _find(rng, draw)
        _, reactants, products = system
        product = products[0][0]
        start_text = ", ".join(f"[{f}] = {show(v)}" for f, v in start.items())
        stem = (f"ปฏิกิริยา {system[0]} เริ่มต้นมี {start_text} mol/dm³ และไม่มีผลิตภัณฑ์ ที่ภาวะสมดุลพบ "
                f"[{product}] = {show(eq[product])} mol/dm³")
        if rng.random() < 0.5:
            target = rng.choice([f for f, _, _ in reactants])
            return numeric(stem=f"{stem} [{target}] ที่ภาวะสมดุลเท่าใด", answer=eq[target],
                           wrongs=[start[target] - eq[product] if start[target] - eq[product] > 0 and start[target] - eq[product] != eq[target] else start[target],
                                   eq[product], start[target]], unit="mol/dm³", topic=TOPIC_CONC,
                           hint="ใช้ตาราง ICE: การเปลี่ยนแปลงของแต่ละสารเป็นไปตามสัมประสิทธิ์ แล้วที่สมดุล = เริ่มต้น ± การเปลี่ยนแปลง")
        return numeric(stem=f"{stem} ค่าคงที่สมดุลเท่าใด", answer=k,
                       wrongs=[1 / k if exact(1 / k) and 1 / k != k else k * 2, k * 2, k + 1], unit="", topic=TOPIC_CONC,
                       hint="หาความเข้มข้นที่สมดุลของทุกสารจากตาราง ICE แล้วแทนในนิพจน์ K")


@question_type(
    "chem.equilibrium_concentration_application",
    display_name={"th": "หาความเข้มข้นที่ภาวะสมดุลจากค่า K และความเข้มข้นเริ่มต้น"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CONC,
)
class EquilibriumConcentrationApplication(QuestionType):
    """A ⇌ B gives [B] = K·a / (1 + K); H₂ + I₂ ⇌ 2HI with a square K gives √K = 2x / (a − x)."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            def draw():
                k = rng.choice((Fraction(1, 4), Fraction(1, 2), 1, Fraction(3, 2), 2, 3, 4, 9))
                a = rng.choice(CONCS)
                b = k * a / (1 + k)
                return (k, a, b) if exact(b) else None

            k, a, b = _find(rng, draw)
            system = rng.choice(("ซิส-บิวต์-2-อีน ⇌ ทรานส์-บิวต์-2-อีน", "A(g) ⇌ B(g)", "บิวเทน ⇌ 2-เมทิลโพรเพน"))
            return numeric(stem=f"ปฏิกิริยา {system} มีค่า K = {show(k)} เริ่มต้นมีสารทางซ้าย {show(a)} mol/dm³ เพียงอย่างเดียว "
                                "ที่ภาวะสมดุลความเข้มข้นของสารทางขวาเท่าใด",
                           answer=b, wrongs=[k * a if k * a != b else a, a - b, a / 2 if a / 2 != b else a], unit="mol/dm³",
                           topic=TOPIC_CONC, hint="ให้เปลี่ยนไป x: K = x ÷ (a − x) แก้ได้ x = K·a ÷ (1 + K)")

        def draw():
            root = rng.choice((2, 3, 4, 5, 6, 7, 8))
            a = rng.choice(CONCS)
            x = a * root / (2 + root)
            return (root, a, x) if exact(x) and exact(2 * x) else None

        root, a, x = _find(rng, draw)
        return numeric(stem=f"ปฏิกิริยา H₂(g) + I₂(g) ⇌ 2HI(g) มีค่า K = {root * root} เริ่มต้น [H₂] = [I₂] = {show(a)} mol/dm³ "
                            "และไม่มี HI ที่ภาวะสมดุล [HI] เท่าใด",
                       answer=2 * x, wrongs=[x, a - x, 2 * a], unit="mol/dm³", topic=TOPIC_CONC,
                       hint="ให้ H₂ ลดลง x: K = (2x)² ÷ (a − x)² ถอดรากทั้งสองข้าง √K = 2x ÷ (a − x) แล้ว [HI] = 2x")
