"""Tests for the เคมี element types (ธาตุและตารางธาตุ).

``test_core.py`` already asserts the shape invariants for every registered type;
these pin the things specific to chemistry: the table itself is sound, the answer
is the *right* element fact, and the หมู่/เลขอะตอม window actually restricts
which elements — including the distractors — can appear.
"""

from __future__ import annotations

import random
import re

import pytest

from otk.core import catalog, generate
from otk.sets._support.chemistry import (
    ELEMENTS,
    MAX_GROUP,
    MAX_Z,
    TRANSITION,
    common_charges,
    element_pool,
    nuclide_tex,
)

KEYS = ["chem.symbol_to_name", "chem.name_to_symbol", "chem.atomic_number"]
NUCLIDE_KEYS = ["chem.nuclide", "chem.particles"]

BY_SYMBOL = {e.symbol: e for e in ELEMENTS}
_SYMBOL_TEX = re.compile(r"\\mathrm\{([A-Za-z]+)\}")
_NUCLIDE_TEX = re.compile(
    r"\{\}\^\{(\d+)\}_\{(\d+)\}\\mathrm\{([A-Za-z]+)\}(?:\^\{(\d*)\{([+-])\}\})?$")


def _stem_symbol(q) -> str:
    """The symbol shown in the stem, from either the math block or the name."""
    for b in q.stem:
        if b.kind == "math":
            return _SYMBOL_TEX.search(b.tex).group(1)
    name = q.stem[0].text                      # name_to_symbol: Thai-only stem
    th = name.split("ธาตุ ", 1)[1].split(" (", 1)[0]
    return next(e.symbol for e in ELEMENTS if e.th == th)


def _stem_nuclide(q) -> tuple[int, int, str, int]:
    """(mass, atomic number, symbol, charge) read back off a nuclide stem."""
    m = _NUCLIDE_TEX.fullmatch(q.stem[1].tex)
    assert m, f"unexpected nuclide TeX {q.stem[1].tex!r}"
    a, z, symbol, size, sign = m.groups()
    charge = 0 if sign is None else int(size or 1) * (1 if sign == "+" else -1)
    return int(a), int(z), symbol, charge


# ── The table ────────────────────────────────────────────────────────────────

def test_table_is_the_whole_periodic_table():
    assert [e.z for e in ELEMENTS] == list(range(1, MAX_Z + 1))
    assert all(TRANSITION <= e.group <= MAX_GROUP for e in ELEMENTS)


@pytest.mark.parametrize("field", ["symbol", "th", "en"])
def test_table_has_no_duplicates(field: str):
    # Duplicates would let a distractor be indistinguishable from the answer.
    values = [getattr(e, field) for e in ELEMENTS]
    assert len(values) == len(set(values))


def test_mass_numbers_are_plausible_isotopes():
    for e in ELEMENTS:
        neutrons = e.mass - e.z
        # A nuclide has at least as many nucleons as protons, and no real one is
        # anywhere near this neutron-rich (Pu-244 tops out at n/z ≈ 1.60).
        assert 0 <= neutrons <= 1.65 * e.z, e


@pytest.mark.parametrize("symbol,mass", [("H", 1), ("C", 12), ("O", 16),
                                         ("Na", 23), ("Cl", 35), ("Fe", 56),
                                         ("Ag", 107), ("Au", 197), ("U", 238)])
def test_known_mass_numbers(symbol: str, mass: int):
    assert BY_SYMBOL[symbol].mass == mass


def test_common_charges_follow_the_group_rule_then_the_metal_table():
    assert common_charges(BY_SYMBOL["Na"]) == (1,)      # หมู่ 1A
    assert common_charges(BY_SYMBOL["Mg"]) == (2,)      # หมู่ 2A
    assert common_charges(BY_SYMBOL["O"]) == (-2,)      # หมู่ 6A
    assert common_charges(BY_SYMBOL["Cl"]) == (-1,)     # หมู่ 7A
    assert common_charges(BY_SYMBOL["Fe"]) == (2, 3)    # metal override
    assert common_charges(BY_SYMBOL["Pb"]) == (2, 4)    # หมู่ 4A has no rule
    assert common_charges(BY_SYMBOL["C"]) == ()         # …so carbon stays neutral
    assert common_charges(BY_SYMBOL["Ne"]) == ()        # ก๊าซเฉื่อย


@pytest.mark.parametrize("symbol,charge,tex", [
    ("Na", 0, r"{}^{23}_{11}\mathrm{Na}"),
    ("Na", 1, r"{}^{23}_{11}\mathrm{Na}^{{+}}"),
    ("Al", 3, r"{}^{27}_{13}\mathrm{Al}^{3{+}}"),
    ("Cl", -1, r"{}^{35}_{17}\mathrm{Cl}^{{-}}"),
    ("O", -2, r"{}^{16}_{8}\mathrm{O}^{2{-}}"),
])
def test_nuclide_tex(symbol: str, charge: int, tex: str):
    assert nuclide_tex(BY_SYMBOL[symbol], charge) == tex


def test_a_groups_are_assigned_correctly():
    by_group = {g: [e.symbol for e in ELEMENTS if e.group == g]
                for g in range(1, MAX_GROUP + 1)}
    assert by_group[1] == ["H", "Li", "Na", "K", "Rb", "Cs", "Fr"]
    assert by_group[2] == ["Be", "Mg", "Ca", "Sr", "Ba", "Ra"]
    assert by_group[3] == ["B", "Al", "Ga", "In", "Tl", "Nh"]
    assert by_group[4] == ["C", "Si", "Ge", "Sn", "Pb", "Fl"]
    assert by_group[8] == ["He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og"]
    assert "Fe" not in {s for syms in by_group.values() for s in syms}  # หมู่ 0


# ── Answers are correct ──────────────────────────────────────────────────────

def test_symbol_to_name_answers_with_that_elements_name():
    rng = random.Random(11)
    for _ in range(200):
        q = generate("chem.symbol_to_name", rng)
        el = BY_SYMBOL[_stem_symbol(q)]
        assert q.choices[q.answer].content[0].text == f"{el.th} ({el.en})"


def test_name_to_symbol_answers_with_that_elements_symbol():
    rng = random.Random(12)
    for _ in range(200):
        q = generate("chem.name_to_symbol", rng)
        el = BY_SYMBOL[_stem_symbol(q)]
        assert q.choices[q.answer].content[0].tex == rf"\mathrm{{{el.symbol}}}"


def test_atomic_number_answers_with_that_elements_z():
    rng = random.Random(13)
    for _ in range(200):
        q = generate("chem.atomic_number", rng)
        el = BY_SYMBOL[_stem_symbol(q)]
        assert q.choices[q.answer].content[0].tex == str(el.z)
        # Distractors are other elements' atomic numbers, never invented ones.
        for c in q.choices:
            assert 1 <= int(c.content[0].tex) <= MAX_Z


# ── Reading the nuclide symbol ───────────────────────────────────────────────

def test_nuclide_asks_for_the_number_it_shows():
    rng = random.Random(21)
    seen = set()
    for _ in range(300):
        q = generate("chem.nuclide", rng)
        a, z, symbol, charge = _stem_nuclide(q)
        el = BY_SYMBOL[symbol]
        assert (a, z, charge) == (el.mass, el.z, 0)     # neutral: no ion here
        wants_mass = "เลขมวล" in q.stem[0].text
        seen.add(wants_mass)
        assert q.choices[q.answer].content[0].tex == str(a if wants_mass else z)
        # The number on the other corner is always offered — that's the mistake
        # this item exists to catch (skipped when they coincide, as for H-1).
        if a != z:
            assert str(z if wants_mass else a) in {c.content[0].tex for c in q.choices}
    assert seen == {True, False}                        # both asks come up


def test_particle_counts_are_computed_from_the_stem():
    rng = random.Random(22)
    seen = set()
    for _ in range(400):
        q = generate("chem.particles", rng)
        a, z, symbol, charge = _stem_nuclide(q)
        prompt = q.stem[0].text
        expected = {"โปรตอน": z, "นิวตรอน": a - z, "อิเล็กตรอน": z - charge}
        particle = next(p for p in expected if p in prompt)
        seen.add(particle)
        assert q.choices[q.answer].content[0].tex == str(expected[particle])
        assert ("ไอออน" in prompt) == bool(charge)      # named for what it is
        assert charge in (0, *common_charges(BY_SYMBOL[symbol]))
    assert seen == {"โปรตอน", "นิวตรอน", "อิเล็กตรอน"}


@pytest.mark.parametrize("key,asks", [
    ("chem.nuclide", ["เลขมวล", "เลขอะตอม"]),
    ("chem.particles", ["โปรตอน", "นิวตรอน", "อิเล็กตรอน"]),
])
def test_ask_param_pins_one_fact(key: str, asks: list[str]):
    rng = random.Random(23)
    for i, word in enumerate(asks, start=1):
        prompts = [generate(key, rng, ask=i).stem[0].text for _ in range(40)]
        assert all(word in p for p in prompts)
    # Out of range falls back to drawing a fact per item.
    prompts = [generate(key, rng, ask=99).stem[0].text for _ in range(60)]
    assert {w for w in asks if any(w in p for p in prompts)} == set(asks)


def test_ion_chance_bounds_are_honoured():
    rng = random.Random(24)
    # 0% never ionizes; 100% always does — for elements that have a common ion.
    assert all(_stem_nuclide(generate("chem.particles", rng, ion_chance=0))[3] == 0
               for _ in range(80))
    assert all(_stem_nuclide(
        generate("chem.particles", rng, ion_chance=100, group_lo=1, group_hi=2))[3] > 0
        for _ in range(80))


def test_noble_gases_are_never_ionized():
    rng = random.Random(25)
    for _ in range(80):
        q = generate("chem.particles", rng, group_lo=8, group_hi=8, ion_chance=100)
        assert _stem_nuclide(q)[3] == 0


# ── The หมู่ / เลขอะตอม window ────────────────────────────────────────────────

def test_pool_selects_one_a_group():
    assert [e.symbol for e in element_pool(group_lo=1, group_hi=1)] == \
        ["H", "Li", "Na", "K", "Rb", "Cs", "Fr"]


def test_pool_spans_groups_and_respects_atomic_number():
    pool = element_pool(group_lo=1, group_hi=4, z_hi=20)
    assert [e.symbol for e in pool] == ["H", "Li", "Be", "B", "C", "Na", "Mg",
                                        "Al", "Si", "K", "Ca"]


def test_pool_bounds_are_order_insensitive():
    assert element_pool(group_lo=4, group_hi=1) == element_pool(group_lo=1, group_hi=4)


def test_pool_default_is_the_whole_table():
    assert element_pool() == ELEMENTS


def test_empty_window_is_rejected():
    with pytest.raises(ValueError, match="no elements"):
        element_pool(group_lo=1, group_hi=1, z_lo=100, z_hi=110)


@pytest.mark.parametrize("key", KEYS)
def test_group_window_constrains_every_choice(key: str):
    # Not just the question: distractors must come from the same slice too,
    # otherwise a หมู่-1 drill would quietly show หมู่-8 answers.
    rng = random.Random(14)
    allowed = element_pool(group_lo=1, group_hi=2)
    names = {f"{e.th} ({e.en})" for e in allowed}
    texs = {rf"\mathrm{{{e.symbol}}}" for e in allowed} | {str(e.z) for e in allowed}
    for _ in range(120):
        q = generate(key, rng, group_lo=1, group_hi=2)
        assert BY_SYMBOL[_stem_symbol(q)] in allowed
        for c in q.choices:
            b = c.content[0]
            assert (b.text in names) if b.kind == "text" else (b.tex in texs)


@pytest.mark.parametrize("key", NUCLIDE_KEYS)
def test_group_window_constrains_the_nuclide_shown(key: str):
    rng = random.Random(26)
    allowed = {e.symbol for e in element_pool(group_lo=1, group_hi=2)}
    for _ in range(120):
        q = generate(key, rng, group_lo=1, group_hi=2)
        assert _stem_nuclide(q)[2] in allowed


def test_narrow_window_yields_fewer_real_choices():
    # H, Li, Na only — three real elements, so three choices and no fakes.
    rng = random.Random(15)
    q = generate("chem.symbol_to_name", rng, group_lo=1, group_hi=1, z_hi=11)
    assert len(q.choices) == 3


# ── Catalog wiring ───────────────────────────────────────────────────────────

RANGE_PARAMS = {"group_lo": TRANSITION, "group_hi": MAX_GROUP,
                "z_lo": 1, "z_hi": MAX_Z}


@pytest.mark.parametrize("key,level,topic,extra", [
    ("chem.symbol_to_name", "ม.1", "ธาตุและตารางธาตุ", {}),
    ("chem.name_to_symbol", "ม.1", "ธาตุและตารางธาตุ", {}),
    ("chem.atomic_number", "ม.4", "ธาตุและตารางธาตุ", {}),
    ("chem.nuclide", "ม.4", "โครงสร้างอะตอม", {"ask": 0}),
    ("chem.particles", "ม.1", "โครงสร้างอะตอม", {"ask": 0, "ion_chance": 60}),
])
def test_catalog_exposes_the_subject_level_and_range_params(
        key: str, level: str, topic: str, extra: dict):
    entry = {t["key"]: t for t in catalog()}[key]
    assert entry["subject"] == "เคมี"
    assert entry["level"] == level
    assert entry["legacy_level"] == "ม.1"
    assert entry["topic"] == topic
    assert entry["params"] == {**RANGE_PARAMS, **extra}


# ป.6 — การแยกสารเนื้อผสมอย่างง่าย (classify types are also checked in
# test_classify_types.py; concept banks in test_concept_types.py).
P6_SEPARATION_KEYS = ["chem.mixture_intro", "chem.separate_solids",
                      "chem.separate_solid_liquid", "chem.magnetic_separation",
                      "chem.separation_uses"]


@pytest.mark.parametrize("key", P6_SEPARATION_KEYS)
def test_p6_separation_types_sit_under_matter_topic(key: str):
    entry = {t["key"]: t for t in catalog()}[key]
    assert (entry["subject"], entry["legacy_level"], entry["topic"]) == \
        ("เคมี", "ป.6", "สารในชีวิตประจำวัน")
    assert entry["level"]
