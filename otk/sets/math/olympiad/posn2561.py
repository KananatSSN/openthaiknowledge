"""ปริศนาเชิงตรรกะ

คณิตศาสตร์ · โอลิมปิก (สอวน.) · สอวน.
Indicators: —

Sets moved here from: posn2561.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from math import comb, gcd
from random import Random

from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sheets import figure_attachments
from otk.sheets.posn2561_math import (
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


SHEET = "สอวน. ค่าย 1 (2561)"


SHEET_ID = "posn2561_math"


_MODULES = [q01, q02, q03, q04, q05, q06, q07, q08, q09, q10,
            q11, q12, q13, q14, q15, q16, q17, q18, q19, q20,
            q21, q22, q23, q24, q25, q26, q27, q28, q29, q30]


SOLVE = {n: lru_cache(maxsize=4096)(mod.solve)
         for n, mod in enumerate(_MODULES, start=1)}


FIGURES = figure_attachments(SHEET_ID)


class SheetProblem(WordProblem):
    """A โจทย์ from the 2561 sheet: Thai prompt, exact TeX answer."""

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


def _root_tex(radicand: int) -> str:
    """√n, reduced — ``6`` for 36, ``12\\sqrt{5}`` for 720."""
    outside, inside = 1, radicand
    factor = 2
    while factor * factor <= inside:
        while inside % (factor * factor) == 0:
            inside //= factor * factor
            outside *= factor
        factor += 1
    if inside == 1:
        return str(outside)
    head = "" if outside == 1 else str(outside)
    return rf"{head}\sqrt{{{inside}}}"


def _sum_root_tex(whole: int, radicand: int) -> str:
    """``a + b\\sqrt d``, collapsing to a plain integer when the root is whole."""
    tail = _root_tex(radicand)
    if tail.isdigit():
        return str(whole + int(tail))
    return f"{whole} + {tail}" if whole else tail


def _coef_root_tex(coef: Fraction, radicand: int) -> str:
    """``p/q``, ``p\\sqrt d`` or ``\\frac{p\\sqrt d}{q}``."""
    if radicand == 1:
        return frac_tex(coef)
    head = "" if abs(coef.numerator) == 1 else str(abs(coef.numerator))
    sign = "-" if coef < 0 else ""
    surd = rf"{head}\sqrt{{{radicand}}}"
    if coef.denominator == 1:
        return sign + surd
    return rf"{sign}\frac{{{surd}}}{{{coef.denominator}}}"


def _thai_int(value: int) -> str:
    """A negative number with the typographic minus the Thai prose uses."""
    return str(value) if value >= 0 else f"−{abs(value)}"


def _pow_tex(base: int, exponent: int) -> str:
    return str(base) if exponent == 1 else rf"{base}^{{{exponent}}}"


def _remainder_tex(slope: Fraction, intercept: Fraction) -> str:
    """``mx + n`` over a common denominator: ``\\frac{12x + 1}{5}``."""
    scale = (slope.denominator * intercept.denominator
             // gcd(slope.denominator, intercept.denominator))
    top, bottom = int(slope * scale), int(intercept * scale)
    if top == 0:
        body = str(bottom)
    else:
        head = "" if abs(top) == 1 else str(abs(top))
        body = ("-" if top < 0 else "") + head + "x"
        if bottom:
            body += f" {'-' if bottom < 0 else '+'} {abs(bottom)}"
    return body if scale == 1 else rf"\frac{{{body}}}{{{scale}}}"


def _percent(scale: Fraction) -> str:
    """"50" for 3/2 and for 1/2 — the direction is stated in words alongside."""
    change = (scale - 1) * 100 if scale > 1 else (1 - scale) * 100
    return str(int(change))


_TALLER = [Fraction(3, 2), Fraction(2), Fraction(5, 4), Fraction(11, 10),
           Fraction(7, 5), Fraction(9, 5), Fraction(3), Fraction(13, 10)]


_NARROWER = [Fraction(3, 4), Fraction(1, 2), Fraction(1, 4), Fraction(4, 5),
             Fraction(9, 10), Fraction(3, 5), Fraction(7, 10)]


#: only the pairs whose r/h comes out positive describe a real cylinder.
_CYLINDER_POOL = [(up, down) for up in _TALLER for down in _NARROWER
                  if q21.solve(height_scale=up, radius_scale=down) is not None]


@question_type("math.posn2561_q01",
               display_name={"th": "จำนวนการบ้านจากคำให้การจริงเท็จของนักเรียนห้าคน"},
               level=LEVEL, topic="ปริศนาเชิงตรรกะ")
class HomeworkTruthTellers(SheetProblem):
    """Round two fixes who is who; round one then names the number."""

    _NAMES = ("ก", "ข", "ค", "ง", "จ")

    @staticmethod
    def _pool() -> list[tuple]:
        """Claim sets that the sheet's accusation pattern pins to one number."""
        accusations = q01.PARAMS["accusations"]
        out = []
        for target in range(3, 21):
            claims = (("eq", target + 1), ("lt", target - 2),
                      ("in", (target + 1, target + 2)), ("le", target),
                      ("gt", target - 1))
            limit = target + 8
            if q01.solve(claims=claims, accusations=accusations,
                         limit=limit) == target:
                out.append((claims, accusations, limit, target))
        return out

    _POOL: list[tuple] = []

    def expr(self, rng: Random):
        if not self._POOL:
            HomeworkTruthTellers._POOL = self._pool()
        claims, accusations, limit, _ = rng.choice(self._POOL)
        value = SOLVE[1](claims=claims, accusations=accusations, limit=limit)

        def spoken(claim) -> str:
            op, val = claim
            if op == "eq":
                return f"ครูให้การบ้าน {val} ข้อครับ"
            if op == "lt":
                return f"ครูให้การบ้านไม่ถึง {val} ข้อครับ"
            if op == "le":
                return f"ครูให้การบ้านไม่เกิน {val} ข้อครับ"
            if op == "gt":
                return f"ครูให้การบ้านมากกว่า {val} ข้อครับ"
            return f"ครูให้การบ้าน {val[0]} ข้อ หรือ {val[1]} ข้อนี่แหละครับ"

        first = "  ".join(f"นาย {name} บอกว่า “{spoken(claim)}”"
                          for name, claim in zip(self._NAMES, claims))
        second = "  ".join(
            f"นาย {self._NAMES[speaker]} บอกว่า “"
            + " และ ".join(self._NAMES[who] for who, _ in targets)
            + (" พูดจริงครับ”" if targets[0][1] else " พูดโกหกครับ”")
            for speaker, targets in enumerate(accusations))
        return MathDraw(
            "", str(value),
            prompt=("คุณครูคณิตศาสตร์ถามนักเรียนชายในชั้นเรียน 5 คนถึงการบ้านที่ให้"
                    "ไว้ว่า “คาบที่แล้ว ครูให้การบ้านไว้กี่ข้อคะ” นักเรียนทั้ง 5 คน "
                    f"จึงตอบครูดังนี้  {first}  "
                    "หลังจากที่ครูยังไม่ได้ข้อสรุป จึงได้สอบถามนักเรียนแต่ละคนอีก"
                    f"ครั้งหนึ่ง จนได้ใจความดังนี้  {second}  "
                    "หากนักเรียนแต่ละคนพูดจริงเท่านั้นหรือพูดโกหกเท่านั้น "
                    "คาบที่แล้วครูให้การบ้านกี่ข้อ"),
            hint=r"\text{the second round alone fixes who lies; then read the "
                 r"first round with those labels}",
            distractors=_distinct(str(value), [
                str(value + 1), str(value - 1), str(value + 2),
                str(value - 2), str(value + 3), str(value * 2)]))


@question_type("math.posn2561_q02",
               display_name={"th": "เลขหลักหน่วยของกำลังที่ยกด้วยจำนวนหลัก"},
               level=LEVEL, topic="ทฤษฎีจำนวน: เลขโดด")
class UnitsDigitOfDigitCount(SheetProblem):
    #: (a, p, b, q) whose product is a clean power of ten times a small head.
    _SHAPES = [(25, 25, 8, 20), (4, 10, 5, 12), (2, 100, 5, 100), (25, 6, 8, 5),
               (5, 40, 2, 45), (125, 12, 2, 40), (8, 15, 5, 30)]

    def expr(self, rng: Random):
        a, p, b, q = rng.choice(self._SHAPES)
        base = rng.choice([2, 3, 7, 8, 9])
        value = SOLVE[2](a=a, p=p, b=b, q=q, base=base)
        return MathDraw(
            rf"m = \text{{digits}}\left({a}^{{{p}}} \times {b}^{{{q}}}\right)",
            str(value),
            prompt=(f"{base}^m มีเลขหลักหน่วยเป็นเลขใด เมื่อ m คือจำนวนหลักของ "
                    f"{a}^{p} × {b}^{q}"),
            hint=r"\text{pair the 2s and 5s into powers of ten, then use the "
                 r"period-4 cycle of last digits}",
            distractors=_distinct(str(value), [
                str((value + 1) % 10), str((value - 1) % 10),
                str(base % 10), str((value * 2) % 10), str((value + 4) % 10),
                str((value + 2) % 10)]))


@question_type("math.posn2561_q03",
               display_name={"th": "จำนวนน้อยที่สุดที่มีตัวประกอบตามจำนวนที่กำหนด"},
               level=LEVEL, topic="ตัวประกอบของจำนวนเต็ม")
class SmallestWithDivisorCount(SheetProblem):
    #: (divisor count, number of distinct primes) that a search can confirm.
    _POOL = [(d, k) for d in (12, 16, 18, 24, 30, 36, 40, 48, 60, 72)
             for k in (2, 3)
             if (lambda v: v is not None and v <= 3 * 10 ** 5)(
                 q03.solve(divisors=d, primes=k))]

    def expr(self, rng: Random):
        divisors, primes = rng.choice(self._POOL)
        value = SOLVE[3](divisors=divisors, primes=primes)
        word = {2: "สอง", 3: "สาม", 4: "สี่"}[primes]
        return MathDraw(
            rf"d(n) = {divisors}, \qquad \omega(n) = {primes}", str(value),
            prompt=(f"จงหาจำนวนนับที่น้อยที่สุดที่มีตัวประกอบทั้งหมด {divisors} "
                    f"จำนวน และเป็นตัวประกอบเฉพาะที่แตกต่างกันเพียง{word}จำนวน"),
            hint=r"(a+1)(b+1)(c+1) = d(n);\ \text{put the larger exponents on "
                 r"the smaller primes}",
            distractors=_distinct(str(value), [
                str(value * 2), str(value // 2), str(value + 2 * divisors),
                str(value * 3), str(value // 3 or 1), str(value + 1)]))


@question_type("math.posn2561_q04",
               display_name={"th": "ค่า m + n ที่น้อยที่สุดจาก ห.ร.ม. และ ค.ร.น."},
               level=LEVEL, topic="ห.ร.ม. และ ค.ร.น.")
class MinimalSumFromGcdLcm(SheetProblem):
    _POOL = [(g, g * q) for g in (1, 2, 3, 5, 6, 10, 12, 15, 20, 24, 30)
             for q in (60, 120, 180, 210, 360, 900, 1260, 2520)
             if q04.solve(g=g, lcm=g * q) is not None]

    def expr(self, rng: Random):
        g, lcm = rng.choice(self._POOL)
        value = SOLVE[4](g=g, lcm=lcm)
        return MathDraw(
            rf"\gcd(m, n) = {g}, \qquad \operatorname{{lcm}}(m, n) = {lcm}",
            str(value),
            prompt=("จงหาค่า m + n ที่น้อยที่สุด เมื่อกำหนดให้ m และ n เป็นจำนวนนับ"
                    f"ที่มี ห.ร.ม. และ ค.ร.น. เป็น {g} และ {lcm} ตามลำดับ"),
            hint=r"m = ga,\ n = gb \text{ with } \gcd(a,b) = 1 \text{ and } "
                 r"ab = \ell/g",
            distractors=_distinct(str(value), [
                str(g + lcm), str(value + g), str(value - g),
                str(2 * g * (lcm // g)), str(value + 2 * g), str(value * 2)]))


@question_type("math.posn2561_q05",
               display_name={"th": "จำนวน n ที่ทำให้ nᵏ บวกค่าคงที่หารลงตัว"},
               level=LEVEL, topic="การหารลงตัวและเศษเหลือ")
class ResidueCount(SheetProblem):
    _POOL = [(limit, shift, modulus, power)
             for modulus in (5, 7, 8, 9, 11)
             for power in (2, 3)
             for shift in range(1, 12)
             for limit in (100, 200, 300, 500)
             if (q05.solve(limit=limit, shift=shift, modulus=modulus,
                           power=power) or 0) > 0]

    def expr(self, rng: Random):
        limit, shift, modulus, power = rng.choice(self._POOL)
        value = SOLVE[5](limit=limit, shift=shift, modulus=modulus, power=power)
        exponent = "²" if power == 2 else "³"
        return MathDraw(
            rf"n^{{{power}}} + {shift} \equiv 0 \pmod{{{modulus}}}", str(value),
            prompt=(f"มีจำนวนเต็มบวก n ตั้งแต่ 1 ถึง {limit} ทั้งหมดกี่จำนวน "
                    f"ที่ n{exponent} + {shift} หารด้วย {modulus} ลงตัว"),
            hint=r"\text{only } n \bmod m \text{ matters; count the good "
                 r"residues and multiply by the cycles}",
            distractors=_distinct(str(value), [
                str(limit - value), str(value + modulus), str(value - modulus),
                str(limit // modulus), str(value * 2), str(value + 1)]))


@question_type("math.posn2561_q06",
               display_name={"th": "จำนวนที่เป็นผลบวกของจำนวนเรียงติดกันหลายความยาว"},
               level=LEVEL, topic="การหารลงตัวและเศษเหลือ")
class ConsecutiveRunLengths(SheetProblem):
    """An odd run length forces divisibility; an even one forbids it."""

    _SHAPES = [(3, 4, 5), (3, 5, 7), (2, 3), (3, 4), (5, 6), (3, 5), (2, 3, 5)]

    def expr(self, rng: Random):
        lengths = rng.choice(self._SHAPES)
        above = rng.choice([50, 100, 200, 350, 500, 1000])
        value = SOLVE[6](lengths=lengths, above=above)
        # the MathBlock must stay free of Thai, so the "และ" form is kept for
        # the prompt and the block gets a bare set instead.
        plain = ", ".join(str(k) for k in lengths)
        clauses = "  ".join(
            f"({chr(0x0E01 + i)}) n เป็นผลบวกของจำนวนเต็มบวกที่เรียงติดกัน {k} จำนวน"
            for i, k in enumerate(lengths))
        return MathDraw(
            rf"n > {above}, \qquad k \in \{{{plain}\}}", str(value),
            prompt=(f"กำหนดให้ n เป็นจำนวนเต็มบวกที่มากกว่า {above} "
                    f"จงหา n ที่น้อยที่สุดที่มีสมบัติว่า  {clauses}"),
            hint=r"k \text{ terms from } a:\ n = ka + \tfrac{k(k-1)}2",
            distractors=_distinct(str(value), [
                str(value + 1), str(value - 1), str(above + 1),
                str(value * 2), str(value + 30), str(value - 30)]))


@question_type("math.posn2561_q07",
               display_name={"th": "เศษจากการหารจำนวนที่ซ้ำบล็อกเดิมหลายพันหลัก"},
               level=LEVEL, topic="การหารลงตัวและเศษเหลือ")
class RepeatedBlockRemainder(SheetProblem):
    def expr(self, rng: Random):
        block = rng.choice(["73", "37", "142857", "12", "91", "58", "1234"])
        repeats = rng.randint(200, 2000)
        divisor = rng.choice([7, 11, 13, 37, 101, 41])
        value = SOLVE[7](block=block, repeats=repeats, divisor=divisor)
        digits = len(block) * repeats
        spelled = " และ ".join(sorted(set(block)))
        return MathDraw(
            rf"N = \overline{{{block}{block}\ldots{block}}}"
            rf"\ \ ({repeats}\ \text{{blocks}})", str(value),
            prompt=(f"กำหนดให้ N เป็นจำนวนเต็มที่มี {digits} หลัก ที่เกิดจากการเขียน "
                    f"“{block}” ต่อกัน {repeats} ครั้ง (ประกอบด้วยเลขโดด {spelled}) "
                    f"จงหาเศษจากการหาร N ด้วย {divisor}"),
            hint=r"N = B\left(1 + 10^{|B|} + 10^{2|B|} + \cdots\right);"
                 r"\ \text{the powers cycle}",
            distractors=_distinct(str(value), [
                str((value + 1) % divisor), str((value - 1) % divisor),
                str((value * 2) % divisor), str(divisor - value),
                str((value + 3) % divisor), str((value + 7) % divisor),
                # small divisors leave few residues, so keep a wide candidate
                # list or the choice set collapses.
                str((value + 4) % divisor), str((value + 5) % divisor),
                str((value + 6) % divisor), str((value + 8) % divisor)]))


@question_type("math.posn2561_q08",
               display_name={"th": "จำนวนสับเซตที่ผลบวกของสมาชิกน้อยสุดกับมากสุดคงที่"},
               level=LEVEL, topic="เพาเวอร์เซตและการนับสับเซต")
class MinMaxSumSubsets(SheetProblem):
    def expr(self, rng: Random):
        size = rng.randint(10, 30)
        target = rng.randint(3, 2 * size - 1)
        value = SOLVE[8](size=size, target=target)
        listed = ", ".join(str(i) for i in range(1, 6)) + f", …, {size}"
        return MathDraw(
            rf"A = \{{{listed}\}}, \qquad \min S + \max S = {target}",
            str(value),
            prompt=(f"กำหนดให้ A = {{{listed}}} จงหาจำนวนสับเซต S ของ A ซึ่งผลบวก"
                    "ของสมาชิกที่มีค่าน้อยที่สุดของ S กับสมาชิกที่มีค่ามากที่สุดของ S "
                    f"เท่ากับ {target}"),
            hint=r"\text{fix } (\min, \max);\ \text{everything strictly between "
                 r"is free}",
            distractors=_distinct(str(value), [
                str(value * 2), str(value // 2 or 1), str(value + 1),
                str(value - 1), str(2 ** size), str(value * 3)]))


@question_type("math.posn2561_q09",
               display_name={"th": "งบประมาณถมดินเมื่อชายฝั่งสองด้านยาวเท่ากัน"},
               level=LEVEL, topic="โจทย์ปัญหาปริมาตรและร้อยละ")
class IslandCoastBudget(SheetProblem):
    """The inland cut is not coastline, so each side is half the perimeter."""

    _POOL = [(ab, bc, ad) for ab in range(2, 9) for bc in range(3, 12)
             for ad in range(6, 26) if bc < ad]

    def expr(self, rng: Random):
        ab, bc, ad = rng.choice(self._POOL)
        north = rng.choice([3, 4, 5, 6, 8])
        south = rng.choice([9, 10, 12, 15])
        value = SOLVE[9](ab=ab, bc=bc, ad=ad, north=north, south=south)
        return MathDraw(
            rf"AB = {ab}, \quad BC = {bc}, \quad AD = {ad}", str(value),
            prompt=("เกาะแห่งหนึ่งเป็นรูปสี่เหลี่ยมที่มีมุมฉากที่ A และที่ B โดย "
                    f"AB = {ab} กม., BC = {bc} กม. และ AD = {ad} กม. "
                    "เจ้าของต้องการแบ่งเขตกลางเกาะเป็นเกาะฝั่งเหนือและเกาะฝั่งใต้ "
                    "จากจุด A ไปถึงจุด E บนด้าน CD เพื่อให้ความยาวรอบเกาะที่ติดทะเล"
                    "ของฝั่งเหนือเท่ากับความยาวรอบเกาะที่ติดทะเลของฝั่งใต้  "
                    f"หากผู้รับเหมาคิดราคาถมดินฝั่งเหนือกิโลเมตรละ {north} ล้านบาท "
                    f"ฝั่งใต้กิโลเมตรละ {south} ล้านบาท และขายเหมาเป็นหน่วยเต็ม"
                    "กิโลเมตร เจ้าของเกาะจะใช้งบประมาณกี่ล้านบาท"),
            hint=r"AE \text{ is inland: each side is half the whole coast}",
            # the crop on file is clipped and drops the labels, so it is not shipped
            distractors=_distinct(str(value), [
                str(value + north), str(value + south), str(value - north),
                str((ab + bc + ad) * (north + south)), str(value * 2),
                str(value - south)]))


@question_type("math.posn2561_q10",
               display_name={"th": "ค่ามากที่สุดของ x + y จากผลบวกกำลังสองและกำลังสาม"},
               level=LEVEL, topic="พหุนามสมมาตร")
class SymmetricSquareCubeMax(SheetProblem):
    #: (k, c, t) whose largest admissible sum is a whole number.
    _POOL = [(k, c, t) for k in (1, 2, 3) for c in range(2, 30)
             for t in range(-12, 13)
             if isinstance(q10.solve(k=k, c=c, t=t), int)]

    def expr(self, rng: Random):
        k, c, t = rng.choice(self._POOL)
        value = SOLVE[10](k=k, c=c, t=t)
        head = "" if k == 1 else str(k)
        return MathDraw(
            rf"{head}x^2 + {head}y^2 = {c}, \qquad x^3 + y^3 = {t}", str(value),
            prompt=("ให้ x, y เป็นจำนวนจริง โดยที่สอดคล้องกับสมการทั้งสองต่อไปนี้ "
                    "จงหาค่า x + y ที่มากที่สุด"),
            hint=r"s = x+y,\ p = xy:\ s^3 - 3ps = t \text{ and } s^2 \ge 4p",
            distractors=_distinct(str(value), [
                str(-value), str(value + 1), str(value - 1), str(value * 2),
                str(value + 3), str(value - 3)]))


@question_type("math.posn2561_q11",
               display_name={"th": "ค่า x² + y² จากสมการไดโอแฟนไทน์สองตัวแปร"},
               level=LEVEL, topic="ทฤษฎีจำนวนเชิงพีชคณิต")
class DiophantineSquareSum(SheetProblem):
    """``d = ax² + 1`` divides ``ac − b``, so the search space is a divisor list."""

    #: (a, b, c) vetted to leave exactly one value of x² + y². Built by choosing
    #: (a, x, y) first and solving for c, then confirmed with the solver — a
    #: blind sweep over (a, b, c) finds a solution in well under 1% of cases.
    _SHAPES = [(2, 96, 864), (1, 2, 22), (1, 2, 37), (1, 2, 76), (1, 2, 117),
               (1, 2, 142), (1, 2, 172), (1, 2, 312), (1, 2, 397), (1, 4, 54),
               (1, 4, 238), (1, 6, 992), (1, 8, 1138), (1, 50, 1197),
               (2, 2, 568), (2, 4, 1175), (2, 4, 1180), (2, 26, 1186),
               (2, 28, 1169), (3, 2, 234), (3, 2, 574), (3, 2, 752),
               (3, 2, 1045)]

    def expr(self, rng: Random):
        a, b, c = rng.choice(self._SHAPES)
        value = SOLVE[11](a=a, b=b, c=c)
        head = "" if a == 1 else str(a)
        return MathDraw(
            rf"y^2 + {head}x^2y^2 = {b}x^2 + {c}", str(value),
            prompt=("ให้ x และ y เป็นจำนวนเต็มที่สอดคล้องกับสมการต่อไปนี้ "
                    "จงหาค่าของ x² + y²"),
            hint=r"y^2(ax^2 + 1) = bx^2 + c \Rightarrow (ax^2+1) \mid (ac - b)",
            distractors=_distinct(str(value), [
                str(value + 1), str(value - 1), str(value + 2),
                str(value * 2), str(c // a if a else c), str(value + 5),
                str(abs(value - 9)), str(value + 9)]))


@question_type("math.posn2561_q12",
               display_name={"th": "จำนวนตัวแปรที่น้อยที่สุดเมื่อผลบวกกำลังสองมากกว่ากำลังสองของผลบวก"},
               level=LEVEL, topic="ค่าสัมบูรณ์และค่าสุดขีด")
class SmallestVariableCount(SheetProblem):
    """f is linear in each variable, so its supremum sits at a corner of the cube."""

    def expr(self, rng: Random):
        target = rng.choice([rng.randint(5, 60), rng.randint(100, 400),
                             rng.choice([2018, 2560, 2561, 2562, 1999])])
        value = SOLVE[12](target=target)
        return MathDraw(
            r"x_1^2 + x_2^2 + \cdots + x_n^2 = "
            rf"\left(x_1 + x_2 + \cdots + x_n\right)^2 + {target}",
            str(value),
            prompt=("ให้ x₁, x₂, …, xₙ เป็นจำนวนจริงโดยที่ |xᵢ| < 1 สำหรับ "
                    "i = 1, 2, …, n และสอดคล้องกับสมการต่อไปนี้ "
                    "จงหาค่า n ที่น้อยที่สุดที่ทำให้สมการนี้เป็นจริง"),
            hint=r"\sum x_i^2 - \left(\sum x_i\right)^2 \text{ is linear in each "
                 r"x_i, so look at } x_i = \pm 1",
            distractors=_distinct(str(value), [
                str(target), str(target + 1), str(target + 2), str(target + 3),
                str(2 * target), str(target - 1), str(target + 4)]))


@question_type("math.posn2561_q13",
               display_name={"th": "รากที่สามของนิพจน์ที่ยุบเป็นกำลังสามของผลต่าง"},
               level=LEVEL, topic="การจัดรูปพีชคณิต")
class HiddenCubeOfDifference(SheetProblem):
    """u³ − 3u²v + 3uv² − v³ in disguise — the printed grouping splits it wrong."""

    _SHAPES = [(3, 3, 5, 5), (2, 4, 3, 3), (5, 2, 2, 5), (10, 3, 3, 5),
               (2, 8, 5, 3), (3, 4, 7, 2), (7, 2, 2, 6), (5, 3, 3, 4),
               (2, 6, 7, 2), (11, 2, 5, 3)]

    def expr(self, rng: Random):
        a, m, b, k = rng.choice(self._SHAPES)
        value = SOLVE[13](a=a, m=m, b=b, k=k)
        head = _pow_tex(a, m)
        tail = _pow_tex(b, k)
        return MathDraw(
            rf"\sqrt[3]{{{_pow_tex(a, 2 * m)}\left({head} - 3\cdot {tail}\right)"
            rf" + {_pow_tex(b, 2 * k)}\left(3\cdot {head} - {tail}\right)}}",
            str(value),
            prompt="จงหาค่าของจำนวนต่อไปนี้",
            hint=r"u^3 - 3u^2v + 3uv^2 - v^3 = (u - v)^3",
            distractors=_distinct(str(value), [
                str(-value), str(a ** m + b ** k), str(value + 1),
                str(value - 1), str(a ** m), str(-(b ** k)),
                str(2 * value), str(value + 10)]))


@question_type("math.posn2561_q14",
               display_name={"th": "ผลบวกของผลคูณเลขโดดที่ไม่เป็นศูนย์"},
               level=LEVEL, topic="ทฤษฎีจำนวน: เลขโดด")
class NonzeroDigitProductSum(SheetProblem):
    """A zero digit and a zero pad both contribute a factor of 1."""

    def expr(self, rng: Random):
        limit = rng.choice([9, 49, 99, 150, 250, 499, 999, 1023, 1500, 2018,
                            2561, 4999, 9999])
        value = SOLVE[14](limit=limit)
        return MathDraw(
            rf"\sum_{{n=1}}^{{{limit}}} p(n)", str(value),
            prompt=("สำหรับจำนวนนับ n ใด ๆ นิยามฟังก์ชัน p(n) เป็นผลคูณของเลขโดด"
                    "ที่ไม่เป็นศูนย์ของ n ในระบบฐานสิบ (ตัวอย่างเช่น "
                    "p(1023) = 1·2·3 = 6) จงหาค่าของผลบวกต่อไปนี้"),
            hint=r"\text{a zero digit contributes a factor }1,"
                 r"\text{ so a padded block sums to }46^d",
            distractors=_distinct(str(value), [
                str(value + 1), str(value - 1), str(46 ** len(str(limit))),
                str(value * 2), str(value + 45), str(value - 45),
                str(46 ** len(str(limit)) - 1)]))


@question_type("math.posn2561_q15",
               display_name={"th": "ผลบวกสัมประสิทธิ์ของพหุนามจากสมการเชิงฟังก์ชัน"},
               level=LEVEL, topic="สมการเชิงฟังก์ชันของพหุนาม")
class CoefficientSumFromShiftEquation(SheetProblem):
    """The sum of the coefficients is P(1) — that is why it is asked this way."""

    def expr(self, rng: Random):
        power = rng.randint(1, 7)
        value = SOLVE[15](power=power)
        neighbours = [SOLVE[15](power=p) for p in range(1, 9) if p != power]
        return MathDraw(
            rf"P(x-1) + P(x+1) = x^{{{power}}}", frac_tex(value),
            prompt=("กำหนดให้ P(x) เป็นพหุนามที่สอดคล้องกับสมการต่อไปนี้สำหรับ"
                    "ทุกจำนวนจริง x จงหาผลบวกของสัมประสิทธิ์ของ P(x)"),
            hint=r"\text{the sum of the coefficients is } P(1)",
            distractors=_distinct(frac_tex(value), [
                frac_tex(-value), frac_tex(value + 1), frac_tex(value - 1),
                frac_tex(Fraction(1, 2)), "0", "1",
                *[frac_tex(v) for v in neighbours]]))


@question_type("math.posn2561_q16",
               display_name={"th": "เศษเหลือจากการหารพหุนามด้วยพหุนามกำลังสอง"},
               level=LEVEL, topic="การหารพหุนาม")
class QuadraticRemainder(SheetProblem):
    """The remainder is the line through the two (root, remainder) pairs."""

    def expr(self, rng: Random):
        a = rng.randint(-5, 5)
        b = rng.choice([v for v in range(-6, 7) if v != a])
        ra = rng.randint(-12, 12)
        rb = rng.randint(-12, 12)
        slope, intercept = SOLVE[16](a=a, ra=ra, b=b, rb=rb)
        answer = _remainder_tex(slope, intercept)
        sum_term = ("" if a + b == 0 else
                    f" {'-' if a + b > 0 else '+'} "
                    + ("" if abs(a + b) == 1 else str(abs(a + b))) + "x")
        product = ("" if a * b == 0 else
                   f" {'+' if a * b > 0 else '-'} {abs(a * b)}")
        quadratic = f"x^2{sum_term}{product}"
        return MathDraw(
            rf"P({a}) = {ra}, \qquad P({b}) = {rb}", answer,
            prompt=("สมมติให้ P(x) เป็นพหุนามที่หารด้วย "
                    f"x {'−' if a > 0 else '+'} {abs(a)} และ "
                    f"x {'−' if b > 0 else '+'} {abs(b)} แล้วเหลือเศษ "
                    f"{_thai_int(ra)} และ {_thai_int(rb)} ตามลำดับ "
                    "จงหาเศษเหลือจากการหาร P(x) ด้วยผลคูณของตัวหารทั้งสองนี้"),
            hint=r"r(x) = mx + n \text{ with } r(a) = r_a \text{ and } "
                 r"r(b) = r_b",
            distractors=_distinct(answer, [
                _remainder_tex(-slope, intercept),
                _remainder_tex(slope, -intercept),
                _remainder_tex(intercept, slope),
                str(ra), str(rb), str(ra + rb),
                _remainder_tex(slope + 1, intercept),
                _remainder_tex(slope, intercept + 1), quadratic]))


@question_type("math.posn2561_q17",
               display_name={"th": "พื้นที่สี่เหลี่ยมจัตุรัสบนวงกลมแนบในสามเหลี่ยมมุมฉาก"},
               level=LEVEL, topic="เรขาคณิต: วงกลมแนบใน")
class SquareOnIncircle(SheetProblem):
    """Only the inradius matters: the square's side is always 8r/5."""

    #: Pythagorean legs, so the inradius — and hence the area — stay exact.
    _TRIPLES = [(4, 3), (3, 4), (8, 6), (6, 8), (12, 5), (5, 12), (15, 8),
                (8, 15), (24, 7), (7, 24), (12, 9), (20, 15), (24, 10),
                (16, 12), (21, 20), (20, 21)]

    def expr(self, rng: Random):
        leg_a, leg_b = rng.choice(self._TRIPLES)
        value = SOLVE[17](leg_a=leg_a, leg_b=leg_b)
        answer = frac_tex(value)
        # the crop draws B sitting on the hypotenuse, which happens only at 3-4-5
        as_drawn = leg_a * 3 == leg_b * 4
        return MathDraw(
            rf"XZ = {leg_b}, \qquad ZY = {leg_a}", answer,
            prompt=(f"สามเหลี่ยมมุมฉาก XYZ มีมุมฉากที่ Z โดยด้าน XZ ยาว {leg_b} "
                    f"หน่วย และด้าน ZY ยาว {leg_a} หน่วย วงกลมวงหนึ่งแนบในรูป"
                    "สามเหลี่ยมนี้ โดยเส้นรอบวงสัมผัสด้าน XZ ที่จุด E "
                    "สี่เหลี่ยมจัตุรัส ABCD มีมุม B และ C อยู่บนเส้นรอบวงของวงกลม "
                    "และด้าน AD อยู่บนด้าน XZ ของสามเหลี่ยม โดยที่จุด E แบ่งครึ่ง"
                    "ด้าน AD จงหาพื้นที่สี่เหลี่ยมจัตุรัส ABCD"),
            hint=r"(s - r)^2 + (s/2)^2 = r^2 \Rightarrow s = \tfrac{8r}{5}",
            figure="" if as_drawn else None,
            distractors=_distinct(answer, [
                frac_tex(value * 2), frac_tex(value / 2),
                frac_tex(Fraction(leg_a * leg_b, 2)),
                frac_tex(value * Fraction(25, 16)),
                frac_tex(value + 1), frac_tex(Fraction(64, 25)),
                frac_tex(value * 4), frac_tex(value + 2)]))


@question_type("math.posn2561_q18",
               display_name={"th": "สัดส่วนพื้นที่แรเงาจากเส้นสองเส้นในสี่เหลี่ยมจัตุรัส"},
               level=LEVEL, topic="เรขาคณิต: พื้นที่รูปสี่เหลี่ยม")
class ShadedSquareRatio(SheetProblem):
    """Two triangles meeting at the crossing point, as a share of the square."""

    #: (4, 2) and (6, 3) restate the sheet's own 2 : 1 unreduced — they answer
    #: 13/30 like (2, 1) and, being the ratio the crop is drawn at, they are also
    #: what keeps the figure from showing on barely one draw in forty.
    _RATIOS = [(2, 1), (4, 2), (6, 3), (1, 1), (3, 1), (1, 3), (3, 2), (2, 3),
               (5, 4), (7, 2), (4, 1), (1, 2), (5, 3), (5, 1), (4, 3), (2, 5)]

    def expr(self, rng: Random):
        m, k = rng.choice(self._RATIOS)
        value = SOLVE[18](m=m, k=k)
        answer = frac_tex(value)
        share = gcd(m, k)
        as_drawn = (m // share, k // share) == (2, 1)      # the crop's own ratio
        return MathDraw(
            rf"AC : CB = {m} : {k}", answer,
            prompt=("สี่เหลี่ยมจัตุรัสรูปหนึ่งมีจุด A และ B เป็นปลายทั้งสองของด้านบน "
                    f"และมีจุด C อยู่บนด้านบนโดยที่ AC : CB = {m} : {k} "
                    "ลากส่วนของเส้นตรงจาก A ไปยังมุมล่างขวา และจาก C ไปยัง"
                    "มุมล่างซ้าย ทั้งสองเส้นตัดกันที่จุดหนึ่ง พื้นที่ที่แรเงาคือ"
                    "สามเหลี่ยมที่มีฐาน AC กับสามเหลี่ยมที่มีฐานเป็นด้านล่างทั้งด้าน "
                    "โดยทั้งสองรูปมียอดร่วมกันที่จุดตัดนั้น จงหาสัดส่วนของพื้นที่"
                    "ที่แรเงาต่อพื้นที่สี่เหลี่ยมจัตุรัสรูปนี้"),
            hint=r"y = S - x \text{ and } y = Sx/m, \text{ with } S = m + k",
            figure="" if as_drawn else None,
            distractors=_distinct(answer, [
                frac_tex(1 - value), frac_tex(value / 2), frac_tex(value * 2),
                frac_tex(Fraction(1, 2)), frac_tex(Fraction(13, 30)),
                frac_tex(Fraction(m, m + k)), frac_tex(Fraction(1, 3)),
                frac_tex(Fraction(5, 12)), frac_tex(Fraction(2, 5))]))


@question_type("math.posn2561_q19",
               display_name={"th": "ความยาวรอบรูปเมื่อส่วนสูงแบ่งเป็นสามเหลี่ยมคล้าย"},
               level=LEVEL, topic="เรขาคณิต: สามเหลี่ยมมุมฉาก")
class SimilarSplitPerimeter(SheetProblem):
    """"Similar but not bisecting" is exactly pq = h²."""

    _POOL = [(base, height) for base in range(8, 60, 2)
             for height in range(2, 26)
             if base * base > 4 * height * height]

    def expr(self, rng: Random):
        base, height = rng.choice(self._POOL)
        SOLVE[19](base=base, height=height)        # the closed form still runs
        answer = _sum_root_tex(base, base * (base + 2 * height))
        return MathDraw(
            rf"BC = {base}, \qquad h = {height}", answer,
            prompt=(f"กำหนดสามเหลี่ยม ABC มีฐานยาว {base} เซนติเมตร หากลากเส้น"
                    "จากจุดยอดมาตั้งฉากกับฐาน จะพบว่า เส้นนี้มีความยาว "
                    f"{height} เซนติเมตร, เส้นนี้ไม่แบ่งครึ่งมุมยอด และเส้นนี้"
                    "แบ่งสามเหลี่ยมออกเป็นสามเหลี่ยมสองรูปที่คล้ายกัน "
                    "จงหาความยาวรอบรูปสามเหลี่ยม ABC นี้"),
            hint=r"pq = h^2 \Rightarrow AB^2 = p(p + q), \ "
                 r"(\sqrt p + \sqrt q)^2 = p + q + 2h",
            distractors=_distinct(answer, [
                _sum_root_tex(base, 4 * base * height),
                _root_tex(base * (base + 2 * height)),
                str(base + 2 * height), str(2 * base + 2 * height),
                _sum_root_tex(base, base * base + 4 * height * height),
                str(base + height), _sum_root_tex(base, base * base + height),
                str(3 * base)]))


@question_type("math.posn2561_q20",
               display_name={"th": "ความยาวเส้นสัมผัสจากคอร์ดที่ตั้งฉากกับเส้นผ่านศูนย์กลาง"},
               level=LEVEL, topic="เรขาคณิต: เส้นสัมผัสวงกลม")
class TangentFromPerpendicularChord(SheetProblem):
    """Both tangents meet on x = −r, so AB falls out of the tangent at C."""

    #: (r, ce) with r² − ce² a perfect square, so AB stays a printable fraction;
    #: ce < r keeps E strictly between the centre and D, as the crop draws it.
    _POOL = [(r, ce) for r in range(5, 40) for ce in range(3, 40)
             if ce < r and round((r * r - ce * ce) ** 0.5) ** 2
             == r * r - ce * ce]

    def expr(self, rng: Random):
        r, ce = rng.choice(self._POOL)
        value = Fraction(SOLVE[20](r=r, ce=ce))
        answer = frac_tex(value)
        return MathDraw(
            rf"r = {r}, \qquad CE = {ce}", answer,
            prompt=(f"จากจุด A ลากเส้นสัมผัสวงกลมรัศมี {r} หน่วย ที่จุด B และ C "
                    "กำหนดให้ BD เป็นเส้นผ่านศูนย์กลางของวงกลม และ CE ตั้งฉากกับ "
                    f"BD ดังรูป ถ้าให้ CE ยาว {ce} หน่วย จงหาความยาว AB"),
            hint=r"AB = \dfrac{r\left(r + \sqrt{r^2 - CE^2}\right)}{CE}",
            distractors=_distinct(answer, [
                frac_tex(Fraction(r * r, ce)), frac_tex(Fraction(2 * r)),
                frac_tex(Fraction(r + ce)), frac_tex(value * 2),
                frac_tex(value / 2), frac_tex(Fraction(r * ce, 2)),
                frac_tex(value + 1), frac_tex(Fraction(r))]))


@question_type("math.posn2561_q21",
               display_name={"th": "ปริมาตรทรงกระบอกที่เท่ากับพื้นที่ผิวทั้งก่อนและหลังปรับ"},
               level=LEVEL, topic="โจทย์ปัญหาปริมาตรและร้อยละ")
class CylinderVolumeEqualsSurface(SheetProblem):
    """Two "volume = surface" conditions fix the shape ratio, then the size."""

    _POOL = _CYLINDER_POOL

    def expr(self, rng: Random):
        up, down = rng.choice(self._POOL)
        value = Fraction(SOLVE[21](height_scale=up, radius_scale=down))
        answer = rf"{frac_tex(value)}\pi"
        return MathDraw(
            r"\pi r^2 h = 2\pi r^2 + 2\pi r h", answer,
            prompt=("ทรงกระบอกปิดอันหนึ่งมีปริมาตรเท่ากับพื้นที่ผิว หากเพิ่ม"
                    f"ความสูงขึ้น {_percent(up)}% และลดรัศมีลง {_percent(down)}% "
                    "พบว่าทรงกระบอกปิดอันใหม่ที่ได้ยังคงมีปริมาตรเท่ากับพื้นที่ผิว "
                    "จงหาปริมาตรของทรงกระบอกปิดอันเริ่มต้น"),
            hint=r"rh = 2r + 2h \text{ for both cylinders; divide one by the "
                 r"other to get } r/h",
            distractors=_distinct(answer, [
                rf"{frac_tex(value * 2)}\pi", rf"{frac_tex(value / 2)}\pi",
                rf"{frac_tex(value + 8)}\pi", frac_tex(value),
                r"64\pi", rf"{frac_tex(value * 3)}\pi",
                rf"{frac_tex(value - 8)}\pi", r"16\pi"]))


@question_type("math.posn2561_q22",
               display_name={"th": "ความยาว AR ในสี่เหลี่ยมด้านขนานที่ถูกตัดด้วยเส้นเดียว"},
               level=LEVEL, topic="เรขาคณิต: สี่เหลี่ยมด้านขนาน")
class ParallelogramTransversal(SheetProblem):
    """AR, PR and PQ along the transversal are in geometric proportion."""

    def expr(self, rng: Random):
        pr = rng.randint(1, 12)
        pq = rng.randint(1, 14)
        SOLVE[22](pr=pr, pq=pq)                    # the closed form still runs
        answer = _root_tex(pr * (pr + pq))
        return MathDraw(
            rf"PR = {pr}, \qquad PQ = {pq}", answer,
            prompt=("ให้ ABCD เป็นรูปสี่เหลี่ยมด้านขนานที่ AB ขนานกับ DC และ "
                    "AD ขนานกับ BC ซึ่งเมื่อลากส่วนของเส้นตรงจากจุด A ไปตัดกับ"
                    "เส้นทแยงมุม BD ที่จุด R ไปตัดกับด้าน BC ที่จุด P และไปตัดกับ"
                    f"ส่วนต่อของด้าน DC ที่จุด Q แล้ว จะได้ PR ยาว {pr} หน่วย "
                    f"และ PQ ยาว {pq} หน่วย ดังรูป จงหาความยาว AR"),
            hint=r"AR^2 = PR\left(PR + PQ\right)",
            distractors=_distinct(answer, [
                _root_tex(pq * (pr + pq)), _root_tex(pr * pq),
                str(pr + pq), _root_tex(pr * pr + pq * pq),
                str(abs(pq - pr)), _root_tex((pr + pq) * (pr + pq) - pr * pq),
                str(2 * pr), _root_tex(pr * (pr + 2 * pq))]))


@question_type("math.posn2561_q23",
               display_name={"th": "อัตราส่วน CD : BD เมื่อเส้นผ่านจุดศูนย์กลางตัดฐาน"},
               level=LEVEL, topic="เรขาคณิต: วงกลมล้อมรูปสามเหลี่ยม")
class CircumcentreCevianRatio(SheetProblem):
    """CD : BD = sin 2γ : sin 2β, and nothing else on the figure matters."""

    #: sin of a doubled angle, as (rational coefficient, radicand).
    _SINE = {30: (Fraction(1, 2), 1), 60: (Fraction(1, 2), 3),
             90: (Fraction(1), 1), 120: (Fraction(1, 2), 3)}
    #: the four angles whose doubles land in that table, acute triangles only.
    _POOL = [(beta, gamma) for beta in (15, 30, 45, 60)
             for gamma in (15, 30, 45, 60) if beta + gamma < 90]

    def _exact(self, beta: int, gamma: int) -> tuple[Fraction, int]:
        top, top_root = self._SINE[2 * gamma]
        bottom, bottom_root = self._SINE[2 * beta]
        if top_root == bottom_root:
            return top / bottom, 1
        if top_root == 3:
            return top / bottom, 3
        return top / (3 * bottom), 3               # 1/√3 = √3/3

    @staticmethod
    def _reciprocal(coef: Fraction, radicand: int) -> tuple[Fraction, int]:
        """BD : CD — the ratio the other way up, which is the standard slip."""
        if radicand == 1:
            return 1 / coef, 1
        return 1 / (3 * coef), 3                   # 1/(c√3) = √3/(3c)

    def expr(self, rng: Random):
        beta, gamma = rng.choice(self._POOL)
        SOLVE[23](bao=beta, aco=gamma)             # the closed form still runs
        coef, radicand = self._exact(beta, gamma)
        answer = _coef_root_tex(coef, radicand)
        return MathDraw(
            rf"\angle BAO = {beta}^\circ, \qquad \angle ACO = {gamma}^\circ",
            answer,
            prompt=("ให้ ΔABC เป็นรูปสามเหลี่ยมมุมแหลมที่แนบในวงกลมที่มี O เป็น"
                    "จุดศูนย์กลาง ซึ่งเมื่อลากส่วนของเส้นตรงจากจุด A ผ่านจุด"
                    "ศูนย์กลาง O ไปตัดกับด้าน BC ที่จุด D และลากส่วนของเส้นตรง "
                    f"CO แล้วจะได้ ∠BAO = {beta}° และ ∠ACO = {gamma}° "
                    "จงหาอัตราส่วน CD : BD"),
            hint=r"OA = OB = OC, \text{ so } \angle B = 90^\circ - \gamma "
                 r"\text{ and } \angle C = 90^\circ - \beta",
            distractors=_distinct(answer, [
                _coef_root_tex(*self._reciprocal(coef, radicand)),
                "1", "2", frac_tex(Fraction(1, 2)),
                _coef_root_tex(Fraction(1), 3),
                _coef_root_tex(Fraction(1, 3), 3),
                _coef_root_tex(Fraction(1, 2), 3),
                _coef_root_tex(Fraction(2, 3), 3), "3"]))


@question_type("math.posn2561_q24",
               display_name={"th": "รัศมีกำลังสองจากเส้นตัดวงกลมสองเส้นที่ทำมุมกัน"},
               level=LEVEL, topic="เรขาคณิต: กำลังของจุด")
class SecantPairRadius(SheetProblem):
    """Power of the point sizes the second secant; the angle then places O."""

    #: only 60°, 90° and 120° keep r² rational once the chord midpoints are placed.
    _POOL = [(ab, cd, bp, angle)
             for ab in range(3, 13) for cd in range(2, 10)
             for bp in range(2, 10) for angle in (60, 90, 120)
             if isinstance(q24.solve(ab=ab, cd=cd, bp=bp, angle=angle),
                           (int, Fraction))
             and (q24.solve(ab=ab, cd=cd, bp=bp, angle=angle) or 0) > 0]

    def expr(self, rng: Random):
        ab, cd, bp, angle = rng.choice(self._POOL)
        value = Fraction(SOLVE[24](ab=ab, cd=cd, bp=bp, angle=angle))
        answer = frac_tex(value)
        power = bp * (bp + ab)
        return MathDraw(
            rf"AB = {ab}, \quad CD = {cd}, \quad BP = {bp}, \quad "
            rf"\angle APD = {angle}^\circ", answer,
            prompt=("จากจุด P ภายนอกวงกลมรัศมี r หน่วย ลากเส้นตัดวงกลมสองเส้น "
                    "เส้นแรกตัดวงกลมที่จุด B แล้วจึงถึงจุด A และเส้นที่สองตัด"
                    f"วงกลมที่จุด C แล้วจึงถึงจุด D ดังรูป โดยที่ AB = {ab} หน่วย, "
                    f"CD = {cd} หน่วย, BP = {bp} หน่วย และ ∠APD = {angle}° "
                    "จงหาค่าของ r²"),
            hint=r"PB \cdot PA = PC \cdot PD = PO^2 - r^2;\ \text{the foot of "
                 r"each chord is its midpoint}",
            distractors=_distinct(answer, [
                str(power), frac_tex(value * 2), frac_tex(value / 2),
                frac_tex(value + power), frac_tex(value - 1),
                frac_tex(value + 1), str(bp + ab), str(power + cd)]))


@question_type("math.posn2561_q25",
               display_name={"th": "ความน่าจะเป็นที่ฝนไม่ตกสองวันติดกัน"},
               level=LEVEL, topic="ความน่าจะเป็น")
class RainChainTwoDays(SheetProblem):
    """A two-state chain: only yesterday matters, so the answer factorises."""

    _DAYS = ("จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์")
    _AFTER_RAIN = [Fraction(5, 6), Fraction(2, 3), Fraction(3, 4),
                   Fraction(4, 5), Fraction(1, 3), Fraction(7, 8)]
    _AFTER_DRY = [Fraction(1, 2), Fraction(1, 3), Fraction(2, 3),
                  Fraction(1, 4), Fraction(3, 5), Fraction(5, 8)]

    def expr(self, rng: Random):
        after_rain = rng.choice(self._AFTER_RAIN)
        after_dry = rng.choice(self._AFTER_DRY)
        gap = rng.randint(1, 3)
        start = rng.randint(0, len(self._DAYS) - gap - 2)
        value = SOLVE[25](dry_after_rain=after_rain, dry_after_dry=after_dry,
                          gap=gap)
        answer = frac_tex(value)
        known, first, second = (self._DAYS[start], self._DAYS[start + gap],
                                self._DAYS[start + gap + 1])
        return MathDraw(
            rf"P(N \mid R) = {frac_tex(after_rain)}, \qquad "
            rf"P(N \mid N) = {frac_tex(after_dry)}", answer,
            prompt=("ในการพยากรณ์อากาศช่วงฤดูฝนของเมืองหนึ่ง พบว่า หากในวันหนึ่ง"
                    "ฝนตกแล้ว ความน่าจะเป็นที่ฝนไม่ตกในวันถัดไปเป็น "
                    f"{after_rain.numerator}/{after_rain.denominator} "
                    "และหากในวันหนึ่งฝนไม่ตกแล้ว ความน่าจะเป็นที่ฝนไม่ตกใน"
                    f"วันถัดไปเป็น {after_dry.numerator}/{after_dry.denominator} "
                    f"ถ้าในสัปดาห์นี้ฝนไม่ตกในวัน{known} จงหาความน่าจะเป็นที่ใน"
                    f"สัปดาห์นี้ฝนไม่ตกทั้งในวัน{first}และวัน{second}"),
            hint=r"f_{n+1} = q + (p - q)f_n, \text{ then one more dry day}",
            distractors=_distinct(answer, [
                frac_tex(after_dry ** 2), frac_tex(after_dry),
                frac_tex(value * 2), frac_tex(1 - value),
                frac_tex(after_rain * after_dry), frac_tex(value / 2),
                frac_tex(after_dry ** (gap + 1)),
                frac_tex(Fraction(1, 3)), frac_tex(Fraction(1, 2))]))


@question_type("math.posn2561_q26",
               display_name={"th": "จำนวนวิธีวางลูกบอลบนด้านของโต๊ะที่หมุนได้"},
               level=LEVEL, topic="การนับและการจัดหมู่")
class BallsOnATurningTable(SheetProblem):
    """The sides are indistinguishable, so the count is over rotation orbits."""

    #: indexed by ``sides - 3``.
    _SHAPES = ("สามเหลี่ยมด้านเท่า", "สี่เหลี่ยมจัตุรัส", "ห้าเหลี่ยมด้านเท่า",
               "หกเหลี่ยมด้านเท่า")

    def expr(self, rng: Random):
        sides = rng.randint(3, 6)
        balls = rng.randint(sides + 1, sides + 10)
        value = SOLVE[26](balls=balls, sides=sides)
        labelled = comb(balls - 1, sides - 1)
        return MathDraw(
            rf"n_1 + n_2 + \cdots + n_{{{sides}}} = {balls}, \qquad n_i \ge 1",
            str(value),
            prompt=(f"จงหาจำนวนวิธีที่แตกต่างกันทั้งหมดในการวางลูกบอลที่เหมือนกัน"
                    f"ทั้งหมด {balls} ลูก ไว้บนด้านทั้ง {sides} ด้านของโต๊ะ"
                    f"{self._SHAPES[sides - 3]}ที่เหมือนกันทุกด้าน โดยแต่ละด้าน"
                    "ต้องมีลูกบอลวางอย่างน้อย 1 ลูก และลูกบอลแต่ละลูกจะถูกนับว่า"
                    "วางอยู่บนด้านใดด้านหนึ่งของโต๊ะเท่านั้น "
                    "(การวางที่หมุนโต๊ะแล้วเหมือนกันถือเป็นวิธีเดียวกัน)"),
            hint=r"\text{Burnside over the } n \text{ rotations of the table}",
            distractors=_distinct(str(value), [
                str(labelled), str(value + 1), str(value - 1),
                str(labelled // sides), str(value * 2),
                str(labelled - value), str(value + sides), str(2 * value + 1)]))


@question_type("math.posn2561_q27",
               display_name={"th": "จำนวนเต็มที่ใช้เลขโดดครบชุดที่กำหนดพอดี"},
               level=LEVEL, topic="หลักการรวมและการแยก")
class ExactDigitSetCount(SheetProblem):
    """A(n) is a set: repeats are free, but every listed digit must occur."""

    _POOL = [(digits, limit)
             for digits in ((0, 4, 7), (1, 2), (0, 1), (3, 5, 9), (2, 6),
                            (0, 1, 2, 8), (4, 8), (1, 3, 7), (0, 5), (7,),
                            (2, 3, 5), (0, 9), (1, 4, 6, 8))
             for limit in (1000, 5000, 10000, 100000)
             if (q27.solve(digits=digits, limit=limit) or 0) > 0]

    def expr(self, rng: Random):
        digits, limit = rng.choice(self._POOL)
        value = SOLVE[27](digits=digits, limit=limit)
        listed = ", ".join(str(d) for d in digits)
        return MathDraw(
            rf"P = \left\{{\, n \in \mathbb{{N}} \mid A(n) = \{{{listed}\}}"
            rf"\ \text{{and}}\ n \le {limit} \,\right\}}", str(value),
            prompt=("กำหนด A(n) แทนเซตของเลขโดดที่เขียนแทนจำนวนนับ n เช่น "
                    "A(191) = {1, 9} และ A(2018) = {0, 1, 2, 8} "
                    f"จงหา |P| เมื่อ P คือเซตของจำนวนนับ n ที่ A(n) = {{{listed}}} "
                    f"และ n ≤ {limit}"),
            hint=r"\text{count the strings over the set, then subtract those "
                 r"missing a value}",
            distractors=_distinct(str(value), [
                str(value + 1), str(value - 1), str(value * 2),
                str(value + len(digits)), str(value // 2 or 1),
                str(value + 4), str(value - 4), str(value * 3)]))


@question_type("math.posn2561_q28",
               display_name={"th": "ความน่าจะเป็นที่กบเดินสุ่มมาอยู่ที่จุดที่กำหนด"},
               level=LEVEL, topic="ความน่าจะเป็น")
class FrogRandomWalk(SheetProblem):
    """Position and jump count always share a parity — check that first."""

    def expr(self, rng: Random):
        if rng.random() < 0.5:                      # the parity trap, full size
            steps = rng.choice([2561, 2019, 1001, 777, 2018, 1000])
            position = rng.choice([2018, 1234, 500, 99, 2561, 777])
            if (steps + position) % 2 == 0:         # force the mismatch
                position += 1
        else:                                       # small enough to print
            steps = rng.randint(4, 16)
            position = rng.randrange(-steps, steps + 1, 2 if steps % 2 == 0 else 1)
            if (steps + position) % 2:
                position += 1
        value = Fraction(SOLVE[28](steps=steps, position=position))
        answer = frac_tex(value)
        return MathDraw(
            rf"x_0 = 0, \qquad n = {steps}, \qquad x_n = {position}", answer,
            prompt=("มีกบตัวหนึ่งอยู่ที่จุด x = 0 บนเส้นจำนวน โดยในการกระโดด"
                    "แต่ละครั้ง มันจะกระโดดได้ไกลหนึ่งหน่วยไปทางซ้ายหรือทางขวา"
                    "ด้วยความน่าจะเป็นเท่า ๆ กัน จงหาความน่าจะเป็นที่หลังจาก"
                    f"การกระโดดครั้งที่ {steps} กบตัวนี้จะมาอยู่ที่จุด "
                    f"x = {position} บนเส้นจำนวนนี้"),
            hint=r"u \text{ right-jumps land the frog at } 2u - n",
            distractors=_distinct(answer, [
                frac_tex(Fraction(1, 2)), frac_tex(Fraction(1, 4)),
                rf"\frac{{1}}{{2^{{{steps}}}}}",
                frac_tex(Fraction(abs(position), steps)) if steps else "1",
                frac_tex(value * 2) if value else "1",
                frac_tex(1 - value), frac_tex(Fraction(1, steps)),
                frac_tex(Fraction(1, 3))]))


@question_type("math.posn2561_q29",
               display_name={"th": "ความน่าจะเป็นที่ชนะเกมทอดลูกเต๋าหลายรอบ"},
               level=LEVEL, topic="ความน่าจะเป็น")
class RisingThresholdDiceGame(SheetProblem):
    """Nested rounds: win now, or survive and win later. "มากกว่า" is strict."""

    def expr(self, rng: Random):
        faces = rng.choice([4, 6, 6, 6, 8, 10, 12])
        rounds = rng.randint(2, min(4, faces - 1))
        start = rng.randint(1, faces - rounds)
        thresholds = tuple(start + i for i in range(rounds))
        value = SOLVE[29](faces=faces, thresholds=thresholds)
        answer = frac_tex(value)
        rules = "  ".join(
            (f"ถ้าลูกเต๋าขึ้นแต้มมากกว่า {t} เขาจะชนะ" if i == 0 else
             f"ไม่เช่นนั้นเขาจะได้ทอดลูกเต๋าอีกครั้งหนึ่ง ซึ่งถ้าขึ้นแต้มมากกว่า "
             f"{t} เขาจะชนะ")
            for i, t in enumerate(thresholds))
        first = Fraction(faces - thresholds[0], faces)
        return MathDraw(
            r"t = \left(" + r",\ ".join(str(t) for t in thresholds)
            + rf"\right), \qquad \text{{faces}} = {faces}", answer,
            prompt=(f"เด็กชายพลทอดลูกเต๋าเที่ยงตรงที่มี {faces} หน้าลูกหนึ่งใน"
                    f"เกมการแข่งขัน ซึ่งมีเงื่อนไขดังนี้  {rules}  "
                    "ถ้าไม่ได้ตามนี้ถือว่าแพ้ จงหาว่าเด็กชายพลมีความน่าจะเป็นที่"
                    "จะชนะการแข่งขันนี้เป็นเท่าใด"),
            hint=r"P = \sum_i \left(\prod_{j<i} \tfrac{t_j}{f}\right)"
                 r"\tfrac{f - t_i}{f}",
            distractors=_distinct(answer, [
                frac_tex(first), frac_tex(1 - value), frac_tex(value / 2),
                frac_tex(first ** len(thresholds)),
                frac_tex(min(Fraction(1), value * 2)),
                frac_tex(Fraction(faces - thresholds[-1], faces)),
                frac_tex(Fraction(1, 2)), frac_tex(Fraction(2, 3))]))


@question_type("math.posn2561_q30",
               display_name={"th": "จำนวนตัวหารที่เป็นจำนวนกำลังสอง"},
               level=LEVEL, topic="ตัวประกอบของจำนวนเต็ม")
class SquareDivisorCount(SheetProblem):
    """Each prime picks an even exponent, independently of the others."""

    _PRIMES = (2, 3, 5, 7, 11, 13)

    def expr(self, rng: Random):
        primes = sorted(rng.sample(self._PRIMES, rng.randint(2, 4)))
        factorization = tuple((p, rng.randint(1, 9)) for p in primes)
        value = SOLVE[30](factorization=factorization)
        written = r" \cdot ".join(str(p) if e == 1 else rf"{p}^{{{e}}}"
                                  for p, e in factorization)
        plain = "·".join(str(p) if e == 1 else f"{p}^{e}"
                         for p, e in factorization)
        divisors = 1
        for _, e in factorization:
            divisors *= e + 1
        cubes = 1
        for _, e in factorization:
            cubes *= e // 3 + 1
        return MathDraw(
            written, str(value),
            prompt=(f"จงหาจำนวนตัวหารบวกทั้งหมดของ {plain} "
                    "ที่เป็นจำนวนกำลังสองสมบูรณ์"),
            hint=r"\text{a divisor is a square exactly when every exponent is "
                 r"even}",
            distractors=_distinct(str(value), [
                str(divisors), str(cubes), str(value + 1), str(value - 1),
                str(value * 2), str(divisors - value), str(divisors // 2),
                str(value + 2)]))
