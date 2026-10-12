"""Tests for the offline curriculum-graph tool.

It is a dev tool, so most of it is a browser's problem. What is tested here is
the part that can break silently: the figures. They are baked into the page as
data URIs at build time, so a renamed asset id or a moved figures directory
would not raise — the page would just quietly stop showing diagrams, which is
the one job it has when you are checking that a diagram matches its question.
"""

from __future__ import annotations

import random

import pytest

from otk.core import REGISTRY, generate
from otk.core.curriculum_science import (
    REVIEW_PENDING, SCIENCE_WAVE_C_APPROVED_KEYS, SCIENCE_WAVE_H_KEYS,
)
from otk.tools import curriculum_graph as cg
from otk.tools.sheetpipe.spec import load_sheet, sheet_ids


def _sample(key: str, seed: int = 0) -> dict:
    q = generate(key, random.Random(seed))
    return {"stem": [b.model_dump() for b in q.stem],
            "choices": [[b.model_dump() for b in c.content] for c in q.choices],
            "answer": q.answer}


def _figure_keys() -> list[str]:
    return [it.generator for sid in sheet_ids() for it in load_sheet(sid).items
            if it.figure_asset]


def _key_that_bakes(samples: int = 6) -> str | None:
    """A type whose first ``samples`` draws really do reference their figure.

    Some types attach a crop that only *some* draws may show — 2565 §14 draws the
    sheet's two radii, so it hides the picture whenever the generator changes
    them — and picking one of those here would test nothing.
    """
    for key in _figure_keys():
        rows = [{"key": key, "samples": [_sample(key, s) for s in range(samples)]}]
        if cg._asset_ids(rows):
            return key
    return None


def test_a_shipped_sheet_figure_resolves_without_the_api():
    """The tool reads assets straight off disk — it must find the same file the
    asset store would, without constructing Settings (which would create a data
    directory and a signing key just to draw a graph)."""
    attached = [it for sid in sheet_ids() for it in load_sheet(sid).items
                if it.figure_asset]
    if not attached:
        pytest.skip("no sheet ships a figure")
    path = cg._asset_file(attached[0].figure_asset)
    assert path is not None and path.is_file()


def test_builtin_diagrams_still_resolve():
    assert cg._asset_file("skeleton") is not None


def test_unknown_asset_resolves_to_nothing():
    assert cg._asset_file("no-such-asset") is None
    assert cg._asset_data_uri("no-such-asset") is None


def test_every_figure_a_sample_references_gets_baked():
    """A referenced-but-missing asset is the failure this guards: the page would
    render '[ไม่พบรูป: …]' where the diagram belongs."""
    keys = _figure_keys()
    if not keys:
        pytest.skip("no sheet ships a figure")
    rows = [{"key": k, "samples": [_sample(k, s) for s in range(8)]} for k in keys]
    ids = cg._asset_ids(rows)
    assert ids, "no sample referenced a figure at all"
    baked = cg.assets_for(rows)
    assert set(baked) == set(ids)
    assert all(uri.startswith("data:image/png;base64,") for uri in baked.values())


def test_a_figure_is_baked_once_however_many_samples_use_it():
    key = _key_that_bakes()
    if key is None:
        pytest.skip("no sheet ships a figure every draw shows")
    rows = [{"key": key, "samples": [_sample(key, s) for s in range(6)]}]
    assert len(cg.assets_for(rows)) == len(set(cg._asset_ids(rows)))


def test_every_set_awaiting_review_is_a_registered_key():
    """A stale or misspelled cohort would highlight nothing and look like no work."""
    for name, keys in REVIEW_PENDING.items():
        assert keys, name
        assert keys <= set(REGISTRY), name


def test_review_cohorts_do_not_overlap():
    seen: set[str] = set()
    for keys in REVIEW_PENDING.values():
        assert not seen & keys
        seen |= keys


def test_approved_sets_are_no_longer_marked_as_pending():
    """Approval clears the highlight, or the worklist would never shrink.

    A set Wave H widened after approval is reopened for review under Wave H.
    """
    for key in SCIENCE_WAVE_C_APPROVED_KEYS - SCIENCE_WAVE_H_KEYS:
        assert cg.review_cohort(key) is None, key
    # A baseline set stays unmarked unless Wave H widened it, which reopens it.
    expected = "Phase 5 Wave H" if "geo.rock_cycle" in SCIENCE_WAVE_H_KEYS else None
    assert cg.review_cohort("geo.rock_cycle") == expected


def test_the_page_carries_the_review_marks_and_the_filter():
    name, keys = next(iter(REVIEW_PENDING.items()), ("Phase 5 Wave C", frozenset()))
    if not keys:
        pytest.skip("nothing is awaiting review")
    key = sorted(keys)[0]
    assert cg.review_cohort(key) == name
    rows = [{"key": key, "subject": "ธรณีวิทยา", "level": "ป.1", "topic": "t",
             "display_name": "x", "params": {}, "samples": [_sample(key)],
             "review": cg.review_cohort(key)}]
    html = cg.build_html(rows=rows)
    assert f'"review": "{name}"' in html
    assert 'id="reviewOnly"' in html


def test_build_html_injects_both_data_tokens():
    key = _key_that_bakes()
    if key is None:
        pytest.skip("no sheet ships a figure every draw shows")
    rows = [{"key": key, "subject": "คณิตศาสตร์", "level": "โอลิมปิก (สอวน.)",
             "topic": "", "display_name": "x", "params": {},
             "samples": [_sample(key, s) for s in range(6)]}]
    html = cg.build_html(rows=rows)
    assert "/*__DATA__*/null" not in html
    assert "/*__ASSETS__*/null" not in html
    assert "data:image/png;base64," in html
