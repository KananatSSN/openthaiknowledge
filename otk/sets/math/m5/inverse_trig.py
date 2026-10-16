"""ตัวผกผันของฟังก์ชันตรีโกณมิติ

คณิตศาสตร์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 2 ม.5/1

Sets moved here from: math, math_bank_trig, math_geometry.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import ChoiceType, MathDraw, MathType, frac_tex
from otk.sets._support.math_bank_trig import M5, TRIPLES, _frac_q, _tex_q, pi_tex
from otk.sets._support.math_geometry import _COS, _SIN, _TAN

_INV_TRIG = [
    (tex, val, ang)
    for inv, tex, table in (
        (r"\arcsin", r"\arcsin", {0: "0", 30: r"\frac{1}{2}",
                                  45: r"\frac{\sqrt{2}}{2}",
                                  60: r"\frac{\sqrt{3}}{2}", 90: "1"}),
        (r"\arccos", r"\arccos", {90: "0", 60: r"\frac{1}{2}",
                                  45: r"\frac{\sqrt{2}}{2}",
                                  30: r"\frac{\sqrt{3}}{2}", 0: "1"}))
    for ang, val in table.items()
]


_INV_TAN = [(r"\arctan", val, ang) for ang, val in
            {0: "0", 30: r"\frac{\sqrt{3}}{3}", 45: "1", 60: r"\sqrt{3}"}.items()]


INVERSE = "ตัวผกผันของฟังก์ชันตรีโกณมิติ"


def angle_sum_from_tans(p: Fraction, q: Fraction) -> Fraction:
    """A + B (in π units) for A, B ∈ (0, π/2) with tan A = p, tan B = q, when tan(A + B) = ±1."""
    t = (p + q) / (1 - p * q)
    if t == 1:
        return Fraction(1, 4)
    if t == -1:
        return Fraction(3, 4)
    raise ValueError(t)


def _tan_one_pairs() -> list[tuple[Fraction, Fraction]]:
    out = []
    for p in (Fraction(1, 2), Fraction(1, 3), Fraction(1, 4), Fraction(1, 5), Fraction(2, 3), Fraction(3, 4)):
        out.append((p, (1 - p) / (1 + p)))
    for p in (Fraction(2), Fraction(3), Fraction(4), Fraction(5), Fraction(3, 2), Fraction(5, 3)):
        out.append((p, (1 + p) / (p - 1)))
    return out


TAN_PAIRS = _tan_one_pairs()


def inverse_sin_cos(fn: str, p: int, q: int, r: int) -> tuple[Fraction, Fraction, Fraction]:
    """(sin, cos, argument) of arcsin(p/r), arccos(p/r) or arctan(p/q), all in [0, π/2]."""
    if fn == "arcsin":
        return Fraction(p, r), Fraction(q, r), Fraction(p, r)
    if fn == "arccos":
        return Fraction(q, r), Fraction(p, r), Fraction(p, r)
    return Fraction(p, r), Fraction(q, r), Fraction(p, q)


def compose(outer: str, s1: Fraction, c1: Fraction, s2: Fraction, c2: Fraction, sign: int = 1
            ) -> Fraction | None:
    """sin, cos or tan of α ± β from the parts; None when tan is undefined."""
    s = s1 * c2 + sign * c1 * s2
    c = c1 * c2 - sign * s1 * s2
    if outer == "sin":
        return s
    if outer == "cos":
        return c
    return None if c == 0 else s / c


def complement_solution(p: int, q: int, r: int, s: int) -> Fraction | None:
    """x with arcsin(px + q) + arccos(rx + s) = π/2: px + q = rx + s inside [−1, 1]."""
    if p == r:
        return None
    x = Fraction(s - q, p - r)
    return x if abs(p * x + q) <= 1 else None


def _lin(k: int, c: int) -> str:
    head = {1: "", -1: "-"}.get(k, str(k)) + "x"
    return head if not c else f"{head} {'+' if c > 0 else '-'} {abs(c)}"


@question_type("math.inverse_trig",
               display_name={"th": "ค่าฟังก์ชันตรีโกณมิติผกผัน"}, level={"th": "ม.5"},
               topic="ตัวผกผันของฟังก์ชันตรีโกณมิติ")
class InverseTrig(MathType):
    def expr(self, rng: Random):
        inv, val, ang = rng.choice(_INV_TRIG + _INV_TAN)
        return MathDraw(
            rf"{inv}\left({val}\right)", rf"{ang}^{{\circ}}",
            prompt="เท่ากับกี่องศา (ช่วงหลัก)",
            distractors=[rf"{90 - ang}^{{\circ}}", rf"{(ang + 30) % 360}^{{\circ}}",
                         rf"{180 - ang}^{{\circ}}"])
InverseTrig.PROVENANCE = Provenance("original")


@question_type("math.inverse_trig_range",
               display_name={"th": "เรนจ์ของฟังก์ชันตรีโกณมิติผกผัน"},
               level={"th": "ม.5"}, topic="ตัวผกผันของฟังก์ชันตรีโกณมิติ")
class InverseTrigRange(ChoiceType):
    ITEMS = [
        ("เรนจ์ (ค่าหลัก) ของ arcsin x คือช่วงใด", "[-90°, 90°]",
         ["[0°, 180°]", "[0°, 90°]", "[-180°, 180°]"]),
        ("เรนจ์ (ค่าหลัก) ของ arccos x คือช่วงใด", "[0°, 180°]",
         ["[-90°, 90°]", "[0°, 90°]", "[-180°, 180°]"]),
        ("เรนจ์ (ค่าหลัก) ของ arctan x คือช่วงใด", "(-90°, 90°)",
         ["[0°, 180°]", "[0°, 90°]", "(-180°, 180°)"]),
        ("โดเมนของ arcsin x คือช่วงใด", "[-1, 1]",
         ["จำนวนจริงทั้งหมด", "[0, 1]", "[-90°, 90°]"]),
        ("โดเมนของ arccos x คือช่วงใด", "[-1, 1]",
         ["จำนวนจริงทั้งหมด", "[0, 1]", "[0°, 180°]"]),
        ("โดเมนของ arctan x คือช่วงใด", "จำนวนจริงทั้งหมด",
         ["[-1, 1]", "(-90°, 90°)", "[0, ∞)"]),
        ("ฟังก์ชันผกผันใดมีค่าหลักไม่เป็นลบเสมอ", "arccos x",
         ["arcsin x", "arctan x", "ทั้ง arcsin x และ arctan x"]),
    ]
    _BAD = ("1.2", "1.5", "2", "-2", "-1.1", "√2", "π")
    _GOOD = ("0.5", "-0.5", "1", "-1", "0", "√3/2", "-√2/2")

    def compose(self, rng: Random):
        if rng.random() < 0.4:
            # Only arcsin and arccos stop at ±1; arctan takes any real number.
            bad = rng.choice(self._BAD)
            f = rng.choice(("arcsin", "arccos"))
            other = "arccos" if f == "arcsin" else "arcsin"
            goods = rng.sample(self._GOOD, 2)
            return ("ข้อใดหาค่าไม่ได้", f"{f}({bad})",
                    [f"{other}({goods[0]})", f"arctan({bad})", f"{f}({goods[1]})"])
        return rng.choice(self.ITEMS)
InverseTrigRange.PROVENANCE = Provenance("original")


@question_type("math.inverse_trig_sum_m5",
               display_name={"th": "ค่าตรีโกณมิติของผลบวกมุมจากฟังก์ชันผกผัน"},
               level=M5, topic=INVERSE)
class InverseTrigSumM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        if kind == 0:
            p, q = rng.choice(TAN_PAIRS)
            if rng.random() < 0.5:
                p, q = q, p
            right = angle_sum_from_tans(p, q)
            stem = [text("กำหนดให้"), content_math(r"A, B \in \left(0, \frac{\pi}{2}\right)"), text("ถ้า"),
                    content_math(rf"\tan A = {frac_tex(p)}"), text("และ"), content_math(rf"\tan B = {frac_tex(q)}"),
                    text("แล้ว"), content_math("A + B"), text("เท่ากับเท่าใด")]
            # The other angle with the same |tan|; adding π; the 60° angles.
            other = Fraction(1) - right
            wrongs = [pi_tex(other), pi_tex(right + 1), pi_tex(Fraction(1, 3)), pi_tex(Fraction(2, 3))]
            return _tex_q(stem, pi_tex(right), wrongs, self.topic)
        if kind == 1:
            while True:
                f1, f2 = rng.choice(("arcsin", "arccos", "arctan")), rng.choice(("arcsin", "arccos"))
                t1, t2 = rng.sample(TRIPLES, 2)
                outer = rng.choice(("sin", "cos", "tan"))
                s1, c1, a1 = inverse_sin_cos(f1, *t1)
                s2, c2, a2 = inverse_sin_cos(f2, *t2)
                right = compose(outer, s1, c1, s2, c2)
                if right is not None and compose(outer, s1, c1, s2, c2, -1) is not None:
                    break
            stem = [text("ค่าของ"),
                    content_math(rf"\{outer}\left(\{f1}\left({frac_tex(a1)}\right) + "
                                 rf"\{f2}\left({frac_tex(a2)}\right)\right)"),
                    text("เท่ากับเท่าใด")]
            # The difference formula's signs; the sign flipped; for tan, adding the tans;
            # for sin/cos, the other one.
            named = [compose(outer, s1, c1, s2, c2, -1), -right]
            if outer == "tan":
                named += [s1 / c1 + s2 / c2, 1 / right if right else Fraction(0)]
            else:
                named += [compose("cos" if outer == "sin" else "sin", s1, c1, s2, c2)]
            return _frac_q(stem, right, named, self.topic)
        if kind == 2:
            k = rng.randint(2, 5)
            stem = [text("ถ้า"),
                    content_math(rf"\arccos\left({k * k}x^{{2}}\right) + \arcsin\left({2 * k}x - 1\right) = "
                                 r"\frac{\pi}{2}"),
                    text("แล้ว x เท่ากับเท่าใด")]
            # Half the root; the square's coefficient; the other sign.
            return _frac_q(stem, Fraction(1, k), [Fraction(1, 2 * k), Fraction(1, k * k), Fraction(-1, k),
                                                   Fraction(0)], self.topic)
        while True:
            p, r = rng.sample((1, 2, 3, 4), 2)
            x0, v = rng.randint(-3, 3), rng.choice((-1, 0, 1))
            q, s = v - p * x0, v - r * x0
            if complement_solution(p, q, r, s) == x0:
                break
        stem = [text("ถ้า"),
                content_math(rf"\arcsin({_lin(p, q)}) + \arccos({_lin(r, s)}) = \frac{{\pi}}{{2}}"),
                text("แล้ว x เท่ากับเท่าใด")]
        # Setting the arguments opposite; subtracting the wrong way; the value v itself.
        named = [Fraction(-(q + s), p + r), Fraction(q - s, p - r), Fraction(v)]
        return _frac_q(stem, Fraction(x0), named, self.topic)
InverseTrigSumM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/8 ตรีโกณมิติ',))


@question_type("math.inverse_trig_negative",
               display_name={"th": "ค่าผกผันของอาร์กิวเมนต์ติดลบ"},
               level={"th": "ม.5"}, topic="ตัวผกผันของฟังก์ชันตรีโกณมิติ")
class InverseTrigNegative(MathType):
    """arcsin is odd but arccos is not — a negative argument behaves differently
    in the two, which is the mistake this item catches."""

    def expr(self, rng: Random):
        angle = rng.choice([30, 45, 60])
        kind = rng.randrange(3)
        if kind == 0:
            fn, value, answer = r"\arcsin", _SIN[angle], -angle
            wrong = [180 + angle, 180 - angle, 360 - angle]
        elif kind == 1:
            fn, value, answer = r"\arccos", _COS[angle], 180 - angle
            wrong = [-angle, 180 + angle, angle]
        else:
            # arctan is odd like arcsin, with its range open at ±90°.
            fn, value, answer = r"\arctan", _TAN[angle], -angle
            wrong = [180 - angle, 360 - angle, angle]
        return MathDraw(rf"{fn}\left(-{value}\right)", rf"{answer}^\circ",
                        prompt="จงหาค่าหลักของฟังก์ชันผกผันนี้ (เป็นองศา)",
                        distractors=[rf"{w}^\circ" for w in wrong])
InverseTrigNegative.PROVENANCE = Provenance("original")
