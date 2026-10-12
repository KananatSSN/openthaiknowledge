"""สมการเชิงเส้นบนเลขโดด

คณิตศาสตร์ · โอลิมปิก (สอวน.) · สอวน.
Indicators: —

Sets moved here from: olympiad.
"""

from __future__ import annotations

import math
from fractions import Fraction
from functools import lru_cache
from random import Random

from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem, frac_answer_tex, frac_tex
from otk.sheets import figure_attachments
from otk.sheets.posn2568_math import (
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


SHEET = "สอวน. ค่าย 1 (2568)"


SHEET_ID = "posn2568_math"


_MODULES = [q01, q02, q03, q04, q05, q06, q07, q08, q09, q10, q11, q12, q13,
            q14, q15, q16, q17, q18, q19, q20, q21, q22, q23, q24, q25, q26,
            q27, q28, q29, q30]


#: ``SOLVE[n]`` is question n's cached ``solve``. Cached because several are
#: searches and the distractor machinery re-draws a type a few times per item.
SOLVE = {n: lru_cache(maxsize=4096)(mod.solve)
         for n, mod in enumerate(_MODULES, start=1)}


def _num(value) -> str:
    """TeX for an exact number: integers bare, fractions as \\frac."""
    if isinstance(value, Fraction):
        return frac_answer_tex(value)
    if isinstance(value, float) and value == int(value):
        return str(int(value))
    return str(value)


def _deg(value) -> str:
    return rf"{_num(value)}^\circ"


def _pi(coefficient: str) -> str:
    """``coefficient`` × π, bracketed when it is a sum.

    ``17 + 11\\sqrt2`` has to render as ``(17 + 11√2)π``; without the brackets
    only the last term would look multiplied. A ``+``/``-`` inside braces (as in
    ``\\frac{17 + 11\\sqrt2}{3}``) is already grouped and needs nothing.
    """
    if coefficient == "1":
        return r"\pi"
    depth, compound = 0, False
    for ch in coefficient:
        depth += (ch == "{") - (ch == "}")
        if depth == 0 and ch in "+-":
            compound = True
    return rf"\left({coefficient}\right)\pi" if compound \
        else rf"{coefficient}\pi"


def _radical_pair(scale: Fraction, inner: str) -> str:
    """``scale`` times a radical expression, with 1 and integers tidied up."""
    if scale == 1:
        return inner
    if scale.denominator == 1:
        return rf"{scale.numerator}\left({inner}\right)"
    return rf"\frac{{{scale.numerator}}}{{{scale.denominator}}}\left({inner}\right)"


def _pool_q03() -> list[dict]:
    """Tanks whose new side scale k is a whole number and whose ``extra`` is an
    integer — otherwise the story would quote a fractional cubic metre."""
    out = []
    shapes = ((1, 2, 1), (1, 1, 1), (2, 3, 4), (1, 3, 2))
    stories = ((1, 4, 30), (1, 2, 20), (1, 5, 40), (3, 10, 45))
    for ratio_w, ratio_l, ratio_h in shapes:
        for k in (2, 3, 4, 5, 6):
            for increase_pct in (0, 25, 50, 60, 100):
                for used_num, used_den, remain_pct in stories:
                    capacity = Fraction(ratio_w * ratio_l * ratio_h * k ** 3)
                    volume = capacity / (1 + Fraction(increase_pct, 100))
                    drop = (1 - Fraction(used_num, used_den)
                            - Fraction(remain_pct, 100))
                    extra = volume * drop
                    if drop <= 0 or extra <= 0 or extra.denominator != 1:
                        continue
                    out.append(dict(used_num=used_num, used_den=used_den,
                                    extra=int(extra), remain_pct=remain_pct,
                                    ratio_w=ratio_w, ratio_l=ratio_l,
                                    ratio_h=ratio_h,
                                    increase_pct=increase_pct))
    return out


def _pool_q02() -> list[tuple[int, int]]:
    """(s, p) with p a perfect square and s² − 4√p a small perfect square.

    Both conditions are about keeping the *answer* writable: √p rational makes a
    rational, and s² − 4√p square makes b rational too.
    """
    out = []
    for s in range(4, 16):
        for t in range(0, 4):
            root4 = s * s - t * t
            if root4 <= 0 or root4 % 4:
                continue
            root = root4 // 4                          # √p
            if root >= 2:
                out.append((s, root * root))
    return out


def _pool_q06() -> list[dict]:
    """(K, C) whose four-real-root interval has whole-number endpoints."""
    out = []
    for q in (1, 2, 3):
        for p in range(q + 1, q + 5):
            for u4 in range(1, 61):                     # u = u4/4
                u = Fraction(u4, 4)
                k = u * q * q
                lo, hi = 2 * q * u * (p - q), u * (p * p - q * q)
                if k <= 0 or lo <= 0 or lo >= hi:
                    continue
                if lo.denominator != 1 or hi.denominator != 1:
                    continue
                c = k * hi
                if c.denominator != 1 or c > 10 ** 5:
                    continue
                out.append(dict(k_num=k.numerator, k_den=k.denominator,
                                c=int(c)))
    return out


def _pool_q07() -> list[dict]:
    """(A, B) where A − 2B is a perfect fifth power, so one root is rational."""
    out = []
    for b in range(1, 13):
        for d in (-32, -1, 1, 32):
            a = 2 * b + d
            if a > 0 and a != 2 * b:
                out.append(dict(a=a, b=b))
    return out


def _pool_q09() -> list[dict]:
    out = []
    for k in (20, 25, 30, 35, 40):
        applicants = 856 * k
        for pct in (10, 14, 20, 25, 30):
            male = Fraction(195 * k * pct, 100)
            if male.denominator != 1:
                continue
            for passed in (1350, 2025, 2700):
                for num in range(1, 136):
                    union = Fraction(passed * num, 135)
                    answer = union - male
                    if union.denominator == 1 and 0 < answer <= passed \
                            and answer.denominator == 1:
                        out.append(dict(applicants=applicants,
                                        male_pass_pct=pct, passed=passed,
                                        union_num=num, union_den=135))
    return out


def _pool_q13() -> list[dict]:
    out = []
    for a2 in range(2, 22):
        for a1 in range(1, 12):
            for a0 in range(0, 200, 7):
                p1, p10 = a0 + a1 + a2, a0 + 10 * a1 + 100 * a2
                if p10 > 4000:
                    continue
                out.append(dict(p1=p1, p10=p10, base=10))
    seen, unique = set(), []
    for entry in out:
        key = (entry["p1"], entry["p10"])
        if key not in seen and SOLVE[13](**entry) is not None:
            seen.add(key)
            unique.append(entry)
        if len(unique) >= 40:
            break
    return unique


def _pool_q14() -> list[dict]:
    out = []
    for f1 in range(1, 6):
        for f3 in range(11, 17):
            for mean in (9, 10, 11):
                entry = dict(f1=f1, f2=8, f3=f3, mean=mean, median=mean,
                             mode=8, hi=40)
                if SOLVE[14](**entry) is not None:
                    out.append(entry)
    return out


def _pool_q18() -> list[dict]:
    out = []
    for budget in (30000, 36000, 39600, 42000, 48000):
        for max_boxes in (450, 500, 580, 620, 700):
            for ratio in (1, 2, 3):
                entry = dict(p1=90, p2=60, p3=30, budget=budget,
                             max_boxes=max_boxes, ratio=ratio)
                if SOLVE[18](**entry):
                    out.append(entry)
    return out


def _pool_q23() -> list[dict]:
    """(r, R) where R(R+2r) is a perfect square, so BD and the area stay exact."""
    out = []
    for r in range(1, 41):
        for big in range(1, 61):
            value = big * (big + 2 * r)
            root = math.isqrt(value)
            if root * root == value:
                out.append(dict(r=r, big_r=big))
    return out


def _pool_q30() -> list[dict]:
    out = []
    for deg_a in (4, 5):
        for deg_d in (2, 3):
            for deg_g in (2, 3):
                entry = dict(deg_a=deg_a, deg_b=4, deg_c=4, deg_d=deg_d,
                             deg_g=deg_g)
                if SOLVE[30](**entry) is not None:
                    out.append(entry)
    return out


POOL02, POOL03 = _pool_q02(), _pool_q03()


POOL06, POOL07 = _pool_q06(), _pool_q07()


POOL09, POOL13, POOL14 = _pool_q09(), _pool_q13(), _pool_q14()


POOL18, POOL23, POOL30 = _pool_q18(), _pool_q23(), _pool_q30()


# Weight sets for §19: a small fixed pool so the 3⁶ search stays cached.
WEIGHTS19 = [(2, 5, 6, 8), (1, 1, 1, 1), (1, 2, 3, 4), (3, 1, 4, 1),
             (5, 4, 3, 2), (2, 2, 5, 5), (7, 3, 2, 1), (1, 5, 2, 6),
             (4, 4, 1, 9), (6, 2, 3, 3), (9, 1, 1, 2), (2, 8, 4, 1)]


#: ``key → (asset id, alt text)`` for the questions whose figure ships with the
#: sheet. Read from ``sheet.json`` rather than repeated here, so attaching a
#: figure with ``sheetpipe figures --attach`` is all it takes to make it appear.
FIGURES = figure_attachments(SHEET_ID)


class SheetProblem(WordProblem):
    """A โจทย์ from a digested sheet: Thai prompt, exact TeX answer.

    Where the sheet ships a figure for this question, every draw shows it — the
    diagram is part of the statement, and a question that says "อ่านจากรูป"
    with no รูป is not the question the sheet asked. A draw that asks something
    the figure does not depict opts out with ``MathDraw(figure=None)``.
    """

    sheet = SHEET
    sheet_id = SHEET_ID

    def default_figure(self) -> tuple[str, str]:
        return FIGURES.get(self.key, ("", ""))


@question_type("math.posn2568_q01", display_name={"th": "ค่ามากที่สุดของ a+b+c"},
               level=LEVEL, topic="สมการเชิงเส้นบนเลขโดด")
class MaxDigitSum(SheetProblem):
    def expr(self, rng: Random, cb_lo: int = 12, cb_hi: int = 40,
             cc_lo: int = 41, cc_hi: int = 70):
        cb, cc = rng.randint(cb_lo, cb_hi), rng.randint(cc_lo, cc_hi)
        a, b, c = (rng.randint(1, 9) for _ in range(3))
        total = a + cb * b + cc * c
        best = SOLVE[1](cb=cb, cc=cc, total=total, lo=1, hi=9)
        return MathDraw(
            rf"a + {cb}b + {cc}c = {total}", str(best),
            prompt="ถ้า a, b, c เป็นเลขโดด 1 ถึง 9 ที่สอดคล้องกับสมการต่อไปนี้ "
                   "จงหาค่ามากที่สุดของ a + b + c",
            hint=r"a = \text{total} - cb - cc",
            distractors=[str(a + b + c), str(best + 1), str(best - 1), "27",
                         str(best + 2), str(best - 2), "3"])


@question_type("math.posn2568_q02", display_name={"th": "ระบบสมการรากที่สอง"},
               level=LEVEL, topic="การจัดรูปพีชคณิต")
class RootSystem(SheetProblem):
    def expr(self, rng: Random):
        # s² − 4√p is kept a small perfect square, which is what makes b — and
        # so the answer — a tidy rational instead of a six-digit surd.
        s, p = rng.choice(POOL02)
        value = SOLVE[2](s=s, p=p)
        return MathDraw(
            rf"\sqrt{{a+b}} + \sqrt{{a-b}} = {s}, \qquad a^2 - b^2 = {p}",
            _num(value),
            prompt="ถ้า a และ b เป็นจำนวนจริงที่สอดคล้องกับระบบสมการต่อไปนี้ "
                   "จงหาค่าของ a² + 3b²",
            hint=r"u = \sqrt{a+b},\ v = \sqrt{a-b} \Rightarrow uv = \sqrt{p}",
            distractors=[_num(Fraction(s * s)), str(p), _num(value + 1),
                         _num(value - 1), _num(value * 2)])


@question_type("math.posn2568_q03", display_name={"th": "ถังน้ำทรงสี่เหลี่ยม"},
               level=LEVEL, topic="โจทย์ปัญหาปริมาตรและร้อยละ")
class WaterTank(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL03)
        area = SOLVE[3](**p)
        volume = q03.first_day_volume(p["used_num"], p["used_den"],
                                      p["extra"], p["remain_pct"])
        return MathDraw(
            "", _num(area),
            prompt=(f"วันแรกเติมน้ำเต็มถัง วันที่สองใช้ไป {p['used_num']}/"
                    f"{p['used_den']} ของปริมาตรวันแรก วันที่สามใช้เพิ่มอีก "
                    f"{p['extra']} ลูกบาศก์เมตร แล้วเหลือคิดเป็นร้อยละ "
                    f"{p['remain_pct']} ของวันแรก  ถังใบใหม่เป็นทรงสี่เหลี่ยม"
                    f"มุมฉากที่มีอัตราส่วน กว้าง : ยาว : สูง เป็น "
                    f"{p['ratio_w']} : {p['ratio_l']} : {p['ratio_h']} และ"
                    f"ความจุเพิ่มขึ้นร้อยละ {p['increase_pct']}  "
                    f"พื้นที่ฐานภายในของถังใบใหม่เท่ากับกี่ตารางเมตร"),
            distractors=[_num(volume), _num(area * 2), _num(area + 4),
                         _num(p["extra"]), _num(area + 1)])


@question_type("math.posn2568_q04", display_name={"th": "ผลคูณเทเลสโคป"},
               level=LEVEL, topic="พหุนามและการแยกตัวประกอบ")
class TelescopingProduct(SheetProblem):
    def expr(self, rng: Random, n_lo: int = 4, n_hi: int = 14):
        n = rng.randint(n_lo, n_hi)
        target = q04.ratio(n)
        total = SOLVE[4](target=int(target), n_max=200)
        return MathDraw(
            r"\frac{p(3)p(4)\cdots p(n)}{q(2)q(3)\cdots q(n-1)} = " + _num(target),
            str(total),
            prompt="กำหนดให้ p(x) = x³ + x + 2 และ q(x) = x³ + x − 2  "
                   "ถ้า A เป็นเซตของจำนวนเต็มบวก n ≥ 3 ทั้งหมดที่สอดคล้องกับ"
                   "สมการต่อไปนี้ จงหาผลบวกของสมาชิกทั้งหมดในเซต A",
            hint=r"\frac{(n-1)n(n+1)}{6}",
            distractors=[str(total + 1), str(total - 1), str(int(target))])


@question_type("math.posn2568_q05", display_name={"th": "ผลบวกเลขโดดของ (99…9)³"},
               level=LEVEL, topic="ทฤษฎีจำนวน: เลขโดด")
class RepdigitCubeDigits(SheetProblem):
    def expr(self, rng: Random, n_lo: int = 2, n_hi: int = 60):
        n = rng.randint(n_lo, n_hi)
        target = 18 * n
        return MathDraw(
            rf"S(N^3) = {target}", str(SOLVE[5](target=target)),
            prompt="ให้ S(m) แทนผลบวกของเลขโดดของ m ในระบบเลขฐานสิบ  "
                   "ถ้า N เป็นจำนวนเต็มบวกที่มี n หลัก โดยทุกหลักเป็นเลข 9 "
                   "และสอดคล้องกับเงื่อนไขต่อไปนี้ จงหาค่าของ n",
            hint=r"S(N^3) = 18n",
            distractors=[str(target), str(target // 9), str(n + 1)])


@question_type("math.posn2568_q06", display_name={"th": "ควอร์ติกที่มีรากจริง 4 ราก"},
               level=LEVEL, topic="สมการกำลังสี่")
class QuarticFourRoots(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL06)
        lo, hi = SOLVE[6](**p)
        k = Fraction(p["k_num"], p["k_den"])
        return MathDraw(
            rf"x^4 - ax^2 - {frac_answer_tex(k)}\,a + {p['c']} = 0",
            rf"{_num(int(lo))} < a < {_num(int(hi))}",
            prompt="จงหาเซตของจำนวนจริง a ทั้งหมดที่ทำให้สมการต่อไปนี้ "
                   "มีคำตอบเป็นจำนวนจริงที่แตกต่างกันทั้งหมด 4 คำตอบ",
            hint=r"t = x^2:\ t^2 - at + (C - Ka) = 0",
            distractors=[rf"a > {_num(int(lo))}", rf"a < {_num(int(hi))}",
                         rf"{_num(int(lo))} \le a \le {_num(int(hi))}",
                         rf"0 < a < {_num(int(hi))}"])


@question_type("math.posn2568_q07", display_name={"th": "ระบบสมการที่ยุบเป็น (x±y)⁵"},
               level=LEVEL, topic="ระบบสมการไม่เชิงเส้น")
class QuinticSystem(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL07)
        a, b = p["a"], p["b"]
        low = round((a - 2 * b) ** 0.2) if a > 2 * b else -round((2 * b - a) ** 0.2)
        high = a + 2 * b
        root_hi = rf"\sqrt[5]{{{high}}}"
        sign = "+" if low >= 0 else "-"
        x_tex = rf"\frac{{{root_hi} {sign} {abs(low)}}}{{2}}"
        y_tex = rf"\frac{{{root_hi} {'-' if low >= 0 else '+'} {abs(low)}}}{{2}}"
        return MathDraw(
            rf"\frac{{{a}}}{{2x}} + \frac{{{b}}}{{y}} = (3x^2+y^2)(x^2+3y^2),"
            rf"\qquad \frac{{{a}}}{{2x}} - \frac{{{b}}}{{y}} = 2(y^4-x^4)",
            rf"(x, y) = \left({x_tex},\ {y_tex}\right)",
            prompt="จงหาคู่อันดับ (x, y) ของจำนวนจริงที่สอดคล้องกับระบบสมการ"
                   "ต่อไปนี้",
            hint=r"(x+y)^5 = A + 2B,\qquad (x-y)^5 = A - 2B",
            distractors=[rf"(x, y) = \left({y_tex},\ {x_tex}\right)",
                         rf"(x, y) = \left({root_hi},\ {abs(low)}\right)",
                         rf"(x, y) = \left(\frac{{{root_hi}}}{{2}},"
                         rf"\ \frac{{{root_hi}}}{{2}}\right)"])


@question_type("math.posn2568_q08", display_name={"th": "จำนวน n ที่ทำให้ P(n) < 0"},
               level=LEVEL, topic="อสมการพหุนาม")
class NegativeProductCount(SheetProblem):
    def expr(self, rng: Random, m_lo: int = 4, m_hi: int = 16):
        m = rng.randint(m_lo, m_hi)
        count = SOLVE[8](m=m)
        return MathDraw(
            rf"P(x) = (x-1^2)(x-2^2)(x-3^2)\cdots(x-{m}^2)", str(count),
            prompt="จงหาว่ามีจำนวนเต็มบวก n ทั้งหมดกี่จำนวนที่ทำให้ P(n) < 0 "
                   "เมื่อกำหนด P ดังนี้",
            distractors=[str(m * m), str(count + 2 * m), str(count // 2 or 1)])


@question_type("math.posn2568_q09", display_name={"th": "นักเรียนผ่านการคัดเลือก"},
               level=LEVEL, topic="อัตราส่วนและความน่าจะเป็น")
class CampSelection(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL09)
        answer = SOLVE[9](**p)
        male = Fraction(195 * p["applicants"] // 856 * p["male_pass_pct"], 100)
        return MathDraw(
            "", _num(answer),
            prompt=(f"ผู้สมัครทั้งหมด {p['applicants']:,} คน อัตราส่วนนักเรียน "
                    f"ม.ต้น : ม.ปลาย เท่ากับ 5 : 3 และในกลุ่ม ม.ต้น อัตราส่วน"
                    f"นักเรียนหญิง : ชาย เท่ากับ 68 : 39  ผู้ผ่านการคัดเลือกรวม "
                    f"{p['passed']:,} คน โดยนักเรียนชาย ม.ต้น ที่ผ่านคิดเป็น"
                    f"ร้อยละ {p['male_pass_pct']} ของนักเรียนชาย ม.ต้น ที่สมัคร "
                    f"และความน่าจะเป็นที่สุ่มผู้ผ่านการคัดเลือก 1 คนแล้วได้"
                    f"นักเรียนชาย ม.ต้น หรือ นักเรียนหญิง ม.ปลาย เท่ากับ "
                    f"{p['union_num']}/{p['union_den']}  "
                    f"จงหาจำนวนนักเรียนหญิง ม.ปลาย ที่ผ่านการคัดเลือก"),
            distractors=[_num(male), _num(answer + male), _num(answer * 2)])


@question_type("math.posn2568_q10", display_name={"th": "ค่ามากที่สุดของ (x−y)z"},
               level=LEVEL, topic="ทฤษฎีจำนวนเชิงพีชคณิต")
class MaxXYZ(SheetProblem):
    def expr(self, rng: Random, r_lo: int = 2, r_hi: int = 4):
        for _ in range(60):
            r = rng.randint(r_lo, r_hi)
            x, z = rng.randint(1, 20), rng.randint(1, 20)
            if (x + z) % r:
                continue
            y = (x + z) // r
            total = x * x + y * y + z * z
            best = SOLVE[10](r=r, total=total)
            if best is not None:
                return MathDraw(
                    rf"x + z = {r}y, \qquad x^2 + y^2 + z^2 = {total}",
                    str(best),
                    prompt="ให้ x, y และ z เป็นจำนวนเต็มบวกที่สอดคล้องกับเงื่อนไข"
                           "ต่อไปนี้ จงหาค่ามากที่สุดของ (x − y)z",
                    distractors=[str(-best if best else 1), str(best + y),
                                 str(total - best)])
        raise RuntimeError("no solvable (r, total) found")     # pragma: no cover


@question_type("math.posn2568_q11", display_name={"th": "ผลคูณของ r + 1/r"},
               level=LEVEL, topic="รากของพหุนาม")
class ReciprocalRootProduct(SheetProblem):
    def expr(self, rng: Random, p_lo: int = 3, p_hi: int = 60):
        p = rng.randint(p_lo, p_hi)
        value = SOLVE[11](p=p)
        return MathDraw(
            rf"x^6 - {p}x^4 + {p}x^2 - 1 = 0",
            str(value),
            prompt="ให้ a, b, c, d, e, f เป็นจำนวนจริงที่แตกต่างกันและเป็นคำตอบ"
                   "ของสมการต่อไปนี้  จงหาค่าของ "
                   "(a + 1/a)(b + 1/b)(c + 1/c)(d + 1/d)(e + 1/e)(f + 1/f)",
            hint=r"u = x^2:\ (u-1)\left(u^2 - (p-1)u + 1\right) = 0",
            distractors=[str(-value), str(4 * (p + 1)), str(-4 * p * p)])


@question_type("math.posn2568_q12", display_name={"th": "จำนวนวิเศษสามหลัก"},
               level=LEVEL, topic="ทฤษฎีจำนวน: เลขโดด")
class MagicThreeDigit(SheetProblem):
    def expr(self, rng: Random, weight_hi: int = 3, scale_hi: int = 3):
        for _ in range(60):
            wa, wb, wc = (rng.randint(1, weight_hi) for _ in range(3))
            scale = rng.randint(1, scale_hi)
            count = SOLVE[12](wa=wa, wb=wb, wc=wc, scale=scale)
            # Reject the degenerate ends: "almost none" and "almost all three-digit
            # numbers" are both true but neither is a question worth asking.
            if 15 <= count <= 700:
                break
        else:                                                  # pragma: no cover
            raise RuntimeError("no non-degenerate weights found")
        terms = " + ".join(f"{w}{sym}" if w != 1 else sym
                           for w, sym in ((wa, "a"), (wb, "b"), (wc, "c")))
        return MathDraw(
            rf"d(n) = a^2 + b^2 + c^2, \qquad s(n) = {terms}, "
            rf"\qquad d(n) \le {scale}\,s(n)",
            str(count),
            prompt="จำนวนเต็มบวกสามหลัก n เขียนได้เป็น abc โดย a ≠ 0  "
                   "เรียก n ว่าจำนวนวิเศษถ้าสอดคล้องกับเงื่อนไขต่อไปนี้  "
                   "จงหาว่ามีจำนวนวิเศษทั้งหมดกี่จำนวน",
            distractors=[str(900 - count), str(count + 10), "900"])


@question_type("math.posn2568_q13", display_name={"th": "ค่ามากที่สุดของ |P(−1)|"},
               level=LEVEL, topic="พหุนามสัมประสิทธิ์จำนวนเต็ม")
class MaxPolyAtMinusOne(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL13)
        value = SOLVE[13](**p)
        return MathDraw(
            rf"a_k \ge k, \qquad P(1) = {p['p1']}, \qquad P(10) = {p['p10']}",
            str(value),
            prompt="ให้ P(x) = a₀ + a₁x + a₂x² + … + aₙxⁿ เป็นพหุนามที่มี"
                   "สัมประสิทธิ์เป็นจำนวนเต็มและสอดคล้องกับเงื่อนไขต่อไปนี้ "
                   "จงหาค่ามากที่สุดที่เป็นไปได้ของ |P(−1)|",
            distractors=[str(p["p1"]), str(-value), str(value + 22)])


@question_type("math.posn2568_q14", display_name={"th": "ชุดข้อมูลที่มีค่ากลางกำหนด"},
               level=LEVEL, topic="สถิติ: ค่ากลางของข้อมูล")
class ConstrainedDataset(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL14)
        span = SOLVE[14](**p)
        return MathDraw(
            rf"a,\ {p['f1']},\ b,\ {p['f2']},\ c,\ {p['f3']}", str(span),
            prompt=(f"กำหนดชุดข้อมูลต่อไปนี้ โดย a, b, c เป็นจำนวนเต็มบวก  "
                    f"ชุดข้อมูลนี้มีค่าเฉลี่ยเลขคณิตและมัธยฐานเท่ากับ "
                    f"{p['mean']} และมีฐานนิยมเท่ากับ {p['mode']}  "
                    f"จงหาผลบวกของค่าสูงสุดกับค่าต่ำสุดของชุดข้อมูลนี้"),
            distractors=[str(p["mean"] * 6), str(span + p["f1"]),
                         str(span - p["f1"])])


@question_type("math.posn2568_q15", display_name={"th": "การแจกของขวัญ"},
               level=LEVEL, topic="การนับและการจัดหมู่")
class GiftDistribution(SheetProblem):
    def expr(self, rng: Random, gifts_lo: int = 3, gifts_hi: int = 6,
             students_lo: int = 3, students_hi: int = 5):
        gifts = rng.randint(gifts_lo, gifts_hi)
        students = rng.randint(students_lo, students_hi)
        least = rng.randint(2, min(students, gifts))
        ways = SOLVE[15](gifts=gifts, students=students, least=least)
        return MathDraw(
            "", str(ways),
            prompt=(f"มีของขวัญที่แตกต่างกัน {gifts} ชิ้น แจกให้นักเรียน "
                    f"{students} คน โดยต้องแจกให้หมดทุกชิ้น และต้องมีนักเรียน"
                    f"ได้รับของขวัญอย่างน้อย {least} คน  "
                    f"จงหาจำนวนวิธีทั้งหมดในการแจก"),
            distractors=[str(students ** gifts), str(math.factorial(gifts)),
                         str(ways - math.factorial(min(gifts, students)))])


@question_type("math.posn2568_q16", display_name={"th": "ค่ามากที่สุดของ P + Q"},
               level=LEVEL, topic="ความน่าจะเป็น")
class BulbProbability(SheetProblem):
    def expr(self, rng: Random, n_lo: int = 10, n_hi: int = 40):
        for _ in range(40):
            n = rng.randint(n_lo, n_hi)
            mult = rng.randint(2, max(2, n // 2))
            value = SOLVE[16](n=n, mult=mult)
            if value is None:
                continue
            options = q16.admissible(n, mult)
            return MathDraw(
                "", frac_answer_tex(value),
                prompt=(f"กล่องที่ 1 และกล่องที่ 2 มีหลอดไฟกล่องละ {n} หลอด  "
                        f"แต่ละกล่องมีหลอดเสียอย่างน้อยหนึ่งหลอด จำนวนเท่ากัน "
                        f"และเป็นพหุคูณของ {mult}  สุ่มหยิบจากแต่ละกล่อง "
                        f"กล่องละ 1 หลอด ให้ P เป็นความน่าจะเป็นที่ได้หลอดดี"
                        f"ทั้งสอง และ Q เป็นความน่าจะเป็นที่ได้หลอดเสียทั้งสอง  "
                        f"จงหาค่ามากที่สุดที่เป็นไปได้ของ P + Q"),
                distractors=[frac_answer_tex(min(
                    q16._value(d, n) for d in options)),
                    frac_answer_tex(Fraction(1, 2)),
                    frac_answer_tex(1 - value)])
        raise RuntimeError("no admissible (n, mult) found")    # pragma: no cover


@question_type("math.posn2568_q17", display_name={"th": "ตอบถูกทั้งข้อ 1 และข้อ 2"},
               level=LEVEL, topic="หลักการรวมและการแยก")
class BothCorrect(SheetProblem):
    def expr(self, rng: Random, students_lo: int = 40, students_hi: int = 200):
        students = rng.randrange(students_lo, students_hi + 1, 10)
        cuts = sorted(rng.sample(range(1, students), 3))
        wrongs = [cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1],
                  students - cuts[2]]
        rng.shuffle(wrongs)
        corrects = [students - w for w in wrongs]
        answer = SOLVE[17](students=students, c1=corrects[0], c2=corrects[1],
                           c3=corrects[2], c4=corrects[3])
        listing = ", ".join(str(c) for c in corrects)
        return MathDraw(
            "", str(answer),
            prompt=(f"นักเรียน {students} คน สอบวิชาคณิตศาสตร์โอลิมปิกซึ่งมี"
                    f"ข้อสอบ 4 ข้อ  จำนวนผู้ตอบถูกแต่ละข้อคือ {listing} คน "
                    f"ตามลำดับ และไม่มีนักเรียนคนใดตอบถูกครบทั้ง 4 ข้อ  "
                    f"จงหาจำนวนนักเรียนที่ตอบถูกทั้งข้อ 1 และข้อ 2"),
            hint=r"c_1 + c_2 - N",
            distractors=[str(corrects[0] + corrects[1]), str(students - answer),
                         str(min(corrects[0], corrects[1]))])


@question_type("math.posn2568_q18", display_name={"th": "สั่งอาหารกล่องให้ครบงบ"},
               level=LEVEL, topic="การหาค่าเหมาะที่สุดเชิงจำนวนเต็ม")
class LunchBoxes(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL18)
        least = SOLVE[18](**p)
        return MathDraw(
            "", str(least),
            prompt=(f"โรงเรียนได้รับงบค่าอาหารกลางวัน {p['budget']:,} บาท "
                    f"และต้องใช้ให้หมดพอดี  อาหารกล่องมีราคา {p['p1']}, "
                    f"{p['p2']} และ {p['p3']} บาทต่อกล่อง  โดยจำนวนกล่องรวม"
                    f"ต้องไม่เกิน {p['max_boxes']} กล่อง และจำนวนกล่องราคา "
                    f"{p['p3']} บาท ต้องมีอย่างน้อย {p['ratio']} เท่าของจำนวน"
                    f"กล่องราคา {p['p2']} บาท  จงหาว่าต้องสั่งกล่องราคา "
                    f"{p['p1']} บาท อย่างน้อยที่สุดกี่กล่อง"),
            distractors=[str(p["budget"] // p["p1"]), str(least + 10),
                         str(p["max_boxes"] - least)])


@question_type("math.posn2568_q19", display_name={"th": "คะแนนรวมของ 4 ทีม"},
               level=LEVEL, topic="การให้เหตุผลเชิงตรรกะ")
class GroupStageScores(SheetProblem):
    def expr(self, rng: Random):
        w1, w2, w3, w4 = rng.choice(WEIGHTS19)
        value = SOLVE[19](w1=w1, w2=w2, w3=w3, w4=w4)
        return MathDraw(
            rf"{w1}a + {w2}b + {w3}c + {w4}d", str(value),
            prompt="4 ทีมแข่งขันแบบพบกันหมด ชนะได้ 3 คะแนน เสมอได้ทีมละ 1 "
                   "คะแนน แพ้ได้ 0 คะแนน  เมื่อจบการแข่งขันพบว่า มีนัดที่จบ"
                   "ด้วยผลเสมอเพียง 1 นัด, มีเพียง 1 ทีมที่ชนะได้เพียง 1 นัด, "
                   "มีเพียง 1 ทีมที่ได้คะแนนรวมเป็นจำนวนคี่ และคะแนนรวมของ"
                   "แต่ละทีมไม่ซ้ำกัน  ถ้าคะแนนรวมเรียงจากมากไปน้อยเป็น "
                   "a, b, c, d จงหาค่าของนิพจน์ต่อไปนี้",
            hint=r"(a, b, c, d) = (7, 6, 4, 0)",
            distractors=[str(17), str(value + w1), str(3 * (w1 + w2 + w3 + w4))])


@question_type("math.posn2568_q20",
               display_name={"th": "สี่เหลี่ยมด้านขนานกับวงกลมแนบใน"},
               level=LEVEL, topic="เรขาคณิต: วงกลมแนบใน")
class ParallelogramIncircle(SheetProblem):
    #: θ → exact TeX for 4/(π·sin θ). Only angles with a writable sine.
    _EXACT = {90: r"\frac{4}{\pi}", 30: r"\frac{8}{\pi}", 150: r"\frac{8}{\pi}",
              45: r"\frac{4\sqrt{2}}{\pi}", 135: r"\frac{4\sqrt{2}}{\pi}",
              60: r"\frac{8\sqrt{3}}{3\pi}", 120: r"\frac{8\sqrt{3}}{3\pi}"}

    def expr(self, rng: Random, ask: int = 0):
        # ask = 0 draws per item; 1 is the sheet's own "minimum" question.
        mode = ask if ask in (1, 2) else rng.choice((1, 2))
        if mode == 1:
            SOLVE[20](theta_deg=0)                    # exercise the solver
            return MathDraw(
                "", self._EXACT[90],
                prompt="จงหาค่าต่ำสุดที่เป็นไปได้ของอัตราส่วนระหว่างพื้นที่ของ"
                       "รูปสี่เหลี่ยมด้านขนาน และพื้นที่ของวงกลมแนบในของ"
                       "รูปสี่เหลี่ยมดังกล่าว",
                hint=r"\frac{4}{\pi \sin\theta}",
                distractors=[r"\frac{\pi}{4}", r"\frac{2}{\pi}",
                             self._EXACT[45], self._EXACT[60]])
        theta = rng.choice([t for t in self._EXACT if t != 90])
        SOLVE[20](theta_deg=theta)
        answer = self._EXACT[theta]
        # No figure here: the sheet's drawing is a parallelogram at one fixed
        # angle, and this mode is the one that *names* the angle. Showing a
        # 70°-looking picture beside "มีมุมหนึ่งขนาด 30 องศา" invites the
        # student to measure it.
        # The dict maps supplementary angles to the same value, so distinct
        # values — not distinct keys — are what make distinct choices.
        others = [v for v in dict.fromkeys(self._EXACT.values()) if v != answer]
        return MathDraw(
            "", answer,
            prompt=(f"รูปสี่เหลี่ยมด้านขนานรูปหนึ่งมีวงกลมแนบใน และมีมุมหนึ่ง"
                    f"ขนาด {theta} องศา  จงหาอัตราส่วนระหว่างพื้นที่ของ"
                    f"รูปสี่เหลี่ยมนี้ กับพื้นที่ของวงกลมแนบใน"),
            hint=r"\frac{4}{\pi \sin\theta}",
            figure=None,
            distractors=others + [r"\frac{\pi}{4}", r"\frac{2}{\pi}"])


@question_type("math.posn2568_q21", display_name={"th": "เส้นสัมผัสร่วมของวงกลมสองวง"},
               level=LEVEL, topic="เรขาคณิต: เส้นสัมผัสวงกลม")
class CommonTangents(SheetProblem):
    def expr(self, rng: Random, ab_lo: int = 5, ab_hi: int = 24,
             diff_lo: int = 0, diff_hi: int = 6):
        for _ in range(60):
            ab = rng.randint(ab_lo, ab_hi)
            cd = rng.randint(ab + 1, ab + 20)
            diff = rng.randint(diff_lo, diff_hi)
            if (cd * cd - ab * ab) % 2:
                continue
            value = SOLVE[21](ab=ab, cd=cd, diff=diff)
            return MathDraw(
                rf"AB = {ab}, \qquad CD = {cd}, \qquad b - a = {diff}",
                frac_answer_tex(value),
                prompt="วงกลมเล็กรัศมี a หน่วย และวงกลมใหญ่รัศมี b หน่วย  "
                       "เส้นตรง l₁ เป็นเส้นสัมผัสร่วมภายในซึ่งสัมผัสวงกลมเล็ก"
                       "ที่จุด A และสัมผัสวงกลมใหญ่ที่จุด B  เส้นตรง l₂ เป็น"
                       "เส้นสัมผัสร่วมภายนอกซึ่งสัมผัสวงกลมเล็กที่จุด C และ"
                       "สัมผัสวงกลมใหญ่ที่จุด D  จงหาค่าของ a² + b²",
                hint=r"CD^2 = d^2 - (b-a)^2,\qquad AB^2 = d^2 - (a+b)^2",
                distractors=[str(cd * cd - ab * ab),
                             frac_answer_tex(value * 2),
                             str(cd * cd + ab * ab)])
        raise RuntimeError("no valid tangent lengths found")   # pragma: no cover


@question_type("math.posn2568_q22", display_name={"th": "ขนาดของ ∠AEB"},
               level=LEVEL, topic="เรขาคณิต: มุมในรูปสี่เหลี่ยม")
class QuadrilateralAngle(SheetProblem):
    #: (m² as a Fraction, how the ratio reads in Thai) → the answer is arctan.
    _CASES = [((1, 1), "AC = BD"),
              ((1, 2), "AC = √2 · BD"),
              ((1, 3), "AC = √3 · BD")]

    def expr(self, rng: Random, ask: int = 0):
        idx = ask - 1 if 1 <= ask <= len(self._CASES) else \
            rng.randrange(len(self._CASES))
        (num, den), phrase = self._CASES[idx]
        angle = round(SOLVE[22](m_sq_num=num, m_sq_den=den,
                                foot_num=1, foot_den=2))
        others = [_deg(round(SOLVE[22](m_sq_num=n, m_sq_den=d,
                                       foot_num=1, foot_den=2)))
                  for (n, d), _ in self._CASES]
        return MathDraw(
            "", _deg(angle),
            prompt=(f"กำหนดให้ ABCD เป็นรูปสี่เหลี่ยม โดยมี AD = CD, {phrase} "
                    f"และ AB̅ ตั้งฉากกับ AC̅  ให้ E เป็นจุดตัดของ AC̅ และ BD̅  "
                    f"จงหาขนาดของ ∠AEB (เป็นองศา)"),
            hint=r"\tan\angle AEB = 2\sqrt{m^2 - \tfrac14}",
            distractors=[a for a in others if a != _deg(angle)]
                        + [_deg(90 - angle), _deg(angle * 2), _deg(180 - angle),
                           _deg(angle // 2)])


@question_type("math.posn2568_q23", display_name={"th": "พื้นที่ของรูปสามเหลี่ยม ABE"},
               level=LEVEL, topic="เรขาคณิต: วงกลมสัมผัสกัน")
class TangentCirclesArea(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL23)
        area = SOLVE[23](**p)
        r, big = p["r"], p["big_r"]
        return MathDraw(
            "", _num(Fraction(area).limit_denominator(10 ** 6)),
            prompt=(f"วงกลมเล็กมีจุดศูนย์กลางที่จุด A และรัศมียาว {r} หน่วย  "
                    f"วงกลมใหญ่มีจุดศูนย์กลางที่จุด B และรัศมียาว {big} หน่วย  "
                    f"วงกลมทั้งสองสัมผัสกันภายนอกที่จุด C  ให้ l₁ เป็นเส้นตรง"
                    f"ผ่านจุด B และสัมผัสวงกลมเล็กที่จุด D  ให้ l₂ เป็นเส้น"
                    f"สัมผัสร่วมของวงกลมทั้งสองที่จุด C  ให้ E เป็นจุดตัดของ "
                    f"l₁ และ l₂  จงหาพื้นที่ของรูปสามเหลี่ยม ABE"),
            hint=r"EC = \frac{rR}{\sqrt{R^2 + 2rR}}",
            distractors=[str(r * big), str((r + big) ** 2),
                         _num(Fraction(area * 2).limit_denominator(10 ** 6))])


@question_type("math.posn2568_q24", display_name={"th": "ครึ่งวงกลมซ้อนกัน"},
               level=LEVEL, topic="เรขาคณิต: ครึ่งวงกลมซ้อน")
class StackedSemicircles(SheetProblem):
    def expr(self, rng: Random, d_lo: int = 2, d_hi: int = 24):
        diameter = rng.randint(d_lo, d_hi)
        SOLVE[24](diameter=diameter, levels=2)     # keeps the solver in the loop
        scale = Fraction(diameter, 4)
        answer = _radical_pair(scale, r"\sqrt{6} - \sqrt{2}")
        return MathDraw(
            "", answer,
            prompt=(f"ให้ S เป็นครึ่งวงกลมใหญ่ที่มี AB̅ เป็นเส้นผ่านศูนย์กลาง"
                    f"ยาว {diameter} หน่วย และมีจุดศูนย์กลางที่จุด O  ภายใน S "
                    f"มีครึ่งวงกลมเล็ก 2 รูปวางเรียงซ้อนกันในแนวดิ่ง โดยรูปแรก"
                    f"มีเส้นผ่านศูนย์กลาง CD̅ ขนานกับ AB̅ และส่วนโค้งสัมผัส AB̅ "
                    f"ที่จุด O  ส่วนรูปที่สองมีเส้นผ่านศูนย์กลาง EF̅ ขนานกับ "
                    f"AB̅ และส่วนโค้งสัมผัส CD̅  จงหาความยาวของ EF̅"),
            hint=r"y_i = \frac{y_{i-1} + \sqrt{2R^2 - y_{i-1}^2}}{2}",
            distractors=[_radical_pair(scale, r"\sqrt{6} + \sqrt{2}"),
                         _radical_pair(Fraction(diameter, 2), r"\sqrt{2}"),
                         _radical_pair(scale, r"\sqrt{3} - 1")])


@question_type("math.posn2568_q25", display_name={"th": "ขนาดของ ∠ABC"},
               level=LEVEL, topic="เรขาคณิต: สามเหลี่ยมมุมฉาก")
class RightTriangleCevian(SheetProblem):
    def expr(self, rng: Random, alpha_lo: int = 35, alpha_hi: int = 59):
        alpha = rng.choice([a for a in range(alpha_lo, alpha_hi + 1)
                            if a != 45])
        beta = SOLVE[25](alpha_deg=alpha)
        return MathDraw(
            r"\frac{1}{AP} + \frac{1}{BP} = \frac{2}{CP}", _deg(beta),
            prompt=(f"กำหนดให้ ABC เป็นรูปสามเหลี่ยมมุมฉากที่มี ∠BCA = 90°  "
                    f"ให้ P เป็นจุดบน AB̅ ซึ่ง**ไม่ใช่จุดกึ่งกลางของ AB̅** และ"
                    f"ทำให้เงื่อนไขต่อไปนี้เป็นจริง  ถ้า ∠ACP = {alpha}° "
                    f"แล้วขนาดของ ∠ABC เท่ากับกี่องศา"),
            hint=r"\cos(\beta - \alpha) = \sin 2\alpha",
            # 90 − α is the *other*, degenerate branch: the mistake this item exists
            # to catch, so it leads the distractor list.
            distractors=[_deg(90 - alpha), _deg(alpha), _deg(90 - beta)])


@question_type("math.posn2568_q26", display_name={"th": "ขนาดของ ∠AFE"},
               level=LEVEL, topic="เรขาคณิต: วงกลมล้อมรูปสามเหลี่ยม")
class InscribedTriangleAngle(SheetProblem):
    def expr(self, rng: Random, abc_lo: int = 20, abc_hi: int = 85):
        abc = rng.randint(abc_lo, abc_hi)
        acb = rng.randint(20, 175 - abc)
        angle = SOLVE[26](abc_deg=abc, acb_deg=acb)
        return MathDraw(
            "", _deg(angle),
            prompt=(f"ABC เป็นรูปสามเหลี่ยมแนบในวงกลม โดยมี ∠ABC = {abc}° "
                    f"และ ∠ACB = {acb}°  ให้ DE̅ เป็นเส้นผ่านศูนย์กลางของวงกลม"
                    f"ที่ตัด AB̅ ที่จุด F และ AD̅ แบ่งครึ่ง ∠BAC  "
                    f"จงหาขนาดของ ∠AFE (เป็นองศา)"),
            hint=r"\angle AFE = 90^\circ - \angle ABC",
            distractors=[_deg(90 - acb), _deg(180 - abc - acb),
                         _deg((180 - abc - acb) / 2)])


@question_type("math.posn2568_q27", display_name={"th": "นับสี่เหลี่ยมที่เลี่ยงช่องดำ"},
               level=LEVEL, topic="การนับเชิงการจัด")
class BlockedRectangles(SheetProblem):
    def expr(self, rng: Random, size_lo: int = 4, size_hi: int = 8,
             blocks_lo: int = 1, blocks_hi: int = 5):
        rows = rng.randint(size_lo, size_hi)
        cols = rng.randint(size_lo, size_hi)
        count = rng.randint(blocks_lo, min(blocks_hi, rows * cols))
        blocked = tuple(sorted(rng.sample(
            [(r, c) for r in range(rows) for c in range(cols)], count)))
        total = SOLVE[27](rows=rows, cols=cols, blocked=blocked)
        listing = ", ".join(f"({r + 1}, {c + 1})" for r, c in blocked)
        plain = math.comb(rows + 1, 2) * math.comb(cols + 1, 2)
        return MathDraw(
            "", str(total),
            prompt=(f"กำหนดตารางขนาด {rows}×{cols} โดยมีช่องสีดำอยู่ที่ตำแหน่ง "
                    f"(แถว, หลัก) ดังนี้: {listing}  จงหาจำนวนของรูปสี่เหลี่ยม"
                    f"มุมฉากทั้งหมดที่สร้างขึ้นได้โดยลากเส้นตามแนวเส้นในตาราง "
                    f"โดยต้องไม่มีช่องสีดำใด ๆ อยู่ภายในเลย"),
            distractors=[str(plain), str(plain - total), str(total + count)])


@question_type("math.posn2568_q28", display_name={"th": "ความยาวส่วนโค้งของสายพาน"},
               level=LEVEL, topic="เรขาคณิต: ความยาวส่วนโค้ง")
class TrackBeltArcs(SheetProblem):
    #: The wrap angles only come out whole when R/r is this ratio — which is
    #: exactly why the sheet chose 3 + 2√2 for a unit small wheel.
    _RATIO = 3 + 2 * math.sqrt(2)

    def expr(self, rng: Random, r_lo: int = 1, r_hi: int = 6,
             n_lo: int = 2, n_hi: int = 5):
        r = rng.randint(r_lo, r_hi)
        n_small = rng.randint(n_lo, n_hi)
        gap = rng.randint(1, 3)
        SOLVE[28](big_r=r * self._RATIO, small_r=r, n_small=n_small, gap=gap)
        # (17r + 11r√2)π/3, reduced — r = 3 must read (17 + 11√2)π, not
        # (51 + 33√2)π/3.
        g = math.gcd(17 * r, 11 * r, 3)
        num_tex = (rf"{17 * r // g} + {11 * r // g}\sqrt{{2}}"
                   if 11 * r // g != 1 else r"17 + \sqrt{2}")
        answer = _pi(num_tex if 3 // g == 1
                     else rf"\frac{{{num_tex}}}{{{3 // g}}}")
        return MathDraw(
            "", answer,
            prompt=(f"ชุดล้อตีนตะขาบประกอบด้วยวงล้อใหญ่ 2 วง รัศมียาว "
                    f"{3 * r} + {2 * r}√2 หน่วย และ"
                    f"วงล้อเล็ก {n_small} วง รัศมียาว {r} หน่วย เรียงกันโดยมี"
                    f"ระยะห่างระหว่างวงล้อเล็กแต่ละคู่เท่ากับ {gap} หน่วย  "
                    f"สายพานคล้องรอบชุดล้อนี้  จงหาความยาวรวมของสายพาน"
                    f"เฉพาะส่วนที่เป็นส่วนโค้งของวงกลม"),
            hint=r"165^\circ + 165^\circ + 30^\circ = 360^\circ",
            # The sheet's picture has three small wheels drawn in it, so it is
            # only this question's picture when the draw asks for three.
            figure=None if n_small != 3 else "",
            distractors=[_pi(rf"\frac{{{17 * r} - {11 * r}\sqrt{{2}}}}{{3}}"),
                         _pi(str(2 * r)),
                         _pi(rf"\frac{{{11 * r}\sqrt{{2}}}}{{3}}"),
                         _pi(rf"\frac{{{17 * r}}}{{3}}")])


@question_type("math.posn2568_q29", display_name={"th": "ทรงกลมล้อมรอบทรงสี่หน้า"},
               level=LEVEL, topic="เรขาคณิตสามมิติ")
class TetrahedronSphere(SheetProblem):
    def expr(self, rng: Random, edge_lo: int = 1, edge_hi: int = 30):
        ad, bd, cd = (rng.randint(edge_lo, edge_hi) for _ in range(3))
        SOLVE[29](ad=ad, bd=bd, cd=cd)
        squares = ad * ad + bd * bd + cd * cd
        return MathDraw(
            rf"AD = {ad}, \qquad BD = {bd}, \qquad CD = {cd}",
            _pi(str(squares)),
            prompt="ให้ ABCD เป็นทรงสี่หน้าที่มีด้าน AD, BD และ CD ตั้งฉาก"
                   "ซึ่งกันและกัน  จงหาพื้นที่ผิวของทรงกลมที่ผ่านจุดยอดทั้งสี่",
            hint=r"2R = \sqrt{AD^2 + BD^2 + CD^2}",
            # frac_tex, not _num: the mixed-number form frac_answer_tex adds
            # ("300/7 = 42 6/7") contains an "=" and cannot be multiplied by π.
            distractors=[_pi(str(squares * 4)),
                         _pi(frac_tex(Fraction(squares, 4))),
                         _pi(frac_tex(Fraction(squares * 4, 3)))])


@question_type("math.posn2568_q30", display_name={"th": "ผังบ้านหมู่บ้านแสนสุข"},
               level=LEVEL, topic="ปริศนาเชิงตรรกะ")
class VillagePlan(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL30)
        best = SOLVE[30](**p)
        return MathDraw(
            "", str(best),
            prompt=(f"ผังหมู่บ้านเป็นตาราง 6 แถว 5 หลัก  บ้านของนาย A ถึง G "
                    f"อยู่ที่ (2,2), (2,4), (3,2), (3,4), (5,1), (5,4) และ "
                    f"(6,3) ตามลำดับ  ช่อง (1,1) และ (2,1) เป็นที่ดินว่าง  "
                    f"ช่อง (1,2), (1,3), (1,4), (3,1), (4,1) และ (4,4) มีบ้าน"
                    f"ของชาวบ้านคนอื่น  ช่องที่เหลืออาจมีบ้านหรือไม่มีก็ได้  "
                    f"บ้านสองหลังเป็นเพื่อนบ้านกันหากติดกันในแนวตั้ง แนวนอน "
                    f"หรือแนวทแยงมุม  ถ้านาย A มีเพื่อนบ้าน {p['deg_a']} หลัง, "
                    f"นาย B และนาย C มีคนละ {p['deg_b']} หลัง, นาย D มี "
                    f"{p['deg_d']} หลัง และนาย G มี {p['deg_g']} หลัง  "
                    f"จงหาค่ามากที่สุดที่เป็นไปได้ของผลรวมจำนวนเพื่อนบ้านของ"
                    f"นาย E กับนาย F"),
            distractors=[str(best + 1), str(best + 2), str(best - 1), "10"])
