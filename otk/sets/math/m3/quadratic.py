"""สมการกำลังสอง

คณิตศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ค 1.3 ม.3/2

Sets moved here from: math, math_algebra, math_bank_real, math_m3.
"""

from __future__ import annotations

import math
from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_tex, poly_tex
from otk.sets._support.math_algebra import _nonzero
from otk.sets._support.math_bank_real import M3, _agree, _count_q, _tex_q
from otk.sets._support.math_m3 import LEVEL
from otk.sets._support.math_m4 import maths as _num_maths


def pairs_with_real_roots(n: int) -> int:
    """(b, c) ∈ {1..n}² with x² + bx + c = 0 having a real solution: b² ≥ 4c."""
    return sum(1 for b in range(1, n + 1) for c in range(1, n + 1) if b * b >= 4 * c)


def largest_negative_no_real(p: int) -> int:
    """Largest negative integer a with a²x² + px + 1 = 0 having no real root: p² < 4a²."""
    return -(p // 2 + 1)


def _sqrt_tex(n: int) -> str:
    r = math.isqrt(n)
    if r * r == n:
        return str(r)
    k = max(d for d in range(1, r + 1) if n % (d * d) == 0)
    return rf"{k if k > 1 else ''}\sqrt{{{n // (k * k)}}}"


@question_type("math.quadratic_equation",
               display_name={"th": "สมการกำลังสอง"}, level={"th": "ม.3"},
               topic="สมการกำลังสอง")
class QuadraticEquation(MathType):
    def expr(self, rng: Random, root_hi: int = 9, formula: int = 0):
        if formula:
            m = rng.randint(-4, 4)
            d = rng.choice([2, 3, 5, 6, 7, 10])
            tex = poly_tex((1, "x^{2}"), (-2 * m, "x"), (m * m - d, ""))
            return MathDraw(
                rf"{tex} = 0", rf"x = {m} \pm \sqrt{{{d}}}",
                hint=r"x = \frac{-b \pm \sqrt{b^2 - 4ac}}{2a}", prompt="จงแก้สมการ")
        r1 = rng.choice([1, -1]) * rng.randint(1, root_hi)
        r2 = rng.choice([1, -1]) * rng.randint(1, root_hi)
        tex = poly_tex((1, "x^{2}"), (-(r1 + r2), "x"), (r1 * r2, ""))
        answer = rf"x = {r1}" if r1 == r2 else rf"x = {min(r1, r2)}, \; {max(r1, r2)}"
        return MathDraw(rf"{tex} = 0", answer,
                        hint=r"\text{factorise first}", prompt="จงแก้สมการ")
QuadraticEquation.PROVENANCE = Provenance("original")


@question_type("math.quadratic_sum_product_roots",
               display_name={"th": "สมการกำลังสองจากรากที่กำหนด"},
               level={"th": "ม.3"}, topic="สมการกำลังสอง")
class QuadraticFromRoots(MathType):
    def expr(self, rng: Random, root_hi: int = 9):
        r1, r2 = (rng.randint(-root_hi, root_hi) for _ in range(2))
        b, c = -(r1 + r2), r1 * r2
        return MathDraw(
            f"{r1}, {r2}", poly_tex((1, "x^2"), (b, "x"), (c, "")) + " = 0",
            prompt="สมการกำลังสองใดมีรากตามที่กำหนด",
            distractors=[poly_tex((1, "x^2"), (-b, "x"), (c, "")) + " = 0",
                         poly_tex((1, "x^2"), (b, "x"), (-c, "")) + " = 0",
                         poly_tex((1, "x^2"), (-b, "x"), (-c, "")) + " = 0"])
QuadraticFromRoots.PROVENANCE = Provenance("original")


@question_type("math.quadratic_formula_roots",
               display_name={"th": "สมการกำลังสองด้วยสูตร"},
               level={"th": "ม.3"}, topic="สมการกำลังสอง")
class QuadraticFormulaRoots(MathType):
    """Leading coefficient ≠ 1, so factoring by inspection stops being enough."""
    break_convergence = True  # one-part slips cluster round the answer

    def expr(self, rng: Random, lead_hi: int = 4, root_hi: int = 6):
        a = rng.randint(2, lead_hi)
        r1, r2 = (_nonzero(rng, -root_hi, root_hi) for _ in range(2))
        # a(x − r1)(x − r2)
        b, c = -a * (r1 + r2), a * r1 * r2
        lo, hi = sorted((r1, r2))
        return MathDraw(
            poly_tex((a, "x^2"), (b, "x"), (c, "")) + " = 0",
            f"x = {lo}, {hi}", prompt="จงแก้สมการ",
            distractors=[f"x = {-lo}, {-hi}",
                         f"x = {lo * a}, {hi * a}",
                         f"x = {frac_tex(Fraction(lo, a))}, {frac_tex(Fraction(hi, a))}"])
QuadraticFormulaRoots.PROVENANCE = Provenance("original")


@question_type("math.quadratic_discriminant_m3",
               display_name={"th": "ตัวจำแนกและจำนวนคำตอบจริงของสมการกำลังสอง"},
               level=M3, topic="สมการกำลังสอง")
class QuadraticDiscriminantM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            m = rng.choice((2, 3, 5, 6, 7, 10, 4, 9))
            root = _sqrt_tex(4 * m)
            right = rf"(-{root}, {root})"
            half = _sqrt_tex(m)
            wrongs = [rf"(-{half}, {half})", rf"(-\infty, -{root}) \cup ({root}, \infty)",
                      rf"[-{root}, {root}]"]
            stem = [text("เซตของจำนวนจริง k ที่ทำให้สมการ"),
                    content_math(rf"x^{{2}} - kx + {m} = 0"),
                    text("ไม่มีคำตอบที่เป็นจำนวนจริง คือเซตในข้อใด")]
            return _tex_q(stem, right, wrongs, self.topic)
        if kind == 1:
            n = rng.randint(3, 7)
            right = pairs_with_real_roots(n)
            strict = sum(1 for b in range(1, n + 1) for c in range(1, n + 1) if b * b > 4 * c)
            stem = [text(f"กำหนดให้ S = {{1, 2, …, {n}}} จำนวนคู่อันดับ (b, c) ที่ b, c ∈ S "
                         f"ซึ่งทำให้สมการ"), content_math(r"x^{2} + bx + c = 0"),
                    text("มีคำตอบเป็นจำนวนจริง มีทั้งหมดกี่คู่")]
            # Forgetting the double root (> instead of ≥); the complement; all pairs.
            return _count_q(stem, right, [strict, n * n - right, n * n], self.topic)
        p = rng.choice((5, 7, 9, 11, 13, 15, 8, 10, 12))
        right = largest_negative_no_real(p)
        _agree(right, max(a for a in range(-50, 0) if p * p - 4 * a * a < 0))
        stem = [text("ให้ a เป็นจำนวนเต็มลบที่มากที่สุดที่ทำให้สมการ"),
                content_math(rf"a^{{2}}x^{{2}} + {p}x + 1 = 0"),
                text("ไม่มีคำตอบที่เป็นจำนวนจริง a มีค่าเท่าใด")]
        # The boundary itself; the positive twin; −p/2 truncated.
        wrongs = [right + 1, -right, -(p // 2)]
        return _num_maths(stem, str(right), [str(w) for w in wrongs if w != right], self.topic)
QuadraticDiscriminantM3.PROVENANCE = Provenance("adapted", sources=('openthaiknowledge-bank/rathcenter/3 จำนวนจริง',))


@question_type("math.quadratic_word_problem_m3",
               display_name={"th": "โจทย์ปัญหาสมการกำลังสองตัวแปรเดียว"},
               level=LEVEL, topic="สมการกำลังสอง")
class QuadraticWordProblemM3(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(4)
        if kind == 0:
            w, d = rng.randint(3, 25), rng.randint(2, 12)
            return MathDraw("", str(w),
                            prompt=(f"สนามรูปสี่เหลี่ยมผืนผ้ามีความยาวมากกว่าความกว้าง {d} เมตร มีพื้นที่ "
                                    f"{w * (w + d)} ตารางเมตร สนามกว้างกี่เมตร"),
                            # The length instead of the width, and the root of the area.
                            distractors=_story.keep(w + d, math.isqrt(w * (w + d)) + 1, w * (w + d) // d,
                                                    w - 1, answer=w, lo=1))
        if kind == 1:
            n = rng.randint(4, 30)
            return MathDraw("", str(n),
                            prompt=(f"จำนวนเต็มบวกสองจำนวนเรียงติดกันมีผลคูณเท่ากับ {n * (n + 1)} "
                                    f"จำนวนที่น้อยกว่าคือจำนวนใด"),
                            distractors=_story.keep(n + 1, n - 1, n * (n + 1) // 2, answer=n, lo=1))
        if kind == 2:
            x, k = rng.randint(4, 20), rng.randint(1, 9)
            c = x * x - k * x
            if c <= 0:
                return self.expr(rng)
            return MathDraw("", str(x),
                            prompt=(f"จำนวนบวกจำนวนหนึ่ง ยกกำลังสองแล้วลบด้วย {k} เท่าของจำนวนนั้น ได้ผลลัพธ์ "
                                    f"เท่ากับ {c} จำนวนนั้นคือจำนวนใด"),
                            # The negative root's size, and c / k.
                            distractors=_story.keep(c // x if c % x == 0 and c // x != x else x + k,
                                                    x - k if x > k else x + 1, x + 1, answer=x, lo=1))
        s = rng.randint(5, 20)
        path = rng.randint(1, 3)
        big = (s + 2 * path) ** 2
        return MathDraw("", str(s),
                        prompt=(f"สวนรูปสี่เหลี่ยมจัตุรัสมีทางเดินกว้าง {path} เมตร ล้อมรอบด้านนอก พื้นที่ของสวน"
                                f"รวมทางเดินเท่ากับ {big} ตารางเมตร สวน (ไม่รวมทางเดิน) ยาวด้านละกี่เมตร"),
                        # Taking the path off once instead of on both sides.
                        distractors=_story.keep(s + path, s + 2 * path, s - path, answer=s, lo=1))
QuadraticWordProblemM3.PROVENANCE = Provenance("original")


from otk.core.content import math as _math_block  # noqa: E402
from otk.core.content import text as _text_block  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType, WordProblem  # noqa: E402
from otk.sets._support.math_m3 import LEVEL  # noqa: E402
from otk.sets._support.math_p2 import _maths as _fixed_maths  # noqa: E402
from otk.sets._support.math_p2 import _texts as _fixed_texts  # noqa: E402


def _fk3(*values: Fraction, answer: Fraction, lo: Fraction | None = None) -> list[str]:
    """Distinct fraction distractors as TeX, the answer (and values below lo) left out."""
    out: list[str] = []
    for v in values:
        v = Fraction(v)
        if v == answer or (lo is not None and v < lo) or frac_tex(v) in out:
            continue
        out.append(frac_tex(v))
    return out


def _tk3(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _roots3(a: int, b: int) -> str:
    lo, hi = sorted((a, b))
    return rf"x = {lo}, \; {hi}"


def _g3(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572."""
    return f"{n:,}".replace(",", "{,}")


def _gk3(*values: int, answer: int, lo: int = 0) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g3(int(v)) for v in _story.keep(*values, answer=answer, lo=lo)]


# ── More quadratic equations (2026-11): how many real roots, the sum of the roots, a rectangle's width from
# its area, consecutive numbers, and which number is a root ──


@question_type("math.quadratic_root_count_m3", display_name={"th": "สมการกำลังสองมีคำตอบที่เป็นจำนวนจริงกี่คำตอบ"},
               level=LEVEL, topic="สมการกำลังสอง")
class QuadraticRootCountM3(QuestionType):
    _OPTIONS = ("มี 2 คำตอบที่ต่างกัน", "มี 1 คำตอบ (คำตอบซ้ำ)", "ไม่มีคำตอบที่เป็นจำนวนจริง", "มีคำตอบมากกว่า 2 คำตอบ")

    def build(self, rng: Random, **params):
        kind = rng.randrange(3)
        a = rng.randint(1, 3)
        if kind == 0:
            b = rng.choice((1, -1)) * rng.randint(5, 12)
            c = rng.randint(1, b * b // (4 * a) - 1)
        elif kind == 1:
            h = rng.choice((1, -1)) * rng.randint(1, 6)
            a, b, c = 1, -2 * h, h * h
        else:
            b = rng.randint(-4, 4)
            c = rng.randint(b * b // (4 * a) + 1, b * b // (4 * a) + 10)
        right = self._OPTIONS[kind]
        stem = [_text_block("สมการนี้มีคำตอบที่เป็นจำนวนจริงกี่คำตอบ"),
                _math_block(f"{poly_tex((a, 'x^{2}'), (b, 'x'), (c, ''))} = 0")]
        return _fixed_texts(stem, right, [o for o in self._OPTIONS if o != right], self.topic)


@question_type("math.quadratic_sum_of_roots_m3", display_name={"th": "ผลบวกของคำตอบของสมการกำลังสอง"},
               level=LEVEL, topic="สมการกำลังสอง")
class QuadraticSumOfRootsM3(MathType):
    def expr(self, rng: Random):
        while True:
            p, q = rng.choice((1, -1)) * rng.randint(1, 9), rng.choice((1, -1)) * rng.randint(1, 9)
            if p + q != 0 and p != q:
                break
        right = p + q
        # The sign kept from b; the product; one root.
        return MathDraw(f"{poly_tex((1, 'x^{2}'), (-(p + q), 'x'), (p * q, ''))} = 0", str(right),
                        prompt="ผลบวกของคำตอบทั้งสองของสมการนี้เท่ากับเท่าใด",
                        distractors=_tk3(str(-right), str(p * q), str(max(p, q)), str(right + 1), answer=str(right)))


@question_type("math.rectangle_width_from_area_m3", display_name={"th": "หาความกว้างจากพื้นที่ (สมการกำลังสอง)"},
               level=LEVEL, topic="สมการกำลังสอง")
class RectangleWidthFromAreaM3(WordProblem):
    def expr(self, rng: Random):
        w = rng.randint(3, 20)
        d = rng.randint(1, 12)
        area = w * (w + d)
        prompt = f"รูปสี่เหลี่ยมผืนผ้ามีด้านยาวมากกว่าด้านกว้าง {d} เมตร และมีพื้นที่ {area} ตารางเมตร ด้านกว้างยาวกี่เมตร"
        # The length; the area over the difference; the other root's size.
        return MathDraw("", str(w), prompt=prompt,
                        distractors=_story.keep(w + d, area // d if area // d != w else w + 2, w + d + d, w - 1,
                                                answer=w, lo=1))


@question_type("math.consecutive_product_m3", display_name={"th": "จำนวนนับสองจำนวนที่เรียงติดกันเมื่อรู้ผลคูณ"},
               level=LEVEL, topic="สมการกำลังสอง")
class ConsecutiveProductM3(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(4, 30)
        step = rng.choice((1, 2))
        prod = n * (n + step)
        kind = "จำนวนนับสองจำนวนที่เรียงติดกัน" if step == 1 else "จำนวนคู่สองจำนวนที่เรียงติดกัน" if n % 2 == 0 else "จำนวนคี่สองจำนวนที่เรียงติดกัน"
        prompt = f"{kind}มีผลคูณเท่ากับ {prod} จำนวนที่น้อยกว่าคือจำนวนใด"
        # The larger number; half the product; one off.
        return MathDraw("", str(n), prompt=prompt,
                        distractors=_story.keep(n + step, prod // 2, n - step, n + 2 * step, answer=n, lo=1))


@question_type("math.which_root_m3", display_name={"th": "จำนวนใดเป็นคำตอบของสมการกำลังสอง"},
               level=LEVEL, topic="สมการกำลังสอง")
class WhichRootM3(QuestionType):
    """Fixed choices: a number from another draw could also be a root."""

    def build(self, rng: Random, **params):
        while True:
            p, q = rng.choice((1, -1)) * rng.randint(1, 9), rng.choice((1, -1)) * rng.randint(1, 9)
            if p != q and p != -q:
                break
        poly = poly_tex((1, "x^{2}"), (-(p + q), "x"), (p * q, ""))
        right = str(p)
        # The roots' signs flipped; the constant.
        wrongs = [str(w) for w in (-p, -q, p * q, p + q + 10, p + q + 11) if w not in (p, q)]
        return _fixed_maths([_text_block("จำนวนใดเป็นคำตอบของสมการ"), _math_block(f"{poly} = 0")], right,
                            _tk3(*wrongs, answer=right)[:3], self.topic)


QuadraticRootCountM3.PROVENANCE = Provenance("original")
QuadraticSumOfRootsM3.PROVENANCE = Provenance("original")
RectangleWidthFromAreaM3.PROVENANCE = Provenance("original")
ConsecutiveProductM3.PROVENANCE = Provenance("original")
WhichRootM3.PROVENANCE = Provenance("original")
