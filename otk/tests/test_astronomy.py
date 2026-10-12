"""Tests specific to ดาราศาสตร์ (ระบบสุริยะ).

The classify types (phenomena / space_tech / satellite_uses / space_missions) are
covered by ``test_classify_types.py`` and the concept banks by
``test_concept_types.py``. These pin the planet-order type — a bijection between a
planet and its position from the sun, asked both ways — and that every ดาราศาสตร์
ชุดโจทย์ lands under the right subject/level/topic.
"""

from __future__ import annotations

import random
import re

import pytest

from otk.core import catalog, generate
from otk.sets.astronomy.m3.solar_system_and_gravity import PLANETS

ASTRO_KEYS = [
    "astro.phenomena", "astro.space_tech", "astro.satellite_uses",
    "astro.space_missions", "astro.gravity", "astro.seasons", "astro.sun_path",
    "astro.moon_phases", "astro.tides", "astro.planet_order",
]


def _stem(q) -> str:
    return q.stem[0].text


def _answer(q) -> str:
    return q.choices[q.answer].content[0].text


# ── The planet table is sound ────────────────────────────────────────────────

def test_planets_are_the_eight_in_order():
    assert [p.order for p in PLANETS] == list(range(1, 9))
    assert PLANETS[0].name.startswith("ดาวพุธ")      # Mercury closest
    assert PLANETS[-1].name.startswith("ดาวเนปจูน")  # Neptune farthest
    assert len({p.name for p in PLANETS}) == 8       # no duplicate names


# ── Order ↔ name, both directions ────────────────────────────────────────────

def test_order_to_name_is_correct():
    by_order = {p.order: p.name for p in PLANETS}
    rng = random.Random(1)
    for _ in range(300):
        q = generate("astro.planet_order", rng, ask=1)      # given order → name
        order = int(re.search(r"ลำดับที่ (\d+)", _stem(q)).group(1))
        assert _answer(q) == by_order[order]
        # every choice is a real planet name
        for c in q.choices:
            assert c.content[0].text in by_order.values()


def test_name_to_order_is_correct():
    by_name = {p.name: p.order for p in PLANETS}
    rng = random.Random(2)
    for _ in range(300):
        q = generate("astro.planet_order", rng, ask=2)      # given name → order
        name = re.search(r"“([^”]+)”", _stem(q)).group(1)
        assert _answer(q) == f"ลำดับที่ {by_name[name]}"


def test_planet_order_ask_pins_the_direction():
    rng = random.Random(3)
    # ask=1 asks "which planet"; ask=2 quotes a planet and asks for its position.
    assert all("คือดาวใด" in generate("astro.planet_order", rng, ask=1).stem[0].text
               for _ in range(40))
    assert all("ลำดับที่เท่าใด" in generate("astro.planet_order", rng, ask=2).stem[0].text
               for _ in range(40))


# ── Catalog wiring ───────────────────────────────────────────────────────────

@pytest.mark.parametrize("key", ASTRO_KEYS)
def test_catalog_places_every_astro_type(key):
    entry = {t["key"]: t for t in catalog()}[key]
    assert (entry["subject"], entry["level"], entry["topic"]) == \
        ("ดาราศาสตร์", "ม.3", "ระบบสุริยะ")
