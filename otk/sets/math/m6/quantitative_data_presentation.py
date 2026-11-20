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


from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m6 import M6 as LEVEL  # noqa: E402


def _nz6(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk6(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk6(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk6(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt6(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk6(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk6(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))


def _num6(v) -> str:
    """A terminating decimal without trailing zeros: Fraction(25, 2) -> 12.5."""
    v = Fraction(v)
    sign = "-" if v < 0 else ""
    v = abs(v)
    whole, rem = divmod(v.numerator, v.denominator)
    if not rem:
        return f"{sign}{whole}"
    digits = ""
    for _ in range(6):
        rem *= 10
        d, rem = divmod(rem, v.denominator)
        digits += str(d)
        if not rem:
            break
    return f"{sign}{whole}.{digits.rstrip('0')}"


def _dk6(*values, answer) -> list[str]:
    """Distinct decimal distractors, the answer left out."""
    return _tk6(*(_num6(v) for v in values), answer=_num6(answer))

# ── More frequency tables (2026-11): the class width, the total, a cumulative frequency, a relative frequency
# as a percent, the modal class, how many classes, and a point of the frequency polygon ──


@question_type("math.class_width_m6", display_name={"th": "ความกว้างของอันตรภาคชั้น"}, level=LEVEL, topic=_GROUPED_TOPIC)
class ClassWidthM6(WordProblem):
    def expr(self, rng: Random):
        bins, _, table = _grouped(rng)
        a, b = bins[0]
        right = b - a + 1
        # The written gap; the upper limit; twice.
        return MathDraw("", str(right), prompt=f"{table}{NL}ความกว้างของอันตรภาคชั้นเท่ากับเท่าใด",
                        distractors=_nk6(b - a, b, 2 * right, right + 1, answer=right, lo=1))


@question_type("math.total_frequency_m6", display_name={"th": "จำนวนข้อมูลทั้งหมดจากตารางแจกแจงความถี่"}, level=LEVEL,
               topic=_GROUPED_TOPIC)
class TotalFrequencyM6(WordProblem):
    def expr(self, rng: Random):
        bins, freq, table = _grouped(rng)
        right = sum(freq)
        return MathDraw("", str(right), prompt=f"{table}{NL}ข้อมูลชุดนี้มีทั้งหมดกี่ค่า",
                        distractors=_nk6(len(freq), max(freq) * len(freq), right - freq[0], right + freq[-1], answer=right, lo=1))


@question_type("math.cumulative_of_class_m6", display_name={"th": "ความถี่สะสมของอันตรภาคชั้น"}, level=LEVEL, topic=_GROUPED_TOPIC)
class CumulativeOfClassM6(WordProblem):
    def expr(self, rng: Random):
        bins, freq, table = _grouped(rng)
        i = rng.randint(1, 3)
        a, b = bins[i]
        right = sum(freq[:i + 1])
        # The class's own frequency; one class short; one class too many.
        return MathDraw("", str(right), prompt=f"{table}{NL}ความถี่สะสมของอันตรภาคชั้น {a} – {b} เท่ากับเท่าใด",
                        distractors=_nk6(freq[i], sum(freq[:i]), sum(freq[:i + 2]), sum(freq[i:]), answer=right, lo=1))


@question_type("math.relative_percent_m6", display_name={"th": "ความถี่สัมพัทธ์เป็นร้อยละ"}, level=LEVEL, topic=_GROUPED_TOPIC)
class RelativePercentM6(WordProblem):
    def expr(self, rng: Random):
        bins, freq, table = _grouped(rng, totals=(20, 25, 50))
        i = rng.randrange(5)
        a, b = bins[i]
        total = sum(freq)
        right = freq[i] * 100 // total
        # The frequency itself; out of a hundred items; the cumulative share.
        return MathDraw("", str(right), prompt=f"{table}{NL}อันตรภาคชั้น {a} – {b} มีความถี่สัมพัทธ์คิดเป็นร้อยละเท่าใด",
                        distractors=_nk6(freq[i], right // 2 if right > 1 else right + 3, sum(freq[:i + 1]) * 100 // total,
                                         right + 5, answer=right, lo=1))


@question_type("math.modal_class_m6", display_name={"th": "อันตรภาคชั้นที่มีความถี่สูงสุด"}, level=LEVEL, topic=_GROUPED_TOPIC)
class ModalClassM6(ChoiceType):
    def compose(self, rng: Random):
        while True:
            bins, freq, table = _grouped(rng)
            if freq.count(max(freq)) == 1:
                break
        names = [f"{a} – {b}" for a, b in bins]
        pick = freq.index(max(freq))
        return f"{table}{NL}อันตรภาคชั้นใดมีความถี่สูงสุด", names[pick], [x for i, x in enumerate(names) if i != pick]


@question_type("math.number_of_classes_m6", display_name={"th": "จำนวนอันตรภาคชั้น"}, level=LEVEL, topic=_GROUPED_TOPIC)
class NumberOfClassesM6(WordProblem):
    def expr(self, rng: Random):
        width = rng.choice((5, 10, 20))
        low = rng.randint(10, 50)
        k = rng.randint(4, 10)
        high = low + width * (k - 1) + rng.randint(1, width - 1)
        right = -(-(high - low + 1) // width)
        prompt = f"ข้อมูลมีค่าต่ำสุด {low} และค่าสูงสุด {high} ถ้าแบ่งเป็นอันตรภาคชั้นที่กว้างชั้นละ {width} จะได้อย่างน้อยกี่ชั้น"
        # The range rounded down; the range itself; one too many.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk6((high - low) // width, high - low, right + 1, right - 1, answer=right, lo=1))


@question_type("math.polygon_point_m6", display_name={"th": "จุดบนรูปหลายเหลี่ยมของความถี่"}, level=LEVEL, topic=_GROUPED_TOPIC)
class PolygonPointM6(ChoiceType):
    def compose(self, rng: Random):
        bins, freq, table = _grouped(rng)
        i = rng.randrange(5)
        a, b = bins[i]
        mid = Fraction(a + b, 2)
        right = f"({_num6(mid)}, {freq[i]})"
        wrongs = [f"({a}, {freq[i]})", f"({b}, {freq[i]})", f"({_num6(mid)}, {sum(freq[:i + 1])})" if i else f"({_num6(mid)}, {freq[i] + 1})"]
        return f"{table}{NL}จุดใดอยู่บนรูปหลายเหลี่ยมของความถี่สำหรับอันตรภาคชั้น {a} – {b}", right, wrongs
