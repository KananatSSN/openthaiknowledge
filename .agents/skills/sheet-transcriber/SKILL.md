---
name: sheet-transcriber
description: Transcribe ONE sheet_database PDF whose maths is printed as pictures (the (สสวท) textbook files, scans) into a hand transcript under sheet_database/_transcribed/, verifying every answer with SymPy. Give it the bank path of the file. Used by the sheet-bank skill: one file per run, as a subagent where the agent has them, else inline.
---

You transcribe exactly one bank PDF into a hand transcript and verify every
answer. You work alone and in parallel with other transcribers: write only
your one output file, and do not run `git`, `convert`, or anything that
changes `otk/sheets/bank.json`.

All commands run from the repository root (the directory holding
`sheet_database/` and `otk/`). Prefix Python with
`PYTHONIOENCODING=utf-8` on Windows.

## Input

The caller gives you a **bank path** such as
`rathcenter/11 จำนวนเชิงซ้อน/(สสวท) 5 รูปเชิงขั้ว🌶️.pdf` (relative to
`sheet_database/`), and sometimes notes about the file.

Your output is `sheet_database/_transcribed/<bank path with .md instead of .pdf>`.
If it already exists, stop and report that instead of overwriting it.

## Steps

1. **Fetch if needed, then find the photo pages.**
   `python -m otk.tools.sheetpipe bank fetch "<bank path>"` (only if the
   next command says "not fetched"), then
   `python -m otk.tools.sheetpipe transcript pages "<bank path>" --render`.
   It prints which pages are photos (the textbook exercises), which are text
   (the teacher's-manual answers), and the folder of `pNN.png` renders.
2. **Read every exercise page** with the Read tool. If something is too small,
   re-render that page with `--pages N --zoom 3`, or crop with PIL.
3. **Get the answers, preferring computation.** Work answers out yourself with
   SymPy or a short script (write scripts to the system temp folder, not the
   repo). Read the answer pages only for answers that depend on a figure, a
   table, wording, or an example the manual chooses; the answer pages'
   text layer can also be read with `fitz` (`page.get_text()`), though its
   Thai consonants may be garbled.
4. **Write the transcript** in the format of `otk/tools/sheetpipe/transcript.py`
   (read its docstring first) and in the style of the finished examples in
   `sheet_database/_transcribed/rathcenter/9 เมทริกซ์/` and `.../10 เวกเตอร์/`:
   - First line: a `<!-- -->` comment naming the exercise pages and answer
     pages (with book page numbers), items that are proofs or drawings, and
     anything left out and why.
   - `# <exercise title exactly as printed>`, `> lead` for a shared
     instruction, `@pN` page markers, `n.` items and `k)` sub-items with the
     book's own numbering, `= answer`, `(1) … (4)` choices, `{figure}` where
     an item depends on a picture, a trailing `[exam tag]` if printed.
   - Plain Unicode maths: x², √(x + 1), π, −, ≤, a/b with brackets as needed,
     matrices as `[a b; c d]`, vectors as `(a, b, c)` or with i⃗ j⃗ k⃗.
   - A proof or "draw this" item gets no `=` line; if a drawing item has a
     computable answer (a point, a set, a region), give it.
   - Thai text exactly as printed; keep units in answers.
5. **Verify.** Every answer you computed or copied must be checked by an
   independent computation where one is possible. Where the manual is wrong,
   or answers a different version of the question, put
   `<!-- The manual prints …; … -->` on the line above the item and give the
   correct answer.
6. **Check it parses:**
   `python -m otk.tools.sheetpipe transcript check "<bank path>"`.

## Report back (keep it short)

- Output path; questions / answered.
- Items without an answer, and why (proof, drawing, missing page).
- Manual errors found.
- Anything unreadable or uncertain (be specific: item and what is in doubt).
