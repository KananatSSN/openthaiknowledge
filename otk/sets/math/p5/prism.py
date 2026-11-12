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


from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p5 import LEVEL  # noqa: E402


def _g(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _dec(value: int, places: int) -> str:
    """An integer count of 10**-places as a decimal, trailing zeros dropped: (2350, 3) -> 2.35."""
    sign = "-" if value < 0 else ""
    whole, frac = divmod(abs(value), 10 ** places)
    digits = str(frac).rjust(places, "0").rstrip("0") if places else ""
    return f"{sign}{whole}.{digits}" if digits else f"{sign}{whole}"


def _dk(*values: int, answer: int, places: int, lo: int = 0) -> list[str]:
    """``story.keep`` for decimals held as integer counts of 10**-places."""
    return [_dec(int(v), places) for v in _story.keep(*values, answer=answer, lo=lo)]


# ── More prisms (2026-11): prism or not, objects shaped as prisms, the rectangles in a net, the edges of a
# box, a cube from a wire, faces and corners together, and the base from the faces ──

_BASES = ((3, "สามเหลี่ยม"), (4, "สี่เหลี่ยม"), (5, "ห้าเหลี่ยม"), (6, "หกเหลี่ยม"), (8, "แปดเหลี่ยม"))


@question_type("math.prism_or_not_p5", display_name={"th": "รูปเรขาคณิตสามมิติใดเป็นปริซึม"},
               level=LEVEL, topic="ปริซึม")
class PrismOrNotP5(ConceptBankType):
    ITEMS = [
        Concept("รูปเรขาคณิตสามมิติใดเป็นปริซึม", "ทรงสี่เหลี่ยมมุมฉาก", ("ทรงกระบอก", "กรวย", "ทรงกลม")),
        Concept("รูปเรขาคณิตสามมิติใดไม่ใช่ปริซึม", "พีระมิดฐานสี่เหลี่ยม",
                ("ลูกบาศก์", "ปริซึมสามเหลี่ยม", "ทรงสี่เหลี่ยมมุมฉาก")),
        Concept("ทรงกระบอกเป็นปริซึมหรือไม่ เพราะเหตุใด", "ไม่เป็น เพราะฐานเป็นวงกลม ไม่ใช่รูปหลายเหลี่ยม",
                ("เป็น เพราะมีฐานสองฐาน", "เป็น เพราะฐานทั้งสองเท่ากัน", "ไม่เป็น เพราะไม่มีหน้าข้าง")),
        Concept("ลูกบาศก์เป็นปริซึมชนิดใด", "ปริซึมสี่เหลี่ยม", ("ปริซึมสามเหลี่ยม", "ปริซึมหกเหลี่ยม", "ไม่ใช่ปริซึม")),
    ]


@question_type("math.prism_objects_p5", display_name={"th": "สิ่งของที่มีรูปร่างเป็นปริซึม"},
               level=LEVEL, topic="ปริซึม")
class PrismObjectsP5(ConceptBankType):
    ITEMS = [
        Concept("เต็นท์ทรงหน้าจั่วมีรูปร่างคล้ายรูปใด", "ปริซึมสามเหลี่ยม",
                ("ปริซึมสี่เหลี่ยม", "พีระมิดฐานสามเหลี่ยม", "กรวย")),
        Concept("ดินสอที่มีหน้าตัดเป็นรูปหกเหลี่ยมมีรูปร่างคล้ายรูปใด", "ปริซึมหกเหลี่ยม",
                ("ทรงกระบอก", "ปริซึมห้าเหลี่ยม", "พีระมิดฐานหกเหลี่ยม")),
        Concept("กล่องนมมีรูปร่างคล้ายรูปใด", "ปริซึมสี่เหลี่ยม", ("ปริซึมสามเหลี่ยม", "ทรงกระบอก", "พีระมิด")),
        Concept("แท่งช็อกโกแลตที่มีหน้าตัดเป็นรูปสามเหลี่ยมมีรูปร่างคล้ายรูปใด", "ปริซึมสามเหลี่ยม",
                ("พีระมิดฐานสามเหลี่ยม", "กรวย", "ปริซึมสี่เหลี่ยม")),
    ]


@question_type("math.prism_net_rectangles_p5", display_name={"th": "รูปคลี่ของปริซึมมีรูปสี่เหลี่ยมผืนผ้ากี่รูป"},
               level=LEVEL, topic="ปริซึม")
class PrismNetRectanglesP5(WordProblem):
    def expr(self, rng: Random):
        n, name = rng.choice(_BASES)
        right = n
        prompt = f"รูปคลี่ของปริซึม{name}มีรูปสี่เหลี่ยมที่เป็นหน้าข้างกี่รูป (ไม่นับฐาน)"
        # All the faces; the corners of the prism; two bases counted in.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(n + 2, 2 * n, n - 1, 2, answer=right, lo=1))


@question_type("math.box_edges_total_p5", display_name={"th": "ความยาวรอบสันทั้งหมดของทรงสี่เหลี่ยมมุมฉาก"},
               level=LEVEL, topic="ปริซึม")
class BoxEdgesTotalP5(WordProblem):
    def expr(self, rng: Random):
        w, length, h = rng.randint(3, 20), rng.randint(3, 25), rng.randint(3, 20)
        right = 4 * (w + length + h)
        prompt = (f"กล่องทรงสี่เหลี่ยมมุมฉากกว้าง {w} ซม. ยาว {length} ซม. สูง {h} ซม. "
                  "ถ้านำลวดมาดัดตามสันทุกสัน ต้องใช้ลวดยาวกี่เซนติเมตร")
        # Each length once or twice; the volume.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(w + length + h, 2 * (w + length + h), 6 * (w + length + h),
                                                w * length * h, answer=right, lo=1))


@question_type("math.cube_from_wire_p5", display_name={"th": "ดัดลวดเป็นโครงลูกบาศก์"},
               level=LEVEL, topic="ปริซึม")
class CubeFromWireP5(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(2, 25)
        wire = 12 * a
        prompt = f"ลวดยาว {wire} เซนติเมตร ดัดเป็นโครงลูกบาศก์ได้พอดี ลูกบาศก์มีสันยาวสันละกี่เซนติเมตร"
        # Divided by the faces, the corners, or four sides of a square.
        return MathDraw("", str(a), prompt=prompt,
                        distractors=_story.keep(wire // 6, wire // 8, wire // 4, a + 1, answer=a, lo=1))


@question_type("math.prism_faces_plus_corners_p5", display_name={"th": "จำนวนหน้ารวมกับจำนวนจุดยอดของปริซึม"},
               level=LEVEL, topic="ปริซึม")
class PrismFacesPlusCornersP5(WordProblem):
    def expr(self, rng: Random):
        n, name = rng.choice(_BASES)
        faces, corners, edges = n + 2, 2 * n, 3 * n
        right = faces + corners
        prompt = f"ปริซึม{name}มีจำนวนหน้ารวมกับจำนวนจุดยอดเท่ากับเท่าใด"
        # Edges instead of corners; faces and edges; corners counted once per base.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(faces + edges, corners + edges, faces + n, right + 2,
                                                answer=right, lo=1))


@question_type("math.prism_base_from_faces_p5", display_name={"th": "บอกชนิดของปริซึมจากจำนวนหน้า"},
               level=LEVEL, topic="ปริซึม")
class PrismBaseFromFacesP5(ChoiceType):
    def compose(self, rng: Random):
        n, name = rng.choice(_BASES)
        right = f"ปริซึม{name}"
        others = [f"ปริซึม{m}" for k, m in _BASES if k != n]
        return f"ปริซึมชนิดหนึ่งมีหน้าทั้งหมด {n + 2} หน้า ปริซึมนี้คือปริซึมชนิดใด", right, rng.sample(others, 3)
