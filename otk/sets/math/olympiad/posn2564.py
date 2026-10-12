"""อัตราส่วนจากสมการกำลังสอง

คณิตศาสตร์ · โอลิมปิก (สอวน.) · สอวน.
Indicators: —

Sets moved here from: posn2564.
"""

from __future__ import annotations

import math
from fractions import Fraction
from functools import lru_cache
from math import gcd, isqrt
from random import Random

from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sheets import figure_attachments
from otk.sheets.posn2564_math import (
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


SHEET = "สอวน. ค่าย 1 (2564)"


SHEET_ID = "posn2564_math"


_MODULES = [q01, q02, q03, q04, q05, q06, q07, q08, q09, q10,
            q11, q12, q13, q14, q15, q16, q17, q18, q19, q20,
            q21, q22, q23, q24, q25, q26, q27, q28, q29, q30]


SOLVE = {n: lru_cache(maxsize=4096)(mod.solve)
         for n, mod in enumerate(_MODULES, start=1)}


FIGURES = figure_attachments(SHEET_ID)


class SheetProblem(WordProblem):
    """A โจทย์ from the 2564 sheet: Thai prompt, exact TeX answer."""

    sheet = SHEET
    sheet_id = SHEET_ID

    def default_figure(self) -> tuple[str, str]:
        return FIGURES.get(self.key, ("", ""))


def _distinct(value: str, candidates: list[str], want: int = 4) -> list[str]:
    """The first ``want`` candidates that differ from the answer and each other.

    Hand-picked distractors are near misses by construction, so at particular
    constants one of them *is* the answer; offer more than four and filter.
    """
    out: list[str] = []
    for c in candidates:
        if c != value and c not in out:
            out.append(c)
        if len(out) == want:
            break
    return out


def _num(value) -> str:
    """An int or Fraction as TeX, without the mixed-number tail."""
    return frac_tex(Fraction(value))


def _surd(square) -> str:
    """√(square) for a non-negative rational, simplified: ``\\frac{3\\sqrt{2}}{4}``."""
    square = Fraction(square)
    num, den = square.numerator, square.denominator
    inside = num * den                     # √(n/d) = √(n·d)/d
    out, rad = 1, inside
    for f in range(2, isqrt(inside) + 1):
        while rad % (f * f) == 0:
            rad //= f * f
            out *= f
    g = gcd(out, den)
    out, den = out // g, den // g
    head = ("" if out == 1 and rad != 1 else str(out)) + (rf"\sqrt{{{rad}}}" if rad != 1 else "")
    return head if den == 1 else rf"\frac{{{head}}}{{{den}}}"


def _ratio(fr: Fraction) -> str:
    """A ratio a : b from a Fraction a/b."""
    return f"{fr.numerator} : {fr.denominator}"


POOL01 = [k for k in range(3, 41) if q01.solve(k=k) is not None]


POOL02 = [(c, m) for m in (2, 3, 4, 5) for c in range(2, 60)
          if (x := q02.solve(c=c, m=m)) is not None and x != 0
          and Fraction(x).denominator <= 12 and abs(Fraction(x).numerator) <= 400]


POOL03 = [(py, const) for py in range(1, 9) for const in range(1, 16)
          if (v := q03.solve(py=py, const=const)) is not None
          and Fraction(v).denominator <= 4]


POOL04 = [{"cheap": cheap, "dear": dear, "sell": sell, "profit": profit}
          for cheap in (50, 80, 100, 120) for dear in (200, 300, 400)
          for sell in (120, 150, 180, 200, 240, 250, 300) for profit in (20, 25, 50)
          if (r := q04.solve(cheap=cheap, dear=dear, sell=sell, profit=profit)) is not None
          and Fraction(r) > 0 and Fraction(r).numerator <= 20 and Fraction(r).denominator <= 20]


def _pond(wn, wd, dn, dd, gap):
    """x, y, z from the three printed relations (for the distractors only)."""
    # x = (y + z)·wn/wd and y = z + gap give x = a(2z + gap); then
    # dd·z = dn·(x + y) = dn·(a(2z + gap) + z + gap) is linear in z.
    a = Fraction(wn, wd)
    z = Fraction(dn * (a * gap + gap), dd - dn * (2 * a + 1))
    y = z + gap
    x = a * (y + z)
    return x, y, z


POOL05 = [{"wn": wn, "wd": wd, "dn": dn, "dd": dd, "gap": gap}
          for wn, wd in ((1, 5), (1, 4), (1, 3), (2, 7), (2, 9)) for dn, dd in ((2, 3), (1, 2), (3, 4), (2, 5))
          for gap in (2, 3, 4, 5, 6, 8, 10, 12)
          if (v := q05.solve(wn=wn, wd=wd, dn=dn, dd=dd, gap=gap)) is not None
          and Fraction(v).denominator == 1 and all(
              d > 0 and Fraction(d).denominator == 1 for d in _pond(wn, wd, dn, dd, gap))]


POOL06 = [(digit, hi) for digit in range(1, 10) for hi in (99, 999)]


def _distinct_digits(n: int) -> int:
    return len(set(str(n)))


POOL07 = [n for n in range(5, 11) if q07.solve(degrees=tuple(range(n - 1, 0, -1)), teams=n) is not None]


_TEAMS = "ABCDEFGHIJ"


POOL08 = [(extra, drop) for extra in range(2, 13) for drop in (10, 20, 25, 30, 40, 50, 60, 75)
          if (r := q08.solve(extra=extra, drop=drop)) is not None and Fraction(r).denominator == 1]


POOL09 = [(bac, cde) for bac in range(20, 61, 5) for cde in range(5, 31, 5)
          if (v := q09.solve(bac=bac, cde=cde)) is not None and Fraction(v).denominator == 1
          and 90 < v < 180]


POOL10 = [{"p": p, "q": q, "qo2": qo2, "o1o2": o1o2}
          for p, q in ((3, 4), (2, 3), (3, 5), (4, 5), (1, 2), (5, 6))
          for qo2 in range(q, 31, q) for o1o2 in range(p + q, 61, p + q)
          if (v := q10.solve(p=p, q=q, qo2=qo2, o1o2=o1o2)) is not None and v > 0]


def _pr_square(p, q, qo2, o1o2) -> Fraction:
    o1p = Fraction(qo2 * p, q)
    o1r = Fraction(o1o2 * p, p + q)
    return o1r * o1r - o1p * o1p


POOL11 = [{"area": area, "ae": ae, "eb": eb, "bf": bf, "fc": fc}
          for ae, eb in ((4, 3), (1, 1), (2, 1), (1, 2), (3, 4), (5, 2), (2, 3))
          for bf, fc in ((2, 3), (1, 1), (1, 2), (3, 2), (1, 3), (3, 5))
          for area in range(30, 241, 6)
          if (v := q11.solve(area=area, ae=ae, eb=eb, bf=bf, fc=fc)) is not None
          and Fraction(v).denominator == 1]


POOL12 = [(t, c) for t in range(3, 9) for c in (1, 2, 3)
          if (s := t ** 3 - 3 * c * t) > 0 and q12.solve(sq=s * s, c=c) is not None
          and math.isclose(q12.solve(sq=s * s, c=c), t)]


def _poly_tex(coeffs) -> str:
    """a x² + b x + c as TeX, dropping zero terms and unit coefficients."""
    out = ""
    for power, coeff in zip((2, 1, 0), coeffs):
        coeff = Fraction(coeff)
        if coeff == 0:
            continue
        mag = abs(coeff)
        body = {2: "x^2", 1: "x", 0: ""}[power]
        num = "" if (mag == 1 and body) else _num(mag)
        if out:
            out += f" {'-' if coeff < 0 else '+'} {num}{body}"
        else:
            out = f"{'-' if coeff < 0 else ''}{num}{body}"
    return out or "0"


POOL13 = [(xs, (a, b, c)) for xs in ((1, 2, 3), (0, 1, 2), (-1, 0, 1), (1, 2, 4), (0, 2, 3))
          for a in (1, 2, 3, -1, -2) for b in range(-6, 7) for c in range(-5, 8)
          if abs(b) + abs(c) > 0]


POOL14 = [(100, 10, 99, "เลขสองหลักสุดท้าย"), (100, 1, 99, "เลขสองหลักสุดท้าย"),
          (1000, 100, 999, "เลขสามหลักสุดท้าย"), (10, 1, 9, "เลขหลักหน่วย")]


POOL15 = [(shift, top, divisor) for shift in (1, 3, 5, 7) for top in (4, 5, 6) for divisor in (4, 8, 9)
          if (v := q15.solve(shift=shift, top=top, divisor=divisor)) is not None and 5 <= v < top ** 3]


POOL16 = [top for top in range(3, 10) if q16.solve(top=top, distinct_numbers=True) is not None]


COINS17 = (Fraction(1, 4), Fraction(1, 2), 1, 2, 5, 10)


NOTES17 = (20, 50, 100, 500, 1000)


def _baht(value) -> str:
    """A sum of money as a number of baht, two decimals when there are satang."""
    value = Fraction(value)
    return str(int(value)) if value.denominator == 1 else f"{float(value):.2f}"


def _money(value) -> str:
    value = Fraction(value)
    if value < 1:
        return f"{int(value * 100)} สตางค์"
    whole, rest = divmod(value, 1)
    return f"{int(whole):,} บาท" + (f" {int(rest * 100)} สตางค์" if rest else "")


POOL18 = [n for n in range(4, 61, 2) if q18.solve(n=n) is not None]


POOL20 = [(ef, bf) for bf in range(4, 31) for ef in range(1, bf)
          if q20.solve(ef=ef, bf=bf) is not None]


POOL21 = [(ac, ap) for ac in range(6, 31) for ap in range(3, 31)
          if (r := q21.solve(ac=ac, ap=ap)) is not None and Fraction(r) < 2
          and Fraction(r).numerator <= 30]


def _radius_square(ab, cd, ox) -> Fraction:
    return (Fraction(ox) ** 2 + Fraction(ab, 2) ** 2 + Fraction(cd, 2) ** 2) / 2


POOL22 = [(ab, cd, ox) for ab in range(6, 81, 2) for cd in range(ab, 81, 2) for ox in range(2, 61)
          if q22.solve(ab=ab, cd=cd, ox=ox) is not None
          and isqrt(int(_radius_square(ab, cd, ox))) ** 2 == _radius_square(ab, cd, ox)]


POOL23 = [{"weight": w, "overflow": o} for w in range(8000, 24001, 2000) for o in range(300, 1601, 100)
          if (m := q23.solve(weight=w, overflow=o)) is not None and m > 0]


def _most_cubes_by_weight(weight, big_weight=200, small_weight=400, stock=100) -> int:
    """The most cubes the weight alone allows — the overflow forgotten."""
    best = 0
    for j in range(stock + 1):
        rest = weight - j * small_weight
        if rest >= 0 and rest % big_weight == 0 and rest // big_weight <= stock:
            best = max(best, j + rest // big_weight)
    return best


def _q24_exact(ae_sq, be, gap):
    """(whole, coefficient, radicand) with AD² = whole + coefficient·√radicand, or None."""
    lead = Fraction(ae_sq, be * be) - 2
    if lead == 0:
        return None
    disc = Fraction(4 * gap * gap) + 4 * lead * gap * gap
    if disc < 0:
        return None
    root = Fraction(isqrt(disc.numerator), isqrt(disc.denominator))
    if root * root != disc:
        return None
    c = [r for r in ((2 * gap + root) / (2 * lead), (2 * gap - root) / (2 * lead)) if r > 0]
    if len(c) != 1:
        return None
    c = c[0]
    out, rad = 1, ae_sq                       # √ae_sq = out·√rad
    for f in range(2, isqrt(ae_sq) + 1):
        while rad % (f * f) == 0:
            rad //= f * f
            out *= f
    whole = ae_sq + c * c + (c + gap) ** 2
    if rad == 1:
        return whole + 2 * c * out, 0, 1
    return whole, 2 * c * out, rad


def _surd_sum(whole, coeff, rad, sign="+") -> str:
    if coeff == 0:
        return _num(whole)
    head = "" if coeff == 1 else _num(coeff)
    return f"{_num(whole)} {sign} {head}\\sqrt{{{rad}}}"


POOL24 = [(ae_sq, be, gap) for ae_sq in range(5, 61) for be in range(1, 8) for gap in range(1, 9)
          if be * be < ae_sq and q24.solve(ae_sq=ae_sq, be=be, gap=gap) is not None
          and (e := _q24_exact(ae_sq, be, gap)) is not None and all(Fraction(v).denominator == 1 for v in e)
          and e[1] != 0]


POOL25 = [(terms, width) for width in (2, 3, 4) for terms in range(4, 25)
          if q25.solve(terms=terms, width=width) is not None]


def _block(k: int, width: int) -> str:
    return "·".join(str(k + i) for i in range(width))


def _q26_side(bound, a, c, p, q, sign):
    """The open t-interval keeping one side of the inequality, from its discriminant."""
    head, tail, shift = sign * (a - bound), sign * (c - bound * q), sign * (-bound * p)
    if head <= 0 or tail <= 0:
        return None
    span = math.sqrt(4 * head * tail)
    if not span.is_integer():
        return None
    ends = sorted(((-shift - span) * sign, (-shift + span) * sign))
    return Fraction(int(ends[0])), Fraction(int(ends[1]))


POOL26 = [{"lo": lo, "hi": hi, "a": a, "c": c, "p": 1, "q": 2}
          for lo in range(-8, 0) for hi in range(2, 11) for a in (1, 2, 3) for c in range(-12, 0)
          if lo < a < hi
          and (got := q26.solve(lo=lo, hi=hi, a=a, c=c, p=1, q=2)) is not None
          and all(isinstance(v, Fraction) and v.denominator == 1 for v in got)
          and _q26_side(lo, a, c, 1, 2, 1) and _q26_side(hi, a, c, 1, 2, -1)]


def _interval(lo, hi, strict=True) -> str:
    rel = "<" if strict else r"\le"
    return f"{_num(lo)} {rel} t {rel} {_num(hi)}"


def _factor_small(n: int) -> dict[int, int]:
    out, d = {}, 2
    while d * d <= n:
        while n % d == 0:
            out[d] = out.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


POOL27 = [(base, divisors) for base in (12, 18, 20, 28, 44, 45, 50, 52, 63, 75, 2564)
          for divisors in (15, 21, 33, 35, 39, 51, 55, 77, 2021)
          if q27.solve(base=base, divisors=divisors) is not None and len(_factor_small(divisors)) == 2]


def _power_tex(pairs) -> str:
    return r" \cdot ".join(f"{p}^{{{e}}}" if e != 1 else str(p) for p, e in pairs)


POOL28 = [(p, q) for p in range(2, 41) for q in range(1, 21)
          if (got := q28.solve(p=p, q=q)) is not None and len(got) == 2]


def _pairs(pairs) -> str:
    return r",\ ".join(f"({x}, {y})" for x, y in pairs)


def _prime_count(n: int) -> int:
    return sum(1 for k in range(2, n + 1) if all(k % d for d in range(2, isqrt(k) + 1)))


POOL30 = [(a1, a2, a3, a4, a5) for a1 in range(6, 16) for k in (1, 2, 3) for a3 in range(8, 25, 2)
          for a4 in range(a3 // 2, 2 * a3 + 1) for a5 in range(10, 41)
          if (a2 := a1 * k) and (v := q30.solve(a1=a1, a2=a2, a3=a3, a4=a4, a5=a5)) is not None
          and Fraction(v).denominator == 1 and 10 <= v <= 120][::7]


@question_type("math.posn2564_q01", display_name={"th": "หาค่า (x + a)/(x − a) จาก x² + a² = kax"},
               level=LEVEL, topic="อัตราส่วนจากสมการกำลังสอง")
class SquareRatio(SheetProblem):
    def expr(self, rng: Random):
        k = rng.choice(POOL01)
        square = Fraction(k + 2, k - 2)
        answer = _surd(square)
        assert math.isclose(SOLVE[1](k=k), math.sqrt(square))
        return MathDraw(
            "", answer,
            prompt=(f"กำหนดให้ a และ x เป็นจำนวนจริง โดยที่ 0 < a < x และ x² + a² = {k}ax "
                    "จงหาค่าของ (x + a)/(x − a)"),
            hint=r"\left(\frac{x+a}{x-a}\right)^2 = \frac{x^2+2ax+a^2}{x^2-2ax+a^2}",
            distractors=_distinct(answer, [
                _surd(1 / square),               # turned the fraction upside down
                _num(square),                    # forgot to take the square root
                _surd(Fraction(k + 1, k - 1)),   # expanded (x ± a)² with ±ax
                _surd(k), _num(Fraction(k, 2))]))


@question_type("math.posn2564_q02", display_name={"th": "สมการเลขยกกำลังเศษส่วน (c+x)^(2/3)"},
               level=LEVEL, topic="สมการเลขยกกำลังเศษส่วน")
class FractionalPowers(SheetProblem):
    def expr(self, rng: Random):
        c, m = rng.choice(POOL02)
        x = Fraction(SOLVE[2](c=c, m=m))
        answer = f"x = {_num(x)}"
        cube = m ** 3
        return MathDraw(
            r"(%d+x)^{2/3} + %d(%d-x)^{2/3} = %d(%d - x^2)^{1/3}" % (c, m, c, m + 1, c * c),
            answer,
            prompt="จงหาจำนวนจริง x ≠ 0 ทั้งหมดที่สอดคล้องกับสมการ",
            hint=r"u = (c+x)^{1/3},\ v = (c-x)^{1/3}:\ u^2 - (m+1)uv + mv^2 = (u-v)(u-mv)",
            distractors=_distinct(answer, [
                f"x = {_num(-x)}",                                   # swapped c + x and c − x
                f"x = {_num(Fraction(c * (m * m - 1), m * m + 1))}",  # squared instead of cubed
                f"x = {_num(Fraction(c * (m - 1), m + 1))}",          # set u = m·v without cubing
                f"x = {_num(Fraction(c * (cube + 1), cube - 1))}",    # inverted the ratio
                "x = 0"]))                                           # the root the stem excludes


@question_type("math.posn2564_q03", display_name={"th": "เส้นตรงสองเส้นกับพาราโบลา — หา m + k + a"},
               level=LEVEL, topic="เส้นตรงและพาราโบลา")
class LinesAndParabola(SheetProblem):
    def expr(self, rng: Random):
        py, const = rng.choice(POOL03)
        value = Fraction(SOLVE[3](py=py, const=const))
        answer = _num(value)
        others = [a for a in q03._roots(py, const) if a >= 0]
        wrong_root = [_num(Fraction(4 * Fraction(a).limit_denominator(1000)) - Fraction(py, 2))
                      for a in others]
        return MathDraw(
            "", answer,
            prompt=(f"กำหนดให้ a, m, k เป็นจำนวนจริง ถ้าเส้นตรง y = x − 2a ผ่านจุด (2m, a) ที่อยู่ใน"
                    f"จตุภาคที่ 3 และเส้นตรง y = 3x − 2k ตัดกับพาราโบลา y = −2x² + x − m + k + {const} "
                    f"ที่จุด (a, {py}) จงหาค่าของ m + k + a"),
            hint=r"3a = 2m,\quad k = \tfrac{3a - y_0}{2}",
            distractors=_distinct(answer, [
                *wrong_root,                     # kept the root in the first quadrant
                _num(-value), _num(value + 1), _num(value - 1), _num(2 * value)]))


@question_type("math.posn2564_q04", display_name={"th": "อัตราส่วนผสมกาแฟที่ให้กำไรตามต้องการ"},
               level=LEVEL, topic="โจทย์ปัญหาอัตราส่วนและร้อยละ")
class CoffeeBlend(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL04)
        ratio = Fraction(SOLVE[4](**p))
        answer = _ratio(ratio)
        cheap, dear, sell = p["cheap"], p["dear"], p["sell"]

        def blend(cost):
            # cheap : dear for a mixture costing `cost` a kilogram, if possible
            if not cheap < cost < dear:
                return None
            return Fraction(dear - cost, cost - cheap)

        slips = [blend(Fraction(sell)),                              # ignored the profit
                 blend(Fraction(sell) * (100 - p["profit"]) / 100),  # took profit off the price
                 1 / ratio]                                          # wrote it the other way round
        return MathDraw(
            "", answer,
            prompt=(f"ร้านค้าแห่งหนึ่งขายเมล็ดกาแฟอาราบิก้าผสมกับโรบัสต้า โดยเมล็ดกาแฟโรบัสต้าราคา"
                    f"กิโลกรัมละ {cheap} บาท และอาราบิก้าราคากิโลกรัมละ {dear} บาท ร้านค้าต้องผสม"
                    f"โรบัสต้าต่ออาราบิก้าเป็นอัตราส่วนเท่าใด จึงทำให้ได้กำไร {p['profit']}% "
                    f"เมื่อขายกาแฟผสมในราคากิโลกรัมละ {sell} บาท"),
            hint=r"\text{ต้นทุน} = \frac{\text{ราคาขาย}}{1 + \text{กำไร}}",
            distractors=_distinct(answer, [_ratio(s) for s in slips if s]
                                  + [_ratio(ratio * 2), _ratio(ratio + 1)]))


@question_type("math.posn2564_q05", display_name={"th": "พื้นที่ก้นบ่อจากอัตราส่วนของด้าน"},
               level=LEVEL, topic="โจทย์ปัญหาอัตราส่วน")
class FishPond(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL05)
        area = SOLVE[5](**p)
        x, y, z = _pond(**p)
        assert x * y == area
        answer = f"{_num(area)}"
        return MathDraw(
            "", answer,
            prompt=(f"บ่อเลี้ยงปลาทรงสี่เหลี่ยมมุมฉากมีความกว้าง x หน่วย ยาว y หน่วย และลึก z หน่วย โดยที่ "
                    f"x : (y + z) = {p['wn']} : {p['wd']} และ z : (x + y) = {p['dn']} : {p['dd']} "
                    f"ถ้าความยาวของบ่อยาวกว่าความลึกอยู่ {p['gap']} หน่วย จงหาพื้นที่ก้นบ่อเลี้ยงปลานี้ "
                    f"(ตารางหน่วย)"),
            hint=r"\text{ก้นบ่อ} = \text{กว้าง} \times \text{ยาว} = xy",
            distractors=_distinct(answer, [
                _num(x * z),                 # the wall, not the floor
                _num(y * z),                 # the long wall
                _num(x * y * z),             # the volume
                _num(2 * (x * y + y * z + z * x))]))   # every face


@question_type("math.posn2564_q06", display_name={"th": "ผลบวกของจำนวนเลขโดดที่แตกต่างกัน B(n)"},
               level=LEVEL, topic="ฟังก์ชันบนเลขโดด")
class DigitFunction(SheetProblem):
    def expr(self, rng: Random):
        digit, hi = rng.choice(POOL06)
        value = SOLVE[6](digit=digit, hi=hi)
        has = [n for n in range(1, hi + 1) if str(digit) in str(n)]
        with_two = next(n for n in range(100, 1000) if str(digit) in str(n) and _distinct_digits(n) == 2)
        without = next(n for n in range(500, 1000) if str(digit) not in str(n))
        answer = str(value)
        return MathDraw(
            "", answer,
            prompt=(f"กำหนดให้ B(n) แทนจำนวนเลขโดดที่แตกต่างกันของ n ถ้า {digit} เป็นเลขโดดของ n "
                    f"และ B(n) = 0 ถ้า {digit} ไม่เป็นเลขโดดของ n เช่น B({with_two}) = 2 และ "
                    f"B({without}) = 0 จงหาค่าของ B(1) + B(2) + B(3) + ⋯ + B({hi})"),
            hint=r"\text{นับเฉพาะ } n \text{ ที่มีเลขโดดนั้น แล้วบวกจำนวนเลขโดดที่ต่างกันของแต่ละตัว}",
            distractors=_distinct(answer, [
                str(len(has)),                                        # counted the numbers, not B(n)
                str(sum(str(n).count(str(digit)) for n in has)),      # counted occurrences of the digit
                str(sum(len(str(n)) for n in has)),                   # counted every digit, repeats too
                str(value + 1), str(value - 1)]))


@question_type("math.posn2564_q07", display_name={"th": "การแข่งขันแบบพบกันหมด — ทีมสุดท้ายแข่งไปกี่นัด"},
               level=LEVEL, topic="ทฤษฎีกราฟเบื้องต้น")
class RoundRobin(SheetProblem):
    def expr(self, rng: Random):
        n = rng.choice(POOL07)
        degrees = list(range(n - 1, 0, -1))
        value = SOLVE[7](degrees=tuple(degrees), teams=n)
        teams = list(_TEAMS[:n])
        known, last = teams[:-1], teams[-1]
        order = degrees[:]
        rng.shuffle(order)
        played = ", ".join(f"ทีม {t} แข่งไปแล้ว {d} นัด" for t, d in zip(known, order))
        answer = str(value)
        return MathDraw(
            "", answer,
            prompt=(f"การแข่งขันฟุตบอลแบบพบกันหมดมีทีมเข้าแข่งขัน {n} ทีม คือทีม {', '.join(teams)} "
                    f"(แต่ละคู่แข่งกันไม่เกินหนึ่งนัด) ขณะนี้ {played} จงหาว่าทีม {last} แข่งไปแล้วกี่นัด"),
            hint=r"\text{ทีมที่แข่งครบทุกทีมจับคู่กับทีมที่แข่งไปนัดเดียว แล้วตัดคู่นั้นออก}",
            distractors=_distinct(answer, [str(d) for d in (value + 1, value - 1, n - 1, 0, n // 2 + 1)
                                           if d >= 0]))


@question_type("math.posn2564_q08", display_name={"th": "เพิ่มห้องเรียนแล้วนักเรียนต่อห้องลดลงร้อยละ"},
               level=LEVEL, topic="ร้อยละ")
class ExtraRooms(SheetProblem):
    def expr(self, rng: Random):
        extra, drop = rng.choice(POOL08)
        rooms = SOLVE[8](extra=extra, drop=drop)
        answer = str(rooms)
        return MathDraw(
            "", answer,
            prompt=(f"โรงเรียนแห่งหนึ่งมีนักเรียนชั้น ม.3 จำนวนเท่ากันในทุกห้องเรียน ปีนี้ต้องจัดห้องเรียน"
                    f"ให้นักเรียนกลุ่มนี้เพิ่มอีก {extra} ห้อง และพบว่าจำนวนนักเรียนต่อห้องลดลงจากเดิม "
                    f"{drop}% พอดี (นักเรียนทุกห้องยังเท่ากัน) จงหาว่าเดิมมีห้องเรียนกี่ห้อง"),
            hint=r"\frac{N}{r + e} = \left(1 - \frac{d}{100}\right)\frac{N}{r}",
            distractors=_distinct(answer, [str(v) for v in (
                rooms + extra,                                  # the number after adding rooms
                extra * 100 // drop,                            # e ÷ d%: the drop applied to the new total
                rooms + 1, rooms - 1, rooms * 2) if v > 0]))


@question_type("math.posn2564_q09", display_name={"th": "มุมในวงกลมที่มีเส้นผ่านศูนย์กลาง — หา ∠ACD"},
               level=LEVEL, topic="เรขาคณิตวงกลม")
class CircleAngle(SheetProblem):
    def expr(self, rng: Random):
        bac, cde = rng.choice(POOL09)
        angle = SOLVE[9](bac=bac, cde=cde)
        acb = 180 - angle
        answer = rf"{angle}^\circ"
        return MathDraw(
            "", answer,
            prompt=(f"จากรูป A, B และ C เป็นจุดบนวงกลมซึ่งมี O เป็นจุดศูนย์กลาง เส้นตรง AO ตัดกับ BC "
                    f"และวงกลมที่จุด D และ E ตามลำดับ ถ้า ∠BAC = {bac}° และ ∠CDE = {cde}° "
                    f"แล้ว ∠ACD มีขนาดเท่าไร"),
            hint=r"AE \text{ เป็นเส้นผ่านศูนย์กลาง จึงได้ } \angle ACE = 90^\circ",
            distractors=_distinct(answer, [rf"{v}^\circ" for v in (
                acb,                      # ∠ACB instead of its supplement
                180 - bac - cde, 90 + cde, 90 + bac, angle - cde) if 0 < v < 180]))


@question_type("math.posn2564_q10", display_name={"th": "เส้นสัมผัสร่วมภายในของวงกลมสองวง — หา PR"},
               level=LEVEL, topic="เรขาคณิตวงกลม")
class InternalTangent(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL10)
        square = _pr_square(**p)
        assert math.isclose(SOLVE[10](**p), math.sqrt(square))
        answer = _surd(square)
        qr_square = square * Fraction(p["q"], p["p"]) ** 2
        o1r = Fraction(p["o1o2"] * p["p"], p["p"] + p["q"])
        return MathDraw(
            "", answer,
            prompt=(f"จากรูป เส้นตรง ℓ สัมผัสวงกลมสองวงซึ่งมีจุดศูนย์กลางที่ O₁ และ O₂ ที่จุด P และ Q "
                    f"ตามลำดับ และ O₁O₂ ตัดกับ PQ ที่จุด R ถ้า PR : RQ = {p['p']} : {p['q']}, "
                    f"QO₂ = {p['qo2']} หน่วย และ O₁O₂ = {p['o1o2']} หน่วย แล้วจงหาความยาว PR (หน่วย)"),
            hint=r"\triangle O_1PR \sim \triangle O_2QR",
            distractors=_distinct(answer, [
                _surd(qr_square),          # RQ, the other tangent piece
                _num(o1r),                 # O₁R, the hypotenuse
                _num(square),              # PR², not PR
                _surd(square + 2 * o1r), _surd(square / 4)]))


@question_type("math.posn2564_q11", display_name={"th": "พื้นที่สามเหลี่ยม EBF ในสี่เหลี่ยมผืนผ้า"},
               level=LEVEL, topic="พื้นที่รูปสี่เหลี่ยมและสามเหลี่ยม")
class CornerTriangle(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL11)
        value = Fraction(SOLVE[11](**p))
        area, ae, eb, bf, fc = p["area"], p["ae"], p["eb"], p["bf"], p["fc"]
        answer = _num(value)
        return MathDraw(
            "", answer,
            # No figure: the sheet's drawing shows one placement of E and F, and
            # the ratios here move them.
            figure=None,
            prompt=(f"รูปสี่เหลี่ยมผืนผ้า ABCD มีพื้นที่ {area} ตารางหน่วย จุด E อยู่บนด้าน AB และจุด F "
                    f"อยู่บนด้าน BC ถ้า AE : EB = {ae} : {eb} และ BF : FC = {bf} : {fc} "
                    f"จงหาพื้นที่ของรูปสามเหลี่ยม EBF (ตารางหน่วย)"),
            hint=r"[EBF] = \tfrac12 \cdot EB \cdot BF",
            distractors=_distinct(answer, [
                _num(2 * value),                                                # forgot the ½
                _num(Fraction(area * ae * bf, 2 * (ae + eb) * (bf + fc))),      # used AE for EB
                _num(Fraction(area * eb * fc, 2 * (ae + eb) * (bf + fc))),      # used FC for BF
                _num(Fraction(area * eb * bf, 2 * ae * fc)),                    # part over part, not part over whole
                _num(value + 1)]))


@question_type("math.posn2564_q12", display_name={"th": "หาค่า a + c/a จาก (a³ + c³/a³)²"},
               level=LEVEL, topic="การจัดรูปพีชคณิต")
class CubeIdentity(SheetProblem):
    def expr(self, rng: Random):
        t, c = rng.choice(POOL12)
        s = t ** 3 - 3 * c * t
        assert math.isclose(SOLVE[12](sq=s * s, c=c), t)
        answer = str(t)
        return MathDraw(
            "", answer,
            prompt=(f"กำหนดให้ a เป็นจำนวนจริงบวกที่สอดคล้องกับ (a³ + {c ** 3}/a³)² = {s * s:,} "
                    f"จงหาค่าของ a + {c}/a"),
            hint=r"\left(a + \tfrac{c}{a}\right)^3 = a^3 + \tfrac{c^3}{a^3} + 3c\left(a + \tfrac{c}{a}\right)",
            distractors=_distinct(answer, [
                str(s),                                    # stopped at a³ + c³/a³
                str(t + 1), str(t - 1),
                str(round(s ** (1 / 3))),                  # cube-rooted without the 3c term
                str(t * t)]))


@question_type("math.posn2564_q13", display_name={"th": "พหุนามดีกรีต่ำสุดที่ผ่านสามจุด"},
               level=LEVEL, topic="พหุนามและการประมาณค่า")
class LeastDegreePolynomial(SheetProblem):
    def expr(self, rng: Random):
        xs, (a, b, c) = rng.choice(POOL13)
        points = tuple((x, a * x * x + b * x + c) for x in xs)
        coeffs = tuple(SOLVE[13](points=points))
        assert coeffs == (a, b, c), (points, coeffs)
        answer = f"P(x) = {_poly_tex(coeffs)}"
        (x1, y1), (x2, y2), _ = points
        slope = Fraction(y2 - y1, x2 - x1)
        line = (0, slope, y1 - slope * x1)          # through the first two points only
        conditions = ", ".join(f"P({x}) = {y}" for x, y in points)
        return MathDraw(
            "", answer,
            prompt=f"จงหาพหุนาม P(x) ที่มีดีกรีน้อยที่สุด ซึ่ง {conditions}",
            hint=r"\text{สามเงื่อนไข} \Rightarrow \text{ดีกรีไม่เกิน } 2",
            distractors=_distinct(answer, [f"P(x) = {_poly_tex(v)}" for v in (
                line,
                (a, -b, c),                  # sign slip on the middle term
                (-a, b, c),
                (a, b, c + 1),
                (b, a, c))]))


@question_type("math.posn2564_q14", display_name={"th": "n ที่ทุกกำลังของ n ลงท้ายเหมือน n"},
               level=LEVEL, topic="เลขคณิตมอดุลาร์")
class StableEndings(SheetProblem):
    def expr(self, rng: Random):
        mod, lo, hi, words = rng.choice(POOL14)
        value = SOLVE[14](mod=mod, lo=lo, hi=hi)
        fixed = [n for n in range(lo, hi + 1) if n * n % mod == n % mod]
        answer = str(value)
        return MathDraw(
            "", answer,
            prompt=(f"จงหาผลรวมของจำนวนเต็มบวก n ทั้งหมด โดยที่ {lo} ≤ n ≤ {hi} และ nᵏ มี{words}"
                    f"เหมือนกับ n สำหรับทุกจำนวนเต็มบวก k"),
            hint=rf"n^2 \equiv n \pmod{{{mod}}}",
            distractors=_distinct(answer, [
                str(len(fixed)),                       # counted them instead of adding
                str(value + 1),                        # let n = 1 in where it is excluded
                str(value - fixed[0]),                 # missed the smallest
                str(max(fixed)),                       # stopped at the largest
                str(value + mod)]))


@question_type("math.posn2564_q15", display_name={"th": "นับสามสิ่งอันดับที่ (a+k)^(b^c) หารลงตัว"},
               level=LEVEL, topic="การหารลงตัวและการนับ")
class DivisiblePowers(SheetProblem):
    def expr(self, rng: Random):
        shift, top, divisor = rng.choice(POOL15)
        value = SOLVE[15](shift=shift, top=top, divisor=divisor)
        values = ", ".join(str(i) for i in range(1, top + 1))
        bases_divisible = sum(1 for a in range(1, top + 1) if (a + shift) % divisor == 0)
        answer = str(value)
        return MathDraw(
            "", answer,
            prompt=(f"จงหาจำนวนของสามสิ่งอันดับ (a, b, c) ทั้งหมดที่ a, b, c ∈ {{{values}}} "
                    f"และ (a + {shift})^(b^c) หารด้วย {divisor} ลงตัว"),
            hint=r"\text{แยกตัวประกอบเฉพาะของฐาน แล้วดูว่าเลขชี้กำลัง } b^c \text{ ต้องมากเท่าใด}",
            distractors=_distinct(answer, [
                str(bases_divisible * top * top),      # only bases divisible on their own
                str(top ** 3 - value),                 # counted the complement
                str(value + top), str(value - top), str(value + 1)]))


@question_type("math.posn2564_q16", display_name={"th": "ปริศนาผลรวมและผลคูณของสลากสองใบ"},
               level=LEVEL, topic="ตรรกศาสตร์เชิงปริศนา")
class SumProductPuzzle(SheetProblem):
    def expr(self, rng: Random):
        top = rng.choice(POOL16)
        value = SOLVE[16](top=top, distinct_numbers=True)
        same = SOLVE[16](top=top, distinct_numbers=False)
        cards = ", ".join(str(i) for i in range(1, top + 1))
        answer = str(value)
        return MathDraw(
            "", answer,
            prompt=(f"มีสลากเขียนหมายเลข {cards} อย่างละหนึ่งใบอยู่ในกล่องทึบแต่ละกล่องจากสองกล่อง "
                    f"คุณครูสุ่มหยิบสลากมากล่องละ 1 ใบ แล้วบอกผลรวมของสองหมายเลขให้เด็กชาย A ทราบ "
                    f"และบอกผลคูณให้เด็กหญิง B ทราบ  A: “เธอรู้ไหมว่าคุณครูหยิบได้เลขอะไรบ้าง”  "
                    f"B: “พยายามคิดแล้ว แต่ตัวเลขที่ได้ยินยังบอกไม่ได้ว่าคุณครูหยิบได้เลขอะไรบ้าง แล้วเธอล่ะ”  "
                    f"A: “ตอนแรกก็ไม่รู้ แต่ตอนนี้รู้แล้วแหละ ฉันได้ยินคนละเลขกับเธอนะ”  "
                    f"B: “อ๋อ ตอนนี้ฉันก็รู้แล้ว”  ให้ a และ b เป็นหมายเลขที่คุณครูหยิบได้ "
                    f"จงหาค่าของ a² + b²"),
            hint=r"\text{ตัดกรณีทีละประโยคตามลำดับที่พูด}",
            distractors=_distinct(answer, [
                *([str(same)] if same is not None else []),   # ignored "คนละเลขกับเธอ"
                str(value + 1), str(value - 1), str(2 * value), "8", "13"]))


@question_type("math.posn2564_q17", display_name={"th": "ปริศนาเหรียญและธนบัตรของนักเรียนห้าคน"},
               level=LEVEL, topic="ตรรกศาสตร์เชิงปริศนา")
class CoinsAndNotes(SheetProblem):
    def expr(self, rng: Random):
        # The clues name coins and notes by role, so any five of each, dealt into
        # the roles in any order, keep the deduction (and its one answer).
        coins = tuple(rng.sample(COINS17, 5))
        notes = tuple(rng.sample(NOTES17, 5))
        value = SOLVE[17](coins=coins, notes=notes)
        assert value is not None
        small, one, two, five, ten = coins
        n20, n50, n100, n500, n1000 = notes
        answer = _baht(value)
        return MathDraw(
            "", answer,
            prompt=(f"นักเรียน 5 คน คือ A, B, C, D และ E ได้รับเหรียญคนละ 1 เหรียญ เป็นเหรียญ "
                    f"{', '.join(_money(c) for c in sorted(coins))} และได้รับธนบัตรคนละ 1 ใบ เป็นธนบัตร "
                    f"{', '.join(_money(n) for n in sorted(notes))} โดยที่  "
                    f"• B, ผู้ได้ธนบัตร {_money(n20)}, ผู้ได้ธนบัตร {_money(n50)}, ผู้ได้เหรียญ {_money(two)} "
                    f"และผู้ได้เหรียญ {_money(small)} เป็นคนละคนกัน  "
                    f"• D ไม่ได้ธนบัตร {_money(n20)}  • ผู้ได้เหรียญ {_money(small)} คือ A  "
                    f"• ธนบัตรที่ C ได้มีมูลค่า {_money(n100)}  • D ได้เหรียญ {_money(five)}  "
                    f"• E ไม่ได้เหรียญ {_money(one)}  • ผู้ได้เหรียญ {_money(one)} ไม่ได้ธนบัตร {_money(n1000)}  "
                    f"นักเรียน B ได้รับเงินรวมกี่บาท"),
            hint=r"\text{ข้อแรกระบุคนห้าคนที่ต่างกัน จึงครบทุกคนพอดี}",
            distractors=_distinct(answer, [_baht(v) for v in (
                Fraction(one) + n1000,          # missed the last bullet
                Fraction(ten) + n500,           # gave B the coin E was left with
                Fraction(two) + n500,
                Fraction(one) + n50,
                Fraction(five) + n500)]))


@question_type("math.posn2564_q18", display_name={"th": "ในห้องนี้มีคนพูดจริงอย่างมาก k − 1 คน"},
               level=LEVEL, topic="ตรรกศาสตร์เชิงปริศนา")
class TruthTellers(SheetProblem):
    def expr(self, rng: Random):
        n = rng.choice(POOL18)
        value = SOLVE[18](n=n)
        answer = str(value)
        return MathDraw(
            "", answer,
            prompt=(f"ห้องเรียนห้องหนึ่งมีนักเรียน {n} คน นักเรียนคนที่ 1 พูดว่า “ไม่มีใครในห้องนี้พูดจริงเลย” "
                    f"และนักเรียนคนที่ k พูดว่า “ในห้องนี้มีคนพูดจริงอย่างมาก k − 1 คน” "
                    f"สำหรับ k = 2, 3, …, {n} จงหาว่าในห้องนี้มีคนพูดจริงกี่คน"),
            hint=r"\text{มีคนพูดจริง } t \text{ คน: คำพูดของคนที่ } k \text{ จริงเมื่อ } k \ge t + 1",
            distractors=_distinct(answer, [str(v) for v in (value + 1, value - 1, n - 1, 1, 0)
                                           if v >= 0]))


@question_type("math.posn2564_q19", display_name={"th": "ความน่าจะเป็นที่ x² + ax + b = 0 มีคำตอบเดียว"},
               level=LEVEL, topic="ความน่าจะเป็น")
class DoubleRoot(SheetProblem):
    def expr(self, rng: Random):
        n = rng.randint(2, 12)
        value = Fraction(SOLVE[19](n=n))
        members = "{1, 2, 3, 4}" if n == 2 else f"{{1, 2, 3, …, {n * n}}}"
        answer = _num(value)
        return MathDraw(
            "", answer,
            prompt=(f"สุ่มเลือกจำนวนนับ a และ b จากเซต {members} (เลือกซ้ำกันได้) "
                    f"จงหาความน่าจะเป็นที่สมการ x² + ax + b = 0 จะมีคำตอบเพียงคำตอบเดียว"),
            hint=r"\text{คำตอบเดียว} \iff a^2 = 4b",
            distractors=_distinct(answer, [_num(v) for v in (
                Fraction(1, n ** 4),                 # one favourable pair only
                Fraction(1, n ** 2),
                Fraction(2, n ** 3),                 # counted each pair twice
                Fraction(1, 2 * n ** 3),
                Fraction(n + 1, n ** 4))]))


@question_type("math.posn2564_q20", display_name={"th": "เส้นแบ่งครึ่งมุมภายในและภายนอก — หา CE"},
               level=LEVEL, topic="เรขาคณิต: เส้นแบ่งครึ่งมุม")
class Bisectors(SheetProblem):
    def expr(self, rng: Random):
        ef, bf = rng.choice(POOL20)
        value = SOLVE[20](ef=ef, bf=bf)
        answer = _num(value)
        return MathDraw(
            "", answer,
            prompt=(f"ABC เป็นรูปสามเหลี่ยม เส้นแบ่งครึ่งมุมภายในของ ∠ABC ตัดกับเส้นแบ่งครึ่งมุมภายนอกของ ∠ACB "
                    f"ที่จุด D เส้นตรงที่ขนานกับ BC และผ่านจุด D ตัดด้าน AC ที่จุด E และตัดด้าน AB ที่จุด F "
                    f"ถ้า EF = {ef} หน่วย และ BF = {bf} หน่วย แล้ว CE ยาวเท่าใด"),
            hint=r"FD \parallel BC \Rightarrow \triangle FBD,\ \triangle EDC \text{ เป็นสามเหลี่ยมหน้าจั่ว}",
            distractors=_distinct(answer, [_num(v) for v in (
                bf + ef,                 # the reading where the line meets the extensions
                bf, ef, Fraction(bf * ef, bf + ef), value + 1) if v > 0]))


@question_type("math.posn2564_q21", display_name={"th": "วงกลมแนบในและวงกลมล้อมรอบ — หา BO : BD"},
               level=LEVEL, topic="เรขาคณิตวงกลม")
class InscribedCircumscribed(SheetProblem):
    def expr(self, rng: Random):
        ac, ap = rng.choice(POOL21)
        ratio = Fraction(SOLVE[21](ac=ac, ap=ap))
        answer = _ratio(ratio)
        return MathDraw(
            "", answer,
            prompt=(f"วงกลมแนบในรูปสามเหลี่ยม ABC มีจุดศูนย์กลางที่ O และสัมผัสด้าน AB ที่จุด D ลากเส้นตรงจาก B "
                    f"ผ่าน O ไปตัดวงกลมล้อมรอบรูปสามเหลี่ยม ABC ที่จุด P ถ้า AC = {ac} หน่วย และ AP = {ap} หน่วย "
                    f"แล้วอัตราส่วน BO : BD มีค่าเท่าใด"),
            hint=r"BO : BD = 1 : \cos\tfrac{B}{2},\quad \frac{AC}{AP} = 2\cos\tfrac{B}{2}",
            distractors=_distinct(answer, [_ratio(v) for v in (
                1 / ratio,                       # BD : BO
                Fraction(ap, ac),                # forgot the factor 2
                Fraction(ac, ap),
                Fraction(ac, 2 * ap) + 1)]))


@question_type("math.posn2564_q22", display_name={"th": "คอร์ดสองเส้นตั้งฉากกัน — หารัศมีของวงกลม"},
               level=LEVEL, topic="เรขาคณิตวงกลม")
class PerpendicularChords(SheetProblem):
    def expr(self, rng: Random):
        ab, cd, ox = rng.choice(POOL22)
        square = _radius_square(ab, cd, ox)
        assert math.isclose(SOLVE[22](ab=ab, cd=cd, ox=ox), math.sqrt(square))
        answer = _surd(square)
        return MathDraw(
            "", answer,
            prompt=(f"จากรูป O เป็นจุดศูนย์กลางของวงกลมซึ่งมีคอร์ด AB และ CD ตั้งฉากกันและตัดกันที่จุด X "
                    f"ถ้า AB = {ab} หน่วย, CD = {cd} หน่วย และ OX = {ox} หน่วย แล้ววงกลมนี้มีรัศมียาวกี่หน่วย"),
            hint=r"OX^2 = d_1^2 + d_2^2,\quad d_i^2 = r^2 - \left(\tfrac{\text{คอร์ด}}{2}\right)^2",
            distractors=_distinct(answer, list((
                _surd(square * 2),                                    # forgot to halve
                _surd(Fraction(ox) ** 2 + Fraction(ab, 2) ** 2),      # used one chord only
                _surd(Fraction(ox) ** 2 + Fraction(cd, 2) ** 2),
                _num(Fraction(ab + cd, 4)),
                _surd(square + 1)))))


@question_type("math.posn2564_q23", display_name={"th": "ลูกบาศก์สองขนาดในถังน้ำ — จำนวนมากที่สุด"},
               level=LEVEL, topic="โจทย์ปัญหาปริมาตร")
class CubesInTank(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL23)
        value = SOLVE[23](**p)
        answer = str(value)
        kilos = Fraction(p["weight"], 1000)
        return MathDraw(
            "", answer,
            prompt=(f"มีลูกบาศก์ทรงตันสองชนิด ชนิดแรกยาวด้านละ 3 เซนติเมตร หนักลูกละ 200 กรัม มี 100 ลูก "
                    f"ชนิดที่สองยาวด้านละ 2 เซนติเมตร หนักลูกละ 400 กรัม มี 100 ลูก ถังน้ำ A มีน้ำเต็มพอดี "
                    f"หย่อนลูกบาศก์รวม m ลูกลงในถังจนจมมิด ปรากฏว่าน้ำล้นออกมาไม่เกิน {p['overflow']:,} "
                    f"ลูกบาศก์เซนติเมตร ถ้าน้ำหนักรวมของลูกบาศก์ที่หย่อนลงไปเท่ากับ {_num(kilos)} กิโลกรัม "
                    f"แล้ว m มีค่ามากที่สุดเท่ากับเท่าใด  (หมายเหตุ: ตามหลักของอาร์คิมีดีส เมื่อนำวัตถุใส่ลงใน"
                    f"ภาชนะที่มีน้ำเต็ม ปริมาตรน้ำที่ล้นออกมาเท่ากับปริมาตรของวัตถุส่วนที่จมน้ำ)"),
            hint=r"200i + 400j = W,\quad 27i + 8j \le V,\quad m = i + j",
            distractors=_distinct(answer, [str(v) for v in (
                _most_cubes_by_weight(p["weight"]),     # forgot the overflow limit
                value - 1, value + 1, value - 2,
                p["weight"] // 400) if v > 0]))


@question_type("math.posn2564_q24", display_name={"th": "เส้นผ่านศูนย์กลางกับคอร์ดที่ตัดกัน — หา AD²"},
               level=LEVEL, topic="เรขาคณิตวงกลม")
class DiameterChords(SheetProblem):
    def expr(self, rng: Random):
        ae_sq, be, gap = rng.choice(POOL24)
        whole, coeff, rad = _q24_exact(ae_sq, be, gap)
        assert math.isclose(SOLVE[24](ae_sq=ae_sq, be=be, gap=gap), whole + coeff * math.sqrt(rad))
        answer = _surd_sum(whole, coeff, rad)
        return MathDraw(
            "", answer,
            prompt=(f"จากรูป วงกลมวงหนึ่งมี AD เป็นเส้นผ่านศูนย์กลาง และคอร์ด AC ตัดกับคอร์ด BD ที่จุด E "
                    f"ถ้า AE = √{ae_sq} หน่วย, BE = {be} หน่วย และ CD − CE = {gap} หน่วย "
                    f"แล้วจงหาค่าของ AD²"),
            hint=r"AD \text{ เป็นเส้นผ่านศูนย์กลาง} \Rightarrow \angle ABD = \angle ACD = 90^\circ,\quad AE \cdot EC = BE \cdot ED",
            distractors=_distinct(answer, [
                _surd_sum(whole, coeff, rad, "-"),              # sign slip in (√13 + c)²
                _num(whole),                                    # dropped the cross term
                _surd_sum(whole - ae_sq, coeff, rad),           # left AE² out of AC²
                _surd_sum(whole + coeff, coeff, rad),
                _num(whole + coeff)]))


@question_type("math.posn2564_q25", display_name={"th": "ตัวดำเนินการ x ⊕ y = xy/(x + y)"},
               level=LEVEL, topic="ตัวดำเนินการนิยามใหม่")
class HarmonicOperation(SheetProblem):
    def expr(self, rng: Random):
        terms, width = rng.choice(POOL25)
        value = Fraction(SOLVE[25](terms=terms, width=width))
        answer = _num(value)
        chain = f"({_block(1, width)}) ⊕ ({_block(2, width)}) ⊕ ⋯ ⊕ ({_block(terms, width)})"
        return MathDraw(
            "", answer,
            prompt=(f"สำหรับจำนวนจริงบวก x และ y กำหนด x ⊕ y = xy/(x + y) ซึ่งมีสมบัติการเปลี่ยนกลุ่ม "
                    f"จงหาค่าของ {chain} (ตอบเป็นเศษส่วนอย่างต่ำ)"),
            hint=r"\frac{1}{x \oplus y} = \frac{1}{x} + \frac{1}{y}",
            distractors=_distinct(answer, [_num(v) for v in (
                1 / value,                                                  # stopped at the sum of reciprocals
                Fraction(SOLVE[25](terms=terms - 1, width=width)),          # one term short
                Fraction(SOLVE[25](terms=terms + 1, width=width)),
                value * (width - 1),                                        # dropped the 1/(width−1)
                2 * value)]))


@question_type("math.posn2564_q26", display_name={"th": "ค่า t ที่อสมการเศษส่วนเป็นจริงสำหรับทุก x"},
               level=LEVEL, topic="อสมการและช่วง")
class UniformInequality(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL26)
        low, high = SOLVE[26](**p)
        left = _q26_side(p["lo"], p["a"], p["c"], 1, 2, 1)
        right = _q26_side(p["hi"], p["a"], p["c"], 1, 2, -1)
        answer = _interval(low, high)
        c = p["c"]
        return MathDraw(
            rf"{p['lo']} < \frac{{{p['a'] if p['a'] != 1 else ''}x^2 + tx - {-c}}}{{x^2 + x + 2}} < {p['hi']}",
            answer,
            prompt="จงหาจำนวนจริง t ทั้งหมดที่ทำให้อสมการต่อไปนี้เป็นจริงสำหรับทุกจำนวนจริง x",
            hint=r"x^2 + x + 2 > 0 \text{ เสมอ จึงคูณตลอดได้ แล้วใช้ } b^2 - 4ac < 0",
            distractors=_distinct(answer, [
                _interval(*left), _interval(*right),         # kept one side only
                _interval(low, high, strict=False),          # closed the ends
                _interval(min(left[0], right[0]), max(left[1], right[1]))]))   # took the union


@question_type("math.posn2564_q27", display_name={"th": "จำนวนมากสุดที่มีตัวประกอบที่กำหนดและมีตัวหารตามจำนวน"},
               level=LEVEL, topic="ตัวหารและการแยกตัวประกอบ")
class MostDivisors(SheetProblem):
    def expr(self, rng: Random):
        base, divisors = rng.choice(POOL27)
        pairs = SOLVE[27](base=base, divisors=divisors)
        answer = _power_tex(pairs)
        primes = sorted(set(_factor_small(base)) | set(_factor_small(divisors)))
        note = ", ".join(str(p) for p in primes if p > 7)
        swapped = tuple((p, e) for (p, _), (_, e) in zip(pairs, reversed(pairs)))
        return MathDraw(
            "", answer,
            prompt=(f"จงหาจำนวนเต็มบวกที่มากที่สุดซึ่งมี {base} เป็นตัวประกอบ และมีจำนวนตัวหารบวกทั้งหมด "
                    f"{divisors} จำนวนพอดี" + (f" (หมายเหตุ: {note} เป็นจำนวนเฉพาะ)" if note else "")),
            hint=r"n = p^a q^b \Rightarrow \text{จำนวนตัวหาร} = (a+1)(b+1)",
            distractors=_distinct(answer, [
                _power_tex(swapped),                                         # the other assignment
                _power_tex(tuple((p, e + 1) for p, e in pairs)),             # used the factors as exponents
                _power_tex(((pairs[0][0], divisors - 1),)),                  # one prime only
                _power_tex(tuple((p, e - 1) for p, e in pairs if e > 1)) or "1"]))


@question_type("math.posn2564_q28", display_name={"th": "ระบบสมการเลขยกกำลัง (√x)^(x+y) = y^p"},
               level=LEVEL, topic="ระบบสมการเลขยกกำลัง")
class PowerSystem(SheetProblem):
    def expr(self, rng: Random):
        p, q = rng.choice(POOL28)
        found = SOLVE[28](p=p, q=q)
        answer = _pairs(found)
        big = [pair for pair in found if pair != (1, 1)][0]
        return MathDraw(
            "", answer,
            prompt=(f"จงหาคู่อันดับ (x, y) ของจำนวนเต็มบวกทั้งหมดที่สอดคล้องกับระบบสมการ "
                    f"(√x)^(x + y) = y^{p} และ (√y)^(x + y) = x^{q}"),
            hint=r"\text{อย่าลืมกรณี } x = y = 1 \text{ ที่หายไปเมื่อหารด้วย } \ln x \ln y",
            distractors=_distinct(answer, [
                _pairs([big]),                         # lost (1, 1)
                _pairs([(1, 1), big[::-1]]),           # swapped x and y
                _pairs([(1, 1)]),
                _pairs([big[::-1]])]))


@question_type("math.posn2564_q29", display_name={"th": "จำนวนตรรกยะ a/b ระหว่าง 0 กับ 1 ที่ ab = n!"},
               level=LEVEL, topic="ทฤษฎีจำนวน: การนับ")
class FactorialFractions(SheetProblem):
    def expr(self, rng: Random):
        n = rng.randint(8, 40)
        value = SOLVE[29](n=n)
        omega = _prime_count(n)
        answer = f"{value:,}"
        return MathDraw(
            "", answer,
            prompt=(f"ให้ A เป็นเซตของจำนวนตรรกยะ r = a/b ทั้งหมดที่อยู่ระหว่าง 0 และ 1 โดยที่ a และ b เป็น"
                    f"จำนวนเต็มบวกซึ่ง ห.ร.ม. ของ a และ b เท่ากับ 1 และ ab = {n}·{n - 1}·{n - 2}⋯3·2·1 "
                    f"จงหาจำนวนสมาชิกของ A"),
            hint=r"\text{จำนวนเฉพาะแต่ละตัวของ } n! \text{ ต้องไปอยู่ที่ } a \text{ หรือ } b \text{ ทั้งก้อน}",
            distractors=_distinct(answer, [f"{v:,}" for v in (
                2 ** omega,                # kept both a/b and b/a
                omega,                     # counted the primes
                2 ** (omega - 2),
                2 ** omega - 1)]))


@question_type("math.posn2564_q30", display_name={"th": "สี่เหลี่ยมมุมฉากห้ารูป — พื้นที่ส่วนที่แรเงา"},
               level=LEVEL, topic="พื้นที่รูปสี่เหลี่ยม")
class ShadedRectangle(SheetProblem):
    def expr(self, rng: Random):
        a1, a2, a3, a4, a5 = rng.choice(POOL30)
        value = SOLVE[30](a1=a1, a2=a2, a3=a3, a4=a4, a5=a5)
        got = q30._layout(a1, a2, a3, a4, a5)
        answer = str(value)
        return MathDraw(
            "", answer,
            prompt=(f"จากรูป รูปสี่เหลี่ยมมุมฉากหมายเลข ①, ②, ③, ④ และ ⑤ มีพื้นที่ {a1}, {a2}, {a3}, {a4} "
                    f"และ {a5} ตารางหน่วย ตามลำดับ จงหาว่ารูปสี่เหลี่ยมมุมฉากที่แรเงามีพื้นที่กี่ตารางหน่วย"),
            hint=r"\text{พื้นที่ในแถวเดียวกันเป็นสัดส่วนกับความกว้าง พื้นที่ในคอลัมน์เดียวกันเป็นสัดส่วนกับความสูง}",
            distractors=_distinct(answer, [_num(v) for v in (
                got["a"] * got["w"],          # the shaded part under ③ only
                a3 + a4, a5, value + a1, 2 * value) if v > 0]))
