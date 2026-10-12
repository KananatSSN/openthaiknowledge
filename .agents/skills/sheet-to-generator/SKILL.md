---
name: sheet-to-generator
description: Turn an exam-sheet PDF (สอวน., O-NET, PAT, a school midterm) into working problem generators — extract the questions and figures, write one cross-checked solver per question, then wire each to a question type. Use when the user points at a PDF (in the maintainers' bank, or their own paper under sheet_database/contrib/) and wants it digested, or asks to add questions from a paper exam.
---

# Exam sheet → problem generator

A sheet is *digested* when every question has two things: a **solver** that
computes the answer for arbitrary constants, and a **generator** that asks the
question with fresh ones. The pipeline exists because the second is worthless
without the first being trustworthy — a generator ships answers to students for
numbers nobody ever checked.

Worked example, end to end: `otk/sheets/posn2568_math/` (30 olympiad
questions) and `otk/sets/math/olympiad/posn2568.py`.

## The four stages

```bash
python -m otk.tools.sheetpipe extract  <pdf> <sheet_id>   # 1. text, items, figures
python -m otk.tools.sheetpipe scaffold <pdf> <sheet_id>   # 2. sheet.json + stubs
#                                                             3. solve — the human part
python -m otk.tools.sheetpipe verify   <sheet_id>         # 4. prove it
python -m otk.tools.sheetpipe figures  <pdf> <sheet_id>   #    ship the diagrams
python -m otk.tools.sheetpipe list                        #    how green each sheet is
```

`sheet_id` is a package name under `otk/sheets/` (e.g. `posn2568_math`).

## Your own paper (contributors)

Maintainers work from the private source bank cloned at `sheet_database/`.
Contributors do not have it and do not need it: digest a paper of your own.

1. **Rights first.** The paper's question text, page text and figures are
   committed under `otk/sheets/<sheet_id>/` and published. Use only a paper you
   wrote or have permission to publish, and say which in the pull request. If
   unsure, stop and ask the user.
2. **Put the PDF in your own bank folder**, which git ignores, so the PDF is never
   committed: `sheet_database/contrib/<your GitHub name>/<file>.pdf`. Create the
   folders if they do not exist.
3. **Index it, then run the four stages** on that path:
   ```bash
   python -m otk.tools.sheetpipe bank scan        # adds a record for your file to otk/sheets/bank.json
   python -m otk.tools.sheetpipe extract  sheet_database/contrib/<you>/<file>.pdf <sheet_id>
   python -m otk.tools.sheetpipe scaffold sheet_database/contrib/<you>/<file>.pdf <sheet_id>
   python -m otk.tools.sheetpipe bank scan        # again: links the new sheet to its record
   ```
   The scans keep every record for files you do not have (the maintainers'
   bank); that is expected. Never run `sheetpipe bank prune`: it refuses outside
   the private bank, because it would erase those records.
4. **Fill in `sheet.json`**: a real `title` (paper, year, author or school) and
   `level`. Every set built from the paper derives its provenance from it, so
   the title is the citation.
5. Solve, verify and wire the generators as below. Commit `otk/sheets/<sheet_id>/`,
   the generator file, `otk/sheets/bank.json` and the golden draws; never the
   PDF. One paper per pull request.

The bank-wide pipeline (the `sheet-bank` skill: digests, knowledge units,
coverage plans) needs the private bank and is for maintainers.

---

## Stage 1 — extract

`extract` writes `otk/sheets/<id>/extract/`: `text.txt`, one `itemNN.txt` per
question, and PNG renders of every page carrying artwork.

Item splitting follows the *running number* — a line starting `12.` counts only
if 12 is the next number due, so `3)` inside a bulleted list is ignored. The
sheet's own คำชี้แจง ("จำนวน 30 ข้อ") is parsed and used as a checksum; a
mismatch raises rather than silently digesting 28 of 30.

### Then go look at the figures. Actually look.

On a maths sheet a third of the questions live in their diagram, and the text
layer says nothing about it. Read the rendered pages. For the two figure kinds
that recur, **do not eyeball — read them as data**:

| Figure | Reader | Verify by |
|---|---|---|
| ruled grid with filled cells (ตารางที่มีช่องสีดำ) | `extract.read_cell_grid` | printing `CellGrid.render()` next to the page PNG |
| labelled table / plan (ผัง with letters and icons) | `extract.read_table_layout` | printing the grid and diffing against the PNG |

Both were used for real here (§27's plus of black cells, §30's village plan) and
both outputs are pasted into the solver docstring, so a future reader can check
the reading without reopening the PDF. One misread cell changes the answer and
nothing downstream can notice.

For freehand geometry there is no reader — you have to state the figure's
content as prose in the docstring and as numbers in `PARAMS`. Say explicitly
what the figure told you that the text did not; those readings are where the
answer actually comes from. Real examples from this sheet:

- §21 — which of the two common tangents is the internal one.
- §23 — the order of points along the line (B, E, D), which fixes `BE = BD − h`
  rather than `BD + h`.
- §28 — that a thin dashed line is tangent to the *bottoms* of the big wheels
  and the *tops* of the small ones. Get this wrong and the wheels move.

`extract` also cuts each question's diagram out on its own, to
`extract/figures/itemNN.png`. **Open those, not your memory of the page.** §30's
plan was digested as a 6×4 grid; it is 6×5, the last column is blank, nothing in
the text names it, and the answer is 7 rather than 5.

### Then decide which diagrams the generated questions show

```bash
python -m otk.tools.sheetpipe figures  <pdf> <sheet_id>                # review
python -m otk.tools.sheetpipe figures  <pdf> <sheet_id> --attach 21,29 # ship those
```

Attaching copies the crop to `<sheet_id>/figures/qNN.png`, records
`figure_asset` in `sheet.json`, and every draw of that question then shows it —
nothing else to wire up.

**Attach only a draw-invariant figure.** A generated question redraws its
constants, so the picture may only show what every redraw has in common: the
arrangement of a lettered geometry diagram (§21–§26, §29), a plan whose
positions are fixed and whose counts vary (§30). Never a picture that *is* the
constants — §27's grid of black cells changes every draw, so it stays
unattached. The tool refuses a crop whose text opens with a digit, but that
guard catches only the measured case; the judgement is yours.

Where only some draws match, return `MathDraw(figure=None)` for the rest — §28
shows the belt only when the draw asks for the three small wheels that are drawn
in it.

---

## Stage 3 — solve (the only stage that is judgement)

Fill in each `qNN.py`. The contract is four names, documented in
`otk/tools/sheetpipe/spec.py`:

```python
PARAMS   = {...}   # the constants this question happens to use — its tunables
ANSWER   = ...     # the answer for exactly those constants
VARIANTS = [...]   # other constant sets that must also come out right
def solve(**PARAMS): ...   # the method, closed form where one exists
def check(**PARAMS): ...   # a SECOND, INDEPENDENTLY WRITTEN derivation
```

Optional: `TOL` (a numeric solver declaring its own tolerance) and module
constants recording a figure reading (`FIGURE`, `LAYOUT`).

### `check` is the whole point

`solve` and `check` must reach the same number by *different routes*. Closed form
vs. brute force. Algebra vs. coordinates. A pattern vs. the actual big integers.

This is not ceremony. On this sheet, cross-checking caught **six** real bugs that
reproduced the sheet's own answer or looked fine:

| Question | Bug | Caught by |
|---|---|---|
| §2 | bisection bracket had the monotonicity backwards | numeric root find |
| §5 | closed form used `6(base−1)` where the digit sum is `2(base−1)n` | big-int digit sum |
| §8 | counted `n = 1`, which is `1²` — a root, so `P = 0`, not negative | direct product |
| §12 | (recorded answer was a guess) | both methods agreeing on 45 |
| §19 | (recorded answer was a guess) | both methods agreeing on 68 |
| §27, §30 | (recorded answers were guesses) | both methods agreeing |

Note the pattern in the bottom half: **four of the thirty answers I wrote down by
hand were wrong.** Never hand-write `ANSWER`. Run `solve`, confirm `check`
agrees, then record what they say.

Good second methods, in rough order of preference:

1. **Brute force.** If the search space is under ~10⁶, enumerate it (§1, §8,
   §12, §13, §15, §19, §27, §30).
2. **Numeric construction.** For geometry, build the figure in coordinates and
   measure — tangent points from unit normals, angles from dot products, areas
   by shoelace (§21–§26, §29). Assert the construction's own invariants along
   the way (`AD ⊥ DB`, `DE` really is a diameter); those catch a misread figure,
   which no amount of algebra will.
3. **Root finding.** Bisect or Newton on the original equations rather than the
   rearranged ones (§2, §7, §24, §25).
4. **A different frame.** §29 solves the circumcentre in a rotated, translated
   frame precisely so the equations *don't* decouple and the answer can't be
   read off.

If a second method genuinely does not exist, say why in the docstring; `verify`
reports those separately instead of failing.

### `VARIANTS` is what earns the generator

Variants are constants with no published answer, where the two methods are the
only evidence. Three or more, each genuinely different from `PARAMS` (a test
enforces both). Include the awkward ones: an empty solution set, a degenerate
case, a different base, equal radii.

### Two failure modes worth hunting for

**The question has more than one answer.** §25's condition
`1/AP + 1/BP = 2/CP` also holds whenever P is the midpoint of the hypotenuse —
in *any* right triangle — so `∠ACP = 41°` yields both 33° and 49°. The
generator must state the extra condition out loud ("P ไม่ใช่จุดกึ่งกลางของ AB̅")
or the item has two correct choices. Record it in `SHEET_NOTE` and in
`sheet.json`'s `note`.

**The question stops being well posed at other constants.** §14's data set is
unique for the sheet's numbers but not for `mode = 7`, where two data sets give
different answers. Return `None` rather than picking one — then the generator's
pool skips it (below).

---

## Stage 5 — the generator

One question type per question, all in one file per paper:
`otk/sets/math/olympiad/<paper>.py`, imported in that folder's `__init__.py`.
Follow `otk/sets/math/olympiad/posn2568.py`, and `docs/for_admin/ADDING_PROBLEMS.md` for the
type system itself.

The generator **never re-derives the answer**. It draws constants, calls
`SOLVE[n](...)`, and spends its own code on wording, exact TeX, and distractors.

```python
@question_type("math.<sheet>_qNN", display_name={"th": "..."},
               level={"th": "โอลิมปิก (สอวน.)"}, topic="...")
class Something(SheetProblem):
    def expr(self, rng, lo: int = 4, hi: int = 16):     # numeric kwargs = tunables
        n = rng.randint(lo, hi)
        return MathDraw(problem_tex, str(SOLVE[8](m=n)),
                        prompt="Thai question text",     # Thai lives here, never in TeX
                        distractors=[...])
```

Five things that came up building all thirty:

- **Draw from pools, not free ranges.** Most of these are only well posed for
  some constants. `_pool_*` helpers scan a small grid once at import and keep
  what survives, so a generator can never emit an item whose answer is `None`.
  Pools also keep answers *writable*: §2's pool exists so `s² − 4√p` stays a
  perfect square and the answer is `61` rather than a six-digit surd.
- **Cache the solvers.** Several are searches, and the distractor machinery
  re-draws a type a few times per item. `lru_cache` + small pools = a dict
  lookup.
- **Name the near miss.** The best distractor is the specific mistake the item
  exists to catch — §25 offers `90° − α`, the degenerate branch, first.
- **Exact TeX, not floats.** Keep `solve` numeric (so `check` can verify it) and
  build the exact form in the generator: `(17 + 11√2)π/3`, `√6 − √2`, `4/π`.
  Reduce fractions (`(51 + 33√2)π/3` must read `(17 + 11√2)π`) and bracket
  compound coefficients before `\pi`. Never feed `frac_answer_tex` output into a
  product — its mixed-number form contains an `=`.
- **Check the choice count.** Generate ~60 items and assert four choices every
  time. Fewer means hand-picked distractors are colliding.

---

## Stage 4 — verify, and what "green" means

```bash
python -m otk.tools.sheetpipe verify <sheet_id>
python -m pytest otk/tests/test_sheetpipe.py otk/tests/test_core.py
```

A solver is green only when all three hold: it reproduces the sheet
(`solve(**PARAMS) == ANSWER`), a second method agrees, and the two still agree at
every variant. `test_sheetpipe.py` runs that per question in CI, plus: recorded
answers match the modules, every item's `generator` key is registered, no
generator is orphaned, generators are seed-reproducible, and a few spot checks
that parse a generated stem and re-derive its answer from scratch.

## Checklist for a new sheet

- [ ] `extract` ran and the item count matches the sheet's own คำชี้แจง.
- [ ] Every figure page looked at; grid/table figures read with the readers and
      their output pasted into the solver docstring.
- [ ] `figures` run, every crop opened, and the draw-invariant ones attached —
      with a reason recorded for each one that was not.
- [ ] Each `qNN.py` has `PARAMS`, `ANSWER` (*derived*, never guessed), `solve`,
      an independent `check`, and ≥ 3 real `VARIANTS`.
- [ ] Questions with non-unique answers documented, and the generator states the
      disambiguating condition.
- [ ] `sheet.json` records source text, page, figure notes, topic, answer and
      generator key for every item.
- [ ] One generator per question; Thai in prompts, notation-only TeX in math
      blocks; four choices on every draw.
- [ ] `verify` reports `N/N green, 0 without an independent check`.
- [ ] New keys recorded in the golden draws:
      `python -m otk.tools.golden_draws --update <new keys>`; no existing key's
      entry changed unless that change is intended and noted.
- [ ] `pytest otk/tests/` passes.
