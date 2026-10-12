"""ความแตกต่างของดาวเคราะห์และดาวฤกษ์

ดาราศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 3.1 ป.5/1

Sets moved here from: science_wave_c3.
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
from otk.sets._support.science_wave_c1 import SKY_TOPIC, SUBJECT
from otk.sets._support.science_wave_c3 import STAR_PLANET_SCENARIOS

PROVENANCE = Provenance("original")


STAR = "ดาวฤกษ์"


PLANET = "ดาวเคราะห์"


class Difference(NamedTuple):
    """One respect in which a star and a planet differ, with both sides named."""
    aspect: str
    star: str
    planet: str
    wrongs: tuple[str, str]


# Every wrong choice is authored about *this* aspect. Borrowing another row's
# pairing would offer a statement that is true, only about something else asked.
DIFFERENCES = (
    Difference("การส่องแสง",
               "มีแสงสว่างในตัวเอง",
               "ไม่มีแสงในตัวเอง แต่สะท้อนแสงของดาวฤกษ์",
               ("ต่างก็มีแสงสว่างในตัวเองทั้งคู่",
                "ต่างก็ไม่มีแสงในตัวเองทั้งคู่ แต่สะท้อนแสงของดวงจันทร์")),
    Difference("ลักษณะแสงที่มองเห็นจากโลก",
               "เห็นเป็นจุดแสงที่กะพริบริบหรี่",
               "เห็นเป็นดวงสว่างนิ่ง ไม่กะพริบ",
               ("ต่างก็เห็นกะพริบริบหรี่เหมือนกันทั้งคู่",
                "ต่างก็เห็นเป็นดวงสว่างนิ่งเหมือนกันทั้งคู่")),
    Difference("ตำแหน่งเมื่อเทียบกับดาวดวงอื่นในรอบหลายเดือน",
               "อยู่ในตำแหน่งเดิมเมื่อเทียบกับดาวดวงอื่น จึงรวมกันเป็นกลุ่มดาวได้",
               "ย้ายตำแหน่งไปเรื่อย ๆ เมื่อเทียบกับกลุ่มดาวที่อยู่เบื้องหลัง",
               ("ต่างก็อยู่ในตำแหน่งเดิมเมื่อเทียบกับดาวดวงอื่นทั้งคู่",
                "ต่างก็ย้ายตำแหน่งไปเรื่อย ๆ เมื่อเทียบกับกลุ่มดาวทั้งคู่")),
    Difference("ขนาดและอุณหภูมิ",
               "มีขนาดใหญ่มากและร้อนจัด",
               "มีขนาดเล็กกว่ามากและเย็นกว่า",
               ("ต่างก็มีขนาดใหญ่และร้อนจัดพอ ๆ กันทั้งคู่",
                "ต่างก็มีขนาดเล็กและเย็นพอ ๆ กันทั้งคู่")),
    Difference("การเคลื่อนที่ในระบบสุริยะ",
               "เป็นศูนย์กลางที่ดาวดวงอื่นโคจรรอบ",
               "โคจรรอบดาวฤกษ์",
               ("ต่างก็โคจรรอบโลกทั้งคู่",
                "ต่างก็อยู่นิ่งโดยไม่โคจรรอบสิ่งใดทั้งคู่")),
    Difference("ตัวอย่างที่มองเห็นได้จากโลก",
               "ดวงอาทิตย์ และดาวเหนือ",
               "ดาวศุกร์ และดาวอังคาร",
               ("ดวงอาทิตย์และดาวเหนือเป็นดาวเคราะห์ ส่วนดาวศุกร์และดาวอังคารเป็นดาวฤกษ์",
                "ดวงจันทร์เป็นทั้งดาวฤกษ์และดาวเคราะห์")),
)


def _both_sides(item: Difference) -> str:
    return f"{STAR}{item.star} ส่วน{PLANET}{item.planet}"


def _swapped(item: Difference) -> str:
    return f"{STAR}{item.planet} ส่วน{PLANET}{item.star}"


COMPARISON_MODEL = (
    "ครูทำแบบจำลองในห้องมืด โดยใช้หลอดไฟดวงเล็กที่เปิดสว่างอยู่แทนดาวฤกษ์ "
    "และใช้ลูกบอลทาสีด้านที่ไม่สะท้อนแสงเองแทนดาวเคราะห์ วางลูกบอลไว้ห่างจากหลอดไฟ "
    "แล้วให้นักเรียนมองจากอีกมุมหนึ่งของห้อง "
)


# More statements that treat the two alike, one pair per aspect.
MORE_DIFFERENCE_WRONGS = {
    "การส่องแสง": ("ต่างก็มีแสงในตัวเองเฉพาะเวลากลางคืนทั้งคู่",
                   "ต่างก็รับแสงจากดวงจันทร์แล้วส่องต่อมายังโลกทั้งคู่"),
    "ลักษณะแสงที่มองเห็นจากโลก": ("ต่างก็เปลี่ยนสีทุกคืนเหมือนกันทั้งคู่",
                                  "ต่างก็มองไม่เห็นจากโลกด้วยตาเปล่าทั้งคู่"),
    "ตำแหน่งเมื่อเทียบกับดาวดวงอื่นในรอบหลายเดือน": (
        "ต่างก็หายไปจากท้องฟ้าอย่างถาวรเมื่อผ่านไปหลายเดือนทั้งคู่",
        "ต่างก็กระโดดไปมาระหว่างกลุ่มดาวทุกคืนทั้งคู่"),
    "ขนาดและอุณหภูมิ": ("ต่างก็มีขนาดเท่าโลกพอดีทั้งคู่", "ต่างก็เย็นจนเป็นน้ำแข็งทั้งคู่"),
    "การเคลื่อนที่ในระบบสุริยะ": ("ต่างก็โคจรรอบดวงจันทร์ทั้งคู่", "ต่างก็โคจรรอบดาวหางทั้งคู่"),
    "ตัวอย่างที่มองเห็นได้จากโลก": ("ดวงจันทร์และดาวหางเป็นดาวฤกษ์ทั้งคู่",
                                   "ดาวศุกร์และดวงอาทิตย์เป็นดาวเคราะห์ทั้งคู่"),
}


@question_type(
    "astro.star_planet_compare_foundation",
    display_name={"th": "ดาวฤกษ์และดาวเคราะห์คืออะไร"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=SKY_TOPIC,
)
class StarPlanetCompareFoundation(QuestionType):
    """Know one side at a time, before being asked to set the two against each other."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(DIFFERENCES)
        others = [other for other in DIFFERENCES if other.aspect != item.aspect]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"เมื่อพิจารณาเรื่อง{item.aspect} {STAR}มีลักษณะอย่างไร",
                correct=item.star,
                wrongs=(item.planet,) + tuple(other.star for other in others[:2]),
                hint=f"นึกว่า{STAR}เป็นดาวที่มีแสงสว่างในตัวเอง",
                topic=SKY_TOPIC,
            )
        return _labelled(
            stem=f"เมื่อพิจารณาเรื่อง{item.aspect} {PLANET}มีลักษณะอย่างไร",
            correct=item.planet,
            wrongs=(item.star,) + tuple(other.planet for other in others[:2]),
            hint=f"นึกว่า{PLANET}ไม่มีแสงในตัวเอง แต่โคจรรอบ{STAR}",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.star_planet_compare_fluency",
    display_name={"th": "เปรียบเทียบดาวฤกษ์กับดาวเคราะห์"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=SKY_TOPIC,
)
class StarPlanetCompareFluency(QuestionType):
    """Set the two against each other in one answer — the indicator's own verb.

    ``เปรียบเทียบ`` puts the ``exact`` set here rather than at Foundation, and the
    indicator names two objects, so every answer this set accepts states both
    sides of the comparison.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(DIFFERENCES)
        if rng.random() < 0.3:
            return _labelled(
                stem=f"{COMPARISON_MODEL}ผลที่สังเกตได้คือ หลอดไฟสว่างด้วยตัวเองตลอดเวลา "
                     "ส่วนลูกบอลจะมองเห็นได้ก็ต่อเมื่อมีแสงจากหลอดไฟส่องไปถึง "
                     f"จากแบบจำลองนี้ {STAR}และ{PLANET}ต่างกันอย่างไร",
                correct=f"{STAR}มีแสงสว่างในตัวเอง ส่วน{PLANET}สะท้อนแสงของ{STAR}",
                wrongs=(f"{PLANET}มีแสงสว่างในตัวเอง ส่วน{STAR}สะท้อนแสงของ{PLANET}",
                        f"ทั้ง{STAR}และ{PLANET}ต่างก็มีแสงสว่างในตัวเอง",
                        f"ทั้ง{STAR}และ{PLANET}ต่างก็ไม่มีแสงในตัวเอง"),
                hint="ดูว่าในแบบจำลอง สิ่งใดสว่างเองได้ และสิ่งใดต้องรอแสงจากที่อื่น",
                topic=SKY_TOPIC,
            )
        return _labelled(
            stem=f"เมื่อเปรียบเทียบเรื่อง{item.aspect} {STAR}และ{PLANET}ต่างกันอย่างไร",
            correct=_both_sides(item),
            wrongs=(_swapped(item),) + tuple(rng.sample(item.wrongs + MORE_DIFFERENCE_WRONGS[item.aspect], 2)),
            hint="ตอบให้ครบทั้งสองฝ่าย แล้วตรวจว่าฝ่ายใดเป็นฝ่ายใด",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.star_planet_compare_application",
    display_name={"th": "จำแนกดาวจากสิ่งที่สังเกตได้"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=SKY_TOPIC,
)
class StarPlanetCompareApplication(QuestionType):
    """Decide which a point of light is, and judge a claim about brightness."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, STAR_PLANET_SCENARIOS,
            hint="ถามว่าจุดนั้นมีแสงในตัวเองหรือไม่ และย้ายตำแหน่งเทียบกับกลุ่มดาวหรือเปล่า",
        ), SKY_TOPIC)
