# Publication review (decision D4)

What in this repository may be published when it goes public, family by
family, with the evidence and a recommendation for each. The maintainers
decide; tick a box per family. This is a screening of the material, not legal
advice: where a recommendation says "likely", confirm it with someone
qualified before relying on it.

Written 2026-10-12, against `main` at v0.2.0 + licenses. The wording evidence
comes from `python scripts/source_overlap.py` (method in its docstring): the
share of a set's distinctive question wording, after dropping phrasing that
more than three sets share, that also appears in its source.

## Decision (2026-10-12)

**Publish everything, with citations, and remove any material on its rights
holder's request.** The maintainers' reasoning: every source was publicly
published in the first place. The reviewer's caveat, recorded as given: prior
publication does not itself permit republishing, and citation plus removal on
request lowers the risk rather than removing it; the verbatim families (6, 7
and 9's question text) carry the most.

Done for it: `SOURCES.md` (rights holders, what is included, how each is
cited, the removal policy), a removal-request issue form, the README's
license table, and a link from every explorer page. The source PDFs are still
not distributed (their LFS objects stay private). A later check found that
family 4 is not all team-written: one note in `notes/topics/` is TruePlookpanya
text, and the others do not record their origin; `SOURCES.md` lists them as
third-party. The per-family boxes below
are superseded by this decision; the recommendations are kept as the record.

## Summary

| # | Family | Size | Recommendation |
|---|---|---|---|
| 1 | Code, tools, tests, explorer | — | Publish |
| 2 | Original sets | 3,144 sets | Publish |
| 3 | Knowledge units `otk/knowledge/` | 45 files | Publish |
| 4 | Team-written bank files: `notes/`, `specs/`, `fact_data/`, `outputs/*.md` | 21 files | Publish |
| 5 | Official curriculum documents `docs/curriculum_sources/` | 31 files, 13 MB | Likely publishable; confirm |
| 6 | Exam-compilation digests `sheet_database/_digest/` | 602 files, 8.8 MB | **Do not publish** |
| 7 | Textbook transcripts `sheet_database/_transcribed/` | 97 files | **Do not publish** |
| 8 | Source PDF pointers and `misc/` | 317 files | Drop |
| 9 | Digested olympiad papers `otk/sheets/posn25xx_math/` | 6 papers, 180 sets | **Keep private** (separate package) |
| 10 | Bank-derived modules (`math_bank_*`, `science_wave_e7/f1/f2`) | 102 sets | Publish after rewording 12 sets and a look at 18 |

## 1. Code, tools, tests, explorer — publish

Written for the project. Apache-2.0.

- [ ] Decision

## 2. Original sets — publish

Provenance `original` (`otk.api.provenance`). Against every digest and
transcript, the median distinctive overlap is **0.00** (2,790 of 3,144 sets
long enough to score). The 29 that reach 0.5 are one-line stock instructions
that every exam uses — "จงหาผลบวก 13 พจน์แรกของอนุกรมนี้", "จงหาค่าสัมบูรณ์ของ
จำนวนเชิงซ้อนนี้" — not copied questions (each was read).

- [ ] Decision

## 3. Knowledge units — publish

Method statements and steps in the project's own words, citing sources only by
tag (exam name and item, or bank path). CC BY 4.0.

- [ ] Decision

## 4. Team-written bank files — publish

`notes/` (topic outlines), `specs/math_questions.md` (the primary-maths set
spec), `fact_data/` (fact tables), `outputs/` Markdown (teaching plans and
review sheets written from the sets). Two exceptions to look at:
`outputs/teaching_plan/ข้อสอบแรง.md` discusses a third-party paper (keep only
if it does not reproduce it), and the `outputs/*.pdf` renders are LFS pointers
(drop with family 8).

- [ ] Decision

## 5. Official curriculum documents — likely publishable; confirm

The Ministry of Education's core-curriculum documents and indicator lists,
converted to Markdown, plus `indicators.jsonl` (the task queue and coverage
checks use it). Thai Copyright Act B.E. 2537 §7 excludes ministry
notifications, orders and explanations from copyright; the curriculum is
promulgated by ministry order, so it likely qualifies, but the converted books
include explanatory material. A narrower option keeps only `indicators.jsonl`
(codes and indicator text) and drops the converted books.

- [ ] Publish all — [ ] Keep only `indicators.jsonl` — [ ] Drop

## 6. Exam-compilation digests — do not publish

Text extracted from the rathcenter compilations: O-NET, PAT and กสพท questions
with a tutoring centre's worked solutions, verbatim. Third-party copyright on
both. Move to the private companion (below).

- [ ] Decision

## 7. Textbook transcripts — do not publish

Hand transcripts of IPST (สสวท.) textbook exercises and the teacher's-manual
answers, verbatim. IPST holds the copyright. Move to the private companion.

- [ ] Decision

## 8. Source PDF pointers and `misc/` — drop

`rathcenter/`, `สอวน_math/`, `Faii/` and `outputs/*.pdf` are Git LFS pointer
files whose content is in TutorRank's private store; in a public repository
they could never be fetched. `misc/schedule_2026_09.png` is not content. Drop
them, and `.lfsconfig` with them.

- [ ] Decision

## 9. Digested olympiad papers — keep private

Six สอวน. (POSN) camp-selection papers (2561, 2562, 2565–2568), 30 sets each.
Each set is one paper question with new numbers, and keeps its wording: the
median distinctive overlap with the original question is **0.74, 0.80, 0.71
and 0.81** for 2561, 2562, 2565 and 2567 (23–27 of 30 sets at ≥ 0.5), 0.29 for
2568. 2566 is a scan with no source text recorded, so it scores 0.00 but is
built the same way. The package also holds each question's original text
(`sheet.json` `source`), the papers' page text (`extract/`, 187 files) and
figures cropped from them (61 PNGs).

Options:

- **A. Separate private package** (recommended): move `otk/sheets/posn*`
  into a private `otk-papers` package that registers its sets into otk at
  import (an entry point); TutorRank installs both. Keys and draws are
  unchanged, so learners notice nothing.
- **B. Ask POSN** for permission to publish, and keep them in if granted.
- **C. Drop them** from otk and from TutorRank (their keys are retired).

- [ ] A — [ ] B — [ ] C

## 10. Bank-derived modules — publish after rewording 12 and a look at 18

84 maths sets in `math_bank_*` (built from the rathcenter chapters) and 18
science sets in `science_wave_e7/f1/f2` (from a scanned physics paper and a
teaching plan about it). The maths sets' wording partly echoes their chapter:
module medians 0.25–0.69, against a noise floor of 0.00–0.14 when a module is
compared with an unrelated chapter. Twelve sets reach ≥ 0.5:

| Module | Sets ≥ 0.5 |
|---|---|
| `math_bank_counting` | `arrangement_blocks_gaps_m5` (0.76), `counting_complement_m5` (0.58) |
| `math_bank_trig` | `triangle_side_type_m5` (0.75) |
| `math_bank_logic` | `logic_tautology_m4` (1.00), `logic_deduce_values_m4` (0.74), `logic_verbal_deduction_m4` (0.60) |
| `math_bank_stats` | `stats_transform_m6` (0.69), `stats_data_conditions_m6` (0.58) |
| `math_bank_sequences` | `sequence_patterns_m6` (0.63), `geometric_series_tricks_m6` (0.55), `arithmetic_series_tricks_m6` (0.54) |
| `math_bank_real` | `quadratic_discriminant_m3` (0.52) |

(`python scripts/source_overlap.py --sets 0.5` lists them all.) The science
sets have no source text to compare, so a person should read them against the
paper.

Recommendation: reword the twelve stems in original language (their draws
change: record them with `golden_draws --update`, and TutorRank's release
notes will list them), read the 18 science sets, and publish the rest as
`adapted` with their citations.

- [ ] Decision

## How to publish once decided

1. **Create a private companion repository** (`openthaiknowledge-bank`) for
   everything kept private: the bank (families 6–8) and, under option 9A, the
   `otk-papers` package. The sheet pipeline then reads the bank from a
   configurable path instead of `sheet_database/` in this repository.
2. **Make the changes here** (families 9 and 10), with tests green and the
   golden draws updated only for the reworded sets.
3. **Rewrite history**: everything removed must also leave the history, or it
   stays downloadable. Use `git filter-repo` on a fresh clone, check that no
   removed path is left in any commit, and push the result to a new public
   repository (or force-push this one, after which every clone must be
   re-cloned). Tags are rewritten too; TutorRank pins by tag, so re-tag and
   bump TutorRank to the new tag in the same step.
4. **Then** host the explorer, open the task issues, and announce.
