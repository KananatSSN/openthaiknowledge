"""เส้นขนาน

คณิตศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ค 2.2 ป.5/1

Sets moved here from: math, math_diagrams_geo.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import _img, _math_q, _text_q
from otk.sets._support.math_diagrams_geo import (
    PARALLEL_FIND,
    PARALLEL_NAME,
    angle_at,
    parallel_alt,
)

PROVENANCE = Provenance("original")


# The relation between two numbered angles, as the ป.5 and ม.2 books name them.
_ALTERNATE = {frozenset(p) for p in ((3, 5), (4, 6))}


_CO_INTERIOR = {frozenset(p) for p in ((4, 5), (3, 6))}


RELATIONS = {
    "corresponding": "มุมภายนอกและมุมภายในที่อยู่ตรงข้ามบนข้างเดียวกันของเส้นตัด",
    "alternate": "มุมแย้ง",
    "co_interior": "มุมภายในที่อยู่บนข้างเดียวกันของเส้นตัด",
    "vertical": "มุมตรงข้าม",
}


def relation(i: int, j: int) -> str | None:
    if frozenset((i, j)) in _ALTERNATE:
        return "alternate"
    if frozenset((i, j)) in _CO_INTERIOR:
        return "co_interior"
    if abs(i - j) == 4:
        return "corresponding"
    if (i - 1) // 4 == (j - 1) // 4 and abs(i - j) == 2:
        return "vertical"
    return None


PARALLEL_ALT_NAMES = "เส้นตรงสองเส้นที่ขนานกันถูกตัดด้วยเส้นตัด มีมุมสองมุมกำกับด้วยตัวอักษร a และ b"


@question_type("math.parallel_pair_picture_p5", display_name={"th": "บอกชื่อคู่มุมจากรูปเส้นขนาน"},
               level={"th": "ป.5"}, topic="เส้นขนาน")
class ParallelPairPictureP5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(PARALLEL_NAME)
        (a, _), (b, _) = p.marks
        rel = relation(a, b)
        img = _img(p.asset_id, PARALLEL_ALT_NAMES)
        if rng.random() < 0.6:
            others = [v for k, v in RELATIONS.items() if k != rel]
            return _text_q([text("มุม a และมุม b ในรูปเป็นมุมคู่ใด"), img], RELATIONS[rel], others, self.topic)
        same = rel in ("corresponding", "alternate", "vertical")
        right = "มุม a และมุม b มีขนาดเท่ากัน" if same else "มุม a และมุม b รวมกันได้ 180 องศา"
        other = "มุม a และมุม b รวมกันได้ 180 องศา" if same else "มุม a และมุม b มีขนาดเท่ากัน"
        return _text_q([text("เส้นตรงสองเส้นในรูปขนานกัน ข้อใดถูกต้อง"), img], right,
                       [other, "มุม a และมุม b รวมกันได้ 90 องศา", "มุม a มีขนาดเป็นสองเท่าของมุม b"],
                       self.topic)


@question_type("math.parallel_angle_picture_p5", display_name={"th": "หาขนาดของมุมจากรูปเส้นขนาน"},
               level={"th": "ป.5"}, topic="เส้นขนาน")
class ParallelAnglePictureP5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(PARALLEL_FIND)
        (g, lab), (x, _) = p.marks
        ans = angle_at(p.theta, x)
        given = int(lab)
        # The other size at a crossing, and 90° less the given angle.
        return _math_q([text("เส้นตรงสองเส้นในรูปขนานกัน จงหาขนาดของมุม x (องศา)"),
                        _img(p.asset_id, parallel_alt(p))], str(ans),
                       [str(180 - ans), str(abs(90 - given)), str(360 - given)], self.topic)


@question_type("math.parallel_angles",
               display_name={"th": "มุมแย้ง / มุมภายในของเส้นขนาน"},
               level={"th": "ป.5"}, topic="เส้นขนาน")
class ParallelAngles(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(30, 150)
        if rng.random() < 0.5:
            rel, ans = "มุมแย้ง", a
        else:
            rel, ans = "มุมภายในบนข้างเดียวกัน", 180 - a
        prompt = rng.choice((
            f"เส้นขนานถูกตัดด้วยเส้นตัด มุมหนึ่งมีขนาด {a} องศา {rel}มีขนาดเท่าใด?",
            f"รางรถไฟสองเส้นขนานกัน มีถนนตัดผ่านรางทั้งสอง มุมหนึ่งที่ถนนทำกับรางมีขนาด {a} องศา "
            f"{rel}ของมุมนี้มีขนาดกี่องศา",
            f"เส้นบรรทัดสองเส้นบนสมุดขนานกัน ลากเส้นตรงตัดเส้นบรรทัดทั้งสอง เกิดมุมขนาด {a} องศา "
            f"{rel}ของมุมนี้มีขนาดกี่องศา",
        ))
        return MathDraw("", str(ans), prompt=prompt,
                        distractors=[str(90 - a), str(180 - a if rel == "มุมแย้ง"
                                                      else a), str(360 - a)])
