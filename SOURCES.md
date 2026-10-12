# Sources and removal requests

This repository builds practice problems from published Thai educational
material. Each source below was publicly published by its owner; we cite it,
do not claim it, and do not license it: the project's licenses (Apache-2.0,
CC BY 4.0) cover the project's own work only.

**If you hold the rights to any of this material and want it removed, we will
remove it.** Open a [removal request](../../issues/new?template=removal-request.yml)
(or contact the maintainer through their GitHub profile if you prefer not to
post publicly). We take the material out of the current version promptly and
out of the next release; on request we also rewrite the repository history so
it is no longer downloadable from here.

## What is included, and from whom

| Source | Rights holder | What this repository holds | How it is cited |
|---|---|---|---|
| Past entrance and national exams in the rathcenter compilations — O-NET, A-Level/PAT, กสพท and others (files `(1)`, `(2)`, `(onet)`) | The body that set each exam, as named in each item's tag; the compilations' worked solutions belong to their authors | Text of the questions and solutions (`sheet_database/_digest/`); problem sets adapted from them (each cites its source in `PROVENANCE`) | Each digested question carries its exam tag, e.g. `กสพท คณิต1 (เม.ย. 2564/8)`; each digest names its source file; adapted sets cite the chapter in `PROVENANCE` |
| Rathcenter chapter notes (files `(rath)`) | Their authors | Text digests (`sheet_database/_digest/`) | Source file named in each digest |
| IPST (สสวท.) mathematics textbooks and teacher's manuals | สถาบันส่งเสริมการสอนวิทยาศาสตร์และเทคโนโลยี (IPST) | Transcripts of textbook exercises and their manual answers (`sheet_database/_transcribed/`) | Each transcript names its book, exercise and pages |
| POSN (สอวน.) mathematics camp-selection papers 2561, 2562, 2565–2568 | มูลนิธิส่งเสริมโอลิมปิกวิชาการและพัฒนามาตรฐานวิทยาศาสตร์ศึกษา (POSN) | Each question's text, page text and figures (`otk/sheets/posn25xx_math/`); one problem set per question, with new numbers | `sheet.json` names the paper and item; each set's `PROVENANCE` cites paper and item |
| A physics (force) exam paper (`Faii/ข้อสอบแรง.pdf`) | Its author (not recorded) | Problem sets adapted from it (`science_wave_f1`, `f2`, `e7`) | `PROVENANCE` cites the paper |
| Science topic notes in `sheet_database/notes/topics/` (rocks, separating mixtures, pure substances, electricity) | Their original authors; `กระบวนการเปลี่ยนแปลงของหิน.md` is from TruePlookpanya (trueplookpanya.com), the others do not record where their text came from | The notes' text, used to plan which science sets to write | The source named at the top of a note, where there is one |
| The Basic Education Core Curriculum B.E. 2551 (rev. 2560) and its indicator documents | กระทรวงศึกษาธิการ (Ministry of Education) | The documents converted to Markdown, and an indicator index (`docs/curriculum_sources/`) | Each converted file names its source document |

The source PDFs themselves are not distributed here (their Git LFS objects
are kept privately); the citations identify them.

Every problem set states its provenance (`otk.api.provenance(key)`): `original`
for sets written for this project, `adapted` with the sources it adapts. The
explorer shows it on every set's page. `python scripts/source_overlap.py`
measures how closely each set's wording follows its source.
