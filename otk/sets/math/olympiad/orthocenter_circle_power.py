"""With BC a diameter, F is the orthocentre of ABC and AH·FH = BH·HC = GH²."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2548, วันที่สอง ข้อ 1",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def surd_tex(square: Fraction) -> str:
    """TeX for √square in the form (k/d)√m with m squarefree."""
    inside = square.numerator * square.denominator
    outside, f = 1, 2
    while f * f <= inside:
        while inside % (f * f) == 0:
            inside //= f * f
            outside *= f
        f += 1
    coef = Fraction(outside, square.denominator)
    if inside == 1:
        return frac_tex(coef)
    root = rf"\sqrt{{{inside}}}"
    top = ("" if coef.numerator == 1 else str(coef.numerator)) + root
    return top if coef.denominator == 1 else rf"\frac{{{top}}}{{{coef.denominator}}}"


def foot_distances(bh: int, hc: int, ah: int) -> tuple[Fraction, Fraction]:
    """∠BDC = ∠BEC = 90°, so CD, BE are altitudes and F is the orthocentre.
    Triangles BHF and AHC are similar, so FH = BH·HC/AH; G on the circle over
    the diameter BC gives GH² = BH·HC = AH·FH. Returns (FH, GH²)."""
    return Fraction(bh * hc, ah), Fraction(bh * hc)


@question_type(
    "math.orthocenter_circle_power_olympiad",
    display_name={"th": "ระยะจากจุดออร์โทเซนเตอร์ถึงฐานและกำลังของจุด"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: กำลังของจุด",
)
class OrthocenterCirclePower(WordProblem):
    def expr(self, rng: Random):
        while True:
            bh, hc, ah = rng.randint(1, 12), rng.randint(1, 12), rng.randint(2, 20)
            if ah * ah > bh * hc:
                break
        fh, gh_sq = foot_distances(bh, hc, ah)
        if rng.random() < 0.5:
            answer, ask = frac_tex(fh), "FH"
            wrong = [frac_tex(v) for v in dict.fromkeys([ah - fh, Fraction(bh * hc, bh + hc), Fraction(ah * ah, bh + hc), Fraction(bh * hc, 2 * ah), Fraction(ah * bh, hc)]) if v != fh]
        else:
            answer, ask = surd_tex(gh_sq), "GH"
            wrong = [surd_tex(v) for v in dict.fromkeys([Fraction(bh * bh + hc * hc), Fraction(ah * ah - bh * hc), Fraction((bh + hc) ** 2, 4), Fraction(ah * bh), Fraction(ah * hc)]) if v != gh_sq]
        return MathDraw(
            rf"BH={bh},\quad HC={hc},\quad AH={ah}",
            answer,
            prompt=f"BC เป็นเส้นผ่านศูนย์กลางของวงกลม A อยู่ภายนอกวงกลมและ ABC เป็นสามเหลี่ยมมุมแหลม AB, AC ตัดวงกลมที่ D, E CD ตัด BE ที่ F, AF ตัดวงกลมที่ G และพบ BC ที่ H จงหา {ask}",
            hint="มุมในครึ่งวงกลมเป็นมุมฉาก จึง F เป็นจุดออร์โทเซนเตอร์ และ AH ⟂ BC ใช้สามเหลี่ยมคล้าย BHF กับ AHC และกำลังของจุด H",
            distractors=[t for t in dict.fromkeys(wrong) if t != answer],
        )
