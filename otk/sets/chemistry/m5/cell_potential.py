"""ศักย์ไฟฟ้ามาตรฐานของเซลล์

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/29

Sets moved here from: science_wave_f39.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f39 import (
    COUPLES,
    SUBJECT,
    UPPER_FIVE,
    diagram,
    e_text,
    pair,
    potentials,
)

PROVENANCE = Provenance("original")


TOPIC_EMF = "ศักย์ไฟฟ้ามาตรฐานของเซลล์"


@question_type(
    "chem.cell_potential_foundation",
    display_name={"th": "คำนวณ E°cell ของเซลล์กัลวานิก"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EMF,
)
class CellPotentialFoundation(QuestionType):
    """E°cell = E°cathode − E°anode."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        anode, cathode = pair(rng)
        value = cathode[2] - anode[2]
        return numeric(stem=f"เซลล์ {diagram(anode, cathode)} ({potentials(anode, cathode)}) มีค่า E°cell เท่าใด",
                       answer=value, wrongs=[abs(cathode[2] + anode[2]) or value + 1, value + Fraction(1, 10), value * 2],
                       unit="V", topic=TOPIC_EMF, hint="E°cell = E°แคโทด − E°แอโนด (ใช้ศักย์รีดักชันตามตาราง ไม่คูณด้วยสัมประสิทธิ์)")


@question_type(
    "chem.cell_potential_fluency",
    display_name={"th": "ระบุชนิดเซลล์จากค่า E°cell"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EMF,
)
class CellPotentialFluency(QuestionType):
    """Positive E°cell: galvanic, runs by itself. Negative: electrolytic, needs a power supply."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, b = rng.sample(COUPLES, 2)
        # Written as a (left, oxidised) || b (right, reduced), whichever way round that is.
        value = b[2] - a[2]
        galvanic = value > 0
        right = ("เซลล์กัลวานิก เพราะ E°cell เป็นบวก ปฏิกิริยาเกิดได้เอง" if galvanic
                 else "เซลล์อิเล็กโทรไลต์ เพราะ E°cell เป็นลบ ต้องใช้ไฟฟ้าจากภายนอก")
        wrongs = ("เซลล์อิเล็กโทรไลต์ เพราะ E°cell เป็นลบ ต้องใช้ไฟฟ้าจากภายนอก" if galvanic
                  else "เซลล์กัลวานิก เพราะ E°cell เป็นบวก ปฏิกิริยาเกิดได้เอง",
                  "เซลล์กัลวานิก เพราะ E°cell เป็นลบ", "เซลล์อิเล็กโทรไลต์ เพราะ E°cell เป็นบวก")
        if rng.random() < 0.5:
            return numeric(stem=f"เซลล์ที่เขียนเป็น {diagram(a, b)} ({potentials(a, b)}) มีค่า E°cell เท่าใด",
                           answer=value, wrongs=[-value, value + Fraction(1, 10), a[2] + b[2] if a[2] + b[2] not in (value, -value) and a[2] + b[2] else value * 2],
                           unit="V", topic=TOPIC_EMF, allow_negative=True,
                           hint="E°cell = E°ขวา (แคโทด) − E°ซ้าย (แอโนด) ค่าลบแสดงว่าปฏิกิริยาไม่เกิดเองตามที่เขียน")
        return _labelled(stem=f"ปฏิกิริยาตามแผนภาพ {diagram(a, b)} ({potentials(a, b)}) เป็นเซลล์ชนิดใด", correct=right,
                         wrongs=wrongs, topic=TOPIC_EMF, hint="E°cell > 0 เกิดได้เอง (กัลวานิก) E°cell < 0 ต้องให้ไฟฟ้า (อิเล็กโทรไลต์)")


@question_type(
    "chem.cell_potential_application",
    display_name={"th": "เลือกครึ่งเซลล์ให้ได้ศักย์สูงสุดและหาค่า E° ที่ไม่ทราบ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EMF,
)
class CellPotentialApplication(QuestionType):
    """The widest gap in E° gives the biggest voltage; a known E°cell fixes an unknown E°."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            chosen = rng.sample(COUPLES, 4)
            best = (min(chosen, key=lambda c: c[2]), max(chosen, key=lambda c: c[2]))
            listed = ", ".join(f"{c[1]}/{c[0]} {e_text(c[2])}" for c in chosen)
            right = f"{best[0][0]} กับ {best[1][0]}"
            pairs = [f"{x[0]} กับ {y[0]}" for i, x in enumerate(sorted(chosen, key=lambda c: c[2]))
                     for y in sorted(chosen, key=lambda c: c[2])[i + 1:]]
            return _labelled(stem=f"จากค่า E°: {listed} ครึ่งเซลล์คู่ใดประกอบเป็นเซลล์กัลวานิกที่มีศักย์ไฟฟ้ามากที่สุด",
                             correct=right, wrongs=tuple([p for p in pairs if p != right]), topic=TOPIC_EMF,
                             hint="เลือกคู่ที่ค่า E° ต่างกันมากที่สุด (ต่ำสุดเป็นแอโนด สูงสุดเป็นแคโทด)")
        anode, cathode = pair(rng)
        value = cathode[2] - anode[2]
        hide_anode = rng.random() < 0.5
        known = cathode if hide_anode else anode
        hidden = anode if hide_anode else cathode
        return numeric(stem=f"เซลล์ {diagram(anode, cathode)} มีค่า E°cell = {e_text(value)} ถ้า E° ของ {known[1]}/{known[0]} = "
                            f"{e_text(known[2])} ค่า E° ของ {hidden[1]}/{hidden[0]} เท่าใด",
                       answer=hidden[2], wrongs=[-hidden[2] if hidden[2] else Fraction(1, 10), known[2] + value if hide_anode else known[2] - value,
                                                 hidden[2] + Fraction(1, 10)],
                       unit="V", topic=TOPIC_EMF, allow_negative=True,
                       hint="E°cell = E°แคโทด − E°แอโนด แทนค่าที่รู้แล้วแก้หาค่าที่ไม่รู้")
