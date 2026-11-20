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

### Chemistry POSN 2562 bank — first four waves, 2026-10-21

- Branch/worktree: `codex/posn-chemistry-2562`, `.worktrees/posn-chemistry-2562/`.
- Source: `chemistry/level/upper-secondary/posn-chemistry/posn1-62-chemistry.pdf`, 17 pages, 60 multiple-choice and 15 written questions. Extraction counted all 75. Its public mirror matched the bank LFS object's SHA-256 exactly when private Git LFS credentials were unavailable.
- **66/75 reviewed:** all Part I questions 1–60 and Part II questions 61–66 have independent solvers, three variants each, generators, named mistakes, and knowledge claims. The private digest contains concise paraphrases of those sixty-six; public sheet metadata contains only reviewed items. The q12 reaction table was checked against its figure crop and restated in text.
- Q3's source assumes adjacent electronic gaps shrink as n rises; the generated question states the hydrogen-like model explicitly. Questions 17 and 25 were read from their page figures and recast as textual structures. Q20 narrows the oxoanion claim to exclude O–F and O–O bonds. Q32, Q36 and Q39 figures were read from rendered pages and expressed in the stems; Q35 supplies Z vapor pressure and states the vapor-curve assumption used for its boiling order. Q54 names benzene as the requested solute; Q61 uses the verified Tc configuration; Q62 specifies an average N oxidation state in N₂O; Q64 records all three net ionic equations; Q66 transcribes the bond-energy table. The bank entry remains `PARTIAL 66/75` at the converted stage. Targeted wave checks passed; the full suite is deferred until all 75 questions are digested.

### Chemistry POSN 2561 bank — complete, 2026-10-21

- Branch/worktree: `codex/posn-chemistry-2561`, `.worktrees/posn-chemistry-2561/`.
- Source: `chemistry/level/upper-secondary/posn-chemistry/posn1-61-chemistry.pdf`, 18 PDF pages. The paper declares 75 questions: 60 multiple-choice and 15 written; extraction found all 75. Every item was reviewed, independently solved, claimed by a knowledge unit, and linked to a generator. **75/75 complete.**
- MC1's E⁻, G and A⁺ all have 18 electrons; isotope mass numbers are irrelevant. MC2 gives Z=13 and A=27. MC3's C line (434 nm) has more photon energy than B (486 nm). MC3 says “five lines” but lists four, so the adaptation says four.
- MC4's only always-true claim is that Z has more than six electrons in its second shell; the adaptation says “always” explicitly. MC5 selects fluorine. MC6's false comparison is K < Ca for IE₂; the close Se < Br comparison was checked against NIST ionization data.
- MC7's mixed atomic/ionic radius comparison depends on a radius convention; its adaptation supplies the specific table used. MC8's false order places Ca above As for IE₁; its adaptation supplies measured property values and specifies grey arsenic melting under pressure. MC9 pairs SO₃ with Na₂O to give an acid and a base in water.
- MC10 identifies MgI₂ from the violet iodine extract and hot-water metal reaction. MC11 identifies P from its −3 to +5 oxidation-state range; only positive oxidation states in its oxides is true. MC12 selects dichromate and FeCl₃ as the colored pair. The original Cl₂O distractor has concentration-dependent solution color, so the adaptation uses NaCl.
- MC13's table identifies Mg²⁺, K⁺ and Ba²⁺ from carbonate and sulfate precipitates. MC14 selects Cr(III) over Fe(II) among the actual complexes; MnO₂ is excluded because it is not a coordination complex. MC15 specifies β⁻ to distinguish it from positron emission.
- MC16's four graphs are restated as mass values at zero, one and two half-lives; only the parent-decay curve has the expected 100%, 50%, 25% progression. MC17 is helium-3 plus deuterium fusion. MC18's basic-oxide pair is Ca and Rb.
- MC19 identifies Ga from the 2:3 chlorine ratio, water inertness and colorless acid solution. MC20's printed intended water reaction is missing coefficients and therefore has no correct choice as written; the adaptation balances it. MC21's N≡C–C≡N structure has one single bond, two triple bonds and two lone pairs.
- MC22 contrasts nonpolar CS₂ with network SiO₂; the silica property statement is true. MC23 has statements 1 and 3 true for gaseous SbCl₅, SiH₄ and TeF₆. MC24's fully water-soluble covalent group is ethanol, HF and acetic acid.
- MC25's extraction table supports C being more polar than B; it does not establish exact functional groups or prove B is nonpolar, so the adaptation phrases conclusions as trends and possibilities. MC26's order is butane, ether, ethanol by increasing boiling point; the adaptation specifies a cooled liquid starting mixture. MC27's octet pair is BF₄⁻ and CO₃²⁻; NO₂ is an odd-electron radical and XeF₄ has an expanded octet.
- MC28's fourth N–H bond in NH₄⁺ is equivalent to the other three once the ion forms. MC29 picks bent SO₂ against three linear gas-phase molecules. MC30 picks gaseous PCl₅ because its smallest axial-equatorial angle is 90°; NIST measured SOCl₂ at 96.1° and the other two have larger angles.
- MC31 pairs weakly polar PH₃ with H₂S; every other pair contains a molecule with no permanent dipole. MC32 has statements 1 and 3 true: carbonate C–O bonds are longer than CO₂'s, BF₃ is nonpolar, and CF₄ boils below CHF₃. MC33 gives 60% initial H₂ and now has independently balanced numerical variants.
- MC34 gives Zn from 0.020 mol BaSO₄ and 161 g/mol ASO₄. MC35 requires 36 m³ O₂, hence 180 m³ air at 20% O₂. MC36 requires 18 g Mg for 4.48 L NH₃ at 40% nitride yield. Each of these has numerical variants checked by a second route.
- MC37 leaves 3.50 mmol carbonate in 100 mL, or 0.0350 mol/L. MC38 solves the Al/Zn mass and H₂ balances for 24.9% Al. MC39 adds initial Fe³⁺ to oxidized Fe²⁺, yielding 0.0515 mol/L. Each has independently checked numerical variants.
- MC40 gives 0.450 mol NaBH₄ after balancing the diborane reaction and accounting for 70% yield. MC41 produces 8/5 mol N₂ per mol NaN₃ across two reactions: the source’s 49 g choice is closest to the 49.5 g calculation with its printed R. MC42 needs three H⁺ per formula unit of trona, or 48.0 mL of 0.125 M acid.
- MC43 balances 4KO₂+2CO₂→2K₂CO₃+3O₂ and finds KO₂ limiting, yielding 168 cm³ O₂. MC44 uses mass per litre and molarity to identify H₃PO₄. MC45 counts 49 mmol Na⁺ in 70 mL, or 0.70 mol/L.
- MC46 uses four HCl per Cl₂ and the 36.5% mass fraction to obtain 20.0 g of acid solution; its wording now distinguishes solution from pure HCl. MC47 leaves 0.708 M acetic acid after NaHCO₃ consumes 0.050 mol. MC48 counts 0.0008 mol OH⁻ from the Ba(OH)₂ stock before adding 20.0 mL of NaOH stock.
- MC49 gives about 158 g/mol from benzene boiling-point elevation. MC50 transfers 0.5 m molality from solvent A’s freezing depression to solvent B’s boiling rise, giving 65.0°C. MC51 uses both water constants to obtain 4 m and 72.0 g of X. The adaptations state the nondissociation assumption behind the source answers.
- The private bank digest contains concise paraphrases of all 75 questions. Figures were read from the source during review; no source artwork or copied question text ships in the public repository. The bank entry is `green`.
- The requested cadence was targeted tests for each wave and one full suite after all 75 items were digested.

### Chemistry POSN bank — waves 1–23, 2026-10-21

- Branch/worktree: `codex/posn-chemistry-2560`, `.worktrees/posn-chemistry-2560/`.
- First source: `chemistry/level/upper-secondary/posn-chemistry/posn1-60-chemistry.pdf`, 19 pages,
  60 multiple-choice questions plus 10 written questions. Written questions
  restart at 1 and use internal numbers 61–70.
- All 70 were reviewed against the source, solved independently, claimed by
  knowledge units, and linked to generators. **70/70 complete.**
- `otk/sheets/posn2560_chemistry/sheet.json` contains the complete paper;
  `sheetpipe verify` passed 70/70 solvers and 213 variant runs. Knowledge
  coverage is 70/70 and the bank entry is `green`.
- Source MC3's diagram maps 97 nm to n=4; the generator gives n explicitly
  and specifies an ensemble with all cascades. MC4 returns (Z,A)=(12,22).
  MC6 gives cobalt(III), [Ar]3d6. Figures are restated in words, with no static
  source artwork shipped. Full copied text remains in the private bank.
- Extraction normalized the written heading `9 .` to `9.`; the count check
  confirms 60+10, rather than silently losing written questions 9 and 10.
- Maintainer test cadence: one targeted batch after each chemistry wave,
  including the changed keys, solver checks, provenance, safety, golden draws,
  curriculum/stage/layout checks and Ruff. The full suite is run after the
  complete-sheet wave; the first batch's full run is historical.
- MC1's diagram has the positive ray behind the cathode and electrons behind
  the anode. MC2's Ts oxidation states are model predictions, not measured
  properties. MC5's specified Mg²⁺ and P³⁻ differ in occupied shell count.
  These adaptations state their model assumptions in the generated prompts.
- MC7 compares free-atom/ion unpaired counts; MC8's adaptation names the
  group-2 metal explicitly. MC9's page image shows that S, Cl and Au are
  underlined; the plain-text extraction omits those underlines.
- MC10's diagram B violates Hund's rule. MC11's printed options have no
  correct pair of rankings: the corrected generator uses Ga>As>P>O for
  empirical radius and O>P>As>Ga for first ionization energy. MC12 gives
  Ca and Cl for ions isoelectronic with Ar. The MC11 source discrepancy is
  documented in its sheet record and solver; no printed choice was adopted.
- Next: choose the next chemistry sheet in the bank.

Maintainer cadence (2026-11-16): for sets-only sheet digestion, implement roughly ten new generators before running the combined checks and reporting the batch. Verify source answers while digesting; keep the existing required checks.

### Physics POSN bank — 2026-10-17

- Scope: `physics/level/upper-secondary/posn-physics/MANIFEST.json` lists 33 papers (135 PDF components,
  including national theory/practical papers and answer files).
- `physics/level/upper-secondary/posn-physics/posn1-60-physics.pdf`: all 30 questions transcribed,
  independently solved, mapped to knowledge, and linked to 30 generators in
  `otk/sets/physics/olympiad/posn2560.py`. Part 2 restarts at 1 in the
  source; it is numbered 21–30 in the solver package.
- Validation complete: 30/30 solvers, 90 variant cross-checks, 30/30 knowledge
  coverage, Ruff clean. One completed-sheet full run followed by focused
  repairs; the final focused batch passed all 4,277 checks.
- Test cadence requested by the maintainer: one targeted batch per wave;
  full suite only when a sheet is completely digested. Waves here cover
  6, 10, and 14 items. The final batch exposed a shortest-choice cue in
  item 8, corrected before the completed-sheet full run.
- `physics/level/upper-secondary/posn-physics/posn1-61-physics.pdf`: all 30 questions transcribed,
  independently solved, claimed by 29 knowledge units, and linked to 30
  generators in `otk/sets/physics/olympiad/posn2561.py`. Internal items 21–30
  preserve the ten restarted Part 2 numbers in their provenance. The single
  completed-sheet full run passed: 29,421 passed, 2 skipped (24m57s).
- `physics/level/upper-secondary/posn-physics/posn1-62-physics.pdf`: all 26 questions (15 MC, 10 short
  answers, one worked problem) are transcribed, independently solved, and
  linked to 26 generators and knowledge units. The equal-source circuit reuses
  the existing signed three-branch circuit unit; 25 units are new.
- `physics/level/upper-secondary/posn-physics/posn1-64-physics.pdf`: a scan with no text layer and no answer
  key. All 30 questions (25 MC, 5 short answers) are hand-transcribed, solved
  and independently checked, and linked to 30 generators in
  `otk/sets/physics/olympiad/posn2564.py`. 27 knowledge units are new; items
  8, 11 and 26 reuse the ring-field, steady-RC and signed-circuit units.
- `physics/level/upper-secondary/posn-physics/posn1-65-physics.pdf`: also a scan with no answer key; all 30
  questions (25 MC, 5 short answers) are transcribed, solved, independently
  checked and linked to 30 generators in `otk/sets/physics/olympiad/posn2565.py`.
  26 knowledge units are new; items 8, 9, 23 and 30 reuse existing units.
- `physics/level/upper-secondary/posn-physics/posn1-66-physics.pdf`: 28 questions (20 MC, 7 short answers,
  one worked problem), maths printed as pictures, no answer key; all are
  transcribed, solved, independently checked and linked to 28 generators in
  `otk/sets/physics/olympiad/posn2566.py`. 26 knowledge units are new; items 12
  and 24 reuse the ring-field and steam-volume units.
- `physics/level/upper-secondary/posn-physics/posn1-67-physics.pdf`: 16 questions (15 short answers, one
  worked problem), maths printed as pictures, no answer key; all are
  transcribed, solved, independently checked and linked to 16 generators in
  `otk/sets/physics/olympiad/posn2567.py`. 12 knowledge units are new; items 1,
  8, 10 and 16 reuse existing units. This completes the camp-1 selection
  papers 2560–2567 in the manifest (there is no 2563 paper).
- `physics/level/upper-secondary/posn-physics/posn1-68-physics.pdf`: 25 short-answer questions, maths
  printed as pictures, no answer key; all are transcribed, solved,
  independently checked and linked to 25 generators in
  `otk/sets/physics/olympiad/posn2568.py`. 18 knowledge units are new (items 20
  and 21 share one); items 2, 4, 13, 16, 18 and 19 reuse existing units.
- `physics/level/upper-secondary/posn-physics/posn1-69-physics.pdf`: 10 eight-choice MC and 20 short answers;
  Part 2 restarts at 1 and is numbered 11–30 (provenance keeps "ตอนที่ 2 ข้อ k").
  All 30 are transcribed, solved, independently checked and linked to 30
  generators in `otk/sets/physics/olympiad/posn2569.py`. 17 knowledge units are
  new; 13 items reuse existing units.
- All nine camp-1 selection papers in the manifest (2560–2562, 2564–2569) are
  digested.
- National olympiad (TPhO) papers: each folder holds a theory paper (often in
  Thai and English), an official solution, and an experimental paper. One
  sheet per year: every answerable sub-part of the theory paper is an item,
  and the experimental paper's theory parts are items with synthetic data.
  Duplicate-language versions and solutions are indexed as `ignored` with a
  note; the solution confirms each independently derived answer.
- `physics/level/upper-secondary/posn-physics/tpho-45-physics/` (TPhO 1, 2545): 14 theory sub-parts and 3
  experiment parts → 17 generators in `otk/sets/physics/olympiad/tpho2545.py`.
- `physics/level/upper-secondary/posn-physics/tpho-46-physics/` (TPhO 2, 2546): 16 theory sub-parts and 5
  experiment parts → 21 generators in `otk/sets/physics/olympiad/tpho2546.py`.
- `physics/level/upper-secondary/posn-physics/tpho-47-physics/` (TPhO 3, 2547): 12 theory sub-parts and 3
  experiment parts → 15 generators in `otk/sets/physics/olympiad/tpho2547.py`.
- `physics/level/upper-secondary/posn-physics/tpho-48-physics/` (TPhO 4, 2548): 16 theory items and 3
  experiment parts → 19 generators in `otk/sets/physics/olympiad/tpho2548.py`.
- `physics/level/upper-secondary/posn-physics/tpho-49-physics/` (TPhO 5, 2549): 11 theory sub-parts and 3
  experiment parts → 14 generators in `otk/sets/physics/olympiad/tpho2549.py`.
- `physics/level/upper-secondary/posn-physics/tpho-50-physics/` (TPhO 6, 2550): 12 theory items and 4
  experiment parts → 16 generators in `otk/sets/physics/olympiad/tpho2550.py`.
- `physics/level/upper-secondary/posn-physics/tpho-51-physics/` (TPhO 7, 2551): 13 theory items and 2
  experiment parts → 15 generators in `otk/sets/physics/olympiad/tpho2551.py`.
- `physics/level/upper-secondary/posn-physics/tpho-52-physics/` (TPhO 8, 2552): 12 theory items and 4
  experiment parts → 16 generators in `otk/sets/physics/olympiad/tpho2552.py`.
- `physics/level/upper-secondary/posn-physics/tpho-53-physics/` (TPhO 9, 2553): 11 theory items and 3
  experiment parts → 14 generators in `otk/sets/physics/olympiad/tpho2553.py`.
- `physics/level/upper-secondary/posn-physics/tpho-54-physics/` (TPhO 10, 2554): 16 theory items and 4
  experiment parts → 20 generators in `otk/sets/physics/olympiad/tpho2554.py`.
- `physics/level/upper-secondary/posn-physics/tpho-55-physics/` (TPhO 11, 2555): 13 theory items and 5
  experiment parts → 18 generators in `otk/sets/physics/olympiad/tpho2555.py`.
- `physics/level/upper-secondary/posn-physics/tpho-56-physics/` (TPhO 12, 2556): 17 theory items and 4
  experiment parts → 21 generators in `otk/sets/physics/olympiad/tpho2556.py`.
- `physics/level/upper-secondary/posn-physics/tpho-57-physics/` (TPhO 13, 2557): 12 theory items and 5
  experiment parts → 17 generators in `otk/sets/physics/olympiad/tpho2557.py`.
- `physics/level/upper-secondary/posn-physics/tpho-58-physics/` (TPhO 14, 2558): 13 theory items and 4
  experiment parts → 17 generators in `otk/sets/physics/olympiad/tpho2558.py`.
- `physics/level/upper-secondary/posn-physics/tpho-59-physics/` (TPhO 15, 2559): 19 theory items and 4
  experiment parts → 23 generators in `otk/sets/physics/olympiad/tpho2559.py`.
- `physics/level/upper-secondary/posn-physics/tpho-60-physics/` (TPhO 16, 2560): 18 theory items and 2
  experiment parts → 20 generators in `otk/sets/physics/olympiad/tpho2560.py`.
- `physics/level/upper-secondary/posn-physics/tpho-61-physics/` (TPhO 17, 2561): 19 theory items and 3
  experiment parts → 22 generators in `otk/sets/physics/olympiad/tpho2561.py`.
- `physics/level/upper-secondary/posn-physics/tpho-62-physics/` (TPhO 18, 2562): 18 theory items and 6
  experiment parts → 24 generators in `otk/sets/physics/olympiad/tpho2562.py`.
- `physics/level/upper-secondary/posn-physics/tpho-63-physics/` (TPhO 19, 2563): 15 theory items and 5
  experiment parts → 20 generators in `otk/sets/physics/olympiad/tpho2563.py`.
- `physics/level/upper-secondary/posn-physics/tpho-64-physics/` (TPhO 20, 2564): 24 theory items and 5
  experiment parts → 29 generators in `otk/sets/physics/olympiad/tpho2564.py`.
- `physics/level/upper-secondary/posn-physics/tpho-65-physics/` (TPhO 21, 2565): 17 theory items and 5
  experiment parts → 22 generators in `otk/sets/physics/olympiad/tpho2565.py`.
- Next source: `physics/level/upper-secondary/posn-physics/tpho-66-physics/`. Thirty of 33 papers are
  digested; 3 remain pending.

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
python -m otk.tools.sheetpipe bank status "mathematics/level/upper-secondary/rathcenter/1-*"   # records matching a glob
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
- [x] **`book` layout, the 23 `🍰` lecture books** (session 1). Each book is notes, then `แบบฝึกหัด` blocks, then its answer key bound at the back. `sheetpipe bank set "mathematics/level/upper-secondary/rathcenter/*/🍰*" --answer-key self` marks this, and `answerkey.split` reads the key region after the last exercise block. A key title counts only if it also heads a section of the notes.
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
python -m otk.tools.sheetpipe convert "mathematics/level/upper-secondary/rathcenter/*"
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
1. `sheetpipe knowledge coverage "mathematics/level/upper-secondary/rathcenter/<n> *"` lists the unmapped questions.
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
- **no-text**: `physics/level/unspecified-level/Faii/ข้อสอบแรง.pdf` (hand-digested) and
  `mathematics/level/upper-secondary/posn-math/posn1-64-math.pdf` (27/30 solvers verified).
- **notes/topics/** (6 topic notes, formerly `new_sheet/`) are not yet
  digested. `กระบวนการเปลี่ยนแปลงของหิน` has no matching types at all; the
  others are partly covered.
- **outputs/** (`teaching_plan/`, `review_sheet/`) is marked `ignored`: these
  are written *from* existing sets, not sources.
- The root copy of the 2568 สอวน. paper was a byte-identical duplicate and was
  removed; `posn2568_math` now points at `mathematics/level/upper-secondary/posn-math/01-วิชาคณิตศาสตร์.pdf`.

## 5. Traps already found

- **PDFs are in Git LFS and fetched on demand** (since session 1).
  - The LFS objects are stored with the openthaiknowledge-bank repository
    itself (until 2026-10-16 they were stored with TutorRank's). The bank's
    `.lfsconfig` excludes every PDF from automatic fetches, to stay inside
    GitHub's LFS download quota. The bank's PDFs total ~1.1 GB.
  - A clone therefore holds pointer files for the PDFs. `bank scan` skips them
    as absent, and `convert` says what to fetch.
  - Fetch only what a stage needs: `python -m otk.tools.sheetpipe bank fetch
    "mathematics/level/upper-secondary/rathcenter/13-*"`. That wraps `git lfs pull --include … --exclude ""`.
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
  variables (see `openthaiknowledge-bank/mathematics/level/upper-secondary/posn-math/HANDOFF.md`). Transcribe from page
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
  `mathematics/level/upper-secondary/rathcenter/8-trigonometry/(rath) เฉลย.pdf`. Stage 2 should pair them with
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

### 2026-10-21 — POSN chemistry 2560, eleventh octet and liquids batch

- Visually checked MC31–MC32 on p9 and MC33 on p10. Added independent
  solvers, generators and knowledge claims for all three.
- IF₄⁺ has ten electrons around I while the other printed species have
  octets. MC32's printed ClH₃ is handled as a formal AX₃E₂ model rather than
  a claim about an isolable gas. MC33 states a fixed molecular separation
  when comparing attractive force, so cooling does not change the pair
  force law.
- `verify posn2560_chemistry`: 33/33 green, 102 variant checks, all
  independent. Knowledge validation: 804 units in 670 files, zero problems;
  source coverage: 33/70. Only the three new golden keys were added.
- Targeted wave validation: 229 sheet/set checks and 16,343 affected
  registry, provenance, safety, golden and layout checks passed. Ruff and
  whitespace checks passed. Full suite deferred until all 70 questions are
  complete.

### 2026-10-21 — POSN chemistry 2560, tenth shape, names and bond batch

- Visually checked MC28–MC30 on p9, including MC29's four-row naming table
  and MC30's four reactions. Built solvers, generators and knowledge claims.
- MC28 uses an explicit Lewis/VSEPR model: KrO₂H₂ is AX₄E and seesaw.
  MC29 has **no incorrect printed choice**: all four formula–name pairs match.
  The generator asks for the number of mismatches (zero for the source) and
  variants introduce one to three mismatches. MC30 restores the C=C bond
  marks absent from the PDF's displayed reaction formulas.
- `verify posn2560_chemistry`: 30/30 green, 93 variant checks, all
  independent. Knowledge validation: 801 units in 667 files, zero problems;
  source coverage: 30/70. Only the three new golden keys were added.
- Targeted wave validation: 210 sheet/set checks and 16,331 affected
  registry, provenance, safety, golden and layout checks passed. Ruff and
  whitespace checks passed. Full suite deferred until all 70 questions are
  complete.

### 2026-10-21 — POSN chemistry 2560, ninth polarity and bonding batch

- Visually checked MC25–MC27 on p9. Built solvers, generators, and knowledge
  claims for all three. PF₅ is nonpolar by dipole cancellation; CaCO₃ has
  ionic lattice bonding and covalent bonds within carbonate.
- MC27's textbook answer O₃ uses a donor–acceptor Lewis drawing. The
  adaptation explicitly treats the arrow as electron-pair bookkeeping and
  acknowledges the equivalent O–O bonds of the resonance hybrid.
- `verify posn2560_chemistry`: 27/27 green, 83 variant checks, all
  independent. Knowledge validation: 798 units in 664 files, zero problems;
  source coverage: 27/70. Only the three new golden keys were added.
- Targeted wave validation: 191 sheet/set checks and 16,319 affected
  registry, provenance, safety, golden and layout checks passed. Ruff and
  whitespace checks passed. Full suite deferred until all 70 questions are
  complete.

### 2026-10-21 — POSN chemistry 2560, eighth VSEPR batch

- Visually checked MC22–MC23 on p8 and MC24 on p9. Built solvers,
  generators, and knowledge claims for all three.
- MC22 pairs tetrahedral BF₄⁻ with POCl₃; variants also exercise square
  planar, seesaw and trigonal-pyramidal shapes. MC23 compares each molecule's
  smallest bond angle, using NIST geometry data for ClF₃, ClF₅ and OCl₂.
  MC24 counts only central-atom lone pairs; XeF₂ has three in the source.
- `verify posn2560_chemistry`: 24/24 green, 74 variant checks, all
  independent. Knowledge validation: 795 units in 661 files, zero problems;
  source coverage: 24/70. Only the three new golden keys were added.
- Targeted wave validation: 172 sheet/set checks and 16,307 affected
  registry, provenance, safety, golden and layout checks passed. Ruff and
  whitespace checks passed. Full suite deferred until all 70 questions are
  complete.

### 2026-10-21 — POSN chemistry 2560, seventh precipitation and bonding batch

- Visually checked MC19–MC21 and MC20's five-row table on p8. Built
  solvers, generators and knowledge claims for all three.
- MC19 uses spectator cancellation to produce the Pb²⁺/SO₄²⁻ net ionic
  equation. MC20's printed "covalent" category fits B, D and E; its
  generated prompt specifies the covalent substance whose aqueous solution
  conducts, identifying D uniquely. MC21 selects NO⁺ by N–O bond order and
  checks against experimental bond lengths; variants add neutral NO to
  enable four distinct choices.
- `verify posn2560_chemistry`: 21/21 green, 65 variant checks, all
  independent. Knowledge validation: 792 units in 658 files, zero problems;
  source coverage: 21/70. Only the three new golden keys were added.
- Targeted wave validation: 153 sheet/set checks and 16,295 affected
  registry, provenance, safety, golden and layout checks passed. Ruff and
  whitespace checks passed. Full suite deferred until all 70 questions are
  complete.

### 2026-10-21 — POSN chemistry 2560, sixth nuclear and bonding batch

- Visually checked the three nuclear equations and the hydrogen comparison
  on p7, then the hydrogen-halide boiling choices on p8. Built solvers,
  generators and knowledge claims for MC16–MC18.
- MC16 balances (A,Z) separately: neutron, deuteron, and Ra-226. MC17's
  adaptation directly asks valence counts because the printed oxidation-state
  distractor has a fluorine exception. MC18 uses normal boiling-point data
  and the HF hydrogen-bonding exception.
- `verify posn2560_chemistry`: 18/18 green, 56 variant checks, all
  independent. Knowledge validation: 789 units in 655 files, zero problems;
  source coverage: 18/70. Only the three new golden keys were added.
- Targeted wave validation: 134 sheet/set checks and 16,283 affected
  registry, provenance, safety, golden and layout checks passed. The q18
  safety rule rejected a direct method reference; its lambda replacement
  passed the specific rerun. Ruff and whitespace checks passed. Full suite
  remains deferred until all 70 questions are complete.

### 2026-10-20 — POSN chemistry 2560, fifth oxides and halogens batch

- Visually checked MC13–MC14 on p6 and MC15 on p7. Built independent
  solvers, generators, and knowledge claims for all three.
- MC13 identifies P₄O₁₀ and Cl₂O₇ as acidifying oxides. MC14 uses the
  source's general solubility-rule model for BaSO₄, BaHPO₄, and MgHPO₄;
  actual precipitation depends on concentration and pH. MC15 adds the
  distinctness condition omitted by the printed stem, making X=Cl,
  Y=I, and Z=Br unique.
- `verify posn2560_chemistry`: 15/15 green, 47 variant checks, all
  independent. Knowledge validation: 786 units in 652 files, zero problems;
  source coverage: 15/70. Only the three new golden keys were added.
- Targeted wave validation: 115 sheet/set checks and 16,270 affected
  registry, provenance, safety, golden and layout checks passed. The frozen
  registry count was updated from 4,473 to 4,476 and its one failing check
  was rerun successfully. Ruff and whitespace checks passed. Full suite
  deferred until all 70 questions are complete.

### 2026-10-20 — POSN chemistry 2560, fourth atomic-structure batch

- Visually checked MC10's orbital diagrams on p5 and MC11–MC12's tables on
  p6. Built solvers, generators and knowledge claims for all three.
- Cross-checked MC11 against PubChem empirical/covalent radii and NIST
  ionization energies. None of the four printed answer pairs is correct;
  the generated question asks the corrected rankings.
- `verify posn2560_chemistry`: 12/12 green, 38 variant checks, all
  independent. Knowledge validation: 783 units in 649 files, zero problems;
  source coverage: 12/70. Only the three new golden keys were added.
- Targeted wave validation: 96 sheet/set checks and 16,259 affected registry,
  provenance, safety, golden and layout checks passed. Ruff and whitespace
  checks passed. Full suite remains deferred until all 70 are complete.

### 2026-10-20 — POSN chemistry 2560, third atomic-structure batch

- Visually checked source p5 and built solvers and generators for MC7–MC9.
  The printed underlines on MC9 identify sulfur, chlorine and gold, so the
  verified source oxidation-state answer is (+6,+7,+1).
- Added three knowledge claims and linked the new keys to the supplemental
  chemistry registry; bank progress is 9/70 and remains `converted`.
- `verify posn2560_chemistry`: 9/9 green, 29 variant checks, all independent.
  Knowledge validation: 780 units in 646 files, zero problems; source
  coverage: 9/70. Only the three new golden keys were added.
- Targeted wave validation: 75 sheet/set checks and 16,247 affected registry,
  provenance, safety, golden and layout checks passed. Ruff and whitespace
  checks passed. The full suite remains deferred until all 70 are complete.

### 2026-10-20 — POSN chemistry 2560, second atomic-structure batch

- Visually rechecked p3's perforated cathode/anode diagram and reviewed MC1,
  MC2 and MC5; source choices ง, ค and ง are reproduced by the stated
  physical or chemical models. Built three independent solvers, generators,
  knowledge claims and named distractors. No source artwork was shipped.
- `verify posn2560_chemistry`: 6/6 green, 19 variant checks, all independent.
  Knowledge validation: 777 units in 643 files, zero problems; source
  coverage: 6/70. Only the three new golden keys were added.
- Targeted sheet/solver checks: 6,526 passed, 4 skipped. Registry and safety
  batch: 16,233 passed; its two initial failures were stale frozen sheet
  counts and the generated set index, both corrected. The affected checks
  passed on rerun; Ruff and whitespace checks passed. Full suite deferred
  until the whole 70-question sheet is complete.

### 2026-10-20 — POSN chemistry 2560, first atomic-structure batch

- Created isolated worktree `.worktrees/posn-chemistry-2560` on
  `codex/posn-chemistry-2560` from `457822b`; existing physics work stayed in
  the original checkout. The worktree shares the ignored source bank and venv.
- Fetched the 2560 chemistry paper from LFS and split both parts separately:
  all 70 questions accounted for, including the printed `9 .` heading.
  Raw extraction and review notes are private-bank commit `c138e7d`.
- Visually checked source p4 and built three independently checked solvers
  and generators (MC3, MC4, MC6), with three knowledge claims and nine named
  mistakes. No full copied source text or source PDF is published here.
- `verify posn2560_chemistry`: 3/3 green, 10 variant checks, all independently
  checked. Knowledge validation: 774 units in 640 files, zero problems;
  source coverage: 3/70. First generator/solver batch: 39 checks passed.
  Existing golden fixtures are unchanged; only three new keys were recorded.
- Required full run: 38,977 passed, 13 skipped, seven failures all caused by
  omitting the new chemistry cohort from the frozen-baseline subtraction, and
  two setup errors because the sandbox denied binding a localhost HTTP server.
  Fixed the subtraction; all nine failed/error checks then passed, with local
  server access for the two explorer tests. Ruff and whitespace checks pass.
  The full suite was not repeated after this isolated cohort repair; the
  affected registry/curriculum checks were rerun separately.
- Final focused registry/curriculum/layout/solver checks: 64 passed. The final
  diagnostic label describes the oxide distractor as assuming metal charge +1.
  Its final generator/golden checks: six passed; no existing golden entry changed.
- Keep this paper partial; next items are MC1–2 and MC5, then MC7 onward.

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

### 2026-10-17 — 2551 national paper

- The 2551 national paper (5th TMO) has 16 questions over two days. 8 have
  answers:
  - day 1, item 1: cos θ = 3√3/√31;
  - day 1, item 2: 8/3, assuming BD > DC (the statement is symmetric in B and C);
  - day 1, item 3: x = 2, 5;
  - day 1, item 7: 87;
  - day 1, item 9: 3¹⁰;
  - day 1, item 10: 993;
  - day 2, item 2: N = 130;
  - day 2, item 5: (m(m − 1) + n(n − 1))/(m + n).
- Sixteen knowledge units and sixteen original sets, checked in
  `test_math_olympiad_posn_national_2551.py`. That file includes a full
  coordinate construction of the day 2, item 1 rhombus. The bank entry is
  `generated`.
- Open (sketched only):
  - day 2, item 1: the synthetic proof that ND ∥ PA;
  - day 2, item 6: extending the equation from x²y³ > 2008 to all x, y.
- Registry 3,851 sets; enrichment count 394.

### 2026-10-17 — 2550 national paper

- The 2550 national paper (4th TMO) has 24 questions over two days: 18
  short answers on day 1 and six proofs on day 2. The PDF has no text layer
  and no answer pages, so every answer was derived and checked by computer.
  20 have answers, including:
  - day 1, item 2: √10;
  - day 1, item 5: 2∛2;
  - day 1, item 10: n = 10;
  - day 1, item 14: C(8085, 169);
  - day 1, item 15: 225;
  - day 1, item 18: 1273;
  - day 2, item 1: f constant;
  - day 2, item 4: p = 3, 7.
- 24 knowledge units and 24 original sets, checked in
  `test_math_olympiad_posn_national_2550.py`. The bank entry is
  `generated`.
- Open (sketched only):
  - day 2, item 3: the angle chase that makes A, M, N, D concyclic.
- Registry 3,875 sets; enrichment count 418.

### 2026-10-17 — 2549 national paper

- The 2549 national paper (3rd TMO) has 24 questions over two days: 18
  short answers on day 1 and six proofs on day 2. The text layer drops the
  mathematics and there are no answer pages, so every answer was derived
  and checked by computer. 18 have answers, including:
  - day 1, item 4: 1/√5;
  - day 1, item 5: 118;
  - day 1, item 8: −37;
  - day 1, item 12: 14;
  - day 1, item 13: 781;
  - day 1, item 14: 1274;
  - day 1, item 17: 16.
- 24 knowledge units and 24 original sets, checked in
  `test_math_olympiad_posn_national_2549.py`. Day 2, item 4 (the 4 × 7
  foursome) has a written case proof and an exhaustive search; 4 × 6 can
  avoid one. Day 2, item 5 is settled by the witness m = 1, n = 45. The
  bank entry is `generated`.
- Open: none.
- Registry 3,899 sets; enrichment count 442.

### 2026-10-17 — 2548 national paper

- The 2548 national paper (2nd TMO) has 27 questions over two days: 21
  short answers on day 1 and six items on day 2. The text layer drops the
  mathematics and there are no answer pages, so every answer was derived and
  checked by computer. 23 have answers, including:
  - day 1, item 1: √6 − 2;
  - day 1, item 6: 1701;
  - day 1, item 9: 4050;
  - day 1, item 13: k = 181;
  - day 1, item 17: 23/233;
  - day 1, item 18: 1275/2;
  - day 1, item 20: √6/6;
  - day 2, item 5: 2⁴⁹.
- 27 knowledge units and 27 original sets, checked in
  `test_math_olympiad_posn_national_2548.py`. Day 2, item 3 records an
  explicit f with f(f(n)) = 2n, which the tests check directly. The bank
  entry is `generated`.
- Open: none.
- Registry 3,926 sets; enrichment count 469.

### 2026-10-17 — 2547 national paper

- The 2547 national paper (1st TMO) has 27 questions over two days: 21
  short answers on day 1 and six items on day 2. The text layer drops the
  mathematics and there are no answer pages, so every answer was derived
  and checked by computer. 25 have answers, including:
  - day 1, item 1: 5√6/18;
  - day 1, item 3: x³ − 74x² − 89x − 27;
  - day 1, item 11: 4620;
  - day 1, item 13: 668;
  - day 1, item 16: 536;
  - day 1, item 21: 8;
  - day 2, item 1: 35°;
  - day 2, item 3: 951;
  - day 2, item 5: p = 2.
- Day 1, item 2 has no real solution as printed (the bank note proves it).
  Its answer 3 is only a formal value, and its set uses the consistent sign.
- 27 knowledge units and 27 original sets, checked in
  `test_math_olympiad_posn_national_2547.py`. The bank entry is
  `generated`.
- Open: none.
- Registry 3,953 sets; enrichment count 496.
- Remaining POSN maths at `new`: none. `bank status` for `สอวน_math` now
  shows 18 `generated`, 7 `green` and 1 `ignored`.

### 2026-10-17 — national papers to `green`

- A national paper reaches `green` once it has its own package under
  `otk/sheets/`. Each question gets a solver (`PARAMS`, `ANSWER`, `solve`,
  an independent `check`, ≥ 3 `VARIANTS`) that `sheetpipe verify` passes.
- **Generators.** Each item's generator is the olympiad set already built from
  that question, not a second per-paper module. `test_sheetpipe.py` lists
  these sheets in `SHARED_GENERATORS` and checks that each `adapted` set's
  provenance cites the paper. The 2563–2567 papers' sets are declared
  `original`, so they are accepted without a citation.
- **Numbering.** Day 2 restarts at 1, so its six items are stored after day 1:
  q22–q27 for a 21-item day 1.
- **Proof items.** The solver computes the quantity the proof establishes, and
  the item's `note` says so.
- **2547 (`posnnat2547_math`).** 27/27 green. `bank scan` moved the record to
  `green`.
- **All national papers green.** 2547–2557 and 2562–2567 each have a
  `posnnat25YY_math` package, every solver verified. Together they hold 254
  solvers; `bank scan` moved every record to `green`.
  - 2563, 2564, 2566 and 2567 had no transcript. They were transcribed from the
    renders into the bank's `_transcribed/`. Fetch their PDFs with
    `sheetpipe bank fetch`; a plain `git lfs pull` fetches nothing, because the
    bank's `.lfsconfig` excludes PDFs.
- **Checks that caught real errors.**
  - The 2556 item 6 check found that for even k, ±sign(x)|x|ᵏ also solves the
    equation. The `power_sum_functional` helper was fixed; draws are unchanged.
  - The 2557 item 6 check found the extra prime 67 for (α, β) = (13, 52). The
    solver now searches both divisibility cases to a proven bound.
  - The 2566 item 5 boundary showed up only when the check tested the circle
    centres directly. Sampled chords missed it.
- **Still `generated`: `posn1-69` (2569 first round).** Its digest says the
  extracts and figures stay private, and the paper forbids publication without
  POSN's permission. A sheet package would publish its text and figure crops,
  so it waits for the maintainer.
- Review: the `ignored` index entries for the non-maths สอวน. folders (see
  the 2562 entry) were dropped from this branch to keep it to the maths
  papers. A later `bank scan` adds them back in a change of their own.

### 2026-10-17 — first POSN physics paper, 2560 camp selection

- Reviewed every exercise page of the 11-page PDF and all six automatic
  figure crops. The running-number extractor found only the 20 MCQs and
  merged the ten written items into item 20; the private transcript correctly
  preserves both sections and converts to 30/30 answered digest items.
- Added 30 solver modules with independent checks and 90 changed-constant
  cases, 30 seeded generators, 30 physics knowledge units, supplemental
  curriculum filing, stage metadata, provenance, diagnostic mistake names,
  golden draws, and source/generator regression checks. Knowledge validation
  reports zero problems, coverage is 30/30, and no knowledge gaps remain.
- Recorded four source caveats: item 2 specifies too little curvature data
  for total acceleration; item 5 determines average rather than instantaneous
  contact force; item 20 has both upright and inverted self-image answers
  (30/7 cm and 12 cm); written item 10 needs the screen displacement frame
  stated explicitly. Generated wording resolves each caveat.
- Source text and the full transcript stay in the private bank. The public
  sheet records source citations, paraphrases, parameter readings, and
  diagram notes. No static source crop is attached: labels vary, and crops
  for extracted items 9 and 20 actually contain later questions. Generated
  questions supply explicit geometry or graph coordinates instead.
- Targeted batches: wave 1, 3,878 passed; wave 2, 3,998 passed; wave 3,
  4,172 passed and one choice-length failure, corrected for the full run.
  The full suite ran **once**, after all 30 items were digested: 28,950 passed,
  2 skipped, 30 failed in 30m25s. Of the failures, 29 were new fingerprints
  captured before diagnostic names were added (the fingerprint includes
  those names); the other was the legacy electricity-topic test's cohort
  exclusion. Refreshed only the 30 new keys and added the explicit new cohort
  to that legacy assertion. Existing fingerprints are byte-for-byte unchanged.
  Focused repairs and regression checks: **4,277 passed**; Ruff clean.
  No second full run was performed. The same focused batch also verifies the
  final distractor formulas and printed Part 2 provenance numbering.

### 2026-10-17 — POSN physics 2561 camp selection

- Reviewed the 14-page paper and all 14 automatic figure crops. The extractor
  merges the ten restarted written questions into MC item 20, and its crop
  for that item actually belongs to written question 2. A private hand
  transcript preserves all 30 numbered items and answers; conversion yields
  30/30 answered digest items.
- Added 30 solver modules, each independently checked at the source data and
  three changed-constant cases, plus 30 seeded generators. All 30 items are
  claimed by 29 knowledge units (the two pulley items share one unit).
  Knowledge validation reports zero problems and no generator gaps.
- Explicit generated assumptions resolve source ambiguities: the table/pulley
  speed is restricted to travel on the table, the balloon starts from rest,
  and both door hinges have upward vertical components. The other source
  hinge branch also satisfies equilibrium and is tested separately. Fluid
  labels, circuit connections, graph coordinates, and torque arms are stated
  directly; variable source figures are not attached as static crops.
- The beam-expander source includes a ray drawing and a numerical separation.
  Its checker traces three rays, verifies parallel output and the beam-width
  ratio, and independently finds the lens separation. The generator practises
  the afocal separation condition.
- Targeted waves: 4,383 passed; 4,523 passed; 4,664 passed with one test-helper
  failure parsing negative TeX fractions. Corrected the parser; its focused
  regression passes. All 3,779 existing golden records remain unchanged.
- The full suite ran once, after all 30 items were digested: **29,421 passed,
  2 skipped in 24m57s**. Ruff is clean; source transcripts and full-text digests
  remain in the private bank.

### 2026-10-17 — POSN physics 2562 camp selection

- Reviewed exercise pages 2–10 of the 13-page paper and all 23 automatic
  crops. The paper declares 26 questions: 15 MC, ten short answers, one worked
  problem; pages 11–13 are answer forms. Crops for items 1 and 2 are fragments
  of item 4's choices, and item 26's crop is an answer form. No crop is shipped;
  the generators state geometry, polarity, angle conventions, and topology.
- Added 26 solvers with independent derivations and 78 changed-constant cases,
  plus 26 seeded generators. Every converted item is claimed; the existing
  signed circuit procedure covers item 13, and 25 knowledge units are new.
  Knowledge validation reports zero problems and no generator gaps.
- Source caveats are explicit in generated wording: item 3 gives only a
  necessary siphon-height bound; item 7 requires steady conduction; item 14
  starts with DC steady charging; item 19 uses the limiting release from nearly
  vertical; item 24 needs small-angle motion for the intended half-period.
  Finite-amplitude pendulum timing is not fixed by the source as printed.
- The simultaneous three-disc impact verifies and generates the ordered pair
  of both requested outgoing speeds, including momentum, kinetic energy, and
  restitution checks. Ring-field choices retain exact reduced radicals.
- Targeted waves: 4,394 passed; 4,522 passed; 4,636 passed.
- The full suite ran once, after all 26 items were digested: **29,796 passed,
  2 skipped in 20m08s**. Ruff is clean; full source text and the verified
  transcript remain in the private bank.

### 2026-10-19 — POSN physics 2564 camp selection

- The 11-page PDF is a scan (no text layer): page 1 is the cover, pages 2–10
  the questions, page 11 the answer form. There is no answer key. A private
  hand transcript from page renders converts to 30/30 answered digest items;
  item 26's battery polarities were read from a 300 dpi crop.
- Every answer was derived, checked symbolically in SymPy, and then given a
  solver with an independently written check (time-stepping, Simpson
  quadrature, Biot–Savart and Coulomb element sums, ray tracing in
  coordinates, bisection on the original equations). `sheetpipe verify`:
  30/30 green, 90 variant runs, none without an independent check.
- Source readings made explicit in generated wording: item 6 treats the ball
  as a point with full buoyancy to the surface; item 21's θ is the incidence
  angle at the second face; item 27's x is the perpendicular distance between
  the leaving ray and the incident line, and needs μ sinθ < 1; item 28 names
  each body's mass m, which the source leaves unnamed. Items 1, 5 and 16 ask
  a computed quantity that follows from the printed condition (relative
  acceleration, greatest extension, least energy); item 4 asks e for given
  masses; item 30 generates the ordered pair (tanθ, u²).
- Fraction display: `otk.kit.answer_choices.show` rounds to two decimals, and
  four earlier sets printed a wrong number in their stems: `posn2562_q04`
  (a/A = 1/3 as 0.33), `posn2562_q20` (μ = 5/12 as 0.42), `posn2560_q07`
  (40/3 N as 13.33 N) and `posn2562_q08` (α = 3×10⁻⁵ as 0). The new
  `answer_choices.exact` never rounds (short decimal, k×10⁻ⁿ, or a/b); the
  2560, 2562 and 2564 physics files use it. Only those four sets' golden
  draws changed (maintainer-approved); `test_exact_stem_numbers.py` guards them.
- Targeted run: 18,332 passed, 4 skipped (golden draws, curriculum, stages,
  layout, characterization, sheetpipe, choice counts, answer length, the
  sheet's own tests); `test_per_set` for the 30 keys: 60 passed; Ruff clean.
- The full suite ran once, after all 30 items were digested: **33,240 passed,
  13 skipped in 12m23s**.

### 2026-10-19 — POSN physics 2565 camp selection

- 12-page scan (no text layer, no answer key): cover, questions on pages
  2–11, answer form on page 12. A private hand transcript converts to 30/30
  answered digest items. Item 2's battery polarities and item 11's arcs were
  read from 250 dpi crops: all four emfs face the same way, and both arcs are
  half circles with the same circulation joined by radial leads.
- Every answer was derived and given a solver with an independently written
  check (KCL bisection, Gauss-law integration, catenary, paraxial ray trace
  through lens and mirror, Biot–Savart sums, velocity-Verlet orbit, time-stepped
  slides and pendulum). Four first-draft checks disagreed with their solvers;
  each was a fault in the check, not the answer, and was rewritten.
  `sheetpipe verify`: 30/30 green, 90 variant runs.
- Readings made explicit: item 9's centre offset equals the radius; item 19
  ignores added mass; item 27 is the first-order aim correction for a target at
  launch height; item 29 assumes thin spokes and entry just after a spoke.
  Generalized items: 1 (m^a v^b in the exponent), 2 (any emfs), 3 (+pQ, −sQ),
  13 (any of the five heating-curve processes), 22 (mixtures of monatomic and
  diatomic gas).
- `test_per_set` flagged three shortest-choice cues (items 12, 23, 28: an
  integer or plain decimal among fractions and powers of ten). The generators
  now draw values that put the answer in the same form as its distractors.
- Targeted run: 18,666 passed, 4 skipped; `test_per_set` for the 30 keys: 60
  passed; the sheet's own tests: 64 passed; Ruff clean.
- The full suite ran once, after all 30 items were digested: **33,681 passed,
  13 skipped in 10m09s**.

### 2026-10-19 — POSN physics 2566 camp selection

- 12-page PDF with a text layer but every formula and figure as a picture;
  the text runs out of order, so the transcript comes from page renders. The
  cover declares 28 questions: 1–20 four-choice, 21–27 short answer, 28 worked.
  No answer key; conversion yields 28/28 answered digest items.
- Each answer has a solver with an independently written check (rigid-body
  slicing, time-domain splat impulse, golden-section peak search, isothermal
  column integration, Gauss–Seidel network relaxation, RC circuit simulation,
  paraxial ray trace through a swapped meniscus, torque bisection). `sheetpipe
  verify`: 28/28 green, 84 variant runs.
- Readings made explicit: item 4 uses the splat model (stopping time 2r/v);
  item 10's still strand runs from A to the fold; item 13's starred capacitor
  is in parallel with the lower resistor, so its charge rises then decays;
  item 17's lens B is a diverging meniscus with its R₂ surface first; item 19's
  six resistors join four nodes pairwise. The four graph items become numeric
  (5: peak speed; 9: ψ at given x, t; 12: field-peak distance) or a concept
  choice whose solver is checked by simulation (13).
- Generalized items: 2 (support position), 8 (unequal branches), 11 (brine),
  16 (incidence angle), 19 (six arbitrary resistors), 25 (final angle).
- Targeted run: 18,975 passed, 4 skipped; `test_per_set` for the 28 keys: 58
  passed; the sheet's own tests: 60 passed; Ruff clean.
- The full suite ran once, after all 28 items were digested: **34,082 passed,
  13 skipped in 10m01s**.

### 2026-10-19 — POSN physics 2567 camp selection

- 10-page PDF, formulas and figures as pictures; the cover declares 16
  questions (1–15 short answer, 16 worked) and gives Coulomb's and the
  Biot–Savart law and ln 10 ≈ 2.303. No answer key; conversion yields 16/16
  answered digest items.
- Readings from 300–600 dpi crops: item 7's plates 1 and 4 share the negative
  terminal and 2 and 3 the positive one, so only the outer two gaps hold
  charge (C = 2ε₀A/d); in item 9 the inner loop runs counter-clockwise and the
  outer loop clockwise, B = (μ₀I/2)(1/R₁ − 1/R₂) out of the page.
- Each answer has a solver with an independently written check (time-stepped
  slides and flights, Cramer's rule, a double Biot–Savart sum for the loop
  force, Gauss-law plate charges, RC simulation, direction-vector rotation for
  the raindrop, Gauss–Seidel ladder). `sheetpipe verify`: 16/16 green, 48
  variant runs. Item 11's check confirms the ln N + 0.577 estimate against the
  exact harmonic sum to 0.5%.
- Generalized items: 1 (free-fall depth), 3 (energy fraction), 5 (current
  sense, signed force), 7 (any plate pattern), 9 (loop senses), 11 (N = 10^k),
  15 (T₁ and K/l), 16 (ladder values and node).
- Targeted run: 19,131 passed, 4 skipped; `test_per_set` for the 16 keys: 46
  passed; the sheet's own tests: 35 passed; Ruff clean.
- The full suite ran once, after all 16 items were digested: **34,314 passed,
  13 skipped in 10m54s**.

### 2026-10-19 — POSN physics 2568 camp selection

- 9-page PDF, formulas and figures as pictures; 25 short-answer questions,
  Coulomb's and the Biot–Savart law given, no answer key. Conversion yields
  25/25 answered digest items.
- Readings: item 1's angles are measured from the vertical; item 14's object
  runs from 2.0f (A) to 1.5f (B); item 24 neglects the outlet's kinetic head
  (Poiseuille flow driven by ρgh); item 25's two straight wires are
  semi-infinite and end on the line through O, and all three parts of the
  path add at O.
- Each answer has a solver with an independently written check (time-stepped
  flights, slides and spring collision, ring element sums for E and moving
  charges for B, 1-D finite-volume heat relaxation, paraxial trace through
  the afocal pair, a direct sum of 1/i² to 200,000 terms, virtual work for
  the plate force, vector-summed three-body forces, the Poiseuille velocity
  profile integrated over the section, a Biot–Savart sum along the hairpin).
  `sheetpipe verify`: 25/25 green, 75 variant runs.
- Generalized items: 1 (launch and A directions), 2 (line-of-centres angle),
  10 (bar lengths and areas), 13 (focal ratio), 14 (object ends), 15 (δr/δl
  ratio), 16 (emf from R, C, q, i), 20 (exact π² form), 21 (six planets),
  22 (period scaling).
- Targeted run: 19,431 passed, 4 skipped; `test_per_set` for the 25 keys: 55
  passed; the sheet's own tests: 55 passed; Ruff clean.
- The full suite ran once, after all 25 items were digested: **34,674 passed,
  13 skipped in 11m53s**.

### 2026-10-19 — POSN physics 2569 camp selection

- 15-page PDF, formulas and figures as pictures. Part 1 has 10 questions with
  eight choices each; Part 2 has 20 short answers and restarts at 1. The
  transcript uses section headings, so conversion numbers them 1–30 (30/30
  answered); `sheet.json` sources keep the printed "ตอนที่ 2 ข้อ k".
- Readings: MC2 is the small-amplitude period with the peg at l/2; MC6 assumes
  three unrelated values (17 combinations); Part 2 item 5's hole touches the
  rim and passes through O; item 12's form asks a percentage, 100·C₁/(C₁+C₂);
  item 18 assumes m runs onto the floor without loss; item 20's second lens
  images the first lens's virtual focus.
- Each answer has a solver with an independently written check (bisection on
  conservation laws, time-stepped pendulum with peg and terminal fall, ring
  element sums, a recursive series–parallel enumeration for MC6, grid
  integration of the holed disc, catenary, torque bisection, a simulated
  projectile for the receding condition, paraxial ray traces). `sheetpipe
  verify`: 30/30 green, 90 variant runs. MC6's generator draws actual values,
  so coinciding combinations (e.g. 1, 2, 3 → 16) are counted exactly.
- Targeted run: 19,776 passed, 4 skipped; `test_per_set` for the 30 keys: 30
  passed; the sheet's own tests: 65 passed; Ruff clean.
- The full suite ran once, after all 30 items were digested: **35,104 passed,
  13 skipped in 14m08s**.

### 2026-10-19 — TPhO 1 (2545) national physics olympiad

- Folder of four PDFs, all with text layers: theory in Thai and English, the
  official theory solution, and the experimental paper. The English theory
  paper is the digested source (cleaner text; generated wording is Thai);
  the Thai theory paper and the solution are indexed `ignored` with notes.
- 17 items: theory I.1–I.5 (I.2 in two parts), II.a–e (hoop rolling on a rod),
  III.a–c (magnetic pump), and the experiment's theory parts (Newton's cooling
  law solved and fitted; the Airy dark-ring wavelength) with synthetic data.
  Every answer was re-derived and agrees with the official solution, whose
  III.c data line misprints B = 0.1 T while its arithmetic uses 1.0 T (13.8 W).
- Independent checks include a two-mass spring simulation, a shoelace flux
  for the tilted rod, time-stepped magnetic drag and rolling in the bowl,
  rolling-contact geometry and a mass-element KE sum for the hoop, and root
  finding for the cooling constant. `sheetpipe verify`: 17/17 green, 51 runs.
- Targeted run: 19,941 passed, 4 skipped; `test_per_set` for the 17 keys: 17
  passed; the sheet's own tests: 38 passed; Ruff clean.
- The full suite ran once, after all 17 items were digested: **35,351 passed,
  13 skipped in 11m20s**.

### 2026-10-20 — TPhO 2 (2546) national physics olympiad

- Folder of eleven PDFs: the combined theory paper (three problems) and its
  combined marking scheme, the same split per problem, and the combined
  experimental paper with its two labs split out. The two combined papers are
  the digested sources; the nine copies and marking schemes are `ignored` with
  notes.
- 21 items: 1.1 (v and V), 1.2 (first-order correction), 1.3 (detach angle,
  a choice item), 2.1–2.5 (fuse heating, loss and melting), 3.1–3.5, 3.7, 3.8
  (uniformly charged ball with point charges), and the labs' theory parts:
  rms V_C and C from the 1/V_C² against R² line; I from a bifilar period, the
  cavity shape and the cylinder radius. The sketches 2.6 and 3.6, the
  measurement 1.3 and the error discussion 2.3 have no generator but are
  claimed by their units. Every answer agrees with the marking scheme (2.2:
  0.694 °C/s, 0.70 in the scheme).
- Hanging 2.2(ข) turns the cube about an axis perpendicular to the cylinder,
  which reproduces the paper's I₂ = ρa⁵/6 − πρa³b²/12 − πρab⁴/4.
- Independent checks include RK4 of the Lagrangian for the sliding mass, a
  Newton solve of momentum and energy, the cylinder's maximum speed as the
  detach point, Coulomb quadrature over shells, field integration from
  infinity, complex impedance, and the exact bifilar geometry.
  `sheetpipe verify`: 21/21 green, 63 runs.
- Items 6, 7, 8 and 19 answer to three significant figures (their exact
  forms were fractions over π² with seven-digit terms); stems stay exact.
  Draws whose choices coincide are redrawn.
- Targeted run: `test_per_set` for the 21 keys passed; registry-wide and
  sheetpipe tests passed after recording `str(ANSWER)` in `sheet.json`; the
  sheet's own tests: 46 passed; Ruff clean.
- Full suite: **35,654 passed, 13 skipped in 12m22s**.

### 2026-10-20 — TPhO 3 (2547) national physics olympiad

- Folder of seven PDFs: the theory paper with its marking scheme bound in
  (11 pages), the same split per problem, and the combined experimental paper
  with its two labs split out. The combined theory paper and the combined
  experiment are the digested sources; the five copies are `ignored` with
  notes.
- 15 items: 1(a), 1(b), 1(e), 1(g) (mass pulled by a string over a pulley,
  with and without the pulley's inertia), 2.1 (rod on two springs), 2.2(a),
  2.2(b) (cue ball sliding to rolling), 2.3 (square loop on rails: the two
  sides are parallel cells with internal resistance r), 3(a), 3(b), 3(c),
  3(e) (echoes from a moving reflector; 3(e) is a choice item), and the labs'
  theory parts: I about the centre of mass of a physical pendulum, V_R/V_L of
  an RL circuit, L from the (V_L/V_R)² against 1/R² line. Parts 1(c), 1(d),
  1(f) and 3(d) are steps or limits of other items, claimed by their units.
  Every answer agrees with the bound marking scheme.
- Independent checks include finite differences of the string geometry,
  free-body torque on the pulley, a time-stepped rod with exact spring
  torque, a stepped slide-to-roll, a nodal-analysis loop circuit, event
  simulation of pulse reflections, and phasors. `sheetpipe verify`: 15/15
  green, 45 runs.
- Targeted run: 20,318 passed, 4 skipped; `test_per_set` for the 15 keys: 15
  passed; the sheet's own tests: 34 passed; Ruff clean.
- Full suite: **35,873 passed, 13 skipped in 11m01s**. (A first run started
  in the same batch as the bank commit ran from the bank directory and
  collected nothing; the full suite must run alone.)

### 2026-10-20 — TPhO 4 (2548) national physics olympiad

- Folder of four PDFs: the theory paper, its marking scheme, the two bound
  together (15 pages), and both experimental papers in one file (misspelt
  `thpo_4_exp.pdf`). The bound theory file and the experiments are the
  digested sources; the separate theory and scheme files are `ignored`.
- 19 items: 1.1 (two velocities), 1.2, 1.3 (best intermediate mass and the
  largest fraction it passes on), 1.4 (collisions to halve the energy), 2.1
  (assembly work, adapted to rectangles with whole-number sides and
  diagonal), 2.2–2.5 (proton square: centre potential, positron energy on
  the axis, launch speed over the numerical barrier, small-oscillation ω),
  3.1–3.5 (air between discs: speed, gauge pressure, lift, jet force,
  largest mass), and the labs' theory: κε₀/d from a foil capacitor's
  current, κ of the transparency, λ from a laser reflected off a steel
  ruler.
- Marking-scheme error: 1.4's n ≈ M/(8m) linearises (1 − 2m/M)^(2n) where
  4nm/M = 1/2 is not small. The scheme's own exact line,
  n = −ln 2/(2 ln((M − m)/(M + m))) ≈ (M/m) ln 2/4, is used (about 39% more
  collisions); M/(8m) is the named mistake `collision_count_linearised`.
- Independent checks include centre-of-mass reversal and the
  momentum–energy quadratic, golden-section search for the best mass,
  collision-by-collision counting, a potential grid search, a 45° curvature
  for ω, the radial Euler equation and ring sums for the discs, and
  arctangent angles for the laser. `sheetpipe verify`: 19/19 green, 57 runs.
- Item 18 failed the length-cue rule (a plain κ beside slips in scientific
  notation); one slip became the inverted ratio 1/κ.
- Targeted run: 20,539 passed, 4 skipped; `test_per_set` for the 19 keys
  passed after that change; the sheet's own tests: 41 passed; Ruff clean.
- Full suite: **36,147 passed, 13 skipped in 11m09s**.

### 2026-10-20 — TPhO 5 (2549) national physics olympiad

- One 16-page PDF holds the theory paper (pages 1–5), its marking scheme
  (6–12) and the experimental paper (13–16); transcribed as 18 parts.
- 14 items: 1.1 (focus of a convex–concave pair), 1.2 (least friction to
  roll, adapted to a cylinder, sphere or hoop), 1.3 (least height for a
  loop; normal force level with its centre), 2(a)–(c) (diving-bell caisson:
  river depth, extra air, least tank mass), 3(a)–(d) (Thomson atom: ω for
  one electron, radius from a spectral line, two-electron spacing and
  frequency), and the labs: prism index at minimum deviation, a steelyard
  reading, specific gravity by Archimedes. Lab procedure and measurement
  parts are claimed by their units.
- Marking-scheme discrepancy: 3(b) prints R ~ 0.28 nm for 656 nm; its formula
  with the paper's constants gives 0.313 nm (checked by bisection on the
  emitted wavelength); a test pins it.
- Independent checks include ray-transfer matrices, a slip bisection, energy
  with explicit rotation, Boyle's-law bisection on the fill, a time-stepped
  Thomson oscillator, a numerical two-electron stiffness, and a prism ray
  trace for minimum deviation. `sheetpipe verify`: 14/14 green, 42 runs.
- Targeted run: 20,689 passed, 4 skipped; `test_per_set` for the 14 keys
  passed; the sheet's own tests: 32 passed; Ruff clean.
- Full suite: **36,352 passed, 13 skipped in 11m44s**.

### 2026-10-20 — TPhO 6 (2550) national physics olympiad

- Folder of six PDFs: the theory paper, its marking scheme, the two bound
  together (24 pages), and the experimental papers both combined and split.
  The bound theory file and the combined experiments are the digested
  sources; the four copies are `ignored` with notes.
- 16 items: 1.1.1 (bar lengths from equal sound travel times, adapted ratios;
  1.1.2's zero phase difference is claimed by the unit), 1.2 (plano-convex
  radius and the internal-reflection image), 1.3 (adiabatic piston drop,
  adapted compression ratio), 2.1–2.3.2 (sliding and spinning rod emf, the
  spoked wheel's current and terminal speed), 3.1–3.4 (roller and block on
  an incline: least and greatest holding force, acceleration with a hanging
  mass, μ_s for rolling), and the labs: thermistor B, spring constant and
  effective mass from the T²–M line, beam mass on a spring. Every answer
  agrees with the marking scheme.
- Independent checks include exact Snell ray traces through the lens and
  its inner reflection, an adiabatic work integral, the swept-flux route,
  a time-stepped wheel (sized to its time constant after a first run
  stopped short), friction-limit bisections, an energy route for the
  rolling system, and bisections on B, k and M. `sheetpipe verify`: 16/16
  green, 48 runs.
- Targeted run: 20,873 passed, 4 skipped; `test_per_set` for the 16 keys
  passed; the sheet's own tests: 35 passed; Ruff clean.
- Full suite: **36,584 passed, 13 skipped in 12m02s**.

### 2026-10-20 — TPhO 7 (2551) national physics olympiad

- Folder of eleven PDFs: the theory paper, its 23-page marking scheme, both
  split per problem, and the experimental papers combined and split. The
  theory paper and the combined experiments are the digested sources; the
  nine others are `ignored` with notes.
- 15 items: 1.1.2 (slit shift when liquid fills the mirror-lens, L' =
  R/(2n − 1)), 1.2.2–1.2.3 (drop deviation and the minimum-deviation
  incidence), 2.1 and 2.3–2.5 (a charge through a uniformly charged ball:
  exit speed, work inside, centre speed, centre-to-surface time), 3.1–3.3
  (wedge, block and pulley: held wedge, cut string, intact string with the
  wedge free; masses adapted), and the labs: P_atm from the 1/L–h line
  (asked in kPa so the answer is not the only number in scientific
  notation), and a potentiometer emf. Steps 1.1.1, 1.2.1, 2.2, 3.3.2 and
  3.3.3 are claimed by their units; the drop items join the existing
  `raindrop-deviation` unit. Every answer agrees with the marking scheme.
- Independent checks include a vector ray trace through the drop, RK4 runs
  through the charged ball, an energy route for the held wedge, and a
  Lagrangian for the free wedge against the paper's four force equations.
  `sheetpipe verify`: 15/15 green, 45 runs.
- Targeted run: 21,043 passed, 4 skipped; `test_per_set` for the 15 keys
  passed; the sheet's own tests: 33 passed; Ruff clean.
- Full suite: **36,804 passed, 13 skipped in 11m08s**.

### 2026-10-20 — TPhO 8 (2552) national physics olympiad

- Folder of eleven PDFs laid out like TPhO 7: the theory paper and the
  combined experiments are the digested sources; the separate solution and
  the per-problem and per-lab copies are `ignored` with notes.
- 16 items: 1.1–1.4 (leaking gas tank, moving object's image, electron
  leaving a triangular field parallel to x, charged ball through two
  regions), 2.1–2.3 (stacked elastic balls: height multiple for a general
  m/M, the light ball's speed, time and height of the second collision),
  3.1–3.4 (plate force, spring constant, oscillation ω, the d ≥ D/3 limit),
  and the labs: the square coil's axial field, the Hall sensor's
  sensitivity, a disc magnet's surface field, g from a rod pendulum.
- Marking-scheme error: 2.3 prints the second collision at 0.82 m; its own
  equations (4)–(5) at t = 0.224 s give 0.90 m (an event simulation
  agrees, and a test pins it). The time, 0.48 s, is right. The generator
  keeps to the case the scheme solves (the light ball reaches the ceiling;
  the heavy ball is still in flight).
- Independent checks include a wall-force sum, a chief-ray image, a
  bisection on the exit point, an event simulation of the stacked balls, an
  energy route for the plate force, a bisection on the stable stretch, a
  Biot–Savart sum for the square coil, and a compound-pendulum bisection.
  `sheetpipe verify`: 16/16 green, 48 runs.
- Targeted run: 21,228 passed, 4 skipped; `test_per_set` for the 16 keys
  passed; the sheet's own tests: 36 passed; Ruff clean.
- Full suite: **37,038 passed, 13 skipped in 11m38s**.

### 2026-10-20 — TPhO 9 (2553) national physics olympiad

- Folder of six PDFs laid out like TPhO 6: the bound theory-with-solution
  file (19 pages) and the combined experiments are the digested sources;
  the four copies are `ignored` with notes.
- 14 items: 1.1–1.4 (a light block shuttling between a heavy block and a
  wall: v1, the second and third meeting points, the closest approach
  ℓ₀√(m/M)), 2.1–2.4 (twin pistons on helium: pressure, rise on warming,
  restoring force, period), 3.1 (voltage-doubler table rows, a choice
  item), 3.2.3 (double-star separation and the first vanishing slit
  spacing; 3.2.1–3.2.2 are its steps), and the labs: Brewster angle, a
  syrup's index from its Brewster angle, the seiche period of student 3's
  model (the other students' models are the named mistakes). Every answer
  agrees with the bound solution.
- Independent checks include an exact collision-by-collision simulation
  (which also confirms ℓ₀√(m/M) within 0.2% at M/m = 100), force
  bisections, an exact adiabatic linearisation and a time-stepped piston,
  a time-stepped diode circuit, Fresnel's r_p for the Brewster angle, and
  an energy route for the seiche. `sheetpipe verify`: 14/14 green, 42 runs.
- Targeted run: 21,383 passed, 4 skipped; `test_per_set` for the 14 keys
  passed; the sheet's own tests: 31 passed; Ruff clean.
- Full suite: **37,243 passed, 13 skipped in 11m14s**.

### 2026-10-20 — TPhO 10 (2554) national physics olympiad

- Same six-PDF layout as TPhO 9: the bound theory-with-solution file
  (17 pages) and the combined experiments are the digested sources; the
  four copies are `ignored` with notes.
- 20 items: 1.2–1.6 (a superconducting ring falling onto a magnet: current
  at depth z, the stiffness k, equilibrium z₀, ω, peak current at 2z₀;
  1.1 is a step of 1.2), 2.1–2.6 (two masses on one string turning about
  the vertical: centre of mass, upper tension, the constants A–D as a
  choice item, the small-angle β, and with the middle mass sliding: β and
  L₂/L₁), 3.1–3.7 (a falling water jet: Bernoulli radius, the γ/R pressure,
  the first-order ΔR with 3.3–3.4 as its steps, the break-up distance, the
  drop radius 3R/2), and the labs with synthetic data: one diode's
  threshold from the two directions' thresholds, R from a least-squares
  slope, μ_s from a slope, μ_k from the x_A–x_B slope.
- Scheme slips: 3.6 prints 0.84 m, but t = 0.12 s gives 0.084 m (pinned in
  the test). 3.5's ΔR = 1.34×10⁻⁵ m is its simplified form; the generators
  use the full first-order form (1.32×10⁻⁵ m), and the test pins both.
- Independent checks include an RK4 fall of the ring (ω from turning
  points, peak current from the deepest point), Newton's-law bisections
  for the string angles (the A–D constants recovered by Cramer's rule from
  three solved configurations), a Newton step on the 3.3 relation for ΔR,
  and pressure integrals and time-stepped falls for the jet.
  `sheetpipe verify`: 20/20 green, 60 runs.
- Targeted run: 21,624 passed, 4 skipped; `test_per_set` for the 20 keys
  passed; the sheet's own tests: 45 passed; Ruff clean.
- Full suite: **37,535 passed, 13 skipped in 11m06s**.

### 2026-10-20 — TPhO 11 (2555) national physics olympiad

- Eleven PDFs: the theory paper (4 pages) and its separate solution
  (5 pages), per-problem copies of both, and the labs combined and split.
  The digested sources are `tpho_11_theory.pdf` (answers confirmed against
  `tpho_11_theory_solution.pdf`) and `tpho_11_exp.pdf`; the other nine are
  `ignored` with notes.
- 18 items: 1.1 ก–ค (pinhole image size, with diffraction, best hole
  √(2.44λL)), 1.2 ข (W-tube level H = 2h; 1.2 ก is a sketch), 2 ก–จ (dust
  sticking to a spring oscillator: u₀, loss ½Δmv², loss per cycle
  ΔmE₀/(2m), Δω = ω₀ΔE/E₀, E ∝ ω), 3 ก–จ (charged conducting plate with a
  hole: σ/ε₀, E_r/E = r/d, v_r = erE/(mu) with 3 ค as its step, focus
  3mu²/(2eE)), and the labs with synthetic data: a nut's mass by
  comparison with a battery, a plastic tube's spring constant, k from
  Hooke's law, β₁ from T² against M, and β₂ from the top and bottom turn
  lengths. Every answer agrees with the solution.
- Independent checks include traced extreme rays, a golden-section search
  for the best hole, a pressure bisection, an exact sticking collision
  scaled to first order, dust added in 200,000 small portions (E ∝ ω), a
  finite-disc field, div E = 0 in the hole, time-stepped protons, and
  reverse or Cramer's-rule fits. `sheetpipe verify`: 18/18 green, 54 runs.
- Targeted run: 21,823 passed, 4 skipped; `test_per_set` for the 18 keys
  passed; the sheet's own tests: 40 passed; Ruff clean.
- Full suite: **37,797 passed, 13 skipped in 12m32s**.

### 2026-10-20 — TPhO 12 (2556) national physics olympiad

- Three PDFs: the theory paper, the experimental paper and the
  experiment's solution (`ignored`, used to confirm the lab answers).
  There is **no theory solution**: every theory answer was derived here and
  checked by an independent route; the transcript says so.
- 21 items: 1.1 ก–ค (three hinged rods jerked at the middle: CD's v_y,
  ω = 3u cos θ/(2l), impulse (3/2)mu(1 + sin²θ)), 1.2 ก–จ (meteor: stagnation
  force, deceleration, the constant a in v = u·e^(a·e^(bz)), the brightest
  height, read as the largest power ρv³, and the pressure there), 2 ก–ช
  (gas through a valve into a spring cylinder: P_B, V_B, W_A, W_B, ΔU,
  T_B/T_A = 2γ/(γ + 1)), 3 (rainbow: the bright incidence, primary 42.5°,
  secondary 50.1°; sketches and the dark band are claimed by the units), and
  the lab with synthetic data: μ from the torsion period, the matching
  string length, B_v from τ_max and the inclination.
- Solution slip: the lab's part 5 prints B_v = 0.13 T; its numbers give
  0.133 G = 1.3×10⁻⁵ T (pinned in the test).
- Independent checks include a five-unknown impulse system for the rods,
  Bernoulli integrated along the stagnation line, a Simpson descent of the
  meteor with the brightest point from the ODE's own rate, a parcel-by-parcel
  enthalpy simulation of the valve, golden-section searches on the ray
  deviation, a time-stepped torsion pendulum, and bisections of equation (2).
  `sheetpipe verify`: 21/21 green, 63 runs.
- Process note: a script that set `ANSWER` opened each solver for writing
  before reading it and emptied all 21 files; they were rebuilt from the
  session's own heredocs, the later edits re-applied, and verify re-run.
  Read a file fully before reopening it for writing.
- Targeted run: 22,071 passed, 4 skipped; `test_per_set` for the 21 keys
  passed; the sheet's own tests: 48 passed; Ruff clean.
- Full suite: **38,106 passed, 13 skipped in 11m24s**.

### 2026-10-20 — TPhO 13 (2557) national physics olympiad

- Four PDFs: theory and experiment papers with a solution each (the
  solutions `ignored`, used to confirm every answer; all agree).
- 17 items: 1.1 (wedge fringes: spacing λ/(2n tan θ), expansion
  coefficient from the fringes that pass), 1.2 (passing source: the shift
  heard at closest approach f₀v²/(v² − u²) − f₀, the distance when f₀ is
  heard), 2 (one-wheeled table: stopping distance, the no-tipping limit
  w/(2h), μ from the reversed/forward distance ratio), 3.1 (water hammer:
  ρvu, v = √(B/ρ), the lift vu/g + u²/g), 3.2 (moving dielectric:
  polarisation field and emf vBd(1 − 1/εᵣ)), and the eddy-current lab with
  synthetic data: B of the wheels from V² against a, b and μ from terminal
  speeds, σ = b/Λ and k = Λ/(dD²B²).
- Scheme note: the lab solution's sin θ column corresponds to a 0.75 m
  incline, not the stated 0.70 m; its own v/cos θ and tan θ columns give
  the printed slope 0.366, b = 0.466 kg/s and μ = 0.18 (pinned in a test).
  The generators use the stated 0.70 m with self-consistent data.
- Independent checks include bisected fringe positions and fringe counts,
  retarded-time Doppler from arrival times, a 3 × 3 force-and-torque system
  for the table, a time-stepped falling parcel, a self-consistent
  polarisation bisection, a numerically integrated Faraday-disc emf, and a
  strip-summed disc for Λ. `sheetpipe verify`: 17/17 green, 51 runs.
- Targeted run: 22,254 passed, 4 skipped; `test_per_set` for the 17 keys
  passed; the sheet's own tests: 38 passed; Ruff clean.
- Full suite: **38,354 passed, 13 skipped in 11m52s**.

### 2026-10-20 — TPhO 14 (2558) national physics olympiad

- Four PDFs: theory and lab papers with a solution each (the solutions
  `ignored`, used to confirm every answer).
- 17 items: 1.1 (charged pendulum in a horizontal field: θ_m = 2 tan⁻¹(qE/mg),
  θ₀, the small-oscillation frequency), 1.2 (railway barrier: the
  counterweight distance for the fastest lift, exact and with τ ≈ MgL/2),
  2.1 (sealed vessel with a water film: P_G, the film thickness, t_B/t_A),
  2.2 (pop gun: the adiabatic gap L, the muzzle speed, the best barrel D),
  3 (eddy heating of a copper disc: peak emf, mean power zπa⁴B₀²ω²/(16ρ)),
  and the saline lab with synthetic data: needle bore from the jet, viscosity
  from Poiseuille, the series viscosity η_c, surface tension from drops.
- Scheme slip: the lab's per-drop volume, 1.20 ml/50 = 0.0240 ml, is used as
  0.0235 ml (γ = 83.6 instead of 85.4 mN/m; both pinned in the test).
- Independent checks include an RK4 swing to the turning point, golden-section
  maximisation of the barrier's angular acceleration, mole counting, an Euler
  adiabatic compression, Simpson-integrated pellet work, ring-by-ring and
  period-averaged eddy power, and bisected radius, viscosity and tension.
  `sheetpipe verify`: 17/17 green, 51 runs.
- A q10 draw could leave negative work (the pellet stops in the barrel); the
  generator now redraws those.
- Targeted run: 22,448 passed, 4 skipped; `test_per_set` for the 17 keys
  passed; the sheet's own tests: 38 passed; Ruff clean.
- Full suite: **38,603 passed, 13 skipped in 11m44s**.

### 2026-10-20 — TPhO 15 (2559) national physics olympiad

- Four PDFs: theory and lab papers with a solution each (the solutions
  `ignored`, used to confirm every answer).
- 23 items: 1.1 (streamlines; the Venturi sprayer's minimum speed
  √(8ρ_wgh/(15ρ_a))), 1.2 (wire stretch with temperature: ΔL₁, ΔL₂, the
  compensating area A = (W/Y₀)(ε/(αY₀) − 1), using the solution's
  consistent second form), 1.3 (vacuum lamp: σA(T⁴ − T₀⁴), I ∝ V^0.6
  generalised to R ∝ T^p), 2 (air conditioner: P′_N₂, V = 77.33 m³, the
  atmosphere's work, 777.6 g condensed, 1929 kJ latent, 2506 kJ total, 77%),
  3 (pump drill: α, b = L(θ₀ − θₙ), ω, the balanced push, mean power,
  k = μr/2), and the LDR lab with synthetic data: γ from log R against
  log x, the lamp's luminous flux, grating wavelengths, the corrected
  response ratio.
- Scheme notes: the lab solution's γ = −0.63 (slope 1.2531) comes from a
  graph whose points differ from its table; the table's 14 readings fit
  slope 1.302 (γ = −0.65), pinned in the test. Its 263 lux uses c₁ rounded
  to 4.3×10⁴ while its 294 lm uses 4.27×10⁴ (rounding, not an error).
- Independent checks include a bisected Venturi suction, stepwise warming
  of the wire, an exact small-ΔT bisection for the area, two hot steady
  states for n, mole counting for the air conditioner, RK4 winding of the
  rope angle, the unwinding torque integrated for ω, and summed blade and
  sphere elements. `sheetpipe verify`: 23/23 green, 69 runs.
- Targeted run: 22,722 passed, 4 skipped; `test_per_set` for the 23 keys
  passed; the sheet's own tests: 51 passed; Ruff clean.
- Full suite: **38,938 passed, 13 skipped in 12m06s**.

### 2026-10-20 — TPhO 16 (2560) national physics olympiad

- Four PDFs: theory (20 pages, the last two background reading) and lab
  papers with a solution each (the solutions `ignored`, used to confirm
  every answer). The text layer was readable, so most of the transcript was
  taken from it and checked against page images.
- 20 items: 1.1 (a planet hitting a resting rock: √(u² + 2gR) − u),
  1.2 (triangle cycle: p_C = 7.5 atm, e = 4.8%, the limit 5%), 1.3 (eye
  resolution: 336 µrad diffraction, 42 µrad cones, 101 µm pixels),
  2 (Mach-Zehnder sugar sensor: 377 ppm per fringe, the bright-port
  intensity, 12 ppm from a 0.6 V reading, the 6 ppm misreading after a
  brightness change), 3 (accelerator: proton speed, the dipole current
  1.14×10⁴ A, beam spreading a₀ and β = 5.94×10⁻⁷ m⁻¹, the quadrupole
  gradient 2μ₀I/(πR²), f = mv/(bqd), the doublet f(f − L)/L), and the
  magnet lab with synthetic data: n from log M against log r, k from the
  fall time against 1/m.
- Scheme slip: the lab's k = 27.05 g·s × 9.78/1.01 m = 0.262 kg/s, printed
  as 0.265 (pinned in the test).
- Independent checks include a finite-mass collision bisection, a
  numerically integrated triangle cycle, the Airy zero from a J₁ series,
  a time-averaged field sum, a finite-length Biot-Savart dipole, shell-summed
  beam forces, four-wire field sums, a thin-lens limit by shrinking the lens,
  and ray-transfer matrices for the doublet. `sheetpipe verify`: 20/20 green,
  60 runs.
- Targeted run: 22,941 passed, 4 skipped; `test_per_set` for the 20 keys
  passed; the sheet's own tests: 44 passed; Ruff clean.
- Full suite: **39,228 passed, 13 skipped in 28m19s** (slower than usual
  on this run).

### 2026-10-20 — TPhO 17 (2561) national physics olympiad

- Three PDFs: theory paper, its solution (a scan whose text layer is
  unreadable; `ignored`, used to confirm the answers it shows legibly) and
  the lab paper (no lab solution). The theory paper's text layer has a
  garbled maths font, so equations were read from page images.
- 22 items: 1.1 (a mass bouncing on a spinning beam: L = 2v² sin θ₀/g,
  MLω = 6mv, m/M = θ₀ tan θ₀/3 for the smallest turn 2θ₀), 1.2 (vacuum
  flask: net flow ε₁ε₂σ(T₁⁴ − T₂⁴)/(ε₁ + ε₂ − ε₁ε₂), 6.24 days to melt),
  1.3 (falling rod on a smooth floor: a_B and a_C, strings slack above
  54.7°; 1.3 d is left unanswered), 2 (watt balance: B_r = 0.081 T,
  m = 1.0 kg, m = VI/(ug), the Josephson voltage, the Hall resistance
  h/(νe²), the relative error 1.8×10⁻⁸), 3 (acoustic levitation: P_m, c,
  kinetic and momentum densities, the second-order mean pressure, the push
  of 2.9×10⁻³ N/m² at 120 dB), and the rice lab with synthetic data: the
  heap angle, α₁ from the rolling cylinder, the packing density.
- Scheme note: the lab's linearisation sin θ_c = 0.508 η sin α₁ + const
  does not match its own x_cm(η) (tangent 16/(3π²) = 0.540; a fit over its
  range gives 0.522). The generated item follows the paper's equation (2);
  a test pins the exact tangent.
- Independent checks include a stepped projectile, an elastic-impact
  bisection for the spin, an explicit bounce-by-bounce radiation sum, a
  3 × 3 force-torque system for the rod, a segment-summed coil force,
  dimensional exponents by substitution, worst-case error propagation,
  period averages of the sound fields, and the intensity route for the push.
  `sheetpipe verify`: 22/22 green, 66 runs.
- Targeted run: 23,193 passed, 4 skipped; `test_per_set` for the 22 keys
  passed; the sheet's own tests: 48 passed; Ruff clean.
- Full suite: **39,546 passed, 13 skipped in 14m12s**.

### 2026-10-21 — TPhO 18 (2562) national physics olympiad

- Two PDFs, the theory paper and the LED lab paper, both with clean text
  layers; the folder has no solutions, so every answer is derived here and
  checked by an independent route.
- 24 items: 1 (hydraulic jump: momentum flux ρLh₁v₁², the net hydrostatic
  force, h₂ = (h₁/2)[√(1 + 8v₁²/(gh₁)) − 1], the energy loss with k = 1/4,
  the circular jump R = 4Q²/(π²d²gH²)), 2 (power transmission: P_LR_w/V_L²
  = 0.207, solenoid L = μ₀n²πr²ℓ, M = √(L₁L₂), the primary current, the line
  loss 2.07×10⁻⁷ with a 1000:1 transformer), 3 (protostars: the Sun's
  surface 5.80×10³ K, the binary K.E. = Gm²/(4r), A = 3/5, the virial
  temperature 4.61×10⁶ K, dE/dT = −2.48×10³⁴ J/K, α = 1/2, N/V =
  4.36×10³² m⁻³, M_min = 2.0×10²⁹ kg ≈ 0.1 M☉), and the LED lab with
  synthetic data: the ideality factor, I₀, R_s, the infrared wavelength from
  V_t against 1/λ, the fill factor, R_SH. 2.6 and 3.8 (qualitative) have no
  generator; lab 3.2 C is left unanswered.
- Readings: 1.5's form k ρg(h₂ − h₁)(h₂² + h₁²)/(h₁h₂) needs the energy
  per volume ½ρv² + ½ρgh (k = 1/4); the head h + v²/2g gives the textbook
  (h₂ − h₁)³/(4h₁h₂) instead (a test pins both). 3.10's "smallest N/V" is
  read as the density where the lightest igniting cloud peaks, P_deg =
  P_ideal, which also minimises the mass in 3.11 (a test checks both agree).
- Independent checks include a strip-summed hydrostatic thrust, a momentum
  bisection for h₂, complex phasors for the transformer, an ideal-transformer
  line current, a shell-summed self-energy, an integrated hydrostatic centre
  pressure, golden-section searches for the ignition density and mass,
  centred least squares for the lab lines, and bisections for R_s and R_SH.
  `sheetpipe verify`: 24/24 green, 72 runs.
- Generators reject a draw whose choices mix plain and scientific numbers;
  stems state small readings as mantissa×10ⁿ in plain text.
- Bank index: only the folder's two files were added (a scan also listed
  unrelated new files elsewhere in the bank, left unindexed).
- Targeted run: 23,469 passed, 4 skipped; `test_per_set` for the 24 keys
  passed; the sheet's own tests: 54 passed; Ruff clean.
- Full suite: **39,894 passed, 13 skipped in 14m06s**.

### 2026-10-21 — TPhO 19 (2563) national physics olympiad

- Eight PDFs: three theory problems and the lab, each with its own solution
  (the four solutions `ignored`, used to confirm every answer). Clean text
  layers; the lab's part 3 formula was checked on the page image
  (T = 2μNW₁√(π/(4k))√d exp(k/d) + T₀).
- 20 items: 1.1 (strobe-lit drops: u′ = √(2gh)Δt/(T₀ + Δt),
  a′ = g(Δt/(T₀ + Δt))², A = d₀τ/(T₀²ω)), 1.2 (optical tweezer: δ, photon
  count, F_x, ω² = 4P(n − 1)/(mcRn)), 2 (lapse rates: T₁ = 5.95 °C,
  α = 9.78 K/km, z₁ = 1.44 km and z₂ = 2.90 km, T₂ = −1.7 °C, −5.2 °C/km),
  3 (lensing by Fermat's principle: y², β, the Einstein ring mass
  3.55×10⁴¹ kg), and the interleaved-notebook lab with synthetic data
  (μ from single pulls, the T–N slope and intercept, k and μ from the
  self-amplified pulls). 1.1 a), 1.2 c), 3.1 and the derivations share items.
- Readings: 2.8 reads β(T₂) off the paper's graph; the generated item uses a
  straight line through the solution's β(T₁) = 6.0×10⁻³ with the slope its
  answer implies (0.349×10⁻³ per °C), which reproduces −1.7 °C. The lab's
  part 2 slope in the solution is hand-drawn (0.863 N/sheet, μ = 0.57);
  least squares over the same N ≤ 8 points gives 0.935 (μ = 0.62) and
  T₀ = −0.385 N. The solution converts with 273 K (T₁ = 5.95 °C; 5.94 °C
  with 273.15).
- Independent checks include a two-flash fit for the strobe, the
  quarter-cycle flash sum, exact ray tracing through the sphere, a numerical
  restoring stiffness, integrated adiabatic climbs, a moist-ascent bisection
  and stepping, a golden-section Fermat minimum over the exact path, and
  centred least squares. `sheetpipe verify`: 20/20 green, 60 runs.
- Targeted run: 23,686 passed, 4 skipped; `test_per_set` for the 20 keys
  passed; the sheet's own tests: 45 passed; Ruff clean.
- Full suite: **40,185 passed, 13 skipped in 14m21s**.

### 2026-10-21 — TPhO 20 (2564) national physics olympiad

- Two PDFs, each with its solution bound in (theory 35 pages, lab 21);
  clean text layers.
- 29 items: 1 (rolling thin tube: a = ½g sin θ cos φ, μ ≥ ½tan θ√(1 +
  3sin²φ); loose half cylinder: a = ((m′ + m)/(2m′ + m))g sin θ and the
  tilt β; welded: θ_min = sin⁻¹(k′ sin θ₀) with θ₀ = tan(θ₀/2) = 2.33 rad,
  the kinetic energy, ω at the top and the normal force), 2 (vacuum diode:
  single-electron speed, the Child–Langmuir current, V ∝ x^{4/3}, the space
  charge and the anode charge), 3.1 (breathing: p_D, the work 2.7 J, 30.9
  kcal/day, ΔU = 22.1 J, Q = 24.8 J, the heat-to-work ratio), 3.2 (bilens:
  |v|, the image separation, L_max, fringe spacing λf/a, the most fringes),
  and the cantilever lab with synthetic data (E from the bare sag and from
  the Δy–m slope, the slope change e_N, E and the equivalent mass from
  vibration).
- Scheme notes: 2 g)'s first method gives σ₊ = −(4/3)ε₀V_d/d; its second
  method and neutrality give +, which the item uses (a test pins it). In
  3.1 the α values are graph readings; h)'s w_O = −1.94 J needs α_O ≈ 3.335
  L, and the tabulated 3.35 L gives −1.91 J and a ratio of 31 against 32.6
  (a test pins the sensitivity). The lab's part 1 slope is a drawn line
  (62 GPa; least squares 60.5); its part 3 line is the least-squares fit.
- Independent checks include a Cramer force–torque solve, energy for the
  loose half cylinder, a golden-section worst turn, inertia about the
  contact point, a finite-difference normal force, a stepped electron, a
  Poisson first-integral quadrature for the diode, sliced lung work, ray
  tracing and beam-overlap searches for the bilens, and centred least
  squares. `sheetpipe verify`: 29/29 green, 87 runs.
- Targeted run: 24,029 passed, 4 skipped; `test_per_set` for the 29 keys
  passed; the sheet's own tests: 63 passed; Ruff clean.
- Full suite: **40,602 passed, 13 skipped in 12m59s**.

### 2026-10-21 — TPhO 21 (2565) national physics olympiad

- Two PDFs, each with its solution bound in (theory 24 pages, lab 25);
  clean text layers apart from a few lost fraction slashes.
- 22 items: 1 (a charge in a dipole's field: the axial field, |E| at
  (r, θ), the circling charge's L_z with θ_c = 125.3°, the top speed and the
  swing period), 2 (magnetic cooling: M/(Nμ) = tanh x, S/(Nk_B), χ = Nμ²/k_BT,
  the neighbours' field B_L, T_f = (B_L/B_H)T_i, the heat Q/N), 3 (sonic
  flow: incompressible P₁, T₁ and P₁ from the Mach number, Q(β), the
  critical pressure and the choked flow), and the permanent-magnet lab with
  synthetic data (n and M from log B against log x, B₀ of an iron loop with
  an air gap, M from half-magnet flux, flux summed over rings).
- Scheme notes: 1 g)'s period is written 10.3/β, but its own approximation
  gives 10.44/β (exact 10.49/β); the item uses the paper's approximation and
  a test pins both. 2 i) and k) round 1.85 mT to 2 mT and 2.5×10⁻²⁴ J to
  3×10⁻²⁴ J. The lab's part 1 line is drawn (n = −2.86, M = 1.2×10⁶ A/m);
  least squares gives −2.90 and 1.08×10⁶ A/m. Its part 2 slope is the
  least-squares one.
- Generators: q09's r² slip now stays in the plain-number range (in nm), as
  the format guard otherwise redrew forever; the spin items use cold states
  so that tanh x and its linearisation stay apart.
- Independent checks include two-charge Coulomb sums, a bisected orbit
  angle, a velocity-Verlet swing, the exact period integral, Boltzmann
  weights, multinomial entropy via lgamma, an entropy-matching bisection,
  integrated B dM heat, an enthalpy bisection, a golden-section flow peak,
  the sonic state, and centred least squares. `sheetpipe verify`: 22/22
  green, 66 runs.
- Targeted run: 24,263 passed, 4 skipped; `test_per_set` for the 22 keys
  passed; the sheet's own tests: 49 passed; Ruff clean.
- Full suite: **40,921 passed, 13 skipped in 14m22s**.

### 2026-10-21 — POSN chemistry 2560, MC34–36

- Reviewed the p10 phase-change choices, NaCl lattice drawing, and Charles-law numbers; added independent solvers, three variants, generators and knowledge units for each.
- MC34's broad ionic/covalent vapor-pressure claim is expressed as a specific NaCl/iodine comparison in the adaptation. MC35's 14/13 visible-ion crop is identified as a finite drawing, not a formula unit. MC36 uses kelvin and reports 96.6 cm³.
- The paper remains partial at 36/70; the full suite is deferred until all 70 questions are digested, per the requested test cadence.
- Wave validation: 36/36 sheet solvers and 111 variants green, 807 knowledge units in 673 files with zero validation problems, source coverage 36/70. The focused sheet/set checks passed (248), followed by 37 rechecks after tightening independent verification. Registry, provenance, golden, layout and safety checks passed (16,355); Ruff and whitespace checks passed.

### 2026-10-21 — POSN chemistry 2560, MC37–39

- Reviewed p11 gas questions and added solvers, independent checks, three variants, generators, and knowledge units for each. MC37 chooses helium's highest-temperature/lowest-pressure condition; MC38 defines STP and uses absolute temperature; MC39 tests proportionality using kelvin.
- MC39 initially exposed a normalization mistake in the independent ideal-gas check and a choice-length cue. Both were corrected before acceptance; the choices now use equal-length statement labels.
- The paper remains partial at 39/70. The full suite stays deferred until all 70 questions are digested.
- Wave validation: 39/39 sheet solvers and 120 variants green; 810 knowledge units in 676 files with zero problems; source coverage 39/70. Focused sheet/set checks passed (267). Registry checks passed 16,366 cases and exposed one q37 safety-style issue; after replacing the method reference, the affected 41 checks and sheet verification passed. Ruff and whitespace checks passed.

### 2026-10-21 — POSN chemistry 2560, MC40–42

- Reviewed p11 gas-density, Graham-law, and Zn–Cu alloy questions. Added independently checked solvers, three variants, generators, and knowledge units for each.
- MC40 uses the printed STP convention 22.4 L/mol. MC41's equal-amount effusion times scale as sqrt(M). MC42 uses Zn=65.0 and Cl=35.5, giving 1.30 g Zn and 74.0% Cu.
- Wave validation: 42/42 sheet solvers and 129 variant checks green; 813 knowledge units in 679 files with zero problems; source coverage 42/70; focused sheet/set checks passed (286). The full suite remains deferred until the entire sheet is digested.
- Targeted registry, provenance, safety, golden and layout checks passed (16,379); Ruff and whitespace checks passed.

### 2026-10-21 — POSN chemistry 2560, MC43–45

- Reviewed the p11–p12 reactions, units and choices; added independently checked solvers, three variants, generators and knowledge units for each item.
- MC43 has two true printed answers: 0.36 kg C and 672 dm³ CO₂. Its adaptation asks for the pair of correct statements. MC44 gives 205 L CO₂ from 240 g LiOH at 500 K and 1 atm. MC45 identifies BaCO₃ from matching acid, gas and sample-mass data.
- The paper remains partial at 45/70; the full suite remains deferred until all 70 questions are digested.
- Wave validation: 45/45 sheet solvers and 138 variants green; 816 knowledge units in 682 files with zero validation problems; source coverage 45/70. Focused sheet/set checks passed (305), new-key provenance/safety/golden checks passed (12), curriculum/stage/layout/manifest checks passed (46), and Ruff and whitespace checks passed.

### 2026-10-21 — POSN chemistry 2560, MC46–48

- Reviewed p12 methanol, hydrate and sample-mass questions; added independently checked solvers, three variants, generators and knowledge units for each.
- MC46's CO is limiting and gives 400 g methanol. MC47 counts two H atoms per water molecule to get 1.57×10²⁴ H atoms. MC48 converts all three samples to grams, giving a > b > c.
- Wave validation so far: 48/48 sheet solvers and 147 variants green; 819 knowledge units in 685 files with zero problems; source coverage 48/70; focused sheet/set checks passed (324). The full suite remains deferred until the entire sheet is digested.
- New-key provenance/safety/golden checks passed (12); curriculum/stage/layout/manifest checks passed (46); Ruff and whitespace checks passed.

### 2026-10-21 — POSN chemistry 2560, MC49–51

- Reviewed p12–p13 hydrocarbon combustion, BaSO₄ precipitation, and Zn/HCl questions; added independent solvers, three variants, generators and knowledge units for each.
- MC49 gives C₄H₁₀ and 100 cm³ water vapor. MC50's printed “all sulfate precipitates” permits excess BaCl₂, so X=40 cm³ needs the exact-addition condition stated in the adaptation; BaSO₄ is 2.33 g and Na⁺ is 0.92% w/v under that condition. MC51 balances Zn+2HCl, giving 0.040 mol HCl consumed and 0.560 mol left, so printed claim c is false.
- Wave validation so far: 51/51 sheet solvers and 156 variants green; 822 knowledge units in 688 files with zero problems; source coverage 51/70; focused sheet/set checks passed (343). Full suite remains deferred until all 70 questions are digested.
- New-key provenance/safety/golden checks passed (12); curriculum/stage/layout/manifest checks passed (46); Ruff and whitespace checks passed.

### 2026-10-21 — POSN chemistry 2560, MC52–54

- Reviewed p13 product-yield, ammonia-decomposition, and hydrate-dilution questions; added independent solvers, three variants, generators and knowledge units for each.
- MC52 finds C's molar mass as 44 g/mol from the limiting reactant. MC53 gives a hydrogen mole fraction of 0.72. MC54 gives a 62.5 cm³ aliquot of MgCl₂ stock prepared from its hexahydrate.
- Wave validation: 54/54 sheet solvers and 165 variant runs green; 825 knowledge units in 691 files with zero problems; source coverage 54/70; focused sheet/set checks passed (362). The full suite remains deferred until the entire sheet is digested.
- New-key provenance/safety/golden checks passed (12); curriculum/stage/layout/manifest checks passed (46); Ruff and whitespace checks passed.

### 2026-10-21 — POSN chemistry 2560, MC55–57

- Reviewed p13–p14 solution-concentration questions, including MC57's printed mass table; added independent solvers, three variants, generators and knowledge units for each.
- MC55 converts 3.50 M H₂SO₄ at 1.20 g/cm³ to 4.08 mol/kg of water. MC56 gives 0.500 M NaClO after fourfold dilution. MC57 needs 0.505 g KNO₃ and 0.828 g Pb(NO₃)₂ for the specified mixed solution.
- Wave validation: 57/57 sheet solvers and 174 variant runs green; 828 knowledge units in 694 files with zero problems; source coverage 57/70; focused sheet/set checks passed (381). The full suite remains deferred until the entire sheet is digested.
- New-key provenance/safety/golden checks passed (12); curriculum/stage/layout/manifest checks passed (46); Ruff and whitespace checks passed.

### 2026-10-21 — POSN chemistry 2560, MC58–60

- Reviewed p14–p15 chloride-dilution, mixed CaCl₂ and colligative-property questions; added independently checked solvers, three variants, generators and knowledge units for each. This completes all 60 multiple-choice items; the ten written questions remain.
- MC58 needs 6 cm³ CdCl₂ stock plus 12 cm³ added water. MC59's final CaCl₂ mass concentration is 35.5 g/L. MC60's true printed statement is that A's boiling-point elevation exceeds C's by 0.199 °C; the adaptation asks for that value directly.
- Wave validation: 60/60 sheet solvers and 183 variant runs green; 831 knowledge units in 697 files with zero problems; source coverage 60/70; focused sheet/set checks passed (400). The full suite remains deferred until the ten written questions are digested.
- New-key provenance/safety/golden checks passed (12); curriculum/stage/layout/manifest checks passed (46); Ruff and whitespace checks passed.

### 2026-10-21 — POSN chemistry 2560, written 1–3 (internal 61–63)

- Reviewed p16's three written prompts and answer blanks; added paired-answer solvers, independent checks, three variants, generators and knowledge units for each.
- Written 1 gives neutral Ni as [Ar]3d8 4s2 and Cu⁺ as [Ar]3d10. Written 2 selects NaIO₄ with I at +7 and OF₂ with F at −1. Written 3 leaves 12.5 g I-131 after 16.2 days (two half-lives).
- Wave validation: 63/63 sheet solvers and 192 variant runs green; 834 knowledge units in 700 files with zero problems; source coverage 63/70; focused sheet/set checks passed (419). The full suite remains deferred until the seven remaining written questions are digested.
- New-key provenance/safety/golden checks passed (12); curriculum/stage/layout/manifest checks passed (46); Ruff and whitespace checks passed.

### 2026-10-21 — POSN chemistry 2560, written 4–6 (internal 64–66)

- Reviewed p17–p18 periodic-trend, Born–Haber and bond-energy questions; added independently checked solvers, three variants, generators and knowledge units for each.
- Written 4 gives G<E<D<A and basic oxides A₂E/DE (Na₂O/MgO). Its adaptation asks explicitly for basic oxides. Written 5 gives lattice *formation* enthalpy −2535 kJ/mol; its final source blank says MgF₂ despite abstract M/G in the data, so the adaptation uses MG₂. Written 6 finds both reactions exothermic with a 190 kJ per-mole-product enthalpy difference.
- Wave validation: 66/66 sheet solvers and 201 variant runs green; 837 knowledge units in 703 files with zero problems; source coverage 66/70; focused sheet/set checks passed (438). The full suite remains deferred until the four remaining written questions are digested.
- New-key provenance/safety/golden checks passed (12); curriculum/stage/layout/manifest checks passed (46); Ruff and whitespace checks passed.

### 2026-10-21 — POSN chemistry 2560, written 7–10 (internal 67–70)

- Reviewed p18–p19's final four written questions; added independently checked solvers, three variants, generators and knowledge units for each. This completes all 70 items.
- Written 7 gives 12.0 g D and 4.5 g E; written 8 gives C₃H₆O; written 9 needs 568 g Cl₂ and produces 1043 g KCl; written 10 gives 118 g/mol and 1.50 mol/kg. Written 9 says “four reactions” but prints three, and the adaptation states the three printed equations.
- Completion validation: 70/70 sheet solvers and 213 variant runs green; 841 knowledge units in 707 files with zero problems; source coverage 70/70. Focused sheet/set checks passed (201), bank checks passed (353), registry checks passed (588), and Ruff and whitespace checks passed. The bank entry is green.
- Completed-sheet full suite: 39,883 passed, 13 skipped, two PDF explorer tests errored at setup because the workspace sandbox denied a local HTTP-server socket bind. Those exact two tests passed when rerun with loopback access; no test assertion failed.

### 2026-10-21 — POSN chemistry 2561, MC1–3

- Created the next isolated worktree from the completed 2560 branch, fetched the 2561 paper, and extracted all 75 declared items. Visually reviewed p3 and implemented independently checked solvers, three variants, generators, and knowledge claims for the first three questions.
- The private digest records only short descriptions of these reviewed questions. The source MC3's stated count of five lines conflicts with its four labels; its adaptation explicitly says four.
- Wave validation: 3/3 sheet solvers and nine variants green; 843 knowledge units in 709 files with zero validation problems; the reviewed three source records are claimed. Focused generator/golden checks passed (46), sheet-pipeline checks passed (18), and registry/provenance/safety/layout checks passed (515). Ruff and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, MC4–6

- Reviewed the remaining p3 questions and added independent solvers, three variants, generators, and knowledge units. MC4's guaranteed second-shell count is clarified as an “always” statement; MC5 identifies fluorine. MC6's IE₂ order was checked against [NIST ASD](https://physics.nist.gov/cgi-bin/ASD/ie.pl?at_num_out=on&biblio=on&e_out=0&el_name_out=on&format=0&ion_charge_out=on&ion_conf_out=on&level_out=on&order=0&seq_out=on&shells_out=on&sp_name_out=on&spectra=H-Og+II&submit=Retrieve+Data&unc_out=on&units=1); K < Ca is false, while Se < Br is true.
- Wave validation: 6/6 sheet solvers and 18 variants green; 846 knowledge units in 712 files with zero validation problems; all six reviewed source records are claimed. Focused sheet/set checks passed (31), sheet-pipeline checks passed (33), and registry checks passed 526 cases. One q05 safety-style issue was corrected, then its affected safety check, solver-pool test, sheet verification, Ruff, and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, MC7–9

- Reviewed p4 and MC9's oxide-pair table. Added independent solvers, three variants, generators and knowledge claims for all three questions. MC7 gives the radius values explicitly because mixed atomic/ionic conventions vary. MC8 supplies empirical data and specifies grey As melting under pressure. MC9 pairs SO₃ and Na₂O.
- Wave validation: 9/9 sheet solvers and 27 variants green; 849 knowledge units in 715 files with zero validation problems; all nine reviewed source records are claimed. Focused sheet/set checks passed (37), sheet-pipeline checks passed (48), registry/provenance/safety/layout checks passed (539), and Ruff and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, MC10–12

- Reviewed p4 and added independent solvers, three variants, generators, and knowledge claims for all three questions. MC10 identifies MgI₂; MC11 identifies phosphorus; MC12 selects K₂Cr₂O₇ with FeCl₃. The source's Cl₂O distractor has concentration-dependent aqueous color, so the adaptation uses NaCl for a unique answer.
- Wave validation: 12/12 sheet solvers and 36 variants green; 852 knowledge units in 718 files with zero validation problems; all twelve reviewed source records are claimed. Focused sheet/set checks passed (36), sheet-pipeline checks passed (63), registry/provenance/safety/layout checks passed (551), and Ruff and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, MC13–15

- Reviewed p5 and MC13's two tables. Added independently checked solvers, three variants, generators, and knowledge claims. MC13 is restated as precipitation observations; MC14 separates coordination complexes from simple salts and oxides; MC15 explicitly labels β⁻ versus β⁺.
- Wave validation: 15/15 sheet solvers and 45 variants green; 855 knowledge units in 721 files with zero validation problems; all fifteen reviewed source records are claimed. Focused sheet/set checks passed (42), sheet-pipeline checks passed (78), registry/provenance/safety/layout checks passed (563), and Ruff and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, MC16–18

- Reviewed p5's four decay/growth graphs and p6's nuclear equations and oxide question. The adaptation expresses the four graphs as numerical values, without source artwork. Added independent solvers, three variants, generators and knowledge claims for all three questions.
- Wave validation: 18/18 sheet solvers and 54 variants green; 858 knowledge units in 724 files with zero validation problems; all eighteen reviewed source records are claimed. Focused sheet/set checks passed (48), sheet-pipeline checks passed (93), registry/provenance/safety/layout checks passed (575), and Ruff and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, MC19–21

- Reviewed p6 and MC21's bond-count table. Added independent solvers, three variants, generators and knowledge claims. MC20's printed intended equation is unbalanced; the adaptation repairs the missing coefficients on M and H₂O so exactly one equation is correct.
- Wave validation: 21/21 sheet solvers and 63 variants green; 861 knowledge units in 727 files with zero validation problems; all twenty-one reviewed source records are claimed. Focused sheet/set checks passed (74), sheet-pipeline checks passed (108), registry/provenance/safety/layout checks passed (587), and Ruff and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, MC37–39

- Reviewed p9 precipitation, alloy and acidic permanganate questions. Added independent solvers, three numerical variants, generators, named misconceptions and knowledge claims for each. MC37 states additive volumes; MC38 defines 0°C/1 atm as 22.4 L/mol; MC39 counts initial ferric ions and the five-to-one redox ratio.
- Wave validation: 39/39 sheet solvers and 117 variant runs green; 879 knowledge units in 745 files with zero validation problems; source coverage 39/39. Focused sheet/set checks passed (43), registry/provenance/safety/layout checks passed (659), and the partial-digest bank contract now passes. Ruff and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, MC40–42

- Reviewed p10 diborane yield, the two-stage azide/nitrate nitrogen production, and trona acid equivalents. Added independent solvers, three numerical variants, generators, named misconceptions and knowledge claims for each. MC41’s adaptation asks for one decimal because the printed R gives 49.54 g while the closest source choice is 49 g.
- Wave validation: 42/42 sheet solvers and 126 variant runs green; 882 knowledge units in 748 files with zero validation problems; source coverage 42/42. Focused sheet/set checks passed (46), registry/provenance/safety/layout checks passed (671), and the partial-digest bank check passed. Ruff and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, MC43–45

- Reviewed p10 superoxide oxygen production, acid identification from density and concentration, and sodium-ion concentration after mixing sulfate and phosphate. Added independent solvers, three numerical variants, generators, named misconceptions and knowledge claims for each. MC43 includes a CO₂-limited variant; MC44's variants identify all four candidate acids.
- Wave validation: 45/45 sheet solvers and 135 variant runs green; 885 knowledge units in 751 files with zero validation problems; source coverage 45/45. Focused sheet/set checks passed (49). Registry/provenance/safety/layout checks passed (683 total, with one q44 safety-style correction and affected recheck); the partial-digest bank check passed. Ruff and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, MC46–48

- Reviewed p11 chlorine generation from concentrated hydrochloric acid, acetic acid left after bicarbonate reaction, and a target hydroxide concentration made from ppm Ba(OH)₂ plus concentrated NaOH. Added independent solvers, three numerical variants, generators, named misconceptions and knowledge claims for each. MC46 explicitly asks for the mass of HCl solution.
- Wave validation: 48/48 sheet solvers and 144 variant runs green; 888 knowledge units in 754 files with zero validation problems; source coverage 48/48. Focused sheet/set checks passed (52), registry/provenance/safety/layout checks passed (695), and the partial-digest bank check passed. Ruff and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, MC49–51

- Reviewed p11–12 colligative-property questions. Added independent solvers, three numerical variants, generators, named misconceptions and knowledge claims for each. MC49 and MC51 explicitly assume nonvolatile, nondissociating solutes; MC50 transfers equal molality between two solvents.
- Wave validation: 51/51 sheet solvers and 153 variant runs green; 891 knowledge units in 757 files with zero validation problems; source coverage 51/51. Focused sheet/set checks passed (55), registry/provenance/safety/layout checks passed (707), and the partial-digest bank check passed. Ruff and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, MC52–54

- Reviewed p12 solid-bonding and vapor-pressure questions. Added independent solvers, three variants, generators, named misconceptions and knowledge claims. MC54 adapts the source graph as numerical vapor pressures, preserving A > B > C.
- Wave validation: 54/54 sheet solvers and 162 variant runs green; 894 knowledge units in 760 files with zero validation problems; source coverage 54/54. Focused generator tests passed (55), catalog checks passed (3), registry/provenance/safety/layout checks passed (719), and the partial-digest bank check passed. Ruff and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, MC55–57

- Reviewed p13 temperature/phase table, lotus-leaf wetting, and kinetic-gas statements. Added independent solvers, three variants, generators, named misconceptions and knowledge claims. MC56 specifies untreated clean glass for an unambiguous surface comparison.
- Wave validation: 57/57 sheet solvers and 171 variant runs green; 897 knowledge units in 763 files with zero validation problems; source coverage 57/57. Focused generator tests passed (58), catalog checks passed (3), registry/provenance/safety/layout checks passed (731), and the partial-digest bank check passed. Ruff and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, MC58–60

- Reviewed p13–14 gas density/diffusion, Boyle-law volume ratio and rising-bubble combined gas law. Added independent solvers, three variants, generators, named misconceptions and knowledge claims. MC59 has two equivalent printed options; the adaptation normalizes all choices to x:1 and removes the duplicate. Part I is now complete; fifteen written items remain.
- Wave validation: 60/60 sheet solvers and 180 variant runs green; 900 knowledge units in 766 files with zero validation problems; source coverage 60/60. Focused generator tests passed (61), catalog checks passed (3), registry/provenance/safety/layout checks passed (743), and the partial-digest bank check passed. Ruff and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, written 1–3 (items 61–63)

- Reviewed Zr ground-state configuration, periodic size/ionic formula from outer configurations, and the CH₂BrCl isotope fraction. Added independently checked solvers, three variants, generators, named misconceptions and knowledge claims. The Zr generator explicitly requests noble-gas shorthand; the symbolic question fixes n=3.
- Wave validation: 63/63 sheet solvers and 189 variant runs green; 903 knowledge units in 769 files with zero validation problems; source coverage 63/63. Focused generator tests passed (64), catalog checks passed (3), registry/provenance/safety/layout checks passed (755), and the partial-digest bank check passed. Ruff and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, written 4–9 (items 64–69)

- Reviewed six written questions covering Cr/Mn/Fe, Es synthesis and decay, a Born–Haber cycle, COF₂ Lewis structure, aluminium per pancake and phosphate back titration. Added independently checked solvers, three variants, generators, named misconceptions and knowledge claims. The COF₂ adaptation names dipole–dipole attraction as the strongest specific interaction while acknowledging dispersion.
- Wave validation: 69/69 sheet solvers and 207 variant runs green; 909 knowledge units in 775 files with zero validation problems; source coverage 69/69. Focused generator tests passed (70), new-set choice checks passed (6), registry/provenance/safety/layout checks passed (779), and the partial-digest bank check passed (2). Ruff and whitespace checks passed. The full suite remains deferred until 75/75.

### 2026-10-21 — POSN chemistry 2561, written 10–15 (items 70–75)

- Reviewed the final six written questions: C/H/Br empirical and molecular formulas, solvent evaporation from boiling elevation, mole fraction and molarity after dilution, vapor-pressure order, a heated oxygen cylinder, and Graham-law effusion. Added independent solvers, three variants, generators, named misconceptions and knowledge claims. The vapor-pressure adaptation specifies a common temperature where all four substances can be liquids; its order agrees with [NIST methane](https://webbook.nist.gov/cgi/cbook.cgi?ID=C74828&Type=TBOIL), [ethanol](https://webbook.nist.gov/cgi/cbook.cgi?ID=C64175&Type=TBOIL), [ethyl ether](https://webbook.nist.gov/cgi/cbook.cgi?ID=C60297&Type=TBOIL) and [silane](https://webbook.nist.gov/cgi/cbook.cgi?ID=C7803625&Mask=1E9F) phase data.
- Final validation: 75/75 solvers and 225 variant runs green, 915 knowledge units in 781 topic files with zero validation problems, and source coverage 75/75. Focused generator tests passed (76), new-set choice checks passed (6), registry/provenance/safety/layout checks passed after the q73 style correction (803 including the corrected case), and golden/layout checks passed (4613). The completed-sheet full suite passed: 40,866 passed, 13 skipped. Two older sheet-answer strings were adjusted to match solver precision; the PDF explorer tests were rerun with loopback socket access after the default sandbox denied binding. Ruff and whitespace checks passed. The bank entry is `green`.

### 2026-10-21 — POSN chemistry 2562, MC1–12

- Began a separate worktree from the completed 2561 branch. The public 2562 PDF matched the bank LFS pointer exactly (SHA-256 `bfbfed6dd6f66f523a4baf10c3c9359f5273e64d2337423b0dbafd17bf647a18`). Extracted 75/75 questions from 17 pages; reviewed the first twelve, including q12's table crop.
- Added twelve independent solvers, three variants each, twelve generators, named mistakes, knowledge claims and a private partial digest. Source q3's energy-level assumption is explicit in the generated version. Public metadata contains only reviewed paraphrases; unreviewed extracted text and stubs were removed.
- Targeted validation: 12/12 solver contracts green, 12/12 knowledge claims, 924 knowledge units with zero validation problems, per-set and sheetpipe checks passed, catalog/stage/safety/provenance/golden/layout checks passed after correcting one choice-length cue and the new curriculum filing. Ruff passed. Full suite deferred to sheet completion.

### 2026-11-15 — Entire bank organization and duplicate audit

- Organized source collections under `สนามสอบ/<venue>/` or `ระดับ/<level>/`,
  retaining source filenames and relative collection structure. Compatibility
  directory symlinks preserve old source and pipeline artifact paths.
- Updated bank index, sheet package source paths, knowledge claims, provenance,
  transcripts, digests, documentation and applicable tests. Existing 8,168 index
  records retained their stages, sheet IDs, item counts and stale flags.
- Audited all 8,734 source PDFs: 7,793 local files hashed with full SHA-256,
  plus 941 LFS placeholders compared using their content OIDs. Found 91 duplicate
  groups with 92 additional copies; retained all copies and marked duplicate_of.
- Added 609 missing index entries for LFS PDFs; probing awaits content download.
  Three generated output PDFs remain indexed as outputs.
- Validation: 39 targeted bank/transcript/answer-key tests passed, 2 skipped;
  all indexed PDF paths exist, sheet-package source references resolve,
  and all 7,668 Roonpii manifest paths match index entries.
- Detailed duplicate audit: private bank `_notes/BANK_DUPLICATES.json`.


### 2026-11-15 — Subject-first bank layout

- Applied the requested `[subject]/[exam venue or level]/` hierarchy to all
  8,734 source PDFs. Kept source collection subfolders and filenames where useful.
- Updated index paths, package sources, knowledge claims, provenance and mirrored
  transcript/digest/extraction locations, retaining compatibility aliases.
- Preserved every existing stage, sheet ID, item count and stale flag. Verified
  all indexed PDFs, answer-key and duplicate links, package references, and all
  7,668 Roonpii manifest paths. Scanner excludes file aliases.
- Targeted bank, transcript and answer-key tests: 40 passed, 2 skipped.
- Private migration map: `_notes/SUBJECT_ORGANIZATION.json`.


### 2026-11-15 — English folder names

Renamed subject, venue, level and collection folders to English and updated index and references. Preserved all 8,777 records and their digestion progress. All indexed source PDF folder names are free of Thai characters. Targeted tests: 40 passed, 2 skipped; Ruff and diff checks passed.


### 2026-11-15 — Consolidate duplicate sheets

- Verified full content hashes (or LFS OIDs) for 92 duplicate entries and consolidated them into canonical copies, preserving compatibility links and updating active path references. Kept removed records in the private deduplication audit.
- Retained all stages and question counts; 8,642 unique source PDFs remain: 8,308 new, 305 generated, 27 green, 2 ignored.
- Preserved local availability by populating 40 canonical LFS placeholders from the matching original download URLs, verifying full SHA-256 checksums. All 7,668 imported download records still resolve to local PDFs.
- Validation: no duplicate content hashes remain among source-PDF index entries; all aliases, indexed files and package references resolve. Targeted bank/transcript/answer-key tests: 40 passed, 2 skipped.


### 2026-11-15 — Migration review before publication

- Reviewed source-code changes: generator computations are unchanged; updated
  source paths and added alias-aware bank selection/fetching. Regression tests
  cover skipping aliases during scans and fetching canonical LFS content from
  legacy filenames and folder globs.
- Verified a clean bank checkout: every indexed path and import catalog path
  resolves; no broken aliases; all 8,645 regular PDF files are valid LFS pointers.
- Knowledge validation: 545 units in 411 topic files, zero problems.
- Full regression run: 36,794 passed, 9 skipped; one stale probability-folder
  prefix failed and two localhost tests were blocked by the sandbox. Corrected
  the prefix and remaining terminal directory references. Focused reruns:
  9,931 passed (bank, knowledge, provenance, golden draws); both server tests
  passed with localhost permission. Ruff and main-repository diff checks pass.
- Private bank commit: `2ec4942`, branch `chore/organize-sheet-bank`.


### 2026-11-15 — Remove legacy bank aliases

- Removed all 9,429 compatibility symlinks and empty intermediate folders.
  The bank root now exposes canonical subject folders plus supporting folders.
- Moved the import catalog to `_notes/roonpii/MANIFEST.json` and re-keyed its
  ignored metadata entry. Updated sheet notes, active manifests, skill examples,
  an administration helper and remaining abbreviated directory citations.
- Verified every indexed file, all 7,668 successful import records, all 27 sheet
  package sources, all digest sources and manifest-relative PDF filenames.
  Preserved every stage, sheet ID, item count and stale flag. All 19 distinct
  declared bank citations resolve. No duplicate PDFs or symlinks remain.
- Added an integration regression for canonical layout and metadata placement.
  Validation: 9,953 tests passed, 2 skipped; Ruff and main diff checks passed.
- Historical alias mappings remain in the private `_notes/ALIAS_REMOVAL.json`.
  Old source aliases are intentionally no longer supported; use canonical paths.

### 2026-11-16 — Primary 2 mathematics, text-layer-first batch

- Prioritized the thinnest school maths grade: ป.2 had 110 generators (ป.1 had 111). Selected two usable text PDFs: `mathematics/level/primary-2/4157-2-2564-1-3.pdf` and `mathematics/level/primary-2/4178-2-2567-2-3.pdf`.
- Extracted from their text layers, reviewed every exercise page and the answer tables visually, and used the existing transcript interchange route to convert 21 + 20 questions. No OCR, source PDF changes, or general splitter changes. Private extraction, independent SymPy checks for every answer, and review notes are under `_notes/primary-2-text-first/`.
- Idempotent public mapping: `docs/for_admin/sheet_digestion_primary2.py`. Eighteen Primary 2 knowledge units claim all 41 questions; existing generators are reused for covered skills. Nine contextual gaps add generators in existing addition/subtraction, multiplication, division, money and time unit files, all in application stage 3 with adapted provenance.
- New keys: `comparison_amount_p2`, `half_dozen_packs_p2`, `daily_total_weeks_p2`, `pack_price_irrelevant_p2`, `equal_packs_p2`, `payment_from_change_p2`, `purchase_from_change_p2`, `compare_sale_prices_p2`, `sum_durations_p2` (all `math.`).
- The two bank records progress `new → converted → extracted → generated`; 41/41 questions are claimed and every unit has a generator. This batch does not mark them green. Other bank entries and source paths stay unchanged.
- ป.2 maths now has 119 generators; ป.1 with 111 is the next thinnest school grade. Continue choosing usable text-layer sheets before scans within the priority grade.
- Validation: 21,909 passed, 9 skipped across the skill's integration checks, independent bank-maths solvers, safety/provenance, registry-wide golden draws, science filing, layout/count contracts and existing Primary 2 tests. The nine new sets also pass catalog checks on 300 seeds each. Every original golden record remains identical; only nine new keys are added. Ruff and whitespace checks pass. Existing PDF smoke-test warnings concern unavailable Thai glyphs in the test environment.

### 2026-11-16 — Primary 1 mathematics, next text-layer batch

- Continued with the thinnest school maths grade: ป.1 had 111 sets after the ป.2 batch reached 119. Read text-layer PDFs `mathematics/level/primary-1/3999-1-2564-1-3.pdf`, `4017-1-2567-2-3.pdf` and `4020-1-2567-2-3.pdf` (the latter two under the same directory).
- Reviewed every exercise page and printed key visually, extracted from the text layers, and converted 21 + 21 + 20 = 62 questions through the existing transcript interchange route. Cross-page and same-line choices were joined. Written-response problems stay one item each. No OCR or source PDF changes.
- Private extraction, review and independent SymPy verification for all 62 answers are in `_notes/primary-1-text-first/`. All 60 multiple-choice answers agree with their visually read printed keys; no source corrections were needed.
- `docs/for_admin/sheet_digestion_primary1.py` maps every item exactly once to 13 knowledge units. Reused existing generators for arithmetic, inverse comparisons and missing quantities. Added seven application-stage sets: `math.dozen_change_p1`, `math.equal_amount_total_p1`, `math.calendar_date_shift_p1`, `math.compare_spending_totals_p1`, `math.purchase_from_balance_p1`, `math.budget_conclusion_p1`, `math.length_comparison_statement_p1`.
- The three source records move to generated (21, 21, 20 items); all 62 questions are claimed and every unit has a generator. ป.1 now has 118 maths sets, compared with ป.2's 119. Continue selecting readable text-layer sheets in the thinnest grade; generated is distinct from green publication review.
- Validation: 21,942 passed, 9 skipped across the integration, independent bank-maths solvers, safety/provenance, golden draws, curriculum, filing and existing Primary 1 checks. The seven new sets separately pass 300-seed catalog checks. All 4,955 existing golden records remain identical. Ruff and whitespace checks pass. The mapping rerun is byte-for-byte idempotent and was checked to preserve additional sources and unrelated units. Existing PDF smoke-test warnings concern unavailable Thai glyphs in the test environment.

### 2026-11-16 — Further Primary 1 text-layer papers and comprehension

- Continued with ป.1 (118 maths sets versus ป.2's 119). Digested `mathematics/level/primary-1/3993-1-2564-2-3.pdf`, `4005-1-2565-2-3.pdf`, `4011-1-2565-1-3.pdf`, and `4021-1-2567-2-2.pdf` (all under the same directory): 21 + 21 + 21 + 20 = 83 questions.
- Used existing text layers; the comprehension paper's six figure-dependent questions received a sheet-transcriber pass plus independent parent visual review. All diagrams are described and flagged in the private transcript. Objective codes are not used as exam identity tags. No OCR or PDF changes.
- Independently checked all 83 answers and all 80 MC key positions. Corrected one final-line unit typo in 4005's written answer: 53 − 42 is 11 pencils (แท่ง), whereas the key prints ปี. The correction is documented privately; source PDF bytes stay unchanged.
- `docs/for_admin/sheet_digestion_primary1_batch2.py` appends coverage to existing units, adds 13 units and accounts for all 83 items. Existing generators cover most skills, including every ordinary arithmetic item in 4011. Four actual gaps add `math.multi_dozen_total_p1`, `math.story_matches_sentence_p1`, `math.equivalent_number_forms_p1`, and `math.compare_sums_p1` in their existing unit files, with application-stage placement and adapted provenance.
- Both Primary 1 mapping scripts rerun idempotently and preserve earlier/later source claims. The four source records move to generated (21, 21, 21, 20 items); all units have generators. Generated remains separate from green publication review.
- ป.1 maths now has 122 generators. Next priority: ป.2 with 119, followed by ป.5 with 120. Across these three batches: 20 new generators, nine papers and 186 digested questions.
- Validation: 21,961 passed, 9 skipped across the integration suite, independent bank-maths checks, safety/provenance, golden draws, curriculum/filing contracts and existing Primary 1 tests. Four new sets separately pass 300-seed catalog checks and seven independent tests. All 4,962 earlier golden records are identical; four are added. Ruff and whitespace checks pass. Existing PDF smoke-test warnings concern unavailable Thai glyphs in the test environment.

### 2026-11-16 — Primary 2 division, mixed operations and pictograms

- Returned to ป.2, then thinnest at 119 maths sets. Digested text-layer PDFs `mathematics/level/primary-2/4163-2-2565-2-3.pdf` and `4175-2-2567-2-3.pdf` (same directory). Both received sheet-transcriber reads and independent parent review of every page, printed key and pictogram symbol.
- 4163 has 20 MC items plus five independent written-chart subquestions → 25 digest items. 4175 has 20 MC plus one written item → 21. Total: 46 atomic items from 42 top-level questions. All 40 MC answers match printed keys; all 46 answers are independently verified and every chart dependency is retained.
- Private review and repeatable checks are under `_notes/primary-2-text-first-batch2/`. Recorded source ambiguities about complete groups versus containers, the robust ordering of 4175 Q15 under alternative interpretations, and the cupcake-unit typo in Q19. New generators use unambiguous wording; source PDF bytes stay unchanged.
- `docs/for_admin/sheet_digestion_primary2_batch2.py` appends to existing coverage, adds 20 knowledge units and maps all 46 items. Reused existing generators for skills already covered. Nine gaps add `math.unit_price_p2`, `math.quotient_remainder_story_p2`, `math.least_remainder_p2`, `math.days_to_weeks_p2`, `math.remaining_two_step_p2`, `math.grouped_sales_p2`, `math.two_purchase_total_p2`, `math.pictograph_selected_total_p2`, and `math.pictograph_matching_rows_p2` in existing curriculum files.
- The original Primary 2 mapping now uses the preserving administrative upsert, generalized with a grade argument while keeping the Primary 1 default. All four Primary 1/2 mapping scripts rerun byte-for-byte idempotently and preserve earlier/later claims.
- Both source records reach generated, with 25 and 21 items; generated remains separate from green review. ป.2 now has 128 maths sets. Next: ป.5 at 120, then ป.1 at 122. Across four batches: 29 new generators, 11 papers and 232 digest items.
- Validation: 21,997 passed, 9 skipped across integration, independent bank-maths checks, safety/provenance, golden draws, curriculum/filing contracts and existing Primary 2 tests. New sets also pass catalog checks and 12 independent tests, including both compound-story variants and a sampler case with too few distinct remainders. All 4,966 existing golden records remain identical; nine are added. Ruff and whitespace checks pass. Existing PDF smoke-test warnings concern unavailable Thai glyphs in the test environment.

### 2026-11-16 — Primary 5 geometry, percentages and proportion

- Continued with ป.5, then thinnest at 120 maths sets. Digested text-layer PDFs `mathematics/level/primary-5/4703-5-2564-1-3.pdf` and `4721-5-2567-2-3.pdf` (same directory), 22 questions each. Sheet-transcriber reads were followed by parent review of every exercise/key page, the geometry diagram and complete score table.
- All 44 answers and all 40 MC positions agree with exact independent checks. Retained the outside-height geometry diagram and inclusive score boundary (45 out of 50 passes 90%). Documented the savings question's unspecified interest timing and the printed key's school model; the adapted generator instead states a year-end bonus explicitly. Private review and repeatable checks: `_notes/primary-5-text-first/`.
- `docs/for_admin/sheet_digestion_primary5.py` maps all 44 items exactly once to 21 units. Reused existing sets for skills already covered. Ten application-stage additions: `math.quadrilateral_repetition_p5`, `math.related_quad_dimensions_p5`, `math.parallelogram_land_area_p5`, `math.square_area_from_perimeter_p5`, `math.percent_pass_table_p5`, `math.monthly_savings_bonus_p5`, `math.percent_share_difference_p5`, `math.percent_remainder_share_p5`, `math.fractional_unit_price_p5`, `math.proportional_reward_difference_p5`.
- Decimal dimensions use integer tenths/hundredths; money uses integer satang or exact Fraction/Decimal. Independent tests read visible questions and use polygon area, expanded boundary sums, inverse equations and rational cross multiplication, including the inclusive threshold and early-rounding trap.
- Both records reach generated with 22 items, separate from green review. All five Primary 1/2/5 coverage scripts rerun byte-for-byte idempotently and preserve prior/later claims. No PDF, source path or LFS changes.
- ป.5 maths now has 130 sets. Next priority: ป.1 with 122, then ป.2 with 128. Across five batches: 39 new generators, 13 papers and 276 digest items.
- Validation: 22,047 passed, 9 skipped across integration, independent bank-maths tests, safety/provenance, golden draws, curriculum/filing contracts and existing Primary 5/6 checks. New sets separately pass catalog checks and 12 independent tests. All 4,975 pre-existing golden records remain identical; ten are added. Ruff and whitespace checks pass. Existing PDF smoke-test warnings concern unavailable Thai glyphs in the test environment.

### 2026-11-16 — Primary 1 measurement comprehension

- Returned to ป.1, thinnest at 122 maths sets. Digested readable-text PDF `mathematics/level/primary-1/4018-1-2567-2-2.pdf`: 20 MC items. Transcript review includes every exercise page, the printed key, both scale readings, balanced and tilted pans, and both pictograms. All answers agree with the key; no unresolved issues.
- `docs/for_admin/sheet_digestion_primary1_batch3.py` maps every item exactly once, appending to earlier source claims. Eleven added knowledge units cover measurement, place value and chart skills. Reused existing generators, explicitly linking the 130 expanded-form question to the existing Primary 2 set and the original dial diagrams to the existing picture-scale set.
- Three new application sets in the existing Primary 1 measurement module: `math.measuring_tool_p1`, `math.weight_difference_pairs_p1`, `math.scale_kg_khit_p1`. Tool requirements specify flexibility and the shortest rigid instrument usable in one placement; pair-gap questions normalize kg/khit with unique differences; scale choices normalize the 10-khit boundary and remove midpoint collisions.
- The source reaches generated with 20 items, separate from green review. All six coverage scripts rerun byte-for-byte idempotently; no earlier claims are lost. Private review and repeatable checks are under `_notes/primary-1-text-first-batch3/`. No source PDFs or canonical paths changed.
- ป.1 now has 125 maths sets and remains thinnest; next is ป.2 at 128. Across six batches: 42 new generators, 14 papers and 296 digest items.
- Validation: 22,056 passed, 9 skipped across integration, independent bank-maths tests, safety/provenance, golden draws, curriculum/filing contracts and existing Primary 1 checks. New sets separately pass 300-seed catalog checks and five independent tests, including exhaustive scale-parameter choice checks. All 4,985 earlier golden records remain identical; three are added. Ruff and whitespace checks pass. Existing PDF smoke-test warnings concern unavailable Thai glyphs in the test environment.

### 2026-11-16 — Primary 1 arithmetic equivalence

- Continued with ป.1, thinnest at 125 maths sets. Digested readable-text PDF `mathematics/level/primary-1/4019-1-2567-2-1.pdf`: 20 MC items, no figures. Reviewed every exercise page and the fourth-page key, retaining Q15's last choice across the page break. All 20 answers and key positions independently verified with SymPy; no discrepancies.
- `docs/for_admin/sheet_digestion_primary1_batch4.py` claims all 20 items exactly once across nine new units. Existing arithmetic, missing-addend/subtrahend and successive-subtraction sets cover twelve items. Four uncovered forms add `math.equal_sums_missing_p1`, `math.match_sum_expression_p1`, `math.missing_minuend_p1`, and `math.match_difference_expression_p1` in their existing addition/subtraction modules.
- New questions include reversed equalities, blanks in each sum position and both numeric/expression references. Equal-sum draws go beyond the existing commutative identity; matching expressions use different operands from the reference. Distractors represent incorrect inverses, copying operands and unit/ten errors. Independent tests re-solve visible questions by enumerating integer candidates or counting signed unit tokens.
- The source reaches generated with 20 items, separate from green review. All seven coverage scripts rerun byte-for-byte idempotently; all prior claims remain intact. Private verification and source records are under `_notes/primary-1-text-first-batch4/`. No PDFs or canonical paths changed.
- ป.1 now has 129 maths sets. Next priority: ป.2 with 128. Across seven batches: 46 new generators, 15 papers and 316 digest items.
- Validation: 22,073 passed, 9 skipped across integration, independent bank-maths tests, safety/provenance, golden draws, curriculum/filing contracts and existing Primary 1 checks. Four new sets separately pass 300-seed catalog checks and five independent tests. All 4,988 earlier golden records remain identical; four are added. Ruff and whitespace checks pass. Existing PDF smoke-test warnings concern unavailable Thai glyphs in the test environment.

### 2026-11-16 — Primary 2 place-value differences and ordering

- Continued with ป.2, thinnest at 128 maths sets. Digested readable-text PDF `mathematics/level/primary-2/4179-2-2567-2-2.pdf`: 20 MC questions. Transcriber and parent reviewed all six pages, both abaci, underlined digit, concave polygon, solid diagrams and printed key. All 20 answers agree; Q20 choices spanning pages 4–5 remain attached to Q20.
- `docs/for_admin/sheet_digestion_primary2_batch3.py` maps every item exactly once to ten units. Existing generators cover reading/expansion, comparison (including expanded sums), ordering, polygons and solids; the object-shape recognition question reuses the existing Primary 1 set. Two gaps add `math.digit_value_difference_p2` and `math.number_between_bounds_p2` to the existing Primary 2 numbers module and application stage.
- Independent tests read visible questions, expand positional values as groups, and validate every offered choice against both strict bounds. Fixed a multiple-correct-option issue caught in testing: the bounds question uses an explicit label pool so generic numeric neighbors cannot introduce other valid interior numbers. Covers reversed order, equal digits at different positions, zero contributions and endpoints.
- The source reaches generated with 20 items, separate from green review. All eight administrative coverage scripts rerun byte-for-byte idempotently and preserve prior claims. Private review and repeatable checks: `_notes/primary-2-text-first-batch3/`. No source PDFs or canonical paths changed.
- ป.2 now has 130 maths sets; next priority is ป.1 at 129. Across eight batches: 48 new generators, 16 papers and 336 digest items.
- Validation: 22,080 passed, 9 skipped across integration, independent bank-maths tests, safety/provenance, golden draws, curriculum/filing contracts and existing Primary 2 checks. Two new sets separately pass 300-seed catalog checks and four independent tests. All 4,992 earlier golden records remain identical; two are added. Ruff and whitespace checks pass. Existing PDF smoke-test warnings concern unavailable Thai glyphs in the test environment.

### 2026-11-16 — Primary 1 closest weights and incorrect comparisons

- Continued with ป.1, thinnest at 129 maths sets. Digested readable-text PDF `mathematics/level/primary-1/4006-1-2565-2-2.pdf`: 20 MC questions. Transcriber and parent reviewed every page, every figure and the shaded key on page 5 (which lacks a text layer). All twenty answers agree with the key.
- Q3 omits the direction of ordering; retained the original stem and annotated its intended descending order. Every chart row and scale is preserved, including Q12's different dial capacities and Q20's row-by-row counts 8,7,9,10,7. Parent zoom review confirms seven roundabouts; the asked swing-minus-spring difference is one. No source PDF or canonical path changed.
- `docs/for_admin/sheet_digestion_primary1_batch5.py` maps all twenty items exactly once, appending to earlier units and adding three knowledge units. Existing generators cover most skills and both charts. Two gaps add `math.closest_weight_pair_p1` and `math.false_sum_comparison_p1` in their existing measurement/comparison modules and application stages.
- Independent tests normalize weights to grams to check the uniquely closest pair, and count unit tokens to re-evaluate every offered comparison. All four operators can carry the false statement. The source reaches generated with twenty items, separate from green review. All nine mapping scripts rerun byte-for-byte idempotently; earlier claims are preserved. Private review and repeatable checks: `_notes/primary-1-text-first-batch5/`.
- ป.1 now has 131 maths sets. ป.2, ป.3, ป.4, ป.5 and ม.3 are tied at 130. Across nine batches: 50 new generators, 17 papers and 356 digest items.
- Validation: 22,093 passed, 9 skipped across integration, independent bank-maths tests, safety/provenance, golden draws, curriculum/filing contracts and existing Primary 1 checks. Two new sets separately pass 300-seed catalog checks and four independent tests. All 4,994 earlier golden records remain identical; two are added. Ruff and whitespace checks pass. Existing PDF smoke-test warnings concern unavailable Thai glyphs in the test environment.

### 2026-11-16 — Primary 3 money and inverse word problems

- Continued with ป.3, one of the thinnest maths grades at 130 sets. Digested readable-text PDF `mathematics/level/primary-3/4357-3-2567-2-3.pdf`: 20 MC plus two written responses, 22 atomic items. Reviewed all four pages and the complete printed MC key; every MC answer matches. Independently computed written answers: 970 baht and 40 students. Written scaffolds remain one item each, with original numbering and global digest positions 21–22.
- `docs/for_admin/sheet_digestion_primary3.py` maps all 22 items exactly once to sixteen units. Reused existing multiplication, division, baht/satang addition, change and multi-step generators. Four gaps add `math.half_then_daily_budget_p3`, `math.resale_profit_unit_price_p3`, `math.unit_price_from_balance_p3`, and `math.buy_several_satang_p3` in the existing money/multi-step modules and application stages.
- Prices with satang use integer-satang arithmetic and normalized units. Independent tests reconstruct spending and balances, enumerate selling prices satisfying total-profit constraints, and use Decimal repeated addition to check price multiplication. Explicitly cover all satang residues, including whole-baht results, and cost/profit inputs that individually have remainders but sum to an exactly divisible revenue. Source exact values and all choices are independently checked with SymPy rationals.
- The source reaches generated with 22 items, separate from green review. All ten mapping scripts rerun byte-for-byte idempotently; prior coverage remains intact. Private review and repeatable checks: `_notes/primary-3-text-first/`. No source PDF or canonical path changed.
- ป.3 now has 134 maths sets. Next thinnest: ป.2, ป.4, ป.5 and ม.3, tied at 130. Across ten batches: 54 new generators, 18 papers and 378 digest items. The full catalog now has 5,000 registered sets.
- Validation: broad integration run passed 22,106 tests with 9 skipped, including independent bank-maths, safety/provenance, golden draws, curriculum/filing contracts and existing Primary 3 tests. Final source review expanded resale draws so cost and total profit need not individually divide exactly; the combined revenue still does. After that final change, 21 focused checks (including all new sets, the remainder-specific independent test, provenance and safety) and 5,052 registry-wide checks pass. All 4,996 earlier golden records remain identical; four are added. Ruff and whitespace checks pass. Existing PDF smoke-test warnings concern unavailable Thai glyphs in the test environment.

### 2026-11-16 — Eleven-set batch for thin Primary 4/5 maths grades

- User changed the cadence: implement about ten generators, then test and report together. This combined batch adds six ป.4 and five ป.5 sets from readable-text sources `mathematics/level/primary-4/4539-4-2567-2-3.pdf` and `mathematics/level/primary-5/4724-5-2567-2-3.pdf`: 22 and 20 questions respectively. Transcribers and parent reviewed every page; all 42 answers are independently verified.
- Primary 4 Q19 has a printed-key error: the organizer and 24 friends total 25 people, so (28,750 + 49,250)/25 = 3,120 baht, choice ก. The printed ง.3,250 divides by 24 and forgets the organizer. Preserve the original stem/choices and annotate the correction privately. All other MC answers agree with printed keys. Written answers are 2h55m and 394,000 baht. Primary 5 source wording issues (canal-name change and missing กี่) are retained with notes.
- `docs/for_admin/sheet_digestion_thin_batch11.py` maps every item exactly once across 32 new units, reusing existing generators for covered skills. Added Primary 4: `math.age_year_month_difference_p4`, `math.monthly_reading_duration_p4`, `math.average_task_duration_p4`, `math.repeated_seconds_duration_p4`, `math.reserve_half_remaining_p4`, `math.organizer_shared_cost_p4`. Added Primary 5: `math.reserve_fraction_daily_budget_p5`, `math.equal_pieces_cm_to_mm_p5`, `math.two_cuts_metres_to_cm_p5`, `math.mixed_weight_remaining_kg_p5`, `math.price_per_khit_from_grams_p5`.
- All additions are applications in existing unit files. Independent tests read visible content, use calendar.monthrange, walk month intervals, reconstruct inverse equations and use exact Decimal/Fraction units. Cover all twelve months, year/month borrowing, sequential charging, strict inclusion of the organizer and all conversion factors. All eleven coverage scripts rerun byte-for-byte idempotently and preserve earlier claims.
- Both sources reach generated with 22/20 items, separate from green review. Private source audits: `_notes/thin-maths-batch11/`. No PDFs, source paths or LFS objects changed. ป.4 increases 130→136 and ป.5 130→135. Next thinnest: ป.2 and ม.3 at 130. Across this continuation: 65 new generators, 20 papers and 420 digest items; catalog total 5,011 sets.
- Validation: all 25 focused checks pass, including 300-seed catalog checks for all eleven additions and independent visible-content solvers. One combined integration run for both completed papers passed 22,218 tests with 9 skipped, covering bank-maths, provenance/safety, golden draws, curriculum/stage/filing contracts and existing Primary 4/5/6 checks. All 5,000 earlier golden records are identical; eleven are added. Ruff and whitespace checks pass. Existing PDF smoke-test warnings concern unavailable Thai glyphs in the test environment.

### 2026-11-16 — Twelve-set Primary 2 / Secondary 3 batch

- Continued the roughly ten-set testing/report cadence with the thinnest maths grades, ป.2 and ม.3, both at 130. Digested readable-text PDFs `mathematics/level/primary-2/4176-2-2567-2-2.pdf` (20 MC) and `mathematics/level/secondary-3/5202-3-2567-2.pdf` (40 MC). Transcribers and parent read every page, graph, circle/solid diagram, pictogram and printed key. Source computations agree with all sixty intended key positions under the documented caveats.
- Source caveats retained privately: Primary 2 Q11 calls for an instrument but prints ลิตร. Secondary 3 Q17/19 require care about hypotheses/universal claims; Q18/20 contain two mathematically true statements, with the named theorem supplying the intended key; Q26 relies on implicit regularity; Q30's square base follows from equal-sided cyclic-base assumptions; Q31/32 omit π and the key uses 22/7. These are source quality flags, separate from coverage. New generators state their conditions and do not copy ambiguous prompts unchanged.
- `docs/for_admin/sheet_digestion_p2_m3_batch12.py` claims all sixty items exactly once, adding 39 units and appending two existing chart units. Reused covered generators. Added Primary 2: `math.mixed_length_statement_p2`, `math.capacity_litre_ml_comparison_p2`. Added Secondary 3: `math.system_solution_count_m3`, `math.system_basket_target_m3`, `math.two_rate_allocation_m3`, `math.pyramid_surface_from_edge_m3`, `math.cone_volume_from_slant_m3`, `math.hemisphere_from_sphere_area_m3`, `math.hemisphere_radius_from_volume_m3`, `math.square_pyramid_volume_from_slant_m3`, `math.equilateral_pyramid_base_from_volume_m3`, `math.tangent_chord_angle_m3`.
- Independent tests use matrix ranks, price enumeration, exact inverse balances, Heron face area, height enumeration, hemisphere integration and unit-circle dot products. π and rounding conventions are explicit; Fraction and Decimal avoid binary floating-point answers. New pyramid tests also verify that real solids with the stated dimensions exist.
- Both records reach generated with 20/40 items, separate from green review; flagged source questions remain available for a quality pass. All twelve coverage scripts rerun byte-for-byte idempotently and preserve prior claims. Private review/repeatable checks: `_notes/p2-m3-batch12/`. No PDF bytes, source paths or LFS objects changed.
- ป.2 increases 130→132; ม.3 increases 130→140. Next thinnest: ป.1 with 131 sets. Across this continuation: 77 new generators, 22 papers and 480 digest items; full catalog 5,023 sets.
- Validation: all 26 focused checks pass, including 300-seed catalog checks for all twelve additions and independent visible-content solvers. One combined integration run for both completed papers passed 22,219 tests with 9 skipped, covering bank-maths, provenance/safety, golden draws, curriculum/stage/filing contracts and existing Primary 2 / Secondary 3 checks. All 5,011 earlier golden records are identical; twelve are added. Ruff and whitespace checks pass. Existing PDF smoke-test warnings concern unavailable Thai glyphs in the test environment.

### 2026-11-16 — Thirteen-set Primary 1–3 comprehension batch

- Continued the requested cadence of about ten additions before combined checks/reporting, starting with the thinnest grade, ป.1 (131). Completed readable-text papers `mathematics/level/primary-1/3994-1-2564-2-2.pdf`, `mathematics/level/primary-2/4158-2-2564-1-2.pdf` and `mathematics/level/primary-3/4358-3-2567-2-2.pdf`: twenty MC questions each. A final coverage pass found the daily-activity skill, bringing the batch from twelve to thirteen additions.
- Transcribers reviewed all exercise/key pages; parent reviewed all seventeen rendered pages, including clocks, scales, balances, patterns, every denomination, all eight ledger rows, and image-only shaded keys. Sixty intended answers agree with independent exact computations. P1 Q15's `40 = 20 + 20` is true arithmetic but not canonical tens/ones expanded form; the transcript flags this distinction and the new generator states it explicitly. Objectives remain parenthesized metadata; school instructions are comments. No PDF bytes or canonical paths changed.
- `docs/for_admin/sheet_digestion_primary123_batch13.py` claims all sixty items exactly once, appending sources to existing units and adding nineteen units. All thirteen coverage scripts rerun byte-for-byte idempotently. The three records reach generated with twenty items each, separate from green publication review. Private source review and repeatable computations: `_notes/primary123-batch13/`.
- Added ป.1: `math.expanded_form_judgement_p1`, `math.place_value_statement_p1`, `math.length_order_names_p1`. Added ป.2: `math.colloquial_clock_p2`, `math.clock_hands_from_hour_p2`, `math.clock_period_to_24h_p2`, `math.calendar_event_month_p2`, `math.daily_schedule_activity_p2`, `math.pattern_changing_attribute_p2`. Added ป.3: `math.money_purse_comparison_p3`, `math.money_odd_purse_p3`, `math.satang_ledger_query_p3`, `math.purchase_sentence_models_p3`. Reused existing generators for ordinary counting, comparisons, shapes, charts and arithmetic patterns. Every addition is in an existing curriculum unit module and application stage.
- Independent visible-content tests use digit strings, clock angles, datetime, Decimal repeated sums, frequency counting and SymPy expression evaluation. They test every time/lookup/ledger/model branch, all twenty-four whole hours and every offered statement/expression where alternative valid choices could occur. New time stems state periods precisely; activity questions provide an explicit daily schedule; money uses exact integer satang.
- Counts: ป.1 131→134, ป.2 132→138, ป.3 134→138. Next thinnest: ป.1 (134), then ป.5 (135) and ป.4 (136). Across this continuation: ninety new generators, twenty-five papers, 540 digest items; full catalog 5,036 sets. Knowledge validation reports 769 units across 447 topic files, zero problems. All 8,685 bank records remain present; only the three selected records gain item counts and generated stages. All 5,023 earlier golden records, seed lists and retirement state are preserved.
- Validation: all 26 focused checks pass, including independent solvers and 300-seed catalog checks for thirteen additions. One combined run for all three completed papers passed 22,383 tests, 9 skipped, in 210.96 seconds, covering integration, bank maths, provenance/safety, every golden draw, curriculum/stage/filing contracts and existing Primary 1–3 tests. Ruff and whitespace checks pass. The 33 PDF smoke-test warnings concern pre-existing missing Thai glyphs in the test font.

### 2026-11-16 — Twelve Primary 1 reasoning sets from a complete text-layer paper

- Continued with ป.1, thinnest at 134 maths sets, using readable-text `mathematics/level/primary-1/10257-LPMC-Math-G1-No26-2568.pdf`. This Primary 1 competition source has thirty questions on PDF pages 2–13 and no printed key. A transcriber and parent reviewed all thirteen pages, every option and every figure. Thirty answers are independently computed; no material is omitted and PDF bytes/path are unchanged.
- Source interpretation notes remain private: Q6 intends three positive allocations but allows seven if zero shares are admitted; Q17 has three globally possible rankings but only one printed valid choice; Q22 intends four per small square rather than shared-edge counting; Q30 follows the conventional constant/steadily increasing difference rules. New prompts explicitly require positive shares, ask to select a compatible ranking and make segment/path data visible. No green publication status is asserted.
- `docs/for_admin/sheet_digestion_primary1_reasoning12.py` claims all thirty items once across 29 units. Existing generators cover the other arithmetic, pack-price, equal-cell counting, shape and pattern procedures; the second-difference procedure reuses the existing general sequence generator. All fourteen coverage scripts rerun byte-for-byte idempotently and preserve earlier claims. Knowledge validation reports 798 units across 448 topic files and zero problems. The source reaches generated with thirty items, separate from quality review. Source computations and parent review: `_notes/primary1-reasoning12/`.
- Added `math.block_rotation_p1`, `math.ordered_sharing_p1`, `math.grid_relative_position_p1`, `math.pair_absence_p1`, `math.balance_ball_swaps_p1`, `math.overlap_circle_sums_p1`, `math.race_constraints_p1`, `math.seven_segment_removal_p1`, `math.grid_path_check_p1`, `math.digit_clues_p1`, `math.knockout_matches_p1`, `math.reverse_double_balance_p1`. Each lives in its existing curriculum unit module and application stage. The position generator retains the original front/back and left/right inequalities, including the requirement for people on all four sides.
- Independent visible-content tests use gcd, combinations, numbered-grid reconstruction, legal-swap BFS, exhaustive circle/digit solutions, all race permutations, segment-set subtraction, path endpoints, round-by-round tournament simulation and forward balance enumeration. The grid covers all sixteen combinations of 4/5 rows, 4/5 columns and two inequality directions. Source checks use exact SymPy and explicit figure matrices/paths. Initial checks caught coinciding grid distractors; the final source-faithful inequality model has three distinct reflected-position distractors.
- ป.1 increases 134→146. Next thinnest: ป.5 (135), then ป.4 (136), then ป.2/ป.3 (138). Across this continuation: 102 new generators, twenty-six papers and 570 digest items; full catalog 5,048 sets. All 5,036 earlier golden records, seed lists and retirement state are unchanged. All 8,685 bank records remain present; only this source gains item/stage fields.
- Validation: final focused checks pass all 24 tests, including independent answers and 300-seed catalog checks for twelve additions. One combined integration run passed 22,309 tests, 9 skipped, in 208.37 seconds, including bank maths, provenance/safety, every golden draw, curriculum/stage/filing contracts and existing Primary 1 checks. Ruff and whitespace checks pass. The 33 PDF smoke-test warnings are pre-existing missing Thai glyphs in the test font.

### 2026-11-16 — Ten Primary 5 proportion, percent and chart models

- Continued with ป.5, thinnest at 135 maths sets, using readable-text `mathematics/level/primary-5/4722-5-2567-2-2.pdf`: twenty MC questions. A transcriber and parent reviewed all six pages, every fraction expression, both complete graphs and the printed key. All twenty answers independently agree with the key. PDF bytes/path and earlier references are unchanged.
- Source exact values are preserved: Q3 325/8 minutes, Q11 340/9 percent, Q13 280/11 percent and Q16 3540000/89 baht. Q16 gives no rounding rule, so retain its exact expression. Source wrong options repeat numeric values in Q1/4/12/14; private transcript preserves them, while new generators offer four mathematically distinct values. Bars male 45,23,19,56 and female 22,33,27,14; temperatures 26,24,26,29,30 at 02/04/06/08/10. Every chart value is retained; new prompts provide labelled data tables.
- `docs/for_admin/sheet_digestion_primary5_models10.py` maps all twenty questions once, appending existing units and adding ten units. All fifteen coverage scripts rerun byte-for-byte idempotently. Knowledge validation: 808 units across 449 topic files, zero problems. The source reaches generated with twenty items, separate from green publication review. Private source verification and parent notes: `_notes/primary5-models10/`.
- Added `math.proportion_sentence_p5`, `math.fraction_decimal_to_percent_p5`, `math.percent_expression_comparison_p5`, `math.percent_part_sentence_p5`, `math.percent_remainder_sentence_p5`, `math.profit_sale_sentence_p5`, `math.profit_rate_sentence_p5`, `math.original_from_discount_sentence_p5`, `math.cost_from_loss_sentence_p5`, `math.double_bar_summary_p5`. All are in existing unit modules and application stage. Existing generators cover part-to-whole percentages and line-graph extrema/range.
- Independent tests evaluate all offered expressions with exact SymPy and verify inverse defining equations, checking uniqueness by numeric meaning. Fraction/Decimal tests cross-check conversion, chart tests reconstruct both data series, and all semantic branches are exercised. A regression preserves the source's noninteger inverse-loss cost. The first catalog checks found a length cue in remainder-quantity expressions; final alternatives use comparable calculation structures with sign, inversion and base mistakes.
- ป.5 increases 135→145. Next thinnest: ป.4 (136), then ป.2/ป.3 (138). Across this continuation: 112 new generators, twenty-seven papers, 590 digest items; full catalog 5,058 sets. All 5,048 earlier golden hashes, seed lists and retirement state are unchanged. All 8,685 bank records remain; only the selected source gains item/stage fields.
- Validation: the broad integration run passed 22,355 tests, 9 skipped, in 206.74 seconds, including bank maths, provenance/safety, every golden draw, curriculum/stage/filing contracts and existing Primary 5/6 checks. Final review identified the rare chart case of equal series totals with every selected-series count equal; added a distinct partial-total mistake and a forced regression to guarantee enough choices. After that correction, all 42 targeted checks and all 5,110 registry-wide checks pass. All 5,048 earlier golden records remain identical. Ruff/whitespace checks pass; PDF smoke-test warnings concern pre-existing missing Thai glyphs in the test font.

### 2026-11-16 — Eleven Primary 4 time and symbolic-model sets

- Continued with ป.4, thinnest at 136 maths sets, using readable-text `mathematics/level/primary-4/4540-4-2567-2-2.pdf`: twenty MC questions. A transcriber and parent reviewed all six pages, every clock alternative, all six training rows, all six bus rows, every symbolic expression/story and the printed key. All twenty independently computed answers agree with the key. No item or figure is omitted; source PDF bytes/path are unchanged.
- Source conventions remain explicit: Q3 includes both 2 and 22 July (21 days); Q4 uses a conventional 52-week year (1.5 years→78 weeks); Q6 supplies 30 days/month; Q10 assumes next-morning arrival (19:25→09:15, 13h50m); Q20 is exact 232615/2 baht with no rounding instruction. New generators state inclusive endpoints, approximate-unit conventions, arrival days and strict-before cutoffs. Original wrong-story numeric duplicates are preserved privately; new alternatives are mathematically distinct.
- `docs/for_admin/sheet_digestion_primary4_models11.py` claims all twenty items exactly once, adding fifteen units and appending an existing elapsed-time unit. All sixteen coverage scripts rerun byte-for-byte idempotently. Knowledge validation: 823 units across 449 topic files, zero problems. The source reaches generated with twenty items, separate from green publication review. Private source verification/parent notes: `_notes/primary4-models11/`.
- Added `math.clock_hands_from_minutes_p4`, `math.inclusive_date_weeks_p4`, `math.approximate_months_days_p4`, `math.fractional_year_weeks_p4`, `math.schedule_duration_p4`, `math.departure_cutoff_p4`, `math.add_sub_sentence_p4`, `math.remaining_share_sentence_p4`, `math.quotient_then_add_sentence_p4`, `math.pack_unit_price_sentence_p4`, `math.related_story_for_sentence_p4`. The final coverage review added the explicit fractional-year/week conversion, bringing the batch from ten to eleven. Every key is in an existing unit module and application stage; covered direct-clock, ordinary unit, travel, product-plus-fee and shortfall procedures reuse existing sets.
- Independent visible-content tests use clock angles, datetime dates/intervals, repeated unit groups, rational fractions, strict departure comparisons, inverse equations, repeated revenue sums, exact expression evaluation and semantic evaluation of every story. Tests cover both duration units, both add/subtract models, both story families, all twenty-four clock hours and all three year fractions. Cutoff cases always include an exactly-on-threshold distractor; arrival annotations are checked. A regression preserves the inclusive source interval and fractional sharing result.
- ป.4 increases 136→147. Next thinnest: ป.2/ป.3 (138), then ป.6/ม.3 (140). Across this continuation: 123 new generators, twenty-eight papers, 610 digest items; full catalog 5,069 sets. All 5,058 earlier golden records, seed lists and retirement state are unchanged. All 8,685 bank records remain present; only this source gains item/stage fields.
- Validation: all 23 focused checks pass, including independent solvers, the source regression and 300-seed catalog checks for eleven additions. One combined integration run passed 22,385 tests, 9 skipped, in 208.68 seconds, including bank maths, provenance/safety, every golden draw, curriculum/stage/filing contracts and existing Primary 4 checks. Ruff and whitespace checks pass. The 33 PDF smoke-test warnings concern pre-existing missing Thai glyphs in the test font.

### 2026-11-16 — Ten Primary 2/3 arithmetic and measurement sets

- Continued with ป.2/ป.3, tied thinnest at 138 maths sets, using readable-text `mathematics/level/primary-2/4180-2-2567-2-1.pdf` and `mathematics/level/primary-3/4352-3-2565-1-2.pdf`: twenty MC questions each. Transcribers and parent reviewed all ten pages, every alternative, raw data mark, table, picture and printed key, including the image-only Primary 3 key. All forty intended answers independently agree with the keys. No item or figure is omitted and PDF bytes/canonical paths are unchanged.
- Primary 2 Q15's continued third option is preserved. Primary 3 animal symbols are 5,4,3,6,5 with scale2; raw fruit counts 3,2,1,4; pet picture counts 4,7,5,3. The full schedule and all original table alternatives are retained. Q9 has two equal wrong values (10ขีด=1kg); Q10's platform-scale choice is conventional because basket mass/capacities are unstated. No artificial capacity constraint is added. Intended answers remain separate from publication quality; no green status is asserted.
- `docs/for_admin/sheet_digestion_primary23_batch10.py` claims all forty questions exactly once across twenty units. All seventeen coverage scripts rerun byte-for-byte idempotently and preserve earlier claims. Knowledge validation: 843 units across 453 topic files, zero problems. Both sources reach generated with twenty items each. Private source checks and parent review: `_notes/primary23-batch10/`.
- Added ป.2: `math.match_three_digit_sum_p2`, `math.balance_three_digit_sums_p2`, `math.match_three_digit_difference_p2`, `math.balance_three_digit_differences_p2`. These address three-digit ranges while retaining earlier Primary 1 two-digit generators unchanged. Added ป.3: `math.activity_time_lookup_p3`, `math.weight_comparison_statement_p3`, `math.weight_estimation_error_p3`, `math.capacity_comparison_statement_p3`, `math.capacity_estimation_error_p3`, `math.share_decimal_litres_p3`. Every key is in an existing unit module and application stage; covered arithmetic, pictographs, raw-data tables, scales/tools and unit basics reuse existing sets.
- Independent visible-content tests solve both-sided equations symbolically, evaluate all expressions and verify operand bounds, parse schedules with datetime, normalize weights with Fraction, and use Decimal for capacity comparisons/sharing. Every offered comparison is checked. Tests cover both directions, under/over-estimates, gram and kg/gram answers, all five activity lookups and whole/fractional litre totals. Source regressions preserve 7700g/700g weight errors, 250ml sharing and 200ml capacity error. Distractor constructions guarantee distinct values without changing shared tables or earlier seeded draws.
- ป.2 increases 138→142; ป.3 increases 138→144. Next thinnest: ป.6/ม.3 (140), then ป.2 (142). Across this continuation: 133 new generators, thirty papers, 650 digest items; full catalog 5,079 sets. All 5,069 earlier golden records, seed lists and retirement state are unchanged. All 8,685 bank records remain; only the two selected papers gain item/stage fields.
- Validation: all 21 focused checks pass, including independent solvers, original-unit regressions and 300-seed catalog checks for ten additions. One combined integration run passed 22,494 tests, 9 skipped, in 208.53 seconds, covering bank maths, provenance/safety, every golden draw, curriculum/stage/filing contracts and existing Primary 2/3 tests. Ruff and whitespace checks pass. The 33 PDF smoke-test warnings concern pre-existing missing Thai glyphs in the test font.

### 2026-11-16 — Ten Primary 6 ratio, pattern and volume models

- Continued with ป.6, tied thinnest with ม.3 at 140 maths sets, using readable-text papers `mathematics/level/primary-6/4904-6-2567-2-2.pdf` and `mathematics/level/primary-6/4907-6-2567-2-2.pdf`: twenty MC items each. Transcribers and parent reviewed all twelve pages, every option, shaded shape, pie label, net and printed key. All forty intended answers agree with independent checks. No PDF bytes, canonical paths or earlier references changed.
- Source caveats remain private: 4904 Q13/Q14/Q16 have exact noninteger results1175/6baht,2100/31%,174000/17baht; Q15 mixes interest percentage and baht wording. 4907 Q7 uses an intended product pattern; Q14 requires distinguishing the elongated pictured prism while acknowledging cube/prism taxonomy; Q18 gives width7/5cm after5m→500cm; Q20 retains unusually thick300cm wood and costs3600baht. New generators state pattern rules, simple-interest assumptions and units explicitly. Generated records coverage, separate from publication quality; no green review is asserted.
- `docs/for_admin/sheet_digestion_primary6_batch10.py` claims all forty items exactly once across 33 units. All eighteen mapping scripts rerun byte-for-byte idempotently and preserve earlier claims. Knowledge validation: 876 units across 460 topic files, zero problems. Both papers reach generated with twenty items. Private source review and repeatable answer checks: `_notes/primary6-batch10/`.
- Added `math.non_equivalent_ratio_p6`, `math.principal_interest_ratio_p6`, `math.calendar_percent_sentence_p6`, `math.gcd_lcm_product_model_p6`, `math.quadratic_product_pattern_p6`, `math.axial_cylinder_section_p6`, `math.box_volume_sentence_p6`, `math.cube_litres_sentence_p6`, `math.box_dimension_sentence_p6`, `math.mixed_box_cost_sentence_p6`. All are application-stage additions in existing unit modules. Other procedures reuse covered generators; no existing table or seeded generator is widened.
- Independent visible-content tests check cross products, hypothetical principal/interest balances, exact expression values, SymPy GCD/LCM and positive roots, polygon area and inverse unit equations. Every offered alternative is checked. Both GCD/LCM contexts and both inverse-dimension modes are exercised. A forced (6, 10, 4) box regression handles coincident wrong values and guarantees enough distinct choices. All 22 focused checks pass, including 300-seed catalog checks for all ten additions.
- ป.6 increases 140→150. Next thinnest: ม.3 (140), then ป.2 (142). Across this continuation: 143 new generators, 32 papers, 690 digest items; full catalog 5,089 sets. All 5,079 earlier golden records, seeds and retirement state remain identical. All 8,685 bank records remain; exactly two gain item/stage fields.
- Validation: the combined integration run passed 22,487 tests, 9 skipped, in 210.62 seconds, including bank maths, provenance/safety, every golden draw, curriculum/stage/filing contracts and existing Primary 5/6 checks. Ruff and whitespace checks pass. The 33 PDF smoke-test warnings concern pre-existing missing Thai glyphs in the test font.

### 2026-11-16 — Eleven Secondary 3 inequality and quadratic models

- Continued with ม.3, thinnest at 140 maths sets, using readable-text paper `mathematics/level/secondary-3/5196-3-2564-1.pdf`: forty MC questions. Transcriber and parent reviewed all eight pages, every option, numberline, fraction/radical and the forty image-key marks. Q39 mixed numbers were checked again at larger scale. All intended key positions agree with independent computations under the caveats below. No PDF bytes, canonical path or earlier references changed.
- Source Q13 has exact positive integer solutions7,8: both B(>6) and C(<14) are true. Q15 gives S>15 but all four printed lower bounds are entailed; B is strongest. Both are flagged privately, preserving original choices and intended keys. Q37 rejects algebraic root1 because age five years ago would be negative; valid age10. Q39 choices are mixed numbers, sum−16/3. New generators state age domains and ask for exact extrema; area bounds use positive real dimensions and the greatest universal lower boundary. Generated is coverage, separate from green publication approval.
- `docs/for_admin/sheet_digestion_secondary3_batch11.py` claims all forty questions exactly once across 21 units. All nineteen mapping scripts rerun byte-for-byte idempotently and preserve earlier claims. Knowledge validation: 897 units across 463 topic files, zero problems. The paper reaches generated with forty items. Private source checks/review: `_notes/secondary3-batch11/`.
- Added `math.inequality_representation_m3`, `math.age_constraint_m3`, `math.rectangle_area_bound_m3`, `math.factor_cube_identity_m3`, `math.factor_fourth_power_m3`, `math.quadratic_standard_form_m3`, `math.quadratic_dimension_m3`, `math.quadratic_past_age_m3`, `math.quadratic_number_relation_m3`, `math.quadratic_root_relation_m3`, `math.perpendicular_travel_m3`. All are in existing unit modules and application stage. Ordinary linear solving, integer counts and quadratic roots reuse existing generators; no earlier set or shared table is widened.
- Independent tests inspect visible choices and use exact interval semantics, age enumeration, polynomial identities/degree/coefficients, symbolic limits, inverse area/age equations, root reconstruction and squared distance. Every offered alternative is checked. All semantic modes are exercised, including six numberline/verbal representation cases. Forced regressions cover duplicate false values in past-age and both root-relation contexts. All 25 focused checks pass, including 300-seed catalog checks for eleven additions.
- ม.3 increases 140→151. Next thinnest: ป.2 (142), then ป.3 (144). Across this continuation: 154 new generators, 33 papers, 730 digest items; full catalog 5,100 sets. All 5,089 earlier golden records, seeds and retirement state remain identical. All 8,685 bank records remain; exactly one gains item/stage fields.
- Validation: the combined integration run passed 22,474 tests, 9 skipped, in 232.55 seconds, covering bank maths, provenance/safety, every golden draw, curriculum/stage/filing contracts and existing Secondary 3 tests. Ruff and whitespace checks pass. The 33 PDF smoke-test warnings concern pre-existing missing Thai glyphs in the test font.

### 2026-11-17 — Nine Primary 2/3 measurement and chart sets

- Continued with ป.2, thinnest at 142 maths sets, and ป.3, next at 144. Completed readable-text papers `mathematics/level/primary-2/4152-2-2564-2-2.pdf` and `mathematics/level/primary-3/4354-3-2565-1-3.pdf`, twenty MC questions each. Transcribers and parent reviewed all eleven pages, every option, ruler endpoint, route label, graph tick, container equivalence, seven-day pictograph and both image-only keys. No PDF bytes, canonical paths or earlier references changed.
- Primary 2 Q11 has two false choices A/B; intended key B remains with a quality flag. Q13 dry-bucket selection and Q14 smallest-bottle choice are conventional because calibration/capacities are unstated. Q15 coarse-pieces/heaped rule is retained as the source classroom convention. New generators state tool equivalences/capacity and the activity's measuring rule; volume questions have exactly one false choice and balanced relational wording. Chart symbols Mon–Sun are3,7,4,5,2,3,5 at10 each; new pair-target charts ensure a globally unique pair. Primary 3 Q3's cross-year bank balances can double-count; intended29400 is preserved privately, without assuming separate deposits. New revenue questions use distinct days. Generated records coverage, separate from publication review.
- `docs/for_admin/sheet_digestion_primary23_nine.py` maps all forty items exactly once across 22 units. All twenty mapping scripts rerun byte-for-byte idempotently and preserve earlier claims. Knowledge validation: 919 units across 465 topic files, zero problems. Both papers reach generated with twenty items each. Private source checks/review: `_notes/primary23-nine/`.
- Added Primary 2: `math.round_trip_metres_p2`, `math.volume_comparison_statement_p2`, `math.container_equivalence_p2`, `math.dry_measure_method_p2`, `math.pictograph_pair_target_p2`, `math.pictograph_extreme_amount_p2`. Added Primary 3: `math.comparison_amount_large_p3`, `math.three_revenues_large_p3`, `math.mixed_length_result_p3`. Nine useful gaps satisfy the roughly ten-set cadence; covered procedures reuse existing generators. All new keys live in existing unit modules and application stage, preserving old draws/tables.
- Independent visible-content tests check every alternative with rational unit equivalences, semantic comparisons, exhaustive chart pairs, inverse equations and mixed-unit normalization. Cover both extrema/materials, all three container relations, all four comparison wordings and all eight unit/operation/carry-borrow branches. A forced equal-revenue regression checks that partial totals leave enough distinct distractors. Source regressions preserve1578m round trip, two false source statements,830cm sum and360cm borrowing. All 20 focused checks pass, including 300-seed catalog checks for nine additions.
- ป.2 increases 142→148; ป.3 increases 144→147. Next thinnest: ป.5 (145), then ป.1 (146). Across this continuation: 163 new generators, 35 papers, 770 digest items; full catalog 5,109 sets. All 5,100 earlier golden records, seeds and retirement state remain identical. All 8,685 bank records remain; exactly two gain item/stage fields.
- Validation: the combined integration run passed 22,621 tests, 9 skipped, in 219.41 seconds, covering bank maths, provenance/safety, every golden draw, curriculum/stage/filing contracts and existing Primary 2/3 tests. Ruff and whitespace checks pass. The 33 PDF smoke-test warnings concern pre-existing missing Thai glyphs in the test font.

### 2026-11-17 — Eleven Primary 5 decimal and fraction expression sets

- Continued with ป.5, thinnest at 145 maths sets, using readable-text papers `mathematics/level/primary-5/4723-5-2567-2-1.pdf` and `mathematics/level/primary-5/4725-5-2567-2-2.pdf`: twenty MC items each. Transcribers and parent reviewed all ten pages, every option, fraction/mixed number, decimal, bracket, rounding directive, geometry diagram/lattice/angle label and both printed keys. All intended answers agree with independent computations. No PDF bytes, canonical paths or earlier references changed.
- Decimal exacts: Q19 26.202→26.20 at2dp; Q20 523.4800→523.5 at1dp. No extra source rounding is imposed. New draws use exact Fraction results and round only at the end under an explicit half-up rule; regressions include (13.85÷3)×3.3=15.235→15.24 and the source values. Geometry notes preserve rectangle adjacent-side perpendicularity without assuming perpendicular diagonals; Q16's OQ lattice vector parallels AB; Q17/18 alternate-position names do not require parallelism; Q20's c=h is only a special90degree case, not a general identity. Coverage is separate from green publication review.
- `docs/for_admin/sheet_digestion_primary5_eleven.py` maps all forty questions exactly once across 23 units. All twenty-one mapping scripts rerun byte-for-byte idempotently and preserve earlier claims. Knowledge validation: 942 units across 470 topic files, zero problems. Both papers reach generated with twenty items each. Private source review/repeatable checks: `_notes/primary5-eleven/`.
- Added `math.decimal_three_place_addsub_p5`, `math.decimal_bracket_calculation_p5`, `math.decimal_round_expression_p5`, `math.fraction_comparison_statement_p5`, `math.fraction_expression_extreme_p5`, `math.fraction_story_sentence_p5`, `math.fraction_discount_sentence_p5`, `math.length_equivalence_statement_p5`, `math.odd_length_equivalence_p5`, `math.length_rate_sentence_p5`, `math.khit_cost_sentence_p5`. All live in existing unit modules and application stage. Existing generators cover basic products/division, simple conversions and geometry. No prior set or shared table is widened.
- Independent visible-content tests check every offered alternative using exact expressions, inverse unit equations, semantic story operations and distance to neighbouring rounding outcomes. Cover all eight bracket patterns, both precisions, four comparison symbols, both extrema, all four story operations and every odd-length unit. The odd-length task intentionally has three equivalent wrong values; other numeric choices are distinct where applicable. All 24 focused checks pass, including 300-seed catalog checks for eleven additions.
- ป.5 increases 145→156. Next thinnest: ป.1 (146), then ป.3/ป.4 (147). Across this continuation: 174 new generators, 37 papers, 810 digest items; full catalog 5,120 sets. All 5,109 earlier golden records, seeds and retirement state remain identical. All 8,685 bank records remain; exactly two gain item/stage fields.
- Validation: the combined integration run passed 22,615 tests, 9 skipped, in 219.36 seconds, covering bank maths, provenance/safety, every golden draw, curriculum/stage/filing contracts and existing Primary 5/6 tests. Ruff and whitespace checks pass. The 33 PDF smoke-test warnings concern pre-existing missing Thai glyphs in the test font.

### 2026-11-17 — Nine Primary 1/3 pattern and place-value sets

- Continued with ป.1, thinnest at 146 maths sets, and ป.3, tied next with ป.4 at 147. Completed readable-text papers `mathematics/level/primary-1/4009-1-2565-2-2.pdf` and `mathematics/level/primary-3/4355-3-2565-1-2.pdf`: twenty MC items each. Transcribers and parent reviewed all ten pages, every option, pattern icon/colour/size, underline and both image keys. No PDF bytes, canonical paths or earlier references changed.
- Source flags remain private: P1 Q5 key A assumes only shape changes; B also changes shape but changes size too. New prompts require exactly one changing attribute. P3 Q3 has both > and ≠ true (50405 vs50205), with intended > retained. Q7 A/B/D all sum82916 but only A is canonical place-value expansion. New statements have exactly one true choice and canonical prompts state one digit-value term per place. Maths-content alternatives preserve the intentionally equal-value noncanonical traps without prose rewriting. Q16 road-tool selection is conventional because length/range are unstated. Coverage remains separate from green publication review.
- `docs/for_admin/sheet_digestion_primary13_nine.py` maps all forty items exactly once across 20 units: eleven new and nine reused. Foundational tool/length questions append to existing lower-grade units with the same procedures. All twenty-two mapping scripts rerun byte-for-byte idempotently and preserve earlier claims. Knowledge validation: 953 units across 471 topic files, zero problems. Both papers reach generated with twenty items. Private checks/review: `_notes/primary13-nine/`.
- Added Primary 1: `math.unit_step_sequence_choice_p1`, `math.single_attribute_pattern_p1`. Added Primary 3: `math.digit_place_value_pair_p3`, `math.canonical_expansion_p3`, `math.expanded_comparison_statement_p3`, `math.order_large_sequence_p3`, `math.bracket_missing_number_p3`, `math.longer_than_reference_p3`, `math.length_estimation_error_p3`. Nine useful gaps complete the roughly ten-set batch; all other procedures reuse existing generators. All additions live in existing unit files and application stage; no earlier draws/tables are widened.
- Independent tests inspect every visible alternative via finite differences, attribute changes, positional digits, canonical term multisets, exact expressions, sorted permutations, inverse equations and rational units. Cover both directions, all three attributes, every digit position and zero/nonzero, all four comparison signs, both full-order directions, all three box layouts and all four error direction/size cases. Strict length thresholds include an exactly equal distractor. A forced one-centimetre borrowing regression checks enough distinct choices. Source regressions retain multiple true signs, equal-value noncanonical sums, missing1200 and error75cm. All 20 focused checks pass, including 300-seed catalog checks for nine additions.
- ป.1 increases 146→148; ป.3 increases 147→154. Next thinnest: ป.4 (147), then ป.1/ป.2 (148). Across this continuation: 183 new generators, 39 papers, 850 digest items; full catalog 5,129 sets. All 5,120 earlier golden records, seeds and retirement state remain identical. All 8,685 bank records remain; exactly two gain item/stage fields.
- Validation: the combined integration run passed 22,708 tests, 9 skipped, in 216.47 seconds, covering bank maths, provenance/safety, every golden draw, curriculum/stage/filing contracts and existing Primary 1/3 tests. All 57 pre-existing units in changed knowledge files preserve their metadata, earlier sources and coverage references. Ruff and whitespace checks pass. The 33 PDF smoke-test warnings concern pre-existing missing Thai glyphs in the test font.

### 2026-11-17 — Eleven Primary 4 model and geometry-summary sets

- Continued with ป.4, thinnest at 147 maths sets, using readable-text papers `mathematics/level/primary-4/4537-4-2565-1-2.pdf` and `mathematics/level/primary-4/4543-4-2567-2-2.pdf`, twenty MC questions each. Transcribers and parent reviewed all eleven pages, every option, line/angle symbol, chart/table value and both keys. Q11's small arrow in4537 was rechecked at3x: C has one head, not two, so only D is correct. No PDF bytes, canonical paths or earlier references changed.
- Source flags retained privately:4537 Q17 requires exactly-one-pair and nonsquare conventions; Q19 sums12 absence-events, not necessarily distinct students; Q20 uses only the supplied historical moon counts.4543 Q13 has multiple false/notation-problematic claims (line as arm, whole angle as vertex, hat notation on a point). Printed A is preserved with an ambiguity flag. Rectangle diagonal perpendicularity is special to squares; new dimensions exclude squares explicitly. Both complete charts and all18 height-table cells are retained. Intended keys agree with independent checks under those caveats; generated is coverage, separate from green publication review.
- `docs/for_admin/sheet_digestion_primary4_eleven.py` claims all forty items exactly once across18 new units. All twenty-three mapping scripts rerun byte-for-byte idempotently and preserve earlier claims. Knowledge validation:971 units across479 topic files, zero problems. Both papers reach generated with twenty items. Private source review/repeatable checks: `_notes/primary4-eleven/`.
- Added `math.canonical_expansion_millions_p4`, `math.rounding_statement_p4`, `math.large_addsub_sentence_p4`, `math.discount_fee_sentence_p4`, `math.product_model_statement_p4`, `math.line_notation_p4`, `math.plane_surface_model_p4`, `math.rectangle_property_statement_p4`, `math.square_summary_statement_p4`, `math.three_series_chart_summary_p4`, `math.selected_columns_row_max_p4`. All are in existing unit files and application stage. Existing reading, angle, opposite-side and basic chart generators are reused; no old generator/table is widened.
- Independent visible-content tests inspect every alternative with rational expressions, nearest-multiple distances, repeated products, directed endpoint semantics, coplanarity, SymPy polygons/segments and full chart/row reconstruction. All modes are covered. Selected-category questions keep the irrelevant full-row maximum different and offer only rows present in the table. Square draws avoid the area/perimeter coincidence at side4. Maths content preserves equal-value noncanonical expansion traps. All22 focused checks pass, including300-seed catalog checks for eleven additions.
- ป.4 increases147→158. Next thinnest: ป.1/ป.2 (148), then ป.6 (150). Across this continuation:194 new generators,41 papers,890 digest items; full catalog5,140 sets. All5,129 previous golden records, seeds and retirement state remain identical. All8,685 bank records remain; exactly two gain item/stage fields.
- Validation: 22 focused checks passed. Broad integration: 22,681 passed, 9 skipped, 33 existing font warnings in 214.98 s. Ruff and whitespace checks pass. Earlier golden draws remain unchanged.

### 2026-11-17 — Nine Primary 2 calendar and measurement sets

- Continued at the thinnest levels, ป.1 and ป.2 (148 each), with readable-text papers `mathematics/level/primary-1/4012-1-2565-1-2.pdf`, `mathematics/level/primary-2/4170-2-2565-1-2.pdf` and `mathematics/level/primary-2/4167-2-2565-2-2.pdf`. All sixty MC questions are transcribed, independently checked, converted and mapped. Transcribers and parent reviewed all fifteen pages, every option, diagram, clock, underline and image key. PDF bytes and canonical paths are unchanged.
- All twenty Primary 1 procedures reuse existing generators. Nine useful Primary 2 gaps complete these papers: `math.month_ordinal_p2`, `math.month_pair_days_p2`, `math.half_metre_p2`, `math.unit_quantity_p2`, `math.calibrated_volume_tools_p2`, `math.weighing_tool_precision_p2`, `math.weight_threshold_p2`, `math.weight_extreme_p2`, `math.repeating_colour_pair_p2`. All live in existing unit modules and application stage. No older draws or tables are widened.
- Source caveats remain private: 4012 Q6 requires canonical expansion despite three true equalities; Q12 requires the matching story operands despite two sums equal to 14. 4170 Q9/Q11 use routine assumptions; existing generators give explicit schedules. 4167 Q6/Q20 lack dimensions/masses; Q12 has no quantity/range/protocol to exclude measuring spoons; Q13 names a litre vessel, not merely the unit; Q14/Q15 rely on the classroom dry/liquid and heaped-coarse conventions; Q16 lacks range and precision. New tasks supply explicit measurements, calibration and instrument requirements. Strict weight thresholds retain two equal-to-boundary distractors with exactly one correct alternative. Private records and repeatable checks: `_notes/primary2-nine/`.
- `docs/for_admin/sheet_digestion_primary2_nine.py` claims all sixty items exactly once, adding ten knowledge units and preserving earlier claims. All 173 pre-existing Primary 1/2 units preserve their metadata, sources and coverage references. All twenty-four mapping scripts rerun byte-for-byte idempotently. Knowledge validation: 981 units in 479 topic files, zero problems. All three papers reach generated, denoting coverage separately from green publication review.
- All 18 focused checks pass, including 300-seed catalog checks for nine additions and independent visible-choice checks with exhaustive two-colour assignments, calendar dates, rational half-unit conversions, dimensional families, capacity/resolution inequalities and normalized mass. Both month/name directions, leap/non-leap February, strict heavier/lighter and maximum/minimum modes are covered. Scale labels and row order vary independently; tests cover every correct label at each resolution. All 5,140 earlier golden records, seeds and retirement state remain identical. All 8,685 bank records remain; exactly three gain item/stage fields.
- ป.2 increases 148→157; ป.1 remains 148 because its paper's procedures are already covered. Next thinnest: ป.1 (148), then ป.6 (150). Across this continuation: 203 new generators, 44 papers, 950 digest items; full catalog 5,149 sets.
- Validation: all 18 focused checks passed. Final integration: 22,790 passed, 9 skipped, 33 pre-existing font warnings in 227.95 s. Ruff and whitespace checks pass. All earlier seeded draws remain unchanged.

### 2026-11-17 — Ten Primary 1 LPMC25 application sets

- Continued with ป.1, thinnest at 148 maths sets. Readable-text source `mathematics/level/primary-1/11167-LPMC-Math-G1-No25-2567.pdf` has thirty items across twelve exercise pages plus a cover. All thirty are transcribed, independently checked and converted; every printed MC option is retained. No answer key appears in the PDF: records explicitly label answers and option positions as computed. Transcriber and parent reviewed all exercise pages and the small tile/face/dice details. PDF bytes and canonical references are unchanged.
- Added `math.post_interval_distance_p1`, `math.rank_both_ends_p1`, `math.possible_nth_weekday_p1`, `math.equal_pieces_size_rank_p1`, `math.minimum_coins_p1`, `math.latin_missing_sum_p1`, `math.minimum_bags_p1`, `math.distinct_fruit_assignment_p1`, `math.equalize_piles_p1`, `math.digit_inequality_count_p1`. All append to existing unit modules and application stage; no earlier set or shared table is widened. New wording explicitly permits unused coin denominations and a partially filled final bag. Assignment questions use four real fruit categories, with one unique allocation.
- `docs/for_admin/sheet_digestion_primary1_ten.py` claims all thirty items exactly once, adding 27 units and reusing three units. Ten new generators plus existing types cover fourteen questions. Sixteen explicit gaps remain: 2,4,8,11,13,15,18,19,20,23,24,25,26,28,29,30. The paper stays **extracted**, not generated. Private `_notes/primary1-ten/coverage.json` and review/checks preserve this handoff. Knowledge validation: 1,008 units across 479 topic files, zero problems. All 25 mapping scripts rerun byte-for-byte idempotently.
- Source checks distinguish tile6's closed diamond, happy-face label sum13, polyomino option2 rotated180, Latin missing sum16, impossible dice option2, and eight triangles. Q12 gives10 coins if denominations are optional,13 if all must occur; both interpretations are retained. Q13 requires the intended rotation convention. Q19 depends on ordinary sizes, Q24 on an inferred finite-example rule and Q26 on classroom whole-year timing. These caveats are separate from coverage/publication quality.
- All 20 focused checks passed, including 300-seed catalog checks and independent checks of every displayed alternative using exhaustive starts/allocations, rational areas, breadth-first coin states, Latin completion, integral transport and inverse inequalities. Cases cover post1, both size-order directions, seven allowed denomination sets, all blank counts, full/partial bags, every person/fruit answer and all four strict/inclusive signs including zero. All 897 earlier maths knowledge units preserve metadata, claims and coverage references; all 5,149 earlier golden records, seeds and retirements are identical. All 8,685 bank entries remain; only this paper gains item/stage fields.
- ป.1 increases 148→158. Next thinnest: ป.6 (150), then ม.3 (151). Across this continuation: 213 new generators; 44 fully covered papers plus this partial paper; 980 converted digest items. Full catalog: 5,159 sets.
- Validation: 20 focused checks passed. Integration: 22,768 passed, 9 skipped, 33 pre-existing font warnings in 211.68 s. Ruff and whitespace checks pass. All earlier seeded draws remain unchanged.

### 2026-11-18 — Ten Primary 6 fraction, decimal and volume-model sets

- Continued with ป.6, thinnest at 150 maths sets, using readable-text papers `mathematics/level/primary-6/4898-6-2565-1-2.pdf` and `mathematics/level/primary-6/4901-6-2565-1-2.pdf`. All forty questions and 160 MC alternatives are transcribed and independently checked. Transcribers and parent reviewed all eleven pages, including mixed numbers, tiny fraction operands, patterns, nets and both image keys. No PDF bytes, canonical paths or earlier references changed.
- Added `math.mixed_remaining_model_p6`, `math.two_fraction_purchases_model_p6`, `math.fraction_order_statement_p6`, `math.decimal_operation_model_p6`, `math.decimal_division_story_p6`, `math.ribbon_sale_model_p6`, `math.decimal_bag_count_p6`, `math.multiple_cube_volume_p6`, `math.cuboid_capacity_extreme_p6`, `math.square_grid_perimeter_p6`. All append to existing unit modules and application stage. Existing comparisons, simple fraction stories, GCD/LCM, attribute/solid/net recognition and several volume models are reused. Earlier generators/tables remain unchanged.
- Source caveats remain explicit: 4898 Q4 has two true signs; Q11 has no correct operand model (10 1/8 becomes 10 1/2 in keyed B; correct shortfall 10kg); Q15 has no matching expression (10 pieces at 10.50 gives 105, keyed A gives 84.525); Q16 leaves whole/partial bag semantics unstated. New tasks define the price unit, full/partial bags and exact quantities. In 4901 Q1 common-piece GCD wording is incomplete, Q3 assumes common alarm phase, Q5 key varies only size despite shape-and-size wording, and Q11 concatenates two names. Nets are checked as schematic fan/strip layouts with connectivity and face types, without claiming inventory alone guarantees any net. Private records: `_notes/primary6-ten/`.
- `docs/for_admin/sheet_digestion_primary6_ten.py` claims all forty items exactly once, adding thirteen units. Knowledge validation: 1,021 units in 481 topic files, zero problems. All 26 mapping scripts rerun byte-for-byte idempotently. All 924 earlier maths units and topic headers preserve metadata, prior sources and coverage references. Both selected papers reach generated, meaning procedure coverage separately from green publication quality. The Primary 1 LPMC25 paper keeps its extracted stage and sixteen gaps.
- All 20 focused checks pass, including 300-seed catalog checks and independent visible-choice checks using rational conservation, weighted fractional prices, cross-products, inverse pricing units, feasible capacity bounds, enumerated cubes and exposed grid edges. All story/order/revenue/bag/extreme modes are exercised, including twelve bag-capacity/mode combinations and eight row-name/extreme combinations. Revenue alternatives use explicit equal-length symbols; story alternatives pass length-cue checks. All 5,159 earlier golden records, seeds and retirements remain identical. All 8,685 bank records remain; exactly two gain item/stage fields.
- ป.6 increases 150→160. Next thinnest: ม.3 (151), then ป.3 (154). Across this continuation: 223 new generators, 46 fully covered papers plus one partial paper, 1,020 converted digest items. Full catalog: 5,169 sets.
- Validation: all 20 focused checks passed. Integration: 22,757 passed, 9 skipped, 33 pre-existing font warnings in 229.43 s. Ruff and whitespace checks pass. All earlier seeded draws remain unchanged.

### 2026-11-18 — Eleven Secondary 3 system and solid applications

- Continued with ม.3, thinnest at 151 maths sets. Readable-text source `mathematics/level/secondary-3/5198-3-2565-2.pdf` contains forty questions and 160 MC alternatives across nine pages. All are transcribed, converted, independently checked and mapped. Transcriber and parent reviewed every page, including the circle labels, all figures and printed key. PDF bytes and canonical references are unchanged.
- Added `math.system_parameter_difference_m3`, `math.mixture_mass_ratio_m3`, `math.joint_worker_time_m3`, `math.reversed_digit_system_m3`, `math.pyramid_roof_tile_count_m3`, `math.sphere_area_from_volume_m3`, `math.hemisphere_on_cone_area_m3`, `math.sphere_volume_from_circumference_m3`, `math.pyramid_cast_mass_m3`, `math.cone_cup_count_m3`, `math.pyramid_surface_from_height_m3`. All append to existing unit modules and application stage. Existing systems, circle theory/angle chains, basic solid formulas, fraction/unit conversion and volume conservation generators cover the remaining procedures. No earlier set/table is widened.
- Source exceptions remain explicit: Q14 exact child time is 11.25 days with no exact option (printed C12 requires an unstated whole-day convention); Q19 centre/intersection answers overlap and distinct bisectors are required; Q30 area-based answer is 30 tiles (D), contradicting printed A10, and side10/slant6 is impossible for a right regular pentagonal pyramid; Q33 lacks a direct volume option and its printed555.37 comes from prematurely rounding radius5.1, while a great-circle assumption is unstated. New tasks specify feasible dimensions, area-only material estimation, exact work times, great circles, π, full/partial containers and final-only rounding. All physical/rounding assumptions and all corrected diagram values are retained in `_notes/secondary3-eleven/`.
- `docs/for_admin/sheet_digestion_secondary3_eleven.py` claims all forty items exactly once, adding nineteen units. Knowledge validation: 1,040 units across 481 topic files, zero problems. All 27 mapping scripts rerun byte-for-byte idempotently. All 937 earlier maths units and topic headers preserve metadata, prior sources and coverage references. The paper reaches generated for procedure coverage, separate from green publication review. The earlier Primary 1 LPMC25 partial paper retains its sixteen gaps.
- All 22 focused checks pass, including 300-seed catalog checks and independent visible-choice checks using symbolic systems/rates, mass/value conservation, exhaustive digit pairs, integer coverage bounds, admissible pyramid geometry, exact cube roots, sphere/pyramid integration and 3D triangular face cross-products. Both directions, worker cases, all polygon/tiling cases and cup-fill rules are covered. All 5,169 prior golden records, seeds and retirements remain identical. All 8,685 bank entries remain; only this paper gains item/stage fields.
- ม.3 increases 151→162. Next thinnest: ป.3 (154), then ป.5 (156). Across this continuation: 234 new generators, 47 fully covered papers plus one partial paper, 1,060 converted digest items. Full catalog: 5,180 sets.
- Validation: all 22 focused checks passed. Integration: 22,800 passed, 9 skipped, 33 pre-existing font warnings in 217.60 s. Ruff and whitespace checks pass. All earlier seeded draws remain unchanged.
