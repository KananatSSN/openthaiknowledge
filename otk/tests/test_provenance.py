"""Every set says where it came from (otk/core/provenance.py)."""

from __future__ import annotations

import pytest

from otk.core import REGISTRY
from otk.core.provenance import KINDS, Provenance, provenance


@pytest.mark.parametrize("key", sorted(REGISTRY))
def test_every_set_has_a_provenance(key):
    try:
        found = provenance(key)
    except LookupError:
        pytest.fail(f"{key} must declare its provenance: "
                    "PROVENANCE = Provenance('original') on its class or in its module, "
                    "or Provenance('adapted', sources=(...)) citing what it adapts")
    assert found.kind in KINDS
    assert found.kind == "original" or found.sources


def test_an_adapted_set_must_cite_its_source():
    with pytest.raises(ValueError):
        Provenance("adapted")
    with pytest.raises(ValueError):
        Provenance("borrowed", ("x",))
