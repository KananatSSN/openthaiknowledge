"""ชั้นหน้าตัดดินและการเกิดดิน

ธรณีวิทยา · ม.2 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.2/6

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
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c13 import _swapped, _swaps
from otk.sets._support.science_wave_c15 import FIVE_LETTERS
from otk.sets._support.science_wave_c20 import SOIL_PROFILE_SCENARIOS
from otk.sets._support.life_earth_diagrams import SOIL_PROFILE_ALT, SOIL_PROFILES
from otk.sets._support.ms1_diagrams import diagram_question

PROVENANCE = Provenance("original")


SOIL_PROFILE_TOPIC = "ชั้นหน้าตัดดินและการเกิดดิน"


class Horizon(NamedTuple):
    """A soil horizon, and a description carrying its part in forming soil."""
    name: str
    description: str


HORIZONS = (
    Horizon("ชั้นโอ", "ชั้นบนสุด มีซากพืชซากสัตว์ทับถมและกำลังถูกย่อยสลาย เป็นแหล่งของฮิวมัส"),
    Horizon("ชั้นเอ", "ดินชั้นบนสีเข้ม เกิดจากหินผุผสมกับฮิวมัสที่ย่อยสลายจากชั้นบน เหมาะแก่การเพาะปลูก"),
    Horizon("ชั้นบี", "ดินชั้นล่าง สะสมแร่ธาตุและอนุภาคดินเหนียวที่น้ำชะล้างลงมาจากชั้นบน"),
    Horizon("ชั้นซี", "หินต้นกำเนิดที่ผุพังเป็นก้อนเล็กก้อนใหญ่ปนกัน เป็นจุดเริ่มต้นของการเกิดดิน"),
    Horizon("ชั้นอาร์", "หินพื้นที่ยังไม่ผุพัง อยู่ล่างสุดของหน้าตัดดิน"),
)


class Cause(NamedTuple):
    """A difference between two soils, and the factor that explains it."""
    case: str
    factor: str


FACTORS = ("ชนิดของหินต้นกำเนิด", "ภูมิอากาศ", "สิ่งมีชีวิต", "สภาพภูมิประเทศ", "ระยะเวลา")


# A second case for each factor; like CAUSES, only that factor differs.
MORE_CAUSES = (
    ("ดินสองแห่งอยู่ข้างกันบนที่ราบ ภูมิอากาศและพืชคลุมเหมือนกัน เกิดมานานเท่ากัน "
     "แต่แห่งหนึ่งเกิดจากหินทราย อีกแห่งเกิดจากหินบะซอลต์ ดินแห่งแรกเป็นดินทรายสีจาง แห่งหลังเป็นดินเหนียวสีแดงเข้ม",
     "ชนิดของหินต้นกำเนิด"),
    ("ดินที่เกิดจากหินชนิดเดียวกันบนที่ราบ แห่งหนึ่งอยู่ในเขตหนาวเย็น อีกแห่งอยู่ในเขตร้อนชื้น "
     "ดินในเขตร้อนชื้นผุพังเร็วกว่าและมีชั้นดินหนากว่า",
     "ภูมิอากาศ"),
    ("ดินสองแห่งเกิดจากหินเดียวกัน ภูมิอากาศเดียวกัน แห่งหนึ่งเป็นทุ่งหญ้าที่มีรากหญ้าหนาแน่นและปลวกมาก "
     "อีกแห่งเป็นลานหินที่แทบไม่มีสิ่งมีชีวิต ดินในทุ่งหญ้ามีอินทรียวัตถุมากกว่า",
     "สิ่งมีชีวิต"),
    ("ดินที่เกิดจากหินชนิดเดียวกันในภูมิอากาศเดียวกัน แห่งหนึ่งอยู่ในแอ่งที่น้ำขังบ่อย "
     "อีกแห่งอยู่บนเนินที่น้ำไหลออกเร็ว ดินในแอ่งหนากว่าและมีตะกอนละเอียดสะสมมากกว่า",
     "สภาพภูมิประเทศ"),
    ("ดินสองแห่งเกิดจากหินชนิดเดียวกัน ในภูมิอากาศและภูมิประเทศเดียวกัน แห่งหนึ่งเกิดบนดินถล่มที่เพิ่งเกิดเมื่อไม่กี่ปี "
     "อีกแห่งอยู่บนพื้นที่ที่ไม่ถูกรบกวนมาหลายพันปี ดินแห่งหลังมีชั้นหน้าตัดดินครบกว่า",
     "ระยะเวลา"),
)


CAUSES = (
    Cause("ดินสองแห่งอยู่ในที่ราบ ภูมิอากาศเดียวกัน มีพืชคลุมเหมือนกัน และเกิดมานานใกล้เคียงกัน "
          "แต่แห่งหนึ่งเกิดจากหินแกรนิต อีกแห่งเกิดจากหินปูน ดินจึงมีสีและธาตุอาหารต่างกัน",
          "ชนิดของหินต้นกำเนิด"),
    Cause("ดินที่เกิดจากหินชนิดเดียวกัน บนที่ราบเหมือนกัน แห่งหนึ่งอยู่ในเขตฝนชุกอากาศร้อนชื้น "
          "อีกแห่งอยู่ในเขตแห้งแล้ง ดินในเขตฝนชุกผุพังลึกกว่าและถูกชะล้างมากกว่า",
          "ภูมิอากาศ"),
    Cause("ดินสองแห่งเกิดจากหินชนิดเดียวกันในภูมิอากาศเดียวกัน แห่งหนึ่งเป็นป่าที่มีไส้เดือนและซากพืชมาก "
          "อีกแห่งเป็นลานโล่งไม่มีพืช ดินในป่ามีฮิวมัสมากและร่วนซุยกว่า",
          "สิ่งมีชีวิต"),
    Cause("ดินที่เกิดจากหินชนิดเดียวกันในภูมิอากาศเดียวกัน แห่งหนึ่งอยู่บนไหล่เขาลาดชัน "
          "อีกแห่งอยู่ในที่ราบเชิงเขา ดินบนไหล่เขาบางกว่าเพราะถูกน้ำพาออกไป",
          "สภาพภูมิประเทศ"),
    Cause("ดินสองแห่งเกิดจากหินชนิดเดียวกัน ในภูมิอากาศและภูมิประเทศเดียวกัน แห่งหนึ่งเพิ่งเริ่มเกิดบนลาวาที่เย็นตัวไม่นาน "
          "อีกแห่งเกิดมานานหลายหมื่นปี ดินแห่งหลังหนาและแบ่งชั้นชัดเจนกว่า",
          "ระยะเวลา"),
)


def _match_horizons(letters: list[str]) -> str:
    return " / ".join(f"{horizon.name} → {letter}" for horizon, letter in zip(HORIZONS, letters))


@question_type(
    "geo.soil_profile_foundation",
    display_name={"th": "ระบุปัจจัยที่ทำให้ดินมีลักษณะและสมบัติแตกต่างกัน"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=SOIL_PROFILE_TOPIC,
)
class SoilProfileFoundation(QuestionType):
    """Identify the one factor that differs between two soils — the free verb ระบุ."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cause = rng.choice(CAUSES + tuple(Cause(*row) for row in MORE_CAUSES))
        others = [factor for factor in FACTORS if factor != cause.factor]
        rng.shuffle(others)
        return _labelled(
            stem=f"{cause.case} ปัจจัยใดทำให้ดินสองแห่งนี้แตกต่างกัน",
            correct=cause.factor,
            wrongs=tuple(others[:3]),
            hint="หาสิ่งที่เหมือนกันในทั้งสองแห่งก่อน สิ่งที่ต่างกันเพียงอย่างเดียวคือปัจจัยที่ถาม",
            topic=SOIL_PROFILE_TOPIC,
        )


@question_type(
    "geo.soil_profile_fluency",
    display_name={"th": "อธิบายชั้นหน้าตัดดินและการเกิดดินจากแบบจำลอง"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=SOIL_PROFILE_TOPIC,
)
class SoilProfileFluency(QuestionType):
    """Place all five horizons of a model profile; each wrong choice swaps two."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shuffled = list(HORIZONS)
        rng.shuffle(shuffled)
        listing = " / ".join(f"{letter}. {horizon.description}"
                             for letter, horizon in zip(FIVE_LETTERS, shuffled))
        letter_of = {horizon.name: FIVE_LETTERS[i] for i, horizon in enumerate(shuffled)}
        right = [letter_of[horizon.name] for horizon in HORIZONS]
        return _labelled(
            stem=f"แบบจำลองหน้าตัดดินในขวดใส มีคำอธิบายแต่ละชั้นดังนี้ — {listing} "
                 "ข้อใดอธิบายชั้นหน้าตัดดินและกระบวนการเกิดดินได้ถูกต้องทั้งหมด",
            correct=_match_horizons(right),
            wrongs=tuple(_match_horizons(_swapped(right, i, j)) for i, j in _swaps(rng, 3, 5)),
            hint="เรียงจากบนลงล่าง: ซากพืช ดินชั้นบน ดินชั้นล่าง หินผุ และหินพื้น",
            topic=SOIL_PROFILE_TOPIC,
        )


@question_type(
    "geo.soil_profile_application",
    display_name={"th": "ใช้ความรู้เรื่องหน้าตัดดินในการเกษตรและการสำรวจ"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=SOIL_PROFILE_TOPIC,
)
class SoilProfileApplication(QuestionType):
    """Why topsoil feeds crops, what losing it costs, and studying a profile fairly."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SOIL_PROFILE_SCENARIOS,
            hint="นึกว่าแต่ละชั้นของดินมีองค์ประกอบอะไร และเกิดขึ้นอย่างไร",
        ), SOIL_PROFILE_TOPIC)


@question_type(
    "geo.soil_profile_diagram",
    display_name={"th": "ระบุชั้นหน้าตัดดินจากภาพ"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=SOIL_PROFILE_TOPIC,
)
class SoilProfileDiagram(QuestionType):
    """Read a numbered soil profile: name a horizon, find one from its description, or describe one.

    The numbers are not always top to bottom, so the horizon is placed by its
    position in the picture, not by its number.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(SOIL_PROFILES)
        index = rng.randrange(len(HORIZONS))
        horizon = HORIZONS[index]
        number = spec.numbers[index]
        hint = "ไล่จากผิวดินลงไป: ชั้นโอ (ซากพืชซากสัตว์) ชั้นเอ ชั้นบี ชั้นซี (หินผุ) และชั้นอาร์ (หินพื้น)"
        kind = rng.randrange(3)
        if kind == 0:
            return diagram_question(
                spec.asset_id, SOIL_PROFILE_ALT,
                stem=f"จากภาพหน้าตัดดิน ชั้นหมายเลข {number} คือชั้นใด",
                correct=horizon.name,
                wrongs=tuple(h.name for h in HORIZONS if h is not horizon),
                hint=hint, topic=SOIL_PROFILE_TOPIC,
            )
        if kind == 1:
            return diagram_question(
                spec.asset_id, SOIL_PROFILE_ALT,
                stem=f"จากภาพหน้าตัดดิน ชั้นที่มีลักษณะ “{horizon.description}” คือหมายเลขใด",
                correct=f"หมายเลข {number}",
                wrongs=tuple(f"หมายเลข {n}" for n in spec.numbers if n != number),
                hint=hint, topic=SOIL_PROFILE_TOPIC,
            )
        return diagram_question(
            spec.asset_id, SOIL_PROFILE_ALT,
            stem=f"จากภาพหน้าตัดดิน ชั้นหมายเลข {number} มีลักษณะอย่างไร",
            correct=horizon.description,
            wrongs=tuple(h.description for h in HORIZONS if h is not horizon),
            hint=hint, topic=SOIL_PROFILE_TOPIC,
        )
