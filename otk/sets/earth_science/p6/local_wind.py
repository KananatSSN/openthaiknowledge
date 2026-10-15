"""ลมบก ลมทะเล และมรสุม

ธรณีวิทยา · ป.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.6/4

Sets moved here from: science_wave_c14.
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
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c13 import _swapped, _swaps
from otk.sets._support.science_wave_c14 import WIND_SCENARIOS

PROVENANCE = Provenance("original")


WIND_TOPIC = "ลมบก ลมทะเล และมรสุม"


WIND_MODEL = ("แบบจำลอง: วางถาดทรายคู่กับถาดน้ำในกล่องใส จุดธูปไว้ระหว่างถาด "
              "เปิดหลอดไฟส่องทั้งสองถาดนาน 15 นาที แล้วปิดไฟทิ้งไว้อีก 15 นาที")


class Wind(NamedTuple):
    """One wind: how it forms, what the model shows, and its effects."""
    name: str
    forms: str
    on_living: str
    on_environment: str


# No two winds share a description or an effect, so a swap always changes the text.
WINDS = (
    Wind("ลมทะเล",
         "เกิดตอนกลางวัน พื้นดินร้อนเร็วกว่าน้ำ อากาศเหนือพื้นดินลอยขึ้น ลมจึงพัดจากทะเลเข้าหาฝั่ง",
         "ชาวประมงเรือใบใช้ลมนี้แล่นเรือกลับเข้าฝั่งในตอนบ่าย",
         "ทำให้อากาศบริเวณชายฝั่งเย็นลงในตอนกลางวัน"),
    Wind("ลมบก",
         "เกิดตอนกลางคืน พื้นดินเย็นเร็วกว่าน้ำ อากาศเหนือน้ำลอยขึ้น ลมจึงพัดจากฝั่งออกสู่ทะเล",
         "ชาวประมงเรือใบใช้ลมนี้แล่นเรือออกทะเลในตอนเช้ามืด",
         "พัดความชื้นและควันไฟจากชายฝั่งออกไปทางทะเลในตอนกลางคืน"),
    Wind("มรสุม",
         "เกิดตามฤดูกาล พื้นทวีปกับมหาสมุทรร้อนและเย็นต่างกันเป็นเวลาหลายเดือน ลมจึงพัดเปลี่ยนทิศตามฤดู",
         "ชาวนาอาศัยฝนที่มากับลมนี้ในการปลูกข้าว",
         "นำฝนตกหนักมาเป็นเวลาหลายเดือน บางปีทำให้เกิดน้ำท่วม"),
)


def _effects(wind: Wind) -> str:
    return f"ต่อสิ่งมีชีวิต: {wind.on_living} / ต่อสิ่งแวดล้อม: {wind.on_environment}"


def _compare_winds(names: list[str], forms: list[str]) -> str:
    return " / ".join(f"{name}: {form}" for name, form in zip(names, forms))


MODEL_OBSERVATIONS = (
    ("ลมทะเล", "ขณะเปิดไฟ ควันธูปลอยเอียงจากถาดน้ำไปทางถาดทราย"),
    ("ลมบก", "หลังปิดไฟ ควันธูปลอยเอียงจากถาดทรายไปทางถาดน้ำ"),
)


# The same two observations in other words, so the record reads differently.
MORE_OBSERVATIONS = {
    "ลมทะเล": ("ระหว่างที่หลอดไฟส่องอยู่ ควันธูปเคลื่อนจากเหนือถาดน้ำไปเหนือถาดทราย",
               "เมื่อเปิดไฟได้ไม่กี่นาที ควันธูปถูกพัดจากฝั่งถาดน้ำเข้าหาถาดทราย"),
    "ลมบก": ("เมื่อปิดไฟไปสักพัก ควันธูปเคลื่อนจากเหนือถาดทรายไปเหนือถาดน้ำ",
             "หลังปิดไฟจนทรายเย็นลง ควันธูปถูกพัดจากฝั่งถาดทรายออกไปทางถาดน้ำ"),
}


# More effects of each wind, beside the one in ``WINDS``. No text is shared
# between winds, so a borrowed half always makes a choice wrong.
MORE_EFFECTS = {
    "ลมทะเล": (("คนที่อาศัยริมทะเลเปิดหน้าต่างด้านทะเลรับลมเย็นในตอนกลางวัน",
                "นักท่องเที่ยวริมหาดรู้สึกสบายตัวขึ้นในตอนบ่ายเพราะลมเย็นจากทะเล"),
               ("พัดไอเค็มจากทะเลเข้ามา ทำให้ของที่เป็นเหล็กริมชายฝั่งเป็นสนิมง่าย",
                "พัดความชื้นจากทะเลเข้าสู่ชายฝั่งในตอนกลางวัน")),
    "ลมบก": (("ชาวประมงที่ออกเรือตอนกลางคืนได้ลมส่งท้ายเรือออกสู่ทะเล",
              "ชาวประมงพื้นบ้านอาศัยลมนี้พาเรือออกไปวางอวนก่อนรุ่งสาง"),
             ("พัดกลิ่นและฝุ่นจากแผ่นดินออกไปเหนือทะเลในตอนกลางคืน",
              "พัดอากาศจากแผ่นดินออกสู่ทะเล ชายฝั่งจึงไม่ได้รับไอเค็มในตอนกลางคืน")),
    "มรสุม": (("ชาวประมงชายฝั่งต้องหยุดออกเรือหลายเดือนเพราะคลื่นลมแรงในฤดูนี้",
               "เกษตรกรวางแผนปลูกพืชตามช่วงเดือนที่ลมนี้นำฝนมา"),
              ("ทำให้คลื่นในทะเลสูงและแรงต่อเนื่องหลายเดือน ชายหาดบางแห่งถูกกัดเซาะ",
               "ทำให้แม่น้ำและอ่างเก็บน้ำมีน้ำเพิ่มขึ้นมากในช่วงหลายเดือนนั้น")),
}


def _one_effect_each(rng: Random, wind: Wind) -> Wind:
    """The wind with one of its effects on each side, chosen from all it has."""
    living, environment = MORE_EFFECTS[wind.name]
    return wind._replace(on_living=rng.choice((wind.on_living, *living)),
                         on_environment=rng.choice((wind.on_environment, *environment)))


@question_type(
    "geo.local_wind_foundation",
    display_name={"th": "ผลของลมบก ลมทะเล และมรสุมต่อสิ่งมีชีวิตและสิ่งแวดล้อม"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=WIND_TOPIC,
)
class LocalWindFoundation(QuestionType):
    """Explain a wind's effects on living things and on the environment together.

    The verb names both, so every answer states one effect on each; a wrong
    choice borrows another wind's effect for at least one of the two.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        wind = _one_effect_each(rng, rng.choice(WINDS))
        others = [_one_effect_each(rng, other) for other in WINDS if other.name != wind.name]
        rng.shuffle(others)
        # Every wrong choice borrows another wind's effect for at least one half.
        candidates = ([_effects(other) for other in others]
                      + [_effects(wind._replace(on_living=other.on_living)) for other in others]
                      + [_effects(wind._replace(on_environment=other.on_environment))
                         for other in others])
        return _labelled(
            stem=f"{WIND_MODEL} แบบจำลองนี้ใช้อธิบาย{wind.name} "
                 f"{wind.name}ส่งผลต่อสิ่งมีชีวิตและสิ่งแวดล้อมอย่างไร",
            correct=_effects(wind),
            wrongs=tuple(candidates),
            hint="ตรวจทั้งสองส่วน: ผลต่อคนหรือสัตว์ และผลต่ออากาศ ฝน หรือพื้นที่",
            topic=WIND_TOPIC,
        )


@question_type(
    "geo.local_wind_fluency",
    display_name={"th": "เปรียบเทียบการเกิดลมบก ลมทะเล และมรสุมจากแบบจำลอง"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=WIND_TOPIC,
)
class LocalWindFluency(QuestionType):
    """Compare all three winds from the model; each wrong choice swaps two."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        order = list(WINDS)
        rng.shuffle(order)
        names = [wind.name for wind in order]
        forms = [wind.forms for wind in order]
        seen = " และ".join(rng.choice((observation, *MORE_OBSERVATIONS[name]))
                          for name, observation in MODEL_OBSERVATIONS)
        return _labelled(
            stem=f"{WIND_MODEL} ผลที่สังเกตได้: {seen} "
                 "จากแบบจำลองนี้ ข้อใดเปรียบเทียบการเกิดลมบก ลมทะเล และมรสุมได้ถูกต้องทั้งหมด",
            correct=_compare_winds(names, forms),
            wrongs=tuple(_compare_winds(names, _swapped(forms, i, j))
                         for i, j in _swaps(rng, 3, 3)),
            hint="ถาดทรายแทนพื้นดิน ถาดน้ำแทนทะเล เปิดไฟแทนกลางวัน และมรสุมคือแบบเดียวกันแต่กินเวลาเป็นฤดู",
            topic=WIND_TOPIC,
        )


@question_type(
    "geo.local_wind_application",
    display_name={"th": "ใช้ความรู้เรื่องลมบก ลมทะเล และมรสุมในชีวิตจริง"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=WIND_TOPIC,
)
class LocalWindApplication(QuestionType):
    """Change the model, plan a fishing trip, and tell a daily wind from a seasonal one."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, WIND_SCENARIOS,
            hint="หาว่าบริเวณใดร้อนกว่าในช่วงเวลานั้น แล้วนึกว่าลมจะพัดไปทางใด",
        ), WIND_TOPIC)
