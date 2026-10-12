"""การนำเสนอข้อมูลเชิงปริมาณ

คณิตศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ค 3.1 ม.6/1

Sets moved here from: math_chapters.
"""

from __future__ import annotations

from decimal import Decimal
from fractions import Fraction
from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.math_chapters import M6, NL
from otk.sets._support.math_m4 import maths as _num_maths

PROVENANCE = Provenance("original")


_GROUPED_TOPIC = "การนำเสนอข้อมูลเชิงปริมาณ"


_MEASURED = ("คะแนนสอบวิชาคณิตศาสตร์", "น้ำหนักของนักเรียน (กิโลกรัม)", "อายุของผู้เข้าชมนิทรรศการ (ปี)",
             "ความสูงของต้นกล้า (เซนติเมตร)")


def _num(v: Fraction) -> str:
    return format((Decimal(v.numerator) / Decimal(v.denominator)).normalize(), "f")


def _grouped(rng: Random, totals: tuple[int, ...] = ()):
    """Five classes of equal width; with ``totals`` the frequencies add to one
    of them, so relative frequencies are terminating decimals."""
    width = rng.choice((5, 10))
    start = rng.choice((10, 20, 30, 40, 50))
    bins = [(start + i * width, start + (i + 1) * width - 1) for i in range(5)]
    while True:
        freq = [rng.randint(2, 14) for _ in bins]
        if not totals or sum(freq) in totals:
            break
    lines = [f"ตารางแจกแจงความถี่ของ{rng.choice(_MEASURED)}", "อันตรภาคชั้น | ความถี่"]
    lines += [f"{a} – {b} | {f}" for (a, b), f in zip(bins, freq)]
    return bins, freq, NL.join(lines)


@question_type("math.class_boundaries_m6", display_name={"th": "ขอบชั้นและจุดกึ่งกลางชั้นของอันตรภาคชั้น"},
               level=M6, topic=_GROUPED_TOPIC)
class ClassBoundariesM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        bins, _, table = _grouped(rng)
        a, b = rng.choice(bins)
        cls = f"{a} – {b}"
        half = Fraction(1, 2)
        kind = rng.randrange(3)
        if kind == 0:
            mid = Fraction(a + b, 2)
            ask, right = "จุดกึ่งกลางชั้น", mid
            wrongs = [Fraction(a), Fraction(b), mid + half]
        elif kind == 1:
            ask, right = "ขอบล่าง", a - half
            wrongs = [Fraction(a), Fraction(a - 1), a + half]
        else:
            ask, right = "ขอบบน", b + half
            wrongs = [Fraction(b), Fraction(b + 1), b - half]
        return _num_maths([text(table), text(f"{ask}ของอันตรภาคชั้น {cls} เท่ากับเท่าใด")], _num(right),
                          [_num(w) for w in wrongs], self.topic)


@question_type("math.relative_frequency_m6", display_name={"th": "ความถี่สัมพัทธ์"},
               level=M6, topic=_GROUPED_TOPIC)
class RelativeFrequencyM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        bins, freq, table = _grouped(rng, (20, 25, 40, 50))
        total = sum(freq)
        j = rng.randrange(1, 5)
        f, cum = freq[j], sum(freq[:j + 1])
        cls = f"{bins[j][0]} – {bins[j][1]}"
        if rng.random() < 0.5:
            right = Fraction(f, total)
            ask = f"ความถี่สัมพัทธ์ของอันตรภาคชั้น {cls} เท่ากับเท่าใด"
            # Over 100, the cumulative count, and the rest of the data.
            wrongs = [Fraction(f, 100), Fraction(cum, total), 1 - right]
        else:
            right = Fraction(100 * f, total)
            ask = f"ข้อมูลในอันตรภาคชั้น {cls} คิดเป็นร้อยละเท่าใดของข้อมูลทั้งหมด"
            wrongs = [Fraction(f), Fraction(100 * cum, total), 100 - right]
        return _num_maths([text(table), text(ask)], _num(right), [_num(w) for w in wrongs], self.topic)


@question_type("math.cumulative_frequency_m6", display_name={"th": "ความถี่สะสมและความถี่สะสมสัมพัทธ์"},
               level=M6, topic=_GROUPED_TOPIC)
class CumulativeFrequencyM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        bins, freq, table = _grouped(rng, (20, 25, 40, 50))
        total = sum(freq)
        j = rng.randrange(1, 4)
        cum, prev = sum(freq[:j + 1]), sum(freq[:j])
        upper = _num(Fraction(2 * bins[j][1] + 1, 2))
        kind = rng.randrange(3)
        if kind == 0:
            right = Fraction(cum)
            ask = f"ความถี่สะสมของอันตรภาคชั้น {bins[j][0]} – {bins[j][1]} เท่ากับเท่าใด"
            wrongs = [Fraction(freq[j]), Fraction(prev), Fraction(total - prev)]
        elif kind == 1:
            right = Fraction(total - cum)
            ask = f"ข้อมูลที่มีค่ามากกว่า {upper} มีกี่ค่า"
            wrongs = [Fraction(cum), Fraction(total - prev), Fraction(freq[j + 1])]
        else:
            right = Fraction(100 * cum, total)
            ask = f"ข้อมูลที่มีค่าน้อยกว่า {upper} คิดเป็นร้อยละเท่าใดของข้อมูลทั้งหมด (ความถี่สะสมสัมพัทธ์)"
            wrongs = [Fraction(100 * freq[j], total), Fraction(100 * prev, total), Fraction(cum)]
        return _num_maths([text(table), text(ask)], _num(right), [_num(w) for w in wrongs], self.topic)
