"""เอกนามและพหุนาม

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: ค 1.2 ม.2/1

Sets moved here from: math, math_apply_basic.
"""

from __future__ import annotations

import math
from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import (
    MathDraw,
    MathType,
    WordProblem,
    frac_tex,
    mono_tex,
    poly_tex,
    rand_proper,
)

PROVENANCE = Provenance("original")


def _nz(rng: Random, hi: int, lo: int = 1) -> int:
    """Random nonzero integer with lo <= |n| <= hi."""
    return rng.choice([1, -1]) * rng.randint(lo, hi)


def _x_sym(e: int) -> str:
    return "" if e == 0 else "x" if e == 1 else f"x^{{{e}}}"


def xpoly(*pairs: tuple[int, int]) -> str:
    """Polynomial in x from (coefficient, exponent) pairs, highest power first."""
    coefs: dict[int, int] = {}
    for c, e in pairs:
        coefs[e] = coefs.get(e, 0) + c
    return poly_tex(*((coefs[e], _x_sym(e)) for e in sorted(coefs, reverse=True)))


def _vars_tex(exps: dict[str, int]) -> str:
    return "".join(v if e == 1 else f"{v}^{{{e}}}" for v, e in exps.items() if e)


def _coef_prefix(c: Fraction, has_vars: bool) -> str:
    """Coefficient written in front of the letters: 1 and -1 drop the digit."""
    if has_vars and abs(c) == 1:
        return "-" if c < 0 else ""
    return frac_tex(c)


def _rand_monomial(rng: Random) -> str:
    kind = rng.choice(["int", "int", "unit", "frac", "sqrt", "const"])
    exps = {v: rng.randint(0, 3) for v in "xy"}
    if not any(exps.values()):
        exps["x"] = rng.randint(1, 3)
    body = _vars_tex(exps)
    if kind == "unit":
        return rng.choice(["", "-"]) + body
    if kind == "frac":
        return frac_tex(_nz(rng, 1) * rand_proper(rng, 2, 7)) + body
    if kind == "sqrt":
        return rf"{rng.choice(['', '-'])}\sqrt{{{rng.choice([2, 3, 5])}}}{body}"
    if kind == "const":
        return str(_nz(rng, 12))
    return f"{_nz(rng, 9, lo=2)}{body}"


def _rand_multiterm(rng: Random) -> str:
    """A polynomial of two or three unlike terms — never a single monomial."""
    if rng.random() < 0.5:
        return xpoly(*((_nz(rng, 9), e) for e in rng.sample([3, 2, 1, 0],
                                                            rng.choice([2, 3]))))
    return poly_tex((_nz(rng, 6), "x^{2}"), (_nz(rng, 6), "xy"),
                    (_nz(rng, 6), rng.choice(["y", "y^{2}", ""])))


def _rand_non_polynomial(rng: Random) -> str:
    """An exponent that is negative or fractional, or a letter in a denominator."""
    k, n = rng.randint(2, 9), rng.randint(1, 3)
    return rng.choice([
        rf"\frac{{{k}}}{{{_x_sym(n)}}}",
        rf"{k}x^{{-{n}}}",
        r"\sqrt{x}",
        rf"{k}\sqrt{{x}}",
        r"x^{\frac{1}{2}}",
        rf"x + \frac{{{k}}}{{x}}",
        rf"\frac{{x + {k}}}{{x}}",
    ])


def _poly(*coeffs: int, var: str = "x") -> str:
    """(2, 11, 12) -> 2x^{2} + 11x + 12, highest power first."""
    deg = len(coeffs) - 1
    out = ""
    for i, c in enumerate(coeffs):
        p = deg - i
        if c == 0:
            continue
        mag = abs(c)
        body = ("" if mag == 1 and p else str(mag)) + (var if p else "") + (f"^{{{p}}}" if p > 1 else "")
        sign = "-" if c < 0 else "+"
        out += (f"{'-' if c < 0 else ''}{body}" if not out else f" {sign} {body}")
    return out or "0"


@question_type("math.classify_monomial_polynomial",
               display_name={"th": "จำแนกเอกนามและพหุนาม"}, level={"th": "ม.2"},
               topic="เอกนามและพหุนาม")
class ClassifyMonomialPolynomial(QuestionType):
    # (question, the correct kind, the kinds its wrong choices come from).
    # Every monomial is also a polynomial, so "polynomial" alone is never the
    # correct kind — it would make a monomial choice correct too.
    ASKS = [
        ("ข้อใดเป็นเอกนาม", "mono", ("multi", "multi", "nonpoly")),
        ("ข้อใดไม่เป็นเอกนาม", "notmono", ("mono",) * 3),
        ("ข้อใดเป็นพหุนามแต่ไม่เป็นเอกนาม", "multi", ("mono", "mono", "nonpoly")),
        ("ข้อใดไม่เป็นพหุนาม", "nonpoly", ("mono", "mono", "multi")),
    ]

    def build(self, rng: Random) -> GeneratedQuestion:
        makers = {"mono": _rand_monomial, "multi": _rand_multiterm,
                  "nonpoly": _rand_non_polynomial,
                  "notmono": lambda r: (_rand_multiterm if r.random() < 0.5
                                        else _rand_non_polynomial)(r)}
        ask, right, wrong_kinds = rng.choice(self.ASKS)
        correct = makers[right](rng)
        seen, wrongs = {correct}, []
        for kind in wrong_kinds:
            while (tex := makers[kind](rng)) in seen:
                pass
            seen.add(tex)
            wrongs.append(tex)
        return GeneratedQuestion(
            stem=[text(ask)],
            correct=[content_math(correct)],
            distractors=fixed(*[[content_math(t)] for t in wrongs]),
            topic=self.topic,
            hint=[text("เอกนามคือค่าคงตัวคูณกับตัวแปรที่มีเลขชี้กำลังเป็นจำนวนเต็มบวกหรือศูนย์ "
                       "พหุนามคือเอกนามหรือผลบวกของเอกนาม — เอกนามทุกตัวจึงเป็นพหุนาม")],
        )


@question_type("math.monomial_coefficient_degree",
               display_name={"th": "สัมประสิทธิ์และดีกรีของเอกนาม"}, level={"th": "ม.2"},
               topic="เอกนามและพหุนาม")
class MonomialCoefficientDegree(WordProblem):
    def expr(self, rng: Random):
        if rng.random() < 0.1:                       # a constant: degree 0
            c = Fraction(_nz(rng, 12, lo=2))
            exps = {"x": 0, "y": 0, "z": 0}
        else:
            c = (Fraction(_nz(rng, 9)) if rng.random() < 0.75
                 else _nz(rng, 1) * rand_proper(rng, 2, 7))
            names = rng.sample("xyz", rng.choice([1, 2, 2, 3]))
            exps = {v: (rng.randint(1, 5) if v in names else 0) for v in "xyz"}
        body = _vars_tex(exps)
        mono = _coef_prefix(c, bool(body)) + body
        deg = sum(exps.values())
        used = [e for e in exps.values() if e]
        # Mistakes: the highest power only, the number of letters, the product
        # of the powers. They coincide for one letter to the first power, so
        # off-by-ones follow to keep three distinct wrong choices on hand —
        # the sibling filler would mix in answers to the other two asks.
        wrong_deg = [max(used, default=1), len(used),
                     math.prod(used) if used else 1, deg + 1, deg + 2, deg + 3]
        ask = rng.choice(["coef", "deg", "both"])
        if ask == "coef":
            return MathDraw(
                mono, frac_tex(c), prompt="จงหาสัมประสิทธิ์ของเอกนาม",
                distractors=[frac_tex(-c), str(deg),
                             "0" if abs(c) == 1 else frac_tex(c / abs(c)),
                             frac_tex(c + 1), frac_tex(c - 1)])
        if ask == "deg":
            return MathDraw(mono, str(deg), prompt="จงหาดีกรีของเอกนาม",
                            distractors=[str(d) for d in wrong_deg])
        pair = lambda k, d: rf"({frac_tex(k)},\ {d})"
        return MathDraw(
            mono, pair(c, deg),
            prompt="จงหาสัมประสิทธิ์และดีกรีของเอกนาม ตอบในรูป (สัมประสิทธิ์, ดีกรี)",
            distractors=[rf"({deg},\ {frac_tex(c)})", pair(-c, deg),
                         *(pair(c, d) for d in wrong_deg)])


@question_type("math.monomial_like_addsub",
               display_name={"th": "บวก/ลบเอกนามที่คล้ายกัน"}, level={"th": "ม.2"},
               topic="เอกนามและพหุนาม")
class MonomialLikeAddSub(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        px, py = rng.randint(1, 3), rng.randint(0, 2)
        sym = mono_tex(1, px, py)
        while True:
            cs = [_nz(rng, 9) for _ in range(rng.choice([2, 2, 3]))]
            total = sum(cs)
            if total:
                break
        # Every term but the first is written with its own sign: 5x - 8x + x.
        problem = poly_tex(*((c, sym) for c in cs))
        return MathDraw(
            problem, mono_tex(total, px, py),
            prompt="จงทำให้เป็นรูปอย่างง่าย",
            hint=r"\text{like terms: add the coefficients, keep the letters}",
            distractors=[mono_tex(total, px * len(cs), py * len(cs)),
                         mono_tex(-total, px, py),
                         mono_tex(sum(map(abs, cs)), px, py)])


@question_type("math.negate_polynomial",
               display_name={"th": "เครื่องหมายลบหน้าวงเล็บ"}, level={"th": "ม.2"},
               topic="เอกนามและพหุนาม")
class NegatePolynomial(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        # -(±ax ± b), and later -(±ax² ± bx ± c): every sign inside flips.
        n = rng.choice([2, 2, 3])
        cs = [_nz(rng, 9) for _ in range(n)]
        pairs = list(zip(cs, range(n - 1, -1, -1)))
        inner = xpoly(*pairs)
        neg = [(-c, e) for c, e in pairs]
        # Mistakes: the minus reaches only the first term, or skips it.
        first_only = [neg[0], *pairs[1:]]
        first_skipped = [pairs[0], *neg[1:]]
        return MathDraw(
            rf"-({inner})", xpoly(*neg),
            prompt="จงทำให้เป็นรูปอย่างง่าย",
            hint=r"-(a + b) = -a - b",
            distractors=[xpoly(*first_only), xpoly(*first_skipped), inner])


@question_type("math.combine_like_terms",
               display_name={"th": "รวมพจน์ที่คล้ายกันในพหุนาม"}, level={"th": "ม.2"},
               topic="เอกนามและพหุนาม")
class CombineLikeTerms(MathType):
    def expr(self, rng: Random):
        exps = [1, 1, 0, 0] + ([2, 2] if rng.random() < 0.4 else [])
        while True:
            terms = [(_nz(rng, 9), e) for e in exps]
            rng.shuffle(terms)
            sums = {e: sum(c for c, t in terms if t == e) for e in set(exps)}
            if sums[1]:
                break
        # Mistake: every term after the first read as "+" (the sign is dropped).
        dropped = [terms[0], *((abs(c), e) for c, e in terms[1:])]
        return MathDraw(
            poly_tex(*((c, _x_sym(e)) for c, e in terms)),
            xpoly(*terms),
            prompt="จงทำให้เป็นรูปอย่างง่าย",
            hint=r"\text{group the } x \text{ terms and the constants separately}",
            distractors=[xpoly(*dropped),
                         xpoly(*((-c, e) if e == 0 else (c, e) for c, e in terms)),
                         xpoly((sum(c for c, _ in terms), 1))])


@question_type("math.polynomial_addsub",
               display_name={"th": "บวก/ลบพหุนาม"}, level={"th": "ม.2"},
               topic="เอกนามและพหุนาม")
class PolynomialAddSub(MathType):
    def expr(self, rng: Random):
        a1, b1, a2, b2 = (rng.randint(-6, 6) for _ in range(4))
        op = rng.choice("+-")
        if op == "+":
            ax, bx = a1 + a2, b1 + b2
        else:
            ax, bx = a1 - a2, b1 - b2
        p1 = poly_tex((a1, "x"), (b1, ""))
        p2 = poly_tex((a2, "x"), (b2, ""))
        return MathDraw(rf"({p1}) {op} ({p2})", poly_tex((ax, "x"), (bx, "")),
                        distractors=[poly_tex((ax, "x"), (b1 + b2 if op == "-"
                                                          else b1 - b2, "")),
                                     poly_tex((a1 + a2, "x"), (b1 - b2, ""))])


@question_type("math.polynomial_addsub_quadratic",
               display_name={"th": "บวก/ลบพหุนามดีกรีสอง"}, level={"th": "ม.2"},
               topic="เอกนามและพหุนาม")
class PolynomialAddSubQuadratic(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        p = [(_nz(rng, 7), e) for e in (2, 1, 0)]
        q = [(_nz(rng, 7), e) for e in (2, 1, 0)]
        op = rng.choice("+--")          # subtraction is the one that needs practice
        s = 1 if op == "+" else -1
        ans = xpoly(*p, *((s * c, e) for c, e in q))
        if op == "-":
            # Mistake: only the first term of the second bracket changes sign.
            wrong = xpoly(*p, (-q[0][0], 2), *q[1:])
            flipped = xpoly(*((-c, e) for c, e in p), *q)
        else:
            # Mistake: the constants subtracted instead of added.
            wrong = xpoly(*p, *q[:2], (-q[2][0], 0))
            flipped = xpoly(*p, *((-c, e) for c, e in q))
        return MathDraw(
            rf"({xpoly(*p)}) {op} ({xpoly(*q)})", ans,
            prompt="จงทำให้เป็นรูปอย่างง่าย",
            distractors=[wrong, flipped,
                         xpoly(*p, *((s * c, e) for c, e in q), (1, 0))])


@question_type("math.monomial_product",
               display_name={"th": "คูณเอกนามด้วยเอกนาม"}, level={"th": "ม.2"},
               topic="เอกนามและพหุนาม")
class MonomialProduct(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        c1, c2 = _nz(rng, 6), _nz(rng, 6, lo=2)
        p1, q1 = rng.randint(1, 4), rng.randint(0, 3)
        p2, q2 = rng.randint(1, 3), rng.randint(0, 3)
        wrong = [mono_tex(c1 * c2, p1 * p2, q1 * q2),
                 mono_tex(-c1 * c2, p1 + p2, q1 + q2)]
        if c1 + c2:
            wrong.append(mono_tex(c1 + c2, p1 + p2, q1 + q2))
        return MathDraw(
            rf"({mono_tex(c1, p1, q1)})({mono_tex(c2, p2, q2)})",
            mono_tex(c1 * c2, p1 + p2, q1 + q2),
            prompt="จงทำให้เป็นรูปอย่างง่าย",
            hint=r"x^m \cdot x^n = x^{m+n}",
            distractors=wrong)


@question_type("math.monomial_times_polynomial",
               display_name={"th": "คูณเอกนามกับพหุนาม"}, level={"th": "ม.2"},
               topic="เอกนามและพหุนาม")
class MonomialTimesPolynomial(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        k = rng.randint(2, 5)
        a = rng.choice([n for n in range(-5, 6) if n])
        b = rng.choice([n for n in range(-5, 6) if n])
        inner = poly_tex((a, "x"), (b, ""))
        return MathDraw(
            rf"{k}x({inner})", poly_tex((k * a, "x^{2}"), (k * b, "x")),
            prompt="จงกระจาย",
            distractors=[poly_tex((k * a, "x^{2}"), (b, "")),
                         poly_tex((k * a, "x"), (k * b, ""))])


@question_type("math.negative_monomial_times_polynomial",
               display_name={"th": "คูณพหุนามด้วยเอกนามที่เป็นลบ"}, level={"th": "ม.2"},
               topic="เอกนามและพหุนาม")
class NegativeMonomialTimesPolynomial(MathType):
    def expr(self, rng: Random):
        k, p = rng.randint(1, 5), rng.choice([0, 1, 1, 2])
        if k == 1 and p == 0:
            k = 2
        n = rng.choice([2, 3])
        inner = [(_nz(rng, 6), e) for e in range(n - 1, -1, -1)]
        ans = [(-k * c, e + p) for c, e in inner]
        # Mistake: the minus reaches only the first term.
        first_only = [ans[0], *((k * c, e + p) for c, e in inner[1:])]
        return MathDraw(
            rf"{mono_tex(-k, p, 0)}({xpoly(*inner)})", xpoly(*ans),
            prompt="จงกระจาย",
            hint=r"\text{multiply every term, sign included}",
            distractors=[xpoly(*first_only),
                         xpoly(*((-c, e) for c, e in ans)),
                         xpoly(ans[0], *inner[1:])])


@question_type("math.monomial_quotient",
               display_name={"th": "หารเอกนามด้วยเอกนาม"}, level={"th": "ม.2"},
               topic="เอกนามและพหุนาม")
class MonomialQuotient(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        c, d = _nz(rng, 6), _nz(rng, 5, lo=2)
        px, py = rng.randint(1, 3), rng.randint(0, 2)
        dx, dy = rng.randint(1, 3), rng.randint(0, 2)
        num = mono_tex(c * d, px + dx, py + dy)
        den = mono_tex(d, dx, dy)
        return MathDraw(
            rf"({num}) \div ({den})" if rng.random() < 0.5
            else rf"\frac{{{num}}}{{{den}}}",
            mono_tex(c, px, py),
            prompt="จงทำให้เป็นรูปอย่างง่าย",
            hint=r"x^m \div x^n = x^{m-n}",
            distractors=[mono_tex(-c, px, py),
                         mono_tex(c, px + 2 * dx, py + 2 * dy),
                         mono_tex(c * d * d, px, py)])


# Registered after monomial_quotient: the ladder is staged in registration
# order, and multiplying and dividing monomials together belongs here.
@question_type("math.simplify_polynomial",
               display_name={"th": "คูณ-หารเอกนาม"}, level={"th": "ม.2"}, topic="เอกนามและพหุนาม")
class SimplifyPolynomial(MathType):
    def expr(self, rng: Random):
        if rng.random() < 0.5:
            c1 = rng.choice([1, -1]) * rng.randint(2, 5)
            c2 = rng.choice([1, -1]) * rng.randint(2, 5)
            p1, q1 = rng.randint(1, 3), rng.randint(0, 2)
            p2, q2 = rng.randint(0, 2), rng.randint(1, 3)
            return MathDraw(
                rf"({mono_tex(c1, p1, q1)})({mono_tex(c2, p2, q2)})",
                mono_tex(c1 * c2, p1 + p2, q1 + q2),
                topic="คูณเอกนาม", prompt="จงทำให้เป็นรูปอย่างง่าย")
        c = rng.choice([1, -1]) * rng.randint(2, 5)
        d = rng.choice([1, -1]) * rng.randint(2, 4)
        px, py = rng.randint(1, 3), rng.randint(0, 2)
        dx, dy = rng.randint(1, 2), rng.randint(0, 2)
        return MathDraw(
            rf"\frac{{{mono_tex(c * d, px + dx, py + dy)}}}{{{mono_tex(d, dx, dy)}}}",
            mono_tex(c, px, py),
            topic="หารเอกนาม", prompt="จงทำให้เป็นรูปอย่างง่าย")


@question_type("math.polynomial_div_monomial",
               display_name={"th": "หารพหุนามด้วยเอกนาม"}, level={"th": "ม.2"},
               topic="เอกนามและพหุนาม")
class PolynomialDivMonomial(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        k, p = _nz(rng, 5, lo=2), rng.randint(1, 2)
        n = rng.choice([2, 3])
        quot = [(_nz(rng, 6), e) for e in range(n - 1, -1, -1)]
        num = xpoly(*((k * c, e + p) for c, e in quot))
        # Mistakes: divide only the first term; keep the powers; lose the sign.
        first_only = [quot[0], *((k * c, e + p) for c, e in quot[1:])]
        return MathDraw(
            rf"\frac{{{num}}}{{{mono_tex(k, p, 0)}}}", xpoly(*quot),
            prompt="จงทำให้เป็นรูปอย่างง่าย",
            hint=r"\frac{a + b}{m} = \frac{a}{m} + \frac{b}{m}",
            distractors=[xpoly(*first_only),
                         xpoly(*((c, e + p) for c, e in quot)),
                         xpoly(*((-c, e) for c, e in quot))])


@question_type("math.distribute_and_simplify",
               display_name={"th": "กระจายแล้วจัดรูปพหุนาม"}, level={"th": "ม.2"},
               topic="เอกนามและพหุนาม")
class DistributeAndSimplify(MathType):
    def expr(self, rng: Random):
        while True:
            p, q = rng.randint(2, 5), rng.randint(2, 5)
            a, b, c, d = (_nz(rng, 6) for _ in range(4))
            op = rng.choice("+--")
            s = 1 if op == "+" else -1
            if p * a + s * q * c:
                break
        ans = poly_tex((p * a + s * q * c, "x"), (p * b + s * q * d, ""))
        return MathDraw(
            rf"{p}({poly_tex((a, 'x'), (b, ''))}) {op} "
            rf"{q}({poly_tex((c, 'x'), (d, ''))})", ans,
            prompt="จงทำให้เป็นรูปอย่างง่าย",
            distractors=[
                # the second factor's sign reaches only its first term
                poly_tex((p * a + s * q * c, "x"), (p * b + q * d, "")),
                # constant inside the bracket left unmultiplied
                poly_tex((p * a + s * q * c, "x"), (p * b + s * d, "")),
                poly_tex((p * a + s * q * c, "x"), (b + s * d, ""))])


@question_type("math.polynomial_area_m2",
               display_name={"th": "เขียนพื้นที่และปริมาตรเป็นพหุนาม"},
               level={"th": "ม.2"}, topic="เอกนามและพหุนาม")
class PolynomialAreaM2(WordProblem):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        kind = rng.randrange(5)
        if kind == 0:
            a, b, c = rng.randint(2, 4), rng.randint(1, 6), rng.randint(1, 6)
            return MathDraw("", _poly(a, a * c + b, b * c),
                            prompt=(f"สี่เหลี่ยมผืนผ้ายาว {a}x + {b} หน่วย กว้าง x + {c} หน่วย พื้นที่เป็นพหุนามใด"),
                            distractors=[_poly(a, b * c), _poly(a, a + b + c, b * c), _poly(a, a * c + b, b + c)])
        if kind == 1:
            w = rng.randint(1, 3)
            return MathDraw("", _poly(4 * w, 4 * w * w),
                            prompt=(f"กรอบรูปรูปสี่เหลี่ยมจัตุรัส ด้านในยาวด้านละ x หน่วย ขอบกรอบกว้าง {w} หน่วยทุกด้าน "
                                    f"พื้นที่ของขอบกรอบเป็นพหุนามใด"),
                            distractors=[_poly(2 * w, w * w), _poly(4 * w, 2 * w * w), _poly(1, 4 * w, 4 * w * w)])
        if kind == 2:
            k = rng.randint(2, 6)
            # garden x by (x + k) with a path 1 unit wide around it
            return MathDraw("", _poly(4, 2 * k + 4),
                            prompt=(f"สวนรูปสี่เหลี่ยมผืนผ้ากว้าง x เมตร ยาว x + {k} เมตร ทำทางเดินกว้าง 1 เมตรล้อมรอบสวน "
                                    f"พื้นที่ของทางเดินเป็นพหุนามใด"),
                            distractors=[_poly(2, k + 1), _poly(4, k + 4), _poly(1, k + 4, 2 * k + 4)])
        if kind == 3:
            h = rng.randint(2, 5)
            x = rng.randint(3, 9)
            vol = h * x * (x + 1)
            return MathDraw("", str(vol),
                            prompt=(f"กล่องมีฐานกว้าง x เซนติเมตร ยาว x + 1 เซนติเมตร สูง {h} เซนติเมตร "
                                    f"ปริมาตรจึงเป็น {h}x² + {h}x ลูกบาศก์เซนติเมตร "
                                    f"ถ้า x = {x} กล่องมีปริมาตรกี่ลูกบาศก์เซนติเมตร"),
                            distractors=_story.keep(h * x * x + h, h * (2 * x + 1), x * (x + 1), answer=vol, lo=1))
        big, small = rng.randint(3, 6), rng.randint(1, 2)
        # an L-shape: a square of side x + big with a square of side small cut from a corner
        return MathDraw("", _poly(1, 2 * big, big * big - small * small),
                        prompt=(f"แผ่นกระดาษรูปสี่เหลี่ยมจัตุรัสยาวด้านละ x + {big} หน่วย ตัดมุมหนึ่งออกเป็นสี่เหลี่ยมจัตุรัส "
                                f"ยาวด้านละ {small} หน่วย พื้นที่ที่เหลือเป็นพหุนามใด"),
                        distractors=[_poly(1, big * big - small * small), _poly(1, big, big * big - small * small),
                                     _poly(1, 2 * big, big * big + small * small)])
