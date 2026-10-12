"""แผนภูมิแท่ง

คณิตศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ค 3.1 ป.4/1

Sets moved here from: math, math_diagrams, math_p4.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import BAR_CHARTS, _img, _math_q, _nums, _text_q
from otk.sets._support.math_p2 import _maths, _texts
from otk.sets._support.math_p4 import LEVEL

PROVENANCE = Provenance("original")


BAR_ALT = "แผนภูมิแท่งแนวตั้ง มีแท่ง A ถึง E บนเส้นตาราง"


_LETTERS = "ABCDE"


def _chart_key(rng: Random, n: int):
    chart = rng.choice(_story._CHARTS)
    picked = set(rng.sample(chart.rows, n))
    rows = [r for r in chart.rows if r in picked]          # the chart's own order
    key = " ".join(f"{_LETTERS[i]} = {r}" for i, r in enumerate(rows))
    return chart, rows, key


NL = chr(10)       # a new stem line


@question_type("math.bar_chart_picture_p4", display_name={"th": "อ่านแผนภูมิแท่ง (รูป)"},
               level={"th": "ป.4"}, topic="แผนภูมิแท่ง")
class BarChartPictureP4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        bc = rng.choice(BAR_CHARTS)
        chart, rows, key = _chart_key(rng, len(bc.values))
        unit = chart.unit
        vals = dict(zip(rows, bc.values))
        head = text(f"แผนภูมิแท่งแสดง{chart.title} ({key}) แกนตั้งเป็นจำนวน{chart.symbol_means} ({unit})")
        img = _img(bc.asset_id, BAR_ALT)
        kind = rng.randrange(3)
        x, y = rng.sample(rows, 2)
        if vals[x] < vals[y]:
            x, y = y, x
        if kind == 0:
            ans = vals[x]
            ask = f"{chart.label.format(c=x)}มีกี่{unit}"
            wrongs = _nums(*(v for r, v in vals.items() if r != x), ans + bc.scale, answer=ans, lo=1)
        elif kind == 1:
            ans = vals[x] - vals[y]
            ask = f"{chart.label.format(c=x)}มากกว่า{chart.label.format(c=y)}กี่{unit}"
            wrongs = _nums(vals[x] + vals[y], ans // bc.scale if bc.scale > 1 else ans + 2,
                           ans + bc.scale, vals[x], answer=ans, lo=1)
        else:
            most = rng.random() < 0.5
            pick = (max if most else min)(vals, key=vals.get)
            return _text_q([head, img, text(chart.most.format(most="มากที่สุด" if most else "น้อยที่สุด"))],
                           pick, [r for r in rows if r != pick], self.topic)
        return _math_q([head, img, text(ask)], str(ans), wrongs, self.topic)


@question_type("math.bar_chart_read_p4",
               display_name={"th": "อ่านแผนภูมิแท่ง"},
               level=LEVEL, topic="แผนภูมิแท่ง")
class BarChartReadP4(WordProblem):
    def expr(self, rng: Random):
        scale = rng.choice((5, 10, 20, 50))
        bc = _story.bar_chart(rng, scale=scale)
        row = rng.choice(list(bc.data))
        n = bc.data[row]
        return MathDraw("", str(n), prompt=f"{bc.text}{NL}{bc.label(row)}มีกี่{bc.chart.unit}",
                        # The number of cells, not what they stand for.
                        distractors=_story.keep(n // scale, n + scale, n - scale, answer=n,
                                                lo=1))


@question_type("math.bar_chart_diff",
               display_name={"th": "อ่านแผนภูมิแท่ง (ผลต่าง)"}, level={"th": "ป.4"},
               topic="แผนภูมิแท่ง")
class BarChartDiff(WordProblem):
    def expr(self, rng: Random):
        scale = rng.choice((1, 2, 5, 10))
        bc = _story.bar_chart(rng, scale=scale, lo=1, hi=12)
        hi = max(bc.data, key=bc.data.get)
        lo = min(bc.data, key=bc.data.get)
        diff = bc.data[hi] - bc.data[lo]
        return MathDraw(
            "", str(diff),
            prompt=f"{bc.text}\n{bc.label(hi)}มากกว่า{bc.label(lo)}กี่{bc.chart.unit}",
            # Cells instead of what they stand for, then the tallest bar alone.
            distractors=_story.keep(diff // scale, bc.data[hi], bc.data[hi] + bc.data[lo],
                                    diff + scale, answer=diff, lo=1))


@question_type("math.bar_chart_compare_p4",
               display_name={"th": "แผนภูมิแท่ง: เปรียบเทียบ รวม และมากที่สุด"},
               level=LEVEL, topic="แผนภูมิแท่ง")
class BarChartCompareP4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        scale = rng.choice((5, 10, 20, 50))
        bc = _story.bar_chart(rng, scale=scale)
        x, y = rng.sample(list(bc.data), 2)
        if bc.data[x] < bc.data[y]:
            x, y = y, x
        a, b, unit = bc.data[x], bc.data[y], bc.chart.unit
        kind = rng.randrange(3)
        if kind == 2:
            most = rng.random() < 0.5
            pick = (max if most else min)(bc.data, key=bc.data.get)
            return _texts([text(bc.text),
                           text(bc.chart.most.format(most="มากที่สุด" if most else "น้อยที่สุด"))],
                          pick, [r for r in bc.data if r != pick], self.topic)
        if kind == 0:
            v, ask = a - b, f"{bc.label(x)}มากกว่า{bc.label(y)}กี่{unit}"
        else:
            v, ask = a + b, f"{bc.label(x)}และ{bc.label(y)}รวมกันกี่{unit}"
        wrongs = _story.keep(v // scale, a + b if v == a - b else a - b, v + scale,
                             v - scale, a, answer=v, lo=1)
        return _maths([text(bc.text), text(ask)], str(v), wrongs, self.topic)
