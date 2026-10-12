"""ปริซึม

คณิตศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ค 2.2 ป.5/4

Sets moved here from: math_gaps_shape_data.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_gaps_shape_data import _choices

PROVENANCE = Provenance("original")


_PRISM_FACTS = (
    ("ฐานทั้งสองของปริซึมมีลักษณะอย่างไร",
     "เป็นรูปหลายเหลี่ยมที่เท่ากันทุกประการ และอยู่ในระนาบที่ขนานกัน",
     ("เป็นรูปหลายเหลี่ยมที่มีขนาดต่างกัน", "เป็นรูปวงกลมสองรูปที่ขนานกัน",
      "มีฐานเดียวและมียอดแหลม")),
    ("หน้าข้างของปริซึมที่ตั้งตรงเป็นรูปใด",
     "รูปสี่เหลี่ยมมุมฉาก", ("รูปสามเหลี่ยม", "รูปวงกลม", "รูปห้าเหลี่ยม")),
    ("ปริซึมมีฐานกี่ฐาน", "2 ฐาน", ("1 ฐาน", "3 ฐาน", "4 ฐาน")),
    ("รูปเรขาคณิตสามมิติใดเป็นปริซึม",
     "ทรงสี่เหลี่ยมมุมฉาก", ("พีระมิดฐานสี่เหลี่ยม", "กรวย", "ทรงกลม")),
    ("รูปเรขาคณิตสามมิติใดไม่เป็นปริซึม",
     "พีระมิดฐานสามเหลี่ยม", ("ลูกบาศก์", "ทรงสี่เหลี่ยมมุมฉาก", "ปริซึมห้าเหลี่ยม")),
    ("ความสูงของปริซึมคือระยะใด",
     "ระยะห่างระหว่างฐานทั้งสอง",
     ("ความยาวของด้านหนึ่งของฐาน", "ความยาวรอบฐาน", "ระยะจากจุดยอดถึงฐาน")),
    ("สันข้างของปริซึมที่ตั้งตรงมีลักษณะอย่างไร",
     "ขนานกันและยาวเท่ากันทุกเส้น",
     ("มาบรรจบกันที่จุดยอดจุดเดียว", "ยาวไม่เท่ากัน", "ตั้งฉากกับสันข้างเส้นอื่น")),
    ("สิ่งของใดมีรูปร่างเป็นปริซึมสามเหลี่ยม",
     "เต็นท์ทรงหน้าจั่ว", ("ลูกฟุตบอล", "กรวยจราจร", "กระป๋องนม")),
    ("สิ่งของใดมีรูปร่างเป็นปริซึมสี่เหลี่ยม",
     "กล่องนมกล่องสี่เหลี่ยม", ("ลูกปิงปอง", "หมวกงานวันเกิดทรงกรวย", "แก้วน้ำทรงกระบอก")),
)


_POLY = {3: "สามเหลี่ยม", 4: "สี่เหลี่ยม", 5: "ห้าเหลี่ยม", 6: "หกเหลี่ยม", 8: "แปดเหลี่ยม"}


@question_type("math.prism_parts_p5", display_name={"th": "ส่วนประกอบและลักษณะของปริซึม"},
               level={"th": "ป.5"}, topic="ปริซึม")
class PrismPartsP5(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            # The same two facts asked of a named prism.
            n = rng.choice(list(_POLY))
            if rng.random() < 0.5:
                others = [f"รูป{_POLY[k]}" for k in _POLY if k != n]
                rng.shuffle(others)
                return _choices([text(f"ฐานของปริซึม{_POLY[n]}เป็นรูปใด")], f"รูป{_POLY[n]}",
                                others, self.topic)
            return _choices([text(f"หน้าข้างของปริซึม{_POLY[n]}ที่ตั้งตรงเป็นรูปใด")], "รูปสี่เหลี่ยมมุมฉาก",
                            # The base's own shape first: the face confused with the base.
                            [f"รูป{_POLY[n]}" if n != 4 else "รูปห้าเหลี่ยม", "รูปสามเหลี่ยม",
                             "รูปวงกลม", "รูปห้าเหลี่ยม"], self.topic)
        ask, right, wrongs = rng.choice(_PRISM_FACTS)
        return _choices([text(ask)], right, list(wrongs), self.topic)


@question_type("math.prism_name_p5", display_name={"th": "ชื่อของปริซึมจากรูปฐาน"},
               level={"th": "ป.5"}, topic="ปริซึม")
class PrismNameP5(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        n = rng.choice(list(_POLY))
        others = [k for k in _POLY if k != n]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _choices([text(f"ปริซึมที่มีฐานเป็นรูป{_POLY[n]} เรียกว่าอะไร")],
                            f"ปริซึม{_POLY[n]}",
                            [f"ปริซึม{_POLY[k]}" for k in others] + [f"พีระมิดฐาน{_POLY[n]}"],
                            self.topic)
        # Counting the side faces gives the number of sides of the base.
        return _choices([text(f"ปริซึมที่มีหน้าข้าง {n} หน้า มีฐานเป็นรูปใด")],
                        f"รูป{_POLY[n]}", [f"รูป{_POLY[k]}" for k in others], self.topic)


@question_type("math.prism_counts_p5", display_name={"th": "จำนวนหน้า สัน และจุดยอดของปริซึม"},
               level={"th": "ป.5"}, topic="ปริซึม")
class PrismCountsP5(WordProblem):
    """An n-gon prism has n + 2 faces, 3n edges and 2n vertices."""

    def expr(self, rng: Random):
        n = rng.choice(list(_POLY))
        faces, edges, verts = n + 2, 3 * n, 2 * n
        kind = rng.randrange(4)
        name = f"ปริซึม{_POLY[n]}"
        if kind == 0:
            return MathDraw("", str(faces), prompt=f"{name}มีหน้าทั้งหมดกี่หน้า",
                            distractors=_story.keep(n, n + 1, 2 * n, answer=faces, lo=1))
        if kind == 1:
            return MathDraw("", str(edges), prompt=f"{name}มีสันทั้งหมดกี่สัน",
                            distractors=_story.keep(2 * n, n + 2, 4 * n, answer=edges, lo=1))
        if kind == 2:
            return MathDraw("", str(verts), prompt=f"{name}มีจุดยอดทั้งหมดกี่จุด",
                            distractors=_story.keep(n, n + 2, 3 * n, answer=verts, lo=1))
        # Working back from the edges to the base, then on to the faces.
        return MathDraw("", str(faces), prompt=f"ปริซึมชนิดหนึ่งมีสันทั้งหมด {edges} สัน ปริซึมนี้มีหน้าทั้งหมดกี่หน้า",
                        distractors=_story.keep(n, edges // 2, edges + 2, answer=faces, lo=1))
