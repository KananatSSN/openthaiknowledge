"""Generated diagrams: every family draws, ids are unique, and only registered
ids are drawable."""

from __future__ import annotations

from PIL import Image

from otk.pictures import registry as diagrams


def test_every_family_draws_a_png(tmp_path, monkeypatch):
    monkeypatch.setenv("GENERATOR_DIAGRAM_DIR", str(tmp_path))
    for specs, drawer in diagrams.FAMILIES:
        for spec in (specs[0], specs[-1]):
            path = diagrams.diagram_path(spec.asset_id)
            assert path is not None and path.parent == tmp_path, drawer
            with Image.open(path) as img:
                assert img.format == "PNG" and min(img.size) > 40, drawer


def test_ids_are_unique_across_families():
    ids = [spec.asset_id for specs, _ in diagrams.FAMILIES for spec in specs]
    assert len(ids) == len(set(ids)) == len(diagrams.registry())


def test_unknown_ids_are_never_drawn(tmp_path, monkeypatch):
    monkeypatch.setenv("GENERATOR_DIAGRAM_DIR", str(tmp_path))
    assert diagrams.diagram_path("pc1_apple_999") is None
    assert diagrams.diagram_path("../secret") is None
    assert not list(tmp_path.iterdir())
