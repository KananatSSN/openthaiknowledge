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
