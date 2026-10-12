"""การหมุนเวียนของอากาศจากความกดอากาศ

ธรณีวิทยา · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.6/8

Sets moved here from: science_wave_c24.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c13 import _swapped, _swaps
from otk.sets._support.science_wave_c15 import FIVE_LETTERS
from otk.sets._support.science_wave_c23 import Part
from otk.sets._support.science_wave_c24 import PRESSURE_SCENARIOS, parts_item

PROVENANCE = Provenance("original")


PRESSURE_TOPIC = "การหมุนเวียนของอากาศจากความกดอากาศ"


# The causal chain from warming to wind, in order.
PRESSURE_CHAIN = (
    "อากาศเหนือบริเวณนั้นได้รับความร้อนจากพื้นผิว",
    "อากาศขยายตัว ความหนาแน่นลดลง",
    "อากาศลอยตัวขึ้น ความกดอากาศที่ผิวพื้นบริเวณนั้นลดต่ำลง",
    "อากาศจากบริเวณความกดอากาศสูงรอบ ๆ ไหลเข้ามาแทนที่เกิดเป็นลม",
)


PLACE_PAIRS = (
    ("พื้นดินริมชายฝั่ง", "ผิวน้ำทะเล"),
    ("ลานคอนกรีตกลางเมือง", "ผืนป่าชานเมือง"),
    ("ทุ่งนาที่ไถเตรียมดินไว้", "อ่างเก็บน้ำ"),
)


def pressure_parts(hot: str, cool: str) -> tuple[Part, ...]:
    """The whole cell between a warmer and a cooler place."""
    return (
        Part("ความกดอากาศ",
             f"ที่ผิวพื้นเหนือ{hot}ต่ำกว่าเหนือ{cool}",
             f"ที่ผิวพื้นเหนือ{hot}สูงกว่าเหนือ{cool}"),
        Part("การเคลื่อนที่แนวดิ่ง",
             f"อากาศเหนือ{hot}ลอยตัวขึ้น ส่วนอากาศเหนือ{cool}จมตัวลง",
             f"อากาศเหนือ{cool}ลอยตัวขึ้น ส่วนอากาศเหนือ{hot}จมตัวลง"),
        Part("ลมใกล้ผิวพื้น",
             f"พัดจาก{cool}ไปยัง{hot}",
             f"พัดจาก{hot}ไปยัง{cool}"),
        Part("อากาศระดับบน",
             f"ไหลจากเหนือ{hot}กลับไปยังเหนือ{cool}",
             f"ไหลจากเหนือ{cool}กลับไปยังเหนือ{hot}"),
    )


@question_type(
    "geo.pressure_circulation_foundation",
    display_name={"th": "เรียงลำดับการเกิดลมจากความแตกต่างของความกดอากาศ"},
    level=UPPER_SIX, subject=SUBJECT, topic=PRESSURE_TOPIC,
)
class PressureCirculationFoundation(QuestionType):
    """Order the chain from a warmed surface to the wind it drives."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        order = list(range(len(PRESSURE_CHAIN)))
        rng.shuffle(order)
        listing = " / ".join(f"{FIVE_LETTERS[pos]}. {PRESSURE_CHAIN[i]}" for pos, i in enumerate(order))
        letter_of = {i: FIVE_LETTERS[pos] for pos, i in enumerate(order)}
        right = [letter_of[i] for i in range(len(PRESSURE_CHAIN))]
        return _labelled(
            stem=f"เหตุการณ์ต่อไปนี้ — {listing} ข้อใดเรียงลำดับการเกิดลมได้ถูกต้อง",
            correct=" → ".join(right),
            # One swap, or two disjoint swaps at once (every step moved).
            wrongs=tuple(" → ".join(_swapped(right, i, j)) for i, j in _swaps(rng, 3, len(right)))
                   + (" → ".join(_swapped(_swapped(right, 0, 1), 2, 3)),
                      " → ".join(_swapped(_swapped(right, 0, 2), 1, 3))),
            hint="เริ่มจากความร้อน แล้วตามว่าอากาศเปลี่ยนไปอย่างไรจนเกิดลม",
            topic=PRESSURE_TOPIC,
        )


@question_type(
    "geo.pressure_circulation_fluency",
    display_name={"th": "อธิบายการหมุนเวียนของอากาศจากข้อมูลอุณหภูมิ"},
    level=UPPER_SIX, subject=SUBJECT, topic=PRESSURE_TOPIC,
)
class PressureCirculationFluency(QuestionType):
    """A temperature record; explain the whole cell it drives."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        places = list(rng.choice(PLACE_PAIRS))
        rng.shuffle(places)
        low = rng.randint(22, 30)
        temps = [low, low + rng.randint(3, 9)]
        rng.shuffle(temps)
        hot, cool = (places[0], places[1]) if temps[0] > temps[1] else (places[1], places[0])
        return parts_item(
            rng, pressure_parts(hot, cool),
            stem=(f"จากข้อมูลที่รวบรวมได้ ในเวลาเดียวกัน อุณหภูมิอากาศเหนือ{places[0]} {temps[0]} องศาเซลเซียส "
                  f"และเหนือ{places[1]} {temps[1]} องศาเซลเซียส ข้อใดอธิบายการหมุนเวียนของอากาศระหว่างสองบริเวณนี้ได้ถูกต้องทั้งหมด"),
            hint="บริเวณที่ร้อนกว่าอากาศลอยตัวขึ้นและความกดอากาศต่ำ ลมใกล้ผิวพื้นพัดเข้าหาบริเวณนั้น",
            topic=PRESSURE_TOPIC,
        )


@question_type(
    "geo.pressure_circulation_application",
    display_name={"th": "วิเคราะห์ลมมรสุม ลมบก ลมทะเล และลมภูเขา"},
    level=UPPER_SIX, subject=SUBJECT, topic=PRESSURE_TOPIC,
)
class PressureCirculationApplication(QuestionType):
    """The southwest monsoon, fishing on land and sea breezes, and valley winds."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, PRESSURE_SCENARIOS,
            hint="หาบริเวณที่ร้อนกว่าในช่วงเวลานั้น อากาศลอยตัวขึ้นที่นั่น ลมใกล้ผิวพื้นจึงพัดเข้าหา",
        ), PRESSURE_TOPIC)
