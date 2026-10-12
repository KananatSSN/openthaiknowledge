"""องค์ประกอบของเซลล์เคมีไฟฟ้า

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/28

Sets moved here from: science_wave_f39.
"""

from __future__ import annotations

from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f39 import (
    CHARGE,
    SUBJECT,
    UPPER_FIVE,
    diagram,
    half,
    pair,
    potentials,
)

PROVENANCE = Provenance("original")


TOPIC_CELL = "องค์ประกอบของเซลล์เคมีไฟฟ้า"


@question_type(
    "chem.electrochemical_cell_foundation",
    display_name={"th": "แอโนด แคโทด และทิศทางการเคลื่อนที่ของอิเล็กตรอน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CELL,
)
class ElectrochemicalCellFoundation(QuestionType):
    """In a galvanic cell the lower E° metal is the anode (oxidised, negative)."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        anode, cathode = pair(rng)
        stem = f"เซลล์กัลวานิกประกอบด้วยครึ่งเซลล์ {anode[0]}/{anode[1]} และ {cathode[0]}/{cathode[1]} ({potentials(anode, cathode)})"
        kind = rng.randrange(3)
        if kind == 0:
            right = f"{anode[0]} เป็นแอโนด (ขั้วลบ)"
            return _labelled(stem=f"{stem} ข้อใดถูกต้อง", correct=right,
                             wrongs=(f"{cathode[0]} เป็นแอโนด (ขั้วลบ)", f"{anode[0]} เป็นแคโทด (ขั้วบวก)",
                                     f"{anode[0]} เป็นแอโนด (ขั้วบวก)"), topic=TOPIC_CELL,
                             hint="ครึ่งเซลล์ที่ E° ต่ำกว่าเกิดออกซิเดชันเป็นแอโนด (ขั้วลบในเซลล์กัลวานิก)")
        if kind == 1:
            right = f"จาก {anode[0]} ไป {cathode[0]} ผ่านลวดตัวนำ"
            return _labelled(stem=f"{stem} อิเล็กตรอนเคลื่อนที่อย่างไร", correct=right,
                             wrongs=(f"จาก {cathode[0]} ไป {anode[0]} ผ่านลวดตัวนำ", f"จาก {anode[0]} ไป {cathode[0]} ผ่านสะพานเกลือ",
                                     "ไม่มีการเคลื่อนที่ของอิเล็กตรอน"), topic=TOPIC_CELL,
                             hint="อิเล็กตรอนออกจากแอโนดผ่านลวดไปแคโทด ส่วนสะพานเกลือให้ไอออนเคลื่อนที่")
        right = "ให้ไอออนเคลื่อนที่เพื่อรักษาสมดุลประจุในครึ่งเซลล์ทั้งสอง"
        return _labelled(stem=f"{stem} สะพานเกลือมีหน้าที่อะไร", correct=right,
                         wrongs=("ให้อิเล็กตรอนเคลื่อนที่ผ่าน", "เป็นตัวเร่งปฏิกิริยา", "เพิ่มความต่างศักย์ของเซลล์"),
                         topic=TOPIC_CELL, hint="สะพานเกลือทำให้วงจรครบโดยให้ไอออนบวกและลบเคลื่อนที่ไปยังครึ่งเซลล์")


@question_type(
    "chem.electrochemical_cell_fluency",
    display_name={"th": "ปฏิกิริยาที่แอโนดและแคโทด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CELL,
)
class ElectrochemicalCellFluency(QuestionType):
    """Oxidation at the anode, reduction at the cathode."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        anode, cathode = pair(rng)
        where = rng.choice(("แอโนด", "แคโทด"))
        right = half(anode[0], anode[1], True) if where == "แอโนด" else half(cathode[0], cathode[1], False)
        wrongs = {half(anode[0], anode[1], False), half(cathode[0], cathode[1], True),
                  half(anode[0], anode[1], True), half(cathode[0], cathode[1], False)} - {right}
        return _labelled(stem=f"เซลล์กัลวานิก {anode[0]}/{anode[1]} กับ {cathode[0]}/{cathode[1]} ({potentials(anode, cathode)}) "
                              f"ปฏิกิริยาที่{where}คือข้อใด",
                         correct=right, wrongs=tuple(sorted(wrongs)), topic=TOPIC_CELL,
                         hint="แอโนด: โลหะที่ E° ต่ำกว่าเสียอิเล็กตรอน แคโทด: ไอออนของโลหะที่ E° สูงกว่ารับอิเล็กตรอน")


@question_type(
    "chem.electrochemical_cell_application",
    display_name={"th": "แผนภาพเซลล์และปฏิกิริยารวม"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CELL,
)
class ElectrochemicalCellApplication(QuestionType):
    """Anode on the left of the double line, cathode on the right."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        anode, cathode = pair(rng)
        if rng.random() < 0.5:
            right = diagram(anode, cathode)
            wrongs = (diagram(cathode, anode), f"{anode[1]}(aq) | {anode[0]}(s) || {cathode[0]}(s) | {cathode[1]}(aq)",
                      f"{anode[0]}(s) || {anode[1]}(aq) | {cathode[1]}(aq) || {cathode[0]}(s)")
            return _labelled(stem=f"เซลล์กัลวานิกจาก {anode[0]}/{anode[1]} และ {cathode[0]}/{cathode[1]} ({potentials(anode, cathode)}) "
                                  "เขียนแผนภาพเซลล์ได้อย่างไร", correct=right, wrongs=wrongs, topic=TOPIC_CELL,
                             hint="แอโนดอยู่ซ้าย แคโทดอยู่ขวา | คั่นสถานะต่างกัน || แทนสะพานเกลือ")
        a, c = CHARGE[anode[0]], CHARGE[cathode[0]]
        k = a * c // gcd(a, c)
        n_anode, n_cathode = k // a, k // c
        lead = lambda n: "" if n == 1 else str(n)
        right = f"{lead(n_anode)}{anode[0]} + {lead(n_cathode)}{cathode[1]} → {lead(n_anode)}{anode[1]} + {lead(n_cathode)}{cathode[0]}"
        wrongs = (f"{lead(n_cathode)}{cathode[0]} + {lead(n_anode)}{anode[1]} → {lead(n_cathode)}{cathode[1]} + {lead(n_anode)}{anode[0]}",
                  f"{anode[0]} + {cathode[0]} → {anode[1]} + {cathode[1]}",
                  f"{anode[1]} + {cathode[1]} → {anode[0]} + {cathode[0]}")
        return _labelled(stem=f"เซลล์ {diagram(anode, cathode)} มีปฏิกิริยารวมตามข้อใด", correct=right, wrongs=wrongs,
                         topic=TOPIC_CELL, hint="รวมครึ่งปฏิกิริยาที่แอโนด (ซ้าย) กับแคโทด (ขวา) โดยให้อิเล็กตรอนเท่ากัน")
