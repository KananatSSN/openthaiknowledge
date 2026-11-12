"""ชนิดของรูปสี่เหลี่ยม

คณิตศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ค 2.2 ป.5/*

Sets moved here from: math, math_formats, math_gaps_shape_data, math_geometry.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem
from otk.sets._support.math_diagrams import _text_q
from otk.sets._support.math_gaps_shape_data import _ConstructionSteps

PROVENANCE = Provenance("original")


class Quad(NamedTuple):
    name: str
    thai: str
    pts: tuple[tuple[float, float], ...]
    ticks: tuple[int, ...]          # per side: 0 none, 1 or 2 tick marks
    right: tuple[int, ...]          # vertices with a right-angle mark
    parallel: tuple[int, ...]       # per side: 0 none, 1 or 2 arrow marks
    pairs: int                      # pairs of parallel sides


_QUADS = (
    Quad("square", "รูปสี่เหลี่ยมจัตุรัส", ((0, 0), (1, 0), (1, 1), (0, 1)),
         (1, 1, 1, 1), (0, 1, 2, 3), (1, 2, 1, 2), 2),
    Quad("rectangle", "รูปสี่เหลี่ยมผืนผ้า", ((0, 0), (1.6, 0), (1.6, 0.9), (0, 0.9)),
         (1, 2, 1, 2), (0, 1, 2, 3), (1, 2, 1, 2), 2),
    Quad("parallelogram", "รูปสี่เหลี่ยมด้านขนาน", ((0, 0), (1.5, 0), (1.9, 0.9), (0.4, 0.9)),
         (1, 2, 1, 2), (), (1, 2, 1, 2), 2),
    Quad("rhombus", "รูปสี่เหลี่ยมขนมเปียกปูน", ((0, 0), (1, 0), (1.5, 0.866), (0.5, 0.866)),
         (1, 1, 1, 1), (), (1, 2, 1, 2), 2),
    Quad("trapezoid", "รูปสี่เหลี่ยมคางหมู", ((0, 0), (1.8, 0), (1.3, 0.9), (0.4, 0.9)),
         (0, 0, 0, 0), (), (1, 0, 1, 0), 1),
    Quad("kite", "รูปสี่เหลี่ยมรูปว่าว", ((0, 1.1), (0.55, 0.45), (0, -0.6), (-0.55, 0.45)),
         (1, 2, 2, 1), (), (0, 0, 0, 0), 0),
)


QUADS_BY_NAME = {q.name: q for q in _QUADS}


_TURNS = (0, 20, -15)


class QuadPicture(NamedTuple):
    name: str
    turn: int

    @property
    def asset_id(self) -> str:
        return f"mquad_{self.name}_{'n' if self.turn < 0 else ''}{abs(self.turn)}"

    @property
    def quad(self) -> Quad:
        return QUADS_BY_NAME[self.name]


QUAD_PICTURES = tuple(QuadPicture(q.name, t) for q in _QUADS for t in _TURNS)


_NEAR = {"square": ("รูปสี่เหลี่ยมขนมเปียกปูน", "รูปสี่เหลี่ยมผืนผ้า"),
         "rectangle": ("รูปสี่เหลี่ยมจัตุรัส", "รูปสี่เหลี่ยมด้านขนาน"),
         "parallelogram": ("รูปสี่เหลี่ยมผืนผ้า", "รูปสี่เหลี่ยมคางหมู"),
         "rhombus": ("รูปสี่เหลี่ยมจัตุรัส", "รูปสี่เหลี่ยมรูปว่าว"),
         "trapezoid": ("รูปสี่เหลี่ยมด้านขนาน", "รูปสี่เหลี่ยมรูปว่าว"),
         "kite": ("รูปสี่เหลี่ยมขนมเปียกปูน", "รูปสี่เหลี่ยมคางหมู")}


QUAD_ALT = "รูปสี่เหลี่ยมหนึ่งรูป มีเครื่องหมายแสดงด้านที่ยาวเท่ากัน มุมฉาก และด้านที่ขนานกัน"


@question_type("math.classify_quadrilateral",
               display_name={"th": "จำแนกชนิดของรูปสี่เหลี่ยม"}, level={"th": "ป.5"},
               topic="ชนิดของรูปสี่เหลี่ยม")
class ClassifyQuadrilateral(ConceptBankType):
    ITEMS = [
        Concept("รูปสี่เหลี่ยมที่มีด้านเท่ากันทุกด้านและมีมุมฉากคือรูปใด?",
                "สี่เหลี่ยมจัตุรัส",
                ("สี่เหลี่ยมผืนผ้า", "สี่เหลี่ยมด้านขนาน", "สี่เหลี่ยมขนมเปียกปูน")),
        Concept("รูปสี่เหลี่ยมที่มีมุมฉากและด้านตรงข้ามยาวเท่ากันคือรูปใด?",
                "สี่เหลี่ยมผืนผ้า",
                ("สี่เหลี่ยมจัตุรัส", "สี่เหลี่ยมด้านขนาน", "สี่เหลี่ยมคางหมู")),
        Concept("รูปสี่เหลี่ยมที่มีด้านตรงข้ามขนานกันสองคู่คือรูปใด?",
                "สี่เหลี่ยมด้านขนาน",
                ("สี่เหลี่ยมคางหมู", "สี่เหลี่ยมจัตุรัส", "สี่เหลี่ยมรูปว่าว")),
        Concept("รูปสี่เหลี่ยมที่มีด้านเท่ากันทุกด้านแต่ไม่มีมุมฉากคือรูปใด?",
                "สี่เหลี่ยมขนมเปียกปูน",
                ("สี่เหลี่ยมจัตุรัส", "สี่เหลี่ยมผืนผ้า", "สี่เหลี่ยมคางหมู")),
        Concept("รูปสี่เหลี่ยมที่มีด้านขนานกันเพียงคู่เดียวคือรูปใด?",
                "สี่เหลี่ยมคางหมู",
                ("สี่เหลี่ยมด้านขนาน", "สี่เหลี่ยมจัตุรัส", "สี่เหลี่ยมผืนผ้า")),
    ]


@question_type("math.quadrilateral_picture_p5", display_name={"th": "บอกชนิดของรูปสี่เหลี่ยมจากรูป"},
               level={"th": "ป.5"}, topic="ชนิดของรูปสี่เหลี่ยม")
class QuadrilateralPictureP5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(QUAD_PICTURES)
        q = p.quad
        img = image(p.asset_id, alt=QUAD_ALT)
        if rng.random() < 0.65:
            others = [x.thai for x in _QUADS if x.thai not in (q.thai, *_NEAR[q.name])]
            rng.shuffle(others)
            return _text_q([text("รูปสี่เหลี่ยมนี้เป็นรูปสี่เหลี่ยมชนิดใด (ดูจากเครื่องหมายในรูป)"), img],
                           q.thai, [*_NEAR[q.name], *others], self.topic)
        # Counting sides rather than pairs gives 4.
        return _text_q([text("รูปสี่เหลี่ยมนี้มีด้านที่ขนานกันกี่คู่ (ดูจากเครื่องหมายลูกศร)"), img],
                       f"{q.pairs} คู่", [f"{n} คู่" for n in (0, 1, 2, 4) if n != q.pairs],
                       self.topic)


@question_type("math.construct_quadrilateral_p5", display_name={"th": "ขั้นตอนการสร้างรูปสี่เหลี่ยมชนิดต่าง ๆ"},
               level={"th": "ป.5"}, topic="ชนิดของรูปสี่เหลี่ยม")
class ConstructQuadrilateralP5(_ConstructionSteps):
    def procedures(self, rng):
        if rng.random() < 0.5:
            a, b, t = rng.randint(5, 9), rng.randint(3, 6), rng.choice((50, 60, 70, 110, 120))
            goal = (f"การสร้างรูปสี่เหลี่ยมด้านขนาน ABCD ที่มี AB ยาว {a} เซนติเมตร "
                    f"AD ยาว {b} เซนติเมตร และมุม DAB ขนาด {t} องศา")
            steps = [
                f"ลากส่วนของเส้นตรง AB ยาว {a} เซนติเมตร",
                f"ที่จุด A ใช้โพรแทรกเตอร์สร้างมุมขนาด {t} องศา",
                f"บนแขนของมุมที่สร้าง วัดจากจุด A ยาว {b} เซนติเมตร ได้จุด D",
                f"ที่จุด D ลากส่วนของเส้นตรงขนานกับ AB ยาว {a} เซนติเมตร ได้จุด C",
                "ลากส่วนของเส้นตรง BC",
            ]
            faulty = [f"ที่จุด D สร้างมุมฉาก แล้ววัดยาว {a} เซนติเมตร ได้จุด C",
                      f"ที่จุด B สร้างมุมขนาด {t} องศา ในทิศทางตรงข้ามกับมุมที่จุด A"]
            return goal, steps, faulty
        p, q = rng.choice((6, 8, 10)), rng.choice((4, 6))
        goal = (f"การสร้างรูปสี่เหลี่ยมขนมเปียกปูน ABCD ที่มีเส้นทแยงมุม AC ยาว {p} เซนติเมตร "
                f"และ BD ยาว {q} เซนติเมตร")
        steps = [
            f"ลากส่วนของเส้นตรง AC ยาว {p} เซนติเมตร",
            f"หาจุดกึ่งกลาง O ของ AC ซึ่งห่างจาก A เป็นระยะ {p // 2} เซนติเมตร",
            "ที่จุด O สร้างเส้นตรงที่ตั้งฉากกับ AC",
            f"บนเส้นที่ตั้งฉาก วัดจากจุด O ไปทั้งสองข้าง ข้างละ {q // 2} เซนติเมตร ได้จุด B และจุด D",
            "ลากส่วนของเส้นตรง AB, BC, CD และ DA",
        ]
        faulty = [f"ที่จุด A สร้างเส้นตรงที่ตั้งฉากกับ AC แล้ววัดยาว {q} เซนติเมตร",
                  f"บนเส้นที่ตั้งฉาก วัดจากจุด O ไปข้างเดียวยาว {q} เซนติเมตร"]
        return goal, steps, faulty


@question_type("math.parallelogram_properties",
               display_name={"th": "สมบัติของรูปสี่เหลี่ยมด้านขนาน"},
               level={"th": "ป.5"}, topic="ชนิดของรูปสี่เหลี่ยม")
class ParallelogramProperties(ChoiceType):
    ITEMS = [
        ("รูปสี่เหลี่ยมใดมีด้านทุกด้านยาวเท่ากันและมีมุมทุกมุมเป็นมุมฉาก",
         "รูปสี่เหลี่ยมจัตุรัส",
         ["รูปสี่เหลี่ยมผืนผ้า", "รูปสี่เหลี่ยมขนมเปียกปูน",
          "รูปสี่เหลี่ยมคางหมู"]),
        ("รูปสี่เหลี่ยมใดมีด้านขนานกันเพียงคู่เดียว", "รูปสี่เหลี่ยมคางหมู",
         ["รูปสี่เหลี่ยมด้านขนาน", "รูปสี่เหลี่ยมจัตุรัส",
          "รูปสี่เหลี่ยมผืนผ้า"]),
        ("รูปสี่เหลี่ยมใดมีด้านทุกด้านยาวเท่ากัน แต่มุมไม่จำเป็นต้องเป็นมุมฉาก",
         "รูปสี่เหลี่ยมขนมเปียกปูน",
         ["รูปสี่เหลี่ยมผืนผ้า", "รูปสี่เหลี่ยมคางหมู",
          "รูปสี่เหลี่ยมด้านขนาน"]),
        ("รูปสี่เหลี่ยมใดมีมุมทุกมุมเป็นมุมฉาก แต่ด้านที่อยู่ติดกันไม่จำเป็นต้องยาวเท่ากัน",
         "รูปสี่เหลี่ยมผืนผ้า",
         ["รูปสี่เหลี่ยมจัตุรัส", "รูปสี่เหลี่ยมขนมเปียกปูน",
          "รูปสี่เหลี่ยมคางหมู"]),
        ("รูปสี่เหลี่ยมใดมีด้านตรงข้ามขนานกันสองคู่ และยาวเท่ากันสองคู่ แต่มุมไม่จำเป็นต้องเป็นมุมฉาก",
         "รูปสี่เหลี่ยมด้านขนาน",
         ["รูปสี่เหลี่ยมคางหมู", "รูปสี่เหลี่ยมรูปว่าว", "รูปสี่เหลี่ยมจัตุรัส"]),
        ("รูปสี่เหลี่ยมใดมีด้านที่อยู่ติดกันยาวเท่ากันสองคู่ แต่ไม่มีด้านคู่ใดขนานกัน",
         "รูปสี่เหลี่ยมรูปว่าว",
         ["รูปสี่เหลี่ยมขนมเปียกปูน", "รูปสี่เหลี่ยมคางหมู", "รูปสี่เหลี่ยมด้านขนาน"]),
        ("รูปสี่เหลี่ยมใดมีเส้นทแยงมุมยาวเท่ากันและตั้งฉากกัน",
         "รูปสี่เหลี่ยมจัตุรัส",
         ["รูปสี่เหลี่ยมผืนผ้า", "รูปสี่เหลี่ยมขนมเปียกปูน", "รูปสี่เหลี่ยมด้านขนาน"]),
        ("รูปสี่เหลี่ยมใดมีเส้นทแยงมุมยาวเท่ากันและแบ่งครึ่งซึ่งกันและกัน แต่ไม่ตั้งฉากกัน",
         "รูปสี่เหลี่ยมผืนผ้า",
         ["รูปสี่เหลี่ยมจัตุรัส", "รูปสี่เหลี่ยมขนมเปียกปูน", "รูปสี่เหลี่ยมรูปว่าว"]),
        ("รูปสี่เหลี่ยมใดมีเส้นทแยงมุมตั้งฉากกันและแบ่งครึ่งซึ่งกันและกัน แต่ยาวไม่เท่ากัน",
         "รูปสี่เหลี่ยมขนมเปียกปูน",
         ["รูปสี่เหลี่ยมจัตุรัส", "รูปสี่เหลี่ยมผืนผ้า", "รูปสี่เหลี่ยมคางหมู"]),
        ("ข้อใดเป็นจริงสำหรับรูปสี่เหลี่ยมด้านขนานทุกรูป",
         "มุมที่อยู่ตรงข้ามกันมีขนาดเท่ากัน",
         ["มุมทุกมุมเป็นมุมฉาก", "ด้านทุกด้านยาวเท่ากัน", "เส้นทแยงมุมตั้งฉากกัน"]),
        ("ข้อใดเป็นจริงสำหรับรูปสี่เหลี่ยมคางหมูทุกรูป",
         "มีด้านขนานกันหนึ่งคู่",
         ["มีมุมฉากอย่างน้อยหนึ่งมุม", "เส้นทแยงมุมยาวเท่ากัน", "ด้านที่ไม่ขนานกันยาวเท่ากัน"]),
        ("รูปสี่เหลี่ยมจัตุรัสเป็นรูปสี่เหลี่ยมชนิดใดด้วย",
         "เป็นทั้งรูปสี่เหลี่ยมผืนผ้าและรูปสี่เหลี่ยมขนมเปียกปูน",
         ["เป็นรูปสี่เหลี่ยมผืนผ้าเท่านั้น", "เป็นรูปสี่เหลี่ยมขนมเปียกปูนเท่านั้น",
          "ไม่เป็นรูปสี่เหลี่ยมด้านขนาน"]),
    ]

    def compose(self, rng: Random):
        return rng.choice(self.ITEMS)


@question_type("math.quadrilateral_angle",
               display_name={"th": "มุมที่หายไปของรูปสี่เหลี่ยม"},
               level={"th": "ป.5"}, topic="ชนิดของรูปสี่เหลี่ยม")
class QuadrilateralAngle(WordProblem):
    def expr(self, rng: Random, lo: int = 40, hi: int = 140):
        a, b, c = (rng.randint(lo, hi) for _ in range(3))
        d = 360 - (a + b + c)
        if not 10 <= d <= 200:                    # keep the figure possible
            a, b, c = 90, 80, 100
            d = 90
        prompt = rng.choice((
            f"รูปสี่เหลี่ยมรูปหนึ่งมีมุมสามมุมขนาด {a}, {b} และ {c} องศา มุมที่เหลือมีขนาดกี่องศา",
            f"รูปสี่เหลี่ยม ABCD มี ∠A = {a}°, ∠B = {b}° และ ∠C = {c}° จงหาขนาดของ ∠D (องศา)",
            f"แปลงผักรูปสี่เหลี่ยมแปลงหนึ่งมีมุมสามมุมขนาด {a}, {b} และ {c} องศา "
            f"มุมที่สี่ของแปลงผักมีขนาดกี่องศา",
        ))
        return MathDraw(
            "", str(d), prompt=prompt,
            distractors=[str(180 - (a + b + c) % 180), str(a + b + c),
                         str(360 - a - b)])


from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit import story as _story  # noqa: E402
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


# ── More types of quadrilaterals (2026-11): shapes from their diagonals, angles of a parallelogram and a
# trapezoid, a missing side from the perimeter, and a diagonal's length ──


@question_type("math.quadrilateral_diagonals_p5", display_name={"th": "บอกชนิดของรูปสี่เหลี่ยมจากเส้นทแยงมุม"},
               level=LEVEL, topic="ชนิดของรูปสี่เหลี่ยม")
class QuadrilateralDiagonalsP5(ConceptBankType):
    _ALL = ("รูปสี่เหลี่ยมจัตุรัส", "รูปสี่เหลี่ยมผืนผ้า", "รูปสี่เหลี่ยมขนมเปียกปูน", "รูปว่าว",
            "รูปสี่เหลี่ยมด้านขนาน")
    ITEMS = [
        Concept("รูปสี่เหลี่ยมใดมีเส้นทแยงมุมยาวเท่ากัน ตั้งฉากกัน และแบ่งครึ่งซึ่งกันและกัน",
                "รูปสี่เหลี่ยมจัตุรัส", ("รูปสี่เหลี่ยมผืนผ้า", "รูปว่าว", "รูปสี่เหลี่ยมด้านขนาน")),
        Concept("รูปสี่เหลี่ยมใดมีเส้นทแยงมุมยาวเท่ากันและแบ่งครึ่งซึ่งกันและกัน แต่ไม่ตั้งฉากกัน",
                "รูปสี่เหลี่ยมผืนผ้า", ("รูปสี่เหลี่ยมขนมเปียกปูน", "รูปว่าว", "รูปสี่เหลี่ยมจัตุรัส")),
        Concept("รูปสี่เหลี่ยมใดมีเส้นทแยงมุมตั้งฉากและแบ่งครึ่งซึ่งกันและกัน แต่ยาวไม่เท่ากัน",
                "รูปสี่เหลี่ยมขนมเปียกปูน", ("รูปสี่เหลี่ยมผืนผ้า", "รูปสี่เหลี่ยมจัตุรัส", "รูปสี่เหลี่ยมด้านขนาน")),
        Concept("รูปสี่เหลี่ยมใดมีเส้นทแยงมุมตั้งฉากกัน และมีเพียงเส้นเดียวที่แบ่งครึ่งอีกเส้น",
                "รูปว่าว", ("รูปสี่เหลี่ยมขนมเปียกปูน", "รูปสี่เหลี่ยมผืนผ้า", "รูปสี่เหลี่ยมด้านขนาน")),
        Concept("รูปสี่เหลี่ยมใดมีเส้นทแยงมุมแบ่งครึ่งซึ่งกันและกัน แต่ไม่ตั้งฉากกันและยาวไม่เท่ากัน",
                "รูปสี่เหลี่ยมด้านขนาน", ("รูปสี่เหลี่ยมผืนผ้า", "รูปว่าว", "รูปสี่เหลี่ยมจัตุรัส")),
    ]


@question_type("math.parallelogram_angle_p5", display_name={"th": "มุมของรูปสี่เหลี่ยมด้านขนาน"},
               level=LEVEL, topic="ชนิดของรูปสี่เหลี่ยม")
class ParallelogramAngleP5(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(40, 140)
        while a == 90:
            a = rng.randint(40, 140)
        opposite = rng.random() < 0.5
        right = a if opposite else 180 - a
        ask = "∠C" if opposite else "∠B"
        prompt = f"รูปสี่เหลี่ยมด้านขนาน ABCD มี ∠A = {a}° จงหาขนาดของ {ask} (องศา)"
        # The other angle; taken as adding to 360 or 90.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(180 - a if opposite else a, 360 - a, abs(90 - a), right + 10,
                                                answer=right, lo=1))


@question_type("math.trapezoid_angle_p5", display_name={"th": "มุมของรูปสี่เหลี่ยมคางหมู"},
               level=LEVEL, topic="ชนิดของรูปสี่เหลี่ยม")
class TrapezoidAngleP5(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(40, 140)
        while a == 90:
            a = rng.randint(40, 140)
        right = 180 - a
        prompt = f"รูปสี่เหลี่ยมคางหมู ABCD มี AB ขนานกับ DC และ ∠A = {a}° จงหาขนาดของ ∠D (องศา)"
        # Taken as equal; adding to 360 or 90.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(a, 360 - a, abs(90 - a), right + 10, answer=right, lo=1))


@question_type("math.quadrilateral_missing_side_p5", display_name={"th": "หาความยาวด้านจากความยาวรอบรูป"},
               level=LEVEL, topic="ชนิดของรูปสี่เหลี่ยม")
class QuadrilateralMissingSideP5(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            side = rng.randint(3, 30)
            perimeter = 4 * side
            right = side
            prompt = f"รูปสี่เหลี่ยมขนมเปียกปูนยาวรอบรูป {perimeter} เซนติเมตร ด้านแต่ละด้านยาวกี่เซนติเมตร"
            wrongs = (perimeter // 2, perimeter - side, side + 2, perimeter // 8 if perimeter % 8 == 0 else side + 4)
        else:
            a = rng.randint(3, 20)
            b = rng.randint(a + 1, 35)
            perimeter = 2 * (a + b)
            name = "รูปว่าว มีด้านสั้นคู่หนึ่ง" if kind == 1 else "รูปสี่เหลี่ยมด้านขนาน มีด้านหนึ่ง"
            right = b
            prompt = f"{name}ยาว {a} เซนติเมตร ยาวรอบรูป {perimeter} เซนติเมตร อีกด้านยาวกี่เซนติเมตร"
            wrongs = (perimeter - a, perimeter - 2 * a, a + b, (perimeter - a) // 3)
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(*wrongs, right + 1, answer=right, lo=1))


@question_type("math.diagonal_length_p5", display_name={"th": "ความยาวของเส้นทแยงมุม"},
               level=LEVEL, topic="ชนิดของรูปสี่เหลี่ยม")
class DiagonalLengthP5(WordProblem):
    def expr(self, rng: Random):
        d = rng.randint(3, 20) * 2
        half = rng.random() < 0.5
        shape = rng.choice(("รูปสี่เหลี่ยมผืนผ้า", "รูปสี่เหลี่ยมจัตุรัส"))
        if half:
            right = d // 2
            prompt = (f"{shape} ABCD มีเส้นทแยงมุม AC และ BD ตัดกันที่จุด O ถ้า AC ยาว {d} เซนติเมตร "
                      "BO ยาวกี่เซนติเมตร")
            wrongs = (d, 2 * d, d // 4 if d % 4 == 0 else d + 2)
        else:
            right = d
            prompt = f"{shape} ABCD มีเส้นทแยงมุม AC ยาว {d} เซนติเมตร เส้นทแยงมุม BD ยาวกี่เซนติเมตร"
            wrongs = (d // 2, 2 * d, d + 2)
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(*wrongs, right + 1, answer=right, lo=1))
