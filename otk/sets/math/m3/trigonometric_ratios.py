"""อัตราส่วนตรีโกณมิติ

คณิตศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ค 2.2 ม.3/2

Sets moved here from: math, math_formats_hi, math_geometry, math_m3.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random
from typing import NamedTuple

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_tex
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_geometry import _TRIPLES
from otk.sets._support.math_m3 import LEVEL

PROVENANCE = Provenance("original")


def _surd(coef: int, rad: int) -> str:
    if rad == 1:
        return str(coef)
    return rf"\sqrt{{{rad}}}" if coef == 1 else rf"{coef}\sqrt{{{rad}}}"


def _special_sides(angle: int, given: str, value: int) -> dict[str, tuple[int, int]]:
    """Side lengths as (coefficient, radicand), with ``given`` equal to ``value``."""
    if angle == 45:
        if given == "hyp":                         # legs are (value / 2)√2
            leg = (value // 2, 2)
            return {"opp": leg, "adj": leg, "hyp": (value, 1)}
        return {"opp": (value, 1), "adj": (value, 1), "hyp": (value, 2)}
    short, long_ = ("opp", "adj") if angle == 30 else ("adj", "opp")
    k = value // 2 if given == "hyp" else value
    return {short: (k, 1), long_: (k, 3), "hyp": (2 * k, 1)}


class SpecialTriangle(NamedTuple):
    angle: int           # 30 | 45 | 60, the marked angle θ
    given: str           # opp | adj | hyp, labelled with its length
    asked: str           # labelled x
    value: int

    @property
    def asset_id(self) -> str:
        return f"mspec_{self.angle}_{self.given}_{self.asked}_{self.value}"

    @property
    def sides(self) -> dict[str, tuple[int, int]]:
        return _special_sides(self.angle, self.given, self.value)


def _special_triangles() -> tuple[SpecialTriangle, ...]:
    out = []
    integer_sides = {30: ("opp", "hyp"), 60: ("adj", "hyp"), 45: ("opp", "hyp")}
    for angle, givens in integer_sides.items():
        for given in givens:
            for value in (4, 6, 8, 10):
                for asked in ("opp", "adj", "hyp"):
                    if asked != given:
                        out.append(SpecialTriangle(angle, given, asked, value))
    return tuple(out)


SPECIAL_TRIANGLES = _special_triangles()


SPECIAL_ALT = "รูปสามเหลี่ยมมุมฉาก กำหนดขนาดของมุมหนึ่งมุมและความยาวด้านหนึ่งด้าน"


_TRIG_TOPIC = "อัตราส่วนตรีโกณมิติ"


_VAL = {"1/2": r"\frac{1}{2}", "r2/2": r"\frac{\sqrt{2}}{2}", "r3/2": r"\frac{\sqrt{3}}{2}",
        "1": "1", "r3": r"\sqrt{3}", "r3/3": r"\frac{\sqrt{3}}{3}", "2": "2"}


_TABLE = {("sin", 30): "1/2", ("cos", 30): "r3/2", ("tan", 30): "r3/3",
          ("sin", 45): "r2/2", ("cos", 45): "r2/2", ("tan", 45): "1",
          ("sin", 60): "r3/2", ("cos", 60): "1/2", ("tan", 60): "r3"}


@question_type("math.trig_ratio_from_triple",
               display_name={"th": "อัตราส่วนตรีโกณมิติจากด้านสามเหลี่ยม"},
               level={"th": "ม.3"}, topic="อัตราส่วนตรีโกณมิติ")
class TrigRatioFromTriple(MathType):
    def expr(self, rng: Random, k_lo: int = 1, k_hi: int = 4):
        a, b, c = rng.choice(_TRIPLES)
        k = rng.randint(k_lo, k_hi)
        opp, adj, hyp = a * k, b * k, c * k
        fn = rng.choice(["\\sin", "\\cos", "\\tan"])
        value = {"\\sin": Fraction(opp, hyp), "\\cos": Fraction(adj, hyp),
                 "\\tan": Fraction(opp, adj)}[fn]
        wrong = [Fraction(adj, hyp), Fraction(opp, hyp), Fraction(opp, adj),
                 Fraction(hyp, opp)]
        return MathDraw(
            rf"{fn} A", frac_tex(value),
            prompt=(f"รูปสามเหลี่ยมมุมฉาก มีด้านตรงข้ามมุม A ยาว {opp} "
                    f"ด้านประชิดมุม A ยาว {adj} และด้านตรงข้ามมุมฉากยาว {hyp} "
                    "จงหาค่าของอัตราส่วนต่อไปนี้"),
            distractors=[frac_tex(w) for w in wrong if w != value])


@question_type("math.trig_special_values_m3",
               display_name={"th": "ค่าอัตราส่วนตรีโกณมิติของมุม 30, 45 และ 60 องศา"},
               level=LEVEL, topic=_TRIG_TOPIC)
class TrigSpecialValuesM3(MathType):
    # Small combinations whose value is worth knowing by heart.
    _COMBOS = (
        (r"\sin 30^{\circ} + \cos 60^{\circ}", "1", ("2", r"\frac{1}{2}", r"\sqrt{3}")),
        (r"\sin 60^{\circ} \cos 30^{\circ}", r"\frac{3}{4}", (r"\frac{\sqrt{3}}{2}", r"\frac{3}{2}", "1")),
        (r"\tan 45^{\circ} + \sin 30^{\circ}", r"\frac{3}{2}", ("1", r"\frac{1}{2}", "2")),
        (r"\tan 60^{\circ} \tan 30^{\circ}", "1", (r"\sqrt{3}", "3", r"\frac{1}{3}")),
        (r"2\sin 30^{\circ}", "1", (r"\frac{\sqrt{3}}{2}", "2", r"\frac{1}{2}")),
        (r"\sin^{2} 45^{\circ}", r"\frac{1}{2}", (r"\frac{\sqrt{2}}{2}", "1", r"\frac{1}{4}")),
        (r"\sin 45^{\circ} \cos 45^{\circ}", r"\frac{1}{2}", (r"\frac{\sqrt{2}}{2}", "1", "2")),
        (r"\tan^{2} 60^{\circ}", "3", (r"\sqrt{3}", "9", r"\frac{1}{3}")),
        (r"\cos 60^{\circ} - \sin 30^{\circ}", "0", ("1", r"\frac{1}{2}", r"-\frac{1}{2}")),
        (r"4\sin 30^{\circ} \cos 60^{\circ}", "1", ("2", r"\frac{1}{2}", "4")),
        (r"\cos^{2} 30^{\circ} + \sin^{2} 30^{\circ}", "1", (r"\frac{1}{2}", r"\frac{3}{2}", "2")),
    )

    def expr(self, rng: Random):
        if rng.random() < 0.4:
            tex, right, wrongs = rng.choice(self._COMBOS)
            return MathDraw(tex, right, prompt="จงหาค่า", distractors=list(wrongs))
        fn, deg = rng.choice(list(_TABLE))
        right = _TABLE[fn, deg]
        # The co-function (sin ↔ cos) first: the table read along the wrong row.
        swap = {"sin": "cos", "cos": "sin", "tan": "tan"}[fn]
        other = _TABLE[swap, 90 - deg] if swap != "tan" else _TABLE["tan", 90 - deg if deg != 45 else 30]
        first = _TABLE[swap, deg]
        wrongs = [first, other] + [k for k in _VAL if k not in (right, first, other)]
        return MathDraw(rf"\{fn} {deg}^{{\circ}}", _VAL[right], prompt="จงหาค่า",
                        distractors=[_VAL[w] for w in dict.fromkeys(wrongs) if w != right])


@question_type("math.trig_application_height",
               display_name={"th": "ตรีโกณมิติประยุกต์: หาความสูง"},
               level={"th": "ม.3"}, topic="อัตราส่วนตรีโกณมิติ")
class TrigApplicationHeight(MathType):
    _WHAT = (("ตึก", "ยอดตึก"), ("ต้นไม้", "ยอดต้นไม้"), ("เสาธง", "ยอดเสาธง"),
             ("หอนาฬิกา", "ยอดหอนาฬิกา"), ("เสาไฟฟ้า", "ยอดเสาไฟฟ้า"))

    def expr(self, rng: Random):
        theta = rng.choice([30, 45, 60])
        d = rng.randint(10, 100)
        thing, top = rng.choice(self._WHAT)
        # The stem shows no expression: printing one here printed the answer.
        return MathDraw(
            "", rf"{d}\tan {theta}^{{\circ}}",
            prompt=f"ยืนห่าง{thing} {d} เมตร มอง{top}เป็นมุมเงย {theta} องศา "
                   f"ความสูงของ{thing}เท่ากับข้อใด? (ไม่คิดความสูงของผู้มอง)",
            distractors=[rf"\frac{{{d}}}{{\tan {theta}^{{\circ}}}}",
                         rf"{d}\sin {theta}^{{\circ}}",
                         rf"{d}\cos {theta}^{{\circ}}"])


@question_type("math.special_triangle_picture_m3", display_name={"th": "หาความยาวด้านจากมุม 30° 45° และ 60°"},
               level={"th": "ม.3"}, topic="อัตราส่วนตรีโกณมิติ")
class SpecialTrianglePictureM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        t = rng.choice(SPECIAL_TRIANGLES)
        coef, rad = t.sides[t.asked]
        right = _surd(coef, rad)
        others = {1, 2, 3} - {rad}
        # The wrong root; no root at all; the other two sides.
        wrongs = [_surd(coef, r) for r in sorted(others)] + [
            _surd(*t.sides[s]) for s in ("opp", "adj", "hyp") if s != t.asked]
        wrongs += [str(coef * 2), _surd(coef + 1, rad)]
        return _math_q([text("จากรูป x ยาวกี่หน่วย"), image(t.asset_id, alt=SPECIAL_ALT)],
                       right, [w for w in dict.fromkeys(wrongs) if w != right], self.topic)


@question_type("math.trig_word_problem_m3",
               display_name={"th": "โจทย์ปัญหาอัตราส่วนตรีโกณมิติ (มุมเงยและมุมก้ม)"},
               level=LEVEL, topic=_TRIG_TOPIC)
class TrigWordProblemM3(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(4)
        if kind == 0:
            span = 2 * rng.randint(2, 15)
            return MathDraw("", rf"{span // 2}\sqrt{{3}}",
                            prompt=(f"บันไดยาว {span} เมตร พาดกับกำแพงทำมุม 60 องศากับพื้น ปลายบันไดอยู่สูงจากพื้น"
                                    f"กี่เมตร"),
                            # cos 60° used for sin 60°, and the full length.
                            distractors=[str(span // 2), rf"{span}\sqrt{{3}}", rf"{span // 2}\sqrt{{2}}"])
        if kind == 1:
            d = rng.randint(5, 60)
            return MathDraw("", str(d),
                            prompt=(f"ยืนห่างจากเสาธง {d} เมตร มองเห็นยอดเสาเป็นมุมเงย 45 องศา เสาธงสูงกี่เมตร "
                                    f"(ไม่คิดความสูงของผู้มอง)"),
                            distractors=[rf"{d}\sqrt{{2}}", rf"\frac{{{d}}}{{2}}", rf"{d}\sqrt{{3}}"])
        if kind == 2:
            h = 3 * rng.randint(2, 20)
            return MathDraw("", rf"{h // 3}\sqrt{{3}}",
                            prompt=(f"ยืนห่างจากตึก {h} เมตร มองเห็นยอดตึกเป็นมุมเงย 30 องศา ตึกสูงกี่เมตร "
                                    f"(ไม่คิดความสูงของผู้มอง)"),
                            # tan 60° in place of tan 30°.
                            distractors=[rf"{h}\sqrt{{3}}", rf"\frac{{{h}}}{{2}}", rf"{h // 3}\sqrt{{2}}"])
        h = rng.randint(10, 80)
        return MathDraw("", rf"{h}\sqrt{{3}}",
                        prompt=(f"จากยอดประภาคารสูง {h} เมตร มองเห็นเรือเป็นมุมก้ม 30 องศา เรืออยู่ห่างจาก"
                                f"ฐานประภาคารกี่เมตร"),
                        distractors=[rf"\frac{{{h}\sqrt{{3}}}}{{3}}", str(2 * h), rf"\frac{{{h}}}{{2}}"])
