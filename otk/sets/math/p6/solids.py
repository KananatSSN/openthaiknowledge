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

from fractions import Fraction  # noqa: E402

from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit import story as _story  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import WordProblem  # noqa: E402
from otk.sets._support.math_p4 import as_mixed  # noqa: E402
from otk.sets._support.math_p6 import LEVEL  # noqa: E402


def _g6(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk6(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g6(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _d6(value: int, places: int) -> str:
    """An integer count of 10**-places as a decimal, trailing zeros dropped: (2350, 3) -> 2.35."""
    sign = "-" if value < 0 else ""
    whole, frac = divmod(abs(value), 10 ** places)
    digits = str(frac).rjust(places, "0").rstrip("0") if places else ""
    return f"{sign}{whole}.{digits}" if digits else f"{sign}{whole}"


def _dk6(*values: int, answer: int, places: int, lo: int = 0) -> list[str]:
    """``story.keep`` for decimals held as integer counts of 10**-places."""
    return [_d6(int(v), places) for v in _story.keep(*values, answer=answer, lo=lo)]


def _fk6(*values: Fraction, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer and non-positive values left out."""
    out: list[str] = []
    for v in values:
        if v > 0 and v != answer and as_mixed(v) not in out:
            out.append(as_mixed(v))
    return out


# ── More solids (2026-11): a solid from its description, pyramid counts, curved surfaces, Euler's rule with
# one count missing, objects as solids, and cross-sections ──

_PYRAMIDS6 = ((3, "สามเหลี่ยม"), (4, "สี่เหลี่ยม"), (5, "ห้าเหลี่ยม"), (6, "หกเหลี่ยม"), (8, "แปดเหลี่ยม"))


@question_type("math.solid_from_description_p6", display_name={"th": "บอกชื่อรูปเรขาคณิตสามมิติจากลักษณะ"},
               level=LEVEL, topic="รูปเรขาคณิต 3 มิติ")
class SolidFromDescriptionP6(ConceptBankType):
    ITEMS = [
        Concept("รูปเรขาคณิตสามมิติใดมีฐานเป็นวงกลมหนึ่งฐาน และมีจุดยอดหนึ่งจุด", "กรวย",
                ("ทรงกระบอก", "ทรงกลม", "พีระมิดฐานสี่เหลี่ยม")),
        Concept("รูปเรขาคณิตสามมิติใดมีฐานเป็นวงกลมสองฐานที่เท่ากันและขนานกัน", "ทรงกระบอก",
                ("กรวย", "ทรงกลม", "ปริซึมสี่เหลี่ยม")),
        Concept("รูปเรขาคณิตสามมิติใดทุกจุดบนผิวอยู่ห่างจากจุดศูนย์กลางเท่ากัน", "ทรงกลม",
                ("ทรงกระบอก", "กรวย", "ลูกบาศก์")),
        Concept("รูปเรขาคณิตสามมิติใดมีหน้าทุกหน้าเป็นรูปสี่เหลี่ยมจัตุรัสที่เท่ากัน", "ลูกบาศก์",
                ("ทรงสี่เหลี่ยมมุมฉาก", "พีระมิดฐานสี่เหลี่ยม", "ปริซึมสามเหลี่ยม")),
        Concept("รูปเรขาคณิตสามมิติใดมีฐานเป็นรูปหลายเหลี่ยมหนึ่งฐาน และหน้าข้างเป็นรูปสามเหลี่ยมที่มีจุดยอดร่วมกัน",
                "พีระมิด", ("ปริซึม", "ทรงกระบอก", "กรวย")),
    ]


@question_type("math.pyramid_counts_p6", display_name={"th": "จำนวนหน้า สัน และจุดยอดของพีระมิด"},
               level=LEVEL, topic="รูปเรขาคณิต 3 มิติ")
class PyramidCountsP6(WordProblem):
    def expr(self, rng: Random):
        n, name = rng.choice(_PYRAMIDS6)
        kind = rng.randrange(3)
        counts = {"หน้า": n + 1, "สัน": 2 * n, "จุดยอด": n + 1}
        what = ("หน้า", "สัน", "จุดยอด")[kind]
        right = counts[what]
        prompt = f"พีระมิดฐาน{name}มี{what}ทั้งหมดกี่{what if what != 'จุดยอด' else 'จุด'}"
        # The prism's count; the base's sides; the other counts.
        prism = {"หน้า": n + 2, "สัน": 3 * n, "จุดยอด": 2 * n}[what]
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(prism, n, 2 * n if what != "สัน" else n + 1, right + 1,
                                                answer=right, lo=1))


@question_type("math.curved_surface_p6", display_name={"th": "รูปเรขาคณิตสามมิติที่มีผิวโค้ง"},
               level=LEVEL, topic="รูปเรขาคณิต 3 มิติ")
class CurvedSurfaceP6(ConceptBankType):
    ITEMS = [
        Concept("รูปเรขาคณิตสามมิติใดมีผิวโค้งเพียงอย่างเดียว ไม่มีหน้าเรียบ", "ทรงกลม",
                ("ทรงกระบอก", "กรวย", "ลูกบาศก์")),
        Concept("รูปเรขาคณิตสามมิติใดไม่มีผิวโค้งเลย", "ปริซึมสามเหลี่ยม", ("ทรงกระบอก", "กรวย", "ทรงกลม")),
        Concept("ทรงกระบอกมีหน้าเรียบกี่หน้า", "2 หน้า", ("1 หน้า", "3 หน้า", "ไม่มีหน้าเรียบ")),
        Concept("กรวยมีหน้าเรียบกี่หน้า", "1 หน้า", ("2 หน้า", "ไม่มีหน้าเรียบ", "3 หน้า")),
    ]


@question_type("math.euler_missing_count_p6", display_name={"th": "หาจำนวนที่หายไปจาก หน้า + จุดยอด − สัน = 2"},
               level=LEVEL, topic="รูปเรขาคณิต 3 มิติ")
class EulerMissingCountP6(WordProblem):
    def expr(self, rng: Random):
        n = rng.choice((3, 4, 5, 6, 7, 8, 10))
        prism = rng.random() < 0.5
        f, v, e = (n + 2, 2 * n, 3 * n) if prism else (n + 1, n + 1, 2 * n)
        ask = rng.randrange(3)
        right = (f, v, e)[ask]
        given = [f"มีหน้า {f} หน้า", f"มีจุดยอด {v} จุด", f"มีสัน {e} สัน"]
        what = ("หน้า", "จุดยอด", "สัน")[ask]
        rest = " และ".join(g for i, g in enumerate(given) if i != ask)
        prompt = f"รูปเรขาคณิตสามมิติรูปหนึ่ง{rest} จะมี{what}กี่{what if what != 'จุดยอด' else 'จุด'} (หน้า + จุดยอด − สัน = 2)"
        # Off by two the other way; the given counts added.
        others = [x for i, x in enumerate((f, v, e)) if i != ask]
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(right + 4 if ask == 2 else right - 4, right + 2 if ask != 2 else right - 2,
                                                sum(others), right + 1, answer=right, lo=1))


@question_type("math.objects_as_solids_p6", display_name={"th": "สิ่งของรอบตัวเป็นรูปเรขาคณิตสามมิติใด"},
               level=LEVEL, topic="รูปเรขาคณิต 3 มิติ")
class ObjectsAsSolidsP6(ConceptBankType):
    ITEMS = [
        Concept("ลูกฟุตบอลมีรูปร่างคล้ายรูปใด", "ทรงกลม", ("ทรงกระบอก", "กรวย", "ลูกบาศก์")),
        Concept("กระป๋องน้ำอัดลมมีรูปร่างคล้ายรูปใด", "ทรงกระบอก", ("กรวย", "ทรงกลม", "ปริซึมสี่เหลี่ยม")),
        Concept("กรวยจราจรมีรูปร่างคล้ายรูปใด", "กรวย", ("ทรงกระบอก", "พีระมิดฐานสามเหลี่ยม", "ทรงกลม")),
        Concept("ลูกเต๋ามีรูปร่างคล้ายรูปใด", "ลูกบาศก์", ("ทรงกลม", "ปริซึมสามเหลี่ยม", "พีระมิดฐานสี่เหลี่ยม")),
        Concept("พีระมิดที่ประเทศอียิปต์มีรูปร่างคล้ายรูปใด", "พีระมิดฐานสี่เหลี่ยม",
                ("ปริซึมสามเหลี่ยม", "กรวย", "พีระมิดฐานห้าเหลี่ยม")),
    ]


@question_type("math.cross_section_p6", display_name={"th": "หน้าตัดของรูปเรขาคณิตสามมิติ"},
               level=LEVEL, topic="รูปเรขาคณิต 3 มิติ")
class CrossSectionP6(ConceptBankType):
    ITEMS = [
        Concept("ตัดทรงกระบอกด้วยระนาบที่ขนานกับฐาน หน้าตัดเป็นรูปใด", "รูปวงกลม",
                ("รูปวงรี", "รูปสามเหลี่ยม", "รูปสี่เหลี่ยมผืนผ้า")),
        Concept("ตัดลูกบาศก์ด้วยระนาบที่ขนานกับหน้าหนึ่ง หน้าตัดเป็นรูปใด", "รูปสี่เหลี่ยมจัตุรัส",
                ("รูปสามเหลี่ยม", "รูปวงกลม", "รูปหกเหลี่ยม")),
        Concept("ตัดกรวยด้วยระนาบที่ขนานกับฐาน หน้าตัดเป็นรูปใด", "รูปวงกลม",
                ("รูปวงรี", "รูปสามเหลี่ยม", "รูปห้าเหลี่ยม")),
        Concept("ตัดปริซึมสามเหลี่ยมด้วยระนาบที่ขนานกับฐาน หน้าตัดเป็นรูปใด", "รูปสามเหลี่ยม",
                ("รูปวงกลม", "รูปห้าเหลี่ยม", "รูปสี่เหลี่ยมผืนผ้า")),
        Concept("ตัดทรงกลมด้วยระนาบใดก็ตาม หน้าตัดเป็นรูปใด", "รูปวงกลม",
                ("รูปวงรี", "รูปสามเหลี่ยม", "รูปหกเหลี่ยม")),
    ]
