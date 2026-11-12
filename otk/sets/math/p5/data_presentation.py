"""การนำเสนอข้อมูล

คณิตศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ค 3.1 ป.5/1, ค 3.1 ป.5/2

Sets moved here from: math, math_diagrams, math_gaps_shape_data.
"""

from __future__ import annotations

from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import LINE_GRAPHS, _img, _math_q, _nums
from otk.sets._support.math_gaps_shape_data import _TALLY, _choices, _table

PROVENANCE = Provenance("original")


LINE_ALT = "กราฟเส้นที่มีจุดข้อมูลหกจุด แกนนอนเป็นลำดับที่ 1 ถึง 6 บนเส้นตาราง"


@question_type("math.line_graph_picture_p5", display_name={"th": "อ่านกราฟเส้น (รูป)"},
               level={"th": "ป.5"}, topic="การนำเสนอข้อมูล")
class LineGraphPictureP5(QuestionType):
    _SERIES = (("ความสูงของต้นถั่ว", "สัปดาห์ที่", "เซนติเมตร"),
               ("จำนวนผู้เข้าชมห้องสมุด", "วันที่", "คน"),
               ("อุณหภูมิของน้ำในการทดลอง", "นาทีที่", "องศาเซลเซียส"),
               ("ยอดขายขนมของร้านค้า", "เดือนที่", "ชิ้น"))

    def build(self, rng: Random) -> GeneratedQuestion:
        g = rng.choice(LINE_GRAPHS)
        title, xname, unit = rng.choice(self._SERIES)
        head = text(f"กราฟเส้นแสดง{title} แกนนอนเป็น{xname} 1 ถึง 6 แกนตั้งมีหน่วยเป็น{unit}")
        img = _img(g.asset_id, LINE_ALT)
        v = g.values
        kind = rng.randrange(3)
        if kind == 0:
            i = rng.randrange(6)
            ans = v[i]
            wrongs = _nums(*(x for x in v if x != ans), ans + g.step, answer=ans)
            ask = f"{xname} {i + 1} มีค่าเท่าใด"
        elif kind == 1:
            i, j = sorted(rng.sample(range(6), 2))
            if v[i] == v[j]:
                return self.build(rng)
            ans = abs(v[j] - v[i])
            way = "เพิ่มขึ้น" if v[j] > v[i] else "ลดลง"
            ask = f"จาก{xname} {i + 1} ถึง{xname} {j + 1} {way}กี่{unit}"
            wrongs = _nums(v[i] + v[j], ans + g.step, max(v) - min(v), ans - g.step, 2 * ans,
                           answer=ans, lo=1)
        else:
            top = max(v)
            if v.count(top) > 1:
                return self.build(rng)
            ans = v.index(top) + 1
            ask = f"{xname}ใดมีค่ามากที่สุด"
            wrongs = _nums(top, v.index(min(v)) + 1, ans % 6 + 1, answer=ans, lo=1)
        return _math_q([head, img, text(ask)], str(ans), wrongs, self.topic)


@question_type("math.line_graph_change",
               display_name={"th": "อ่านกราฟเส้น (การเปลี่ยนแปลง)"}, level={"th": "ป.5"},
               topic="การนำเสนอข้อมูล")
class LineGraphChange(WordProblem):
    _SERIES = (("อุณหภูมิตอนเที่ยงของแต่ละวัน", ("จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์"),
                "องศาเซลเซียส", (24, 40)),
               ("ความสูงของต้นถั่ว", ("สัปดาห์ที่ 1", "สัปดาห์ที่ 2", "สัปดาห์ที่ 3",
                                     "สัปดาห์ที่ 4", "สัปดาห์ที่ 5"), "เซนติเมตร", (2, 60)),
               ("จำนวนผู้เข้าชมงาน", ("ปี 2564", "ปี 2565", "ปี 2566", "ปี 2567", "ปี 2568"),
                "คน", (100, 900)))

    def expr(self, rng: Random):
        title, points, unit, (lo, hi) = rng.choice(self._SERIES)
        values = rng.sample(range(lo, hi + 1), len(points))
        i, j = sorted(rng.sample(range(len(points)), 2))
        rows = "\n".join(f"{x}: {v}" for x, v in zip(points, values))
        change = abs(values[j] - values[i])
        way = "เพิ่มขึ้น" if values[j] > values[i] else "ลดลง"
        return MathDraw(
            "", str(change),
            prompt=(f"กราฟเส้นแสดง{title} อ่านค่าจากกราฟได้ดังนี้\n{rows}\n"
                    f"จาก{points[i]}ถึง{points[j]} {way}กี่{unit}"),
            distractors=_story.keep(values[i] + values[j], change + 1, max(values) - min(values),
                                    change - 1, answer=change, lo=1))


@question_type("math.bar_chart_make_p5", display_name={"th": "เขียนแผนภูมิแท่งจากข้อมูล"},
               level={"th": "ป.5"}, topic="การนำเสนอข้อมูล")
class BarChartMakeP5(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        title, rows, unit = rng.choice(_TALLY)
        scale = rng.choice((5, 10, 20, 50))
        counts = [scale * rng.randint(2, 12) for _ in rows]
        i = rng.randrange(len(rows))
        table = _table(title, rows, counts, unit)
        if rng.random() < 0.5:
            right = counts[i] // scale
            stem = [text(f"{table}\nถ้าเขียนแผนภูมิแท่ง โดยให้ความยาว 1 ช่องแทน {scale} {unit} "
                         f"แท่งของ{rows[i]} ต้องยาวกี่ช่อง")]
            wrongs = _story.keep(counts[i], right * 2, right + 1, answer=right, lo=1)
            return GeneratedQuestion(stem=stem, correct=[content_math(str(right))],
                                     distractors=fixed(*[[content_math(w)] for w in wrongs]),
                                     topic=self.topic)
        # Choosing a scale: the only one of the offered scales that makes the
        # longest bar 10 to 20 squares. Data with two such scales is redrawn.
        top = max(counts)
        scales = (1, 2, 5, 10, 20, 50, 100, 200)
        ok = [s for s in scales if 10 <= -(-top // s) <= 20]
        if len(ok) != 1:
            return self.build(rng, **params)
        right_scale = ok[0]
        wrong_scales = [s for s in scales if s != right_scale]
        rng.shuffle(wrong_scales)
        stem = [text(f"{table}\nกระดาษกราฟมีช่องตามแนวยาว 20 ช่อง ถ้าต้องการให้แท่งที่ยาวที่สุด"
                     f"ยาวอย่างน้อย 10 ช่องแต่ไม่เกิน 20 ช่อง ควรให้ 1 ช่องแทนกี่{unit}")]
        return _choices(stem, f"{right_scale} {unit}", [f"{s} {unit}" for s in wrong_scales], self.topic)


@question_type("math.line_graph_problem_p5", display_name={"th": "ใช้ข้อมูลจากกราฟเส้นแก้โจทย์ปัญหา"},
               level={"th": "ป.5"}, topic="การนำเสนอข้อมูล")
class LineGraphProblemP5(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    _SERIES = (
        ("ความสูงของต้นถั่ว (เซนติเมตร) ในแต่ละสัปดาห์", ("สัปดาห์ที่ 1", "สัปดาห์ที่ 2", "สัปดาห์ที่ 3",
                                                          "สัปดาห์ที่ 4", "สัปดาห์ที่ 5"), "เซนติเมตร", True),
        ("จำนวนผู้เข้าชมห้องสมุด (คน) ในแต่ละวัน", ("จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์"), "คน", False),
        ("ยอดขายไอศกรีม (ถ้วย) ในแต่ละเดือน", ("มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม"), "ถ้วย", False),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        title, xs, unit, rising = rng.choice(self._SERIES)
        while True:
            if rising:
                ys = [rng.randint(2, 6)]
                for _ in xs[1:]:
                    ys.append(ys[-1] + rng.randint(1, 8))
            else:
                ys = [rng.randint(20, 90) for _ in xs]
            steps = [b - a for a, b in zip(ys, ys[1:])]
            if len(set(steps)) == len(steps) and max(steps) > 0:
                break
        data = f"กราฟเส้นแสดง{title} อ่านค่าจากกราฟได้ดังนี้\n" + "\n".join(
            f"{x}: {y}" for x, y in zip(xs, ys))
        # A total only means something for counts; a height is not summed.
        kind = rng.randrange(3) if not rising else rng.choice((0, 2))
        if kind == 0:
            k = max(range(len(steps)), key=lambda i: steps[i])
            right = f"จาก{xs[k]}ถึง{xs[k + 1]}"
            wrongs = [f"จาก{xs[i]}ถึง{xs[i + 1]}" for i in range(len(steps)) if i != k]
            # The largest value, taken for the largest rise, is the usual slip.
            return _choices([text(f"{data}\nช่วงใดเพิ่มขึ้นมากที่สุด")], right, wrongs, self.topic)
        if kind == 1:
            total = sum(ys)
            wrongs = _story.keep(max(ys) * len(ys), total - ys[0], total + ys[-1], answer=total, lo=1)
            stem = [text(f"{data}\nรวมทั้ง {len(xs)} ช่วง มีทั้งหมดกี่{unit}")]
            return GeneratedQuestion(stem=stem, correct=[content_math(str(total))],
                                     distractors=fixed(*[[content_math(w)] for w in wrongs]),
                                     topic=self.topic)
        spread = max(ys) - min(ys)
        wrongs = _story.keep(max(ys), max(ys) + min(ys), abs(ys[-1] - ys[0]),
                             spread + 1, spread - 1, answer=spread, lo=1)[:3]
        stem = [text(f"{data}\nค่าที่มากที่สุดมากกว่าค่าที่น้อยที่สุดอยู่กี่{unit}")]
        return GeneratedQuestion(stem=stem, correct=[content_math(str(spread))],
                                 distractors=fixed(*[[content_math(w)] for w in wrongs]),
                                 topic=self.topic)


from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p5 import LEVEL  # noqa: E402


def _g(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _dec(value: int, places: int) -> str:
    """An integer count of 10**-places as a decimal, trailing zeros dropped: (2350, 3) -> 2.35."""
    sign = "-" if value < 0 else ""
    whole, frac = divmod(abs(value), 10 ** places)
    digits = str(frac).rjust(places, "0").rstrip("0") if places else ""
    return f"{sign}{whole}.{digits}" if digits else f"{sign}{whole}"


def _dk(*values: int, answer: int, places: int, lo: int = 0) -> list[str]:
    """``story.keep`` for decimals held as integer counts of 10**-places."""
    return [_dec(int(v), places) for v in _story.keep(*values, answer=answer, lo=lo)]


# ── More line graphs (2026-11): the total, how many gaps rise or fall, the highest point, how many points pass a value,
# the next point of a steady change, and the true statement ──

_LINE_SERIES = (
    ("ความสูงของต้นถั่ว", tuple(f"สัปดาห์ที่ {i}" for i in range(1, 6)), "เซนติเมตร", (2, 60)),
    ("อุณหภูมิตอนเที่ยง", ("จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์"), "องศาเซลเซียส", (24, 40)),
    ("จำนวนผู้เข้าห้องสมุด", tuple(f"วันที่ {i}" for i in range(1, 6)), "คน", (20, 90)),
)


def _line_text(title: str, unit: str, points, values) -> str:
    rows = "\n".join(f"{x}: {v}" for x, v in zip(points, values))
    return f"กราฟเส้นแสดง{title} ({unit}) อ่านค่าจากกราฟได้ดังนี้\n{rows}"


def _line(rng: Random):
    title, points, unit, (lo, hi) = rng.choice(_LINE_SERIES)
    values = rng.sample(range(lo, hi + 1), len(points))
    return _line_text(title, unit, points, values), points, unit, values


@question_type("math.line_graph_total_p5", display_name={"th": "อ่านกราฟเส้น (ผลรวมทุกจุด)"},
               level=LEVEL, topic="การนำเสนอข้อมูล")
class LineGraphTotalP5(WordProblem):
    def expr(self, rng: Random):
        tt, points, unit, values = _line(rng)
        right = sum(values)
        # The first and last points only; one point left out; the highest point five times.
        return MathDraw("", str(right), prompt=f"{tt}\nรวมทุกจุดเป็นกี่{unit}",
                        distractors=_story.keep(values[0] + values[-1], right - values[2], 5 * max(values),
                                                right + 10, answer=right, lo=1))


@question_type("math.line_graph_count_rises_p5", display_name={"th": "อ่านกราฟเส้น (นับช่วงที่เพิ่มขึ้น)"},
               level=LEVEL, topic="การนำเสนอข้อมูล")
class LineGraphCountRisesP5(WordProblem):
    def expr(self, rng: Random):
        tt, points, unit, values = _line(rng)
        rises = sum(b > a for a, b in zip(values, values[1:]))
        falls = len(values) - 1 - rises
        rising = rng.random() < 0.5
        right = rises if rising else falls
        # The other kind of change; the points instead of the gaps; one off.
        return MathDraw("", str(right), prompt=f"{tt}\nมีกี่ช่วงที่ค่า{'เพิ่มขึ้น' if rising else 'ลดลง'}จากจุดก่อนหน้า",
                        distractors=_story.keep(falls if rising else rises, len(values), right + 1, right - 1,
                                                answer=right, lo=0, hi=len(values)))


@question_type("math.line_graph_highest_p5", display_name={"th": "อ่านกราฟเส้น (จุดสูงสุดหรือต่ำสุด)"},
               level=LEVEL, topic="การนำเสนอข้อมูล")
class LineGraphHighestP5(ChoiceType):
    def compose(self, rng: Random):
        tt, points, unit, values = _line(rng)
        most = rng.random() < 0.5
        pick = values.index(max(values) if most else min(values))
        return (f"{tt}\nจุดใดมีค่า{'มากที่สุด' if most else 'น้อยที่สุด'}", points[pick],
                [x for i, x in enumerate(points) if i != pick])


@question_type("math.line_graph_count_above_p5", display_name={"th": "อ่านกราฟเส้น (นับจุดที่เกินค่าที่กำหนด)"},
               level=LEVEL, topic="การนำเสนอข้อมูล")
class LineGraphCountAboveP5(WordProblem):
    def expr(self, rng: Random):
        tt, points, unit, values = _line(rng)
        k = rng.randint(min(values), max(values) - 1)
        right = sum(v > k for v in values)
        # Counting a point equal to the value; the points at or below; all of them.
        return MathDraw("", str(right), prompt=f"{tt}\nมีกี่จุดที่มีค่ามากกว่า {k} {unit}",
                        distractors=_story.keep(sum(v >= k for v in values), len(values) - right, len(values),
                                                right + 1, right - 1, answer=right, lo=0, hi=len(values)))


@question_type("math.line_graph_next_p5", display_name={"th": "อ่านกราฟเส้น (คาดคะเนจุดถัดไป)"},
               level=LEVEL, topic="การนำเสนอข้อมูล")
class LineGraphNextP5(WordProblem):
    def expr(self, rng: Random):
        step = rng.randint(2, 9)
        start = rng.randint(5, 40)
        values = [start + step * i for i in range(5)]
        points = tuple(f"สัปดาห์ที่ {i}" for i in range(1, 6))
        tt = _line_text("ความสูงของต้นไม้", "เซนติเมตร", points, values)
        right = values[-1] + step
        # The last point repeated; twice the step; the first point added.
        return MathDraw("", str(right),
                        prompt=f"{tt}\nถ้าต้นไม้สูงขึ้นในอัตราเดิม สัปดาห์ที่ 6 จะสูงกี่เซนติเมตร",
                        distractors=_story.keep(values[-1], values[-1] + 2 * step, values[-1] + start,
                                                right + 1, answer=right, lo=1))


@question_type("math.line_graph_true_p5", display_name={"th": "อ่านกราฟเส้น (ข้อความที่ถูกต้อง)"},
               level=LEVEL, topic="การนำเสนอข้อมูล")
class LineGraphTrueP5(ChoiceType):
    def compose(self, rng: Random):
        tt, points, unit, values = _line(rng)
        i = rng.randrange(len(points) - 1)
        a, b = values[i], values[i + 1]
        way, other = ("เพิ่มขึ้น", "ลดลง") if b > a else ("ลดลง", "เพิ่มขึ้น")
        d = abs(b - a)
        x, y = points[i], points[i + 1]
        right = f"จาก{x}ถึง{y} {way} {d} {unit}"
        wrongs = [f"จาก{x}ถึง{y} {other} {d} {unit}", f"จาก{x}ถึง{y} {way} {a + b} {unit}",
                  f"จาก{x}ถึง{y} {way} {d + 2} {unit}"]
        return f"{tt}\nข้อความใดถูกต้อง", right, wrongs
