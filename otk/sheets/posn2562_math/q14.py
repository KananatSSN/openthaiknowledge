"""ข้อ 14 — ค่าของ a − 7b − 2c

ให้ a, b, c เป็นจำนวนจริงที่ยังไม่ทราบค่า และ p(x) = ax² + bx + c
ถ้า (p(x))³ − x มี x³ − 13x² + 44x − 32 เป็นตัวประกอบ แล้ว a − 7b − 2c มีค่าเท่าใด

The cubic factors as ``(x − 1)(x − 4)(x − 8)``, so at each of its roots

    (p(r))³ = r   ⟹   p(r) = ∛r     (p is real, so the real cube root)

which pins the quadratic through three points:

    p(1) = 1,   p(4) = ∛4,   p(8) = 2

Everything lives in ℚ(∛2): with t = ∛2 the values are 1, t² and t³ = 2, and
solving the Vandermonde system exactly gives

    a = (10 − 7t²)/84,   b = (21t² − 26)/28,   c = (38 − 14t²)/21

so ``a − 7b − 2c = 3 − 4t² =`` **3 − 4∛4 ≈ −3.3496**.

That the answer is irrational is not a transcription error — the coefficient
combination was checked against the page at 420 dpi. The t² parts do *not*
cancel: they contribute ``−1/12 − 21/4 + 4/3 = −4``. (A combination that does
cancel them is ``a + b + c``, which is just p(1) = 1.) The sheet is comfortable
with surd answers — q6, q15, q18 and q19 all have them.

Reading ``(p(x))³`` as the threefold composition instead gives an *ambiguous*
question — the 3-cycle 1→4→8→1 gives −27 and the reverse cycle gives 8 — which
is further evidence that the cube of the value is meant.

``solve`` does exact linear algebra in ℚ[t]/(t³ − 2). ``check`` interpolates
numerically by Lagrange, then **expands (p(x))³ − x to degree six and divides it
by the printed cubic**, refusing to answer unless the remainder really vanishes.
"""

from __future__ import annotations

from fractions import Fraction

#: roots of the printed cubic, and the combination asked for.
PARAMS = {"roots": (1, 4, 8), "combo": (1, -7, -2)}
ANSWER = -3.3496042078727974
TOL = 1e-9
VARIANTS = [
    {"roots": (1, 4, 8), "combo": (1, 1, 1)},        # p(1) = 1 exactly
    {"roots": (1, 2, 8), "combo": (1, -7, -2)},
    {"roots": (1, 8, 64), "combo": (1, -7, -2)},     # every root a perfect cube
    {"roots": (1, 4, 8), "combo": (0, 1, 0)},
    {"roots": (2, 4, 8), "combo": (1, -7, -2)},
    {"roots": (1, 4, 4), "combo": (1, -7, -2)},      # a repeated root
    {"roots": (1, 3, 8), "combo": (1, -7, -2)},      # ∛3 is not in ℚ(∛2)
]
#: the cubic field everything is expressed in.
BASE = 2


def _mul(x, y):
    """Multiply in ℚ[t]/(t³ − BASE): (c₀, c₁, c₂) means c₀ + c₁t + c₂t²."""
    out = [Fraction(0)] * 5
    for i, u in enumerate(x):
        for j, v in enumerate(y):
            out[i + j] += u * v
    out[0] += BASE * out[3]
    out[1] += BASE * out[4]
    return tuple(out[:3])


def _cube_root(value: int):
    """value^{1/3} as an element of ℚ[t]/(t³ − 2), or None if it is not one."""
    if value <= 0:
        return None
    for power in range(0, 3):                     # value = q³ · 2^power
        scaled = Fraction(value, BASE ** power)
        if scaled.denominator != 1:
            continue
        whole = scaled.numerator
        root = round(whole ** (1 / 3))
        for cand in (root - 1, root, root + 1):
            if cand > 0 and cand ** 3 == whole:
                out = [Fraction(0)] * 3
                out[power] = Fraction(cand)
                return tuple(out)
    return None


def coefficients(roots=(1, 4, 8)):
    """(a, b, c) as elements of ℚ[t]/(t³ − 2), or None."""
    if len(set(roots)) != 3:
        return None
    values = [_cube_root(r) for r in roots]
    if any(v is None for v in values):
        return None
    # Vandermonde system, solved by elimination over the ring's coefficients:
    # each unknown is a triple, and the matrix is rational, so the three
    # components decouple into three independent 3×3 rational solves.
    matrix = [[Fraction(r * r), Fraction(r), Fraction(1)] for r in roots]
    out = []
    for component in range(3):
        rows = [row[:] + [values[i][component]] for i, row in enumerate(matrix)]
        for col in range(3):
            pivot = next((r for r in range(col, 3) if rows[r][col] != 0), None)
            if pivot is None:
                return None
            rows[col], rows[pivot] = rows[pivot], rows[col]
            head = rows[col][col]
            rows[col] = [x / head for x in rows[col]]
            for r in range(3):
                if r != col and rows[r][col] != 0:
                    factor = rows[r][col]
                    rows[r] = [x - factor * y for x, y in zip(rows[r], rows[col])]
        out.append([rows[r][3] for r in range(3)])
    # out[component][unknown] → regroup into (a, b, c), each a ring element
    return tuple(tuple(out[k][i] for k in range(3)) for i in range(3))


def solve(roots=(1, 4, 8), combo=(1, -7, -2)):
    """The requested combination of a, b and c, as a real number."""
    got = coefficients(roots)
    if got is None:
        return None
    total = [Fraction(0)] * 3
    for weight, piece in zip(combo, got):
        for k in range(3):
            total[k] += weight * piece[k]
    root = BASE ** (1 / 3)
    return float(total[0]) + float(total[1]) * root + float(total[2]) * root * root


def check(roots=(1, 4, 8), combo=(1, -7, -2)):
    """Independent: interpolate numerically, then divide the sextic by the cubic.

    p is built by Lagrange interpolation through (r, ∛r); ``(p(x))³ − x`` is then
    expanded into its seven coefficients and long-divided by the cubic that the
    roots define. Only if the remainder really is zero — the printed condition,
    tested rather than assumed — is the combination reported.
    """
    if len(set(roots)) != 3:
        return None
    if any(r <= 0 for r in roots):
        return None
    if coefficients(roots) is None:
        return None                       # keep both routes to the same domain

    values = [r ** (1 / 3) for r in roots]
    coefs = [0.0, 0.0, 0.0]               # p(x) = coefs[0]x² + coefs[1]x + coefs[2]
    for i, (xi, yi) in enumerate(zip(roots, values)):
        others = [roots[j] for j in range(3) if j != i]
        denom = (xi - others[0]) * (xi - others[1])
        # (x − o₀)(x − o₁) = x² − (o₀+o₁)x + o₀o₁
        scale = yi / denom
        coefs[0] += scale
        coefs[1] += -scale * (others[0] + others[1])
        coefs[2] += scale * others[0] * others[1]

    def poly_mul(u, v):
        out = [0.0] * (len(u) + len(v) - 1)
        for i, x in enumerate(u):
            for j, y in enumerate(v):
                out[i + j] += x * y
        return out

    cube = poly_mul(poly_mul(coefs, coefs), coefs)      # degree 6, high power first
    cube[-2] -= 1.0                                     # subtract x

    divisor = [1.0,
               -float(sum(roots)),
               float(roots[0] * roots[1] + roots[1] * roots[2]
                     + roots[0] * roots[2]),
               -float(roots[0] * roots[1] * roots[2])]
    work = list(cube)
    for i in range(len(work) - len(divisor) + 1):
        factor = work[i] / divisor[0]
        for j, d in enumerate(divisor):
            work[i + j] -= factor * d
    scale = max(abs(x) for x in cube) or 1.0
    if max(abs(x) for x in work[-(len(divisor) - 1):]) > 1e-6 * scale:
        return None                                     # not actually a factor

    return sum(w * coef for w, coef in zip(combo, coefs))
