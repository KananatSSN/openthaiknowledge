"""เวลา

คณิตศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.2/*

Sets moved here from: math, math_diagrams, math_number, math_p2.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem
from otk.sets._support.math_diagrams import CLOCK_ALT, CLOCKS, _img, _text_q
from otk.sets._support.math_p2 import LEVEL, _texts, clock

PROVENANCE = Provenance("original")


def _clock_text(h: int, m: int) -> str:
    return f"{h}.{m:02d} น."


def said(h: int, m: int) -> str:
    """8, 5 -> 8 นาฬิกา 5 นาที."""
    return f"{h} นาฬิกา" + (f" {m} นาที" if m else "")


@question_type("math.clock_read_p2", display_name={"th": "อ่านเวลาจากหน้าปัดนาฬิกา"},
               level={"th": "ป.2"}, topic="เวลา")
class ClockReadP2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        c = rng.choice(CLOCKS)
        h, m = c.h, c.m
        # Hands swapped, the hour hand read as the next hour, the long hand's
        # number read as minutes.
        swapped = _clock_text(m // 5 or 12, (h % 12) * 5)
        wrongs = [swapped, _clock_text(h % 12 + 1, m) if m >= 30 else _clock_text((h - 2) % 12 + 1, m),
                  _clock_text(h, m // 5) if m // 5 != m else _clock_text(h, (m + 30) % 60),
                  _clock_text(h, (m + 30) % 60), _clock_text(h, (m + 5) % 60),
                  _clock_text(h % 12 + 1, (m + 5) % 60)]
        return _text_q([text("นาฬิกาบอกเวลาเท่าใด"), _img(c.asset_id, CLOCK_ALT)],
                       _clock_text(h, m), wrongs, self.topic)


@question_type("math.time_notation_p2",
               display_name={"th": "การอ่านและเขียนบอกเวลา (นาฬิกา นาที)"},
               level=LEVEL, topic="เวลา")
class TimeNotationP2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        h = rng.randint(6, 18)
        m = rng.choice(range(5, 60, 5))
        kind = rng.randrange(3)
        if kind == 0:
            # Hour and minute swapped, one hour off, 5 minutes written as .5.
            wrongs = [f"{m}.{h:02d} น.", clock(h + 1, m),
                      f"{h}.{m} น." if m < 10 else clock(h, 60 - m), clock(h - 1, m)]
            return _texts([text(f"เวลา {said(h, m)} เขียนแบบใด")], clock(h, m),
                          [w for w in dict.fromkeys(wrongs) if w != clock(h, m)], self.topic)
        if kind == 1:
            wrongs = [said(m, h) if m <= 23 else said(h, 60 - m), said(h + 1, m),
                      said(h - 1, m), said(h, (m + 30) % 60)]
            return _texts([text(f"เวลา {clock(h, m)} อ่านว่าอย่างไร")], said(h, m),
                          [w for w in dict.fromkeys(wrongs) if w != said(h, m)], self.topic)
        # Hands of a 12-hour face: the short hand sits between two numbers.
        h12 = (h - 1) % 12 + 1
        mark = m // 5
        return _texts(
            [text(f"เข็มสั้นของนาฬิกาอยู่ระหว่างเลข {h12} กับ {h12 % 12 + 1} "
                  f"เข็มยาวชี้ที่เลข {mark} นาฬิกาบอกเวลาเท่าใด")],
            clock(h12, m),
            # The number under the long hand read as minutes comes first.
            [w for w in dict.fromkeys([clock(h12, mark), clock(h12 % 12 + 1, m),
                                       clock(mark, h12 * 5 % 60),
                                       clock(h12, (m + 30) % 60)])
             if w != clock(h12, m)],
            self.topic)


@question_type("math.calendar_weekday",
               display_name={"th": "อ่านปฏิทิน: หาวันในสัปดาห์"}, level={"th": "ป.2"},
               topic="เวลา")
class CalendarWeekday(ChoiceType):
    _DAYS = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]

    def compose(self, rng: Random):
        d = rng.randint(1, 21)
        wday = rng.choice(self._DAYS)
        stem = (f"ถ้าวันที่ {d} เป็นวัน{wday} แล้ววันที่ {d + 7} เป็นวันอะไร?")
        return stem, wday, [x for x in self._DAYS if x != wday]


@question_type("math.hours_minutes_p2",
               display_name={"th": "ชั่วโมงและนาที"},
               level=LEVEL, topic="เวลา")
class HoursMinutesP2(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        kind = rng.randrange(3)
        if kind == 0:
            h, m = rng.randint(1, 3), rng.choice(range(5, 60, 5))
            ans = 60 * h + m
            return MathDraw("", str(ans),
                            prompt=f"{h} ชั่วโมง {m} นาที เท่ากับกี่นาที",
                            # A hundred minutes to the hour is the slip to catch.
                            distractors=_story.keep(100 * h + m, h + m, 60 * h, ans + 60,
                                                    answer=ans))
        if kind == 1:
            h, m = rng.randint(1, 2), rng.choice(range(5, 60, 5))
            total = 60 * h + m
            return MathDraw("", str(m),
                            prompt=f"{total} นาที เท่ากับ {h} ชั่วโมงกับอีกกี่นาที",
                            distractors=_story.keep(total - 100 * h, total - 60, m + 10,
                                                    total, answer=m, lo=1))
        a, b = rng.choice(range(15, 60, 5)), rng.choice(range(15, 60, 5))
        activity = rng.choice(("ทำการบ้าน", "อ่านหนังสือ", "ช่วยแม่ทำงานบ้าน", "เล่นดนตรี"))
        return MathDraw("", str(a + b),
                        prompt=(f"{p}{activity}ช่วงเช้า {a} นาที และช่วงเย็น {b} นาที "
                                f"รวม{activity}กี่นาที"),
                        distractors=_story.keep(abs(a - b), a + b + 10, a + b - 5, 60,
                                                answer=a + b, lo=1))


@question_type("math.time_to_hour",
               display_name={"th": "อ่านเวลา: อีกกี่นาทีถึงชั่วโมงถัดไป"},
               level={"th": "ป.2"}, topic="เวลา")
class TimeToHour(WordProblem):
    def expr(self, rng: Random):
        h = rng.randint(1, 12)
        m = rng.choice(range(5, 60, 5))
        p = rng.choice(_story.NAMES)
        prompt = rng.choice((
            f"เวลา {h} นาฬิกา {m} นาที อีกกี่นาทีจะถึง {h + 1} นาฬิกาพอดี?",
            f"ตอนนี้เป็นเวลา {h} นาฬิกา {m} นาที การแข่งขันจะเริ่มเวลา {h + 1} นาฬิกาตรง "
            f"อีกกี่นาทีการแข่งขันจะเริ่ม",
            f"{p}ออกจากบ้านเวลา {h} นาฬิกา {m} นาที และถึงบ้านคุณยายเวลา {h + 1} นาฬิกาพอดี "
            f"{p}ใช้เวลาเดินทางกี่นาที",
        ))
        return MathDraw(
            "", str(60 - m), prompt=prompt,
            distractors=[str(m), str(60 + m), str(30 - m)])


@question_type("math.time_elapsed", display_name={"th": "เวลาผ่านไปกี่นาที"},
               level={"th": "ป.2"}, topic="เวลา")
class TimeElapsed(WordProblem):
    def expr(self, rng: Random, minutes_lo: int = 20, minutes_hi: int = 150):
        start_h = rng.randint(7, 16)
        start_m = rng.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        span = rng.randrange(minutes_lo, minutes_hi, 5)
        total = start_h * 60 + start_m + span
        end_h, end_m = divmod(total, 60)
        s, e = f"{start_h:02d}:{start_m:02d}", f"{end_h:02d}:{end_m:02d}"
        p = rng.choice(_story.NAMES)
        prompt = rng.choice((
            f"เริ่มอ่านหนังสือเวลา {s} น. และเลิกอ่านเวลา {e} น. ใช้เวลาอ่านหนังสือกี่นาที",
            f"{p}เริ่มทำการบ้านเวลา {s} น. และทำเสร็จเวลา {e} น. {p}ใช้เวลาทำการบ้านกี่นาที",
            f"รถโดยสารออกจากสถานีเวลา {s} น. และถึงปลายทางเวลา {e} น. ใช้เวลาเดินทางกี่นาที",
            f"ภาพยนตร์เรื่องหนึ่งเริ่มฉายเวลา {s} น. และจบเวลา {e} น. ภาพยนตร์เรื่องนี้ยาวกี่นาที",
        ))
        return MathDraw(
            "", str(span), prompt=prompt,
            # Reading the clock difference as a decimal is the classic error.
            distractors=[str((end_h - start_h) * 100 + (end_m - start_m)),
                         str(span + 60), str(abs(span - 60) or 5)])
