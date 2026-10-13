"""สมบัติการละลายในตัวทำละลายชนิดต่าง ๆ

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/17

Sets moved here from: science_wave_e6.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e6 import SUBJECT, _labelled

PROVENANCE = Provenance("original")


TOPIC_SOLUBILITY = "สมบัติการละลายในตัวทำละลายชนิดต่าง ๆ"


DISSOLVES, DOES_NOT_DISSOLVE = "ละลายได้ดี", "ละลายได้ไม่ดี"


SOLUBILITY_FILLERS = ("ละลายได้ดี เพราะสารทุกชนิดละลายในตัวทำละลายที่เป็นของเหลวได้",
                      "ขึ้นอยู่กับอุณหภูมิเท่านั้น ไม่เกี่ยวกับสภาพขั้วของสาร",
                      "ละลายได้ดีเฉพาะเมื่อคนแรง ๆ เป็นเวลานาน", "ละลายได้ไม่ดี เพราะสารที่มีขั้วไม่ละลายในตัวทำละลายใดเลย")


# The outcome with its reason, so the answer is not the one short choice.
DISSOLVE_WHY = {True: "ละลายได้ดี เพราะสภาพขั้วของสารทั้งสองเหมือนกัน",
                False: "ละลายได้ไม่ดี เพราะสภาพขั้วของสารทั้งสองต่างกัน"}


class SolubilityItem(NamedTuple):
    pair_name: str
    dissolves: bool


SOLUBILITY_ITEMS: tuple[SolubilityItem, ...] = (
    SolubilityItem("เกลือแกง (มีขั้ว) ในน้ำ (มีขั้ว)", True),
    SolubilityItem("น้ำตาลทราย (มีขั้ว) ในน้ำ (มีขั้ว)", True),
    SolubilityItem("น้ำมันพืช (ไม่มีขั้ว) ในเฮกเซน (ไม่มีขั้ว)", True),
    SolubilityItem("ไอโอดีน (ไม่มีขั้ว) ในคาร์บอนเตตระคลอไรด์ (ไม่มีขั้ว)", True),
    SolubilityItem("น้ำมันพืช (ไม่มีขั้ว) ในน้ำ (มีขั้ว)", False),
    SolubilityItem("ไอโอดีน (ไม่มีขั้ว) ในน้ำ (มีขั้ว)", False),
    SolubilityItem("แนฟทาลีน (ไม่มีขั้ว) ในน้ำ (มีขั้ว)", False),
    SolubilityItem("เอทานอล (มีขั้ว) ในน้ำ (มีขั้ว)", True),
    SolubilityItem("แนฟทาลีน (ไม่มีขั้ว) ในเฮกเซน (ไม่มีขั้ว)", True),
    SolubilityItem("ขี้ผึ้ง (ไม่มีขั้ว) ในเฮกเซน (ไม่มีขั้ว)", True),
    SolubilityItem("เกลือแกง (มีขั้ว) ในเฮกเซน (ไม่มีขั้ว)", False),
    SolubilityItem("น้ำตาลทราย (มีขั้ว) ในเฮกเซน (ไม่มีขั้ว)", False),
    SolubilityItem("ขี้ผึ้ง (ไม่มีขั้ว) ในน้ำ (มีขั้ว)", False),
)


POLAR_SOLVENT, NONPOLAR_SOLVENT = "ตัวทำละลายที่มีขั้ว (เช่น น้ำ)", "ตัวทำละลายที่ไม่มีขั้ว (เช่น เฮกเซน)"


SOLVENT_FILLERS = ("ตัวทำละลายชนิดใดก็ได้ ละลายได้เท่ากัน", "ไม่ละลายในตัวทำละลายชนิดใดเลย",
                   "ตัวทำละลายที่ร้อนจัดเท่านั้น (เช่น น้ำเดือด)", "ตัวทำละลายที่มีสีเดียวกับตัวละลาย")


LIKE_HINT = "สารมีขั้วละลายได้ดีในตัวทำละลายมีขั้ว และสารไม่มีขั้วละลายได้ดีในตัวทำละลายไม่มีขั้ว (like dissolves like)"


SOLUBILITY_RULES = (
    ("สารที่มีขั้ว (เช่น เกลือแกงหรือน้ำตาล) ละลายได้ดีในตัวทำละลายชนิดใด", POLAR_SOLVENT,
     (NONPOLAR_SOLVENT, *SOLVENT_FILLERS)),
    ("สารที่ไม่มีขั้ว (เช่น น้ำมันพืช) ละลายได้ดีในตัวทำละลายชนิดใด", NONPOLAR_SOLVENT,
     (POLAR_SOLVENT, *SOLVENT_FILLERS)),
    ("คราบน้ำมันเครื่องซึ่งไม่มีขั้วบนมือ ควรใช้ตัวทำละลายชนิดใดช่วยละลายออก", NONPOLAR_SOLVENT,
     (POLAR_SOLVENT, *SOLVENT_FILLERS)),
    ("หลัก \"like dissolves like\" หมายถึงข้อใด",
     "สารละลายได้ดีในตัวทำละลายที่มีสภาพขั้วคล้ายกัน",
     ("สารละลายได้ดีในตัวทำละลายที่มีสีคล้ายกัน", "สารทุกชนิดละลายได้ดีในน้ำ",
      "สารมีขั้วละลายได้ดีในตัวทำละลายไม่มีขั้วเท่านั้น", "สารละลายได้ดีในตัวทำละลายที่มีมวลเท่ากัน",
      "สารละลายได้ดีเมื่อมีสถานะเดียวกับตัวทำละลายเท่านั้น")),
    ("เหตุใดเกลือแกงจึงละลายในเฮกเซนได้ไม่ดี",
     "เกลือแกงเป็นสารมีขั้ว ส่วนเฮกเซนไม่มีขั้ว แรงดึงดูดระหว่างกันจึงไม่เหมาะกับการละลาย",
     ("เพราะเฮกเซนมีขั้วมากกว่าน้ำ จึงดึงดูดไอออนของเกลือแรงเกินไปจนไม่แยกตัว", "เกลือแกงไม่มีขั้ว ส่วนเฮกเซนมีขั้ว แรงดึงดูดระหว่างกันจึงไม่เหมาะกับการละลาย", "เพราะเฮกเซนเป็นของแข็ง",
      "เพราะเกลือแกงระเหยได้ง่าย", "เพราะเฮกเซนทำปฏิกิริยากับเกลือเกิดสารใหม่ที่ตกตะกอน")),
)


SOLUBILITY_RULES += (
    ('เหตุใดน้ำมันพืชจึงไม่ละลายน้ำ แต่แยกเป็นชั้นลอยอยู่ด้านบน', 'น้ำมันพืชไม่มีขั้ว ส่วนน้ำมีขั้ว จึงละลายเข้ากันไม่ได้ และน้ำมันมีความหนาแน่นน้อยกว่า',
     ('น้ำมันพืชมีขั้วมากกว่าน้ำ จึงผลักกันจนแยกชั้นและน้ำมันลอยอยู่ด้านบนเสมอ', 'น้ำมันพืชมีความหนาแน่นมากกว่าน้ำ แต่ถูกอากาศดันให้ลอยขึ้นไปอยู่ด้านบน', 'น้ำมันพืชละลายในน้ำได้ดีแล้ว แต่ต้องคนนานหลายชั่วโมงจึงจะเห็นว่าละลาย', 'น้ำมันพืชทำปฏิกิริยากับน้ำเกิดสารใหม่ที่เป็นชั้นอยู่บนผิวน้ำ', 'น้ำและน้ำมันพืชไม่มีขั้วทั้งคู่ จึงแยกชั้นตามอุณหภูมิของของเหลว')),
    ('ไอโอดีนซึ่งเป็นสารไม่มีขั้วละลายได้ดีในตัวทำละลายชนิดใด', 'ตัวทำละลายที่ไม่มีขั้ว (เช่น เฮกเซน)',
     ('ตัวทำละลายที่มีขั้ว (เช่น น้ำ)', 'ตัวทำละลายชนิดใดก็ได้ ละลายได้เท่ากัน', 'ไม่ละลายในตัวทำละลายชนิดใดเลย', 'ตัวทำละลายที่ร้อนจัดเท่านั้น (เช่น น้ำเดือด)', 'ตัวทำละลายที่มีสีเดียวกับตัวละลาย')),
    ('เหตุใดเอทานอลจึงละลายน้ำได้ดี', 'เอทานอลมีส่วนที่มีขั้ว จึงเกิดแรงดึงดูดกับโมเลกุลน้ำที่มีขั้วได้ดี',
     ('เอทานอลไม่มีขั้วเลย จึงแทรกตัวระหว่างโมเลกุลน้ำได้ง่าย', 'เอทานอลทำปฏิกิริยากับน้ำเกิดเป็นสารใหม่ทั้งหมด', 'เอทานอลมีความหนาแน่นเท่ากับน้ำพอดี จึงผสมกันได้', 'เอทานอลเป็นของแข็งที่ละลายได้ในทุกตัวทำละลาย', 'น้ำไม่มีขั้ว จึงละลายสารทุกชนิดรวมทั้งเอทานอลได้')),
)


@question_type(
    "chem.solubility_solvent_foundation",
    display_name={"th": "สารมีขั้วละลายได้ดีในตัวทำละลายชนิดใด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_SOLUBILITY,
)
class SolubilitySolventFoundation(QuestionType):
    """The general rule — "like dissolves like" — not yet a named pair."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, correct, wrongs = rng.choice(SOLUBILITY_RULES)
        return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_SOLUBILITY, hint=LIKE_HINT)


@question_type(
    "chem.solubility_solvent_fluency",
    display_name={"th": "สารคู่ที่กำหนดละลายกันได้ดีหรือไม่"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_SOLUBILITY,
)
class SolubilitySolventFluency(QuestionType):
    """Classify one named solute/solvent pair directly — the whole indicator."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(SOLUBILITY_ITEMS)
        return _labelled(
            stem=f"{item.pair_name} ละลายกันได้ดีหรือไม่",
            correct=DISSOLVE_WHY[item.dissolves],
            wrongs=(DISSOLVE_WHY[not item.dissolves], *SOLUBILITY_FILLERS),
            topic=TOPIC_SOLUBILITY,
            hint="สารมีขั้วละลายได้ดีในตัวทำละลายมีขั้ว และสารไม่มีขั้วละลายได้ดีในตัวทำละลายไม่มีขั้ว",
        )


@question_type(
    "chem.solubility_solvent_application",
    display_name={"th": "สารคู่ในข้อใดตรงกับผลการละลายที่กำหนด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_SOLUBILITY,
)
class SolubilitySolventApplication(QuestionType):
    """Reverse direction: given the outcome, pick the matching pair."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        dissolves = rng.choice((True, False))
        same = [item for item in SOLUBILITY_ITEMS if item.dissolves == dissolves]
        other = [item for item in SOLUBILITY_ITEMS if item.dissolves != dissolves]
        correct = rng.choice(same)
        wrongs = rng.sample(other, 3)
        result = DISSOLVES if dissolves else DOES_NOT_DISSOLVE
        return _labelled(
            stem=f"สารคู่ในข้อใดต่อไปนี้{result}เมื่อผสมกัน",
            correct=correct.pair_name,
            wrongs=tuple(w.pair_name for w in wrongs),
            topic=TOPIC_SOLUBILITY,
            hint="สารมีขั้วละลายได้ดีในตัวทำละลายมีขั้ว และสารไม่มีขั้วละลายได้ดีในตัวทำละลายไม่มีขั้ว",
        )
