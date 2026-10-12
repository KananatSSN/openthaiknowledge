"""Vector sets built from the sheet bank's knowledge units.

``sheetpipe plan`` found three units of ``otk/knowledge/math/vectors.json``,
exercised by กสพท and A-level questions in ``sheet_database/rathcenter/10 เวกเตอร์``,
that no problem set practised. The existing sets compute one dot or cross
product of vectors they print; the exams combine them:

=====================================  ==========================================
unit                                   set
=====================================  ==========================================
vector.triple-product                  math.vector_triple_product_m5
vector.identities                      math.vector_identity_m5
vector.points                          math.vector_points_m5
=====================================  ==========================================

Vectors have small integer components, so dot and cross products are
integers and every length is k√m. ``test_math_bank_vectors.py`` checks the
solvers with SymPy, the statement banks on random vectors, and pins the
source exams' answers.
"""

from __future__ import annotations

Vec = tuple[int, int, int]


def dot(u, v) -> int:
    return sum(a * b for a, b in zip(u, v))


def cross(u, v) -> Vec:
    return (u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0])


# ── Scalar triple products ───────────────────────────────────────────────────

def triple(a, b, c) -> int:
    """a · (b × c)."""
    return dot(a, cross(b, c))


# ── Identities ───────────────────────────────────────────────────────────────


# ── Vectors between points ───────────────────────────────────────────────────


