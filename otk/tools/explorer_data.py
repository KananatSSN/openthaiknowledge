"""Build the data the explorer site reads: the catalog, examples, and pictures.

The explorer (``explorer/``) is a static site with no server, so everything a
visitor can see is generated here ahead of time:

* ``catalog.json`` — one row per set, for browsing and search;
* ``sets/<key>.json`` — the set's details, its source file, its provenance, and a few example
  questions drawn from fixed seeds, each wrong choice labelled with the
  mistake it stands for where the set names one;
* ``assets/<id>.png`` — every picture those examples show.

    python -m otk.tools.explorer_data                # into explorer/static/data
    python -m otk.tools.explorer_data --out DIR --limit 50

The output is a build artifact (git-ignored); the site's build runs this first.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from random import Random

from otk.api import REGISTRY, catalog, mistake_names, provenance, shipped_asset

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = ROOT / "explorer" / "static" / "data"
EXAMPLE_SEEDS = (1, 2, 3, 4, 5, 6)
EXAMPLES = 3
ROW_FIELDS = ("key", "display_name", "subject", "level", "topic", "unit", "learning_stage",
              "learning_stage_label", "course_type", "strand_code", "strand",
              "standard_code", "indicator_codes", "curriculum_node_id")


def _write(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
                    encoding="utf-8")


def source_file(key: str) -> str:
    """The set's file, relative to the repository root (``otk/sets/...``)."""
    module = sys.modules[type(REGISTRY[key]).__module__]
    return Path(module.__file__).resolve().relative_to(ROOT).as_posix()


def _images(blocks: list[dict]) -> list[str]:
    return [b["asset_id"] for b in blocks if b.get("kind") == "image"]


def examples(key: str) -> list[dict]:
    """Up to ``EXAMPLES`` distinct questions, each with its choices' named mistakes."""
    out, seen = [], set()
    for seed in EXAMPLE_SEEDS:
        question = REGISTRY[key].generate(Random(seed))
        body = question.model_dump(mode="json")
        fingerprint = json.dumps([body["stem"], body["choices"]], ensure_ascii=False)
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        body["mistakes"] = list(question.mistakes) or [None] * len(body["choices"])
        out.append(body)
        if len(out) == EXAMPLES:
            break
    return out


def build(out: Path, limit: int | None = None) -> dict:
    if out.exists():
        shutil.rmtree(out)
    rows = catalog()[:limit] if limit else catalog()
    try:
        otk_version = version("openthaiknowledge")
    except PackageNotFoundError:
        otk_version = "dev"

    pictures: set[str] = set()
    index = []
    for row in rows:
        key = row["key"]
        origin = provenance(key)
        summary = {field: row.get(field) for field in ROW_FIELDS}
        summary["provenance"] = origin.kind
        index.append(summary)
        shown = examples(key)
        for question in shown:
            pictures.update(_images(question["stem"]))
            for choice in question["choices"]:
                pictures.update(_images(choice["content"]))
        _write(out / "sets" / f"{key}.json",
               {**summary, "provenance": origin.as_dict(), "source_file": source_file(key),
                "examples": shown})

    missing = []
    for asset_id in sorted(pictures):
        source = shipped_asset(asset_id)
        if source is None:
            missing.append(asset_id)
            continue
        target = out / "assets" / f"{asset_id}.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)

    _write(out / "catalog.json", {"version": otk_version, "sets": index,
                                  "mistakes": mistake_names()})
    return {"sets": len(index), "pictures": len(pictures) - len(missing), "missing": missing}


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--limit", type=int, help="only the first N sets (for a quick look)")
    args = parser.parse_args(argv)
    result = build(args.out, args.limit)
    print(f"{result['sets']} sets, {result['pictures']} pictures -> {args.out}")
    if result["missing"]:
        raise SystemExit(f"pictures with no file: {', '.join(result['missing'])}")


if __name__ == "__main__":
    main()
