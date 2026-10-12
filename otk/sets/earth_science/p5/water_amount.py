"""ปริมาณน้ำในแหล่งต่าง ๆ

ธรณีวิทยา · ป.5 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.5/1

Sets moved here from: science_wave_c12.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b24 import PRIMARY_FIVE
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c12 import AMOUNT_SCENARIOS

PROVENANCE = Provenance("original")


AMOUNT_TOPIC = "ปริมาณน้ำในแหล่งต่าง ๆ"


class Source(NamedTuple):
    """A kind of water on Earth, its share per 1,000 parts, and whether people can use it."""
    name: str
    parts: int
    usable: bool


# Rounded shares of all the water on Earth, per 1,000 parts. Only the liquid
# fresh water people can reach — under the ground and on the surface — counts as
# usable; sea water is salty and ice is frozen and far away.
SOURCES = (
    Source("มหาสมุทรและทะเล", 970, False),
    Source("ธารน้ำแข็งและพืดน้ำแข็ง", 20, False),
    Source("น้ำใต้ดิน", 9, True),
    Source("แม่น้ำ ลำคลอง หนอง และบึง", 1, True),
)


SCALES = (1, 2, 3, 4, 5, 10)


UNITS = ("ขวด", "ถ้วย", "ลิตร")


def water_table(rng: Random) -> tuple[str, dict[str, int], str]:
    """The share of each source, scaled per draw, as printed in the stem."""
    scale = rng.choice(SCALES)
    unit = rng.choice(UNITS)
    amounts = {source.name: source.parts * scale for source in SOURCES}
    total = sum(amounts.values())
    text = (f"ถ้าเปรียบน้ำทั้งหมดบนโลกเป็นน้ำ {total:,} {unit} จะแบ่งได้ดังนี้ — "
            + " / ".join(f"{name} {amount:,} {unit}" for name, amount in amounts.items()))
    return text, amounts, unit


def _usable(amounts: dict[str, int]) -> int:
    return sum(amounts[source.name] for source in SOURCES if source.usable)


@question_type(
    "geo.water_amount_foundation",
    display_name={"th": "เปรียบเทียบปริมาณน้ำในแต่ละแหล่งจากข้อมูล"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=AMOUNT_TOPIC,
)
class WaterAmountFoundation(QuestionType):
    """Compare the amount of water in each source — the first free verb."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        text, amounts, unit = water_table(rng)
        names = list(amounts)
        draw = rng.random()
        if draw < 0.35:
            wanted = rng.choice(("มากที่สุด", "น้อยที่สุด"))
            pick = max if wanted == "มากที่สุด" else min
            answer = pick(amounts, key=amounts.get)
            return _labelled(
                stem=f"{text} จากข้อมูลนี้ แหล่งน้ำใดมีปริมาณน้ำ{wanted}",
                correct=answer,
                wrongs=tuple(name for name in names if name != answer),
                hint="เปรียบเทียบตัวเลขของทุกแหล่งในข้อมูล",
                topic=AMOUNT_TOPIC,
            )
        if draw < 0.7:
            ranked = sorted(names, key=amounts.get, reverse=True)
            orders = {" > ".join(ranked): None}   # insertion-ordered, unlike a set
            while len(orders) < 4:
                shuffled = ranked[:]
                rng.shuffle(shuffled)
                orders[" > ".join(shuffled)] = None
            return _labelled(
                stem=f"{text} จากข้อมูลนี้ ข้อใดเรียงแหล่งน้ำจากปริมาณมากไปน้อยได้ถูกต้อง",
                correct=" > ".join(ranked),
                wrongs=tuple(order for order in orders if order != " > ".join(ranked)),
                hint="หาแหล่งที่มากที่สุดก่อน แล้วไล่ลงไปทีละแหล่ง",
                topic=AMOUNT_TOPIC,
            )
        first, second = rng.sample(names[:3], 2)
        if amounts[first] < amounts[second]:
            first, second = second, first
        difference = amounts[first] - amounts[second]
        return _labelled(
            stem=f"{text} จากข้อมูลนี้ {first}มีน้ำมากกว่า{second}กี่{unit}",
            correct=f"{difference:,} {unit}",
            wrongs=(f"{amounts[first] + amounts[second]:,} {unit}",
                    f"{amounts[first]:,} {unit}",
                    f"{amounts[second]:,} {unit}"),
            hint="นำปริมาณที่มากกว่าลบด้วยปริมาณที่น้อยกว่า",
            topic=AMOUNT_TOPIC,
        )


@question_type(
    "geo.water_amount_fluency",
    display_name={"th": "ระบุปริมาณน้ำที่มนุษย์นำมาใช้ได้จากข้อมูล"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=AMOUNT_TOPIC,
)
class WaterAmountFluency(QuestionType):
    """Identify how much of the water people can use — the second free verb."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        text, amounts, unit = water_table(rng)
        usable = _usable(amounts)
        surface = amounts[SOURCES[3].name]
        fresh = sum(amounts[source.name] for source in SOURCES[1:])
        if rng.random() < 0.5:
            return _labelled(
                stem=f"{text} จากข้อมูลนี้ น้ำที่มนุษย์สามารถนำมาใช้ประโยชน์ได้มีประมาณกี่{unit}",
                correct=f"{usable:,} {unit}",
                wrongs=(f"{surface:,} {unit}",
                        f"{fresh:,} {unit}",
                        f"{amounts[SOURCES[0].name]:,} {unit}"),
                hint="นับเฉพาะน้ำจืดที่เป็นของเหลวและมนุษย์เข้าถึงได้ ไม่นับน้ำเค็มและน้ำแข็ง",
                topic=AMOUNT_TOPIC,
            )
        usable_names = " และ".join(source.name for source in SOURCES if source.usable)
        return _labelled(
            stem=f"{text} จากข้อมูลนี้ แหล่งใดเป็นน้ำที่มนุษย์สามารถนำมาใช้ประโยชน์ได้ "
                 f"และรวมกันมีกี่{unit}",
            correct=f"{usable_names} รวม {usable:,} {unit}",
            wrongs=(f"{SOURCES[0].name} รวม {amounts[SOURCES[0].name]:,} {unit}",
                    f"{SOURCES[1].name}และ{SOURCES[2].name} รวม "
                    f"{amounts[SOURCES[1].name] + amounts[SOURCES[2].name]:,} {unit}",
                    f"{SOURCES[3].name}เท่านั้น รวม {surface:,} {unit}"),
            hint="น้ำเค็มดื่มไม่ได้ และน้ำแข็งอยู่ไกลและแข็งตัว จึงนำมาใช้ได้ยาก",
            topic=AMOUNT_TOPIC,
        )


@question_type(
    "geo.water_amount_application",
    display_name={"th": "ใช้ข้อมูลปริมาณน้ำอธิบายความสำคัญของน้ำจืด"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=AMOUNT_TOPIC,
)
class WaterAmountApplication(QuestionType):
    """Explain why usable water is scarce, and what losing a source would mean."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, AMOUNT_SCENARIOS,
            hint="นึกว่าน้ำส่วนใหญ่บนโลกอยู่ที่ใด และมนุษย์ใช้น้ำแบบใดได้",
        ), AMOUNT_TOPIC)
