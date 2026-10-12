"""No item may print its own answer in the stem.

Found by the 2026-09 content audit: ``trig_application_height`` showed the
answer expression under every question, the ordering sets sometimes showed
their numbers already in the order asked for, ``combination_identity`` showed
C(n, n/2), and ``matrix_inverse_m5`` could draw a matrix that is its own
inverse.
"""

from __future__ import annotations

from random import Random

import pytest

from otk.core import generate

KEYS = (
    "math.trig_application_height",
    "math.order_numbers",
    "math.order_numbers_p2",
    "math.order_fractions",
    "math.combination_identity",
    "math.matrix_inverse_m5",
)


def _blocks(blocks) -> list[str]:
    return [block.model_dump_json() for block in blocks]


@pytest.mark.parametrize("key", KEYS)
def test_the_stem_never_shows_the_answer(key):
    for seed in range(400):
        q = generate(key, Random(seed))
        answer = q.choices[q.answer].content
        assert not (len(answer) == 1 and _blocks(answer)[0] in _blocks(q.stem)), (key, seed)
