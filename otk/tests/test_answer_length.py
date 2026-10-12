"""Regression coverage for conspicuously long correct prose answers."""

from __future__ import annotations

from random import Random

import pytest

from otk.core import generate
from scripts.audit_answer_length import is_strong_length_leak


CONTEXTUAL_KEYS = (
    "body.immune_response_application",
    "life.dna_technology_application",
    "geo.soil_profile_application",
    "plant.photosynthesis_application",
    "plant.photosynthesis_importance_application",
    "plant.transport_direction_application",
    "plant.reproduction_application",
    "plant.seed_application",
    "plant.nutrient_application",
    "plant.tissue_culture_application",
    "cell.shape_function_application",
    "cell.organisation_application",
    "body.respiratory_application",
    "body.breathing_application",
    "ecology.ecosystem_interaction_application",
    "ecology.relationship_survey_application",
    "ecology.decomposer_application",
    "ecology.biomagnification_application",
    "ecology.balance_application",
    "phys.energy_conservation_fluency",
    "chem.conservation_mass_fluency",
    "tech.technology_link_application",
    "tech.technology_impact_application",
)


@pytest.mark.parametrize("key", CONTEXTUAL_KEYS)
def test_contextual_choices_are_distinct_and_not_length_leaked(key):
    for seed in range(100):
        question = generate(key, Random(seed))
        rendered = [choice.model_dump_json() for choice in question.choices]
        assert len(rendered) == len(set(rendered))
        assert not is_strong_length_leak(question), (key, seed, rendered)
