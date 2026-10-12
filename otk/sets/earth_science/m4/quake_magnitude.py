"""แผ่นดินไหว

ธรณีวิทยา · ม.4 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/6

Sets moved here from: science_wave_f75.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f75 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_QUAKE = "แผ่นดินไหว"


QUAKE_FACTS = (
    ("ขนาดของแผ่นดินไหว (magnitude) ต่างจากความรุนแรง (intensity) อย่างไร", "ขนาดบอกพลังงานที่ปล่อยออกมาซึ่งมีค่าเดียว ความรุนแรงบอกผลในแต่ละที่",
     ("ขนาดขึ้นกับระยะห่างจากจุดเกิด ส่วนความรุนแรงมีค่าเดียวทุกพื้นที่", "ความรุนแรงมีค่าเดียวทุกพื้นที่", "ทั้งสองคือสิ่งเดียวกัน วัดได้ด้วยเครื่องวัดแผ่นดินไหวเครื่องเดียว", "ขนาดวัดจากความเสียหายของอาคาร")),
    ("จุดเหนือศูนย์เกิดแผ่นดินไหวคือข้อใด", "ตำแหน่งบนผิวโลกที่อยู่ตรงเหนือจุดที่หินแตกหรือเลื่อน",
     ("จุดที่หินแตกหรือเลื่อนซึ่งอยู่ลึกลงไปใต้ผิวโลกหลายกิโลเมตร", "ตำแหน่งสถานีวัด", "จุดที่ความเสียหายน้อยที่สุดบนผิวโลก", "ศูนย์กลางของโลกที่อยู่ใต้จุดที่หินแตก")),
    ("ขณะเกิดแผ่นดินไหวในอาคาร ควรปฏิบัติอย่างไร", "หมอบลง หาที่กำบังใต้โต๊ะที่แข็งแรง และจับยึดไว้",
     ("วิ่งลงบันไดทันที", "ใช้ลิฟต์ออกจากอาคาร", "ยืนใกล้หน้าต่างกระจก", "ยืนใต้โคมไฟแขวน")),
    ("ดินเหลว (liquefaction) จากแผ่นดินไหวเกิดขึ้นในพื้นที่แบบใด", "ดินทรายอิ่มน้ำที่สั่นจนสูญเสียความแข็งแรงคล้ายของเหลว",
     ("หินแกรนิตแข็ง", "ภูเขาหินปูน", "ทะเลทรายที่แห้งสนิท", "ธารน้ำแข็ง")),
    ("แผ่นดินไหวส่วนใหญ่ของโลกเกิดบริเวณใด", "แนวรอยต่อของแผ่นธรณี เช่น วงแหวนแห่งไฟรอบมหาสมุทรแปซิฟิก",
     ("กลางแผ่นทวีปที่ไม่มีรอยเลื่อน เช่น ที่ราบกว้างในทวีปออสเตรเลีย", "ขั้วโลกเหนือและขั้วโลกใต้ที่มีน้ำแข็งหนาทับอยู่", "แนวเส้นศูนย์สูตรที่โลกหมุนเร็วที่สุด", "บริเวณที่มีฝนตกชุก")),
    ("ก่อนแผ่นดินไหวใหญ่มักเกิดอะไร และหลังแผ่นดินไหวใหญ่เกิดอะไร", "อาจมีแผ่นดินไหวนำ และหลังจากนั้นมักมีแผ่นดินไหวตาม",
     ("ไม่มีแผ่นดินไหวใดเกิดก่อนหรือหลังเลย", "หลังแผ่นดินไหวใหญ่จะไม่มีแผ่นดินไหวอีก", "แผ่นดินไหวตามรุนแรงกว่าเสมอ และเกิดก่อนแผ่นดินไหวหลัก", "เกิดสึนามิทุกครั้งแม้เกิดบนบก")),
    ("บริเวณใดของประเทศไทยมีความเสี่ยงแผ่นดินไหวค่อนข้างสูง", "ภาคเหนือและภาคตะวันตกที่มีรอยเลื่อนมีพลัง",
     ("ภาคกลางตอนล่างเท่านั้น", "ทุกพื้นที่เสี่ยงเท่ากัน", "เฉพาะเกาะกลางอ่าวไทย", "ไม่มีพื้นที่ใดเสี่ยง")),
)


QUAKE_HINT = ("ขนาดบอกพลังงานของแผ่นดินไหว เพิ่ม 1 แมกนิจูด แอมพลิจูดคลื่นเพิ่ม 10 เท่า พลังงานเพิ่มประมาณ 32 เท่า "
              "ความรุนแรงบอกผลที่แต่ละที่ ขณะเกิดให้หมอบ ป้อง เกาะ")


MERCALLI = (("II-III", "คนที่อยู่นิ่ง ๆ บนตึกสูงรู้สึกได้ ของแขวนแกว่งเล็กน้อย"), ("IV", "คนในอาคารรู้สึกได้ ประตูหน้าต่างสั่นมีเสียง"),
            ("V", "คนเกือบทุกคนรู้สึก ของวางไม่มั่นคงตกหล่น"), ("VI", "ทุกคนรู้สึก เครื่องเรือนหนักเคลื่อนที่ ปูนฉาบร่วง"),
            ("VII", "คนตกใจวิ่งออกนอกอาคาร อาคารที่สร้างไม่ดีเสียหาย"), ("VIII", "อาคารธรรมดาพังบางส่วน ปล่องไฟและกำแพงล้ม"),
            ("IX", "อาคารที่ออกแบบดีเสียหายมาก พื้นดินแตก"), ("X", "อาคารส่วนใหญ่พัง รางรถไฟบิดงอ"))


@question_type(
    "geo.quake_magnitude_foundation",
    display_name={"th": "ขนาด ความรุนแรง และการปฏิบัติตนเมื่อเกิดแผ่นดินไหว"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_QUAKE,
)
class QuakeMagnitudeFoundation(QuestionType):
    """Magnitude against intensity, focus and epicentre, and safety."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(QUAKE_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_QUAKE, hint=QUAKE_HINT)


@question_type(
    "geo.quake_magnitude_fluency",
    display_name={"th": "อ่านมาตราความรุนแรงเมอร์คัลลี"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_QUAKE,
)
class QuakeMagnitudeFluency(QuestionType):
    """Which Mercalli level matches what people saw."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        level, seen = rng.choice(MERCALLI)
        others = rng.sample([m for m in MERCALLI if m[0] != level], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"ผู้คนรายงานว่า \"{seen}\" ความรุนแรงตามมาตราเมอร์คัลลีน่าจะเป็นระดับใด", correct=f"ระดับ {level}",
                             wrongs=tuple(f"ระดับ {m[0]}" for m in others), topic=TOPIC_QUAKE, hint=QUAKE_HINT)
        return _labelled(stem=f"ความรุนแรงแผ่นดินไหวระดับ {level} ตามมาตราเมอร์คัลลีมีลักษณะอย่างไร", correct=seen, wrongs=tuple(m[1] for m in others),
                         topic=TOPIC_QUAKE, hint=QUAKE_HINT)


@question_type(
    "geo.quake_magnitude_application",
    display_name={"th": "เปรียบเทียบขนาดแผ่นดินไหว"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_QUAKE,
)
class QuakeMagnitudeApplication(QuestionType):
    """Ten times the amplitude and about 32 times the energy per magnitude step."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        low = Fraction(rng.randrange(30, 71), 10)
        step = rng.randint(1, 3)
        high = low + step
        if rng.random() < 0.5:
            return numeric(stem=f"แผ่นดินไหวขนาด {show(high)} มีแอมพลิจูดของคลื่นเป็นกี่เท่าของแผ่นดินไหวขนาด {show(low)} (ขนาดเพิ่ม 1 แอมพลิจูดเพิ่ม 10 เท่า)",
                           answer=10 ** step, wrongs=[step, 10 * step, 32 ** step], unit="เท่า", topic=TOPIC_QUAKE, hint=QUAKE_HINT)
        return numeric(stem=f"แผ่นดินไหวขนาด {show(high)} ปล่อยพลังงานประมาณกี่เท่าของแผ่นดินไหวขนาด {show(low)} (ขนาดเพิ่ม 1 พลังงานเพิ่มประมาณ 32 เท่า)",
                       answer=32 ** step, wrongs=[32 * step, 10 ** step, step], unit="เท่า", topic=TOPIC_QUAKE, hint=QUAKE_HINT)
