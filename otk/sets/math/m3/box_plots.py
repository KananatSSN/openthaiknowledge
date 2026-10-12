"""สถิติ (แผนภาพกล่อง)

คณิตศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ค 3.1 ม.3/1

Sets moved here from: math, math_diagrams_geo, math_m3, math_thin_topics.
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
from otk.sets._support.math_diagrams_hi import BOX_ALT, BOX_PLOTS
from otk.sets._support.math_m3 import LEVEL
from otk.sets._support.math_m4 import maths as _num_maths
from otk.sets._support.math_p2 import _texts

PROVENANCE = Provenance("original")


M2 = {"th": "ม.2"}


def _summary(rng: Random) -> tuple[int, ...]:
    while True:
        v = sorted(rng.sample(range(20, 100), 5))
        if min(b - a for a, b in zip(v, v[1:])) >= 3:
            return tuple(v)


def _box_text(name: str, s) -> str:
    return (f"ห้อง {name}: ค่าต่ำสุด {s[0]} ควอร์ไทล์ที่ 1 = {s[1]} มัธยฐาน {s[2]} "
            f"ควอร์ไทล์ที่ 3 = {s[3]} ค่าสูงสุด {s[4]}")


@question_type("math.box_plot_picture_m2", display_name={"th": "อ่านแผนภาพกล่อง (รูป)"},
               level={"th": "ม.2"}, topic="สถิติ (แผนภาพกล่อง)")
class BoxPlotPictureM2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        b = rng.choice(BOX_PLOTS)
        img = _img(b.asset_id, BOX_ALT)
        kind = rng.randrange(4)
        if kind == 0:
            return _math_q([text("ค่าต่ำสุดของข้อมูลเท่ากับเท่าใด"), img], str(b.lo),
                           [str(b.q1), str(b.hi), str(b.med)], self.topic)
        if kind == 1:
            return _math_q([text("ควอร์ไทล์ที่ 1 เท่ากับเท่าใด"), img], str(b.q1),
                           [str(b.lo), str(b.med), str(b.q3)], self.topic)
        if kind == 2:
            return _math_q([text("ข้อมูลประมาณร้อยละเท่าใดมีค่าอยู่ระหว่างควอร์ไทล์ที่ 1 และควอร์ไทล์ที่ 3"), img],
                           "50", ["25", "75", "100"], self.topic)
        return _math_q([text("ผลต่างระหว่างค่าสูงสุดกับมัธยฐานเท่ากับเท่าใด"), img], str(b.hi - b.med),
                       [str(b.hi - b.q3), str(b.med - b.lo), str(b.hi - b.lo)], self.topic)


@question_type("math.boxplot_iqr",
               display_name={"th": "พิสัยระหว่างควอไทล์ (IQR)"}, level={"th": "ม.2"},
               topic="สถิติ (แผนภาพกล่อง)")
class BoxplotIQR(WordProblem):
    def expr(self, rng: Random):
        vals = sorted(rng.sample(range(1, 60), 5))
        mn, q1, q2, q3, mx = vals
        what = rng.choice(("คะแนนสอบของนักเรียนห้องหนึ่ง", "น้ำหนัก (กิโลกรัม) ของนักเรียนกลุ่มหนึ่ง",
                           "เวลา (นาที) ที่นักเรียนใช้เดินทางมาโรงเรียน"))
        prompt = rng.choice((
            f"จากแผนภาพกล่อง Min={mn}, Q1={q1}, Q2={q2}, Q3={q3}, Max={mx} "
            f"พิสัยระหว่างควอไทล์ (IQR) เท่ากับเท่าใด?",
            f"แผนภาพกล่องของ{what}มีค่าต่ำสุด {mn} ควอไทล์ที่ 1 เท่ากับ {q1} มัธยฐาน {q2} "
            f"ควอไทล์ที่ 3 เท่ากับ {q3} และค่าสูงสุด {mx} พิสัยระหว่างควอไทล์เท่ากับเท่าใด",
        ))
        return MathDraw("", str(q3 - q1), prompt=prompt,
                        distractors=[str(mx - mn), str(q2), str(q3 - q2)])


@question_type("math.box_plot_summary_m3",
               display_name={"th": "ค่าสรุปห้าค่าและแผนภาพกล่องจากข้อมูล"},
               level=LEVEL, topic="สถิติ (แผนภาพกล่อง)")
class BoxPlotSummaryM3(WordProblem):
    def expr(self, rng: Random):
        n = rng.choice((7, 11))
        data = sorted(rng.sample(range(10, 100), n))
        q1, med, q3 = data[(n + 1) // 4 - 1], data[(n + 1) // 2 - 1], data[3 * (n + 1) // 4 - 1]
        shown = data[:]
        rng.shuffle(shown)
        stem = f"ข้อมูลชุดหนึ่งคือ {', '.join(map(str, shown))}"
        kind = rng.randrange(4)
        if kind == 0:
            return MathDraw("", str(med), prompt=f"{stem} มัธยฐานของข้อมูลเท่ากับเท่าใด",
                            # The middle of the list as written, before sorting.
                            distractors=_story.keep(shown[n // 2], q1, q3, answer=med))
        if kind == 1:
            return MathDraw("", str(q1), prompt=f"{stem} ควอร์ไทล์ที่ 1 เท่ากับเท่าใด",
                            distractors=_story.keep(data[0], med, data[(n + 1) // 4], answer=q1))
        if kind == 2:
            return MathDraw("", str(q3), prompt=f"{stem} ควอร์ไทล์ที่ 3 เท่ากับเท่าใด",
                            distractors=_story.keep(data[-1], med, data[3 * (n + 1) // 4 - 2], answer=q3))
        return MathDraw("", str(q3 - q1),
                        prompt=f"{stem} พิสัยระหว่างควอร์ไทล์ (Q3 − Q1) เท่ากับเท่าใด",
                        distractors=_story.keep(data[-1] - data[0], q3 - med, med - q1, answer=q3 - q1,
                                                lo=1))


@question_type("math.box_plot_compare_m2", display_name={"th": "เปรียบเทียบข้อมูลสองชุดด้วยแผนภาพกล่อง"},
               level=M2, topic="สถิติ (แผนภาพกล่อง)")
class BoxPlotCompareM2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            a, b = _summary(rng), _summary(rng)
            if a[2] != b[2] and a[3] - a[1] != b[3] - b[1]:
                break
        head = text("ข้อมูลคะแนนสอบของนักเรียนสองห้องสรุปเป็นแผนภาพกล่องได้ดังนี้\n"
                    + _box_text("ก", a) + "\n" + _box_text("ข", b))
        kind = rng.randrange(3)
        if kind == 0:
            ans = abs(a[2] - b[2])
            return _num_maths([head, text("มัธยฐานของสองห้องต่างกันกี่คะแนน")], str(ans),
                              [str(abs(a[3] - b[3])), str(abs(a[4] - b[4])), str(abs(a[1] - b[1]))], self.topic)
        if kind == 1:
            ia, ib = a[3] - a[1], b[3] - b[1]
            right = "ห้อง ก" if ia > ib else "ห้อง ข"
            wrong = "ห้อง ข" if ia > ib else "ห้อง ก"
            return _texts([head, text("ห้องใดมีคะแนนช่วงกลางกระจายมากกว่า (พิจารณาพิสัยระหว่างควอร์ไทล์)")],
                          right, [wrong, "ทั้งสองห้องกระจายเท่ากัน", "สรุปไม่ได้จากแผนภาพกล่อง"], self.topic)
        ans = max(a[3] - a[1], b[3] - b[1])
        return _num_maths([head, text("พิสัยระหว่างควอร์ไทล์ที่มากกว่าของสองห้องมีค่าเท่าใด")], str(ans),
                          [str(max(a[4] - a[0], b[4] - b[0])), str(min(a[3] - a[1], b[3] - b[1])),
                           str(max(a[2], b[2]))], self.topic)
