"""Offline worksheet CLI — a thin shim over ``otk.core`` (no web app).

Generates a worksheet PDF from a JSON config, using the same question registry
and renderer the web app uses. This preserves the offline path: no server, no
database.

    python -m otk worksheet.json -o out.pdf
    otk worksheet.json                 # writes worksheet.pdf
    otk --list                         # list question-type keys
    otk worksheet.json --choices       # print each question's options

A config is a JSON object matching the ``Worksheet`` model; the only required
key is ``generators``. Example:

    {
      "title": "แบบฝึกหัดการบวก",
      "generators": { "math.addition": 2, "math.multiplication": 1 },
      "num_problems": 20,
      "columns": 2,
      "answer_key": true,
      "show_choices": false
    }
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .core import REGISTRY, sort_key
from .core.render import render_pdf
from .core.render.assets import shipped_asset
from .core.worksheet import Worksheet, build_worksheet


def _use_utf8_stdout() -> None:
    """Thai type names are unprintable on a cp1252 Windows console, which
    raised UnicodeEncodeError rather than listing anything."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def _print_list() -> None:
    for key in sorted(REGISTRY, key=sort_key):
        spec = REGISTRY[key]
        print(f"{key:34} {spec.level_for('th'):8} {spec.display_name_for('th')}")


def _default_thai_font() -> str:
    """First installed Thai-capable font, so Thai headers render out of the box."""
    from matplotlib import font_manager
    installed = {f.name for f in font_manager.fontManager.ttflist}
    for cand in ("Leelawadee UI", "Garuda", "Loma", "Laksaman", "Waree", "Tahoma"):
        if cand in installed:
            return cand
    return ""


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="otk", description="Generate a worksheet PDF from a JSON config.")
    parser.add_argument("config", nargs="?", help="worksheet JSON config")
    parser.add_argument("-o", "--output", help="output PDF path (default: <config>.pdf)")
    parser.add_argument("-n", "--num", type=int, help="override num_problems")
    parser.add_argument("--seed", type=int, help="override seed (reproducible sheet)")
    parser.add_argument("--no-answer-key", action="store_true", help="omit the answer key")
    parser.add_argument("--choices", action="store_true",
                        help="print each question's options (for multiple-choice types)")
    parser.add_argument("--list", action="store_true",
                        help="list available question-type keys and exit")
    args = parser.parse_args(argv)
    _use_utf8_stdout()

    if args.list:
        _print_list()
        return
    if not args.config:
        parser.error("a config file is required (or use --list)")

    config_path = Path(args.config)
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        parser.error(f"cannot read config: {e}")

    if args.num is not None:
        data["num_problems"] = args.num
    if args.seed is not None:
        data["seed"] = args.seed
    if args.no_answer_key:
        data["answer_key"] = False
    if args.choices:
        data["show_choices"] = True
    data.setdefault("font_family", _default_thai_font())

    try:
        config = Worksheet(**data)
        questions = build_worksheet(config)
    except (ValueError, TypeError) as e:
        parser.error(str(e))

    out = Path(args.output) if args.output else config_path.with_suffix(".pdf")
    # Offline, the resolvable assets are the ones that ship with the repo:
    # built-in diagrams and digested sheet figures. Without this an image
    # question printed as a blank space.
    render_pdf(config, questions, out, asset_resolver=shipped_asset)
    print(f"wrote {out} ({len(questions)} problems)")


if __name__ == "__main__":
    main()
