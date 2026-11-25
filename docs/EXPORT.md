# Exporting otk for apps that don't run Python

`python -m otk.tools.export` writes a release of otk as plain JSON and PNG files. An
app in TypeScript, Swift or anything else can then use the problem sets without porting
any generator: it reads the questions otk drew, with their answers, hints, named
mistakes and pictures.

```bash
python -m otk.tools.export out/                              # every set, seeds 0-199
python -m otk.tools.export out/ --prefix math. --level ม.2   # one grade of maths
python -m otk.tools.export out/ --key math.count_objects_p1 --seeds 20
```

`--key`, `--prefix`, `--subject` and `--level` can each be repeated. A set is exported
when it passes every kind of filter you give. `--jobs` sets the number of worker
processes (default: one per core).

For a consumer, run it from an otk release tag, not an arbitrary commit, so the release
notes tell you what changed between two exports:

```bash
git checkout v0.17.0 && python -m otk.tools.export ../my-app/otk-data
```

## What you get

```
out/
  manifest.json          format, otk version and commit, seeds, filters, counts
  catalog.json           one row per set, and the name of every mistake
  questions/<key>.json   that set's distinct questions, each with its seed
  pictures/<asset>.png   every picture any exported question shows
  otk-export.d.ts        TypeScript types for all of the above
```

`otk-export.d.ts` is the full schema. Copy it into your app. In short:

- **A question** has `stem`, `choices`, the `answer` index, a `hint`, and `mistakes`.
  `mistakes` lines up with `choices`: for each wrong choice it gives the key of the
  mistake that choice stands for, or `null`. `catalog.json` → `mistakes` holds each
  key's Thai and English name.
- **Content** is a list of blocks: `text`, `math` (KaTeX-compatible TeX without `$`),
  `image` (show `pictures/<asset_id>.png`, with optional arrow or dot `markers` given
  as fractions of the picture) and `code`.
- **`seed`** is the seed otk drew the question from. Store `{key, seed}` to bring a
  question back later. `REGISTRY[key].generate(Random(seed))` in Python gives the same
  question.
- **Repeats are dropped.** Seeds whose question is identical to an earlier one's are
  left out, so the seeds in a file have gaps. A set's row in the catalog gives
  `questions`, the number kept. It also gives `stems`, the number of different stems
  among them, which is the set's real variety: a paper's question with three variants
  has 4 stems, however many seeds shuffle their choices.

## Guarantees

The export carries otk's promises to consumers (see the README):

- **Keys are permanent.** A key keeps its meaning and is never reused.
- **A seed keeps its question** from release to release, unless the release notes name
  the set as changed.
- **Byte-identical output.** The same release and options always give identical files,
  so `diff -r` between two exports lists exactly the sets and pictures a release changed.

## Size

At v0.17.0 and the default 200 seeds, an export of every set:

- takes about 5 minutes on 8 cores;
- holds 5,950 sets, about 1.09 million questions and 3,724 pictures;
- is about 1.1 GB on disk, but about 58 MB gzipped, because the questions repeat a lot
  of structure.

Export or ship it by grade or subject, compress it, and load a set's file when it is
first needed. Fewer seeds make it proportionally smaller.

## The answers are in the files

otk's own API never sends the answer index or the mistake labels to a browser.
TutorRank keeps them on its server. This export contains both, because an offline app
has to mark answers itself. If cheating matters to your app (a ranked mode, a prize),
keep the files on a server and send questions without `answer` and `mistakes`.

## Pictures and your own art

Pictures are drawn into a fresh directory on every run, so an export never ships a
picture cached by an older release. Two environment variables change that:

- `GENERATOR_DIAGRAM_DIR` reuses a picture cache between runs.
- `GENERATOR_OBJECT_SPRITES` names a folder of painted sprites (`apple.png`, `fish.png`,
  …). otk then draws its counting pictures with them instead of flat shapes
  (`otk/pictures/counting_pictures.py`).

A question refers to a picture only by its asset id. Redrawing a picture under the
same id changes no question, so an app can also replace a file in `pictures/` with its
own art for that id.
