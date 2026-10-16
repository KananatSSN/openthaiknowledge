"""The sheet bank index — what is in ``openthaiknowledge-bank/`` and how far each file got.

The bank is a folder people drop sheets into. This module keeps one record per
file in ``otk/sheets/bank.json`` so the answer to "what is left to digest?" is
a command (``sheetpipe bank status``) rather than a pile of per-folder handoff
notes.

A record has two kinds of field, and a rescan treats them differently:

* **mechanical** — ``kind``, ``sha256``, ``size`` and the PDF probe (``pages``,
  ``text_chars``, ``layout``, ``glyph_damage``). Recomputed whenever the file's
  hash changes.
* **owned** — ``sheet_id``, ``stage``, ``note``. Written by a person or an agent
  (``sheetpipe bank set``) or derived from a digested sheet's ``sheet.json``.
  A rescan never erases them; if the file changed under a record that had
  progressed, the record is flagged ``stale`` instead.

The PDFs themselves are gitignored, so a worktree or CI box usually has only the
tracked ``.md``/``.py`` bank files. The index is therefore committed, and a scan
never drops a record just because its file is absent here — ``bank prune`` does
that, explicitly.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
from collections import Counter
from dataclasses import asdict, dataclass, fields
from pathlib import Path

from .spec import SHEETS_ROOT, load_sheet, sheet_ids

BANK_FILE = SHEETS_ROOT / "bank.json"
REPO_ROOT = SHEETS_ROOT.parents[1]
DEFAULT_ROOT = REPO_ROOT / "openthaiknowledge-bank"
#: The maintainers' private source bank. A contributor's own ``openthaiknowledge-bank/``
#: folder (their papers under ``contrib/<name>/``) is not a clone of it.
PRIVATE_BANK = "openthaiknowledge-bank"

#: Pipeline stages in order. ``ignored`` is off the ladder: a file the bank
#: holds but that nothing should be built from (a schedule, an archive).
STAGES = ("new", "converted", "extracted", "planned", "generated", "green",
          "ignored")

KIND_BY_SUFFIX = {".pdf": "exam", ".md": "notes", ".py": "fact-data"}

# Files that are bookkeeping about the bank, not sheets in it.
_SKIP_NAMES = {"HANDOFF.md", "README.md"}

# ``[กสพท คณิต1 (มี.ค. 2567/1)]``, ``[O-NET 62/14]``, ``[A-level 2 (…)]`` — the
# exam a question came from. Needs letters *and* a two-digit number, so an
# interval like ``[−1, 2]`` is not one.
SOURCE_TAG = re.compile(
    r"\[(?=[^\]\n]*[A-Za-zก-ฮ]{2})(?=[^\]\n]*\d{2})[^\]\n]{4,60}\]")

# A page with less text than this is a scan (or pure artwork) to the probe.
MIN_CHARS_PER_PAGE = 100


@dataclass
class BankEntry:
    path: str                        # bank-relative POSIX path — the record's key
    kind: str                        # exam | notes | fact-data | other
    sha256: str = ""                 # first 16 hex digits of the content hash
    size: int = 0
    pages: int = 0                   # PDF probe — 0 for non-PDFs
    text_chars: int = 0
    layout: str = ""                 # numbered | choice-block | book | scan | no-text | unknown
    glyph_damage: int = 0            # fontfix.raw_damage of the raw text layer
    duplicate_of: str = ""           # an earlier path with the same content
    scan_pages: int = 0              # pages with no text layer, only an image
    items: int = 0                   # questions in the digest (sheetpipe convert)
    sheet_id: str = ""               # owned: package under otk/sheets/
    stage: str = "new"               # owned: one of STAGES
    note: str = ""                   # owned: free text
    answer_key: str = ""             # owned: bank path of a separate answer-key file
    stale: bool = False              # file changed after it had progressed

    @property
    def folder(self) -> str:
        return self.path.split("/", 1)[0] if "/" in self.path else "."


OWNED = ("sheet_id", "stage", "note", "answer_key")


# ── Probing ──────────────────────────────────────────────────────────────────

def file_hash(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()[:16]


def guess_layout(pages: list[str]) -> str:
    """How the sheet's questions are delimited — which splitter stage 2 needs.

    ``choice-block`` wins over ``numbered``: a choice-block sheet's choices are
    themselves ``1.``–``5.`` runs, which the running-number reading would take
    for five-question exams.
    """
    from .extract import split_items

    if not pages or sum(len(p.strip()) for p in pages) < MIN_CHARS_PER_PAGE * len(pages):
        return "no-text"
    text = "\n".join(pages)
    if len(SOURCE_TAG.findall(text)) >= 2:
        return "choice-block"
    if len(split_items(pages)) >= 5:
        return "numbered"
    return "unknown"


def probe_pdf(path: Path) -> dict:
    """Probe the *raw* text layer: ``glyph_damage`` is what extraction repairs."""
    from .extract import _fitz
    from .fontfix import raw_damage

    from .ocr import is_scan

    with _fitz().open(str(path)) as doc:
        pages = [p.get_text() for p in doc]
        scans = sum(is_scan(p) for p in doc)
    layout = guess_layout(pages)
    if layout != "no-text" and scans * 2 >= len(pages):
        layout = "scan"                  # mostly photographed pages, text on a few
    elif any("สารบัญ" in p for p in pages[:3]):
        layout = "book"                  # a lecture book: contents, notes, examples
    return {"pages": len(pages),
            "text_chars": sum(len(p.strip()) for p in pages),
            "layout": layout,
            "scan_pages": scans,
            "glyph_damage": raw_damage("\n".join(pages))}


def kind_of(path: Path) -> str:
    return KIND_BY_SUFFIX.get(path.suffix.lower(), "other")


LFS_POINTER = b"version https://git-lfs"


def is_lfs_pointer(path: Path) -> bool:
    """A Git LFS pointer standing in for a file whose content was not fetched.

    Bank PDFs live in LFS, and CI checks out without it, so a PDF path can hold
    a 130-byte pointer instead of a PDF. Treat that as "not present here".
    """
    try:
        with path.open("rb") as fh:
            return fh.read(len(LFS_POINTER)) == LFS_POINTER
    except OSError:
        return False


def present(path: Path) -> bool:
    """Is the real content of ``path`` on this machine?"""
    return path.is_file() and not is_lfs_pointer(path)


def bank_files(root: Path) -> list[Path]:
    """Every sheet file under ``root``, skipping hidden entries, bookkeeping,
    and LFS pointers whose content has not been fetched."""
    out = []
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root)
        if (p.is_file() and p.name not in _SKIP_NAMES
                and not any(part.startswith((".", "_")) for part in rel.parts)
                and not is_lfs_pointer(p)):
            out.append(p)
    return out


# ── The index ────────────────────────────────────────────────────────────────

def has_private_bank(root: Path = DEFAULT_ROOT) -> bool:
    """True when ``root`` is a clone of the private source bank.

    Only then do the bank's digests and transcripts exist, and only then may
    ``bank prune`` drop records whose files are missing.
    """
    config = root / ".git" / "config"
    try:
        return PRIVATE_BANK in config.read_text("utf-8")
    except OSError:
        return False


def default_root() -> Path:
    return Path(os.environ.get("SHEET_BANK") or DEFAULT_ROOT)


def load_bank(path: Path = BANK_FILE) -> dict[str, BankEntry]:
    if not path.is_file():
        return {}
    raw = json.loads(path.read_text("utf-8"))
    known = {f.name for f in fields(BankEntry)}
    return {e["path"]: BankEntry(**{k: v for k, v in e.items() if k in known})
            for e in raw.get("entries", [])}


def save_bank(bank: dict[str, BankEntry], path: Path = BANK_FILE) -> None:
    # Only non-default fields are written, so a record stays one short line of
    # diff when a single field moves.
    blank = {f.name: f.default for f in fields(BankEntry)}
    entries = [{k: v for k, v in asdict(e).items()
                if k in ("path", "kind") or v != blank[k]}
               for _, e in sorted(bank.items())]
    path.write_text(json.dumps({"entries": entries}, ensure_ascii=False,
                               indent=1) + "\n", encoding="utf-8", newline="\n")


def scan(root: Path, bank: dict[str, BankEntry] | None = None,
         probe=probe_pdf, reprobe: bool = False) -> tuple[dict[str, BankEntry], Counter]:
    """Bring ``bank`` up to date with the files under ``root``.

    Returns the new bank and a tally of what happened (``added``, ``changed``,
    ``unchanged``, ``absent``). Records whose file is not under ``root`` are
    kept untouched and counted as ``absent``. ``reprobe`` refreshes the
    mechanical fields of unchanged files too, which you need after the probe
    itself changes. It does not mark them stale.
    """
    bank = dict(bank or {})
    tally: Counter = Counter()
    seen: set[str] = set()
    for f in bank_files(root):
        key = f.relative_to(root).as_posix()
        seen.add(key)
        digest = file_hash(f)
        old = bank.get(key)
        same = bool(old) and old.sha256 == digest
        if same and not reprobe:
            tally["unchanged"] += 1
            continue
        entry = BankEntry(path=key, kind=kind_of(f), sha256=digest,
                          size=f.stat().st_size)
        if entry.kind == "exam":
            for k, v in probe(f).items():
                setattr(entry, k, v)
        if entry.kind == "other":
            entry.stage = "ignored"
        if old:
            for k in OWNED:
                setattr(entry, k, getattr(old, k))
            if same:
                entry.stale = old.stale
                tally["unchanged"] += 1
            else:
                entry.stale = old.stage not in ("new", "ignored")
                tally["changed"] += 1
        else:
            tally["added"] += 1
        bank[key] = entry
    tally["absent"] = len(set(bank) - seen)
    mark_duplicates(bank)
    return bank, tally


def mark_duplicates(bank: dict[str, BankEntry]) -> None:
    """Point every later copy of the same content at the first path holding it."""
    first: dict[str, str] = {}
    for key in sorted(bank):
        e = bank[key]
        e.duplicate_of = first.setdefault(e.sha256, key) if e.sha256 else ""
        if e.duplicate_of == key:
            e.duplicate_of = ""


def _bank_key(source_pdf: str) -> str:
    """``sheet.json``'s ``source_pdf`` (repo-relative) as a bank key."""
    p = source_pdf.replace("\\", "/")
    prefix = DEFAULT_ROOT.name + "/"
    return p[len(prefix):] if p.startswith(prefix) else p


def sheet_stage(sheet_id: str) -> str:
    """Where a digested sheet stands, from its own solvers."""
    from .verify import verify_sheet

    results = verify_sheet(load_sheet(sheet_id))
    if results and all(r.ok for r in results):
        return "green"
    return "generated" if any(r.ok for r in results) else "extracted"


def link_digested(bank: dict[str, BankEntry], stage_of=sheet_stage) -> list[str]:
    """Attach every ``otk/sheets/<id>/`` to the bank record of its source PDF.

    Returns the sheet ids whose source is not in the bank — a renamed or moved
    PDF, which someone has to reconcile by hand.
    """
    unmatched = []
    for sid in sheet_ids():
        key = _bank_key(load_sheet(sid).source_pdf)
        if key not in bank:
            unmatched.append(sid)
            continue
        stage = stage_of(sid)
        # A byte-identical copy elsewhere in the bank is the same sheet, digested.
        for entry in bank.values():
            if entry.path == key or entry.duplicate_of == key:
                entry.sheet_id, entry.stage, entry.stale = sid, stage, False
    return unmatched


def select(bank: dict[str, BankEntry], pattern: str) -> list[BankEntry]:
    """Records whose path equals ``pattern`` or matches it as a glob."""
    if pattern in bank:
        return [bank[pattern]]
    return [e for k, e in sorted(bank.items()) if fnmatch.fnmatchcase(k, pattern)]


def set_fields(entries: list[BankEntry], *, sheet_id: str | None = None,
               stage: str | None = None, note: str | None = None,
               answer_key: str | None = None) -> None:
    if stage is not None and stage not in STAGES:
        raise ValueError(f"unknown stage {stage!r}; one of {', '.join(STAGES)}")
    for e in entries:
        if sheet_id is not None:
            e.sheet_id = sheet_id
        if stage is not None:
            e.stage = stage
            e.stale = False
        if note is not None:
            e.note = note
        if answer_key is not None:
            e.answer_key = answer_key


def status_table(bank: dict[str, BankEntry]) -> str:
    """One row per top-level folder: counts by kind, layout and stage."""
    cols = [s for s in STAGES]
    rows: dict[str, Counter] = {}
    for e in bank.values():
        c = rows.setdefault(e.folder, Counter())
        c["files"] += 1
        c[e.kind] += 1
        c[e.stage] += 1
        if e.layout:
            c["L:" + e.layout] += 1
        c["stale"] += e.stale
        c["dup"] += bool(e.duplicate_of)
        c["items"] += e.items
        c["damaged"] += e.glyph_damage > 0

    head = ["folder", "files", "exam", "notes", "data"] + list(cols) + [
        "numbered", "choice", "book", "scan", "no-text", "items", "damaged", "dup", "stale"]
    keys = ["files", "exam", "notes", "fact-data"] + cols + [
        "L:numbered", "L:choice-block", "L:book", "L:scan", "L:no-text", "items", "damaged", "dup", "stale"]
    total: Counter = sum(rows.values(), Counter())
    lines = [[name] + [str(c[k] or "") for k in keys]
             for name, c in sorted(rows.items())]
    lines.append(["TOTAL"] + [str(total[k] or "") for k in keys])
    widths = [max(len(r[i]) for r in [head] + lines) for i in range(len(head))]
    fmt = lambda r: "  ".join(v.ljust(w) if i == 0 else v.rjust(w)
                              for i, (v, w) in enumerate(zip(r, widths)))
    return "\n".join([fmt(head)] + [fmt(r) for r in lines])
