"""ค่าสูงสุด-ต่ำสุดสัมพัทธ์

คณิตศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม แคลคูลัส 1 ม.6/2

Sets moved here from: math, math_apply_add, math_bank_calculus, math_m6, math_pictures_add, math_thin_topics.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import image, text
from otk.core.content import math as content_math
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_tex, poly_tex
from otk.sets._support.math_apply_add import M6, _c
from otk.sets._support.math_bank_calculus import M6 as M6_math_bank_calculus
from otk.sets._support.math_bank_calculus import _num_q, _tex_q, peval
from otk.sets._support.math_diagrams import _text_q
from otk.sets._support.math_m4 import maths as _num_maths
from otk.sets._support.math_pictures_add import DERIV_CURVES

EXTREMA = "ค่าสูงสุด-ต่ำสุดสัมพัทธ์"


def cubic_from_critical(k: int, p: int, q: int, c: Fraction) -> list[Fraction]:
    """kx³ + ax² + bx + c with f′(x) = 3k(x − p)(x − q): a = −3k(p + q)/2, b = 3kpq."""
    return [Fraction(k), Fraction(-3 * k * (p + q), 2), Fraction(3 * k * p * q), Fraction(c)]


def critical_statements(k: int, p: int, q: int) -> list[tuple[str, bool]]:
    """Statements about f with critical points p < q and leading coefficient k (Thai text, truth)."""
    up = k > 0                      # f′ > 0 outside (p, q) when k > 0
    return [
        (f"f มีค่าสูงสุดสัมพัทธ์ที่ x = {p}", up),
        (f"f มีค่าต่ำสุดสัมพัทธ์ที่ x = {q}", up),
        (f"f มีค่าต่ำสุดสัมพัทธ์ที่ x = {p}", not up),
        (f"f มีค่าสูงสุดสัมพัทธ์ที่ x = {q}", not up),
        (f"บนช่วง ({p}, {q}) f เป็นฟังก์ชันเพิ่ม", not up),
        (f"บนช่วง ({p}, {q}) f เป็นฟังก์ชันลด", up),
        (f"บนช่วง (−∞, {p}) f เป็นฟังก์ชันลด", not up),
        (f"บนช่วง ({q}, ∞) f เป็นฟังก์ชันเพิ่ม", up),
    ]


def symmetric_statements(p: int) -> list[tuple[str, bool]]:
    """f cubic with critical points ±p (so f(x) − f(0) is odd) and f(0) ≠ 0 unknown: (text, truth)."""
    return [
        (f"f′′(−{p}) · f′′({p}) < 0", True),
        (f"f(−{p}) + f({p}) = 2f(0)", True),
        ("ค่าเฉลี่ยเลขคณิตของ f(−2), f(−1), f(0), f(1), f(2) เท่ากับ f(0)", True),
        (f"f({p}√3) = f(0)", True),
        (f"f({p}√3) = 2f(0)", False),
        (f"f(−{p}) = f({p})", False),
        ("f′(0) = 0", False),
    ]


def _lab(i: int) -> str:
    return ("ก.", "ข.", "ค.", "ง.")[i]


M5 = {"th": "ม.5"}


DERIV_ALT = "กราฟของ y = f(x) มีจุด A ถึง E อยู่บนกราฟ เรียงจากซ้ายไปขวา"


_LETTERS = "ABCDE"


def _cubic(rng: Random):
    """x³ + px² + qx + r with turning points at two whole numbers r1 < r2."""
    while True:
        r1, r2 = sorted(rng.sample(range(-4, 5), 2))
        if (r1 + r2) % 2 == 0:
            break
    p, q, r = -3 * (r1 + r2) // 2, 3 * r1 * r2, rng.randint(-5, 5)
    return r1, r2, (p, q, r)


@question_type("math.derivative_sign_picture_m6",
               display_name={"th": "อ่านเครื่องหมายของอนุพันธ์และจุดวกกลับจากกราฟ"},
               level={"th": "ม.6"}, topic="ค่าสูงสุด-ต่ำสุดสัมพัทธ์")
class DerivativeSignPictureM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        c = rng.choice(DERIV_CURVES)
        maxi = c.p if c.s > 0 else c.q
        mini = c.q if c.s > 0 else c.p

        def sign(x):
            v = c.s * (x - c.p) * (x - c.q)
            return (v > 0) - (v < 0)

        groups = {
            "จุดใดเป็นจุดสูงสุดสัมพัทธ์": [i for i, x in enumerate(c.xs) if x == maxi],
            "จุดใดเป็นจุดต่ำสุดสัมพัทธ์": [i for i, x in enumerate(c.xs) if x == mini],
            "ที่จุดใด f′(x) > 0": [i for i, x in enumerate(c.xs) if sign(x) > 0],
            "ที่จุดใด f′(x) < 0": [i for i, x in enumerate(c.xs) if sign(x) < 0],
        }
        asks = [k for k, v in groups.items() if len(v) == 1]
        ask = rng.choice(asks)
        [i] = groups[ask]
        wrong = [_LETTERS[j] for j in range(5) if j != i]
        rng.shuffle(wrong)
        return _text_q([text(f"จากกราฟของ y = f(x) ในภาพ {ask}"), image(c.asset_id, alt=DERIV_ALT)],
                       _LETTERS[i], wrong[:3], self.topic)
DerivativeSignPictureM6.PROVENANCE = Provenance("original")


@question_type("math.turning_point_m5", display_name={"th": "ค่าสูงสุดและค่าต่ำสุดสัมพัทธ์ของฟังก์ชันกำลังสาม"},
               level=M5, topic="ค่าสูงสุด-ต่ำสุดสัมพัทธ์")
class TurningPointM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        r1, r2, (p, q, r) = _cubic(rng)
        f = lambda x: x ** 3 + p * x * x + q * x + r
        fn = content_math("f(x) = " + poly_tex((1, "x^{3}"), (p, "x^{2}"), (q, "x"), (r, "")))
        kind = rng.randrange(3)
        # The leading coefficient is positive: the maximum comes first.
        if kind == 0:
            return _num_maths([text("ฟังก์ชัน"), fn, text("มีค่าสูงสุดสัมพัทธ์ที่ x เท่าใด")], str(r1),
                              [str(r2), str(r1 + r2), str(-r1)], self.topic)
        if kind == 1:
            return _num_maths([text("ฟังก์ชัน"), fn, text("มีค่าต่ำสุดสัมพัทธ์ที่ x เท่าใด")], str(r2),
                              [str(r1), str(r1 + r2), str(-r2)], self.topic)
        return _num_maths([text("ค่าสูงสุดสัมพัทธ์ของฟังก์ชัน"), fn, text("เท่ากับเท่าใด")], str(f(r1)),
                          [str(f(r2)), str(r1), str(f(0))], self.topic)
TurningPointM5.PROVENANCE = Provenance("original")


@question_type("math.extrema",
               display_name={"th": "ค่าสูงสุด-ต่ำสุดสัมพัทธ์"}, level={"th": "ม.5"},
               topic="ค่าสูงสุด-ต่ำสุดสัมพัทธ์")
class Extrema(MathType):
    def expr(self, rng: Random):
        while True:
            r1, r2 = sorted(rng.sample(range(-4, 5), 2))
            if (r1 + r2) % 2 == 0:
                break
        c2 = -3 * (r1 + r2) // 2
        c1 = 3 * r1 * r2
        c0 = rng.randint(-5, 5)
        f = lambda x: x ** 3 + c2 * x * x + c1 * x + c0
        poly = poly_tex((1, "x^{3}"), (c2, "x^{2}"), (c1, "x"), (c0, ""))
        return MathDraw(
            rf"y = {poly}",
            rf"\text{{max}} \; ({r1}, {f(r1)}), \;\; \text{{min}} \; ({r2}, {f(r2)})",
            hint=r"\text{solve } y' = 0", prompt="จงหาจุดสูงสุดและต่ำสุดสัมพัทธ์")
Extrema.PROVENANCE = Provenance("original")


@question_type("math.optimization_geometry_m6",
               display_name={"th": "โจทย์ปัญหาค่าสูงสุด (กล่อง รั้ว สี่เหลี่ยมใต้โค้ง ราคา)"},
               level=M6, topic="ค่าสูงสุด-ต่ำสุดสัมพัทธ์")
class OptimizationGeometryM6(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(5)
        if kind == 0:
            s = rng.choice((12, 18, 24, 30, 36))
            x, v = s // 6, 2 * s ** 3 // 27
            if rng.random() < 0.5:
                return MathDraw("", str(x),
                                prompt=(f"ตัดมุมทั้งสี่ของแผ่นสังกะสีรูปสี่เหลี่ยมจัตุรัสยาวด้านละ {s} เซนติเมตร "
                                        f"ออกเป็นสี่เหลี่ยมจัตุรัสด้านละ x เซนติเมตร แล้วพับเป็นกล่องไม่มีฝา "
                                        f"x ควรเป็นเท่าใดกล่องจึงจุได้มากที่สุด"),
                                distractors=_story.keep(s // 4, s // 3, s // 2, x + 1, answer=x, lo=1))
            return MathDraw("", _c(v),
                            prompt=(f"ตัดมุมทั้งสี่ของแผ่นสังกะสีรูปสี่เหลี่ยมจัตุรัสยาวด้านละ {s} เซนติเมตร "
                                    f"แล้วพับเป็นกล่องไม่มีฝา กล่องจุได้มากที่สุดกี่ลูกบาศก์เซนติเมตร"),
                            distractors=[_c((s // 4) * (s // 2) ** 2), _c((s // 3) * (s // 3) ** 2),
                                         _c(x * (s - x) ** 2)])
        if kind == 1:
            L = rng.choice((40, 80, 120, 200, 240))
            return MathDraw("", _c(L * L // 8),
                            prompt=(f"มีรั้วยาว {L} เมตร ต้องการล้อมที่ดินรูปสี่เหลี่ยมผืนผ้าติดริมแม่น้ำ "
                                    f"โดยไม่ต้องล้อมด้านที่ติดแม่น้ำ ล้อมได้พื้นที่มากที่สุดกี่ตารางเมตร"),
                            distractors=[_c(L * L // 16), _c(L * L // 9 if L % 3 == 0 else L * L // 12),
                                         _c(L * L // 4)])
        if kind == 2:
            k = rng.choice((1, 2, 3))
            c = 3 * k * k
            return MathDraw("", str(4 * k ** 3),
                            prompt=(f"สี่เหลี่ยมผืนผ้ารูปหนึ่งมีด้านหนึ่งอยู่บนแกน X และมีจุดยอดสองจุดอยู่บนพาราโบลา "
                                    f"y = {c} - x² พื้นที่มากที่สุดของสี่เหลี่ยมนี้เป็นกี่ตารางหน่วย"),
                            distractors=_story.keep(2 * k ** 3, 2 * k * c, k * c, 8 * k ** 3, answer=4 * k ** 3, lo=1))
        if kind == 3:
            S = rng.choice((9, 12, 15, 18, 24))
            y = 2 * S // 3
            best = (S - y) * y * y
            return MathDraw("", _c(best),
                            prompt=(f"จำนวนบวกสองจำนวน x และ y มีผลบวกเท่ากับ {S} "
                                    f"ค่ามากที่สุดของ xy² เป็นเท่าใด"),
                            distractors=[_c((S // 2) * (S - S // 2) ** 2), _c(y * (S - y) ** 2),
                                         _c(S ** 3 // 4)])
        n, k = rng.choice(((1000, 10), (1200, 20), (600, 5), (900, 15), (2000, 25)))
        p = n // (2 * k)
        return MathDraw("", _c(p),
                        prompt=(f"ถ้าตั้งราคาสินค้าชิ้นละ p บาท จะขายได้ {_c(n)} - {k}p ชิ้น "
                                f"ควรตั้งราคาชิ้นละกี่บาทจึงจะได้รายรับมากที่สุด"),
                        distractors=_story.keep(n // k, p * 2 - 1 if p > 1 else 3, n // (4 * k) or 1, p + k,
                                                answer=p, lo=1))
OptimizationGeometryM6.PROVENANCE = Provenance("original")


@question_type("math.cubic_critical_points_m6",
               display_name={"th": "สร้างฟังก์ชันกำลังสามจากค่าวิกฤต"},
               level=M6_math_bank_calculus, topic=EXTREMA)
class CubicCriticalPointsM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            k = rng.choice((1, -1))
            while True:
                p, q = sorted(rng.sample(range(-4, 5), 2))
                if (p + q) % 2 == 0:
                    break
            c = Fraction(rng.randint(-5, 6))
            f = cubic_from_critical(k, p, q, c)
            t = rng.choice([v for v in range(-3, 4) if v])
            lead = "x^{3}" if k == 1 else "-x^{3}"
            hi, lo = (p, q) if k == 1 else (q, p)
            stem = [text("ให้"), content_math(rf"f(x) = {lead} + ax^{{2}} + bx + c"),
                    text("เมื่อ a, b และ c เป็นจำนวนจริง ถ้า"), content_math(f"f(0) = {frac_tex(c)}"),
                    text(f"และ f มีค่าสูงสุดสัมพัทธ์ที่ x = {hi} และค่าต่ำสุดสัมพัทธ์ที่ x = {lo} แล้ว"),
                    content_math(f"f({t})"), text("เท่ากับเท่าใด")]
            # f′ taken as k(x − p)(x − q) (no factor 3); the b sign flipped; a sign flipped.
            no3 = [Fraction(k), Fraction(-k * (p + q), 2), Fraction(k * p * q), c]
            b_flip = [f[0], f[1], -f[2], f[3]]
            a_flip = [f[0], -f[1], f[2], f[3]]
            named = [peval(no3, t), peval(b_flip, t), peval(a_flip, t)]
            return _num_q(stem, peval(f, t), named, self.topic)
        if kind == 1:
            k = rng.choice((1, 1, -1))
            p, q = sorted(rng.sample(range(-4, 5), 2))
            picks = rng.sample(critical_statements(k, p, q), 4)
            lead = "x^{3}" if k == 1 else "-x^{3}"
            stem = [text("กำหนดให้"), content_math(rf"f(x) = {lead} + ax^{{2}} + bx + c"),
                    text(f"เมื่อ a, b, c เป็นจำนวนจริง ถ้า f มีค่าวิกฤตที่ x = {p} และ x = {q} "
                         "พิจารณาข้อความต่อไปนี้")]
            for i, (s, _) in enumerate(picks):
                stem.append(text(f"{_lab(i)} {s}"))
            stem.append(text("จำนวนข้อความที่ถูกต้องเท่ากับเท่าใด"))
            right = sum(t for _, t in picks)
            return _tex_q(stem, str(right), [str(v) for v in sorted(range(5), key=lambda v: abs(v - right))],
                          self.topic)
        p = rng.randint(1, 5)
        picks = rng.sample(symmetric_statements(p), 4)
        stem = [text(f"กำหนดให้ f(x) เป็นฟังก์ชันพหุนามดีกรีสาม ซึ่งมีค่าวิกฤตที่ x = {p} และ x = −{p} "
                     "พิจารณาข้อความต่อไปนี้")]
        for i, (s, _) in enumerate(picks):
            stem.append(text(f"{_lab(i)} {s}"))
        stem.append(text("จำนวนข้อความที่ถูกเท่ากับเท่าใด"))
        right = sum(t for _, t in picks)
        return _tex_q(stem, str(right), [str(v) for v in sorted(range(5), key=lambda v: abs(v - right))],
                      self.topic)
CubicCriticalPointsM6.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/15 แคลคูลัส',))


@question_type("math.optimization_word_m6",
               display_name={"th": "โจทย์ปัญหาค่าสูงสุดและค่าต่ำสุด (อนุพันธ์)"},
               level=M5, topic="ค่าสูงสุด-ต่ำสุดสัมพัทธ์")
class OptimizationWordM6(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            fence = 4 * rng.randint(10, 60)
            # Three sides fenced, the fourth a river: x(L − 2x), max at x = L/4.
            x = fence // 4
            area = x * (fence - 2 * x)
            return MathDraw("", f"{area:,}".replace(",", "{,}"),
                            prompt=(f"ต้องการล้อมรั้วที่ดินรูปสี่เหลี่ยมผืนผ้าริมแม่น้ำ โดยไม่ต้องล้อมด้านที่ติดแม่น้ำ "
                                    f"มีรั้วยาว {fence} เมตร จะล้อมได้พื้นที่มากที่สุดกี่ตารางเมตร"),
                            # Treating it as a four-sided square.
                            distractors=[f"{(fence // 4) ** 2:,}".replace(",", "{,}"),
                                         f"{(fence // 3) ** 2:,}".replace(",", "{,}"),
                                         f"{area // 2:,}".replace(",", "{,}")])
        if kind == 1:
            s = 2 * rng.randint(5, 30)
            return MathDraw("", str((s // 2) ** 2),
                            prompt=f"จำนวนจริงบวกสองจำนวนมีผลบวกเท่ากับ {s} ผลคูณของสองจำนวนนี้มีค่ามากที่สุดเท่าใด",
                            distractors=_story.keep(s * s // 4 - 1, s // 2, (s // 2) * (s // 2 + 1), s * s,
                                                    answer=(s // 2) ** 2))
        a = rng.randint(1, 5)
        b = 2 * a * rng.randint(1, 8)
        c = rng.randint(10, 80)
        t = b // (2 * a)
        top = -a * t * t + b * t + c
        return MathDraw(rf"h(t) = -{a if a > 1 else ''}t^{{2}} + {b}t + {c}", str(top),
                        prompt="ลูกบอลถูกโยนขึ้นไป ความสูง (เมตร) ที่เวลา t วินาทีเป็นไปตามฟังก์ชันนี้ ลูกบอลขึ้นไปได้สูงสุดกี่เมตร",
                        # The time of the peak instead of its height.
                        distractors=_story.keep(t, c, top + a, b * t + c, answer=top))
OptimizationWordM6.PROVENANCE = Provenance("original")
