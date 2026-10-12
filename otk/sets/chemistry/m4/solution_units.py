"""ความเข้มข้นของสารละลายในหน่วยต่าง ๆ

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 3 ม.4/9

Sets moved here from: science_wave_f42.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f42 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_CONC = "ความเข้มข้นของสารละลายในหน่วยต่าง ๆ"


SOLUTES = (("NaCl", Fraction(117, 2)), ("NaOH", 40), ("KCl", Fraction(149, 2)), ("C₆H₁₂O₆", 180), ("CuSO₄", Fraction(319, 2)),
           ("KNO₃", 101), ("Na₂CO₃", 106), ("C₁₂H₂₂O₁₁", 342))


UNIT_MEANINGS = (
    ("ร้อยละโดยมวล (% w/w)", "มวลตัวละลาย (g) ในสารละลาย 100 g"),
    ("ร้อยละโดยมวลต่อปริมาตร (% w/v)", "มวลตัวละลาย (g) ในสารละลาย 100 cm³"),
    ("ร้อยละโดยปริมาตร (% v/v)", "ปริมาตรตัวละลาย (cm³) ในสารละลาย 100 cm³"),
    ("โมลาริตี (mol/dm³)", "จำนวนโมลตัวละลายในสารละลาย 1 dm³"),
    ("โมแลลิตี (mol/kg)", "จำนวนโมลตัวละลายในตัวทำละลาย 1 kg"),
    ("ส่วนในล้านส่วน (ppm)", "มวลตัวละลาย 1 ส่วนในสารละลาย 10⁶ ส่วน เช่น mg ต่อ kg"),
    ("เศษส่วนโมล", "จำนวนโมลของสารนั้นหารด้วยจำนวนโมลรวมของทุกสาร"),
)


@question_type(
    "chem.solution_units_foundation",
    display_name={"th": "ความหมายของหน่วยความเข้มข้น"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CONC,
)
class SolutionUnitsFoundation(QuestionType):
    """Know what each unit divides by what."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        unit, meaning = rng.choice(UNIT_MEANINGS)
        others = [u for u in UNIT_MEANINGS if u[0] != unit]
        if rng.random() < 0.5:
            return _labelled(stem=f"ความเข้มข้นในหน่วย {unit} หมายถึงอะไร", correct=meaning,
                             wrongs=tuple(u[1] for u in rng.sample(others, 3)), topic=TOPIC_CONC,
                             hint="ดูว่าหน่วยนี้เทียบตัวละลายกับสารละลายหรือตัวทำละลาย และใช้มวล ปริมาตร หรือโมล")
        return _labelled(stem=f"\"{meaning}\" คือความเข้มข้นในหน่วยใด", correct=unit,
                         wrongs=tuple(u[0] for u in rng.sample(others, 3)), topic=TOPIC_CONC,
                         hint="โมลาริตีเทียบกับสารละลาย โมแลลิตีเทียบกับตัวทำละลาย")


@question_type(
    "chem.solution_units_fluency",
    display_name={"th": "คำนวณโมลาริตีและโมแลลิตี"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CONC,
)
class SolutionUnitsFluency(QuestionType):
    """mol/dm³ uses the solution's volume; mol/kg uses the solvent's mass."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            solute, m = rng.choice(SOLUTES)
            moles = Fraction(rng.randrange(1, 41), rng.choice((10, 20, 40)))
            grams = moles * m
            amount = rng.choice((100, 200, 250, 400, 500, 1000))
            conc = moles / amount * 1000
            return (solute, m, moles, grams, amount, conc) if exact(grams) and exact(conc) else None

        solute, m, moles, grams, amount, conc = _find(rng, draw)
        if rng.random() < 0.5:
            return numeric(stem=f"ละลาย {solute} {show(grams)} กรัม (มวลต่อโมล {show(m)}) ในน้ำจนได้สารละลาย {amount} cm³ "
                                "สารละลายนี้เข้มข้นกี่ mol/dm³",
                           answer=conc, wrongs=[moles, grams / amount * 1000 if exact(grams / amount * 1000) else conc * 2, conc / 10 if exact(conc / 10) else conc + 1],
                           unit="mol/dm³", topic=TOPIC_CONC, hint="โมลาริตี = โมลตัวละลาย ÷ ปริมาตรสารละลาย (dm³)")
        return numeric(stem=f"ละลาย {solute} {show(grams)} กรัม (มวลต่อโมล {show(m)}) ในน้ำ {amount} กรัม "
                            "สารละลายนี้เข้มข้นกี่ mol/kg",
                       answer=conc, wrongs=[moles, conc * 2, conc / 10 if exact(conc / 10) else conc + 1], unit="mol/kg",
                       topic=TOPIC_CONC, hint="โมแลลิตี = โมลตัวละลาย ÷ มวลตัวทำละลาย (kg)")


@question_type(
    "chem.solution_units_application",
    display_name={"th": "ความเข้มข้นเป็นร้อยละ ppm เศษส่วนโมล และเปลี่ยนเป็นโมลาริตี"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_CONC,
)
class SolutionUnitsApplication(QuestionType):
    """ppm, mole fraction, and % w/w with density to mol/dm³."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            mg = rng.randrange(1, 200)
            kg = rng.choice((1, 2, 4, 5, 10))
            ppm = Fraction(mg, kg)
            if not exact(ppm):
                return self.build(rng)
            ion = rng.choice(("ตะกั่ว", "ปรอท", "ฟลูออไรด์", "ไนเตรต", "คลอไรด์"))
            return numeric(stem=f"น้ำตัวอย่าง {kg} kg มี{ion}ละลายอยู่ {mg} mg มีความเข้มข้นของ{ion}กี่ ppm", answer=ppm,
                           wrongs=[ppm * 1000, mg * kg if mg * kg != ppm else ppm + 1, ppm * 10], unit="ppm",
                           topic=TOPIC_CONC, hint="ppm = มวลตัวละลาย (mg) ÷ มวลสารละลาย (kg)")
        if kind == 1:
            def draw():
                a = Fraction(rng.randrange(1, 21), 4)
                b = Fraction(rng.randrange(1, 41), 4)
                x = a / (a + b)
                return (a, b, x) if exact(x) else None

            a, b, x = _find(rng, draw)
            return numeric(stem=f"สารละลายประกอบด้วยเอทานอล {show(a)} โมล และน้ำ {show(b)} โมล เศษส่วนโมลของเอทานอลเท่าใด",
                           answer=x, wrongs=[a / b if exact(a / b) and a / b != x else 1 - x, 1 - x, x * 2 if x * 2 < 1 else x / 2],
                           unit="", topic=TOPIC_CONC, hint="เศษส่วนโมล = โมลของสารนั้น ÷ โมลรวมของทุกสาร")

        def draw():
            name, m = rng.choice((("HCl", Fraction(73, 2)), ("H₂SO₄", 98), ("HNO₃", 63), ("NaOH", 40)))
            percent = Fraction(rng.choice((10, 20, 25, 30, 36, 40, 50, 60, 70, 98)))
            density = Fraction(rng.randrange(100, 185), 100)
            molarity = percent / 100 * density * 1000 / m
            return (name, m, percent, density, molarity) if exact(molarity) else None

        name, m, percent, density, molarity = _find(rng, draw)
        return numeric(stem=f"สารละลาย {name} เข้มข้นร้อยละ {show(percent)} โดยมวล มีความหนาแน่น {show(density)} g/cm³ "
                            f"เข้มข้นกี่ mol/dm³ (มวลต่อโมล {show(m)})",
                       answer=molarity, wrongs=[percent * density / m if exact(percent * density / m) and percent * density / m != molarity else molarity * 2,
                                                molarity * 2, percent * 10 / m if exact(percent * 10 / m) and percent * 10 / m != molarity else molarity + 1],
                       unit="mol/dm³", topic=TOPIC_CONC,
                       hint="สารละลาย 1 dm³ หนัก 1000 × ความหนาแน่น กรัม มีตัวละลายร้อยละที่กำหนด แล้วเปลี่ยนเป็นโมล")
