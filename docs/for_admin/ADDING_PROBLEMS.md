# Adding new problem types

A "problem" in the rewrite is a **question type**: a small class that generates a
multiple-choice question. Adding one is a one-file change — it then shows up in
the practice quiz, the catalog, the leaderboards, and the worksheet builder
automatically.

This guide covers five cases, easiest first:

1. [A math type](#1-a-math-type) — the common case.
2. [A labelled-diagram type](#2-a-labelled-diagram-image--arrow-type) — anatomy
   and any "point at the picture" question.
3. [A classify-by-category type](#3-a-classify-by-category-type) — "which group
   does this belong to?" over a table of categories → examples (most science
   concept sets).
4. [A concept-bank type](#4-a-concept-bank-type) — a fixed list of single-fact
   questions, each carrying its own hand-picked wrong answers (definitions,
   conditions, cause-and-effect).
5. [A fully custom type](#5-a-fully-custom-type) — anything else (trivia, text,
   matching, …).

> **Digesting a whole exam paper?** Don't start here. A PDF of past questions
> goes through the sheet pipeline — see
> **[DIGESTING_EXAM_SHEETS.md](DIGESTING_EXAM_SHEETS.md)** — which extracts the
> questions, keeps a cross-checked solver per question under
> [`otk/sheets/`](../../otk/sheets/), and only then produces types like the
> ones below. See [`posn2568.py`](../../otk/sets/math/olympiad/posn2568.py) for the
> worked output.

First, the mental model.

## The content model

A question is **structured data**, never a bitmap or a raw string. Everything is
built from three block types ([`otk/core/content.py`](../../otk/core/content.py)):

| Block | Holds | Rendered as |
|---|---|---|
| `TextBlock(text=...)` | Thai (or any) text | plain text |
| `MathBlock(tex=...)` | **notation-only** TeX (no `$`), e.g. `3 + 5` | KaTeX in the browser / mathtext in PDFs |
| `ImageBlock(asset_id=..., markers=[...])` | a diagram id + arrow markers | `<img>` + overlaid arrows |

Convenience constructors: `text("...")`, `math(r"...")`, `image("id", Marker(...))`.

> **Rule:** `MathBlock` TeX is notation-only — **no Thai** (a test enforces this
> for every `math.*` type). Thai instructions go in a `TextBlock` (a *prompt*).
> This is why the split exists.

A question type returns a `GeneratedQuestion(stem, correct, distractors, topic)`;
the framework materializes distractors, shuffles, and hides the correct index.
You rarely build this by hand — the base classes below do it for you.

---

## 1. A math type

Subclass `MathType` and implement one method, `expr`, returning
`(problem_tex, answer_tex)`. Decorate it with `@question_type`.

```python
# in the unit's file, e.g. otk/sets/math/p2/multiplication.py
from random import Random

from otk.core.registry import question_type
from otk.kit.math_problems import MathType


@question_type(
    "math.double",                       # unique key: "<family>.<name>"
    display_name={"th": "คูณสอง"},        # shown in the UI
    level={"th": "ป.2"},                  # groups it under ป.2 (see levels below)
    topic="คูณสอง",                       # Thai topic — powers leaderboards/badges
)
class Double(MathType):
    def expr(self, rng: Random, lo: int = 2, hi: int = 50):
        n = rng.randint(lo, hi)
        return rf"{n} \times 2", rf"{2 * n}"
```

That's the whole type. You get for free:

- 4 shuffled choices — the correct answer plus **distractors** (answers of other
  draws, padded with nearby integers for low-variety types);
- an entry in `/api/catalog`, so it appears in the quiz and the builder;
- worksheet-PDF rendering;
- `lo` and `hi` as **tunable range controls** (see below).

### Where it goes

A set lives in its curriculum unit's file,
`otk/sets/<subject>/<level>/<unit>.py` (find the unit in
[`otk/sets/INDEX.md`](../../otk/sets/INDEX.md) or the subject's `README.md`).
Add the class there and it registers on import; keep the file's sets in stage
order. A unit with no file yet gets a new one — see §2c.

### Per-item prompt / hint / topic

Return a `MathDraw` instead of a tuple when you need a Thai prompt line, a hint,
or a per-item topic:

```python
@question_type("math.next_even", display_name={"th": "จำนวนคู่ถัดไป"},
               level={"th": "ป.1"})
class NextEven(MathType):
    def expr(self, rng: Random, lo: int = 2, hi: int = 98):
        n = rng.randrange(lo, hi, 2)
        return MathDraw(rf"{n}", rf"{n + 2}",
                        topic="จำนวนคู่",
                        prompt="จงเขียนจำนวนคู่ถัดไป")   # Thai lives here, not in TeX
```

`MathDraw` fields: `problem_tex`, `answer_tex`, `topic=""`, `prompt=""`,
`hint=""`, `distractors=[]`, `figure=""`, `figure_alt=""`.

### Giving a question a diagram

Set `figure` to an asset id and it renders under the stem, in the browser and in
the worksheet PDF alike:

```python
return MathDraw("", answer, prompt="…", figure="sheet-posn2568_math-q29")
```

If *every* draw of a type shows the same diagram, override `default_figure()`
instead of repeating the id — that is how questions digested from an exam sheet
keep the sheet's own figure (see
[`DIGESTING_EXAM_SHEETS.md`](DIGESTING_EXAM_SHEETS.md)). With a default in place,
`figure=""` inherits it and `figure=None` suppresses it for one draw.

The rule for a shared diagram is that it may only show what every draw has in
common. A picture of the constants themselves contradicts the stem the moment
they are redrawn.

### Reuse the TeX helpers

Common builders live at the top of
[`otk/kit/math_problems.py`](../../otk/kit/math_problems.py) (right above
`MathType`): `frac_tex`, `frac_answer_tex`,
`rand_proper(rng, den_lo=2, den_hi=12)` (random reduced fraction), `poly_tex`,
`binomial_tex`, `mono_tex`, `sqrt_tex`, `paren`. Prefer these over hand-writing
TeX.

---

## Tunable parameters

Any **keyword argument with a numeric default** on `expr` (int/float, not bool)
becomes a tunable parameter — discovered automatically. In `Double` above, `lo`
and `hi` become range inputs in the worksheet builder and can be overridden per
worksheet:

```json
{ "generators": { "math.double": { "weight": 2, "params": { "lo": 10, "hi": 99 } } } }
```

No extra wiring — declaring `def expr(self, rng, lo=2, hi=50)` is all it takes.
(For a custom type the same rule applies to its `build` method — `ask` on a
classify type in §3, or the chemistry example in §5.)

---

## 2. A labelled-diagram (image + arrow) type

This is the anatomy-style tool: show a diagram with an arrow at one part, ask for
its name, offer sibling part-names as choices.

### 2a. Provide the image (asset)

Diagrams are served at `/v1/assets/<asset_id>` from two places
([`services/generator/assets.py`](../../services/generator/assets.py)):

- **Built-in** — drop a PNG in
  [`otk/pictures/`](../../otk/pictures/); the file
  `heart.png` is served as asset id `heart`. Keep this for photos (the rock
  samples); anything that can be drawn in code should be generated instead.
- **Generated diagram** (math or science) — not a file at all: register its spec tuple and
  drawing function in
  [`otk/pictures/registry.py`](../../otk/pictures/registry.py) and the
  generator draws each picture the first time it is requested (see that
  module's docstring).
- **Sheet figure** — a figure digested alongside a past paper, under
  `otk/sheets/<sheet_id>/figures/`, addressed by its generated id.

Both are immutable repository content. The generator resolves nothing else
([`resolve_public_asset`](../../services/generator/assets.py)); user-uploaded
images live in Supabase Storage, not here.

`asset_id` must match `^[A-Za-z0-9_.-]{1,64}$`.

### 2b. Define the type

Subclass `LabeledDiagramType` and return a list of `Part`s. Markers use
**normalized 0..1 coordinates** (origin top-left), so they line up with the
image regardless of pixel size.

```python
# in the unit's file under otk/sets/biology/
from otk.core.content import Marker
from otk.core.registry import question_type
from otk.sets.biology.m4.skeleton import LabeledDiagramType, Part


@question_type("anatomy.heart", display_name={"th": "หัวใจ"},
               level={"th": "ม.5"}, topic="กายวิภาค: หัวใจ")
class HeartLabel(LabeledDiagramType):
    _PARTS = [
        Part("heart", Marker(x=0.30, y=0.25), "เอเทรียมขวา"),
        Part("heart", Marker(x=0.70, y=0.25), "เอเทรียมซ้าย"),
        Part("heart", Marker(x=0.35, y=0.65), "เวนตริเคิลขวา"),
        Part("heart", Marker(x=0.65, y=0.65), "เวนตริเคิลซ้าย"),
    ]

    def parts(self):
        return self._PARTS
```

`Part(asset_id, marker, label)`. Distractors are the other labels in the list
(via `label_pool`), so provide **at least 4** parts for four choices.

### 2c. A new unit file

A unit with no file yet gets `otk/sets/<subject>/<level>/<unit>.py`: an English
ASCII name, a docstring whose first line is the unit's Thai title, and
`PROVENANCE` (see `AGENTS.md`). Import it in the level's `__init__.py`:

```python
from . import heart  # noqa: F401
```

Then regenerate the guides: `python -m otk.tools.sets_index`.
`otk/tests/test_sets_layout.py` fails if either step is missed.

---

## 3. A classify-by-category type

A huge share of science สาระ reduces to one shape: a few **categories**, each with
a list of real **examples** (or properties), and you ask the student to sort them.
`ClassifyType` ([`otk/kit/classify.py`](../../otk/kit/classify.py))
builds that from a table alone — no `build` method to write. It powers ชีวะ
(นิเวศวิทยา), เคมี ป.6 (สารในชีวิตประจำวัน), ฟิสิกส์ (คลื่นและแสง) and ดาราศาสตร์
(ระบบสุริยะ).

Subclass it, set `CATEGORIES` and two Thai **stem templates**, and decorate:

```python
# in the unit's file under otk/sets/
from otk.core.registry import question_type
from otk.kit.classify import Category, ClassifyType


@question_type("ecology.feeding",
               display_name={"th": "การจัดกลุ่มสิ่งมีชีวิต (ตามพฤติกรรมการกิน)"},
               level={"th": "ป.6"}, subject="ชีวะ", topic="สิ่งมีชีวิตกับสิ่งแวดล้อม")
class FeedingGroups(ClassifyType):
    CLASSIFY_STEM = "“{member}” จัดอยู่ในกลุ่มใดเมื่อแบ่งตามพฤติกรรมการกิน"
    PICK_STEM = "สัตว์ในข้อใดจัดเป็น{category}"

    CATEGORIES = [
        Category("สัตว์กินพืช (Herbivore)",  ("วัว", "ช้าง", "กระต่าย", "ยีราฟ")),
        Category("สัตว์กินสัตว์ (Carnivore)", ("เสือ", "งู", "เหยี่ยว", "จระเข้")),
        Category("สัตว์กินทั้งพืชและสัตว์ (Omnivore)", ("มนุษย์", "หมู", "ไก่", "หมี")),
    ]
```

From that one table you get **two** question styles, drawn at random per item:

- **classify** (`CLASSIFY_STEM`, fills `{member}`) — show one example, ask which
  category it's in. Distractors are the *other* category labels.
- **pick** (`PICK_STEM`, fills `{category}`) — name a category, ask which example
  belongs to it. Distractors are examples drawn **only from the other
  categories**, so exactly one choice is ever right, however they shuffle.

The `ask` parameter (a tunable, like a math type's `lo`/`hi`) pins one style —
`1` = classify, `2` = pick — or `0` draws one per item. So a worksheet can drill
just one direction.

Two rules keep the choices honest, both worth respecting when you write the table:

- **Every example belongs to exactly one category.** A shared example would make a
  `classify` question have two right answers. A test enforces this per type.
- **Give each category enough examples** that a `pick` question can find distinct
  distractors — with only two categories, a `classify` item has just two choices
  (valid, but thin).

Wrap the `{member}` in “…” (as above) so it reads as a quoted item; the shared
tests rely on that to recover the example. That's the whole type — it self-registers
and flows into the catalog, quiz, and builder like any other.

---

## 4. A concept-bank type

Some สาระ is neither a calculation nor a category table: it's a set of concept
questions, each with one correct statement and its *own* hand-picked wrong ones
(a definition, a condition, a cause-and-effect). `ConceptBankType`
([`otk/kit/concept_bank.py`](../../otk/kit/concept_bank.py)) holds that
bank and draws one item per question; because each item ships its own distractors,
the choices stay diagnostic instead of random. It powers concept หัวข้อ across
เคมี, ฟิสิกส์ and ดาราศาสตร์ (e.g. `astro.gravity`, `astro.seasons`,
`phys.dispersion`).

Set `ITEMS` to a list of `Concept(stem, correct, distractors)` and decorate —
nothing else:

```python
# in the unit's file under otk/sets/astronomy/
from otk.core.registry import question_type
from otk.kit.concept_bank import Concept, ConceptBankType


@question_type("astro.day_night",
               display_name={"th": "กลางวัน-กลางคืน"},
               level={"th": "ม.3"}, subject="ดาราศาสตร์", topic="ระบบสุริยะ")
class DayNight(ConceptBankType):
    ITEMS = [
        Concept("การเกิดกลางวันและกลางคืนบนโลกเกิดจากสิ่งใด",
                "โลกหมุนรอบตัวเอง",
                ("โลกโคจรรอบดวงอาทิตย์",
                 "ดวงจันทร์บังดวงอาทิตย์เป็นช่วง ๆ",
                 "แกนโลกเอียงประมาณ 23.5 องศา")),
        # … more items
    ]
```

Each `Concept` is one four-choice question: its `correct` plus its three
`distractors`, drawn straight through `label_pool` (§5). Give **at least three
distractors per item** for a full four choices, and — like every type — make the
wrong answers *plausible* siblings so the choice set actually tests the concept.
It self-registers and flows into the catalog, quiz, and builder like any other.

---

## 5. A fully custom type

For anything that isn't math, a labelled diagram, or a category table, subclass
`QuestionType` directly and implement `build(rng, **params)` → `GeneratedQuestion`.
You assemble the stem from blocks and pick a distractor strategy.

```python
from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type


@question_type("trivia.capitals", display_name={"th": "เมืองหลวง"})
class Capitals(QuestionType):
    _DATA = {"ไทย": "กรุงเทพฯ", "ญี่ปุ่น": "โตเกียว",
             "ฝรั่งเศส": "ปารีส", "อียิปต์": "ไคโร"}

    def build(self, rng, **params):
        country = rng.choice(list(self._DATA))
        return GeneratedQuestion(
            stem=[text(f"เมืองหลวงของ{country}คือ?")],
            correct=[text(self._DATA[country])],
            distractors=label_pool(list(self._DATA.values())),
            topic="เมืองหลวง",
        )
```

### A family over one data table

When several types quiz *different facts about the same rows*, put the table and
the drawing logic in one base class and let each type say only what it asks and
what a choice looks like. [`otk/sets/_support/chemistry.py`](../../otk/sets/_support/chemistry.py)
is the worked example: one table of all 118 elements feeds five types, from
`chem.symbol_to_name` to `chem.particles`.

(If your table is just *categories → examples* and the only questions are "which
group is this?" / "which is an example of this group?", you don't need a custom
family at all — reach for [`ClassifyType`](#3-a-classify-by-category-type) in §3,
which is that base already written. Build a custom family like `ElementType` only
when you ask *several different facts* about each row.)

```python
class ElementType(QuestionType):
    @abstractmethod
    def stem(self, it): ...          # what the question shows
    @abstractmethod
    def answer(self, it): ...        # what one choice looks like

    def alternates(self, it):        # optional near misses, offered first
        return []

    def question(self, draw):        # draw() is re-called for each distractor
        it = draw()
        return GeneratedQuestion(
            stem=self.stem(it), correct=self.answer(it),
            distractors=combine(fixed(*self.alternates(it)),
                                sibling_answers(lambda: self.answer(draw()))),
            topic=self.topic)

    def build(self, rng, group_lo=0, group_hi=8, z_lo=1, z_hi=118):
        pool = element_pool(group_lo, group_hi, z_lo, z_hi)   # ← tunable range
        return self.question(lambda: Item(rng.choice(pool), self.ASKS[0]))
```

Four things worth copying:

- **Restrict the pool, not the question.** Drawing distractors from the *same*
  filtered pool means a "หมู่ 1 only" sheet can't show a หมู่ 8 answer. A pool
  smaller than four yields fewer choices — real ones — instead of invented facts.
- **Numeric kwargs on `build` are the range controls** (`group_lo`, `z_hi`, …),
  discovered exactly like a math type's `lo`/`hi`. A subclass that needs another
  knob (`ion_chance`) overrides `build` to declare it and delegates back to
  `question()`.
- **Draw the item, then hold it fixed.** When one type can ask several things
  (โปรตอน/นิวตรอน/อิเล็กตรอน), pick the variant *once* per question so the
  distractors answer the same question. Exposing it as an `ask` param — `0` draws
  one per item, `1..n` pins one — lets a worksheet drill exactly one of them.
- **Name the near miss.** `alternates()` puts the specific mistake the item is
  built to catch (เลขอะตอม when เลขมวล was asked) in front of the sampled
  distractors, which is what makes the choice set diagnostic rather than random.

### Distractor strategies

A strategy is a callable `strategy(correct, rng, need) -> list[list[Block]]`
returning up to `need` distinct distractor contents. Built-ins
([`otk/core/distractors.py`](../../otk/core/distractors.py)):

| Strategy | Use |
|---|---|
| `sibling_answers(sample)` | draw more items and use their answers (math default) |
| `numeric_neighbors()` | pad an integer answer with ±1, ±2, … |
| `label_pool(labels)` | pick from a fixed set of text labels (diagrams, trivia) |
| `combine(a, b, ...)` | run strategies in order until enough are found |

Write your own by returning a matching callable from `build()`.

---

## How it flows through the app

Once registered, a type needs **no other changes**:

- **Catalog / quiz** — `GET /api/catalog` lists it (grouped by level); the quiz
  serves it via `POST /api/practice`. The correct index is sealed in a signed
  token and never sent to the browser.
- **Worksheets** — the builder lets teachers pick it; `math.*` types render into
  the PDF. (Image questions currently show alt-text in PDFs; they're online-first.)
- **Leaderboards & badges** — driven by the `topic` string you set.

### School levels

`level={"th": "..."}` must be one of the ordered levels in `LEVEL_SYSTEMS["th"]`
([`otk/core/registry.py`](../../otk/core/registry.py)):

```
ป.1 ป.2 ป.3 ป.4 ป.5 ป.6  ม.1 ม.2 ม.3 ม.4 ม.5 ม.6  เทคนิคคิดเลขเร็ว
```

Anything else (or omitting it) drops the type into the trailing **อื่น ๆ**
("other") group.

---

## Testing your type

The property test in
[`otk/tests/test_core.py`](../../otk/tests/test_core.py) is **parametrized over
every registered type**, so a new type is covered the moment you add it. Run:

```
python -m pytest otk/tests/test_core.py
```

It checks each type produces a valid question with 2–4 distinct choices, never
leaks the answer, round-trips through JSON, and — for `math.*` — puts **no Thai
in `MathBlock` TeX**. Add a targeted correctness test if the answer is worth
pinning (see `test_addition_answer_is_correct`).

## Where a set appears on the learning map

The `/skills` learning map is drawn from the catalog alone: one column per subject,
one row per ระดับชั้น, and a card per หัวข้อ (or curriculum node) holding its sets.
A new type appears there as soon as its `subject`, `level` and `topic` are right
and the catalog is republished; there is nothing else to register. (The radial
math skill tree and its `otk/core/skilltree.py` were retired on 2026-09-29.)

## Checklist

- [ ] Class in its unit's file, `otk/sets/<subject>/<level>/<unit>.py`;
      `@question_type("<family>.<name>", ...)` with a Thai `display_name`, a valid
      `level`, and a `topic`.
- [ ] New **unit file** only: imported in its level's `__init__.py`, and
      `python -m otk.tools.sets_index` run.
- [ ] Math TeX is notation-only; Thai is in a prompt/`TextBlock`.
- [ ] Always use the passed `rng` (never the global `random`) — worksheets must
      be reproducible.
- [ ] Diagram types: the `asset_id` resolves (built-in PNG or uploaded) and there
      are ≥ 4 parts.
- [ ] `pytest otk/tests/test_core.py` is green.
