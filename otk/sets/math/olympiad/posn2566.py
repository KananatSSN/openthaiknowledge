"""ฟังก์ชันเวียนเกิด

คณิตศาสตร์ · โอลิมปิก (สอวน.) · สอวน.
Indicators: —

Sets moved here from: posn2566.
"""

from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from math import gcd, isqrt
from random import Random

from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem, frac_answer_tex, frac_tex
from otk.sheets import figure_attachments
from otk.sheets.posn2566_math import (
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


SHEET = "สอวน. ค่าย 1 (2566)"


SHEET_ID = "posn2566_math"


_MODULES = [q01, q02, q03, q04, q05, q06, q07, q08, q09, q10,
            q11, q12, q13, q14, q15, q16, q17, q18, q19, q20,
            q21, q22, q23, q24, q25, q26, q27, q28, q29, q30]


SOLVE = {n: lru_cache(maxsize=4096)(mod.solve)
         for n, mod in enumerate(_MODULES, start=1)}


FIGURES = figure_attachments(SHEET_ID)


class SheetProblem(WordProblem):
    """A โจทย์ from the 2566 sheet: Thai prompt, exact TeX answer."""

    sheet = SHEET
    sheet_id = SHEET_ID

    def default_figure(self) -> tuple[str, str]:
        return FIGURES.get(self.key, ("", ""))


def _distinct(value, candidates: list[str], want: int = 4) -> list[str]:
    """The first ``want`` candidates that differ from the answer and each other.

    Same guard as the 2567 sheet's: hand-picked distractors are near misses by
    construction, so at particular constants one of them *is* the answer. Offer
    more than four and filter, or a draw silently ships three choices.
    """
    out: list[str] = []
    for c in candidates:
        if c != value and c not in out:
            out.append(c)
        if len(out) == want:
            break
    return out


def _value_tex(value) -> str:
    """A solver's answer as TeX, whether it came back an int or a Fraction."""
    return frac_answer_tex(value) if isinstance(value, Fraction) else str(value)


def _pairs_tex(pairs) -> str:
    """A list of ordered pairs as TeX: ``(-1, -1), (\\frac{1}{2}, -\\frac{5}{2})``.

    ``frac_tex``, not ``frac_answer_tex``: the mixed-number form the latter
    appends is for a standalone answer, and reads as a third component inside a
    pair.
    """
    def one(v):
        return frac_tex(v) if isinstance(v, Fraction) else str(v)

    return ",\\ ".join(rf"\left({one(x)}, {one(y)}\right)" for x, y in pairs)


def _lin_tex(const: int, slope: int, sym: str = "x", *, x_first: bool = False) -> str:
    """``3 - 5x`` / ``4x + 5`` — one linear form, written the way the sheet does."""
    head = f"{'' if abs(slope) == 1 else abs(slope)}{sym}"
    if slope == 0:
        return str(const)
    if const == 0:
        return f"{'-' if slope < 0 else ''}{head}"
    if x_first:
        return f"{'-' if slope < 0 else ''}{head} {'+' if const > 0 else '-'} {abs(const)}"
    return f"{const} {'+' if slope > 0 else '-'} {head}"


#: (threshold, add) with back = add + 1 — the plateau case, where f is constant
#: at threshold + add - 1 above the threshold. Off that relation the recursion
#: has no closed form and `solve` falls back to evaluating it, which is far too
#: slow to call from a generator's pool.
POOL01 = [{"threshold": t, "add": a, "back": a + 1}
          for t in (20, 50, 60, 80, 100, 120, 200, 500)
          for a in (4, 6, 8, 10, 12)]


def _pool_q02() -> list[dict]:
    """Day fractions and a leftover share that really pin a whole crate.

    The sheet's own 3/4, 2/3, 1/2 leave 1/24 of the crate, and 1/34 is only a
    little less — the gap between the two is what the two extra oranges a day
    have to fill. Any (takes, extra, leftover) whose crate comes out a positive
    whole number is a legitimate redraw, so the pool is the scan for them.
    """
    out = []
    ladders = [(Fraction(3, 4), Fraction(2, 3), Fraction(1, 2)),
               (Fraction(2, 3), Fraction(1, 2), Fraction(1, 2)),
               (Fraction(1, 2), Fraction(2, 3), Fraction(3, 4)),
               (Fraction(4, 5), Fraction(3, 4), Fraction(2, 3)),
               (Fraction(3, 4), Fraction(1, 2)),
               (Fraction(2, 3), Fraction(3, 4)),
               (Fraction(1, 2), Fraction(1, 2)),
               (Fraction(5, 6), Fraction(1, 2))]
    for takes in ladders:
        keep = 1
        for take in takes:
            keep *= 1 - take
        for extra in (1, 2, 3, 4, 5):
            for den in range(2, 200):
                leftover = Fraction(1, den)
                if leftover >= keep:
                    continue
                p = {"takes": takes, "extra": extra, "leftover": leftover}
                total = q02.solve(**p)
                if total is not None and 8 <= total <= 4000:
                    out.append(p)
    return out


POOL02 = _pool_q02()


#: how many oranges each day removes on top of its share, spelled in Thai.
_DAY_TH = ("วันที่ 1", "วันที่ 2", "วันที่ 3", "วันที่ 4", "วันที่ 5")


def _pool_q03() -> list[dict]:
    """|p| + |q| = |p + q| pairs with opposite slopes, so the set is an interval.

    p₁ and q₁ must have opposite signs or the solution set is unbounded and the
    question has no largest member — `solve` returns None there, which is
    exactly the configuration to keep out of the pool.
    """
    out = []
    for p1 in range(-6, 0):
        for q1 in range(1, 7):
            for p0 in range(1, 10):       # positive constants, as the sheet prints
                for q0 in range(1, 10):
                    if Fraction(-p0, p1) == Fraction(-q0, q1):
                        continue          # the interval collapses to a point
                    out.append({"p": (p0, p1), "q": (q0, q1)})
    return out


POOL03 = _pool_q03()


#: the coefficients of 5a - 4b, kept small and of opposite sign as printed.
COMBOS03 = [(a, b) for a in range(1, 7) for b in range(-6, 0)]


def _pool_q04() -> list[dict]:
    """(a, b, c) whose key c + ab is small enough to factor and non-degenerate.

    key = 0 is a whole line of solutions and |x+y| is unbounded; `solve` returns
    None there. Everything else is fair, but the key is kept modest so the
    printed answer is a number a student could plausibly write down.
    """
    return [{"a": a, "b": b, "c": c}
            for a in range(2, 80) for b in range(2, 80) for c in (1, 2, 3, 4)
            if a != b and c + a * b <= 6000 and gcd(a, b) <= 2][:4000]


POOL04 = _pool_q04()


#: The constraint only collapses at m = 1 (m³ = 1 over the reals), so there is
#: one set of constants and the generator has to vary something else — the
#: letters, and how many copies of the expression are asked for.
LETTERS05 = (("a", "b"), ("x", "y"), ("p", "q"), ("u", "v"), ("s", "t"))


MULTIPLIERS05 = (1, 2, 3, 4, 5, 6, 10)


def _pool_q06() -> list[dict]:
    """Isosceles triangles whose equal side is a whole number.

    AE = 2·area/BC, and BC = √((AB/2)² + CD²), so the answer is only a printable
    fraction when the half-base and the altitude form a Pythagorean pair. The
    sheet's own 8–6–10 is the (3,4,5) triple doubled.
    """
    out = []
    for m in range(2, 9):
        for n in range(1, m):
            if (m - n) % 2 == 0 or gcd(m, n) != 1:
                continue
            leg_a, leg_b = m * m - n * n, 2 * m * n
            for k in range(1, 5):
                for half, height in ((leg_a * k, leg_b * k), (leg_b * k, leg_a * k)):
                    if half > 40 or height > 40:
                        continue
                    out.append({"base": 2 * half, "area": half * height})
    return sorted({(p["base"], p["area"]) for p in out})


POOL06 = [{"base": b, "area": a} for b, a in _pool_q06()]


def _pool_q07() -> list[dict]:
    """Angle sets whose pentagon has an area at all — and a printable one.

    Two conditions, and neither is obvious from the page. The area is invariant
    in BC only when ``∠BCE + ∠ECD − ∠(ED, ray AE) = 180°`` (the sheet's
    125 + 80 − 25), and off that relation `solve` returns None, because "the
    area" is then a function of BC rather than a number. Given the relation the
    area depends on ∠EAB and ∠ABC alone — and among all the pairs scanned only
    45°/90° and its swap give a rational one, ½·AB². So the drawing varies
    while the answer stays a number a student can write down, which is the
    item's own point.

    Every (angles, AB) combination is verified here rather than at one AB and
    scaled: `solve` identifies the quadratic numerically and rejects a
    coefficient it cannot see as zero, and that judgement is relative to an
    area which itself moves with AB. A pool checked only at AB = 4 hands the
    generator draws whose answer is None.
    """
    out = []
    for angle_a, angle_b in ((45, 90), (90, 45)):
        for angle_c in range(95, 156, 5):
            for angle_e_out in range(10, 51, 5):
                angle_dce = 180 + angle_e_out - angle_c
                if not 30 <= angle_dce <= 140:
                    continue
                for ab in range(2, 13):
                    p = {"ab": ab, "angle_a": angle_a, "angle_b": angle_b,
                         "angle_c": angle_c, "angle_dce": angle_dce,
                         "angle_e_out": angle_e_out}
                    if q07.solve(**p) == Fraction(ab * ab, 2):
                        out.append(p)
    return out


POOL07 = _pool_q07()


#: N_m = N_{m+1} forces n = 2m + 1, and then the count is m(m+1) — so only a
#: pronic number can be asked about. Anything else has no n at all.
POOL08 = [{"target": m * (m + 1)} for m in range(2, 60)]


def _pool_q09() -> list[dict]:
    """Box contents where "the ratio changed" is neither impossible nor certain.

    An empty colour kills one of the two paths and the answer degenerates to 0
    or 1, so both boxes keep at least one of each — which is also the only way
    the story reads as printed.
    """
    out = []
    for r1 in range(1, 7):
        for b1 in range(1, 7):
            for r2 in range(1, 7):
                for b2 in range(1, 7):
                    p = {"box1": (r1, b1), "box2": (r2, b2)}
                    v = q09.solve(**p)
                    if v is not None and 0 < v < 1:
                        out.append(p)
    return out


POOL09 = _pool_q09()


#: Rectangles whose 2wh is a perfect square, so r₁ + r₂ is a whole number; the
#: bound keeps the surviving root small enough that the circles really fit,
#: which is what makes the discarded root visibly impossible. A rectangle whose
#: sides are k and 2k is excluded even though it qualifies: there the sum comes
#: out exactly k = AB, and an item whose answer is a length printed in its own
#: stem can be guessed without solving anything.
POOL11 = [{"width": w, "height": h}
          for w in range(2, 81) for h in range(2, 81)
          if isqrt(2 * w * h) ** 2 == 2 * w * h
          and 0 < w + h - isqrt(2 * w * h) <= min(w, h)
          and h != 2 * w and w != 2 * h]


#: (c, rhs) whose elimination leaves a quartic with a rational root. Both are
#: kept non-negative so the printed system reads like the sheet's — a negative c
#: would print "-1 + x + xy" and "+ -1" inside the bracket. Most give one pair;
#: the sheet's own (1, 1) is one of only four in range that give more than one,
#: so "ทั้งหมด" usually means a single pair — which is still the same question,
#: since nothing tells the solver how many to expect.
POOL12 = [{"c": c, "rhs": rhs} for c in range(1, 10) for rhs in range(0, 14)
          if q12.solve(c=c, rhs=rhs)]


#: (templates, mean) whose digit equation has a solution at all. Scanned once
#: offline and frozen here: `solve` searches 10⁴ assignments per call, which is
#: fine for a cached draw but far too slow to rescan at import.
POOL15 = [
    {"templates": ("33A", "5B6", "6C3", "D11"), "mean": 500},
    {"templates": ("33A", "5B6", "6C3", "D11"), "mean": 450},
    {"templates": ("12A", "3B4", "5C6", "D78"), "mean": 400},
    {"templates": ("21A", "4B7", "9C1", "D35"), "mean": 480},
    {"templates": ("1A4", "47B", "5C2", "D72"), "mean": 500},
    {"templates": ("9A5", "B06", "35C", "D95"), "mean": 520},
    {"templates": ("A48", "4B5", "21C", "2D4"), "mean": 450},
    {"templates": ("82A", "B75", "1C7", "88D"), "mean": 520},
    {"templates": ("A82", "5B7", "C16", "99D"), "mean": 550},
    {"templates": ("49A", "B40", "2C9", "D92"), "mean": 450},
    {"templates": ("A46", "B85", "8C9", "14D"), "mean": 520},
    {"templates": ("9A4", "2B6", "9C8", "D72"), "mean": 550},
    {"templates": ("A97", "B29", "5C0", "15D"), "mean": 450},
    {"templates": ("A70", "B74", "4C4", "97D"), "mean": 400},
    {"templates": ("39A", "1B2", "C72", "9D2"), "mean": 450},
    {"templates": ("A18", "44B", "2C3", "D76"), "mean": 450},
]


#: rhs = 35·d where a² − b² = d has an integer solution — d odd or d ≡ 0 (mod 4).
#: A prime d forces the single factorisation 1 × d and the answer explodes
#: (d = 347 gives ab = 30102), so the pool keeps the answers small enough to be
#: worth writing down.
POOL17 = [{"rhs": 35 * d} for d in range(1, 400)
          if (v := q17.solve(rhs=35 * d)) is not None and v <= 600]


#: (c₁, c₂) whose common root exists. The root has to divide both constants, so
#: consecutive pairs behave like the sheet's 65/66 — gcd 1, hence x = ±1.
POOL18 = [{"c1": c1, "c2": c1 + step}
          for c1 in range(2, 120) for step in (1, 2, 3)
          if q18.solve(c1=c1, c2=c1 + step)]


#: p is stated to be *degree two*, so the optimal a must not be zero — and it is
#: zero exactly when the best p(1) comes out equal to p(±val). Those constants
#: are dropped: there the honest answer is that no admissible p attains the
#: bound, which is a different question from the one the sheet asks.
POOL19 = [{"val": val, "target": target, "big": big}
          for val in range(2, 9) for target in range(1, 10)
          for big in range(3, 14)
          if big > val
          and (v := q19.solve(val=val, target=target, big=big)) is not None
          and v != target]


#: AF = 2√(r₁² + r₁r₂ + r₂²), so an integer answer needs an Eisenstein triple —
#: (3, 5) → 49 is the sheet's own, and (7, 8) → 169 the next one up.
POOL21 = [{"r1": r1, "r2": r2} for r1 in range(1, 41) for r2 in range(1, 41)
          if isqrt(r1 * r1 + r1 * r2 + r2 * r2) ** 2
          == r1 * r1 + r1 * r2 + r2 * r2]


def _pool_q22() -> list[dict]:
    """Constants where AB is a whole number and the perimeter comes out exact.

    GD and MD have to make GDB a right triangle with whole sides — GB = 2·MD is
    the hypotenuse — and then the perimeter (FG/AB)(AB + AC + BC) has to land on
    an integer, with AC, BC, AB a genuine triangle.
    """
    out = []
    triples = [(3, 4, 5), (4, 3, 5), (6, 8, 10), (8, 6, 10), (5, 12, 13),
               (12, 5, 13), (9, 12, 15), (12, 9, 15), (8, 15, 17), (15, 8, 17)]
    for gd, db, gb in triples:
        for ad in range(1, 12):
            ab = ad + db
            for fg in range(1, 6):
                for ac in range(3, 30):
                    for bc in range(3, 30):
                        if not abs(ac - bc) < ab < ac + bc or fg > ab:
                            continue
                        if fg * (ab + ac + bc) % ab:
                            continue
                        out.append({"fg": fg, "gd": gd, "ad": ad,
                                    "md": Fraction(gb, 2), "ac": ac, "bc": bc})
    return out


POOL22 = _pool_q22()


#: BC is a chord of the small circle, so BC < 2·AB; the rest keeps the printed
#: ratio short enough to read. Sixty of these were checked against the solver's
#: independent construction before the range was fixed.
POOL23 = [{"ab": ab, "bc": bc, "cd": cd}
          for ab in range(2, 9) for bc in range(1, 2 * ab) for cd in range(1, ab + 1)
          if (v := q23.solve(ab=ab, bc=bc, cd=cd)) is not None
          and v.denominator <= 60 and v <= 40]


#: A prime total forces the mean to be 1 and the class size to be the total —
#: which is the sheet's first step and the reason 23 is printed rather than 24.
#: `solve` enumerates count vectors of size n, so the totals stay modest.
POOL24 = [{"max_score": 3, "total_score": t}
          for t in (7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43)
          if q24.solve(max_score=3, total_score=t) is not None]


#: The sheet's 2×2×2 box with the number of cubes varying. A non-cubic box is
#: not offered: the shapes that fit one are not closed under the cube's
#: symmetries, so `check`'s Burnside count — the item's whole second method —
#: does not apply there.
POOL26 = [p for p in
          ({"n": n, "a": 2, "b": 2, "c": 2} for n in range(2, 8))
          if q26.solve(**p)]


def _set_tex(values) -> str:
    return r"\{" + ",\\ ".join(str(v) for v in values) + r"\}"


#: (k, c): the quadratic is a·x² − ((k+1)a − c)x + (ka − c) = 0, which always has
#: x = 1 and a second root k − c/a, so the answer is the divisors of c plus 0.
#: c is kept composite-ish so the set is worth listing.
POOL28 = [{"k": k, "c": c} for k in range(1, 6) for c in (4, 6, 8, 9, 10, 12,
                                                          14, 15, 16, 18, 20)]


#: The halving condition has roots s = 2k and s = 4k, so the printed bound has
#: to sit at or above the small root's area and below the big one's — that is
#: the whole job of "พื้นที่มากกว่า …" and the pool keeps it doing that job.
POOL29 = [{"scale": k, "min_area": m}
          for k in range(1, 7)
          for m in range(4 * k * k, 16 * k * k, max(1, k * k // 2))]


def _truth_tex(state) -> str:
    return "(" + ",\\ ".join(r"\text{T}" if v else r"\text{F}" for v in state) + ")"


#: (known state, the two steps). Every state's orbit is checked to still be
#: running when the answer is read, so no draw asks about a step the sheet's own
#: reasoning — "seven steps on from what you were given" — cannot reach.
POOL30 = [{"known_state": s, "known_step": k, "target_step": k + d}
          for s in q30.STATES for k in (5, 10, 16) for d in (5, 7, 8, 11)]


@question_type("math.posn2566_q01", display_name={"th": "ฟังก์ชันเวียนเกิด f(f(x−k))"},
               level=LEVEL, topic="ฟังก์ชันเวียนเกิด")
class NestedRecursion(SheetProblem):
    def expr(self, rng: Random):
        p = dict(rng.choice(POOL01))
        p["start"] = p["threshold"] + rng.randint(1, 60)
        value = SOLVE[1](**p)
        t, add, back, start = p["threshold"], p["add"], p["back"], p["start"]
        return MathDraw(
            rf"f(x) = \begin{{cases}} x + {add} & x < {t} \\"
            rf" f(f(x - {back})) & x \ge {t} \end{{cases}}",
            str(value),
            prompt=(f"ให้ f เป็นฟังก์ชันซึ่งนิยามดังนี้  "
                    f"จงหาค่าของ f({start})"),
            hint=rf"{add} = {back} - 1 \Rightarrow f(x) = f(x-1) "
                 rf"\text{{ for }} {t} \le x \le {t + back - 1}",
            distractors=_distinct(str(value), [
                str(start + add),        # applied the first rule to start
                str(t + add),            # forgot the -1 at the top of the plateau
                str(start - back + add), # one step of the recursion, then stopped
                str(value + 1), str(value - 1), str(start)]))


@question_type("math.posn2566_q02", display_name={"th": "ลังส้มที่หยิบเป็นเศษส่วนทุกวัน"},
               level=LEVEL, topic="โจทย์ปัญหาเศษส่วน")
class OrangeCrate(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL02)
        total = SOLVE[2](**p)
        takes, extra, leftover = p["takes"], p["extra"], p["leftover"]
        days = "  ".join(
            f"ใน{_DAY_TH[i]} หนูปอหยิบส้มจากลังใบนี้ไป{'อีก ' if i else ' '}"
            f"{t.numerator}/{t.denominator} ของส้ม"
            f"{'ที่เหลือ' if i else 'ทั้งหมด'}และหยิบเพิ่มอีก {extra} ลูก"
            for i, t in enumerate(takes))
        last = _DAY_TH[len(takes)]
        return MathDraw(
            "", str(total),
            prompt=(f"มีส้มอยู่ในลังใบหนึ่ง  {days}  ถ้าใน{last} หนูปอพบว่าส้ม"
                    f"ที่เหลืออยู่ในลังใบนี้เท่ากับ {leftover.numerator}/"
                    f"{leftover.denominator} ของส้มทั้งหมด อยากทราบว่าในลังใบนี้"
                    f"มีส้มทั้งหมดกี่ลูก  (ในระหว่างวันเหล่านี้ไม่มีการใส่ส้มเพิ่ม"
                    f"ลงไปในลัง และไม่มีผู้อื่นที่มาหยิบส้มออกจากลังใบนี้)"),
            hint=r"R_{k} = (1 - t_k)R_{k-1} - e,\quad R_n = \ell N",
            distractors=_distinct(str(total), [
                str(total + extra), str(total - extra),
                str(leftover.denominator * len(takes)),
                str(total * leftover.numerator // leftover.denominator or 1),
                str(total + 1), str(total * 2)]))


@question_type("math.posn2566_q03", display_name={"th": "เซตคำตอบของสมการค่าสัมบูรณ์"},
               level=LEVEL, topic="ค่าสัมบูรณ์และค่าสุดขีด")
class AbsoluteValueInterval(SheetProblem):
    def expr(self, rng: Random):
        base = rng.choice(POOL03)
        left_a, left_b = rng.choice(COMBOS03)
        p = {**base, "left_a": left_a, "left_b": left_b}
        value = SOLVE[3](**p)
        (p0, p1), (q0, q1) = base["p"], base["q"]
        combo = _lin_tex(0, left_a, "a") + (
            f" {'+' if left_b > 0 else '-'} "
            f"{'' if abs(left_b) == 1 else abs(left_b)}b")
        return MathDraw(
            rf"|{_lin_tex(p0 + q0, p1 + q1)}| = "
            rf"|{_lin_tex(p0, p1)}| + |{_lin_tex(q0, q1, x_first=True)}|",
            frac_answer_tex(value),
            prompt=(f"ให้ A เป็นเซตคำตอบของสมการต่อไปนี้  ถ้า a เป็นสมาชิกใน"
                    f"เซต A ที่มีค่ามากที่สุด และ b เป็นสมาชิกในเซต A ที่มีค่า"
                    f"น้อยที่สุด แล้วค่าของ {combo} เท่ากับเท่าใด"),
            hint=r"|u| + |v| = |u + v| \iff uv \ge 0",
            distractors=_distinct(frac_answer_tex(value), [
                # the two roots swapped: a and b read off the wrong ends
                frac_answer_tex(left_a * min(Fraction(-p0, p1), Fraction(-q0, q1))
                                + left_b * max(Fraction(-p0, p1), Fraction(-q0, q1))),
                frac_answer_tex(Fraction(-p0, p1)),
                frac_answer_tex(Fraction(-q0, q1)),
                frac_answer_tex(value + 1), frac_answer_tex(value - 1),
                frac_answer_tex(-value)]))


@question_type("math.posn2566_q04", display_name={"th": "ค่ามากสุดของ |x+y| บนสมการไดโอแฟนไทน์"},
               level=LEVEL, topic="สมการไดโอแฟนไทน์เชิงเส้น")
class SimonsTrick(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL04)
        value = SOLVE[4](**p)
        a, b, c = p["a"], p["b"], p["c"]
        key = c + a * b
        return MathDraw(
            rf"{c} + {a}x + {b}y = xy", str(value),
            prompt=("ให้ x และ y เป็นจำนวนเต็มซึ่งสอดคล้องกับสมการต่อไปนี้  "
                    "จงหาค่ามากที่สุดที่เป็นไปได้ของ |x + y|"),
            hint=rf"(x - {b})(y - {a}) = {key}",
            distractors=_distinct(str(value), [
                str(abs(a + b - key - 1)),      # the d = -1 divisor
                str(key),                        # the product, not the sum
                str(a + b + 2 * isqrt(key)),     # the middle divisor
                str(value - 1), str(value + 1), str(a + b)]))


@question_type("math.posn2566_q05", display_name={"th": "ค่าที่เป็นไปได้ของนิพจน์บน a = b(a+1)"},
               level=LEVEL, topic="การจัดรูปพีชคณิต")
class ConstantOnACurve(SheetProblem):
    def expr(self, rng: Random):
        u, v = rng.choice(LETTERS05)
        k = rng.choice(MULTIPLIERS05)
        value = k * SOLVE[5](m=1, power=2)
        head = "" if k == 1 else str(k)
        return MathDraw(
            rf"{head}\left(\frac{{{u}}}{{{v}^2}} - \frac{{{v}}}{{{u}^2}} "
            rf"- {u}{v}\right)",
            frac_answer_tex(value),
            prompt=(f"ให้ {u} และ {v} เป็นจำนวนจริงที่ไม่เท่ากับศูนย์ โดยที่ "
                    f"{u} = {v}({u} + 1)  จงหาค่าที่เป็นไปได้ทั้งหมดของนิพจน์"
                    f"ต่อไปนี้"),
            hint=rf"{v} = \frac{{{u}}}{{{u}+1}} \Rightarrow "
                 rf"\frac{{({u}+1)^3 - 1 - {u}^3}}{{{u}({u}+1)}}",
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(Fraction(k)),        # forgot the factor 3
                frac_answer_tex(-value),
                frac_answer_tex(value + k), frac_answer_tex(value - k),
                frac_answer_tex(Fraction(3 * k, 2)), "0"]))


@question_type("math.posn2566_q06", display_name={"th": "ส่วนสูง AE ในสามเหลี่ยมหน้าจั่ว"},
               level=LEVEL, topic="เรขาคณิต: สามเหลี่ยมมุมฉาก")
class TwoAltitudes(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL06)
        value = SOLVE[6](**p)
        base, area = p["base"], p["area"]
        height = Fraction(2 * area, base)
        side = isqrt((Fraction(base, 2) ** 2 + height ** 2).numerator)
        return MathDraw(
            "", frac_answer_tex(value),
            prompt=(f"กำหนด ABC เป็นรูปสามเหลี่ยมมีพื้นที่ {area} ตารางหน่วย "
                    f"ให้จุด D และจุด E อยู่บนด้าน AB และ BC ตามลำดับ ซึ่งทำให้ "
                    f"CD ตั้งฉากกับ AB และ AE ตั้งฉากกับ BC  ถ้า AC = BC และ "
                    f"AB = {base} จงหาความยาวของ AE "
                    f"(เขียนคำตอบเป็นเศษส่วนอย่างต่ำ)"),
            hint=r"\tfrac12 \cdot AB \cdot CD = \tfrac12 \cdot BC \cdot AE",
            # Halving and doubling lead, so the answer is not the one fraction
            # among whole numbers.
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(value / 2),           # dropped the ½ on one side
                frac_answer_tex(height),              # CD, the other altitude
                frac_answer_tex(value * 2),
                str(side),                            # BC itself
                frac_answer_tex(Fraction(base, 2)),
                str(area)]))


@question_type("math.posn2566_q07", display_name={"th": "พื้นที่รูปห้าเหลี่ยมจากมุมที่กำหนด"},
               level=LEVEL, topic="เรขาคณิต: พื้นที่รูปสี่เหลี่ยม")
class InvariantPentagon(SheetProblem):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def expr(self, rng: Random):
        p = rng.choice(POOL07)
        value = SOLVE[7](**p)
        ab = p["ab"]
        return MathDraw(
            "", _value_tex(value),
            prompt=(f"กำหนด ABCE เป็นรูปสี่เหลี่ยมรูปหนึ่ง ที่มีด้าน AB ยาว "
                    f"{ab} หน่วย ด้าน BC ยาวไม่เกิน {ab} หน่วย และ CDE เป็นรูป"
                    f"สามเหลี่ยมรูปหนึ่ง โดยที่มุม EAB กาง {p['angle_a']} องศา "
                    f"มุม ABC กาง {p['angle_b']} องศา มุม BCE กาง "
                    f"{p['angle_c']} องศา มุม ECD กาง {p['angle_dce']} องศา "
                    f"และรังสี ED ทำมุม {p['angle_e_out']} องศากับส่วนต่อของ AE "
                    f"โดยที่ D และ B อยู่คนละข้างของ AE  "
                    f"จงหาพื้นที่ของรูปห้าเหลี่ยม ABCDE"),
            # No shipped crop: the sheet's drawing prints AB = 4 and all five
            # angles, every one of which this generator redraws.
            figure=None,
            hint=r"\angle BCE + \angle ECD - 180^\circ = "
                 r"\angle(ED, \overrightarrow{AE}) \Rightarrow "
                 r"[ABCDE] \text{ is free of } BC",
            distractors=_distinct(_value_tex(value), [
                str(ab * ab),                      # forgot the half
                _value_tex(Fraction(ab * ab, 4)),
                str(2 * ab * ab),
                str(4 * ab),
                _value_tex(Fraction(ab, 2)),
                str(ab * ab + 2)]))


@question_type("math.posn2566_q08", display_name={"th": "จำนวนจุดจากจำนวนเส้นเชื่อมสองสี"},
               level=LEVEL, topic="การนับเชิงการจัด")
class BicolouredChords(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL08)
        value = SOLVE[8](**p)
        target, m = p["target"], (value - 1) // 2
        return MathDraw(
            rf"N_m = N_{{m+1}} = {target}", str(value),
            prompt=("มีจุดอยู่บนเส้นรอบวงของวงกลมจำนวน n จุด โดยที่ n ≥ 2 "
                    "กำหนดสีจุดแต่ละจุดเป็นสีแดงหรือสีดำสีใดสีหนึ่งเพียงสีเดียว "
                    "ลากเส้นเชื่อมต่อระหว่างจุดสองจุดใด ๆ บนเส้นรอบวงที่มีสีต่างกัน "
                    "ให้ N_k แทนจำนวนเส้นเชื่อมที่ลาก เมื่อมีจุดสีดำบนเส้นรอบวง"
                    "จำนวน k จุด  ถ้าพบว่า N_m เท่ากับ N_(m+1) ตามที่กำหนด "
                    "สำหรับบาง m ในเซต {1, 2, 3, …, n − 1}  จงหาค่าของ n"),
            hint=r"N_k = k(n-k),\quad N_m = N_{m+1} \Rightarrow n = 2m + 1",
            distractors=_distinct(str(value), [
                str(value + 1),            # forgot that n must be odd
                str(m),                    # answered m instead of n
                str(m + 1),
                str(target),
                str(2 * m), str(value - 2)]))


@question_type("math.posn2566_q09", display_name={"th": "ความน่าจะเป็นที่อัตราส่วนในกล่องเปลี่ยน"},
               level=LEVEL, topic="ความน่าจะเป็น")
class SwappedMarbles(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL09)
        value = SOLVE[9](**p)
        (r1, b1), (r2, b2) = p["box1"], p["box2"]
        n1, n2 = r1 + b1, r2 + b2
        # The classic slip: forgetting that box 2 holds one marble more than it
        # started with by the time the second draw happens.
        naive = Fraction(r1 * b2 + b1 * r2, n1 * n2)
        return MathDraw(
            "", frac_answer_tex(value),
            prompt=(f"มีกล่องบรรจุลูกแก้วจำนวน 2 ใบ โดยที่กล่องใบที่ 1 มีลูกแก้ว"
                    f"สีแดง {r1} ลูก สีน้ำเงิน {b1} ลูก และกล่องใบที่ 2 มีลูกแก้ว"
                    f"สีแดง {r2} ลูก สีน้ำเงิน {b2} ลูก  สุ่มหยิบลูกแก้ว 2 ครั้ง "
                    f"ครั้งละ 1 ลูก โดยครั้งแรกสุ่มหยิบลูกแก้ว 1 ลูกจากกล่องใบที่ 1 "
                    f"นำมาใส่ในกล่องใบที่ 2 ครั้งที่สองสุ่มหยิบลูกแก้ว 1 ลูกจาก"
                    f"กล่องใบที่ 2 นำมาใส่ในกล่องใบที่ 1  จงหาความน่าจะเป็นที่"
                    f"ในแต่ละกล่อง อัตราส่วนของจำนวนลูกแก้วสีแดงต่อจำนวนลูกแก้ว"
                    f"สีน้ำเงินไม่เหมือนเดิม (เขียนคำตอบเป็นเศษส่วนอย่างต่ำ)"),
            hint=r"P = \frac{r_1}{n_1}\cdot\frac{b_2}{n_2+1} "
                 r"+ \frac{b_1}{n_1}\cdot\frac{r_2}{n_2+1}",
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(naive),            # box 2 not counted as n₂+1
                frac_answer_tex(1 - value),        # answered "unchanged"
                frac_answer_tex(Fraction(r1, n1) * Fraction(b2, n2 + 1)),
                frac_answer_tex(Fraction(1, 2)),
                frac_answer_tex(Fraction(r1 + r2, n1 + n2)),
                frac_answer_tex(value / 2)]))


@question_type("math.posn2566_q10", display_name={"th": "คู่อันดับที่รากเป็นจำนวนเต็มบวกต่างกัน"},
               level=LEVEL, topic="รากของพหุนาม")
class IntegerRootPairs(SheetProblem):
    def expr(self, rng: Random):
        digits = rng.randint(6, 20)
        value = SOLVE[10](digits=digits)
        top = digits - 1
        return MathDraw(
            r"x^2 - ax + b = 0", str(value),
            prompt=(f"ให้ S เป็นเซตของคู่อันดับ (a, b) โดยที่ a, b ∈ "
                    f"{{0, 1, 2, …, {top}}} และ a > b  จงหาจำนวนคู่อันดับ (a, b) "
                    f"ทั้งหมดในเซต S ที่ทำให้สมการต่อไปนี้มีคำตอบทั้งหมดเป็น"
                    f"จำนวนเต็มบวกที่แตกต่างกัน"),
            hint=r"p + q > pq \iff (p-1)(q-1) < 1 \iff p = 1 \text{ or } q = 1",
            distractors=_distinct(str(value), [
                str(value + 1),        # let k run all the way to the top digit
                str(value + 2),
                str(top),
                str(value - 1),
                str(digits), str(2 * value)]))


@question_type("math.posn2566_q11", display_name={"th": "ผลบวกรัศมีของวงกลมสัมผัสในสี่เหลี่ยม"},
               level=LEVEL, topic="เรขาคณิต: วงกลมสัมผัสกัน")
class TangentCornerCircles(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL11)
        value = SOLVE[11](**p)
        w, h = p["width"], p["height"]
        return MathDraw(
            "", str(value),
            prompt=(f"ให้ ABCD เป็นรูปสี่เหลี่ยมผืนผ้าที่มีด้าน AB ยาว {w} หน่วย "
                    f"และด้าน BC ยาว {h} หน่วย  ให้ T₁ เป็นวงกลมที่มีจุดศูนย์กลาง "
                    f"O₁ รัศมี r₁ ซึ่งสัมผัสกับด้าน AD และด้าน CD และให้ T₂ เป็น"
                    f"วงกลมที่มีจุดศูนย์กลาง O₂ รัศมี r₂ ซึ่งสัมผัสกับด้าน AB และ"
                    f"ด้าน BC และสัมผัสกับวงกลม T₁  จงหาค่าของ r₁ + r₂"),
            # The crop is lettered only, but it draws AB as the longer side —
            # so it ships on the landscape draws and stands down on the rest.
            figure="" if w > h else None,
            hint=r"s = r_1 + r_2:\ (w-s)^2 + (s-h)^2 = s^2 "
                 r"\Rightarrow s = (w+h) \pm \sqrt{2wh}",
            distractors=_distinct(str(value), [
                str(w + h + isqrt(2 * w * h)),     # the impossible second root
                str(w + h),
                str(isqrt(2 * w * h)),
                str(value * 2), str(value + 1), str(min(w, h))]))


@question_type("math.posn2566_q12", display_name={"th": "คู่อันดับตรรกยะจากระบบสมการ"},
               level=LEVEL, topic="ระบบสมการไม่เชิงเส้น")
class RationalPairSystem(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL12)
        pairs = SOLVE[12](**p)
        c, rhs = p["c"], p["rhs"]
        # the x = 0 branch the first equation forbids, and the pairs with y
        # read off the wrong sign — both are what a hurried elimination gives.
        flipped = tuple((x, -y) for x, y in pairs)
        return MathDraw(
            rf"{c} + x + xy = x^2 \qquad "
            rf"x^2\bigl(({c} + y)(x + y) + {c}\bigr) = {rhs}",
            _pairs_tex(pairs),
            prompt=("จงหาคู่อันดับของจำนวนตรรกยะ (x, y) ทั้งหมด "
                    "ซึ่งเป็นคำตอบของระบบสมการต่อไปนี้"),
            hint=rf"x \ne 0 \Rightarrow y = x - \frac{{{c}}}{{x}} - 1",
            distractors=_distinct(_pairs_tex(pairs), [
                _pairs_tex(flipped),
                _pairs_tex(pairs[:-1]) if len(pairs) > 1 else _pairs_tex(
                    tuple((y, x) for x, y in pairs)),
                _pairs_tex(tuple((y, x) for x, y in pairs)),
                _pairs_tex(pairs + ((Fraction(0), Fraction(0)),)),
                _pairs_tex(tuple((x, y + 1) for x, y in pairs)),
                _pairs_tex(tuple((-x, y) for x, y in pairs))]))


@question_type("math.posn2566_q13", display_name={"th": "จำนวนสามสิ่งอันดับของเซต"},
               level=LEVEL, topic="เพาเวอร์เซตและการนับสับเซต")
class CoveringTuples(SheetProblem):
    def expr(self, rng: Random):
        sets = rng.choice([2, 3, 3, 3, 4])
        universe = rng.randint(4, 20)
        value = SOLVE[13](universe=universe, sets=sets)
        base = 2 ** sets - 2
        names = "ABCDE"[:sets]
        tuple_th = {2: "คู่อันดับ", 3: "สามสิ่งอันดับ", 4: "สี่สิ่งอันดับ"}[sets]
        union = " ∪ ".join(names)
        meet = " ∩ ".join(names)
        # 12 digits at the sheet's own constants, so the power is the answer's
        # readable form — as on 2567 ข้อ 28.
        def power(b: int) -> str:
            return rf"{b}^{{{universe}}}" if universe > 1 else str(b)
        assert value == base ** universe        # the printed power *is* the count
        return MathDraw(
            "", power(base),
            prompt=(f"จงหาจำนวนของ{tuple_th}ของเซต "
                    f"({', '.join(names)}) ทั้งหมดที่สอดคล้องกับเงื่อนไขต่อไปนี้  "
                    f"1) {union} = {{1, 2, 3, …, {universe}}}  "
                    f"2) {meet} = ∅"),
            hint=r"\text{each element picks one of } 2^k - 2 \text{ patterns}",
            distractors=_distinct(power(base), [
                power(2 ** sets),          # forgot both forbidden patterns
                power(2 ** sets - 1),      # forgot only one
                power(base + 1),
                rf"{base}^{{{universe - 1}}}",
                rf"{universe}^{{{base}}}",
                power(base - 1)]))


@question_type("math.posn2566_q14", display_name={"th": "จัดที่นอนโดยมีคู่ติดกันและคู่ที่ต้องแยก"},
               level=LEVEL, topic="การนับและการจัดหมู่")
class AdjacentBeds(SheetProblem):
    def expr(self, rng: Random):
        beds = rng.randint(5, 30)
        value = SOLVE[14](beds=beds)
        slots = beds - 1
        disjoint = slots * slots - slots - 2 * (beds - 2)
        return MathDraw(
            "", str(value),
            prompt=(f"มีคน 4 คน คือ A, B, C และ D เข้าพักห้องพักห้องหนึ่ง"
                    f"ซึ่งมีเตียงเดี่ยว {beds} เตียงเรียงกันเป็นแถวตรง โดยที่การ"
                    f"เลือกเตียงนอนของคนทั้ง 4 คนมีเงื่อนไข ดังนี้  "
                    f"1) A กับ B อยากได้เตียงนอนติดกัน  "
                    f"2) C กับ D อยากได้เตียงนอนติดกัน  "
                    f"3) A กับ C ไม่ต้องการได้เตียงนอนติดกัน  "
                    f"จงหาจำนวนวิธีที่จะจัดที่นอนให้ 4 คนนี้ตามต้องการ"),
            hint=r"4 \cdot \#\{\text{disjoint slot pairs}\} - 2(B - 3)",
            distractors=_distinct(str(value), [
                str(4 * disjoint),            # forgot condition 3
                str(disjoint),                # forgot the orders inside a block
                str(2 * disjoint),
                str(value + 2), str(value - 2),
                str(4 * disjoint - (beds - 3))]))


@question_type("math.posn2566_q15", display_name={"th": "จำนวนสี่หลักมากที่สุดจากเลขโดดที่กำหนด"},
               level=LEVEL, topic="ทฤษฎีจำนวน: เลขโดด")
class LargestArrangement(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL15)
        value = SOLVE[15](**p)
        shown = ", ".join(p["templates"])
        digits = sorted((int(d) for d in str(value)), reverse=True)
        # the smallest arrangement of the same digits: the smallest non-zero
        # digit leads, since a four-digit number cannot open with 0.
        low = sorted(digits)
        lead = next(i for i, d in enumerate(low) if d)
        smallest = int("".join(str(d) for d in
                               [low[lead]] + low[:lead] + low[lead + 1:]))
        return MathDraw(
            "", str(value),
            prompt=(f"ให้จำนวนนับสามหลักในรูปฐานสิบ 4 จำนวน คือ {shown} เมื่อ "
                    f"A, B, C, D ∈ {{0, 1, 2, 3, …, 9}} และค่าเฉลี่ยเลขคณิตของ"
                    f"จำนวนนับทั้งสี่จำนวนดังกล่าวมีค่าเท่ากับ {p['mean']}  "
                    f"ให้ S แทนเซตของจำนวนสี่หลักทั้งหมดที่เกิดจากนำเลขโดด "
                    f"A, B, C และ D ทุกตัวมาจัดเรียงเป็นจำนวนที่มีสี่หลัก  "
                    f"จงหาสมาชิกของเซต S ที่มีค่ามากที่สุด"),
            hint=r"\sum \text{templates} = 4\mu \Rightarrow "
                 r"\text{a linear equation in } A, B, C, D",
            distractors=_distinct(str(value), [
                str(smallest),          # answered the smallest member of S
                str(value - 1), str(value + 1),
                str(value - 100), str(value + 100),
                str(int(str(value)[::-1]))]))


@question_type("math.posn2566_q16", display_name={"th": "พหุนามที่มีรากเลื่อนไปหนึ่ง"},
               level=LEVEL, topic="รากของพหุนาม")
class ShiftedRoots(SheetProblem):
    def expr(self, rng: Random):
        coef = rng.choice([rng.randint(2, 40), rng.randint(1900, 2100),
                           rng.randint(100, 999)])
        tail = rng.choice([1, 1, 2, 3, 5])
        value = SOLVE[16](coef=coef, tail=tail)
        return MathDraw(
            rf"x^3 - {coef}x^2 = {tail} \qquad "
            rf"p(x) = x^3 + a_2x^2 + a_1x + a_0",
            str(value),
            prompt=(f"ให้ r₁, r₂ และ r₃ เป็นคำตอบของสมการ x³ − {coef}x² = "
                    f"{tail} และ p(x) เป็นพหุนามที่มีสัมประสิทธิ์เป็นจำนวนจริง"
                    f"ตามที่กำหนด โดยที่ p(r₁ + 1) = p(r₂ + 1) = p(r₃ + 1) = 0  "
                    f"จงหาค่าของ |p(1) + p(−1)|"),
            hint=r"p(x) = q(x-1) \text{ where } q(x) = x^3 - cx^2 - t",
            distractors=_distinct(str(value), [
                str(4 * coef + 2 * tail),      # dropped the constant 8
                str(4 * coef + 8),             # dropped the tail
                str(coef), str(value + 2), str(value - 2),
                str(2 * coef + tail)]))


@question_type("math.posn2566_q17", display_name={"th": "ค่าน้อยสุดของ ab ที่ไม่เป็นลบ"},
               level=LEVEL, topic="ทฤษฎีจำนวนเชิงพีชคณิต")
class LeastProduct(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL17)
        value = SOLVE[17](**p)
        rhs = p["rhs"]
        return MathDraw(
            rf"(6a + b)^2 - (a + 6b)^2 = {rhs}", str(value),
            prompt=("ให้ a และ b เป็นจำนวนเต็มที่สอดคล้องกับสมการต่อไปนี้  "
                    "จงหาค่าของ ab ที่น้อยที่สุดที่ไม่เป็นลบ"),
            hint=r"(6a+b)^2 - (a+6b)^2 = 35(a^2 - b^2)",
            distractors=_distinct(str(value), [
                str(rhs // 35),              # answered a² − b²
                str(value + 1), str(value - 1) if value else str(value + 2),
                str(rhs), str(2 * value), str(rhs // 70)]))


@question_type("math.posn2566_q18", display_name={"th": "พหุนามดีกรีห้าสองอันที่มีรากร่วม"},
               level=LEVEL, topic="พหุนามสัมประสิทธิ์จำนวนเต็ม")
class SharedQuinticRoot(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL18)
        pairs = sorted(SOLVE[18](**p))
        c1, c2 = p["c1"], p["c2"]
        answer = _pairs_tex(pairs)
        return MathDraw(
            rf"x^5 + mx - {c1} = 0 \qquad x^5 + nx - {c2} = 0",
            answer,
            prompt=("จงหาคู่อันดับของจำนวนเต็ม (m, n) ทั้งหมด ที่ทำให้สมการ"
                    "ทั้งสองต่อไปนี้มีคำตอบร่วมกันอย่างน้อยหนึ่งคำตอบ"),
            hint=r"x \mid c_1 \text{ and } x \mid c_2,\quad "
                 r"m = \frac{c_1 - x^5}{x}",
            distractors=_distinct(answer, [
                _pairs_tex([(n, m) for m, n in pairs]),
                _pairs_tex(pairs[:1]),
                _pairs_tex([(m, n) for m, n in pairs][:1] + [(0, 1)]),
                _pairs_tex([(c1 - 1, c2 - 1)]),
                _pairs_tex([(-m, -n) for m, n in pairs]),
                _pairs_tex([(m + 1, n + 1) for m, n in pairs])]))


@question_type("math.posn2566_q19", display_name={"th": "ค่ามากที่สุดของ p(1) ของพหุนามกำลังสอง"},
               level=LEVEL, topic="เรนจ์ของฟังก์ชันกำลังสอง")
class MaximalValue(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL19)
        value = SOLVE[19](**p)
        val, target, big = p["val"], p["target"], p["big"]
        return MathDraw(
            "", str(value),
            prompt=(f"ให้ p(x) เป็นพหุนามดีกรีสองที่มีสัมประสิทธิ์เป็นจำนวนจริง "
                    f"โดยที่ p({val}) = p(−{val}) = {target} และ p({big}) > 0  "
                    f"ถ้า p(1) เป็นจำนวนเต็ม แล้วค่ามากที่สุดที่เป็นไปได้ของ "
                    f"p(1) เท่ากับเท่าใด"),
            hint=r"p(x) = a(x^2 - v^2) + t,\quad p(1) = t + a(1 - v^2)",
            distractors=_distinct(str(value), [
                str(target),                  # took a = 0
                str(value + 1), str(value - 1),
                str(target + val * val), str(2 * value), str(value + val)]))


@question_type("math.posn2566_q20", display_name={"th": "m น้อยที่สุดที่ 2^(2^m) − 1 หารลงตัว"},
               level=LEVEL, topic="การหารลงตัวและเศษเหลือ")
class FermatDivisor(SheetProblem):
    def expr(self, rng: Random):
        k = rng.randint(1, 12)
        exp = 2 ** k
        value = SOLVE[20](exp=exp)
        return MathDraw(
            rf"2^{{{exp}}} + 1 \mid 2^{{(2^m)}} - 1", str(value),
            prompt=(f"จงหาจำนวนเต็มบวก m ที่น้อยที่สุด ที่ทำให้ 2^{exp} + 1 "
                    f"หาร 2^(2^m) − 1 ลงตัว"),
            hint=r"2^{(2^m)} - 1 = \prod_{j<m} F_j,\quad F_j = 2^{(2^j)} + 1",
            distractors=_distinct(str(value), [
                str(k),                     # answered the Fermat index itself
                str(k + 2), str(exp),
                str(2 * k), str(exp + 1), str(value + 3)]))


@question_type("math.posn2566_q21", display_name={"th": "ความยาว AF จากวงกลมสามวง"},
               level=LEVEL, topic="เรขาคณิต: กำลังของจุด")
class ThreeCircles(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL21)
        value = SOLVE[21](**p)
        r1, r2 = p["r1"], p["r2"]
        power = 2 * r1 * (2 * r1 + r2)          # AB · AO₂
        return MathDraw(
            "", str(value),
            prompt=(f"ให้ C₁, C₂ และ C₃ เป็นวงกลมสามวง โดยมี O₁, O₂ และ O₃ เป็น"
                    f"จุดศูนย์กลางของวงกลม C₁, C₂ และ C₃ ตามลำดับ  วงกลม C₁ มี"
                    f"รัศมียาว {r1} หน่วย และวงกลม C₂ มีรัศมียาว {r2} หน่วย  "
                    f"วงกลม C₁ และวงกลม C₂ สัมผัสกันที่จุด B และวงกลม C₂ ผ่าน"
                    f"จุด O₃  AD เป็นส่วนของเส้นตรงที่ทำให้ AB และ BD เป็นเส้น"
                    f"ผ่านศูนย์กลางของวงกลม C₁ และวงกลม C₂ ตามลำดับ  วงกลม C₃ "
                    f"ผ่านจุด O₂ และตัดกับวงกลม C₁ ที่จุด B และจุด E  AF เป็น"
                    f"ส่วนของเส้นตรงที่ตัดวงกลม C₁ และวงกลม C₃ ที่จุด A, E และ F  "
                    f"จงหาความยาวของ AF"),
            # Lettered only, but drawn with C₂ the larger circle — so it ships
            # on those draws and passes figure=None on the rest.
            figure="" if r2 > r1 else None,
            hint=r"AE \cdot AF = AB \cdot AO_2,\quad "
                 r"AF = 2\sqrt{r_1^2 + r_1r_2 + r_2^2}",
            distractors=_distinct(str(value), [
                str(power),                     # answered the power of A
                str(2 * (r1 + r2)),             # dropped the cross term
                str(r1 + 2 * r2 + 1),
                str(2 * r1 + r2), str(value + 2), str(value - 2)]))


@question_type("math.posn2566_q22", display_name={"th": "ความยาวรอบรูปสามเหลี่ยมจากเส้นตั้งฉาก"},
               level=LEVEL, topic="เรขาคณิต: สามเหลี่ยมมุมฉาก")
class PerpendicularTriangle(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL22)
        value = SOLVE[22](**{k: float(v) if isinstance(v, Fraction) else v
                             for k, v in p.items()})
        md = p["md"]
        gb = 2 * md                                   # always a whole number
        ab = p["ad"] + isqrt(int(gb) ** 2 - p["gd"] ** 2)
        md_th = (str(md.numerator) if md.denominator == 1
                 else f"{md.numerator}/{md.denominator}")
        return MathDraw(
            "", str(int(value)),
            prompt=(f"ให้ ABC เป็นรูปสามเหลี่ยมที่มีด้าน AC ยาว {p['ac']} หน่วย "
                    f"ด้าน BC ยาว {p['bc']} หน่วย  ลากเส้นตั้งฉากกับด้านทั้งสาม"
                    f"ทำให้เกิดรูปสามเหลี่ยม EFG ภายใน โดยที่ FG และ GD อยู่บน"
                    f"เส้นตั้งฉากกับ AB ที่จุด D และ FG = {p['fg']}, GD = "
                    f"{p['gd']}, AD = {p['ad']}  จุด M เป็นจุดกึ่งกลางของส่วนของ"
                    f"เส้นตรง GB โดย MD = {md_th}  จงหาความยาวรอบรูปสามเหลี่ยม EFG"),
            # the sheet's drawing prints all six of these lengths.
            figure=None,
            hint=r"GB = 2\,MD \Rightarrow AB;\quad "
                 r"EFG \sim CAB \text{ with ratio } FG : AB",
            distractors=_distinct(str(int(value)), [
                str(p["ac"] + p["bc"] + ab),     # the perimeter of ABC itself
                str(int(value) + p["fg"]), str(int(value) - p["fg"]),
                str(ab), str(2 * int(value)), str(int(value) + 1)]))


@question_type("math.posn2566_q25", display_name={"th": "พื้นที่แรเงาของวงกลมหกวง"},
               level=LEVEL, topic="เรขาคณิต: ความยาวส่วนโค้ง")
class SixCircleRosette(SheetProblem):
    def expr(self, rng: Random):
        r = rng.randint(1, 9)
        SOLVE[25](r=r)                       # the float the exact form must match
        k = r * r
        head = "" if k == 1 else str(3 * k)
        exact = (r"3\pi - 3\sqrt{3}" if k == 1
                 else rf"{3 * k}\pi - {3 * k}\sqrt{{3}}")
        return MathDraw(
            "", exact,
            prompt=(f"วงกลมวงเล็กที่มีรัศมียาว {r} หน่วยจำนวน 6 วง ตัดกันที่"
                    f"จุดศูนย์กลางของวงกลมวงใหญ่ โดยที่วงกลมวงเล็กสองวงที่อยู่"
                    f"ถัดกันผ่านจุดศูนย์กลางของกันและกัน และมีจุดตัดจุดหนึ่งบน"
                    f"วงกลมวงใหญ่  ส่วนที่แรเงาคือบริเวณภายในวงกลมวงใหญ่ที่อยู่ใน"
                    f"วงกลมวงเล็กเป็นจำนวนวงคี่วง  จงหาพื้นที่ของส่วนที่แรเงา"),
            hint=r"R = r\sqrt3,\quad A_1 = \pi r^2,\ A_2 = 3\sqrt3 r^2,\ "
                 r"A_3 = (2\pi - 3\sqrt3)r^2",
            # One two-term slip leads, so the answer is not the one binomial.
            distractors=_distinct(exact, [
                rf"{3 * k}\pi - {6 * k}\sqrt{{3}}",
                rf"{3 * k}\pi" if k != 1 else r"3\pi",          # the whole disc
                rf"{3 * k}\sqrt{{3}}" if k != 1 else r"3\sqrt{3}",
                (rf"{k}\pi" if k != 1 else r"\pi"),
                rf"{2 * 3 * k}\pi - {3 * k}\sqrt{{3}}",
                rf"{head or 3}\pi + {head or 3}\sqrt{{3}}"]))


@question_type("math.posn2566_q23", display_name={"th": "อัตราส่วน EG/ED ในวงกลมสองวง"},
               level=LEVEL, topic="เรขาคณิต: กำลังของจุด")
class TwoCircleRatio(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL23)
        value = SOLVE[23](**p)
        ab, bc, cd = p["ab"], p["bc"], p["cd"]
        gf = Fraction(2 * ab * cd, bc)          # = GC, from the power of C
        return MathDraw(
            "", frac_answer_tex(value),
            prompt=(f"ให้ A เป็นจุดศูนย์กลางของวงกลมวงเล็ก ซึ่งตัดกับวงกลม"
                    f"วงใหญ่ที่จุด B โดยที่จุด A อยู่บนวงกลมวงใหญ่ด้วย  ให้ C "
                    f"เป็นจุดบนวงกลมวงเล็ก และ E, F, G เป็นจุดบนวงกลมวงใหญ่ "
                    f"โดยที่ A, C, D, F อยู่บนเส้นตรงเดียวกัน  B, C, G อยู่บน"
                    f"เส้นตรงเดียวกัน  และ D เป็นจุดที่ EG ตัดกับ AF  "
                    f"ถ้า AB = {ab} และ BC = {bc}, CD = {cd} และ GD ตั้งฉากกับ "
                    f"CF  จงหาค่าของ EG/ED (เขียนคำตอบเป็นเศษส่วนอย่างต่ำ)"),
            hint=r"CA \cdot CF = CB \cdot CG,\quad ED \cdot DG = DA \cdot DF",
            distractors=_distinct(frac_answer_tex(value), [
                frac_answer_tex(value - 1),          # answered DG/ED
                frac_answer_tex(1 / value),
                frac_answer_tex(gf),                 # answered GF
                frac_answer_tex(Fraction(cd * (ab + cd))),   # the power of D
                frac_answer_tex(value + 1),
                frac_answer_tex(Fraction(2 * ab, bc))]))


@question_type("math.posn2566_q24", display_name={"th": "ค่าเฉลี่ยและฐานนิยมสองค่าของคะแนนสอบ"},
               level=LEVEL, topic="สถิติ: ค่ากลางของข้อมูล")
class TwoModes(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL24)
        value = SOLVE[24](**p)
        top, total = p["max_score"], p["total_score"]
        return MathDraw(
            "", str(value),
            prompt=(f"การสอบย่อยของนักเรียนกลุ่มหนึ่ง มีคะแนนเต็ม {top} คะแนน "
                    f"จากผลการสอบย่อยของนักเรียนกลุ่มนี้พบว่า คะแนนสอบของนักเรียน"
                    f"แต่ละคนเป็นจำนวนเต็มที่ไม่เป็นลบ คะแนนสอบของนักเรียนกลุ่มนี้"
                    f"มีค่าเฉลี่ยเลขคณิตเท่ากับ a คะแนน มีฐานนิยมที่แตกต่างกัน"
                    f"สองค่า คือ a คะแนน และ b คะแนน และผลรวมของคะแนนสอบของ"
                    f"นักเรียนกลุ่มนี้เท่ากับ {total} คะแนน  จงหาจำนวนนักเรียน"
                    f"มากที่สุดที่เป็นไปได้ที่ได้คะแนนสอบไม่เท่ากับ {top} คะแนน"),
            hint=r"n \cdot a = \Sigma \text{ and } a \le m "
                 r"\Rightarrow a = 1,\ n = \Sigma",
            distractors=_distinct(str(value), [
                str(total),                 # forgot that c₃ cannot be 0
                str(total - 2), str(value - 1), str(value + 1),
                str(total // 2), str(top * top)]))


@question_type("math.posn2566_q26", display_name={"th": "จำนวนรูปทรงจากลูกบาศก์หน่วยในกล่อง"},
               level=LEVEL, topic="เรขาคณิตสามมิติ")
class GluedCubes(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL26)
        value = SOLVE[26](**p)
        n, a, b, c = p["n"], p["a"], p["b"], p["c"]
        return MathDraw(
            "", str(value),
            prompt=(f"มีลูกบาศก์ขนาดหนึ่งลูกบาศก์หน่วยจำนวน {n} ลูกที่เหมือนกัน"
                    f"ทุกประการ ต้องการนำลูกบาศก์ทั้ง {n} ลูกมาประกอบกัน โดยวาง"
                    f"เรียงในแนวนอนหรือแนวตั้งให้หน้าของลูกบาศก์ประกบกันสนิทพอดี "
                    f"ด้วยการทากาวประกบหน้าทั้งหน้าของลูกบาศก์เข้าด้วยกัน เป็น"
                    f"รูปทรงใหม่ซึ่งสามารถบรรจุลงในกล่องทรงสี่เหลี่ยมมุมฉากที่มี"
                    f"ฝาปิด ขนาด {a} × {b} × {c} ลูกบาศก์หน่วย โดยที่แต่ละหน้าของ"
                    f"รูปทรงใหม่นี้ขนานกับหน้าใดหน้าหนึ่งของกล่อง  จงหาจำนวนวิธี"
                    f"ทั้งหมดในการประกอบลูกบาศก์ทั้ง {n} ลูก โดยกำหนดว่าวิธีประกอบ"
                    f"รูปทรงที่หมุนหรือพลิกให้เหมือนกันได้ ถือว่าเป็นวิธีเดียวกัน"),
            hint=r"\text{orbits of the connected } n\text{-subsets under the "
                 r"48 symmetries}",
            distractors=_distinct(str(value), [
                str(value + 1), str(value + 2), str(value - 1),
                str(2 * value), str(a * b * c - n), str(value + 3)]))


@question_type("math.posn2566_q27", display_name={"th": "ส่วนของเส้นตรงยาวเป็นจำนวนเต็มบนตาข่าย"},
               level=LEVEL, topic="การนับเชิงการจัด")
class IntegerSegments(SheetProblem):
    def expr(self, rng: Random):
        gx = rng.randint(2, 9)
        gy = rng.choice([gx, gx, rng.randint(2, 9)])
        value = SOLVE[27](grid_x=gx, grid_y=gy)
        # the count if only the axis-parallel segments are noticed — the whole
        # item is spotting the (3,4,5) displacements as well.
        axis = (gy + 1) * (gx + 1) * gx // 2 + (gx + 1) * (gy + 1) * gy // 2
        return MathDraw(
            "", str(value),
            prompt=(f"ให้ S แทนเซตของจุดบนระนาบที่มีพิกัดเป็น (x, y) โดยที่ "
                    f"x ∈ {{0, 1, 2, …, {gx}}} และ y ∈ {{0, 1, 2, …, {gy}}}  "
                    f"จงหาจำนวนส่วนของเส้นตรงที่มีจุดปลายเป็นจุดใน S และมีความ"
                    f"ยาวเป็นจำนวนเต็มบวก"),
            hint=r"dx^2 + dy^2 = k^2:\ \text{axis-parallel, plus } (3,4)"
                 r"\text{ and } (4,3)",
            distractors=_distinct(str(value), [
                str(axis),                    # missed the (3,4,5) segments
                str(value - 12), str(value + 12),
                str((gx + 1) * (gy + 1)),     # answered the number of points
                str(value // 2), str(value + 1)]))


@question_type("math.posn2566_q28", display_name={"th": "จำนวนเต็ม a ที่รากเป็นจำนวนเต็มทุกราก"},
               level=LEVEL, topic="สมการกำลังสองและเครื่องหมายราก")
class IntegerRootParameter(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL28)
        values = SOLVE[28](**p)
        k, c = p["k"], p["c"]
        # the sheet prints the constant term factored — 2(a − 2) rather than
        # 2a − 4 — so do the same wherever k divides c.
        tail = (rf"{'' if k == 1 else k}(a - {c // k})" if c % k == 0
                else rf"{'' if k == 1 else k}a - {c}")
        return MathDraw(
            rf"ax^2 - ({k + 1}a - {c})x + {tail} = 0", _set_tex(values),
            prompt=("จงหาจำนวนเต็ม a ทั้งหมดที่ทำให้สมการต่อไปนี้มีคำตอบ"
                    "ทุกคำตอบเป็นจำนวนเต็ม"),
            hint=rf"x = 1 \text{{ is always a root; the other is }} "
                 rf"{k} - \frac{{{c}}}{{a}}",
            distractors=_distinct(_set_tex(values), [
                _set_tex([v for v in values if v]),        # forgot a = 0
                _set_tex([v for v in values if v > 0]),    # positive divisors
                _set_tex([v for v in values if v >= 0]),
                _set_tex(list(values) + [c + 1]),
                _set_tex([v for v in values if abs(v) != c]),
                str(len(values))]))


@question_type("math.posn2566_q29", display_name={"th": "XY² ของบันไดรูปสี่เหลี่ยมจัตุรัส"},
               level=LEVEL, topic="เรขาคณิต: พื้นที่รูปสี่เหลี่ยม")
class HalvedStaircase(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL29)
        value = SOLVE[29](**p)
        k, m = p["scale"], p["min_area"]
        return MathDraw(
            "", str(value),
            prompt=(f"รูปสี่เหลี่ยมจัตุรัสมีด้านยาวด้านละ {2 * k} หน่วย จำนวน "
                    f"2 รูป ด้านยาวด้านละ {3 * k} หน่วย จำนวน 2 รูป ด้านยาว"
                    f"ด้านละ {4 * k} หน่วย จำนวน 1 รูป และรูปสี่เหลี่ยมจัตุรัส"
                    f"ที่มีพื้นที่มากกว่า {m} ตารางหน่วย จำนวน 1 รูป นำรูป"
                    f"สี่เหลี่ยมจัตุรัสทั้ง 6 รูปดังกล่าวมาเรียงต่อกันเป็นบันได "
                    f"โดยรูปที่ไม่ทราบด้านวางชิดขอบล่างเดียวกับรูปที่อยู่ทางซ้าย"
                    f"ของมัน  ถ้าลากส่วนของเส้นตรงจากจุด X (มุมบนซ้ายของบันได) "
                    f"ไปยังจุด Y (มุมล่างขวาของรูปที่ไม่ทราบด้าน) ทำให้แบ่งพื้นที่"
                    f"ออกเป็นสองส่วนเท่า ๆ กัน  จงหาค่าของ XY²"),
            # the sheet's drawing prints every side length, this one included.
            figure=None,
            hint=r"\text{the halving condition has two roots; the printed "
                 r"bound discards the smaller}",
            distractors=_distinct(str(value), [
                str(157 * k * k - 2 * 6 * k),   # dropped a term of the sum
                str((11 * k) ** 2), str((6 * k) ** 2),
                str(11 * k + 6 * k), str(value + 1), str(2 * value)]))


@question_type("math.posn2566_q30", display_name={"th": "ค่าความจริงของ f ที่วนซ้ำหลายชั้น"},
               level=LEVEL, topic="การให้เหตุผลเชิงตรรกะ")
class IteratedTruthTable(SheetProblem):
    def expr(self, rng: Random):
        p = rng.choice(POOL30)
        value = SOLVE[30](**p)
        known, target = p["known_step"], p["target_step"]
        state = p["known_state"]
        letters = "PQR"
        given = "  ".join(
            f"{letters[i]}₁ มีค่าความจริงเป็น{'จริง' if v else 'เท็จ'}"
            for i, v in enumerate(state))
        return MathDraw(
            r"Q \circledast R \equiv (Q \wedge \sim R) \vee (R \wedge \sim Q)"
            r"\qquad f(P, Q, R) = \bigl(P \rightarrow (Q \circledast R),\ "
            r"P \wedge (Q \circledast R),\ P \wedge (Q \vee R)\bigr)",
            _truth_tex(value),
            prompt=(f"สำหรับประพจน์ P, Q และ R ใด ๆ กำหนดรูปแบบของประพจน์ "
                    f"Q ⊛ R และฟังก์ชัน f ตามที่กำหนด และให้ fⁿ(P, Q, R) = "
                    f"f(fⁿ⁻¹(P, Q, R)) สำหรับ n ≥ 2  สมมุติว่า "
                    f"f^{known}(P, Q, R) = (P₁, Q₁, R₁) และ f^{target}(P, Q, R) "
                    f"= (P₂, Q₂, R₂) โดยที่ {given}  จงหาค่าความจริงของประพจน์ "
                    f"P₂, Q₂ และ R₂ ตามลำดับ"),
            hint=rf"f^{{{target}}} = f^{{{target - known}}} \circ f^{{{known}}}",
            # Every orbit of f falls into the same 2-cycle, so the answer is one
            # of two triples and the near-miss distractors collide constantly.
            # The eight triples are offered outright after them: with only eight
            # possible answers, "some other triple" is a fair wrong choice.
            distractors=_distinct(_truth_tex(value), [
                _truth_tex(q30.step(value)),          # one step too many
                _truth_tex(state),                    # answered the given state
                _truth_tex(tuple(not v for v in value)),
                _truth_tex((value[1], value[2], value[0])),
                *(_truth_tex(s) for s in q30.STATES)]))
