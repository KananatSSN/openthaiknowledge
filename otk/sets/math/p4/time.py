"""เวลา

คณิตศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.4/*

Sets moved here from: math_p4.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_p2 import _texts, clock
from otk.sets._support.math_p4 import LEVEL

PROVENANCE = Provenance("original")


_TIME_TOPIC = "เวลา"


# (bigger unit, smaller unit, how many, the base-10/100 slip)
_TIME_UNITS = (("นาที", "วินาที", 60), ("ชั่วโมง", "นาที", 60), ("วัน", "ชั่วโมง", 24),
               ("สัปดาห์", "วัน", 7), ("ปี", "เดือน", 12), ("ปี", "วัน", 365))


_MONTHS = (("มกราคม", 31), ("กุมภาพันธ์", 28), ("มีนาคม", 31), ("เมษายน", 30),
           ("พฤษภาคม", 31), ("มิถุนายน", 30), ("กรกฎาคม", 31), ("สิงหาคม", 31),
           ("กันยายน", 30), ("ตุลาคม", 31), ("พฤศจิกายน", 30), ("ธันวาคม", 31))


@question_type("math.time_units_p4",
               display_name={"th": "ความสัมพันธ์ของหน่วยเวลา (วินาที ถึง ปี)"},
               level=LEVEL, topic=_TIME_TOPIC)
class TimeUnitsP4(WordProblem):
    def expr(self, rng: Random):
        big, small, k = rng.choice(_TIME_UNITS[:5])
        a = rng.randint(1, 9)
        b = rng.randint(1, k - 1)
        if rng.random() < 0.6:
            ans = a * k + b
            return MathDraw("", str(ans), prompt=f"{a} {big} {b} {small} เท่ากับกี่{small}",
                            distractors=_story.keep(100 * a + b, a * k, a + b, 10 * a + b,
                                                    answer=ans))
        total = a * k + b
        return MathDraw("", str(b),
                        prompt=f"{total} {small} เท่ากับ {a} {big} กับอีกกี่{small}",
                        distractors=_story.keep(total - 100 * a if total > 100 * a else b + k,
                                                total - a, b + 1, k - b, answer=b, lo=1))


@question_type("math.calendar_word_problem_p4",
               display_name={"th": "โจทย์ปัญหาเวลา: วัน เดือน ปี"},
               level=LEVEL, topic=_TIME_TOPIC)
class CalendarWordProblemP4(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        kind = rng.randrange(3)
        if kind == 0:
            born = rng.randint(2550, 2560)
            now = rng.randint(born + 7, 2570)
            ans = now - born
            return MathDraw("", str(ans),
                            prompt=(f"{p}เกิดปี พ.ศ. {born} ถ้าวันเกิดของปี พ.ศ. {now} ผ่านไปแล้ว "
                                    f"{p}อายุกี่ปี"),
                            distractors=_story.keep(ans + 1, ans - 1, ans + 10, answer=ans, lo=1))
        m = rng.randrange(11)
        name, days = _MONTHS[m]
        nxt, _ = _MONTHS[m + 1]
        start = rng.randint(10, days - 1)
        end = rng.randint(2, 25)
        ans = days - start + end
        if kind == 1:
            return MathDraw("", str(ans),
                            prompt=(f"วันนี้วันที่ {start} {name} อีกกี่วันจะถึงวันที่ {end} {nxt} "
                                    f"(เดือน{name}มี {days} วัน)"),
                            # Every month as 30 days, and simply subtracting the dates.
                            distractors=_story.keep(30 - start + end, abs(end - start),
                                                    ans + 1, answer=ans, lo=1))
        weeks = rng.randint(2, 8)
        extra = rng.randint(1, 6)
        return MathDraw("", str(7 * weeks + extra),
                        prompt=(f"{p}ไปค่ายฤดูร้อน {weeks} สัปดาห์ {extra} วัน "
                                f"คิดเป็นกี่วัน"),
                        distractors=_story.keep(10 * weeks + extra, weeks + extra,
                                                7 * weeks, answer=7 * weeks + extra))


@question_type("math.travel_time_p4",
               display_name={"th": "โจทย์ปัญหาระยะเวลาการเดินทาง (ข้ามวัน)"},
               level=LEVEL, topic=_TIME_TOPIC)
class TravelTimeP4(QuestionType):
    _TRIPS = (("รถไฟ", "กรุงเทพฯ", "เชียงใหม่"), ("รถทัวร์", "กรุงเทพฯ", "อุบลราชธานี"),
              ("รถไฟ", "กรุงเทพฯ", "หาดใหญ่"), ("รถทัวร์", "ขอนแก่น", "ภูเก็ต"))

    def build(self, rng: Random) -> GeneratedQuestion:
        kind, a, b = rng.choice(self._TRIPS)
        h1, m1 = rng.randint(17, 22), rng.choice(range(0, 60, 5))
        # Long enough to cross midnight: the question says "the next day".
        to_midnight = 24 * 60 - (60 * h1 + m1)
        span = rng.randrange(to_midnight + 60, to_midnight + 10 * 60, 5)
        end = 60 * h1 + m1 + span
        h2, m2 = divmod(end % (24 * 60), 60)
        hours, mins = divmod(span, 60)
        said = lambda h, m: f"{h} ชั่วโมง" + (f" {m} นาที" if m else "")
        right = said(hours, mins)
        naive = 60 * (h2 - h1) + (m2 - m1)          # forgetting the midnight
        wrongs = [said(*divmod(abs(naive), 60)), said(hours + 1, mins),
                  said(hours, (mins + 30) % 60), said(24 - hours, mins), said(hours - 1, mins)]
        return _texts([text(f"{kind}ออกจาก{a}เวลา {clock(h1, m1)} ถึง{b}เวลา {clock(h2, m2)} "
                            f"ของวันรุ่งขึ้น ใช้เวลาเดินทางเท่าใด")], right,
                      [w for w in dict.fromkeys(wrongs) if w != right], self.topic)
