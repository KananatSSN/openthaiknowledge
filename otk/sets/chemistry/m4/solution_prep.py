"""การเตรียมสารละลาย

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 3 ม.4/10

Sets moved here from: science_wave_f43.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f43 import CHEMISTRY, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_PREP = "การเตรียมสารละลาย"


SOLUTES = (("NaCl", Fraction(117, 2)), ("NaOH", 40), ("KCl", Fraction(149, 2)), ("C₆H₁₂O₆", 180), ("CuSO₄·5H₂O", Fraction(499, 2)),
           ("KNO₃", 101), ("Na₂CO₃", 106), ("KMnO₄", 158), ("NaHCO₃", 84))


STEPS = ("ชั่งตัวละลายตามมวลที่คำนวณได้", "ละลายตัวละลายด้วยน้ำกลั่นจำนวนหนึ่งในบีกเกอร์",
         "เทสารละลายลงขวดกำหนดปริมาตรและกลั้วบีกเกอร์ด้วยน้ำกลั่นเทตาม",
         "เติมน้ำกลั่นจนถึงขีดบอกปริมาตร", "ปิดจุกแล้วกลับขวดไปมาให้สารละลายผสมกันทั่ว")


VOLUMES = (50, 100, 250, 500, 1000)


@question_type(
    "chem.solution_prep_foundation",
    display_name={"th": "ขั้นตอนการเตรียมสารละลายด้วยขวดกำหนดปริมาตร"},
    level=UPPER_FOUR, subject=CHEMISTRY, topic=TOPIC_PREP,
)
class SolutionPrepFoundation(QuestionType):
    """Weigh, dissolve, transfer and rinse, fill to the mark, mix."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.35:
            chosen = sorted(rng.sample(range(len(STEPS)), 4))
            labels = ["ก", "ข", "ค", "ง"]
            shuffled = rng.sample(chosen, 4)
            named = {step: labels[k] for k, step in enumerate(shuffled)}
            listed = " ".join(f"{labels[k]}. {STEPS[step]}" for k, step in enumerate(shuffled))
            right = " → ".join(named[step] for step in chosen)
            others = [" → ".join(p) for p in permutations([named[step] for step in chosen]) if " → ".join(p) != right]
            return _labelled(stem=f"เรียงขั้นตอนการเตรียมสารละลายให้ถูกต้อง: {listed}", correct=right,
                             wrongs=tuple(others), topic=TOPIC_PREP,
                             hint="ชั่ง → ละลายในบีกเกอร์ → ถ่ายลงขวดกำหนดปริมาตรและกลั้ว → ปรับปริมาตรถึงขีด → เขย่าให้ผสม")
        if rng.random() < 0.5:
            i = rng.randrange(len(STEPS) - 1)
            others = [s for j, s in enumerate(STEPS) if j != i + 1]
            return _labelled(stem=f"ในการเตรียมสารละลายด้วยขวดกำหนดปริมาตร ขั้นตอนต่อจาก \"{STEPS[i]}\" คือข้อใด",
                             correct=STEPS[i + 1], wrongs=tuple(others), topic=TOPIC_PREP,
                             hint="ชั่ง → ละลายในบีกเกอร์ → ถ่ายลงขวดกำหนดปริมาตรและกลั้ว → ปรับปริมาตรถึงขีด → เขย่าให้ผสม")
        mistakes = (
            ("ละลายตัวละลายในน้ำจนได้ 250 cm³ ในบีกเกอร์แล้วใช้เลย", "ปริมาตรไม่แม่นยำ เพราะบีกเกอร์ไม่ใช่เครื่องวัดปริมาตร"),
            ("เติมน้ำเกินขีดบอกปริมาตรแล้วดูดส่วนเกินออก", "ความเข้มข้นต่ำกว่าที่ต้องการ เพราะตัวละลายบางส่วนถูกดูดออกไปด้วย"),
            ("ไม่กลั้วบีกเกอร์หลังเทสารละลายลงขวด", "ความเข้มข้นต่ำกว่าที่ต้องการ เพราะตัวละลายบางส่วนค้างในบีกเกอร์"),
            ("อ่านขีดบอกปริมาตรโดยมองจากด้านบน", "ปริมาตรคลาดเคลื่อน เพราะต้องให้ส่วนโค้งล่างของผิวของเหลวอยู่ระดับสายตา"),
        )
        action, effect = rng.choice(mistakes)
        others = [m[1] for m in mistakes if m[1] != effect]
        return _labelled(stem=f"นักเรียน{action} จะเกิดผลอย่างไร", correct=effect, wrongs=tuple(others), topic=TOPIC_PREP,
                         hint="ตัวละลายต้องย้ายไปขวดทั้งหมด และปริมาตรต้องพอดีขีดบนขวดกำหนดปริมาตร")


@question_type(
    "chem.solution_prep_fluency",
    display_name={"th": "คำนวณมวลตัวละลายที่ต้องใช้เตรียมสารละลาย"},
    level=UPPER_FOUR, subject=CHEMISTRY, topic=TOPIC_PREP,
)
class SolutionPrepFluency(QuestionType):
    """mass = molarity × volume (dm³) × molar mass."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            solute, m = rng.choice(SOLUTES)
            c = Fraction(rng.choice((5, 10, 20, 25, 40, 50, 100, 200)), 100)
            v = rng.choice(VOLUMES)
            grams = c * v / 1000 * m
            return (solute, m, c, v, grams) if exact(grams) else None

        solute, m, c, v, grams = _find(rng, draw)
        return numeric(stem=f"ต้องการเตรียมสารละลาย {solute} เข้มข้น {show(c)} mol/dm³ ปริมาตร {v} cm³ ต้องชั่ง {solute} กี่กรัม "
                            f"(มวลต่อโมล {show(m)})",
                       answer=grams, wrongs=[c * v * m if exact(c * v * m) else grams * 2, grams * 10, c * v / 1000 if exact(c * v / 1000) else grams + 1],
                       unit="กรัม", topic=TOPIC_PREP, hint="โมล = ความเข้มข้น × ปริมาตร (dm³) แล้วมวล = โมล × มวลต่อโมล")


@question_type(
    "chem.solution_prep_application",
    display_name={"th": "เตรียมสารละลายโดยการเจือจาง"},
    level=UPPER_FOUR, subject=CHEMISTRY, topic=TOPIC_PREP,
)
class SolutionPrepApplication(QuestionType):
    """C₁V₁ = C₂V₂: the moles of solute do not change."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            c1 = Fraction(rng.choice((50, 100, 200, 250, 500, 1000, 1200, 1800)), 100)
            c2 = Fraction(rng.choice((5, 10, 20, 25, 40, 50, 100)), 100)
            v2 = rng.choice(VOLUMES)
            v1 = c2 * v2 / c1
            return (c1, c2, v2, v1) if c2 < c1 and exact(v1) else None

        c1, c2, v2, v1 = _find(rng, draw)
        name = rng.choice(("HCl", "H₂SO₄", "NaOH", "HNO₃", "NH₃"))
        if rng.random() < 0.6:
            return numeric(stem=f"ต้องการเตรียม {name} เข้มข้น {show(c2)} mol/dm³ ปริมาตร {v2} cm³ จากสารละลายเข้มข้น {show(c1)} mol/dm³ "
                                "ต้องใช้สารละลายเข้มข้นกี่ cm³",
                           answer=v1, wrongs=[c1 * v2 / c2 if exact(c1 * v2 / c2) else v1 * 2, v2 - v1, v1 * 10], unit="cm³",
                           topic=TOPIC_PREP, hint="C₁V₁ = C₂V₂ เพราะโมลตัวละลายเท่าเดิมก่อนและหลังเจือจาง")
        return numeric(stem=f"นำ {name} เข้มข้น {show(c1)} mol/dm³ มา {show(v1)} cm³ เติมน้ำจนได้ {v2} cm³ สารละลายใหม่เข้มข้นกี่ mol/dm³",
                       answer=c2, wrongs=[c1 * v2 / v1 if exact(c1 * v2 / v1) else c2 * 2, c1 - c2, c2 * 10], unit="mol/dm³",
                       topic=TOPIC_PREP, hint="C₂ = C₁V₁ ÷ V₂")
