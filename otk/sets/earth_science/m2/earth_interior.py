"""โครงสร้างภายในโลก

ธรณีวิทยา · ม.2 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.2/4

Sets moved here from: science_wave_c20.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b8 import LEVEL as MIDDLE_TWO
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import LETTERS, SUBJECT
from otk.sets._support.science_wave_c20 import INTERIOR_FACTS, INTERIOR_SCENARIOS

PROVENANCE = Provenance("original")


INTERIOR_TOPIC = "โครงสร้างภายในโลก"


class Shell(NamedTuple):
    """A chemical layer of the Earth, its depth, main elements and density band."""
    name: str
    depth: str
    elements: str
    density: tuple[float, float]


# Densities in g/cm³ from non-overlapping bands, so the densest row is always the
# core and the lightest the crust, as the real layers are.
SHELLS = (
    Shell("เปลือกโลก", "ผิวโลกถึงลึกประมาณ 5 ถึง 70 กิโลเมตร",
          "ออกซิเจน ซิลิคอน อะลูมิเนียม", (2.6, 3.0)),
    Shell("เนื้อโลก", "ใต้เปลือกโลกถึงลึกประมาณ 2,900 กิโลเมตร",
          "ออกซิเจน ซิลิคอน แมกนีเซียม และเหล็ก", (3.3, 5.6)),
    Shell("แก่นโลก", "ลึกประมาณ 2,900 กิโลเมตรถึงใจกลางโลก",
          "เหล็กและนิกเกิล", (9.9, 13.0)),
)


def layer_table(rng: Random) -> list[tuple[Shell, float]]:
    rows = [(shell, round(rng.uniform(*shell.density), 1)) for shell in SHELLS]
    rng.shuffle(rows)
    return rows


@question_type(
    "geo.earth_interior_foundation",
    display_name={"th": "ชั้นของโลกตามองค์ประกอบทางเคมี"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=INTERIOR_TOPIC,
)
class EarthInteriorFoundation(QuestionType):
    """Name the three layers and what each is made of, without a data table."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, INTERIOR_FACTS,
            hint="ยิ่งลึกยิ่งมีธาตุที่หนักมาก",
        ), INTERIOR_TOPIC)


@question_type(
    "geo.earth_interior_fluency",
    display_name={"th": "อธิบายโครงสร้างภายในโลกจากข้อมูล"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=INTERIOR_TOPIC,
)
class EarthInteriorFluency(QuestionType):
    """Name the layer each row of a collected layer table describes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rows = layer_table(rng)
        record = " / ".join(
            f"ชั้น {letter}: ความลึก {shell.depth} ธาตุหลัก {shell.elements} ความหนาแน่น {density} กรัมต่อลูกบาศก์เซนติเมตร"
            for letter, (shell, density) in zip(LETTERS, rows))
        index = rng.randrange(3)
        shell = rows[index][0]
        return _labelled(
            stem=f"แบบจำลองโครงสร้างภายในโลกสร้างจากข้อมูลที่รวบรวมได้ — {record} "
                 f"จากข้อมูลนี้ ชั้น {LETTERS[index]} คือชั้นใด",
            correct=shell.name,
            wrongs=tuple(other.name for other in SHELLS if other.name != shell.name) + ("ชั้นบรรยากาศ",),
            hint="ดูความลึกและธาตุหลัก ชั้นที่ลึกที่สุดมีธาตุหนักและความหนาแน่นสูงที่สุด",
            topic=INTERIOR_TOPIC,
        )


@question_type(
    "geo.earth_interior_application",
    display_name={"th": "วิเคราะห์โครงสร้างภายในโลก"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=INTERIOR_TOPIC,
)
class EarthInteriorApplication(QuestionType):
    """Why heavy metals sank, how the interior is known, and judging a model."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, INTERIOR_SCENARIOS,
            hint="นึกถึงความหนาแน่นของธาตุ และหลักฐานที่วัดได้จากผิวโลก",
        ), INTERIOR_TOPIC)
