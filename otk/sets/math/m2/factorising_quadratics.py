"""การแยกตัวประกอบของพหุนามดีกรีสอง

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: ค 1.2 ม.2/2

Sets moved here from: math_gaps_secondary.
"""

from __future__ import annotations

import math
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem, binomial_tex, poly_tex
from otk.sets._support.math_gaps_secondary import _distinct, _lin, _num, _nz, _quad

PROVENANCE = Provenance("original")


def _plain(tex: str) -> str:
    """A small polynomial as sentence text: x^{2} + 5x + 6 → x² + 5x + 6."""
    return tex.replace("^{2}", "²").replace("^{3}", "³").replace("-", "−")


_M2_TOPIC = "การแยกตัวประกอบของพหุนามดีกรีสอง"


@question_type("math.factor_common_m2", display_name={"th": "แยกตัวประกอบโดยดึงตัวประกอบร่วม"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorCommonM2(WordProblem):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        while True:
            k, a, b = rng.randint(2, 9), rng.randint(1, 6), _nz(rng, -9, 9)
            if math.gcd(a, abs(b)) == 1 and a != abs(b):
                break
        expanded = _quad(k * a, k * b, 0)
        right = f"{k}x({_lin(a, b)})"
        # Stopping after the number or after the x, and a sign slip.
        return MathDraw(expanded, right, prompt="จงแยกตัวประกอบให้สมบูรณ์",
                        distractors=_distinct(right, f"{k}({_quad(a, b, 0)})", f"x({_lin(k * a, k * b)})",
                                              f"{k}x({_lin(a, -b)})", f"{k}({_lin(a, b)})"))


@question_type("math.factor_trinomial_m2", display_name={"th": "แยกตัวประกอบพหุนามดีกรีสอง x² + bx + c"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorTrinomialM2(WordProblem):
    def expr(self, rng: Random):
        while True:
            p, q = _nz(rng, -9, 9), _nz(rng, -9, 9)
            if p != q and p + q:
                break
        expanded = _quad(1, p + q, p * q)
        right = f"{binomial_tex(p)}{binomial_tex(q)}"
        # Both signs flipped, one sign flipped (the product's sign right,
        # the sum's wrong), and a pair that multiplies to c but misses b.
        pair = next(((m, p * q // m) for m in range(1, 10)
                     if p * q % m == 0 and m + p * q // m != p + q and m != p * q // m), None)
        wrongs = [f"{binomial_tex(-p)}{binomial_tex(-q)}", f"{binomial_tex(p)}{binomial_tex(-q)}",
                  f"{binomial_tex(-p)}{binomial_tex(q)}"]
        if pair:
            wrongs.insert(1, f"{binomial_tex(pair[0])}{binomial_tex(pair[1])}")
        return MathDraw(expanded, right, prompt="จงแยกตัวประกอบ",
                        distractors=[w for w in dict.fromkeys(wrongs) if w != right])


@question_type("math.factor_apply_m2", display_name={"th": "นำการแยกตัวประกอบไปใช้แก้ปัญหา"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorApplyM2(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            p, q = rng.sample(range(2, 10), 2)
            area = _plain(_quad(1, p + q, p * q))
            right = _lin(1, q)
            return MathDraw("", right, prompt=(
                f"รูปสี่เหลี่ยมผืนผ้ารูปหนึ่งมีพื้นที่ {area} ตารางหน่วย ถ้าด้านหนึ่งยาว x + {p} หน่วย "
                f"อีกด้านหนึ่งยาวกี่หน่วย"),
                distractors=_distinct(right, _lin(1, p * q), _lin(1, p + q), _lin(1, q - p)))
        if kind == 1:
            k = rng.randint(3, 9)
            area = _plain(_quad(1, 2 * k, k * k))
            right = _lin(1, k)
            return MathDraw("", right, prompt=(
                f"รูปสี่เหลี่ยมจัตุรัสรูปหนึ่งมีพื้นที่ {area} ตารางหน่วย ด้านยาวด้านละกี่หน่วย"),
                distractors=_distinct(right, _lin(1, 2 * k), _lin(1, k * k), _lin(2, k)))
        # a² − b² = (a − b)(a + b) makes a hard product easy.
        n, d = rng.choice((20, 30, 40, 50, 60, 70, 80, 90, 100)), rng.randint(1, 3)
        value = (n - d) * (n + d)
        return MathDraw(rf"{n - d} \times {n + d}", _num(value),
                        prompt="ใช้ผลต่างกำลังสองหาค่า",
                        distractors=[_num(int(v)) for v in
                                     _story.keep(n * n + d * d, n * n - d, (n - d) * n, answer=value)])


# ── More factorising (สสวท. ม.2 เล่ม 2 บทที่ 2): the two special products both ways, a leading
# coefficient other than 1, reading a product back as a sum, a missing term, a quick product of
# numbers, and grouping ──

def _prod(*factors: str) -> str:
    return "".join(f"({f})" for f in factors)


def _expand(p: int, q: int, r: int, s: int) -> tuple[int, int, int]:
    """(px + q)(rx + s) = pr x² + (ps + qr) x + qs."""
    return p * r, p * s + q * r, q * s


@question_type("math.factor_difference_squares_m2", display_name={"th": "แยกตัวประกอบผลต่างของกำลังสอง"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorDifferenceSquaresM2(WordProblem):
    """a² − b² = (a − b)(a + b), once with a coefficient on x and once after a common factor."""

    def expr(self, rng: Random):
        kind = rng.randrange(3)
        a = rng.randint(2, 12)
        if kind == 0:
            expanded, right = _quad(1, 0, -a * a), _prod(_lin(1, -a), _lin(1, a))
            # Read as a perfect square either way; the square root of the constant forgotten.
            wrongs = [f"({_lin(1, -a)})^{{2}}", f"({_lin(1, a)})^{{2}}", _prod(_lin(1, -a * a), _lin(1, 1))]
        elif kind == 1:
            while True:
                k, a = rng.randint(2, 5), rng.randint(1, 9)
                if math.gcd(k, a) == 1:
                    break
            expanded, right = _quad(k * k, 0, -a * a), _prod(_lin(k, -a), _lin(k, a))
            # The coefficient's square root not taken; read as a square; the signs alike.
            wrongs = [_prod(_lin(k * k, -a), _lin(k * k, a)), f"({_lin(k, -a)})^{{2}}", _prod(_lin(k, a), _lin(k, a))]
        else:
            m, a = rng.randint(2, 5), rng.randint(2, 9)
            expanded, right = _quad(m, 0, -m * a * a), f"{m}" + _prod(_lin(1, -a), _lin(1, a))
            # The common factor left out; left inside one bracket; read as a square.
            wrongs = [_prod(_lin(1, -a), _lin(1, a)), _prod(_lin(m, -a), _lin(1, a)), f"{m}({_lin(1, -a)})^{{2}}"]
        return MathDraw(expanded, right, prompt="จงแยกตัวประกอบให้สมบูรณ์", distractors=_distinct(right, *wrongs))


@question_type("math.factor_perfect_square_m2", display_name={"th": "แยกตัวประกอบกำลังสองสมบูรณ์"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorPerfectSquareM2(WordProblem):
    """A² ± 2AB + B² = (A ± B)², with A = kx."""

    def expr(self, rng: Random):
        while True:
            k, a = rng.choice((1, 1, 2, 3)), rng.randint(1, 9)
            if math.gcd(k, a) == 1:
                break
        sign = rng.choice((1, -1))
        expanded = _quad(k * k, sign * 2 * k * a, a * a)
        right = f"({_lin(k, sign * a)})^{{2}}"
        # The other sign; the difference of squares; the middle coefficient halved wrongly (kx ± 2a).
        wrongs = [f"({_lin(k, -sign * a)})^{{2}}", _prod(_lin(k, -a), _lin(k, a)), f"({_lin(k, sign * 2 * a)})^{{2}}",
                  f"({_lin(k, sign * a * a)})^{{2}}"]
        return MathDraw(expanded, right, prompt="จงแยกตัวประกอบ", distractors=_distinct(right, *wrongs))


@question_type("math.factor_leading_coeff_m2", display_name={"th": "แยกตัวประกอบ ax² + bx + c เมื่อ a ไม่เท่ากับ 1"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorLeadingCoeffM2(WordProblem):
    """(px + q)(rx + s) with p or r above 1: the constants must pair with the right coefficients."""

    def expr(self, rng: Random):
        while True:
            p, r = rng.choice((1, 2, 3)), rng.choice((2, 3, 5))
            q, s = _nz(rng, -7, 7), _nz(rng, -7, 7)
            a, b, c = _expand(p, q, r, s)
            if math.gcd(p, abs(q)) == 1 and math.gcd(r, abs(s)) == 1 and b and (p, q) != (r, s):
                break
        right = _prod(_lin(p, q), _lin(r, s))
        # The constants swapped between brackets; both signs flipped; one sign flipped. Only forms that
        # really expand to something else are offered.
        candidates = [(p, s, r, q), (p, -q, r, -s), (p, q, r, -s), (p, -q, r, s)]
        wrongs = [_prod(_lin(w, x), _lin(y, z)) for w, x, y, z in candidates if _expand(w, x, y, z) != (a, b, c)]
        return MathDraw(_quad(a, b, c), right, prompt="จงแยกตัวประกอบ", distractors=_distinct(right, *wrongs))


@question_type("math.factor_identify_m2", display_name={"th": "ผลคูณของพหุนามดีกรีหนึ่งสองพหุนาม"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorIdentifyM2(WordProblem):
    """The reverse direction: which trinomial does (x + p)(x + q) factorise?"""

    def expr(self, rng: Random):
        while True:
            p, q = _nz(rng, -9, 9), _nz(rng, -9, 9)
            if p != q and p + q and p * q != p + q:
                break
        right = _quad(1, p + q, p * q)
        # The sum and the product swapped; the middle sign flipped; the constant added, not multiplied.
        wrongs = [_quad(1, p * q, p + q), _quad(1, -(p + q), p * q), _quad(1, p + q, p + q), _quad(1, p * q, p * q)]
        return MathDraw(_prod(_lin(1, p), _lin(1, q)), right, prompt="พหุนามในข้อใดเท่ากับผลคูณนี้",
                        distractors=_distinct(right, *wrongs))


@question_type("math.factor_missing_term_m2", display_name={"th": "หาพจน์ที่หายไปจากการแยกตัวประกอบ"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorMissingTermM2(WordProblem):
    """x² + bx + c = (x + p)(x + q): the middle coefficient is p + q and the constant pq."""

    def expr(self, rng: Random):
        while True:
            p, q = _nz(rng, -9, 9), _nz(rng, -9, 9)
            if p != q and p + q:
                break
        b, c = p + q, p * q
        if rng.random() < 0.5:
            # Given the constant and one factor, find the middle coefficient.
            prompt = (f"ถ้า x² + kx {'+' if c > 0 else '−'} {abs(c)} แยกตัวประกอบได้เป็น "
                      f"({_plain(_lin(1, p))})(x + ?) แล้ว k มีค่าเท่าใด")
            # The constant itself; the other factor's number; p − q.
            return MathDraw("", str(b), prompt=prompt, distractors=[str(w) for w in dict.fromkeys((c, q, p - q)) if w != b])
        prompt = (f"ถ้า x² {'+' if b > 0 else '−'} {abs(b)}x + k แยกตัวประกอบได้เป็น "
                  f"({_plain(_lin(1, p))})(x + ?) แล้ว k มีค่าเท่าใด")
        # The middle coefficient itself; p times b; the other factor's number.
        return MathDraw("", str(c), prompt=prompt, distractors=[str(w) for w in dict.fromkeys((b, p * b, q)) if w != c])


@question_type("math.factor_number_trick_m2", display_name={"th": "ใช้ผลต่างของกำลังสองคำนวณ"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorNumberTrickM2(WordProblem):
    """a² − b² = (a − b)(a + b) turns two squares into one easy product."""

    def expr(self, rng: Random):
        total = rng.choice((100, 100, 200, 60, 80))
        b = rng.randint(total // 2 - 19, total // 2 - 2)
        a = total - b
        value = a * a - b * b
        # (a − b)² for a² − b²; b not squared; (a − b) times 10.
        wrongs = [(a - b) ** 2, a * a - b, (a - b) * total + (a - b)]
        return MathDraw(rf"{a}^{{2}} - {b}^{{2}}", _num(value), prompt="จงหาค่าโดยใช้การแยกตัวประกอบผลต่างของกำลังสอง",
                        distractors=[_num(int(w)) for w in _story.keep(*wrongs, answer=value, lo=1)])


@question_type("math.factor_grouping_m2", display_name={"th": "แยกตัวประกอบโดยดึงพหุนามร่วม"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorGroupingM2(WordProblem):
    """x(y + p) + q(y + p) = (x + q)(y + p): the common factor is a whole bracket."""

    def expr(self, rng: Random):
        p, q = _nz(rng, -9, 9), _nz(rng, -9, 9)
        bracket = poly_tex((1, "y"), (p, ""))
        expanded = f"x({bracket}) {'+' if q > 0 else '-'} {abs(q)}({bracket})"
        right = f"({_lin(1, q)})({bracket})"
        # Multiplying the outside terms; the brackets added; the sign of q lost.
        wrongs = [f"{abs(q)}x({bracket})" if q > 0 else f"-{abs(q)}x({bracket})",
                  f"({_lin(1, q)}) + ({bracket})", f"({_lin(1, -q)})({bracket})"]
        return MathDraw(expanded, right, prompt="จงแยกตัวประกอบ", distractors=_distinct(right, *wrongs))


# ── Factorising to fifteen (2026-11): four terms in pairs, a square less a square of a binomial, spotting a
# perfect square, completing one, and a common factor in two letters ──


@question_type("math.factor_four_terms_m2", display_name={"th": "แยกตัวประกอบพหุนามสี่พจน์โดยจัดกลุ่ม"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorFourTermsM2(WordProblem):
    """xy + qx + py + pq = x(y + q) + p(y + q) = (x + p)(y + q)."""

    def expr(self, rng: Random):
        while True:
            p, q = _nz(rng, -9, 9), _nz(rng, -9, 9)
            if abs(p) != abs(q):
                break
        expanded = poly_tex((1, "xy"), (q, "x"), (p, "y"), (p * q, ""))
        ybr = poly_tex((1, "y"), (q, ""))
        right = f"({_lin(1, p)})({ybr})"
        # The numbers paired with the wrong letters; both signs flipped; the product put in one bracket.
        wrongs = [f"({_lin(1, q)})({poly_tex((1, 'y'), (p, ''))})", f"({_lin(1, -p)})({poly_tex((1, 'y'), (-q, ''))})",
                  f"({_lin(1, p * q)})({poly_tex((1, 'y'), (1, ''))})"]
        return MathDraw(expanded, right, prompt="จงแยกตัวประกอบ", distractors=_distinct(right, *wrongs))


@question_type("math.factor_square_minus_square_m2", display_name={"th": "ผลต่างของกำลังสองที่มีพหุนามในวงเล็บ"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorSquareMinusSquareM2(WordProblem):
    """(x + a)² − b² = (x + a − b)(x + a + b)."""

    def expr(self, rng: Random):
        while True:
            a, b = _nz(rng, -9, 9), rng.randint(2, 9)
            if abs(a) != b:
                break
        problem = f"({_lin(1, a)})^{{2}} - {b * b}"
        right = f"({_lin(1, a - b)})({_lin(1, a + b)})"
        # b² not square-rooted; a dropped; a squared bracket.
        wrongs = [f"({_lin(1, a - b * b)})({_lin(1, a + b * b)})", f"({_lin(1, -b)})({_lin(1, b)})",
                  f"({_lin(1, a - b)})^{{2}}", f"({_lin(1, -a - b)})({_lin(1, -a + b)})"]
        return MathDraw(problem, right, prompt="จงแยกตัวประกอบ", distractors=_distinct(right, *wrongs))


@question_type("math.factor_perfect_square_check_m2", display_name={"th": "พหุนามใดเป็นกำลังสองสมบูรณ์"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorPerfectSquareCheckM2(WordProblem):
    """x² ± 2kx + k² is a perfect square; kx in the middle, 2k as the constant, or −k² are not."""

    def expr(self, rng: Random):
        k, s = rng.randint(3, 9), rng.choice((1, -1))  # from 3: at 2, 2k = k² and a wrong choice is right
        right = _quad(1, s * 2 * k, k * k)
        wrongs = [_quad(1, s * k, k * k), _quad(1, s * 2 * k, 2 * k), _quad(1, s * 2 * k, -k * k)]
        return MathDraw("", right, prompt="พหุนามในข้อใดเป็นกำลังสองสมบูรณ์", distractors=_distinct(right, *wrongs))


@question_type("math.factor_perfect_square_k_m2", display_name={"th": "หาค่าคงตัวที่ทำให้เป็นกำลังสองสมบูรณ์"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorPerfectSquareKM2(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        c = rng.randint(2, 12)
        if kind == 0:
            # x² + kx + c² with k > 0: k = 2c.
            return MathDraw("", str(2 * c), prompt=f"ถ้า x² + kx + {c * c} เป็นกำลังสองสมบูรณ์ และ k > 0 แล้ว k มีค่าเท่าใด",
                            distractors=_story.keep(c, c * c, 4 * c, 2 * c * c, answer=2 * c, lo=1))
        if kind == 1:
            # x² + 2cx + k: k = c².
            return MathDraw("", str(c * c), prompt=f"ถ้า x² + {2 * c}x + k เป็นกำลังสองสมบูรณ์ แล้ว k มีค่าเท่าใด",
                            distractors=_story.keep(2 * c, 4 * c * c, c, (2 * c) ** 2, answer=c * c, lo=1))
        a = rng.randint(2, 5)
        c = rng.choice([v for v in range(1, 10) if math.gcd(a, v) == 1])
        return MathDraw("", str(2 * a * c), prompt=(f"ถ้า {a * a}x² + kx + {c * c} เป็นกำลังสองสมบูรณ์ และ k > 0 "
                                                   f"แล้ว k มีค่าเท่าใด"),
                        distractors=_story.keep(a * c, 2 * c, 2 * a * a * c, a * a + c * c, answer=2 * a * c, lo=1))


@question_type("math.factor_two_variable_m2", display_name={"th": "ดึงตัวประกอบร่วมที่มีตัวแปรสองตัว"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorTwoVariableM2(WordProblem):
    """gax²y ± gbxy² = gxy(ax ± by)."""

    def expr(self, rng: Random):
        while True:
            g, a, b = rng.randint(2, 9), rng.randint(1, 7), rng.randint(1, 7)
            if a != b and math.gcd(a, b) == 1:
                break
        s = rng.choice((1, -1))
        expanded = poly_tex((g * a, "x^{2}y"), (s * g * b, "xy^{2}"))
        right = f"{g}xy({poly_tex((a, 'x'), (s * b, 'y'))})"
        wrongs = [f"{g}({poly_tex((a, 'x^{2}y'), (s * b, 'xy^{2}'))})", f"xy({poly_tex((g * a, 'x'), (s * g * b, 'y'))})",
                  f"{g}xy({poly_tex((a, 'x'), (-s * b, 'y'))})", f"{g}x({poly_tex((a, 'xy'), (s * b, 'y^{2}'))})"]
        return MathDraw(expanded, right, prompt="จงแยกตัวประกอบให้สมบูรณ์", distractors=_distinct(right, *wrongs))
