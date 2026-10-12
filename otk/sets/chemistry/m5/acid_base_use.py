"""การใช้ประโยชน์ความรู้เกี่ยวกับกรด-เบส

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/23

Sets moved here from: science_wave_f37.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f37 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_USE = "การใช้ประโยชน์ความรู้เกี่ยวกับกรด-เบส"


PROBLEMS = (
    ("ปวดท้องเพราะกรดในกระเพาะอาหารมากเกินไป", "กินยาลดกรดที่มี Mg(OH)₂",
     ("ดื่มน้ำมะนาว", "กินยาที่มีกรดแอซีติก", "ดื่มน้ำอัดลม")),
    ("ดินเป็นกรดมากเกินไปจนพืชโตช้า", "โรยปูนขาวหรือหินปูนบดลงในดิน",
     ("ใส่ปุ๋ยแอมโมเนียมซัลเฟต", "รดด้วยน้ำส้มสายชู", "โรยกำมะถันผง")),
    ("ดินเป็นเบสมากเกินไป", "ใส่กำมะถันผงหรือปุ๋ยแอมโมเนียมซัลเฟต",
     ("โรยปูนขาว", "โรยขี้เถ้าไม้", "โรยโซเดียมไฮดรอกไซด์")),
    ("ถูกมดแดงกัด (มีกรดฟอร์มิก)", "ทาด้วยสารละลายโซเดียมไฮโดรเจนคาร์บอเนต (เบกิ้งโซดา)",
     ("ทาด้วยน้ำมะนาว", "ทาด้วยน้ำส้มสายชู", "ทาด้วยกรดไฮโดรคลอริกเจือจาง")),
    ("มีคราบหินปูน (CaCO₃) ในกาต้มน้ำ", "แช่ด้วยน้ำส้มสายชูหรือกรดซิทริก",
     ("แช่ด้วยน้ำสบู่", "แช่ด้วยน้ำปูนใส", "แช่ด้วยแอมโมเนีย")),
    ("ฟันผุเพราะแบคทีเรียผลิตกรดหลังกินของหวาน", "แปรงฟันด้วยยาสีฟันที่เป็นเบสอ่อน",
     ("อมลูกอมเปรี้ยว", "บ้วนปากด้วยน้ำส้มสายชู", "ดื่มน้ำอัดลมตาม")),
    ("น้ำในสระว่ายน้ำมี pH ต่ำเกินไป", "เติมโซเดียมคาร์บอเนตเพื่อเพิ่ม pH",
     ("เติมกรดไฮโดรคลอริก", "เติมน้ำส้มสายชู", "เติมแอมโมเนียมคลอไรด์")),
)


NEEDS_ACID = frozenset({"ดินเป็นเบสมากเกินไป", "มีคราบหินปูน (CaCO₃) ในกาต้มน้ำ"})


# Worded as whole actions, as long as the answers they sit beside.
ACID_FIXES = ("แช่หรือราดด้วยน้ำส้มสายชูเจือจาง", "บีบน้ำมะนาวลงไปให้ทั่ว", "ละลายกรดซิทริกในน้ำแล้วราด",
              "ใช้กรดไฮโดรคลอริกเจือจางล้าง", "ดื่มน้ำอัดลมหลังอาหารทุกมื้อ", "ใส่ปุ๋ยแอมโมเนียมซัลเฟตเพิ่ม")


BASE_FIXES = ("โรยปูนขาวลงไปให้ทั่วบริเวณ", "ใช้สารละลายโซเดียมไฮดรอกไซด์ล้าง", "ละลายเบกิ้งโซดาในน้ำแล้วราด",
              "โรยขี้เถ้าไม้ลงไปแล้วคลุกให้ทั่ว", "ใช้น้ำสบู่ขัดล้างหลายครั้ง", "ใช้แอมโมเนียเจือจางราด")


# (antacid, mass per mole, HCl it takes per formula)
ANTACIDS = (("Mg(OH)₂", 58, 2), ("Al(OH)₃", 78, 3), ("NaHCO₃", 84, 1), ("CaCO₃", 100, 2))


@question_type(
    "chem.acid_base_use_foundation",
    display_name={"th": "ใช้ความรู้กรด-เบสแก้ปัญหาในชีวิตประจำวัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_USE,
)
class AcidBaseUseFoundation(QuestionType):
    """Neutralise the excess: a base for too much acid, an acid for too much base."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        problem, right, wrongs = rng.choice(PROBLEMS)
        # When the fix is a base, every wrong fix is an acid, and the other way round.
        wrongs = tuple(rng.sample(BASE_FIXES if problem in NEEDS_ACID else ACID_FIXES, 3))
        return _labelled(stem=f"ปัญหา: {problem} ควรแก้อย่างไร", correct=right, wrongs=wrongs, topic=TOPIC_USE,
                         hint="กรดมากเกินไปใช้เบสสะเทิน เบสมากเกินไปใช้กรดสะเทิน")


@question_type(
    "chem.acid_base_use_fluency",
    display_name={"th": "ยาลดกรดสะเทินกรดในกระเพาะอาหาร"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_USE,
)
class AcidBaseUseFluency(QuestionType):
    """mol HCl neutralised = mol antacid × HCl per formula."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            name, mass, per = rng.choice(ANTACIDS)
            grams = Fraction(rng.randrange(1, 41), 10) * mass / 10
            moles_hcl = grams / mass * per
            return (name, mass, per, grams, moles_hcl) if exact(grams) and exact(moles_hcl * 1000) else None

        name, mass, per, grams, moles_hcl = _find(rng, draw)
        millimoles = moles_hcl * 1000
        return numeric(stem=f"ยาลดกรดเม็ดหนึ่งมี {name} {show(grams)} กรัม (มวลต่อโมล {mass}) สะเทิน HCl ในกระเพาะได้กี่มิลลิโมล",
                       answer=millimoles, wrongs=[millimoles / per if per > 1 and exact(millimoles / per) else millimoles * 2,
                                                  millimoles * 2 if per != 2 else millimoles * 3, grams * 1000 / 36],
                       unit="มิลลิโมล", topic=TOPIC_USE,
                       hint="โมลยา = มวล ÷ มวลต่อโมล แล้วคูณจำนวน HCl ที่ยาหนึ่งหน่วยสูตรสะเทินได้ (เช่น Mg(OH)₂ + 2HCl)")


@question_type(
    "chem.acid_base_use_application",
    display_name={"th": "เปรียบเทียบประสิทธิภาพของยาลดกรด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_USE,
)
class AcidBaseUseApplication(QuestionType):
    """Per gram, the antacid that takes the most HCl wins."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            def draw():
                (na, ma, pa), (nb, mb, pb) = rng.sample(ANTACIDS, 2)
                ga, gb = rng.randrange(1, 21) / Fraction(10), rng.randrange(1, 21) / Fraction(10)
                ha, hb = ga / ma * pa, gb / mb * pb
                return (na, ma, pa, ga, ha, nb, mb, pb, gb, hb) if ha != hb else None

            na, ma, pa, ga, ha, nb, mb, pb, gb, hb = _find(rng, draw)
            better = na if ha > hb else nb
            worse = nb if better == na else na
            return _labelled(stem=f"ยา A มี {na} {show(ga)} กรัม (มวลต่อโมล {ma}, สะเทิน HCl {pa} โมลต่อโมล) ยา B มี {nb} {show(gb)} กรัม "
                                  f"(มวลต่อโมล {mb}, สะเทิน HCl {pb} โมลต่อโมล) ยาใดสะเทินกรดได้มากกว่า",
                             correct=f"ยาที่มี {better}", wrongs=(f"ยาที่มี {worse}", "สะเทินได้เท่ากัน",
                                                                   "บอกไม่ได้ถ้าไม่รู้ปริมาตรกรด"),
                             topic=TOPIC_USE, hint="โมล HCl ที่สะเทินได้ = (มวล ÷ มวลต่อโมล) × HCl ต่อโมล แล้วเทียบกัน")
        chosen = rng.sample(ANTACIDS, 3)
        best = max(chosen, key=lambda a: Fraction(a[2], a[1]))
        listed = ", ".join(f"{n} (มวลต่อโมล {m}, สะเทิน HCl {p} โมลต่อโมล)" for n, m, p in chosen)
        return _labelled(stem=f"ยาลดกรดมวลเท่ากัน ชนิดใดสะเทินกรดในกระเพาะได้มากที่สุด: {listed}", correct=best[0],
                         wrongs=tuple(a[0] for a in chosen if a is not best) + ("สะเทินได้เท่ากันเพราะมวลเท่ากัน",),
                         topic=TOPIC_USE, hint="เทียบโมล HCl ที่สะเทินได้ต่อกรัม = (HCl ต่อโมล) ÷ มวลต่อโมล")
