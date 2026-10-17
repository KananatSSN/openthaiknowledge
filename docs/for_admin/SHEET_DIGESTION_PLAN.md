# Sheet digestion system — plan and progress

Multi-session build. **Start every session here**: read §3 (status) and the
newest entry of §6 (session log), then pick up the first unchecked item.

| | |
|---|---|
| **Branch / worktree** | `worktree-sheet-digestion` at `.claude/worktrees/sheet-digestion` |
| **Existing pipeline guide** | [`DIGESTING_EXAM_SHEETS.md`](DIGESTING_EXAM_SHEETS.md) (`sheetpipe`, exam path) |
| **Agent recipe** | [`.agents/skills/sheet-to-generator/SKILL.md`](../../.agents/skills/sheet-to-generator/SKILL.md) |
| **Code** | [`otk/tools/sheetpipe/`](../../otk/tools/sheetpipe/) |

---

## 1. Goal

Drop a sheet into the **sheet bank** (`openthaiknowledge-bank/`), convert it to text,
extract the knowledge it teaches, and generate verified problem sets from that
knowledge — with the bank's state visible at a glance instead of living in
per-folder handoff notes.

Non-goal: generating questions with an LLM at runtime. A model may *author*
digests, knowledge units, solvers and fact banks, but everything shipped to a
student is committed code/data that passes the gates in stage 6. That is the
repo's standing guarantee (every answer cross-checked) and this system keeps it.

## 2. Design

```
openthaiknowledge-bank/  ──1 scan────▶ otk/sheets/bank.json  (path, hash, kind, stage)
                 ──2 convert──▶ otk/sheets/<id>/digest.md + items.json
                 ──3 extract──▶ otk/sheets/<id>/knowledge.json
                 ──4 plan─────▶ coverage diff vs registry → work list
                 ──5 generate─▶ solvers (compute) | fact banks (concept) → types
                 ──6 gate─────▶ sheetpipe verify + guessability + registry tests
```

| Stage | What | Built on |
|---|---|---|
| 1 scan | Inventory every bank file: content hash, kind (`exam`/`notes`/`fact-data`), text-layer probe, layout guess, `sheet_id`, stage. Rescan preserves human-owned fields and flags changed files stale. | new `sheetpipe/bank.py` |
| 2 convert | Pluggable item splitters (`numbered` = today's; `choice-block` for rathcenter; `notes` for `.md`), Thai glyph repair, opt-in vision transcription for vector-typeset equations. Output human `digest.md` + machine `items.json`. | `extract.py` |
| 3 extract | Knowledge units: `formula` / `procedure` / `concept` / `fact-list`, with variables, level, IPST indicator, and the items that exercise each. Near-duplicate items across sheets merge. Wrong printed keys recorded. | `curriculum_*.py`, teaching_plan pattern |
| 4 plan | Diff knowledge units against the registry by indicator/topic → *covered* / *new* / *extends type X*. | `REGISTRY`, `curriculum_*.py` |
| 5 generate | Compute units → existing solver contract (`solve`/`check`/`VARIANTS`). Concept units → declarative fact-bank format + generic types (which-belongs, odd-one-out, match, classify). | `olympiad.py`, `science_wave_*`, `distractors.py` |
| 6 gate | Existing checks, plus stage bookkeeping in `bank.json`. | `test_sheetpipe.py`, guessability tests |

### Key decisions

| Date | Decision | Why |
|---|---|---|
| 2026-09-30 | LLM at authoring time only | Keeps "every shipped answer is cross-checked" |
| 2026-09-30 | `bank.json` lives in `otk/sheets/` (tracked); bank root is configurable (`--root` / `SHEET_BANK`) | Progress state must be versioned, and a checkout may lack the PDFs (CI, or before `git lfs pull`) |
| 2026-09-30 | **Bank PDFs are tracked with Git LFS** (user decision). `.gitignore` un-ignores `openthaiknowledge-bank/**/*.pdf`, and `.gitattributes` routes them to LFS | 317 files, ~390 MB. Plain git would put that in every clone's history. CI checks out without LFS; `bank.present()` treats pointer files as absent |
| 2026-09-30 | Bank entries keyed by bank-relative POSIX path; mechanical fields recomputed on scan, `sheet_id`/`stage`/`note` preserved | Rescans must never erase human/agent progress |
| 2026-09-30 | Digests are committed under `openthaiknowledge-bank/_digest/` (3.6 MB for rathcenter), not under `otk/sheets/` | They are the only version-controlled form of a sheet's text, since the PDFs are gitignored. A digest is not a Python package, so it stays out of `otk/sheets/`, which is only for sheets with solvers. The bank scan skips `_`-prefixed folders |
| 2026-09-30 | Font repair is learned per document with a word-frequency model, not a fixed table | The same ASCII letter means different marks in different PDFs (`U` is `่` in some and `้` in others), and dictionary membership alone picks rare words (`ครั่ง`, `ทั่ง`) |

## 3. Status

Phases in build order. Check an item only when its tests pass.

### Phase 1 — bank index & status board ✅ (session 1)
- [x] `sheetpipe/bank.py`: scan, classify, PDF probe (pages, text chars, layout guess, glyph-damage count), duplicate detection
- [x] `sheetpipe bank scan|status|set|prune` CLI
- [x] Link existing `otk/sheets/*/sheet.json` (`source_pdf`) to bank entries (and their byte-identical copies); derive stage from verify results
- [x] Tests: `otk/tests/test_sheetpipe_bank.py` (13, incl. a consistency check on the committed index)
- [x] First real scan committed as `otk/sheets/bank.json`; known hand-digested files annotated with `bank set`

**Usage**
```bash
python -m otk.tools.sheetpipe bank scan                   # needs `git lfs pull` first
python -m otk.tools.sheetpipe bank status                 # summary table
python -m otk.tools.sheetpipe bank status "rathcenter/1 *"   # records matching a glob
python -m otk.tools.sheetpipe bank set "<path|glob>" --stage converted --sheet-id x --note "…"
```
A first scan of the full bank takes ~3 min (PDF probing); rescans only
re-probe files whose hash changed. Pass `--reprobe` after changing the probe
itself; it refreshes the mechanical fields without marking anything stale.

### Phase 2 — convert (unlocks rathcenter's 305 PDFs)
- [x] `choice-block` splitter (session 1): `choiceblock.py`. It cuts questions by margin-label geometry (labels are narrow blocks at x≈72, emitted at the page end), reads each band top to bottom, and takes the tag, choices (including stacked-math choices), answer and solution. Answers come from the second label run (the solutions), anchored by tag so that a dropped solution label does not merge two answers. Tests: `test_sheetpipe_choiceblock.py`.
- [x] `sheetpipe convert <bank path|glob>` (session 1): `convert.py` writes `openthaiknowledge-bank/_digest/<bank path>.json` + `.md` and sets the bank stage to `converted` with an `items` count. It has run on all of rathcenter: **173 files → 1,071 questions**, 98% with answers.
- [x] Thai glyph repair (session 1). There are two layers:
  - `thai.normalize`, a table: `9` for `้`, PUA tone marks, and OCR's split `ำ`.
  - `fontfix.py`, glyph level, learned per document and font: ASCII→tone-mark maps (`L/M/Q`→`่`, `U/9/1`→`้`, `K`→`็`, `f`→`์`), scored with a TNC unigram model from PyThaiNLP. It also handles Cordia's `า`→`ำ` swap and the zero-width-nikhahit `ำ` (`จ ำนวน`, `ก าหนด`, `น ้า`).
  - Result: 6,503 hits cut to 16 across the bank. `test_sheetpipe_fontfix.py` covers it.
- [x] OCR for scanned pages (session 1): `ocr.py` uses Tesseract `tha+eng`, `--psm 6`. `extract`/`scaffold` OCR only pages with no text layer; `sheetpipe ocr <pdf>` runs it standalone.
- [ ] **Latin-1-for-consonant damage**. It appears on the `(สสวท)` answer-key pages (IPST คู่มือครู): `üิชา` = วิชา, `ý` = ศ, `ÿ` = ส, `þ` = ษ, `Ā` = ห. Plan: extend `fontfix` so that the wedged-character learner also takes Latin-1/Extended-A characters, with Thai consonants as candidates.
- [x] **Separate answer keys** (session 1): `answerkey.py`, for the nine `(rath)` trig notes and `(rath) เฉลย.pdf`.
  - A new owned bank field, `answer_key`, is set with `sheetpipe bank set <glob> --answer-key <key path>`. `convert` then splits that sheet with `answerkey`, whatever its layout, and skips the key file itself.
  - Both sides restart sub-numbering under every item, so the exercise side decides the structure. An item is the next number whose own line is Thai, or a bare number whose text carries a question word or exam tag. Everything else numbered is a sub-item. The key is read against that structure, and a section counts only if every key token is consumed.
  - Sections match by title. The running header is stripped at most once per page, because the chapter name is also a section title.
  - Items citing an exam (`[PAT 1 (ต.ค. 55)/9]`) become choice questions with that tag.
  - **Result: 283 questions, 276 answered.** All 12 exercise blocks align with their key sections. Key section `ตาราง` has no exercise block.
  - Knowledge sources gained a third form, `{"sheet": path, "section": title}`, which claims a whole section.
  - Known noise: sidebar formula boxes can leak into a stem, and stacked fractions read as "1 2".
  - Tests: `test_sheetpipe_answerkey.py`.
- [ ] **Numbered splitter + OCR** for the 74 `numbered` `(สสวท)` files. Their exercise pages are photos, and their answer pages are teacher's-manual text full of equation-editor debris (`114\n8 114\n7`) plus Latin-1 consonant damage. OCR can't read the maths on the photos, so these are transcribed by eye instead (below) rather than split.
- [ ] Sectioned splitter: numbering that restarts per part (Faii's five ตอน), with inline answer keys
- [x] **`book` layout, the 23 `🍰` lecture books** (session 1). Each book is notes, then `แบบฝึกหัด` blocks, then its answer key bound at the back. `sheetpipe bank set "rathcenter/*/🍰*" --answer-key self` marks this, and `answerkey.split` reads the key region after the last exercise block. A key title counts only if it also heads a section of the notes.
  - The trig book is the nine `(rath)` notes bound together, so it is marked `ignored` rather than digested twice.
  - Structure is decided by `align`, a small DP that labels numbered lines item / sub-item / choice / noise to best match the key. It replaced a greedy Thai-text rule, which answered only 70% of book items.
  - **Result: 22 books, 2,267 questions, 2,153 answered (95%).** The conic book is the weakest (47/78): worked-example sidebars with their own numbered Thai steps, and a section split across two `แบบฝึกหัด` headings.
  - The books' ~200 exercise sections are claimed by `{"sheet", "section"}` sources (the mapping, as a re-runnable script, is `docs/for_admin/sheet_digestion_book_sections.py`). 20 new units cover basics the exam chapters never needed: set basics, vector basics, complex arithmetic, derivative rules, circle and conic standard forms, and so on.
  - Three gaps got new sets in `math_bank_notes.py`: `sigma_sums_m6`, `radical_equation_m4` (extraneous roots and infinite nested radicals) and `stars_bars_m5`. A fourth gap, operations defined in the notes themselves (e.g. a * b = a + b − ab; the notes call this `การสร้างเครื่องหมายใหม่`), is recorded in the unit's note; there is no ม.4 stage node for it yet.
  - **All of rathcenter now stands at 3,617/3,617 converted questions claimed, with 0 units uncovered.**
- [ ] `notes` splitter for `.md` banks
- [~] **Transcription by eye for picture-maths sheets** (session 2): `transcript.py`. User decision: the pages are read in session (render, read, write), not through a model API.
  - A transcript lives at `openthaiknowledge-bank/_transcribed/<bank path>.md`. `convert` prefers it to any splitter, needs no PDF, and marks the digest `"transcribed": true`. The format is in the module docstring: `# section`, `> lead`, `n.` items, `k)` sub-items, `= answer`, `(n)` choices, `@pN` pages, `{figure}`, trailing exam tags.
  - Sub-items become their own questions with section `"<title> <n>.<k>"`, the answer-key convention. Knowledge sources gained `"number"`, so `{"sheet", "section": "แบบฝึกหัดท้ายบท", "number": 9}` claims one exercise and its subs (the chapter-end exercises mix topics).
  - Every transcribed answer is checked: SymPy for algebra, a numeric scan where SymPy stalls. Where the teacher's manual is wrong or answers another version of the question, the transcript says so in a `<!-- -->` line and carries the computed answer.
  - **Workflow (reusable): the `sheet-bank` skill (`.agents/skills/sheet-bank/SKILL.md`) runs the whole bank loop, and the `sheet-transcriber` subagent (`.claude/agents/sheet-transcriber.md`) transcribes one file.** The main session dispatches one subagent per file, a chapter at a time, then spot-checks, converts, claims and commits. CLI: `sheetpipe transcript todo` (what is left), `transcript pages <path> --render` (photo vs answer pages, PNG renders), `transcript check <glob>`. Measured: about 40k tokens and a minute per 2-page exercise file, 2–4× cheaper than reading in one long session (whose cost is dominated by re-reading its own history). No model API is used.
  - Progress: every picture-maths file is transcribed and claimed (97 files, 3,455 questions); `sheetpipe transcript todo` is empty and every converted question in the bank (7,072) is claimed by a knowledge unit with a problem set.
  - Manual errors found so far, each noted in its transcript: logic 2.2 1.4 and 1.12 (false-hypothesis implications marked false), conics ท้ายบท 25 (64y²/3 for 64y²/5), exponentials ท้ายบท 8.9 (missing x < 1), radicals 6.2 (6.1's answer repeated), sets 3.9ก 2.5–2.6, midpoints 6 (only one median endpoint), complex 1.5 2.6 (−π/12 rewritten as 11π/12), complex ท้ายบท 10.4 (sign and 3¹⁰⁰ dropped).
  - Tests: `test_sheetpipe_transcript.py`.

**Convert usage**
```bash
python -m otk.tools.sheetpipe convert "rathcenter/*"
```
It takes ~3 min for all of rathcenter. Files that are not `new`/`converted` are
skipped unless `--force` is passed. Other layouts are reported as skipped,
with the reason.

### Phase 3 — knowledge units ✅ (session 1)
- [x] Schema, loader and validator in `sheetpipe/knowledge.py`; the data lives in `otk/knowledge/<subject>/<topic>.json` (the schema is in the module docstring).
  - Sources name questions by **exam tag** (stable across the compilations that repeat a question), or by `{sheet, item}` when a question has no tag.
  - `knowledge validate` checks sources, `covered_by` keys, prerequisites and cycles, per-kind fields, and topic names.
- [x] `knowledge coverage [glob] [--mark]`: shows which converted questions no unit claims; `--mark` advances fully mapped sheets to `extracted`.
- [x] Reference topic **probability**: 15 units (11 probability, 2 counting, 1 permutation) account for all 59 converted probability questions (50 distinct exam questions). The units' notes record wrong-looking keys and traps.
- Tests: `test_sheetpipe_knowledge.py`.

**How to author a topic** (the loop for the next topics):
1. `sheetpipe knowledge coverage "rathcenter/<n> *"` lists the unmapped questions.
2. Read the `.md` digests. Write units in `otk/knowledge/math/<topic>.json`, one per distinct skill, with sources by tag. Use the registry's topic string.
3. Set `covered_by` only after sampling the candidate type (`generate(key)`) and confirming it practises the unit. A same-topic type often drills something narrower.
4. `knowledge validate` → 0 problems; `knowledge coverage … --mark`.

### Phase 4 — coverage diff ✅ (session 1)
- [x] `sheetpipe plan [topic] [--all] [--mark]` lists units with no problem set, most-exercised first. Each comes with same-topic registry types to check: school types before olympiad ones, nearest grade first. `--mark` advances `extracted` sheets whose units are all covered to `generated`.

### Phase 5 — generate ✅ for probability (session 1)
- [x] **Compute units → closed-form generators, with solvers proven against brute force.** `otk/core/types/math_bank_probability.py` adds 6 sets, one per gap:
  - `probability_union_m5`
  - `probability_two_way_table_m5`
  - `probability_without_replacement_m5`
  - `probability_digit_numbers_m5`
  - `probability_random_arrangement_m5`
  - `probability_grid_route_m5`

  Each is placed in `math_stages.py`. `test_math_bank_probability.py` enumerates every experiment by brute force over the generators' whole parameter range, and pins the source exams' printed answers. Distractors are named mistakes. The six probability sheets are now `generated`, and `plan` shows 0 of 15 units uncovered.
- [x] **เซต** (session 1). 13 units (`otk/knowledge/math/sets.json`) account for all 57 converted questions (32 distinct). `plan` found 9 gaps, and `otk/core/types/math_bank_sets.py` adds 8 sets to close them:
  - `set_expression_eval_m4`
  - `set_expression_match_m4`
  - `set_always_true_m4`
  - `set_two_set_word_m4`
  - `set_exactly_k_m4`
  - `set_region_algebra_m4`
  - `set_multiples_count_m4`
  - `set_extremal_m4`

  Each counting set draws hidden Venn-region counts and states totals derived from them. It answers with a solver that sees only the stated numbers, and `_agree` asserts that the solver recovers the hidden count on every item. `test_math_bank_sets.py` checks every solver against brute force over region counts, checks the "always true" verdicts on a larger universe, and pins 13 exam answers.
- [x] **ตรรกศาสตร์** (session 1). 9 units (`logic.json`) account for all 25 converted questions (17 distinct). There were 6 gaps, and `math_bank_logic.py` adds 6 sets:
  - `logic_compound_value_m4`
  - `logic_deduce_values_m4`
  - `logic_verbal_deduction_m4`
  - `logic_tautology_m4`
  - `logic_custom_connective_m4`
  - `logic_quantifier_finite_m4`

  They share one formula engine (build, TeX and Thai rendering, evaluate). Items are drawn only when the options split cleanly over every assignment the premises allow. `test_math_bank_logic.py` checks the engine against a compile-to-Python route, re-checks drawn items that way, and pins 6 exams' verdicts.
  - Digest issue seen: the `(onet)` logic file's items have no `ตอบ`; the solutions are unlabelled there. One O-NET item's stem swallowed the previous solution.
- [x] **3 จำนวนจริง** (session 1). The chapter spans six registry topics, so the units are split across six files: `polynomial-division`, `absolute-value`, `quadratic-inequality`, `quadratic-equation`, `real-numbers` and `linear` (all `.json`). 14 units cover all 115 converted questions (65 distinct). There were 7 gaps, and `math_bank_real.py` adds 7 sets, each filed with its own topic's stage path. How the answers are decided:
  - integer counts: exact scan;
  - absolute-value equations: exact piecewise solver;
  - coefficient problems: hidden-truth `_agree` check;
  - order properties: counterexample grid.

  `test_math_bank_real.py` re-solves every family with SymPy (installed, and `importorskip`-ed) and pins 11 exam answers.
  - **Placement rule learned:** a unit with no matching stage node (order properties at ม.4) goes to the node where the skill is taught (linear inequalities, ม.3). A new node would need three stages of sets.
- [x] **4 ฟังก์ชัน** (session 1). 12 units across 6 files: `functions`, `function-graphs`, `parabola`, `quadratic-range`, `derivative`, plus one source added to `quadratic-equation`. They cover all 95 converted questions (57 distinct).
  - Most units were already covered by existing sets (domain, composition, inverses, shifts, parabolas from features, modelling).
  - `math_bank_functions.py` adds 5 sets for the 5 gaps:
    - `piecewise_function_m4`
    - `graph_inequality_parameters_m4`
    - `relation_pairs_m4`
    - `graph_transform_point_m4` (reflections, and exponential-graph constants)
    - `derivative_chain_m5` (a chain-rule question found in this folder)
  - `test_math_bank_functions.py` checks against SymPy (piecewise solving, inequality solution sets, derivatives) and pins exam answers.
  - **Trap:** a draw loop whose condition can be unsatisfiable hangs the suite. `relation_pairs` drew a region with no lattice point. Every `while True` draw must be provably satisfiable; bound the parameters rather than hope.
- [x] **5 เลขยกกำลัง** (session 1). 8 units across `powers.json` and `exponential-equations.json`, plus 2 in `radicals.json`, cover all 77 converted questions (44 distinct). Many digests are garbled because equations are typeset as vector art, but the questions still classify. There were 5 gaps, and `math_bank_powers.py` adds 5 sets:
  - `exponential_equation_advanced_m4`: factoring, substitution, quadratic exponents, and inequalities
  - `rational_power_evaluate_m5`
  - `root_sign_properties_m5`
  - `power_compare_m5`
  - `radical_denest_m4`

  `test_math_bank_powers.py` checks with SymPy: real roots of negatives, solution sets, and denesting.
  - **Test note:** SymPy can return an endpoint as an unsimplified log expression. Compare `simplify(end - expected) == 0`, not the intervals directly.
- [x] **6 เอกซ์โพเนนเชียลและลอการิทึม** (session 1). 11 of the 42 questions were already claimed by chapter 5's exponential-equation units. `logarithms.json` adds 5 units for the rest (29 distinct questions). There were 3 gaps, and `math_bank_logs.py` adds 3 sets:
  - `log_mixed_bases_m5`
  - `log_equation_advanced_m5`
  - `log_inequality_m5`

  `test_math_bank_logs.py` checks the identities with SymPy, substitutes every solution back, and compares the inequality solvers with SymPy's solution sets. That check caught a solver bug on equal arguments.
- [x] **7 เรขาคณิตวิเคราะห์และภาคตัดกรวย** (session 1). 4 units in `conics.json`, `circles.json` and `lines.json` cover all 32 converted questions (16 distinct). The existing conic sets start from standard forms centred at the origin, but the exams start from general forms or from foci. `math_bank_conics.py` adds 4 sets:
  - `conic_general_form_m4`
  - `conic_focal_definition_m4`
  - `circle_tangency_m4`
  - `line_closest_point_m4`

  They are built backwards from Pythagorean triples and chosen tangency points. SymPy checks expand the standard forms, test the focal definitions at vertices, and verify distances; 6 exam answers are pinned.
- [x] **8 ตรีโกณมิติ** (session 1). 12 units in `trig-ratios.json`, `trig-functions.json`, `inverse-trig.json`, `trig-equations.json` and `triangle-laws.json` cover all 46 converted questions (32 distinct). The 8 `(rath)` trig files are still unconverted (interleaved labels, answers in a separate เฉลย file). There were 6 gaps, and `math_bank_trig.py` adds 6 sets:
  - `right_triangle_relations_m5`: hypotenuse plus one ratio or the area, linking the two acute angles
  - `trig_radian_arc_m5`: radians and arc length on a circle
  - `trig_identity_reduce_m5`: reduce to one function, cos⁴ − sin⁴, the sin 3θ/sin θ ratio
  - `inverse_trig_sum_m5`: sin/cos/tan of arcsin + arccos, A + B from tans, arcsin u + arccos v = π/2
  - `trig_equation_count_m5`: how many solutions in [0, nπ], including tan(λx) = tan(λπ) for irrational λ
  - `triangle_side_type_m5`: obtuse/right/acute from sides, and how many integer third sides give an obtuse triangle

  `test_math_bank_trig.py` checks identities with SymPy, counts roots by scanning, and brute-forces the triangle counts; 12 exam answers are pinned.
  - **Test note:** SymPy does not simplify sums like `atan(1/2) + atan(1/3) − π/4` or `tan(2·asin(5/13))` to 0. Compare at 50 digits (`abs(N(expr, 50)) < 1e-40`) instead.
- [x] **9 เมทริกซ์** (session 1). 5 units in `matrices.json` cover all 25 converted questions (13 distinct). The existing sets compute a determinant or an inverse; the exams reason about them. There were 3 gaps, and `math_bank_matrices.py` adds 3 sets:
  - `determinant_properties_m5`: row operations, det(kA), det(AB⁻¹), solving for an entry from det(B⁻¹A)
  - `matrix_unique_solution_m5`: the parameter value that makes det = 0
  - `matrix_equation_m5`: AX = C, ABᵗ = kI, [A : I] ~ [I : P], and a true-statement count for AB = I

  `test_math_bank_matrices.py` checks the exact `Fraction` arithmetic against SymPy matrices and the AB = I statements on random invertible pairs (each "false" one must fail somewhere); 6 exam answers are pinned.
- [x] **10 เวกเตอร์** (session 1). 5 units in `vectors.json` cover all 26 converted questions (15 distinct). There were 3 gaps, and `math_bank_vectors.py` adds 3 sets:
  - `vector_triple_product_m5`: (v × i) · (j + k), forms reducing to ±a · (b × c), u × v ⊥ w, which v is parallel
  - `vector_identity_m5`: |u · v|² + |u × v|² = |u|²|v|², cos θ from |u ± v|² = k|u × v|², a true-statement count
  - `vector_points_m5`: triangle area, AB ⊥ CD then |AD|, cos of an angle, all from 3-D points

  `test_math_bank_vectors.py` checks the triple-product forms symbolically and the statements on random vectors; 6 exam answers are pinned.
- [x] **11 จำนวนเชิงซ้อน** (session 1). 5 units in `complex.json` cover all 36 converted questions (18 distinct). There were 4 gaps, and `math_bank_complex.py` adds 4 sets:
  - `complex_power_cycle_m5`: iⁿ with large and factorial exponents, ((1 + i)/(1 − i))ⁿ, counting x with i^(px+q) = i^(rx+s)
  - `complex_equation_parts_m5`: z̄ + i|z| = a + bi, z + |z − s| = a + bi, square roots, |z² − m| = kiz + d
  - `complex_conjugate_root_m5`: building x² + ax + b and quartics/cubics from a complex root
  - `complex_modulus_rules_m5`: moduli of products and quotients, |z₁ − z₂| in polar form, a true-statement count

  `test_math_bank_complex.py` substitutes every solution back with SymPy (and shows rejected roots fail); 7 exam answers are pinned. A real bug surfaced: when x = ±y, the "swapped parts" distractor for a square root was itself a square root.
- [x] **12 หลักการนับ** (session 1). The probability chapter's `counting.json` and `permutation.json` gained 5 units and more sources; all 62 converted questions (31 distinct) are claimed. There were 4 gaps, and `math_bank_counting.py` adds 4 sets:
  - `counting_complement_m5`: "at least one" as total minus none
  - `coloring_regions_m5`: rows k(k − 1)ⁿ⁻¹, all-different colours, four-region layouts described in words
  - `arrangement_blocks_gaps_m5`: subjects kept together, alternating groups, no two neighbouring seats
  - `distribute_to_groups_m5`: labelled groups, two baskets with leftovers, n + 1 people into n rooms

  `test_math_bank_counting.py` recounts every closed form by brute-force enumeration; 13 exam answers are pinned.
- [x] **14 ลำดับและอนุกรม** (session 1). 12 units in `arithmetic-sequences.json`, `geometric-sequences.json`, `series.json` and `finance.json` cover all 188 converted questions (96 distinct). There were 5 gaps, and `math_bank_sequences.py` adds 5 sets:
  - `arithmetic_series_tricks_m6`: alternating sums, alternating squares, sums between two indices, products of cᵃⁿ
  - `sequence_patterns_m6`: second-difference sequences, aₙ from Sₙ, aₙ₊₂ − aₙ = d, Sₘ₋₁ from Sₘ and Sₘ₊₁, the triangle of numbers
  - `geometric_series_tricks_m6`: r from two conditions, a₁aₙ = aₖ², S₁₀ from S₁₂ with r = √q, sum vs alternating sum, Σaₙ² from Σaₙ and Σ(−1)ⁿaₙ, S∞ from S₅ and a₆ + ⋯ + a₁₅
  - `telescoping_series_m6`: Σ c/((n + p)(n + p + k)), the Fibonacci-like sum, mean from the median of 1/(n(n + 1)), Σ k·2ᵏ
  - `compounding_periods_m5`: rate per period and number of periods, forward and backward, interest earned

  `test_math_bank_sequences.py` recomputes every answer term by term or with SymPy's summation; 16 exam answers are pinned.
- Fix found by `test_core`'s invariants (more seeds than the per-set tests): `vector_points_m5` crashed when a distractor's vector had length 0. `length_tex(0)` now returns 0, and D = A is redrawn.
- **Test-run note:** don't wire new modules or edit knowledge JSON while the repo-wide suite runs. `test_committed_knowledge_is_valid` reads the JSON at test time but the registry at import time, so it reports a spurious failure.
- [x] **15 แคลคูลัส** (session 1). 7 new units, spread over the new `calculus-*.json` files plus one new unit in `derivative.json`, cover all 51 converted questions (28 distinct). There were 4 gaps, and `math_bank_calculus.py` adds 4 sets:
  - `parabola_area_m6`: the parabola from the area it encloses with the x-axis
  - `cubic_critical_points_m6`: build a cubic from its critical points; statements about increase and decrease
  - `tangent_conditions_m6`: a tangent with a given slope; the quadratic from its minimum and a tangent line; tangents to k/(x + d)
  - `derivative_inverse_product_m6`: g′(b) for g = f⁻¹; ∫(2x f + (x² − c) f′); the chain rule from values

  SymPy checks everything, including g′ by implicit differentiation; 9 exam answers are pinned.
- [x] **16 สถิติ** (session 1). 6 units in `stats-central.json`, `stats-position.json`, `stats-spread.json` and `stats-presentation.json` cover all 111 converted questions (105 distinct). The existing sets already covered most of them; the classification was scripted, with every tag resolved and checked against the digest. There were 2 gaps, and `math_bank_stats.py` adds 2 sets:
  - `stats_data_conditions_m6`: mean = mode; median − mode = k; data from mode, median and range. Hidden data are recovered by brute force, and a draw is kept only when the asked quantity is unique.
  - `stats_transform_m6`: y = ax + b; variance from Σ(x − c)²; x̄ ± ks; pooled variance; min Σw|a − x|

  `test_math_bank_stats.py` rechecks with the `statistics` module and brute force.
- [x] **17 ตัวแปรสุ่ม** (session 1). 3 units in `random-variables.json` cover all 24 converted questions (12 distinct). There were 2 gaps, and `math_bank_random.py` adds 2 sets:
  - `normal_z_table_m6`: the stem prints the z-table, rounded to 4 places; the questions ask for areas, percentile cut-offs, equal standard scores, or μ and σ from symmetric tails
  - `expected_game_value_m6`: expected profit of a two-ticket draw
- **All 17 rathcenter math chapters are through Phases 3–5.** Every converted rathcenter question is claimed by a knowledge unit, and `plan` reports no uncovered units (140 units).
- [x] **3 จำนวนจริง, (สสวท) transcripts** (session 2). The 286 transcribed questions are claimed by sections; four new units (`poly.division-algorithm`, `real.partial-fractions`, `abs.properties`, `abs.inequality`). Three gaps, and `math_bank_textbook_real.py` adds 3 sets:
  - `polynomial_long_division_m4`: quotient or remainder on division by a monic quadratic, or the dividend from b, q, r. The distractors are real divisions after a slip (missing terms dropped, divisor signs flipped, divisor constant forgotten).
  - `partial_fractions_m4`: A, B for two linear factors (the cover-up rule), or A + B + C over x(x² + k)
  - `absolute_value_properties_m4`: which statement always holds, decided by counterexample search
  `test_math_bank_textbook_real.py` re-solves with SymPy.
- [x] **1, 2, 4, 6, 7 (สสวท) transcripts** (session 2). 1,178 questions claimed by sections (one exercise number at a time in the mixed chapter-end sets). Two new units, `logic.propositions` and `function.monotonic` (the latter already covered by `increasing_interval` and `monotonic_at_point`). One gap: `math_bank_textbook_logic.py` adds `proposition_identify_m4` (proposition, open sentence, or neither; and truth value), whose mathematical labels the test evaluates.
- Hints: main now requires a strategy hint for every Foundation and Fluency IPST maths set (`test_math_hints.py`, which belongs in the suite command below). 31 sets this branch had wired in early lacked one; `math_hints.py` now has them. Any new set placed in stage 1 or 2 needs a hint there too.
- [ ] Next: transcribe the other (สสวท) chapters the same way, one chapter at a time, then their knowledge pass. After that, Phase 5 concept fact-banks and Phase 6 automation.
- Generator conventions learned so far:
  - Foundation-stage sets offer 3 choices (`max_choices`); test against that, not 4.
  - Never put Thai in TeX, not even in `\text{}`. Split into text and math blocks.
  - Put a space between a Latin letter and a Thai word (`โรงพยาบาล A และ`).
  - Don't nest same-type quotes in f-strings; the repo also runs Python 3.10/3.11.
  - Check every "named mistake" distractor really differs from the answer. Some are equal by identity, e.g. 2/C(a+b, a) = 2·a!·b!/(a+b)!.
- [ ] Concept units → declarative fact-bank format (from `openthaiknowledge-bank/fact_data/*.py` dicts) + generic types (which-belongs, odd-one-out, match, classify). This waits until a topic has concept units without a set.

### Phase 6 — automation
- [ ] Extend the skill to the notes path; headless per-sheet runner

## 4. Bank at a glance

_From `sheetpipe bank status`, 2026-10-02, after the root was tidied._
`openthaiknowledge-bank/README.md` explains every folder and the `rathcenter` file
prefixes.

```
folder      files  exam  notes  data  new  generated  green  ignored
Faii            1     1                         1
fact_data       4                  4    4
misc            1                                              1
notes          10           10         10
outputs         9     3      6                                 9
rathcenter    305   305               51      253              1
specs           1            1                  1
สอวน_math       7     7                 1                 6
TOTAL         338   316     17     4   66      255      6     11
```

- **rathcenter: 5,360 questions converted and claimed.** What remains: about
  50 `(สสวท)` files of chapters 11–17 (hand transcription, chapter 11 in
  progress) and 3 stray `(1)` files.
- **no-text**: `Faii/ข้อสอบแรง.pdf` (hand-digested) and
  `สอวน_math/posn1-64-math.pdf` (27/30 solvers verified).
- **notes/topics/** (6 topic notes, formerly `new_sheet/`) are not yet
  digested. `กระบวนการเปลี่ยนแปลงของหิน` has no matching types at all; the
  others are partly covered.
- **outputs/** (`teaching_plan/`, `review_sheet/`) is marked `ignored`: these
  are written *from* existing sets, not sources.
- The root copy of the 2568 สอวน. paper was a byte-identical duplicate and was
  removed; `posn2568_math` now points at `สอวน_math/01-วิชาคณิตศาสตร์.pdf`.

## 5. Traps already found

- **PDFs are in Git LFS and fetched on demand** (since session 1).
  - The LFS objects are stored with the openthaiknowledge-bank repository
    itself (until 2026-10-16 they were stored with TutorRank's). The bank's
    `.lfsconfig` excludes every PDF from automatic fetches, to stay inside
    GitHub's LFS download quota. The bank's PDFs total ~1.1 GB.
  - A clone therefore holds pointer files for the PDFs. `bank scan` skips them
    as absent, and `convert` says what to fetch.
  - Fetch only what a stage needs: `python -m otk.tools.sheetpipe bank fetch
    "rathcenter/13 *"`. That wraps `git lfs pull --include … --exclude ""`.
  - The pipeline mostly works from the committed digests, so most sessions
    fetch nothing.
  - If the bank outgrows the LFS quota, or several people pull it, move LFS storage to
    Cloudflare R2 (an LFS server on a Worker; R2 downloads are free), as
    proposed in session 1.
  - The default bank root (`openthaiknowledge-bank/` of the checkout you run in) is
    enough; no `--root` is needed.
- **rathcenter question numbers are margin labels.** Each is its own narrow
  block at x≈72, level with the question's first line, but the text layer
  emits the labels at the *end* of the page. Text order inside a question is
  not reading order either (set definitions come after the tag). Cut by
  geometry; `choiceblock.py` does.
- **Solutions runs drop labels sometimes**, and some files have no solution
  labels at all. Anchor on the source tag, which every solution repeats.
- **Stacked math in choices.** `1.` alone on a line, then `1` / `5` = 1/5.
  The JSON keeps the lines; the Markdown shows `1/5`.
- **สอวน. equations are vector art.** Text extraction drops exponents and
  variables (see `openthaiknowledge-bank/สอวน_math/HANDOFF.md`). Transcribe from page
  renders.
- **Glyph damage is per document, not per font name.** Each PDF embeds its
  own Cordia New subset with its own broken ToUnicode map. Only `Cordia New` /
  `CordiaNew` spans are damaged; THSarabun and Angsana are clean.
  - The same ASCII letter differs between PDFs: `U` is `้` in most and was
    once scored as `่`.
  - Dictionary membership is not enough: `ครั่ง`, `ทั่ง` and `นั่น` are real
    words. Score with word frequency, which `fontfix` does.
  - Digits next to Thai are often maths (`น3`, `น2ล` → `นิล`!). A digit needs
    two distinct improving words before it is mapped.
  - `ตอบ`-style Thai+digit hits like `คณิต1` are not damage.
- **Answer-key files live in the bank.** For example
  `rathcenter/8 ตรีโกณมิติ/(rath) เฉลย.pdf`. Stage 2 should pair them with
  their question file rather than treat them as sheets.
- **`new_sheet/`, `review_sheet/`, `teaching_plan/` moved into the bank.**
  The user decided this in session 1. The tracked `.md` files moved with
  `git mv`, and references were updated.
- **Merging this branch into the main checkout.** The main checkout still has
  the bank PDFs as *untracked* files at the same paths that the branch now
  tracks, so `git merge` stops with "untracked working tree files would be
  overwritten". They are byte-identical to the committed ones (the bank
  hashes match). **Before merging**, move them aside, for example
  `mv openthaiknowledge-bank ../openthaiknowledge-bank.bak`, then after the merge run
  `git lfs pull`. Also delete the stale `teaching_plan/`, `new_sheet/` and
  `review_sheet/` folders at the repo root, which only hold untracked PDFs by
  then. The `.zip` in the bank stays ignored.
- **OCR quality.** Thai prose is good with `--psm 6`, but expect `ข้าย` for
  ซ้าย and `A.` for `ง.`. Maths comes out garbled. It takes ~4 s per page at
  300 dpi.
- **OCR setup.** Tesseract is from `winget install UB-Mannheim.TesseractOCR`
  and ships English only. Thai lives in `%LOCALAPPDATA%\tessdata`
  (tessdata_best `tha`, `eng`, and `osd` copied from the install), because
  Program Files needs admin. `ocr.py` finds both automatically.
- **Faii's paper restarts numbering in each of its five parts** and has answer
  keys inline, so `split_items` reads only one run. The sectioned splitter
  (Phase 2) fixes that.
- **`(สสวท)` answer pages use Latin-1 letters for consonants** (`üิชา` =
  วิชา, `ý` = ศ, `ÿ` = ส, `þ` = ษ, `Ā` = ห), as well as PUA vowels (`` =
  ี, `` = ึ). `thai.normalize` handles the PUA; the consonants are
  still open.
- **PyThaiNLP** (`pip install pythainlp`, already in `pyproject.toml`'s
  optional dependencies) is needed for the font repair. Without it, extraction
  falls back to the table repair.
- **Windows console is cp1252.** Any script printing Thai must reconfigure
  stdout to UTF-8 (the CLI's `main` does) or set `PYTHONIOENCODING=utf-8`.

## 6. Session log

### 2026-09-30 — session 1
- Surveyed existing pieces; wrote this plan.
- Phase 1 done: `bank.py`, CLI, 13 tests, first scan committed.
  `test_sheetpipe.py` still green (1301 passed, 4 skipped).
- Measured the bank (see §4, §5): source-tag formats, glyph-damage classes.
- Moved `new_sheet/`, `review_sheet/`, `teaching_plan/` into the bank (see §5
  for the post-merge step) and annotated the derived ones as `ignored`.
- Installed Tesseract + Thai. Added `thai.py` (table repair), `ocr.py`
  (scanned-page fallback in `extract`/`scaffold`, `sheetpipe ocr`),
  `bank scan --reprobe`. Tests: `test_sheetpipe_ocr.py` (12). The sheetpipe
  and wave E/F suites pass (3,687 passed).
- Built per-document font repair (`fontfix.py`), with PyThaiNLP installed.
  6,503 hits of damage cut to 16.
- Built the `choice-block` splitter (`choiceblock.py`) and `sheetpipe
  convert`. All of rathcenter's choice-block files are converted:
  173 files, 1,071 questions, digests committed under `openthaiknowledge-bank/_digest/`.
- Probe: added the `book` and `scan` layouts and `scan_pages`; the bank gained
  an `items` field. The sheetpipe suites pass (1,342 passed).
- User decision: **bank PDFs tracked with Git LFS** (see §2 and the merge
  note in §5). Pointer-safe tests and scan.
- Phases 3–5 for probability, end to end: 15 knowledge units, `plan` found 6
  gaps, and 6 new generators (brute-force-verified) closed them. The six
  probability sheets are `generated`. Suites pass: core, stages, curriculum,
  choice counts, answer length (7,873), plus the sheetpipe and new-type tests.
- Digest quality issues seen while authoring (not yet fixed):
  - The math font in some A-level files maps digits to symbols
    (`$` = 1, `&` = 0), so those choices read wrong.
  - `(1) 1 ความน่าจะเป็น.pdf` item 7 swallowed a pasted exam page (its
    questions 28–30).
  - The units' `note` fields record both.
- **Next:** repeat the Phase 3–5 loop topic by topic. The digests already
  exist for 1,071 questions across 17 math topics. Or pick up Phase 2's long
  tail (`(สสวท)` files: Latin-1 repair, numbered splitter, OCR).

### 2026-10-02 — session 2
- Rebased the branch onto main (36 commits; no conflicts). The repo-wide suite
  passes (10,257) but now takes ~31 min, so give it a 45-min limit.
- User decision: the picture-maths sheets are transcribed by eye in session,
  not through a model API. Built `transcript.py`; chapter 3 transcribed,
  claimed and closed (3 new sets).

### 2026-10-02 — session 3
- Chapter 11 (จำนวนเชิงซ้อน) closed: files 5–7 and ท้ายบท transcribed by four
  parallel subagents (~25–65k tokens each), spot-checked against the photo
  pages, converted with files 1–4: 8 files, 255 questions, 241 answered (the
  rest are proofs and drawings). All claimed in `complex.json`.
- One new unit, `complex.polynomial-solve` (factor theorem, then the quadratic
  formula over ℂ), and its set `complex_polynomial_solve_m5` in
  `math_bank_complex.py`, placed in the complex path's stage 3. Its test
  compares every root set with SymPy's and pins three textbook answers.
- Chapter 12 (หลักการนับ) closed: 6 files, 137 questions, 136 answered (one
  proof), claimed in `counting.json` and `permutation.json` by existing units;
  no new gap. Figure items (2.1 items 5–6, 2.3 item 5) were re-derived from
  the renders. The chapter-end transcript records the manual's readings of
  ambiguous wording (rectangles exclude squares; one chess pair, not a full
  pairing).
- Chapter 13 (ความน่าจะเป็น) closed: 4 files, 193 questions, 191 answered
  (a tree diagram and a proof), claimed in `probability.json` by existing
  units; no new gap. The figure items (ท้ายบท 7 wheel, 45 snakes and ladders,
  47 grid route) were checked against the renders.
- Chapter 17 (ตัวแปรสุ่ม) closed: 5 files, 146 questions, all answered. Two
  new units in `random-variables.json`: `random.discrete-uniform` (covered by
  the existing `uniform_distribution_m6`) and `random.distribution-variance`
  with a new set `random_variable_variance_m6` (stage 1; probability or
  frequency table → Var, or σ of a symmetric three-point law), tested against
  SymPy's `FiniteRV` and pinned to 4.2ข item 1 and ท้ายบท items 2–3.
- Manual slips recorded in the transcripts: 4.3 item 10 prints σ² ≈ 0.0289
  from a rounded σ (exact 1/36); 4.2.2 item 6.3's setup says p = 0.1 but
  computes with 0.2. Normal-table answers keep the manual's 4-place values,
  with a comment wherever the exact value differs.
- Chapter 14 (ลำดับและอนุกรม) closed: 10 files, 369 questions, 363 answered
  (the rest are proofs). One new unit, `sequence.terms` (terms from a general
  term or a recursion), with the set `sequence_terms_m6` in
  `math_bank_sequences.py` (stage 1 of ลำดับเลขคณิต), checked against
  SymPy's `rsolve` and pinned to 1.1.1 item 2. `series.sequence-limit` now
  states the rⁿ cases its set already practised. Everything else fits existing
  units.
- Manual errors recorded in the ท้ายบท transcript: 21.3 (limit −1, not 0),
  23 (x = ±2 also converge: r = 1), 53 (2,001,942.08, digits swapped), 60
  (51,000 for 510,000 in the working); 1.1.3 item 1.4 prints ratio −1 for 1/3.
  Transcribers that skipped the manual comparison (files 4 and 7) were checked
  by hand against the answer pages' text layer.
- Transcribers must not run while the suite runs if the claim step follows:
  `convert` rewrites `bank.json`, which the suite reads, so convert after.
- Chapters 15 (แคลคูลัส, 10 files, 452 questions), 16 (สถิติ, 2 files), 8's
  ท้ายบท (134 questions, 40 of them proofs) and the two stray `(1)` files
  closed; the bank has no picture-maths file left without a transcript.
  Calculus and trigonometry fit existing units (three existing sets added to
  `covered_by`: `higher_order_derivative`, `indefinite_integral_basic`,
  `continuity_check`/`continuity_k`). Two new units for the stray exam items,
  each with a set: `real.remainders` → `remainder_arithmetic_m4` (stage 3 of
  การหารพหุนาม) and `matrix.power-cycle` → `matrix_power_cycle_m5` (stage 3 of
  เมทริกซ์), checked by brute force and SymPy and pinned to the exam answers.
- Manual errors recorded: แคลคูลัส ท้ายบท 58 (36.83 km, so the 450-baht cap,
  not 25.33 km / 380 baht) and 60 (17/4, not 2); 2.1ก 1.2's table repeats
  rows; 2.8.3 item 8 says วินาที for นาที; ตรีโกณมิติ ท้ายบท 20.10
  (3π/4, not ∅).

### 2026-10-13 — POSN archive local extraction

- The official POSN mathematics archive supplied 25 PDFs. Seven selection
  papers already have green 30-question packages; the other 18 papers were
  extracted locally into the ignored `openthaiknowledge-bank/_local_digest/posn_math/`
  folder, yielding 284 numbered questions and page renders for visual review.
- The scanned 2565 national paper was hand-transcribed locally: 10 questions,
  six with independently checked answers and four proof prompts. The 2554
  paper's 15 pages of worked solutions were kept separate from its 12 prompts.
- Four answers in the 2569 selection paper were checked independently. Two
  original algebra practice sets were added to the public registry, with no
  source text or figures published. All other newly extracted questions still
  require manual figure/notation review, solver checks, and generators.
- The private bank clone was unavailable; the user chose local-only extracts.
  Its tracked index and the bank-wide knowledge coverage stages were not
  advanced. The local progress file records the remaining work.

### 2026-10-13 — POSN bank installation and 2565 national paper

- Restored the private bank clone at `openthaiknowledge-bank/`, preserving the former
  local folder as a sibling backup. Its 25 POSN PDFs and private extracts were
  merged; `bank scan` added 18 exam PDFs and the ignored source manifest.
- Checked and converted the 2565 national transcript: 10 questions, 6 with
  answers and 4 proof prompts. The digest remains in the private bank.
- Claimed questions 2 and 7 with new knowledge units. Original practice sets
  for signed pair sums and recurrence divisibility use independently checked
  solvers; neither publishes source wording or figures.
- Remaining on this paper: questions 1, 3–5, 9 need knowledge mapping and
  suitable generators. The 2569 selection paper and other national papers
  remain in the private review queue.
- Question 8 was checked against its page render. The reduced denominator in
  `aₙ = aₙ₊₁² − aₙ₊₁` is the square of the next term's denominator, forcing
  an infinite rational sequence to consist of integers. Descent leaves only
  the two constant sequences. A shifted original generator and a finite-path
  cross-check now cover the associated knowledge unit.
- Question 6 was checked against its page render. Each disjoint 2×2 block
  holds at most one infected seat if infected seats do not touch and no seat
  receives two transmissions. The 60×60 grid has 900 blocks, so 901 infected
  seats force the stated conclusion. A signal-grid original generator tests
  that block bound, with exhaustive checks on small grids.
- Question 10 was proved using digit sums modulo 9. A multiple of 3 excludes
  infinitely many sums; otherwise one of `n, 2n, …, 9n` supplies any desired
  residue and `n(10^k−1)` supplies a digit-sum increment of `9k` for large k.
  Concatenating these multiples reaches every sufficiently large sum. A
  bounded-count original generator is checked by explicit constructions.
- Question 5 was proved by comparing noncollinear point tuples with the same
  centroid. Any nonzero solution gives a multiplicative character of the
  additive plane; divisibility and the centroid equation force it to be
  constant. An original generator varies the number of points and a nonzero
  coefficient, and independently counts the real roots of the constant
  equation.
- Question 4 was classified by the collision
  `P(0)P(1-u)=P(-v)` for every monic quadratic `P=x²+ux+v`, together with the
  monic construction `x^(n-3)(x³-x)+2` for every `n≥3`. The latter is always
  `2 mod 3`, while products of two values are `1 mod 3`. An original bounded
  degree-count generator covers the unit.
- Question 3 follows by splitting the circle into four right-angle sectors.
  With 543 more blue than pink points overall, one sector has excess at least
  136. Its angular prefix differences change by one at each point, so a prefix
  has excess exactly 100; trimming the boundary yields an acute sector. An
  original four-list prefix-sum generator tests the same pigeonhole and unit-
  step principle without reproducing the source setup. Knowledge coverage is
  8/10; geometry items 1 and 9 remain.
- Page 2 of the 2569 selection paper was reviewed for items 3 and 5. Their
  private digest is explicitly partial (2/30), and the bank entry remains
  `new`. Item 3's fixed-gcd, square-lcm sum is 1500; item 5's real-root product
  after polynomial composition is 35. Two original generators vary the
  parameters, with direct enumeration and exact-root checks respectively.
  The remaining 28 items are not represented by this partial digest.
- Page 3 of that paper was checked for items 8 and 9, extending the partial
  digest to 4/30 while leaving the bank entry `new`. Counting noncollinear
  triples among square-edge marks gives 4736, and counting distinct sums of
  three draws from six powers of three gives 56. Original generators extend
  these to convex polygons and bounded power-sum multisets, with direct
  coordinate and sum-enumeration checks. The other 26 items remain unreviewed
  in the digest.
- Page 3 item 10 and page 4 item 11 of the 2569 selection paper were checked
  against page renders. The explicitly partial digest now contains 6/30 items;
  the bank entry remains `new`. The consecutive obtuse-triangle event has
  probability 1/84, giving requested sum 85. Five-position proper colorings
  with three colors used at most twice number 36. Original generators vary the
  progression gap and capped path-coloring parameters; direct enumeration
  checks both solvers. The other 24 items remain unreviewed in the digest.
- Page 4 items 12 and 13 of the 2569 selection paper were checked against the
  render. The explicitly partial digest now contains 8/30 items; the bank
  entry remains `new`. The probability of three distinct labels from the
  overlapping boxes is 9/20. The six-character code count is 48,000 because
  digits may repeat, while the four vowels must be distinct. Original
  generators vary box overlaps and code alphabets, with independent exhaustive
  checks. The other 22 items remain unreviewed in the digest.
- Page 5 items 15 and 17 of the 2569 selection paper were checked against the
  render. The explicitly partial digest now contains 10/30 items; the bank
  entry remains `new`. Three water depths determine a rectangular box capacity
  of 480 cubic centimeters, and perpendicular chords determine a circle area
  of 65π. Original generators vary box dimensions and chord segments, with
  physical-box and exact-coordinate circle checks. The other 20 items remain
  unreviewed in the digest.
- Page 6 items 18 and 19 of the 2569 selection paper were checked against the
  render. The explicitly partial digest now contains 12/30 items; the bank
  entry remains `new`. Incenter parallels give a sum of three small-triangle
  perimeters equal to the original perimeter, 40. A circle through an altitude
  foot and base midpoint meets a side again at distance 134/13 from the apex.
  Exact-coordinate checks validate both original generators. The other 18
  items remain unreviewed in the digest.
- Page 7 figure items 21 and 22 of the 2569 selection paper were checked
  against the render. The explicitly partial digest now contains 14/30 items;
  the bank entry remains `new`. A circle tangent to two sides and passing
  through a square's center gives square area 8. A tangent and horizontal
  chord give circle area 60 from a triangle area. Exact-coordinate checks
  validate both original generators; source figures remain private. The other
  16 items remain unreviewed in the digest.
- Page 8 figure items 23 and 24 of the 2569 selection paper were checked
  against the render. The explicitly partial digest now contains 16/30 items;
  the bank entry remains `new`. Three tangent semicircles give equilateral
  triangle area 27√3, and four equal links give a circle central angle of
  106°. Original generators vary the radius and apex angle, with coordinate
  checks for all tangencies and the circle center. The other 14 items remain
  unreviewed in the digest.
- Page 9 items 25 and 26 of the 2569 selection paper were checked against the
  render. The explicitly partial digest now contains 18/30 items; the bank
  entry remains `new`. Minimizing the squares of the final three labels gives
  208 for the first six. The racing conditions allow five distinct pairs of
  first- and third-place finishers. Original generators vary the fixed sum and
  race constraints; independent exhaustive enumeration checks both solvers.
  The other 12 items remain unreviewed in the digest.
- Page 9 items 27 and 28 of the 2569 selection paper were checked against the
  render. The explicitly partial digest now contains 20/30 items; the bank
  entry remains `new`. The digit-ordering puzzle has eight valid five-digit
  endings, and two equal-share observations give 1,344 chicks initially.
  Original generators vary the target digit sum and redistribution sizes;
  independent enumeration and sharing checks validate them. The other 10
  items remain unreviewed in the digest.
- Page 10 items 29 and 30 of the 2569 selection paper were checked against
  the render. The explicitly partial digest now contains 22/30 items; the
  bank entry remains `new`. Conditional switch passes leave 845 switches on.
  Strictly diagonal-free strip placements give 86 favorable pairs out of
  12×12, so the probability is 43/72 and the requested value is 4372.
  Original generators vary switch divisors and grid dimensions; independent
  set-count and cell-enumeration checks validate them. Eight items remain
  unreviewed in the digest.
- Page 2 items 1 and 2 of the 2569 selection paper were checked against the
  render. The explicitly partial digest now contains 24/30 items; the bank
  entry remains `new`. Expanding shifted squares gives 1086, and simplifying
  the symmetric cubic quotient using the roots' sum and product gives 425.
  Original generators vary the power sums and quadratic roots; direct
  numerical substitution checks both identities. Six items remain unreviewed.
- Page 3 items 6 and 7 of the 2569 selection paper were checked against the
  render. The explicitly partial digest now contains 26/30 items; the bank
  entry remains `new`. Checking all three coefficient swaps gives the unique
  positive integer 11. Reducing the polynomial quotient at a quadratic
  irrational gives exactly 5. Original generators vary the quadratic
  coefficients and reducible quotient; rational-root enumeration and SymPy
  substitution check them. Four items remain unreviewed.
- Page 2 item 4 and page 4 item 14 of the 2569 selection paper were checked
  against their renders. The explicitly partial digest now contains 28/30
  items; the bank entry remains `new`. A nested-radical substitution gives
  minimum parameter 7 for two distinct real solutions. Row fractions and the
  stated size range give a 24-person group. Original generators vary radical
  offsets and row fractions; direct root substitution and integral-headcount
  enumeration check them. Items 16 and 20 remain unreviewed.
- Page 5 figure item 16 and page 6 figure item 20 of the 2569 selection paper
  were checked against their renders. The digest now contains all 30/30 items.
  Vector closure gives the notched hexagon perimeter 80; the area of the
  diagonal 8–15–17 triangle gives (ab+bc+ca)² = 19200. Original generators
  vary side lengths and diagonal squares, with exact-coordinate and direct
  algebra checks. Knowledge coverage is 30/30, the bank entry is `generated`,
  and source figures remain private.
- Question 1 of the 2565 national paper is now solved and mapped. Power of the
  interior point gives the side ratio; outward right-isosceles constructions
  give an SAS similarity, then equal inscribed angles give equal chords.
  Coordinate line-circle intersections independently check the result. An
  original mirrored-rotation ratio generator practices the similarity lemma.
  Knowledge coverage is 9/10; only the geometry proof in item 9 remains.
- The remaining 2565 national geometry item is now solved and mapped.
  A tangent-chord identity places the first intersection on the opposite
  contact chord; two Menelaus applications turn the construction into
  complementary angle bisectors. An original triangle exercise asks for
  the variable segment ratio behind the proof, with exact-coordinate
  checks. Knowledge coverage is 10/10 and the bank entry is `generated`.
- Items 6 and 8 of the 2567 national paper were checked against the page 2
  render. A zero-sum half of the symmetric nonzero integers exists for every
  n at least 2, using opposite pairs and, for odd n, the triple -2,-1,3.
  The opposite midpoint chords of a convex hexagon satisfy UX + WZ = VY as
  directed vectors, giving strict triangle inequalities. Original generators
  exercise the partition classification and the chord cosine relation;
  brute-force subsets and exact midpoint coordinates independently check them.
  The private digest is partial (2/10); the bank entry remains `new`.
- Page 2 items 7 and 9 of the 2567 national paper are now verified. For item
  7, the cubic roots are 1 and a conjugate sixth-root pair; seventh powers
  preserve them, and a multinomial coefficient counts the tuples. For item 9,
  CRT produces consecutive numbers with a prime valuation of exactly one;
  the central binomial coefficient for a=d-1 is divisible by d. Original
  generators vary tuple sizes and prime-square congruences. Independent
  ordered-tuple enumeration, brute CRT search, perfect-power checks, and
  direct binomial divisibility checks support the solutions. The private
  digest is partial (4/10); the bank entry remains `new`.
- Items 3 and 10 of the 2567 national paper are now verified against the
  rendered pages. Normalizing the functional equation and using image-value
  anti-periods forces f(x)=sqrt(c)/x. Concavity equalizes opposite cube roots
  in the cyclic-product problem; one-variable optimization gives the exact
  maximum 4^14/5^10 for the source constraint. Original generators vary the
  constant and the cube-root sum. Exact substitution, symbolic concavity,
  an attaining configuration, and a rational grid check support the results.
  The private digest is partial (6/10); the bank entry remains `new`.
- Items 2 and 4 of the 2567 national paper are now verified against page 1.
  The paired fifth-power divisibility conditions force coprime m,n, then
  incompatible eighth- and twenty-fourth-power congruences unless m=n=1.
  The grid minimum is 2024: a row with at most 22 purple cells forces at
  least 231 columns to have at least 9, while eleven complete 8-by-23 blocks
  attain the bound. Original generators vary modular remainders and block
  dimensions; direct exponentiation, finite search, small-grid brute force,
  and constructive checks independently verify them. The private digest is
  partial (8/10); questions 1 and 5 remain and the bank entry stays `new`.
- The last two 2567 national questions, 1 and 5, are now mapped. Equal arm
  lengths give a directed intersection parameter on BD from both A and C;
  equality forces AB+CD=BC+AD for interior construction points. A coordinate
  model for the acute triangle gives the same slope from D to the two
  right-angle intersections on its circumcircle when AH=2HD. Original
  generators vary the directed parameter and the triangle coordinates;
  exact line and circle intersections check both. The source wording of
  item 1 permits a boundary interpretation that gives a counterexample;
  the private notes record this and the set explicitly uses interior points.
  Knowledge coverage is 10/10 and the bank entry is `generated`.
- Began the 2566 national paper with page 1 items 1 and 4. Wilson's theorem
  reduces the 20-integer product modulo 23 to a quadratic nonresidue unless
  the sum is divisible by 23. Coloring each match by the losing score gives
  a bound of 100 players when every triangle is monochromatic or rainbow,
  contradicting the paper's 101. Original generators vary near-complete
  residue products and sharp color bounds for affine planes of prime order.
  Direct modular products and exhaustive small-plane triangle checks support
  the results. The private digest is partial (2/10); eight items remain, and
  the bank entry stays `new`.
- Page 1 item 3 and page 2 item 9 of the 2566 national paper are now mapped.
  The functional equation has exactly the zero map and the two signed identity
  maps; an exhaustive finite-field search checks the classification on small
  fields. A simple root of a²+a+2023 modulo 7 lifts through every power of 7,
  giving arbitrarily many divisors; brute congruence search checks the first
  levels. Original generators vary the equation's scale and the lifting
  constant and depth. The private digest is partial (4/10); items 2, 5, 6, 7,
  8, and 10 remain pending, and the bank entry stays `new`.
- Page 2 items 6 and 7 of the 2566 national paper are now mapped. Cauchy
  and AM–GM prove the sharp cyclic inequality, with equality when a=b=c;
  exact rational samples check its homogeneous extension. The diagonal-strip
  lamp minimum is n+1: off-diagonal lamp pairs can be replaced by diagonal
  endpoints without increasing the count, after which every diagonal point
  needs a lamp. Exhaustive small placements and independent integer
  optimization support the construction. Original generators vary the
  product constraint and strip length. The private digest is partial (6/10);
  items 2, 5, 8, and 10 remain pending, and the bank entry stays `new`.
- Page 1 item 2 and page 2 item 10 of the 2566 national paper are now mapped.
  Side-weighted coordinates show that the incenter and excenter heights sum
  to BC, putting their midpoint on its perpendicular bisector; exact and
  numerical coordinate checks support a height generator. The flag colors
  are cyclic cosets. A primitive-root sum forces at least three smallest
  color classes for odd vertex count, while prime-power examples force and
  attain p classes; exact-cover enumeration checks small polygons. The
  private digest is partial (8/10); only items 5 and 8 remain pending, and
  the bank entry stays `new`.
- The last two 2566 national questions, 5 and 8, are now mapped. A cotangent
  comparison confines the second viewpoint to a sharp wedge and gives the
  minimum angle 270°−θ; numerical sight-angle checks verify the boundary.
  Coordinates of the two tangent-circle intersections make EF horizontal and
  give PQ=2a(u²+v²−a²)/(u²+v²+a²) when AB=2a; exact rational circle and line
  constructions independently verify EF=PQ+AB. Original numeric variants
  are registered for both topics, and the private digest covers all ten items.
  The bank entry is `generated`.
- Began the 2564 national paper with items 2 and 6. The positive-integer
  recurrence has a unique sequence: its nonnegative quotient would otherwise
  be divisible by arbitrarily large products. The 21-by-21 odd-parity grid
  has 2^400 colorings, since the final row and column are forced by the
  freely chosen 20-by-20 block. Parameterized generators vary the recurrence
  constants and same-parity grid dimensions. Direct recurrence searches and
  exhaustive small-grid counts independently check them. The private digest
  is partial (2/10), and the bank entry remains `new`.
- Items 1 and 7 of the 2564 national paper are now mapped. Coordinates of the
  tangent contact points show their crossing chord meets the isosceles base
  at its midpoint; direct tangent construction checks varied exact triangles.
  The functional equation has only the constant solutions 0 and ±1, since
  f(1) either vanishes identically or forces nonvanishing and then constancy.
  A scaled version varies the two nonzero values; finite-domain enumeration
  and exact substitutions independently check it. The private digest is
  partial (4/10), with six questions remaining and the bank entry still `new`.
- Items 8 and 10 of the 2564 national paper are now mapped. Equal powers of A
  to the two diameter circles force equal side fractions, placing P on the
  A-median; exact line intersections and circle geometry check a height
  generator. Reciprocal pairing puts at least seven roots of a degree-13
  palindromic polynomial in the unit disk, where six angular sectors force
  two roots less than one unit apart. A degree-varying generator counts the
  pairs certified by that argument; independent occupancy optimization and
  reciprocal-root constructions check its bound. The private digest is
  partial (6/10); items 3, 4, 5, and 9 remain, and the bank entry stays `new`.
- Item 3 of the 2564 national paper is now mapped. The reciprocal-sum
  constraint bounds abc and a+b+c by AM–GM; convexity of x^(x−1) minimizes
  a^a bc+b^b ca+c^c ab at a=b=c=3. The scaled generator has attained
  minimum 3(3k)^(3k+2), checked by
  direct evaluation of all small integer reciprocal triples. The private
  digest is partial (7/10); items 4, 5, and 9 remain, and the bank entry
  stays `new`.
- Item 9 of the 2564 national paper is now mapped. Coprime reduction of the
  LCM divisibility condition forces each pair's difference to equal its gcd.
  The least member makes S finite; comparing the least and greatest shows any
  intermediate member would generate an LCM quotient above the greatest.
  A minimum-to-maximum generator covers both possible two-member families,
  with exhaustive small-set checks. The private digest is partial (8/10);
  items 4 and 5 remain, and the bank entry stays `new`.
- Item 4 of the 2564 national paper is now mapped. Each of 21 near-diameter
  chords splits the other 19 gates into groups of 9 and 10 and has 90 distinct
  crossings. Two lotus-pot types force at least 45 of one type, lighting all
  21 paths; two path materials force at least 11 lighted paths of one material.
  A gate-count generator asks for this bound, with direct chord enumeration and
  small exhaustive colourings as independent checks. The private digest is
  partial (9/10); item 5 remains, and the bank entry stays `new`.
- A higher-resolution reading corrected items 3 and 4 and resolved item 5 of
  the 2564 national paper. Item 3 is a^a bc+b^b ca+c^c ab and now uses
  convexity of x^(x−1); item 4 requires 11 lighted paths sharing a material,
  obtained by two pigeonhole steps. Item 5 has 4^k p^4 and odd m,k. Prime-power
  reduction followed by Sophie Germain factorization leaves only (5,5,1),
  verified by direct substitution and a bounded independent search. The
  complete 10/10 digest and all ten generator links are recorded in the bank;
  coverage and plan checks advanced its stage to `generated`.
- Items 1 and 2 of the 2563 national paper are now mapped. Partitioning
  n-cycles into generator classes proves phi(2n)|n!; an Euler-product
  generator varies the quotient and independent tests enumerate reduced
  residues and small cycle groups. A reverse-order elf assignment minimizes
  the latest delivery at floor((N+1)^2/4), with brute-force matching checks.
  The private digest is partial (2/10); items 3–10 remain and the bank entry
  stays `new`.
- Item 3 of the 2563 national paper is now mapped. Tangential kites and squares
  give midpoint Jensen and a scaling identity, which together force additivity.
  A rational-value generator uses this result, with exact repeated-addition
  checks. The private digest is partial (3/10); items 4–10 remain and the bank
  entry stays `new`.
- Item 7 of the 2563 national paper is now mapped. Values at zero and one
  restrict the integer-valued inequality to three functions: zero, one, and
  the indicator of zero. A parameterized generator asks for possible sample
  sums; finite-domain function enumeration checks the classification. The
  private digest is partial (4/10); items 4–6 and 8–10 remain. Item 5's
  three-edge process still needs a complete existence proof.
- Item 10 of the 2563 national paper is now mapped. Polynomial congruence
  forces every value P(m) to divide the fixed factorial offset, so P is
  constant. The source case has only P=±1; a parameterized starting index and
  offset produce a divisor-count generator, checked against direct factorial
  gcds. The private digest is partial (5/10); items 4–6 and 8–9 remain.
- Item 9 of the 2563 national paper is now mapped. Each tractor visits one
  cell per fixed-coordinate-sum diagonal, giving a lower bound of (n−k)²
  unvisited cells. Boundary and nested L-shaped routes attain the bound;
  exhaustive small-grid path combinations check it independently. The private
  digest is partial (6/10); items 4–6 and 8 remain.
- Item 8 of the 2563 national paper is now mapped. Cauchy reduces the cyclic
  fraction sum to a bound in the sums of squares and cubes; power means prove
  the minimum 1 at equal variables. A scaled generator has minimum t⁴, checked
  on exact rational grids. The private digest is partial (7/10); items 4–6
  remain.
- Item 6 of the 2563 national paper is now mapped. With tangent lengths
  x=AF=AE and y=BF=BD, the two angle-bisector intersections on AB satisfy
  AL=x²/(x+y) and AK=x+xy/(x+y). Thus the stated triangles are similar and
  FK=FL=xy/(x+y). Independent coordinate ray reflections check both
  bisectors across acute triangles. The private digest is partial (8/10);
  items 4–5 remain.
- Item 4 of the 2563 national paper is now mapped. Coordinate equations for
  the two circles make their tangents meet AB and AC at height huv/(h²+uv),
  while EF meets the altitude at twice that height. An exact rational
  construction of feet, circumcentres and line intersections checks the
  midpoint generator. The private digest is partial (9/10); item 5 remains.
- Item 5 completes the 2563 national paper. An edge count forces n≡0 or 2
  modulo 3. Boundary-ring capacity forces the inner open grid's side cells to
  alternate, so n must be odd except for n=2. Base constructions and a
  repeatable six-wide frame prove every n≡3 or 5 modulo 6 works. An explicit
  edge-owner test validates constructions through n=61 and tiny boards by
  exhaustive search. All ten items are mapped; the bank entry is `generated`.

### 2026-10-16 — 2562 national paper; science papers indexed

- Cloned the bank. `bank scan` found 177 new non-maths สอวน. papers (physics,
  chemistry, biology, computing, astronomy, geography, earth science, IJSO,
  linguistics). It indexed only their `MANIFEST.json`, `.docx` and `.emf`
  files, all as `ignored`. Their ~1,000 PDFs stay unindexed until fetched;
  they need a science knowledge path that does not exist yet. The user chose
  to finish the POSN maths papers first.
- The 2562 national paper (16th TMO) went through the documented route: a
  transcript in `_transcribed/`, then `convert`. 10 questions; 4 have answers
  (3: f(x) = √(4x + c) with c ≥ 0, not just 2√x; 4: a = ±1; 6: f(x) = x/2;
  9: 4038), and 6 are proofs.
- Ten knowledge units (`olympiad_*.json`) claim the ten items, each covered by
  a new original set in `otk/sets/math/olympiad/`. Their independent checks
  are in `test_math_olympiad_posn_national_2562.py`: coordinates for 1 and 8,
  unbounded search for 2, substitution for 3, enumeration and a bitset parity
  DP (including total 2019) for 4, brute-force bijections for 7, the
  angle-sum bound for 9, and direct factorials for 10. Proof sketches are in
  the bank's `_notes/posn-national-62-math.md`. The bank entry is
  `generated`.
- **Open:** item 5 (Σ(4a − 1)/(2b + 1)² ≥ 1 under abc = 1) has no written proof
  yet. The bound is checked numerically, and the set relies only on the exact
  scaling identity plus that bound. A separable tangent-line proof is
  impossible here; the note says why.
- `test_refactor_characterization` freezes the registry size, now 3,759.
- Remaining POSN maths at `new`: the national papers 2547–2557 (11 papers).

### 2026-10-16 — 2557 national paper

- The 2557 national paper (11th TMO) went through the same route. 8 questions,
  5 answered:
  - 2: f(x) = x and f(x) = −x²;
  - 4: P = ±1, since gcd(2557 + 213·2014, 2557·2556) = 1;
  - 5: k = ∛9 − 1;
  - 6: p = 2, 3;
  - 8: n(n − 1)/2 + 1 cards.

  Items 1, 3 and 7 are proofs.
- Eight knowledge units and eight original sets cover them, checked in
  `test_math_olympiad_posn_national_2557.py`. The bank entry is `generated`.
- Item 7's point E is the one with BE ∥ AD, which gives
  O₁O₂ = AB/(2 sin ∠ADC). The tempting "ABED cyclic" is wrong, and the
  coordinates show why.
- Open: item 2's case f(1) = −1 is proved only for rational x; the step for
  irrational x is only sketched in the note.
- Registry 3,767 sets; enrichment count 310.
- Remaining POSN maths at `new`: national papers 2547–2556 (10 papers).

### 2026-10-16 — 2556 national paper

- The 2556 national paper (10th TMO): 12 questions, 6 answered.
  - 1: 48, because p > 4 includes p = 5; this is not the familiar 240.
  - 2: BC = 3 + √3.
  - 4: five polynomials.
  - 5: n = 21301.
  - 6: f = 0, ±x, ±|x|.
  - 10: (2, 14).
- Twelve knowledge units and twelve original sets cover the paper, checked in
  `test_math_olympiad_posn_national_2556.py`. The bank entry is `generated`.
- A SymPy check caught a sign slip in the item 8 set: a₃ carries (−1)ⁿ⁻¹. The
  minimum variant now uses even n only.
- Item 12's area equality is verified by coordinates only; no synthetic proof
  is written.
- Registry 3,779 sets; enrichment count 322.
- Remaining POSN maths at `new`: national papers 2547–2555 (9 papers).

### 2026-10-16 — 2555 national paper

- The 2555 national paper (9th TMO): 12 questions, read from the renders
  because the text layer misplaces Thai vowels. 3 have answers:
  - 5: f(x) = 2x + 1;
  - 6: n = 197;
  - 8: P/Q = (3n − 1)/(4n − 1).

  The other 9 are proofs.
- Twelve knowledge units and twelve original sets, checked in
  `test_math_olympiad_posn_national_2555.py`. The bank entry is `generated`.
- A TeX trap: a clean-up step strips a coefficient "1" before a letter, so
  `d_1d_2` renders as `d_d_2`. Write subscripts braced, as `d_{1}`.
- Open: item 5's uniqueness proof stops at z = ±1/2, so the set asks only for
  the linear solution. Item 11 is checked by coordinates only.
- Registry 3,791 sets; enrichment count 334.
- Remaining POSN maths at `new`: national papers 2547–2554 (8 papers).

### 2026-10-16 — 2554 national paper

- The 2554 national paper (8th TMO): 12 questions on pages 1–2. Pages 3–17
  are official worked solutions, used only as a cross-check.
- Answers:
  - 2: f ≡ 1.
  - 5: n ∈ {1, 625, 6561, 4100625}.
  - 6: 1005·1006/2011.
  - 10: no such f.
  - 12: 2·3²⁵⁵⁴.

  The first four agree with the official key.
- **The official key undercounts item 12.** It prints 3² + 3¹²⁷⁷ + 3²⁵⁵⁴ and
  counts only one shift direction per period. Brute force on 6, 12 and 15
  chairs gives 2·3ᵐ. The transcript carries the corrected answer, with a
  comment, as the (สสวท) transcripts do for teacher's-manual errors.
- Twelve knowledge units and twelve original sets, checked in
  `test_math_olympiad_posn_national_2554.py`. The bank entry is `generated`.
- Registry 3,803 sets; enrichment count 346.
- `test_per_set` caught two choice-length cues, and both sets were reworked:
  - a "∅" answer was always the shortest choice, so item 10 became a count
    of the (a, b) pairs that admit a solution;
  - a reduced N/4 answer was the shortest choice, so item 6 now uses odd N,
    as in the source.
- Remaining POSN maths at `new`: national papers 2547–2553 (7 papers).

### 2026-10-17 — 2553 national paper

- The 2553 national paper (7th TMO) has 16 questions: 10 on day 1 and 6 on
  day 2, with numbering restarting on day 2. The transcript uses two sections,
  and the knowledge units cite `{sheet, section, number}`.
- Answers:
  - day 1, item 1: 55;
  - day 1, item 2: DF is a diameter, = xyz/(2Δ);
  - day 1, item 4: 150°;
  - day 1, item 9: −1/2;
  - day 1, item 10: p = 7;
  - day 2, item 5: f ≡ 1005/2.
- Sixteen knowledge units and sixteen original sets, checked in
  `test_math_olympiad_posn_national_2553.py`. That file includes a
  Greenwood–Gleason colouring of K16, which shows R(3,3,3) = 17 is needed in
  the day 2, item 2 argument. The bank entry is `generated`.
- Set modules must register at least one set (`test_sets_layout`), so a shared
  helper module in `olympiad/` is not allowed; helpers are inlined.
- Open (sketched only):
  - day 1, item 6: proof that f is even;
  - day 2, item 4: the altitude inequality;
  - day 2, item 5: uniqueness in the plane.
- Registry 3,819 sets; enrichment count 362.
- Remaining POSN maths at `new`: national papers 2547–2552 (6 papers).

### 2026-10-17 — 2552 national paper

- The 2552 national paper (6th TMO) has 16 questions over two days, laid out
  like 2553. 9 have answers:
  - day 1, item 1: 2;
  - day 1, item 2: (n − k)2ᵏ⁻¹;
  - day 1, item 3: 393215;
  - day 1, item 4: 3/20;
  - day 1, item 5: x + 1;
  - day 1, item 6: 2(c − b)/(a + b + c);
  - day 1, item 9: √((4 − √3)/13);
  - day 2, item 2: no such f;
  - day 2, item 6: three polynomials.
- Sixteen knowledge units and sixteen original sets, checked in
  `test_math_olympiad_posn_national_2552.py`. The bank entry is `generated`.
- Open (sketched only):
  - day 1, item 5: uniqueness beyond linear f;
  - day 2, item 3: the "only if" direction;
  - day 2, item 5: the Zarankiewicz and pigeonhole argument;
  - day 2, item 6: the degree bound.
- Registry 3,835 sets; enrichment count 378.
- Remaining POSN maths at `new`: national papers 2547–2551 (5 papers).
