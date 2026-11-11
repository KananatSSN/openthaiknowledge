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


# ── More two-step word problems (2026-11): two kinds bought, buy then share, save then spend, empty seats,
# loads delivered, two rooms compared, and pages still to read ──
from otk.core.registry import question_type  # noqa: E402
from otk.kit.math_problems import MathType, WordProblem  # noqa: E402
from otk.sets._support.math_p3 import LEVEL  # noqa: E402


@question_type("math.buy_two_kinds_p3", display_name={"th": "ซื้อของสองชนิดหลายชิ้น"},
               level=LEVEL, topic="โจทย์ปัญหาระคน")
class BuyTwoKindsP3(WordProblem):
    def expr(self, rng: Random):
        m, a, n, b = rng.randint(2, 9), rng.randint(5, 60), rng.randint(2, 9), rng.randint(5, 60)
        right = m * a + n * b
        x, y = rng.sample(("สมุด", "ปากกา", "ยางลบ", "ไม้บรรทัด", "ดินสอสี"), 2)
        prompt = f"ซื้อ{x} {m} ชิ้น ชิ้นละ {a} บาท และ{y} {n} ชิ้น ชิ้นละ {b} บาท ต้องจ่ายเงินทั้งหมดกี่บาท"
        # Every number added; only one kind; the counts and prices crossed.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(m + a + n + b, m * a, (m + n) * (a + b), m * b + n * a,
                                                answer=right, lo=1))


@question_type("math.buy_then_share_p3", display_name={"th": "ซื้อมาแล้วแบ่งให้เท่า ๆ กัน"},
               level=LEVEL, topic="โจทย์ปัญหาระคน")
class BuyThenShareP3(WordProblem):
    def expr(self, rng: Random):
        people = rng.randint(2, 9)
        each = rng.randint(3, 20)
        per_box = rng.choice((6, 8, 10, 12, 24))
        while (people * each) % per_box:
            each += 1
        boxes = people * each // per_box
        prompt = (f"ครูซื้อลูกอม {boxes} ถุง ถุงละ {per_box} เม็ด แบ่งให้นักเรียน {people} คนเท่า ๆ กัน "
                  f"ได้คนละกี่เม็ด")
        # The total not shared; shared by bags; one more each.
        return MathDraw("", str(each), prompt=prompt,
                        distractors=_story.keep(boxes * per_box, per_box // people if per_box > people else people,
                                                each + 1, boxes, answer=each, lo=1))


@question_type("math.save_then_spend_p3", display_name={"th": "ออมเงินแล้วใช้ไป"},
               level=LEVEL, topic="โจทย์ปัญหาระคน")
class SaveThenSpendP3(WordProblem):
    def expr(self, rng: Random):
        per, days = rng.choice((10, 15, 20, 25)), rng.randint(10, 30)
        spend = rng.randint(1, per * days // 10) * 10
        right = per * days - spend
        p = rng.choice(_story.NAMES)
        prompt = f"{p}ออมเงินวันละ {per} บาท เป็นเวลา {days} วัน แล้วซื้อหนังสือราคา {spend} บาท {p}เหลือเงินกี่บาท"
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(per * days, per * days + spend, per + days - spend, right + per,
                                                answer=right, lo=0))


@question_type("math.empty_seats_p3", display_name={"th": "เก้าอี้ว่างกี่ตัว"},
               level=LEVEL, topic="โจทย์ปัญหาระคน")
class EmptySeatsP3(WordProblem):
    def expr(self, rng: Random):
        rows, per = rng.randint(5, 20), rng.randint(8, 25)
        seats = rows * per
        people = rng.randint(seats // 2, seats - 1)
        right = seats - people
        prompt = (f"หอประชุมจัดเก้าอี้ {rows} แถว แถวละ {per} ตัว มีนักเรียนมานั่ง {people} คน "
                  f"คนละหนึ่งตัว เหลือเก้าอี้ว่างกี่ตัว")
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(seats, rows + per - people, right + per, right - 1, answer=right, lo=0))


@question_type("math.loads_delivered_p3", display_name={"th": "ขนของหลายเที่ยวแล้วยังเหลือ"},
               level=LEVEL, topic="โจทย์ปัญหาระคน")
class LoadsDeliveredP3(WordProblem):
    def expr(self, rng: Random):
        per, trips, left = rng.randint(20, 90), rng.randint(3, 9), rng.randint(5, 60)
        right = per * trips + left
        prompt = (f"รถบรรทุกขนกล่องได้เที่ยวละ {per} กล่อง ขนไปแล้ว {trips} เที่ยว ยังเหลือกล่องอีก {left} กล่อง "
                  f"เดิมมีกล่องทั้งหมดกี่กล่อง")
        # The left-over subtracted; one trip too few; the numbers added.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(per * trips - left, per * (trips - 1) + left, per + trips + left,
                                                per * trips, answer=right, lo=1))


@question_type("math.two_rooms_compare_p3", display_name={"th": "เปรียบเทียบจำนวนที่จัดเป็นแถวสองห้อง"},
               level=LEVEL, topic="โจทย์ปัญหาระคน")
class TwoRoomsCompareP3(WordProblem):
    def expr(self, rng: Random):
        while True:
            a, b, c, d = rng.randint(3, 9), rng.randint(4, 12), rng.randint(3, 9), rng.randint(4, 12)
            if a * b != c * d:
                break
        if a * b < c * d:
            a, b, c, d = c, d, a, b
        right = a * b - c * d
        prompt = (f"ห้องแรกจัดโต๊ะ {a} แถว แถวละ {b} ตัว ห้องที่สองจัดโต๊ะ {c} แถว แถวละ {d} ตัว "
                  f"ห้องแรกมีโต๊ะมากกว่าห้องที่สองกี่ตัว")
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(abs(a - c) + abs(b - d), a * b + c * d, abs(b - d), right + 1,
                                                answer=right, lo=1))


@question_type("math.pages_left_p3", display_name={"th": "อ่านหนังสือแล้วเหลืออีกกี่หน้า"},
               level=LEVEL, topic="โจทย์ปัญหาระคน")
class PagesLeftP3(WordProblem):
    def expr(self, rng: Random):
        per, days = rng.randint(8, 25), rng.randint(3, 10)
        read = per * days
        total = read + rng.randint(10, 200)
        right = total - read
        p = rng.choice(_story.NAMES)
        prompt = f"หนังสือเล่มหนึ่งมี {total} หน้า {p}อ่านวันละ {per} หน้า เป็นเวลา {days} วัน เหลืออีกกี่หน้า"
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(read, total - per, right - per, total - per - days, answer=right, lo=1))
