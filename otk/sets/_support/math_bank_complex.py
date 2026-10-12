"""Complex-number sets built from the sheet bank's knowledge units.

``sheetpipe plan`` found four units of ``otk/knowledge/math/complex.json``,
exercised by กสพท and A-level questions in
``sheet_database/rathcenter/11 จำนวนเชิงซ้อน``, that no problem set practised (the last came with the (สสวท) exercises):

=====================================  ==========================================
unit                                   set
=====================================  ==========================================
complex.powers-of-i                    math.complex_power_cycle_m5
complex.equation-parts                 math.complex_equation_parts_m5
complex.conjugate-root                 math.complex_conjugate_root_m5
complex.modulus-rules                  math.complex_modulus_rules_m5
complex.polynomial-solve               math.complex_polynomial_solve_m5
=====================================  ==========================================

Numbers are Gaussian rationals held as ``(Fraction, Fraction)`` pairs, and
lengths are k√m, so every answer is exact. ``test_math_bank_complex.py``
checks the solvers with SymPy (substituting solutions back into their
equations), the statement bank on random numbers, and pins the source exams'
answers.
"""

from __future__ import annotations

from fractions import Fraction

C = tuple[Fraction, Fraction]


def c(re, im=0) -> C:
    return Fraction(re), Fraction(im)


def mul(a: C, b: C) -> C:
    return a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0]


def cpow(a: C, n: int) -> C:
    out = c(1)
    for _ in range(n):
        out = mul(out, a)
    return out


# ── Powers of i ──────────────────────────────────────────────────────────────


# ── Equations in z, z̄ and |z| ────────────────────────────────────────────────


# ── Conjugate roots of real polynomials ──────────────────────────────────────


# ── Modulus rules ────────────────────────────────────────────────────────────


# ── Solving polynomial equations over ℂ ──────────────────────────────────────


