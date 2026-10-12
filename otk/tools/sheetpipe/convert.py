"""Stage 2: a bank file in, a text digest out.

``sheetpipe convert <bank path | glob>`` picks a splitter from the file's
probed layout and writes two files under ``sheet_database/_digest/``, at the
file's bank path:

* ``<name>.json`` — the machine-readable digest. It has the source path and
  hash, the splitter used, and one record per question: stem, choices, the
  exam tag, pages, whether it has a figure, answer, and worked solution.
* ``<name>.md`` — the same questions for a person to read and check.

The digest is committed. The PDFs are gitignored, so it is the only form of a
sheet's text that a checkout, a reviewer, or a later session can see.

A sheet with a hand transcript (``sheet_database/_transcribed/<bank
path>.md``, see :mod:`.transcript`) is read from that, and needs no PDF.
Otherwise, a sheet whose bank record names an ``answer_key`` (a separate file holding
its answers, as with the ``(rath)`` trigonometry notes) is split by
``answerkey``, whatever its layout. Otherwise the layout picks the splitter;
only ``choice-block`` has one so far. Other layouts are reported and skipped;
the plan in ``docs/for_admin/SHEET_DIGESTION_PLAN.md`` says which splitter
each one waits on.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from . import answerkey
from . import bank as bk
from . import choiceblock
from . import transcript

DIGEST_ROOT = bk.DEFAULT_ROOT / "_digest"
SPLITTERS = {"choice-block": choiceblock.split}


@dataclass
class Result:
    path: str
    items: int = 0
    answered: int = 0
    skipped: str = ""                 # why nothing was written, if so


def digest_paths(bank_path: str) -> tuple[Path, Path]:
    base = DIGEST_ROOT / bank_path
    return base.with_suffix(".json"), base.with_suffix(".md")


_INT = re.compile(r"^[−-]?\d+$")


def inline(choice: str) -> str:
    """A choice on one line: a two-number stack is a fraction, anything else
    stacked is joined with `` / ``. The JSON keeps the lines as they were."""
    parts = [p.strip() for p in choice.splitlines() if p.strip()]
    if len(parts) == 2 and all(_INT.match(p) for p in parts):
        return f"{parts[0]}/{parts[1]}"
    return " / ".join(parts)


def render_md(entry: bk.BankEntry, items: list[choiceblock.Item],
              transcribed: bool = False) -> str:
    how = "transcribed by eye" if transcribed else f"layout `{entry.layout}`"
    out = [f"# {Path(entry.path).stem}", "",
           f"Source: `sheet_database/{entry.path}` · {len(items)} questions · {how}", ""]
    for it in items:
        head = f"## {it.number}"
        if it.section:
            head += f" · {it.section}"
        if it.tag:
            head += f" — {it.tag}"
        out += [head, ""]
        if it.figure:
            out += [f"*(figure on p.{', '.join(map(str, it.pages))})*", ""]
        out += [it.stem, ""]
        for k, v in it.choices.items():
            out.append(f"{k}. {inline(v) or '*(picture)*'}")
        if it.choices:
            out.append("")
        if it.answer:
            out += [f"**ตอบ** {it.answer}", ""]
    return "\n".join(out).rstrip() + "\n"


def convert(entry: bk.BankEntry, root: Path) -> Result:
    src = root / entry.path
    transcribed = transcript.path_for(entry.path).is_file()
    if transcribed:
        split = lambda _pdf: transcript.split(entry.path)
    elif entry.answer_key:
        key = root / entry.answer_key
        split = lambda pdf: answerkey.split(pdf, key)
        if not bk.present(key):
            return Result(entry.path, skipped="answer key not fetched: sheetpipe bank fetch "
                                              f'"{entry.answer_key}"')
    else:
        split = SPLITTERS.get(entry.layout)
        if split is None:
            return Result(entry.path, skipped=f"no splitter for layout {entry.layout or entry.kind!r}")
    if not transcribed and not bk.present(src):
        return Result(entry.path, skipped="not fetched: sheetpipe bank fetch "
                                          f'"{entry.path}"')
    items = split(src)
    if not items:
        return Result(entry.path, skipped="splitter found no questions")

    js, md = digest_paths(entry.path)
    js.parent.mkdir(parents=True, exist_ok=True)
    js.write_text(json.dumps(
        {"source": entry.path, "sha256": entry.sha256, "layout": entry.layout,
         **({"answer_key": entry.answer_key} if entry.answer_key and not transcribed else {}),
         **({"transcribed": True} if transcribed else {}),
         "items": [it.to_json() for it in items]},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    md.write_text(render_md(entry, items, transcribed), encoding="utf-8", newline="\n")
    return Result(entry.path, len(items), sum(bool(it.answer) for it in items))


def load_digest(bank_path: str) -> dict:
    return json.loads(digest_paths(bank_path)[0].read_text("utf-8"))
