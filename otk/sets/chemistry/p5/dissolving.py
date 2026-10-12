"""การละลายของสารในน้ำ

เคมี · ป.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ป.5/2

Sets moved here from: science_wave_d6.
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
from otk.sets._support.science_wave_c23 import Part
from otk.sets._support.science_wave_c24 import parts_item
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d6 import FIFTH

PROVENANCE = Provenance("original")


DISSOLVING_TOPIC = "การละลายของสารในน้ำ"


class Solute(NamedTuple):
    name: str
    dissolves: bool
    seen: str


SOLUTES = (
    Solute("น้ำตาลทราย", True, "มองไม่เห็นเกล็ดน้ำตาล ของผสมใสและเป็นเนื้อเดียวกันทั้งแก้ว"),
    Solute("เกลือแกง", True, "มองไม่เห็นเกล็ดเกลือ ของผสมใสและเป็นเนื้อเดียวกันทั้งแก้ว"),
    Solute("ด่างทับทิม", True, "สีม่วงกระจายทั่วทั้งแก้ว ของผสมใส ไม่มีผงเหลืออยู่"),
    Solute("ทราย", False, "ยังมองเห็นเม็ดทราย และเม็ดทรายตกลงที่ก้นแก้ว"),
    Solute("ผงชอล์ก", False, "ของผสมขุ่น และเมื่อตั้งทิ้งไว้มีผงตกตะกอนที่ก้นแก้ว"),
    Solute("ขี้เลื่อย", False, "ยังมองเห็นขี้เลื่อยลอยอยู่ที่ผิวน้ำ"),
    Solute("ผงกาแฟสำเร็จรูป", True, "ของผสมสีน้ำตาลใส ไม่มีผงเหลืออยู่ที่ก้นแก้ว"),
    Solute("จุนสี", True, "สีฟ้ากระจายทั่วทั้งแก้ว ของผสมใส ไม่มีผลึกเหลืออยู่"),
    Solute("ผงถ่าน", False, "ของผสมสีดำขุ่น และมีผงถ่านตกตะกอนที่ก้นแก้ว"),
    Solute("ผงตะไบเหล็ก", False, "ผงเหล็กจมอยู่ที่ก้นแก้ว น้ำด้านบนใส"),
)


DISSOLVED = "ละลายน้ำ ได้สารละลายที่เป็นเนื้อเดียวกัน"


UNDISSOLVED = "ไม่ละลายน้ำ ยังมองเห็นอนุภาคของสารแยกอยู่"


def solute_part(solute: Solute) -> Part:
    right, wrong = (DISSOLVED, UNDISSOLVED) if solute.dissolves else (UNDISSOLVED, DISSOLVED)
    return Part(solute.name, right, wrong)


DISSOLVING_SCENARIOS = (
    ("นักเรียนใส่น้ำตาลก้อนลงในน้ำสองแก้ว แก้วแรกคน แก้วที่สองไม่คน พบว่าน้ำตาลในแก้วแรกหมดเร็วกว่า ข้อสรุปใดสอดคล้องกับผลนี้",
     "การคนช่วยให้น้ำตาลละลายได้เร็วขึ้น",
     ("การคนทำให้น้ำตาลไม่ละลาย",
      "น้ำตาลในแก้วที่สองไม่ละลายน้ำเลย",
      "การคนทำให้น้ำตาลกลายเป็นทราย",
      "การคนทำให้น้ำระเหยเร็วขึ้นเท่านั้น",
      "น้ำตาลก้อนละลายได้เฉพาะเมื่อไม่คน")),
    ("แม่ทำน้ำเชื่อมโดยละลายน้ำตาลในน้ำ เมื่อต้มน้ำเชื่อมจนน้ำระเหยไปหมด จะพบอะไรในหม้อ",
     "เกล็ดน้ำตาลเหลืออยู่ เพราะน้ำตาลที่ละลายไม่ได้หายไป เพียงกระจายอยู่ในน้ำ",
     ("ไม่เหลืออะไรเลย เพราะน้ำตาลระเหยไปพร้อมน้ำ",
      "เม็ดทรายเหลืออยู่แทนน้ำตาล",
      "น้ำเหลืออยู่แต่น้ำตาลหายไป",
      "น้ำตาลกลายเป็นเกลือ",
      "น้ำตาลกลายเป็นแก๊สลอยออกไปหมด")),
    ("นักเรียนต้องการแยกทรายออกจากน้ำเกลือ ควรใช้วิธีใดก่อน เพราะเหตุใด",
     "กรองด้วยกระดาษกรอง เพราะทรายไม่ละลายน้ำจึงค้างบนกระดาษกรอง ส่วนเกลือที่ละลายผ่านไปกับน้ำ",
     ("กรองด้วยกระดาษกรอง เพราะเกลือไม่ละลายน้ำจึงค้างบนกระดาษกรอง",
      "คนให้แรงขึ้น ทรายจะละลายหายไป",
      "ใช้แม่เหล็กดูด เพราะเกลือเป็นโลหะ",
      "ต้มให้เดือด ทรายจะระเหยไปกับไอน้ำ",
      "ตั้งทิ้งไว้ เกลือจะตกตะกอนแยกออกจากทราย")),
    ("นักเรียนใส่น้ำตาลปริมาณเท่ากันลงในน้ำร้อนและน้ำเย็นปริมาณเท่ากัน พบว่าน้ำตาลในน้ำร้อนละลายหมดเร็วกว่า ข้อสรุปใดสอดคล้องกับผลนี้",
     "น้ำที่ร้อนกว่าช่วยให้น้ำตาลละลายได้เร็วขึ้น",
     ("น้ำเย็นทำให้น้ำตาลละลายเร็วกว่า",
      "น้ำตาลไม่ละลายในน้ำเย็นเลย",
      "น้ำร้อนทำให้น้ำตาลกลายเป็นแก๊ส",
      "อุณหภูมิไม่มีผลต่อการละลาย",
      "น้ำร้อนทำให้น้ำตาลเปลี่ยนเป็นทราย")),
    ("เหตุใดเมื่อชงน้ำหวานจากผงน้ำหวานแล้วตั้งทิ้งไว้ จึงไม่มีผงตกอยู่ที่ก้นแก้ว",
     "ผงน้ำหวานละลายน้ำ กระจายเป็นเนื้อเดียวกันทั้งแก้ว จึงไม่ตกตะกอน",
     ("ผงน้ำหวานลอยอยู่ที่ผิวน้ำทั้งหมด",
      "ผงน้ำหวานระเหยไปพร้อมกับน้ำ",
      "ผงน้ำหวานไม่ละลาย แต่เบาเกินกว่าจะตก",
      "ผงน้ำหวานเกาะติดผนังแก้วทั้งหมด",
      "ผงน้ำหวานกลายเป็นน้ำแข็งในแก้ว")),
)


@question_type(
    "chem.dissolving_foundation",
    display_name={"th": "ระบุสารที่ละลายน้ำได้"},
    level=FIFTH, subject=SUBJECT, topic=DISSOLVING_TOPIC,
)
class DissolvingFoundation(QuestionType):
    """Which of four substances dissolves in water."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        dissolves = rng.random() < 0.5
        right = rng.choice([s for s in SOLUTES if s.dissolves == dissolves])
        wrongs = [s.name for s in SOLUTES if s.dissolves != dissolves]
        return _labelled(
            stem=f"สารใด{'ละลายน้ำได้' if dissolves else 'ไม่ละลายน้ำ'}",
            correct=right.name,
            wrongs=tuple(wrongs),
            hint="สารที่ละลายน้ำจะกระจายจนมองไม่เห็นอนุภาค และได้ของผสมเนื้อเดียวกัน",
            topic=DISSOLVING_TOPIC,
        )


@question_type(
    "chem.dissolving_fluency",
    display_name={"th": "อธิบายการละลายของสารในน้ำจากผลการทดลอง"},
    level=FIFTH, subject=SUBJECT, topic=DISSOLVING_TOPIC,
)
class DissolvingFluency(QuestionType):
    """Three substances stirred into water; explain whether each dissolved."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        one = rng.choice([s for s in SOLUTES if s.dissolves])
        other = rng.choice([s for s in SOLUTES if not s.dissolves])
        third = rng.choice([s for s in SOLUTES if s not in (one, other)])
        chosen = [one, other, third]
        rng.shuffle(chosen)
        record = " / ".join(f"{s.name}: {s.seen}" for s in chosen)
        return parts_item(
            rng, tuple(solute_part(s) for s in chosen),
            stem=(f"นักเรียนใส่สารชนิดละ 1 ช้อนลงในน้ำแก้วละ 100 มิลลิลิตร แล้วคนให้ทั่ว ได้ผลดังนี้ — {record} "
                  "จากหลักฐานนี้ ข้อใดอธิบายการละลายของสารทั้งสามได้ถูกต้องทั้งหมด"),
            hint="ถ้ามองไม่เห็นอนุภาคและได้ของผสมใสเป็นเนื้อเดียวกัน สารนั้นละลายน้ำ",
            topic=DISSOLVING_TOPIC,
        )


@question_type(
    "chem.dissolving_application",
    display_name={"th": "ใช้ความรู้เรื่องการละลายในชีวิตประจำวัน"},
    level=FIFTH, subject=SUBJECT, topic=DISSOLVING_TOPIC,
)
class DissolvingApplication(QuestionType):
    """Stirring, boiling syrup dry, and separating sand from salt water."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, DISSOLVING_SCENARIOS,
            hint="สารที่ละลายยังอยู่ในน้ำ เพียงมองไม่เห็น ส่วนสารที่ไม่ละลายยังแยกเป็นอนุภาคอยู่",
        ), DISSOLVING_TOPIC)
