"""Random-variable sets built from the sheet bank's knowledge units.

``sheetpipe plan`` found units of ``otk/knowledge/math/random-variables.json``,
exercised by กสพท and A-level questions in ``openthaiknowledge-bank/rathcenter/17 ตัวแปรสุ่ม``,
that no problem set practised. The existing normal-distribution sets use the
68–95–99.7 rule only; the exams hand over a z-table:

=====================================  ==========================================
unit                                   set
=====================================  ==========================================
random.normal-table                    math.normal_z_table_m6
random.expected-value                  math.expected_game_value_m6
random.distribution-variance           math.random_variable_variance_m6
=====================================  ==========================================

Table entries are Φ(z) rounded to four places, printed in the stem, and every
answer is computed from the printed entries. ``test_math_bank_random.py``
checks the table against math.erf, the inverse problems by substitution,
the game values by enumeration, and pins the source exams' answers.
"""

from __future__ import annotations




# ── Expected value of a game ─────────────────────────────────────────────────


# ── Variance of a discrete random variable ──────────────────────────────────


