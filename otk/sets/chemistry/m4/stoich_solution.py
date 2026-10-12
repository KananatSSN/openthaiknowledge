"""การคำนวณปริมาณสารในปฏิกิริยาเคมีที่เกี่ยวข้องกับความเข้มข้นของสารละลาย

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.4/3

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
)

PROVENANCE = Provenance("original")


TOPIC_SOLUTION = "การคำนวณปริมาณสารในปฏิกิริยาเคมีที่เกี่ยวข้องกับความเข้มข้นของสารละลาย"


AQUEOUS = tuple(e for e in EQUATIONS if sum(1 for _, _, st in e[0] if st == "aq") >= 1)


PRECIPITATIONS = tuple(e for e in EQUATIONS if any(st == "s" for _, _, st in e[1])
                       and all(st == "aq" for _, _, st in e[0]))


NEUTRALISATIONS = tuple(e for e in EQUATIONS if len(e[0]) == 2 and all(st == "aq" for _, _, st in e[0])
                        and any(f == "H₂O" for _, f, _ in e[1]))


LIQUID_STOCKS = frozenset({"HCl", "H₂SO₄", "H₂O₂"})


MOLARITIES = tuple(Fraction(k, 100) for k in (5, 10, 20, 25, 40, 50, 75, 100, 150, 200))


VOLUMES = tuple(range(5, 101, 5))


@question_type(
    "chem.stoich_solution_foundation",
    display_name={"th": "จำนวนโมลจากความเข้มข้นและปริมาตรสารละลาย"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_SOLUTION,
)
class StoichSolutionFoundation(QuestionType):
    """mol = mol/dm³ × dm³, with cm³ ÷ 1000."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            eq = rng.choice(AQUEOUS)
            solute = rng.choice([x for x in eq[0] if x[2] == "aq"])
            c, v = rng.choice(MOLARITIES), rng.choice(VOLUMES)
            n = c * v / 1000
            return (eq, solute, c, v, n) if exact(n) else None

        eq, solute, c, v, n = _find(rng, draw)
        if rng.random() < 0.5:
            return numeric(stem=f"สารละลาย {solute[1]} เข้มข้น {show(c)} mol/dm³ ปริมาตร {v} cm³ มี {solute[1]} กี่โมล",
                           answer=n, wrongs=[c * v, n * 10, c / v * 1000 if exact(c / v * 1000) else n * 2], unit="โมล",
                           topic=TOPIC_SOLUTION, hint="โมล = ความเข้มข้น (mol/dm³) × ปริมาตร (dm³) และ 1 dm³ = 1000 cm³")
        grams = n * mass_of(solute[1])
        # Only a solid is weighed out; HCl, H₂SO₄ and H₂O₂ come as stock solutions.
        if not exact(grams) or solute[1] in LIQUID_STOCKS:
            return self.build(rng)
        return numeric(stem=f"ต้องการเตรียมสารละลาย {solute[1]} เข้มข้น {show(c)} mol/dm³ ปริมาตร {v} cm³ "
                            f"ต้องใช้ {solute[1]} กี่กรัม (มวลต่อโมล {show(mass_of(solute[1]))})",
                       answer=grams, wrongs=[c * v * mass_of(solute[1]), n, grams * 10], unit="กรัม",
                       topic=TOPIC_SOLUTION, hint="โมล = ความเข้มข้น × ปริมาตร (dm³) แล้วมวล = โมล × มวลต่อโมล")


@question_type(
    "chem.stoich_solution_fluency",
    display_name={"th": "ปริมาตรสารละลายที่ทำปฏิกิริยาพอดีกัน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_SOLUTION,
)
class StoichSolutionFluency(QuestionType):
    """Acid against base, or two salts: moles by the equation, then volume or concentration."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            eq = rng.choice(NEUTRALISATIONS + PRECIPITATIONS)
            a, b = eq[0][0], eq[0][1]
            if rng.random() < 0.5:
                a, b = b, a
            ca, cb = rng.sample(MOLARITIES, 2)
            va = rng.choice(VOLUMES)
            vb = ca * va * b[0] / (a[0] * cb)
            return (eq, a, b, ca, va, cb, vb) if exact(vb) and vb <= 500 else None

        eq, a, b, ca, va, cb, vb = _find(rng, draw)
        hint = "โมล A = C × V แล้วใช้อัตราส่วนในสมการหาโมล B จากนั้น V_B = โมล B ÷ C_B"
        if rng.random() < 0.5:
            return numeric(stem=f"จากสมการ {equation_text(eq)} สารละลาย {a[1]} {show(ca)} mol/dm³ ปริมาตร {va} cm³ "
                                f"ทำปฏิกิริยาพอดีกับสารละลาย {b[1]} {show(cb)} mol/dm³ กี่ cm³",
                           answer=vb, wrongs=[ca * va / cb, vb * 2, va], unit="cm³", topic=TOPIC_SOLUTION, hint=hint)
        return numeric(stem=f"จากสมการ {equation_text(eq)} สารละลาย {a[1]} {show(ca)} mol/dm³ ปริมาตร {va} cm³ "
                            f"ทำปฏิกิริยาพอดีกับสารละลาย {b[1]} {show(vb)} cm³ สารละลาย {b[1]} เข้มข้นกี่ mol/dm³",
                       answer=cb, wrongs=[ca * va / vb, cb * 2, ca], unit="mol/dm³", topic=TOPIC_SOLUTION, hint=hint)


@question_type(
    "chem.stoich_solution_application",
    display_name={"th": "มวลตะกอนจากการผสมสารละลาย"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_SOLUTION,
)
class StoichSolutionApplication(QuestionType):
    """Moles of the reagent → moles of precipitate → grams."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            eq = rng.choice(PRECIPITATIONS)
            reagent = rng.choice(eq[0])
            solid = next(x for x in eq[1] if x[2] == "s")
            c, v = rng.choice(MOLARITIES), rng.choice(VOLUMES)
            n = c * v / 1000 * solid[0] / reagent[0]
            grams = n * mass_of(solid[1])
            return (eq, reagent, solid, c, v, grams) if exact(grams) else None

        eq, reagent, solid, c, v, grams = _find(rng, draw)
        return numeric(stem=f"เติมสารละลาย {reagent[1]} {show(c)} mol/dm³ ปริมาตร {v} cm³ ลงในสารละลายอีกชนิดที่มากเกินพอ "
                            f"ตามสมการ {equation_text(eq)} จะได้ตะกอน {solid[1]} กี่กรัม (มวลต่อโมล {solid[1]} = "
                            f"{show(mass_of(solid[1]))})",
                       answer=grams, wrongs=[grams * 1000, c * v * mass_of(solid[1]) / 1000 if solid[0] != reagent[0] else grams * 2,
                                             grams / 10 if exact(grams / 10) else grams + 1],
                       unit="กรัม", topic=TOPIC_SOLUTION,
                       hint="โมลสารละลายที่ใช้หมด = C × V (dm³) แล้วใช้อัตราส่วนในสมการหาโมลตะกอน × มวลต่อโมล")
