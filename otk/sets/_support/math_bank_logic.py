"""ตรรกศาสตร์ sets built from the sheet bank's knowledge units.

``sheetpipe plan ตรรกศาสตร์`` found six units of
``otk/knowledge/math/logic.json`` that no problem set practised, all
exercised by A-level, กสพท and O-NET questions in
``openthaiknowledge-bank/rathcenter/2 ตรรกศาสตร์``:

=====================================  ===========================================
unit                                   set
=====================================  ===========================================
evaluate-compound                      math.logic_compound_value_m4
deduce-values                          math.logic_deduce_values_m4
verbal-deduction                       math.logic_verbal_deduction_m4
tautology                              math.logic_tautology_m4
custom-connective                      math.logic_custom_connective_m4
quantifier-finite                      math.logic_quantifier_finite_m4
=====================================  ===========================================

All six share one small formula engine: build, render to TeX or Thai, and
evaluate. Every answer is decided by exhaustive truth tables. An item is
built only when its options split cleanly, with exactly one option on the
asked side over every assignment the premises allow. So no item has two
defensible answers. ``test_math_bank_logic.py`` checks the evaluator against
an independent compile-to-Python route and pins the source exams' verdicts.
"""

from __future__ import annotations

from itertools import product

T, F = "T", "F"

# ── The engine ───────────────────────────────────────────────────────────────
#
# A formula is a tuple: ("var", "p"), ("not", f), or (op, f, g) with op one of
# and / or / imp / iff.


def evaluate(f: tuple, env: dict[str, bool]) -> bool:
    kind = f[0]
    if kind == "var":
        return env[f[1]]
    if kind == "not":
        return not evaluate(f[1], env)
    a, b = evaluate(f[1], env), evaluate(f[2], env)
    return {"and": a and b, "or": a or b, "imp": (not a) or b, "iff": a == b}[kind]


def assignments(names: list[str]):
    for values in product((True, False), repeat=len(names)):
        yield dict(zip(names, values))


def table(f: tuple, names: list[str]) -> tuple[bool, ...]:
    return tuple(evaluate(f, env) for env in assignments(names))


def is_tautology(f: tuple, names: list[str]) -> bool:
    return all(table(f, names))


# ── Evaluate a compound from given values ────────────────────────────────────


# ── Work backwards from a compound's value ───────────────────────────────────


# ── The same, in Thai sentences ──────────────────────────────────────────────


# ── Tautologies ──────────────────────────────────────────────────────────────


# ── A connective defined by its table ────────────────────────────────────────


# ── Quantifiers over a small universe ────────────────────────────────────────


