"""ปัจจัยที่มีผลต่อการเปลี่ยนแปลงขนาดประชากร

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.1 ม.4/3

Sets moved here from: science_wave_b33.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b19 import UPPER_FOUR, Fact, _fact_question
from otk.sets._support.science_wave_b31 import ECOLOGY_TOPIC
from otk.sets._support.science_wave_b33 import (
    BIOLOGICAL,
    PHYSICAL,
    POPULATION_EFFECTS,
    POPULATION_SCENARIOS,
)

PROVENANCE = Provenance("original")


class Factor(NamedTuple):
    """A change in the surroundings and which kind of component it is."""
    change: str
    kind: str


FACTORS = (
    Factor("ฝนแล้งยาวนานจนแหล่งน้ำแห้ง", PHYSICAL),
    Factor("อุณหภูมิน้ำทะเลสูงขึ้นผิดปกติ", PHYSICAL),
    Factor("น้ำท่วมใหญ่ท่วมพื้นที่เป็นเวลานาน", PHYSICAL),
    Factor("ความเค็มของน้ำในปากแม่น้ำเพิ่มขึ้นในหน้าแล้ง", PHYSICAL),
    Factor("ไฟป่าจากฟ้าผ่าเผาทุ่งหญ้า", PHYSICAL),
    Factor("เชื้อโรคระบาดในประชากร", BIOLOGICAL),
    Factor("สัตว์ต่างถิ่นเข้ามาแย่งอาหาร", BIOLOGICAL),
    Factor("จำนวนผู้ล่าเพิ่มขึ้น", BIOLOGICAL),
    Factor("พืชที่เป็นอาหารถูกแมลงศัตรูพืชทำลาย", BIOLOGICAL),
    Factor("ปรสิตเกาะกินสัตว์ในฝูงจำนวนมาก", BIOLOGICAL),
)


POPULATION_FACTS = (
    Fact("ขนาดประชากรจะเพิ่มขึ้นเมื่อใด",
         "เมื่อจำนวนที่เกิดรวมกับที่อพยพเข้า มากกว่าจำนวนที่ตายรวมกับที่อพยพออก"),
    Fact("องค์ประกอบทางกายภาพที่มีผลต่อขนาดประชากรมีอะไรบ้าง",
         "อุณหภูมิ ปริมาณน้ำ แสง ความเค็ม และภัยธรรมชาติ"),
    Fact("องค์ประกอบทางชีวภาพที่มีผลต่อขนาดประชากรมีอะไรบ้าง",
         "ผู้ล่า เชื้อโรค ปรสิต คู่แข่งขัน และสิ่งมีชีวิตที่เป็นอาหาร"),
    Fact("เหตุใดประชากรจึงเพิ่มขึ้นไปเรื่อย ๆ ไม่ได้",
         "เพราะอาหาร พื้นที่ และทรัพยากรมีจำกัด "
         "ประชากรจึงเพิ่มได้ถึงระดับที่สิ่งแวดล้อมรองรับได้เท่านั้น"),
    Fact("การแก่งแย่งกันภายในประชากรเดียวกันจะรุนแรงขึ้นเมื่อใด",
         "เมื่อประชากรหนาแน่นมากจนอาหารและพื้นที่ไม่พอสำหรับทุกตัว"),
    Fact("เหตุใดโรคระบาดจึงลดขนาดประชากรที่อยู่กันหนาแน่นได้รุนแรงกว่า",
         "เพราะสมาชิกอยู่ใกล้กัน เชื้อโรคจึงแพร่จากตัวหนึ่งไปสู่อีกตัวได้เร็ว"),
)


@question_type(
    "ecology.population_change_foundation",
    display_name={"th": "ปัจจัยที่มีผลต่อขนาดประชากร"},
    level=UPPER_FOUR, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class PopulationChangeFoundation(QuestionType):
    """Give examples of physical and biological changes that move a population."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            return _fact_question(
                rng, POPULATION_FACTS, topic=ECOLOGY_TOPIC,
                hint="ขนาดประชากรเปลี่ยนได้สี่ทาง คือ เกิด ตาย อพยพเข้า และอพยพออก",
            )
        kind = rng.choice((PHYSICAL, BIOLOGICAL))
        item = rng.choice([one for one in FACTORS if one.kind == kind])
        others = [one.change for one in FACTORS if one.kind != kind]
        rng.shuffle(others)
        return _labelled(
            stem=f"ข้อใดเป็นตัวอย่างการเปลี่ยนแปลงขององค์ประกอบทาง{kind}"
                 "ที่มีผลต่อขนาดประชากร",
            correct=item.change, wrongs=tuple(others[:3]),
            hint="องค์ประกอบทางกายภาพไม่มีชีวิต ส่วนองค์ประกอบทางชีวภาพคือสิ่งมีชีวิตอื่น",
            topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.population_change_fluency",
    display_name={"th": "อธิบายการเปลี่ยนแปลงขนาดประชากร"},
    level=UPPER_FOUR, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class PopulationChangeFluency(QuestionType):
    """Explain how one physical or biological change moves a population."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(POPULATION_EFFECTS)
        return _labelled(
            stem=item.stem, correct=item.correct, wrongs=tuple(item.wrongs),
            hint="ถามว่าการเปลี่ยนแปลงนั้นทำให้เกิดมากขึ้น ตายมากขึ้น "
                 "หรืออพยพเข้าออกมากขึ้น",
            topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.population_change_application",
    display_name={"th": "วิเคราะห์ข้อมูลการเปลี่ยนแปลงขนาดประชากร"},
    level=UPPER_FOUR, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class PopulationChangeApplication(QuestionType):
    """Read population data and untangle which factor did what."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, POPULATION_SCENARIOS,
            hint="แยกให้ออกว่ามีปัจจัยใดเปลี่ยนไปบ้าง แล้วตามผลของแต่ละปัจจัยไปทีละขั้น",
        ), ECOLOGY_TOPIC)
