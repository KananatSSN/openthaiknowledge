"""สารกำหนดปริมาณ

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.4/6

Sets moved here from: science_wave_f31.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f30 import EQUATIONS, equation_text, mass_of
from otk.sets._support.science_wave_f31 import QUARTERS, SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_LIMIT = "สารกำหนดปริมาณ"


TWO_REACTANTS = tuple(eq for eq in EQUATIONS if len(eq[0]) == 2 and eq[0][0][1] != eq[0][1][1])


def limiting_case(rng: Random, in_grams: bool):
    """Two reactant amounts that are not in the exact ratio, and what they give."""
    def draw():
        eq = rng.choice(TWO_REACTANTS)
        (ca, a, _), (cb, b, _) = eq[0]
        na, nb = rng.sample(QUARTERS[:24], 2)
        runs_a, runs_b = na / ca, nb / cb
        if runs_a == runs_b:
            return None
        extent = min(runs_a, runs_b)
        limiting = a if runs_a < runs_b else b
        excess = b if limiting == a else a
        left = (nb - extent * cb) if excess == b else (na - extent * ca)
        product = rng.choice(eq[1])
        n_product = extent * product[0]
        values = {"na": na, "nb": nb, "left": left, "product": n_product}
        if in_grams:
            values = {"na": na * mass_of(a), "nb": nb * mass_of(b), "left": left * mass_of(excess),
                      "product": n_product * mass_of(product[1])}
        if not all(exact(v) for v in values.values()):
            return None
        return eq, a, b, limiting, excess, product, values
    return _find(rng, draw)


@question_type(
    "chem.limiting_reagent_foundation",
    display_name={"th": "ระบุสารกำหนดปริมาณ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_LIMIT,
)
class LimitingReagentFoundation(QuestionType):
    """Divide each reactant's moles by its coefficient; the smaller runs out first."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        grams = rng.random() < 0.5
        eq, a, b, limiting, excess, _, v = limiting_case(rng, grams)
        unit = "กรัม" if grams else "โมล"
        extra = f" (มวลต่อโมล {a} = {show(mass_of(a))}, {b} = {show(mass_of(b))})" if grams else ""
        return _labelled(stem=f"ผสม {a} {show(v['na'])} {unit} กับ {b} {show(v['nb'])} {unit} ให้ทำปฏิกิริยาตามสมการ "
                              f"{equation_text(eq)}{extra} สารใดเป็นสารกำหนดปริมาณ",
                         correct=f"{limiting} เพราะหมดก่อน",
                         wrongs=(f"{excess} เพราะหมดก่อน", f"{limiting} เพราะเหลืออยู่หลังปฏิกิริยาสิ้นสุด",
                                 "ไม่มี เพราะทำปฏิกิริยาพอดีกัน",
                                 # The wrong reactant with a wrong reason.
                                 f"{excess} เพราะเหลืออยู่หลังปฏิกิริยาสิ้นสุด",
                                 f"{excess} เพราะมีจำนวนโมลน้อยกว่า"),
                         topic=TOPIC_LIMIT,
                         hint="เปลี่ยนเป็นโมล หารด้วยสัมประสิทธิ์ในสมการ สารที่ได้ค่าน้อยกว่าหมดก่อนและเป็นสารกำหนดปริมาณ")


@question_type(
    "chem.limiting_reagent_fluency",
    display_name={"th": "ปริมาณผลิตภัณฑ์จากสารกำหนดปริมาณ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_LIMIT,
)
class LimitingReagentFluency(QuestionType):
    """The product follows the reactant that runs out."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        grams = rng.random() < 0.5
        eq, a, b, limiting, excess, product, v = limiting_case(rng, grams)
        unit = "กรัม" if grams else "โมล"
        extra = (f" (มวลต่อโมล {a} = {show(mass_of(a))}, {b} = {show(mass_of(b))}, "
                 f"{product[1]} = {show(mass_of(product[1]))})") if grams else ""
        return numeric(stem=f"ผสม {a} {show(v['na'])} {unit} กับ {b} {show(v['nb'])} {unit} ให้ทำปฏิกิริยาตามสมการ "
                            f"{equation_text(eq)}{extra} จะได้ {product[1]} มากที่สุดกี่{unit}",
                       answer=v["product"], wrongs=[v["product"] * 2, v["na"] + v["nb"] if not grams else v["product"] + 1,
                                                   v["product"] / 2 if exact(v["product"] / 2) else v["product"] + 2],
                       unit=unit, topic=TOPIC_LIMIT,
                       hint="หาสารกำหนดปริมาณก่อน แล้วคำนวณผลิตภัณฑ์จากสารนั้นเท่านั้น")


@question_type(
    "chem.limiting_reagent_application",
    display_name={"th": "สารที่เหลือจากปฏิกิริยาเมื่อมีสารกำหนดปริมาณ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_LIMIT,
)
class LimitingReagentApplication(QuestionType):
    """Excess left = what was there − what the limiting reagent used up."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        grams = rng.random() < 0.5
        eq, a, b, limiting, excess, _, v = limiting_case(rng, grams)
        unit = "กรัม" if grams else "โมล"
        extra = f" (มวลต่อโมล {a} = {show(mass_of(a))}, {b} = {show(mass_of(b))})" if grams else ""
        start_excess = v["na"] if excess == a else v["nb"]
        return numeric(stem=f"ผสม {a} {show(v['na'])} {unit} กับ {b} {show(v['nb'])} {unit} ให้ทำปฏิกิริยาตามสมการ "
                            f"{equation_text(eq)}{extra} เมื่อปฏิกิริยาสิ้นสุด สารที่มากเกินพอเหลืออยู่กี่{unit}",
                       answer=v["left"], wrongs=[start_excess, start_excess - v["left"] if start_excess != 2 * v["left"] else v["left"] * 3,
                                                 v["left"] * 2], unit=unit, topic=TOPIC_LIMIT,
                       hint="สารกำหนดปริมาณใช้หมด คำนวณว่าสารอีกตัวถูกใช้ไปเท่าใดตามอัตราส่วน แล้วลบออกจากที่มีอยู่")
