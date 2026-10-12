"""โจทย์ปัญหาระคน

คณิตศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.3/*

Sets moved here from: math_p3.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_p2 import _maths, evaluate, two_step_add_sub_story
from otk.sets._support.math_p3 import LEVEL

PROVENANCE = Provenance("original")


_MIXED_TOPIC = "โจทย์ปัญหาระคน"


def mixed_story_p3(rng: Random):
    """``(story, sentence, value, wrong sentences)``: two steps, all four
    operations, numbers a ป.3 learner works with."""
    p, q = _story.names(rng)
    kind = rng.randrange(6)
    if kind == 0:
        n, price = rng.randint(3, 9), rng.randint(15, 95)
        note = rng.choice([x for x in (500, 1000) if x > n * price])
        return (f"{p}ซื้อสมุด {n} เล่ม เล่มละ {price} บาท จ่ายด้วยธนบัตรใบละ {note} บาท "
                f"จะได้เงินทอนกี่บาท", rf"{note} - {n} \times {price}", note - n * price,
                [rf"{note} - {n} - {price}", rf"{n} \times {price}", rf"({note} - {n}) \times {price}"])
    if kind == 1:
        per, groups = rng.randint(3, 9), rng.randint(12, 60)
        extra = rng.randint(5, 40)
        total = per * groups
        return (f"ครูมีดินสอ {total} แท่ง แบ่งให้นักเรียน {per} กลุ่ม กลุ่มละเท่า ๆ กัน "
                f"แล้วให้เพิ่มอีกกลุ่มละ {extra} แท่ง แต่ละกลุ่มได้ดินสอกี่แท่ง",
                rf"{total} \div {per} + {extra}", groups + extra,
                [rf"{total} \div ({per} + {extra})", rf"{total} - {per} + {extra}",
                 rf"({total} + {extra}) \div {per}"])
    if kind == 2:
        boxes, each, sold = rng.randint(12, 40), rng.randint(6, 24), rng.randint(20, 150)
        sold = min(sold, boxes * each - 1)
        return (f"ร้านค้ามีขนมปัง {boxes} กล่อง กล่องละ {each} ก้อน ขายไป {sold} ก้อน "
                f"ร้านค้าเหลือขนมปังกี่ก้อน", rf"{boxes} \times {each} - {sold}",
                boxes * each - sold,
                [rf"{boxes} \times {each} + {sold}", rf"{boxes} + {each} - {sold}",
                 rf"{boxes} \times ({each} - {sold})"])
    if kind == 3:
        a, b, share = rng.randint(100, 900), rng.randint(100, 900), rng.randint(2, 9)
        total = a + b
        total -= total % share
        b = total - a
        return (f"{p}มีเงิน {a} บาท {q}มีเงิน {b} บาท นำเงินมารวมกันแล้วแบ่งให้เด็ก {share} คน "
                f"คนละเท่า ๆ กัน เด็กแต่ละคนได้เงินกี่บาท", rf"({a} + {b}) \div {share}",
                total // share,
                [rf"{a} + {b} \div {share}", rf"{a} + {b} - {share}", rf"({a} + {b}) \times {share}"])
    if kind == 4:
        rows, seats, absent = rng.randint(8, 25), rng.randint(10, 30), rng.randint(5, 60)
        absent = min(absent, rows * seats - 1)
        return (f"หอประชุมมีเก้าอี้ {rows} แถว แถวละ {seats} ตัว วันนี้มีคนมาร่วมงานจนเหลือเก้าอี้ว่าง "
                f"{absent} ตัว มีคนนั่งเก้าอี้กี่คน", rf"{rows} \times {seats} - {absent}",
                rows * seats - absent,
                [rf"{rows} + {seats} - {absent}", rf"{rows} \times {seats} + {absent}",
                 rf"{rows} \times ({seats} - {absent})"])
    weekly, weeks, spent = rng.randint(20, 150), rng.randint(3, 9), rng.randint(10, 200)
    spent = min(spent, weekly * weeks - 1)
    return (f"{p}ออมเงินสัปดาห์ละ {weekly} บาท เป็นเวลา {weeks} สัปดาห์ แล้วนำไปซื้อหนังสือ "
            f"{spent} บาท {p}เหลือเงินออมกี่บาท", rf"{weekly} \times {weeks} - {spent}",
            weekly * weeks - spent,
            [rf"{weekly} + {weeks} - {spent}", rf"{weekly} \times {weeks} + {spent}",
             rf"{weekly} \times ({weeks} - {spent})"])


def _whole_values(sentences: list[str]) -> list[int]:
    out = []
    for s in sentences:
        v = evaluate(s)
        if v == int(v) and v >= 0:
            out.append(int(v))
    return out


@question_type("math.mixed_ops_p3",
               display_name={"th": "การบวก ลบ คูณ หารระคน (มีวงเล็บ)"},
               level=LEVEL, topic=_MIXED_TOPIC)
class MixedOpsP3(MathType):
    def expr(self, rng: Random):
        a, b = rng.randint(12, 99), rng.randint(2, 9)
        c = rng.randint(10, 200)
        form = rng.randrange(5)
        if form == 0:
            tex, v, w = rf"{a} \times {b} + {c}", a * b + c, [a * (b + c), a + b + c]
        elif form == 1:
            c = min(c, a * b - 1)
            tex, v, w = rf"{a} \times {b} - {c}", a * b - c, [a * b + c, a - b + c]
        elif form == 2:
            n = a * b
            tex, v, w = rf"{n} \div {b} + {c}", a + c, [n - b + c, n + c, a * c]
        elif form == 3:
            tex, v, w = rf"({c} + {a}) \times {b}", (c + a) * b, [c + a * b, c * b + a]
        else:
            big = a * b + c * b
            # Dividing only the second number: big − (cb ÷ b).
            tex, v, w = rf"({big} - {c * b}) \div {b}", a, [big - c, big - c * b]
        return MathDraw(tex, str(v), prompt="จงหาผลลัพธ์",
                        distractors=_story.keep(*w, v + 10, v - 1, answer=v, lo=0))


@question_type("math.two_step_sentence_p3",
               display_name={"th": "เขียนประโยคสัญลักษณ์ของโจทย์ปัญหาสองขั้นตอน"},
               level=LEVEL, topic=_MIXED_TOPIC)
class TwoStepSentenceP3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        story, sentence, v, wrongs = mixed_story_p3(rng)
        wrongs = [w for w in wrongs if evaluate(w) != v]
        return _maths([text(story), text("ประโยคสัญลักษณ์ใดใช้หาคำตอบของโจทย์นี้ได้")],
                      rf"{sentence} = \square", [rf"{w} = \square" for w in wrongs],
                      self.topic)


@question_type("math.two_step_word_problem_p3",
               display_name={"th": "โจทย์ปัญหาสองขั้นตอน (บวก ลบ คูณ หาร)"},
               level=LEVEL, topic=_MIXED_TOPIC)
class TwoStepWordProblemP3(WordProblem):
    def expr(self, rng: Random):
        if rng.random() < 0.3:
            story, ans, first, same = two_step_add_sub_story(rng, 3000)
            return MathDraw("", str(ans), prompt=story,
                            distractors=_story.keep(first, same, ans + 100, ans - 10,
                                                    answer=ans, lo=0))
        story, _, v, wrongs = mixed_story_p3(rng)
        return MathDraw("", str(v), prompt=story,
                        distractors=_story.keep(*_whole_values(wrongs), v + 10, v - 1,
                                                answer=v, lo=0))
