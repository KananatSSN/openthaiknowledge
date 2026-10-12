"""ฝน หิมะ และลูกเห็บ

ธรณีวิทยา · ป.5 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.5/5

Sets moved here from: science_wave_c13.
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
from otk.sets._support.science_wave_c10 import LETTERS, SUBJECT
from otk.sets._support.science_wave_c13 import PRECIPITATION_SCENARIOS, _swapped, _swaps

PROVENANCE = Provenance("original")


PRECIPITATION_TOPIC = "ฝน หิมะ และลูกเห็บ"


class Fall(NamedTuple):
    """One kind of precipitation, how it forms, and what a report of it looks like."""
    name: str
    how: str
    report: str


FALLS = (
    Fall("ฝน",
         "ละอองน้ำในเมฆรวมตัวกันจนหนักแล้วตกลงมาเป็นหยดน้ำ",
         "หยดน้ำตกลงมาต่อเนื่องหลายชั่วโมง อุณหภูมิอากาศที่พื้น 27 องศาเซลเซียส"),
    Fall("หิมะ",
         "ไอน้ำในเมฆที่เย็นจัดกลายเป็นผลึกน้ำแข็ง ตกลงมาผ่านอากาศที่เย็นจัดจึงไม่ละลาย",
         "เกล็ดน้ำแข็งสีขาวนุ่มรูปหกแฉกตกลงมาช้า ๆ อุณหภูมิอากาศที่พื้น -4 องศาเซลเซียส"),
    Fall("ลูกเห็บ",
         "หยดน้ำถูกกระแสลมในเมฆฝนฟ้าคะนองพัดขึ้นลงหลายรอบ แข็งตัวพอกเป็นชั้น ๆ จนหนักแล้วตกลงมาเป็นก้อนน้ำแข็ง",
         "ก้อนน้ำแข็งแข็งขนาดเท่าเมล็ดถั่วตกลงมาพร้อมพายุฝนฟ้าคะนอง ผ่าดูเห็นเป็นชั้น ๆ "
         "อุณหภูมิอากาศที่พื้น 33 องศาเซลเซียส"),
)


# Things one sees, one kind each, and a condensation form that does not fall.
FALL_EXAMPLES = {
    "ฝน": ("หยดน้ำตกลงมาจนหลังคาเปียกและน้ำไหลลงรางน้ำ",
           "หยดน้ำตกลงมาเป็นสายระหว่างพายุในฤดูฝน"),
    "หิมะ": ("เกล็ดสีขาวนุ่มตกลงมาสะสมบนพื้นจนขาวทั้งเมืองในประเทศเขตหนาว",
             "เกล็ดน้ำแข็งนุ่ม ๆ ค่อย ๆ ลอยตกลงมาบนยอดเขาสูงที่หนาวจัด"),
    "ลูกเห็บ": ("ก้อนน้ำแข็งแข็งตกกระทบหลังคาสังกะสีเสียงดังระหว่างพายุฝนฟ้าคะนอง",
                "ก้อนน้ำแข็งกลม ๆ ตกลงมาระหว่างพายุฤดูร้อนแล้วละลายบนพื้น"),
}


NOT_A_FALL = ("หยดน้ำใสเกาะบนใบหญ้าตอนเช้า", "ละอองขาวลอยต่ำเหนือนาข้าวตอนเช้ามืด")


# More records of each kind. Every one keeps the cue the base report gives:
# drops or soft flakes or layered lumps, and the air temperature at the ground.
MORE_FALL_REPORTS = {
    "ฝน": ("หยดน้ำตกลงมาหนักราวครึ่งชั่วโมงจนถนนมีน้ำขัง อุณหภูมิอากาศที่พื้น 29 องศาเซลเซียส",
           "หยดน้ำตกลงมาปรอย ๆ เกือบทั้งวัน อุณหภูมิอากาศที่พื้น 24 องศาเซลเซียส"),
    "หิมะ": ("เกล็ดสีขาวนุ่มสะสมบนหลังคาหนาขึ้นเรื่อย ๆ อุณหภูมิอากาศที่พื้น -2 องศาเซลเซียส",
             "เกล็ดน้ำแข็งรูปหกแฉกตกลงบนถุงมือแล้วยังไม่ละลาย อุณหภูมิอากาศที่พื้น -6 องศาเซลเซียส"),
    "ลูกเห็บ": ("ก้อนน้ำแข็งแข็งขนาดเท่าลูกปิงปองตกลงมาระหว่างพายุฝนฟ้าคะนอง ผ่าดูเห็นเป็นชั้น ๆ "
                "อุณหภูมิอากาศที่พื้น 31 องศาเซลเซียส",
                "ก้อนน้ำแข็งกลมแข็งตกกระทบหลังคาเสียงดังระหว่างฟ้าคะนอง ผ่าดูเห็นเป็นชั้น ๆ "
                "อุณหภูมิอากาศที่พื้น 35 องศาเซลเซียส"),
}


def _report(rng: Random, fall: Fall) -> str:
    return rng.choice((fall.report, *MORE_FALL_REPORTS[fall.name]))


def _compare_falls(letters: list[str], names: list[str]) -> str:
    by_name = {fall.name: fall for fall in FALLS}
    return " / ".join(f"เหตุการณ์ {letter} เป็น{name} เพราะ{by_name[name].how}"
                      for letter, name in zip(letters, names))


@question_type(
    "geo.precipitation_forms_foundation",
    display_name={"th": "ฝน หิมะ และลูกเห็บ"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=PRECIPITATION_TOPIC,
)
class PrecipitationFormsFoundation(QuestionType):
    """Know each of the three one at a time, before comparing them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        fall = rng.choice(FALLS)
        others = [other.how for other in FALLS if other.name != fall.name]
        ask = rng.randrange(4)
        if ask == 2:
            return _labelled(
                stem=f"“{rng.choice(FALL_EXAMPLES[fall.name])}” คือสิ่งใด",
                correct=fall.name,
                wrongs=tuple(other.name for other in FALLS if other.name != fall.name)
                       + ("น้ำค้าง",),
                hint="ถามว่าสิ่งที่ตกลงมาเป็นน้ำหรือน้ำแข็ง และเป็นเกล็ดนุ่มหรือก้อนแข็ง",
                topic=PRECIPITATION_TOPIC,
            )
        if ask == 3:
            return _labelled(
                stem=f"ข้อใดเป็นตัวอย่างของ “{fall.name}”",
                correct=rng.choice(FALL_EXAMPLES[fall.name]),
                wrongs=tuple(rng.choice(FALL_EXAMPLES[other.name])
                             for other in FALLS if other.name != fall.name)
                       + (rng.choice(NOT_A_FALL),),
                hint="ถามว่าสิ่งที่ตกลงมาเป็นน้ำหรือน้ำแข็ง และเป็นเกล็ดนุ่มหรือก้อนแข็ง",
                topic=PRECIPITATION_TOPIC,
            )
        if ask == 0:
            return _labelled(
                stem=f"“{fall.name}” เกิดขึ้นได้อย่างไร",
                correct=fall.how,
                wrongs=tuple(others) + ("ไอน้ำควบแน่นเป็นหยดน้ำเกาะบนผิววัตถุที่เย็น",),
                hint="ถามว่าสิ่งที่ตกลงมาเป็นน้ำหรือน้ำแข็ง และเกิดในเมฆแบบใด",
                topic=PRECIPITATION_TOPIC,
            )
        return _labelled(
            stem=f"สิ่งที่เกิดจาก{fall.how} เรียกว่าอะไร",
            correct=fall.name,
            wrongs=tuple(other.name for other in FALLS if other.name != fall.name) + ("น้ำค้าง",),
            hint="ถามว่าสิ่งที่ตกลงมาเป็นน้ำหรือน้ำแข็ง และเกิดในเมฆแบบใด",
            topic=PRECIPITATION_TOPIC,
        )


@question_type(
    "geo.precipitation_forms_fluency",
    display_name={"th": "เปรียบเทียบการเกิดฝน หิมะ และลูกเห็บจากข้อมูล"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=PRECIPITATION_TOPIC,
)
class PrecipitationFormsFluency(QuestionType):
    """Name and explain all three from a record; each wrong choice swaps two."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        events = list(FALLS)
        rng.shuffle(events)
        letters = list(LETTERS[:3])
        record = " / ".join(f"เหตุการณ์ {letter}: {_report(rng, fall)}"
                            for letter, fall in zip(letters, events))
        names = [fall.name for fall in events]
        return _labelled(
            stem=f"นักเรียนรวบรวมรายงานเหตุการณ์ที่มีสิ่งตกลงมาจากท้องฟ้า 3 เหตุการณ์ — {record} "
                 "จากข้อมูลนี้ ข้อใดเปรียบเทียบการเกิดฝน หิมะ และลูกเห็บได้ถูกต้องทั้งหมด",
            correct=_compare_falls(letters, names),
            wrongs=tuple(_compare_falls(letters, _swapped(names, i, j))
                         for i, j in _swaps(rng, 3, 3)),
            hint="ดูว่าสิ่งที่ตกลงมาเป็นหยดน้ำ เกล็ดนุ่ม หรือก้อนแข็งเป็นชั้น แล้วดูอุณหภูมิที่พื้นประกอบ",
            topic=PRECIPITATION_TOPIC,
        )


@question_type(
    "geo.precipitation_forms_application",
    display_name={"th": "อธิบายฝน หิมะ และลูกเห็บในประเทศไทย"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=PRECIPITATION_TOPIC,
)
class PrecipitationFormsApplication(QuestionType):
    """Summer hail in Thailand, no snow in Bangkok, and staying safe in a storm."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, PRECIPITATION_SCENARIOS,
            hint="ถามว่าน้ำแข็งเกิดที่ใดในเมฆ และอากาศระหว่างทางอุ่นพอจะละลายหรือไม่",
        ), PRECIPITATION_TOPIC)
