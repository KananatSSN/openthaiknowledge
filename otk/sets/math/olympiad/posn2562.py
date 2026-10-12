"""สมการเลขชี้กำลัง

คณิตศาสตร์ · โอลิมปิก (สอวน.) · สอวน.
Indicators: —

Sets moved here from: posn2562.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from math import gcd
from random import Random

from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem, frac_answer_tex
from otk.sheets import figure_attachments
from otk.sheets.posn2562_math import (
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


SHEET = "สอวน. ค่าย 1 (2562)"


SHEET_ID = "posn2562_math"


_MODULES = [q01, q02, q03, q04, q05, q06, q07, q08, q09, q10,
            q11, q12, q13, q14, q15, q16, q17, q18, q19, q20,
            q21, q22, q23, q24, q25, q26, q27, q28, q29, q30]


SOLVE = {n: lru_cache(maxsize=4096)(mod.solve)
         for n, mod in enumerate(_MODULES, start=1)}


FIGURES = figure_attachments(SHEET_ID)


class SheetProblem(WordProblem):
    """A โจทย์ from the 2562 sheet: Thai prompt, exact TeX answer."""

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


def _surd_tex(radicand: int) -> str:
    """√n, reduced — ``6`` for 36, ``2\\sqrt{3}`` for 12."""
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


def _pm_surd(p: int, q: int, d: int, den: int) -> str:
    """``(p + q√d)/den``, reduced and with the trivial parts dropped."""
    common = gcd(gcd(abs(p), abs(q)), abs(den)) or 1
    p, q, den = p // common, q // common, den // common
    if den < 0:
        p, q, den = -p, -q, -den
    mag = "" if abs(q) == 1 else str(abs(q))
    surd = str(abs(q)) if d in (0, 1) else rf"{mag}\sqrt{{{d}}}"
    if q == 0:
        top = str(p)
    elif p == 0:
        top = ("-" if q < 0 else "") + surd
    else:
        top = f"{p} {'-' if q < 0 else '+'} {surd}"
    if den == 1:
        return top
    return rf"\frac{{{top}}}{{{den}}}"


def _round_tex(value: float, places: int = 4) -> str:
    """A decimal answer, trimmed — for the items whose value is a real number."""
    text = f"{value:.{places}f}".rstrip("0").rstrip(".")
    return text if text not in ("", "-") else "0"


@question_type("math.posn2562_q01",
               display_name={"th": "ค่าของอัตราส่วนเลขชี้กำลังที่กำหนดด้วย a³ⁿ"},
               level=LEVEL, topic="สมการเลขชี้กำลัง")
class CubePowerRatio(SheetProblem):
    """Every printed exponent leaves the same remainder mod 3 — that is the item."""

    _SHAPES = [((4, 7, -5), (-2, 1)), ((1, -2), (4, -5)), ((2, 5), (-1,)),
               ((0, 3, 6), (-3, 0)), ((1, 4, -2), (1, -2)), ((5, 2, -4), (-1, 2))]

    def expr(self, rng: Random):
        top, bottom = rng.choice(self._SHAPES)
        value = rng.choice([2, 3, 5, 6, 7, 10])
        got = SOLVE[1](top=top, bottom=bottom, value=value)

        def power_sum(exponents) -> str:
            return " + ".join(rf"a^{{{e}n}}" for e in exponents)

        return MathDraw(
            rf"\frac{{{power_sum(top)}}}{{{power_sum(bottom)}}}",
            frac_answer_tex(got),
            prompt=(f"ถ้า a³ⁿ = {value} เมื่อ a เป็นจำนวนจริง และ n เป็นจำนวนเต็ม "
                    "แล้วนิพจน์ต่อไปนี้มีค่าเท่าใด"),
            hint=r"t = a^n,\ t^3 = v:\ \text{multiply above and below by }"
                 r"t^{s}\text{ until every power is a power of } t^3",
            distractors=_distinct(frac_answer_tex(got), [
                frac_answer_tex(got + 1), frac_answer_tex(got - 1),
                frac_answer_tex(got * value), frac_answer_tex(1 / got),
                frac_answer_tex(got / 2)]))


@question_type("math.posn2562_q02",
               display_name={"th": "ค่าน้อยที่สุดของ m + n จาก ห.ร.ม. และ ค.ร.น."},
               level=LEVEL, topic="ห.ร.ม. และ ค.ร.น.")
class MinimalSumFromGcdLcm(SheetProblem):
    #: (gcd, lcm) pairs where a coprime split exists.
    _POOL = [(g, g * q) for g in (1, 2, 3, 4, 6, 10, 12, 15, 20, 24)
             for q in (30, 60, 210, 360, 720, 1260, 2520)
             if q02.solve(g=g, lcm=g * q) is not None]

    def expr(self, rng: Random):
        g, lcm = rng.choice(self._POOL)
        value = SOLVE[2](g=g, lcm=lcm)
        return MathDraw(
            rf"\gcd(m, n) = {g}, \quad \operatorname{{lcm}}(m, n) = {lcm}",
            str(value),
            prompt=(f"ให้ m และ n เป็นจำนวนเต็มบวกที่มี ห.ร.ม. และ ค.ร.น. เป็น {g} "
                    f"และ {lcm} ตามลำดับ จงหาค่าที่น้อยที่สุดที่เป็นไปได้ของ m + n"),
            hint=r"m = ga,\ n = gb,\ \gcd(a,b) = 1,\ ab = \ell/g:\ "
                 r"\text{split the prime powers}",
            distractors=_distinct(str(value), [
                str(g + lcm),                    # the two given numbers
                str(value + g), str(value - g), str(2 * g * (lcm // g)),
                str(value + 2 * g)]))


@question_type("math.posn2562_q03",
               display_name={"th": "ผลบวกของรากจริงของสมการติดกรณฑ์"},
               level=LEVEL, topic="สมการกำลังสองและเครื่องหมายราก")
class SharedRadicandRoots(SheetProblem):
    """The polynomial part and the radicand are the same quadratic."""

    _POOL = [p for p in ({"p": mult, "q": mult * shift, "r": rest,
                          "k": coef, "s": shift, "t": inner,
                          "target": target}
                         for mult in (1, 2, 3)
                         for shift in (-5, -4, 2, 3)
                         for inner in (-3, 1, 3)
                         for rest in (0, 1, 7)
                         for coef in (2, 4, 6)
                         for target in (12, 31, 40, 55, 63))
             if q03.solve(**p) is not None]

    def expr(self, rng: Random):
        p = rng.choice(self._POOL)
        value = SOLVE[3](**p)

        def term(coef: int, sym: str, lead: bool = False) -> str:
            if coef == 0:
                return ""
            mag = "" if abs(coef) == 1 and sym else str(abs(coef))
            if lead:
                return f"{'-' if coef < 0 else ''}{mag}{sym}"
            return f" {'-' if coef < 0 else '+'} {mag}{sym}"

        left = (term(p["p"], "x^2", lead=True) + term(p["q"], "x")
                + term(p["r"], ""))
        inside = ("x^2" + term(p["s"], "x") + term(p["t"], ""))
        return MathDraw(
            rf"{left} + {p['k']}\sqrt{{{inside}}} = {p['target']}", str(value),
            prompt="จงหาผลบวกของรากจริงทั้งหมดของสมการต่อไปนี้",
            hint=r"u = x^2 + sx + t\ \text{is the radicand itself};\ "
                 r"w = \sqrt u \ge 0",
            distractors=_distinct(str(value), [
                str(-value), str(value + p["s"]), str(2 * value),
                str(value + 1), str(value - 1)]))


@question_type("math.posn2562_q04",
               display_name={"th": "ผลบวกอายุของลูกสาวสามคนที่มีฝาแฝดเป็นคนโต"},
               level=LEVEL, topic="ตัวประกอบของจำนวนเต็ม")
class TwinAgesProduct(SheetProblem):
    #: products for which exactly one (twin age, younger age) pair exists.
    _POOL = [n for n in range(2, 400) if q04.solve(product=n) is not None]

    def expr(self, rng: Random):
        product = rng.choice(self._POOL)
        value = SOLVE[4](product=product)
        return MathDraw(
            "", str(value),
            prompt=("ครอบครัวหนึ่ง มีสมาชิกทั้งหมด 5 คน ประกอบด้วย พ่อ แม่ และ"
                    "ลูกสาว 3 คน โดยที่ลูกสาว 2 คนโตเป็นฝาแฝดกัน ถ้าผลคูณของอายุ"
                    f"ของลูกสาวทั้งสามคนเท่ากับ {product} แล้วผลบวกของอายุของ"
                    "ลูกสาวทั้งสามคนมีค่าเท่าใด (อายุคิดเป็นจำนวนเต็มปี)"),
            hint=r"t^2 y = N,\ y < t \ \Rightarrow\ \text{sum} = 2t + y",
            distractors=_distinct(str(value), [
                str(value + 1), str(value - 1), str(value + 5),
                str(product), str(value * 2), str(value + 2),
                str(value - 2), str(value + 3)]))


@question_type("math.posn2562_q05",
               display_name={"th": "รัศมีทรงกลมที่ล้อมกล่องทรงสี่เหลี่ยมมุมฉาก"},
               level=LEVEL, topic="เรขาคณิตสามมิติ")
class InscribedBoxRadius(SheetProblem):
    #: (surface, edges) whose diagonal comes out a whole number.
    _POOL = [(2 * pairwise, 4 * perimeter)
             for perimeter in range(6, 60)
             for pairwise in range(1, perimeter * perimeter // 2)
             if (perimeter * perimeter - 2 * pairwise) > 0
             and (perimeter * perimeter - 2 * pairwise) % 4 == 0
             and int(((perimeter * perimeter - 2 * pairwise) // 4) ** 0.5) ** 2
             == (perimeter * perimeter - 2 * pairwise) // 4]

    def expr(self, rng: Random):
        surface, edges = rng.choice(self._POOL)
        value = SOLVE[5](surface=surface, edges=edges)
        return MathDraw(
            rf"\text{{surface}} = {surface}, \quad \text{{edges}} = {edges}",
            str(value),
            prompt=("กล่องทรงสี่เหลี่ยมมุมฉากใบหนึ่งบรรจุแนบในทรงกลมที่มีรัศมี r "
                    "หน่วย ถ้ากล่องใบนี้มีพื้นที่ผิวทั้ง 6 ด้านรวมกันเท่ากับ "
                    f"{surface} ตารางหน่วย และผลรวมของความยาวสันกล่องทั้ง 12 สัน "
                    f"เท่ากับ {edges} หน่วย จงหาความยาวรัศมี r"),
            hint=r"(2r)^2 = a^2+b^2+c^2 = (a+b+c)^2 - 2(ab+bc+ca)",
            distractors=_distinct(str(value), [
                str(2 * value), str(value + 1), str(value - 1),
                str(edges // 4), str(value * value), str(value + 2),
                str(value + 3), str(value + 5)]))


@question_type("math.posn2562_q06",
               display_name={"th": "ความยาวเส้นสูงจากมุมฉากลงสู่ด้านตรงข้าม"},
               level=LEVEL, topic="เรขาคณิต: สามเหลี่ยมมุมฉาก")
class AltitudeGeometricMean(SheetProblem):
    def expr(self, rng: Random, lo: int = 1, hi: int = 24):
        ad = rng.randint(lo, hi)
        bd = rng.randint(lo, hi)
        SOLVE[6](ad=ad, bd=bd)              # the numeric pair still has to agree
        answer = _surd_tex(ad * bd)
        return MathDraw(
            rf"AD = {ad}, \quad BD = {bd}", answer,
            prompt=("กำหนดให้ ABC เป็นรูปสามเหลี่ยมที่มีมุม C เป็นมุมฉาก ลากส่วนของ"
                    "เส้นตรงจากจุด C ไปตั้งฉากกับด้าน AB ที่จุด D  ถ้า "
                    f"AD = {ad} และ BD = {bd} จงหาความยาวของ CD"),
            hint=r"\triangle ACD \sim \triangle CBD \Rightarrow "
                 r"\frac{AD}{CD} = \frac{CD}{BD}",
            distractors=_distinct(answer, [
                str(ad + bd),                       # the hypotenuse
                _surd_tex(ad * ad + bd * bd),       # AC, by Pythagoras
                _surd_tex(ad + bd), str(abs(ad - bd) or 1),
                _surd_tex(2 * ad * bd)]))


@question_type("math.posn2562_q07",
               display_name={"th": "ความน่าจะเป็นที่จำนวนสัตว์ในคอกเป็นจำนวนเฉพาะ"},
               level=LEVEL, topic="ความน่าจะเป็น")
class PrimePenProbability(SheetProblem):
    #: (pens, legs) where the head counts really do fill the pens exactly.
    _POOL = [(pens, legs) for legs in range(8, 80, 2) for pens in range(2, 40)
             if q07.solve(pens=pens, legs=legs) is not None]

    def expr(self, rng: Random):
        pens, legs = rng.choice(self._POOL)
        value = SOLVE[7](pens=pens, legs=legs)
        return MathDraw(
            "", frac_answer_tex(value),
            prompt=(f"ชาวบ้านคนหนึ่งเลี้ยงหมูและเป็ดไว้ทั้งหมด {pens} คอก แต่ละคอก"
                    "ต้องประกอบด้วยทั้งหมูและเป็ด โดยที่แต่ละคอกมีจำนวนรวมของสัตว์"
                    "ทั้งสองชนิดแตกต่างกันทั้งหมด แต่มีจำนวนขารวมกัน "
                    f"{legs} ขาเท่ากันทุกคอก  หากสุ่มเลือกมาคอกหนึ่ง จงหาความน่าจะเป็น"
                    "ที่จำนวนรวมของสัตว์คอกนั้นเป็นจำนวนเฉพาะ"),
            hint=r"4p + 2d = L \Rightarrow p + d = \tfrac L2 - p,"
                 r"\ 1 \le p \le \tfrac L4",
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(1 - value),
                frac_answer_tex(value + Fraction(1, pens)),
                frac_answer_tex(value - Fraction(1, pens)),
                frac_answer_tex(Fraction(1, pens)),
                frac_answer_tex(value / 2),
                # small pen counts make the ±1/pens neighbours collide with
                # 1 − value, so keep a second ring of near misses.
                frac_answer_tex(value + Fraction(2, pens)),
                frac_answer_tex(value - Fraction(2, pens)),
                frac_answer_tex(Fraction(2, pens)),
                frac_answer_tex(1 - value - Fraction(1, pens))]))


@question_type("math.posn2562_q08",
               display_name={"th": "เงินรางวัลรวมจากคำให้การของนักวิ่งสามคน"},
               level=LEVEL, topic="ปริศนาเชิงตรรกะ")
class RacePrizeDeduction(SheetProblem):
    #: (prizes, ahead_of_a, behind_c) that force exactly one finishing order.
    _POOL = [(prizes, ahead, behind)
             for prizes in ((7000, 5000, 2500, 1500, 500),
                            (10000, 6000, 3000, 2000, 1000),
                            (12000, 8000, 4000, 2000, 1000),
                            (9000, 4500, 3000, 1500, 750))
             for ahead in (1, 2, 3)
             for behind in (0, 1, 2, 3)
             if q08.solve(prizes=prizes, ahead_of_a=ahead,
                          behind_c=behind) is not None]

    def expr(self, rng: Random):
        prizes, ahead, behind = rng.choice(self._POOL)
        value = SOLVE[8](prizes=prizes, ahead_of_a=ahead, behind_c=behind)
        listed = ", ".join(f"{p:,}" for p in prizes)
        return MathDraw(
            "", str(value),
            prompt=("การแข่งขันวิ่ง 200 เมตร รายการหนึ่งมีผู้เข้าแข่งขัน 5 คน ได้แก่"
                    "นักเรียน A, B, C, D และ E การแข่งขันนี้มีเงินรางวัลให้ตั้งแต่"
                    f"อันดับที่ 1 ถึงอันดับที่ 5 เป็น {listed} บาท ตามลำดับ  "
                    "เมื่อแข่งขันเสร็จ A, B และ C ให้ข้อมูลดังนี้  "
                    f"นักเรียน A: คนที่ถึงก่อนผมมีไม่น้อยกว่า {ahead} คน "
                    "แต่ผมเข้าเส้นชัยก่อนนาย D  "
                    "นักเรียน B: ผมถึงเส้นชัยตามหลังนาย E เลย  "
                    f"นักเรียน C: คนที่ถึงเส้นชัยหลังผมมีเพียง {behind} คนเท่านั้น  "
                    "นักเรียน A, B และ C ได้เงินรางวัลรวมกันเป็นเงินทั้งหมดกี่บาท"),
            hint=r"\text{C's own count fixes his place; A and D follow, then }"
                 r"\text{E and B as a consecutive pair}",
            distractors=_distinct(str(value), [
                str(sum(prizes) - value),          # the other two runners
                str(sum(prizes)), str(value + prizes[-1]),
                str(value - prizes[-1]), str(sum(prizes[:3]))]))


@question_type("math.posn2562_q09",
               display_name={"th": "ช่วงของผลรวมคะแนนทั้งคู่หลังเล่นครบทุกเกม"},
               level=LEVEL, topic="การหาค่าเหมาะที่สุดเชิงจำนวนเต็ม")
class CombinedScoreSpread(SheetProblem):
    """Who wins never matters — only whether a game was decided or drawn."""

    def expr(self, rng: Random):
        games = rng.randint(5, 20)
        draw = rng.randint(1, 3)
        win = rng.choice([w for w in range(2 * draw + 1, 2 * draw + 6)])
        loss = rng.choice([0, 0, 1])
        value = SOLVE[9](games=games, win=win, loss=loss, draw=draw)
        return MathDraw(
            rf"\text{{win}} = {win}, \quad \text{{loss}} = {loss}, "
            rf"\quad \text{{draw}} = {draw}", str(value),
            prompt=("น้องมิวและน้องแบ๊มแข่งเล่นเกมหมากฮอสกัน โดยในแต่ละเกม ผู้ชนะ"
                    f"จะได้ {win} คะแนน ผู้แพ้จะได้ {loss} คะแนน และถ้าเสมอจะได้"
                    f"คนละ {draw} คะแนน  จงหาว่าเมื่อเล่นกันไปจนครบ {games} เกมแล้ว "
                    "ผลรวมของคะแนนทั้งหมดของทั้งคู่ที่มีค่ามากที่สุดที่เป็นไปได้ "
                    "ต่างจากค่าน้อยที่สุดที่เป็นไปได้อยู่เท่าใด"),
            hint=r"\text{each game contributes } w + l \text{ or } 2d,"
                 r"\ \text{so the spread is } g\,|w + l - 2d|",
            distractors=_distinct(str(value), [
                str(games * (win + loss)),        # the maximum, not the spread
                str(games * 2 * draw), str(value + games),
                str(value // 2 or 1), str(value + 2 * games),
                str(value + 1), str(value - 1), str(value + 3),
                str(value * 2 + 1)]))


@question_type("math.posn2562_q10",
               display_name={"th": "ค่าของ mn จากเศษเหลือของพหุนามกำลังสาม"},
               level=LEVEL, topic="การหารพหุนาม")
class PrimeConstantCubic(SheetProblem):
    #: (u, ru, v, rv) where the primality of p pins the family to one member.
    _POOL = [(u, ru, v, rv)
             for u in (1, 2, -1)
             for v in (-3, -1, 2, -2)
             for ru in range(0, 9)
             for rv in range(0, 9)
             if u != v and q10.solve(u=u, ru=ru, v=v, rv=rv) is not None
             and all(abs(c) <= 40 for c in q10.coefficients(u, ru, v, rv)[0][:2])]

    @staticmethod
    def _linear(root: int) -> str:
        return f"x - {root}" if root > 0 else f"x + {-root}"

    def expr(self, rng: Random):
        u, ru, v, rv = rng.choice(self._POOL)
        value = SOLVE[10](u=u, ru=ru, v=v, rv=rv)
        first = (f"หารด้วย {self._linear(u)} แล้วเหลือเศษ {ru}" if ru
                 else f"หารด้วย {self._linear(u)} ลงตัว")
        second = (f"หารด้วย {self._linear(v)} แล้วเหลือเศษ {rv}" if rv
                  else f"หารด้วย {self._linear(v)} ลงตัว")
        return MathDraw(
            r"f(x) = x^3 + mx^2 + nx + p", str(value),
            prompt=("กำหนดให้ f(x) เป็นพหุนามดังต่อไปนี้ โดยที่ p เป็นจำนวนเฉพาะบวก "
                    f"และ m, n เป็นจำนวนเต็ม  ถ้า f(x) {first} แต่{second} "
                    "จงหาค่าของ mn"),
            hint=r"\text{two linear equations in } m, n, p;\ "
                 r"\text{eliminating } n \text{ forces } p",
            distractors=_distinct(str(value), [
                # mn is often 0 or small, where −mn and 2mn collapse onto it.
                str(-value), str(value + 1), str(value - 1), str(2 * value),
                str(value + 4), str(value - 4), str(value + 2),
                str(value - 2)]))


@question_type("math.posn2562_q11",
               display_name={"th": "ค่าของ m + p จากเศษเหลือที่เท่ากัน"},
               level=LEVEL, topic="การหารลงตัวและเศษเหลือ")
class EqualRemainderPair(SheetProblem):
    #: (x, y) where exactly one modulus leaves a prime remainder on both.
    _POOL = [(x, y) for x in range(40, 240, 3) for y in range(x + 7, 400, 5)
             if q11.solve(x=x, y=y) is not None]

    def expr(self, rng: Random):
        x, y = rng.choice(self._POOL)
        value = SOLVE[11](x=x, y=y)
        return MathDraw(
            rf"{x} \bmod m = {y} \bmod m = p", str(value),
            prompt=(f"ให้ m เป็นจำนวนเต็มบวก โดยที่เศษเหลือจากการหาร {x} และ {y} "
                    "ด้วย m มีค่าเท่ากัน คือ p  ถ้า p เป็นจำนวนเฉพาะบวก "
                    "จงหาค่าของ m + p"),
            hint=r"m \mid (y - x);\ \text{test each divisor on the remainder}",
            distractors=_distinct(str(value), [
                str(abs(y - x)),                   # the difference itself
                str(value + 1), str(value - 1), str(2 * value),
                str(value + 5)]))


@question_type("math.posn2562_q12",
               display_name={"th": "เศษจากการหารเลขยกกำลังซ้อนด้วยสิบ"},
               level=LEVEL, topic="การหารลงตัวและเศษเหลือ")
class NestedPowerRemainder(SheetProblem):
    def expr(self, rng: Random):
        b1, b2 = rng.choice([(2, 3), (2, 7), (3, 7), (2, 9), (3, 4), (6, 7)])
        e1 = rng.randint(1000, 2999)
        e2 = rng.randint(1000, 2999)
        outer1 = rng.choice([2020, 2024, 1996, 2016])       # a multiple of 4
        outer2 = rng.randint(2000, 2600)
        mod = rng.choice([10, 10, 10, 100])
        bases = ((b1, e1), (b2, e2))
        value = SOLVE[12](bases=bases, outer=(outer1, outer2), mod=mod)
        return MathDraw(
            rf"\left(\left({b1}^{{{e1}}}\,{b2}^{{{e2}}}\right)^{{{outer1}}}"
            rf"\right)^{{{outer2}}}",
            str(value),
            prompt=f"จงหาเศษจากการหารจำนวนต่อไปนี้ด้วย {mod}",
            hint=r"\text{last digits repeat with period } 4;\ "
                 r"\text{only the exponents mod that period matter}",
            distractors=_distinct(str(value), [
                str((value + 1) % mod), str((value - 1) % mod),
                str((value * 2) % mod), str((value + mod // 2) % mod),
                str((value + 3) % mod)]))


@question_type("math.posn2562_q13",
               display_name={"th": "ค.ร.น. จากผลบวกกำลังสองและ ห.ร.ม."},
               level=LEVEL, topic="ห.ร.ม. และ ค.ร.น.")
class LcmFromSquareSum(SheetProblem):
    #: (a² + b², gcd) leaving exactly one pair.
    _POOL = [(total, g) for g in (1, 2, 3, 5, 10)
             for total in range(5, 3000)
             if q13.solve(total=total, g=g) is not None]

    def expr(self, rng: Random):
        total, g = rng.choice(self._POOL)
        value = SOLVE[13](total=total, g=g)
        return MathDraw(
            rf"a^2 + b^2 = {total}, \quad \gcd(a, b) = {g}", str(value),
            prompt=(f"ให้ a และ b เป็นจำนวนเต็มบวก โดยที่ a² + b² = {total} "
                    f"ถ้า ห.ร.ม. ของ a และ b มีค่าเท่ากับ {g} จงหา ค.ร.น. ของ a และ b"),
            hint=r"a = gx,\ b = gy,\ \gcd(x,y) = 1:\ x^2 + y^2 = N/g^2,"
                 r"\ \operatorname{lcm} = gxy",
            distractors=_distinct(str(value), [
                str(value * g), str(value // g if g > 1 else value + 1),
                str(total // g), str(value + g), str(value + 1),
                str(value - 1), str(value + 2), str(value * 2)]))


@question_type("math.posn2562_q14",
               display_name={"th": "ค่าผสมของสัมประสิทธิ์จากพหุนามที่ยกกำลังสาม"},
               level=LEVEL, topic="พหุนามและการแยกตัวประกอบ")
class CubeRootInterpolation(SheetProblem):
    """(p(r))³ = r at each root, so p interpolates the three cube roots."""

    #: root triples that stay inside ℚ(∛2), so the answer is a clean surd form.
    _POOL = [roots for roots in ((1, 4, 8), (1, 2, 8), (1, 8, 64), (2, 4, 8),
                                 (1, 2, 4), (2, 8, 32), (1, 4, 32))
             if q14.coefficients(roots) is not None]
    _COMBOS = ((1, -7, -2), (1, -3, -1), (2, -5, -3), (1, -2, -4), (3, -7, -1))

    def expr(self, rng: Random):
        roots = rng.choice(self._POOL)
        combo = rng.choice(self._COMBOS)
        value = SOLVE[14](roots=roots, combo=combo)
        c2 = sum(roots)
        c1 = roots[0] * roots[1] + roots[1] * roots[2] + roots[0] * roots[2]
        c0 = roots[0] * roots[1] * roots[2]

        def term(coef: int, sym: str) -> str:
            if coef == 0:
                return ""
            mag = "" if abs(coef) == 1 and sym else str(abs(coef))
            return f" {'-' if coef < 0 else '+'} {mag}{sym}"

        cubic = "x^3" + term(-c2, "x^2") + term(c1, "x") + term(-c0, "")
        wanted = (f"a{term(combo[1], 'b')}{term(combo[2], 'c')}"
                  if combo[0] == 1 else
                  f"{combo[0]}a{term(combo[1], 'b')}{term(combo[2], 'c')}")
        return MathDraw(
            rf"p(x) = ax^2 + bx + c, \qquad {cubic}", _round_tex(value),
            prompt=("ให้ a, b, c เป็นจำนวนจริงที่ยังไม่ทราบค่า และ p(x) = ax² + bx + c  "
                    f"ถ้า (p(x))³ − x มี {cubic.replace('^3', '³').replace('^2', '²')} "
                    f"เป็นตัวประกอบ แล้ว {wanted.replace('  ', ' ')} มีค่าเท่าใด "
                    "(ตอบเป็นทศนิยม 4 ตำแหน่ง)"),
            hint=r"p(r) = \sqrt[3]{r} \text{ at each root; solve the Vandermonde "
                 r"system in } \mathbb{Q}(\sqrt[3]{2})",
            distractors=_distinct(_round_tex(value), [
                _round_tex(-value), _round_tex(value + 1), _round_tex(value - 1),
                _round_tex(value * 2), _round_tex(value / 2),
                _round_tex(value + 3)]))


@question_type("math.posn2562_q15",
               display_name={"th": "ระยะห่างของคอร์ดพาราโบลาที่จุดกำเนิดแบ่งครึ่ง"},
               level=LEVEL, topic="เรขาคณิตวิเคราะห์: พาราโบลา")
class OriginBisectedChord(SheetProblem):
    #: (a, b, c) whose chord length is a clean surd — c and a of opposite sign.
    _POOL = [(a, b, c) for a in range(1, 7) for b in range(-8, 9)
             for c in range(-12, 0)
             if q15.exact_square(a, b, c) is not None]

    def expr(self, rng: Random):
        a, b, c = rng.choice(self._POOL)
        SOLVE[15](a=a, b=b, c=c)              # the numeric pair still has to agree
        answer = _surd_tex(q15.exact_square(a, b, c))

        def term(coef: int, sym: str) -> str:
            if coef == 0:
                return ""
            mag = "" if abs(coef) == 1 and sym else str(abs(coef))
            return f" {'-' if coef < 0 else '+'} {mag}{sym}"

        curve = (f"{a if a != 1 else ''}x^2" + term(b, "x") + term(c, ""))
        return MathDraw(
            rf"y = {curve}", answer,
            prompt=("ให้ A และ B เป็นจุดบนพาราโบลาต่อไปนี้ ที่มีจุด (0, 0) เป็น"
                    "จุดกึ่งกลางระหว่างสองจุดนี้ จงหาระยะห่างระหว่างจุด A และจุด B"),
            hint=r"B = -A \Rightarrow 2au^2 + 2c = 0,\ v = bu,"
                 r"\quad AB = 2|u|\sqrt{1 + b^2}",
            distractors=_distinct(answer, [
                _surd_tex(q15.exact_square(a, b, c) // 4 or 1),   # half the chord
                _surd_tex(q15.exact_square(a, b, c) + 1),
                _surd_tex(1 + b * b), _surd_tex(4 * (1 + b * b)),
                _surd_tex(q15.exact_square(a, b, c) * 4),
                _surd_tex(q15.exact_square(a, b, c) + 2),
                _surd_tex(q15.exact_square(a, b, c) * 9),
                _surd_tex(q15.exact_square(a, b, c) + 5)]))


@question_type("math.posn2562_q16",
               display_name={"th": "ค่าของนิพจน์จากสมการกำลังสองที่กลับส่วนกัน"},
               level=LEVEL, topic="รากของพหุนาม")
class ReciprocalQuadraticPair(SheetProblem):
    """The second equation is the first one reversed — 1/b is a root of the first."""

    _POOL = [(p, q) for p in range(-14, 15) for q in range(-8, 9)
             if q16.solve(p=p, q=q) is not None]

    def expr(self, rng: Random):
        p, q = rng.choice(self._POOL)
        value = SOLVE[16](p=p, q=q)

        def term(coef: int, sym: str) -> str:
            if coef == 0:
                return ""
            mag = "" if abs(coef) == 1 and sym else str(abs(coef))
            return f" {'-' if coef < 0 else '+'} {mag}{sym}"

        first = "a^2" + term(p, "a") + term(q, "")
        second = (f"{q}b^2" if q != 1 else "b^2") + term(p, "b") + " + 1"
        return MathDraw(
            rf"{first} = 0, \qquad {second} = 0", str(value),
            prompt=("ให้ a และ b เป็นจำนวนจริง ซึ่ง ab ≠ 1 ถ้า a และ b สอดคล้องกับ"
                    "สมการต่อไปนี้ จงหาค่าของ (ab + a + 1)/b"),
            hint=r"\tfrac1b \text{ solves the first equation too, and } ab \ne 1"
                 r"\Rightarrow a + \tfrac1b = -p,\ \tfrac ab = q",
            distractors=_distinct(str(value), [
                str(-value), str(p + q), str(-p), str(q), str(value + 1),
                str(value - 1)]))


@question_type("math.posn2562_q17",
               display_name={"th": "ปริมาตรกล่องจากอัตราส่วนพื้นที่ผิวต่อปริมาตร"},
               level=LEVEL, topic="เรขาคณิตสามมิติ")
class SurfaceToVolumeBoxes(SheetProblem):
    #: (k1, k2, f, g) giving a positive box with a whole-number volume.
    _POOL = [(k1, k2, Fraction(f), Fraction(1, d))
             for k1 in range(1, 5) for k2 in range(1, 7)
             for f in (2, 3, 4) for d in (2, 3, 4)
             if isinstance(q17.solve(k1=k1, k2=k2, f=Fraction(f),
                                     g=Fraction(1, d)), int)]

    def expr(self, rng: Random):
        k1, k2, f, g = rng.choice(self._POOL)
        value = SOLVE[17](k1=k1, k2=k2, f=f, g=g)
        share = {2: "ครึ่งหนึ่ง", 3: "หนึ่งในสาม", 4: "หนึ่งในสี่"}[g.denominator]
        return MathDraw(
            rf"S_1 = {k1}V_1, \qquad S_2 = {k2}V_2", str(value),
            prompt=("มีกล่องทรงสี่เหลี่ยมมุมฉากที่ฐานเป็นรูปสี่เหลี่ยมจัตุรัสสองกล่อง "
                    f"กล่องแรกมีพื้นที่ผิวทั้งหกด้านรวมกันเท่ากับ {k1} เท่าของปริมาตร "
                    f"กล่องที่สองมีความสูงเป็น{share}และมีความยาวฐานเป็น {f} เท่าของ"
                    f"กล่องแรก และมีพื้นที่ผิวทั้งหกด้านของกล่องนี้รวมกันเท่ากับ {k2} "
                    "เท่าของปริมาตร จงหาปริมาตรของกล่องแรก"),
            hint=r"2s + 4h = k_1 sh \text{ and } 2fs + 4gh = k_2 fg\,sh;"
                 r"\ s \text{ cancels}",
            distractors=_distinct(str(value), [
                str(value * 2), str(value // 2 or 1), str(value + 1),
                str(value - 1), str(value * 4), str(value + 6)]))


@question_type("math.posn2562_q18",
               display_name={"th": "ด้านของลูกบาศก์ที่แนบพอดีในกรวยตรง"},
               level=LEVEL, topic="เรขาคณิตสามมิติ")
class CubeInCone(SheetProblem):
    def expr(self, rng: Random):
        radius = rng.randint(1, 6)
        height = rng.choice([h for h in range(2, 13)
                             if h * h != 2 * radius * radius])
        SOLVE[18](radius=radius, height=height)   # the numeric pair must agree
        p, q, d, den = q18.exact_form(radius, height)
        answer = _pm_surd(p, q, d, den)
        return MathDraw(
            rf"R = {radius}, \qquad H = {height}", answer,
            prompt=("กรวยตรงอันหนึ่งมีฐานเป็นรูปวงกลมรัศมี "
                    f"{radius} หน่วย และมีความสูง {height} หน่วยวัดจากยอดกรวยถึงจุด"
                    "ศูนย์กลางของฐาน กำหนดให้รูปทรงสี่เหลี่ยมลูกบาศก์รูปหนึ่งถูกแนบ"
                    "อยู่ภายในกรวยตรงอันนี้พอดี (จุดมุมสี่มุมล่างอยู่บนฐานกรวย และ"
                    "จุดมุมสี่มุมบนอยู่บนผิวข้างของกรวย) จงหาความยาวของด้านแต่ละด้าน"
                    "ของรูปทรงสี่เหลี่ยมลูกบาศก์นี้"),
            hint=r"\frac{a}{\sqrt2} = R\left(1 - \frac aH\right)",
            distractors=_distinct(answer, [
                # putting the edge midpoints on the cone instead of the corners
                _pm_surd(0, radius * height, 1, height + radius),
                _pm_surd(-p, q, d, den), _pm_surd(p, 2 * q, d, den),
                _pm_surd(p, q, d, den + 1), _pm_surd(2 * p, q, d, den)]))


@question_type("math.posn2562_q19",
               display_name={"th": "รัศมีวงกลมแนบในจากคอร์ดสัมผัสที่ขนานกับฐาน"},
               level=LEVEL, topic="เรขาคณิต: วงกลมแนบใน")
class TangentChordInradius(SheetProblem):
    """r is half the geometric mean of the two parallel sides."""

    _POOL = [(de, bc) for bc in range(4, 90) for de in range(1, bc)
             if q19.exact_square(de, bc) is not None]

    def expr(self, rng: Random):
        de, bc = rng.choice(self._POOL)
        SOLVE[19](de=de, bc=bc)               # the numeric pair still has to agree
        value = q19.exact_square(de, bc)
        return MathDraw(
            rf"DE = {de}, \qquad BC = {bc}", str(value),
            prompt=("กำหนดให้ ABC เป็นรูปสามเหลี่ยมหน้าจั่วที่ AB = AC ให้ D และ E "
                    "เป็นจุดบนด้าน AB และ AC ตามลำดับ โดยที่ DE สัมผัสวงกลมแนบใน"
                    f"สามเหลี่ยม ABC และขนานกับด้าน BC  ถ้า DE = {de} หน่วย และ "
                    f"BC = {bc} หน่วย จงหารัศมีของวงกลมแนบในสามเหลี่ยม"),
            hint=r"\text{the gap between the parallels is } 2r"
                 r"\Rightarrow r = \tfrac12\sqrt{DE \cdot BC}",
            distractors=_distinct(str(value), [
                str(2 * value),                       # the diameter
                str((de + bc) // 4 or 1), str(value + 1), str(value - 1),
                str(value * value), str(value + 2), str(value + 3),
                str(value + 4), str(3 * value)]))


@question_type("math.posn2562_q20",
               display_name={"th": "พื้นที่สามเหลี่ยมจากจุดตัดของเส้นทแยงในรูปมุมฉากสองรูป"},
               level=LEVEL, topic="เรขาคณิต: พื้นที่รูปสี่เหลี่ยม")
class RightAngleIntersectionArea(SheetProblem):
    """Two right angles make the whole figure rational — no surd ever appears."""

    def expr(self, rng: Random):
        ab = rng.randint(2, 9)
        bc = rng.randint(2, 12)
        ad = rng.randint(bc + 1, bc + 10)      # D above C, as the crop shows
        value = SOLVE[20](ab=ab, bc=bc, ad=ad, num=1, den=2)
        return MathDraw(
            rf"AB = {ab}, \quad BC = {bc}, \quad AD = {ad}",
            frac_answer_tex(value),
            prompt=("กำหนดให้ ABC และ ABD เป็นรูปสามเหลี่ยมมุมฉากที่มี "
                    "∠ABC = ∠BAD = 90° ดังรูป โดยมี "
                    f"AB = {ab}, BC = {bc} และ AD = {ad} หน่วย ลากส่วนของเส้นตรง"
                    "จากจุด B ไปแบ่งครึ่งส่วนของเส้นตรง AD ที่จุด L  ถ้า AC ตัดกับ "
                    "BD และ BL ที่จุด M และ N ตามลำดับ แล้วจงหาพื้นที่ของรูป"
                    "สามเหลี่ยม BMN"),
            hint=r"A=(0,0),\ B=(c,0),\ C=(c,h),\ D=(0,d);"
                 r"\ M,N 	ext{ are both on } AC",
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(value * 2), frac_answer_tex(value / 2),
                frac_answer_tex(Fraction(ab * bc, 2)),      # the whole triangle
                frac_answer_tex(value + 1), frac_answer_tex(value * 3),
                frac_answer_tex(Fraction(ab * ad, 2))]))


@question_type("math.posn2562_q21",
               display_name={"th": "มุมในรูปสี่เหลี่ยมจัตุรัสที่ตอบเป็นพจน์เชิงเส้นของ α"},
               level=LEVEL, topic="เรขาคณิต: สี่เหลี่ยมจัตุรัส")
class SquareAngleInAlpha(SheetProblem):
    """The midpoint is forced, so the question varies which angle it asks for."""

    _NAMES = {"dce": "∠DCE", "dcf": "∠DCF", "ecb": "∠ECB"}

    @staticmethod
    def _linear_tex(constant: Fraction, coefficient: Fraction) -> str:
        if coefficient == 0:
            return rf"{constant}^\circ"
        magnitude = abs(coefficient)
        if magnitude == 1:
            body = r"\alpha"
        elif magnitude.denominator != 1:
            top = "" if magnitude.numerator == 1 else str(magnitude.numerator)
            body = rf"\frac{{{top}\alpha}}{{{magnitude.denominator}}}"
        else:
            body = rf"{magnitude}\alpha"
        sign = "-" if coefficient < 0 else "+"
        return rf"{constant}^\circ {sign} {body}"

    def expr(self, rng: Random):
        ask = rng.choice(sorted(self._NAMES))
        constant, coefficient = SOLVE[21](num=1, den=2, ask=ask)
        answer = self._linear_tex(constant, coefficient)
        others = [self._linear_tex(*q21.ASKS[other])
                  for other in sorted(self._NAMES) if other != ask]
        return MathDraw(
            r"\angle CEF = 90^\circ, \qquad \angle BCF = \alpha", answer,
            prompt=("กำหนด ABCD เป็นรูปสี่เหลี่ยมจัตุรัสดังรูป โดยมี E เป็นจุด"
                    "กึ่งกลางของด้าน AD และ ∠CEF = 90° โดย F อยู่บนด้าน AB  "
                    f"ให้ ∠BCF = α จงหาขนาดของ {self._NAMES[ask]} ในพจน์ของ α "
                    "(คำตอบต้องไม่อยู่ในรูปของฟังก์ชันตรีโกณมิติ)"),
            hint=r"CE \text{ bisects } \angle DCF, \text{ and }"
                 r"\angle BCD = 90^\circ",
            distractors=_distinct(answer, [
                *others,
                self._linear_tex(constant, -coefficient),
                self._linear_tex(Fraction(90) - constant, coefficient),
                self._linear_tex(constant, coefficient * 2),
                self._linear_tex(constant + 15, coefficient)]))


@question_type("math.posn2562_q22",
               display_name={"th": "ผลบวกของสองมุมจากอัตราส่วนมุมและด้าน"},
               level=LEVEL, topic="เรขาคณิต: สามเหลี่ยมมุมฉาก")
class AngleRatioTriangle(SheetProblem):
    #: (k, m) whose answer lands on a whole number of degrees.
    _POOL = [(k, m) for k in (2, 3, 4, 5)
             for m in (1, 1.5, 2, 2.5, 3)
             if (lambda v: v is not None and abs(v - round(v)) < 1e-7)(
                 q22.solve(k=k, m=m))]

    def expr(self, rng: Random):
        k, m = rng.choice(self._POOL)
        value = round(SOLVE[22](k=k, m=m))
        ratio = str(int(m)) if float(m).is_integer() else str(m)
        return MathDraw(
            rf"\angle B = {k}\angle C, \qquad BC = {ratio}\,AB", str(value),
            prompt=("กำหนดให้ ΔABC เป็นรูปสามเหลี่ยม ซึ่ง "
                    f"∠B = {k}∠C และ BC = {ratio} AB  จงหา ∠A + ∠C "
                    "(ตอบเป็นองศา)"),
            hint=r"\sin A = m \sin C \Rightarrow \sin((k+1)\gamma) = m\sin\gamma,"
                 r"\quad \angle A + \angle C = 180^\circ - k\gamma",
            distractors=_distinct(str(value), [
                str(180 - value),                    # ∠B itself
                str(value + 10), str(value - 10), str(value // 2),
                str(value + 30), str(value - 30)]))


@question_type("math.posn2562_q23",
               display_name={"th": "จำนวนครั้งของการจับมือสองรอบในงานเลี้ยง"},
               level=LEVEL, topic="การนับและการจัดหมู่")
class TwoRoundHandshakes(SheetProblem):
    def expr(self, rng: Random):
        people = 2 * rng.randint(3, 40)
        value = SOLVE[23](people=people)
        return MathDraw(
            "", str(value),
            prompt=(f"ณ งานเลี้ยงหนึ่ง มีผู้ร่วมงานทั้งหมด {people} คน แต่ละคนได้รับ"
                    f"หมายเลขตามลำดับการเข้างานตั้งแต่ 1 ถึง {people} ผู้ร่วมงาน"
                    "ทักทายจับมือกันทั้งหมด 2 รอบ ดังนี้  "
                    "รอบที่ 1 คนที่มีหมายเลข i จับมือกับคนที่มีหมายเลข i+1 สำหรับ "
                    f"i = 1, 2, …, {people - 1} และคนที่ {people} จับกับคนที่ 1  "
                    "รอบที่ 2 คนที่มีหมายเลขคู่จับมือกับคนที่มีหมายเลขมากกว่าตัวเอง"
                    "ทั้งหมดที่ยังไม่เคยจับมือกัน  "
                    "อยากทราบว่าในงานนี้จะมีการจับมือทักทายกันทั้งหมดกี่ครั้ง"),
            hint=r"n + \left(\tfrac n2 - 1\right)^2",
            distractors=_distinct(str(value), [
                str(people * (people - 1) // 2),         # everyone with everyone
                str(value - people), str(value + people),
                str((people // 2 - 1) ** 2), str(value + 1)]))


@question_type("math.posn2562_q24",
               display_name={"th": "จำนวนวิธีเลือกช่องที่ต่างแถวและต่างหลัก"},
               level=LEVEL, topic="การนับเชิงการจัด")
class DistinctRowsAndColumns(SheetProblem):
    def expr(self, rng: Random):
        rows = rng.randint(3, 8)
        cols = rng.randint(3, 8)
        pick = rng.randint(2, min(rows, cols))
        value = SOLVE[24](rows=rows, cols=cols, pick=pick)
        from math import comb, factorial
        return MathDraw(
            rf"{rows} \times {cols}, \qquad \text{{choose }} {pick}", str(value),
            prompt=(f"พิจารณาตารางขนาด {rows}×{cols} ซึ่งมีทั้งหมด {rows * cols} "
                    f"ช่อง จงหาจำนวนวิธีในการเลือกช่อง {pick} ช่อง จากตาราง "
                    "โดยที่แต่ละช่องที่เลือกมาอยู่ต่างแถวและต่างหลักกันทั้งหมด"),
            hint=r"\binom{r}{k}\binom{c}{k}k!",
            distractors=_distinct(str(value), [
                str(comb(rows, pick) * comb(cols, pick)),      # forgot the matching
                str(comb(rows * cols, pick)),                  # ignored the rule
                str(value * factorial(pick)), str(value // pick or 1),
                str(value + 1), str(value - 1), str(value + 6),
                str(value * 2 + 1)]))


@question_type("math.posn2562_q25",
               display_name={"th": "ผลบวกเลขโดดที่ทำให้จำนวนหารด้วยตัวประกอบสามตัวลงตัว"},
               level=LEVEL, topic="โจทย์เลขหลักฐานสิบ")
class DigitTemplateDivisibility(SheetProblem):
    #: (template, divisor) leaving exactly one digit sum.
    _POOL = [(t, d)
             for t in ("20ab13c", "5a7b2c", "1ab2c", "9ab7c", "a1b2c", "4ab2c",
                       "7a2b5c", "3ab1c")
             for d in (36, 44, 72, 88, 99, 132, 144, 198, 264, 297, 396, 504,
                       792, 891)
             if q25.solve(template=t, divisor=d) is not None]

    def expr(self, rng: Random):
        template, divisor = rng.choice(self._POOL)
        value = SOLVE[25](template=template, divisor=divisor)
        letters = sorted({ch for ch in template if ch.isalpha()})
        listed = ", ".join(letters)
        wanted = " + ".join(letters)
        width = {5: "ห้า", 6: "หก", 7: "เจ็ด"}.get(len(template), str(len(template)))
        return MathDraw(
            rf"\overline{{{template}}} \equiv 0 \pmod{{{divisor}}}", str(value),
            prompt=(f"กำหนดให้ {listed} เป็นเลขโดด และจำนวน {template} เป็น"
                    f"จำนวนเต็ม{width}หลักที่หารด้วย {divisor} ลงตัว "
                    f"จงหาค่าของ {wanted}"),
            hint=r"\text{split the divisor into coprime factors and apply one "
                 r"digit rule per factor}",
            distractors=_distinct(str(value), [
                str(value + 1), str(value - 1), str(value + 9),
                str(27 - value), str(value * 2), str(value + 3)]))


@question_type("math.posn2562_q26",
               display_name={"th": "รากมากที่สุดของสมการที่พารามิเตอร์ตัดกันพอดี"},
               level=LEVEL, topic="รากของพหุนาม")
class ParameterCancellingRoots(SheetProblem):
    """p never has to be found — the two equations differ by exactly the shift."""

    _POOL = [(b, c, shift) for b in range(-20, 21)
             for c in range(-40, 5) for shift in (-4, -2, 2, 4)
             if q26.solve(b=b, c=c, shift=shift) is not None]

    def expr(self, rng: Random):
        b, c, shift = rng.choice(self._POOL)
        value = SOLVE[26](b=b, c=c, shift=shift)

        def term(coef: int, sym: str) -> str:
            if coef == 0:
                return ""
            mag = "" if abs(coef) == 1 and sym else str(abs(coef))
            return f" {'-' if coef < 0 else '+'} {mag}{sym}"

        first = "x^2" + term(b, "x") + term(c, "")
        tail = f"+ p {'+' if shift > 0 else '-'} {abs(shift)}"
        return MathDraw(
            rf"{first} = p, \qquad (x - r_1)(x - r_2) {tail} = 0", str(value),
            prompt=("กำหนดให้ p เป็นจำนวนจริง และ r₁, r₂ เป็นรากทั้งสองของสมการแรก "
                    "แล้วรากที่มีค่ามากที่สุดของสมการที่สองมีค่าเท่าใด"),
            hint=r"(x-r_1)(x-r_2) = x^2 + bx + c - p,\ \text{so } p \text{ cancels}",
            distractors=_distinct(str(value), [
                str(-b - value),                  # the other root
                str(value + 1), str(value - 1), str(-value), str(value * 2),
                str(value + 3), str(value - 3), str(value + 7)]))


@question_type("math.posn2562_q27",
               display_name={"th": "ความยาวลำดับที่ลบตัวประกอบใหญ่สุดทุกขั้น"},
               level=LEVEL, topic="ตัวประกอบของจำนวนเต็ม")
class LargestProperDivisorChain(SheetProblem):
    """Additive over prime removals — the sequence is never walked."""

    def expr(self, rng: Random):
        base = rng.choice([2019, 2018, 2020, 1155, 2431, 2021, 1729, 6, 12, 15])
        exponent = rng.randint(1, 3000)
        value = SOLVE[27](base=base, exponent=exponent)
        return MathDraw(
            rf"a_1 = {base}^{{{exponent}}}, \qquad a_{{n+1}} = a_n - f(a_n)",
            str(value),
            prompt=("สำหรับจำนวนเต็มบวก n ≥ 2 ใด ๆ นิยาม f(n) เป็นตัวประกอบที่ใหญ่"
                    "ที่สุดของ n ที่ไม่ใช่ตัวมันเอง กำหนดให้ลำดับดังต่อไปนี้  "
                    "ถ้า a_k คือพจน์แรกของลำดับนี้ที่มีค่าน้อยกว่า 2 "
                    "แล้ว k มีค่าเท่าใด"),
            hint=r"f(n) = n/p \text{ with } p \text{ the smallest prime;}"
                 r"\ T(p) = 1 + \textstyle\sum_q e_q(p-1)T(q)",
            distractors=_distinct(str(value), [
                str(value - 1), str(value + 1), str(exponent),
                str(2 * exponent), str(value * 2), str(value - exponent)]))


@question_type("math.posn2562_q28",
               display_name={"th": "ความน่าจะเป็นที่กบไม่ใช้ก้าวที่ยาวที่สุด"},
               level=LEVEL, topic="ความน่าจะเป็น")
class FrogStepProbability(SheetProblem):
    #: (stairs, jumps, avoided) that both routes can handle.
    _POOL = [(stairs, jumps, avoid)
             for jumps in ((1, 2, 3), (1, 2, 4), (1, 3, 4), (1, 2, 3, 4))
             for stairs in range(4, 12)
             for avoid in jumps
             if q28.solve(stairs=stairs, jumps=jumps, avoid=avoid) is not None]

    def expr(self, rng: Random):
        stairs, jumps, avoid = rng.choice(self._POOL)
        value = SOLVE[28](stairs=stairs, jumps=jumps, avoid=avoid)
        listed = ", ".join(str(j) for j in jumps[:-1]) + f" หรือ {jumps[-1]}"
        sample = SOLVE[28](stairs=3, jumps=jumps, avoid=avoid)
        return MathDraw(
            "", frac_answer_tex(value),
            prompt=(f"กบตัวหนึ่งต้องการกระโดดขึ้นบันได โดยกบสามารถกระโดดขึ้นบันได"
                    f"ได้ครั้งละ {listed} ขั้นเท่านั้น  ถ้าบันไดมี {stairs} ขั้น "
                    "จงหาความน่าจะเป็นที่กบตัวนี้ไม่มีการกระโดดขึ้นบันไดครั้งละ "
                    f"{avoid} ขั้นเลย (นับแต่ละวิธีกระโดดว่ามีโอกาสเท่ากัน)"),
            hint=r"\frac{\#\{\text{compositions avoiding } a\}}"
                 r"{\#\{\text{all compositions}\}}",
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(1 - value), frac_answer_tex(value / 2),
                frac_answer_tex(value / 3), frac_answer_tex(1 - value / 2),
                frac_answer_tex(sample) if sample is not None else
                frac_answer_tex(value / 5),
                frac_answer_tex(Fraction(1, len(jumps))),
                frac_answer_tex(value * 2 / 3),
                frac_answer_tex(value + Fraction(1, 20)),
                frac_answer_tex(value * 3 / 4), frac_answer_tex(value * 4 / 5),
                frac_answer_tex(1 - value / 3),
                frac_answer_tex(value - Fraction(1, 30))]))


@question_type("math.posn2562_q29",
               display_name={"th": "จำนวนหลอดไฟที่เปิดอยู่หลังนักเรียนสลับสถานะครบทุกคน"},
               level=LEVEL, topic="ตัวประกอบของจำนวนเต็ม")
class LockerProblemBulbs(SheetProblem):
    """A bulb ends up on exactly when its number has an odd divisor count."""

    def expr(self, rng: Random):
        bulbs = rng.randint(200, 4000)
        value = SOLVE[29](bulbs=bulbs)
        return MathDraw(
            rf"N = {bulbs}", str(value),
            prompt=(f"ในห้องประชุมแห่งหนึ่งมีหลอดไฟ {bulbs} ดวง ซึ่งแต่ละดวงติด"
                    f"หมายเลข 1 ถึง {bulbs} และมีนักเรียน {bulbs} คน เข้าไปเปลี่ยน"
                    "สถานะของหลอดไฟ (ปิดหรือเปิด) ทีละคนตามลำดับ โดยนักเรียนแต่ละ"
                    "คนจะเปลี่ยนสถานะของหลอดไฟทุกดวงที่ลำดับการเข้าของตนเองหาร"
                    "หมายเลขของหลอดไฟดวงนั้นลงตัว (เช่น นักเรียนลำดับที่ 2 จะเปลี่ยน"
                    "สถานะของหลอดไฟทุกดวงที่เป็นหมายเลขคู่) ถ้าในตอนเริ่มต้นหลอดไฟ"
                    "ทุกดวงมีสถานะเป็นปิด จงหาจำนวนหลอดไฟที่เปิดอยู่หลังจากนักเรียน"
                    f"คนที่ {bulbs} เข้าไปเปลี่ยนสถานะของหลอดไฟเสร็จแล้ว"),
            hint=r"\text{bulb } n \text{ is flipped } d(n) \text{ times, which is "
                 r"odd exactly for squares}",
            distractors=_distinct(str(value), [
                str(value + 1), str(value - 1), str(bulbs // 2),
                str(value * 2), str(bulbs // value), str(value + 5)]))


@question_type("math.posn2562_q30",
               display_name={"th": "วันเกิดจากคำพูดจริงเท็จสามวันติดกัน"},
               level=LEVEL, topic="ปริศนาเชิงตรรกะ")
class BirthdayTruthTeller(SheetProblem):
    """Built the way the sheet built it — see ``q30.build``."""

    @staticmethod
    def _make_pool() -> list[tuple]:
        rng = Random(20620)
        out: list[tuple] = []
        while len(out) < 60:
            days = rng.choice([28, 30, 31])
            birthday = rng.randint(6, days)
            s1x = tuple(rng.sample(range(1, days + 1), rng.randint(4, 7)))
            s3x = tuple(rng.sample(range(1, days + 1), rng.randint(4, 7)))
            made = q30.build(birthday, s1x, s3x, days)
            if made is None:
                continue
            first, middle, last = made
            if q30.solve(first=first, middle=middle, last=last,
                         days=days) != birthday:
                continue
            out.append((first, middle, last, days, birthday))
        return out

    _POOL: list[tuple] = []
    _MONTHS = {28: "กุมภาพันธ์", 30: "กันยายน", 31: "มกราคม"}

    def expr(self, rng: Random):
        if not self._POOL:
            BirthdayTruthTeller._POOL = self._make_pool()
        first, middle, last, days, _ = rng.choice(self._POOL)
        value = SOLVE[30](first=first, middle=middle, last=last, days=days)
        month = self._MONTHS[days]

        def listed(group) -> str:
            body = ", ".join(str(x) for x in group[:-1])
            return f"{body} และ {group[-1]}" if len(group) > 1 else str(group[0])

        return MathDraw(
            "", str(value),
            prompt=(f"ฟ้าเล่นเกมทายวันเกิดของส้มในเดือน{month}ซึ่งเป็นเดือนเกิดของ"
                    f"ส้มพอดี ซึ่งในเดือน{month} ส้มจะพูดจริงในวันที่ตรงกับเลขที่"
                    "วันเกิดของเธอเท่านั้น และโกหกในวันอื่น ๆ ทั้งหมด โดยส้มพูดกับฟ้า"
                    f"ในช่วง 3 วันที่ติดต่อกันในเดือน{month} ดังนี้  "
                    f"วันแรก ส้มพูดว่า “ฉันพูดโกหกในวันที่ {listed(first)}”  "
                    f"วันต่อมา ส้มพูดว่า “วันนี้เป็นวันที่ {listed(middle)}”  "
                    f"และวันสุดท้าย ส้มพูดว่า “ฉันพูดโกหกในวันที่ {listed(last)}”  "
                    f"จากข้อมูลที่ให้มา วันเกิดของส้มคือวันที่เท่าไหร่ในเดือน{month}"),
            hint=r"\text{“I lie on } S \text{” is true} \iff B \notin S;"
                 r"\ \text{at most one of the three days is } B",
            distractors=_distinct(str(value), [
                str(value - 2), str(value - 1), str(value + 1),
                str(first[0]), str(last[0]), str(value + 2)]))
