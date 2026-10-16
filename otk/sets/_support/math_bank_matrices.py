"""Matrix sets built from the sheet bank's knowledge units.

``sheetpipe plan`` found units of ``otk/knowledge/math/matrices.json``,
exercised by กสพท and A-level questions in ``openthaiknowledge-bank/rathcenter/9 เมทริกซ์``,
that no problem set practised. The existing sets compute a determinant or an
inverse of a matrix they print; the exams reason about them instead:

=====================================  ==========================================
unit                                   set
=====================================  ==========================================
matrix.det-properties                  math.determinant_properties_m5
matrix.unique-solution                 math.matrix_unique_solution_m5
matrix.matrix-equation                 math.matrix_equation_m5
matrix.power-cycle                     math.matrix_power_cycle_m5
=====================================  ==========================================

Matrices are small integer ones and all arithmetic is in ``Fraction``, so every
answer is exact. ``test_math_bank_matrices.py`` checks the solvers with SymPy
matrices and pins the source exams' answers.
"""

from __future__ import annotations




# ── Small exact matrix arithmetic ────────────────────────────────────────────


# ── Determinant properties ───────────────────────────────────────────────────


# ── When a system has exactly one solution ───────────────────────────────────


# ── Matrix equations ─────────────────────────────────────────────────────────


# ── Powers of a matrix with a cycle ──────────────────────────────────────────


