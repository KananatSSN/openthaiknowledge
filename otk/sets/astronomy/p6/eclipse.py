"""การเกิดสุริยุปราคาและจันทรุปราคา

ดาราศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ว 3.1 ป.6/1

Sets moved here from: science_wave_c4.
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
from otk.sets._support.science_wave_b17 import PRIMARY_SIX
from otk.sets._support.science_wave_c1 import SKY_TOPIC, SUBJECT
from otk.sets._support.science_wave_c4 import ECLIPSE_SCENARIOS

PROVENANCE = Provenance("original")


SOLAR = "สุริยุปราคา"


LUNAR = "จันทรุปราคา"


ECLIPSE_MODEL = (
    "ครูวางโคมไฟแทนดวงอาทิตย์ ลูกบอลใหญ่แทนโลก และลูกบอลเล็กแทนดวงจันทร์ "
    "แล้วเลื่อนลูกบอลเล็กไปตามวงโคจรรอบลูกบอลใหญ่ จนกระทั่งทั้งสามเรียงอยู่ในแนวเดียวกัน "
)


class Eclipse(NamedTuple):
    """One respect in which the two eclipses differ, with both sides named."""
    aspect: str
    solar: str
    lunar: str
    wrongs: tuple[str, str]


ECLIPSES = (
    Eclipse("ลำดับการเรียงตัว",
            "ดวงจันทร์อยู่ระหว่างดวงอาทิตย์กับโลก",
            "โลกอยู่ระหว่างดวงอาทิตย์กับดวงจันทร์",
            ("ดวงอาทิตย์อยู่ระหว่างโลกกับดวงจันทร์ทั้งสองปรากฏการณ์",
             "ทั้งสองปรากฏการณ์ไม่ต้องเรียงอยู่ในแนวเดียวกันก็เกิดได้")),
    Eclipse("เงาที่ทาบลงบนอะไร",
            "เงาของดวงจันทร์ทาบลงบนผิวโลก",
            "เงาของโลกทาบลงบนดวงจันทร์",
            ("เงาของดวงอาทิตย์ทาบลงบนโลกทั้งสองปรากฏการณ์",
             "ไม่มีเงาเกี่ยวข้องเลยทั้งสองปรากฏการณ์")),
    Eclipse("ช่วงเวลาที่มองเห็น",
            "เห็นได้ในเวลากลางวัน",
            "เห็นได้ในเวลากลางคืน",
            ("เห็นได้ในเวลากลางวันทั้งสองปรากฏการณ์",
             "เห็นได้ในเวลากลางคืนทั้งสองปรากฏการณ์")),
    Eclipse("รูปร่างปรากฏของดวงจันทร์ในวันนั้น",
            "ตรงกับวันจันทร์ดับ คือแรม 15 ค่ำ",
            "ตรงกับวันจันทร์เต็มดวง คือขึ้น 15 ค่ำ",
            ("ตรงกับวันขึ้น 8 ค่ำทั้งสองปรากฏการณ์",
             "ไม่เกี่ยวกับรูปร่างปรากฏของดวงจันทร์เลย")),
    Eclipse("บริเวณบนโลกที่มองเห็นได้",
            "เห็นได้เฉพาะบริเวณแคบ ๆ ที่เงาของดวงจันทร์ทาบถึง",
            "เห็นได้ทั่วทั้งซีกโลกที่เป็นกลางคืนในขณะนั้น",
            ("เห็นได้ทั่วทั้งโลกพร้อมกันทั้งสองปรากฏการณ์",
             "เห็นได้เฉพาะบริเวณแคบ ๆ ทั้งสองปรากฏการณ์")),
)


def _eclipse_pair(item: Eclipse) -> str:
    return f"{SOLAR}: {item.solar} ส่วน{LUNAR}: {item.lunar}"


def _eclipse_swapped(item: Eclipse) -> str:
    return f"{SOLAR}: {item.lunar} ส่วน{LUNAR}: {item.solar}"


# More statements that treat the two eclipses alike, one pair per aspect.
MORE_ECLIPSE_WRONGS = {
    "ลำดับการเรียงตัว": ("โลกอยู่ระหว่างดวงอาทิตย์กับดวงจันทร์ทั้งสองปรากฏการณ์",
                        "ดวงจันทร์อยู่ระหว่างดวงอาทิตย์กับโลกทั้งสองปรากฏการณ์"),
    "เงาที่ทาบลงบนอะไร": ("เงาของดวงจันทร์ทาบลงบนดวงอาทิตย์ทั้งสองปรากฏการณ์",
                         "เงาของโลกทาบลงบนดวงอาทิตย์ทั้งสองปรากฏการณ์"),
    "ช่วงเวลาที่มองเห็น": ("เห็นได้เฉพาะตอนรุ่งเช้าทั้งสองปรากฏการณ์",
                          "เห็นได้ทั้งกลางวันและกลางคืนพร้อมกันทั้งสองปรากฏการณ์"),
    "รูปร่างปรากฏของดวงจันทร์ในวันนั้น": ("ตรงกับวันจันทร์เต็มดวงทั้งสองปรากฏการณ์",
                                         "ตรงกับวันจันทร์ดับทั้งสองปรากฏการณ์"),
    "บริเวณบนโลกที่มองเห็นได้": ("เห็นได้เฉพาะที่ขั้วโลกทั้งสองปรากฏการณ์",
                                "เห็นได้เฉพาะในซีกโลกที่เป็นกลางวันทั้งสองปรากฏการณ์"),
}


# (how the model is set up, light, Earth, Moon). The last three name the props
# so each event below reads in the model's own words.
ECLIPSE_SETUPS = (
    (ECLIPSE_MODEL, "โคมไฟ", "ลูกบอลใหญ่", "ลูกบอลเล็ก"),
    ("ในห้องมืด นักเรียนใช้ไฟฉายแทนดวงอาทิตย์ ลูกโลกจำลองแทนโลก และส้มลูกเล็กแทนดวงจันทร์ "
     "แล้วถือส้มเดินรอบลูกโลกจำลองจนทั้งสามเรียงอยู่ในแนวเดียวกัน ",
     "ไฟฉาย", "ลูกโลกจำลอง", "ส้ม"),
    ("นักเรียนสามคนยืนในห้องมืด คนแรกถือหลอดไฟแทนดวงอาทิตย์ คนที่สองถือลูกฟุตบอลแทนโลก "
     "คนที่สามถือลูกปิงปองแทนดวงจันทร์ แล้วคนที่สามเดินวนรอบคนที่สองจนทั้งสามอยู่ในแนวเดียวกัน ",
     "หลอดไฟ", "ลูกฟุตบอล", "ลูกปิงปอง"),
    ("ครูติดหลอดไฟไว้กลางห้องแทนดวงอาทิตย์ ให้นักเรียนถือลูกบอลพลาสติกแทนโลก "
     "และแขวนลูกแก้วไว้ปลายไม้แทนดวงจันทร์ แล้วหมุนไม้จนทั้งสามเรียงอยู่ในแนวเดียวกัน ",
     "หลอดไฟ", "ลูกบอลพลาสติก", "ลูกแก้ว"),
)


# What the class sees at the moment of the eclipse, in the props' names.
SOLAR_EVENTS = (
    "เมื่อ{small}มาอยู่ระหว่าง{light}กับ{big} และเงาของ{small}ทาบลงบน{big}",
    "นักเรียนเห็นจุดมืดเล็ก ๆ บน{big} ซึ่งเป็นเงาของ{small}ที่บังแสงจาก{light}ไว้",
    "แสงจาก{light}ส่องไปไม่ถึงบางส่วนของ{big} เพราะ{small}ขวางทางแสงอยู่",
)
LUNAR_EVENTS = (
    "เมื่อ{big}มาอยู่ระหว่าง{light}กับ{small} และเงาของ{big}ทาบลงบน{small}",
    "{small}ที่เคยสว่างอยู่ค่อย ๆ มืดลง เพราะเคลื่อนเข้าไปในเงาของ{big}",
    "แสงจาก{light}ส่องไปไม่ถึง{small} เพราะ{big}ขวางทางแสงอยู่",
)


SOLAR_HOW = (f"{SOLAR} เกิดเมื่อดวงจันทร์มาอยู่ระหว่างดวงอาทิตย์กับโลก "
             "แล้วเงาของดวงจันทร์ทาบลงบนผิวโลก")
LUNAR_HOW = (f"{LUNAR} เกิดเมื่อโลกมาอยู่ระหว่างดวงอาทิตย์กับดวงจันทร์ "
             "แล้วเงาของโลกทาบลงบนดวงจันทร์")
SOLAR_WRONGS = (
    f"{LUNAR} เกิดเมื่อดวงจันทร์มาอยู่ระหว่างดวงอาทิตย์กับโลก "
    "แล้วเงาของดวงจันทร์ทาบลงบนผิวโลก",
    f"{SOLAR} เกิดเมื่อโลกมาอยู่ระหว่างดวงอาทิตย์กับดวงจันทร์ "
    "แล้วเงาของโลกทาบลงบนดวงจันทร์",
    f"{SOLAR} เกิดเมื่อดวงจันทร์เคลื่อนเข้าไปอยู่หลังดวงอาทิตย์จนมองไม่เห็น",
    f"{SOLAR} เกิดเมื่อเมฆหนาบังดวงอาทิตย์ทั้งท้องฟ้า",
    f"{SOLAR} เกิดเมื่อโลกหมุนหนีดวงอาทิตย์ในตอนกลางคืน",
    f"{SOLAR} เกิดเมื่อดวงจันทร์มาอยู่ระหว่างดวงอาทิตย์กับโลก "
    "แล้วเงาของโลกทาบลงบนดวงจันทร์",
    f"{SOLAR} เกิดเมื่อดวงอาทิตย์มาอยู่ระหว่างโลกกับดวงจันทร์ "
    "แล้วเงาของดวงจันทร์ทาบลงบนผิวโลก",
    LUNAR_HOW,
)
LUNAR_WRONGS = (
    f"{SOLAR} เกิดเมื่อโลกมาอยู่ระหว่างดวงอาทิตย์กับดวงจันทร์ "
    "แล้วเงาของโลกทาบลงบนดวงจันทร์",
    f"{LUNAR} เกิดเมื่อดวงจันทร์มาอยู่ระหว่างดวงอาทิตย์กับโลก "
    "แล้วเงาของดวงจันทร์ทาบลงบนผิวโลก",
    f"{LUNAR} เกิดเมื่อดวงจันทร์หรี่แสงของตัวเองลงชั่วคราว",
    f"{LUNAR} เกิดเมื่อดวงจันทร์เคลื่อนไปอยู่หลังดวงอาทิตย์",
    f"{LUNAR} เกิดเมื่อเงาของดวงจันทร์ทาบลงบนโลก",
    f"{LUNAR} เกิดเมื่อโลกมาอยู่ระหว่างดวงอาทิตย์กับดวงจันทร์ "
    "แล้วเงาของดวงจันทร์ทาบลงบนผิวโลก",
    f"{LUNAR} เกิดเมื่อดวงอาทิตย์มาอยู่ระหว่างโลกกับดวงจันทร์ "
    "แล้วเงาของโลกทาบลงบนดวงจันทร์",
    SOLAR_HOW,
)


# More respects in which the two differ, each with its own pair of alike-statements.
ECLIPSES = (*ECLIPSES,
    Eclipse("การดูด้วยตาเปล่า",
            "ห้ามมองด้วยตาเปล่า ต้องใช้แว่นกรองแสงที่ได้มาตรฐาน",
            "มองด้วยตาเปล่าได้อย่างปลอดภัย",
            ("มองด้วยตาเปล่าได้ปลอดภัยทั้งสองปรากฏการณ์",
             "ต้องใช้แว่นกรองแสงทั้งสองปรากฏการณ์")),
    Eclipse("สิ่งที่ถูกบังหรือมืดลง",
            "ดวงอาทิตย์ถูกดวงจันทร์บังไปบางส่วนหรือทั้งดวง",
            "ดวงจันทร์มืดลงหรือเป็นสีแดงอิฐเพราะอยู่ในเงาของโลก",
            ("ดวงจันทร์มืดลงทั้งสองปรากฏการณ์",
             "ดวงอาทิตย์ถูกบังทั้งสองปรากฏการณ์")),
    Eclipse("ระยะเวลาที่มืดเต็มดวง",
            "ช่วงมืดเต็มดวงนานเพียงไม่กี่นาที",
            "ช่วงเต็มดวงนานได้ราวหนึ่งชั่วโมง",
            ("ช่วงเต็มดวงนานหลายวันทั้งสองปรากฏการณ์",
             "ช่วงเต็มดวงนานไม่กี่วินาทีทั้งสองปรากฏการณ์")),
)
MORE_ECLIPSE_WRONGS |= {
    "การดูด้วยตาเปล่า": ("ต้องใช้กล้องโทรทรรศน์เท่านั้นทั้งสองปรากฏการณ์",
                         "มองผ่านแว่นกันแดดธรรมดาได้ทั้งสองปรากฏการณ์"),
    "สิ่งที่ถูกบังหรือมืดลง": ("โลกมืดลงทั้งดวงทั้งสองปรากฏการณ์",
                               "ดาวฤกษ์ทุกดวงดับลงทั้งสองปรากฏการณ์"),
    "ระยะเวลาที่มืดเต็มดวง": ("ช่วงเต็มดวงนานตลอดทั้งคืนทั้งสองปรากฏการณ์",
                              "ช่วงเต็มดวงนานเท่ากันพอดีทุกครั้งทั้งสองปรากฏการณ์"),
}

@question_type(
    "astro.eclipse_foundation",
    display_name={"th": "อธิบายการเกิดสุริยุปราคาและจันทรุปราคา"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=SKY_TOPIC,
)
class EclipseFoundation(QuestionType):
    """Explain how each eclipse happens, inside the model the indicator names."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        setup, light, big, small = rng.choice(ECLIPSE_SETUPS)
        solar = rng.random() < 0.5
        event = rng.choice(SOLAR_EVENTS if solar else LUNAR_EVENTS)
        return _labelled(
            stem=f"{setup}{event.format(light=light, big=big, small=small)} "
                 "แบบจำลองนี้อธิบายการเกิดปรากฏการณ์ใด และเกิดขึ้นได้อย่างไร",
            correct=SOLAR_HOW if solar else LUNAR_HOW,
            wrongs=SOLAR_WRONGS if solar else LUNAR_WRONGS,
            hint="ดูว่าในแบบจำลอง เงาของสิ่งใดทาบลงบนสิ่งใด",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.eclipse_fluency",
    display_name={"th": "เปรียบเทียบสุริยุปราคากับจันทรุปราคา"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=SKY_TOPIC,
)
class EclipseFluency(QuestionType):
    """Set the two eclipses against each other — the indicator's second free verb.

    ``เปรียบเทียบ`` puts this set at Fluency, and the indicator names two objects,
    so every answer it accepts states both sides.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(ECLIPSES)
        return _labelled(
            stem=f"เมื่อเปรียบเทียบเรื่อง{item.aspect} {SOLAR}และ{LUNAR}ต่างกันอย่างไร",
            correct=_eclipse_pair(item),
            wrongs=(_eclipse_swapped(item),) + tuple(rng.sample(
                item.wrongs + MORE_ECLIPSE_WRONGS[item.aspect], 2)),
            hint="ตอบให้ครบทั้งสองปรากฏการณ์ แล้วตรวจว่าข้อความใดเป็นของปรากฏการณ์ใด",
            topic=SKY_TOPIC,
        )


@question_type(
    "astro.eclipse_application",
    display_name={"th": "วิเคราะห์ปรากฏการณ์อุปราคา"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=SKY_TOPIC,
)
class EclipseApplication(QuestionType):
    """Judge a viewing plan, a cloud explanation, and a model out of line."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, ECLIPSE_SCENARIOS,
            hint="ถามว่าเงาของสิ่งใดทาบลงบนสิ่งใด และมองเห็นได้กว้างแค่ไหน",
        ), SKY_TOPIC)
