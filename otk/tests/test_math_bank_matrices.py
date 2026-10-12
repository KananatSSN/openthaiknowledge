"""The matrix sets built from the sheet bank's knowledge units.

The exact-arithmetic helpers and every solver are checked against SymPy
matrices; the AB = I statement bank is checked on random invertible pairs;
the source exams' answers are pinned.
"""

from __future__ import annotations

import random
from fractions import Fraction

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m5 import matrices as mm

sympy = pytest.importorskip("sympy")
KEYS = ("math.determinant_properties_m5", "math.matrix_unique_solution_m5", "math.matrix_equation_m5",
        "math.matrix_power_cycle_m5")


def S(m):
    return sympy.Matrix([[sympy.Rational(v.numerator, v.denominator) for v in row] for row in m])


def R(v):
    v = Fraction(v)
    return sympy.Rational(v.numerator, v.denominator)


def _random(rng, n):
    while True:
        m = mm.mat([[rng.randint(-5, 5) for _ in range(n)] for _ in range(n)])
        if mm.det(m):
            return m


def test_arithmetic_matches_sympy():
    rng = random.Random(1)
    for n in (2, 3):
        for _ in range(40):
            a, b = _random(rng, n), _random(rng, n)
            assert R(mm.det(a)) == S(a).det()
            assert S(mm.matmul(a, b)) == S(a) * S(b)
            assert S(mm.inverse(a)) == S(a).inv()
            assert S(mm.transpose(a)) == S(a).T


def test_unimodular():
    rng = random.Random(2)
    for n in (2, 3):
        for _ in range(50):
            assert abs(mm.det(mm._unimodular(rng, n))) == 1


def test_det_after_row_operations():
    rng = random.Random(3)
    for _ in range(60):
        n = rng.choice((2, 3))
        a = _random(rng, n)
        k = rng.choice((2, 3, -2))
        c = rng.choice((Fraction(2), Fraction(1, 5), Fraction(-1)))
        for op in ("swap", "add", "scale"):
            b = S(a)
            if op == "swap":
                b.row_swap(0, 1)
            elif op == "add":
                b[1, :] = b[1, :] + k * b[0, :]
            else:
                b[1, :] = k * b[1, :]
            cb = R(c) * b
            assert R(mm.det_after(n, mm.det(a), op, k, c, "plain")) == cb.det()
            assert R(mm.det_after(n, mm.det(a), op, k, c, "transpose")) == cb.T.det()
            assert R(mm.det_after(n, mm.det(a), op, k, c, "inverse")) == cb.inv().det()


def test_det_inverse_from_scaled_and_unknown():
    x = sympy.Symbol("x")
    for n in (2, 3):
        for k in (2, 3):
            a = S(_random(random.Random(n * k), n))
            assert R(mm.det_inverse_from_scaled(n, k, mm.det(mm.mat(a.tolist())) * k ** n)) == a.inv().det()
    for a12, b22, c11, e22 in ((-1, 3, -2, 1), (2, 5, 3, -1), (0, 2, 1, 2)):
        A = sympy.Matrix([[x, a12], [0, b22]])
        B = sympy.Matrix([[c11, 0], [x, e22]])
        for xv in (-3, 2, 7):
            v = (B.inv() * A).det().subs(x, xv)
            assert mm.unknown_from_quotient(a12, b22, c11, e22, Fraction(str(v))) == xv


def test_excluded_value():
    a = sympy.Symbol("a")
    rng = random.Random(5)
    for _ in range(80):
        m = mm.mat([[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)])
        pos = (rng.randrange(3), rng.randrange(3))
        r = mm.excluded_value(m, pos)
        sm = S(m)
        sm[pos] = a
        roots = sympy.solve(sm.det(), a)
        if r is None:
            assert roots == []
        else:
            assert roots == [R(r)]


def test_matrix_equation_solvers():
    rng = random.Random(6)
    for _ in range(40):
        a = mm._unimodular(rng, 2)
        c = mm.mat([[rng.randint(-5, 5) for _ in range(2)] for _ in range(2)])
        assert S(a) * S(mm.solve_left(a, c)) == S(c)
        b = mm._unimodular(rng, 3)
        k = rng.choice((1, 2, 3))
        w = mm.mat([[rng.randint(-4, 5)] for _ in range(3)])
        A = k * S(b).T.inv()                        # the A with ABᵗ = kI
        assert A * S(b).T == k * sympy.eye(3)
        assert A * S(mm.solve_from_transpose_identity(b, k, w)) == S(w)


def test_ab_identity_statements():
    rng = random.Random(7)
    EYE = sympy.eye(3)

    def holds(tex, A, B):
        return {
            "BA = I": B * A == EYE, r"A^{-1} = B": A.inv() == B, r"B^{-1} = A": B.inv() == A,
            r"(A^{t})^{-1} = B^{t}": A.T.inv() == B.T, r"B^{t}A^{t} = I": B.T * A.T == EYE,
            r"A^{t}B^{t} = I": A.T * B.T == EYE, r"\det(A)\det(B) = 1": A.det() * B.det() == 1,
            r"A^{2}B^{2} = I": A ** 2 * B ** 2 == EYE, "A = B": A == B,
            r"\det(A) = \det(B)": A.det() == B.det(), "A + B = 2I": A + B == 2 * EYE,
            r"A^{2} = B^{2}": A ** 2 == B ** 2, r"A^{t} = B": A.T == B,
        }[tex]

    seen_false = set()
    for _ in range(30):
        while True:
            A = S(mm.mat([[rng.randint(-3, 3) for _ in range(3)] for _ in range(3)]))
            if A.det() not in (0, 1, -1):
                break
        B = A.inv()
        for tex, true in mm.AB_IDENTITY_FACTS:
            if true:
                assert holds(tex, A, B), tex
            elif not holds(tex, A, B):
                seen_false.add(tex)
    assert seen_false == {t for t, true in mm.AB_IDENTITY_FACTS if not true}


def test_exam_answers_reproduce():
    assert mm.det_after(3, Fraction(10), "swap", 0, Fraction(1, 5), "plain") == Fraction(-2, 25)  # กสพท (มี.ค. 2563/6)
    assert mm.det_inverse_from_scaled(3, 2, Fraction(24)) == Fraction(1, 3)          # กสพท คณิต1 (มี.ค. 2562/5)
    a, b = mm.mat([[2, 1], [3, 5]]), mm.mat([[4, 3], [-2, 2]])
    assert mm.det(mm.matmul(a, mm.inverse(b))) == Fraction(1, 2)                    # กสพท คณิต1 (มี.ค. 2561/5)
    assert mm.unknown_from_quotient(-1, 3, -2, 1, Fraction(-6)) == 4                  # A-level 1 (มี.ค. 2566/9)
    x = mm.solve_left(mm.mat([[1, 1], [3, 2]]), mm.mat([[-2, 1], [3, 4]]))
    assert 2 * x[0][0] + x[0][1] + x[1][0] + x[1][1] == 6                             # A-level 1 (มี.ค. 2567/21)
    m = mm.mat([[0, 2, -2], [1, 1, -1], [2, 1, 2]])                                   # กสพท คณิต1 (ธ.ค. 2558/5)
    assert mm.excluded_value(m, (0, 0)) == 2


def test_matrix_power_cycles_match_sympy():
    for rows, k in mm.CYCLIC:
        a = sympy.Matrix(rows)
        assert mm.cycle_length(mm.mat(rows)) == k
        assert a ** k == sympy.eye(2) and all(a ** j != sympy.eye(2) for j in range(1, k))
        for n in (1, 7, 50, 101):
            assert sympy.Matrix(mm.mat_pow(mm.mat(rows), n)) == a ** n
        assert mm.identity_powers(mm.mat(rows), 100) == sum(a ** j == sympy.eye(2) for j in range(1, 101))


def test_matrix_power_exam_answer():
    # วิชาสามัญ คณิตศาสตร์ 1 (ธ.ค. 2558/29): A is a rotation by π/3, so Aᵏ = I for 16 values of k in 1..100.
    assert mm.identity_powers(mm.mat([[1, -1], [1, 0]]), 100) == 16


@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    assert want in (3, 4)
    for seed in range(120):
        q = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in q.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert q.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()
