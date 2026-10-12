"""บวก ลบ คูณ หารระคน

คณิตศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.2/*

Sets moved here from: math, math_p2.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_p2 import LEVEL, _maths, evaluate, two_step_add_sub_story

PROVENANCE = Provenance("original")


def _times_then_add_story(rng: Random, a: int, b: int, c: int) -> str:
    """a groups of b, then c more: the ป.2 two-step shape."""
    p = rng.choice(_story.NAMES)
    t = rng.choice(_story.THINGS)
    goods, other = rng.sample(("สมุด", "ดินสอ", "ยางลบ", "ขนม", "นม", "ปากกา"), 2)
    stories = (
        f"{p}แบ่ง{t.noun}ใส่ถุงไว้ {a} ถุง ถุงละ {b} {t.cl} และมีที่ไม่ได้ใส่ถุงอีก "
        f"{c} {t.cl} {p}มี{t.noun}ทั้งหมดกี่{t.cl}",
        f"ห้องประชุมจัดเก้าอี้ {a} แถว แถวละ {b} ตัว และวางเก้าอี้เสริมอีก {c} ตัว "
        f"ห้องประชุมมีเก้าอี้ทั้งหมดกี่ตัว",
        f"{p}ซื้อ{goods} {a} ชิ้น ชิ้นละ {b} บาท และซื้อ{other}อีก {c} บาท "
        f"{p}จ่ายเงินทั้งหมดกี่บาท",
        f"{p}อ่านหนังสือวันละ {b} หน้า เป็นเวลา {a} วัน แล้วอ่านเพิ่มอีก {c} หน้า "
        f"{p}อ่านหนังสือได้ทั้งหมดกี่หน้า",
        f"ชาวสวนปลูกต้นมะม่วง {a} แถว แถวละ {b} ต้น และปลูกไว้ริมรั้วอีก {c} ต้น "
        f"ชาวสวนปลูกต้นมะม่วงทั้งหมดกี่ต้น",
        f"แม่ค้ามีขนมบรรจุกล่อง {a} กล่อง กล่องละ {b} ชิ้น และมีขนมที่ยังไม่บรรจุอีก {c} ชิ้น "
        f"แม่ค้ามีขนมทั้งหมดกี่ชิ้น",
    )
    return rng.choice(stories)


_MIXED_TOPIC = "บวก ลบ คูณ หารระคน"


def mixed_expression(rng: Random, hi: int = 100):
    """``(tex, value, wrongs)`` for a two-operation expression. Brackets are
    written wherever working left to right would give a different answer."""
    while True:
        a, b, c = rng.randint(2, 9), rng.randint(2, 9), rng.randint(1, 30)
        form = rng.randrange(7)
        if form == 0:
            tex, v, w = rf"{a} \times {b} + {c}", a * b + c, [a * (b + c), a + b + c]
        elif form == 1:
            tex, v, w = rf"{a} \times {b} - {c}", a * b - c, [a * (b - c), a * b + c]
        elif form == 2:
            n = a * b
            tex, v, w = rf"{n} \div {a} + {c}", b + c, [n - a + c, b * c, n + c]
        elif form == 3:
            n = a * b
            tex, v, w = rf"{n} \div {a} - {c % b + 1}", b - (c % b + 1), [n - a - (c % b + 1),
                                                                            b + (c % b + 1), b]
        elif form == 4:
            tex, v, w = rf"({c} + {a}) \times {b}", (c + a) * b, [c + a * b, c * b + a,
                                                                   c + a + b]
        elif form == 5:
            big = c + a + rng.randint(1, 9)
            tex, v, w = rf"({big} - {a}) \times {b}", (big - a) * b, [big - a * b, big * b - a,
                                                                       big - a + b]
        else:
            n = a * b
            tex, v, w = rf"({n} + {a}) \div {a}", b + 1, [n + 1, b, n // a + a]
        if 0 <= v <= hi:
            return tex, v, w


def _mixed_story(rng: Random):
    """``(story, sentence, value, wrong sentences)`` for a two-step ป.2 story."""
    p, q = _story.names(rng)
    t = rng.choice(_story.THINGS)
    a, b = rng.randint(2, 9), rng.randint(2, 9)
    kind = rng.randrange(5)
    if kind == 0:
        c = rng.randint(1, a * b - 1)
        return (f"{p}มี{t.noun} {a} ถุง ถุงละ {b} {t.cl} แบ่งให้{q}ไป {c} {t.cl} "
                f"{p}เหลือ{t.noun}กี่{t.cl}", rf"{a} \times {b} - {c}", a * b - c,
                [rf"{a} \times {b} + {c}", rf"{a} + {b} - {c}", rf"{a} \times ({b} - {c})",
                 rf"{a} + {b} + {c}", rf"{c} - {a} \times {b}"])
    if kind == 1:
        c = rng.randint(1, 40)
        price = a * b
        note = rng.choice([n for n in (20, 50, 100, 500) if n >= price])
        return (f"{p}ซื้อขนม {a} ชิ้น ชิ้นละ {b} บาท จ่ายด้วยธนบัตรใบละ {note} บาท "
                f"จะได้เงินทอนกี่บาท", rf"{note} - {a} \times {b}", note - price,
                [rf"{note} - {a} - {b}", rf"{note} - {a} + {b}", rf"{a} \times {b}",
                 rf"{note} + {a} \times {b}", rf"({note} - {a}) \times {b}"])
    if kind == 2:
        n = a * b
        c = rng.randint(1, 20)
        return (f"แบ่ง{t.noun} {n} {t.cl} ให้เด็ก {a} คน คนละเท่า ๆ กัน "
                f"แล้วแม่ให้เด็กแต่ละคนเพิ่มอีกคนละ {c} {t.cl} เด็กแต่ละคนมี{t.noun}กี่{t.cl}",
                rf"{n} \div {a} + {c}", b + c,
                [rf"{n} \div ({a} + {c})", rf"{n} - {a} + {c}", rf"{n} + {c}",
                 rf"{n} \times {a} + {c}", rf"{n} \div {a} - {c}"])
    if kind == 3:
        c = rng.randint(2, 9)
        c1, c2 = rng.sample(_story.COLOURS, 2)
        return (f"กล่องหนึ่งใส่ลูกแก้ว{c1} {a} ลูก และลูกแก้ว{c2} {b} ลูก "
                f"ถ้ามีกล่องแบบนี้ {c} กล่อง จะมีลูกแก้วทั้งหมดกี่ลูก",
                rf"({a} + {b}) \times {c}", (a + b) * c,
                [rf"{a} + {b} \times {c}", rf"{a} + {b} + {c}", rf"{a} \times {b} + {c}",
                 rf"({a} + {b}) \div {c}", rf"{a} \times {c} + {b}"])
    c = rng.randint(1, 30)
    return (f"ร้านค้ามีไข่ไก่ {a} แผง แผงละ {b * 5} ฟอง และมีไข่ที่ไม่ได้ใส่แผงอีก {c} ฟอง "
            f"ร้านค้ามีไข่ไก่ทั้งหมดกี่ฟอง", rf"{a} \times {b * 5} + {c}", a * b * 5 + c,
            [rf"{a} + {b * 5} + {c}", rf"{a} \times ({b * 5} + {c})", rf"{a} \times {b * 5} - {c}",
             rf"({a} + {c}) \times {b * 5}", rf"{a} \times {c} + {b * 5}"])


@question_type("math.mixed_ops_p2",
               display_name={"th": "การบวก ลบ คูณ หารระคน"},
               level=LEVEL, topic=_MIXED_TOPIC)
class MixedOpsP2(MathType):
    def expr(self, rng: Random, hi: int = 100):
        tex, v, wrongs = mixed_expression(rng, max(20, min(int(hi), 1000)))
        return MathDraw(tex, str(v), prompt="จงหาผลลัพธ์",
                        distractors=_story.keep(*wrongs, v + 1, v - 1, answer=v, lo=0))


@question_type("math.two_step_word_problem",
               display_name={"th": "โจทย์ปัญหา 2 ขั้นตอน (คูณแล้วบวก)"},
               level={"th": "ป.2"}, topic="บวก ลบ คูณ หารระคน")
class TwoStepWordProblem(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.randint(2, 9), rng.randint(2, 9)
        c = rng.randint(1, 50)
        ans = a * b + c
        return MathDraw(
            "", rf"{ans}",
            prompt=_times_then_add_story(rng, a, b, c),
            # Adding the three numbers, stopping after one step, then (a + b) × c.
            distractors=_story.keep(a + b + c, a * b, a * b - c, (a + b) * c, answer=ans,
                                    lo=1))


@question_type("math.mixed_ops_sentence_p2",
               display_name={"th": "เขียนประโยคสัญลักษณ์ของโจทย์ระคน"},
               level=LEVEL, topic=_MIXED_TOPIC)
class MixedOpsSentenceP2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        story, sentence, v, wrongs = _mixed_story(rng)
        # A wrong sentence that happens to give the same number would be a
        # second right answer, so only those with another value are offered.
        wrongs = [w for w in wrongs if evaluate(w) != v]
        return _maths([text(story), text("ประโยคสัญลักษณ์ใดใช้หาคำตอบของโจทย์นี้ได้")],
                      rf"{sentence} = \square", [rf"{w} = \square" for w in wrongs],
                      self.topic)


@question_type("math.mixed_ops_word_problem_p2",
               display_name={"th": "โจทย์ปัญหาการบวก ลบ คูณ หารระคน"},
               level=LEVEL, topic=_MIXED_TOPIC)
class MixedOpsWordProblemP2(WordProblem):
    def expr(self, rng: Random):
        story, _, v, wrong_sentences = _mixed_story(rng)
        # The values of the sentences a learner might write instead.
        wrongs = [int(x) for x in map(evaluate, wrong_sentences) if x == int(x)]
        return MathDraw("", str(v), prompt=story,
                        distractors=_story.keep(*wrongs, v + 1, v - 1, answer=v, lo=0))


@question_type("math.two_step_add_sub_p2",
               display_name={"th": "โจทย์ปัญหา 2 ขั้นตอน (บวกและลบ)"},
               level=LEVEL, topic="บวก ลบ คูณ หารระคน")
class TwoStepAddSubP2(WordProblem):
    def expr(self, rng: Random, hi: int = 1000):
        story, ans, first, same = two_step_add_sub_story(rng, max(300, min(int(hi), 1000)))
        return MathDraw("", str(ans), prompt=story,
                        distractors=_story.keep(first, same, ans + 10, ans - 10,
                                                answer=ans, lo=0))
