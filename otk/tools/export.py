"""Export otk's questions as plain JSON and PNG files, for apps that do not run Python.

A TypeScript app, a mobile app or a spreadsheet can install a release of otk by
reading these files, with no port of the generators. For each set it gets the
questions drawn from seeds ``0 .. N-1`` (exact repeats dropped), each with its
answer, hint and the named mistake behind every wrong choice, plus the
catalog and every picture those questions show:

    out/
      manifest.json          format, otk version and commit, seeds, counts
      catalog.json           one row per set, and the names of every mistake
      questions/<key>.json   that set's distinct questions, each with its seed
      pictures/<asset>.png   every picture a question shows
      otk-export.d.ts        TypeScript types for the files above

    python -m otk.tools.export out/
    python -m otk.tools.export out/ --prefix math. --level ม.2 --seeds 200
    python -m otk.tools.export out/ --key math.count_objects_p1 --seeds 20

The same release and options always give byte-identical files, so diffing two
exports shows exactly what a release changed. Questions are drawn with each
set's default parameters. ``docs/EXPORT.md`` describes the format.

Pictures are drawn into a fresh directory for each run, so an export never
ships a picture cached by an older release. Set ``GENERATOR_DIAGRAM_DIR`` to
reuse a cache, and ``GENERATOR_OBJECT_SPRITES`` to draw the counting pictures
with your own sprites (see ``otk/pictures/counting_pictures.py``).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ProcessPoolExecutor
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from random import Random

FORMAT = "otk-export"
FORMAT_VERSION = 1
DEFAULT_SEEDS = 200
ROOT = Path(__file__).resolve().parents[2]
ROW_FIELDS = ("key", "display_name", "subject", "level", "topic", "unit", "learning_stage",
              "learning_stage_key", "learning_stage_label", "source_key", "course_type",
              "strand_code", "strand", "standard_code", "indicator_codes",
              "curriculum_node_id")

TYPES = """\
// Types for an otk export (format "otk-export", version 1). Written by
// `python -m otk.tools.export`; see docs/EXPORT.md in openthaiknowledge.

export type Block =
  | { kind: 'text'; text: string }
  | { kind: 'math'; tex: string }            // KaTeX-compatible TeX, without $
  | { kind: 'image'; asset_id: string; alt: string; markers: Marker[] }  // pictures/<asset_id>.png
  | { kind: 'code'; code: string; language: string };

/** An arrow or dot on a picture; x and y are fractions of its size, from the top left. */
export interface Marker { x: number; y: number; angle: number; style: 'arrow' | 'dot' }

export interface Choice { content: Block[] }

export interface Question {
  seed: number;                  // REGISTRY[key].generate(Random(seed)) in otk gives this question
  type: string;                  // the set's key
  topic: string;
  level: string;
  stem: Block[];
  choices: Choice[];
  answer: number;                // index into choices
  hint: Block[];
  mistakes: (string | null)[];   // per choice: a key of Catalog.mistakes, null if none is named
}

export interface QuestionFile { key: string; seeds: number; questions: Question[] }

export interface Provenance { kind: 'original' | 'adapted'; sources?: string[]; [field: string]: unknown }

export interface SetRow {
  key: string;
  display_name: string;
  subject: string;
  level: string;
  topic: string;
  unit: string | null;
  learning_stage: number;
  learning_stage_key: string;
  learning_stage_label: string;
  source_key: string;
  course_type: string | null;
  strand_code: string | null;
  strand: string | null;
  standard_code: string | null;
  indicator_codes: string[] | null;
  curriculum_node_id: string | null;
  sheet: string;                 // the past paper a set was digested from, or ""
  sheet_id: string;
  provenance: Provenance;
  questions: number;             // distinct questions in questions/<key>.json
  stems: number;                 // distinct stems among them: the set's real variety, since the
                                 // same stem recurs with its choices in another order
}

export interface Catalog {
  sets: SetRow[];
  mistakes: Record<string, Record<string, string>>;  // mistake key -> name by language ("th", "en")
}

export interface Manifest {
  format: 'otk-export';
  format_version: 1;
  otk_version: string;
  otk_commit: string | null;     // ends in "-dirty" when the working tree had changes
  seeds: number;                 // seeds 0 .. seeds-1 were drawn for every set
  filters: { keys: string[]; prefixes: string[]; subjects: string[]; levels: string[] };
  sets: number;
  questions: number;
  pictures: number;
}
"""


def _dump(payload) -> str:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def _write(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_dump(payload) + "\n", encoding="utf-8")


def _images(blocks: list[dict]) -> list[str]:
    return [b["asset_id"] for b in blocks if b.get("kind") == "image"]


def draw_set(key: str, seeds: int) -> tuple[list[dict], set[str]]:
    """The set's distinct questions over seeds ``0 .. seeds-1``, and the pictures they show."""
    from otk.api import REGISTRY

    questions, seen, pictures = [], set(), set()
    for seed in range(seeds):
        question = REGISTRY[key].generate(Random(seed))
        body = question.model_dump(mode="json")
        body["mistakes"] = list(question.mistakes) or [None] * len(body["choices"])
        fingerprint = _dump(body)
        if fingerprint in seen:
            continue
        seen.add(fingerprint)
        questions.append({"seed": seed, **body})
        pictures.update(_images(body["stem"]))
        pictures.update(_images(body["hint"]))
        for choice in body["choices"]:
            pictures.update(_images(choice["content"]))
    return questions, pictures


def _export_chunk(keys: list[str], seeds: int, out: str) -> dict[str, tuple[int, int, list[str]]]:
    """Worker: write each set's question file; return its question and stem counts and pictures."""
    done = {}
    for key in keys:
        questions, pictures = draw_set(key, seeds)
        _write(Path(out) / "questions" / f"{key}.json",
               {"key": key, "seeds": seeds, "questions": questions})
        stems = len({_dump(q["stem"]) for q in questions})
        done[key] = (len(questions), stems, sorted(pictures))
    return done


def _copy_pictures(assets: list[str], out: str) -> list[str]:
    """Worker: copy (drawing first where needed) each picture; return the ids with no file."""
    from otk.api import shipped_asset

    missing = []
    for asset_id in assets:
        source = shipped_asset(asset_id)
        if source is None:
            missing.append(asset_id)
        else:
            shutil.copyfile(source, Path(out) / "pictures" / f"{asset_id}.png")
    return missing


def otk_commit() -> str | None:
    """The checked-out commit, when otk runs from a git clone; ``-dirty`` if otk/ has changes."""
    try:
        commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True,
                                         stderr=subprocess.DEVNULL).strip()
        dirty = subprocess.check_output(["git", "status", "--porcelain", "--", "otk"], cwd=ROOT,
                                        text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    return commit + ("-dirty" if dirty else "")


def otk_version() -> str:
    """The version being exported: pyproject's in a clone (an editable install's metadata
    can be stale), else the installed package's."""
    pyproject = ROOT / "pyproject.toml"
    if pyproject.is_file():
        found = re.search(r'^version\s*=\s*"([^"]+)"', pyproject.read_text(encoding="utf-8"), re.M)
        if found:
            return found.group(1)
    try:
        return version("openthaiknowledge")
    except PackageNotFoundError:
        return "dev"


def select(keys=(), prefixes=(), subjects=(), levels=()) -> list[dict]:
    """Catalog rows that pass every filter given; an empty filter lets everything through."""
    from otk.api import REGISTRY, catalog

    unknown = sorted(set(keys) - set(REGISTRY))
    if unknown:
        raise SystemExit(f"no such set: {', '.join(unknown)}")
    return [row for row in catalog()
            if (not keys or row["key"] in keys)
            and (not prefixes or row["key"].startswith(tuple(prefixes)))
            and (not subjects or row["subject"] in subjects)
            and (not levels or row["level"] in levels)]


def _chunks(items: list, n: int) -> list[list]:
    return [items[i::n] for i in range(n) if items[i::n]]


def build(out: Path, *, seeds: int = DEFAULT_SEEDS, keys=(), prefixes=(), subjects=(),
          levels=(), jobs: int = 1) -> dict:
    """Write an export of the selected sets into ``out`` (replacing it); return the manifest."""
    from otk.api import REGISTRY, mistake_names, provenance

    if seeds < 1:
        raise SystemExit("--seeds must be at least 1")
    rows = select(keys, prefixes, subjects, levels)
    if not rows:
        raise SystemExit("no set matches the filters")
    if out.exists():
        shutil.rmtree(out)
    (out / "pictures").mkdir(parents=True)

    order = [row["key"] for row in rows]
    results: dict[str, tuple[int, int, list[str]]] = {}
    jobs = max(1, min(jobs, len(order)))
    if jobs == 1:
        results = _export_chunk(order, seeds, str(out))
    else:
        with ProcessPoolExecutor(jobs) as pool:
            for part in pool.map(_export_chunk, _chunks(order, jobs * 4),
                                 [seeds] * (jobs * 4), [str(out)] * (jobs * 4)):
                results.update(part)

    assets = sorted({a for *_, pictures in results.values() for a in pictures})
    if jobs == 1 or len(assets) < 50:
        missing = _copy_pictures(assets, str(out))
    else:
        with ProcessPoolExecutor(jobs) as pool:
            parts = _chunks(assets, jobs * 4)
            missing = [a for part in pool.map(_copy_pictures, parts, [str(out)] * len(parts))
                       for a in part]
    if missing:
        raise SystemExit(f"pictures with no file: {', '.join(sorted(missing))}")

    sets = []
    for row in rows:
        t = REGISTRY[row["key"]]
        sets.append({**{f: row.get(f) for f in ROW_FIELDS}, "sheet": t.sheet,
                     "sheet_id": t.sheet_id, "provenance": provenance(row["key"]).as_dict(),
                     "questions": results[row["key"]][0], "stems": results[row["key"]][1]})
    _write(out / "catalog.json", {"sets": sets, "mistakes": mistake_names()})
    (out / "otk-export.d.ts").write_text(TYPES, encoding="utf-8")

    manifest = {
        "format": FORMAT, "format_version": FORMAT_VERSION,
        "otk_version": otk_version(), "otk_commit": otk_commit(), "seeds": seeds,
        "filters": {"keys": sorted(keys), "prefixes": sorted(prefixes),
                    "subjects": sorted(subjects), "levels": sorted(levels)},
        "sets": len(sets), "questions": sum(n for n, *_ in results.values()),
        "pictures": len(assets),
    }
    (out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n",
                                       encoding="utf-8")
    return manifest


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description=__doc__.split("\n\n")[0],
        epilog="Filters combine: a set is exported when it passes every kind given.")
    parser.add_argument("out", type=Path, help="directory to write (replaced if it exists)")
    parser.add_argument("--seeds", type=int, default=DEFAULT_SEEDS,
                        help=f"draw seeds 0..N-1 for every set (default {DEFAULT_SEEDS})")
    parser.add_argument("--key", action="append", default=[], help="only this set (repeatable)")
    parser.add_argument("--prefix", action="append", default=[],
                        help="only keys starting with this, e.g. math. (repeatable)")
    parser.add_argument("--subject", action="append", default=[],
                        help="only this subject, e.g. คณิตศาสตร์ (repeatable)")
    parser.add_argument("--level", action="append", default=[],
                        help="only this level, e.g. ม.2 (repeatable)")
    parser.add_argument("--jobs", type=int, default=os.cpu_count() or 1,
                        help="worker processes (default: one per core)")
    args = parser.parse_args(argv)
    # A fresh picture cache, unless the caller chose one, so no stale drawing ships.
    os.environ.setdefault("GENERATOR_DIAGRAM_DIR", tempfile.mkdtemp(prefix="otk-export-"))
    manifest = build(args.out, seeds=args.seeds, keys=args.key, prefixes=args.prefix,
                     subjects=args.subject, levels=args.level, jobs=args.jobs)
    print(f"{manifest['sets']} sets, {manifest['questions']} questions, "
          f"{manifest['pictures']} pictures -> {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
