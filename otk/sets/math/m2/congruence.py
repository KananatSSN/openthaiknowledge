"""ความเท่ากันทุกประการ

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: ค 2.2 ม.2/*

Sets moved here from: math, math_formats_hi, math_geometry.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import _text_q

PROVENANCE = Provenance("original")


class CongruentPair(NamedTuple):
    case: str            # sss | sas | asa | aas | rhs | aaa
    variant: int

    @property
    def asset_id(self) -> str:
        return f"mcong_{self.case}_{self.variant}"


CASE_THAI = {"sss": "ด.ด.ด.", "sas": "ด.ม.ด.", "asa": "ม.ด.ม.", "aas": "ม.ม.ด.",
             "rhs": "ฉ.ด.ด.", "aaa": "สรุปไม่ได้ว่าเท่ากันทุกประการ"}


CONGRUENT_PAIRS = tuple(CongruentPair(c, v) for c in CASE_THAI for v in range(2))


CONG_ALT = "รูปสามเหลี่ยมสองรูป มีเครื่องหมายแสดงด้านและมุมที่เท่ากัน"


@question_type("math.congruence_case",
               display_name={"th": "กรณีความเท่ากันทุกประการของสามเหลี่ยม"},
               level={"th": "ม.2"}, topic="ความเท่ากันทุกประการ")
class CongruenceCase(ConceptBankType):
    ITEMS = [
        Concept("ถ้าทราบด้านสองด้านและมุมระหว่างด้าน ใช้กรณีใด?", "ด.ม.ด.",
                ("ม.ด.ม.", "ด.ด.ด.", "ม.ม.ด.")),
        Concept("ถ้าทราบมุมสองมุมและด้านระหว่างมุม ใช้กรณีใด?", "ม.ด.ม.",
                ("ด.ม.ด.", "ด.ด.ด.", "ม.ม.ด.")),
        Concept("ถ้าทราบด้านทั้งสามด้าน ใช้กรณีใด?", "ด.ด.ด.",
                ("ด.ม.ด.", "ม.ด.ม.", "ม.ม.ด.")),
        Concept("ถ้าทราบมุมสองมุมและด้านที่ไม่ใช่ด้านระหว่างมุม ใช้กรณีใด?",
                "ม.ม.ด.", ("ด.ม.ด.", "ม.ด.ม.", "ด.ด.ด.")),
    ]


@question_type("math.congruence_picture_m2", display_name={"th": "บอกกรณีความเท่ากันทุกประการจากรูป"},
               level={"th": "ม.2"}, topic="ความเท่ากันทุกประการ")
class CongruencePictureM2(QuestionType):
    _NEAR = {"sss": ("ด.ม.ด.", "ฉ.ด.ด."), "sas": ("ม.ด.ม.", "ด.ด.ด."), "asa": ("ม.ม.ด.", "ด.ม.ด."),
             "aas": ("ม.ด.ม.", "สรุปไม่ได้ว่าเท่ากันทุกประการ"), "rhs": ("ด.ม.ด.", "ด.ด.ด."),
             "aaa": ("ม.ม.ด.", "ม.ด.ม.")}

    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(CONGRUENT_PAIRS)
        right = CASE_THAI[p.case]
        others = [v for v in CASE_THAI.values() if v not in (right, *self._NEAR[p.case])]
        rng.shuffle(others)
        return _text_q([text("จากเครื่องหมายที่กำหนด รูปสามเหลี่ยมสองรูปนี้เท่ากันทุกประการ"
                             "ด้วยความสัมพันธ์แบบใด"), image(p.asset_id, alt=CONG_ALT)],
                       right, [*self._NEAR[p.case], *others], self.topic)


@question_type("math.congruent_sides", display_name={"th": "ด้านที่สมนัยกัน"},
               level={"th": "ม.2"}, topic="ความเท่ากันทุกประการ")
class CongruentSides(WordProblem):
    """Congruence transfers measurements — the point of proving it at all."""

    def expr(self, rng: Random, lo: int = 4, hi: int = 25):
        ab, bc, ca = (rng.randint(lo, hi) for _ in range(3))
        which = rng.choice([("DE", ab), ("EF", bc), ("FD", ca)])
        name, value = which
        return MathDraw(
            "", str(value),
            prompt=(f"รูปสามเหลี่ยม ABC เท่ากันทุกประการกับรูปสามเหลี่ยม DEF "
                    f"ถ้า AB = {ab}, BC = {bc} และ CA = {ca} เซนติเมตร "
                    f"แล้ว {name} ยาวกี่เซนติเมตร"),
            distractors=[str(v) for _, v in
                         [("DE", ab), ("EF", bc), ("FD", ca)] if v != value]
            + [str(ab + bc + ca)])


@question_type("math.congruent_angles", display_name={"th": "มุมที่สมนัยกัน"},
               level={"th": "ม.2"}, topic="ความเท่ากันทุกประการ")
class CongruentAngles(WordProblem):
    def expr(self, rng: Random, lo: int = 25, hi: int = 110):
        a = rng.randint(lo, hi)
        b = rng.randint(lo, max(lo + 1, 175 - a))
        c = 180 - a - b
        which = rng.choice(["D", "E", "F"])
        value = {"D": a, "E": b, "F": c}[which]
        return MathDraw(
            "", str(value),
            prompt=(f"รูปสามเหลี่ยม ABC เท่ากันทุกประการกับรูปสามเหลี่ยม DEF "
                    f"ถ้ามุม A = {a} องศา และมุม B = {b} องศา "
                    f"แล้วมุม {which} มีขนาดกี่องศา"),
            distractors=[str(v) for k, v in {"D": a, "E": b, "F": c}.items()
                         if v != value] + ["180"])
