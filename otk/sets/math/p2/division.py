"""การหาร

คณิตศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.2/*

Sets moved here from: math_p2, math_pictures_p2.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_p2 import _LEGS, LEVEL
from otk.sets._support.math_pictures import BY_KEY, _img, _near
from otk.sets._support.math_pictures_p2 import GROUPS, P2

PROVENANCE = Provenance("original")


def _division_story(rng: Random, total: int, per: int, share: bool) -> str:
    p = rng.choice(_story.NAMES)
    t = rng.choice(_story.THINGS)
    if share:
        return rng.choice((
            f"แบ่ง{t.noun} {total} {t.cl} ให้เด็ก {per} คน คนละเท่า ๆ กัน "
            f"เด็กแต่ละคนได้{t.noun}กี่{t.cl}",
            f"{p}มีเงิน {total} บาท แบ่งใส่กระปุกออมสิน {per} ใบ ใบละเท่า ๆ กัน "
            f"แต่ละใบมีเงินกี่บาท",
            f"ครูมีดินสอสี {total} แท่ง แจกให้นักเรียน {per} กลุ่ม กลุ่มละเท่า ๆ กัน "
            f"แต่ละกลุ่มได้ดินสอสีกี่แท่ง",
        ))
    animal, legs = rng.choice([x for x in _LEGS if x[1] == per] or [(None, 0)])
    stories = [
        f"จัด{t.noun} {total} {t.cl} ใส่ถุง ถุงละ {per} {t.cl} จะได้กี่ถุง",
        f"นักเรียน {total} คน แบ่งเป็นกลุ่ม กลุ่มละ {per} คน ได้กี่กลุ่ม",
        f"{p}มีเงิน {total} บาท ซื้อขนมชิ้นละ {per} บาท ได้กี่ชิ้น",
    ]
    if animal:
        stories.append(f"นับขา{animal}ได้ {total} ขา มี{animal}กี่ตัว")
    return rng.choice(stories)


@question_type("math.division_facts_p2",
               display_name={"th": "การหารลงตัว (ผลหารหนึ่งหลัก)"},
               level=LEVEL, topic="การหาร")
class DivisionFactsP2(MathType):
    def expr(self, rng: Random):
        b, q = rng.randint(2, 9), rng.randint(1, 9)
        a = b * q
        return MathDraw(rf"{a} \div {b}", str(q), prompt="จงหาผลหาร",
                        distractors=_story.keep(q + 1, q - 1, b, a - b, answer=q, lo=0))


@question_type("math.division_picture_p2", display_name={"th": "การหารจากภาพ"},
               level=P2, topic="การหาร")
class DivisionPictureP2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        g = rng.choice(GROUPS)
        kind = BY_KEY[g.kind]
        img = _img(g.asset_id, [g.kind])
        total = g.groups * g.size
        ask = rng.randrange(3)
        if ask == 0:
            # Sharing: how many each.
            return _math_q([text(f"แบ่ง{kind.thai} {total} {kind.unit} ใส่จาน {g.groups} ใบ "
                                 f"ใบละเท่า ๆ กัน ได้จานละกี่{kind.unit}"), img],
                           str(g.size), _near(g.size, g.groups, total - g.groups, lo=1), self.topic)
        if ask == 1:
            # Grouping: how many groups.
            return _math_q([text(f"จัด{kind.thai} {total} {kind.unit} ใส่จาน จานละ {g.size} "
                                 f"{kind.unit} ได้กี่จาน"), img],
                           str(g.groups), _near(g.groups, g.size, total - g.size, lo=1), self.topic)
        correct = f"{total} \\div {g.groups} = {g.size}"
        wrongs = [f"{total} - {g.groups} = {total - g.groups}",
                  f"{total} \\div {g.groups} = {g.size + 1}",
                  f"{g.groups} \\times {g.size} = {total + g.size}"]
        return _math_q([text(f"แบ่ง{kind.thai}ใส่จาน {g.groups} ใบ ใบละเท่า ๆ กัน "
                             "ประโยคสัญลักษณ์ใดตรงกับภาพ"), img], correct, wrongs, self.topic)


@question_type("math.division_remainder_p2",
               display_name={"th": "การหารไม่ลงตัว: ผลหารและเศษ"},
               level=LEVEL, topic="การหาร")
class DivisionRemainderP2(MathType):
    def expr(self, rng: Random):
        b = rng.randint(2, 9)
        q = rng.randint(1, 9)
        r = rng.randint(1, b - 1)
        a = b * q + r
        if rng.random() < 0.5:
            return MathDraw(rf"{a} \div {b}", str(q), prompt="ผลหารเท่ากับเท่าใด",
                            # The remainder read as the quotient; one too many.
                            distractors=_story.keep(r, q + 1, q - 1, answer=q, lo=0))
        return MathDraw(rf"{a} \div {b}", str(r), prompt="เศษเท่ากับเท่าใด",
                        distractors=_story.keep(q, b - r, r + b, r + 1, answer=r, lo=0))


@question_type("math.multiply_divide_relation_p2",
               display_name={"th": "ความสัมพันธ์ของการคูณและการหาร"},
               level=LEVEL, topic="การหาร")
class MultiplyDivideRelationP2(MathType):
    def expr(self, rng: Random):
        b, q = rng.randint(2, 9), rng.randint(2, 9)
        a = b * q
        sq = r"\square"
        kind = rng.randrange(3)
        if kind == 0:
            return MathDraw(rf"{q} \times {b} = {a} \quad\Rightarrow\quad {a} \div {b} = {sq}",
                            str(q), prompt="ใช้ความสัมพันธ์ของการคูณและการหาร หาจำนวนที่แทนใน □",
                            distractors=_story.keep(a, b, q + 1, a - b, answer=q))
        if kind == 1:
            return MathDraw(rf"{a} \div {sq} = {q}", str(b), prompt="จงหาจำนวนที่แทนใน □",
                            distractors=_story.keep(a * q if a * q <= 999 else a + q, a - q,
                                                    b + 1, q, answer=b))
        return MathDraw(rf"{sq} \div {b} = {q}", str(a), prompt="จงหาจำนวนที่แทนใน □",
                        distractors=_story.keep(q, b + q, a + b, a - b, answer=a))


@question_type("math.division_word_problem_p2",
               display_name={"th": "โจทย์ปัญหาการหาร (แบ่งเท่า ๆ กัน และจัดกลุ่ม)"},
               level=LEVEL, topic="การหาร")
class DivisionWordProblemP2(WordProblem):
    def expr(self, rng: Random):
        per, q = rng.randint(2, 9), rng.randint(2, 9)
        total = per * q
        share = rng.random() < 0.5
        return MathDraw("", str(q), prompt=_division_story(rng, total, per, share),
                        # Subtracting or multiplying instead of dividing.
                        distractors=_story.keep(total - per, total * per if total * per <= 999
                                                else q + 2, q + 1, q - 1, answer=q, lo=1))
