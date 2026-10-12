"""สถิติ

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: ค 3.1 ม.2/*

Sets moved here from: math, math_data, math_m2, math_pictures_hi.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_data import _seq
from otk.sets._support.math_diagrams import _math_q, _text_q
from otk.sets._support.math_m2 import LEVEL
from otk.sets._support.math_p2 import _maths, _texts
from otk.sets._support.math_pictures import _near
from otk.sets._support.math_pictures_hi import DOT_PLOTS, HISTOGRAMS

PROVENANCE = Provenance("original")


NL = chr(10)       # a new stem line


_STAT_TOPIC = "สถิติ"


def _median(xs: list[int]) -> Fraction:
    s = sorted(xs)
    n = len(s)
    return Fraction(s[n // 2]) if n % 2 else Fraction(s[n // 2 - 1] + s[n // 2], 2)


def _num(v: Fraction) -> str:
    return str(v.numerator) if v.denominator == 1 else str(float(v))


DOT_ALT = "แผนภาพจุด แต่ละจุดแทนข้อมูลหนึ่งค่า"


HIST_ALT = "ฮิสโทแกรมแสดงความถี่ของข้อมูลในแต่ละอันตรภาคชั้น"


_HIST_CONTEXT = {10: "คะแนนสอบ (คะแนน)", 5: "ความสูงของนักเรียน (เซนติเมตร)"}


@question_type("math.central_tendency",
               display_name={"th": "ค่ากลางของข้อมูล"}, level={"th": "ม.3"},
               topic="สถิติ")
class CentralTendency(WordProblem):
    def expr(self, rng: Random):
        v = rng.randint(1, 9)
        while True:
            others = rng.sample([x for x in range(1, 15) if x != v], 3)
            data = [v, v] + others
            if sum(data) % 5 == 0:                  # integer mean
                break
        sd = sorted(data)
        mean, median, mode = sum(data) // 5, sd[2], v
        kind, name, ans = rng.choice([
            ("mean", "ค่าเฉลี่ยเลขคณิต", mean),
            ("median", "มัธยฐาน", median),
            ("mode", "ฐานนิยม", mode)])
        return MathDraw("", str(ans),
                        prompt=f"จากข้อมูล {', '.join(map(str, data))} จงหา{name}",
                        distractors=[str(x) for x in (mean, median, mode)
                                     if x != ans])


@question_type("math.dot_plot_m2",
               display_name={"th": "แผนภาพจุด"},
               level=LEVEL, topic=_STAT_TOPIC)
class DotPlotM2(WordProblem):
    def expr(self, rng: Random):
        values = list(range(rng.randint(0, 3), rng.randint(0, 3) + 6))
        counts = [rng.randint(0, 6) for _ in values]
        while counts.count(max(counts)) > 1 or sum(counts) < 6:
            counts = [rng.randint(0, 6) for _ in values]
        what = rng.choice(("จำนวนหนังสือที่นักเรียนแต่ละคนอ่านในเดือนนี้", "จำนวนพี่น้องของนักเรียนแต่ละคน",
                           "จำนวนประตูที่ทีมยิงได้ในแต่ละนัด"))
        rows = [f"{v}: " + " ".join("●" * c) for v, c in zip(values, counts)]
        plot = f"แผนภาพจุดแสดง{what} (● 1 จุดแทนข้อมูล 1 ค่า){NL}" + NL.join(rows)
        data = [v for v, c in zip(values, counts) for _ in range(c)]
        kind = rng.randrange(3)
        if kind == 0:
            mode = values[counts.index(max(counts))]
            return MathDraw("", str(mode), prompt=f"{plot}{NL}ฐานนิยมของข้อมูลคือเท่าใด",
                            distractors=_story.keep(max(counts), values[-1], mode + 1,
                                                    answer=mode, lo=0))
        if kind == 1:
            return MathDraw("", str(len(data)), prompt=f"{plot}{NL}ข้อมูลชุดนี้มีทั้งหมดกี่ค่า",
                            distractors=_story.keep(len(values), sum(data), len(data) + 1,
                                                    answer=len(data), lo=1))
        total = sum(data)
        return MathDraw("", str(total), prompt=f"{plot}{NL}ผลรวมของข้อมูลทั้งหมดเท่ากับเท่าใด",
                        distractors=_story.keep(sum(values), len(data), total + values[-1],
                                                answer=total, lo=1))


@question_type("math.dot_plot_picture_m2", display_name={"th": "อ่านแผนภาพจุดจากภาพ"},
               level={"th": "ม.2"}, topic="สถิติ")
class DotPlotPictureM2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(DOT_PLOTS)
        data = p.data
        lead = text("แผนภาพจุดแสดงจำนวนประตูที่ทีมหนึ่งยิงได้ในแต่ละนัด (1 จุด แทน 1 นัด)")
        img = image(p.asset_id, alt=DOT_ALT)
        ask = rng.randrange(3)
        if ask == 0:
            mode = max(set(data), key=data.count)
            # The tallest stack's height rather than its value.
            return _math_q([lead, text("ฐานนิยมของข้อมูลนี้คือเท่าใด"), img], str(mode),
                           _near(mode, data.count(mode), max(data), len(data), lo=0), self.topic)
        if ask == 1:
            return _math_q([lead, text("ทีมนี้แข่งทั้งหมดกี่นัด"), img], str(len(data)),
                           _near(len(data), len(p.counts), sum(data), max(p.counts), lo=1), self.topic)
        k = p.start + len(p.counts) // 2
        n = sum(1 for v in data if v >= k)
        return _math_q([lead, text(f"มีกี่นัดที่ทีมนี้ยิงได้ตั้งแต่ {k} ประตูขึ้นไป"), img], str(n),
                       _near(n, sum(1 for v in data if v > k), len(data) - n, data.count(k), lo=0),
                       self.topic)


@question_type("math.median_from_data", display_name={"th": "มัธยฐานของข้อมูล"},
               level={"th": "ม.3"}, topic="สถิติ")
class MedianFromData(MathType):
    def expr(self, rng: Random, count_lo: int = 5, count_hi: int = 11,
             value_hi: int = 50):
        n = rng.choice(range(count_lo | 1, count_hi + 1, 2))   # odd → exact
        data = rng.sample(range(1, value_hi), n)
        median = sorted(data)[n // 2]
        return MathDraw(
            _seq(data), str(median), prompt="จงหามัธยฐานของข้อมูลชุดนี้",
            # The middle of the list *as given*, before sorting.
            distractors=[str(data[n // 2]), str(max(data)), str(min(data))])


@question_type("math.stem_and_leaf_m2",
               display_name={"th": "แผนภาพต้น-ใบ"},
               level=LEVEL, topic=_STAT_TOPIC)
class StemAndLeafM2(WordProblem):
    def expr(self, rng: Random):
        stems = sorted(rng.sample(range(3, 10), 4))
        data = sorted(10 * s + rng.randint(0, 9) for s in stems for _ in range(rng.randint(1, 4)))
        rows = [f"{s} | " + " ".join(str(v % 10) for v in data if v // 10 == s) for s in stems]
        plot = (f"แผนภาพต้น-ใบแสดงคะแนนสอบของนักเรียนกลุ่มหนึ่ง (ต้นเป็นหลักสิบ ใบเป็นหลักหน่วย){NL}"
                + NL.join(rows))
        kind = rng.randrange(4)
        if kind == 0:
            return MathDraw("", str(len(data)), prompt=f"{plot}{NL}นักเรียนกลุ่มนี้มีกี่คน",
                            # Counting stems instead of leaves.
                            distractors=_story.keep(len(stems), len(data) + 1, len(data) - 1,
                                                    answer=len(data), lo=1))
        if kind == 1:
            rng_ = data[-1] - data[0]
            return MathDraw("", str(rng_), prompt=f"{plot}{NL}พิสัยของคะแนนเท่ากับเท่าใด",
                            distractors=_story.keep(data[-1], stems[-1] - stems[0],
                                                    data[-1] + data[0], answer=rng_, lo=1))
        if kind == 2:
            cut = 10 * stems[2]
            ans = sum(1 for v in data if v >= cut)
            return MathDraw("", str(ans),
                            prompt=f"{plot}{NL}มีนักเรียนที่ได้คะแนนตั้งแต่ {cut} คะแนนขึ้นไปกี่คน",
                            distractors=_story.keep(len(data) - ans, ans + 1,
                                                    sum(1 for v in data if v > cut), answer=ans, lo=0))
        med = _median(data)
        return MathDraw("", _num(med), prompt=f"{plot}{NL}มัธยฐานของคะแนนเท่ากับเท่าใด",
                        distractors=[x for x in dict.fromkeys(
                            [_num(Fraction(data[len(data) // 2 - 1])), _num(Fraction(sum(data), len(data))
                                                                         .limit_denominator(1)),
                             _num(Fraction(data[0] + data[-1], 2)), _num(med + 1), _num(med - 1)])
                            if x != _num(med)])


@question_type("math.histogram_picture_m2", display_name={"th": "อ่านฮิสโทแกรมจากภาพ"},
               level={"th": "ม.2"}, topic="สถิติ")
class HistogramPictureM2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        h = rng.choice(HISTOGRAMS)
        lead = text(f"ฮิสโทแกรมแสดง{_HIST_CONTEXT[h.width]} ของนักเรียนกลุ่มหนึ่ง "
                    "แกนนอนบอกขอบเขตของแต่ละชั้น แกนตั้งบอกความถี่")
        img = image(h.asset_id, alt=HIST_ALT)
        n = len(h.freq)
        ask = rng.randrange(3)
        if ask == 0:
            i = rng.randrange(n)
            f = h.freq[i]
            return _math_q([lead, text(f"ชั้น {h.label(i)} มีความถี่เท่าใด"), img], str(f),
                           _near(f, h.freq[i - 1] if i else h.freq[1], f + 1, f + 2, lo=1), self.topic)
        if ask == 1:
            total = sum(h.freq)
            return _math_q([lead, text("นักเรียนกลุ่มนี้มีทั้งหมดกี่คน"), img], str(total),
                           _near(total, n, max(h.freq), total - h.freq[0], lo=1), self.topic)
        best = max(range(n), key=lambda i: h.freq[i])
        others = [h.label(i) for i in range(n) if i != best]
        return _text_q([lead, text("ชั้นใดมีความถี่มากที่สุด"), img], h.label(best),
                       [others[(best + k) % len(others)] for k in range(3)], self.topic)


@question_type("math.grouped_frequency_m2",
               display_name={"th": "ตารางแจกแจงความถี่แบบอันตรภาคชั้นและฮิสโทแกรม"},
               level=LEVEL, topic=_STAT_TOPIC)
class GroupedFrequencyM2(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random) -> GeneratedQuestion:
        width = rng.choice((5, 10))
        start = rng.choice((20, 30, 40, 50))
        bins = [(start + i * width, start + (i + 1) * width - 1) for i in range(5)]
        freq = [rng.randint(1, 15) for _ in bins]
        while freq.count(max(freq)) > 1:
            freq = [rng.randint(1, 15) for _ in bins]
        what = rng.choice(("คะแนนสอบ", "น้ำหนักของนักเรียน (กิโลกรัม)",
                           "ความสูงของต้นกล้า (เซนติเมตร)"))
        lines = [f"ตารางแจกแจงความถี่ของ{what}", "อันตรภาคชั้น | ความถี่"]
        lines += [f"{a} – {b} | {f}" for (a, b), f in zip(bins, freq)]
        table = NL.join(lines)
        kind = rng.randrange(3)
        if kind == 0:
            i = freq.index(max(freq))
            right = f"{bins[i][0]} – {bins[i][1]}"
            others = [f"{a} – {b}" for (a, b), f in zip(bins, freq) if f != max(freq)]
            return _texts([text(table), text("อันตรภาคชั้นใดมีความถี่มากที่สุด")], right,
                          others[:3], self.topic)
        if kind == 1:
            cut = bins[2][0]
            ans = sum(f for (a, _), f in zip(bins, freq) if a >= cut)
            return _maths([text(table), text(f"ข้อมูลที่มีค่าตั้งแต่ {cut} ขึ้นไปมีกี่ค่า")], str(ans),
                          _story.keep(sum(freq) - ans, ans - freq[2], sum(freq), ans + 1,
                                      answer=ans, lo=0), self.topic)
        return _maths([text(table), text("ความกว้างของอันตรภาคชั้นเท่ากับเท่าใด")], str(width),
                      _story.keep(width - 1, width + 1, 5 * width, bins[0][0], answer=width, lo=1),
                      self.topic)
