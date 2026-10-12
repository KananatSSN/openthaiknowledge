# Digesting exam sheets with `sheetpipe`

`sheetpipe` turns a PDF of a past exam paper — สอวน., O-NET, PAT, a school
midterm — into working problem generators: one per question, each producing
fresh numbers with a correct answer.

It exists because the obvious approach is unsafe. Copying thirty questions into
thirty generators by hand means shipping thirty answers to students that nobody
verified, and a generator that is wrong is worse than no generator: it teaches
the mistake and marks the right answer wrong. So the pipeline's whole design is
about earning the right to say *"this answer is correct for constants nobody has
ever checked."*

| | |
|---|---|
| **Code** | [`otk/tools/sheetpipe/`](../../otk/tools/sheetpipe/) |
| **Output** | [`otk/sheets/<sheet_id>/`](../../otk/sheets/) |
| **Worked example** | [`otk/sheets/posn2568_math/`](../../otk/sheets/posn2568_math/) — 30 olympiad questions |
| **Generators built from it** | [`otk/sets/math/olympiad/`](../../otk/sets/math/olympiad/), one file per paper |
| **Step-by-step recipe** | [`.agents/skills/sheet-to-generator/SKILL.md`](../../.agents/skills/sheet-to-generator/SKILL.md) |

Requires **PyMuPDF** for the extraction stages (`pip install pymupdf`). It is
imported lazily, so verifying and running already-digested sheets works without
it.

---

## The four stages

```bash
python -m otk.tools.sheetpipe extract  <pdf> <sheet_id>   # 1. text, items, figures
python -m otk.tools.sheetpipe scaffold <pdf> <sheet_id>   # 2. sheet.json + stubs
#                                                             3. solve — you do this part
python -m otk.tools.sheetpipe verify   [sheet_id ...]     # 4. prove it
python -m otk.tools.sheetpipe figures  <pdf> <sheet_id>   #    ship the diagrams
python -m otk.tools.sheetpipe list                        #    how green each sheet is
```

What is in `sheet_database/` and how far each file has got is tracked in
`otk/sheets/bank.json`. Run `python -m otk.tools.sheetpipe bank status`
to see it, and see [`SHEET_DIGESTION_PLAN.md`](SHEET_DIGESTION_PLAN.md) for
the bank commands.

This guide covers sheets that get **one solver per question**, such as the
สอวน. papers. Question banks (the rathcenter compilations: each question
tagged with its exam, with choices and a worked solution) go through
`sheetpipe convert` first. That writes a text digest per file to
`sheet_database/_digest/`, and the knowledge-extraction stage works from
there.

`sheet_id` is a package name under `otk/sheets/` — lowercase, no spaces, e.g.
`posn2568_math`. Stages 1, 2 and 4 are mechanical. **Only stage 3 is judgement**,
and it is the bulk of the work.

Each stage leaves an artifact on disk, so a sheet can be picked up months later
without re-deriving anything.

---

## Stage 1 — `extract`

```bash
python -m otk.tools.sheetpipe extract "sheet_database/สอวน_math/01-วิชาคณิตศาสตร์.pdf" posn2568_math
```

Writes `otk/sheets/<sheet_id>/extract/`:

| File | What it is |
|---|---|
| `text.txt` | the whole text layer, page by page |
| `itemNN.txt` | one file per question |
| `pages/pNN.png` | renders of the pages carrying artwork |
| `figures/itemNN.png` | each question's diagram, cut out on its own |

Thai exam PDFs are typeset rather than scanned, so the text layer is usually
good. What it cannot carry is the figures.

Text is repaired as it is extracted (`thai.normalize` fixes legacy-font damage
such as `นี9` for นี้). A page with no text layer, meaning a scan, is OCR'd with
Tesseract when that is installed, and `text.txt` marks it `(ocr)`. OCR reads
Thai prose well and mathematics badly, so transcribe equations from the render.
For setup, see [`ocr.py`](../../otk/tools/sheetpipe/ocr.py).

### How questions are found

Item numbers must run 1, 2, 3, … — a "3." inside a bulleted list is skipped
because it is not the next number due. That one rule handles prices, years and
sub-conditions without a parser.

It is not enough on its own, though, and the way it fails is worth knowing:

> **An exam's คำชี้แจง is itself a numbered list.** On the POSN 2568 sheet the
> instructions ran 1–8 and the questions ran 1–30. Reading greedily from the
> first "1." consumed the eight instructions and then resumed at question 9 —
> 8 + 22 = 30 items, so even the count check waved it through, and items 1–8 of
> `sheet.json` held exam rules instead of questions.

`split_items` therefore builds *every* possible reading and picks the best:
matching the declared count first, then the longest, then the one starting later
in the document — because instructions always precede the questions they
describe. If your sheet has a stranger front matter, check `item01.txt` before
going further.

The sheet's own คำชี้แจง ("จำนวน 30 ข้อ") is parsed by `declared_item_count` and
used as a checksum; a mismatch raises rather than silently digesting 28 of 30.

### Then go and look at the figures

On a maths sheet a third of the questions live in their diagram, and the text
layer says nothing about it. Open the renders. For the two figure kinds that
recur, **do not eyeball — read them as data**:

| Figure | Reader | Verify by |
|---|---|---|
| ruled grid with filled cells (ตารางที่มีช่องสีดำ) | `extract.read_cell_grid` | printing `CellGrid.render()` beside the page PNG |
| labelled table / plan (ผัง with letters and icons) | `extract.read_table_layout` | printing the grid and diffing against the PNG |

```python
from otk.tools.sheetpipe import extract as ex

boxes = ex.image_boxes(pdf, page=11)          # find the figure's bounding box
grid = ex.read_cell_grid(pdf, page=11, clip=boxes[0])
print(grid.render())                          # ASCII art — diff this against the PNG
```

Paste the reading into the solver's docstring as a module constant (`FIGURE`,
`LAYOUT`), so a future reader can check it without reopening the PDF. One
misread cell changes the answer and nothing downstream can notice.

For freehand geometry there is no reader. State the figure's content as prose in
the docstring and as numbers in `PARAMS`, and say explicitly what the figure told
you that the text did not — those readings are where the answer actually comes
from. Real examples from the worked sheet: which of two common tangents is the
internal one (§21); the order of points along a line, which fixes `BE = BD − h`
rather than `BD + h` (§23); that a dashed line is tangent to the *bottoms* of the
big wheels and the *tops* of the small ones (§28).

> **Read the crop, not your memory of the figure.** §30's plan was digested as a
> 6×4 grid. It is 6×5 — the last column is entirely blank, nothing in the text
> names it, and only the ruling says it is there. Those six cells neighbour B, D
> and F, and the answer is 7, not 5. The crop is what makes that visible.

---

## Stage 2 — `scaffold`

```bash
python -m otk.tools.sheetpipe scaffold "<pdf>" posn2568_math --title "ข้อสอบ… ปีการศึกษา 2568"
```

Creates the sheet package:

```
otk/sheets/posn2568_math/
    __init__.py
    sheet.json          ← provenance: one entry per question
    q01.py … q30.py     ← solver stubs, each raising NotImplementedError
```

Existing `qNN.py` files are never overwritten, so re-running is safe.

`sheet.json` is plain JSON and survives independently of this code. Per item:
`number`, `solver`, `title`, `source` (verbatim Thai), `page`, `figure` (how a
diagram was digitized — also the picture's alt text), `figure_asset` (set by
`sheetpipe figures`, see below), `topic`, `answer`, `generator` (the registry key
built from it), `note` (caveats).

---

## Stage 3 — solve *(the only stage that is judgement)*

Fill in each `qNN.py`. The contract is four names:

```python
PARAMS   = {"m": 10}          # the constants this question happens to use — its tunables
ANSWER   = 50                 # the answer for exactly those constants
VARIANTS = [{"m": 7}, ...]    # other constant sets that must also come out right

def solve(m=10): ...          # the method, closed form where one exists
def check(m=10): ...          # a SECOND, INDEPENDENTLY WRITTEN derivation
```

Optional: `TOL` (a numeric solver declaring its own tolerance — a geometry
construction cannot hit 1e-9, and should say so rather than let the harness
guess) and constants recording a figure reading (`FIGURE`, `LAYOUT`).

Every key of `PARAMS` must be a keyword argument of `solve`, and `solve` must
work for *other values* of them. That is what "change the constant" means.

### `check` is the whole point

`solve` and `check` must reach the same value by **different routes**. Closed
form vs. brute force. Algebra vs. coordinates. A pattern vs. the actual big
integers.

This is not ceremony. On the worked sheet, cross-checking caught six real bugs
that either reproduced the sheet's own answer or looked entirely fine:

| Question | Bug | Caught by |
|---|---|---|
| §2 | bisection bracket had the monotonicity backwards | numeric root find |
| §5 | closed form used `6(base−1)` where the digit sum is `2(base−1)n` | big-int digit sum |
| §8 | counted `n = 1`, which is `1²` — a root, so `P = 0`, not negative | direct product |
| §12, §19, §27, §30 | the recorded answer was a guess | both methods agreeing |

Note the bottom row: **four of the thirty answers, written down by hand, were
wrong.** Never hand-write `ANSWER`. Run `solve`, confirm `check` agrees, then
record what they say.

Good second methods, in rough order of preference:

1. **Brute force.** Search space under ~10⁶? Enumerate it.
2. **Numeric construction.** For geometry, build the figure in coordinates and
   measure — tangent points from unit normals, angles from dot products, areas
   by shoelace. Assert the construction's own invariants along the way
   (`AD ⊥ DB`, `DE` really is a diameter); those catch a misread figure, which
   no amount of algebra will.
3. **Root finding.** Bisect or Newton on the *original* equations, not the
   rearranged ones.
4. **A different frame.** §29 solves the circumcentre in a rotated, translated
   frame precisely so the equations don't decouple and the answer can't be read
   off.

If a second method genuinely does not exist, say why in the docstring; `verify`
reports those separately instead of failing.

### `VARIANTS` is what earns the generator

Variants are constants with no published answer, where the two methods are the
only evidence. Three or more, each genuinely different from `PARAMS` (a test
enforces both). Include the awkward ones: an empty solution set, a degenerate
case, a different base, equal radii.

### Two failure modes worth hunting for

**The question has more than one answer.** §25's condition `1/AP + 1/BP = 2/CP`
also holds whenever P is the midpoint of the hypotenuse — in *any* right
triangle — so `∠ACP = 41°` yields both 33° and 49°. The generator must state the
extra condition out loud, or the item has two correct choices. Record it in
`SHEET_NOTE` and in `sheet.json`'s `note`.

**The question stops being well posed at other constants.** §14's data set is
unique for the sheet's numbers but not for `mode = 7`, where two data sets give
different answers. Return `None` rather than picking one — then the generator's
pool skips it.

---

## Stage 4 — `verify`

```bash
python -m otk.tools.sheetpipe verify              # every sheet
python -m otk.tools.sheetpipe verify posn2568_math
```

```
[OK  ] q08 x2 6 variants
[OK  ] q30 x2 5 variants

30/30 solvers green, 152 variant runs, 0 without an independent check
```

`x2` means a second method exists; `--` means it does not. Exit status is 1 if
anything failed, so this drops straight into CI.

A solver is **green** only when all three hold:

* **reference** — `solve(**PARAMS) == ANSWER`: it reproduces the sheet.
* **cross-check** — `check(**PARAMS) == solve(**PARAMS)`: a second, independently
  written method agrees.
* **variants** — the same agreement at every entry of `VARIANTS`.

Nothing about a closed-form `solve` justifies the strong claim on its own: a
wrong exponent reproduces the sheet's answer just fine if you only ever test the
sheet's numbers.

```bash
python -m otk.tools.sheetpipe list
# posn2568_math   30/30 green   ข้อสอบคัดเลือกเข้าค่าย 1 สอวน. คณิตศาสตร์ ปีการศึกษา 2568
```

---

## Shipping the figures — `figures`

A question the sheet illustrated should stay illustrated. `extract` already cuts
each diagram out of the PDF; `figures` is where you decide which of those crops
the *generated* questions show.

```bash
python -m otk.tools.sheetpipe figures "<pdf>" posn2568_math
```

```
10 figures cropped for review in …/otk/sheets/posn2568_math/extract/figures
  q20  p08    167x147   -
  q21  p08    403x230   -       𝑙1 𝑙2
  q27  p11    116x127   -
  q30  p13    171x169   -       ว่าง ว่าง 𝑨 𝑩 𝑪 𝑫 𝑬 𝑭
0 attached; generated questions show those.
```

Then attach the ones you have looked at and approved:

```bash
python -m otk.tools.sheetpipe figures "<pdf>" posn2568_math --attach 20,21,22,29,30
```

That copies the crop to `otk/sheets/<sheet_id>/figures/qNN.png` and records
`figure_asset` in `sheet.json`. Nothing else is needed: `SheetProblem` reads the
attachments at import, `assetstore` serves them at `/assets/sheet-<sheet_id>-qNN`
like any other diagram, and the worksheet PDF renderer picks them up through the
same resolver. `--detach` reverses it.

### Why attaching is opt-in

Because the thing that makes a crop safe **is not visible in the crop**.

A generated question redraws its constants. The picture may only show what every
redraw has in common:

| Safe — the arrangement is the figure | Unsafe — the figure *is* the constants |
|---|---|
| a lettered geometry diagram (§21–§26, §29) | §27's 7×7 grid with five cells blacked in — the next draw blacks in different ones |
| a plan whose positions are fixed and whose *counts* vary (§30) | any diagram carrying a measurement the generator varies |

Only the person who wrote the generator knows which of the two a picture is, so
the tool crops, reports, and waits to be told. It does refuse one case on its
own: a crop whose text opens with a digit (`12`, `3.5cm`) is a measurement, and
`--attach` rejects it unless you pass `--force`. A digit inside a name — `l₁`,
`A2` — does not count; renaming a line is not a redraw.

Crops are pulled back off neighbouring text automatically, so a figure never
arrives carrying a sliver of the question's own numbers.

### Checking a shipped figure

The place to look is the offline curriculum graph, which bakes the figures in as
data URIs:

```bash
python -m otk.tools.curriculum_graph
```

`🖼 เฉพาะที่มีรูป` filters the tree to the types that have one — that is the
answer to "which problem sets have a figure". Click a type and the panel shows
the real diagram under the stem with its alt text; 🎲 cycles the draws. **Cycle
them.** A figure is only correct if it survives every draw, and the hover
tooltip tells you what to expect: `🖼 รูปประกอบ 1/6 ตัวอย่าง` means five of the
six draws deliberately hide it.

### When only some draws match the picture

Attachment is per question, but a type can opt a single draw out with
`MathDraw(figure=None)`:

```python
# §28's picture has three small wheels drawn in it, so it is only this
# question's picture when the draw asks for three.
figure=None if n_small != 3 else "",
```

`""` (the default) means "show the type's figure if it has one"; an explicit
asset id overrides it; `None` suppresses it for that draw. §20 uses this too —
the sheet's parallelogram is drawn at one fixed angle, so the draw that *names*
the angle hides it rather than inviting the student to measure the picture.

---

## Stage 5 — the generator

One question type per question, all in the paper's file under
[`otk/sets/math/olympiad/`](../../otk/sets/math/olympiad/) (imported in that
folder's `__init__.py`). Follow
[`posn2568.py`](../../otk/sets/math/olympiad/posn2568.py), and
[`ADDING_PROBLEMS.md`](ADDING_PROBLEMS.md) for the type system itself.

The generator **never re-derives the answer**. It draws constants, calls the
solver, and spends its own code on wording, exact TeX and distractors:

```python
SOLVE = {n: lru_cache(maxsize=4096)(mod.solve) for n, mod in enumerate(_MODULES, 1)}

@question_type("math.<sheet>_qNN", display_name={"th": "..."},
               level={"th": "โอลิมปิก (สอวน.)"}, topic="...")
class Something(SheetProblem):
    def expr(self, rng, lo: int = 4, hi: int = 16):    # numeric kwargs = tunables
        n = rng.randint(lo, hi)
        return MathDraw(problem_tex, str(SOLVE[8](m=n)),
                        prompt="Thai question text",   # Thai lives here, never in TeX
                        distractors=[...])
```

Five things that came up building all thirty:

- **Draw from pools, not free ranges.** Most of these are only well posed for
  some constants. A `_pool_*` helper scans a small grid once at import and keeps
  what survives, so a generator can never emit an item whose answer is `None`.
  Pools also keep answers *writable*: §2's pool exists so `s² − 4√p` stays a
  perfect square and the answer is `61` rather than a six-digit surd.
- **Cache the solvers.** Several are searches, and the distractor machinery
  re-draws a type a few times per item. `lru_cache` + small pools = a dict lookup.
- **Name the near miss.** The best distractor is the specific mistake the item
  exists to catch — §25 offers `90° − α`, the degenerate branch, first.
- **Exact TeX, not floats.** Keep `solve` numeric so `check` can verify it, and
  build the exact form in the generator: `(17 + 11√2)π/3`, `√6 − √2`, `4/π`.
  Reduce fractions and bracket compound coefficients before `\pi`. Never feed
  `frac_answer_tex` output into a product — its mixed-number form contains an `=`.
- **Check the choice count.** Generate ~60 items and assert four choices every
  time. Fewer means hand-picked distractors are colliding.

---

## Using it from Python

```python
from otk.tools.sheetpipe import load_sheet, solver_modules, verify_sheet

sheet = load_sheet("posn2568_math")
print(sheet.title, len(sheet.items))

item = sheet.item(8)
print(item.topic, item.answer, item.generator)

for item, mod in solver_modules(sheet):
    print(item.number, mod.solve(**mod.PARAMS))

results = verify_sheet(sheet)
print(sum(r.ok for r in results), "green")
```

---

## Checklist for a new sheet

- [ ] `extract` ran and the item count matches the sheet's own คำชี้แจง.
- [ ] `item01.txt` really is question 1 — not the first line of the คำชี้แจง.
- [ ] Every figure page looked at; grid/table figures read with the readers and
      their output pasted into the solver docstring.
- [ ] `figures` run, every crop opened, and the draw-invariant ones attached —
      with a reason recorded for each one that was not.
- [ ] Each attached figure checked against several draws in
      `python -m otk.tools.curriculum_graph` (🖼 filter → click → 🎲).
- [ ] Each `qNN.py` has `PARAMS`, `ANSWER` (*derived*, never guessed), `solve`,
      an independent `check`, and ≥ 3 real `VARIANTS`.
- [ ] Questions with non-unique answers documented, and the generator states the
      disambiguating condition.
- [ ] `sheet.json` records source text, page, figure notes, topic, answer and
      generator key for every item.
- [ ] One generator per question; Thai in prompts, notation-only TeX in math
      blocks; four choices on every draw.
- [ ] `verify` reports `N/N green, 0 without an independent check`.
- [ ] `pytest otk/tests/test_sheetpipe.py` passes.

## Troubleshooting

| Symptom | Cause |
|---|---|
| `sheetpipe extraction needs PyMuPDF` | `pip install pymupdf` |
| `split_items found 28 items, sheet declares 30` | question numbers not at line start, or a page's text layer is missing (a scanned insert) |
| items 1–N are the exam rules | front matter the run-picker could not out-vote — check `item01.txt` and fix the split before solving |
| `figures` finds nothing, or one figure per page | the PDF is a scan: the whole page is a single image. `extract` OCRs the text, but figure cropping needs a text layer to anchor on |
| `q… print numbers on the figure` | the crop carries a measurement the generator varies — leave it unattached, or pin the constant |
| a shipped figure contradicts the stem | it was not draw-invariant after all: `--detach` it, or opt the mismatching draws out with `MathDraw(figure=None)` |
| `PARAMS not accepted by solve()` | a key of `PARAMS` is not a keyword argument of `solve` |
| `solve(**PARAMS)=… != ANSWER=…` | `ANSWER` was hand-written; run `solve`, confirm `check`, record that |
| `variant N: solve=… != check=…` | the two methods disagree — one is wrong, or the question is not well posed at those constants |
| `0 without an independent check` is not 0 | a solver has no `check`; go find a second derivation |
