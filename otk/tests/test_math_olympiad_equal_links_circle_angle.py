"""Check the central angle via an independently constructed circle center."""

from math import acos, cos, degrees, pi, sin
from random import Random

from otk.core import REGISTRY, generate
from otk.sets.math.olympiad.equal_links_circle_angle import central_angle_from_equal_links


def _coordinate_central_angle(apex_angle: int) -> float:
    half = apex_angle * pi / 360
    half_base = sin(half)
    height = cos(half)
    half_chord = 1 + half_base
    center_y = (height**2 - half_chord**2) / (2 * height)
    radius_sq = half_chord**2 + center_y**2
    cosine = (center_y**2 - half_chord**2) / radius_sq
    return degrees(acos(max(-1.0, min(1.0, cosine))))


def test_matches_coordinate_circles():
    for angle in range(25, 156):
        assert abs(_coordinate_central_angle(angle) - central_angle_from_equal_links(angle)) < 1e-9


def test_checked_source_case():
    assert central_angle_from_equal_links(74) == 106


def test_generated_draws():
    key = "math.equal_links_circle_central_angle_olympiad"
    for seed in range(100):
        question = generate(key, rng=Random(seed))
        choices = [choice.model_dump_json() for choice in question.choices]
        assert len(choices) == REGISTRY[key].max_choices == len(set(choices))
        assert question.model_dump_json() == generate(key, rng=Random(seed)).model_dump_json()
