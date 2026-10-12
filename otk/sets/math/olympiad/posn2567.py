"""พหุนามสมมาตร

คณิตศาสตร์ · โอลิมปิก (สอวน.) · สอวน.
Indicators: —

Sets moved here from: posn2567.
"""

from __future__ import annotations

import math
from fractions import Fraction
from functools import lru_cache
from random import Random

from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem, frac_answer_tex
from otk.sheets import figure_attachments
from otk.sheets.posn2567_math import (
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


SHEET = "สอวน. ค่าย 1 (2567)"


SHEET_ID = "posn2567_math"


_MODULES = [q01, q02, q03, q04, q05, q06, q07, q08, q09, q10,
            q11, q12, q13, q14, q15, q16, q17, q18, q19, q20,
            q21, q22, q23, q24, q25, q26, q27, q28, q29, q30]


SOLVE = {n: lru_cache(maxsize=4096)(mod.solve)
         for n, mod in enumerate(_MODULES, start=1)}


FIGURES = figure_attachments(SHEET_ID)


class SheetProblem(WordProblem):
    """A โจทย์ from the 2567 sheet: Thai prompt, exact TeX answer."""

    sheet = SHEET
    sheet_id = SHEET_ID

    def default_figure(self) -> tuple[str, str]:
        return FIGURES.get(self.key, ("", ""))


def _pool_q01() -> list[dict]:
    """(squares, pairs) pairs that a real triple can actually produce.

    a²+b²+c² ≥ ab+bc+ca always, so squares ≥ p is required; without it the
    generator would ask about a configuration that does not exist.
    """
    out = []
    for p in range(-6, 13):
        for squares in range(max(1, p), 31):
            if (squares + 3 * p) > 0:
                out.append({"squares": squares, "pairs": squares + 3 * p})
    return out


def _pool_q02() -> list[dict]:
    """(total, remainder) with a divisor count worth counting."""
    out = []
    for remainder in (6, 8, 10, 12, 15, 20, 24, 30, 40):
        for base in (240, 360, 480, 600, 720, 1000, 1200, 2000, 2400, 3600):
            total = base + remainder
            if SOLVE[2](total=total, remainder=remainder) >= 3:
                out.append({"total": total, "remainder": remainder})
    return out


def _pool_q03() -> list[dict]:
    out = []
    for rhs3 in (2, 3, 4, 5, 9):
        for rhs5 in (1, 2, 3):
            for off_hi in range(4, 26):
                p = {"lhs3": 1, "lhs5": 1, "rhs3": rhs3, "rhs5": rhs5,
                     "off_lo": 1, "off_hi": off_hi}
                if SOLVE[3](**p) is not None:
                    out.append(p)
    return out


def _pool_q08() -> list[dict]:
    """Quartics that x²+px+q really divides, with integral m and n."""
    out = []
    for p in (-2, -1, 1, 2, 3, 4):
        for q in (2, 3, 5, 6, 7, 11):
            for c2 in range(-2, 9):
                for c1 in range(-6, 7):
                    if SOLVE[8](p=p, q=q, c2=c2, c1=c1) is not None:
                        out.append({"p": p, "q": q, "c2": c2, "c1": c1})
    return out


def _pool_q09() -> list[dict]:
    """Constants whose boundary is a whole number, so the answer reads a ≤ -5."""
    out = []
    for shift in range(0, 7):
        for konst in range(1, 41):
            v = SOLVE[9](shift=shift, konst=konst)
            if v is not None and v.denominator == 1 and v < 0:
                out.append({"shift": shift, "konst": konst})
    return out


def _pool_q12() -> list[dict]:
    """(∠ODE, ∠OBE) pairs the configuration actually admits.

    Unequal, because the "swapped the two angles" distractor 180-u-2v collapses
    onto the answer when u = v and the item would come out with three choices.
    """
    return [{"ode_deg": u, "obe_deg": v}
            for u in range(5, 61, 5) for v in range(5, 61, 5)
            if u != v and u + v <= 80]


def _pool_q13() -> list[dict]:
    """(height, diagonal) with a rational area — the sheet asks for a fraction."""
    return [{"height": h, "diagonal": d}
            for d in range(5, 62) for h in range(3, d)
            if q13.solve(height=h, diagonal=d) is not None]


def _pool_q14() -> list[dict]:
    """Radii for the two big circles, the sheet's equal pair included."""
    return [{"r_low": lo, "r_up": up}
            for lo in range(1, 8) for up in range(1, 8)
            if math.gcd(lo, up) == 1 or lo == up == 1]


def _pool_q21() -> list[dict]:
    """Box contents whose stated probability really does pin a whole count."""
    out = []
    for g1 in range(2, 10):
        for b1 in range(2, 10):
            for g2 in range(1, 8):
                for den in (2, 3, 4, 5, 6, 9):
                    for num in range(1, den):
                        p = {"g1": g1, "b1": b1, "g2": g2,
                             "p_num": num, "p_den": den}
                        v = SOLVE[21](**p)
                        if v is not None and 2 <= v <= 60:
                            out.append(p)
    return out


def _pool_q23() -> list[dict]:
    """(top, draws) whose probability is neither 0 nor 1 and stays enumerable."""
    return [{"top": t, "draws": k}
            for t in (9, 10, 12, 15, 18, 20) for k in (2, 3, 4)
            if 0 < SOLVE[23](top=t, draws=k) < 1 and t ** k <= 2 * 10 ** 6]


POOL01, POOL02, POOL03 = _pool_q01(), _pool_q02(), _pool_q03()


POOL08, POOL09 = _pool_q08(), _pool_q09()


POOL12, POOL13, POOL14 = _pool_q12(), _pool_q13(), _pool_q14()


POOL21, POOL23 = _pool_q21(), _pool_q23()


#: (A's points, C's points) that leave exactly one point table — most do not.
POOL29 = [{"pts_a": a, "pts_c": c} for a in range(0, 13) for c in range(0, 13)
          if SOLVE[29](pts_a=a, pts_c=c) is not None]


#: clue placements for the farm puzzle whose assignment is still unique.
POOL30 = [{"pig_person": p, "boekban_person": b, "not_mana_person": m}
          for p in range(4) for b in range(4) for m in range(4)
          if SOLVE[30](pig_person=p, boekban_person=b, not_mana_person=m)
          is not None]


def _pow2_tex(value: int) -> str:
    """A power of two as ``2^{126}``, anything else as ``odd \\cdot 2^{k}``.

    ข้อ 28's answers run to forty digits, so they are written in the form the
    counting argument produces rather than expanded.
    """
    k = (value & -value).bit_length() - 1
    odd = value >> k
    if odd == 1:
        return rf"2^{{{k}}}" if k else "1"
    return rf"{odd} \cdot 2^{{{k}}}" if k else str(odd)


#: multipliers k in ∠DCF = k(∠ADE - ∠BAD) whose answer 45 + 90/(k+1) is a whole
#: number of degrees — the sheet's k = 2 is the first of them.
MULTIPLIERS = [k for k in range(2, 40) if 90 % (k + 1) == 0]


#: regular n-gons whose ∠BND = 720/n is a whole number of degrees.
POLYGONS = [n for n in range(5, 21) if 720 % n == 0]


#: (R_A, R_B) for ข้อ 18 — perfect squares, so the answer is a printable surd.
RADII_PAIRS = [{"r_a": p * p, "r_b": q * q}
               for p in range(1, 7) for q in range(1, p + 1)]


def _distinct(value, candidates: list[str], want: int = 4) -> list[str]:
    """The first ``want`` candidates that differ from the answer and each other.

    Hand-picked distractors are near misses by construction, so some of them
    collapse onto the answer — or onto one another — at particular constants
    (∠BND = 90° for the octagon makes "180 - ∠BND" the answer again). Offering a
    few extra and filtering keeps every draw at four choices without weakening
    the first, best distractor.
    """
    out: list[str] = []
    for c in candidates:
        if c != value and c not in out:
            out.append(c)
        if len(out) == want:
            break
    return out


def _surd_tex(coef: Fraction, radicand: int) -> str:
    """``coef·√radicand`` as reduced TeX: 45\\sqrt{2}, \\frac{5\\sqrt{2}}{3}, 7."""
    root = "" if radicand == 1 else rf"\sqrt{{{radicand}}}"
    if not root:
        return frac_answer_tex(coef)
    if coef == 1:
        return root
    if coef.denominator == 1:
        return rf"{coef.numerator}{root}"
    num = "" if coef.numerator == 1 else str(coef.numerator)
    return rf"\frac{{{num}{root}}}{{{coef.denominator}}}"


def _pm_surd(m: int, n: int, d: int, den: int) -> str:
    """``(m + n√d)/den`` as reduced TeX — the shape every ข้อ 18 answer takes."""
    if d == 1:                                   # the root closed up
        return frac_answer_tex(Fraction(m + n, den))
    g = math.gcd(math.gcd(abs(m), abs(n)), den)
    m, n, den = m // g, n // g, den // g
    sign = "-" if n < 0 else "+"
    coef = "" if abs(n) == 1 else str(abs(n))
    top = rf"{m} {sign} {coef}\sqrt{{{d}}}"
    return top if den == 1 else rf"\frac{{{top}}}{{{den}}}"


@lru_cache(maxsize=None)
def _partitions(k: int) -> int:
    """Unrestricted partitions of k — the count when "distinct" is forgotten."""
    ways = [1] + [0] * k
    for part in range(1, k + 1):
        for s in range(part, k + 1):
            ways[s] += ways[s - part]
    return ways[k]


#: t → t³ - 3t, the value the sheet gives for a³ + 1/a³.
CUBE_SUMS = [t ** 3 - 3 * t for t in range(3, 8)]


@question_type("math.posn2567_q01", display_name={"th": "ค่าของ ab + bc + ca"},
               level=LEVEL, topic="พหุนามสมมาตร")
class SymmetricPairSum(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL01)
        value = SOLVE[1](**p)
        return MathDraw(
            "", frac_answer_tex(value),
            prompt=(f"ให้ a, b และ c เป็นจำนวนจริง โดยที่ "
                    f"a² + b² + c² = {p['squares']} และ "
                    f"(a+b)(b+c) + (b+c)(c+a) + (c+a)(a+b) = {p['pairs']}  "
                    f"ค่าของ ab + bc + ca เท่ากับเท่าใด"),
            hint=r"(a+b)(b+c)+(b+c)(c+a)+(c+a)(a+b) = s^2 + p,\quad a^2+b^2+c^2 = s^2 - 2p",
            distractors=[str(p["pairs"] - p["squares"]),
                         frac_answer_tex(Fraction(p["pairs"] + p["squares"], 3)),
                         str(p["squares"]), str(p["pairs"] // 3)])


@question_type("math.posn2567_q02", display_name={"th": "จำนวนตัวหารที่เหลือเศษกำหนด"},
               level=LEVEL, topic="การหารลงตัวและเศษเหลือ")
class DivisorsWithRemainder(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL02)
        value = SOLVE[2](**p)
        total, r = p["total"], p["remainder"]
        # The classic slip is forgetting that a remainder must be smaller than
        # the divisor, which counts every divisor of total - r.
        from otk.sheets.posn2567_math.q02 import _divisors
        return MathDraw(
            "", str(value),
            prompt=(f"ให้ A เป็นเซตของจำนวนเต็มบวก n ทั้งหมด โดยที่ n หาร "
                    f"{total} เหลือเศษ {r}  จำนวนสมาชิกของเซต A เท่ากับเท่าใด"),
            hint=r"n \mid (N - r) \text{ and } n > r",
            distractors=[str(len(_divisors(total - r))),
                         str(value + 1), str(value - 1),
                         str(len(_divisors(total)))])


@question_type("math.posn2567_q03", display_name={"th": "สมการเลขชี้กำลังฐาน 3 และ 5"},
               level=LEVEL, topic="สมการเลขชี้กำลัง")
class ExponentTower(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL03)
        value = SOLVE[3](**p)
        base = 3 ** p["rhs3"] * 5 ** p["rhs5"]
        return MathDraw(
            rf"15^{{\frac{{1}}{{x+{p['off_lo']}}}}} = "
            rf"\left({base} \cdot 5^{{\frac{{y}}{{2}}}}\right)"
            rf"^{{\frac{{1}}{{x+{p['off_hi']}}}}}",
            str(value),
            prompt=("ให้ x และ y เป็นจำนวนเต็มบวกที่สอดคล้องกับสมการต่อไปนี้  "
                    "ค่าของ x + y เท่ากับเท่าใด"),
            hint=r"3^{\alpha}5^{\beta} = 3^{\gamma}5^{\delta} \iff "
                 r"\alpha = \gamma,\ \beta = \delta",
            distractors=[str(value + 1), str(value - 1), str(2 * value),
                         str(p["off_hi"] - p["off_lo"])])


@question_type("math.posn2567_q04", display_name={"th": "อนุกรมสลับเครื่องหมาย"},
               level=LEVEL, topic="อนุกรมสลับเครื่องหมาย")
class AlternatingSeriesRange(SheetProblem):
    def expr(self, rng: Random, top_lo: int = 100, top_hi: int = 2024):
        ca = rng.choice([c for c in range(2, 9)])
        cb = rng.choice([c for c in range(1, ca)])
        top = 2 * rng.randint(top_lo // 2, top_hi // 2)
        value = SOLVE[4](ca=ca, cb=cb, top=top)
        combo = f"{ca}A + B" if cb == 1 else f"{ca}A + {cb}B"
        return MathDraw(
            "", rf"0 < a \le {frac_answer_tex(value)}",
            prompt=(f"กำหนดให้ a เป็นจำนวนจริงบวก และให้ "
                    f"A = a - a² + a³ - a⁴ + ⋯ - a^{top} และ "
                    f"B = a + a² + a³ + a⁴ + ⋯ + a^{top}  "
                    f"จงหาเซตของจำนวนจริงบวก a ทั้งหมดที่ทำให้ {combo} ≥ 0"),
            hint=rf"{combo} = \sum_j a^{{2j-1}}\left[({ca}+{cb}) - ({ca}-{cb})a\right]",
            distractors=[rf"0 < a \le {frac_answer_tex(Fraction(ca, cb))}",
                         rf"a \ge {frac_answer_tex(value)}",
                         rf"0 < a \le {frac_answer_tex(value + 1)}",
                         r"a > 0"])


@question_type("math.posn2567_q05", display_name={"th": "ตัดหลักแรกแล้วเหลือหนึ่งส่วน m"},
               level=LEVEL, topic="โจทย์เลขหลักฐานสิบ")
class StripLeadingDigit(SheetProblem):
    #: multipliers for which a solution exists at all (m-1 must divide t·10^d
    #: for some digit t) — scanned once so no draw can come out empty.
    _POOL = [m for m in range(11, 92)
             if q05.solve(multiplier=m) is not None]

    def expr(self, rng: Random):
        m = rng.choice(self._POOL)
        value = SOLVE[5](multiplier=m)
        return MathDraw(
            "", str(value),
            prompt=(f"จงหาจำนวนเต็มบวก a ที่น้อยที่สุด ซึ่งเมื่อเขียน a ใน"
                    f"ระบบฐานสิบและตัดหลักแรก (จากซ้ายมือสุด) ออกแล้ว จะได้"
                    f"จำนวนเต็มบวก b โดยที่ a มีค่าเท่ากับ {m} เท่าของ b"),
            hint=r"t \cdot 10^d = (m-1)b",
            distractors=[str(value * 10), str(value // 10 if value >= 10 else value + 1),
                         str(m * 10), str(value + m)])


@question_type("math.posn2567_q06", display_name={"th": "กำลังสองรูปแบบ xxaabb"},
               level=LEVEL, topic="กำลังสองสมบูรณ์")
class PatternedSquare(SheetProblem):
    #: middle digit pairs for which the pattern has exactly one square — the
    #: sheet's own 44 is one of them.
    _POOL = [(a, b) for a in range(10) for b in range(10)
             if len(q06.solve(mid_a=a, mid_b=b)) == 1]

    def expr(self, rng: Random):
        a, b = rng.choice(self._POOL)
        (n,) = SOLVE[6](mid_a=a, mid_b=b)
        return MathDraw(
            "", str(n),
            prompt=(f"จงหาจำนวนเต็มบวก n ที่มีสมบัติว่า ในระบบฐานสิบ n² อยู่ใน"
                    f"รูป xx{a}{b}yy เมื่อ x และ y เป็นเลขโดด โดยที่ x > 0"),
            hint=r"11 \mid n^2 \Rightarrow 11 \mid n",
            distractors=[str(n + 11), str(n - 11), str(n // 11), str(n * n)[:3]])


@question_type("math.posn2567_q07", display_name={"th": "ผลบวกของกำลังกลับส่วน"},
               level=LEVEL, topic="เอกลักษณ์ a^k + 1/a^k")
class ReciprocalPowerSum(SheetProblem):
    def expr(self, rng: Random):
        cube_sum = rng.choice(CUBE_SUMS)
        wanted = tuple(sorted(rng.sample([2, 3, 4, 5, 6, 7], rng.randint(3, 4))))
        value = SOLVE[7](cube_sum=cube_sum, wanted=wanted)
        terms = " + ".join(rf"\frac{{1}}{{a^{{{k}}}}}" for k in wanted)
        terms += " + " + " + ".join(rf"a^{{{k}}}" for k in wanted)
        return MathDraw(
            terms, str(value),
            prompt=(f"กำหนดให้ a เป็นจำนวนจริงที่ไม่เท่ากับศูนย์ และ "
                    f"a³ + 1/a³ = {cube_sum}  จงหาค่าของนิพจน์ต่อไปนี้"),
            hint=r"p_k = p_1 p_{k-1} - p_{k-2},\qquad p_1^3 - 3p_1 = a^3 + \tfrac{1}{a^3}",
            distractors=[str(value + 1), str(value - 1), str(2 * value),
                         str(cube_sum * len(wanted))])


@question_type("math.posn2567_q08", display_name={"th": "ตัวประกอบกำลังสองของพหุนามกำลังสี่"},
               level=LEVEL, topic="การหารพหุนาม")
class QuarticFactor(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL08)
        value = SOLVE[8](**p)
        from otk.sheets.posn2567_math.q08 import _mn
        m, n = (int(v) for v in _mn(**p))
        b, q = p["p"], p["q"]
        div = "x^2" + (f" + {b}x" if b > 0 else f" - {abs(b)}x" if b else "") + f" + {q}"
        c1 = p["c1"]
        quart = (rf"x^4 + mx^3 + {p['c2']}x^2 "
                 + (f"+ {c1}x " if c1 > 0 else f"- {abs(c1)}x " if c1 else "")
                 + "+ n")
        return MathDraw(
            rf"{div} \quad\mid\quad {quart}", str(value),
            prompt=("กำหนดให้ m และ n เป็นจำนวนเต็ม  ถ้าพหุนามทางซ้ายเป็น"
                    "ตัวประกอบของพหุนามทางขวา แล้วค่าของ m² + n² เท่ากับเท่าใด"),
            hint=r"x^4 + mx^3 + \dots = (x^2+px+q)(x^2+bx+c)",
            distractors=[str(m + n), str((m + n) ** 2), str(abs(m * n)),
                         str(m * m - n * n if m * m != n * n else value + 2)])


@question_type("math.posn2567_q09", display_name={"th": "สมการกำลังสองที่มีรากบวก"},
               level=LEVEL, topic="สมการกำลังสองและเครื่องหมายราก")
class PositiveRootRange(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL09)
        value = SOLVE[9](**p)
        shift, konst = p["shift"], p["konst"]
        inner = f"a + {shift}" if shift else "a"
        # Interval notation, not a Thai "หรือ": a MathBlock carries notation
        # only, and the union is exactly what the wrong answer looks like.
        other = frac_answer_tex(1 - 2 * shift - value)   # the discriminant's other root
        low = frac_answer_tex(value)
        return MathDraw(
            rf"x^2 + 2({inner})x + a + {konst} = 0",
            rf"(-\infty, {low}]",
            prompt=("จงหาเซตของจำนวนจริง a ทั้งหมดที่ทำให้สมการต่อไปนี้ "
                    "มีคำตอบเป็นจำนวนจริงบวกอย่างน้อย 1 คำตอบ"),
            hint=r"D \ge 0,\quad \text{sum} = -2(a+s),\quad \text{product} = a+k",
            # Solving D ≥ 0 and stopping there gives the union — both roots are
            # real on the upper piece, but both are negative. That is the item.
            distractors=[rf"(-\infty, {low}] \cup [{other}, \infty)",
                         rf"[{low}, \infty)",
                         rf"(-\infty, {low})",
                         rf"(-\infty, {frac_answer_tex(value + 1)}]"])


@question_type("math.posn2567_q10", display_name={"th": "ค่าของ AC²/((AB)(AE))"},
               level=LEVEL, topic="เรขาคณิต: สี่เหลี่ยมขนมเปียกปูน")
class RhombusFootRatio(SheetProblem):
    def expr(self, rng: Random, side_lo: int = 2, side_hi: int = 15):
        side = rng.randint(side_lo, side_hi)
        # The angle is drawn in the sheet's figure at one fixed value, so the
        # prompt must not name a different one — and it never needs to: the
        # ratio is the same for every rhombus, which is the point of the item.
        angle = rng.choice([30, 45, 60, 70, 80, 100, 110, 120, 135, 150])
        value = SOLVE[10](side=side, angle_deg=angle)
        return MathDraw(
            r"\frac{AC^2}{(AB)(AE)}", frac_answer_tex(value),
            prompt=(f"ให้ ABCD เป็นรูปสี่เหลี่ยมขนมเปียกปูนที่มีด้านยาว "
                    f"{side} หน่วย และ CE ตั้งฉากกับ BE ดังรูป  "
                    f"จงหาค่าของนิพจน์ต่อไปนี้"),
            hint=r"AC^2 = 2s^2(1+\cos\alpha),\qquad AE = s(1+\cos\alpha)",
            distractors=["1", "4", frac_answer_tex(Fraction(1, 2)), str(side)])


@question_type("math.posn2567_q11", display_name={"th": "พื้นที่สามเหลี่ยมในสี่เหลี่ยมจัตุรัส"},
               level=LEVEL, topic="เรขาคณิต: สี่เหลี่ยมจัตุรัส")
class SquareInscribedTriangle(SheetProblem):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def expr(self, rng: Random, bf_lo: int = 2, bf_hi: int = 20):
        bf = rng.randint(bf_lo, bf_hi)
        # The square's side is never stated — the area depends only on BF, which
        # is the point of the item — so any side larger than BF will do for the
        # solver's own well-posedness guard.
        value = SOLVE[11](bf=bf, side=3 * bf)
        sq = Fraction(bf) ** 2
        return MathDraw(
            "", frac_answer_tex(value),
            prompt=(f"จากรูป ABCD เป็นรูปสี่เหลี่ยมจัตุรัส โดยมี EG ขนานกับ AB "
                    f"และ BF ตั้งฉากกับ FC ที่จุด F  ถ้า BF = {bf} หน่วย "
                    f"แล้วพื้นที่ของรูปสามเหลี่ยม AEG เท่ากับกี่ตารางหน่วย"),
            hint=r"\angle BFC = 90^\circ \Rightarrow (s-f)^2 = y(s-y),\quad "
                 r"BF^2 = s(s-y)",
            distractors=[frac_answer_tex(sq), frac_answer_tex(sq / 4),
                         frac_answer_tex(2 * sq), frac_answer_tex(sq / 8)])


@question_type("math.posn2567_q12", display_name={"th": "มุมในวงกลมสองวงที่ตัดกัน"},
               level=LEVEL, topic="เรขาคณิต: วงกลมสองวงตัดกัน")
class TwoCirclesAngleSum(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL12)
        value = SOLVE[12](**p)
        u, v = p["ode_deg"], p["obe_deg"]
        return MathDraw(
            "", f"{frac_answer_tex(value)}^\\circ",
            prompt=(f"จากรูป วงกลมสองวงตัดกันที่จุด A และจุด B โดยมีจุด O เป็น"
                    f"จุดศูนย์กลางของวงกลมวงใหญ่  CD เป็นส่วนของเส้นตรงที่ตัด"
                    f"วงกลมทั้งสองที่จุด C, A และ D โดยที่ CA เป็นเส้นผ่าน"
                    f"ศูนย์กลางของวงกลมวงเล็ก  CE เป็นส่วนของเส้นตรงที่ตัดวงกลม"
                    f"ทั้งสองที่จุด C, B และ E  ถ้า ∠ODE = {u}° และ ∠OBE = {v}° "
                    f"แล้ว ∠ACB + ∠ADO เท่ากับกี่องศา"),
            hint=r"\angle ABC = 90^\circ \Rightarrow \angle ABE = 90^\circ "
                 r"\Rightarrow \angle ADE = 90^\circ",
            # The first is the two given angles used the other way round; the
            # next two are each half of the sum, answered alone.
            distractors=[f"{180 - u - 2 * v}^\\circ", f"{90 - u - v}^\\circ",
                         f"{90 - u}^\\circ", f"{180 - 2 * u - 2 * v}^\\circ"])


@question_type("math.posn2567_q13", display_name={"th": "พื้นที่คางหมูที่เส้นทแยงมุมตั้งฉาก"},
               level=LEVEL, topic="เรขาคณิต: สี่เหลี่ยมคางหมู")
class PerpendicularDiagonalTrapezoid(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL13)
        value = SOLVE[13](**p)
        h, d = p["height"], p["diagonal"]
        leg = math.isqrt(d * d - h * h)             # the other diagonal's cosine leg
        return MathDraw(
            "", frac_answer_tex(value),
            prompt=(f"รูปสี่เหลี่ยมคางหมูรูปหนึ่งมีส่วนสูงยาว {h} หน่วย โดยที่"
                    f"เส้นทแยงมุมของรูปสี่เหลี่ยมคางหมูตั้งฉากกัน ถ้าเส้นทแยงมุม"
                    f"เส้นหนึ่งยาว {d} หน่วย จงหาพื้นที่ของรูปสี่เหลี่ยมคางหมูนี้ "
                    f"(เขียนคำตอบเป็นเศษส่วนอย่างต่ำ)"),
            hint=r"\sin\theta = \frac{h}{d_1},\qquad d_2\cos\theta = h,"
                 r"\qquad \text{area} = \tfrac{1}{2}d_1 d_2",
            distractors=[frac_answer_tex(Fraction(h * d, 2)),
                         frac_answer_tex(2 * value),
                         frac_answer_tex(Fraction(d * leg, 2)),
                         frac_answer_tex(Fraction(h * leg, 2))])


@question_type("math.posn2567_q14", display_name={"th": "อัตราส่วนพื้นที่วงกลมเล็กต่อวงกลมใหญ่"},
               level=LEVEL, topic="เรขาคณิต: วงกลมสัมผัสกัน")
class TangentCirclesAreaRatio(SheetProblem):
    def expr(self, rng: Random):
        # The sheet's own picture draws the two big circles equal, so it may only
        # be shown when the draw keeps them equal; the rest hide it and say the
        # two radii out loud instead.
        equal = rng.random() < 0.4
        p = {"r_low": 1, "r_up": 1} if equal else rng.choice(POOL14)
        value = SOLVE[14](**p)
        lo, up = p["r_low"], p["r_up"]
        if equal:
            said = ("วงกลมใหญ่สองวงรัศมีเท่ากันและสัมผัสกันภายนอก")
        else:
            said = (f"วงกลมใหญ่สองวงสัมผัสกันภายนอก โดยวงล่างมีรัศมี {lo} หน่วย "
                    f"และวงบนมีรัศมี {up} หน่วย")
        return MathDraw(
            "", frac_answer_tex(value),
            prompt=(f"จากรูป {said} รูปสามเหลี่ยมหน้าจั่วมีจุดยอดจุดหนึ่งอยู่บน"
                    f"วงกลมใหญ่วงบน และด้านทั้งสามของรูปสามเหลี่ยมเป็นเส้นสัมผัส"
                    f"วงกลมใหญ่วงล่าง วงกลมเล็กสัมผัสภายในกับวงกลมใหญ่วงบน และ"
                    f"สัมผัสคอร์ด ณ จุดกึ่งกลางของคอร์ด  จงหาอัตราส่วนของพื้นที่"
                    f"วงกลมเล็กต่อพื้นที่วงกลมใหญ่วงบน"),
            figure=None if not equal else "",
            hint=r"d = \frac{Rr}{r+2R},\qquad \rho = \tfrac{1}{2}(R - d)",
            distractors=[frac_answer_tex(Fraction(up, lo + 2 * up)),
                         frac_answer_tex(Fraction(up, lo + up) ** 2),
                         frac_answer_tex(Fraction(2 * up, lo + 2 * up) ** 2),
                         frac_answer_tex(Fraction(1, 2))])


@question_type("math.posn2567_q15", display_name={"th": "มุมสัมผัส–คอร์ดกับเส้นผ่านศูนย์กลาง"},
               level=LEVEL, topic="เรขาคณิต: เส้นสัมผัสวงกลม")
class TangentChordAngle(SheetProblem):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def expr(self, rng: Random):
        k = rng.choice(MULTIPLIERS)
        value = SOLVE[15](mult=k)
        return MathDraw(
            "", f"{frac_answer_tex(value)}^\\circ",
            prompt=(f"จากรูป AB เป็นเส้นผ่านศูนย์กลางของวงกลม เส้นตรง DE สัมผัส"
                    f"วงกลมที่จุด D  BF เป็นส่วนของเส้นตรงที่ลากต่อจาก AB ออกไป"
                    f"ทางจุด B และตัดเส้นตรง DE ที่จุด C โดยที่จุด D อยู่ระหว่าง"
                    f"จุด C และจุด E  ถ้า ∠DCF = {k}(∠ADE − ∠BAD) "
                    f"แล้ว ∠ADE มีขนาดกี่องศา"),
            hint=r"\theta + \alpha = 90^\circ,\qquad "
                 r"\angle DCF = 180^\circ - (\theta - \alpha)",
            # The first is ∠BAD, answered instead of ∠ADE; the last divides by k
            # rather than by k+1, forgetting the straight angle at C.
            distractors=[f"{frac_answer_tex(90 - value)}^\\circ",
                         f"{frac_answer_tex(value - 45)}^\\circ",
                         f"{frac_answer_tex(180 - value)}^\\circ",
                         f"{frac_answer_tex(45 + Fraction(90, k))}^\\circ"])


@question_type("math.posn2567_q16", display_name={"th": "มุมในรูปหลายเหลี่ยมปกติ"},
               level=LEVEL, topic="เรขาคณิต: รูปหลายเหลี่ยมปกติ")
class RegularPolygonRotationAngle(SheetProblem):
    def expr(self, rng: Random):
        n = rng.choice(POLYGONS)
        value = SOLVE[16](sides=n)
        deg = f"{frac_answer_tex(value)}^\\circ"
        # The sheet draws a hexagon and letters it ABCDEF, so the crop may only
        # be shown at n = 6; other draws name five consecutive vertices instead.
        if n == 6:
            said = "จากรูป ABCDEF เป็นรูปหกเหลี่ยมด้านเท่ามุมเท่า"
        else:
            said = (f"ให้ A, B, C, D และ E เป็นจุดยอดห้าจุดที่อยู่ติดกันตามลำดับ"
                    f"ของรูป {n} เหลี่ยมด้านเท่ามุมเท่ารูปหนึ่ง")
        return MathDraw(
            "", deg,
            prompt=(f"{said}  ส่วนของเส้นตรง BN ตัด AC ที่จุด M และพบกับ CE "
                    f"ที่จุด N  ถ้า AM = CN แล้วขนาดของ ∠BND เท่ากับกี่องศา"),
            figure=None if n != 6 else "",
            hint=r"\rho:\ A \mapsto C,\ B \mapsto D,\ C \mapsto E "
                 r"\Rightarrow \overline{MB} \mapsto \overline{ND}",
            # An angle of a plane figure, so anything at or past 180° would give
            # itself away; those candidates are dropped rather than offered.
            distractors=_distinct(deg, [
                f"{frac_answer_tex(a)}^\\circ" for a in
                (Fraction(360, n), Fraction(1440, n), 180 - value,
                 180 - Fraction(360, n), Fraction(90), Fraction(60))
                if 0 < a < 180]))


@question_type("math.posn2567_q17", display_name={"th": "ปริมาตรของ cuboctahedron"},
               level=LEVEL, topic="เรขาคณิตสามมิติ")
class CuboctahedronVolume(SheetProblem):
    def expr(self, rng: Random, edge_lo: int = 1, edge_hi: int = 12):
        a = rng.randint(edge_lo, edge_hi)
        coef = SOLVE[17](edge=a)                    # V = coef·√2
        cube = Fraction(2) * a ** 3                 # the cube it was cut from
        return MathDraw(
            "", _surd_tex(coef, 2),
            prompt=(f"นำลูกบาศก์ลูกหนึ่งมาตัดมุมของลูกบาศก์ทั้งแปดมุมออกด้วย"
                    f"ระนาบให้ผ่านขอบ 3 ขอบของลูกบาศก์ที่ประกอบเป็นมุมแต่ละมุม "
                    f"จะได้รูปทรงสิบสี่หน้าที่เรียกว่า cuboctahedron ซึ่งมีหน้า 6 "
                    f"หน้าเป็นรูปสี่เหลี่ยมจัตุรัส อีก 8 หน้าเป็นรูปสามเหลี่ยม"
                    f"ด้านเท่า และมีขอบ 24 ขอบ ดังรูป  ถ้าขอบแต่ละขอบของรูปทรง"
                    f"สิบสี่หน้ามีความยาวเท่ากับ {a} หน่วย แล้วรูปทรงนี้มีปริมาตร"
                    f"เท่ากับเท่าใด"),
            hint=r"V = (a\sqrt{2})^3 - 8\cdot\tfrac{1}{6}"
                 r"\left(\tfrac{a\sqrt{2}}{2}\right)^3",
            # The cube itself, the corners alone, and the answer with the √2
            # dropped — the three ways to stop one step early.
            distractors=_distinct(_surd_tex(coef, 2), [
                _surd_tex(cube, 2), _surd_tex(coef, 1),
                _surd_tex(cube - coef, 2), _surd_tex(2 * coef, 2)]))


@question_type("math.posn2567_q18", display_name={"th": "รัศมีของวงกลมที่แทรกระหว่างสองวง"},
               level=LEVEL, topic="เรขาคณิต: วงกลมสัมผัสกัน")
class InsertedEqualCircles(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(RADII_PAIRS)
        ra, rb = p["r_a"], p["r_b"]
        m, n, d = q18.exact_form(**p)
        root = math.isqrt(ra), math.isqrt(rb)
        # r₀ is the single circle that fits in the gap touching both and the
        # line — the answer to the question one condition simpler than this one.
        single = Fraction(root[0] * root[1], root[0] + root[1]) ** 2
        return MathDraw(
            "", _pm_surd(m, -n, d, 2),
            prompt=(f"วงกลม A และวงกลม B มีรัศมีเป็น {ra} หน่วย และ {rb} หน่วย"
                    f"ตามลำดับ วงกลมทั้งสองสัมผัสกันภายนอกและสัมผัสกับเส้นตรง L  "
                    f"สร้างวงกลมเล็กสองวงรัศมีเท่ากันเป็น r หน่วย ซึ่งต่างสัมผัส"
                    f"กันภายนอก และสัมผัสกับเส้นตรง L โดยวงหนึ่งสัมผัสภายนอกกับ"
                    f"วงกลม A อีกวงหนึ่งสัมผัสภายนอกกับวงกลม B  จงหาค่าของ r"),
            hint=r"2\sqrt{R_A r} + 2r + 2\sqrt{R_B r} = 2\sqrt{R_A R_B}",
            distractors=_distinct(_pm_surd(m, -n, d, 2), [
                frac_answer_tex(single), _pm_surd(m, n, d, 2),
                _pm_surd(m, -n, d, 4), _pm_surd(m, -n, d, 1)]))


@question_type("math.posn2567_q19", display_name={"th": "จำนวนสับเซตที่มีผลบวกกำหนด"},
               level=LEVEL, topic="การนับและการจัดหมู่")
class SubsetsWithGivenSum(SheetProblem):
    def expr(self, rng: Random, top_lo: int = 40, top_hi: int = 80):
        top = rng.randint(top_lo, top_hi)
        # The target sits just below the total, so the item is the complement
        # trick and not a 2000-column table.
        rest = rng.randint(3, 12)
        target = top * (top + 1) // 2 - rest
        value = SOLVE[19](top=top, target=target)
        return MathDraw(
            "", str(value),
            prompt=(f"กำหนดให้ A = {{1, 2, ..., {top}}}  จงหาจำนวนของสับเซต H "
                    f"ทั้งหมดของเซต A โดยที่ผลบวกของสมาชิกทั้งหมดในเซต H "
                    f"มีค่าเท่ากับ {target}"),
            hint=r"\left|\{H : \Sigma H = t\}\right| = "
                 r"\left|\{H : \Sigma H = \Sigma A - t\}\right|",
            distractors=_distinct(str(value), [
                str(_partitions(rest)), str(value + 1), str(value - 1),
                str(rest), str(2 * value)]))


@question_type("math.posn2567_q20", display_name={"th": "จำนวนสี่สิ่งอันดับที่เรียงตามเงื่อนไข"},
               level=LEVEL, topic="การนับเชิงการจัด")
class OrderedQuadruples(SheetProblem):
    def expr(self, rng: Random):
        top = rng.choice([9] * 3 + [5, 6, 7, 8, 11, 12, 13, 15])
        value = SOLVE[20](top=top)
        said = ("a, b, c และ d เป็นเลขโดด" if top == 9 else
                f"a, b, c และ d เป็นจำนวนเต็มตั้งแต่ 0 ถึง {top}")
        return MathDraw(
            "a < b \\le c < d", str(value),
            prompt=(f"จงหาจำนวนของสี่สิ่งอันดับ (a, b, c, d) ทั้งหมดที่ {said} "
                    f"ซึ่งสอดคล้องกับเงื่อนไขต่อไปนี้"),
            hint=r"(a,b,c,d) \mapsto (a,\,b,\,c+1,\,d+2)",
            # Reading every relation as strict, or every one as loose.
            distractors=_distinct(str(value), [
                str(math.comb(top + 1, 4)), str(math.comb(top + 4, 4)),
                str(math.comb(top + 2, 3)), str(math.comb(top + 2, 5))]))


@question_type("math.posn2567_q21", display_name={"th": "จำนวนลูกบอลจากความน่าจะเป็นสีเดียวกัน"},
               level=LEVEL, topic="ความน่าจะเป็น")
class BallsFromMatchProbability(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL21)
        value = SOLVE[21](**p)
        g1, b1, g2 = p["g1"], p["b1"], p["g2"]
        prob = Fraction(p["p_num"], p["p_den"])
        return MathDraw(
            "", str(value),
            prompt=(f"มีกล่อง 2 ใบ กล่องใบที่หนึ่งบรรจุลูกบอลสีเขียว {g1} ลูก "
                    f"และลูกบอลสีน้ำเงิน {b1} ลูก กล่องใบที่สองบรรจุลูกบอล"
                    f"สีเขียว {g2} ลูก และลูกบอลสีน้ำเงินอย่างน้อยหนึ่งลูก  "
                    f"สุ่มหยิบลูกบอลออกจากกล่อง กล่องละหนึ่งลูก ถ้าความน่าจะเป็น"
                    f"ที่ได้ลูกบอลทั้งสองลูกมีสีเดียวกันเท่ากับ "
                    f"{prob.numerator}/{prob.denominator} แล้วกล่องใบที่สอง"
                    f"มีลูกบอลสีน้ำเงินทั้งหมดกี่ลูก"),
            hint=r"\frac{g_1g_2 + b_1b}{(g_1+b_1)(g_2+b)} = p",
            distractors=_distinct(str(value), [
                str(value + 1), str(value - 1), str(g1 + b1),
                str(value + g2), str(2 * value)]))


@question_type("math.posn2567_q22", display_name={"th": "ผลบวกของตัวส่วนที่เป็นไปได้"},
               level=LEVEL, topic="ความน่าจะเป็น")
class PossibleDenominatorSum(SheetProblem):
    def expr(self, rng: Random, m_lo: int = 6, m_hi: int = 40):
        m = rng.randint(m_lo, m_hi)
        purple = rng.randint(1, m - 1)
        value = SOLVE[22](purple=purple, green=m - purple)
        divisors = [k for k in range(1, m + 1) if m % k == 0]
        return MathDraw(
            "", str(value),
            prompt=(f"กล่องใบหนึ่งบรรจุลูกแก้วสีม่วง {purple} ลูก ลูกแก้วสีเขียว "
                    f"{m - purple} ลูก และลูกแก้วสีส้มจำนวนหนึ่ง  สุ่มหยิบลูกแก้ว "
                    f"1 ลูกจากกล่องใบนี้  ถ้าความน่าจะเป็นที่ได้ลูกแก้วสีส้ม"
                    f"เท่ากับ 1/a เมื่อ a เป็นจำนวนเต็มบวก แล้วผลบวกของ a "
                    f"ที่เป็นไปได้ทั้งหมดเท่ากับเท่าใด"),
            hint=r"\frac{k}{m+k} = \frac{1}{a} \iff a = 1 + \frac{m}{k}",
            # σ(m) alone forgets the +1 on each divisor; d(m) keeps only those.
            distractors=_distinct(str(value), [
                str(sum(divisors)), str(len(divisors)), str(m + 1),
                str(value - 1), str(value + 1)]))


@question_type("math.posn2567_q23", display_name={"th": "ความน่าจะเป็นที่ผลคูณหารด้วย 10 ลงตัว"},
               level=LEVEL, topic="ความน่าจะเป็น")
class ProductDivisibleByTen(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL23)
        value = SOLVE[23](**p)
        top, draws = p["top"], p["draws"]
        # Treating "some multiple of 5" and "some even" as independent is the
        # mistake the item exists to catch, so it leads the distractors.
        five = 1 - Fraction(top - top // 5, top) ** draws
        even = 1 - Fraction(top - top // 2, top) ** draws
        cards = ", ".join(str(i) for i in range(1, min(top, 5) + 1)) + f", ..., {top}"
        return MathDraw(
            "", frac_answer_tex(value),
            prompt=(f"กล่องใบหนึ่งบรรจุบัตรตัวเลขอยู่ {top} ใบ ซึ่งมีหมายเลข "
                    f"{cards} กำกับบนบัตร บัตรละ 1 หมายเลข  สุ่มหยิบบัตรจาก"
                    f"กล่องใบนี้ {draws} ใบ โดยหยิบทีละ 1 ใบแล้วใส่คืนก่อนหยิบ"
                    f"บัตรครั้งต่อไป  จงหาความน่าจะเป็นของเหตุการณ์ที่ผลคูณของ"
                    f"หมายเลขบนหน้าบัตรทั้ง {draws} ใบเป็นจำนวนที่หารด้วย 10 "
                    f"ลงตัว (เขียนคำตอบเป็นเศษส่วนอย่างต่ำ)"),
            hint=r"P = 1 - P(\text{no }5) - P(\text{no even}) + P(\text{neither})",
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(five * even), frac_answer_tex(five),
                frac_answer_tex(even), frac_answer_tex(1 - value)]))


@question_type("math.posn2567_q24", display_name={"th": "จำนวนสี่เหลี่ยมจากจุดบนครึ่งวงกลม"},
               level=LEVEL, topic="การนับและการจัดหมู่")
class SemicircleQuadrilaterals(SheetProblem):
    def expr(self, rng: Random):
        green = rng.randint(4, 8)
        red = rng.randint(6, 30)
        value = SOLVE[24](red=red, green=green)
        return MathDraw(
            "", str(value),
            prompt=(f"กำหนดจุด {red + green} จุด เป็นจุดสีแดง {red} จุด และ"
                    f"จุดสีเขียว {green} จุด บนเส้นรอบรูปของรูปครึ่งวงกลมรูปหนึ่ง "
                    f"โดยมีจุดสีแดงเท่านั้นที่อยู่บนเส้นผ่านศูนย์กลางของวงกลม  "
                    f"ต้องการสร้างรูปสี่เหลี่ยมโดยใช้จุด 4 จุดจากจุดเหล่านี้"
                    f"เป็นจุดยอด จะได้รูปสี่เหลี่ยมที่แตกต่างกันทั้งหมดกี่รูป"),
            hint=r"\binom{g}{4} + \binom{g}{3}r + \binom{g}{2}\binom{r}{2}",
            # The first ignores collinearity entirely; the second adds back the
            # 1-green-3-red case that three collinear points forbid.
            distractors=_distinct(str(value), [
                str(math.comb(red + green, 4)),
                str(value + green * math.comb(red, 3)),
                str(math.comb(green, 2) * math.comb(red, 2)),
                str(value - 1)]))


@question_type("math.posn2567_q25", display_name={"th": "ผลต่างของจำนวนคำตอบบวกกับไม่เป็นลบ"},
               level=LEVEL, topic="สมการไดโอแฟนไทน์เชิงเส้น")
class DiophantineSolutionGap(SheetProblem):
    def expr(self, rng: Random):
        a, b, c = sorted(rng.sample([1, 1, 2, 2, 3, 3, 4, 5], 3))
        total = rng.randint(a + b + c + 2, 40)
        value = SOLVE[25](a=a, b=b, c=c, total=total)
        both = q25._nonneg(a, b, c, total)
        terms = " + ".join(f"{'' if k == 1 else k}{v}"
                           for k, v in ((a, "x"), (b, "y"), (c, "z")))
        return MathDraw(
            rf"{terms} = {total}", str(value),
            prompt=("ให้ A เป็นเซตของสามสิ่งอันดับ (x, y, z) ของจำนวนเต็มบวก"
                    "ทั้งหมดที่สอดคล้องกับสมการต่อไปนี้ และ B เป็นเซตของ"
                    "สามสิ่งอันดับ (x, y, z) ของจำนวนเต็มที่ไม่เป็นลบทั้งหมดที่"
                    "สอดคล้องกับสมการเดียวกัน  จงหาว่าเซต A และเซต B "
                    "มีจำนวนสมาชิกต่างกันอยู่เท่าใด"),
            hint=r"|A| = \#\{\text{non-negative solutions of } "
                 r"ax+by+cz = N-(a+b+c)\}",
            distractors=_distinct(str(value), [
                str(both), str(both - value), str(both + value),
                str(value + 1)]))


@question_type("math.posn2567_q26", display_name={"th": "ค่ามากสุดบวกค่าน้อยสุดของผลบวกระยะทาง"},
               level=LEVEL, topic="ค่าสัมบูรณ์และค่าสุดขีด")
class AbsoluteSumRange(SheetProblem):
    def expr(self, rng: Random):
        pts = tuple(sorted(rng.sample(range(-6, 13), 3)))
        lo = rng.randint(-10, pts[0])
        hi = rng.randint(pts[2], pts[2] + 12)
        value = SOLVE[26](points=pts, lo=lo, hi=hi)
        from otk.sheets.posn2567_math.q26 import _f
        at_lo, at_hi = int(_f(lo, pts)), int(_f(hi, pts))
        best = int(_f(pts[1], pts))                  # the median value
        terms = " + ".join(
            r"\left|x\right|" if p == 0 else
            rf"\left|x {'-' if p > 0 else '+'} {abs(p)}\right|" for p in pts)
        return MathDraw(
            rf"X = \{{\, {terms} \;:\; {lo} \le x \le {hi} \,\}}", str(value),
            prompt=("กำหนดให้ X เป็นเซตต่อไปนี้  ถ้า a เป็นสมาชิกในเซต X "
                    "ที่มีค่ามากที่สุด และ b เป็นสมาชิกในเซต X ที่มีค่าน้อยที่สุด "
                    "แล้วค่าของ a + b เท่ากับเท่าใด"),
            hint=r"\sum|x - p_i| \text{ is convex: min at the median, max at an end}",
            # Taking the nearer endpoint for the maximum is the whole trap.
            distractors=_distinct(str(value), [
                str(min(at_lo, at_hi) + best), str(max(at_lo, at_hi) - best),
                str(at_lo + at_hi), str(2 * best), str(value + 1)]))


@question_type("math.posn2567_q27", display_name={"th": "จำนวน n ที่ทำให้รากเป็นตรรกยะ"},
               level=LEVEL, topic="รากของพหุนาม")
class RationalRootCount(SheetProblem):
    def expr(self, rng: Random, exp_lo: int = 6, exp_hi: int = 30):
        ep, eq = rng.randint(exp_lo, exp_hi), rng.randint(exp_lo, exp_hi)
        value = SOLVE[27](ep=ep, eq=eq)
        pairs = (ep + 1) * (eq + 1)
        return MathDraw(
            rf"p^{{{ep}}}x^2 + nx + q^{{{eq}}} = 0", str(value),
            prompt=("ให้ p และ q เป็นจำนวนเฉพาะที่แตกต่างกัน  ให้ A เป็นเซตของ"
                    "จำนวนเต็มบวก n ทั้งหมดที่ทำให้สมการต่อไปนี้มีคำตอบทุกคำตอบ"
                    "เป็นจำนวนตรรกยะ  จงหาจำนวนสมาชิกของเซต A"),
            hint=r"p^e x^2 + nx + q^f = (p^i x + q^{f-j})(p^{e-i}x + q^{j})",
            # Forgetting that swapping the two factors repeats n doubles the count.
            distractors=_distinct(str(value), [
                str(pairs), str(pairs // 2), str(value - 1), str(value + 1)]))


@question_type("math.posn2567_q28", display_name={"th": "จำนวนสับเซตของเพาเวอร์เซตที่กำหนดผลต่าง"},
               level=LEVEL, topic="เพาเวอร์เซตและการนับสับเซต")
class PowerSetDifference(SheetProblem):
    def expr(self, rng: Random):
        scalars = tuple(sorted(rng.sample([1, 3, 5, 7, 9], 3)))
        pool = [(scalars[0],), (scalars[1],), (scalars[2],),
                scalars[:2], scalars[1:], (scalars[0], scalars[2])]
        sets = tuple(rng.sample(pool, rng.randint(3, 4)))
        # Every set-valued element is built from the scalars, so all of them lie
        # in P(A): |A ∩ P(A)| = len(sets), and B can hold between 1 and that many
        # elements of A — which is what keeps `missing` in range and the count > 0.
        size = len(scalars) + len(sets)
        missing = rng.randint(len(scalars), size - 1)
        p = {"scalars": scalars, "sets": sets, "missing": missing}
        value = SOLVE[28](**p)

        def show(x) -> str:
            return "\\{" + ", ".join(str(v) for v in x) + "\\}"

        listing = ", ".join([str(v) for v in scalars] + [show(s) for s in sets])
        return MathDraw(
            rf"A = \{{{listing}\}}", _pow2_tex(value),
            prompt=(f"ให้ S = {{ B : B ⊆ P(A) และ A − B มีสมาชิก {missing} ตัว }} "
                    f"เมื่อ P(A) เป็นเพาเวอร์เซตของเซต A  "
                    f"จงหาจำนวนสมาชิกของเซต S"),
            hint=r"B \subseteq P(A),\ \text{so } A \cap B \subseteq A \cap P(A)",
            # Counting every element of A as a possible member of B is the miss.
            distractors=_distinct(_pow2_tex(value), [
                _pow2_tex(math.comb(size, size - missing) * 2 ** (2 ** size
                                                                  - len(sets))),
                _pow2_tex(value * 2), _pow2_tex(value // 2),
                _pow2_tex(2 ** (2 ** size))]))


@question_type("math.posn2567_q29", display_name={"th": "ตารางคะแนนฟุตบอลพบกันหมด"},
               level=LEVEL, topic="การให้เหตุผลเชิงตรรกะ")
class RoundRobinPoints(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL29)
        value = SOLVE[29](**p)
        table = next(iter(q29._tables_by_ac(1, 2, 4, 0)[(p["pts_a"], p["pts_c"])]))
        return MathDraw(
            "", str(value),
            prompt=(f"โรงเรียนแห่งหนึ่งจัดการแข่งขันฟุตบอลระหว่างห้อง A, B, C, D "
                    f"และ E แบบพบกันหมด โดยทีมที่ชนะได้ 3 แต้ม เสมอได้ 1 แต้ม "
                    f"และแพ้ได้ 0 แต้ม  จากผลการแข่งขันพบว่า (1) ห้อง A ได้แต้ม"
                    f"รวม {p['pts_a']} แต้ม (2) ห้อง B ชนะในการแข่งขันกับห้อง C "
                    f"(3) ห้อง C ได้แต้มรวม {p['pts_c']} แต้ม (4) ห้อง D มีแต้ม"
                    f"รวมมากกว่าทุกห้อง (5) ห้อง E มีแต้มรวมน้อยกว่าทุกห้อง "
                    f"(6) ห้อง E เสมอในการแข่งขันกับห้อง A  "
                    f"ห้อง B ได้แต้มทั้งหมดกี่แต้ม"),
            hint=r"3\,\text{wins} + 1\,\text{draw},\quad "
                 r"\textstyle\sum \text{points} = 3\cdot 10 - \#\text{draws}",
            # D's and E's totals are the two other numbers on the table.
            distractors=_distinct(str(value), [
                str(table[3]), str(table[4]), str(value - 3), str(value + 3)]))


@question_type("math.posn2567_q30", display_name={"th": "ปริศนานามสกุลกับฟาร์ม"},
               level=LEVEL, topic="ปริศนาเชิงตรรกะ")
class FarmSurnamePuzzle(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL30)
        table = SOLVE[30](**p)
        who = rng.randrange(4)
        surname, farm = table[who]

        # The answer is a pair of Thai words, and a MathBlock carries notation
        # only — so the prompt numbers the surnames and the farms and the choices
        # are the resulting code.
        def pair(s: int, f: int) -> str:
            return rf"({s + 1},\ {f + 1})"

        codes = ("  รหัสนามสกุล: "
                 + ", ".join(f"{n} = {i + 1}" for i, n in enumerate(q30.SURNAMES))
                 + "  และรหัสฟาร์ม: "
                 + ", ".join(f"ฟาร์ม{n} = {i + 1}" for i, n in enumerate(q30.FARMS)))
        others = [pair(s, f) for i, (s, f) in enumerate(table) if i != who]
        return MathDraw(
            "", pair(surname, farm),
            prompt=(f"นายเอ นายบี นายซี และนายดี ทำงานอยู่ในฟาร์มวัว ฟาร์มกุ้ง "
                    f"ฟาร์มไก่ และฟาร์มหมู นามสกุลของคนทั้งสี่โดยไม่เรียงตามชื่อ"
                    f"คือ เบิกบาน ปันใจ มานะ และลือชัย และมีข้อมูลเพิ่มเติมดังนี้ "
                    f"(1) แต่ละคนทำงานอยู่คนละฟาร์ม (2) คนที่นามสกุลมานะ "
                    f"ไม่ได้ทำงานในฟาร์มกุ้งหรือฟาร์มไก่ (3) "
                    f"{q30.PEOPLE[p['pig_person']]}ทำงานในฟาร์มหมู (4) เบิกบาน"
                    f"เป็นนามสกุลของ{q30.PEOPLE[p['boekban_person']]} (5) "
                    f"นามสกุลของ{q30.PEOPLE[p['pig_person']]}ไม่ใช่ลือชัยหรือ"
                    f"มานะ (6) มานะไม่ใช่นามสกุลของ"
                    f"{q30.PEOPLE[p['not_mana_person']]} (7) คนที่นามสกุลลือชัย "
                    f"ไม่ได้ทำงานในฟาร์มกุ้ง  จงหาว่า{q30.PEOPLE[who]}"
                    f"มีนามสกุลอะไรและทำงานอยู่ในฟาร์มอะไร "
                    f"โดยตอบเป็นคู่อันดับ (รหัสนามสกุล, รหัสฟาร์ม) เมื่อ{codes}"),
            hint=r"4! \cdot 4! = 576",
            # The other three people's answers, plus one crossed pairing.
            distractors=_distinct(pair(surname, farm), [
                *others, pair(surname, (farm + 1) % 4)]))
