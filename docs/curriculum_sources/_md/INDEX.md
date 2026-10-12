# Curriculum sources as text

Markdown copies of the official IPST and OBEC curriculum PDFs in
`docs/curriculum_sources/`, plus an index of every indicator and learning
outcome. Use them to check curriculum claims — codes, grades, official
wording, counts — without opening a PDF. The PDFs are not in git; see
`../README.md` for where they came from.

## What to use for what

| Question | Use |
|---|---|
| Does code X exist? What does it say? Which grade? | `indicators.jsonl` |
| How many indicators does a standard or grade have? | `indicators.jsonl` |
| Core science indicators, additional science outcomes | `_ทั่วไป/ตัวชี้วัดและสาระการเรียนรู้แกนกลาง_วิทยาศาสตร์_2560.md` (the same book as `SciCurriculum_2560.pdf`, which `science_ipst_outcomes.csv` cites) |
| Core maths indicators, additional maths outcomes | `คณิตศาสตร์_ประถมศึกษา/ตัวชี้วัดและสาระการเรียนรู้แกนกลาง_คณิตศาสตร์_2560.md` (covers ป.1–ม.6 despite the folder name) |
| สาระการเรียนรู้แกนกลาง (the content column beside each indicator) | the same two books |
| Teaching intent, scope and sequence, unit plans | the `คู่มือการใช้หลักสูตร_*` guides |
| Physics additional outcomes grouped by strand | `ฟิสิกส์/ผลการเรียนรู้_ฟิสิกส์_กลุ่มที่1-4.md` |
| Sample course descriptions ม.1–ม.3 | `วิทยาศาสตร์_มัธยมศึกษา/คำอธิบายรายวิชา_*` |
| The pre-2560 core curriculum (2551) | `_ทั่วไป/หลักสูตรแกนกลางการศึกษาขั้นพื้นฐาน_2551_ฉบับ_สสวท.md`; the English edition is `Basic_Education_Core_Curriculum_2551_EN.md` |

The สพฐ. copy of the 2551 curriculum is not converted: its text layer lost
every ส to a space. The สสวท. copy is the same book.

## indicators.jsonl

One JSON object per line, built from the two indicator books:

```json
{"code": "ว 1.1 ป.1/1", "subject": "science", "kind": "core",
 "standard": "ว 1.1", "level": "ป.1", "number": 1,
 "text": "ระบุชื่อพืชและสัตว์ที่อาศัยอยู่บริเวณต่าง ๆ จากข้อมูลที่รวบรวมได้",
 "official_code": true, "formula_fix": null,
 "source": "_ทั่วไป/ตัวชี้วัดและสาระการเรียนรู้แกนกลาง_วิทยาศาสตร์_2560.pdf", "page": 20}
```

- `code` uses Arabic digits and the repo's own format: `ว 2.3 ม.3/1`,
  `ค 1.1 ป.1/5`, `ฟิสิกส์เพิ่มเติม 3 ม.5/9`.
- `page` is the PDF page (not the printed folio), the same numbering as
  the `<!-- page N -->` markers.
- `kind` is `core` or `additional`. Contents: science 415 core + 315
  additional; maths 157 core + 32 additional.
- `official_code` is false for the maths additional course. That book prints
  no codes there, so `ค เพิ่มเติม <สาระ> <area> ม.4/1` follows the science
  pattern (สาระ, learning-area number, grade, printed item number) and is ours.
- `formula_fix` marks the five entries whose formula was corrected by
  checking the rendered page (fractions, vectors and subscripts do not
  survive extraction).

```bash
python -c "import json; [print(r['code'], r['text']) for r in map(json.loads, open('docs/curriculum_sources/_md/indicators.jsonl', encoding='utf-8')) if r['standard'] == 'ว 3.1']"
```

A grade with no indicator does not appear. The books print `-` for it, or,
for some maths grades, "(มีการจัดการเรียนการสอนเพื่อเป็นพื้นฐาน แต่ไม่วัดผล)":
the topic is taught but has no indicator (for example `ค 1.2 ป.2`).

## Reading the Markdown

- Text keeps the book's Thai digits (`ป.๑`, `ว ๒.๓`); only the index
  converts them.
- Line breaks follow the PDF. Thai wraps without spaces, and the typesetters
  sometimes left a space at a wrap. Compare wording with whitespace removed;
  spacing differences are not wording differences.
- Tables come out cell by cell, not as Markdown tables. The indicator books'
  three columns (ชั้น | ตัวชี้วัด | สาระการเรียนรู้) appear in reading order;
  use the index when the column matters.
- Formulas are flattened (`v = s t` for v = s/t). Check any formula
  against the PDF page.
- `QUALITY.md` scores each file. Every file is below 2% unknown words; the
  remainder is names and loanwords.

## Regenerating

```bash
pip install -e .[curriculum-sources]
python scripts/curriculum_sources_to_md.py   # Markdown + QUALITY.md
python scripts/curriculum_index.py           # indicators.jsonl
```

The converter needs TH Sarabun PSK installed. It decodes most of the Thai by
the font's own glyph names, because the PDFs' text layers are unreliable:
InDesign labels า as ำ, Word drops nikhahit and the lowered mai ek to
spaces, older files use presentation-form code points, and the 2551
curriculum is Thai bytes shown through MacRoman.
