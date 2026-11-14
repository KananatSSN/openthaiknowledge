"""แผนภูมิรูปวงกลม

คณิตศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ค 3.1 ป.6/1

Sets moved here from: math, math_diagrams_geo, math_p6.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import _img, _math_q
from otk.sets._support.math_diagrams_geo import PIE_CHARTS
from otk.sets._support.math_diagrams_geo import PieChart as PieChart_math_diagrams_geo
from otk.sets._support.math_p4 import grouped
from otk.sets._support.math_p6 import LEVEL

PROVENANCE = Provenance("original")


def pie_alt(p: PieChart_math_diagrams_geo) -> str:
    return "แผนภูมิรูปวงกลมแบ่งเป็น 4 ส่วน " + " ".join(
        f"ส่วน {k} ร้อยละ {v}" for k, v in zip("ABCD", p.percents))


# (the chart's heading with the total left as {}, the unit)
_PIE_STORIES = (
    ("แผนภูมิรูปวงกลมแสดงอาหารกลางวันที่นักเรียนชอบ จากนักเรียนทั้งหมด {} คน", "คน"),
    ("แผนภูมิรูปวงกลมแสดงกีฬาที่ชอบของผู้ตอบแบบสอบถามทั้งหมด {} คน", "คน"),
    ("แผนภูมิรูปวงกลมแสดงรายจ่ายแต่ละประเภทของครอบครัวหนึ่ง ซึ่งมีรายจ่ายทั้งหมด {} บาท", "บาท"),
)


NL = chr(10)       # a new stem line


_PIE = (
    ("วิธีเดินทางมาโรงเรียนของนักเรียน", ("เดิน", "จักรยาน", "รถโรงเรียน", "รถยนต์ผู้ปกครอง"), "คน"),
    ("รายจ่ายต่อเดือนของครอบครัวหนึ่ง", ("ค่าอาหาร", "ค่าเดินทาง", "ค่าเล่าเรียน", "เงินออม"), "บาท"),
    ("กีฬาที่นักเรียนชอบ", ("ฟุตบอล", "วอลเลย์บอล", "แบดมินตัน", "ว่ายน้ำ"), "คน"),
)


def pie(rng: Random):
    """``(text, {slice: percent}, total, unit)``; percents are multiples of 5
    summing to 100 and total makes every slice whole."""
    title, slices, unit = rng.choice(_PIE)
    while True:
        cuts = sorted(rng.sample(range(1, 20), 3))
        pcts = [5 * x for x in (cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1], 20 - cuts[2])]
        if min(pcts) >= 5 and len(set(pcts)) == 4:
            break
    total = rng.choice((200, 400, 600, 800, 1000, 2000, 12000, 20000 if unit == "บาท" else 1200))
    data = dict(zip(slices, pcts))
    lines = [f"แผนภูมิรูปวงกลมแสดง{title} (ทั้งหมด {grouped(total)} {unit})"]
    lines += [f"{s}: ร้อยละ {p}" for s, p in data.items()]
    return "\n".join(lines), data, total, unit


@question_type("math.pie_chart",
               display_name={"th": "อ่านแผนภูมิรูปวงกลม"}, level={"th": "ป.6"},
               topic="แผนภูมิรูปวงกลม")
class PieChart(WordProblem):
    _WHAT = (("ผลไม้ที่นักเรียนชอบ", "มะม่วง", "คน"), ("รายจ่ายของครอบครัว", "ค่าอาหาร", "บาท"),
             ("สีที่นักเรียนชอบ", "สีฟ้า", "คน"), ("ประเภทหนังสือในห้องสมุด", "นิทาน", "เล่ม"))

    def expr(self, rng: Random):
        title, part, unit = rng.choice(self._WHAT)
        p = rng.choice([5, 10, 15, 20, 25, 30, 40, 45, 60])
        total = rng.randint(1, 20) * 100
        ans = total * p // 100
        return MathDraw("", str(ans),
                        prompt=(f"แผนภูมิรูปวงกลมแสดง{title} ทั้งหมด {total} {unit} "
                                f"ส่วนที่เป็น{part}คิดเป็นร้อยละ {p} {part}มีกี่{unit}"),
                        distractors=_story.keep(p, total - ans, total * p // 10, answer=ans, lo=1))


@question_type("math.pie_chart_picture_p6", display_name={"th": "อ่านแผนภูมิรูปวงกลม (รูป)"},
               level={"th": "ป.6"}, topic="แผนภูมิรูปวงกลม")
class PieChartPictureP6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(PIE_CHARTS)
        img = _img(p.asset_id, pie_alt(p))
        story, unit = rng.choice(_PIE_STORIES)
        total = rng.choice((200, 400, 500, 600, 800, 1000, 1200))
        i, j = rng.sample(range(4), 2)
        a, b = "ABCD"[i], "ABCD"[j]
        pi, pj = p.percents[i], p.percents[j]
        head = story.format(f"{total:,}")
        kind = rng.randrange(3)
        if kind == 0:
            ans = total * pi // 100
            return _math_q([text(f"{head} ส่วน {a} คิดเป็นกี่{unit}"), img], str(ans),
                           [str(pi), str(total * (100 - pi) // 100), str(ans * 2), str(ans // 2),
                            str(total * pj // 100)], self.topic)
        if kind == 1:
            ans = total * abs(pi - pj) // 100
            return _math_q([text(f"{head} ส่วน {a} กับส่วน {b} ต่างกันกี่{unit}"), img], str(ans),
                           [str(abs(pi - pj)), str(total * (pi + pj) // 100), str(ans + total // 20)],
                           self.topic)
        ans = pi * 36 // 10
        return _math_q([text(f"ส่วน {a} ในแผนภูมิรูปวงกลมนี้มีมุมที่จุดศูนย์กลางกี่องศา"), img], str(ans),
                       [str(pi), str(pi * 2), str(360 - ans)], self.topic)


@question_type("math.pie_chart_amount_p6",
               display_name={"th": "แผนภูมิรูปวงกลม: หาจำนวนจากร้อยละ"},
               level=LEVEL, topic="แผนภูมิรูปวงกลม")
class PieChartAmountP6(WordProblem):
    def expr(self, rng: Random):
        tx, data, total, unit = pie(rng)
        x, y = rng.sample(list(data), 2)
        if rng.random() < 0.5:
            ans = total * data[x] // 100
            return MathDraw("", str(ans), prompt=f"{tx}{NL}{x}คิดเป็นกี่{unit}",
                            distractors=_story.keep(data[x], total - ans, ans * 10, ans // 2,
                                                    answer=ans, lo=1))
        if data[x] < data[y]:
            x, y = y, x
        ans = total * (data[x] - data[y]) // 100
        return MathDraw("", str(ans), prompt=f"{tx}{NL}{x}มากกว่า{y}กี่{unit}",
                        distractors=_story.keep(data[x] - data[y], total * (data[x] + data[y]) // 100,
                                                total * data[x] // 100, answer=ans, lo=1))


@question_type("math.pie_chart_missing_p6",
               display_name={"th": "แผนภูมิรูปวงกลม: หาส่วนที่หายไปและมุมที่จุดศูนย์กลาง"},
               level=LEVEL, topic="แผนภูมิรูปวงกลม")
class PieChartMissingP6(WordProblem):
    def expr(self, rng: Random):
        tx, data, total, unit = pie(rng)
        hidden = rng.choice(list(data))
        if rng.random() < 0.5:
            shown = tx.replace(f"{hidden}: ร้อยละ {data[hidden]}", f"{hidden}: ร้อยละ ?")
            ans = data[hidden]
            return MathDraw("", str(ans), prompt=f"{shown}{NL}{hidden}คิดเป็นร้อยละเท่าใด",
                            distractors=_story.keep(100 - ans, total * ans // 100, ans + 5,
                                                    answer=ans, lo=1))
        ans = 360 * data[hidden] // 100
        if 360 * data[hidden] % 100:
            return self.expr(rng)
        return MathDraw("", str(ans),
                        prompt=f"{tx}{NL}ส่วนของ{hidden}ทำมุมที่จุดศูนย์กลางของวงกลมกี่องศา",
                        # A percent read straight as degrees, or taken of 180.
                        distractors=_story.keep(data[hidden], 180 * data[hidden] // 100,
                                                ans + 18, answer=ans, lo=1))

from fractions import Fraction  # noqa: E402

from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p4 import as_mixed  # noqa: E402
from otk.sets._support.math_p6 import LEVEL  # noqa: E402


def _g6(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk6(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g6(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _d6(value: int, places: int) -> str:
    """An integer count of 10**-places as a decimal, trailing zeros dropped: (2350, 3) -> 2.35."""
    sign = "-" if value < 0 else ""
    whole, frac = divmod(abs(value), 10 ** places)
    digits = str(frac).rjust(places, "0").rstrip("0") if places else ""
    return f"{sign}{whole}.{digits}" if digits else f"{sign}{whole}"


def _dk6(*values: int, answer: int, places: int, lo: int = 0) -> list[str]:
    """``story.keep`` for decimals held as integer counts of 10**-places."""
    return [_d6(int(v), places) for v in _story.keep(*values, answer=answer, lo=lo)]


def _fk6(*values: Fraction, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer and non-positive values left out."""
    out: list[str] = []
    for v in values:
        if v > 0 and v != answer and as_mixed(v) not in out:
            out.append(as_mixed(v))
    return out


# ── More pie charts (2026-11): a percent as an angle, an angle as a percent, the whole from a part, a missing
# percent, the largest part, and two parts together ──

_PIE6 = ("ฟุตบอล", "ว่ายน้ำ", "แบดมินตัน", "วิ่ง", "บาสเกตบอล")


def _pie_percents6(rng: Random, k: int = 4) -> list[int]:
    """k percents, multiples of five, all different, adding to 100."""
    while True:
        cuts = sorted(rng.sample(range(1, 20), k - 1))
        parts = [5 * (b - a) for a, b in zip([0, *cuts], [*cuts, 20])]
        if len(set(parts)) == k:
            return parts


def _pie_text6(names, parts, unit: str = "ร้อยละ") -> str:
    rows = "\n".join(f"{x}: {unit} {p}" if unit == "ร้อยละ" else f"{x}: {p} องศา" for x, p in zip(names, parts))
    return f"แผนภูมิรูปวงกลมแสดงกีฬาที่นักเรียนชอบ\n{rows}"


@question_type("math.pie_angle_from_percent_p6", display_name={"th": "แผนภูมิรูปวงกลม (ร้อยละเป็นมุม)"},
               level=LEVEL, topic="แผนภูมิรูปวงกลม")
class PieAngleFromPercentP6(WordProblem):
    def expr(self, rng: Random):
        p = 5 * rng.randint(1, 15)
        right = p * 36 // 10
        what = rng.choice(_PIE6)
        prompt = f"ในแผนภูมิรูปวงกลม ส่วนของ{what}คิดเป็นร้อยละ {p} ส่วนนี้ทำมุมที่จุดศูนย์กลางกี่องศา"
        # The percent read as degrees; a circle taken as 180 or 100 degrees.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(p, p * 18 // 10, 360 - right, right + 18, answer=right, lo=1))


@question_type("math.pie_percent_from_angle_p6", display_name={"th": "แผนภูมิรูปวงกลม (มุมเป็นร้อยละ)"},
               level=LEVEL, topic="แผนภูมิรูปวงกลม")
class PiePercentFromAngleP6(WordProblem):
    def expr(self, rng: Random):
        right = 5 * rng.randint(1, 15)
        angle = right * 36 // 10
        what = rng.choice(_PIE6)
        prompt = f"ในแผนภูมิรูปวงกลม ส่วนของ{what}ทำมุมที่จุดศูนย์กลาง {angle} องศา คิดเป็นร้อยละเท่าใด"
        # The angle itself; the rest of the circle; a half circle used.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(angle, 100 - right, angle * 10 // 18 if angle * 10 % 18 == 0 else right + 10,
                                                right + 5, answer=right, lo=1, hi=99))


@question_type("math.pie_total_from_part_p6", display_name={"th": "แผนภูมิรูปวงกลม (หาจำนวนทั้งหมด)"},
               level=LEVEL, topic="แผนภูมิรูปวงกลม")
class PieTotalFromPartP6(WordProblem):
    def expr(self, rng: Random):
        names = rng.sample(_PIE6, 4)
        parts = _pie_percents6(rng)
        i = rng.randrange(4)
        total = 20 * rng.randint(2, 30)
        count = total * parts[i] // 100
        prompt = f"{_pie_text6(names, parts)}\nถ้านักเรียนที่ชอบ{names[i]}มี {count} คน นักเรียนทั้งหมดมีกี่คน"
        # The count plus the percent; the others' count; the percent as the count.
        return MathDraw("", str(total), prompt=prompt,
                        distractors=_story.keep(count + parts[i], total - count, count * parts[i] // 10 or count + 1,
                                                total + 20, answer=total, lo=1))


@question_type("math.pie_missing_percent_p6", display_name={"th": "แผนภูมิรูปวงกลม (ร้อยละที่หายไป)"},
               level=LEVEL, topic="แผนภูมิรูปวงกลม")
class PieMissingPercentP6(WordProblem):
    def expr(self, rng: Random):
        names = rng.sample(_PIE6, 4)
        parts = _pie_percents6(rng)
        i = rng.randrange(4)
        shown = [("?" if j == i else p) for j, p in enumerate(parts)]
        right = parts[i]
        tt = _pie_text6(names, shown)
        known = sum(p for j, p in enumerate(parts) if j != i)
        # The known parts added; a circle taken as 360; one known part.
        return MathDraw("", str(right), prompt=f"{tt}\nส่วนของ{names[i]}คิดเป็นร้อยละเท่าใด",
                        distractors=_story.keep(known, 360 - known, parts[(i + 1) % 4], right + 5,
                                                answer=right, lo=1, hi=99))


@question_type("math.pie_largest_part_p6", display_name={"th": "แผนภูมิรูปวงกลม (ส่วนที่มากหรือน้อยที่สุด)"},
               level=LEVEL, topic="แผนภูมิรูปวงกลม")
class PieLargestPartP6(ChoiceType):
    def compose(self, rng: Random):
        names = rng.sample(_PIE6, 4)
        parts = _pie_percents6(rng)
        angles = [p * 36 // 10 for p in parts]
        most = rng.random() < 0.5
        pick = angles.index(max(angles) if most else min(angles))
        stem = f"{_pie_text6(names, angles, unit='องศา')}\nกีฬาใดมีนักเรียนชอบ{'มากที่สุด' if most else 'น้อยที่สุด'}"
        return stem, names[pick], [x for j, x in enumerate(names) if j != pick]


@question_type("math.pie_two_parts_p6", display_name={"th": "แผนภูมิรูปวงกลม (สองส่วนรวมกัน)"},
               level=LEVEL, topic="แผนภูมิรูปวงกลม")
class PieTwoPartsP6(WordProblem):
    def expr(self, rng: Random):
        names = rng.sample(_PIE6, 4)
        parts = _pie_percents6(rng)
        i, j = rng.sample(range(4), 2)
        total = 20 * rng.randint(2, 30)
        right = total * (parts[i] + parts[j]) // 100
        prompt = (f"{_pie_text6(names, parts)}\nถ้ามีนักเรียนทั้งหมด {total} คน "
                  f"นักเรียนที่ชอบ{names[i]}และ{names[j]}รวมกันมีกี่คน")
        # The percents added as people; one sport only; everyone else.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(parts[i] + parts[j], total * parts[i] // 100, total - right,
                                                right + 10, answer=right, lo=1))
