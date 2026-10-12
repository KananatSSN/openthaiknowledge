"""What a release changes for consumers, from the golden draws of two versions.

A consumer replays stored seeds and keys learner data by set, so the three
things it must know about a release are which sets are new, which now draw
different questions for the same seed, and which were retired. All three
follow from ``otk/tests/golden_draws.json`` at the two versions, plus whether
``otk/api.py`` changed.

    python scripts/release_notes.py v0.1.0 v0.2.0      # Markdown on stdout
    python scripts/release_notes.py v0.2.0 HEAD --json

Any git revision works for either end.
"""

from __future__ import annotations

import argparse
import ast
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = "otk/tests/golden_draws.json"


def _show(rev: str, path: str) -> str | None:
    result = subprocess.run(["git", "show", f"{rev}:{path}"], cwd=ROOT,
                            capture_output=True, text=True)
    return result.stdout if result.returncode == 0 else None


def _golden(rev: str) -> dict:
    # Fall back to the package's old name for revisions before the move.
    raw = _show(rev, FIXTURE) or _show(rev, "hwgen/tests/golden_draws.json")
    if raw is None:
        raise SystemExit(f"{rev} has no golden draws fixture")
    return json.loads(raw)


def _exports(rev: str) -> set[str]:
    """``otk.api.__all__`` at a revision (empty before otk.api existed)."""
    source = _show(rev, "otk/api.py") or _show(rev, "hwgen/api.py") or ""
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", None) == "__all__" for t in node.targets):
            return set(ast.literal_eval(node.value))
    return set()


def changes(old: str, new: str) -> dict:
    before, after = _golden(old), _golden(new)
    old_sets, new_sets = before["sets"], after["sets"]
    exports_before, exports_after = _exports(old), _exports(new)
    return {
        "from": old,
        "to": new,
        "added": sorted(set(new_sets) - set(old_sets)),
        "changed": sorted(k for k in set(old_sets) & set(new_sets)
                          if old_sets[k] != new_sets[k]),
        "retired": sorted(set(after["retired"]) - set(before["retired"])),
        "seeds_changed": before["seeds"] != after["seeds"],
        "api_added": sorted(exports_after - exports_before),
        "api_removed": sorted(exports_before - exports_after),
    }


def markdown(c: dict) -> str:
    def section(title: str, keys: list[str], note: str) -> list[str]:
        if not keys:
            return []
        lines = [f"### {title} ({len(keys)})", "", note, ""]
        lines += [f"- `{k}`" for k in keys]
        return lines + [""]

    out = [f"## Changes for consumers: {c['from']} → {c['to']}", ""]
    if c["seeds_changed"]:
        out += ["**The golden-draw seeds changed:** the comparison below is not meaningful.", ""]
    if c["api_removed"]:
        out += ["**Breaking: removed from `otk.api`:** "
                + ", ".join(f"`{n}`" for n in c["api_removed"]), ""]
    if c["api_added"]:
        out += ["Added to `otk.api`: " + ", ".join(f"`{n}`" for n in c["api_added"]), ""]
    out += section("Changed sets", c["changed"],
                   "These draw different questions for the same seed. A consumer that "
                   "replays stored seeds will show a different question for them.")
    out += section("New sets", c["added"], "Keys that did not exist before.")
    out += section("Retired sets", c["retired"],
                   "No longer registered; their keys will never be reused.")
    if not (c["changed"] or c["added"] or c["retired"] or c["api_added"]
            or c["api_removed"]):
        out += ["No set was added, changed or retired, and the API is unchanged.", ""]
    return "\n".join(out)


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("old", help="the previous release (tag or revision)")
    parser.add_argument("new", nargs="?", default="HEAD")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = changes(args.old, args.new)
    print(json.dumps(result, indent=2) if args.json else markdown(result))


if __name__ == "__main__":
    main()
