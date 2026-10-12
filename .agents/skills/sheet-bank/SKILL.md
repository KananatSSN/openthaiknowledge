---
name: sheet-bank
description: Digest sheets added to sheet_database/ end to end — index them, turn them into text (splitters for text PDFs, parallel sheet-transcriber subagents for picture-maths PDFs), claim every question with a knowledge unit, build problem sets for the gaps, test, and commit. Use when the user adds sheets to the bank, asks to "digest", "continue the bank", "transcribe the (สสวท) files", or asks what is left.
---

# Sheet bank → knowledge → problem sets

The bank is `sheet_database/`: a separate, private repository
(KananatSSN/openthaiknowledge-bank) cloned there and ignored by this one. If it
is missing, stop: only maintainers have it. Commit bank files (digests,
transcripts, notes) in the bank repository; commit everything else here.
Layout: `sheet_database/README.md`. Its index
is `otk/sheets/bank.json`; every file moves through the stages
`new → converted → extracted → generated` (or `ignored`). The progress log is
`docs/for_admin/SHEET_DIGESTION_PLAN.md` — read its §3 and §6 first, and add a
session entry when you finish.

All commands: `PYTHONIOENCODING=utf-8 python -m otk.tools.sheetpipe …`
(written below as `sheetpipe …`), run from the repository root.

For a single olympiad-style paper where each question deserves its own solver,
use the `sheet-to-generator` skill instead.

## 0. See what is waiting

```bash
sheetpipe bank scan                 # index files added since last time (keeps stages)
sheetpipe bank status               # per-folder summary
sheetpipe transcript todo           # picture-maths files with no transcript yet
```

PDFs are Git LFS objects, not downloaded by default:
`sheetpipe bank fetch "<bank path or glob>"`.

## 1. Text → digest

Pick by the file's `layout` (shown by `sheetpipe bank status "<glob>"`):

| Layout | How |
|---|---|
| `choice-block` (exam compilations) | `sheetpipe convert "<glob>"` |
| has an answer key in another file | `sheetpipe bank set "<glob>" --answer-key "<key path>"`, then `convert` |
| `book` (notes + key bound at the back) | `sheetpipe bank set "<glob>" --answer-key self`, then `convert` |
| `numbered` / `scan` (maths printed as pictures) | transcribe — step 2 — then `convert` |
| anything else | new splitter needed; see the plan doc §3 Phase 2 |

## 2. Transcribe picture-maths files with subagents

Agents without subagents: transcribe each file yourself, one at a time,
following `.agents/skills/sheet-transcriber/SKILL.md`, and skip the
parallelism notes below.

One `sheet-transcriber` subagent per file, run in the background, **one
chapter (≤ 8 files) at a time** so the reports stay reviewable and rate
limits are respected. Prompt each with just the bank path, plus anything you
know about the file (e.g. "pages 1–2 are the exercises; item 3's table is
missing"):

> Transcribe `rathcenter/12 หลักการนับ/(สสวท) 5 จัดหมู่🍒.pdf`.

When the reports come back:

1. `sheetpipe transcript check "<chapter glob>"` — every file must parse.
2. **Spot-check** each transcript: open one exercise page
   (`sheetpipe transcript pages "<path>" --render --pages 1`) and compare a
   few items word for word, especially numbers, signs and exponents. Read
   every item a report flags as uncertain.
3. Check the answered count is plausible: unanswered items should be proofs,
   drawings, or things the report names.
4. Fix small problems yourself; for a bad file, delete it and re-run the
   subagent with a note on what went wrong.
5. `sheetpipe convert "<chapter glob>"` (a transcript wins over any splitter).

The transcriber runs on Sonnet (`model: sonnet` in its definition), about
half Opus's price; the main session reviews on its own model. The spot-check
in step 2 is what makes that safe, so do not skip it. If a chapter's
transcripts keep needing fixes, pass `model: "opus"` when dispatching for
that chapter.

Measured cost (2026-10, Opus pilot): one subagent per 2-page exercise file
≈ 40k tokens, about a minute. The same work in one long session costs 2–4×
more, because every call re-reads the session's growing history.

## 3. Knowledge pass

Every converted question must be claimed by a unit in
`otk/knowledge/math/<topic>.json` (schema: `otk/tools/sheetpipe/knowledge.py`).

```bash
sheetpipe knowledge coverage "<glob>"   # which items are unclaimed
```

Claim by source, most specific that fits:
`{"tag": "O-NET (มี.ค. 2561/31)"}` for exam questions,
`{"sheet": path, "section": "แบบฝึกหัด 2.4"}` for a whole exercise, or
`{"sheet": path, "section": "แบบฝึกหัดท้ายบท", "number": 9}` for one item of a
mixed chapter-end exercise (with its sub-items). Write the mapping as a small
script that appends sources (re-runnable, idempotent); add a new unit only
when no existing unit's statement covers the questions.

```bash
sheetpipe knowledge validate
sheetpipe knowledge coverage --mark     # fully claimed sheets → extracted
```

## 4. Gaps → problem sets

```bash
sheetpipe plan          # units with no problem set
```

For each gap, write a generator (conventions in the plan doc §3 Phase 5 and
the sets already in the unit's file):

- Write the set in its unit's file, `otk/sets/<subject>/<level>/<unit>.py`
  (find it in `otk/sets/INDEX.md`; a new unit file is imported in its level's
  `__init__.py`), register it with `@question_type`, and place the key in its
  topic's stage path in `otk/sets/_support/math_stages.py`.
- A set in stage 1 or 2 of an IPST topic needs a strategy hint in
  `otk/sets/_support/math_hints.py`.
- Run `python -m otk.tools.sets_index` to refresh the guides.
- Answers come from a solver checked by an independent route in its test
  (`otk/tests/test_math_bank_*.py`, SymPy or brute force); distractors are
  named mistakes; tests use `REGISTRY[key].max_choices`.
- Add the key to the unit's `covered_by`, then `sheetpipe plan --mark`.

## 5. Test and commit

Never edit knowledge JSON or wire modules while the suite runs. The full
suite takes ~35 min; run it in the background with a 2-hour limit:

```bash
python -m pytest otk/tests/test_core.py otk/tests/test_math_stages.py \
  otk/tests/test_choice_counts.py otk/tests/test_answer_length.py \
  otk/tests/test_curriculum.py otk/tests/test_math_topics.py \
  otk/tests/test_math_thin_topics.py otk/tests/test_curriculum_graph.py \
  otk/tests/test_math_hints.py otk/tests/test_sheetpipe*.py \
  otk/tests/test_math_bank_*.py -q -p no:cacheprovider --basetemp=<temp dir>
```

Record every new set in the golden draws before running the suite —
`python -m otk.tools.golden_draws --update <new keys>` — and run
`otk/tests/test_golden_draws.py` (~10 s with `-n auto`): it fails if an
existing set's draws changed or a key vanished.

For transcripts alone, `otk/tests/test_sheetpipe*.py` (~3 min) is enough.
Commit one chapter at a time (transcripts + digests + bank.json, then the
knowledge and sets). Update the plan doc's progress lines and session log.
Commit locally; push only when the user asks.
