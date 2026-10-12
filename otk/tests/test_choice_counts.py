"""How many choices each set offers, pinned so it cannot change by accident.

Four choices is the norm. Four things deviate from it, and only the first three
are deliberate:

1. The staged mathematics progression scaffolds the choice count on purpose.
   Every authored IPST Foundation set (``math_stages``) offers at most three
   (``FOUNDATION_CHOICES``); the retired ``math.ipst.foundation.*`` fillers
   offered two and ``math.ipst.fluency.*`` three.
2. :class:`~otk.kit.classify.ClassifyType` asks in two directions. The
   *pick* direction draws four members; the *classify* direction offers one
   choice per category, so a table with fewer than four categories necessarily
   offers fewer than four choices. There is nothing truthful to pad it with —
   the categories *are* the answer space — so a small table is accepted here and
   listed, rather than padded with an invented category.
3. Some answer spaces are closed and smaller than four — a number is prime or
   composite, a comparison is <, = or >, a rock is one of three kinds. A fourth
   choice there would be one that is not an answer at all.
4. Three mathematics sets run their distractor pool dry. That is a real defect
   rather than a design, and it is listed separately so it is not mistaken for
   one.

New sets must offer four. Three sets in Phase 5 were reshaped to keep that —
``ecology.matter_cycle_fluency`` split its consumers by trophic level,
``ecology.balance_actions_fluency`` became one-of-four instead of a two-category
table, and ``cell.plant_animal_fluency`` asks for a pair — and
:func:`expected_counts` is what makes the next one fail loudly instead of
shipping. The check itself runs in ``test_per_set.py``, on the draws it takes
once per set; this module owns the rule and its exceptions.
"""

from __future__ import annotations



from otk.core.registry import REGISTRY
from otk.sets._support.math_progression import FOUNDATION_CHOICES
from otk.sets._support.math_stages import stage_of


# Small ``ClassifyType`` tables: fewer than four categories, so the classify
# direction cannot offer four choices. All predate Phase 5.
SMALL_CLASSIFY_TABLES = frozenset({
    "astro.space_tech",
    "chem.acid_base",
    "chem.element_or_compound",
    "chem.matter_change",
    "chem.pure_or_mixture",
    "chem.separation_filter_magnet",
    "chem.separation_solution_methods",
    "chem.solution_colloid_suspension",
    "chem.states",
    "ecology.feeding",
    "elec.quantities",
    "elec.resistance_factors",
    "elec.series_parallel_rules",
    "geo.igneous_cooling",
    "geo.rock_formation",
    "geo.rock_types",
    "phys.em_spectrum",
    "phys.light",
    "phys.optics",
    "phys.wave_types",
})

# Sets whose answer space is closed and smaller than four. A number is prime or
# composite; a statement is true or false; a comparison is <, = or >; a rock is
# igneous, sedimentary or metamorphic. Offering a fourth choice would mean
# offering one that is not an answer at all.
CLOSED_ANSWER_SPACES = frozenset({
    "chem.group_of_element_1_2",
    "elec.circuit_type",
    "geo.rock_photo_group",
    "math.classify_data_type",
    "math.classify_line",
    "math.classify_real_number",
    "math.classify_triangle_by_angle",
    "math.compare_decimals",
    "math.compare_nonstandard_weight",
    "math.compare_sign",
    "math.improper_integral",
    "math.p_series",
    "math.prime_or_composite",
    "math.truth_value",
    "math.valid_argument",
})

# A bare yes/no label ("forms a hydrogen bond" or not): two choices, decided
# 2026-09-30 (docs/for_admin/MCQ_GUESSABILITY.md). Padding them to four meant
# two fillers nobody would pick.
YES_NO_TWO_CHOICE = frozenset({
    "biology.plant_response_application",
    "chem.electrolyte_dissociation_foundation",
    "chem.hydrocarbon_saturation_fluency",
    "chem.hydrogen_bond_fluency",
})

# Known defect, not design: the distractor pool runs dry, always for
# ``math.area_between_curves`` and on a small fraction of draws for the other
# two. Listed so it stays visible and so the rest of the catalog can be held to
# four without this masking it.
POOL_RUNS_DRY = frozenset({
    "math.area_between_curves",
    "math.expected_value",
    "math.horizontal_asymptote",
})


_AUTHORED_STAGE = stage_of()


def expected_counts(key: str) -> set[int]:
    """The choice counts this key is allowed to produce."""
    base = _base_counts(key)
    if _AUTHORED_STAGE.get(key) == 1:
        return {min(n, FOUNDATION_CHOICES) for n in base}
    return base


def _base_counts(key: str) -> set[int]:
    if key.startswith("math.ipst.foundation."):
        return {2}
    if key.startswith("math.ipst.fluency."):
        return {3}
    if key in SMALL_CLASSIFY_TABLES:
        return {2, 3, 4}
    if key in CLOSED_ANSWER_SPACES:
        return {2, 3}
    if key in POOL_RUNS_DRY:
        return {3, 4}
    if key in YES_NO_TWO_CHOICE:
        return {2}
    return {4}


def test_the_deviation_lists_name_only_sets_that_still_exist():
    """A set renamed or deleted must not leave a stale exemption behind."""
    buckets = (SMALL_CLASSIFY_TABLES, CLOSED_ANSWER_SPACES, POOL_RUNS_DRY, YES_NO_TWO_CHOICE)
    for bucket in buckets:
        assert bucket <= set(REGISTRY), sorted(bucket - set(REGISTRY))
    # A key in two buckets would make the reason for its exemption ambiguous.
    assert sum(len(bucket) for bucket in buckets) == len(set().union(*buckets))


def test_no_phase_5_science_set_is_exempt():
    """Everything Wave A, Wave B, the ``ว 1.1`` closure, Wave C and Wave D added offers four choices.

    The exemptions above are all legacy. If a new set ever needs one, that is a
    content decision to take deliberately rather than by adding a line here.
    """
    from otk.core.curriculum_science import (
        SCIENCE_BIOLOGY_CLOSURE_KEYS, SCIENCE_WAVE_B_KEYS, SCIENCE_WAVE_C_KEYS,
        SCIENCE_WAVE_D_KEYS, SCIENCE_WAVE_KEYS,
    )
    exempt = SMALL_CLASSIFY_TABLES | CLOSED_ANSWER_SPACES | POOL_RUNS_DRY
    assert not (SCIENCE_WAVE_KEYS | SCIENCE_WAVE_B_KEYS
                | SCIENCE_BIOLOGY_CLOSURE_KEYS
                | SCIENCE_WAVE_C_KEYS | SCIENCE_WAVE_D_KEYS) & exempt
