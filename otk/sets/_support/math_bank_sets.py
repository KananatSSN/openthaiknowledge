"""เซต sets built from the sheet bank's knowledge units.

``sheetpipe plan เซต`` found nine units of ``otk/knowledge/math/sets.json``
that no problem set practised, all exercised by A-level, กสพท and O-NET
questions in ``sheet_database/rathcenter/1 เซต``. Eight sets cover them:

=====================================  ===========================================
unit(s)                                set
=====================================  ===========================================
compound-expressions, recover-set      math.set_expression_eval_m4
region-expression                      math.set_expression_match_m4
identities                             math.set_always_true_m4
two-set-word                           math.set_two_set_word_m4
exactly-k                              math.set_exactly_k_m4
region-algebra                         math.set_region_algebra_m4
divisibility-counting                  math.set_multiples_count_m4
extremal                               math.set_extremal_m4
=====================================  ===========================================

The counting sets draw the hidden truth as Venn-region counts, state totals
derived from them, and answer with a solver that sees only the stated numbers.
Every item checks that its solver recovers the hidden count, and
``test_math_bank_sets.py`` checks each solver against brute force over region
counts. The set-algebra sets decide truth by evaluating over explicit
elements, or over every subset of a small universe.
"""

from __future__ import annotations




# ── Expressions over three sets ──────────────────────────────────────────────


# ── Statements that are always true ──────────────────────────────────────────


# ── Counting from Venn regions ───────────────────────────────────────────────


# ── Multiples ────────────────────────────────────────────────────────────────


# ── Extremes ─────────────────────────────────────────────────────────────────


