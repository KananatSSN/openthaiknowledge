"""สมการเคมีและการดุลสมการเคมี

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.4/1

Sets moved here from: science_wave_f30.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f30 import (
    EQUATIONS,
    SUBJECT,
    UPPER_FOUR,
    equation_text,
    species,
)

PROVENANCE = Provenance("original")


TOPIC_EQUATION = "สมการเคมีและการดุลสมการเคมี"


STATES = {"s": "ของแข็ง", "l": "ของเหลว", "g": "แก๊ส", "aq": "สารละลายในน้ำ"}


SYMBOLS = (
    ("(s)", "สารอยู่ในสถานะของแข็ง"), ("(l)", "สารอยู่ในสถานะของเหลว"), ("(g)", "สารอยู่ในสถานะแก๊ส"),
    ("(aq)", "สารละลายในน้ำ"), ("→", "เกิดปฏิกิริยาไปข้างหน้าจนสมบูรณ์ (ไปทางเดียว)"),
    ("⇌", "ปฏิกิริยาเกิดได้ทั้งไปข้างหน้าและย้อนกลับ"), ("Δ เหนือลูกศร", "ต้องให้ความร้อนแก่ปฏิกิริยา"),
    ("ตัวเลขหน้าสูตร", "จำนวนโมล (หรือจำนวนโมเลกุล) ของสารที่ทำปฏิกิริยาพอดีกัน"),
)


@question_type(
    "chem.equation_balance_foundation",
    display_name={"th": "ความหมายของสัญลักษณ์ในสมการเคมี"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EQUATION,
)
class EquationBalanceFoundation(QuestionType):
    """States, arrows, heat, and the coefficients as mole ratios."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "(s) ของแข็ง (l) ของเหลว (g) แก๊ส (aq) สารละลายในน้ำ ตัวเลขหน้าสูตรคืออัตราส่วนโดยโมล"
        if rng.random() < 0.4:
            symbol, meaning = rng.choice(SYMBOLS)
            others = [m for s, m in SYMBOLS if s != symbol]
            return _labelled(stem=f"สัญลักษณ์ {symbol} ในสมการเคมีหมายความว่าอย่างไร", correct=meaning,
                             wrongs=tuple(others), topic=TOPIC_EQUATION, hint=hint)
        eq = rng.choice(EQUATIONS)
        coef, formula, state = rng.choice(species(eq))
        if rng.random() < 0.5:
            return _labelled(stem=f"ในสมการ {equation_text(eq, states=True)} สาร {formula} อยู่ในสถานะใด",
                             correct=STATES[state], wrongs=tuple(v for k, v in STATES.items() if k != state),
                             topic=TOPIC_EQUATION, hint=hint)
        a, b = rng.sample(species(eq), 2)
        return _labelled(stem=f"จากสมการ {equation_text(eq)} อัตราส่วนโดยโมลของ {a[1]} ต่อ {b[1]} เป็นเท่าใด",
                         correct=f"{a[0]} : {b[0]}",
                         wrongs=tuple(dict.fromkeys(x for x in (f"{b[0]} : {a[0]}", "1 : 1", f"{a[0] + 1} : {b[0]}",
                                                                   f"{a[0]} : {b[0] + 1}", f"{a[0] * 2} : {b[0]}",
                                                                   f"{a[0]} : {b[0] + 2}")
                                                    if x != f"{a[0]} : {b[0]}"))[:3],
                         topic=TOPIC_EQUATION, hint=hint)


@question_type(
    "chem.equation_balance_fluency",
    display_name={"th": "ดุลสมการเคมี"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EQUATION,
)
class EquationBalanceFluency(QuestionType):
    """The smallest whole-number coefficients that make every atom count match."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq = rng.choice(EQUATIONS)
        hint = "ดุลธาตุที่ปรากฏน้อยที่สุดก่อน ดุล H และ O ท้ายสุด แล้วตรวจให้จำนวนอะตอมแต่ละธาตุเท่ากันทั้งสองข้าง"
        if rng.random() < 0.6:
            coef, formula, _ = rng.choice(species(eq))
            return numeric(stem=f"ดุลสมการ {equation_text(eq, blanks=True)} ด้วยเลขจำนวนเต็มน้อยที่สุด "
                                f"สัมประสิทธิ์ของ {formula} เท่าใด",
                           answer=coef, wrongs=[coef + 1, coef * 2, coef + 2], unit="", topic=TOPIC_EQUATION, hint=hint)
        total = sum(c for c, _, _ in species(eq))
        return numeric(stem=f"ดุลสมการ {equation_text(eq, blanks=True)} ด้วยเลขจำนวนเต็มน้อยที่สุด "
                            "ผลรวมสัมประสิทธิ์ทั้งหมดเท่าใด",
                       answer=total, wrongs=[total + 1, total - 1, len(species(eq))], unit="", topic=TOPIC_EQUATION,
                       hint=hint)


@question_type(
    "chem.equation_balance_application",
    display_name={"th": "ตรวจสอบสมการเคมีที่ดุลแล้ว"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EQUATION,
)
class EquationBalanceApplication(QuestionType):
    """Pick the balanced equation; the others are off by one coefficient."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq = rng.choice(EQUATIONS)
        wrongs = set()
        tries = 0
        while len(wrongs) < 3 and tries < 50:
            tries += 1
            side = rng.randrange(2)
            items = list(eq[side])
            i = rng.randrange(len(items))
            c, f, st = items[i]
            new_c = c + rng.choice((1, -1, 1)) if c > 1 else c + 1
            items[i] = (new_c, f, st)
            bad = (tuple(items), eq[1]) if side == 0 else (eq[0], tuple(items))
            wrongs.add(equation_text(bad))
        return _labelled(stem="สมการเคมีใดดุลแล้ว", correct=equation_text(eq), wrongs=tuple(sorted(wrongs))[:3],
                         topic=TOPIC_EQUATION, hint="นับจำนวนอะตอมของแต่ละธาตุทั้งสองข้างของลูกศร ต้องเท่ากันทุกธาตุ")
