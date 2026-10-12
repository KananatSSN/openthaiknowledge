"""The explorer's data builder writes what the site reads (otk/tools/explorer_data.py)."""

from __future__ import annotations

import json

from otk.tools.explorer_data import ROOT, build


def test_builds_rows_examples_and_their_pictures(tmp_path):
    result = build(tmp_path, limit=40)
    assert result["sets"] == 40 and not result["missing"]

    catalog = json.loads((tmp_path / "catalog.json").read_text("utf-8"))
    assert len(catalog["sets"]) == 40 and catalog["mistakes"]
    for row in catalog["sets"]:
        detail = json.loads((tmp_path / "sets" / f"{row['key']}.json").read_text("utf-8"))
        assert detail["provenance"]["kind"] == row["provenance"]
        assert detail["source_file"].startswith("otk/sets/")
        assert (ROOT / detail["source_file"]).is_file()
        assert 1 <= len(detail["examples"]) <= 3
        for example in detail["examples"]:
            assert len(example["mistakes"]) == len(example["choices"])
            for block in example["stem"]:
                if block["kind"] == "image":
                    assert (tmp_path / "assets" / f"{block['asset_id']}.png").is_file()
