"""Acceptance gate for Phase 5 Wave G — gaps inside indicators already complete.

Every indicator this wave touches was already at three sets, so the wave is not
about coverage counted by indicator. It is about ideas a tutor teaches early that
no set in the registry asked for.

Slice 1 — ``ป.6`` ไฟฟ้าเบื้องต้น:

* **สัญลักษณ์ไฟฟ้า** — the only ``ป.6`` set that mentioned สัญลักษณ์ asked *why*
  symbols are used. None showed one. ``phys.circuit_symbol_*`` fixes that.
* **วงจรปิด / วงจรเปิด** — ``ว 2.3 ป.6/1``'s trio walks through each component
  and its function and never asks about the loop they have to form.
  ``phys.closed_circuit_*`` does, in words only.

Slice 2 — ``ม.1`` ความร้อน และ ลมฟ้าอากาศ:

* **ความชื้นสัมพัทธ์** (``ว 3.2 ม.1/2``) — named by the indicator as an
  องค์ประกอบ, fed to learners as data by ``geo.weather_forecast_fluency``, and
  matched by nothing in the registry. Text only.
* **แผนที่อากาศ** (``ว 3.2 ม.1/4``) — existed only at ``ม.6``, so a ``ม.1``
  learner told to forecast "จากข้อมูล" never saw the form that data arrives in.
* **การถ่ายโอนความร้อนจากภาพ** (``ว 2.3 ม.1/6``) — telling การนำ, การพา and
  การแผ่รังสี apart from a drawing rather than from three sentences.

Slice 3 — ``ม.1`` ``Q = mL``:

* **ความร้อนแฝง** (``ว 2.3 ม.1/1``) — the indicator names *two* equations,
  ``Q = mcΔT`` **and** ``Q = mL``. Only the first had a set, and searching the
  registry for ``ความร้อนแฝง`` matched nothing at any level. Four sets, because
  the pair of equations needs a fourth question — which one a stretch of the
  heating curve calls for — that neither equation alone asks.

Slices 1 and 2 claim no ``exact``: each indicator's own verb is something a
multiple-choice item cannot perform (เขียนแผนภาพ, ต่อวงจร, สร้างแบบจำลอง,
พยากรณ์อากาศ) or something a different trio already does (ระบุส่วนประกอบ,
บรรยายหน้าที่, อธิบายปัจจัยที่มีผล).

``phys.latent_heat_fluency`` is the one exception in the wave, and it is pinned
as such below. ``ว 2.3 ม.1/1`` writes ``Q = mL`` into its own text and asks for
คำนวณ; that set computes ``Q = mL``. Claiming less would be filing a set as
adjacent to a verb it performs word for word.

The drawings themselves are checked in ``test_circuit_symbols.py`` and
``test_ms1_diagrams.py``; this file is the filing gate.
"""

from __future__ import annotations

from random import Random

import pytest

from otk.core import generate
from otk.core.curriculum_science import (
    BASIC,
    SCIENCE_SUBJECTS,
    SUPPLEMENTAL,
    REVIEW_PENDING,
    SCIENCE_BIOLOGY_CLOSURE_KEYS,
    SCIENCE_PLACEMENTS,
    SCIENCE_WAVE_B_KEYS,
    SCIENCE_WAVE_C_KEYS,
    SCIENCE_WAVE_D_KEYS,
    SCIENCE_WAVE_E_KEYS,
    SCIENCE_WAVE_F_KEYS,
    SCIENCE_WAVE_G_APPROVED_KEYS,
    SCIENCE_WAVE_G_KEYS,
    SCIENCE_WAVE_KEYS,
)
from otk.core.registry import REGISTRY


SEEDS = 120


def _triple(prefix: str) -> tuple[str, str, str]:
    return tuple(f"{prefix}_{stage}"
                 for stage in ("foundation", "fluency", "application"))


#: Every group this wave adds, by the indicator it is filed under. All but one
#: are trios; ``ว 2.3 ม.1/1`` is four, so the tests below check the shape of a
#: group rather than assuming three.
GROUPS = {
    "ว 2.3 ป.6/2": _triple("phys.circuit_symbol"),
    "ว 2.3 ป.6/1": _triple("phys.closed_circuit"),
    "ว 3.2 ม.1/2": _triple("geo.humidity"),
    "ว 3.2 ม.1/4": _triple("geo.weather_chart"),
    "ว 2.3 ม.1/6": _triple("phys.heat_transfer_diagram"),
    "ว 2.3 ม.1/1": _triple("phys.latent_heat") + ("phys.latent_heat_scenario",),
}

#: The one set in the wave that performs its indicator's own verb.
EXACT_KEYS = frozenset({"phys.latent_heat_fluency"})

TOPICS = {
    "ว 2.3 ป.6/2": "สัญลักษณ์ไฟฟ้าและการอ่านแผนภาพวงจรไฟฟ้า",
    "ว 2.3 ป.6/1": "วงจรปิด วงจรเปิด และเส้นทางของกระแสไฟฟ้า",
    "ว 3.2 ม.1/2": "ความชื้นสัมพัทธ์ของอากาศ",
    "ว 3.2 ม.1/4": "การอ่านแผนที่อากาศอย่างง่าย",
    "ว 2.3 ม.1/6": "การจำแนกการถ่ายโอนความร้อนจากภาพ",
    "ว 2.3 ม.1/1": "การคำนวณปริมาณความร้อนแฝงในการเปลี่ยนสถานะ",
}

LEVELS = {
    "ว 2.3 ป.6/2": "ป.6", "ว 2.3 ป.6/1": "ป.6",
    "ว 3.2 ม.1/2": "ม.1", "ว 3.2 ม.1/4": "ม.1", "ว 2.3 ม.1/6": "ม.1",
    "ว 2.3 ม.1/1": "ม.1",
}

STANDARDS = {
    "ว 2.3 ป.6/2": "ว 2.3", "ว 2.3 ป.6/1": "ว 2.3",
    "ว 3.2 ม.1/2": "ว 3.2", "ว 3.2 ม.1/4": "ว 3.2", "ว 2.3 ม.1/6": "ว 2.3",
    "ว 2.3 ม.1/1": "ว 2.3",
}

#: Slice 4's sets carry **no indicator code at all**, so they cannot be keyed by
#: one. They are keyed by their unit instead, and checked by their own tests
#: below rather than by the indicator-shaped ones above.
UNINDICATED_GROUPS = {
    "วิทยาศาสตร์และวิธีการทางวิทยาศาสตร์": _triple("sci.scientific_method"),
    "ทักษะกระบวนการทางวิทยาศาสตร์": (
        "sci.process_skill_foundation", "sci.process_skill_fluency",
        "sci.process_skill_variables", "sci.process_skill_application"),
}

INDICATOR_KEYS = tuple(key for keys in GROUPS.values() for key in keys)
UNINDICATED_KEYS = tuple(key for keys in UNINDICATED_GROUPS.values() for key in keys)
NEW_KEYS = INDICATOR_KEYS + UNINDICATED_KEYS


# ── filing ────────────────────────────────────────────────────────────────────

def test_every_new_key_is_registered_and_placed():
    for key in NEW_KEYS:
        assert key in REGISTRY, key
        assert key in SCIENCE_PLACEMENTS, key


def test_wave_g_is_its_own_cohort():
    assert set(NEW_KEYS) == SCIENCE_WAVE_G_KEYS
    for earlier in (SCIENCE_WAVE_KEYS, SCIENCE_WAVE_B_KEYS,
                    SCIENCE_BIOLOGY_CLOSURE_KEYS, SCIENCE_WAVE_C_KEYS,
                    SCIENCE_WAVE_D_KEYS, SCIENCE_WAVE_E_KEYS,
                    SCIENCE_WAVE_F_KEYS):
        assert not SCIENCE_WAVE_G_KEYS & earlier


def test_approval_is_recorded_for_whole_groups():
    assert SCIENCE_WAVE_G_APPROVED_KEYS <= SCIENCE_WAVE_G_KEYS
    for code, keys in GROUPS.items():
        assert set(keys) & SCIENCE_WAVE_G_APPROVED_KEYS in (set(), set(keys)), code


def test_every_unapproved_set_is_on_the_review_worklist():
    pending = set().union(*REVIEW_PENDING.values()) if REVIEW_PENDING else set()
    assert SCIENCE_WAVE_G_KEYS - SCIENCE_WAVE_G_APPROVED_KEYS <= pending


def test_each_group_is_filed_as_one_unit_under_one_indicator():
    for code, keys in GROUPS.items():
        specs = [SCIENCE_PLACEMENTS[key] for key in keys]
        assert {spec.indicator_codes for spec in specs} == {(code,)}, code
        assert {spec.unit for spec in specs} == {TOPICS[code]}, code
        assert {spec.level for spec in specs} == {LEVELS[code]}, code
        assert {spec.course_type for spec in specs} == {BASIC}, code
        assert {spec.standard_code for spec in specs} == {STANDARDS[code]}, code


def test_no_set_claims_the_indicator_verb_it_does_not_perform():
    """Drawing, wiring, naming parts and describing functions are all elsewhere.

    ``EXACT_KEYS`` is the whole list of sets that do perform their indicator's
    verb, so widening it is an edit here rather than a silent upgrade.
    """
    for key in INDICATOR_KEYS:
        expected = "exact" if key in EXACT_KEYS else "standard_scope"
        assert SCIENCE_PLACEMENTS[key].mapping_status == expected, key


def test_the_one_exact_set_computes_the_equation_its_indicator_names():
    """``ว 2.3 ม.1/1`` writes ``Q = mL`` down; this set is the one that does it."""
    assert EXACT_KEYS <= set(NEW_KEYS)
    for key in EXACT_KEYS:
        assert "Q = mL" in REGISTRY[key].display_name["th"], key


def test_the_new_trios_do_not_displace_the_indicators_existing_sets():
    """Both indicators keep the trio they already had — this wave adds, never replaces."""
    for key in ("phys.circuit_diagram_foundation", "phys.circuit_diagram_fluency",
                "phys.circuit_diagram_application", "phys.circuit_parts_foundation",
                "phys.circuit_parts_fluency", "phys.circuit_parts_application",
                "geo.weather_factors_foundation", "geo.weather_factors_fluency",
                "geo.weather_factors_application", "geo.weather_forecast_foundation",
                "geo.weather_forecast_fluency", "geo.weather_forecast_application",
                "phys.heat_transfer_mode_foundation", "phys.heat_transfer_mode_fluency",
                "phys.heat_transfer_mode_application", "phys.heat_quantity_foundation",
                "phys.heat_quantity_fluency", "phys.heat_quantity_application"):
        assert key in REGISTRY, key
        assert key not in SCIENCE_WAVE_G_KEYS, key


@pytest.mark.parametrize("key", INDICATOR_KEYS)
def test_every_set_carries_its_unit_topic(key):
    code = next(one for one, keys in GROUPS.items() if key in keys)
    assert REGISTRY[key].topic == TOPICS[code]


# ── slice 4: the sets with no indicator ──────────────────────────────────────

def test_the_unindicated_sets_are_filed_as_outside_scope_with_no_indicator():
    """No ``ม.1`` outcome names these skills, so claiming one would be a lie.

    All 52 ``ม.1`` rows in ``science_ipst_outcomes.csv`` were checked; the only
    rows in the whole curriculum mentioning ``สมมติฐาน`` or ``ทักษะกระบวนการ``
    are ``ม.4``/``ม.6`` เพิ่มเติม. This is the filing seventeen existing sets
    already use for taught content the curriculum does not enumerate.
    """
    for key in UNINDICATED_KEYS:
        spec = SCIENCE_PLACEMENTS[key]
        assert spec.mapping_status == "outside_scope", key
        assert spec.indicator_codes == (), key
        assert spec.standard_code == "", key
        assert spec.course_type == SUPPLEMENTAL, key
        assert spec.level == "ม.1", key


def test_the_unindicated_sets_carry_the_sixth_subject():
    """A learner-facing addition, so it is pinned rather than left to drift."""
    for key in UNINDICATED_KEYS:
        assert REGISTRY[key].subject == "วิทยาศาสตร์ทั่วไป", key
    assert "วิทยาศาสตร์ทั่วไป" in SCIENCE_SUBJECTS


def test_no_other_set_in_the_registry_uses_the_sixth_subject():
    """The subject means these skills and nothing else."""
    general = {key for key, spec in REGISTRY.items()
               if spec.subject == "วิทยาศาสตร์ทั่วไป"}
    assert general == set(UNINDICATED_KEYS)


@pytest.mark.parametrize("key", UNINDICATED_KEYS)
def test_every_unindicated_set_carries_its_unit_topic(key):
    unit = next(one for one, keys in UNINDICATED_GROUPS.items() if key in keys)
    assert REGISTRY[key].topic == unit
    assert SCIENCE_PLACEMENTS[key].unit == unit


@pytest.mark.parametrize("key", NEW_KEYS)
def test_every_draw_offers_four_distinct_choices(key):
    for seed in range(SEEDS):
        question = generate(key, Random(seed))
        assert len({c.model_dump_json() for c in question.choices}) == 4, (key, seed)
        assert question.hint, (key, seed)


@pytest.mark.parametrize("key", NEW_KEYS)
def test_a_set_is_reproducible_from_its_seed(key):
    for seed in range(20):
        first = generate(key, Random(seed))
        assert first.model_dump_json() == generate(key, Random(seed)).model_dump_json()
