"""``python -m otk.tools.sheetpipe`` — drive the sheet pipeline.

    extract  <pdf> <sheet_id>   stage 1: page text, item split, figure crops
    scaffold <pdf> <sheet_id>   stage 2: sheet.json + one solver stub per item
    figures  <pdf> <sheet_id>   review the figure crops; --attach ships them
    verify   [sheet_id ...]     stage 4: run the solver contract (exit 1 on fail)
    list                        every digested sheet and how green it is
    convert  <bank path|glob>   stage 2 for question banks: digest JSON + Markdown
    transcript todo|pages|check stage 2 for picture-maths sheets: what needs reading,
                                render the pages, check a hand transcript
    knowledge validate|coverage stage 3: check otk/knowledge/, and what it accounts for
    plan     [topic]            stage 4: knowledge units that no problem set practises
    ocr      <pdf>              OCR a scanned PDF (extract does this per scanned page)
    bank scan|status|set|fetch|prune  the sheet_database/ index (otk/sheets/bank.json);
                                fetch downloads PDFs from Git LFS on demand

Stage 3 — actually solving — is the part you do by hand (or with a model); the
stubs raise ``NotImplementedError`` so ``verify`` counts them as unfinished
rather than quietly passing.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ... import sheets
from . import bank as bk, extract as ex, ocr
from .spec import SHEETS_ROOT, ItemSpec, SheetSpec, load_sheet, sheet_ids
from .verify import report, verify_sheet

STUB = '''"""ข้อ {n} — {title}

{source}

TODO(stage 3): replace the body below.
  * PARAMS  — the constants this question happens to use (its tunables)
  * ANSWER  — the answer for exactly those constants
  * solve() — the method, in closed form where one exists
  * check() — a *second, independent* derivation (brute force / simulation)
  * VARIANTS — other constant sets that must also come out right
"""

from __future__ import annotations

PARAMS = {{}}
ANSWER = None
VARIANTS: list[dict] = []


def solve():
    raise NotImplementedError("q{n:02d} not solved yet")
'''


def _work_dir(sheet_id: str) -> Path:
    return SHEETS_ROOT / sheet_id


def cmd_extract(args) -> int:
    out = _work_dir(args.sheet_id) / "extract"
    out.mkdir(parents=True, exist_ok=True)
    pages, sources = ocr.read_pages(args.pdf)
    (out / "text.txt").write_text(
        "\n".join(f"=== PAGE {i}{' (ocr)' if src == 'ocr' else ''} ===\n{t}"
                  for i, (t, src) in enumerate(zip(pages, sources), 1)),
        encoding="utf-8")
    if "ocr" in sources:
        print(f"OCR'd {sources.count('ocr')} scanned page(s). Check every constant "
              "against the page render, and transcribe any maths by eye.")

    declared = ex.declared_item_count(pages)
    items = ex.split_items(pages, expect=declared)
    for n, body in items.items():
        (out / f"item{n:02d}.txt").write_text(body, encoding="utf-8")

    figs = ex.figure_pages(args.pdf)
    ex.render_pages(args.pdf, out / "pages", figs)
    cropped = ex.extract_figures(args.pdf, out / "figures", expect=declared)
    print(f"{len(pages)} pages, {len(items)} items "
          f"(sheet declares {declared or '?'}), "
          f"figures on pages {figs} rendered to {out / 'pages'}")
    print(f"{len(cropped)} per-item figure crops in {out / 'figures'}: "
          + ", ".join(f"q{f.item}" for f in cropped))
    print("Next: LOOK at those renders. Every figure question needs its geometry "
          "written down as data before it can be solved — and `sheetpipe figures` "
          "to decide which crops the generated questions should show.")
    return 0


def cmd_scaffold(args) -> int:
    pkg = _work_dir(args.sheet_id)
    pkg.mkdir(parents=True, exist_ok=True)
    pages, _ = ocr.read_pages(args.pdf)
    items = ex.split_items(pages, expect=ex.declared_item_count(pages))

    spec = SheetSpec(sheet_id=args.sheet_id, title=args.title or args.sheet_id,
                     source_pdf=str(args.pdf))
    for n in sorted(items):
        spec.items.append(ItemSpec(number=n, solver=f"q{n:02d}",
                                   source=items[n]))
        stub = pkg / f"q{n:02d}.py"
        if not stub.exists():
            stub.write_text(
                STUB.format(n=n, title="", source=items[n]), encoding="utf-8")
    (pkg / "sheet.json").write_text(spec.to_json(), encoding="utf-8")
    (pkg / "__init__.py").touch()
    print(f"scaffolded {len(spec.items)} solver stubs in {pkg}")
    return 0


def _parse_items(raw: str) -> list[int]:
    return [int(part) for part in raw.replace(" ", "").split(",") if part]


def cmd_figures(args) -> int:
    """Review the figure crops, and ship the ones that are safe to reuse.

    Shipping is opt-in per item and always will be, because the thing that makes
    a crop safe is not visible in the crop. A generated question redraws its
    constants; the picture may only show what every redraw has in common. A
    lettered geometry diagram qualifies. A 7×7 grid with certain cells blacked
    in does not — that grid *is* the constants, and the next draw blacks in
    different cells. Only the person who wrote the generator knows which of the
    two a picture is, so the tool crops, reports, and waits to be told.
    """
    pkg = _work_dir(args.sheet_id)
    review = pkg / "extract" / "figures"
    pages = ex.page_texts(args.pdf)
    found = {f.item: f for f in ex.extract_figures(
        args.pdf, review, expect=ex.declared_item_count(pages))}
    sheet = load_sheet(args.sheet_id) if (pkg / "sheet.json").is_file() else None

    attach = _parse_items(args.attach)
    detach = _parse_items(args.detach)
    if unknown := sorted(set(attach) - set(found)):
        print(f"no figure found for {unknown}; nothing attached")
        return 1
    if not args.force:
        numeric = sorted(n for n in attach if found[n].numeric)
        if numeric:
            print(f"q{numeric} print numbers on the figure "
                  f"({[found[n].words for n in numeric]}). A generated question "
                  "redraws its numbers, so the picture would contradict the "
                  "stem. Pass --force only if those numbers never change.")
            return 1

    for n in attach:
        dest = sheets.figure_file(args.sheet_id, n)
        dest.parent.mkdir(parents=True, exist_ok=True)
        ex.crop_figure(args.pdf, found[n], dest, dpi=args.dpi)
    if sheet is not None and (attach or detach):
        for it in sheet.items:
            if it.number in attach:
                it.figure_asset = sheets.figure_asset_id(args.sheet_id, it.number)
            elif it.number in detach:
                it.figure_asset = ""
                sheets.figure_file(args.sheet_id, it.number).unlink(missing_ok=True)
        (pkg / "sheet.json").write_text(sheet.to_json(), encoding="utf-8")

    shipped = {it.number: it.figure_asset
               for it in (sheet.items if sheet else []) if it.figure_asset}
    print(f"{len(found)} figures cropped for review in {review}")
    for n, fig in sorted(found.items()):
        w, h = fig.box[2] - fig.box[0], fig.box[3] - fig.box[1]
        mark = "shipped" if n in shipped else ("NUMERIC" if fig.numeric else "-")
        print(f"  q{n:02d}  p{fig.page:02d}  {w:5.0f}x{h:<5.0f} {mark:8s}"
              + (" ".join(fig.words[:8]) if fig.words else ""))
    print(f"{len(shipped)} attached; generated questions show those.")
    return 0


def cmd_verify(args) -> int:
    ids = args.sheet_id or sheet_ids()
    if not ids:
        print("no digested sheets found under", SHEETS_ROOT)
        return 1
    failed = False
    for sid in ids:
        results = verify_sheet(load_sheet(sid))
        print(f"── {sid} " + "─" * max(0, 60 - len(sid)))
        print(report(results))
        failed |= any(not r.ok for r in results)
    return 1 if failed else 0


def cmd_list(args) -> int:
    for sid in sheet_ids():
        sheet = load_sheet(sid)
        results = verify_sheet(sheet)
        green = sum(r.ok for r in results)
        print(f"{sid:24s} {green}/{len(results)} green  {sheet.title}")
    return 0


def cmd_ocr(args) -> int:
    if not ocr.available(args.lang):
        print(f"Tesseract with {args.lang} not found — see otk/tools/sheetpipe/ocr.py")
        return 1
    pages = _parse_items(args.pages) or None
    text = "\n".join(f"=== PAGE {p} (ocr) ===\n{t}"
                     for p, t in ocr.ocr_pages(args.pdf, pages, args.dpi, args.lang).items())
    if args.out:
        Path(args.out).write_text(text + "\n", encoding="utf-8")
        print("wrote", args.out)
    else:
        print(text)
    return 0


def cmd_convert(args) -> int:
    from . import convert as cv

    root = Path(args.root) if args.root else bk.default_root()
    bank = bk.load_bank()
    entries = [e for e in bk.select(bank, args.pattern) if e.kind == "exam"]
    if not entries:
        print("no exam record matches", args.pattern)
        return 1
    done = skipped = 0
    keys = {e.answer_key for e in bank.values() if e.answer_key and e.answer_key != e.path}
    for e in entries:
        if e.path in keys:
            print(f"  - {e.path}: answer key of other sheets, read when they convert")
            skipped += 1
            continue
        if e.stage not in ("new", "converted") and not args.force:
            print(f"  = {e.path}: already {e.stage} (--force to redo)")
            continue
        r = cv.convert(e, root)
        if r.skipped:
            skipped += 1
            print(f"  - {e.path}: {r.skipped}")
            continue
        done += 1
        e.items, e.stage = r.items, "converted" if e.stage == "new" else e.stage
        print(f"  + {e.path}: {r.items} questions, {r.answered} answered")
    bk.save_bank(bank)
    print(f"converted {done}, skipped {skipped}; digests in {cv.DIGEST_ROOT}")
    return 0


def cmd_transcript_todo(args) -> int:
    from . import transcript as tr
    bank = bk.load_bank()
    rows = [e for e in tr.todo(bank) if not args.pattern or e in bk.select(bank, args.pattern)]
    for e in rows:
        print(f"{e.pages or 0:4}p  {e.path}")
    print(f"{len(rows)} file(s), {sum(e.pages or 0 for e in rows)} pages need a transcript "
          f"(write to {tr.ROOT})")
    return 0


def cmd_transcript_pages(args) -> int:
    import tempfile
    from . import transcript as tr
    root = Path(args.root) if args.root else bk.default_root()
    pdf = root / args.path
    if not bk.present(pdf):
        print(f'not fetched: python -m otk.tools.sheetpipe bank fetch "{args.path}"')
        return 1
    photos = tr.page_kinds(pdf)
    print("photo pages (exercises):", [i + 1 for i, p in enumerate(photos) if p])
    print("text pages (answers):   ", [i + 1 for i, p in enumerate(photos) if not p])
    if args.render:
        import hashlib
        out = Path(args.out) if args.out else (
            Path(tempfile.gettempdir()) / "sheetpipe_pages"
            / hashlib.sha1(args.path.encode()).hexdigest()[:8])
        pages = [int(p) for p in args.pages.split(",")] if args.pages else None
        tr.render_pages(pdf, out, args.zoom, pages)
        print("rendered to", out)
    return 0


def cmd_transcript_check(args) -> int:
    from . import transcript as tr
    bank = bk.load_bank()
    paths = [e.path for e in bk.select(bank, args.pattern) if tr.path_for(e.path).is_file()]
    bad = 0
    for p in paths:
        try:
            n, a = tr.check(p)
            print(f"  ok {n:4} questions, {a:4} answered  {p}")
        except tr.TranscriptError as err:
            bad += 1
            print(f"  !! {err}")
    print(f"{len(paths) - bad}/{len(paths)} transcripts parse")
    return 1 if bad else 0


def cmd_knowledge_validate(args) -> int:
    from . import knowledge as kn

    files = kn.load_all()
    problems = kn.validate(files)
    units = sum(len(f.units) for f in files)
    for p in problems:
        print("  ! " + p)
    print(f"{units} units in {len(files)} topic files, {len(problems)} problem(s)")
    return 1 if problems else 0


def cmd_knowledge_coverage(args) -> int:
    """How much of each converted sheet the knowledge units account for."""
    from . import knowledge as kn

    files = kn.load_all()
    bank = bk.load_bank()
    entries = [e for e in bk.select(bank, args.pattern or "*") if e.items]
    total = mapped_total = marked = 0
    for e in entries:
        mapped, n, missing = kn.sheet_coverage(e.path, files)
        total, mapped_total = total + n, mapped_total + mapped
        if args.pattern or mapped:
            gap = f"  unmapped: {', '.join(map(str, missing))}" if missing else ""
            print(f"{mapped:3d}/{n:<3d} {e.path}{gap}")
        if args.mark and not missing and e.stage == "converted":
            e.stage, marked = "extracted", marked + 1
    print(f"{mapped_total}/{total} converted questions are claimed by a knowledge unit")
    if args.mark:
        bk.save_bank(bank)
        print(f"marked {marked} fully mapped sheet(s) as extracted")
    return 0


def cmd_plan(args) -> int:
    """Stage 4: knowledge units with no problem set, most-exercised first."""
    from . import knowledge as kn

    rows = [r for r in kn.plan(kn.load_all())
            if not args.topic or r.topic == args.topic]
    gaps = [r for r in rows if r.status == "uncovered"]
    for r in rows:
        if r.status == "covered" and not args.all:
            continue
        mark = "  " if r.status == "covered" else "✗ "
        print(f"{mark}{r.unit.id:44s} {r.level:5s} {r.questions:3d} q  {r.unit.title}")
        if r.status == "covered":
            print(f"      covered by {', '.join(r.unit.covered_by)}")
        elif r.candidates:
            shown = ", ".join(r.candidates[:6]) + (" …" if len(r.candidates) > 6 else "")
            print(f"      check first: {shown}")
    print(f"{len(gaps)} of {len(rows)} units have no problem set"
          + ("" if args.all else " (--all to list covered units too)"))
    if args.mark:
        # A sheet is generated when every unit that claims one of its
        # questions is practised by some problem set.
        files = kn.load_all()
        units = {u.id: u for f in files for u in f.units}
        claims = kn.mapped_positions(files)
        bank = bk.load_bank()
        marked = 0
        for e in bank.values():
            if e.stage != "extracted":
                continue
            ids = {uid for (path, _), us in claims.items() if path == e.path for uid in us}
            if ids and all(units[uid].covered_by for uid in ids):
                e.stage, marked = "generated", marked + 1
        bk.save_bank(bank)
        print(f"marked {marked} extracted sheet(s) as generated")
    return 0


def cmd_bank_scan(args) -> int:
    root = Path(args.root) if args.root else bk.default_root()
    if not root.is_dir():
        print("no sheet bank at", root)
        return 1
    bank, tally = bk.scan(root, bk.load_bank(), reprobe=args.reprobe)
    unmatched = bk.link_digested(bank)
    bk.save_bank(bank)
    print(f"scanned {root}: {tally['added']} added, {tally['changed']} changed, "
          f"{tally['unchanged']} unchanged, {tally['absent']} not present here")
    for sid in unmatched:
        print(f"  ! {sid}: its source_pdf is not in the bank")
    stale = [e.path for e in bank.values() if e.stale]
    for path in stale:
        print(f"  ! stale: {path} changed after it reached a later stage")
    return 0


def cmd_bank_status(args) -> int:
    bank = bk.load_bank()
    if not bank:
        print("bank index is empty — run `sheetpipe bank scan`")
        return 1
    if args.pattern:
        for e in bk.select(bank, args.pattern):
            print(f"{e.stage:9s} {e.layout or e.kind:12s} {e.sheet_id or '-':16s} "
                  f"{e.path}" + (f"  — {e.note}" if e.note else ""))
        return 0
    print(bk.status_table(bank))
    return 0


def cmd_bank_set(args) -> int:
    bank = bk.load_bank()
    entries = bk.select(bank, args.pattern)
    if not entries:
        print("no bank record matches", args.pattern)
        return 1
    if args.answer_key and args.answer_key != "self" and args.answer_key not in bank:
        print("no bank record for the answer key", args.answer_key)
        return 1
    bk.set_fields(entries, sheet_id=args.sheet_id, stage=args.stage, note=args.note)
    for e in entries:                 # "self": a book that binds its key at the back
        if args.answer_key:
            e.answer_key = e.path if args.answer_key == "self" else args.answer_key
    bk.save_bank(bank)
    print(f"updated {len(entries)} record(s)")
    return 0


def cmd_bank_fetch(args) -> int:
    """Download the LFS content of the bank PDFs matching a pattern.

    The bank is its own (private) repository, cloned at ``sheet_database/``.
    Its `.lfsconfig` excludes the PDFs from automatic fetches, to stay inside
    the GitHub LFS download quota; this pulls just the files a stage needs.
    """
    import subprocess

    if not (bk.DEFAULT_ROOT / ".git").exists():
        print(f"no bank repository at {bk.DEFAULT_ROOT}; see README → The source bank")
        return 1
    cmd = ["git", "lfs", "pull", "--include", args.pattern, "--exclude", ""]
    print("running:", " ".join(f'"{c}"' if " " in c or not c else c for c in cmd))
    done = subprocess.run(cmd, cwd=bk.DEFAULT_ROOT)
    if done.returncode:
        return done.returncode
    bank = bk.load_bank()
    have = sum(bk.present(bk.DEFAULT_ROOT / e.path) for e in bk.select(bank, args.pattern))
    print(f"{have} matching bank file(s) now present")
    return 0


def cmd_bank_prune(args) -> int:
    root = Path(args.root) if args.root else bk.default_root()
    bank = bk.load_bank()
    gone = [k for k in bank if not (root / k).is_file()]
    for k in gone:
        print("  - " + k)
        del bank[k]
    bk.save_bank(bank)
    print(f"pruned {len(gone)} record(s) with no file under {root}")
    return 0


def main(argv: list[str] | None = None) -> int:
    # Sheet titles and question text are Thai; a Windows console defaults to
    # cp1252 and would crash on the first line of output.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser(prog="sheetpipe", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("extract")
    p.add_argument("pdf")
    p.add_argument("sheet_id")
    p.set_defaults(fn=cmd_extract)

    p = sub.add_parser("scaffold")
    p.add_argument("pdf")
    p.add_argument("sheet_id")
    p.add_argument("--title", default="")
    p.set_defaults(fn=cmd_scaffold)

    p = sub.add_parser("figures")
    p.add_argument("pdf")
    p.add_argument("sheet_id")
    p.add_argument("--attach", default="",
                   help="comma-separated item numbers whose crop to ship")
    p.add_argument("--detach", default="",
                   help="comma-separated item numbers to stop shipping")
    p.add_argument("--force", action="store_true",
                   help="attach even a crop that prints numbers")
    p.add_argument("--dpi", type=int, default=300)
    p.set_defaults(fn=cmd_figures)

    p = sub.add_parser("verify")
    p.add_argument("sheet_id", nargs="*")
    p.set_defaults(fn=cmd_verify)

    p = sub.add_parser("list")
    p.set_defaults(fn=cmd_list)

    p = sub.add_parser("convert", help="stage 2: bank file(s) → sheet_database/_digest/")
    p.add_argument("pattern", help="bank path, or a glob over bank paths")
    p.add_argument("--root", default="", help="bank folder holding the PDFs")
    p.add_argument("--force", action="store_true",
                   help="reconvert files past the converted stage")
    p.set_defaults(fn=cmd_convert)

    tx = sub.add_parser("transcript", help="hand transcripts of picture-maths sheets").add_subparsers(
        dest="transcript_cmd", required=True)
    p = tx.add_parser("todo", help="exam files that still need a transcript")
    p.add_argument("pattern", nargs="?", default="", help="limit to a bank path glob")
    p.set_defaults(fn=cmd_transcript_todo)
    p = tx.add_parser("pages", help="which pages are photos; --render writes PNGs")
    p.add_argument("path", help="bank path of one PDF")
    p.add_argument("--render", action="store_true")
    p.add_argument("--pages", default="", help="comma-separated 1-based pages (default all)")
    p.add_argument("--zoom", type=float, default=1.5)
    p.add_argument("--out", default="", help="folder for the PNGs (default: a temp folder)")
    p.add_argument("--root", default="")
    p.set_defaults(fn=cmd_transcript_pages)
    p = tx.add_parser("check", help="parse transcripts and count answers")
    p.add_argument("pattern", help="bank path or glob")
    p.set_defaults(fn=cmd_transcript_check)

    kn = sub.add_parser("knowledge", help="stage 3: otk/knowledge/ units").add_subparsers(
        dest="knowledge_cmd", required=True)
    p = kn.add_parser("validate")
    p.set_defaults(fn=cmd_knowledge_validate)
    p = kn.add_parser("coverage")
    p.add_argument("pattern", nargs="?", default="",
                   help="bank path or glob; lists unmapped items per sheet")
    p.add_argument("--mark", action="store_true",
                   help="set fully mapped converted sheets to stage 'extracted'")
    p.set_defaults(fn=cmd_knowledge_coverage)

    p = sub.add_parser("plan", help="stage 4: knowledge units with no problem set")
    p.add_argument("topic", nargs="?", default="", help="limit to one topic")
    p.add_argument("--all", action="store_true", help="list covered units too")
    p.add_argument("--mark", action="store_true",
                   help="set extracted sheets whose units are all covered to 'generated'")
    p.set_defaults(fn=cmd_plan)

    p = sub.add_parser("ocr", help="OCR a scanned PDF (Tesseract, Thai + English)")
    p.add_argument("pdf")
    p.add_argument("--pages", default="", help="comma-separated 1-based pages")
    p.add_argument("--dpi", type=int, default=ocr.DPI)
    p.add_argument("--lang", default=ocr.LANG)
    p.add_argument("--out", default="")
    p.set_defaults(fn=cmd_ocr)

    bank = sub.add_parser("bank", help="the sheet_database/ index").add_subparsers(
        dest="bank_cmd", required=True)
    p = bank.add_parser("scan")
    p.add_argument("--root", default="", help="bank folder (default: $SHEET_BANK "
                   "or sheet_database/)")
    p.add_argument("--reprobe", action="store_true",
                   help="re-probe unchanged files too (after the probe changes)")
    p.set_defaults(fn=cmd_bank_scan)
    p = bank.add_parser("status")
    p.add_argument("pattern", nargs="?", default="",
                   help="list matching records instead of the summary")
    p.set_defaults(fn=cmd_bank_status)
    p = bank.add_parser("set")
    p.add_argument("pattern", help="bank path, or a glob over bank paths")
    p.add_argument("--sheet-id")
    p.add_argument("--stage", choices=bk.STAGES)
    p.add_argument("--note")
    p.add_argument("--answer-key", help="bank path of the file holding these sheets' answers, "
                                        "or 'self' for a book with its key at the back")
    p.set_defaults(fn=cmd_bank_set)
    p = bank.add_parser("fetch", help="download bank PDFs from Git LFS on demand")
    p.add_argument("pattern", help='glob under sheet_database/, e.g. "rathcenter/13 *"')
    p.set_defaults(fn=cmd_bank_fetch)
    p = bank.add_parser("prune")
    p.add_argument("--root", default="")
    p.set_defaults(fn=cmd_bank_prune)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
