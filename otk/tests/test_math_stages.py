"""The authored learning path (math_stages) covers every IPST set exactly once."""

from __future__ import annotations

from collections import Counter, defaultdict

from otk.core import REGISTRY, catalog
from otk.sets._support.math_stages import MATH_STAGE_PATHS, stage_of


def _ipst_topics() -> dict[tuple[str, str, str], set[str]]:
    topics: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    for row in catalog():
        if row["subject"] == "คณิตศาสตร์" and row["course_type"] in {
            "สสวท. พื้นฐาน", "สสวท. เพิ่มเติม",
        }:
            topics[(row["course_type"], row["level"], row["topic"])].add(row["key"])
    return topics


def test_every_ipst_set_is_placed_in_its_own_topic():
    topics = _ipst_topics()
    assert set(MATH_STAGE_PATHS) == set(topics)
    for node, keys in topics.items():
        listed = {f"math.{key}" for stage in MATH_STAGE_PATHS[node] for key in stage}
        assert listed == keys, node


def test_no_set_is_listed_twice_and_every_stage_has_a_set():
    counts = Counter(key for path in MATH_STAGE_PATHS.values()
                     for stage in path for key in stage)
    assert [key for key, n in counts.items() if n > 1] == []
    for node, path in MATH_STAGE_PATHS.items():
        assert len(path) == 3 and all(path), node


def test_registry_carries_the_authored_stage():
    for key, stage in stage_of().items():
        assert REGISTRY[key].learning_stage == stage, key


def test_prerequisites_come_first():
    # The inversions the keyword heuristic produced.
    stage = stage_of()
    before = [
        ("math.one_digit_subtraction", "math.missing_subtrahend"),
        ("math.reduce_fraction", "math.div_fractions"),
        ("math.improper_to_mixed", "math.mul_fractions"),
        ("math.decimal_multiply_p5", "math.decimal_divide_p5"),
        ("math.order_of_ops_integers", "math.order_of_ops"),
        ("math.product_rule", "math.scientific_multiply"),
        ("math.mean_from_data", "math.mean_missing_value_m1"),
        ("math.negative_exponent", "math.fractional_exponent"),
        ("math.times_table", "math.multiply_4x1_p3"),
    ]
    for easier, harder in before:
        assert stage[easier] < stage[harder], (easier, harder)
