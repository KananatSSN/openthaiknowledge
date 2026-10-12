"""Golden draws: a fingerprint of what every set produces for a few fixed seeds.

otk promises its consumers that a set's key is permanent and that a seed
always draws the same question (``otk/api.py``). TutorRank stores the seed of
every question it served and replays it, and keys every learner statistic by
set key. ``otk/tests/test_golden_draws.py`` holds otk to both promises
against ``otk/tests/golden_draws.json``:

* ``sets`` maps every live key to one hash over its first ``SEEDS`` draws
  (the whole question, plus the mistake each choice names);
* ``retired`` lists keys that were removed. A retired key may never come back.

When a change to a set's draws is intended, regenerate its entry and say so in
the release notes::

    python -m otk.tools.golden_draws --update                # every set
    python -m otk.tools.golden_draws --update math.foo_p5    # just these

A key that disappears must be retired explicitly::

    python -m otk.tools.golden_draws --retire math.old_set
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from random import Random

SEEDS = (0, 1, 2, 20260824, 2**31 - 1)
FIXTURE = Path(__file__).resolve().parents[1] / "tests" / "golden_draws.json"


def draw_hash(key: str) -> str:
    """Hash of the set's draws for ``SEEDS``, at its default parameters."""
    from otk.core import REGISTRY

    digest = hashlib.sha256()
    for seed in SEEDS:
        question = REGISTRY[key].generate(Random(seed))
        record = {"question": question.model_dump(mode="json"), "mistakes": question.mistakes}
        digest.update(json.dumps(record, sort_keys=True, ensure_ascii=False,
                                 separators=(",", ":")).encode())
        digest.update(b"\n")
    return digest.hexdigest()[:16]


def load() -> dict:
    if not FIXTURE.exists():
        return {"seeds": list(SEEDS), "sets": {}, "retired": []}
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def save(data: dict) -> None:
    data = {"seeds": list(SEEDS), "sets": dict(sorted(data["sets"].items())),
            "retired": sorted(set(data["retired"]))}
    FIXTURE.write_text(json.dumps(data, ensure_ascii=False, indent=0) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> None:
    from otk.core import REGISTRY

    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("keys", nargs="*", help="limit to these set keys")
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--update", action="store_true", help="record current draws")
    action.add_argument("--retire", action="store_true", help="move removed keys to retired")
    args = parser.parse_args(argv)

    data = load()
    if args.retire:
        for key in args.keys:
            if key in REGISTRY:
                parser.error(f"{key} is still registered; remove the set first")
            data["sets"].pop(key, None)
            data["retired"].append(key)
    else:
        unknown = [key for key in args.keys if key not in REGISTRY]
        if unknown:
            parser.error(f"not registered: {', '.join(unknown)}")
        for key in args.keys or sorted(REGISTRY):
            data["sets"][key] = draw_hash(key)
    save(data)
    print(f"{len(data['sets'])} sets, {len(data['retired'])} retired -> {FIXTURE}")


if __name__ == "__main__":
    main()
