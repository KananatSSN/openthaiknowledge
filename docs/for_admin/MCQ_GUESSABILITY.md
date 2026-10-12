# MCQ guessability: audit and fix tracker

Multi-session work to stop students from answering problem sets by test-taking
cues (the longest choice, the smallest number, the odd one out) instead of
the subject. Update this file at the end of every session.

Branch: `fix/mcq-guessability` (merge to `main` when a workstream is done and
tests pass; start the next one on a fresh branch).

## How to measure

```sh
python -X utf8 scripts/audit_mcq_cues.py --csv docs/for_admin/mcq_cue_audit.csv   # ~1 min, all sets
python -X utf8 scripts/audit_mcq_cues.py --only <key> [<key> ...]                  # numbers for a few sets
python -X utf8 scripts/audit_mcq_cues.py --only <key> --show 5                     # print draws
```

`mcq_cue_audit.csv` is the worklist: one row per set, flagged sets first. Each
measure is the share of 60 seeded draws where following the cue picks the
correct choice (chance is 1/n: 25% with four choices, 33% with three).

| Flag | Measure | Flagged when |
|---|---|---|
| `longest` | correct choice is visibly the longest: longer than every distractor by 10% of its length and at least 3 characters | >= 45%, and >= chance + 20% |
| `shortest` | correct choice is visibly the shortest, by the same gap | >= 45%, and >= chance + 20% |
| `rank` | numeric choices: commonest sorted position of the correct value | >= 60% (20+ numeric draws) |
| `convergent` | correct choice is most similar to the others (each distractor alters one part of it) | >= 60% |

The older `scripts/audit_answer_length.py` (and `otk/tests/test_answer_length.py`)
only catches a correct answer that is at least 8 characters and 25% longer than
every distractor; most real leaks sit under that bar, so it is not the target.

## Scoreboard

Sets flagged (of 3,335), 60 draws each. The baseline is `8057f7d` measured
with today's rules (visible-gap length rule, chance-relative bar).

| Flag | Baseline | Now | Target |
|---|---:|---:|---:|
| `rank` | 614 | 10 | 0 |
| `longest` | 307 | 0 | 0 |
| `shortest` | 20 | 0 | 0 |
| `convergent` | 291 | 56 | ~16 are `posn*` past-paper sets, kept as they are |

## Workstreams

### 1. Numeric rank cue (`rank`) — in progress

Cause: hand-picked mistakes err in one direction (adding instead of
subtracting always overshoots; science "slips" are ×2, ×10, +1), so the
correct value sat at the same sorted position every draw. `numeric_neighbors`
(+1, −1, +2) put it second smallest every time.

Done:
- [x] `rank_balanced` in `otk/core/distractors.py`: for a numeric answer
  (optionally with a shared unit suffix) draws how many distractors fall below
  it and fills each side from the strategy's candidates in authored order.
  The first candidate (the most diagnostic mistake, e.g. the nuclide's other
  corner number) is always kept when there are 3+ distractor slots; with 2
  (three-choice Foundation items) it leads its side instead, offered 2 draws
  in 3, because pinning would leave the answer's rank all but fixed.
- [x] Applied to every type in `QuestionType.generate` (reorders only; never
  invents a value, because where the choices are the stem's own numbers an
  invented one could be correct).
- [x] `MathType` / `WordProblem` use `invent=True`: a short side is topped up
  with near values spaced at the answer's second significant digit.
- [x] Science numeric helpers offer slips on both sides (÷2/×2, ÷10/×10, ±1,
  ±2) instead of exactly three that overshoot: `science_wave_f3.numeric`
  (used by ~90 modules), `_numeric` in e11/e13/e14/e15, e10 `_accel` and final
  velocity, e12 transformer, e9 `_amount_choices`.
- [x] `math_m4.maths` (used by the apply-stage and several chapter modules)
  always follows the named mistakes with ±1, ±2, ±5 neighbours.

Remaining (76 sets, see CSV `rank` flag). Each needs its own builder
looked at; a set at 1.00 means every distractor errs one way. Groups:
- Science builders with their own lists: `science_wave_f1` (buoyancy,
  friction coefficient, gauge pressure, mechanical equilibrium), `d10`
  (concentration), `c12` (water amount), `d15` (spring scale), `d28` (heat
  quantity, thermometer), `e7` (vector resultant), `f33` (equilibrium), and
  one-offs listed in the CSV.
- Computing (13): trace/loop/condition items whose outputs are counts
  (`technology_t1s4`, `t3s3`, `t4`, `t1s5`, `t3s2`, ...).
- Math pictures/diagrams/charts (`math_diagrams.py`, `math_pictures*.py`,
  `math_gaps_shape_data.py`, `math_formats.py`), `place_value_millions_p4`
  (1.00), `complex_nth_roots_m5` (0.96).
- Sets whose choices are the stem's own numbers ("which is largest") are only
  a real cue if the choice list is not fixed by the stem; check before fixing.

### 2. Longest-answer cue (`longest`) — in progress

Baseline 307 sets under the visible-gap rule (the first audit's 458 counted
119-against-121 differences nobody can see).

Done:
- [x] `length_balanced` in `distractors.py`, applied to every non-numeric
  answer in `QuestionType.generate` (through `balanced`): when the chosen
  distractors are all visibly shorter (or longer) than the answer and the
  strategy has a spare that is not, the spare replaces the furthest one.
- [x] 366 call sites passed `rng.sample(wrongs, 3)` into `labelled` /
  `_labelled`, which hid the spares from the balancer; they now pass the whole
  list (`label_pool` shuffles, so draws stay as varied).
- [x] `ConceptBankType` passes every distractor to `label_pool` (it used to
  sample three first, hiding the spares).
- [x] Rewritten by hand, all now clear: every flagged set in
  `technology_t1`, `t1s3`–`t1s7`, `t2s1`–`t2s4`, `t3s1`, `t3s4`–`t3s6`
  (computing and design-technology, 38 sets); `substances.py` (11 chemistry
  sets); `science_wave_a.py` (5); `math.py` ivt, linear approximation,
  surface area of revolution, series tests; `science_wave_f63` (4),
  `science_wave_b` (4), `science_pilots` (4), `science_wave_f82` (4),
  `astronomy.py` (4), `science_wave_f79` (4).

How to rewrite a bank (the pattern that worked):
1. `python -X utf8 scripts/list_length_leaks.py --keys <key>` shows the
   leaking items; find the bank by its correct text.
2. Keep the correct answer (trim only if it carries detail the question does
   not need). Rewrite wrongs as real misconceptions *in the same shape*: if the
   answer is "X เพราะ Y", each wrong is "X' เพราะ Y'"; if the answer lists
   three parts, each wrong lists three parts (one slipping in the variable,
   one the measured result, one irrelevant). This also removes joke
   distractors (workstream 3).
3. `python -X utf8 scripts/check_bank_lengths.py <module> <BANK>` until it
   reports 0 rows, then `scripts/audit_mcq_cues.py --only <keys>`.
4. Do not make every wrong a one-slip copy of the answer: the answer then
   becomes the centre of the cluster and trips `convergent` (seen on
   `comp.logic_design_foundation`). Keep one near-copy per row at most.
5. Thai vowel and tone marks count as characters: measure, do not eyeball.
6. Write files with `newline="
"` (Python on Windows writes CRLF otherwise).
7. Keep each bank's row contract: the technology tests hold exactly five
   wrongs per row (and variety floors of 25 distinct questions). If a rewrite
   drops a wrong, add one back with `scripts/append_bank_wrongs.py`, which
   finds the row by its correct text (ast offsets are UTF-8 bytes; the tool
   converts them for Thai).
8. Replace a short wrong only inside its own item: short strings ("การกรอง",
   "น้ำเกลือ") also appear in category tables and other items. Anchor on the
   item's stem or correct text, and check for duplicate choices afterwards
   (`label_pool` does not de-duplicate).
9. Prefer `scripts/replace_bank_text.py` (by value, via ast) over text
   search: bank strings are often split across lines. It skips a value that
   occurs twice (one row's answer is another's distractor); handle those by
   hand. Content-review tests pin some misconceptions and qualifiers by
   phrase (e.g. "ขึ้นเวลาเดิมทุกวัน", "บางพื้นที่อาจมีรูปแบบต่างออกไป"): keep
   the phrase and give every choice the same qualifier instead of dropping it.
   After a batch, scan for duplicate choices within a row.
10. For formula recall (math), the full formula is the longest and every
   one-slip distractor makes it the centre (`convergent`). Use distractors as
   complete as the answer that are not all copies of it;
   `tmp`-style search over candidate sets with `SequenceMatcher` helps.

Remaining (191 `longest`, 13 `shortest`): science files, worst first from the
CSV. Next: `science_wave_f78`, `d28`, `f40` (four sets each), then about 120
files with one to three sets.

Still to add: a test that fails when a set's `longest` share is >= 45%, with
an allow-list of the sets not yet fixed that only ever shrinks.

### 3. Implausible distractors — not started

Not measurable automatically. Seen widely in science foundation sets:
"ทายาสีฟันทันที", "เช็ดด้วยมือเปล่าทันที", "การเผาไหม้ถ่านหิน" (Sun's energy),
"ไม่มีปัญหาใด", "น้ำไม่ดูดกลืนแสงเลย". Replace with real misconceptions
students hold. Fix these while doing workstream 2, set by set.

### 4. Smaller cues — not started

- Yes/no stems padded to four choices with two fillers (19 sets): make them
  genuine four-way questions or two-choice items. 2026-09-30: rechecked;
  most are now four-way (yes/no crossed with a right or wrong reason).
  `phys.light_travel_application` (both scenarios) and
  `chem.redox_series_foundation` were still padded with absolute fillers
  ("เสมอ", "ทุกกรณี") and are now four-way too, and
  `biology.blood_transfusion_fluency` lost its "ได้ทุกกรณี" filler. Still
  padded, because the answer is a bare label with nothing to hang a reason
  on: `chem.hydrogen_bond_fluency`, `chem.electrolyte_dissociation_foundation`,
  `chem.hydrocarbon_saturation_fluency`, `biology.plant_response_application`.
  Decided 2026-09-30: two-choice items. All four now set `max_choices = 2`
  and offer only the opposite label. `chem.electrolyte_dissociation_foundation`
  gained two "no" rules (ethanol, urea) so its answer is not usually the
  shorter label. Three of them then fell below the wave H floor of 25
  distinct questions, having met it only because shuffled fillers made draws
  look new. Their banks grew on 2026-10-01 to 26 items each, half yes and half
  no: electrolyte rules name an example substance (ionic, acid, base; covalent
  non-acid), hydrogen bond adds substances with H on N/O (and ethers, ketones,
  aldehydes with none), hydrocarbons add alkanes, alkenes, alkynes and rings.
  The floor exemption is removed.
- The 10 remaining `rank` sets are left as they are (decided 2026-09-30).
- `posn*` sheet problems keep their original past-paper choices even where
  flagged `convergent` (decided 2026-10-01): they reproduce real exam items.
  `chem.material_choice_foundation`, `phys.light_travel_application`,
  `comp.block_bugs_foundation`, `phys.magnet_sort_application`,
  `phys.series_cells_benefit_application`, `phys.circuit_diagram_fluency`,
  `comp.work_licence_fluency`, `chem.hydrogen_bond_fluency`,
  `chem.electrolyte_dissociation_foundation`, `chem.electrolyte_dissociation_fluency`,
  `chem.organic_acid_base_foundation`, `chem.solubility_solvent_fluency`,
  `chem.hydrocarbon_saturation_fluency`, `chem.redox_series_foundation`,
  `biology.nephron_fluency`, `biology.plant_response_application`,
  `biology.blood_transfusion_fluency`, `math.posn2568_q30`, `math.continuity_check`.
- Absolute words ("เสมอ", "เท่านั้น") only in wrong choices — done
  2026-09-30 for the 18 sets where the answer never had one and a wrong had
  one in 80%+ of draws. The word was dropped where the choice stays wrong
  without it, or the wrong reason was replaced; two element-hazard fillers
  that would have read true without "เท่านั้น" were replaced.
- Mixed answer formats: `math.quadratic_inequality_word_m4` sometimes shows
  one interval answer beside three plain-number siblings (the interval is
  correct). Check other types that mix draw shapes with `sibling_answers`.
- Low variety (<= 12 distinct questions in 60 draws): `elec.circuit_type`,
  `math.polar_to_cartesian`, `math.p_series`, `math.power_series_representation`,
  `math.improper_integral`.
- `convergent`: prose sets are now handled at draw time (see the session log).
  Math types opt in with `break_convergence = True` (51 set so far). What is
  left is 61 math sets (numeric answers, which the breaker skips so as not to
  undo rank balancing; types with no sibling spares such as
  `math.newton_method`; the `posn*` sheet problems) and prose sets whose pool
  has no spare distractor that ends the cluster. Distractors that each
  change one part of the answer (sign, constant) let a majority vote win; mix
  error types, or add wrongs that change two parts at once.

### 5. Curriculum gaps — closed 2026-10-12

Closed by the open-source task-queue pass: the 32 maths codes are cited
(`_ADDITIONAL_INDICATORS` in `otk/core/curriculum_math.py`), the four science
gaps have sets (Wave I, `otk/core/types/science_wave_i1.py`), and the 11
attitude, project and seminar codes are recorded as not assessable by
multiple choice (`otk/core/indicator_exclusions.py`). The audit as it stood:

919 official indicators (`docs/curriculum_sources/_md/indicators.jsonl`); 872
cited by a set.
- Math ม.4–6 เพิ่มเติม: 32 codes uncited, but the content exists (206 sets
  filed `additional_outcome` with empty `indicator_codes`). Citation work only.
- Science: sets that can be written as MCQ are missing for ว 1.2 ม.1/2
  (microscope use), เคมีเพิ่มเติม 2 ม.5/4 (reaction-rate factors), เคมีเพิ่มเติม 1
  ม.6/9 (esterification, hydrolysis, saponification tests), เคมีเพิ่มเติม 1 ม.6/13
  (plastic and rubber identification). The other 11 uncited science codes are
  attitudes, projects or seminars that MCQ cannot assess.

## Session log

- 2026-09-29 — Audit run; tracker, `scripts/audit_mcq_cues.py` and CSV
  worklist added. Workstream 1: `rank_balanced`, science numeric helpers.
  `rank` 614 → 76.
- 2026-09-29 (cont.) — Workstream 2 started: `length_balanced`, `balanced`
  (no double wrapping), sign-range rule for numeric candidates, prose-only
  length balancing; 366 `rng.sample(wrongs, 3)` call sites unwrapped; all
  computing/technology sets, `substances.py`, `science_wave_a.py` and four
  math formula sets rewritten. `longest` 307 → 212. Tests updated where the
  intended output changed (golden seeded question, block-program answer
  wording, six-fact INFORMATION/TRADES banks).
- 2026-09-29 (cont. 2) — Science prose banks rewritten in `science_wave_f78`,
  `d28`, `f40`, `f67`, `f56`, `f74`, `f59`, `f45`, `f57`, `b2`, `f85`, `f86`,
  `f77`, `d32`, plus fixes in `astronomy.py`, `substances.py`,
  `science_successors.py` and `f79`. `LabSafetyApplication` and
  `NucleicAcidFoundation` no longer pool wrongs across rows. `longest`
  191 → 149, `shortest` 13 → 11. The limiting-factor test now expects
  "ความเข้มของแสง".
- 2026-09-29 (cont. 3) — `d21`, `d22`, `a2`, `e3`, `d4`, `f27`, `e6`, then
  `posn2566`, `f51`, `f52`, `f58`, `f60`, `f69`, `f70`, `f71`. Where a bare
  label was the answer among long fillers, the answer now carries its reason
  (`POLARITY_WHY`, `DISSOLVE_WHY`) or the choices are formulas only
  (polarity application); the two e-wave tests follow. Lengthened wrongs are
  checked with `scripts/debug_convergent.py` so they do not copy the answer's wording
  and raise `convergent`. `longest` 149 → 115, `shortest` 11 → 7.
- 2026-09-30 — Length cues cleared across the rest of the a/b/c/d/e/f/g
  science waves, math and posn2566 (`longest` 115 → 11, `shortest` 7 → 2);
  the 13 left are all chemistry. Added `scripts/debug_length.py`, which prints
  only the draws where the answer stands out. Removed every cross-row
  distractor pool (`pool = [w for _, _, ws in ...]`) in f35, f40, f41, f45,
  f46, f47, f48, f58, f73, f75, f76, f77 and f78: the third distractor was
  another question's wrong answer, often off topic. Where a small bank then
  fell below the variety floor, a row gained a comparable-length distractor.
  Tests follow the new wording where they pinned it (colour names without the
  bracketed loan words, the moment and weight answers).
- 2026-09-30 (cont.) — Last 13 chemistry length cues cleared: `longest` and
  `shortest` are now 0. Added `near_length_sample` (distractors.py) for choices
  drawn from a list of names or formulas. Rank workstream: types may now set
  `invent_numbers = True` (registry.py) so the registry's rank balancing adds
  near values on the short side. It is set only on computed-answer types (all
  81 flagged ones qualified; none offers the stem's own numbers as choices).
  `rank` 81 → 20. What is left is mostly small-integer math (answers 1–4,
  where the positive-only rule leaves no room below) and sheet problems whose
  distractors are ×½, ×2, ×4 of the answer; `scripts/debug_rank.py` shows
  sample draws.
- 2026-09-30 (cont. 2) — Added `otk/tests/test_mcq_cues.py`: every set,
  the audit's 60 seeded draws, length rule only (about 75 seconds). It fails
  if any set's answer is visibly the longest or shortest too often, so the
  length cue cannot come back unnoticed. No allow-list was needed.
- 2026-09-30 (cont. 3) — Convergence breaker (distractors.py,
  `_break_convergence`). When the answer is the most similar choice to the
  others and a spare distractor exists, the balancer swaps in a random spare
  that ends it without making a length cue. It runs only for prose choices:
  math and sheet problems may show the stem's own values as choices, so they
  are left alone. Eight small banks lost too much variety under it and fell
  below the wave H floor; each got 1–3 more wrongs (earth rotation, eclipse,
  organic acid–base, polymer impact, humidity, both bulb sets, thermal
  expansion benefit). `convergent` 291 → 262.
- 2026-09-30 (cont. 4) — `rank_balanced` passed a whole set through
  unbalanced when any spare candidate was another shape (a fraction such as
  `\frac{25}{3}` beside whole-number answers), which hit the ×½/×2 sheet
  problems and expected value. It now drops the unparsable spares when the
  default choices are all plain numbers. `rank` 20 → 10. The ten left are
  small answers (0–4) where the non-negative rule leaves nothing below.
  Drawing the below/above split only from the feasible range was tried and
  dropped: it cleared some sets but pushed others over the 0.60 bar.
- 2026-09-30 (cont. 5) — `break_convergence` (registry.py) wraps a type's
  balanced strategy in `unconverged` (distractors.py), which asks for spares
  (answers from sibling draws) and runs the convergence breaker on symbolic
  answers. Set on the 51 math classes a trial showed it clears, none with a
  new length cue. Not set on sheet problems or where the choices are the
  stem's own values. `convergent` 262 → 211 (math 112 → 61).
- 2026-09-30 (cont. 6) — Double slips (distractors.py, `_double_slips`). A
  prose set whose three wrongs each alter one part of the answer has no spare
  to swap in; the breaker now builds one by applying two of those wrongs'
  edits together (group 14 period 5 beside group 13 period 6). Whole words
  only, since char-level splices made non-words ("ไขสันหน้า") and
  equivalents ("Cl-H", "2 : 2"). Not built where two slips could cancel into
  an equivalent answer: fewer than four words, ratios, powers of ten, routes
  and code (←↑↓, =), a reordering of the answer's own words, or an edit that
  adds or drops a negation. Authored spares are still tried first. A sample
  per set (`tmp/doubles.txt` at the time) was read for correctness.
  `convergent` 211 → 174.
- 2026-09-30 (cont. 7) — Absolute-word cue: 18 sets (answer never absolute,
  a wrong absolute in 80%+ of draws, checked over 30 draws per set) now carry
  none in their wrongs. `chem.metallic_bond_foundation` then showed a length
  cue, so its `METAL_FALSE` wrongs were lengthened to the answers' size.
  Light travel and redox series: absolute fillers replaced with a wrong
  reason under each yes/no label; the light-travel "see" and "cannot see"
  answers were brought to the same length, since each is the other's wrong.
- 2026-09-30 (cont. 8) — Double slips for matchings and many-part lines: a
  " / " answer is split into its parts, and an edit keeps its changes as
  separate pieces, so two disjoint swaps of matched pairs combine into a
  valid third matching. The reordering guard no longer applies to " / " or
  " → " answers, where order is the content. Each edit may change at most 40%
  of the answer (larger ones spliced in another item's clause), and a sequence
  that repeats a step is skipped. `convergent` 174 → 164.
- 2026-09-30 (cont. 9) — Safety fix for double slips. A review found two word
  flips in running prose cancelling into a TRUE "wrong" choice: "ยิ่งยาว
  ยิ่งสั่นห่าง และให้เสียงต่ำลง" (pitch), "ไซเล็ม: อยู่ด้านใน…" (xylem is
  inside), and "H₂O กับ H₃O⁺" (also a conjugate pair; this one shipped in
  `3794d28`). Doubles are now built only where each part is judged alone
  (" / " part lines), where any other order is wrong (matchings, " → "
  sequences), or from changes to numbers only in plain prose. Also skipped:
  loop answers ("ทำซ้ำ"), and numbers all scaled by one factor, which keep a
  proportion right ("O 368 กับ S 368" for "O 184 กับ S 184").
  `convergent` 164 → 183: the rest need authored wrongs.
- 2026-09-30 (cont. 10) — The negation guard no longer applies inside " / "
  part lines (a negation in one part cannot cancel another part), which
  unblocks classification lines such as dissolving ("ละลายน้ำ" / "ไม่ละลายน้ำ"
  per substance). `chem.rate_use_fluency` now authors its own two-part
  spares: a factor the method does not touch is false whichever way the rate
  goes. Wave C swap tests accept one swap or two combined. `convergent`
  183 → 174.
- 2026-09-30 (cont. 11) — Authored two-part spares, each false on its own
  whatever else it says: ke/pe experiments (the held-fixed variable "lowers"
  or "has no effect"), field distance (closer is weaker), wind use and hazard,
  forecast and volcano/tsunami plans (both halves crossed from elsewhere),
  mass motion and chemical change (true reading, false conclusion; wrong
  label on another activity's evidence), contact force (two activities
  misplaced), periodic position (both coordinates moved; two of a trio
  swapped), de Broglie (h itself, and h/(mv²)). Fixed a bug that dropped every
  double whose numbers were unchanged (the scaled-proportion guard saw a
  factor of 1). Sixteen hints that promised "ข้อที่ผิดจะผิดเพียง…เดียว" now say
  "ผิดอย่างน้อยหนึ่ง…", since a wrong may now be wrong in two parts.
- 2026-09-30 (cont. 12) — Three more batches of authored two-part spares
  (commits `df512aaf`, `7837f0be`, `27595e03`, `1361e281`): chemistry
  (electrolysis, limiting reagent, element classes, material property and
  grouping, solution labels, object parts, reversible change), geo
  (greenhouse, surface processes, fossil fuel), physics diagrams (friction,
  displacement, speed and velocity, spring scale, resultant, light meter),
  life (organism group) and computing (block programs, flowchart, loops,
  arrows). Where a program's correctness could depend on the choice, a spare
  is kept only if the generator's own walk or run shows it misses. Several
  computing generators sampled three wrongs before balancing; they now pass
  the whole pool. `convergent` 157 → 131; computing is clear.
- 2026-10-01 — Numeric breaker. `rank_balanced` now ends with the
  convergence breaker, restricted (`keep_side`) to swapping a chosen number
  for an unused one on the same side of the answer, so its rank balance is
  unchanged. Numbers with units ("520 ล้านถุง", "−332 kJ/mol") were never
  covered before. With five more authored sets (`f839e38b`),
  `convergent` 131 → 78; `rank` stays 10 and the length flags 0.
- 2026-10-01 (cont.) — Symbolic math (`ab53764f`, `d0e1bf10`): Newton,
  arc length, centroid, integrating factor, Taylor, difference quotient,
  related rates, literal equation, rationalising, factoring, rational
  inequality, inverse function, exp/log and absolute-value graphs gain
  two-slip wrongs and opt into `break_convergence`. Where the kept first
  wrong was a one-slip copy, a two-slip wrong now leads (no swap can move
  the answer out of the centre otherwise). Then chemistry and physics
  (`5f03a83e`): rate compare, nuclides, oxidation number (every computed
  wrong offered, not three), heat equilibrium, friction forces, Newton's
  second law. `convergent` 78 → 56.
