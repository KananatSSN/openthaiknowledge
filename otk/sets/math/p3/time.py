"""เวลา

คณิตศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.3/*

Sets moved here from: math_diagrams, math_p3.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import CLOCK_ALT, ClockSpec, _img, _math_q, _nums
from otk.sets._support.math_p2 import _texts, clock
from otk.sets._support.math_p3 import LEVEL

PROVENANCE = Provenance("original")


def clock_of(h: int, m: int) -> ClockSpec:
    return ClockSpec((h - 1) % 12 + 1, m)


_TIME_TOPIC = "เวลา"


def spoken(h: int, half: bool = False) -> str:
    """How an hour is said in everyday Thai: 15 -> บ่าย 3 โมง, 20 -> 2 ทุ่ม."""
    if h == 0:
        word = "เที่ยงคืน"
    elif h <= 5:
        word = f"ตี {h}"
    elif h <= 11:
        word = f"{h} โมงเช้า"
    elif h == 12:
        word = "เที่ยงวัน"
    elif h == 13:
        word = "บ่ายโมง"
    elif h <= 15:
        word = f"บ่าย {h - 12} โมง"
    elif h <= 18:
        word = f"{h - 12} โมงเย็น"
    else:
        word = f"{h - 18} ทุ่ม"
    if not half:
        return word
    # 7.30 is "7 โมงครึ่ง" and 17.30 "5 โมงครึ่ง"; เช้า/เย็น drop out.
    if word.endswith(("โมงเช้า", "โมงเย็น")):
        return word.removesuffix("เช้า").removesuffix("เย็น") + "ครึ่ง"
    return word + (" ครึ่ง" if word.startswith("ตี") else "ครึ่ง")


@question_type("math.clock_24h_p3",
               display_name={"th": "การบอกเวลาแบบ 24 ชั่วโมง (โมง ทุ่ม ตี)"},
               level=LEVEL, topic=_TIME_TOPIC)
class Clock24hP3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        h = rng.choice([*range(1, 12), *range(13, 24)])
        # 6.30 and 18.30 are both "6 โมงครึ่ง" in speech; neither is asked.
        half = h not in (6, 18) and rng.random() < 0.3
        m = 30 if half else 0
        near = [(h % 12) or 12, (h + 12) % 24, (h + 1) % 24, (h - 1) % 24]
        if rng.random() < 0.5:
            wrongs = [clock(x, m) for x in near]
            return _texts([text(f"“{spoken(h, half)}” ตรงกับเวลาใด")], clock(h, m),
                          [w for w in dict.fromkeys(wrongs) if w != clock(h, m)], self.topic)
        wrongs = [spoken(x, half and x not in (0, 12)) for x in near]
        return _texts([text(f"เวลา {clock(h, m)} เรียกว่าอะไร")], spoken(h, half),
                      [w for w in dict.fromkeys(wrongs) if w != spoken(h, half)], self.topic)


@question_type("math.clock_duration_p3", display_name={"th": "หาระยะเวลาจากหน้าปัดนาฬิกาสองเรือน"},
               level={"th": "ป.3"}, topic="เวลา")
class ClockDurationP3(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    _TASKS = ("อ่านหนังสือ", "ทำการบ้าน", "เล่นฟุตบอล", "ช่วยแม่ทำอาหาร", "ซ้อมดนตรี")

    def build(self, rng: Random) -> GeneratedQuestion:
        h = rng.randint(7, 10)
        m = rng.randrange(0, 60, 5)
        span = rng.randrange(15, 175, 5)
        eh, em = divmod(60 * h + m + span, 60)
        a, b = clock_of(h, m), clock_of(eh, em)
        p = rng.choice(_story.NAMES)
        task = rng.choice(self._TASKS)
        decimal_gap = (100 * eh + em) - (100 * h + m)
        wrongs = _nums(decimal_gap, span + 60, abs(span - 60), span + 5, answer=span, lo=1)
        return _math_q([text(f"{p}เริ่ม{task}ตามเวลาที่นาฬิกาเรือนแรกบอก และเลิกตามเวลาที่นาฬิกา"
                             f"เรือนที่สองบอก (ช่วงเช้าเดียวกัน) {p}{task}กี่นาที"),
                        _img(a.asset_id, "นาฬิกาเรือนแรก: " + CLOCK_ALT),
                        _img(b.asset_id, "นาฬิกาเรือนที่สอง: " + CLOCK_ALT)],
                       str(span), wrongs, self.topic)


@question_type("math.duration_p3",
               display_name={"th": "ระยะเวลา (ชั่วโมงและนาที)"},
               level=LEVEL, topic=_TIME_TOPIC)
class DurationP3(WordProblem):
    _WHAT = ("ภาพยนตร์เริ่มฉาย", "การแข่งขันฟุตบอลเริ่ม", "ร้านเปิด", "การสอบเริ่ม",
             "รถไฟออกจากสถานี")
    _END = {"ภาพยนตร์เริ่มฉาย": "ฉายจบ", "การแข่งขันฟุตบอลเริ่ม": "แข่งจบ",
            "ร้านเปิด": "ร้านปิด", "การสอบเริ่ม": "สอบเสร็จ", "รถไฟออกจากสถานี": "รถไฟถึงปลายทาง"}

    def expr(self, rng: Random):
        what = rng.choice(self._WHAT)
        if rng.random() < 0.35:
            # Whole hours across noon, said the everyday way.
            start = rng.randint(7, 11)
            end = rng.randint(13, 18)
            return MathDraw("", str(end - start),
                            prompt=(f"{what}เวลา {spoken(start)} และ{self._END[what]}เวลา "
                                    f"{spoken(end)} รวมเป็นเวลากี่ชั่วโมง"),
                            # Subtracting the spoken numbers: 9 โมง to 5 โมงเย็น as 4.
                            distractors=_story.keep(abs(start - (end - 12)), end - start + 1,
                                                    end - start - 1, end, answer=end - start,
                                                    lo=1))
        h1, m1 = rng.randint(7, 16), rng.choice(range(0, 60, 5))
        span = rng.randrange(35, 200, 5)
        h2, m2 = divmod(60 * h1 + m1 + span, 60)
        decimal_gap = (100 * h2 + m2) - (100 * h1 + m1)
        return MathDraw("", str(span),
                        prompt=(f"{what}เวลา {clock(h1, m1)} และ{self._END[what]}เวลา "
                                f"{clock(h2, m2)} ใช้เวลากี่นาที"),
                        # Subtracting the clock readings as if they were decimals.
                        distractors=_story.keep(decimal_gap, span + 60, span - 60, span + 10,
                                                answer=span, lo=1))


@question_type("math.time_word_problem_p3",
               display_name={"th": "โจทย์ปัญหาเวลา: เริ่มหรือเสร็จกี่โมง"},
               level=LEVEL, topic=_TIME_TOPIC)
class TimeWordProblemP3(QuestionType):
    _TASKS = ("ทำการบ้าน", "เดินทางไปโรงเรียน", "ซ้อมดนตรี", "ทำความสะอาดห้อง",
              "อ่านหนังสือ", "เล่นฟุตบอล")

    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(_story.NAMES)
        task = rng.choice(self._TASKS)
        h, m = rng.randint(6, 19), rng.choice(range(5, 60, 5))
        span = rng.randrange(15, 60, 5)
        if rng.random() < 0.5:
            eh, em = divmod(60 * h + m + span, 60)
            naive = f"{h}.{m + span} น." if m + span >= 60 else clock(h + 1, m + span)
            wrongs = [naive, clock(eh - 1, em), clock(eh + 1, em),
                      clock(h, (m + span) % 60) if m + span >= 60 else clock(eh, (em + 10) % 60)]
            return _texts([text(f"{p}เริ่ม{task}เวลา {clock(h, m)} ใช้เวลา {span} นาที "
                                f"{p}{task}เสร็จเวลาใด")], clock(eh, em),
                          [w for w in dict.fromkeys(wrongs) if w != clock(eh, em)], self.topic)
        sh, sm = divmod(60 * h + m - span, 60)
        # 8.05 − 25 นาที worked as a decimal: 7.80.
        naive = f"{h - 1}.{100 + m - span} น." if m < span else clock(h, m - span + 10)
        wrongs = [naive, clock(sh + 1, sm), clock(sh - 1, sm), clock(sh, (sm + 30) % 60)]
        return _texts([text(f"{p}ต้องไปถึงโรงเรียนเวลา {clock(h, m)} ถ้าใช้เวลาเดินทาง "
                            f"{span} นาที {p}ต้องออกจากบ้านอย่างช้าที่สุดเวลาใด")], clock(sh, sm),
                      [w for w in dict.fromkeys(wrongs) if w != clock(sh, sm)], self.topic)


# ── More time (2026-11): minutes as hours and minutes, hours and minutes as minutes, days as hours, the year,
# the longest activity, and the weekday of a date ──
from otk.core.registry import question_type  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p3 import LEVEL  # noqa: E402

_WEEKDAYS = ("วันอาทิตย์", "วันจันทร์", "วันอังคาร", "วันพุธ", "วันพฤหัสบดี", "วันศุกร์", "วันเสาร์")


@question_type("math.minutes_to_hours_p3", display_name={"th": "เปลี่ยนนาทีเป็นชั่วโมงและนาที"},
               level=LEVEL, topic="เวลา")
class MinutesToHoursP3(ChoiceType):
    def compose(self, rng: Random):
        h, m = rng.randint(1, 5), rng.choice((5, 10, 15, 20, 25, 30, 35, 40, 45, 50))
        total = 60 * h + m
        right = f"{h} ชั่วโมง {m} นาที"
        # An hour taken as 100 minutes; an hour off either way; ten minutes off.
        wrongs = [f"{total // 100} ชั่วโมง {total % 100} นาที", f"{h + 1} ชั่วโมง {m} นาที",
                  f"{h} ชั่วโมง {m + 10} นาที", f"{h - 1} ชั่วโมง {m} นาที"]
        return f"{total} นาที เท่ากับเท่าใด", right, [w for w in dict.fromkeys(wrongs) if w != right][:3]


@question_type("math.hours_to_minutes_p3", display_name={"th": "เปลี่ยนชั่วโมงและนาทีเป็นนาที"},
               level=LEVEL, topic="เวลา")
class HoursToMinutesP3(WordProblem):
    def expr(self, rng: Random):
        h, m = rng.randint(1, 6), rng.randint(1, 59)
        right = 60 * h + m
        # An hour taken as 100 minutes; the minutes left out; the numbers added.
        return MathDraw("", str(right), prompt=f"{h} ชั่วโมง {m} นาที เท่ากับกี่นาที",
                        distractors=_story.keep(100 * h + m, 60 * h, h + m, right + 60, answer=right, lo=1))


@question_type("math.days_to_hours_p3", display_name={"th": "วันและชั่วโมง"},
               level=LEVEL, topic="เวลา")
class DaysToHoursP3(WordProblem):
    def expr(self, rng: Random):
        d, h = rng.randint(1, 6), rng.randint(0, 23)
        right = 24 * d + h
        prompt = f"{d} วัน{f' {h} ชั่วโมง' if h else ''} เท่ากับกี่ชั่วโมง"
        # A day taken as 12 or 60 hours; the numbers added.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(12 * d + h, 60 * d + h, d + h, right + 24, answer=right, lo=1))


@question_type("math.year_facts_p3", display_name={"th": "ปี เดือน สัปดาห์ และวัน"},
               level=LEVEL, topic="เวลา")
class YearFactsP3(ConceptBankType):
    ITEMS = [
        Concept("1 ปีมีกี่เดือน", "12 เดือน", ("10 เดือน", "24 เดือน", "52 เดือน")),
        Concept("1 ปีปกติมีกี่วัน", "365 วัน", ("360 วัน", "366 วัน", "300 วัน")),
        Concept("1 ปีมีประมาณกี่สัปดาห์", "52 สัปดาห์", ("12 สัปดาห์", "48 สัปดาห์", "100 สัปดาห์")),
        Concept("1 วันมีกี่ชั่วโมง", "24 ชั่วโมง", ("12 ชั่วโมง", "60 ชั่วโมง", "100 ชั่วโมง")),
        Concept("1 ชั่วโมงมีกี่นาที", "60 นาที", ("100 นาที", "24 นาที", "30 นาที")),
        Concept("ปีอธิกสุรทินมีกี่วัน", "366 วัน", ("365 วัน", "364 วัน", "360 วัน")),
    ]


@question_type("math.longest_activity_p3", display_name={"th": "กิจกรรมใดใช้เวลานานที่สุด"},
               level=LEVEL, topic="เวลา")
class LongestActivityP3(ChoiceType):
    _ACTS = ("อ่านหนังสือ", "เล่นดนตรี", "ทำการบ้าน", "เล่นกีฬา", "ช่วยงานบ้าน", "วาดภาพ")

    def compose(self, rng: Random):
        while True:
            lengths = [rng.choice((20, 25, 30, 35, 40, 45, 50, 55, 65, 75, 90)) for _ in range(4)]
            if len(set(lengths)) == 4:
                break
        acts = rng.sample(self._ACTS, 4)
        starts = [rng.randint(8, 18) * 60 + rng.choice((0, 10, 15, 30, 40)) for _ in range(4)]
        most = rng.random() < 0.5

        def clock(t: int) -> str:
            return f"{t // 60:02d}.{t % 60:02d} น."
        lines = [f"{a} {clock(s)} ถึง {clock(s + n)}" for a, s, n in zip(acts, starts, lengths)]
        pick = (max if most else min)(range(4), key=lambda i: lengths[i])
        return (f"{chr(10).join(lines)}\nกิจกรรมใดใช้เวลา{'นานที่สุด' if most else 'น้อยที่สุด'}",
                acts[pick], [a for i, a in enumerate(acts) if i != pick])


@question_type("math.calendar_date_weekday_p3", display_name={"th": "วันที่ในเดือนเดียวกันตรงกับวันอะไร"},
               level=LEVEL, topic="เวลา")
class CalendarDateWeekdayP3(ChoiceType):
    def compose(self, rng: Random):
        d1 = rng.randint(1, 10)
        w1 = rng.randrange(7)
        d2 = d1 + rng.randint(5, 20)
        right = _WEEKDAYS[(w1 + d2 - d1) % 7]
        # A day either side; the starting weekday.
        wrongs = [_WEEKDAYS[(w1 + d2 - d1 + 1) % 7], _WEEKDAYS[(w1 + d2 - d1 - 1) % 7], _WEEKDAYS[w1]]
        spare = _WEEKDAYS[(w1 + d2 - d1 + 2) % 7]
        return (f"วันที่ {d1} ของเดือนหนึ่งตรงกับ{_WEEKDAYS[w1]} วันที่ {d2} ของเดือนเดียวกันตรงกับวันอะไร",
                right, [w for w in dict.fromkeys([*wrongs, spare]) if w != right])
