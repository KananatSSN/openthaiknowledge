"""Check added ม.2 transformations with independent coordinate calculations."""

import re
from random import Random

import pytest

from otk.api import REGISTRY, catalog

KEYS = (
    "math.rotation_about_center_m2",
    "math.translation_then_reflection_m2",
    "math.inverse_transformation_m2",
)


def _pt(x, y):
    return f"({x}, {y})"


def _solve_from_stem(key, stem):
    if key == KEYS[0]:
        x, y, h, k = map(int, re.search(
            r"A = \((-?\d+), (-?\d+)\).*C = \((-?\d+), (-?\d+)\)", stem).groups())
        dx, dy = x - h, y - k
        if "ทวนเข็มนาฬิกา 90" in stem:
            return _pt(h - dy, k + dx)
        if "ตามเข็มนาฬิกา 90" in stem:
            return _pt(h + dy, k - dx)
        return _pt(2 * h - x, 2 * k - y)
    if key == KEYS[1]:
        x, y, u, v = map(int, re.search(
            r"A = \((-?\d+), (-?\d+)\).*เวกเตอร์ \((-?\d+), (-?\d+)\)", stem).groups())
        return _pt(-x - u, y + v)
    u, v, image_x, image_y = map(int, re.search(
        r"เวกเตอร์ \((-?\d+), (-?\d+)\).*A' = \((-?\d+), (-?\d+)\)", stem).groups())
    # Undo the translation first, then undo reflection across the x-axis.
    return _pt(image_x - u, -(image_y - v))


@pytest.mark.parametrize("key", KEYS)
@pytest.mark.parametrize("seed", range(150))
def test_transformation_answer_and_named_choices(key, seed):
    q = REGISTRY[key].generate(Random(seed))
    expected = _solve_from_stem(key, q.stem[0].text)
    assert q.choices[q.answer].content[0].tex == expected
    assert len(q.choices) == 4
    assert all(m is not None for i, m in enumerate(q.mistakes) if i != q.answer)
    assert all(choice.content[0].tex != expected
               for i, choice in enumerate(q.choices) if i != q.answer)


@pytest.mark.parametrize("key", KEYS)
def test_stage_and_variety(key):
    row = next(row for row in catalog() if row["key"] == key)
    assert (row["level"], row["topic"], row["learning_stage"]) == (
        "ม.2", "การแปลงทางเรขาคณิต", 3,
    )
    stems = {REGISTRY[key].generate(Random(seed)).stem[0].text for seed in range(200)}
    assert len(stems) >= 100
