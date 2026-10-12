"""การเกิดดาวฤกษ์

ดาราศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.1 ม.6/4

Sets moved here from: science_wave_c7.
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
from otk.sets._support.science_wave_c1 import SUBJECT
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c7 import FORMATION_FACTS, FORMATION_SCENARIOS

PROVENANCE = Provenance("original")


FORMATION_TOPIC = "การเกิดดาวฤกษ์"


class Stage(NamedTuple):
    """One step from cloud to star, with all three named quantities."""
    name: str
    size: str
    pressure: str
    temperature: str
    what: str


# ``ม.6/4`` names ความดัน, อุณหภูมิ and ขนาด, so every row carries all three and
# the table can be read across as well as down.
STAGES = (
    Stage("เนบิวลา (กลุ่มแก๊สและฝุ่น)",
          "กว้างหลายปีแสง", "ต่ำมาก", "ประมาณ 10-50 เคลวิน",
          "แก๊สและฝุ่นกระจายอยู่อย่างเบาบางและเย็นจัด"),
    Stage("กลุ่มแก๊สที่เริ่มยุบตัว",
          "หดเล็กลงอย่างรวดเร็ว", "เริ่มสูงขึ้นที่ใจกลาง", "เริ่มสูงขึ้นเป็นหลายร้อยเคลวิน",
          "แรงโน้มถ่วงชนะความดันของแก๊ส กลุ่มแก๊สจึงยุบเข้าหาใจกลาง"),
    Stage("ดาวฤกษ์ก่อนเกิด",
          "เล็กลงมากแล้วแต่ยังใหญ่กว่าดาวฤกษ์", "สูงขึ้นเรื่อย ๆ", "หลายแสนถึงล้านเคลวินที่แก่น",
          "พลังงานศักย์โน้มถ่วงเปลี่ยนเป็นความร้อน แก่นจึงร้อนและถูกอัดแน่นขึ้นจนเปล่งแสงได้เอง"),
    Stage("ดาวฤกษ์ในแถบลำดับหลัก",
          "คงที่ ไม่ยุบลงอีก", "คงที่ สมดุลกับแรงโน้มถ่วง", "สูงกว่า 10 ล้านเคลวินที่แก่น",
          "ปฏิกิริยาหลอมนิวเคลียสของไฮโดรเจนเริ่มขึ้น "
          "ความดันจากพลังงานที่ได้ต้านแรงโน้มถ่วงได้พอดี"),
)


SIZE = "ขนาด"


PRESSURE = "ความดัน"


TEMPERATURE = "อุณหภูมิ"


# The one answer reaching all three quantities the indicator names.
FORMATION_SPANNING = (
    f"{SIZE}หดเล็กลง {PRESSURE}และ{TEMPERATURE}ที่แก่นสูงขึ้น "
    "จนเกิดปฏิกิริยาหลอมนิวเคลียส แล้วทั้งสามจึงคงที่")


FORMATION_SPANNING_WRONGS = (
    f"{SIZE}ขยายใหญ่ขึ้น ขณะที่{PRESSURE}และ{TEMPERATURE}ที่แก่นลดลงเรื่อย ๆ "
    "จนเย็นพอให้เกิดปฏิกิริยาหลอมนิวเคลียส",
    f"{SIZE}หดเล็กลง ขณะที่{PRESSURE}สูงขึ้นแต่{TEMPERATURE}ที่แก่นลดลง "
    "จนแก่นเย็นลงพอที่แรงโน้มถ่วงจะหยุดการยุบตัว",
    f"{SIZE} {PRESSURE} และ{TEMPERATURE}คงที่ตลอดกระบวนการ "
    "ดาวฤกษ์จึงเกิดขึ้นได้โดยไม่ต้องยุบตัวเลย",
)


def _stage_table() -> str:
    return " / ".join(
        f"{stage.name}: {SIZE}{stage.size} {PRESSURE}ที่แก่น{stage.pressure} "
        f"{TEMPERATURE}{stage.temperature}" for stage in STAGES)


MORE_SPANNING_WRONGS = (
    "ขนาดหดเล็กลง ขณะที่ความดันลดลงแต่อุณหภูมิที่แก่นสูงขึ้น จนแก่นร้อนพอให้เกิดปฏิกิริยาหลอมนิวเคลียส",
    "ขนาดขยายใหญ่ขึ้น ขณะที่ความดันและอุณหภูมิที่แก่นสูงขึ้น จนดาวฤกษ์ระเบิดออก",
)


# Values and events no row of STAGES shows.
STAGE_TEMPERATURE_DECOYS = ("ประมาณ 1 ล้านล้านเคลวินที่ผิว", "ต่ำกว่า 0 เคลวิน")


STAGE_EVENT_DECOYS = ("แก๊สระเหยออกไปในอวกาศจนหมด ไม่มีสิ่งใดเหลืออยู่",
                      "ดาวฤกษ์ระเบิดเป็นซูเปอร์โนวาทันที")


@question_type(
    "astro.star_formation_foundation",
    display_name={"th": "จากเนบิวลาสู่ดาวฤกษ์"},
    level=UPPER_SIX, subject=SUBJECT, topic=FORMATION_TOPIC,
)
class StarFormationFoundation(QuestionType):
    """Know where stars come from and what heats a collapsing core."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, FORMATION_FACTS,
            hint="นึกว่าการยุบตัวเปลี่ยนพลังงานศักย์โน้มถ่วงไปเป็นความร้อน",
        ), FORMATION_TOPIC)


@question_type(
    "astro.star_formation_fluency",
    display_name={"th": "การเปลี่ยนแปลงความดัน อุณหภูมิ และขนาด"},
    level=UPPER_SIX, subject=SUBJECT, topic=FORMATION_TOPIC,
)
class StarFormationFluency(QuestionType):
    """Track all three quantities the indicator names, from the table in the stem."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem = ("ตารางแสดงการเปลี่ยนแปลงระหว่างการเกิดดาวฤกษ์เป็นดังนี้ "
                f"{_stage_table()} ")
        draw = rng.random()
        if draw < 0.4:
            return _labelled(
                stem=stem + "จากข้อมูลนี้ ข้อใดสรุปการเปลี่ยนแปลงความดัน อุณหภูมิ "
                            "และขนาด ตั้งแต่ก่อนเกิดจนเป็นดาวฤกษ์ได้ถูกต้อง",
                correct=FORMATION_SPANNING,
                wrongs=tuple(FORMATION_SPANNING_WRONGS + MORE_SPANNING_WRONGS),
                hint="ตอบให้ครบทั้งสามปริมาณ แล้วตรวจทิศทางของแต่ละปริมาณจากตาราง",
                topic=FORMATION_TOPIC,
            )
        stage = rng.choice(STAGES)
        others = [other for other in STAGES if other.name != stage.name]
        rng.shuffle(others)
        if draw < 0.7:
            return _labelled(
                stem=stem + f"จากข้อมูลนี้ ในขั้น “{stage.name}” "
                            "อุณหภูมิเป็นเท่าใด",
                correct=stage.temperature,
                wrongs=tuple([other.temperature for other in others[:3]]
                                        + list(STAGE_TEMPERATURE_DECOYS)),
                hint="หาชื่อขั้นที่โจทย์ถามในตาราง แล้วอ่านค่าอุณหภูมิของแถวนั้น",
                topic=FORMATION_TOPIC,
            )
        return _labelled(
            stem=stem + f"ในขั้น “{stage.name}” เกิดอะไรขึ้น",
            correct=stage.what,
            wrongs=tuple([other.what for other in others[:3]]
                                    + list(STAGE_EVENT_DECOYS)),
            hint="เทียบขนาด ความดัน และอุณหภูมิของแถวนั้นกับแถวก่อนหน้า",
            topic=FORMATION_TOPIC,
        )


@question_type(
    "astro.star_formation_application",
    display_name={"th": "วิเคราะห์การเกิดดาวฤกษ์"},
    level=UPPER_SIX, subject=SUBJECT, topic=FORMATION_TOPIC,
)
class StarFormationApplication(QuestionType):
    """Reason about a cloud too light, a core still cold, and dust in the way."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, FORMATION_SCENARIOS,
            hint="ถามว่าแก่นร้อนถึงระดับที่หลอมนิวเคลียสได้แล้วหรือยัง",
        ), FORMATION_TOPIC)
