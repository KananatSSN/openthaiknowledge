"""ฟังก์ชันตรีโกณมิติ

คณิตศาสตร์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 2 ม.5/1

Sets moved here from: math, math_bank_trig, math_diagrams_hi, math_geometry, math_m5, math_pictures_add.
"""

from __future__ import annotations

import math
from fractions import Fraction
from random import Random

from otk.core.content import image, text
from otk.core.content import math as content_math
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import ChoiceType, MathDraw, MathType, frac_tex
from otk.sets._support.math_bank_trig import M5, _frac_q, _tex_q, pi_tex, simplify_root, surd_tex
from otk.sets._support.math_diagrams import _img
from otk.sets._support.math_diagrams_hi import SINE_GRAPHS
from otk.sets._support.math_m4 import maths as _math_q
from otk.sets._support.math_m4 import maths as _maths
from otk.sets._support.math_pictures_add import UNIT_POINTS, _q


def _unit_trig(fn: str, deg: int):
    """Exact TeX for sin/cos/tan at a standard angle (0–330°); None if undefined."""
    ref = deg % 180
    if ref > 90:
        ref = 180 - ref
    mag = {
        "sin": {0: "0", 30: r"\frac{1}{2}", 45: r"\frac{\sqrt{2}}{2}",
                60: r"\frac{\sqrt{3}}{2}", 90: "1"},
        "cos": {0: "1", 30: r"\frac{\sqrt{3}}{2}", 45: r"\frac{\sqrt{2}}{2}",
                60: r"\frac{1}{2}", 90: "0"},
        "tan": {0: "0", 30: r"\frac{\sqrt{3}}{3}", 45: "1", 60: r"\sqrt{3}",
                90: None},
    }[fn][ref]
    if mag is None:
        return None
    if fn == "sin":
        neg = 180 < deg < 360
    elif fn == "cos":
        neg = 90 < deg < 270
    else:
        neg = (90 < deg < 180) or (270 < deg < 360)
    return "-" + mag if (neg and mag != "0") else mag


_UNIT_CIRCLE = [
    (tex, deg, _unit_trig(fn, deg))
    for deg in (0, 30, 45, 60, 90, 120, 135, 150, 180,
                210, 225, 240, 270, 300, 315, 330)
    for fn, tex in (("sin", r"\sin"), ("cos", r"\cos"), ("tan", r"\tan"))
    if _unit_trig(fn, deg) is not None
]


FUNCTIONS = "ฟังก์ชันตรีโกณมิติ"


def root_tex(q: Fraction) -> str:
    """√q for a rational q ≥ 0."""
    q = Fraction(q)
    k, m = simplify_root(q.numerator * q.denominator)
    return surd_tex(Fraction(k, q.denominator), m)


#: Angle t (as a multiple of π) → (cos t, sin t), each as (coefficient, radicand).
UNIT_CIRCLE: dict[Fraction, tuple[tuple[Fraction, int], tuple[Fraction, int]]] = {
    Fraction(1, 6): ((Fraction(1, 2), 3), (Fraction(1, 2), 1)),
    Fraction(1, 4): ((Fraction(1, 2), 2), (Fraction(1, 2), 2)),
    Fraction(1, 3): ((Fraction(1, 2), 1), (Fraction(1, 2), 3)),
    Fraction(1, 2): ((Fraction(0), 1), (Fraction(1), 1)),
    Fraction(2, 3): ((Fraction(-1, 2), 1), (Fraction(1, 2), 3)),
    Fraction(3, 4): ((Fraction(-1, 2), 2), (Fraction(1, 2), 2)),
    Fraction(5, 6): ((Fraction(-1, 2), 3), (Fraction(1, 2), 1)),
    Fraction(7, 6): ((Fraction(-1, 2), 3), (Fraction(-1, 2), 1)),
    Fraction(11, 6): ((Fraction(1, 2), 3), (Fraction(-1, 2), 1)),
}


def arc_to_point(r: int, t: Fraction) -> Fraction:
    """Arc from (r, 0) counter-clockwise to the point at angle tπ: s = r·tπ (returned in π units)."""
    return r * t


FUNCS = {"sin": r"\sin\theta", "cos": r"\cos\theta", "tan": r"\tan\theta",
         "cosec": r"\operatorname{cosec}\theta", "sec": r"\sec\theta", "cot": r"\cot\theta"}


RECIPROCAL = {"sin": "cosec", "cos": "sec", "tan": "cot", "cosec": "sin", "sec": "cos", "cot": "tan"}


#: TeX expression → the single function it reduces to (wherever both are defined).
REDUCIBLE = (
    (r"\sin\theta + \cos\theta\cot\theta", "cosec"),
    (r"\cos\theta + \sin\theta\tan\theta", "sec"),
    (r"\cot\theta\sec\theta", "cosec"),
    (r"\tan\theta\operatorname{cosec}\theta", "sec"),
    (r"\sin\theta\sec\theta", "tan"),
    (r"\cos\theta\operatorname{cosec}\theta", "cot"),
    (r"\frac{1 - \cos^{2}\theta}{\sin\theta}", "sin"),
    (r"(1 - \sin^{2}\theta)\sec\theta", "cos"),
    (r"\sec\theta - \sin\theta\tan\theta", "cos"),
    (r"\operatorname{cosec}\theta - \cos\theta\cot\theta", "sin"),
    (r"\frac{\sec^{2}\theta - 1}{\tan\theta}", "tan"),
    (r"(1 + \tan^{2}\theta)\cos\theta", "sec"),
    (r"(\operatorname{cosec}^{2}\theta - 1)\tan\theta", "cot"),
    (r"\frac{\tan\theta}{\sec\theta}", "sin"),
)


#: cos⁴A − sin⁴A and its relatives, with the factor applied to cos 2A.
POWER_FORMS = ((r"\cos^{4}A - \sin^{4}A", 1), (r"\sin^{4}A - \cos^{4}A", -1),
               (r"(\cos A - \sin A)(\cos A + \sin A)", 1))


def triple_angle_cos(k: int) -> Fraction:
    """cos 2θ when sin²3θ/sin²θ − cos²3θ/cos²θ = k: (2c + 1)² − (2c − 1)² = 8c."""
    return Fraction(k, 8)


TRIG = {"sin": math.sin, "cos": math.cos, "tan": math.tan,
        "cot": lambda t: 1 / math.tan(t), "sec": lambda t: 1 / math.cos(t),
        "cosec": lambda t: 1 / math.sin(t)}


COFUNCTION = {"sin": "cos", "cos": "sin", "tan": "cot", "cot": "tan", "sec": "cosec", "cosec": "sec"}


def reduce_angle(fn: str, k: int, sign: int) -> tuple[int, str]:
    """f(kπ/2 + sign·θ) = ±g(θ): g is f for even k, its cofunction for odd k.

    Read numerically at a non-special θ, where the ratio is exactly ±1.
    """
    theta = 0.3
    g = fn if k % 2 == 0 else COFUNCTION[fn]
    ratio = TRIG[fn](k * math.pi / 2 + sign * theta) / TRIG[g](theta)
    return (1 if ratio > 0 else -1), g


def _fn_tex(fn: str, arg: str) -> str:
    name = r"\operatorname{cosec}" if fn == "cosec" else "\\" + fn
    return f"{name} {arg}" if arg == r"\theta" else rf"{name}\left({arg}\right)"


def special(deg: int) -> tuple[tuple[Fraction, int], tuple[Fraction, int]]:
    """(cos, sin) of a multiple of 15° that has a table value, each as coefficient·√m."""
    deg %= 360
    table = {0: ((Fraction(1), 1), (Fraction(0), 1)), 180: ((Fraction(-1), 1), (Fraction(0), 1)),
             90: ((Fraction(0), 1), (Fraction(1), 1)), 270: ((Fraction(0), 1), (Fraction(-1), 1))}
    if deg in table:
        return table[deg]
    t = Fraction(deg, 180)
    if t in UNIT_CIRCLE:
        return UNIT_CIRCLE[t]
    (c, cm), (sn, sm) = UNIT_CIRCLE[2 - t]               # the mirror below the axis
    return (c, cm), (-sn, sm)


SPECIAL_DEGREES = (0, 30, 45, 60, 90, 120, 135, 150, 180, 210, 240, 270, 300, 330)


def surd_sum(terms: list[tuple[Fraction, int]]) -> list[tuple[Fraction, int]]:
    """Like radicands combined; zero terms dropped; ordered √m first, then rationals."""
    acc: dict[int, Fraction] = {}
    for c, m in terms:
        acc[m] = acc.get(m, Fraction(0)) + c
    return sorted(((c, m) for m, c in acc.items() if c), key=lambda t: -t[1])


def surd_sum_tex(terms: list[tuple[Fraction, int]]) -> str:
    terms = surd_sum(terms)
    if not terms:
        return "0"
    if len(terms) == 1:
        return surd_tex(*terms[0])
    den = math.lcm(*(c.denominator for c, _ in terms))
    parts = []
    for i, (c, m) in enumerate(terms):
        n = int(c * den)
        body = ("" if abs(n) == 1 and m != 1 else str(abs(n))) + (rf"\sqrt{{{m}}}" if m != 1 else "")
        parts.append(("-" if n < 0 else "") + body if i == 0 else f" {'-' if n < 0 else '+'} {body}")
    num = "".join(parts)
    return num if den == 1 else rf"\frac{{{num}}}{{{den}}}"


def product_to_sum(kind: str, a: int, b: int) -> list[tuple[Fraction, int]]:
    """2cosAcosB, 2sinAsinB or 2sinAcosB as a sum of two table values."""
    ca, sa = special(a - b)
    cb, sb = special(a + b)
    if kind == "cc":
        return surd_sum([ca, cb])
    if kind == "ss":
        return surd_sum([ca, (-cb[0], cb[1])])
    return surd_sum([sb, sa])                              # 2 sin A cos B = sin(A + B) + sin(A − B)


def sum_to_product(kind: str, a: int, b: int) -> tuple[Fraction, int]:
    """sinA + sinB, cosA + cosB or cosA − cosB as a single k√m (the half-angles are table angles)."""
    h, d = (a + b) // 2, (a - b) // 2
    ch, sh = special(h)
    cd, sd = special(d)
    pick = {"s+": (sh, cd, 2), "c+": (ch, cd, 2), "c-": (sh, sd, -2)}[kind]
    (c1, m1), (c2, m2), k = pick
    kk, mm = simplify_root(m1 * m2)
    return Fraction(k) * c1 * c2 * kk, mm


#: θ with a telescoping cosine product, and its value.
COS_PRODUCTS = ((r"\cos 20^{\circ} \cos 40^{\circ} \cos 80^{\circ}", Fraction(1, 8)),
                (r"\cos 36^{\circ} \cos 72^{\circ}", Fraction(1, 4)),
                (r"\sin 10^{\circ} \sin 50^{\circ} \sin 70^{\circ}", Fraction(1, 8)),
                (r"\cos \frac{\pi}{7} \cos \frac{2\pi}{7} \cos \frac{4\pi}{7}", Fraction(-1, 8)))


def _deg(d: int) -> str:
    return rf"{d}^{{\circ}}"


SINE_ALT = "กราฟของฟังก์ชันตรีโกณมิติบนช่วง 0 ถึง 360 องศา มีเส้นตาราง แกน y กำกับทุก 1 หน่วย"


_R2, _R3, _R6 = r"\sqrt{2}", r"\sqrt{3}", r"\sqrt{6}"


# Exact values from the angle-sum formulas: (expression, value)
_SUMS = (
    (r"\sin 75^{\circ}", rf"\frac{{{_R6} + {_R2}}}{{4}}"), (r"\cos 75^{\circ}", rf"\frac{{{_R6} - {_R2}}}{{4}}"),
    (r"\sin 15^{\circ}", rf"\frac{{{_R6} - {_R2}}}{{4}}"), (r"\cos 15^{\circ}", rf"\frac{{{_R6} + {_R2}}}{{4}}"),
    (r"\sin 105^{\circ}", rf"\frac{{{_R6} + {_R2}}}{{4}}"), (r"\cos 105^{\circ}", rf"\frac{{{_R2} - {_R6}}}{{4}}"),
    (r"\tan 75^{\circ}", rf"2 + {_R3}"), (r"\tan 15^{\circ}", rf"2 - {_R3}"),
)


_SUM_POOL = sorted({v for _, v in _SUMS} | {rf"\frac{{{_R3} + 1}}{{2}}", rf"\frac{{{_R6}}}{{4}}", rf"1 + {_R3}"})


def _pi(f: Fraction) -> str:
    """A multiple of π in lowest terms, as TeX: 2/3 gives 2π/3, 1 gives π."""
    num = "" if f.numerator == 1 else str(f.numerator)
    if f.denominator == 1:
        return rf"{num}\pi"
    return rf"\frac{{{num}\pi}}{{{f.denominator}}}"


UNIT_ALT = ("วงกลมหนึ่งหน่วยบนระนาบพิกัดฉาก มีจุด P บนวงกลม ส่วนโค้งแสดงมุม θ จากแกน X ทางบวก "
            "และมุมที่ OP ทำกับแกน X")


_SIN = {30: (1, 2), 45: (r"\sqrt{2}", 2), 60: (r"\sqrt{3}", 2)}


def _trig_value(fn: str, ref: int, sign: int) -> str:
    if fn == "tan":
        mag = {30: r"\frac{\sqrt{3}}{3}", 45: "1", 60: r"\sqrt{3}"}[ref]
    else:
        num, den = _SIN[ref if fn == "sin" else 90 - ref]
        mag = rf"\frac{{{num}}}{{{den}}}"
    return ("-" if sign < 0 else "") + mag


@question_type("math.unit_circle_quadrant_sign",
               display_name={"th": "เครื่องหมายของฟังก์ชันตรีโกณมิติในแต่ละจตุภาค"},
               level={"th": "ม.5"}, topic="ฟังก์ชันตรีโกณมิติ")
class UnitCircleQuadrantSign(ChoiceType):
    def compose(self, rng: Random):
        quadrant = rng.choice([1, 2, 3, 4])
        fn = rng.choice(["sin", "cos", "tan"])
        positive = {
            1: {"sin", "cos", "tan"}, 2: {"sin"},
            3: {"tan"}, 4: {"cos"},
        }[quadrant]
        answer = "เป็นบวก" if fn in positive else "เป็นลบ"
        other = "เป็นลบ" if answer == "เป็นบวก" else "เป็นบวก"
        stem = f"ถ้ามุม θ อยู่ในจตุภาคที่ {quadrant} แล้วค่าของ {fn} θ เป็นอย่างไร"
        return stem, answer, [other, "เป็นศูนย์เสมอ", "หาค่าไม่ได้"]
UnitCircleQuadrantSign.PROVENANCE = Provenance("original")


@question_type("math.reference_angle", display_name={"th": "มุมอ้างอิง"},
               level={"th": "ม.5"}, topic="ฟังก์ชันตรีโกณมิติ")
class ReferenceAngle(MathType):
    def expr(self, rng: Random, lo: int = 91, hi: int = 359):
        theta = rng.randrange(lo, hi)
        if theta <= 180:
            ref = 180 - theta
        elif theta <= 270:
            ref = theta - 180
        else:
            ref = 360 - theta
        return MathDraw(rf"\theta = {theta}^\circ", rf"{ref}^\circ",
                        prompt="มุมอ้างอิงของมุมนี้มีขนาดกี่องศา",
                        distractors=[rf"{180 - ref}^\circ", rf"{theta}^\circ",
                                     rf"{abs(360 - theta - ref) or 90}^\circ"])
ReferenceAngle.PROVENANCE = Provenance("original")


@question_type("math.unit_circle_picture_m5",
               display_name={"th": "ค่าฟังก์ชันตรีโกณมิติจากจุดบนวงกลมหนึ่งหน่วย"},
               level={"th": "ม.5"}, topic="ฟังก์ชันตรีโกณมิติ")
class UnitCirclePictureM5(QuestionType):
    break_convergence = True  # one-part slips cluster round the answer
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(UNIT_POINTS)
        quad = s.deg // 90                      # 0..3
        signs = {"sin": 1 if quad < 2 else -1, "cos": 1 if quad in (0, 3) else -1}
        signs["tan"] = signs["sin"] * signs["cos"]
        fn = rng.choice(("sin", "cos", "tan"))
        swap = {"sin": "cos", "cos": "sin", "tan": "tan"}[fn]
        swap_ref = 90 - s.ref if fn == "tan" else s.ref
        correct = _trig_value(fn, s.ref, signs[fn])
        wrongs = [_trig_value(fn, s.ref, -signs[fn]), _trig_value(swap, swap_ref, signs[fn]),
                  _trig_value(swap, swap_ref, -signs[fn])]
        pad = [_trig_value(fn, r, sg) for r in (30, 60, 45) for sg in (signs[fn], -signs[fn])]
        return _q([text("จุด P อยู่บนวงกลมหนึ่งหน่วย และ OP ทำมุม θ กับแกน X ทางบวกดังภาพ จงหาค่าของ"),
                   content_math(rf"\{fn} \theta"), image(s.asset_id, alt=UNIT_ALT)],
                  correct, wrongs, self.topic, pad)
UnitCirclePictureM5.PROVENANCE = Provenance("original")


@question_type("math.trig_unit_circle",
               display_name={"th": "ค่าตรีโกณมิติบนวงกลมหนึ่งหน่วย"},
               level={"th": "ม.5"}, topic="ฟังก์ชันตรีโกณมิติ")
class TrigUnitCircle(MathType):
    def expr(self, rng: Random):
        fn, deg, val = rng.choice(_UNIT_CIRCLE)
        flip = val[1:] if val.startswith("-") else ("-" + val if val != "0" else val)
        return MathDraw(rf"{fn} {deg}^{{\circ}}", val, prompt="จงหาค่าแบบแม่นตรง",
                        distractors=[flip])
TrigUnitCircle.PROVENANCE = Provenance("original")


@question_type("math.trig_radian_arc_m5",
               display_name={"th": "มุมเรเดียนและความยาวส่วนโค้งของวงกลม"},
               level=M5, topic=FUNCTIONS)
class TrigRadianArcM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            t = rng.choice([a for a in UNIT_CIRCLE if 0 < a < 1 and a != Fraction(1, 2)])
            r = rng.choice((2, 4, 6))
            (c, m), _ = UNIT_CIRCLE[t]
            right = arc_to_point(r, t)
            stem = [text("จุด"), content_math(rf"\left({surd_tex(c * r, m)}, y\right)"), text("โดยที่"),
                    content_math("y > 0"),
                    text(f"อยู่บนวงกลมรัศมี {r} หน่วยซึ่งมีจุดศูนย์กลางที่จุดกำเนิด "
                         "ความยาวส่วนโค้งที่วัดทวนเข็มนาฬิกาจากจุด"),
                    content_math(f"({r}, 0)"), text("ไปถึงจุดนั้นเท่ากับกี่หน่วย")]
            # Forgetting the radius; measuring clockwise; the reference angle; measuring from (−r, 0);
            # measuring from (0, r); the diameter; r²θ.
            ref = min(t, 1 - t)
            wrongs = [pi_tex(t), pi_tex(r * (2 - t)), pi_tex(r * ref), pi_tex(r * (1 - t)),
                      pi_tex(r * abs(t - Fraction(1, 2))), pi_tex(2 * r * t), pi_tex(r * r * t)]
            return _tex_q(stem, pi_tex(right), wrongs, self.topic)
        if kind == 1:
            deg = rng.choice((30, 45, 60, 72, 120, 135, 150, 210, 240, 300))
            r = rng.randint(2, 12)
            t = Fraction(deg, 180)
            right = r * t
            stem = [text(f"วงกลมรัศมี {r} หน่วย มีมุมที่จุดศูนย์กลาง"), content_math(rf"{deg}^{{\circ}}"),
                    text("รองรับส่วนโค้ง ส่วนโค้งนี้ยาวกี่หน่วย")]
            # Degrees used as radians; the sector area ½r²θ; forgetting the radius; the diameter.
            wrongs = [str(r * deg), pi_tex(Fraction(r * r) * t / 2), pi_tex(t), pi_tex(2 * r * t)]
            return _tex_q(stem, pi_tex(right), wrongs, self.topic)
        t = rng.choice((Fraction(1, 6), Fraction(1, 4), Fraction(1, 3), Fraction(2, 3), Fraction(3, 4),
                        Fraction(5, 6), Fraction(5, 4), Fraction(3, 2)))
        r = rng.randint(2, 9)
        stem = [text(f"ส่วนโค้งของวงกลมรัศมี {r} หน่วย ยาว"), content_math(pi_tex(r * t)),
                text("หน่วย มุมที่จุดศูนย์กลางซึ่งรองรับส่วนโค้งนี้มีขนาดกี่องศา")]
        deg = t * 180
        # Not dividing by the radius; multiplying by it; the supplement; halving, doubling.
        wrongs = [deg * r, deg * r * r, 180 - deg if deg < 180 else deg - 180, deg / 2, deg * 2]
        fmt = lambda d: rf"{frac_tex(Fraction(d))}^{{\circ}}"
        return _tex_q(stem, fmt(deg), [fmt(w) for w in wrongs], self.topic)
TrigRadianArcM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/8 ตรีโกณมิติ',))


@question_type("math.trig_reduction_m5",
               display_name={"th": "แปลงมุมให้อยู่ในรูปอย่างง่าย"},
               level=M5, topic=FUNCTIONS)
class TrigReductionM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        fn = rng.choice(list(TRIG))
        k, sign = rng.randint(0, 4), rng.choice((1, -1))
        if k == 0:
            sign = -1                              # f(−θ)
        out_sign, g = reduce_angle(fn, k, sign)
        shift = pi_tex(Fraction(k, 2)) if k else ""
        arg = (f"{shift} {'+' if sign > 0 else '-'} \\theta" if k else "-\\theta")
        stem = [text("รูปอย่างง่ายของ"), content_math(_fn_tex(fn, arg)), text("คือข้อใด")]
        fmt = lambda s_, h: ("-" if s_ < 0 else "") + _fn_tex(h, r"\theta")
        other = COFUNCTION[g]
        # The sign lost; the function kept (or swapped) wrongly; both.
        wrongs = [fmt(-out_sign, g), fmt(out_sign, other), fmt(-out_sign, other)]
        return _tex_q(stem, fmt(out_sign, g), wrongs, self.topic)
TrigReductionM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/8 ตรีโกณมิติ',))


@question_type("math.trig_graph_m5",
               display_name={"th": "แอมพลิจูด คาบ และค่าสูงสุดของกราฟฟังก์ชันไซน์และโคไซน์"},
               level=M5, topic="ฟังก์ชันตรีโกณมิติ")
class TrigGraphM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        a = rng.choice((1, 2, 3, 4, 5, -2, -3))
        b = rng.choice((1, 2, 3, 4, 6))
        c = rng.randint(-3, 3)
        fn = rng.choice(("sin", "cos"))
        amp = "" if a == 1 else "-" if a == -1 else str(a)
        inner = "x" if b == 1 else f"{b}x"
        tail = f" + {c}" if c > 0 else f" - {-c}" if c < 0 else ""
        eq = rf"y = {amp}\{fn} {inner}{tail}"
        kind = rng.randrange(3)
        period = _pi(Fraction(2, b))
        if kind == 0:
            return _maths([text("แอมพลิจูดของกราฟนี้เท่ากับเท่าใด"), content_math(eq)], str(abs(a)),
                          [str(a) if a < 0 else str(-a), str(b), str(abs(a) + c) if c else str(2 * abs(a)),
                           str(2 * abs(a)) if c else str(abs(a) + 1)], self.topic)
        if kind == 1:
            # 2π left undivided, multiplied by b, and π over b.
            wrong = [_pi(Fraction(2)) if b != 1 else _pi(Fraction(1)), _pi(Fraction(2 * b)),
                     _pi(Fraction(1, b)) if b > 1 else _pi(Fraction(1, 2)), rf"\frac{{{b}}}{{2\pi}}"]
            return _maths([text("คาบของฟังก์ชันนี้เท่ากับเท่าใด"), content_math(eq)], period, wrong, self.topic)
        top = abs(a) + c
        return _maths([text("ค่าสูงสุดของฟังก์ชันนี้เท่ากับเท่าใด"), content_math(eq)], str(top),
                      [str(abs(a)), str(-abs(a) + c), str(top + 1), str(a + b + c)], self.topic)
TrigGraphM5.PROVENANCE = Provenance("original")


@question_type("math.trig_identity_reduce_m5",
               display_name={"th": "ลดรูปนิพจน์ตรีโกณมิติด้วยเอกลักษณ์"},
               level=M5, topic=FUNCTIONS)
class TrigIdentityReduceM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            expr, f = rng.choice(REDUCIBLE)
            stem = [text("รูปอย่างง่ายของ"), content_math(expr), text("คือข้อใด")]
            # The reciprocal function, then two others.
            others = [g for g in FUNCS if g not in (f, RECIPROCAL[f])]
            rng.shuffle(others)
            return _tex_q(stem, FUNCS[f], [FUNCS[RECIPROCAL[f]], *[FUNCS[g] for g in others]], self.topic)
        if kind == 1:
            form, sign = rng.choice(POWER_FORMS)
            two_a = rng.choice([a for a in UNIT_CIRCLE if a != Fraction(1, 2)])
            (c, m), (s, sm) = UNIT_CIRCLE[two_a]
            right = surd_tex(sign * c, m)
            angle = rf"\left({pi_tex(two_a / 2)}\right)"
            stem = [text("ค่าของ"), content_math(form.replace("A", angle)), text("เท่ากับเท่าใด")]
            # Reading it as sin² + cos² = 1; the sign lost; sin 2A instead of cos 2A; not halving.
            wrongs = ["1", surd_tex(-sign * c, m), surd_tex(sign * s, sm), surd_tex(2 * sign * c, m)]
            return _tex_q(stem, right, wrongs, self.topic)
        k = rng.choice([v for v in range(-7, 8) if v])
        c2 = triple_angle_cos(k)
        stem = [text("กำหนดให้"), content_math(r"\theta \in \left(0, \frac{\pi}{2}\right)"), text("ถ้า"),
                content_math(rf"\frac{{\sin^{{2}} 3\theta}}{{\sin^{{2}} \theta}} - "
                             rf"\frac{{\cos^{{2}} 3\theta}}{{\cos^{{2}} \theta}} = {k}")]
        if rng.random() < 0.5:
            stem += [text("แล้ว"), content_math(r"\cos 2\theta"), text("เท่ากับเท่าใด")]
            # 4c instead of 8c; 2c; k itself over 16.
            return _frac_q(stem, c2, [Fraction(k, 4), Fraction(k, 2), Fraction(k, 16), -c2], self.topic)
        stem += [text("แล้ว"), content_math(r"\cos\theta"), text("เท่ากับเท่าใด")]
        right = root_tex((1 + c2) / 2)
        # sin θ instead; stopping at cos 2θ; the 4c slip carried through.
        wrongs = [root_tex((1 - c2) / 2), frac_tex(c2) if c2 > 0 else frac_tex(-c2)]
        slip = Fraction(k, 4)
        if -1 < slip < 1:
            wrongs.append(root_tex((1 + slip) / 2))
        wrongs += [root_tex(1 + c2), root_tex((1 + c2) / 4)]
        return _tex_q(stem, right, wrongs, self.topic)
TrigIdentityReduceM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/8 ตรีโกณมิติ',))


@question_type("math.trig_product_sum_m5",
               display_name={"th": "สูตรแปลงผลคูณกับผลบวกผลต่าง"},
               level=M5, topic=FUNCTIONS)
class TrigProductSumM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            while True:
                a, b = rng.choice(range(15, 180, 15)), rng.choice(range(15, 90, 15))
                form = rng.choice(("cc", "ss", "sc"))
                if a > b and (a + b) in SPECIAL_DEGREES + (360,) and (a - b) in SPECIAL_DEGREES \
                        and (a % 30 or b % 30) and product_to_sum(form, a, b):
                    break
            head = {"cc": rf"2\cos {_deg(a)} \cos {_deg(b)}", "ss": rf"2\sin {_deg(a)} \sin {_deg(b)}",
                    "sc": rf"2\sin {_deg(a)} \cos {_deg(b)}"}[form]
            stem = [text("ค่าของ"), content_math(head), text("เท่ากับเท่าใด")]
            right = surd_sum_tex(product_to_sum(form, a, b))
            # The other two formulas; the sum taken without the factor from ½.
            others = [surd_sum_tex(product_to_sum(f, a, b)) for f in ("cc", "ss", "sc") if f != form]
            half = surd_sum_tex([(c / 2, m) for c, m in product_to_sum(form, a, b)])
            neg = surd_sum_tex([(-c, m) for c, m in product_to_sum(form, a, b)])
            double = surd_sum_tex([(2 * c, m) for c, m in product_to_sum(form, a, b)])
            return _tex_q(stem, right, [*others, half, neg, double, "1", "-1", r"\frac{1}{2}"], self.topic)
        if kind == 1:
            while True:
                a, b = rng.choice(range(15, 180, 15)), rng.choice(range(15, 180, 15))
                form = rng.choice(("s+", "c+", "c-"))
                if a > b and (a + b) % 2 == 0 and (a + b) // 2 in SPECIAL_DEGREES \
                        and (a - b) // 2 in SPECIAL_DEGREES and (a % 30 or b % 30) \
                        and sum_to_product(form, a, b)[0]:        # a zero value makes every slip 0 too
                    break
            head = {"s+": rf"\sin {_deg(a)} + \sin {_deg(b)}", "c+": rf"\cos {_deg(a)} + \cos {_deg(b)}",
                    "c-": rf"\cos {_deg(a)} - \cos {_deg(b)}"}[form]
            stem = [text("ค่าของ"), content_math(head), text("เท่ากับเท่าใด")]
            c, m = sum_to_product(form, a, b)
            # Half the value; the sign lost; the other formulas' values; doubled; the wrong root.
            others = [surd_tex(*sum_to_product(f, a, b)) for f in ("s+", "c+", "c-") if f != form]
            wrongs = [surd_tex(c / 2, m), surd_tex(-c, m), *others, surd_tex(2 * c, m),
                      surd_tex(c, 3 if m != 3 else 2)]
            return _tex_q(stem, surd_tex(c, m), [w for w in wrongs if w != "0"] + ["0"], self.topic)
        expr, value = rng.choice(COS_PRODUCTS)
        stem = [text("ค่าของ"), content_math(expr), text("เท่ากับเท่าใด")]
        # Doubled, halved, sign flipped.
        return _tex_q(stem, frac_tex(value), [frac_tex(value * 2), frac_tex(value / 2), frac_tex(-value),
                                              frac_tex(value * 4)], self.topic)
TrigProductSumM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/8 ตรีโกณมิติ',))


@question_type("math.sine_graph_picture_m5",
               display_name={"th": "อ่านแอมพลิจูด คาบ และสมการจากกราฟไซน์และโคไซน์"},
               level={"th": "ม.5"}, topic="ฟังก์ชันตรีโกณมิติ")
class SineGraphPictureM5(QuestionType):
    def _eq(self, fn: str, a: int, b: int) -> str:
        amp = "" if a == 1 else "-" if a == -1 else str(a)
        inner = "x" if b == 1 else f"{b}x"
        return rf"y = {amp}\{fn} {inner}"

    def build(self, rng: Random) -> GeneratedQuestion:
        g = rng.choice(SINE_GRAPHS)
        img = _img(g.asset_id, SINE_ALT)
        kind = rng.randrange(3)
        if kind == 0:
            return _math_q([text("แอมพลิจูดของกราฟนี้เท่ากับเท่าใด"), img], str(abs(g.a)),
                           [str(2 * abs(g.a)), str(g.b), str(abs(g.a) + 1)], self.topic)
        if kind == 1:
            period = 360 // g.b
            return _math_q([text("คาบของกราฟนี้เท่ากับกี่องศา"), img], str(period),
                           [str(period // 2), str(period * 2), "360" if period != 360 else "180"], self.topic)
        other = "cos" if g.fn == "sin" else "sin"
        wrongs = [self._eq(other, g.a, g.b), self._eq(g.fn, -g.a, g.b),
                  self._eq(g.fn, g.a, g.b * 2 if g.b < 4 else 1),
                  # Amplitude and frequency swapped.
                  self._eq(g.fn, g.b, abs(g.a)) if g.b != abs(g.a) else self._eq(g.fn, g.a + 1, g.b)]
        return _math_q([text("สมการของกราฟนี้คือข้อใด"), img], self._eq(g.fn, g.a, g.b), wrongs, self.topic)
SineGraphPictureM5.PROVENANCE = Provenance("original")


@question_type("math.trig_sum_formula_m5",
               display_name={"th": "สูตรผลบวกและมุมสองเท่าของฟังก์ชันตรีโกณมิติ"},
               level=M5, topic="ฟังก์ชันตรีโกณมิติ")
class TrigSumFormulaM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.5:
            expr, right = rng.choice(_SUMS)
            wrongs = [v for v in _SUM_POOL if v != right]
            rng.shuffle(wrongs)
            return _maths([text("จงหาค่าที่แท้จริง"), content_math(expr)], right, wrongs[:3], self.topic)
        a, b, c = rng.choice(((3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25)))
        s, co = Fraction(a, c), Fraction(b, c)
        which = rng.randrange(3)
        if which == 0:
            v, ask = 2 * s * co, r"\sin 2\theta"
            wrongs = [2 * s, s * s, 2 * s * s]
        elif which == 1:
            v, ask = co * co - s * s, r"\cos 2\theta"
            wrongs = [1 - 2 * co * co, 2 * co, co * co + s * s - Fraction(1, c)]
        else:
            v, ask = 1 - 2 * s * s, r"\cos 2\theta"
            wrongs = [2 * s * s - 1, 1 - s * s, 2 * co]
        return _maths([text("ถ้า θ เป็นมุมแหลม และ"), content_math(rf"\sin\theta = {frac_tex(s)}"),
                       text("จงหาค่าของ"), content_math(ask)], frac_tex(v),
                      [frac_tex(w) for w in wrongs if w != v] + [frac_tex(-v)], self.topic)
TrigSumFormulaM5.PROVENANCE = Provenance("original")
