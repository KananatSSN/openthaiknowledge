"""Keys are permanent and seeds are stable (otk/tools/golden_draws.py).

A failure here means a set's draws or its key changed. If that was intended,
regenerate the set's entry (``python -m otk.tools.golden_draws --update KEY``)
and name the set in the release notes: every consumer that replays stored
seeds — TutorRank's practice history — will now show a different question.
"""

from __future__ import annotations

import pytest

from otk.core import REGISTRY
from otk.tools.golden_draws import SEEDS, draw_hash, load

GOLDEN = load()


def test_the_fixture_uses_the_current_seeds():
    assert GOLDEN["seeds"] == list(SEEDS)


def test_every_set_is_recorded():
    missing = sorted(set(REGISTRY) - set(GOLDEN["sets"]))
    assert not missing, ("new sets need an entry: python -m otk.tools.golden_draws "
                         f"--update {' '.join(missing)}")


def test_no_key_disappears_without_being_retired():
    gone = sorted(set(GOLDEN["sets"]) - set(REGISTRY))
    assert not gone, ("removed sets must be retired: python -m otk.tools.golden_draws "
                      f"--retire {' '.join(gone)}")


def test_a_retired_key_is_never_reused():
    assert not set(GOLDEN["retired"]) & set(REGISTRY)
    assert not set(GOLDEN["retired"]) & set(GOLDEN["sets"])


@pytest.mark.parametrize("key", sorted(set(GOLDEN["sets"]) & set(REGISTRY)))
def test_draws_are_unchanged(key):
    assert draw_hash(key) == GOLDEN["sets"][key], (
        f"{key} now draws different questions for the same seeds")
