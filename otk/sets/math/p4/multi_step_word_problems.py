"""โจทย์ปัญหาระคน

คณิตศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.4/*

Sets moved here from: math_gaps_primary, math_p4.
"""

from __future__ import annotations

from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_gaps_primary import _choices
from otk.sets._support.math_p2 import _maths, evaluate
from otk.sets._support.math_p4 import LEVEL, grouped

PROVENANCE = Provenance("original")


_MIXED_TOPIC = "โจทย์ปัญหาระคน"


def mixed_story_p4(rng: Random):
    """``(story, sentence, value, wrong sentences)`` with ป.4-sized numbers."""
    p = rng.choice(_story.NAMES)
    kind = rng.randrange(6)
    if kind == 0:
        seats, buses, walk = rng.randint(35, 55), rng.randint(4, 12), rng.randint(20, 120)
        return (f"โรงเรียนพานักเรียนไปทัศนศึกษาด้วยรถบัส {buses} คัน คันละ {seats} คน "
                f"และมีนักเรียนเดินทางเองอีก {walk} คน มีนักเรียนไปทัศนศึกษาทั้งหมดกี่คน",
                rf"{buses} \times {seats} + {walk}", buses * seats + walk,
                [rf"{buses} + {seats} + {walk}", rf"{buses} \times ({seats} + {walk})",
                 rf"{buses} \times {seats} - {walk}", rf"({buses} + {walk}) \times {seats}"])
    if kind == 1:
        price, n = rng.randint(120, 950), rng.randint(12, 48)
        paid = (price * n // 1000 + 1) * 1000
        return (f"โรงเรียนซื้อพัดลม {n} เครื่อง เครื่องละ {price} บาท จ่ายเงิน {grouped(paid)} บาท "
                f"จะได้เงินทอนกี่บาท", rf"{paid} - {n} \times {price}", paid - n * price,
                [rf"{paid} - {n} - {price}", rf"({paid} - {n}) \times {price}", rf"{n} \times {price}",
                 rf"{paid} + {n} \times {price}"])
    if kind == 2:
        per, days = rng.randint(125, 480), rng.randint(12, 30)
        share = rng.choice((2, 3, 4, 5, 6))
        total = per * days
        total -= total % share
        return (f"สหกรณ์ขายไข่ได้เงิน {grouped(total)} บาท นำไปแบ่งให้สมาชิก {share} คน "
                f"คนละเท่า ๆ กัน แล้วแต่ละคนนำไปฝากธนาคารคนละ {per // 2} บาท "
                f"แต่ละคนเหลือเงินกี่บาท", rf"{total} \div {share} - {per // 2}",
                total // share - per // 2,
                [rf"{total} \div ({share} - {per // 2})" if share > per // 2 else rf"{total} - {share} - {per // 2}",
                 rf"({total} - {per // 2}) \div {share}", rf"{total} \div {share} + {per // 2}",
                 rf"{total} \times {share} - {per // 2}"])
    if kind == 3:
        boxes, per, broken = rng.randint(15, 60), rng.choice((12, 24, 30)), rng.randint(5, 60)
        return (f"ร้านค้าสั่งไข่ไก่ {boxes} แผง แผงละ {per} ฟอง ระหว่างขนส่งไข่แตก {broken} ฟอง "
                f"เหลือไข่ไก่ที่ดีกี่ฟอง", rf"{boxes} \times {per} - {broken}",
                boxes * per - broken,
                [rf"{boxes} \times {per} + {broken}", rf"{boxes} \times ({per} - {broken})"
                 if per > broken else rf"{boxes} + {per} - {broken}",
                 rf"({boxes} - {broken}) \times {per}" if boxes > broken else rf"{boxes} - {broken} + {per}",
                 rf"{boxes} + {per} + {broken}"])
    if kind == 4:
        a, b, share = rng.randint(1000, 9000), rng.randint(1000, 9000), rng.choice((4, 5, 6, 8))
        total = a + b
        b += (-total) % share
        return (f"{p}เก็บเงินได้ {grouped(a)} บาท พี่ให้เงินเพิ่มอีก {grouped(b)} บาท "
                f"{p}แบ่งเงินทั้งหมดเป็น {share} ส่วนเท่า ๆ กันเพื่อใช้ {share} เดือน "
                f"ใช้ได้เดือนละกี่บาท", rf"({a} + {b}) \div {share}", (a + b) // share,
                [rf"{a} + {b} \div {share}", rf"({a} + {b}) \times {share}",
                 rf"{a} + {b} - {share}", rf"({a} - {b}) \div {share}" if a > b else rf"{a} \div {share} + {b}"])
    length, width, cost = rng.randint(12, 40), rng.randint(8, 25), rng.randint(15, 60)
    return (f"สวนรูปสี่เหลี่ยมผืนผ้ากว้าง {width} เมตร ยาว {length} เมตร ล้อมรั้วรอบสวน "
            f"ค่ารั้วเมตรละ {cost} บาท ต้องจ่ายค่ารั้วกี่บาท",
            rf"2 \times ({length} + {width}) \times {cost}", 2 * (length + width) * cost,
            [rf"{length} \times {width} \times {cost}", rf"({length} + {width}) \times {cost}",
             rf"2 \times {length} + {width} \times {cost}", rf"{length} + {width} + {cost}"])


def _whole(sentences: list[str]) -> list[int]:
    out = []
    for s in sentences:
        v = evaluate(s)
        if v == int(v) and v >= 0:
            out.append(int(v))
    return out


@question_type("math.mixed_ops_p4",
               display_name={"th": "หาผลลัพธ์การบวก ลบ คูณ หารระคน (คูณหารก่อนบวกลบ)"},
               level=LEVEL, topic=_MIXED_TOPIC)
class MixedOpsP4(MathType):
    def expr(self, rng: Random):
        a, b = rng.randint(12, 99), rng.randint(3, 9)
        c, d = rng.randint(100, 900), rng.randint(2, 9)
        form = rng.randrange(4)
        if form == 0:
            tex, v = rf"{c} + {a} \times {b}", c + a * b
            w = [(c + a) * b, c + a + b]
        elif form == 1:
            c = max(c, a * b + 1)
            tex, v = rf"{c} - {a} \times {b}", c - a * b
            w = [abs((c - a) * b), c - a + b]
        elif form == 2:
            n = a * b
            tex, v = rf"{c} + {n} \div {b}", c + a
            w = [(c + n) // b if (c + n) % b == 0 else c + n - b, c + n + b]
        else:
            c -= c % d
            tex, v = rf"{a} \times {b} + {c} \div {d}", a * b + c // d
            w = [(a * b + c) // d if (a * b + c) % d == 0 else a * (b + c) // d, a * b + c * d]
        # Working strictly left to right is the slip to catch.
        return MathDraw(tex, str(v), prompt="จงหาผลลัพธ์ (คูณหรือหารก่อนบวกหรือลบ)",
                        distractors=_story.keep(*w, v + 10, v - 1, answer=v, lo=0))


@question_type("math.story_for_sentence_p4",
               display_name={"th": "เลือกโจทย์ปัญหาที่ตรงกับประโยคสัญลักษณ์"},
               level={"th": "ป.4"}, topic="โจทย์ปัญหาระคน")
class StoryForSentenceP4(QuestionType):
    """Four two-step stories built from the same three numbers; the learner
    picks the one the number sentence solves."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        p = rng.choice(_story.NAMES)
        a, b = rng.randint(3, 9), rng.randint(12, 48)
        c = rng.randint(5, min(40, a * b - 1))
        stories = {
            "a*b+c": f"{p}ซื้อสมุด {a} แพ็ค แพ็คละ {b} เล่ม และมีสมุดอยู่แล้ว {c} เล่ม {p}มีสมุดทั้งหมดกี่เล่ม",
            "a*b-c": f"{p}มีสมุด {a} แพ็ค แพ็คละ {b} เล่ม แจกเพื่อนไป {c} เล่ม {p}เหลือสมุดกี่เล่ม",
            "a*(b+c)": (f"โรงเรียนมีห้องเรียน {a} ห้อง แต่ละห้องมีนักเรียนชาย {b} คน "
                        f"และนักเรียนหญิง {c} คน โรงเรียนมีนักเรียนทั้งหมดกี่คน"),
            "(a+b)*c": (f"{p}มีดินสอ {a} แท่ง ซื้อเพิ่มอีก {b} แท่ง แล้วนำดินสอทั้งหมดไปแลกลูกอม "
                        f"แท่งละ {c} เม็ด {p}ได้ลูกอมทั้งหมดกี่เม็ด"),
        }
        sentences = {
            "a*b+c": rf"{a} \times {b} + {c} = \square",
            "a*b-c": rf"{a} \times {b} - {c} = \square",
            "a*(b+c)": rf"{a} \times ({b} + {c}) = \square",
            "(a+b)*c": rf"({a} + {b}) \times {c} = \square",
        }
        shown = rng.choice(list(sentences))
        return _choices([text("โจทย์ปัญหาข้อใดใช้ประโยคสัญลักษณ์นี้หาคำตอบได้"),
                         content_math(sentences[shown])],
                        stories[shown], [s for k, s in stories.items() if k != shown], self.topic)


@question_type("math.two_step_sentence_p4",
               display_name={"th": "เขียนประโยคสัญลักษณ์แสดงการบวก ลบ คูณ หารระคน"},
               level=LEVEL, topic=_MIXED_TOPIC)
class TwoStepSentenceP4(QuestionType):
    break_convergence = True  # one-part slips cluster round the answer
    def build(self, rng: Random) -> GeneratedQuestion:
        story, sentence, v, wrongs = mixed_story_p4(rng)
        wrongs = [w for w in wrongs if evaluate(w) != v]
        return _maths([text(story), text("ประโยคสัญลักษณ์ใดใช้หาคำตอบของโจทย์นี้ได้")],
                      rf"{sentence} = \square", [rf"{w} = \square" for w in wrongs],
                      self.topic)


@question_type("math.two_step_word_problem_p4",
               display_name={"th": "โจทย์ปัญหาการบวก ลบ คูณ หารระคน"},
               level=LEVEL, topic=_MIXED_TOPIC)
class TwoStepWordProblemP4(WordProblem):
    def expr(self, rng: Random):
        story, _, v, wrongs = mixed_story_p4(rng)
        return MathDraw("", str(v), prompt=story,
                        distractors=_story.keep(*_whole(wrongs), v + 100, answer=v, lo=0))
