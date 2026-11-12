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


# ── More parallel lines (2026-11): corresponding angles, checking lines are parallel, co-interior angles
# from their difference, what parallel lines are, vertically opposite angles, parallels in daily life, and
# an alternate pair from its sum ──


@question_type("math.corresponding_angle_p5", display_name={"th": "มุมภายนอกและมุมภายในที่อยู่ตรงข้ามบนข้างเดียวกันของเส้นตัด"},
               level=LEVEL, topic="เส้นขนาน")
class CorrespondingAngleP5(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(35, 145)
        while a == 90:
            a = rng.randint(35, 145)
        prompt = (f"เส้นตรงสองเส้นขนานกัน มีเส้นตัดผ่าน มุมภายนอกมุมหนึ่งมีขนาด {a} องศา "
                  "มุมภายในที่อยู่ตรงข้ามบนข้างเดียวกันของเส้นตัดมีขนาดกี่องศา")
        # Taken as adding to a straight angle or a right angle; doubled.
        return MathDraw("", str(a), prompt=prompt,
                        distractors=_story.keep(180 - a, abs(90 - a), 360 - a, a + 10, answer=a, lo=1))


@question_type("math.is_parallel_check_p5", display_name={"th": "ตรวจสอบว่าเส้นตรงสองเส้นขนานกันหรือไม่"},
               level=LEVEL, topic="เส้นขนาน")
class IsParallelCheckP5(ChoiceType):
    def compose(self, rng: Random):
        a = rng.randint(40, 140)
        while a == 90:
            a = rng.randint(40, 140)
        parallel = rng.random() < 0.5
        b = 180 - a if parallel else 180 - a + rng.choice((-6, -4, -2, 2, 4, 6))
        stem = (f"เส้นตัดตัดเส้นตรงสองเส้น เกิดมุมภายในที่อยู่บนข้างเดียวกันของเส้นตัดขนาด {a} องศา "
                f"และ {b} องศา เส้นตรงสองเส้นนี้ขนานกันหรือไม่")
        yes = "ขนานกัน เพราะมุมทั้งสองรวมกันได้ 180 องศา"
        no = f"ไม่ขนานกัน เพราะมุมทั้งสองรวมกันได้ {a + b} องศา"
        if parallel:
            return stem, yes, ["ไม่ขนานกัน เพราะมุมทั้งสองมีขนาดไม่เท่ากัน", "ขนานกัน เพราะมุมทั้งสองเป็นมุมแหลม",
                               "บอกไม่ได้ เพราะไม่รู้ความยาวของเส้นตรง"]
        return stem, no, [f"ขนานกัน เพราะมุมทั้งสองรวมกันได้ {a + b} องศา", "ขนานกัน เพราะมุมทั้งสองเป็นมุมแหลม",
                          "บอกไม่ได้ เพราะไม่รู้ความยาวของเส้นตรง"]


@question_type("math.co_interior_from_difference_p5", display_name={"th": "หามุมภายในบนข้างเดียวกันจากผลต่าง"},
               level=LEVEL, topic="เส้นขนาน")
class CoInteriorFromDifferenceP5(WordProblem):
    def expr(self, rng: Random):
        small = rng.randint(30, 85)
        diff = 180 - 2 * small
        big = small + diff
        ask_big = rng.random() < 0.5
        right = big if ask_big else small
        prompt = (f"เส้นตรงสองเส้นขนานกัน มีเส้นตัดผ่าน มุมภายในที่อยู่บนข้างเดียวกันของเส้นตัดคู่หนึ่ง "
                  f"มุมหนึ่งใหญ่กว่าอีกมุม {diff} องศา มุม{'ใหญ่' if ask_big else 'เล็ก'}มีขนาดกี่องศา")
        # The other angle; the sum treated as 90 or 360.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(small if ask_big else big, (90 + diff) // 2 if ask_big else (90 - diff) // 2,
                                                (360 + diff) // 2 if ask_big else (360 - diff) // 2, right + 10,
                                                answer=right, lo=1))


@question_type("math.parallel_concepts_p5", display_name={"th": "สมบัติของเส้นขนาน"},
               level=LEVEL, topic="เส้นขนาน")
class ParallelConceptsP5(ConceptBankType):
    ITEMS = [
        Concept("เส้นตรงสองเส้นที่ขนานกันมีลักษณะอย่างไร", "อยู่บนระนาบเดียวกันและไม่ตัดกัน",
                ("ตัดกันเป็นมุมฉาก", "ตัดกันที่จุดเดียว", "ยาวเท่ากันเสมอ")),
        Concept("ระยะห่างระหว่างเส้นขนานสองเส้นเป็นอย่างไร", "เท่ากันทุกตำแหน่ง",
                ("กว้างขึ้นเรื่อย ๆ", "แคบลงเรื่อย ๆ", "ไม่แน่นอน")),
        Concept("สัญลักษณ์ใดใช้แทนคำว่า ขนานกับ", "∥", ("⊥", "∠", "≅")),
        Concept("ถ้าเส้นตรงเส้นหนึ่งตั้งฉากกับเส้นขนานเส้นหนึ่ง จะตั้งฉากกับเส้นขนานอีกเส้นหรือไม่",
                "ตั้งฉากด้วย", ("ไม่ตั้งฉาก", "ขนานกับอีกเส้น", "บอกไม่ได้")),
        Concept("เส้นตัดตัดเส้นขนานสองเส้น มุมแย้งมีขนาดเป็นอย่างไร", "เท่ากัน",
                ("รวมกันได้ 180 องศา", "รวมกันได้ 90 องศา", "ต่างกัน 90 องศา")),
    ]


@question_type("math.vertical_angle_p5", display_name={"th": "มุมตรงข้ามและมุมประชิดเมื่อเส้นตรงตัดกัน"},
               level=LEVEL, topic="เส้นขนาน")
class VerticalAngleP5(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(25, 155)
        while a == 90:
            a = rng.randint(25, 155)
        opposite = rng.random() < 0.5
        right = a if opposite else 180 - a
        ask = "มุมที่อยู่ตรงข้ามกับมุมนี้" if opposite else "มุมที่อยู่ข้างกันบนเส้นตรงเดียวกัน"
        prompt = f"เส้นตรงสองเส้นตัดกัน เกิดมุมหนึ่งขนาด {a} องศา {ask}มีขนาดกี่องศา"
        # The other kind of angle; taken as adding to a right angle or a full turn.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(180 - a if opposite else a, abs(90 - a), 360 - a, right + 10,
                                                answer=right, lo=1))


@question_type("math.parallel_daily_life_p5", display_name={"th": "เส้นขนานในชีวิตประจำวัน"},
               level=LEVEL, topic="เส้นขนาน")
class ParallelDailyLifeP5(ConceptBankType):
    ITEMS = [
        Concept("ข้อใดเป็นตัวอย่างของเส้นขนาน", "รางรถไฟสองข้าง",
                ("ใบกรรไกรที่กางออก", "เข็มนาฬิกาตอน 3 นาฬิกา", "ทางแยกรูปตัววาย")),
        Concept("ขอบคู่ใดของกระดานดำเป็นเส้นขนาน", "ขอบบนและขอบล่างของกระดานดำ",
                ("ขอบบนและขอบข้างของกระดานดำ", "เข็มนาฬิกาตอน 9 นาฬิกา", "ขาของตัวอักษร A")),
        Concept("ข้อใดเป็นตัวอย่างของเส้นตั้งฉาก ไม่ใช่เส้นขนาน", "ขอบพื้นกับขอบผนังที่ชนกัน",
                ("เส้นบรรทัดในสมุด", "รางรถไฟสองข้าง", "สายไฟที่ขึงคู่กัน")),
        Concept("ข้อใดไม่ใช่ตัวอย่างของเส้นขนาน", "ถนนสองสายที่ตัดกันที่สี่แยก",
                ("เส้นบรรทัดในสมุด", "ขั้นบันได", "สายไฟที่ขึงคู่กัน")),
    ]


@question_type("math.alternate_from_sum_p5", display_name={"th": "หามุมแย้งจากผลบวก"},
               level=LEVEL, topic="เส้นขนาน")
class AlternateFromSumP5(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(20, 85)
        total = 2 * a
        prompt = (f"เส้นตรงสองเส้นขนานกัน มีเส้นตัดผ่าน มุมแย้งคู่หนึ่งรวมกันได้ {total} องศา "
                  "แต่ละมุมมีขนาดกี่องศา")
        # The sum itself; what is left of a straight angle; half of that.
        return MathDraw("", str(a), prompt=prompt,
                        distractors=_story.keep(total, 180 - total, 180 - a, a + 10, answer=a, lo=1))
