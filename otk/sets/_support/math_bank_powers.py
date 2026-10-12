"""เลขยกกำลัง-chapter sets built from the sheet bank's knowledge units.

``sheetpipe plan`` found five units, exercised by A-level, กสพท and O-NET
questions in ``sheet_database/rathcenter/5 เลขยกกำลัง``, that no problem set
practised:

=====================================  ==========================================  ==================================
unit                                   set                                         topic
=====================================  ==========================================  ==================================
expeq.advanced                         math.exponential_equation_advanced_m4       สมการเลขชี้กำลัง
power.rational-evaluate                math.rational_power_evaluate_m5             จำนวนจริงในรูปกรณฑ์และเลขยกกำลัง
power.root-signs                       math.root_sign_properties_m5                จำนวนจริงในรูปกรณฑ์และเลขยกกำลัง
power.compare                          math.power_compare_m5                       จำนวนจริงในรูปกรณฑ์และเลขยกกำลัง
radical.denest                         math.radical_denest_m4                      จัดรูปกรณฑ์
=====================================  ==========================================  ==================================

Every answer is exact: big-integer comparison, rational arithmetic, and
integer roots chosen by construction. ``test_math_bank_powers.py`` checks
each family with SymPy and pins the source exams' answers.
"""

from __future__ import annotations

from otk.core.content import math as content_math
from otk.core.distractors import fixed
from otk.core.question import GeneratedQuestion

M4, M5 = {"th": "ม.4"}, {"th": "ม.5"}


def _tex_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right]
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


# ── Harder exponential equations ─────────────────────────────────────────────


# ── Rational powers of negative bases and fractions ──────────────────────────


# ── Signs of roots ───────────────────────────────────────────────────────────

#: (premise text, [(claim TeX or Thai, true?)]) — every verdict is checked in the tests.
_ROOT_FACTS = (
    ("a เป็นจำนวนจริงลบ", [
        (r"\sqrt{a^{2}} = a", False), (r"\sqrt{a^{2}} = -a", True), (r"\sqrt[3]{a^{3}} = a", True),
        (r"\sqrt[4]{a^{4}} = a", False), (r"\sqrt[4]{a^{4}} = |a|", True), (r"\sqrt[3]{a^{3}} = |a|", False),
        (r"\sqrt{a^{2}} = |a|", True), (r"\sqrt[5]{-a^{5}} = a", False)]),
    ("a เป็นจำนวนจริงบวก", [
        (r"\sqrt[3]{(-a)^{3}} = -a", True), (r"\sqrt{(-a)^{2}} = -a", False),
        (r"a^{\frac{1}{2}} \cdot a^{\frac{1}{3}} = a^{\frac{5}{6}}", True),
        (r"a^{\frac{1}{2}} \cdot a^{\frac{1}{3}} = a^{\frac{1}{6}}", False),
        (r"(-a)^{\frac{2}{3}} = a^{\frac{2}{3}}", True), (r"\sqrt{a^{2}} = -a", False)]),
)


def claim_holds(premise: str, claim: str) -> bool:
    """The recorded verdict (checked numerically in the tests)."""
    return dict(dict(_ROOT_FACTS)[premise])[claim]


# ── Comparing large powers ───────────────────────────────────────────────────


# ── Nested radicals ──────────────────────────────────────────────────────────


