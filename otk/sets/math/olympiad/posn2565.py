"""สมการเลขชี้กำลัง

คณิตศาสตร์ · โอลิมปิก (สอวน.) · สอวน.
Indicators: —

Sets moved here from: posn2565.
"""

from __future__ import annotations

import itertools
import math
from fractions import Fraction
from functools import lru_cache
from random import Random

from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem, frac_answer_tex, frac_tex
from otk.sheets import figure_attachments
from otk.sheets.posn2565_math import (
    q01,
    q02,
    q03,
    q04,
    q05,
    q06,
    q07,
    q08,
    q09,
    q10,
    q11,
    q12,
    q13,
    q14,
    q15,
    q16,
    q17,
    q18,
    q19,
    q20,
    q21,
    q22,
    q23,
    q24,
    q25,
    q26,
    q27,
    q28,
    q29,
    q30,
)

LEVEL = {"th": "โอลิมปิก (สอวน.)"}


SHEET = "สอวน. ค่าย 1 (2565)"


SHEET_ID = "posn2565_math"


_MODULES = [q01, q02, q03, q04, q05, q06, q07, q08, q09, q10,
            q11, q12, q13, q14, q15, q16, q17, q18, q19, q20,
            q21, q22, q23, q24, q25, q26, q27, q28, q29, q30]


SOLVE = {n: lru_cache(maxsize=4096)(mod.solve)
         for n, mod in enumerate(_MODULES, start=1)}


FIGURES = figure_attachments(SHEET_ID)


class SheetProblem(WordProblem):
    """A โจทย์ from the 2565 sheet: Thai prompt, exact TeX answer."""

    sheet = SHEET
    sheet_id = SHEET_ID

    def default_figure(self) -> tuple[str, str]:
        return FIGURES.get(self.key, ("", ""))


def _distinct(value: str, candidates: list[str], want: int = 4) -> list[str]:
    """The first ``want`` candidates differing from the answer and each other."""
    out: list[str] = []
    for c in candidates:
        if c != value and c not in out:
            out.append(c)
        if len(out) == want:
            break
    return out


#: (base1, base2, exponent) with the two bases distinct — the ratio is only a
#: whole number when the third base is a power of their product.
TOWERS = [(b1, b2, p) for b1, b2 in ((2, 3), (2, 5), (3, 5), (2, 7), (3, 7))
          for p in range(2, 7)]


def _pool_q03() -> list[dict]:
    """Target rows that really are combinations of the sheet's two rows."""
    r1, r2 = (1, -2, 3, -4), (4, -3, 2, -1)
    from otk.sheets.posn2565_math.q03 import _combination
    out = []
    for u in range(-3, 6):
        for v in range(-3, 6):
            target = tuple(u * a + v * b for a, b in zip(r1, r2))
            if any(abs(t) > 12 for t in target) or not any(target):
                continue
            if _combination(r1, r2, target) is not None:
                out.append(target)
    return out


def _pool_q04() -> list[dict]:
    """Constants for which every solution of the cycle gives the same value."""
    out = []
    for p in range(1, 8):
        for q in range(1, 8):
            v = SOLVE[4](p=p, q=q, r=1)
            if v is not None and abs(v) < 100:
                out.append({"p": p, "q": q, "r": 1})
    return out


def _pool_q06() -> list[dict]:
    """Box contents where every count in the story is a whole number."""
    out = []
    for a, b in ((4, 7), (1, 2), (2, 3), (3, 5), (5, 7), (1, 4), (2, 5)):
        for units in range(6, 26):
            total = (a + b) * units
            for eaten in (0, 5, 10, 15, 20):
                for c, d in ((1, 6), (1, 2), (1, 3), (2, 5), (1, 4), (3, 7)):
                    p = {"total": total, "a": a, "b": b,
                         "eaten": eaten, "c": c, "d": d}
                    v = SOLVE[6](**p)
                    if v is not None and v > 0:
                        out.append(p)
    return out


#: targets whose triple count is worth asking for.
TARGETS = [t for t in range(3, 80) if SOLVE[7](target=t) >= 3]


POOL03, POOL04, POOL06 = _pool_q03(), _pool_q04(), _pool_q06()


def _surd_tex(rational: Fraction, coef: Fraction, radicand: int) -> str:
    """``p``, ``q\\sqrt d`` or ``p + q\\sqrt d``, with a coefficient of 1 implicit."""
    whole = str(rational.numerator if rational.denominator == 1 else rational)
    if coef == 0 or radicand in (0, 1):
        return whole
    mag = "" if abs(coef) == 1 else str(abs(coef))
    surd = rf"{mag}\sqrt{{{radicand}}}"
    if rational == 0:
        return ("-" if coef < 0 else "") + surd
    return f"{whole} {'-' if coef < 0 else '+'} {surd}"


@question_type("math.posn2565_q01", display_name={"th": "ค่าของ ab/(bc+ca) จากเลขชี้กำลัง"},
               level=LEVEL, topic="สมการเลขชี้กำลัง")
class EqualPowersRatio(SheetProblem):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def expr(self, rng: Random):
        b1, b2, p = rng.choice(TOWERS)
        value = SOLVE[1](base1=b1, base2=b2, p=p, q=p)
        third = (b1 * b2) ** p
        return MathDraw(
            rf"{b1}^a = {b2}^b = {third}^c", frac_answer_tex(value),
            prompt=("ถ้า a, b และ c เป็นจำนวนจริงบวกซึ่งสอดคล้องกับสมการ"
                    "ต่อไปนี้ แล้วค่าของ ab/(bc + ca) เท่ากับเท่าใด"),
            hint=r"\frac{ab}{bc+ca} = \frac{1/c}{1/a + 1/b} "
                 r"= \frac{\ln N}{\ln b_1 + \ln b_2}",
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(value + 1), frac_answer_tex(value - 1),
                frac_answer_tex(2 * value), frac_answer_tex(Fraction(1, value))]))


@question_type("math.posn2565_q02", display_name={"th": "ค่าของ a จากกรณฑ์ซ้อน"},
               level=LEVEL, topic="การถอดกรณฑ์ซ้อน")
class NestedRadicalValue(SheetProblem):
    def expr(self, rng: Random, k_lo: int = 1, k_hi: int = 12):
        k = rng.randint(k_lo, k_hi)
        value = SOLVE[2](k=k)
        return MathDraw(
            rf"\sqrt{{a}} = \frac{{\sqrt{{{4 * k} + {2 * k}\sqrt{{3}}}}}}"
            rf"{{\sqrt{{2}} + \sqrt{{2 + \sqrt{{3}}}}}}",
            frac_answer_tex(value),
            prompt=("ให้ a เป็นจำนวนตรรกยะบวก โดยที่สมการต่อไปนี้เป็นจริง "
                    "จงเขียน a ในรูปเศษส่วนอย่างต่ำของจำนวนเต็มบวก"),
            hint=r"4k + 2k\sqrt{3} = \left(\sqrt{k} + \sqrt{3k}\right)^2,"
                 r"\qquad 2 + \sqrt{3} = \frac{(\sqrt{3}+1)^2}{2}",
            # Forgetting to square, and the reciprocal, are the two near misses.
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(Fraction(1, 1) / value),
                frac_answer_tex(Fraction(k)),
                frac_answer_tex(Fraction(4 * k, 3)),
                frac_answer_tex(Fraction(k, 3))]))


@question_type("math.posn2565_q03", display_name={"th": "ค่าที่เป็นไปได้ของผลรวมเชิงเส้น"},
               level=LEVEL, topic="ระบบสมการเชิงเส้น")
class ForcedLinearCombination(SheetProblem):
    _ROWS = ((1, -2, 3, -4), (4, -3, 2, -1))

    def expr(self, rng: Random):
        target = rng.choice(POOL03)
        rhs1, rhs2 = rng.randint(-10, 12), rng.randint(-10, 12)
        r1, r2 = self._ROWS
        value = SOLVE[3](row1=r1, rhs1=rhs1, row2=r2, rhs2=rhs2, target=target)
        swapped = SOLVE[3](row1=r1, rhs1=rhs2, row2=r2, rhs2=rhs1, target=target)

        def row_tex(row) -> str:
            out = ""
            for coef, sym in zip(row, "abcd"):
                if coef == 0:
                    continue
                mag = "" if abs(coef) == 1 else str(abs(coef))
                if not out:                      # leading term: no spaces
                    out = f"{'-' if coef < 0 else ''}{mag}{sym}"
                else:
                    out += f" {'-' if coef < 0 else '+'} {mag}{sym}"
            return out

        return MathDraw(
            rf"\begin{{aligned}} {row_tex(r1)} &= {rhs1} \\ "
            rf"{row_tex(r2)} &= {rhs2} \end{{aligned}}",
            frac_answer_tex(value),
            prompt=(f"กำหนดให้ a, b, c และ d เป็นจำนวนจริงซึ่งสอดคล้องกับระบบ"
                    f"สมการต่อไปนี้  จงหาค่าที่เป็นไปได้ทั้งหมดของ "
                    f"{row_tex(target)}"),
            hint=r"\text{target} = \alpha\,\text{row}_1 + \beta\,\text{row}_2 "
                 r"\Rightarrow \text{value} = \alpha v_1 + \beta v_2",
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(swapped) if swapped is not None else "0",
                frac_answer_tex(value + 1), frac_answer_tex(value - 1),
                str(rhs1 + rhs2)]))


@question_type("math.posn2565_q04", display_name={"th": "ระบบสมการวงกลมสามตัวแปร"},
               level=LEVEL, topic="ระบบสมการไม่เชิงเส้น")
class CyclicReciprocalSystem(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL04)
        w = (1, 2, 3)
        value = SOLVE[4](**p, w1=w[0], w2=w[1], w3=w[2])
        return MathDraw(
            rf"a + \frac{{{p['p']}}}{{b}} = {p['p']}, \qquad "
            rf"b + \frac{{{p['q']}}}{{c}} = {p['q']}, \qquad "
            rf"c + \frac{{{p['r']}}}{{a}} = {p['r']}",
            frac_answer_tex(value),
            prompt=("ถ้า a, b และ c เป็นจำนวนจริงซึ่งสอดคล้องกับระบบสมการ"
                    "ต่อไปนี้ แล้ว a + 2b + 3c มีค่าเท่ากับเท่าใด"),
            hint=r"c = r - \frac{r}{a},\quad b = q - \frac{q}{c},"
                 r"\quad b = \frac{p}{p-a}",
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(value + 1), frac_answer_tex(-value),
                frac_answer_tex(Fraction(p["p"] + p["q"] + p["r"])),
                frac_answer_tex(value * 2)]))


@question_type("math.posn2565_q05", display_name={"th": "พหุนามดีกรีสองจากสมการเชิงฟังก์ชัน"},
               level=LEVEL, topic="สมการเชิงฟังก์ชันของพหุนาม")
class QuadraticFunctionalEquation(SheetProblem):
    def expr(self, rng: Random, m_lo: int = 2, m_hi: int = 12):
        k = rng.choice([n for n in range(-9, 10) if n])
        m = rng.randint(m_lo, m_hi)
        value = SOLVE[5](k=k, m=m)
        return MathDraw(
            rf"P(x^2) + {k}x = P(x) + {k}x^4" if k > 0 else
            rf"P(x^2) - {abs(k)}x = P(x) - {abs(k)}x^4",
            frac_answer_tex(Fraction(value)),
            prompt=(f"ให้ P(x) เป็นพหุนามดีกรีสองซึ่งสอดคล้องกับสมการต่อไปนี้ "
                    f"แล้ว P({m}) − P(0) มีค่าเท่ากับเท่าใด"),
            hint=r"P(x) = \alpha x^2 + \beta x + \gamma "
                 r"\Rightarrow \alpha = \beta = k",
            # Dropping the linear term, or evaluating P(m) as if γ were 0.
            distractors=_distinct(frac_answer_tex(Fraction(value)), [
                frac_answer_tex(Fraction(k * m * m)),
                frac_answer_tex(Fraction(k * m)),
                frac_answer_tex(Fraction(value + k)),
                frac_answer_tex(Fraction(m * m + m))]))


@question_type("math.posn2565_q06", display_name={"th": "อัตราส่วนขนมที่เปลี่ยนไปหลังกิน"},
               level=LEVEL, topic="อัตราส่วนและความน่าจะเป็น")
class RatioAfterEating(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL06)
        value = SOLVE[6](**p)
        choc0 = p["total"] * p["a"] // (p["a"] + p["b"])
        return MathDraw(
            "", str(value),
            prompt=(f"กล่องใบหนึ่งบรรจุช็อกโกแลตและลูกอมรวมกันจำนวน "
                    f"{p['total']} ชิ้น โดยมีอัตราส่วนระหว่างจำนวนช็อกโกแลตกับ"
                    f"ลูกอมเป็น {p['a']}:{p['b']}  สมชายกินลูกอมไป {p['eaten']} "
                    f"ชิ้น และกินช็อกโกแลตไปจำนวนหนึ่ง ทำให้อัตราส่วนระหว่าง"
                    f"จำนวนช็อกโกแลตกับลูกอมเปลี่ยนเป็น {p['c']}:{p['d']}  "
                    f"จงหาว่าสมชายกินช็อกโกแลตไปกี่ชิ้น"),
            hint=r"\frac{c_0 - x}{s_0 - e} = \frac{c}{d}",
            # The count he has left, and the sweets, are the two wrong readings.
            distractors=_distinct(str(value), [
                str(choc0 - value), str(choc0), str(p["eaten"]),
                str(value + p["eaten"])]))


@question_type("math.posn2565_q07", display_name={"th": "จำนวนสามสิ่งอันดับที่ ab+bc+ca คงที่"},
               level=LEVEL, topic="การนับและการจัดหมู่")
class SymmetricTripleCount(SheetProblem):
    def expr(self, rng: Random):
        target = rng.choice(TARGETS)
        value = SOLVE[7](target=target)
        return MathDraw(
            rf"ab + bc + ca = {target}", str(value),
            prompt=("มีสามสิ่งอันดับ (a, b, c) ของจำนวนเต็มบวกทั้งหมดกี่ชุด"
                    "ซึ่งสอดคล้องกับสมการต่อไปนี้"),
            hint=r"c(a+b) = n - ab \Rightarrow ab < n",
            # Counting the sorted triples instead of the ordered ones.
            distractors=_distinct(str(value), [
                str(max(1, value // 3)), str(value + 3), str(value - 3),
                str(2 * value)]))


@question_type("math.posn2565_q08", display_name={"th": "ความน่าจะเป็นที่มีแต้มเป็นจำนวนเฉพาะ"},
               level=LEVEL, topic="ความน่าจะเป็น")
class AtLeastOnePrimeFace(SheetProblem):
    def expr(self, rng: Random):
        faces = rng.choice([4, 6, 6, 6, 8, 10, 12, 20])
        dice = rng.choice([2, 2, 3])
        value = SOLVE[8](faces=faces, dice=dice)
        with_one = 1 - Fraction(faces - sum(
            1 for v in range(1, faces + 1)
            if v == 1 or q08._is_prime(v)), faces) ** dice
        return MathDraw(
            "", frac_answer_tex(value),
            prompt=(f"นายเพชรทำการโยนลูกเต๋า {dice} ลูก 1 ครั้ง โดยลูกเต๋าแต่ละ"
                    f"ลูกมี {faces} หน้า และมีแต้ม 1 ถึง {faces}  จงหาความ"
                    f"น่าจะเป็นที่มีลูกเต๋าอย่างน้อย 1 ลูกขึ้นแต้มที่เป็น"
                    f"จำนวนเฉพาะ"),
            hint=r"P = 1 - \left(\frac{\#\text{non-prime}}{f}\right)^{n}",
            # Counting 1 as a prime is the classic slip; so is forgetting the
            # complement and answering P(none).
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(with_one), frac_answer_tex(1 - value),
                frac_answer_tex(Fraction(1, 2)), frac_answer_tex(value / 2)]))


@question_type("math.posn2565_q09", display_name={"th": "ค่าความจริงของ p, q และ p → q"},
               level=LEVEL, topic="การให้เหตุผลเชิงตรรกะ")
class TruthValueTriple(SheetProblem):
    _QUADRATICS = [(2, 1, 2), (1, 1, 1), (3, 2, 5), (1, -3, 2), (1, 0, -4),
                   (2, -7, 3), (1, 0, 0), (5, 1, 1)]

    def expr(self, rng: Random):
        a, b, c = rng.choice(self._QUADRATICS)
        direction = rng.choice(["pq", "qp"])
        value = SOLVE[9](a=a, b=b, c=c, direction=direction)
        arrow = "p → q" if direction == "pq" else "q → p"

        def tex(triple) -> str:
            return "(" + ",\\ ".join(f"\\text{{{v}}}" for v in triple) + ")"

        quad = f"{a}x^2" + (f" + {b}x" if b > 0 else f" - {abs(b)}x" if b else "")
        quad += f" + {c}" if c > 0 else f" - {abs(c)}" if c else ""
        others = [("T", "T", "T"), ("T", "F", "F"), ("T", "F", "T"),
                  ("F", "F", "T"), ("F", "T", "T")]
        return MathDraw(
            rf"p:\ \forall x \exists y,\ x^2 - y = y^2 - x \qquad "
            rf"q:\ \exists x,\ {quad} = 0",
            tex(value),
            prompt=(f"ให้เอกภพสัมพัทธ์เป็นเซตของจำนวนจริง  จงหาค่าความจริงของ"
                    f"ประพจน์ p, ประพจน์ q และประพจน์ {arrow} ตามลำดับ "
                    f"(T แทนจริง, F แทนเท็จ)"),
            hint=r"y = x \text{ witnesses } p;\quad "
                 r"q \iff b^2 - 4ac \ge 0",
            distractors=_distinct(tex(value), [tex(t) for t in others]))


@question_type("math.posn2565_q10", display_name={"th": "ระดับน้ำก่อนหย่อนลูกแก้ว"},
               level=LEVEL, topic="โจทย์ปัญหาปริมาตรและร้อยละ")
class MarbleRaisesWater(SheetProblem):
    def expr(self, rng: Random):
        k = rng.randint(2, 6)
        m = rng.randint(2, 5)
        value = SOLVE[10](k=k, m=m)
        times = {2: "สองเท่า", 3: "สามเท่า", 4: "สี่เท่า", 5: "ห้าเท่า",
                 6: "หกเท่า"}[k]
        part = {2: "ครึ่งหนึ่ง", 3: "หนึ่งในสาม", 4: "หนึ่งในสี่",
                5: "หนึ่งในห้า"}[m]
        return MathDraw(
            "", frac_answer_tex(value),
            prompt=(f"แก้วน้ำใบหนึ่งภายในเป็นทรงกระบอกตรง โดยความสูงของ"
                    f"ทรงกระบอกเป็น{times}ของรัศมีของทรงกระบอก และมีลูกแก้ว"
                    f"ทรงกลมซึ่งมีรัศมีเป็น{part}ของรัศมีของทรงกระบอก  จงหาว่า"
                    f"จะต้องเติมน้ำให้สูงเป็นสัดส่วนเท่าใดของความสูงของ"
                    f"ทรงกระบอก เพื่อให้เมื่อนำลูกแก้วลูกนี้มาใส่ในแก้วน้ำแล้ว "
                    f"ระดับน้ำจะเพิ่มขึ้นจนเต็มแก้วพอดี"),
            hint=r"\pi R^2 h = \pi R^2 H - \tfrac{4}{3}\pi\left(\tfrac{R}{m}\right)^3",
            # The displaced fraction itself, and the marble/​glass volume ratio.
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(1 - value),
                frac_answer_tex(Fraction(4, 3 * m ** 3)),
                frac_answer_tex(1 - Fraction(4, 3 * m ** 2 * k)),
                frac_answer_tex(Fraction(m - 1, m))]))


@question_type("math.posn2565_q11", display_name={"th": "พื้นที่ส่วนที่เหลือของรูปสี่เหลี่ยม"},
               level=LEVEL, topic="เรขาคณิต: พื้นที่รูปสี่เหลี่ยม")
class QuadrilateralRegionArea(SheetProblem):
    def expr(self, rng: Random, ratio_lo: int = 1, ratio_hi: int = 3):
        r = rng.randint(ratio_lo, ratio_hi)
        # X, Y, Z are the areas [ADE], [ABE], [BCE]; drawing them as multiples of
        # (1+r) is what keeps the three printed areas whole numbers.
        x, y, z = (rng.randint(2, 9) * (1 + r) for _ in range(3))
        a1 = x // (1 + r)
        a2 = (r * x + y) // (1 + r)
        a3 = (r * y + z) // (1 + r)
        value = SOLVE[11](a1=a1, a2=a2, a3=a3, ratio=r)
        return MathDraw(
            rf"\frac{{DF}}{{FA}} = \frac{{AG}}{{GB}} = \frac{{BH}}{{HC}} "
            rf"= \frac{{1}}{{{r}}}",
            frac_answer_tex(value),
            prompt=(f"รูปสี่เหลี่ยม ABCD มี E, F, G และ H เป็นจุดบนด้าน CD, DA, "
                    f"AB และ BC ตามลำดับ โดยมีอัตราส่วนดังต่อไปนี้  ถ้าพื้นที่ของ"
                    f"รูปสามเหลี่ยม DEF เท่ากับ {a1} ตารางหน่วย พื้นที่ของรูป"
                    f"สี่เหลี่ยม AFEG เท่ากับ {a2} ตารางหน่วย และพื้นที่ของรูป"
                    f"สี่เหลี่ยม BGEH เท่ากับ {a3} ตารางหน่วย แล้วพื้นที่ของรูป"
                    f"สามเหลี่ยม ECH เท่ากับกี่ตารางหน่วย"),
            hint=r"[DEF] = fX,\ [AFEG] = (1-f)X + fY,\ [BGEH] = (1-f)Y + fZ,"
                 r"\ [ECH] = (1-f)Z",
            # Reading the chain one step short, and mistaking the answer for the
            # first region by symmetry.
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(Fraction(z, 1 + r)), str(a1),
                frac_answer_tex(Fraction(a1 + a2 + a3, 3)),
                str(a1 + a2 + a3)]))


@question_type("math.posn2565_q12", display_name={"th": "มุมในสามเหลี่ยมที่มีเส้นมัธยฐาน"},
               level=LEVEL, topic="เรขาคณิต: สามเหลี่ยมและเส้นมัธยฐาน")
class MedianAngleChase(SheetProblem):
    #: the sheet's constants, plus the ∠ADC = 90° family — the only two that
    #: leave the answer a whole number of degrees (see the solver's docstring).
    _POOL = [p for p in
             ([{"adc_deg": 45, "bcd_deg": 15, "ask": a}
               for a in ("acd", "abc", "bac", "acb")]
              + [{"adc_deg": 90, "bcd_deg": g, "ask": a}
                 for g in range(5, 36, 5) for a in ("abc", "bac", "acb")])
             if SOLVE[12](**p) is not None]
    _NAMES = {"acd": "∠ACD", "abc": "∠ABC", "bac": "∠BAC", "acb": "∠ACB"}

    def expr(self, rng: Random):
        p = rng.choice(self._POOL)
        value = SOLVE[12](**p)
        d, g = p["adc_deg"], p["bcd_deg"]
        return MathDraw(
            "", f"{frac_answer_tex(value)}^\\circ",
            prompt=(f"ให้ ABC เป็นรูปสามเหลี่ยม โดยที่ BC > AB และมี D เป็นจุด"
                    f"กึ่งกลางด้าน AB  ถ้า ∠ADC = {d}° และ ∠BCD = {g}° แล้ว "
                    f"{self._NAMES[p['ask']]} มีขนาดกี่องศา"),
            hint=r"AD = DB \Rightarrow \frac{\sin x}{\sin(\delta + x)} "
                 r"= \frac{\sin\gamma}{\sin(\delta - \gamma)}",
            distractors=_distinct(f"{frac_answer_tex(value)}^\\circ", [
                f"{d}^\\circ", f"{g}^\\circ", f"{d - g}^\\circ",
                f"{frac_answer_tex(180 - value)}^\\circ",
                f"{frac_answer_tex(90 - value)}^\\circ"]))


@question_type("math.posn2565_q13", display_name={"th": "ความสูงของพีระมิดฐานสามเหลี่ยม"},
               level=LEVEL, topic="เรขาคณิตสามมิติ")
class ApexAltitude(SheetProblem):
    def expr(self, rng: Random, edge_lo: int = 1, edge_hi: int = 12):
        # {60°, 90°, 120°} in any order is the one angle triple whose altitude is
        # rational — it comes out at exactly half the edge — so the tunable is
        # the edge itself, and the permutation.
        angles = rng.sample([60, 90, 120], 3)
        edge = rng.randint(edge_lo, edge_hi)
        value = Fraction(edge, 2)
        return MathDraw(
            "", frac_answer_tex(value),
            prompt=(f"กำหนดให้ ABCD เป็นพีระมิดฐานสามเหลี่ยมซึ่งมีรูปสามเหลี่ยม "
                    f"BCD เป็นฐาน โดยที่ AB = AC = AD = {edge} หน่วย และ "
                    f"∠BAC = {angles[0]}°, ∠BAD = {angles[1]}°, "
                    f"∠CAD = {angles[2]}°  ถ้า O เป็นจุดบนฐานของพีระมิดที่ทำให้ "
                    f"∠AOB = ∠AOC = ∠AOD = 90° แล้ว OA มีค่าเท่ากับกี่หน่วย"),
            hint=r"OA \perp \text{base} \Rightarrow OA = \frac{3V}{[BCD]}",
            # The circumradius of the base, and the edge itself, are the two
            # other lengths in the picture.
            distractors=_distinct(frac_answer_tex(value), [
                str(edge), frac_answer_tex(Fraction(edge, 3)),
                frac_answer_tex(Fraction(edge * 3, 2)),
                frac_answer_tex(Fraction(edge, 4))]))


@question_type("math.posn2565_q14", display_name={"th": "รัศมีวงกลมที่แทรกระหว่างสองวง"},
               level=LEVEL, topic="เรขาคณิต: วงกลมสัมผัสกัน")
class WedgedCircleRadius(SheetProblem):
    _POOL = [(p * p, q * q) for p in range(2, 8) for q in range(1, p)]

    def expr(self, rng: Random):
        r1, r2 = rng.choice(self._POOL)
        value = SOLVE[14](r1=r1, r2=r2)
        p, q = math.isqrt(r1), math.isqrt(r2)
        return MathDraw(
            "", frac_answer_tex(value),
            prompt=(f"กำหนดให้วงกลมที่มีขนาดแตกต่างกัน 3 วงสัมผัสภายนอกซึ่งกัน"
                    f"และกันและมีเส้นสัมผัสร่วมกัน โดยวงกลมวงเล็กที่สุดอยู่"
                    f"ระหว่างวงกลมอีกสองวง  ถ้าความยาวรัศมีของวงกลมทั้งสามวง"
                    f"เรียงจากมากไปน้อยเป็น {r1} หน่วย {r2} หน่วย และ x หน่วย "
                    f"แล้ว จงหา x"),
            # The sheet's picture is drawn at 4:1 and the radii are exactly what
            # this generator varies, so it is shown only at those constants.
            figure=None if (r1, r2) != (4, 1) else "",
            hint=r"\frac{1}{\sqrt{x}} = \frac{1}{\sqrt{R_1}} "
                 r"+ \frac{1}{\sqrt{R_2}}",
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(Fraction(p * q, p + q)),
                frac_answer_tex(Fraction(r1 * r2, r1 + r2)),
                frac_answer_tex(Fraction(r2, r1)),
                frac_answer_tex(Fraction((p + q) ** 2, p * q))]))


@question_type("math.posn2565_q15", display_name={"th": "มุม BCD จากด้านที่เป็นสัดส่วน"},
               level=LEVEL, topic="เรขาคณิต: มุมในรูปสี่เหลี่ยม")
class ProportionalSidesAngle(SheetProblem):
    def expr(self, rng: Random):
        base = rng.randint(2, 9)
        num, den = rng.choice([(3, 2), (2, 1), (5, 2), (4, 3), (5, 3), (3, 1)])
        ab = base * den * den
        ac = base * den * num
        ad = base * num * num                       # AB·AD = AC² by construction
        theta = rng.choice([15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 75])
        if rng.random() < 0.5:
            ab, ad = ad, ab                         # the ratio the other way
        value = SOLVE[15](ab=ab, ac=ac, ad=ad, theta_deg=theta)
        return MathDraw(
            "", f"{frac_answer_tex(value)}^\\circ",
            prompt=(f"ให้ ABCD เป็นรูปสี่เหลี่ยม โดย AB = {ab}, AC = {ac}, "
                    f"AD = {ad}  ถ้า ∠BAC = ∠CAD = {theta}° แล้ว ∠BCD "
                    f"มีขนาดกี่องศา"),
            hint=r"\frac{AB}{AC} = \frac{AC}{AD} \Rightarrow "
                 r"\triangle ABC \sim \triangle ACD",
            # 2θ is the angle at A; 90 - θ and θ are the two other easy reads.
            distractors=_distinct(f"{frac_answer_tex(value)}^\\circ", [
                f"{2 * theta}^\\circ", f"{180 - 2 * theta}^\\circ",
                f"{90 + theta}^\\circ", f"{theta}^\\circ"]))


@question_type("math.posn2565_q16", display_name={"th": "ผลบวกคำตอบของสมการยกกำลังเท่ากับหนึ่ง"},
               level=LEVEL, topic="สมการเลขชี้กำลัง")
class PowerEqualsOne(SheetProblem):
    #: (base, exponent) coefficient sets whose three cases all have rational roots
    _POOL = [p for p in
             ({"b": b, "c": c, "p": 2, "q": -11, "r": 15}
              for b in (-1, -3, -5) for c in (-1, 1, -3))
             if q16.solve(**p) is not None]

    def expr(self, rng: Random):
        p = rng.choice(self._POOL)
        value = SOLVE[16](**p)
        b, c = p["b"], p["c"]
        mag = "" if abs(b) == 1 else str(abs(b))
        base = "x^2" + (f" + {mag}x" if b > 0 else f" - {mag}x" if b else "")
        base += f" + {c}" if c > 0 else f" - {abs(c)}" if c else ""
        expo = f"{p['p']}x^2 - {abs(p['q'])}x + {p['r']}"
        # Dropping the base = -1 case, or keeping both of its roots, are the two
        # ways this is got wrong.
        from otk.sheets.posn2565_math.q16 import _roots
        minus_one = _roots(1, b, c + 1) or []
        return MathDraw(
            rf"\left({base}\right)^{{{expo}}} = 1", frac_answer_tex(value),
            prompt="จงหาผลบวกของคำตอบทั้งหมดของสมการต่อไปนี้",
            hint=r"u^v = 1 \iff v = 0,\ u = 1,\ \text{or } u = -1 "
                 r"\text{ with } v \text{ even}",
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(value - sum(minus_one, Fraction(0))
                                if len(minus_one) == 2 else value + 1),
                frac_answer_tex(value + sum(minus_one, Fraction(0))),
                frac_answer_tex(value - 1), frac_answer_tex(2 * value)]))


@question_type("math.posn2565_q17", display_name={"th": "ค่าคงที่จากเศษเหลือของพหุนามกำลังสี่"},
               level=LEVEL, topic="การหารพหุนาม")
class QuarticRemainderCombination(SheetProblem):
    #: node triples whose multiplier P(-1)/P(0) is a whole number — without that
    #: the question would have to print a fraction as its own coefficient.
    _NODES = [n for n in ((1, 2, 3), (1, 3, 8), (1, 4, 5), (2, 5, 9),
                          (2, 6, 7), (3, 4, 5))
              if q17.multiplier(n) is not None]

    def expr(self, rng: Random):
        nodes = rng.choice(self._NODES)
        r2, r1, r0 = rng.choice([(1, 0, 0), (0, 1, 0), (1, 1, 0), (2, -1, 5),
                                 (0, 0, 1), (1, -2, 3)])
        value = SOLVE[17](nodes=nodes, r2=r2, r1=r1, r0=r0)
        m = int(q17.multiplier(nodes))
        rem = {(1, 0, 0): "k²", (0, 1, 0): "k", (1, 1, 0): "k² + k",
               (2, -1, 5): "2k² − k + 5", (0, 0, 1): "1",
               (1, -2, 3): "k² − 2k + 3"}[(r2, r1, r0)]
        listed = ", ".join(str(n) for n in nodes)
        return MathDraw(
            r"f(x) = x^4 + ax^3 + bx^2 + cx + d", frac_answer_tex(value),
            prompt=(f"กำหนดให้ f(x) เป็นพหุนามดังต่อไปนี้ เมื่อ a, b, c, d เป็น"
                    f"จำนวนจริง และสำหรับแต่ละ k = {listed} เศษที่ได้จากการหาร "
                    f"f(x) ด้วย x − k เท่ากับ {rem}  จงหาค่าของ "
                    f"f(−1) − {m}f(0)"),
            hint=r"f(x) = R(x) + \prod_i (x - n_i)\,(x - r),"
                 r"\quad m = \frac{P(-1)}{P(0)}",
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(value + m), frac_answer_tex(value - m),
                frac_answer_tex(-value), frac_answer_tex(2 * value)]))


@question_type("math.posn2565_q18", display_name={"th": "ค่าของ c จากอนุกรมที่กำลังสองสมบูรณ์"},
               level=LEVEL, topic="อนุกรมเลขคณิต")
class PerfectSquareSeries(SheetProblem):
    def expr(self, rng: Random, terms_lo: int = 4, terms_hi: int = 16):
        terms = rng.randint(terms_lo, terms_hi)
        value = SOLVE[18](terms=terms)
        count, t, b, k = q18.coefficients(terms)
        return MathDraw(
            rf"\begin{{aligned}} a &= x + (x+1) + (x+2) + \dots + (x+{terms}) \\ "
            rf"b &= 8 + 16 + 24 + \dots + {8 * terms} \\ "
            rf"c &= {k}x \end{{aligned}}",
            str(value),
            prompt=("กำหนดให้ x เป็นจำนวนจริง และนิยาม a, b, c ดังต่อไปนี้  "
                    "ถ้า 4a² + b + c + 4 = 0 แล้วจงหาค่าของ c "
                    "(ตอบเป็นจำนวนเต็ม)"),
            hint=r"a = (n+1)x + T,\quad b = 8T,\quad "
                 r"4a^2 + b + c + 4 = \left(2(n+1)x + 2(T+1)\right)^2",
            # b itself, and the value of x, are the two other numbers in play.
            distractors=_distinct(str(value), [
                str(b), str(-b), str(value // 2), str(-8 * t)]))


@question_type("math.posn2565_q19", display_name={"th": "ค่าของ y − x จากสมการกำลังสาม"},
               level=LEVEL, topic="การจัดรูปพีชคณิต")
class MonotoneCubicDifference(SheetProblem):
    def expr(self, rng: Random):
        p = rng.randint(0, 6)
        q = rng.randint(1, 7)
        k = rng.choice([0, 1, 2, 3, 5, 7, 11])
        value = SOLVE[19](p=p, q=q, k=k)
        cx2, cy2, cx, cy, const = q19.coefficients(p, q, k)

        def term(coef, sym) -> str:
            if coef == 0:
                return ""
            mag = "" if abs(coef) == 1 else str(abs(coef))
            return f" {'-' if coef < 0 else '+'} {mag}{sym}"

        eq = ("x^3 - y^3" + term(cx2, "x^2") + term(cy2, "y^2")
              + term(cx, "x") + term(cy, "y") + term(const, "") + " = 0")
        return MathDraw(
            eq, str(value),
            prompt=("กำหนดให้ x, y เป็นจำนวนจริงซึ่งสอดคล้องกับสมการต่อไปนี้ "
                    "จงหาค่าของ y − x"),
            hint=r"(x+p)^3 + k(x+p) = (y-q)^3 + k(y-q),"
                 r"\quad t \mapsto t^3 + kt \text{ is injective}",
            distractors=_distinct(str(value), [
                str(p), str(q), str(-value), str(value + 1)]))


@question_type("math.posn2565_q20", display_name={"th": "รหัสจากค่ากลางของข้อมูล"},
               level=LEVEL, topic="สถิติ: ค่ากลางของข้อมูล")
class StatisticsCode(SheetProblem):
    _POOL = [p for p in ({"length": 5, "top": t, "min_kind": kind}
                         for t in range(7, 13)
                         for kind in ("odd_prime", "prime", "odd", "any"))
             if q20.solve(**p) is not None]
    _KINDS = {"odd_prime": "จำนวนเฉพาะคี่", "prime": "จำนวนเฉพาะ",
              "odd": "จำนวนคี่", "any": "จำนวนใด ๆ"}

    def expr(self, rng: Random):
        p = rng.choice(self._POOL)
        code = SOLVE[20](**p)
        digits = "".join(str(d) for d in code)
        return MathDraw(
            "", digits,
            prompt=(f"นายหินได้ขุดพบหีบสมบัติใบหนึ่งซึ่งถูกล็อคด้วยรหัส และเขา"
                    f"ยังพบกระดาษแผ่นหนึ่งที่บอกใบ้ถึงรหัสปลดล็อกหีบใบนี้ซึ่งมี"
                    f"ข้อความดังนี้  (1) รหัสเป็นเลขห้าตัวเรียงจากน้อยไปมาก "
                    f"โดยแต่ละตัวเป็นจำนวนเต็มตั้งแต่ 0 ถึง {p['top']} "
                    f"(อาจมีเลขซ้ำได้)  (2) ฐานนิยมของเลขห้าตัวนี้มีเพียงค่าเดียว "
                    f"(3) ค่าเฉลี่ยของเลขห้าตัวนี้มีค่าเท่ากับมัธยฐาน แต่มีค่า"
                    f"น้อยกว่าฐานนิยม  (4) ค่าต่ำสุดของเลขห้าตัวนี้เป็น"
                    f"{self._KINDS[p['min_kind']]}  จงหารหัสปลดล็อกหีบสมบัติใบนี้"),
            hint=r"\text{mean} = \text{median} \iff \Sigma d = 5 d_3",
            # Near misses that break exactly one clue each.
            distractors=_distinct(digits, [
                "".join(str(d) for d in (code[0], *code[2:], code[1])),
                "".join(str(d) for d in sorted(code, reverse=True)),
                "".join(str(d + 1) if i else str(d)
                        for i, d in enumerate(code)),
                "".join(str(max(0, d - 1)) for d in code)]))


@question_type("math.posn2565_q21",
               display_name={"th": "ค่าของนิพจน์จากสมการที่ให้ผลรวมสมมาตร"},
               level=LEVEL, topic="การจัดรูปพีชคณิต")
class SymmetricPowerSums(SheetProblem):
    """Never solves for a, b or c — each equation hands over one symmetric sum."""

    #: (m, s), with c pinned by t = 2 so the answer stays a printable surd.
    _POOL = [(m, s) for m in range(-3, 5)
             for s in (2, 3, 6, 7, 11, 14, 18, 23, 27)
             if q21.exact_form(m, s, 2) is not None]

    def expr(self, rng: Random):
        m, s = rng.choice(self._POOL)
        SOLVE[21](m=m, s=s, t=2)          # the closed form still has to run
        rational, coef, radicand = q21.exact_form(m, s, 2)
        answer = _surd_tex(rational, coef, radicand)
        lead = "" if m == 0 else f"{m} + "
        return MathDraw(
            rf"a = {lead}\frac{{1}}{{a}}, \quad "
            rf"b^2 = {s} - \frac{{1}}{{b^2}}, \quad "
            rf"c^3 = 2 - \frac{{1}}{{c^3}}",
            answer,
            prompt=("กำหนดให้ a, b, c เป็นจำนวนจริง ซึ่ง b > 0 และสอดคล้องกับ"
                    "สมการต่อไปนี้  จงหาค่าของ "
                    "a³ + b³ + c⁴ − 1/a³ + 1/b³ + 1/c⁴"),
            hint=r"a - \tfrac1a = m,\quad b + \tfrac1b = \sqrt{s+2},"
                 r"\quad c^3 = 1",
            # reading the first bracket as a sum, and the two usual slips in
            # expanding (b + 1/b)³.
            distractors=_distinct(answer, [
                _surd_tex(rational - 2 * (m ** 3 + 3 * m), coef, radicand),
                _surd_tex(rational, coef + 3, radicand),
                _surd_tex(rational + 2, coef, radicand),
                _surd_tex(rational, -coef, radicand),
                # when s + 2 is a perfect square the surd collapses and the
                # first three candidates can coincide, so keep plain shifts too.
                _surd_tex(rational - 2, coef, radicand),
                _surd_tex(rational + 6, coef, radicand),
                _surd_tex(-rational, coef, radicand),
                _surd_tex(rational + 4, coef, radicand)]))


@question_type("math.posn2565_q22",
               display_name={"th": "การจัดวางกล่องบนชั้นวางตามเงื่อนไข"},
               level=LEVEL, topic="การนับและการจัดหมู่")
class ShelfArrangement(SheetProblem):
    #: parameter sets that leave at least one legal arrangement.
    _POOL = [p for p in ({"shelves": 4, "first_box": fb, "anchor": anchor,
                          "away": away, "white": white}
                         for fb in (1, 3, 5, 7)
                         for anchor in range(fb, fb + 4)
                         for away in itertools.combinations(
                             [b for b in range(fb, fb + 4) if b != anchor], 2)
                         for white in range(fb, fb + 4))
             if q22.solve(**p) is not None]

    @staticmethod
    def _pairs_tex(pairs) -> str:
        return r",\ ".join(rf"({a},\, {b})" for a, b in pairs)

    def expr(self, rng: Random):
        p = rng.choice(self._POOL)
        pairs = SOLVE[22](**p)
        answer = self._pairs_tex(pairs)
        boxes = list(range(p["first_box"], p["first_box"] + 4))
        listed = ", ".join(str(b) for b in boxes[:-1]) + f" และ {boxes[-1]}"
        u, v = p["away"]
        mirrored = sorted({*pairs, *((a, 5 - b) for a, b in pairs)})
        return MathDraw(
            "", answer,
            prompt=(f"กำหนดให้มีลูกเทนนิส 2 ลูก มีลูกปิงปองสีส้มและลูกปิงปอง"
                    f"สีขาวอย่างละ 1 ลูก มีชั้นวางของ 4 ชั้น โดยเรียกชั้นบนสุด"
                    f"ว่าชั้นที่ 1 และชั้นถัดมาคือชั้นที่ 2, 3 และ 4 ตามลำดับ "
                    f"และมีกล่อง 4 ใบที่มีหมายเลขติดไว้ดังนี้ กล่องหมายเลข "
                    f"{listed}  นำลูกปิงปองและลูกเทนนิสไปใส่ไว้ในกล่อง กล่องละ "
                    f"1 ลูก และวางกล่องบนชั้นวางของ ชั้นละ 1 กล่อง โดยมี"
                    f"เงื่อนไขดังนี้  (ก) ลูกเทนนิส 2 ลูกต้องอยู่บนชั้นที่ติดกัน  "
                    f"(ข) ลูกปิงปอง 2 ลูกจะไม่อยู่บนชั้นที่ติดกัน  "
                    f"(ค) กล่องหมายเลข {u} และกล่องหมายเลข {v} จะไม่วางบนชั้น"
                    f"ที่อยู่ติดกับชั้นที่กล่องหมายเลข {p['anchor']} วางอยู่  "
                    f"ถ้าวางลูกปิงปองสีขาวไว้ในกล่องหมายเลข {p['white']} "
                    f"จงหาคู่อันดับ (a, b) ที่เป็นไปได้ทั้งหมด เมื่อลูกปิงปอง"
                    f"สีส้มอยู่ในกล่องหมายเลข a และวางบนชั้นที่ b"),
            hint=r"(\text{c}) \Rightarrow \text{anchor box has} \le 1 "
                 r"\text{neighbour} \Rightarrow \text{shelf } 1 \text{ or } 4",
            distractors=_distinct(answer, [
                # keeping only the top arrangement; swapping the two entries of
                # the pair; sliding every shelf down one; and the middle shelves
                # rule (ค) actually rules out.
                self._pairs_tex(pairs[:1]),
                self._pairs_tex([(b, a) for a, b in pairs]),
                self._pairs_tex([(a, b % 4 + 1) for a, b in pairs]),
                self._pairs_tex(sorted({(a, 2 if b == 1 else 3)
                                        for a, b in pairs})),
                self._pairs_tex(mirrored),
                self._pairs_tex(sorted({*pairs, (p["white"], 2)}))]))


@question_type("math.posn2565_q23",
               display_name={"th": "พื้นที่แรเงาระหว่างครึ่งวงกลมแนบในกับมุมฉาก"},
               level=LEVEL, topic="เรขาคณิต: วงกลมแนบใน")
class SemicircleCornerArea(SheetProblem):
    """The region at C is a square of side r less a quarter disk — nothing else."""

    #: (p, q) with 2pq a perfect square, so the radius comes out whole.
    _POOL = [(p, q) for p in range(1, 33) for q in range(1, 33)
             if q23.exact_radius(p, q) is not None]

    def expr(self, rng: Random):
        p, q = rng.choice(self._POOL)
        SOLVE[23](p=p, q=q)                # the numeric pair still has to agree
        r = q23.exact_radius(p, q)
        area = Fraction(r * r)
        quarter = area / 4

        def tex(square: Fraction, coef: Fraction) -> str:
            # plain fractions here: the mixed-number form frac_answer_tex adds
            # would land in the middle of the expression.
            return rf"{frac_tex(square)} - {frac_tex(coef)}\pi"

        answer = tex(area, quarter)
        return MathDraw(
            rf"DG = {p}, \quad EF = {q}", answer,
            prompt=("จากรูป ให้ ABC เป็นรูปสามเหลี่ยมมุมฉาก โดยมีมุม C เป็นมุมฉาก "
                    "ให้ DE เป็นเส้นผ่านศูนย์กลางของครึ่งวงกลมแนบในรูปสามเหลี่ยม "
                    "ABC ให้ G และ F เป็นจุดบนด้าน AC และ BC ตามลำดับ โดยที่ DG "
                    f"ตั้งฉากกับ AC และ EF ตั้งฉากกับ BC  ถ้า DG = {p} หน่วย และ "
                    f"EF = {q} หน่วย แล้วบริเวณที่แรเงา (บริเวณที่ปิดล้อมด้วยด้าน "
                    "CA ด้าน CB และส่วนโค้ง) มีพื้นที่เท่ากับกี่ตารางหน่วย"),
            hint=r"r = p + q + \sqrt{2pq},\quad \text{area} = r^2 - \tfrac{\pi r^2}{4}",
            # the crop names 6 and 12 on the figure itself.
            figure=self.default_figure()[0] if (p, q) == (6, 12) else None,
            distractors=_distinct(answer, [
                tex(area, area / 2),               # half disk instead of quarter
                tex(area * 2, quarter),
                tex(area, quarter * 2),
                tex(area / 2, quarter / 2),
                tex(area + 1, quarter)]))


@question_type("math.posn2565_q24",
               display_name={"th": "ผลคูณของฟังก์ชันตรีโกณของครึ่งมุมในรูปสี่เหลี่ยมจัตุรัส"},
               level=LEVEL, topic="เรขาคณิต: สี่เหลี่ยมจัตุรัส")
class SquareHalfAngleProduct(SheetProblem):
    """∠ADG = ∠AED for every cut point, so all four products are computable."""

    #: the midpoints are the only cut giving a rational answer, so the question
    #: varies instead — which of the four products it asks for.
    _ASKS = {
        "sin_cos": (r"\sin\!\left(\frac{\angle ADG}{2}\right)"
                    r"\cos\!\left(\frac{\angle AED}{2}\right)",
                    "sin(∠ADG/2)·cos(∠AED/2)"),
        "sin_sin": (r"\sin\!\left(\frac{\angle ADG}{2}\right)"
                    r"\sin\!\left(\frac{\angle AED}{2}\right)",
                    "sin(∠ADG/2)·sin(∠AED/2)"),
        "cos_cos": (r"\cos\!\left(\frac{\angle ADG}{2}\right)"
                    r"\cos\!\left(\frac{\angle AED}{2}\right)",
                    "cos(∠ADG/2)·cos(∠AED/2)"),
        "tan": (r"\frac{\sin\!\left(\frac{\angle ADG}{2}\right)}"
                r"{\cos\!\left(\frac{\angle AED}{2}\right)}",
                "sin(∠ADG/2)/cos(∠AED/2)"),
    }

    def expr(self, rng: Random):
        ask = rng.choice(sorted(self._ASKS))
        value = SOLVE[24](num=1, den=2, ask=ask)
        tex, spoken = self._ASKS[ask]
        others = [SOLVE[24](num=1, den=2, ask=other)
                  for other in sorted(self._ASKS) if other != ask]
        answer = frac_answer_tex(value)
        return MathDraw(
            tex, answer,
            prompt=("กำหนดให้ ABCD เป็นรูปสี่เหลี่ยมจัตุรัสที่มี E และ F เป็นจุด"
                    "กึ่งกลางด้าน BC และ CD และให้เส้นตรง AE และเส้นตรง BF "
                    f"ตัดกันที่จุด G  จงหาค่าของ {spoken}"),
            hint=r"AE \perp BF,\quad \angle ADG = \angle AED = \theta,"
                 r"\quad \cos\theta = \tfrac35",
            distractors=_distinct(answer, [
                *(frac_answer_tex(v) for v in others),
                frac_answer_tex(1 - value), frac_answer_tex(value / 2),
                # the three products share their values, so top the list up with
                # near misses that do not collide with any of them.
                frac_answer_tex(value * 2), frac_answer_tex(Fraction(3, 5)),
                frac_answer_tex(Fraction(1, 4)), frac_answer_tex(Fraction(3, 10))]))


@question_type("math.posn2565_q25",
               display_name={"th": "ค่ามากที่สุดของ m − n จากผลบวกของส่วนกลับ"},
               level=LEVEL, topic="การหาค่าเหมาะที่สุดเชิงจำนวนเต็ม")
class UnitFractionSpread(SheetProblem):
    #: (k, num) pairs that admit at least one solution.
    _POOL = [(k, num) for k in range(5, 60) for num in (1, 2, 3)
             if q25.solve(k=k, num=num) is not None]

    def expr(self, rng: Random):
        k, num = rng.choice(self._POOL)
        value = SOLVE[25](k=k, num=num)
        return MathDraw(
            rf"\frac{{1}}{{m}} + \frac{{1}}{{n}} = \frac{{{num}}}{{{k}}}",
            str(value),
            prompt=("ให้ m และ n เป็นจำนวนเต็มบวกซึ่ง m ≥ n และสอดคล้องกับสมการ"
                    "ต่อไปนี้  จงหาค่ามากที่สุดที่เป็นไปได้ของ m − n"),
            hint=r"m = \frac{kn}{\;\text{num}\cdot n - k\;};\ "
                 r"\text{push the denominator down to its smallest divisor}",
            distractors=_distinct(str(value), [
                str(value + k), str(value - k), str(k * k), str(value // 2 or 1),
                str(value + 1)]))


@question_type("math.posn2565_q26",
               display_name={"th": "ค่าของ x + y จากระบบสมการที่มีกรณฑ์"},
               level=LEVEL, topic="ระบบสมการไม่เชิงเส้น")
class SymmetricRadicalSystem(SheetProblem):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    #: (a, b) with b + 3a = 2t³, the condition that keeps u + v a multiple of √2.
    _POOL = [(a, 2 * t ** 3 - 3 * a) for t in (2, 3, 4)
             for a in range(1, 3 * t ** 3)
             if q26.solve(a=a, b=2 * t ** 3 - 3 * a) is not None]

    def expr(self, rng: Random):
        a, b = rng.choice(self._POOL)
        value = SOLVE[26](a=a, b=b)

        def side(coef: int) -> str:
            return r"\sqrt{2}" if coef == 1 else rf"{coef}\sqrt{{2}}"

        return MathDraw(
            rf"\begin{{aligned}} x\sqrt{{y}} + y\sqrt{{x}} &= {side(a)} \\ "
            rf"x\sqrt{{x}} + y\sqrt{{y}} &= {side(b)} \end{{aligned}}",
            frac_answer_tex(value),
            prompt=("ให้ x และ y เป็นจำนวนจริงบวกซึ่งสอดคล้องกับระบบสมการ"
                    "ต่อไปนี้  แล้ว x + y มีค่าเท่ากับเท่าใด"),
            hint=r"u = \sqrt{x},\ v = \sqrt{y}:\ uv(u+v) = a\sqrt2,\ "
                 r"(u+v)^3 - 3uv(u+v) = b\sqrt2",
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(value + 1), frac_answer_tex(value - 1),
                frac_answer_tex(value * 2), frac_answer_tex(value + 2),
                frac_answer_tex(Fraction(a + b))]))


@question_type("math.posn2565_q27",
               display_name={"th": "เศษจากการหารส่วนจำนวนเต็มของเศษส่วนขนาดใหญ่"},
               level=LEVEL, topic="การหารลงตัวและเศษเหลือ")
class FloorOfHugeQuotient(SheetProblem):
    #: (k, c) with c³ well below 10^k, so the identity's tail really is < 1.
    _POOL = [(k, c) for k in range(6, 15) for c in range(1, 40)
             if c ** 3 < 10 ** k]

    def expr(self, rng: Random):
        k, c = rng.choice(self._POOL)
        mod = rng.choice([100, 1000, 10000])
        value = SOLVE[27](k=k, c=c, mod=mod)
        return MathDraw(
            # 1000^k is 10^{3k} — the sheet's own disguise for the numerator.
            rf"a = \frac{{1000^{{{k}}}}}{{10^{{{k}}} + {c}}}", str(value),
            prompt=("สำหรับจำนวนจริง a ใด ๆ กำหนดให้ ⌊a⌋ คือจำนวนเต็มมากที่สุด"
                    "ที่น้อยกว่าหรือเท่ากับ a  ถ้า a เป็นดังต่อไปนี้ แล้วเศษ"
                    f"จากการหาร ⌊a⌋ ด้วย {mod} มีค่าเท่ากับเท่าใด"),
            hint=r"\frac{x^3}{x+c} = x^2 - cx + c^2 - \frac{c^3}{x+c},"
                 r"\quad 0 < \frac{c^3}{x+c} < 1",
            distractors=_distinct(str(value), [
                str((c * c) % mod),              # forgetting the −1
                str((c * c - 2) % mod), str((c ** 3 - 1) % mod),
                str((c - 1) % mod), str((value + mod // 2) % mod),
                # small c makes the structural near-misses collide; plain
                # shifts keep the choice list full.
                str((value + 1) % mod), str((value - 1) % mod),
                str((2 * value) % mod), str((value + 7) % mod)]))


@question_type("math.posn2565_q28",
               display_name={"th": "ค่ามากที่สุดของ x + y บนภาคตัดกรวยที่มีจุดตรรกยะจุดเดียว"},
               level=LEVEL, topic="ทฤษฎีจำนวนเชิงพีชคณิต")
class SingleRationalPoint(SheetProblem):
    """Built backwards: the discriminant is forced to be k(py − q)², k non-square."""

    @staticmethod
    def _build() -> list[tuple[int, int, int, int, int]]:
        out = []
        for k in (2, 3, 5, 6, 7, 10, 11, 12, 13):
            for p in range(1, 4):
                for q in range(-3, 5):
                    for b in range(-8, 10, 2):
                        for d in range(-16, 18, 2):
                            if ((b * b - k * p * p) % 4 or (d * d - k * q * q) % 4
                                    or (2 * b * d + 2 * k * p * q) % 4):
                                continue
                            c = (b * b - k * p * p) // 4
                            f = (d * d - k * q * q) // 4
                            e = (2 * b * d + 2 * k * p * q) // 4
                            if max(abs(c), abs(e), abs(f)) > 60:
                                continue
                            value = q28.solve(b=b, c=c, d=d, e=e, f=f)
                            if value is not None and abs(value) <= 30:
                                out.append((b, c, d, e, f))
        return out

    _POOL: list[tuple[int, int, int, int, int]] = []

    def expr(self, rng: Random):
        if not self._POOL:
            SingleRationalPoint._POOL = self._build()
        b, c, d, e, f = rng.choice(self._POOL)
        value = SOLVE[28](b=b, c=c, d=d, e=e, f=f)

        def term(coef: int, sym: str, lead: bool = False) -> str:
            if coef == 0:
                return ""
            mag = "" if abs(coef) == 1 and sym else str(abs(coef))
            if lead:
                return f"{'-' if coef < 0 else ''}{mag}{sym}"
            return f" {'-' if coef < 0 else '+'} {mag}{sym}"

        eq = ("x^2" + term(b, "xy") + term(c, "y^2") + term(d, "x")
              + term(e, "y") + term(f, "") + " = 0")
        return MathDraw(
            eq, frac_answer_tex(value),
            prompt=("กำหนดให้ x, y เป็นจำนวนตรรกยะที่สอดคล้องกับสมการต่อไปนี้ "
                    "จงหาค่ามากที่สุดที่เป็นไปได้ของ x + y "
                    "(สังเกตว่าโจทย์บังคับให้เป็นจำนวนตรรกยะ)"),
            hint=r"\text{disc}_x = (B^2-4C)y^2 + (2BD-4E)y + (D^2-4F) = k(py-q)^2,"
                 r"\quad k \text{ not a square}",
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(-value), frac_answer_tex(value + 1),
                frac_answer_tex(value - 1), frac_answer_tex(value * 2),
                frac_answer_tex(value + 3), frac_answer_tex(value - 3),
                frac_answer_tex(value + 5), frac_answer_tex(value - 6)]))


@question_type("math.posn2565_q29",
               display_name={"th": "พหุนามสัมประสิทธิ์เลขโดดจากค่าที่จุดสองจุด"},
               level=LEVEL, topic="พหุนามสัมประสิทธิ์จำนวนเต็ม")
class DigitCoefficientPolynomial(SheetProblem):
    #: (sum of coefficients, value at the base, base) with a unique polynomial.
    _POOL = [(total, value, base)
             for base in (3, 4, 5)
             for total in range(2, 8)
             for value in range(base, 220)
             if q29.solve(total=total, value=value, base=base) is not None]

    @staticmethod
    def _poly_tex(coefs) -> str:
        degree = len(coefs) - 1
        parts = []
        for i, coef in enumerate(coefs):
            if coef == 0:
                continue
            power = degree - i
            mag = "" if coef == 1 and power else str(coef)
            body = "" if power == 0 else ("x" if power == 1 else f"x^{{{power}}}")
            parts.append(f"{mag}{body}")
        return " + ".join(parts) if parts else "0"

    def expr(self, rng: Random):
        total, value, base = rng.choice(self._POOL)
        coefs = SOLVE[29](total=total, value=value, base=base)
        answer = self._poly_tex(coefs)
        shifted = list(coefs)
        shifted[-1] = shifted[-1] + 1
        return MathDraw(
            rf"P(1) = {total}, \quad P({base}) = {value}", answer,
            prompt=("นักคณิตศาสตร์สองท่านสนทนากันดังนี้  "
                    "เกาส์: ผมมีพหุนามอยู่พหุนามหนึ่งที่มีสัมประสิทธิ์เป็นเลขโดด "
                    "(ตั้งแต่ 0 ถึง 9)  "
                    "ออยเลอร์: ผลรวมของสัมประสิทธิ์ทั้งหมดในพหุนามนี้มีค่าเท่าใด  "
                    f"เกาส์: {total}  "
                    f"ออยเลอร์: ถ้านำ {base} ไปแทนค่าในพหุนามนี้ล่ะ จะได้เท่าใด  "
                    f"เกาส์: {value}  "
                    "ออยเลอร์: ผมรู้แล้วล่ะว่าคุณมีพหุนามใด  "
                    "เกาส์มีพหุนามใดตามบทสนทนานี้"),
            hint=r"P(1) = \sum a_i,\ \text{and } P(1) < b \Rightarrow "
                 r"\text{the } a_i \text{ are the base-} b \text{ digits}",
            distractors=_distinct(answer, [
                self._poly_tex(shifted),
                self._poly_tex(tuple(reversed(coefs))),
                self._poly_tex(tuple(c + 1 for c in coefs)),
                self._poly_tex(coefs[1:] or (0,)),
                self._poly_tex((1,) + tuple(coefs)),
                self._poly_tex(tuple(coefs) + (0,)),
                self._poly_tex(tuple(coefs) + (1,)),
                self._poly_tex((2,) + tuple(coefs)[1:])]))


@question_type("math.posn2565_q30",
               display_name={"th": "จำนวนสิ่งอันดับที่มีผลบวกสลับเครื่องหมายตามกำหนด"},
               level=LEVEL, topic="การนับเชิงการจัด")
class AlternatingSumPermutations(SheetProblem):
    #: (n, target) with at least one tuple; n stays even.
    _POOL = [(n, t) for n in (6, 8, 10, 12)
             for t in range(-n * n // 2, n * n // 2 + 1)
             if (q30.solve(n=n, target=t) or 0) > 0]

    def expr(self, rng: Random):
        n, target = rng.choice(self._POOL)
        value = SOLVE[30](n=n, target=target)
        signs = " ".join(f"{'+' if i % 2 == 0 else '-'} x_{{{i + 1}}}"
                         for i in range(n)).lstrip("+ ")
        return MathDraw(
            rf"\begin{{aligned}} \{{x_1, \dots, x_{{{n}}}\}} &= "
            rf"\{{1, 2, \dots, {n}\}} \\ {signs} &= {target} \end{{aligned}}",
            str(value),
            prompt=(f"จงหาจำนวน {n} สิ่งอันดับ (x₁, x₂, …, x{n}) ทั้งหมด "
                    "ซึ่งสอดคล้องเงื่อนไขทั้งสองข้อต่อไปนี้"),
            hint=r"A + B = \tfrac{n(n+1)}{2},\ A - B = t \Rightarrow "
                 r"\text{count subsets of size } \tfrac n2 \text{ summing to } A",
            distractors=_distinct(str(value), [
                str(value * 2), str(value // 2 or 1),
                str(math.factorial(n // 2) ** 2), str(math.factorial(n)),
                str(value + math.factorial(n // 2))]))
