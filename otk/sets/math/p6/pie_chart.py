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
