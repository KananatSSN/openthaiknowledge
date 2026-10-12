"""ปรากฏการณ์เรือนกระจก

ธรณีวิทยา · ป.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.6/8

Sets moved here from: science_wave_c16.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b17 import PRIMARY_SIX
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c16 import GREENHOUSE_FACTS, GREENHOUSE_SCENARIOS, MECHANISM

PROVENANCE = Provenance("original")


GREENHOUSE_TOPIC = "ปรากฏการณ์เรือนกระจก"


# Effects of extra warming on living things; one is drawn into each answer.
EFFECTS = (
    "ปะการังฟอกขาวและตายเพราะน้ำทะเลอุ่นขึ้น",
    "สัตว์และพืชบางชนิดต้องย้ายถิ่นหรือสูญพันธุ์เพราะที่อยู่ร้อนเกินไป",
    "ฝนแล้งและน้ำท่วมรุนแรงขึ้นจนพืชผลทางการเกษตรเสียหาย",
)


def jar_readings(rng: Random) -> tuple[str, int, int]:
    """Which jar is covered, and the two final temperatures: covered always warmer."""
    covered = rng.choice(("ก", "ข"))
    start = rng.randint(28, 31)
    open_end = start + rng.randint(2, 4)
    covered_end = open_end + rng.randint(3, 6)
    return covered, covered_end, open_end


def _explain(jar: str, effect: str) -> str:
    return (f"ฝาพลาสติกทำหน้าที่เหมือนแก๊สเรือนกระจก โหล {jar} จึงร้อนกว่า "
            f"ในโลกจริง{MECHANISM} ถ้ามีมากเกินไปโลกจะร้อนขึ้น ส่งผลให้{effect}")


@question_type(
    "geo.greenhouse_effect_foundation",
    display_name={"th": "ปรากฏการณ์เรือนกระจกและแก๊สเรือนกระจก"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=GREENHOUSE_TOPIC,
)
class GreenhouseEffectFoundation(QuestionType):
    """The mechanism, the gases, and the human sources, one fact at a time."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, GREENHOUSE_FACTS,
            hint="แสงเข้ามาได้ แต่ความร้อนที่ผิวโลกแผ่ออกไปถูกกักไว้",
        ), GREENHOUSE_TOPIC)


@question_type(
    "geo.greenhouse_effect_fluency",
    display_name={"th": "อธิบายปรากฏการณ์เรือนกระจกและผลต่อสิ่งมีชีวิตจากแบบจำลอง"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=GREENHOUSE_TOPIC,
)
class GreenhouseEffectFluency(QuestionType):
    """Explain the phenomenon and its effect on living things from a two-jar model."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        covered, covered_end, open_end = jar_readings(rng)
        other = "ข" if covered == "ก" else "ก"
        readings = {covered: covered_end, other: open_end}
        effect = rng.choice(EFFECTS)
        return _labelled(
            stem=("แบบจำลอง: นำโหลแก้ว 2 ใบ ใส่เทอร์โมมิเตอร์ไว้ในแต่ละใบ "
                  f"ปิดปากโหล {covered} ด้วยแผ่นพลาสติกใส ส่วนโหล {other} เปิดไว้ "
                  "ตั้งกลางแดด 30 นาที แล้ววัดอุณหภูมิได้ "
                  f"โหล ก {readings['ก']} องศาเซลเซียส / โหล ข {readings['ข']} องศาเซลเซียส "
                  "ข้อใดอธิบายการเกิดปรากฏการณ์เรือนกระจกและผลต่อสิ่งมีชีวิตจากแบบจำลองนี้ได้ถูกต้อง"),
            correct=_explain(covered, effect),
            wrongs=(_explain(other, effect),
                    f"ฝาพลาสติกทำหน้าที่เหมือนแก๊สเรือนกระจก โหล {covered} จึงร้อนกว่า "
                    "ในโลกจริงแก๊สเรือนกระจกสร้างความร้อนขึ้นเอง "
                    f"ถ้ามีมากเกินไปโลกจะร้อนขึ้น ส่งผลให้{effect}",
                    f"ฝาพลาสติกทำหน้าที่เหมือนแก๊สเรือนกระจก โหล {covered} จึงร้อนกว่า "
                    f"ในโลกจริง{MECHANISM} แต่ความร้อนที่เพิ่มขึ้นไม่ส่งผลต่อสิ่งมีชีวิตใด ๆ",
                    # The wrong jar as well as a wrong second half.
                    f"ฝาพลาสติกทำหน้าที่เหมือนแก๊สเรือนกระจก โหล {other} จึงร้อนกว่า "
                    "ในโลกจริงแก๊สเรือนกระจกสร้างความร้อนขึ้นเอง "
                    f"ถ้ามีมากเกินไปโลกจะร้อนขึ้น ส่งผลให้{effect}",
                    f"ฝาพลาสติกทำหน้าที่เหมือนแก๊สเรือนกระจก โหล {other} จึงร้อนกว่า "
                    f"ในโลกจริง{MECHANISM} แต่ความร้อนที่เพิ่มขึ้นไม่ส่งผลต่อสิ่งมีชีวิตใด ๆ"),
            hint="อ่านอุณหภูมิของโหลที่ปิดฝาก่อน แล้วตรวจทั้งกลไกและผลต่อสิ่งมีชีวิต",
            topic=GREENHOUSE_TOPIC,
        )


@question_type(
    "geo.greenhouse_effect_application",
    display_name={"th": "วิเคราะห์ปรากฏการณ์เรือนกระจกและภาวะโลกร้อน"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=GREENHOUSE_TOPIC,
)
class GreenhouseEffectApplication(QuestionType):
    """Change the model, answer "get rid of it", and trace deforestation and coral."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, GREENHOUSE_SCENARIOS,
            hint="แยกให้ออกระหว่างปรากฏการณ์เรือนกระจกที่จำเป็น กับแก๊สเรือนกระจกที่เพิ่มมากเกินไป",
        ), GREENHOUSE_TOPIC)
