"""การใช้ประโยชน์จากดิน

ธรณีวิทยา · ป.2 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.2/2

Sets moved here from: science_wave_c10.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import PRIMARY_TWO, _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import SOIL_USE_SCENARIOS, SUBJECT

PROVENANCE = Provenance("original")


SOIL_USE_TOPIC = "การใช้ประโยชน์จากดิน"


class Use(NamedTuple):
    """One use of soil, the soil that suits it, and why."""
    use: str
    soil: str
    because: str


# One use per soil type, so a use names one soil and one reason.
SOIL_USES = (
    Use("ปลูกผักและไม้ดอก", "ดินร่วน",
        "มีซากพืชซากสัตว์มาก อุ้มน้ำได้พอดีและระบายน้ำได้ดี"),
    Use("ปั้นโอ่งและเผาเป็นภาชนะดินเผา", "ดินเหนียว",
        "จับตัวกันแน่น ปั้นเป็นรูปร่างได้และไม่แตกง่าย"),
    Use("ปลูกมันสำปะหลังและแตงโม", "ดินทราย",
        "ระบายน้ำได้เร็ว น้ำจึงไม่ขังจนหัวหรือรากเน่า"),
)


# More uses for the same three soils. SOIL_USES keeps one use per soil so its
# reasons stay apart; these only feed the "which soil" question.
MORE_SOIL_USES = (
    ("ทำนาปลูกข้าวที่ต้องขังน้ำไว้ในแปลง", "ดินเหนียว"),
    ("ปั้นอิฐสำหรับก่อสร้าง", "ดินเหนียว"),
    ("ปลูกไม้ผลในสวนหลังบ้าน", "ดินร่วน"),
    ("ปลูกผักสวนครัวในกระถาง", "ดินร่วน"),
    ("ปลูกถั่วลิสงที่ต้องขุดฝักขึ้นจากดิน", "ดินทราย"),
)


REASON_DECOYS = (
    "เป็นดินที่มีสีสวยที่สุด",
    "เป็นดินที่มีน้ำหนักเบาที่สุด",
    "เป็นดินที่หาซื้อได้ในราคาถูกที่สุด",
)


CATEGORIES = (
    "ปลูกพืช",
    "ทำเครื่องปั้นดินเผา",
    "สร้างที่อยู่อาศัย",
    "เป็นที่อยู่อาศัยของสัตว์",
)


# Examples of each category, as a survey would record them.
EXAMPLES = {
    "ปลูกพืช": ("แปลงผักหลังบ้าน", "สวนมะม่วง", "นาข้าว"),
    "ทำเครื่องปั้นดินเผา": ("โรงปั้นโอ่ง", "ร้านทำกระถางดินเผา", "เตาเผาอิฐ"),
    "สร้างที่อยู่อาศัย": ("บ้านดิน", "ลานดินที่ถมไว้สร้างบ้าน", "ผนังบ้านที่ฉาบด้วยดิน"),
    "เป็นที่อยู่อาศัยของสัตว์": ("รูไส้เดือนในสนาม", "รังมดใต้ต้นไม้", "โพรงกิ้งกือในกองดิน"),
}


def survey(rng: Random) -> tuple[list[tuple[str, str]], dict[str, int]]:
    """A community survey with a unique most common use and exactly one absent use.

    Counts are 3, 2 and 1 across three categories and 0 for the fourth, so both
    the "most" and the "not found" questions have exactly one answer.
    """
    order = list(CATEGORIES)
    rng.shuffle(order)
    counts = dict(zip(order, (3, 2, 1, 0)))
    rows = [(example, category)
            for category, count in counts.items()
            for example in rng.sample(EXAMPLES[category], count)]
    rng.shuffle(rows)
    return rows, counts


def survey_text(rows: list[tuple[str, str]]) -> str:
    return " / ".join(f"{example}: ใช้ดินเพื่อ{category}" for example, category in rows)


@question_type(
    "geo.soil_use_foundation",
    display_name={"th": "ประโยชน์ของดินแต่ละชนิด"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=SOIL_USE_TOPIC,
)
class SoilUseFoundation(QuestionType):
    """Match a use to the soil that suits it and to the reason."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(SOIL_USES)
        others = [other for other in SOIL_USES if other.use != item.use]
        ask = rng.randrange(3)
        if ask == 2:
            category = rng.choice(CATEGORIES)
            return _labelled(
                stem=f"“{rng.choice(EXAMPLES[category])}” เป็นการใช้ดินเพื่อสิ่งใด",
                correct=category,
                wrongs=tuple(other for other in CATEGORIES if other != category),
                hint="นึกว่าดินในตัวอย่างนั้นถูกนำไปทำอะไร",
                topic=SOIL_USE_TOPIC,
            )
        if ask == 0:
            use, soil = rng.choice([(one.use, one.soil) for one in SOIL_USES] + list(MORE_SOIL_USES))
            return _labelled(
                stem=f"ถ้าต้องการใช้ดินเพื่อ{use} ควรเลือกดินชนิดใด",
                correct=soil,
                wrongs=tuple(one.soil for one in SOIL_USES if one.soil != soil)
                       + ("ดินชนิดใดก็ได้ผลเหมือนกัน",),
                hint="นึกว่างานนั้นต้องการดินที่อุ้มน้ำ ปั้นได้ หรือระบายน้ำเร็ว",
                topic=SOIL_USE_TOPIC,
            )
        return _labelled(
            stem=f"เหตุใดจึงใช้{item.soil}{item.use}",
            correct=item.because,
            wrongs=tuple(other.because for other in others)
                   + (rng.choice(REASON_DECOYS),),
            hint="นึกถึงเนื้อดินและการจับตัวของดินชนิดนั้น",
            topic=SOIL_USE_TOPIC,
        )


@question_type(
    "geo.soil_use_fluency",
    display_name={"th": "อธิบายการใช้ประโยชน์จากดินจากข้อมูลการสำรวจ"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=SOIL_USE_TOPIC,
)
class SoilUseFluency(QuestionType):
    """Read a community survey of soil use and answer from it alone."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rows, counts = survey(rng)
        stem = f"นักเรียนสำรวจการใช้ดินในชุมชนได้ข้อมูลดังนี้ — {survey_text(rows)} จากข้อมูลนี้"
        if rng.random() < 0.5:
            most = max(counts, key=counts.get)
            return _labelled(
                stem=f"{stem} ชุมชนนี้ใช้ดินเพื่อสิ่งใดมากที่สุด",
                correct=most,
                wrongs=tuple(category for category in CATEGORIES if category != most),
                hint="นับว่าการใช้ดินแต่ละแบบพบกี่แห่ง",
                topic=SOIL_USE_TOPIC,
            )
        absent = next(category for category, count in counts.items() if count == 0)
        return _labelled(
            stem=f"{stem} การใช้ประโยชน์จากดินแบบใดที่ไม่พบในการสำรวจครั้งนี้",
            correct=absent,
            wrongs=tuple(category for category in CATEGORIES if category != absent),
            hint="ตรวจทีละแบบว่ามีอยู่ในบันทึกหรือไม่",
            topic=SOIL_USE_TOPIC,
        )


@question_type(
    "geo.soil_use_application",
    display_name={"th": "ใช้ประโยชน์และดูแลดินในชุมชน"},
    level=PRIMARY_TWO, subject=SUBJECT, topic=SOIL_USE_TOPIC,
)
class SoilUseApplication(QuestionType):
    """Improve a soil for a job, match a community to its soil, and look after soil."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SOIL_USE_SCENARIOS,
            hint="นึกว่าดินชนิดนั้นมีลักษณะอย่างไร และงานที่ถามต้องการดินแบบใด",
        ), SOIL_USE_TOPIC)
