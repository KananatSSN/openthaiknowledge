"""กราฟการเปลี่ยนแปลงปริมาณสารในปฏิกิริยา

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/1

Sets moved here from: science_wave_f33.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f33 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_GRAPH = "กราฟการเปลี่ยนแปลงปริมาณสารในปฏิกิริยา"


GAS_RUNS = (
    ("Mg(s) + 2HCl(aq) → MgCl₂(aq) + H₂(g)", "H₂"),
    ("CaCO₃(s) + 2HCl(aq) → CaCl₂(aq) + H₂O(l) + CO₂(g)", "CO₂"),
    ("2H₂O₂(aq) → 2H₂O(l) + O₂(g)", "O₂"),
    ("Zn(s) + 2HCl(aq) → ZnCl₂(aq) + H₂(g)", "H₂"),
)


# Increments per interval, shrinking to zero: a reaction slowing as reactant runs out.
PATTERNS = ((20, 14, 9, 5, 2, 0), (24, 16, 10, 6, 4, 0), (30, 18, 10, 6, 2, 0, 0), (16, 12, 8, 5, 3, 1, 0),
            (18, 12, 7, 3, 0, 0), (26, 15, 9, 5, 3, 2, 0))


def gas_table(rng: Random):
    reaction, gas = rng.choice(GAS_RUNS)
    steps = rng.choice(PATTERNS)
    scale = rng.choice((1, 2, 3, 5))
    step = rng.choice((10, 15, 20, 30))
    volumes = [0]
    for inc in steps:
        volumes.append(volumes[-1] + inc * scale)
    times = [i * step for i in range(len(volumes))]
    return reaction, gas, times, volumes


def table_text(times, volumes, unit="cm³") -> str:
    return "; ".join(f"{t} s: {v} {unit}" for t, v in zip(times, volumes))


@question_type(
    "chem.rate_graph_foundation",
    display_name={"th": "ลักษณะกราฟปริมาณสารตั้งต้นและผลิตภัณฑ์กับเวลา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GRAPH,
)
class RateGraphFoundation(QuestionType):
    """Reactants fall and products rise, fast at first and then levelling off."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        reaction, gas = rng.choice(GAS_RUNS)
        reactant = reaction.split(" + ")[0].split("(")[0].lstrip("2")
        shapes = {
            "product": "เพิ่มขึ้นเร็วในช่วงแรก แล้วค่อย ๆ ช้าลงจนคงที่",
            "reactant": "ลดลงเร็วในช่วงแรก แล้วค่อย ๆ ช้าลงจนคงที่",
            "line_up": "เพิ่มขึ้นด้วยอัตราคงที่เป็นเส้นตรง",
            "line_down": "ลดลงด้วยอัตราคงที่เป็นเส้นตรงจนเป็นศูนย์",
            "late": "เพิ่มขึ้นช้าในช่วงแรก แล้วเร็วขึ้นเรื่อย ๆ",
        }
        if rng.random() < 0.5:
            right = shapes["product"]
            stem = f"ปฏิกิริยา {reaction} กราฟปริมาตรแก๊ส {gas} ที่เกิดขึ้นกับเวลามีลักษณะอย่างไร"
        else:
            right = shapes["reactant"]
            stem = f"ปฏิกิริยา {reaction} กราฟปริมาณ {reactant} ที่เหลืออยู่กับเวลามีลักษณะอย่างไร"
        return _labelled(stem=stem, correct=right, wrongs=tuple([v for v in shapes.values() if v != right]),
                         topic=TOPIC_GRAPH,
                         hint="ช่วงแรกสารตั้งต้นมีมาก ปฏิกิริยาจึงเร็ว เมื่อสารตั้งต้นลดลงปฏิกิริยาช้าลง กราฟจึงค่อย ๆ ราบ")


@question_type(
    "chem.rate_graph_fluency",
    display_name={"th": "อ่านข้อมูลปริมาตรแก๊สกับเวลา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GRAPH,
)
class RateGraphFluency(QuestionType):
    """Total gas, the time it stops, and the fastest interval."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        reaction, gas, times, volumes = gas_table(rng)
        stem = f"ปฏิกิริยา {reaction} วัดปริมาตรแก๊ส {gas} สะสมได้ดังนี้ {table_text(times, volumes)}"
        kind = rng.randrange(3)
        if kind == 0:
            return numeric(stem=f"{stem} ปฏิกิริยาให้แก๊ส {gas} ทั้งหมดกี่ cm³", answer=volumes[-1],
                           wrongs=[volumes[-2] if volumes[-2] != volumes[-1] else volumes[-3], sum(volumes) // len(volumes) or 1,
                                   volumes[1]], unit="cm³", topic=TOPIC_GRAPH,
                           hint="เมื่อปริมาตรไม่เพิ่มอีก ปฏิกิริยาสิ้นสุดแล้ว ค่าสุดท้ายคือปริมาตรแก๊สทั้งหมด")
        if kind == 1:
            stop = next(t for t, v in zip(times, volumes) if v == volumes[-1])
            return numeric(stem=f"{stem} ปฏิกิริยาสิ้นสุดที่เวลาประมาณกี่วินาที", answer=stop,
                           wrongs=[times[-1] if times[-1] != stop else stop + times[1], stop - times[1] or times[1] * 2,
                                   times[1]], unit="s", topic=TOPIC_GRAPH,
                           hint="ปฏิกิริยาสิ้นสุดเมื่อปริมาตรแก๊สหยุดเพิ่มเป็นครั้งแรก")
        labels = [f"{times[i]}-{times[i + 1]} s" for i in range(len(times) - 1)]
        right = labels[0]
        return _labelled(stem=f"{stem} ช่วงเวลาใดมีอัตราการเกิดแก๊สสูงที่สุด", correct=right,
                         wrongs=tuple(labels[1:]), topic=TOPIC_GRAPH,
                         hint="ช่วงเวลาเท่ากัน ช่วงที่ปริมาตรเพิ่มมากที่สุดมีอัตราสูงที่สุด")


@question_type(
    "chem.rate_graph_application",
    display_name={"th": "คำนวณอัตราจากข้อมูลและเปรียบเทียบช่วงเวลา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GRAPH,
)
class RateGraphApplication(QuestionType):
    """Average rate over an interval of the table, and over the whole run."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            reaction, gas, times, volumes = gas_table(rng)
            i, j = sorted(rng.sample(range(len(times)), 2))
            rate = Fraction(volumes[j] - volumes[i], times[j] - times[i])
            return (reaction, gas, times, volumes, i, j, rate) if exact(rate) and rate > 0 else None

        reaction, gas, times, volumes, i, j, rate = _find(rng, draw)
        return numeric(stem=f"ปฏิกิริยา {reaction} วัดปริมาตรแก๊ส {gas} สะสมได้ดังนี้ {table_text(times, volumes)} "
                            f"อัตราการเกิดแก๊สเฉลี่ยช่วง {times[i]}-{times[j]} s เท่าใด",
                       answer=rate, wrongs=[Fraction(volumes[j], times[j]) if exact(Fraction(volumes[j], times[j])) and volumes[i] else rate * 2,
                                            rate * 2, Fraction(times[j] - times[i], volumes[j] - volumes[i]) if exact(Fraction(times[j] - times[i], volumes[j] - volumes[i])) else rate + 1],
                       unit="cm³/s", topic=TOPIC_GRAPH,
                       hint="อัตราเฉลี่ย = (ปริมาตรที่ปลายช่วง − ปริมาตรที่ต้นช่วง) ÷ ระยะเวลาของช่วง")
