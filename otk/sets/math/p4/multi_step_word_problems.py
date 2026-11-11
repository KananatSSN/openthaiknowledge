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


# ── More multi-step word problems (2026-11): two kinds bought, ticket money, a shared bill, a year's saving,
# full trays, and trips there and back ──

from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType, WordProblem  # noqa: E402
from otk.sets._support.math_p4 import LEVEL  # noqa: E402


def _g(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


@question_type("math.ticket_income_p4", display_name={"th": "รายได้จากการขายบัตรสองประเภท"},
               level=LEVEL, topic="โจทย์ปัญหาระคน")
class TicketIncomeP4(WordProblem):
    def expr(self, rng: Random):
        adult, child = rng.choice((80, 100, 120, 150)), rng.choice((30, 40, 50, 60))
        a, c = rng.randint(50, 400), rng.randint(50, 400)
        right = adult * a + child * c
        prompt = (f"สวนสัตว์ขายบัตรผู้ใหญ่ใบละ {adult} บาท ได้ {a} ใบ และบัตรเด็กใบละ {child} บาท ได้ {c} ใบ "
                  f"ได้เงินทั้งหมดกี่บาท")
        # The prices crossed; every ticket at the adult price; only adults.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(adult * c + child * a, adult * (a + c), adult * a, right + 100, answer=right, lo=1))


@question_type("math.buy_two_kinds_p4", display_name={"th": "ซื้อของสองชนิดจำนวนมาก"},
               level=LEVEL, topic="โจทย์ปัญหาระคน")
class BuyTwoKindsP4(WordProblem):
    def expr(self, rng: Random):
        m, a, n, b = rng.randint(12, 60), rng.randint(15, 120), rng.randint(12, 60), rng.randint(15, 120)
        right = m * a + n * b
        x, y = rng.sample(("สมุด", "ปากกา", "ลูกฟุตบอล", "เสื้อกีฬา", "ถุงเท้า"), 2)
        prompt = f"โรงเรียนซื้อ{x} {m} ชิ้น ชิ้นละ {a} บาท และ{y} {n} ชิ้น ชิ้นละ {b} บาท จ่ายเงินทั้งหมดกี่บาท"
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(m * b + n * a, (m + n) * a, m * a, right + 100, answer=right, lo=1))


@question_type("math.cost_per_person_p4", display_name={"th": "ค่าใช้จ่ายรวมแล้วหารเฉลี่ยคนละเท่ากัน"},
               level=LEVEL, topic="โจทย์ปัญหาระคน")
class CostPerPersonP4(WordProblem):
    def expr(self, rng: Random):
        vans = rng.randint(2, 6)
        k = rng.randint(10, 80)
        people = rng.randint(10, 40)
        right = vans * k
        rent = people * k
        total = vans * rent
        prompt = (f"กลุ่มเพื่อน {people} คนเช่ารถตู้ {vans} คัน คันละ {rent:,} บาท แบ่งจ่ายค่าเช่าคนละเท่า ๆ กัน "
                  f"ต้องจ่ายคนละกี่บาท")
        # One van shared; the total not shared; split by the vans.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(k, total, rent, right + 10, answer=right, lo=1))


@question_type("math.yearly_saving_p4", display_name={"th": "ออมเงินทุกเดือนตลอดปี"},
               level=LEVEL, topic="โจทย์ปัญหาระคน")
class YearlySavingP4(WordProblem):
    def expr(self, rng: Random):
        per = rng.randint(3, 40) * 50
        spend = rng.randint(1, per * 12 // 500) * 500
        right = per * 12 - spend
        p = rng.choice(_story.NAMES)
        prompt = f"{p}ฝากเงินเดือนละ {per:,} บาท ครบ 1 ปี แล้วถอนไปซื้อของ {spend:,} บาท {p}เหลือเงินฝากกี่บาท"
        # A year taken as 10 months; nothing taken out; one month short.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(per * 10 - spend, per * 12, per * 11 - spend, right + per, answer=right, lo=0))


@question_type("math.full_trays_p4", display_name={"th": "บรรจุได้กี่ชุดเต็ม"},
               level=LEVEL, topic="โจทย์ปัญหาระคน")
class FullTraysP4(WordProblem):
    def expr(self, rng: Random):
        per = rng.choice((12, 24, 30))
        trays = rng.randint(20, 200)
        extra = rng.randint(1, per - 1)
        n = per * trays + extra
        thing, box = rng.choice((("ไข่ไก่", "แผง"), ("ขวดน้ำ", "ลัง"), ("ขนม", "กล่อง")))
        prompt = f"มี{thing} {n:,} ชิ้น บรรจุ{box}ละ {per} ชิ้น ได้กี่{box}เต็ม"
        # Counting the part-filled one; the left-over; one fewer.
        return MathDraw("", str(trays), prompt=prompt,
                        distractors=_story.keep(trays + 1, extra, trays - 1, n // 10, answer=trays, lo=1))


@question_type("math.round_trips_p4", display_name={"th": "ระยะทางไปกลับหลายวัน"},
               level=LEVEL, topic="โจทย์ปัญหาระคน")
class RoundTripsP4(WordProblem):
    def expr(self, rng: Random):
        km, days = rng.randint(3, 45), rng.randint(5, 26)
        right = 2 * km * days
        p = rng.choice(_story.NAMES)
        prompt = f"บ้านของ{p}อยู่ห่างจากที่ทำงาน {km} กิโลเมตร {p}ขับรถไปกลับทุกวันเป็นเวลา {days} วัน รวมระยะทางกี่กิโลเมตร"
        # One way only; one day only; the numbers added.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(km * days, 2 * km, km + days, 2 * km * (days - 1), answer=right, lo=1))
