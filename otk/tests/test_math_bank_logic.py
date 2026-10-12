"""The ตรรกศาสตร์ sets built from the sheet bank's knowledge units.

The formula engine is checked against an independent route: each formula is
compiled to a Python boolean expression string and ``eval``-ed. The items are
checked by re-deciding every option over every assignment the stem allows.
The source exams' verdicts are pinned.
"""

from __future__ import annotations

import random

import pytest

from otk.core import REGISTRY, generate
from otk.sets.math.m4 import logic as ml
from otk.sets._support.math_bank_logic import assignments, evaluate, is_tautology, table
from otk.sets.math.m4.logic import neg, var

KEYS = ("math.logic_compound_value_m4", "math.logic_deduce_values_m4",
        "math.logic_verbal_deduction_m4", "math.logic_tautology_m4",
        "math.logic_custom_connective_m4", "math.logic_quantifier_finite_m4")
p, q, r, s = var("p"), var("q"), var("r"), var("s")


def to_python(f) -> str:
    if f[0] == "var":
        return f[1]
    if f[0] == "not":
        return f"(not {to_python(f[1])})"
    a, b = to_python(f[1]), to_python(f[2])
    return {"and": f"({a} and {b})", "or": f"({a} or {b})",
            "imp": f"((not {a}) or {b})", "iff": f"({a} == {b})"}[f[0]]


def test_engine_matches_compiled_python():
    rng = random.Random(0)
    for _ in range(3000):
        f = ml.random_formula(rng, ["p", "q", "r"], 3)
        code = compile(to_python(f), "<f>", "eval")
        for env in assignments(["p", "q", "r"]):
            assert evaluate(f, env) == eval(code, {}, dict(env))


def test_no_degenerate_operands():
    rng = random.Random(1)

    def walk(f):
        if f[0] in ml.BINARY:
            assert ml.tex(f[1]) != ml.tex(f[2]), ml.tex(f)
            walk(f[1])
            walk(f[2])
        elif f[0] == "not":
            walk(f[1])

    for _ in range(2000):
        walk(ml.random_formula(rng, ["p", "q", "r"], 3))


def test_tex_parenthesizes_compounds():
    assert ml.tex(("imp", ("and", neg(p), q), r)) == r"(\sim p \land q) \to r"
    assert ml.tex(neg(("or", p, q))) == r"\sim (p \lor q)"


# ── The exam questions the units came from ───────────────────────────────────

def test_exam_verdicts():
    names = ["p", "q", "r"]
    # A-level 1 (มี.ค. 2567/2): only (p ∧ q) → (~p → r) is a tautology.
    options = [("imp", ("or", p, q), ("imp", neg(p), r)), ("imp", ("and", p, q), ("imp", neg(p), r)),
               ("imp", ("or", p, q), ("or", neg(p), r)), ("imp", ("and", p, q), ("or", neg(p), r)),
               ("imp", ("imp", p, q), ("or", neg(p), r))]
    assert [is_tautology(f, names) for f in options] == [False, True, False, False, False]
    # O-NET (ก.พ. 2565/2): only (p ∨ q) → q takes both values.
    two = ["p", "q"]
    options = [("imp", ("or", p, q), q), ("imp", ("and", neg(p), q), q),
               ("imp", ("and", neg(q), q), p), ("or", p, ("imp", p, q)),
               ("iff", ("or", p, q), ("and", neg(p), neg(q)))]
    assert [len(set(table(f, two))) for f in options] == [2, 1, 1, 1, 1]
    # A-level 2 (มี.ค. 2567/3): p, q true and r false — only (p ∨ q) → r is false.
    env = {"p": True, "q": True, "r": False}
    options = [("imp", p, ("or", q, r)), ("or", p, ("imp", q, r)), ("or", ("imp", p, q), r),
               ("imp", ("or", p, q), r), ("or", ("imp", p, q), ("imp", q, r))]
    assert [evaluate(f, env) for f in options] == [True, True, True, False, True]
    # A-level 1 (มี.ค. 2566/3): (~p ∧ q) → [~r → (r ↔ s)] false pins p F, q T, r F, s T.
    premise = ("imp", ("and", neg(p), q), ("imp", neg(r), ("iff", r, s)))
    envs = ml.forced(premise, False, ["p", "q", "r", "s"])
    assert envs == [{"p": False, "q": True, "r": False, "s": True}]
    assert evaluate(("and", q, s), envs[0])
    # A-level 1 (มี.ค. 2566/4): p ∗ q with table F T F T is ~q.
    star = (False, True, False, True)
    assert table(("or", ("and", p, neg(q)), ("and", neg(p), neg(q))), two) == star
    # กสพท คณิต1 (เม.ย. 2564/2): U = {2, 3, 4}; ก) and ค) true, ข) false.
    U = [2, 3, 4]
    assert any((x + 1 <= 5) == (2 * x > 1) for x in U)
    assert not ((not all(x * x > 1 for x in U)) or any(x - 3 > 1 for x in U))
    assert any((x + 2 != x * x) or x * x < 0 for x in U)


# ── The generated items ──────────────────────────────────────────────────────

@pytest.mark.parametrize("key", KEYS)
def test_items_offer_full_distinct_choices_and_are_reproducible(key):
    want = REGISTRY[key].max_choices
    assert REGISTRY[key].topic == "ตรรกศาสตร์" and want in (3, 4)
    for seed in range(60):
        item = generate(key, rng=random.Random(seed))
        texts = [c.model_dump_json() for c in item.choices]
        assert len(texts) == want and len(set(texts)) == want, (key, seed)
        assert item.model_dump_json() == generate(key, rng=random.Random(seed)).model_dump_json()


def _holds(f, env) -> bool:
    return eval(to_python(f), {}, dict(env))


@pytest.mark.parametrize("seed", range(60))
def test_deduction_items_have_exactly_one_defensible_answer(seed):
    # Premises re-checked with the compiled-Python route: every assignment
    # they allow gives the right option the asked value and no wrong option.
    names = ["p", "q", "r"]
    premise, value, want, right, wrongs = ml.draw_deduce(random.Random(seed))
    envs = [e for e in assignments(names) if _holds(premise, e) == value]
    assert envs
    assert all(_holds(right, e) == want for e in envs)
    assert all(_holds(w, e) != want for w in wrongs for e in envs)

    premises, want, right, wrongs = ml.draw_verbal(random.Random(seed), "ปิติ",
                                                   {"p": "ก", "q": "ข", "r": "ค"})
    envs = [e for e in assignments(names) if all(_holds(f, e) == v for f, v in premises)]
    assert envs
    assert all(_holds(right, e) == want for e in envs)
    assert all(_holds(w, e) != want for w in wrongs for e in envs)


def test_thai_rendering():
    verbs = {"p": "กวาดบ้าน", "q": "รดน้ำต้นไม้"}
    assert ml.thai(("imp", neg(q), neg(p)), "ปิติ", verbs) == \
        "ถ้าปิติไม่ได้รดน้ำต้นไม้ แล้วปิติไม่ได้กวาดบ้าน"
    assert ml.thai(("iff", p, q), "ปิติ", verbs) == "ปิติกวาดบ้านก็ต่อเมื่อปิติรดน้ำต้นไม้"
