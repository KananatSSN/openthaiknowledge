"""รูปเรขาคณิต 3 มิติ

คณิตศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ค 2.2 ป.6/*

Sets moved here from: math, math_diagrams, math_gaps_shape_data, math_geometry.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import SOLIDS, _img, _math_q, _nums
from otk.sets._support.math_gaps_shape_data import _choices

PROVENANCE = Provenance("original")


POLYHEDRA = tuple(s for s in SOLIDS if s.faces)


_NETS = (
    ("รูปสี่เหลี่ยมจัตุรัสที่เท่ากันทุกประการ 6 รูป", "ลูกบาศก์"),
    ("รูปสี่เหลี่ยมผืนผ้า 6 รูป ที่เท่ากันทุกประการเป็นคู่ ๆ 3 คู่", "ทรงสี่เหลี่ยมมุมฉาก"),
    ("รูปสามเหลี่ยมที่เท่ากันทุกประการ 2 รูป และรูปสี่เหลี่ยมผืนผ้า 3 รูป", "ปริซึมสามเหลี่ยม"),
    ("รูปวงกลมที่เท่ากันทุกประการ 2 รูป และรูปสี่เหลี่ยมผืนผ้า 1 รูป", "ทรงกระบอก"),
    ("รูปสี่เหลี่ยมจัตุรัส 1 รูป และรูปสามเหลี่ยมที่เท่ากันทุกประการ 4 รูป", "พีระมิดฐานสี่เหลี่ยม"),
    ("รูปสามเหลี่ยมที่เท่ากันทุกประการ 4 รูป", "พีระมิดฐานสามเหลี่ยม"),
    ("รูปวงกลม 1 รูป และรูปส่วนหนึ่งของวงกลมที่เป็นรูปพัด 1 รูป", "กรวย"),
)


_SOLIDS = [("ลูกบาศก์", 6, 12, 8), ("ทรงสี่เหลี่ยมมุมฉาก", 6, 12, 8),
           ("พีระมิดฐานสี่เหลี่ยม", 5, 8, 5), ("พีระมิดฐานสามเหลี่ยม", 4, 6, 4),
           ("ปริซึมสามเหลี่ยม", 5, 9, 6), ("ปริซึมห้าเหลี่ยม", 7, 15, 10)]


@question_type("math.solid_counts_picture_p6",
               display_name={"th": "นับหน้า สัน และจุดยอดของรูปเรขาคณิตสามมิติจากรูป"},
               level={"th": "ป.6"}, topic="รูปเรขาคณิต 3 มิติ")
class SolidCountsPictureP6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(POLYHEDRA)
        what, ans = rng.choice((("หน้า", s.faces), ("สัน", s.edges), ("จุดยอด", s.vertices)))
        # The other two counts are the tempting mix-ups.
        wrongs = _nums(*(v for v in (s.faces, s.edges, s.vertices) if v != ans), ans + 1, ans - 1,
                       answer=ans, lo=1)
        return _math_q([text(f"รูปเรขาคณิตสามมิติในรูปมีกี่{what}"),
                        _img(s.asset_id, "รูปเรขาคณิตสามมิติที่มีหน้าเป็นรูปหลายเหลี่ยม เส้นประแสดงสันที่ถูกบัง")],
                       str(ans), wrongs, self.topic)


@question_type("math.solid_faces_edges_vertices",
               display_name={"th": "นับหน้า/ขอบ/จุดยอดของรูปทรง"}, level={"th": "ป.6"},
               topic="รูปเรขาคณิต 3 มิติ")
class SolidFacesEdgesVertices(WordProblem):
    # (faces, edges, vertices)
    _SOLIDS = {"ลูกบาศก์": (6, 12, 8),
               "ปริซึมสามเหลี่ยม": (5, 9, 6),
               "พีระมิดฐานสี่เหลี่ยม": (5, 8, 5)}
    _ASK = {"หน้า": 0, "ขอบ": 1, "จุดยอด": 2}

    def expr(self, rng: Random):
        solid = rng.choice(list(self._SOLIDS))
        ask = rng.choice(list(self._ASK))
        counts = self._SOLIDS[solid]
        ans = counts[self._ASK[ask]]
        others = [str(c) for i, c in enumerate(counts) if i != self._ASK[ask]]
        return MathDraw("", str(ans),
                        prompt=f"{solid}มีจำนวน{ask}เท่าใด?",
                        distractors=others + [str(ans + 1)])


@question_type("math.net_to_solid_p6", display_name={"th": "รูปคลี่ของรูปเรขาคณิตสามมิติ"},
               level={"th": "ป.6"}, topic="รูปเรขาคณิต 3 มิติ")
class NetToSolidP6(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        parts, solid = rng.choice(_NETS)
        if rng.random() < 0.5:
            return _choices([text(f"รูปคลี่ที่ประกอบด้วย{parts} เมื่อพับแล้วจะได้รูปเรขาคณิตสามมิติใด")],
                            solid, [s for _, s in _NETS if s != solid], self.topic)
        return _choices([text(f"รูปคลี่ของ{solid}ประกอบด้วยรูปใดบ้าง")],
                        parts, [p for p, s in _NETS if s != solid], self.topic)


@question_type("math.euler_formula", display_name={"th": "สูตรของออยเลอร์ (หน้า+จุดยอด−ขอบ)"},
               level={"th": "ป.6"}, topic="รูปเรขาคณิต 3 มิติ")
class EulerFormula(WordProblem):
    def expr(self, rng: Random):
        name, faces, edges, vertices = rng.choice(_SOLIDS)
        which = rng.choice(["edges", "vertices", "faces"])
        # Thai counters differ per feature: ขอบ counts in เส้น, จุดยอด in จุด.
        asked, counter, value = {
            "edges": ("ขอบ", "เส้น", edges),
            "vertices": ("จุดยอด", "จุด", vertices),
            "faces": ("หน้า", "หน้า", faces),
        }[which]
        others = {"edges": (faces, vertices), "vertices": (faces, edges),
                  "faces": (edges, vertices)}[which]
        return MathDraw(
            "", str(value),
            prompt=f"{name}มี{asked}กี่{counter}",
            distractors=[str(others[0]), str(others[1]), str(value + 2)])
