"""สมบัติของวัสดุที่ใช้ทำวัตถุ

เคมี · ป.1 · สสวท. พื้นฐาน
Indicators: ว 2.1 ป.1/1

Sets moved here from: science_wave_d1.
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
from otk.sets._support.science_wave_d1 import FIRST, MATERIALS, PROPERTY, SUBJECT

PROVENANCE = Provenance("original")


PROPERTY_TOPIC = "สมบัติของวัสดุที่ใช้ทำวัตถุ"


class Thing(NamedTuple):
    """An object and its parts, each part made of one material."""
    name: str
    parts: tuple[tuple[str, str], ...]


THINGS = (
    Thing("กรรไกร", (("ใบมีด", "โลหะ"), ("ด้ามจับ", "พลาสติก"))),
    Thing("กระทะ", (("ตัวกระทะ", "โลหะ"), ("ด้ามจับ", "ไม้"))),
    Thing("ดินสอที่มียางลบติดปลาย", (("แท่งดินสอ", "ไม้"), ("ยางลบ", "ยาง"))),
    Thing("รองเท้าผ้าใบ", (("ตัวรองเท้า", "ผ้า"), ("พื้นรองเท้า", "ยาง"))),
    Thing("กรอบรูป", (("ขอบกรอบ", "ไม้"), ("แผ่นหน้ากรอบ", "แก้ว"))),
    Thing("ช้อนกินข้าว", (("ทั้งคัน", "โลหะ"),)),
    Thing("ไม้บรรทัด", (("ทั้งอัน", "ไม้"),)),
    Thing("ผ้าเช็ดหน้า", (("ทั้งผืน", "ผ้า"),)),
    Thing("ยางรัดของ", (("ทั้งเส้น", "ยาง"),)),
)


def _made_of(pairs: tuple[tuple[str, str], ...]) -> str:
    """How many materials, then each with its property, as a ป.1 answer reads."""
    count = "ชนิดเดียว" if len(pairs) == 1 else f" {len(pairs)} ชนิด"
    body = " และ".join(f"{material} ซึ่ง{PROPERTY[shown]}" for material, shown in pairs)
    return f"ทำจากวัสดุ{count} คือ {body}"


PROPERTY_SCENARIOS = (
    ("ด้ามจับของกระทะมักทำจากไม้ ส่วนตัวกระทะทำจากโลหะ ข้อใดอธิบายได้ถูกต้อง",
     "วัตถุหนึ่งชิ้นทำจากวัสดุหลายชนิดได้ แต่ละส่วนใช้วัสดุที่มีสมบัติเหมาะกับหน้าที่ของส่วนนั้น",
     ("วัตถุหนึ่งชิ้นต้องทำจากวัสดุชนิดเดียวเสมอ",
      "ด้ามจับทำจากไม้เพราะไม้มีผิวมันวาวเหมือนโลหะ",
      "ตัวกระทะทำจากโลหะเพราะโลหะนุ่มและพับได้",
      "ด้ามจับทำจากไม้เพราะไม้ใสมองผ่านได้",
      "ตัวกระทะทำจากโลหะเพราะโลหะดึงแล้วยืดได้")),
    ("นักเรียนจับกระดาษแผ่นหนึ่งแล้วดึงเบา ๆ กระดาษฉีกขาด แต่เมื่อดึงผ้าเช็ดหน้าแรงเท่ากัน ผ้าไม่ขาด หลักฐานนี้บอกอะไร",
     "กระดาษฉีกขาดได้ง่ายกว่าผ้า",
     ("ผ้าฉีกขาดได้ง่ายกว่ากระดาษ",
      "กระดาษและผ้าเป็นวัสดุชนิดเดียวกัน",
      "กระดาษดึงแล้วยืดออกและหดกลับได้",
      "กระดาษแข็งแรงกว่าผ้า",
      "ผ้าใสมองผ่านได้เหมือนแก้ว")),
    ("ลูกโป่งทำจากยาง เมื่อเป่าลมเข้าไปลูกโป่งพองออก และเมื่อปล่อยลมออกลูกโป่งหดเล็กลง สิ่งที่สังเกตได้นี้แสดงสมบัติใดของยาง",
     "ยางดึงแล้วยืดออกและหดกลับได้",
     ("ยางใสมองผ่านได้",
      "ยางแข็งมีลวดลายของเนื้อไม้",
      "ยางบางฉีกขาดได้ง่าย",
      "ยางผิวมันวาวเหมือนโลหะ",
      "ยางแข็งและเปราะแตกง่าย")),
    ("หน้าต่างบ้านใช้แผ่นแก้ว เพราะแก้วมีสมบัติใดที่สังเกตได้",
     "แก้วใส มองผ่านได้ จึงมองเห็นข้างนอกและแสงส่องเข้ามาได้",
     ("แก้วนุ่ม พับได้",
      "แก้วดึงแล้วยืดออกได้",
      "แก้วมีลวดลายของเนื้อไม้",
      "แก้วฉีกขาดได้ง่าย",
      "แก้วดูดซับน้ำฝนไว้ได้")),
    ("ผ้าเช็ดมือทำจากผ้า ข้อใดเป็นสมบัติที่สังเกตได้ของผ้า",
     "ผ้านุ่ม พับหรือขยำได้",
     ("ผ้าใส มองผ่านได้",
      "ผ้าแข็ง ผิวมันวาว",
      "ผ้าแข็ง มีลวดลายของเนื้อไม้",
      "ผ้าบางใสเหมือนกระจก",
      "ผ้าแตกเมื่อตกพื้น")),
)


@question_type(
    "chem.material_property_foundation",
    display_name={"th": "บอกสมบัติที่สังเกตได้ของวัสดุ"},
    level=FIRST, subject=SUBJECT, topic=PROPERTY_TOPIC,
)
class MaterialPropertyFoundation(QuestionType):
    """One material; the property a learner can see or feel."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        material = rng.choice(MATERIALS)
        others = [other for other in MATERIALS if other != material]
        return _labelled(
            stem=f"ข้อใดเป็นสมบัติที่สังเกตได้ของ{material}",
            correct=PROPERTY[material],
            wrongs=tuple(PROPERTY[other] for other in rng.sample(others, 3)),
            hint="นึกถึงตอนที่ได้จับหรือมองวัสดุนั้น ว่าเป็นอย่างไร",
            topic=PROPERTY_TOPIC,
        )


@question_type(
    "chem.material_property_fluency",
    display_name={"th": "อธิบายวัสดุและสมบัติของวัตถุจากการสังเกต"},
    level=FIRST, subject=SUBJECT, topic=PROPERTY_TOPIC,
)
class MaterialPropertyFluency(QuestionType):
    """An observation record of an object's parts; name every material and its property."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        thing = rng.choice(THINGS)
        seen = " ".join(f"{part}{PROPERTY[material]}" for part, material in thing.parts)
        right = tuple((material, material) for _, material in thing.parts)
        used = {material for _, material in thing.parts}
        stray = rng.choice([m for m in MATERIALS if m not in used])
        if len(right) == 1:
            material = right[0][0]
            wrongs = (
                _made_of(((stray, material),)),
                _made_of(((material, stray),)),
                f"ทำจากวัสดุ 2 ชนิด คือ {material} ซึ่ง{PROPERTY[material]} และ{stray} ซึ่ง{PROPERTY[stray]}",
                # Wrong on two counts: a material it lacks, a property mismatched.
                _made_of(((stray, stray),)),
                f"ทำจากวัสดุ 2 ชนิด คือ {stray} ซึ่ง{PROPERTY[material]} และ{material} ซึ่ง{PROPERTY[stray]}",
            )
        else:
            (first, _), (second, _) = right
            wrongs = (
                _made_of(((first, second), (second, first))),
                _made_of(((stray, first), (second, second))),
                f"ทำจากวัสดุชนิดเดียว คือ {first} ซึ่ง{PROPERTY[first]}",
                # Wrong on two counts: a material it lacks and a swapped
                # property; or one material with the other's property.
                _made_of(((stray, stray), (second, first))),
                f"ทำจากวัสดุชนิดเดียว คือ {second} ซึ่ง{PROPERTY[first]}",
            )
        return _labelled(
            stem=(f"นักเรียนสังเกต{thing.name} บันทึกได้ว่า {seen} "
                  f"จากหลักฐานนี้ ข้อใดอธิบายวัสดุที่ใช้ทำ{thing.name}ได้ถูกต้อง"),
            correct=_made_of(right),
            wrongs=wrongs,
            hint="นับว่ามีกี่ส่วนที่สังเกตได้ต่างกัน แล้วจับคู่สิ่งที่เห็นกับวัสดุทีละส่วน",
            topic=PROPERTY_TOPIC,
        )


@question_type(
    "chem.material_property_application",
    display_name={"th": "ใช้สมบัติที่สังเกตได้ของวัสดุอธิบายสิ่งรอบตัว"},
    level=FIRST, subject=SUBJECT, topic=PROPERTY_TOPIC,
)
class MaterialPropertyApplication(QuestionType):
    """Objects of several materials, telling glass from plastic, and a balloon."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, PROPERTY_SCENARIOS,
            hint="ใช้สิ่งที่มองเห็นหรือจับได้เป็นหลักฐาน แล้วเชื่อมกับสมบัติของวัสดุ",
        ), PROPERTY_TOPIC)


# More rows: the set drew from five, so a learner met them all in a few
# tries. Each added row is a situation no other row describes, since every
# row's answer is a distractor for the others, and has five wrong readings.
PROPERTY_SCENARIOS += (
    ('เมื่อเทน้ำลงบนฟองน้ำ น้ำหายเข้าไปในฟองน้ำ สิ่งที่สังเกตได้นี้แสดงสมบัติใดของฟองน้ำ',
     'ดูดซับน้ำได้',
     ('กันน้ำได้', 'มองผ่านได้', 'แข็งมาก', 'ผิวมันวาว', 'ยืดและหดกลับไม่ได้')),
    ('ถุงพลาสติกใส่น้ำแล้วน้ำไม่ซึมออกมา สมบัติใดของพลาสติกที่ทำให้เป็นเช่นนี้',
     'กันน้ำได้',
     ('ดูดซับน้ำได้ดี', 'เปราะแตกง่าย', 'ผิวขรุขระ', 'นำไฟฟ้าได้', 'ละลายน้ำได้')),
    ('ช้อนโลหะขัดแล้วเห็นเงาสะท้อนได้ สิ่งที่สังเกตได้นี้แสดงสมบัติใดของโลหะ',
     'ผิวมันวาว',
     ('ดูดซับน้ำได้', 'ยืดหยุ่นได้', 'มองผ่านได้', 'นิ่มมาก', 'ผิวหยาบ')),
    ('ก้อนหินกับฟองน้ำ เมื่อกดด้วยนิ้วแรงเท่ากัน ฟองน้ำยุบลงแต่ก้อนหินไม่ยุบ หลักฐานนี้บอกอะไร',
     'ก้อนหินแข็งกว่าฟองน้ำ',
     ('ฟองน้ำแข็งกว่าก้อนหิน', 'ทั้งสองแข็งเท่ากัน', 'ก้อนหินดูดซับน้ำได้ดีกว่า', 'ฟองน้ำโปร่งใสกว่า', 'ก้อนหินยืดหยุ่นกว่า')),
)
