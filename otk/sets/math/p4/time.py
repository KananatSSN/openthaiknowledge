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


# ── More time (2026-11): days as weeks and days, decades and centuries, the longest duration, race times in
# seconds, a stopwatch difference, days between two dates, and leap years ──

from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p4 import LEVEL  # noqa: E402


def _g(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


@question_type("math.days_to_weeks_p4", display_name={"th": "เปลี่ยนวันเป็นสัปดาห์และวัน"},
               level=LEVEL, topic="เวลา")
class DaysToWeeksP4(ChoiceType):
    def compose(self, rng: Random):
        w, d = rng.randint(2, 15), rng.randint(1, 6)
        total = 7 * w + d
        right = f"{w} สัปดาห์ {d} วัน"
        wrongs = [f"{total // 10} สัปดาห์ {total % 10} วัน", f"{w + 1} สัปดาห์ {d} วัน", f"{w} สัปดาห์ {d + 1} วัน",
                  f"{w - 1} สัปดาห์ {d} วัน"]
        return f"{total} วัน เท่ากับเท่าใด", right, [x for x in dict.fromkeys(wrongs) if x != right][:3]


@question_type("math.decade_century_p4", display_name={"th": "ทศวรรษ ศตวรรษ และสหัสวรรษ"},
               level=LEVEL, topic="เวลา")
class DecadeCenturyP4(ConceptBankType):
    ITEMS = [
        Concept("1 ทศวรรษมีกี่ปี", "10 ปี", ("100 ปี", "12 ปี", "1,000 ปี")),
        Concept("1 ศตวรรษมีกี่ปี", "100 ปี", ("10 ปี", "1,000 ปี", "50 ปี")),
        Concept("1 สหัสวรรษมีกี่ปี", "1,000 ปี", ("100 ปี", "10 ปี", "10,000 ปี")),
        Concept("3 ทศวรรษเท่ากับกี่ปี", "30 ปี", ("300 ปี", "3 ปี", "36 ปี")),
        Concept("2 ศตวรรษเท่ากับกี่ปี", "200 ปี", ("20 ปี", "2,000 ปี", "120 ปี")),
    ]


@question_type("math.longest_duration_p4", display_name={"th": "ระยะเวลาใดนานที่สุดหรือสั้นที่สุด"},
               level=LEVEL, topic="เวลา")
class LongestDurationP4(ChoiceType):
    def compose(self, rng: Random):
        while True:
            minutes = rng.sample(range(70, 300, 5), 4)
            if len({m // 60 for m in minutes}) >= 2:
                break
        texts = [(f"{m // 60} ชั่วโมง {m % 60} นาที" if m % 60 else f"{m // 60} ชั่วโมง") if rng.random() < 0.5
                 else f"{m} นาที" for m in minutes]
        most = rng.random() < 0.5
        pick = (max if most else min)(range(4), key=lambda i: minutes[i])
        return (f"ระยะเวลาใด{'นานที่สุด' if most else 'สั้นที่สุด'}", texts[pick],
                [t for i, t in enumerate(texts) if i != pick])


_MONTH_DAYS_P4 = {"มกราคม": 31, "กุมภาพันธ์": 28, "มีนาคม": 31, "เมษายน": 30, "พฤษภาคม": 31, "มิถุนายน": 30,
                  "กรกฎาคม": 31, "สิงหาคม": 31, "กันยายน": 30, "ตุลาคม": 31, "พฤศจิกายน": 30, "ธันวาคม": 31}


def _min_sec(t: int) -> str:
    m, s = divmod(t, 60)
    return f"{m} นาที {s} วินาที" if m else f"{s} วินาที"


@question_type("math.race_times_p4", display_name={"th": "รวมเวลาเป็นวินาที"},
               level=LEVEL, topic="เวลา")
class RaceTimesP4(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.randint(65, 299), rng.randint(40, 299)
        right = a + b
        p = rng.choice(_story.NAMES)
        prompt = f"{p}วิ่งรอบแรกใช้เวลา {_min_sec(a)} รอบที่สองใช้เวลา {_min_sec(b)} รวมสองรอบใช้เวลากี่วินาที"
        # A minute taken as 100 seconds; the minutes left out; the numbers added as written.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(100 * (a // 60) + a % 60 + 100 * (b // 60) + b % 60, a % 60 + b % 60,
                                                right + 60, right - 10, answer=right, lo=1))


@question_type("math.stopwatch_difference_p4", display_name={"th": "เวลาต่างกันกี่วินาที"},
               level=LEVEL, topic="เวลา")
class StopwatchDifferenceP4(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(130, 400)
        b = rng.randint(60, a - 5)
        right = a - b
        x, y = rng.sample(("ทีมแดง", "ทีมฟ้า", "ทีมเขียว", "ทีมเหลือง"), 2)
        prompt = (f"{x}ทำภารกิจเสร็จในเวลา {_min_sec(a)} {y}ทำเสร็จในเวลา {_min_sec(b)} "
                  f"{y}เร็วกว่า{x}กี่วินาที")
        # A minute taken as 100 seconds; added instead; a minute off.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(abs(100 * (a // 60) + a % 60 - 100 * (b // 60) - b % 60), a + b,
                                                right + 60, abs(right - 60), answer=right, lo=1))


@question_type("math.days_between_dates_p4", display_name={"th": "นับจำนวนวันระหว่างวันที่สองวัน"},
               level=LEVEL, topic="เวลา")
class DaysBetweenDatesP4(WordProblem):
    def expr(self, rng: Random):
        months = list(_MONTH_DAYS_P4)
        i = rng.randrange(11)
        m1, m2 = months[i], months[i + 1]
        d1 = rng.randint(1, _MONTH_DAYS_P4[m1] - 1)
        d2 = rng.randint(1, 28)
        right = (_MONTH_DAYS_P4[m1] - d1) + d2
        prompt = f"นับจากวันที่ {d1} {m1} ถึงวันที่ {d2} {m2} ของปีเดียวกัน (ปีปกติ) เป็นเวลากี่วัน"
        # Every month taken as 30 days; the dates subtracted; a day off.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep((30 - d1) + d2, abs(d2 - d1), right + 1, right - 1, answer=right, lo=1))


@question_type("math.leap_year_p4", display_name={"th": "ปีปกติและปีอธิกสุรทิน"},
               level=LEVEL, topic="เวลา")
class LeapYearP4(ConceptBankType):
    ITEMS = [
        Concept("ในปีอธิกสุรทิน เดือนกุมภาพันธ์มีกี่วัน", "29 วัน", ("28 วัน", "30 วัน", "31 วัน")),
        Concept("ในปีปกติ เดือนกุมภาพันธ์มีกี่วัน", "28 วัน", ("29 วัน", "30 วัน", "31 วัน")),
        Concept("ปีอธิกสุรทินมีกี่วัน", "366 วัน", ("365 วัน", "364 วัน", "360 วัน")),
        Concept("ปีอธิกสุรทินมีทุก ๆ กี่ปี (โดยทั่วไป)", "4 ปี", ("2 ปี", "10 ปี", "12 ปี")),
        Concept("ปีปกติมีกี่สัปดาห์กับอีกกี่วัน", "52 สัปดาห์ กับอีก 1 วัน",
                ("52 สัปดาห์พอดี", "50 สัปดาห์ กับอีก 15 วัน", "53 สัปดาห์พอดี")),
    ]


@question_type("math.age_year_month_difference_p4", display_name={"th": "หาผลต่างอายุเป็นปีและเดือน"},
               level=LEVEL, topic="เวลา")
class AgeYearMonthDifferenceP4(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-4/4539-4-2567-2-3.pdf, ข้อ 2, 10",))

    def compose(self, rng: Random):
        ay, am = rng.randint(20, 60), rng.randint(0, 11)
        by, bm = rng.randint(1, ay - 2), rng.randint(0, 11)
        a, b = 12 * ay + am, 12 * by + bm
        def say(months):
            y, m = divmod(months, 12)
            return f"{y} ปี {m} เดือน"
        if rng.randrange(2):
            stem = f"พี่อายุ {say(a)} น้องอายุ {say(b)} พี่อายุมากกว่าน้องเท่าไร"
        else:
            stem = f"พี่อายุ {say(a)} น้องอายุน้อยกว่าพี่ {say(b)} น้องอายุเท่าไร"
        answer = a - b
        # Borrow ten instead of twelve months; a year off; add ages.
        return stem, say(answer), [say(answer - 2), say(answer + 12), say(a + b)]


@question_type("math.monthly_reading_duration_p4", display_name={"th": "รวมเวลาอ่านหนังสือทุกวันตลอดเดือน"},
               level=LEVEL, topic="เวลา")
class MonthlyReadingDurationP4(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-4/4539-4-2567-2-3.pdf, ข้อ 3",))

    def compose(self, rng: Random):
        month, days = rng.choice(_MONTHS)
        per = rng.randint(15, 75)
        total = days * per
        def say(minutes):
            h, m = divmod(minutes, 60)
            return f"{h} ชั่วโมง {m} นาที"
        return (f"ในเดือน{month}ของปีปกติ อ่านหนังสือทุกวัน วันละ {per} นาที "
                "ใช้เวลาอ่านทั้งเดือนเท่าไร", say(total),
                [say(per), say(total - per), say(total + 60)])


@question_type("math.average_task_duration_p4", display_name={"th": "เฉลี่ยเวลาทำงานทีละชิ้น"},
               level=LEVEL, topic="เวลา")
class AverageTaskDurationP4(WordProblem):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-4/4539-4-2567-2-3.pdf, ข้อ 4",))

    def expr(self, rng: Random):
        count, each = rng.randint(2, 9), rng.randint(15, 120)
        total = count * each
        h, m = divmod(total, 60)
        return MathDraw("", str(total // count),
                        prompt=(f"ชาร์จไฟฉาย {count} กระบอก โดยชาร์จทีละกระบอก ใช้เวลารวม "
                                f"{h} ชั่วโมง {m} นาที เฉลี่ยกระบอกละกี่นาที"),
                        distractors=_story.keep(total, (100 * h + m) // count,
                                                total - count, each + 1, answer=each, lo=0))


@question_type("math.repeated_seconds_duration_p4", display_name={"th": "รวมเวลาจากจำนวนงานและวินาทีต่องาน"},
               level=LEVEL, topic="เวลา")
class RepeatedSecondsDurationP4(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-4/4539-4-2567-2-3.pdf, ข้อ 7",))

    def compose(self, rng: Random):
        count, seconds = rng.randint(20, 50), rng.randint(40, 100)
        total = count * seconds
        def say(s):
            m, s = divmod(s, 60)
            return f"{m} นาที {s} วินาที"
        wrong = [seconds, count + seconds, (total // 100) * 60 + total % 100, total + 60]
        return (f"ทำแบบฝึกหัด {count} ข้อ ใช้เวลาเฉลี่ยข้อละ {seconds} วินาที "
                "ใช้เวลารวมเท่าไร", say(total), list(dict.fromkeys(say(s) for s in wrong)))


@question_type("math.clock_hands_from_minutes_p4", display_name={"th": "ระบุตำแหน่งเข็มจากเวลาที่มีนาที"}, level={"th": "ป.4"}, topic="เวลา")
class ClockHandsFromMinutesP4(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-4/4540-4-2567-2-2.pdf, ข้อ 2",))

    def compose(self, rng: Random):
        hour,minute = rng.randrange(24),rng.randrange(5,60,5)
        h = hour%12 or 12
        mark = minute//5
        def label(short,long):
            return f"เข็มสั้นอยู่ระหว่างเลข {short} กับ {short%12+1} เข็มยาวชี้เลข {long}"
        return (f"เวลา {hour:02d}.{minute:02d} น. เข็มสั้นและเข็มยาวอยู่ตำแหน่งใด",
                label(h,mark),[label(h%12+1,mark),label(h,mark%11+1),label((h-2)%12+1,mark)])


@question_type("math.inclusive_date_weeks_p4", display_name={"th": "นับสัปดาห์โดยรวมวันเริ่มต้นและวันสุดท้าย"}, level={"th": "ป.4"}, topic="เวลา")
class InclusiveDateWeeksP4(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-4/4540-4-2567-2-2.pdf, ข้อ 3",))

    def compose(self, rng: Random):
        start,weeks = rng.randint(1,7),rng.randint(1,3)
        end = start+weeks*7-1
        month,_ = rng.choice(_MONTHS)
        return (f"ฝึกว่ายน้ำทุกวันตั้งแต่วันที่ {start} ถึงวันที่ {end} เดือน{month} "
                "นับรวมทั้งวันเริ่มต้นและวันสุดท้าย ฝึกทั้งหมดกี่สัปดาห์",
                str(weeks),[str(n) for n in dict.fromkeys((weeks-1,weeks+1,weeks*7,weeks*7-1)) if n != weeks])


@question_type("math.approximate_months_days_p4", display_name={"th": "เปลี่ยนวันเป็นเดือนและวันตามเกณฑ์ที่กำหนด"}, level={"th": "ป.4"}, topic="เวลา")
class ApproximateMonthsDaysP4(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-4/4540-4-2567-2-2.pdf, ข้อ 6",))

    def compose(self, rng: Random):
        months,days = rng.randint(1,8),rng.randint(1,29)
        total = months*30+days
        def label(m,d):
            return f"{m} เดือน {d} วัน"
        return (f"ระยะเวลา {total} วัน คิดเป็นกี่เดือนกับอีกกี่วัน กำหนดให้หนึ่งเดือนเท่ากับ 30 วัน",
                label(*divmod(total,30)),[label(*divmod(total,31)),label(months+1,days),label(months,days+1)])


@question_type("math.schedule_duration_p4", display_name={"th": "หาระยะเวลากิจกรรมจากตารางเวลา"}, level={"th": "ป.4"}, topic="เวลา")
class ScheduleDurationP4(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-4/4540-4-2567-2-2.pdf, ข้อ 7–8",))

    def compose(self, rng: Random):
        activities = ("คิดเลขเร็ว","ลูกคิด","ภาษาไทย","วาดภาพ")
        start = rng.randrange(450,545,5)
        rows=[]
        for activity in activities:
            end = start+rng.randrange(20,180,5)
            rows.append((activity,start,end))
            start=end
        activity,begin,end = rng.choice(rows)
        minutes = end-begin
        as_minutes = rng.choice((False,True))
        def time(t):
            return f"{t//60:02d}.{t%60:02d}"
        def label(t):
            return str(t) if as_minutes else f"{t//60} ชั่วโมง {t%60} นาที"
        data = " ; ".join(f"{name} | {time(a)} | {time(b)}" for name,a,b in rows)
        question = "กี่นาที" if as_minutes else "กี่ชั่วโมงกี่นาที"
        return ("ตารางอบรมในวันเดียวกัน (กิจกรรม | เริ่ม | จบ): "+data+
                f" กิจกรรม{activity}ใช้เวลา{question}",label(minutes),
                [label(minutes+60),label(minutes+5),label(minutes-5)])


@question_type("math.departure_cutoff_p4", display_name={"th": "เลือกเที่ยวรถที่ออกก่อนเวลาที่กำหนด"}, level={"th": "ป.4"}, topic="เวลา")
class DepartureCutoffP4(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-4/4540-4-2567-2-2.pdf, ข้อ 9",))

    def compose(self, rng: Random):
        cutoff = rng.randrange(360,780,5)
        times = [cutoff-rng.randrange(5,125,5),cutoff,*[cutoff+d for d in rng.sample(range(5,125,5),2)]]
        rng.shuffle(times)
        names = ("สาย ก","สาย ข","สาย ค","สาย ง")
        def time(t):
            return f"{t//60:02d}.{t%60:02d}"
        rows=[]
        for name,departure in zip(names,times):
            arrival = departure+rng.randrange(360,845,5)
            day = "วันถัดไป" if arrival>=1440 else "วันเดียวกัน"
            rows.append(f"{name} | {time(departure)} | {time(arrival%1440)} {day}")
        right = names[next(i for i,t in enumerate(times) if t<cutoff)]
        return ("ตารางรถ (สาย | เวลาออกวันนี้ | เวลาถึง): "+" ; ".join(rows)+
                f" ต้องการรถที่ออกก่อน {time(cutoff)} น. ต้องเลือกสายใด (ออกตรงเวลานี้ไม่นับว่าก่อน)",
                right,[name for name in names if name != right])


@question_type("math.fractional_year_weeks_p4", display_name={"th": "เปลี่ยนปีและเศษส่วนของปีเป็นสัปดาห์ตามเกณฑ์"},
               level=LEVEL, topic="เวลา")
class FractionalYearWeeksP4(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-4/4540-4-2567-2-2.pdf, ข้อ 4",))

    def compose(self, rng: Random):
        years,quarters = rng.randint(1,8),rng.randint(1,3)
        description = f"{years} ปีครึ่ง" if quarters==2 else f"{years} ปี กับอีก {quarters}/4 ปี"
        answer = years*52+quarters*13
        return (f"ตามเกณฑ์หนึ่งปีคิดเป็น 52 สัปดาห์ ระยะเวลา {description} คิดเป็นกี่สัปดาห์ตามเกณฑ์นี้",
                str(answer),[str(years*52),str(years*52+quarters),str(years*12+quarters*3)])

_DAYS = ("จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์")


@question_type("math.periodic_schedule_p4", display_name={"th": "นับครั้งของกิจกรรมที่ทำตามวันในสัปดาห์"},
               level={"th": "ป.4"}, topic=_TIME_TOPIC)
class PeriodicScheduleP4(ChoiceType):
    """Count each weekday's occurrences in the span (whole weeks plus the leftover days),
    then multiply by what happens on that day."""
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/exam-venue/srinakharinwirot-patumwan-demonstration-school/23472-1-2568-21-BKN.pdf, ข้อ 5",
        "openthaiknowledge-bank/mathematics/exam-venue/mahidol-wittayanusorn/8519-MWIT35_R1.pdf, ข้อ 7"))

    def compose(self, rng: Random):
        days = rng.randint(15, 40)
        start = rng.randrange(7)
        busy = sorted(rng.sample(range(7), rng.randint(2, 4)))
        each = rng.randint(2, 5)
        count = sum(1 for d in range(days) if (start + d) % 7 in busy)
        answer = count * each
        weeks = days // 7
        # Whole weeks only; every day counted; leftover days all counted; one per busy day.
        pool = (weeks * len(busy) * each, days * each, (weeks * len(busy) + days % 7) * each, count)
        wrongs = [w for w in dict.fromkeys(pool) if w != answer]
        for extra in (answer + each, answer - each, answer + 2 * each):
            if len(wrongs) >= 3:
                break
            if extra != answer and extra not in wrongs and extra > 0:
                wrongs.append(extra)
        busy_days = " ".join("วัน" + _DAYS[d] for d in busy)
        stem = (f"วันแรกของช่วงนี้เป็นวัน{_DAYS[start]} ตลอด {days} วัน (นับวันแรกด้วย) "
                f"น้องเขียนจดหมายวันละ {each} ฉบับเฉพาะ{busy_days} น้องเขียนจดหมายทั้งหมดกี่ฉบับ")
        return stem, str(answer), [str(w) for w in wrongs][:4]
