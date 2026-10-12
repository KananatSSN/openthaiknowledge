"""ลอการิทึม sets built from the sheet bank's knowledge units.

``sheetpipe plan`` found three units of ``otk/knowledge/math/logarithms.json``,
exercised by กสพท and A-level questions in
``sheet_database/rathcenter/6 เอกโพเนนเชียล และ ลอการิทึม``, that no problem set
practised:

=====================================  ==========================================
unit                                   set
=====================================  ==========================================
log.mixed-bases                        math.log_mixed_bases_m5
log.equation-advanced                  math.log_equation_advanced_m5
log.inequality                         math.log_inequality_m5
=====================================  ==========================================

Every item is built from integer exponents, so each answer is an exact
rational. ``test_math_bank_logs.py`` checks the identities with SymPy,
substitutes every claimed solution back into its equation, and pins the
source exams' answers.
"""

from __future__ import annotations




# ── Mixed bases ──────────────────────────────────────────────────────────────


# ── Harder log equations ─────────────────────────────────────────────────────


# ── Log inequalities ─────────────────────────────────────────────────────────


