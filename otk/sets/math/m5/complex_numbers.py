"""จำนวนเชิงซ้อน

คณิตศาสตร์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 1 ม.5/1

Sets moved here from: math, math_algebra, math_bank_complex, math_chapters, math_m5.
"""

from __future__ import annotations

import math
from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed, redraw_until_full
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, frac_tex, poly_tex
from otk.sets._support.math_algebra import _nonzero
from otk.sets._support.math_bank_complex import C, c
from otk.sets._support.math_bank_trig import pi_tex, simplify_root, surd_tex
from otk.sets._support.math_chapters import _deg, _distinct
from otk.sets._support.math_m4 import maths as _maths_math_m5
from otk.sets._support.math_m4 import maths as _num_maths
from otk.sets._support.math_p2 import _maths


def _complex_tex(re: int, im: int) -> str:
    """a + bi with 1/-1 coefficients folded and a pure real/imaginary collapsed."""
    if im == 0:
        return str(re)
    imag = "i" if abs(im) == 1 else f"{abs(im)}i"
    if re == 0:
        return imag if im > 0 else f"-{imag}"
    return f"{re} + {imag}" if im > 0 else f"{re} - {imag}"


M5 = {"th": "ม.5"}


TOPIC = "จำนวนเชิงซ้อน"


I_POWERS: tuple[C, ...] = ((Fraction(1), Fraction(0)), (Fraction(0), Fraction(1)),
                           (Fraction(-1), Fraction(0)), (Fraction(0), Fraction(-1)))


def _tex_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    """Named mistakes first; duplicates and the answer itself dropped; three kept."""
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right][:3]
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


def _frac_q(stem: list, right: Fraction, named: list, topic: str) -> GeneratedQuestion:
    out: list[str] = []
    for w in [*named, -right, right + 1, right - 1, right + 2, right * 2, right - 2]:
        if w is None:
            continue
        t = frac_tex(Fraction(w))
        if t != frac_tex(right) and t not in out:
            out.append(t)
    return _tex_q(stem, frac_tex(right), out, topic)


def ctex(z) -> str:
    """a + bi with the usual shortcuts: i, -i, 3i, \\frac{7}{2}i, 0."""
    re, im = Fraction(z[0]), Fraction(z[1])
    if im == 0:
        return frac_tex(re)
    mag = abs(im)
    body = "i" if mag == 1 else (f"{mag.numerator}i" if mag.denominator == 1 else rf"{frac_tex(mag)}i")
    if re == 0:
        return ("-" if im < 0 else "") + body
    return f"{frac_tex(re)} {'-' if im < 0 else '+'} {body}"


def i_power(n: int) -> C:
    return I_POWERS[n % 4]


def count_matching(n_max: int, p: int, q: int, r: int, s: int) -> int:
    """#x ∈ {1, …, n_max} with ((1 + i)/(1 − i))^(px + q) = i^(rx + s): i^(px + q) = i^(rx + s)."""
    return sum((p * x + q - (r * x + s)) % 4 == 0 for x in range(1, n_max + 1))


#: TeX of a base and what it equals as a power of i (base = i^e): (1 + i)/(1 − i) = i.
BASES = ((r"\frac{1 + i}{1 - i}", 1), (r"\frac{1 - i}{1 + i}", 3), (r"\left(\frac{1 + i}{\sqrt{2}}\right)^{2}", 1),
         (r"\frac{(1 - i)^{2}}{2}", 3))


def _lin(k: int, cst: int, var: str = "x") -> str:
    head = {1: "", -1: "-"}.get(k, str(k)) + var
    return head if not cst else f"{head} {'+' if cst > 0 else '-'} {abs(cst)}"


def conj_plus_i_modulus(a: int, b: int) -> C:
    """z with z̄ + i|z| = a + bi (b > 0): x = a, √(a² + y²) = b + y ⇒ y = (a² − b²)/(2b)."""
    return Fraction(a), Fraction(a * a - b * b, 2 * b)


def z_plus_modulus_shift(a: int, b: int, s: int) -> C | None:
    """z with z + |z − s| = a + bi (s real): y = b, √((x − s)² + b²) = a − x ⇒ x = (a² − s² − b²)/(2(a − s))."""
    if a == s:
        return None
    x = Fraction(a * a - s * s - b * b, 2 * (a - s))
    return (x, Fraction(b)) if a - x >= 0 else None


def imaginary_axis_roots(m: int, k: int, d: int) -> tuple[list[int], list[int]]:
    """Integer solutions y (z = yi) of |z² − m| = kiz + d with m > 0, k ≠ 0, as (valid, rejected).

    The right side is real only when Re(z) = 0. Then |−y² − m| = y² + m and kiz + d = d − ky,
    so y² + ky + (m − d) = 0, and a root counts only if d − ky ≥ 0.
    """
    disc = k * k - 4 * (m - d)
    if disc < 0:
        return [], []
    root = math.isqrt(disc)
    if root * root != disc or (root - k) % 2:
        return [], []
    ys = sorted({(-k + root) // 2, (-k - root) // 2})
    valid = [y for y in ys if d - k * y >= 0]
    return valid, [y for y in ys if y not in valid]


def square_root_of(x: int, y: int) -> C:
    """(x + yi)², used backwards: the square roots of (x² − y²) + 2xyi are ±(x + yi)."""
    return c(x * x - y * y, 2 * x * y)


def quadratic_from_root(p: int, q: int) -> tuple[int, int]:
    """(a, b) with x² + ax + b having root p + qi: a = −2p, b = p² + q²."""
    return -2 * p, p * p + q * q


def poly_mul(f: list[int], g: list[int]) -> list[int]:
    """Coefficients from the highest power down."""
    out = [0] * (len(f) + len(g) - 1)
    for i, a in enumerate(f):
        for j, b in enumerate(g):
            out[i + j] += a * b
    return out


def poly_eval(f: list[int], x: int) -> int:
    v = 0
    for a in f:
        v = v * x + a
    return v


def quartic_with_rational_root(p: int, q: int) -> list[int]:
    """P = x⁴ + … − (p² + q²), integer, with root p + qi and a rational root: (x² − 2px + p² + q²)(x² − 1).

    The rest is x² + mx + n with n = −1 (the constant term fixes it); a rational root of a monic integer
    quadratic is an integer, so the roots are 1 and −1 and m = 0.
    """
    a, b = quadratic_from_root(p, q)
    return poly_mul([1, a, b], [1, 0, -1])


#: Δ (π units) → cos Δ = coefficient·√m. z₁'s modulus carries the same √m, so the cross term is rational.
COS_DELTA = {Fraction(1, 4): (Fraction(1, 2), 2), Fraction(3, 4): (Fraction(-1, 2), 2),
             Fraction(1, 3): (Fraction(1, 2), 1), Fraction(2, 3): (Fraction(-1, 2), 1),
             Fraction(1, 2): (Fraction(0), 1)}


def polar_distance_sq(r1: int, r2: int, delta: Fraction) -> Fraction:
    """|z₁ − z₂|² for z₁ = r₁√m cis α, z₂ = r₂ cis β, α − β = Δ, cos Δ = c√m: law of cosines.

    |z₁|² = r₁²m and 2|z₁||z₂|cos Δ = 2r₁r₂·c·m.
    """
    cos_c, m = COS_DELTA[delta]
    return Fraction(r1 * r1 * m + r2 * r2) - 2 * r1 * r2 * cos_c * m


#: Statements about arbitrary nonzero complex z, w: (TeX, always true).
COMPLEX_FACTS = (
    (r"z\bar{z} = |z|^{2}", True), (r"|zw| = |z||w|", True), (r"|\bar{z}| = |z|", True),
    (r"\left|\frac{1}{z}\right| = \frac{1}{|z|}", True), (r"z + \bar{z} = 2\operatorname{Re}(z)", True),
    (r"\overline{zw} = \bar{z}\,\bar{w}", True), (r"|z^{3}| = |z|^{3}", True),
    (r"|z + w| = |z| + |w|", False), (r"z^{2} = |z|^{2}", False), (r"|z - w| = |z| - |w|", False),
    (r"\operatorname{Re}(zw) = \operatorname{Re}(z)\operatorname{Re}(w)", False), (r"\frac{\bar{z}}{z} = 1", False),
    (r"|z + \bar{z}| = 2|z|", False),
)


def factor_roots_poly(rats: list[Fraction], b: int, c: int) -> list[int]:
    """Coefficients (highest first) of ∏(den·x − num) over the rational roots, times x² + bx + c."""
    f = [1, b, c]
    for r in rats:
        f = poly_mul(f, [r.denominator, -r.numerator])
    return f


def poly_tex_desc(f: list[int]) -> str:
    deg = len(f) - 1
    terms = [(a, "" if k == 0 else ("x" if k == 1 else f"x^{{{k}}}")) for a, k in zip(f, range(deg, -1, -1))]
    out = ""
    for a, sym in terms:
        if a == 0:
            continue
        mag = "" if abs(a) == 1 and sym else str(abs(a))
        out += (("-" if a < 0 else "") if not out else (" - " if a < 0 else " + ")) + mag + sym
    return out


def complex_pair(b: int, c: int) -> tuple[Fraction, Fraction, int]:
    """Roots of x² + bx + c with b² < 4c: re ± im·√m·i, re = −b/2, im·√m = √(4c − b²)/2."""
    k, m = simplify_root(4 * c - b * b)
    return Fraction(-b, 2), Fraction(k, 2), m


def _pair_tex(re: Fraction, im: Fraction, m: int) -> list[str]:
    body = ("i" if im == 1 else f"{frac_tex(im)}i") if m == 1 else surd_tex(im, m) + "i"
    if re == 0:
        return [body, "-" + body]
    return [f"{frac_tex(re)} + {body}", f"{frac_tex(re)} - {body}"]


def solution_set_tex(rats: list[Fraction], pair: tuple[Fraction, Fraction, int] | None) -> str:
    items = [frac_tex(r) for r in sorted(set(rats))] + (_pair_tex(*pair) if pair else [])
    return r"\left\{" + ", ".join(items) + r"\right\}"


def _cis(m: int, ang: int) -> str:
    body = rf"\cos {_deg(ang)} + i\sin {_deg(ang)}"
    return body if m == 1 else rf"{m}(\cos {_deg(ang)} + i\sin {_deg(ang)})"


# n -> moduli whose nth root is whole
_ROOT_MODULI = {2: (4, 9, 16, 25), 3: (1, 8, 27, 64), 4: (1, 16, 81), 6: (1, 64)}


_AXIS = {0: "{r}", 90: "{r}i", 180: "-{r}", 270: "-{r}i"}


def _complex_tex_math_chapters(r: int, theta: int) -> str:
    if theta in _AXIS:
        return _AXIS[theta].format(r="" if r == 1 and theta in (90, 270) else r)
    return _cis(r, theta)


@question_type("math.complex_add_conjugate",
               display_name={"th": "บวก ลบ และสังยุคของจำนวนเชิงซ้อน"},
               level={"th": "ม.5"}, topic="จำนวนเชิงซ้อน")
class ComplexAddConjugate(MathType):
    def expr(self, rng: Random, part_hi: int = 9):
        a, b = _nonzero(rng, -part_hi, part_hi), _nonzero(rng, -part_hi, part_hi)
        c, d = _nonzero(rng, -part_hi, part_hi), _nonzero(rng, -part_hi, part_hi)
        kind = rng.choice(["sum", "conjugate_product"])
        if kind == "sum":
            re, im = a + c, b + d
            shown = (rf"({poly_tex((a, ''), (b, 'i'))}) + "
                     rf"({poly_tex((c, ''), (d, 'i'))})")
            return MathDraw(
                shown, poly_tex((re, ""), (im, "i")), prompt="จงหาผลลัพธ์",
                distractors=[poly_tex((a - c, ""), (b - d, "i")),
                             poly_tex((re, ""), (-im, "i")),
                             poly_tex((a + d, ""), (b + c, "i"))])
        # z·z̄ = a² + b², always real — the reason conjugates rationalize.
        shown = (rf"({poly_tex((a, ''), (b, 'i'))})"
                 rf"({poly_tex((a, ''), (-b, 'i'))})")
        return MathDraw(
            shown, str(a * a + b * b), prompt="จงหาผลคูณ",
            distractors=[str(a * a - b * b), poly_tex((a * a, ""), (b * b, "i")),
                         str(2 * a * b)])
ComplexAddConjugate.PROVENANCE = Provenance("original")


@question_type("math.complex_power_cycle_m5",
               display_name={"th": "กำลังของ i และวัฏจักรทุก 4"},
               level=M5, topic=TOPIC)
class ComplexPowerCycleM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            a = rng.randint(21, 199)
            f = rng.randint(4, 101)
            b = rng.randint(10, 99)
            sign = rng.choice((1, -1))
            # i^(f!) = 1 since 4 divides f! for f ≥ 4.
            right = tuple(x + sign * y + z for x, y, z in zip(i_power(a), i_power(b), c(1)))
            stem = [text("ให้"), content_math("i^{2} = -1"), text("ค่าของ"),
                    content_math(rf"i^{{{a}}} {'+' if sign > 0 else '-'} i^{{{b}}} + i^{{{f}!}}"),
                    text("เท่ากับเท่าใด")]
            total = lambda pa, pb, pf: tuple(x + sign * y + z for x, y, z in zip(pa, pb, pf))
            # i^(f!) read as i^f; the middle sign lost; every residue off by one; the conjugate.
            w1 = total(i_power(a), i_power(b), i_power(f))
            w2 = tuple(x - sign * y + z for x, y, z in zip(i_power(a), i_power(b), c(1)))
            w3 = total(i_power(a + 1), i_power(b + 1), c(1))
            near = [(right[0] + 1, right[1]), (right[0], right[1] + 1), (right[0] - 1, right[1])]
            wrongs = [ctex(w) for w in (w1, w2, w3)] + [ctex((right[0], -right[1])), ctex((-right[0], -right[1]))] \
                + [ctex(w) for w in near]
            return _tex_q(stem, ctex(right), wrongs, self.topic)
        if kind == 1:
            tex, e = rng.choice(BASES)
            n = rng.randint(5, 60)
            right = i_power(e * n)
            stem = [text("ให้"), content_math("i^{2} = -1"), text("ค่าของ"),
                    content_math(rf"\left({tex}\right)^{{{n}}}"), text("เท่ากับเท่าใด")]
            # Taking the base as i when it is −i (or the reverse); n mod 4 misread by one; 1.
            others = [ctex(i_power(k)) for k in (e * n + 2, (4 - e) * n, e * n + 1, e * n + 3)]
            return _tex_q(stem, ctex(right), others, self.topic)
        while True:
            p, r = rng.sample(range(1, 5), 2)
            if (p - r) % 2:
                break
        q, s = rng.randint(-6, 6), rng.randint(-6, 6)
        n_max = rng.choice((50, 60, 99, 100, 120, 155, 200))
        right = count_matching(n_max, p, q, r, s)
        stem = [text(f"กำหนดให้ A = {{1, 2, 3, …, {n_max}}} และ"), content_math("i^{2} = -1"), text("ถ้า"),
                content_math(rf"B = \left\{{x \in A \;\middle|\; \left(\frac{{1 + i}}{{1 - i}}\right)^{{{_lin(p, q)}}}"
                             rf" = i^{{{_lin(r, s)}}}\right\}}"),
                text("แล้วจำนวนสมาชิกของ B เท่ากับเท่าใด")]
        # The residue off by two (−i taken for i); the other residues; a quarter of A.
        named = [count_matching(n_max, p, q + 2, r, s), count_matching(n_max, p, q + 1, r, s),
                 count_matching(n_max, p, q + 3, r, s), n_max // 4]
        out = [str(v) for v in [*named, right + 1, right - 1, right + 2] if v != right and v >= 0]
        return _tex_q(stem, str(right), out, self.topic)
ComplexPowerCycleM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/11 จำนวนเชิงซ้อน',))


@question_type("math.complex_multiply",
               display_name={"th": "การคูณจำนวนเชิงซ้อน"}, level={"th": "ม.5"},
               topic="จำนวนเชิงซ้อน")
class ComplexMultiply(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        a, c = rng.randint(-5, 5), rng.randint(-5, 5)
        b = rng.choice([n for n in range(-5, 6) if n])
        d = rng.choice([n for n in range(-5, 6) if n])
        return MathDraw(
            rf"({_complex_tex(a, b)})({_complex_tex(c, d)})",
            _complex_tex(a * c - b * d, a * d + b * c),
            hint=r"i^2 = -1",
            distractors=[_complex_tex(a * c + b * d, a * d + b * c),   # forgot i²
                         _complex_tex(a * c, b * d),
                         _complex_tex(a * c - b * d, a * d - b * c)])
ComplexMultiply.PROVENANCE = Provenance("original")


@question_type("math.complex_modulus", display_name={"th": "ค่าสัมบูรณ์ของจำนวนเชิงซ้อน"},
               level={"th": "ม.5"}, topic="จำนวนเชิงซ้อน")
class ComplexModulus(MathType):
    def expr(self, rng: Random, k_lo: int = 1, k_hi: int = 4):
        a, b, c = rng.choice([(3, 4, 5), (5, 12, 13), (8, 15, 17), (7, 24, 25),
                              (6, 8, 10), (9, 12, 15)])
        k = rng.randint(k_lo, k_hi)
        re, im = a * k, b * k
        if rng.random() < 0.5:
            re = -re
        if rng.random() < 0.5:
            im = -im
        return MathDraw(
            poly_tex((re, ""), (im, "i")), str(c * k),
            prompt="จงหาค่าสัมบูรณ์ของจำนวนเชิงซ้อนนี้",
            distractors=[str(abs(re) + abs(im)), str((c * k) ** 2),
                         str(abs(abs(re) - abs(im)))])
ComplexModulus.PROVENANCE = Provenance("original")


@question_type("math.complex_equation_parts_m5",
               display_name={"th": "สมการจำนวนเชิงซ้อนที่มีสังยุคและค่าสัมบูรณ์"},
               level=M5, topic=TOPIC)
class ComplexEquationPartsM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        if kind == 0:
            a, b = rng.randint(-12, 12), rng.randint(1, 12)
            x, y = conj_plus_i_modulus(a, b)
            stem = [text("ให้ z เป็นจำนวนเชิงซ้อนที่สอดคล้องกับสมการ"),
                    content_math(rf"\bar{{z}} + i|z| = {ctex(c(a, b))}"), text("เมื่อ"), content_math("i^{2} = -1")]
            if rng.random() < 0.5:
                stem.append(text("ส่วนจินตภาพของ z เท่ากับเท่าใด"))
                # z̄'s sign forgotten (y → −y); a² + b² over 2b; b itself.
                return _frac_q(stem, y, [-y, Fraction(a * a + b * b, 2 * b), Fraction(b), Fraction(a * a - b * b, b)],
                               self.topic)
            stem += [content_math("|z|"), text("เท่ากับเท่าใด")]
            right = b + y
            return _frac_q(stem, right, [b - y, Fraction(abs(a)), right * 2, Fraction(a * a + b * b, b)], self.topic)
        if kind == 1:
            while True:
                a, b, s = rng.randint(-8, 8), rng.randint(-6, 6), rng.randint(-4, 4)
                z = z_plus_modulus_shift(a, b, s)
                if z is not None and b:
                    break
            stem = [text("ถ้า z เป็นจำนวนเชิงซ้อนซึ่งสอดคล้องกับสมการ"),
                    content_math(rf"z + |z {'-' if s > 0 else '+'} {abs(s)}| = {ctex(c(a, b))}" if s
                                 else rf"z + |z| = {ctex(c(a, b))}"),
                    text("แล้วส่วนจริงของ z เท่ากับเท่าใด")]
            # Forgetting b² under the root; (x + s) instead of (x − s); the plain a.
            named = [Fraction(a * a - s * s, 2 * (a - s)), Fraction(a * a - s * s - b * b, 2 * (a + s)) if a + s else None,
                     Fraction(a)]
            return _frac_q(stem, z[0], named, self.topic)
        if kind == 2:
            while True:
                x, y = rng.randint(-5, 5), rng.randint(1, 5)
                if x and abs(x) != y:           # x = ±y would make y + xi a square root too
                    break
            w = square_root_of(x, y)
            stem = [text("ข้อใดเป็นรากที่สองของ"), content_math(ctex(w))]
            # The conjugate; real and imaginary parts swapped; the sign of one part flipped.
            wrongs = [ctex(c(x, -y)), ctex(c(y, x)), ctex(c(-x, y)), ctex(c(y, -x))]
            right = ctex(c(x, y) if rng.random() < 0.5 else c(-x, -y))
            return _tex_q(stem, right, wrongs, self.topic)
        while True:
            y1, y2 = rng.sample(range(-4, 5), 2)
            k = -(y1 + y2)
            m = rng.randint(1, 5)
            d = m - y1 * y2
            valid, rejected = imaginary_axis_roots(m, k, d)
            if valid and sorted(valid + rejected) == sorted((y1, y2)) and k:
                break
        right = c(0, sum(valid))
        rhs = f"{'' if k == 1 else '-' if k == -1 else k}iz" + (f" {'+' if d >= 0 else '-'} {abs(d)}" if d else "")
        stem = [text("ผลบวกของจำนวนเชิงซ้อน z ทั้งหมดที่สอดคล้องกับสมการ"),
                content_math(rf"|z^{{2}} - {m}| = {rhs}"), text("เท่ากับเท่าใด")]
        # Keeping the rejected root; the opposite sign; the product of the roots.
        wrongs = [ctex(c(0, y1 + y2)), ctex(c(0, -sum(valid))), ctex(c(0, y1 * y2)), ctex(c(sum(valid)))]
        return _tex_q(stem, ctex(right), wrongs, self.topic)
ComplexEquationPartsM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/11 จำนวนเชิงซ้อน',))


@question_type("math.complex_modulus_rules_m5",
               display_name={"th": "สมบัติของค่าสัมบูรณ์และสังยุคของจำนวนเชิงซ้อน"},
               level=M5, topic=TOPIC)
class ComplexModulusRulesM5(QuestionType):
    @redraw_until_full()
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            r1, r2, r3 = rng.sample((1, 2, 3, 4, 5), 3)
            e1, e3 = rng.randint(1, 3), rng.randint(1, 2)
            right = Fraction(r1 ** e1 * r2, r3 ** e3)
            power = lambda j, e: f"z_{{{j}}}" + ("" if e == 1 else f"^{{{e}}}")
            stem = [text("ให้"), content_math(r"z_{1}, z_{2}, z_{3}"),
                    text("เป็นจำนวนเชิงซ้อน โดยที่"),
                    content_math(rf"|z_{{1}}| = {r1},\ |z_{{2}}| = {r2},\ |z_{{3}}| = {r3}"), text("แล้ว"),
                    content_math(rf"\left|\frac{{{power(1, e1)}\,\overline{{z_{{2}}}}}}{{{power(3, e3)}}}\right|"),
                    text("เท่ากับเท่าใด")]
            # Powers ignored; the conjugate read as a reciprocal; multiplying by |z₃|.
            named = [Fraction(r1 * r2, r3), Fraction(r1 ** e1, r2 * r3 ** e3), Fraction(r1 ** e1 * r2 * r3 ** e3)]
            return _frac_q(stem, right, named, self.topic)
        if kind == 1:
            delta = rng.choice(list(COS_DELTA))
            m = COS_DELTA[delta][1]
            r1, r2 = rng.randint(1, 3), rng.randint(1, 4)
            beta = rng.choice((Fraction(1, 8), Fraction(1, 6), Fraction(1, 12), Fraction(1, 4)))
            alpha = beta + delta
            d2 = polar_distance_sq(r1, r2, delta)
            root = lambda n: surd_tex(Fraction(simplify_root(n)[0]), simplify_root(n)[1])
            mod1 = surd_tex(Fraction(r1), m)
            cis = lambda t: rf"\left(\cos {pi_tex(t)} + i\sin {pi_tex(t)}\right)"
            stem = [text("ถ้า"), content_math(rf"z_{{1}} = {'' if mod1 == '1' else mod1}{cis(alpha)}"), text("และ"),
                    content_math(rf"z_{{2}} = {'' if r2 == 1 else r2}{cis(beta)}"), text("แล้ว"),
                    content_math(r"|z_{1} - z_{2}|"), text("เท่ากับเท่าใด")]
            # The cross term's sign flipped; the squared distance; the cross term dropped; |z₁ + z₂|² − 1.
            squares = r1 * r1 * m + r2 * r2
            wrongs = [root(int(2 * squares - d2)), frac_tex(d2), root(squares), str(r1 + r2), root(int(d2) + 1),
                      root(int(d2) + 2)]
            return _tex_q(stem, root(int(d2)), wrongs, self.topic)
        picks = rng.sample(COMPLEX_FACTS, 4)
        right = sum(t for _, t in picks)
        stem = [text("ให้ z และ w เป็นจำนวนเชิงซ้อนใด ๆ ที่ไม่เป็นศูนย์ พิจารณาข้อความต่อไปนี้")]
        for lab, (tex, _) in zip(("ก.", "ข.", "ค.", "ง."), picks):
            stem += [text(lab), content_math(tex)]
        stem.append(text("จำนวนข้อความที่ถูกต้องเท่ากับเท่าใด"))
        wrongs = [str(v) for v in sorted(range(5), key=lambda v: abs(v - right)) if v != right]
        return _tex_q(stem, str(right), wrongs, self.topic)
ComplexModulusRulesM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/11 จำนวนเชิงซ้อน',))


@question_type("math.complex_conjugate_root_m5",
               display_name={"th": "รากสังยุคของพหุนามสัมประสิทธิ์จริง"},
               level=M5, topic=TOPIC)
class ComplexConjugateRootM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        p, q = rng.choice([v for v in range(-5, 6) if v]), rng.randint(1, 4)
        root = ctex(c(p, -q if rng.random() < 0.5 else q))
        a, b = quadratic_from_root(p, q)
        if kind == 0:
            ask = rng.choice(("a + b", "ab", "b - a"))
            right = {"a + b": a + b, "ab": a * b, "b - a": b - a}[ask]
            stem = [text("ถ้าจำนวนเชิงซ้อน"), content_math(root), text("เป็นคำตอบหนึ่งของสมการ"),
                    content_math("x^{2} + ax + b = 0"), text("โดยที่ a และ b เป็นจำนวนจริง แล้ว"),
                    content_math(ask), text("เท่ากับเท่าใด")]
            # a's sign lost (a = 2p); b = p² − q²; both.
            alt = lambda a_, b_: {"a + b": a_ + b_, "ab": a_ * b_, "b - a": b_ - a_}[ask]
            named = [alt(-a, b), alt(a, p * p - q * q), alt(-a, p * p - q * q)]
            return _frac_q(stem, Fraction(right), named, self.topic)
        if kind == 1:
            f = quartic_with_rational_root(p, q)
            x0 = rng.choice((2, 3, -2, 0))
            right = poly_eval(f, x0)
            stem = [text("กำหนดให้"), content_math(rf"P(x) = x^{{4}} + ax^{{3}} + bx^{{2}} + cx - {p * p + q * q}"),
                    text("เมื่อ a, b และ c เป็นจำนวนเต็ม ถ้าสมการ"), content_math("P(x) = 0"),
                    text("มีคำตอบเป็นจำนวนตรรกยะอย่างน้อยหนึ่งตัว และมี"), content_math(root),
                    text("เป็นคำตอบ แล้ว"), content_math(f"P({x0})"), text("มีค่าเท่ากับเท่าใด")]
            # The factor's middle sign lost; x² + 1 as the other factor; the conjugate forgotten (only (x − root)).
            w1 = poly_eval(poly_mul([1, -a, b], [1, 0, -1]), x0)
            w2 = poly_eval(poly_mul([1, a, b], [1, 0, 1]), x0)
            w3 = -right
            return _frac_q(stem, Fraction(right), [w1, w2, w3], self.topic)
        r = rng.choice([v for v in range(-4, 5) if v])
        f = poly_mul([1, a, b], [1, -r])
        stem = [text("ถ้า"), content_math(root), text("และ"), content_math(str(r)),
                text("เป็นคำตอบของสมการ"), content_math("x^{3} + ax^{2} + bx + c = 0"),
                text("โดยที่ a, b และ c เป็นจำนวนจริง แล้ว"), content_math("a + b + c"), text("เท่ากับเท่าใด")]
        right = sum(f[1:])
        # The factor's middle sign lost; (x + r) instead of (x − r); P(1) itself.
        w1 = sum(poly_mul([1, -a, b], [1, -r])[1:])
        w2 = sum(poly_mul([1, a, b], [1, r])[1:])
        return _frac_q(stem, Fraction(right), [w1, w2, right + 1], self.topic)
ComplexConjugateRootM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/11 จำนวนเชิงซ้อน',))


@question_type("math.complex_polynomial_solve_m5",
               display_name={"th": "เซตคำตอบของสมการพหุนามในระบบจำนวนเชิงซ้อน"},
               level=M5, topic=TOPIC)
class ComplexPolynomialSolveM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        ints = [v for v in range(-3, 4) if v]
        rats = [Fraction(v) for v in rng.sample(ints, rng.choice((1, 2)))]
        if len(rats) == 1 and rng.random() < 0.3:
            rats.append(rats[0])                                   # a double root, listed once in the set
        elif rng.random() < 0.3:
            rats[0] = Fraction(rng.choice((-3, -1, 1, 3)), 2)      # a root of 2x − u
        b = rng.choice([v for v in range(-4, 5) if v])
        c = rng.randint(b * b // 4 + 1, b * b // 4 + 6)
        f = factor_roots_poly(rats, b, c)
        pair = complex_pair(b, c)
        right = solution_set_tex(rats, pair)
        re, im, m = pair
        k = int(im * 2)
        # −b/2's sign lost; x − r read as a root −r; √(4c − b²) not halved; the complex pair dropped.
        wrongs = [solution_set_tex(rats, (-re, im, m)), solution_set_tex([-r for r in rats], pair),
                  solution_set_tex(rats, (re, Fraction(k), m)), solution_set_tex(rats, None)]
        stem = [text("เซตคำตอบของสมการ"), content_math(f"{poly_tex_desc(f)} = 0"),
                text("ในระบบจำนวนเชิงซ้อน คือข้อใด")]
        return _tex_q(stem, right, wrongs, self.topic)
ComplexPolynomialSolveM5.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/11 จำนวนเชิงซ้อน',))


@question_type("math.complex_nth_roots_m5", display_name={"th": "รากที่ n ของจำนวนเชิงซ้อน"},
               level=M5, topic="จำนวนเชิงซ้อน")
class ComplexNthRootsM5(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random) -> GeneratedQuestion:
        n = rng.choice(sorted(_ROOT_MODULI))
        r = rng.choice(_ROOT_MODULI[n])
        theta = rng.choice([t for t in range(0, 360, 30) if t % n == 0])
        m = round(r ** (1 / n))
        w = _complex_tex_math_chapters(r, theta)
        roots = {(theta + 360 * j) // n % 360 for j in range(n)}
        kind = rng.randrange(3)
        if kind == 0 and r > 1:
            return _num_maths([text(f"รากที่ {n} ทุกตัวของ"), content_math(w), text("มีค่าสัมบูรณ์เท่าใด")],
                              str(m), [str(r), frac_tex(Fraction(r, n)), str(m * m) if m * m != r else str(m + 2)],
                              self.topic)
        if kind == 1:
            gap = 360 // n
            wrongs = _distinct(_deg(gap), *[_deg(v) for v in (180 // n, 360 // (n + 1), gap * 2, theta // n or 45)])
            return _maths([text(f"รากที่ {n} ทั้งหมดของ"), content_math(w),
                           text("อยู่บนวงกลมวงเดียวกัน รากที่อยู่ติดกันทำมุมที่จุดกำเนิดกี่องศา")],
                          _deg(gap), wrongs[:3], self.topic)
        ang = rng.choice(sorted(roots))
        right = _cis(m, ang)
        # The modulus left unrooted, the argument left undivided, and
        # arguments that are not roots at all.
        cands = ([_cis(r, ang)] if r != m else []) + [
            _cis(m, a % 360) for a in (theta, (theta + 180) // n, ang + 90, ang + 45, ang + 15, ang + 30,
                                       ang + 60)
            if a % 360 not in roots]
        return _maths([text(f"ข้อใดเป็นรากที่ {n} ของ"), content_math(w)], right,
                      _distinct(right, *cands)[:3], self.topic)
ComplexNthRootsM5.PROVENANCE = Provenance("original")


@question_type("math.complex_polar_m5", display_name={"th": "จำนวนเชิงซ้อนในรูปเชิงขั้วและทฤษฎีบทเดอมัวร์"},
               level=M5, topic="จำนวนเชิงซ้อน")
class ComplexPolarM5(QuestionType):
    # (z, modulus, argument in degrees)
    _Z = ((r"1 + i", r"\sqrt{2}", 45), (r"1 - i", r"\sqrt{2}", 315), (r"\sqrt{3} + i", "2", 30),
          (r"-1 + i", r"\sqrt{2}", 135), (r"1 + \sqrt{3}i", "2", 60), (r"-\sqrt{3} + i", "2", 150),
          (r"-1 - i", r"\sqrt{2}", 225), (r"2i", "2", 90), (r"-3", "3", 180))

    def build(self, rng: Random) -> GeneratedQuestion:
        z, r, deg = rng.choice(self._Z)
        if rng.random() < 0.6:
            right = rf"{r}(\cos {deg}^{{\circ}} + i\sin {deg}^{{\circ}})"
            wrong_deg = [(deg + 180) % 360, (90 - deg) % 360 or 270, (360 - deg) % 360 or 180,
                         (deg + 90) % 360, (deg + 45) % 360]
            wrong_deg = [d for d in dict.fromkeys(wrong_deg) if d != deg]
            wrongs = [rf"{r}(\cos {d}^{{\circ}} + i\sin {d}^{{\circ}})" for d in wrong_deg]
            other_r = "2" if r != "2" else r"\sqrt{2}"
            wrongs.append(rf"{other_r}(\cos {deg}^{{\circ}} + i\sin {deg}^{{\circ}})")
            return _maths_math_m5([text("จงเขียนจำนวนเชิงซ้อนนี้ในรูปเชิงขั้ว"), content_math(rf"z = {z}")], right,
                          wrongs, self.topic)
        # (1 + i)^n with n even: 2^{n/2} at argument 45n°.
        n = rng.choice((2, 4, 6, 8))
        mod = 2 ** (n // 2)
        ang = (45 * n) % 360
        val = {0: f"{mod}", 90: f"{mod}i", 180: f"-{mod}", 270: f"-{mod}i"}[ang]
        wrongs = {f"{mod}", f"{mod}i", f"-{mod}", f"-{mod}i", f"{2 ** n}", f"{2 * n}i"} - {val}
        return _maths_math_m5([text("จงหาค่า (ใช้ทฤษฎีบทเดอมัวร์)"), content_math(rf"(1 + i)^{{{n}}}")], val,
                      sorted(wrongs)[:4], self.topic)
ComplexPolarM5.PROVENANCE = Provenance("original")
