"""เมทริกซ์

คณิตศาสตร์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม จำนวนและพีชคณิต 3 ม.5/3

Sets moved here from: math, math_algebra, math_apply_add, math_bank_matrices, math_gaps_indicators, math_m5.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_tex
from otk.sets._support.math_apply_add import M5 as M5_math_apply_add
from otk.sets._support.math_apply_add import _c
from otk.sets._support.math_gaps_indicators import M5 as M5_math_gaps_indicators
from otk.sets._support.math_gaps_indicators import _nz
from otk.sets._support.math_m4 import maths
from otk.sets._support.math_m4 import maths as _maths
from otk.sets._support.math_m5 import M5 as M5_math_m5
from otk.sets._support.math_m5 import _mat


def _independent(rng: Random, lo: int, hi: int) -> tuple[int, int, int, int]:
    while True:
        a1, c1, a2, c2 = (rng.randint(lo, hi) for _ in range(4))
        if a1 * c2 - a2 * c1:
            return a1, c1, a2, c2


M5 = {"th": "ม.5"}


TOPIC = "เมทริกซ์"


Matrix = list[list[Fraction]]


def _tex_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    """Named mistakes first; duplicates and the answer itself dropped; three kept."""
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right][:3]
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


def _frac_q(stem: list, right: Fraction, named: list, topic: str) -> GeneratedQuestion:
    out: list[str] = []
    for w in [*named, -right, right + 1, right - 1, right * 2, right + 2, right / 2]:
        if w is None:
            continue
        t = frac_tex(Fraction(w))
        if t != frac_tex(right) and t not in out:
            out.append(t)
    return _tex_q(stem, frac_tex(right), out, topic)


def mat(rows) -> Matrix:
    return [[Fraction(v) for v in row] for row in rows]


def det(m: Matrix) -> Fraction:
    """Cofactor expansion along the first row (n ≤ 3 here)."""
    if len(m) == 1:
        return m[0][0]
    return sum(((-1) ** j) * m[0][j] * det([row[:j] + row[j + 1:] for row in m[1:]]) for j in range(len(m)))


def matmul(a: Matrix, b: Matrix) -> Matrix:
    return [[sum(a[i][k] * b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]


def transpose(m: Matrix) -> Matrix:
    return [list(col) for col in zip(*m)]


def inverse(m: Matrix) -> Matrix:
    """Adjugate over determinant."""
    n, d = len(m), det(m)
    if n == 1:
        return [[1 / d]]
    cof = [[((-1) ** (i + j)) * det([r[:j] + r[j + 1:] for k, r in enumerate(m) if k != i]) for j in range(n)]
           for i in range(n)]
    return [[cof[j][i] / d for j in range(n)] for i in range(n)]


def mat_tex(m) -> str:
    """pmatrix of numbers; a string entry (an unknown) is printed as is."""
    cell = lambda x: x if isinstance(x, str) else frac_tex(Fraction(x))
    rows = r" \\ ".join(" & ".join(cell(x) for x in row) for row in m)
    return rf"\begin{{pmatrix}} {rows} \end{{pmatrix}}"


def _unimodular(rng: Random, n: int) -> Matrix:
    """An integer matrix with determinant ±1: a product of elementary row additions and a swap."""
    m = mat([[int(i == j) for j in range(n)] for i in range(n)])
    for _ in range(3 * n):
        i, j = rng.sample(range(n), 2)
        k = rng.choice((-2, -1, 1, 2))
        m[i] = [a + k * b for a, b in zip(m[i], m[j])]
    if rng.random() < 0.5:
        m[0], m[1] = m[1], m[0]
    if max(abs(v) for row in m for v in row) > 9:
        return _unimodular(rng, n)
    return m


def det_after(n: int, d: Fraction, op: str, k: int, c: Fraction, target: str) -> Fraction:
    """det of cB, cBᵗ or (cB)⁻¹, where B is A (n × n, det A = d) after one row operation.

    op: "swap" negates, "scale" multiplies by k, "add" leaves det unchanged.
    """
    b = {"swap": -d, "scale": k * d, "add": d}[op]
    scaled = c ** n * b
    return 1 / scaled if target == "inverse" else scaled


def det_inverse_from_scaled(n: int, k: int, v: Fraction) -> Fraction:
    """det(A⁻¹) when det(kA) = v for n × n A: det A = v / kⁿ."""
    return Fraction(k) ** n / v


def unknown_from_quotient(a12: int, b22: int, c11: int, e22: int, v: Fraction) -> Fraction:
    """x with det(B⁻¹A) = v for A = [[x, a12], [0, b22]], B = [[c11, 0], [x, e22]]: b22·x / (c11·e22) = v."""
    return v * c11 * e22 / b22


_OPS_TH = {"swap": "สลับแถวที่ 1 กับแถวที่ 2 ของ A",
           "add": "บวก {k} เท่าของแถวที่ 1 เข้ากับแถวที่ 2 ของ A",
           "scale": "คูณแถวที่ 2 ของ A ด้วย {k}"}


def excluded_value(m: Matrix, pos: tuple[int, int]) -> Fraction | None:
    """The parameter value a making det = 0 when a sits at pos; None if det does not depend on a."""
    i, j = pos
    minor = det([r[:j] + r[j + 1:] for k, r in enumerate(m) if k != i])
    slope = ((-1) ** (i + j)) * minor
    if slope == 0:
        return None
    base = [row[:] for row in m]
    base[i][j] = Fraction(0)
    return -det(base) / slope


def _term(coef, var: str, first: bool) -> str:
    if isinstance(coef, str):
        return (coef if first else f"+ {coef}") + var
    coef = int(coef)
    if coef == 0:
        return ""
    sign = "-" if coef < 0 else ("" if first else "+")
    mag = "" if abs(coef) == 1 else str(abs(coef))
    return f"{sign} {mag}{var}".strip() if not first else f"{sign}{mag}{var}"


def system_tex(m, rhs) -> str:
    """Rows of a 3-variable system joined by commas; a string coefficient is a parameter."""
    lines = []
    for row, r in zip(m, rhs):
        parts, first = [], True
        for coef, var in zip(row, ("x", "y", "z")):
            t = _term(coef, var, first)
            if t:
                parts.append(t)
                first = False
        lines.append(" ".join(parts) + f" = {r}")
    return r",\quad ".join(lines)


def _except(r: Fraction) -> str:
    return rf"(-\infty, {frac_tex(r)}) \cup ({frac_tex(r)}, \infty)"


def solve_left(a: Matrix, c: Matrix) -> Matrix:
    """X with AX = C."""
    return matmul(inverse(a), c)


def solve_from_transpose_identity(b: Matrix, k: int, w: Matrix) -> Matrix:
    """v with Av = w when ABᵗ = kI: A⁻¹ = Bᵗ/k."""
    return [[x / k for x in row] for row in matmul(transpose(b), w)]


#: (statement TeX, true whenever A and B are square with AB = I).
AB_IDENTITY_FACTS = (
    ("BA = I", True), (r"A^{-1} = B", True), (r"B^{-1} = A", True), (r"(A^{t})^{-1} = B^{t}", True),
    (r"B^{t}A^{t} = I", True), (r"A^{t}B^{t} = I", True), (r"\det(A)\det(B) = 1", True), (r"A^{2}B^{2} = I", True),
    ("A = B", False), (r"\det(A) = \det(B)", False), ("A + B = 2I", False), (r"A^{2} = B^{2}", False),
    (r"A^{t} = B", False),
)


#: Integer 2 × 2 matrices whose powers cycle back to I, with the cycle length:
#: rotations by 180°, 90°, 120° and 60° written in an integer basis, and a reflection.
CYCLIC = (
    ([[0, -1], [1, 0]], 4), ([[0, 1], [-1, 0]], 4), ([[-1, -1], [1, 0]], 3), ([[0, -1], [1, -1]], 3),
    ([[1, -1], [1, 0]], 6), ([[0, 1], [-1, 1]], 6), ([[0, 1], [1, 0]], 2), ([[-1, 0], [0, -1]], 2),
)


def mat_pow(a: Matrix, n: int) -> Matrix:
    out = mat([[1, 0], [0, 1]])
    for _ in range(n):
        out = matmul(out, a)
    return out


def cycle_length(a: Matrix, limit: int = 12) -> int:
    """Smallest k ≥ 1 with Aᵏ = I."""
    p = a
    for k in range(1, limit + 1):
        if p == mat([[1, 0], [0, 1]]):
            return k
        p = matmul(p, a)
    raise ValueError("no cycle")


def identity_powers(a: Matrix, n: int) -> int:
    """How many k in 1..n give Aᵏ = I: the multiples of the cycle length."""
    return n // cycle_length(a)


def _term_math_m5(k: int, var: str, first: bool = False) -> str:
    """3, 'y' -> '+ 3y'; -1, 'y' -> '- y'."""
    mag = "" if abs(k) == 1 else str(abs(k))
    if first:
        return f"{'-' if k < 0 else ''}{mag}{var}"
    return f"{'-' if k < 0 else '+'} {mag}{var}"


def _frac_mat(m) -> str:
    rows = r" \\ ".join(" & ".join(frac_tex(Fraction(x)) for x in row) for row in m)
    return rf"\begin{{pmatrix}} {rows} \end{{pmatrix}}"


@question_type("math.matrix_add_scalar", display_name={"th": "บวกและคูณเมทริกซ์ด้วยสเกลาร์"},
               level={"th": "ม.5"}, topic="เมทริกซ์")
class MatrixAddScalar(MathType):
    def expr(self, rng: Random, entry_hi: int = 9, scalar_hi: int = 4):
        a = [[rng.randint(-entry_hi, entry_hi) for _ in range(2)] for _ in range(2)]
        b = [[rng.randint(-entry_hi, entry_hi) for _ in range(2)] for _ in range(2)]
        k = rng.randint(2, scalar_hi)

        def mat(m):
            return (rf"\begin{{pmatrix}} {m[0][0]} & {m[0][1]} \\ "
                    rf"{m[1][0]} & {m[1][1]} \end{{pmatrix}}")

        res = [[a[i][j] + k * b[i][j] for j in range(2)] for i in range(2)]
        wrong1 = [[a[i][j] + b[i][j] for j in range(2)] for i in range(2)]
        wrong2 = [[k * (a[i][j] + b[i][j]) for j in range(2)] for i in range(2)]
        wrong3 = [[a[i][j] - k * b[i][j] for j in range(2)] for i in range(2)]
        return MathDraw(
            rf"A = {mat(a)}, \; B = {mat(b)}", mat(res),
            prompt=f"จงหา A + {k}B",
            distractors=[mat(wrong1), mat(wrong2), mat(wrong3)])
MatrixAddScalar.PROVENANCE = Provenance("original")


@question_type("math.matrix_transpose_m5", display_name={"th": "เมทริกซ์สลับเปลี่ยน"},
               level=M5_math_gaps_indicators, topic="เมทริกซ์")
class MatrixTransposeM5(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rows, cols = rng.choice(((2, 3), (3, 2), (2, 2), (3, 3)))
        while True:
            m = [[rng.randint(-9, 9) for _ in range(cols)] for _ in range(rows)]
            t = [list(col) for col in zip(*m)]
            if t != m and len({x for row in m for x in row}) == rows * cols:
                break
        wrongs = [
            # Each row reversed instead of turned into a column.
            [row[::-1] for row in m],
            # The rows read upwards.
            [list(col)[::-1] for col in zip(*m)],
            # The matrix upside down.
            m[::-1],
            m,
        ]
        return maths([text("กำหนดให้"), content_math(f"A = {_mat(m)}"), text("จงหา"), content_math("A^{t}")],
                     _mat(t), [_mat(w) for w in wrongs if w != t], self.topic)
MatrixTransposeM5.PROVENANCE = Provenance("original")


@question_type("math.determinant_2x2",
               display_name={"th": "ดีเทอร์มิแนนต์ 2×2"}, level={"th": "ม.5"},
               topic="เมทริกซ์")
class Determinant2x2(MathType):
    def expr(self, rng: Random):
        a, b, c, d = (rng.randint(-6, 6) for _ in range(4))
        tex = rf"\begin{{vmatrix}} {a} & {b} \\ {c} & {d} \end{{vmatrix}}"
        return MathDraw(tex, str(a * d - b * c),
                        distractors=[str(a * c - b * d), str(a * b - c * d),
                                     str(a * d + b * c)])
Determinant2x2.PROVENANCE = Provenance("original")


@question_type("math.matrix_multiply_2x2", display_name={"th": "คูณเมทริกซ์ 2×2"},
               level={"th": "ม.5"}, topic="เมทริกซ์")
class MatrixMultiply2x2(MathType):
    def expr(self, rng: Random, entry_hi: int = 6):
        a = [[rng.randint(-entry_hi, entry_hi) for _ in range(2)] for _ in range(2)]
        b = [[rng.randint(-entry_hi, entry_hi) for _ in range(2)] for _ in range(2)]

        def mat(m):
            return (rf"\begin{{pmatrix}} {m[0][0]} & {m[0][1]} \\ "
                    rf"{m[1][0]} & {m[1][1]} \end{{pmatrix}}")

        prod = [[a[i][0] * b[0][j] + a[i][1] * b[1][j] for j in range(2)]
                for i in range(2)]
        # Multiplying entrywise is the mistake this item exists to catch.
        entrywise = [[a[i][j] * b[i][j] for j in range(2)] for i in range(2)]
        swapped = [[b[i][0] * a[0][j] + b[i][1] * a[1][j] for j in range(2)]
                   for i in range(2)]
        return MathDraw(
            rf"A = {mat(a)}, \; B = {mat(b)}", mat(prod), prompt="จงหา AB",
            distractors=[mat(entrywise), mat(swapped),
                         mat([[prod[0][0], prod[1][0]], [prod[0][1], prod[1][1]]])])
MatrixMultiply2x2.PROVENANCE = Provenance("original")


@question_type("math.determinant_properties_m5",
               display_name={"th": "สมบัติของดีเทอร์มิแนนต์"},
               level=M5, topic=TOPIC)
class DeterminantPropertiesM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        if kind == 0:
            n = rng.choice((2, 3))
            d = Fraction(rng.choice((-6, -4, -3, 2, 3, 4, 5, 6, 10)))
            op = rng.choice(("swap", "add", "scale"))
            k = rng.choice((2, 3, -2))
            c = rng.choice((Fraction(2), Fraction(3), Fraction(1, 2), Fraction(1, 5), Fraction(-1)))
            target = rng.choice(("plain", "transpose", "inverse"))
            right = det_after(n, d, op, k, c, target)
            inner = {"plain": f"{frac_tex(c) if c != -1 else '-'}B",
                     "transpose": f"{frac_tex(c) if c != -1 else '-'}B^{{t}}",
                     "inverse": rf"\left({frac_tex(c) if c != -1 else '-'}B\right)^{{-1}}"}[target]
            stem = [text(f"กำหนดให้ A เป็นเมทริกซ์มิติ {n} × {n} ซึ่ง"), content_math(rf"\det(A) = {frac_tex(d)}"),
                    text(f"ถ้า B เป็นเมทริกซ์ที่ได้จากการ{_OPS_TH[op].format(k=k)} แล้ว"),
                    content_math(rf"\det\left({inner}\right)"), text("เท่ากับเท่าใด")]
            # c instead of cⁿ; the row operation ignored; the reciprocal (or not).
            flip = (lambda v: 1 / v) if target == "inverse" else (lambda v: v)
            b = {"swap": -d, "scale": k * d, "add": d}[op]
            named = [flip(c * b), flip(c ** n * d), 1 / right, flip(c ** n * (-b))]
            return _frac_q(stem, right, named, self.topic)
        if kind == 1:
            n, k = rng.choice((2, 3)), rng.choice((2, 3))
            d = Fraction(rng.choice((-4, -3, -2, 2, 3, 4, 5)))
            v = Fraction(k) ** n * d
            right = det_inverse_from_scaled(n, k, v)
            stem = [text(f"ถ้า A เป็นเมทริกซ์มิติ {n} × {n} ซึ่ง"), content_math(rf"\det({k}A) = {frac_tex(v)}"),
                    text("แล้ว"), content_math(r"\det\left(A^{-1}\right)"), text("เท่ากับเท่าใด")]
            # k instead of kⁿ; det A itself; 1/det(kA).
            return _frac_q(stem, right, [Fraction(k) / v, d, 1 / v], self.topic)
        if kind == 2:
            while True:
                a = mat([[rng.randint(-4, 6) for _ in range(2)] for _ in range(2)])
                b = mat([[rng.randint(-4, 6) for _ in range(2)] for _ in range(2)])
                if det(a) and det(b) and abs(det(a)) != abs(det(b)):
                    break
            form = rng.choice(("AB^{-1}", "A^{-1}B", "A^{t}B", "2AB^{-1}"))
            da, db = det(a), det(b)
            right = {"AB^{-1}": da / db, "A^{-1}B": db / da, "A^{t}B": da * db, "2AB^{-1}": 4 * da / db}[form]
            stem = [text("ถ้า"), content_math(rf"A = {mat_tex(a)}"), text("และ"), content_math(rf"B = {mat_tex(b)}"),
                    text("แล้ว"), content_math(rf"\det\left({form}\right)"), text("เท่ากับเท่าใด")]
            # The quotient the other way; the product; 2 instead of 2² for the scaled form.
            named = [db / da if form != "A^{-1}B" else da / db, da * db if form != "A^{t}B" else da / db,
                     2 * da / db, da - db]
            return _frac_q(stem, right, named, self.topic)
        while True:
            a12, b22 = rng.randint(-3, 3), rng.choice((1, 2, 3, -2, 5))
            c11, e22 = rng.choice((-2, 1, 2, 3, -1)), rng.choice((1, 2, -1, 3))
            x = rng.choice([v for v in range(-6, 10) if v])
            v = Fraction(b22 * x, c11 * e22)
            if v.denominator == 1 and unknown_from_quotient(a12, b22, c11, e22, v) == x:
                break
        stem = [text("ให้"), content_math(rf"A = {mat_tex([[ 'x', a12], [0, b22]])}"), text("และ"),
                content_math(rf"B = {mat_tex([[c11, 0], ['x', e22]])}"),
                text("เมื่อ x เป็นจำนวนจริง ถ้า"), content_math(rf"\det\left(B^{{-1}}A\right) = {frac_tex(v)}"),
                text("แล้ว x เท่ากับเท่าใด")]
        # det A · det B taken for the quotient; det B / det A; the sign of det B lost.
        named = [v / (b22 * c11 * e22), Fraction(c11 * e22, b22) / v, -x]
        return _frac_q(stem, Fraction(x), named, self.topic)
DeterminantPropertiesM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/9 เมทริกซ์',))


@question_type("math.matrix_system_word_m5",
               display_name={"th": "โจทย์ปัญหาระบบสมการสองตัวแปร (แก้ด้วยเมทริกซ์)"},
               level=M5_math_apply_add, topic="เมทริกซ์")
class MatrixSystemWordM5(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(5)
        if kind == 0:
            x, y = rng.randint(8, 20) * 10, rng.randint(3, 9) * 10     # adult, child price
            a1, c1, a2, c2 = _independent(rng, 2, 9)
            n1, n2 = rng.randint(2, 5), rng.randint(2, 5)
            return MathDraw("", _c(n1 * x + n2 * y),
                            prompt=(f"วันแรกขายบัตรผู้ใหญ่ {a1} ใบ บัตรเด็ก {c1} ใบ ได้เงิน {_c(a1 * x + c1 * y)} บาท "
                                    f"วันที่สองขายบัตรผู้ใหญ่ {a2} ใบ บัตรเด็ก {c2} ใบ ได้เงิน {_c(a2 * x + c2 * y)} บาท "
                                    f"ครอบครัวที่มีผู้ใหญ่ {n1} คน และเด็ก {n2} คน ต้องจ่ายค่าบัตรกี่บาท"),
                            distractors=[_c(n1 * y + n2 * x), _c((n1 + n2) * x), _c(x + y)])
        if kind == 1:
            x, y = rng.randint(15, 45), rng.randint(5, 14)             # notebook, pen
            a1, c1, a2, c2 = _independent(rng, 1, 6)
            return MathDraw("", str(x),
                            prompt=(f"ซื้อสมุด {a1} เล่มกับปากกา {c1} ด้าม จ่าย {a1 * x + c1 * y} บาท "
                                    f"ซื้อสมุด {a2} เล่มกับปากกา {c2} ด้าม จ่าย {a2 * x + c2 * y} บาท "
                                    f"สมุดราคาเล่มละกี่บาท"),
                            distractors=_story.keep(y, x + y, x - y, answer=x, lo=1))
        if kind == 2:
            fives, tens = rng.randint(6, 30), rng.randint(6, 30)
            return MathDraw("", str(tens),
                            prompt=(f"กระปุกออมสินมีเหรียญห้าบาทและเหรียญสิบบาทรวม {fives + tens} เหรียญ "
                                    f"คิดเป็นเงิน {5 * fives + 10 * tens} บาท มีเหรียญสิบบาทกี่เหรียญ"),
                            distractors=_story.keep(fives, (5 * fives + 10 * tens) // 10, tens + 5,
                                                    answer=tens, lo=1))
        if kind == 3:
            chickens, cows = rng.randint(10, 60), rng.randint(5, 40)
            return MathDraw("", str(cows),
                            prompt=(f"ฟาร์มแห่งหนึ่งมีไก่และวัวรวมกัน {chickens + cows} ตัว นับขาได้ "
                                    f"{2 * chickens + 4 * cows} ขา ฟาร์มนี้มีวัวกี่ตัว"),
                            distractors=_story.keep(chickens, (2 * chickens + 4 * cows) // 4, cows * 2,
                                                    answer=cows, lo=1))
        x, y = rng.randint(4, 12) * 10, rng.randint(2, 8) * 10          # mango, orange per kg
        a1, c1, a2, c2 = _independent(rng, 1, 5)
        gap = x - y
        return MathDraw("", str(abs(gap)),
                        prompt=(f"ซื้อมะม่วง {a1} กิโลกรัมกับส้ม {c1} กิโลกรัม จ่าย {a1 * x + c1 * y} บาท "
                                f"ซื้อมะม่วง {a2} กิโลกรัมกับส้ม {c2} กิโลกรัม จ่าย {a2 * x + c2 * y} บาท "
                                f"มะม่วงกับส้มราคากิโลกรัมละต่างกันกี่บาท"),
                        distractors=_story.keep(x, y, x + y, answer=abs(gap), lo=1))
MatrixSystemWordM5.PROVENANCE = Provenance("original")


@question_type("math.matrix_unique_solution_m5",
               display_name={"th": "ค่าพารามิเตอร์ที่ทำให้ระบบสมการมีคำตอบเดียว"},
               level=M5, topic=TOPIC)
class MatrixUniqueSolutionM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            m = mat([[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)])
            pos = (rng.randrange(3), rng.randrange(3))
            r = excluded_value(m, pos)
            # Every equation keeps at least two variables (the parameter counts as one).
            full = all(sum(bool(v) or (i, j) == pos for j, v in enumerate(row)) >= 2 for i, row in enumerate(m))
            if r is not None and r.denominator == 1 and abs(r) <= 8 and full:
                break
        rows = [[("a" if (i, j) == pos else v) for j, v in enumerate(row)] for i, row in enumerate(m)]
        rhs = [rng.randint(-3, 4) for _ in range(3)]
        stem = [text("ระบบสมการ"), content_math(system_tex(rows, rhs))]
        # The excluded value's sign flipped; the minor's sign (the cofactor sign) forgotten.
        i, j = pos
        base = [row[:] for row in m]
        base[i][j] = Fraction(0)
        minor = det([r_[:j] + r_[j + 1:] for k, r_ in enumerate(m) if k != i])
        unsigned = -det(base) / minor
        others = [v for v in (-r, unsigned, r + 1, r - 1, r + 2) if v != r]
        if rng.random() < 0.5:
            stem.append(text("มีคำตอบเพียงคำตอบเดียวเมื่อ a อยู่ในเซตใด"))
            wrongs = [_except(v) for v in others[:2]] + [rf"\{{{frac_tex(r)}\}}"] + [_except(v) for v in others[2:]]
            return _tex_q(stem, _except(r), wrongs, self.topic)
        stem.append(text("ไม่มีคำตอบเพียงคำตอบเดียว (ไม่มีคำตอบหรือมีคำตอบมากมาย) เมื่อ a เท่ากับเท่าใด"))
        return _frac_q(stem, r, others, self.topic)
MatrixUniqueSolutionM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/9 เมทริกซ์',))


@question_type("math.matrix_equation_m5",
               display_name={"th": "แก้สมการเมทริกซ์ด้วยอินเวอร์ส"},
               level=M5, topic=TOPIC)
class MatrixEquationM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        if kind == 0:
            a = _unimodular(rng, 2)
            x = mat([[rng.randint(-5, 7) for _ in range(2)] for _ in range(2)])
            c = matmul(a, x)
            weights = [rng.choice((1, 1, 2, -1)) for _ in range(4)]
            combo = lambda m: sum(w * v for w, v in zip(weights, (m[0][0], m[0][1], m[1][0], m[1][1])))
            expr = " ".join(_term(w, v, i == 0) for i, (w, v) in enumerate(zip(weights, "abcd")))
            stem = [text("จากสมการ"), content_math(rf"{mat_tex(a)} \begin{{pmatrix}} a & b \\ c & d \end{{pmatrix}} = "
                                                    rf"{mat_tex(c)}"),
                    text("ค่าของ"), content_math(expr), text("เท่ากับเท่าใด")]
            # Multiplying A⁻¹ on the right; multiplying by A instead of A⁻¹; the plain sum.
            wrong_x = matmul(c, inverse(a))
            named = [combo(wrong_x), combo(matmul(a, c)), sum(v for row in x for v in row)]
            return _frac_q(stem, combo(x), named, self.topic)
        if kind == 1:
            n = 3
            b = _unimodular(rng, n)
            k = rng.choice((1, 2, 3))
            w = mat([[rng.randint(-4, 5)] for _ in range(n)])
            v = solve_from_transpose_identity(b, k, w)
            idx = rng.randrange(n)
            name = "xyz"[idx]
            stem = [text("กำหนดให้ I เป็นเมทริกซ์เอกลักษณ์มิติ 3 × 3 และ"), content_math(rf"B = {mat_tex(b)}"),
                    text("ถ้า A เป็นเมทริกซ์มิติ 3 × 3 ซึ่ง"),
                    content_math(rf"AB^{{t}} = {'' if k == 1 else k}I"), text("และ"),
                    content_math(rf"A\begin{{pmatrix}} x \\ y \\ z \end{{pmatrix}} = {mat_tex(w)}"),
                    text(f"แล้ว {name} เท่ากับเท่าใด")]
            # B instead of Bᵗ; forgetting to divide by k; multiplying by k.
            no_t = [[x_ / k for x_ in row] for row in matmul(b, w)]
            named = [no_t[idx][0], v[idx][0] * k, v[idx][0] * k * k, v[(idx + 1) % n][0]]
            return _frac_q(stem, v[idx][0], named, self.topic)
        if kind == 2:
            p = _unimodular(rng, 3)
            w = mat([[rng.randint(-4, 5)] for _ in range(3)])
            v = matmul(p, w)
            idx = rng.randrange(3)
            name = "abc"[idx]
            stem = [text("กำหนดให้ A เป็นเมทริกซ์มิติ 3 × 3 ซึ่ง"), content_math(r"[A : I] \sim [I : P]"),
                    text("โดยที่ I เป็นเมทริกซ์เอกลักษณ์ และ"), content_math(rf"P = {mat_tex(p)}"), text("ถ้า"),
                    content_math(rf"A\begin{{pmatrix}} a \\ b \\ c \end{{pmatrix}} = {mat_tex(w)}"),
                    text(f"แล้ว {name} เท่ากับเท่าใด")]
            # Using Pᵗ; using A = P (so solving P v = w); the next entry.
            named = [matmul(transpose(p), w)[idx][0], solve_left(p, w)[idx][0], v[(idx + 1) % 3][0]]
            return _frac_q(stem, v[idx][0], named, self.topic)
        picks = rng.sample(AB_IDENTITY_FACTS, 4)
        right = sum(t for _, t in picks)
        labels = ("ก.", "ข.", "ค.", "ง.")
        stem = [text("ให้ A และ B เป็นเมทริกซ์จัตุรัสมิติเดียวกัน และ I เป็นเมทริกซ์เอกลักษณ์ ถ้า"),
                content_math("AB = I"), text("พิจารณาข้อความต่อไปนี้")]
        for lab, (tex, _) in zip(labels, picks):
            stem += [text(lab), content_math(tex)]
        stem.append(text("จำนวนข้อความที่ถูกต้องเท่ากับเท่าใด"))
        wrongs = [str(v) for v in sorted(range(5), key=lambda v: abs(v - right)) if v != right]
        return _tex_q(stem, str(right), wrongs, self.topic)
MatrixEquationM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/9 เมทริกซ์',))


@question_type("math.matrix_power_cycle_m5",
               display_name={"th": "เมทริกซ์ยกกำลังที่วนกลับเป็นเมทริกซ์เอกลักษณ์"},
               level=M5, topic=TOPIC)
class MatrixPowerCycleM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        rows, k = rng.choice(CYCLIC)
        a = mat(rows)
        if rng.random() < 0.5:
            n = rng.randint(50, 200)
            right = identity_powers(a, n)
            stem = [text("กำหนดให้"), content_math(rf"A = {mat_tex(a)}"),
                    text(f"จำนวนเต็มบวก k ที่ไม่เกิน {n} ซึ่งทำให้"), content_math("A^{k} = I"), text("มีกี่จำนวน")]
            # Half the cycle (A^(k/2) = −I read as I); one cycle too many; ceiling.
            wrongs = [n // max(1, k // 2), n // (k + 1), -(-n // k), right + 1, right - 1]
            return _tex_q(stem, str(right), [str(w) for w in wrongs if w >= 0], self.topic)
        rows, k = rng.choice([c for c in CYCLIC if c[1] >= 3])      # a 2-cycle has too few distinct powers
        a = mat(rows)
        n = rng.randint(20, 120)
        right = mat_pow(a, n)
        stem = [text("กำหนดให้"), content_math(rf"A = {mat_tex(a)}"), text("แล้ว"),
                content_math(f"A^{{{n}}}"), text("เท่ากับข้อใด")]
        # One power off either way; I whatever the remainder; the remainder taken mod 4.
        wrongs = [mat_pow(a, n % k + 1), mat_pow(a, (n - 1) % k), mat([[1, 0], [0, 1]]), mat_pow(a, n % 4),
                  mat_pow(a, (n + 2) % k), [[-v for v in r] for r in right]]
        return _tex_q(stem, mat_tex(right), [mat_tex(w) for w in wrongs], self.topic)
MatrixPowerCycleM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/9 เมทริกซ์',))


@question_type("math.matrix_row_operations_m5", display_name={"th": "แก้ระบบสมการด้วยการดำเนินการตามแถว"},
               level=M5_math_gaps_indicators, topic="เมทริกซ์")
class MatrixRowOperationsM5(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        x, y = rng.randint(-6, 6), rng.randint(-6, 6)
        a1, b1 = _nz(rng, 1, 3), _nz(rng, -5, 5)
        k = _nz(rng, -3, 3)
        b2 = _nz(rng, -5, 5)
        while b2 == k * b1:
            b2 = _nz(rng, -5, 5)
        a2 = k * a1
        c1, c2 = a1 * x + b1 * y, a2 * x + b2 * y
        aug = [[a1, b1, c1], [a2, b2, c2]]
        new = [0, b2 - k * b1, c2 - k * c1]
        if rng.random() < 0.5:
            times = "" if abs(k) == 1 else str(abs(k))
            op = rf"R_{{2}} {'-' if k > 0 else '+'} {times}R_{{1}}"
            stem = [text("เมทริกซ์แต่งเติมของระบบสมการคือ"), content_math(_mat(aug)),
                    text("หลังดำเนินการตามแถว"), content_math(rf"{op} \to R_{{2}}"), text("แถวที่ 2 เป็นข้อใด")]
            # Adding instead of subtracting; the right-hand column left alone;
            # the operation done the other way round.
            wrongs = [[a2 + k * a1, b2 + k * b1, c2 + k * c1], [0, b2 - k * b1, c2],
                      [0, k * b1 - b2, k * c1 - c2], [0, b2 - k * b1, c2 - c1],
                      [0, b2 - k * b1 + 1, c2 - k * c1], [0, b2 - b1, c2 - c1 - 1]]
            fmt = lambda v: rf"\begin{{pmatrix}} {v[0]} & {v[1]} & {v[2]} \end{{pmatrix}}"  # noqa: E731
            return maths(stem, fmt(new), [fmt(w) for w in wrongs if w != new], self.topic)
        # Back substitution from the reduced matrix.
        reduced = [[a1, b1, c1], new]
        stem = [text("หลังดำเนินการตามแถว เมทริกซ์แต่งเติมของระบบสมการในตัวแปร x และ y เป็น"),
                content_math(_mat(reduced)), text("จงหาค่าของ x")]
        return maths(stem, str(x), [str(y), str(-x), str(c1 - b1 * y), str(c1)], self.topic)
MatrixRowOperationsM5.PROVENANCE = Provenance("original")


@question_type("math.matrix_inverse_m5", display_name={"th": "อินเวอร์สการคูณของเมทริกซ์ 2×2"},
               level=M5_math_m5, topic="เมทริกซ์")
class MatrixInverseM5(QuestionType):
    break_convergence = True  # one-part slips cluster round the answer
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            a, b, c, d = (rng.randint(-6, 6) for _ in range(4))
            det = a * d - b * c
            # Every entry non-zero: a matrix with zeros makes several of the
            # swap-and-negate mistakes coincide.
            # A matrix that is its own inverse would make "the matrix itself"
            # the right answer.
            if (det in (1, -1, 2, -2, 3, 4, 5) and a and b and c and d
                    and not (det == -1 and a == -d)):
                break
        inv = [[Fraction(d, det), Fraction(-b, det)], [Fraction(-c, det), Fraction(a, det)]]
        # Swapping without negating, negating without swapping, forgetting 1/det.
        wrongs = [[[Fraction(d, det), Fraction(b, det)], [Fraction(c, det), Fraction(a, det)]],
                  [[Fraction(a, det), Fraction(-b, det)], [Fraction(-c, det), Fraction(d, det)]],
                  [[d, -b], [-c, a]], [[Fraction(-d, det), Fraction(b, det)], [Fraction(c, det), Fraction(-a, det)]],
                  # The transpose of the inverse, and the matrix itself.
                  [[Fraction(d, det), Fraction(-c, det)], [Fraction(-b, det), Fraction(a, det)]],
                  [[a, b], [c, d]], [[2 * x for x in row] for row in inv]]
        return _maths([text("จงหาอินเวอร์สการคูณของเมทริกซ์"), content_math(_mat([[a, b], [c, d]]))],
                      _frac_mat(inv), [_frac_mat(w) for w in wrongs], self.topic)
MatrixInverseM5.PROVENANCE = Provenance("original")


@question_type("math.determinant_3x3_m5", display_name={"th": "ดีเทอร์มิแนนต์ของเมทริกซ์ 3×3"},
               level=M5_math_m5, topic="เมทริกซ์")
class Determinant3x3M5(MathType):
    def expr(self, rng: Random):
        m = [[rng.randint(-4, 5) for _ in range(3)] for _ in range(3)]
        (a, b, c), (d, e, f), (g, h, i) = m
        det = a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)
        # The middle cofactor's sign lost, and the main diagonal only.
        slip = a * (e * i - f * h) + b * (d * i - f * g) + c * (d * h - e * g)
        return MathDraw(rf"\det {_mat(m)}", str(det), prompt="จงหาค่า",
                        distractors=_story.keep(slip, a * e * i, -det if det else 1, det + 1,
                                                answer=det, lo=-9999))
Determinant3x3M5.PROVENANCE = Provenance("original")


@question_type("math.cramer_rule_m5", display_name={"th": "แก้ระบบสมการด้วยเมทริกซ์ (กฎของคราเมอร์)"},
               level=M5_math_m5, topic="เมทริกซ์")
class CramerRuleM5(MathType):
    def expr(self, rng: Random):
        while True:
            a, b, c, d = (rng.choice([v for v in range(-5, 6) if v]) for _ in range(4))
            det = a * d - b * c
            if det:
                break
        x, y = rng.randint(-6, 6), rng.randint(-6, 6)
        e, f = a * x + b * y, c * x + d * y
        system = (rf"{_term_math_m5(a, 'x', True)} {_term_math_m5(b, 'y')} = {e},\quad "
                  rf"{_term_math_m5(c, 'x', True)} {_term_math_m5(d, 'y')} = {f}")
        return MathDraw(system, str(x), prompt="จงหาค่า x จากระบบสมการ",
                        # y in place of x, and D_x left undivided.
                        distractors=_story.keep(y, (e * d - b * f), -x, x + 1, answer=x, lo=-9999))
CramerRuleM5.PROVENANCE = Provenance("original")
