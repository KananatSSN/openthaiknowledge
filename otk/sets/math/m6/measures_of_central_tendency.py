"""ค่ากลางของข้อมูล

คณิตศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ค 3.1 ม.6/*

Sets moved here from: math_apply_stage, math_bank_stats, math_formats_hi, math_m6.
"""

from __future__ import annotations

from collections import Counter
from decimal import Decimal
from fractions import Fraction
from functools import lru_cache
from itertools import combinations_with_replacement
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.sets._support.math_bank_stats import M6, _num_q, median, num
from otk.sets._support.math_diagrams import _text_q
from otk.sets._support.math_m4 import maths
from otk.sets._support.math_m4 import maths as _maths
from otk.sets._support.math_m6 import _dec


def _d2(v: Fraction) -> str:
    return f"{Decimal(v.numerator) / Decimal(v.denominator):.2f}"


CENTRAL = "ค่ากลางของข้อมูล"


def mean(xs) -> Fraction:
    return Fraction(sum(xs), len(xs))


def unique_mode(xs):
    """The single mode, or None when there is none (all equal counts) or several."""
    c = Counter(xs)
    top = max(c.values())
    ms = [v for v, k in c.items() if k == top]
    return ms[0] if len(ms) == 1 and top > 1 else None


def data_tex(xs) -> str:
    return " ,\\ ".join(x if isinstance(x, str) else num(x) for x in xs)


def x_for_mean_equals_mode(known: list[Fraction]) -> list[Fraction]:
    """Every x making mean(known + [x]) equal the (single) mode of known + [x]."""
    out = []
    for x in set(known):
        data = [*known, x]
        if unique_mode(data) == x and mean(data) == x:
            out.append(x)
    return sorted(out)


def x_for_median_minus_mode(known: list[int], gap: int, lo: int, hi: int) -> list[int]:
    """Every integer x in [lo, hi] with median − mode = gap (a single mode required)."""
    out = []
    for x in range(lo, hi + 1):
        data = [*known, x]
        m = unique_mode(data)
        if m is not None and median(data) - m == gap:
            out.append(x)
    return out


@lru_cache(maxsize=None)
def _multisets(n: int, hi: int) -> tuple[tuple[int, ...], ...]:
    return tuple(combinations_with_replacement(range(1, hi + 1), n))


def matching_sets(n: int, hi: int, mode: int, med: Fraction, rng_: int) -> list[tuple[int, ...]]:
    """Sorted n-tuples of positive integers ≤ hi with the given single mode, median and range."""
    return [s for s in _multisets(n, hi)
            if s[-1] - s[0] == rng_ and median(s) == med and unique_mode(s) == mode]


_MEAN, _MEDIAN, _MODE = "ค่าเฉลี่ยเลขคณิต", "มัธยฐาน", "ฐานนิยม"


NL = chr(10)


_CENTRE_TOPIC = "ค่ากลางของข้อมูล"


def _freq_table(rng: Random, label: str = "คะแนน"):
    values = sorted(rng.sample(range(1, 11), 5))
    freq = [rng.randint(1, 9) for _ in values]
    lines = [f"{label} (x) | ความถี่ (f)"] + [f"{x} | {f}" for x, f in zip(values, freq)]
    return values, freq, NL.join(lines)


@question_type("math.choose_average_m6", display_name={"th": "เลือกค่ากลางที่เหมาะสมกับข้อมูล"},
               level={"th": "ม.6"}, topic="ค่ากลางของข้อมูล")
class ChooseAverageM6(QuestionType):
    """An outlier calls for the median, categories for the mode, a balanced
    numeric set for the mean."""

    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            pay = sorted(rng.sample(range(12, 26), 6))
            boss = rng.randint(150, 300)
            data = ", ".join(f"{p * 1000:,}" for p in pay + [boss])
            stem = (f"เงินเดือน (บาท) ของพนักงานร้านหนึ่ง 7 คน คือ {data} "
                    "ค่ากลางใดเหมาะสมที่สุดที่จะใช้เป็นตัวแทนเงินเดือนของพนักงานร้านนี้")
            right = _MEDIAN
        elif kind == 1:
            what = rng.choice((("สีเสื้อที่นักเรียนชอบ", "แดง ฟ้า ฟ้า เขียว ฟ้า ชมพู แดง ฟ้า"),
                               ("ขนาดรองเท้าที่ขายได้ในหนึ่งวัน", "38 39 39 40 39 41 38 39 42"),
                               ("รสไอศกรีมที่ลูกค้าสั่ง", "วานิลลา ช็อกโกแลต วานิลลา สตรอว์เบอร์รี วานิลลา")))
            stem = (f"ข้อมูล{what[0]}: {what[1]} ถ้าต้องการทราบว่าสิ่งใดเป็นที่นิยมมากที่สุด "
                    "ควรใช้ค่ากลางใด")
            right = _MODE
        else:
            centre = rng.randint(55, 75)
            offsets = rng.sample((-6, -4, -3, -1, 1, 3, 4, 6), 6)
            data = ", ".join(str(centre + o) for o in offsets)
            stem = (f"คะแนนสอบของนักเรียน 6 คน คือ {data} ข้อมูลไม่มีค่าที่ผิดปกติ "
                    "ค่ากลางใดใช้ข้อมูลทุกค่าและเหมาะสมที่สุด")
            right = _MEAN
        return _text_q([text(stem)], right,
                       [x for x in (_MEAN, _MEDIAN, _MODE, "พิสัย") if x != right], self.topic)
ChooseAverageM6.PROVENANCE = Provenance("original")


@question_type("math.mean_frequency_table_m6",
               display_name={"th": "ค่าเฉลี่ยเลขคณิตจากตารางแจกแจงความถี่"},
               level=M6, topic=_CENTRE_TOPIC)
class MeanFrequencyTableM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        # (what was counted, the column label, what the mean is of)
        title, label, of = rng.choice((
            ("คะแนนสอบย่อยของนักเรียนกลุ่มหนึ่ง", "คะแนน", "คะแนน"),
            ("จำนวนหนังสือที่นักเรียนแต่ละคนอ่านในเดือนหนึ่ง", "จำนวนเล่ม", "จำนวนหนังสือที่อ่าน"),
            ("จำนวนสมาชิกในครอบครัวของนักเรียนห้องหนึ่ง", "จำนวนคน", "จำนวนสมาชิกในครอบครัว"),
            ("จำนวนครั้งที่นักกีฬาแต่ละคนชู้ตลูกบาสเกตบอลลงห่วง", "จำนวนครั้ง", "จำนวนครั้งที่ชู้ตลง"),
        ))
        while True:
            values, freq, table = _freq_table(rng, label)
            n = sum(freq)
            mean = Fraction(sum(x * f for x, f in zip(values, freq)), n)
            if (mean * 100).denominator == 1:
                break
        # Averaging the scores without weights, and Σfx over the number of rows.
        wrongs = [_dec(Fraction(sum(values), len(values))),
                  _dec(Fraction(sum(x * f for x, f in zip(values, freq)), len(values))),
                  _dec(mean + Fraction(1, 2)), _dec(mean - Fraction(1, 2))]
        return _maths([text(f"ตารางแจกแจงความถี่ของ{title}" + NL + table),
                       text(f"ค่าเฉลี่ยเลขคณิตของ{of}เท่ากับเท่าใด")], _dec(mean), wrongs, self.topic)
MeanFrequencyTableM6.PROVENANCE = Provenance("original")


@question_type("math.weighted_mean_m6", display_name={"th": "ค่าเฉลี่ยเลขคณิตถ่วงน้ำหนักและค่าเฉลี่ยรวม"},
               level=M6, topic=_CENTRE_TOPIC)
class WeightedMeanM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.5:
            credits = [rng.choice((1, 2, 3)) for _ in range(4)]
            grades = [rng.choice((1, 1.5, 2, 2.5, 3, 3.5, 4)) for _ in range(4)]
            gpa = Fraction(sum(Fraction(g).limit_denominator(2) * c for g, c in zip(grades, credits)), sum(credits))
            rows = NL.join(f"วิชาที่ {i + 1} | {c} หน่วยกิต | เกรด {g:g}" for i, (c, g) in enumerate(zip(credits, grades)))
            wrongs = [_dec(Fraction(sum(Fraction(g).limit_denominator(2) for g in grades), 4)),
                      _dec(gpa + Fraction(1, 4)), _dec(gpa - Fraction(1, 4)),
                      _dec(Fraction(sum(Fraction(g).limit_denominator(2) * c for g, c in zip(grades, credits)), 4))]
            return _maths([text("ผลการเรียนของนักเรียนคนหนึ่ง" + NL + rows),
                           text("เกรดเฉลี่ยของภาคเรียนนี้ (ทศนิยม 2 ตำแหน่ง) เท่ากับเท่าใด")],
                          _dec(gpa), [w for w in wrongs if w != _dec(gpa)], self.topic)
        if rng.random() < 0.4:
            # Marks weighted by their share of the course.
            weights = rng.choice(((20, 30, 50), (30, 30, 40), (10, 40, 50), (25, 25, 50)))
            marks = [rng.randint(45, 95) for _ in range(3)]
            mean = Fraction(sum(w * m for w, m in zip(weights, marks)), 100)
            parts = ("คะแนนเก็บ", "สอบกลางภาค", "สอบปลายภาค")
            rows = NL.join(f"{p} | น้ำหนักร้อยละ {w} | ได้ {m} คะแนน (เต็ม 100)"
                           for p, w, m in zip(parts, weights, marks))
            return _maths([text(f"{rng.choice(_story.NAMES)}มีผลการเรียนวิชาหนึ่งดังนี้" + NL + rows),
                           text("คะแนนเฉลี่ยถ่วงน้ำหนักของวิชานี้ (ทศนิยม 2 ตำแหน่ง) เท่ากับเท่าใด")],
                          _dec(mean), [_dec(Fraction(sum(marks), 3)), _dec(mean + 1), _dec(mean - 1)], self.topic)
        n1, n2 = rng.randint(10, 40), rng.randint(10, 40)
        m1, m2 = rng.randint(50, 80), rng.randint(50, 80)
        combined = Fraction(n1 * m1 + n2 * m2, n1 + n2)
        group, member, unit, measure = rng.choice((
            ("ห้อง", "นักเรียน", "คน", "ได้คะแนนเฉลี่ย {m} คะแนน"),
            ("ทีม", "นักกีฬา", "คน", "หนักเฉลี่ย {m} กิโลกรัม"),
            ("กล่อง", "มะม่วง", "ผล", "หนักเฉลี่ยผลละ {m} กรัม"),
        ))
        # Mangoes weigh in hundreds of grams: the same means, ten times over.
        scale = 10 if unit == "ผล" else 1
        combined *= scale
        first, second = measure.format(m=m1 * scale), measure.format(m=m2 * scale)
        return _maths([text(f"{group}แรกมี{member} {n1} {unit} {first} {group}ที่สองมี{member} {n2} {unit} "
                            f"{second} ค่าเฉลี่ยรวมของทั้งสอง{group} (ทศนิยม 2 ตำแหน่ง) เท่ากับเท่าใด")],
                      _dec(combined), [_dec(Fraction(m1 + m2, 2) * scale),
                                       _dec(combined + 1), _dec(combined - 1)],
                      self.topic)
WeightedMeanM6.PROVENANCE = Provenance("original")


@question_type("math.mean_word_m6", display_name={"th": "โจทย์ปัญหาค่าเฉลี่ยเลขคณิต (เพิ่ม ลด และคะแนนที่ต้องได้)"},
               level={"th": "ม.6"}, topic="ค่ากลางของข้อมูล")
class MeanWordM6(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        n, m = rng.randint(5, 30), rng.randint(40, 80)
        if kind == 0:
            v = rng.randint(20, 99)
            new = Fraction(n * m + v, n + 1)
            stem = (f"นักเรียน {n} คนมีน้ำหนักเฉลี่ย {m} กิโลกรัม มีนักเรียนใหม่หนัก {v} กิโลกรัมเข้ามาเพิ่ม "
                    f"น้ำหนักเฉลี่ยใหม่เท่ากับกี่กิโลกรัม (ทศนิยม 2 ตำแหน่ง)")
            wrongs = [Fraction(m + v, 2), Fraction(n * m + v, n), new + 1]
        elif kind == 1:
            v = rng.randint(20, 99)
            new = Fraction(n * m - v, n - 1)
            stem = (f"ข้อมูล {n} จำนวนมีค่าเฉลี่ย {m} ถ้าตัดข้อมูลที่มีค่า {v} ออกไปหนึ่งจำนวน "
                    f"ค่าเฉลี่ยของข้อมูลที่เหลือเท่ากับเท่าใด (ทศนิยม 2 ตำแหน่ง)")
            wrongs = [Fraction(m - v), Fraction(n * m - v, n), new - 1]
        else:
            # need = target·(t + 1) − now·t, kept within a score out of 100.
            tests, target = rng.randint(3, 6), rng.randint(60, 85)
            now = target - rng.randint(1, max(1, (100 - target) // tests))
            need = Fraction(target * (tests + 1) - now * tests)
            stem = (f"{rng.choice(_story.NAMES)}สอบย่อยไปแล้ว {tests} ครั้ง ได้คะแนนเฉลี่ย {now} คะแนน "
                    f"ครั้งที่ {tests + 1} ต้องได้กี่คะแนน คะแนนเฉลี่ยทั้ง {tests + 1} ครั้งจึงจะเป็น {target} คะแนน "
                    f"(ทศนิยม 2 ตำแหน่ง)")
            new = need
            wrongs = [Fraction(target), Fraction(2 * target) - Fraction(now), need + tests]
        return maths([text(stem)], _d2(new), [_d2(w) for w in wrongs], self.topic)
MeanWordM6.PROVENANCE = Provenance("original")


@question_type("math.stats_data_conditions_m6",
               display_name={"th": "หาข้อมูลที่ไม่ทราบจากเงื่อนไขของค่ากลาง"},
               level=M6, topic=CENTRAL)
class StatsDataConditionsM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            while True:
                m = rng.randint(8, 30)
                devs = rng.sample([Fraction(v, 2) for v in range(1, 13)], 4)
                known = [Fraction(m)] + [m + d for d in devs] + [m - d for d in devs]
                if len(set(known)) == len(known) and x_for_mean_equals_mode(known) == [m]:
                    break
            rng.shuffle(known)
            stem = [text("ข้อมูลชุดหนึ่งประกอบด้วย"), content_math(data_tex(["x", *known])),
                    text("ถ้าค่าเฉลี่ยเลขคณิตของข้อมูลชุดนี้เท่ากับฐานนิยม แล้ว x มีค่าเท่ากับเท่าใด")]
            s = sorted(known)
            # The median of the known values; the value next to it; the mean with x left out as 0.
            named = [median(known), s[len(s) // 2 + 1], sum(known) / (len(known) + 1)]
            return _num_q(stem, m, named, self.topic)
        if kind == 1:
            while True:
                n = rng.choice((8, 10))
                known = [rng.randint(5, 18) for _ in range(n - 1)]
                gap = rng.choice((1, 2, 3))
                xs = x_for_median_minus_mode(known, gap, 1, 20)
                if len(xs) == 1:
                    break
            x = xs[0]
            data = [*known, x]
            stem = [text(f"ให้ x เป็นจำนวนเต็มบวก ข้อมูลคะแนนสอบ (เต็ม 20 คะแนน) ของนักเรียน {n} คน เป็นดังนี้"),
                    content_math(data_tex(["x", *known])),
                    text(f"ถ้าข้อมูลชุดนี้มีมัธยฐานมากกว่าฐานนิยมอยู่ {gap} แล้วค่าเฉลี่ยเลขคณิตเท่ากับเท่าใด")]
            # The mean without x; x taken as the mode; the median itself.
            named = [mean(known), mean([*known, unique_mode(data)]), median(data)]
            return _num_q(stem, mean(data), named, self.topic)
        while True:
            n = rng.choice((4, 5))
            hi = 15 if n == 5 else 20
            data = tuple(sorted(rng.randint(1, hi) for _ in range(n)))
            mo = unique_mode(data)
            if mo is None:
                continue
            ask = rng.choice(("sum", "max"))
            sets = matching_sets(n, hi, mo, median(data), data[-1] - data[0])
            values = {sum(s) if ask == "sum" else s[-1] for s in sets}
            if len(values) == 1:
                break
        right = values.pop()
        what = "ผลบวกของข้อมูลชุดนี้" if ask == "sum" else "ค่าที่มากที่สุดของข้อมูลชุดนี้"
        stem = [text(f"ข้อมูลชุดหนึ่งเป็นจำนวนเต็มบวก {n} จำนวน ถ้าฐานนิยมเท่ากับ {mo} มัธยฐานเท่ากับ"),
                content_math(num(median(data))), text(f"และพิสัยเท่ากับ {data[-1] - data[0]} แล้ว{what}เท่ากับเท่าใด")]
        # n × median; mode + range; n × mode.
        named = [n * median(data), mo + data[-1] - data[0], n * mo] if ask == "sum" else \
            [median(data) + data[-1] - data[0], mo + data[-1] - data[0] + 1, data[-1] - data[0]]
        return _num_q(stem, right, named, self.topic)
StatsDataConditionsM6.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/16 สถิติ',))


@question_type("math.median_mode_frequency_m6",
               display_name={"th": "มัธยฐานและฐานนิยมจากตารางแจกแจงความถี่"},
               level=M6, topic=_CENTRE_TOPIC)
class MedianModeFrequencyM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        values, freq, table = _freq_table(rng)
        while freq.count(max(freq)) > 1:
            values, freq, table = _freq_table(rng)
        data = [x for x, f in zip(values, freq) for _ in range(f)]
        n = len(data)
        if rng.random() < 0.5:
            mode = values[freq.index(max(freq))]
            return _maths([text("ตารางแจกแจงความถี่" + NL + table), text("ฐานนิยมของข้อมูลนี้เท่ากับเท่าใด")],
                          str(mode), [str(max(freq)), str(values[len(values) // 2]), str(max(values)),
                                      str(mode + 1)], self.topic)
        med = Fraction(data[n // 2]) if n % 2 else Fraction(data[n // 2 - 1] + data[n // 2], 2)
        # The middle row of the table, and the middle frequency.
        wrongs = [_dec(Fraction(values[2])), _dec(Fraction(sorted(freq)[2])),
                  _dec(Fraction(sum(data), n)), _dec(med + 1)]
        return _maths([text("ตารางแจกแจงความถี่" + NL + table), text("มัธยฐานของข้อมูลนี้เท่ากับเท่าใด")],
                      _dec(med), wrongs, self.topic)
MedianModeFrequencyM6.PROVENANCE = Provenance("original")
