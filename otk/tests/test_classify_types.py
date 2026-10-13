"""Tests for every ``ClassifyType`` — the shared classify/pick concept types.

These are parametrized over *all* registered ``ClassifyType`` subclasses (ชีวะ
ecology, เคมี ป.6, ฟิสิกส์ คลื่นและแสง, ดาราศาสตร์ ระบบสุริยะ), so a new subject
table is covered the moment it is added. The properties that matter:

* the table is sound — no example lands in two categories (which would make a
  "classify" question ambiguous), and category labels are unique;
* ``classify`` answers with the shown example's own category;
* ``pick`` offers *exactly one* choice from the asked category, so there is a
  single right answer no matter how the choices shuffle.
"""

from __future__ import annotations

import random
import re

import pytest

from otk.core import REGISTRY, catalog, generate
from otk.kit.classify import ClassifyType

CLASSIFY_KEYS = sorted(k for k, t in REGISTRY.items()
                       if isinstance(t, ClassifyType))
# Tables with too few groups for a four-choice classify question ask only "pick".
CLASSIFYING_KEYS = [k for k in CLASSIFY_KEYS if "classify" in REGISTRY[k].ASKS]
_QUOTED = re.compile(r"“([^”]+)”")            # every classify stem quotes its member


def _cats(key):
    return REGISTRY[key].CATEGORIES


def _by_member(key) -> dict[str, str]:
    return {m: c.label for c in _cats(key) for m in c.members}


# ── The table is sound ───────────────────────────────────────────────────────

@pytest.mark.parametrize("key", CLASSIFY_KEYS)
def test_no_example_belongs_to_two_categories(key):
    members = [m for c in _cats(key) for m in c.members]
    assert len(members) == len(set(members)), f"{key}: an example is in two groups"


@pytest.mark.parametrize("key", CLASSIFY_KEYS)
def test_category_labels_are_unique(key):
    labels = [c.label for c in _cats(key)]
    assert len(labels) == len(set(labels)), f"{key}: duplicate category label"


@pytest.mark.parametrize("key", CLASSIFY_KEYS)
def test_every_category_has_at_least_one_example(key):
    assert all(c.members for c in _cats(key)), f"{key}: an empty category"


# ── Answers are the correct classification ───────────────────────────────────

@pytest.mark.parametrize("key", CLASSIFYING_KEYS)
def test_classify_answers_with_the_examples_category(key):
    by_member = _by_member(key)
    rng = random.Random(1)
    for _ in range(200):
        q = generate(key, rng, ask=1)          # 1 = classify an example
        m = _QUOTED.search(q.stem[0].text)
        assert m, f"{key}: classify stem does not quote its example"
        member = m.group(1)
        assert member in by_member, f"{key}: {member!r} is not a known example"
        assert q.choices[q.answer].content[0].text == by_member[member]


@pytest.mark.parametrize("key", CLASSIFY_KEYS)
def test_pick_has_exactly_one_choice_from_the_asked_category(key):
    cats = _cats(key)
    by_member = _by_member(key)
    rng = random.Random(2)
    for _ in range(200):
        q = generate(key, rng, ask=2)          # 2 = pick a member of a category
        stem = q.stem[0].text
        asked = next(c.label for c in cats if c.label in stem)
        answer = q.choices[q.answer].content[0].text
        assert by_member[answer] == asked      # the correct choice fits the ask
        in_cat = [c.content[0].text for c in q.choices
                  if by_member[c.content[0].text] == asked]
        assert in_cat == [answer], f"{key}: more than one choice fits the ask"


@pytest.mark.parametrize("key", CLASSIFYING_KEYS)
def test_ask_param_pins_the_style(key):
    # ask=1 always quotes an example; ask=2 never does (it names a category).
    rng = random.Random(3)
    assert all(_QUOTED.search(generate(key, rng, ask=1).stem[0].text)
               for _ in range(40))
    assert not any(_QUOTED.search(generate(key, rng, ask=2).stem[0].text)
                   for _ in range(40))


# ── Catalog wiring: the new subjects/levels/topics ───────────────────────────

EXPECTED = {
    "chem.states": ("เคมี", "ป.6", "สารในชีวิตประจำวัน"),
    "chem.matter_change": ("เคมี", "ป.6", "สารในชีวิตประจำวัน"),
    "chem.acid_base": ("เคมี", "ป.6", "สารในชีวิตประจำวัน"),
    "chem.phase_change": ("เคมี", "ป.6", "สารในชีวิตประจำวัน"),
    "chem.separation": ("เคมี", "ป.6", "สารในชีวิตประจำวัน"),
    "chem.separate_solids": ("เคมี", "ป.6", "สารในชีวิตประจำวัน"),
    "phys.wave_types": ("ฟิสิกส์", "ม.3", "คลื่นและแสง"),
    "phys.em_spectrum": ("ฟิสิกส์", "ม.3", "คลื่นและแสง"),
    "phys.light": ("ฟิสิกส์", "ม.3", "คลื่นและแสง"),
    "phys.optics": ("ฟิสิกส์", "ม.3", "คลื่นและแสง"),
    "phys.curved_mirror_image": ("ฟิสิกส์", "ม.3", "คลื่นและแสง"),
    "phys.lens_image": ("ฟิสิกส์", "ม.3", "คลื่นและแสง"),
    "astro.phenomena": ("ดาราศาสตร์", "ม.3", "ระบบสุริยะ"),
    "astro.space_tech": ("ดาราศาสตร์", "ม.3", "ระบบสุริยะ"),
    "astro.satellite_uses": ("ดาราศาสตร์", "ม.3", "ระบบสุริยะ"),
    "astro.space_missions": ("ดาราศาสตร์", "ม.3", "ระบบสุริยะ"),
}


@pytest.mark.parametrize("key,expected", EXPECTED.items())
def test_catalog_places_each_type(key, expected):
    entry = {t["key"]: t for t in catalog()}[key]
    subject, legacy_level, topic = expected
    assert (entry["subject"], entry["legacy_level"], entry["topic"]) == \
        (subject, legacy_level, topic)
    assert entry["level"]
    assert entry["params"] == {"ask": 0}


def test_astronomy_is_a_new_subject_in_the_catalog():
    subjects = {t["subject"] for t in catalog()}
    assert "ดาราศาสตร์" in subjects
