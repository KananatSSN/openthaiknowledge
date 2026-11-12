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

from fractions import Fraction  # noqa: E402

from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m3 import LEVEL  # noqa: E402


def _fk3(*values: Fraction, answer: Fraction, lo: Fraction | None = None) -> list[str]:
    """Distinct fraction distractors as TeX, the answer (and values below lo) left out."""
    out: list[str] = []
    for v in values:
        v = Fraction(v)
        if v == answer or (lo is not None and v < lo) or frac_tex(v) in out:
            continue
        out.append(frac_tex(v))
    return out


def _tk3(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _roots3(a: int, b: int) -> str:
    lo, hi = sorted((a, b))
    return rf"x = {lo}, \; {hi}"


def _g3(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572."""
    return f"{n:,}".replace(",", "{,}")


def _gk3(*values: int, answer: int, lo: int = 0) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g3(int(v)) for v in _story.keep(*values, answer=answer, lo=lo)]


# ── More box plots (2026-11): the range, a whisker, the middle half, what each part holds, two medians
# compared, and the five-number summary of a list ──


def _five3(rng: Random) -> list[int]:
    while True:
        values = sorted(rng.sample(range(10, 100), 5))
        if values[2] - values[1] > 1 and values[3] - values[2] > 1:
            return values


def _summary_text3(v: list[int]) -> str:
    return (f"ค่าต่ำสุด {v[0]} ควอร์ไทล์ที่ 1 เท่ากับ {v[1]} มัธยฐาน {v[2]} "
            f"ควอร์ไทล์ที่ 3 เท่ากับ {v[3]} และค่าสูงสุด {v[4]}")


@question_type("math.box_plot_range_m3", display_name={"th": "พิสัยจากแผนภาพกล่อง"},
               level=LEVEL, topic="สถิติ (แผนภาพกล่อง)")
class BoxPlotRangeM3(WordProblem):
    def expr(self, rng: Random):
        v = _five3(rng)
        right = v[4] - v[0]
        prompt = f"แผนภาพกล่องของข้อมูลชุดหนึ่งมี{_summary_text3(v)} พิสัยของข้อมูลเท่ากับเท่าใด"
        # The interquartile range; the maximum alone; the median less the minimum.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(v[3] - v[1], v[4], v[2] - v[0], right + 1, answer=right, lo=1))


@question_type("math.box_plot_whisker_m3", display_name={"th": "ความยาวของหนวดในแผนภาพกล่อง"},
               level=LEVEL, topic="สถิติ (แผนภาพกล่อง)")
class BoxPlotWhiskerM3(WordProblem):
    def expr(self, rng: Random):
        v = _five3(rng)
        upper = rng.random() < 0.5
        right = v[4] - v[3] if upper else v[1] - v[0]
        side = "ขวา (จาก Q3 ถึงค่าสูงสุด)" if upper else "ซ้าย (จากค่าต่ำสุดถึง Q1)"
        prompt = f"แผนภาพกล่องของข้อมูลชุดหนึ่งมี{_summary_text3(v)} หนวดด้าน{side}ยาวกี่หน่วย"
        # The other whisker; the box; the whole range.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(v[1] - v[0] if upper else v[4] - v[3], v[3] - v[1], v[4] - v[0],
                                                right + 2, answer=right, lo=1))


@question_type("math.box_plot_middle_half_m3", display_name={"th": "ข้อมูลครึ่งกลางอยู่ในช่วงใด"},
               level=LEVEL, topic="สถิติ (แผนภาพกล่อง)")
class BoxPlotMiddleHalfM3(ChoiceType):
    def compose(self, rng: Random):
        v = _five3(rng)
        stem = f"แผนภาพกล่องของข้อมูลชุดหนึ่งมี{_summary_text3(v)} ข้อมูลประมาณครึ่งหนึ่งที่อยู่ตรงกลางมีค่าอยู่ในช่วงใด"
        return stem, f"{v[1]} ถึง {v[3]}", [f"{v[0]} ถึง {v[4]}", f"{v[0]} ถึง {v[2]}", f"{v[2]} ถึง {v[4]}"]


@question_type("math.box_plot_parts_m3", display_name={"th": "แต่ละส่วนของแผนภาพกล่องมีข้อมูลประมาณร้อยละเท่าใด"},
               level=LEVEL, topic="สถิติ (แผนภาพกล่อง)")
class BoxPlotPartsM3(ConceptBankType):
    ITEMS = [
        Concept("ข้อมูลที่มีค่าน้อยกว่าควอร์ไทล์ที่ 1 มีประมาณร้อยละเท่าใดของข้อมูลทั้งหมด", "ร้อยละ 25",
                ("ร้อยละ 50", "ร้อยละ 75", "ร้อยละ 10")),
        Concept("ข้อมูลที่อยู่ระหว่างควอร์ไทล์ที่ 1 กับควอร์ไทล์ที่ 3 มีประมาณร้อยละเท่าใด", "ร้อยละ 50",
                ("ร้อยละ 25", "ร้อยละ 75", "ร้อยละ 100")),
        Concept("ข้อมูลที่มีค่ามากกว่าควอร์ไทล์ที่ 1 มีประมาณร้อยละเท่าใดของข้อมูลทั้งหมด", "ร้อยละ 75",
                ("ร้อยละ 25", "ร้อยละ 50", "ร้อยละ 100")),
        Concept("ข้อมูลที่มีค่าไม่เกินมัธยฐานมีประมาณร้อยละเท่าใดของข้อมูลทั้งหมด", "ร้อยละ 50",
                ("ร้อยละ 25", "ร้อยละ 75", "ร้อยละ 100")),
        Concept("ข้อมูลที่อยู่ระหว่างค่าต่ำสุดกับค่าสูงสุดมีประมาณร้อยละเท่าใด", "ร้อยละ 100",
                ("ร้อยละ 50", "ร้อยละ 75", "ร้อยละ 25")),
    ]


@question_type("math.box_plot_two_medians_m3", display_name={"th": "เปรียบเทียบมัธยฐานของข้อมูลสองชุด"},
               level=LEVEL, topic="สถิติ (แผนภาพกล่อง)")
class BoxPlotTwoMediansM3(WordProblem):
    def expr(self, rng: Random):
        while True:
            a, b = _five3(rng), _five3(rng)
            if a[2] != b[2]:
                break
        if a[2] < b[2]:
            a, b = b, a
        right = a[2] - b[2]
        prompt = (f"คะแนนสอบห้องแรกมี{_summary_text3(a)} ห้องที่สองมี{_summary_text3(b)} "
                  "มัธยฐานของห้องแรกมากกว่าของห้องที่สองเท่าใด")
        # The maxima compared; the first quartiles; the third quartiles.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(abs(a[4] - b[4]), abs(a[1] - b[1]), abs(a[3] - b[3]), right + 1,
                                                answer=right, lo=1))


@question_type("math.five_number_summary_m3", display_name={"th": "ค่าสรุปห้าค่าของข้อมูล"},
               level=LEVEL, topic="สถิติ (แผนภาพกล่อง)")
class FiveNumberSummaryM3(ChoiceType):
    def compose(self, rng: Random):
        n = rng.choice((7, 11))
        data = sorted(rng.sample(range(10, 100), n))
        q1, med, q3 = data[(n + 1) // 4 - 1], data[(n + 1) // 2 - 1], data[3 * (n + 1) // 4 - 1]
        shown = data[:]
        rng.shuffle(shown)

        def five(xs) -> str:
            return ", ".join(map(str, xs))

        right = five((data[0], q1, med, q3, data[-1]))
        wrongs = [five((shown[0], q1, med, q3, shown[-1])) if (shown[0], shown[-1]) != (data[0], data[-1])
                  else five((data[0], data[1], med, data[-2], data[-1])),
                  five((data[0], data[(n + 1) // 4], med, data[3 * (n + 1) // 4 - 2], data[-1])),
                  five((data[0], q1, shown[n // 2], q3, data[-1])) if shown[n // 2] != med
                  else five((data[1], q1, med, q3, data[-2]))]
        stem = (f"ข้อมูลชุดหนึ่งคือ {', '.join(map(str, shown))} ค่าสรุปห้าค่า "
                "(ค่าต่ำสุด, Q1, มัธยฐาน, Q3, ค่าสูงสุด) คือข้อใด")
        return stem, right, _tk3(*wrongs, five((data[0], q1, med, q3, data[-1] + 1)), answer=right)[:3]
