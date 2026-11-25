"""The plain-JSON export (otk/tools/export.py): what apps outside Python install."""

from __future__ import annotations

import json
from random import Random

import pytest

from otk.api import REGISTRY, catalog
from otk.tools import export

PICTURE_SET = "math.count_objects_p1"     # every question shows a picture
SHEET_SET = "chem.posn2561_q01"          # digested from a past paper, few variants
KEYS = [PICTURE_SET, SHEET_SET]
SEEDS = 12


@pytest.fixture
def built(tmp_path, monkeypatch):
    monkeypatch.setenv("GENERATOR_DIAGRAM_DIR", str(tmp_path / "cache"))

    def run(name="out", **options):
        out = tmp_path / name
        options.setdefault("keys", KEYS)
        return out, export.build(out, seeds=SEEDS, **options)
    return run


def _files(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in sorted(root.rglob("*"))
            if p.is_file()}


def test_manifest_counts_what_was_written(built):
    out, manifest = built()
    assert manifest == json.loads((out / "manifest.json").read_text(encoding="utf-8"))
    assert manifest["format"] == "otk-export" and manifest["format_version"] == 1
    assert manifest["seeds"] == SEEDS and manifest["sets"] == len(KEYS)
    questions = sum(len(json.loads((out / "questions" / f"{k}.json").read_text("utf-8"))["questions"])
                    for k in KEYS)
    assert manifest["questions"] == questions
    assert manifest["pictures"] == len(list((out / "pictures").glob("*.png"))) > 0
    assert (out / "otk-export.d.ts").read_text(encoding="utf-8").startswith("// Types")


def test_each_question_is_what_its_seed_draws(built):
    out, _ = built()
    for key in KEYS:
        payload = json.loads((out / "questions" / f"{key}.json").read_text(encoding="utf-8"))
        assert payload["key"] == key and payload["seeds"] == SEEDS
        seeds = [q["seed"] for q in payload["questions"]]
        assert seeds == sorted(set(seeds)) and seeds[0] == 0 and seeds[-1] < SEEDS
        for q in payload["questions"]:
            drawn = REGISTRY[key].generate(Random(q["seed"]))
            expected = drawn.model_dump(mode="json")
            expected["mistakes"] = list(drawn.mistakes) or [None] * len(expected["choices"])
            assert {k: v for k, v in q.items() if k != "seed"} == expected


def test_repeats_are_dropped_and_seeds_between_them_repeat_one(built):
    out, _ = built()
    payload = json.loads((out / "questions" / f"{SHEET_SET}.json").read_text(encoding="utf-8"))
    kept = {q["seed"] for q in payload["questions"]}
    bodies = [json.dumps({k: v for k, v in q.items() if k != "seed"}, sort_keys=True)
              for q in payload["questions"]]
    assert len(bodies) == len(set(bodies))
    for seed in set(range(SEEDS)) - kept:
        dumped = REGISTRY[SHEET_SET].generate(Random(seed)).model_dump(mode="json")
        assert any(dumped["stem"] == q["stem"] and dumped["choices"] == q["choices"]
                   for q in payload["questions"])


def test_every_picture_shown_is_shipped(built):
    out, _ = built()
    for key in KEYS:
        payload = json.loads((out / "questions" / f"{key}.json").read_text(encoding="utf-8"))
        for q in payload["questions"]:
            blocks = [*q["stem"], *q["hint"], *(b for c in q["choices"] for b in c["content"])]
            for block in blocks:
                if block["kind"] == "image":
                    assert (out / "pictures" / f"{block['asset_id']}.png").is_file()


def test_catalog_rows_follow_the_api_catalog(built):
    out, _ = built()
    data = json.loads((out / "catalog.json").read_text(encoding="utf-8"))
    rows = {r["key"]: r for r in catalog()}
    assert [s["key"] for s in data["sets"]] == [k for k in rows if k in KEYS]
    for row in data["sets"]:
        for field in export.ROW_FIELDS:
            assert row[field] == rows[row["key"]].get(field)
        assert row["provenance"]["kind"] in ("original", "adapted")
        assert 1 <= row["stems"] <= row["questions"]
    sheet = next(s for s in data["sets"] if s["key"] == SHEET_SET)
    assert sheet["sheet_id"] == "posn2561_chemistry"
    named = {m for k in KEYS
             for q in json.loads((out / "questions" / f"{k}.json").read_text("utf-8"))["questions"]
             for m in q["mistakes"] if m}
    assert named and named <= set(data["mistakes"])


def test_the_same_options_give_identical_files(built):
    first, _ = built("one")
    second, _ = built("two", jobs=2)
    assert _files(first) == _files(second)


def test_filters_select_sets(built):
    rows = export.select(prefixes=["math."], levels=["ป.1"])
    assert rows and all(r["key"].startswith("math.") and r["level"] == "ป.1" for r in rows)
    assert export.select(subjects=["เคมี"], keys=[SHEET_SET])[0]["key"] == SHEET_SET
    with pytest.raises(SystemExit, match="no such set"):
        export.select(keys=["math.not_a_set"])
    with pytest.raises(SystemExit, match="no set matches"):
        built(keys=[SHEET_SET], levels=["ป.1"])
