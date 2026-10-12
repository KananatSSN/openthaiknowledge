"""การวัดการกระจาย

คณิตศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ค 3.1 ม.6/1

Sets moved here from: math, math_bank_stats, math_data, math_m6.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_bank_stats import M6, _num_q, median, num
from otk.sets._support.math_data import _seq
from otk.sets._support.math_m4 import maths as _maths
from otk.sets._support.math_m6 import _dec
from otk.sets._support.math_p2 import _texts

SPREAD = "การวัดการกระจาย"


def variance_from_shifted_squares(n: int, xbar: Fraction, c: Fraction, total: Fraction) -> Fraction:
    """σ² from Σ(x − c)² = total: Σ(x − c)² = Nσ² + N(x̄ − c)²."""
    return total / n - (xbar - c) ** 2


def pooled_variance(groups: list[tuple[int, Fraction, Fraction]]) -> Fraction:
    """Population variance of the union of groups (n, mean, Σ(x − mean)²)."""
    n = sum(g[0] for g in groups)
    m = sum(g[0] * g[1] for g in groups) / n
    return (sum(g[2] + g[0] * (g[1] - m) ** 2 for g in groups)) / n


def weighted_abs_min(points: list[tuple[int, int]]) -> tuple[Fraction, Fraction]:
    """(argmin, min) of Σ wᵢ|aᵢ − x| over x: attained at a weighted median, which is one of the aᵢ."""
    best = None
    for a, _ in points:
        v = sum(w * abs(p - a) for p, w in points)
        if best is None or v < best[1]:
            best = (Fraction(a), Fraction(v))
    return best


@question_type("math.range_of_data", display_name={"th": "พิสัยของข้อมูล"},
               level={"th": "ม.6"}, topic="การวัดการกระจาย")
class RangeOfData(MathType):
    def expr(self, rng: Random, count_lo: int = 5, count_hi: int = 9,
             value_hi: int = 80):
        n = rng.randint(count_lo, count_hi)
        data = rng.sample(range(1, value_hi), n)
        return MathDraw(
            _seq(data), str(max(data) - min(data)),
            prompt="จงหาพิสัยของข้อมูลชุดนี้",
            distractors=[str(max(data)), str(min(data)),
                         str(max(data) + min(data))])
RangeOfData.PROVENANCE = Provenance("original")


@question_type("math.variance",
               display_name={"th": "ความแปรปรวน"}, level={"th": "ม.6"},
               topic="การวัดการกระจาย")
class Variance(WordProblem):
    _PATTERNS = [((-2, -1, 0, 1, 2), 2), ((-3, -1, 0, 1, 3), 4),
                 ((-4, -2, 0, 2, 4), 8)]

    def expr(self, rng: Random):
        devs, var = rng.choice(self._PATTERNS)
        mean = rng.randint(5, 20)
        data = sorted(mean + d for d in devs)
        sumsq = sum(d * d for d in devs)
        listed = ", ".join(map(str, data))
        prompt = rng.choice((
            f"จากข้อมูล {listed} (ค่าเฉลี่ย {mean}) ความแปรปรวนเท่ากับเท่าใด?",
            f"อายุ (ปี) ของเด็ก 5 คนในบ้านหลังหนึ่งคือ {listed} มีค่าเฉลี่ย {mean} ปี "
            f"ความแปรปรวนของอายุเท่ากับเท่าใด",
            f"จำนวนชั่วโมงที่นักเรียน 5 คนดูโทรทัศน์ในสัปดาห์หนึ่งคือ {listed} มีค่าเฉลี่ย {mean} ชั่วโมง "
            f"ความแปรปรวนเท่ากับเท่าใด",
        ))
        return MathDraw("", str(var), prompt=prompt,
                        distractors=[str(sumsq), str(var + 1), str(var * 5)])
Variance.PROVENANCE = Provenance("original")


@question_type("math.standard_deviation", display_name={"th": "ส่วนเบี่ยงเบนมาตรฐาน"},
               level={"th": "ม.6"}, topic="การวัดการกระจาย")
class StandardDeviation(MathType):
    """Deviations are chosen to make the variance a perfect square, so the
    standard deviation is a whole number rather than a rounded one."""

    def expr(self, rng: Random, mean_hi: int = 40):
        mean = rng.randint(5, mean_hi)
        # Symmetric deviations ±d over 4 points: variance = d², sd = d.
        d = rng.randint(1, 9)
        data = [mean - d, mean - d, mean + d, mean + d]
        rng.shuffle(data)
        prompt = rng.choice((
            "จงหาส่วนเบี่ยงเบนมาตรฐานของข้อมูลชุดนี้ (ประชากร)",
            "คะแนนสอบของนักเรียนทั้ง 4 คนในกลุ่มเป็นดังนี้ จงหาส่วนเบี่ยงเบนมาตรฐานของคะแนน (ประชากร)",
            "น้ำหนัก (กิโลกรัม) ของลูกสุนัขทั้ง 4 ตัวในครอกเป็นดังนี้ จงหาส่วนเบี่ยงเบนมาตรฐาน (ประชากร)",
        ))
        return MathDraw(
            _seq(data), str(d), prompt=prompt,
            distractors=[str(d * d), str(mean), str(2 * d)])
StandardDeviation.PROVENANCE = Provenance("original")


@question_type("math.stats_transform_m6",
               display_name={"th": "การแปลงข้อมูลเชิงเส้นและผลบวกกำลังสอง"},
               level=M6, topic=SPREAD)
class StatsTransformM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(5)
        if kind == 0:
            a = rng.choice((Fraction(11, 10), Fraction(2), Fraction(3), Fraction(1, 2), Fraction(-2), Fraction(5, 4)))
            b = rng.choice((Fraction(1, 4), Fraction(3), Fraction(-5), Fraction(10), Fraction(1, 2)))
            xbar, s = Fraction(rng.randint(2, 40)), Fraction(rng.randint(2, 12))
            ask = rng.choice(("mean", "sd", "var"))
            line = f"y = {num(b)} {'+' if a > 0 else '-'} {num(abs(a))}x"
            stem = [text("ข้อมูล x ชุดหนึ่งมีค่าเฉลี่ยเลขคณิต"), content_math(num(xbar)),
                    text("และส่วนเบี่ยงเบนมาตรฐาน"), content_math(num(s)), text("ถ้าแปลงข้อมูลทุกค่าด้วย"),
                    content_math(line)]
            if ask == "mean":
                stem.append(text("ค่าเฉลี่ยเลขคณิตของ y เท่ากับเท่าใด"))
                # b dropped; a applied to b too; x̄ + b.
                return _num_q(stem, a * xbar + b, [a * xbar, a * (xbar + b), xbar + b], self.topic)
            if ask == "sd":
                stem.append(text("ส่วนเบี่ยงเบนมาตรฐานของ y เท่ากับเท่าใด"))
                # b added; a² instead of |a|; a with its sign.
                return _num_q(stem, abs(a) * s, [abs(a) * s + b, a * a * s, a * s], self.topic)
            stem.append(text("ความแปรปรวนของ y เท่ากับเท่าใด"))
            # |a|·s²; a²s; (as + b)².
            return _num_q(stem, a * a * s * s, [abs(a) * s * s, a * a * s, (a * s + b) ** 2], self.topic)
        if kind == 1:
            n = rng.choice((10, 11, 12, 20, 25))
            xbar, c = rng.randint(10, 40), 0
            while c == xbar or c == 0:
                c = xbar + rng.randint(-4, 4)
            var = rng.randint(4, 100)
            total = n * (var + (xbar - c) ** 2)
            stem = [text("ให้"), content_math(rf"a_{{1}}, a_{{2}}, \ldots, a_{{{n}}}"),
                    text(f"เป็นข้อมูลที่มีค่าเฉลี่ยเลขคณิตเท่ากับ {xbar} ถ้า"),
                    content_math(rf"\sum_{{i=1}}^{{{n}}} (a_{{i}} - {c})^{{2}} = {num(total)}"),
                    text("แล้วความแปรปรวนของข้อมูลชุดนี้เท่ากับเท่าใด")]
            right = variance_from_shifted_squares(n, Fraction(xbar), Fraction(c), Fraction(total))
            # Forgetting the shift; adding it; dividing by n − 1.
            named = [Fraction(total, n), Fraction(total, n) + (xbar - c) ** 2, Fraction(total, n - 1) - (xbar - c) ** 2]
            return _num_q(stem, right, named, self.topic)
        if kind == 2:
            k = rng.choice((1, 2, 3))
            xbar, s = rng.randint(20, 1500), rng.randint(2, 40)
            lo, hi = xbar - k * s, xbar + k * s
            ask = rng.choice(("sd", "cv"))
            stem = [text("ข้อมูลชุดหนึ่งมีการกระจายแบบสมมาตร ถ้าช่วง"), content_math(rf"(\bar{{x}} - {k}s,\ \bar{{x}} + {k}s)"),
                    text("เท่ากับ"), content_math(f"({num(lo)},\\ {num(hi)})")]
            if ask == "sd":
                stem.append(text("ส่วนเบี่ยงเบนมาตรฐานเท่ากับเท่าใด"))
                # The half-width; the width; divided by 2k … with k forgotten.
                return _num_q(stem, s, [k * s, 2 * k * s, Fraction(hi - lo, 2 * k + 2)], self.topic)
            stem.append(text("สัมประสิทธิ์การแปรผัน (s/x̄) เท่ากับเท่าใด"))
            return _num_q(stem, Fraction(s, xbar), [Fraction(k * s, xbar), Fraction(xbar, s), Fraction(s, hi)],
                          self.topic)
        if kind == 3:
            groups = []
            for _ in range(2):
                n = rng.randint(4, 12)
                groups.append((n, Fraction(rng.randint(10, 30)), Fraction(n * rng.randint(1, 20))))
            right = pooled_variance(groups)
            (n1, m1, s1), (n2, m2, s2) = groups
            stem = [text("ข้อมูลชุดที่ 1 มี"), content_math(f"{n1}"), text("ตัว ค่าเฉลี่ยเลขคณิต"), content_math(num(m1)),
                    text("และ"), content_math(rf"\sum (x_{{i}} - \bar{{x}})^{{2}} = {num(s1)}"),
                    text("ข้อมูลชุดที่ 2 มี"), content_math(f"{n2}"), text("ตัว ค่าเฉลี่ยเลขคณิต"), content_math(num(m2)),
                    text("และ"), content_math(rf"\sum (y_{{i}} - \bar{{y}})^{{2}} = {num(s2)}"),
                    text("ความแปรปรวนของข้อมูลทั้งสองชุดรวมกันเท่ากับเท่าใด")]
            # The within-group part only; the mean of the two variances; the between part forgotten … squared.
            named = [(s1 + s2) / (n1 + n2), (s1 / n1 + s2 / n2) / 2,
                     (s1 + s2 + (m1 - m2) ** 2) / (n1 + n2)]
            return _num_q(stem, right, named, self.topic)
        while True:
            pts = sorted({rng.randint(-3, 9) for _ in range(rng.randint(4, 6))})
            if len(pts) >= 4:
                break
        points = [(a, rng.choice((1, 2))) for a in pts]
        _, right = weighted_abs_min(points)
        terms = " + ".join(("" if w == 1 else str(w)) + f"|{a} - x|" for a, w in points)
        stem = [text("ให้ x เป็นจำนวนจริงใด ๆ ค่าต่ำสุดของ"), content_math(terms), text("เท่ากับเท่าใด")]
        # Evaluated at the mean; at the plain (unweighted) median; the range.
        mean_x = Fraction(sum(a * w for a, w in points), sum(w for _, w in points))
        at = lambda x: sum(w * abs(a - x) for a, w in points)
        named = [at(mean_x), at(median([a for a, _ in points])), pts[-1] - pts[0]]
        return _num_q(stem, right, named, self.topic)
StatsTransformM6.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/16 สถิติ',))


@question_type("math.coefficient_of_variation_m6",
               display_name={"th": "สัมประสิทธิ์การแปรผัน: เปรียบเทียบการกระจาย"},
               level=M6, topic="การวัดการกระจาย")
class CoefficientOfVariationM6(QuestionType):
    _PAIRS = (("ห้อง ก", "ห้อง ข"), ("โรงงาน A", "โรงงาน B"), ("นักวิ่งคนแรก", "นักวิ่งคนที่สอง"))

    def build(self, rng: Random) -> GeneratedQuestion:
        x, y = rng.choice(self._PAIRS)
        m1, m2 = rng.randrange(20, 90, 5), rng.randrange(20, 90, 5)
        s1, s2 = rng.randint(2, 15), rng.randint(2, 15)
        cv1, cv2 = Fraction(s1, m1), Fraction(s2, m2)
        if cv1 == cv2 or (s1 > s2) == (cv1 > cv2):
            # Keep the raw spread pointing the wrong way: that is what CV corrects.
            s1, s2 = s2, s1
            cv1, cv2 = Fraction(s1, m1), Fraction(s2, m2)
        if cv1 == cv2:
            return self.build(rng)
        if rng.random() < 0.5:
            cv = _dec(cv1 * 100)
            return _maths([text(f"ข้อมูลชุดหนึ่งมีค่าเฉลี่ย {m1} และส่วนเบี่ยงเบนมาตรฐาน {s1} "
                                f"สัมประสิทธิ์การแปรผันเท่ากับร้อยละเท่าใด")], cv,
                          [_dec(Fraction(m1 * 100, s1)), _dec(cv1), _dec(cv1 * 100 + 1)], self.topic)
        more = x if cv1 > cv2 else y
        other = y if more == x else x
        return _texts([text(f"{x} มีค่าเฉลี่ย {m1} ส่วนเบี่ยงเบนมาตรฐาน {s1} และ {y} มีค่าเฉลี่ย {m2} "
                            f"ส่วนเบี่ยงเบนมาตรฐาน {s2} ข้อมูลของใครมีการกระจายสัมพัทธ์มากกว่า")],
                      more, [other, "เท่ากัน", "เปรียบเทียบไม่ได้"], self.topic)
CoefficientOfVariationM6.PROVENANCE = Provenance("original")
