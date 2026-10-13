"""ชนิดและการจัดกลุ่มวัสดุ

เคมี · ป.1 · สสวท. พื้นฐาน
Indicators: ว 2.1 ป.1/2

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


GROUPING_TOPIC = "ชนิดและการจัดกลุ่มวัสดุ"


ITEMS = {
    "ช้อนสแตนเลส": "โลหะ", "กุญแจ": "โลหะ", "ตะปู": "โลหะ",
    "ตะเกียบไม้": "ไม้", "ไม้บรรทัดไม้": "ไม้", "ไม้แขวนเสื้อไม้": "ไม้",
    "ยางรัดของ": "ยาง", "ลูกโป่ง": "ยาง",
    "ผ้าเช็ดหน้า": "ผ้า", "ปลอกหมอน": "ผ้า",
    "แก้วน้ำใส": "แก้ว", "กระจกหน้าต่าง": "แก้ว",
    "กระดาษทิชชู": "กระดาษ", "ถุงกระดาษ": "กระดาษ",
    "กล่องดินสอพลาสติก": "พลาสติก", "ตะกร้าพลาสติก": "พลาสติก",
}


# Objects whose names do not give their material away, for identifying it.
UNNAMED_ITEMS = (
    ("กุญแจ", "โลหะ"), ("ตะปู", "โลหะ"), ("ตะเกียบ", "ไม้"), ("เขียงหั่นผัก", "ไม้"),
    ("ลูกโป่ง", "ยาง"), ("หนังสติ๊ก", "ยาง"), ("ปลอกหมอน", "ผ้า"), ("ผ้าห่ม", "ผ้า"),
    ("กระจกหน้าต่าง", "แก้ว"), ("ขวดโหล", "แก้ว"), ("สมุดวาดเขียน", "กระดาษ"),
    ("ซองจดหมาย", "กระดาษ"), ("กล่องใส่ข้าว", "พลาสติก"), ("ของเล่นตัวต่อ", "พลาสติก"),
)


class Criterion(NamedTuple):
    """A property to group by, the materials that have it, and those plainly without it."""
    name: str
    opposite: str
    have: frozenset[str]
    lack: frozenset[str]


# Materials whose answer would be arguable (clear plastic, stretchy cloth) are
# left out of the criterion they would blur, rather than filed by fiat.
CRITERIA = (
    Criterion("มองผ่านได้", "มองผ่านไม่ได้", frozenset({"แก้ว"}), frozenset({"โลหะ", "ไม้", "ผ้า", "กระดาษ"})),
    Criterion("ดึงแล้วยืดและหดกลับได้", "ดึงแล้วไม่ยืด", frozenset({"ยาง"}), frozenset({"โลหะ", "ไม้", "แก้ว", "กระดาษ"})),
    Criterion("ผิวมันวาว", "ผิวไม่มันวาว", frozenset({"โลหะ"}), frozenset({"ไม้", "ผ้า", "กระดาษ"})),
    Criterion("นุ่ม", "ไม่นุ่ม", frozenset({"ผ้า"}), frozenset({"โลหะ", "ไม้", "แก้ว"})),
)


def _groups(criterion: Criterion, have: list[str], lack: list[str]) -> str:
    return f"กลุ่มที่{criterion.name}: {', '.join(have)} / กลุ่มที่{criterion.opposite}: {', '.join(lack)}"


GROUPING_SCENARIOS = (
    ("นักเรียนจัดกลุ่ม ช้อนสแตนเลส กุญแจ และตะปู ไว้ด้วยกัน ส่วน ตะเกียบไม้ และผ้าเช็ดหน้า ไว้อีกกลุ่ม นักเรียนน่าจะใช้สมบัติใดเป็นเกณฑ์",
     "ผิวมันวาวหรือไม่มันวาว",
     ("มองผ่านได้หรือมองผ่านไม่ได้",
      "ดึงแล้วยืดและหดกลับได้หรือไม่",
      "นุ่มหรือไม่นุ่ม",
      "มีสีแดงหรือไม่มีสีแดง",
      "ใช้ในห้องครัวหรือไม่")),
    ("ถ้าต้องจัดลูกโป่งเข้ากลุ่มตามสมบัติ \"ดึงแล้วยืดและหดกลับได้\" ลูกโป่งควรอยู่กลุ่มเดียวกับสิ่งใด",
     "ยางรัดของ เพราะทำจากยางซึ่งดึงแล้วยืดและหดกลับได้เหมือนกัน",
     ("กุญแจ เพราะทำจากวัสดุที่แข็งเหมือนกัน",
      "แก้วน้ำใส เพราะมองผ่านได้เหมือนกัน",
      "ไม้บรรทัดไม้ เพราะมีลวดลายเหมือนกัน",
      "ช้อนสแตนเลส เพราะแข็งเหมือนกัน",
      "ถุงกระดาษ เพราะเบาเหมือนกัน")),
    ("สิ่งของชุดหนึ่งถูกแบ่งเป็นสองกลุ่ม กลุ่มแรกมี แก้วน้ำใส และกระจกหน้าต่าง กลุ่มที่สองมี ถุงกระดาษ และไม้แขวนเสื้อไม้ ถ้านำกุญแจมาจัดเพิ่ม ควรอยู่กลุ่มใด",
     "กลุ่มที่สอง เพราะกลุ่มแรกมองผ่านได้ แต่กุญแจทำจากโลหะซึ่งมองผ่านไม่ได้",
     ("กลุ่มแรก เพราะกุญแจแข็งเหมือนแก้ว",
      "กลุ่มแรก เพราะกุญแจผิวมันวาวเหมือนกระจก",
      "จัดเข้ากลุ่มใดไม่ได้เลย เพราะกุญแจทำจากโลหะ",
      "กลุ่มแรก เพราะกุญแจเล็กเหมือนแก้วน้ำ",
      "กลุ่มที่สอง เพราะกุญแจนุ่มเหมือนถุงกระดาษ")),
    ("นักเรียนจัดกลุ่ม ผ้าเช็ดหน้า และปลอกหมอน ไว้ด้วยกัน ส่วน ตะปู และตะเกียบไม้ ไว้อีกกลุ่ม นักเรียนน่าจะใช้สมบัติใดเป็นเกณฑ์",
     "นุ่มหรือไม่นุ่ม",
     ("มองผ่านได้หรือมองผ่านไม่ได้",
      "ผิวมันวาวหรือไม่มันวาว",
      "ดึงแล้วยืดและหดกลับได้หรือไม่",
      "ใช้ในห้องครัวหรือไม่",
      "มีสีแดงหรือไม่มีสีแดง")),
    ("ถ้าจัดกลุ่มตามสมบัติ \"มองผ่านได้\" ขวดโหลแก้วควรอยู่กลุ่มเดียวกับสิ่งใด",
     "กระจกหน้าต่าง เพราะทำจากแก้วซึ่งมองผ่านได้เหมือนกัน",
     ("ตะปู เพราะแข็งเหมือนกัน",
      "ผ้าห่ม เพราะใช้ในบ้านเหมือนกัน",
      "ลูกโป่ง เพราะกลมเหมือนกัน",
      "ซองจดหมาย เพราะบางเหมือนกัน",
      "กุญแจ เพราะผิวมันวาวเหมือนกัน")),
)


@question_type(
    "chem.material_grouping_foundation",
    display_name={"th": "ระบุชนิดของวัสดุจากสมบัติที่สังเกตได้"},
    level=FIRST, subject=SUBJECT, topic=GROUPING_TOPIC,
)
class MaterialGroupingFoundation(QuestionType):
    """An object and what is observed of it; name its material."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item, material = rng.choice(UNNAMED_ITEMS)
        others = [other for other in MATERIALS if other != material]
        return _labelled(
            stem=f"{item}ชิ้นหนึ่ง{PROPERTY[material]} {item}ชิ้นนี้ทำจากวัสดุชนิดใด",
            correct=material,
            wrongs=tuple(others),
            hint="จับคู่สิ่งที่สังเกตได้กับวัสดุที่มีสมบัตินั้น",
            topic=GROUPING_TOPIC,
        )


@question_type(
    "chem.material_grouping_fluency",
    display_name={"th": "จัดกลุ่มวัสดุตามสมบัติที่สังเกตได้"},
    level=FIRST, subject=SUBJECT, topic=GROUPING_TOPIC,
)
class MaterialGroupingFluency(QuestionType):
    """Five objects and a property; sort every one into its group."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        criterion = rng.choice(CRITERIA)
        having = [item for item, m in ITEMS.items() if m in criterion.have]
        lacking = [item for item, m in ITEMS.items() if m in criterion.lack]
        count = rng.choice((1, 2))
        chosen = rng.sample(having, count) + rng.sample(lacking, 5 - count)
        rng.shuffle(chosen)
        have = [item for item in chosen if item in having]
        lack = [item for item in chosen if item in lacking]
        wrongs = []
        # Each wrong grouping moves exactly one object to the other side.
        for item in rng.sample(chosen, 3):
            if item in have:
                wrongs.append(_groups(criterion, [i for i in have if i != item] or ["ไม่มี"], lack + [item]))
            else:
                wrongs.append(_groups(criterion, have + [item], [i for i in lack if i != item]))
        # Spares move two objects at once, so the answer is not the grouping
        # every wrong differs from by a single move.
        for pair in (rng.sample(chosen, 2) for _ in range(2)):
            moved = set(pair)
            wrongs.append(_groups(criterion,
                                  [i for i in have if i not in moved] + [i for i in lack if i in moved] or ["ไม่มี"],
                                  [i for i in lack if i not in moved] + [i for i in have if i in moved] or ["ไม่มี"]))
        wrongs = list(dict.fromkeys(wrongs))
        return _labelled(
            stem=(f"นักเรียนจัดกลุ่มสิ่งของ ได้แก่ {', '.join(chosen)} ตามสมบัติ \"{criterion.name}\" "
                  "ข้อใดจัดกลุ่มได้ถูกต้อง"),
            correct=_groups(criterion, have, lack),
            wrongs=tuple(wrongs),
            hint="ระบุก่อนว่าสิ่งของแต่ละชิ้นทำจากวัสดุใด แล้วถามว่าวัสดุนั้นมีสมบัตินี้หรือไม่",
            topic=GROUPING_TOPIC,
        )


@question_type(
    "chem.material_grouping_application",
    display_name={"th": "ใช้เกณฑ์สมบัติของวัสดุจัดกลุ่มสิ่งของ"},
    level=FIRST, subject=SUBJECT, topic=GROUPING_TOPIC,
)
class MaterialGroupingApplication(QuestionType):
    """Infer a sorting rule, and place a new object into existing groups."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, GROUPING_SCENARIOS,
            hint="หาสมบัติที่สิ่งของในกลุ่มเดียวกันมีเหมือนกัน แล้วใช้เป็นเกณฑ์",
        ), GROUPING_TOPIC)


# More rows: the set drew from five, so a learner met them all in a few
# tries. Each added row is a situation no other row describes, since every
# row's answer is a distractor for the others, and has five wrong readings.
GROUPING_SCENARIOS += (
    ('นักเรียนจัดกลุ่ม หนังยาง และลูกบอลยาง ไว้ด้วยกัน ส่วน ช้อนโลหะ และไม้บรรทัดไม้ ไว้อีกกลุ่ม นักเรียนน่าจะใช้สมบัติใดเป็นเกณฑ์',
     'ยืดหยุ่นได้หรือไม่',
     ('มองผ่านได้หรือไม่', 'ดูดซับน้ำได้หรือไม่', 'มีสีเหมือนกันหรือไม่', 'มีกลิ่นหรือไม่', 'ทำจากแก้วหรือไม่')),
    ('ถ้าต้องจัดฟองน้ำเข้ากลุ่มตามสมบัติ "ดูดซับน้ำได้" ฟองน้ำควรอยู่กลุ่มเดียวกับสิ่งใด',
     'ผ้าขนหนู',
     ('ช้อนโลหะ', 'ถุงพลาสติก', 'แก้วน้ำ', 'กระจกหน้าต่าง', 'กุญแจ')),
    ('สิ่งของกลุ่มหนึ่งมี ถุงพลาสติก และเสื้อกันฝน อีกกลุ่มมี ผ้าเช็ดหน้า และกระดาษทิชชู นักเรียนน่าจะใช้สมบัติใดเป็นเกณฑ์',
     'ดูดซับน้ำได้หรือไม่',
     ('ยืดหยุ่นได้หรือไม่', 'มองผ่านได้หรือไม่', 'ทำจากโลหะหรือไม่', 'แข็งมากหรือไม่', 'มีขนาดใหญ่หรือไม่')),
    ('ถ้าจัดกลุ่มตามสมบัติ "ผิวมันวาว" ช้อนโลหะควรอยู่กลุ่มเดียวกับสิ่งใด',
     'กุญแจโลหะ',
     ('ผ้าเช็ดหน้า', 'ตะเกียบไม้', 'ถุงกระดาษ', 'ฟองน้ำ', 'ก้อนดินเหนียว')),
)
