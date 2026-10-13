# OpenThaiKnowledge (otk)

**English** · [ภาษาไทย](README.th.md)

Thai curriculum knowledge as code: 3,468 problem sets, from ป.1 to ม.6 and
olympiad level, each drawing a fresh multiple-choice question with a verified
answer from a seed. Alongside them are the knowledge units they were built
from, and the tooling that turns exam sheets and textbooks into both.

Anyone can contribute by having an AI agent do the work under this
repository's rules, then reviewing what it made. See [License](#license) for
the terms the project and your contributions are published under.

## Contribute with your AI agent

You need:

- a GitHub account;
- [git](https://git-scm.com/), the [GitHub CLI](https://cli.github.com/)
  (`gh`, signed in with `gh auth login`) and [uv](https://docs.astral.sh/uv/);
- a coding agent that can run commands, such as Claude Code or Codex.

Open your agent in the folder where you keep projects, and paste this:

```text
Set up the OpenThaiKnowledge repository on this machine so I can contribute
problem sets. Do the steps in order. After each one, check that it worked; if
one fails, stop and tell me what went wrong instead of working around it.

1. Check the tools. Run `git --version`, `gh auth status` and `uv --version`.
   If git or gh is missing, or gh is not signed in, tell me how to install it
   or sign in on this operating system, and wait for me. If only uv is
   missing, offer to install it with the official installer
   (https://docs.astral.sh/uv/getting-started/installation/) and do so if I
   agree; it installs to ~/.local/bin, so add that to PATH for the rest of
   this session.
   On Windows, also set PYTHONUTF8=1 for every Python command you run here
   (the sets print Thai, which the default console code page cannot encode),
   and offer to set it permanently for my user account.

2. Get the repository. If ./openthaiknowledge already exists and is a clone of
   it, use that and skip to the remote check. If the current folder is itself
   inside another git repository, ask me where to clone instead.
   - If `gh auth status` shows I am signed in as KananatSSN (the owner), do
     not fork: run `gh repo clone KananatSSN/openthaiknowledge`; `origin` must
     be KananatSSN/openthaiknowledge and there is no `upstream`.
   - Otherwise fork and clone the fork:
       gh repo fork KananatSSN/openthaiknowledge --clone --default-branch-only
     `origin` must be my fork and `upstream` KananatSSN/openthaiknowledge.
   Then `cd openthaiknowledge`, check `git remote -v`, and tell me the full
   path of the clone.

3. Create the Python environment, in this folder only. Name the environment
   explicitly so an already active virtualenv is not changed:
     uv venv --python 3.12
     uv pip install --python .venv -e ".[test]" ruff
   (On Windows, the commands below use .venv\Scripts\ instead of .venv/bin/.)

4. Check my git identity for this repository: `git config user.name` and
   `git config user.email` must both print something. If not, ask me for them
   and set them with `git config` (without --global). Every commit here must
   be signed off with `git commit -s`.

5. Verify the setup (about a minute):
     .venv/bin/python -m pytest otk/tests/test_golden_draws.py otk/tests/test_provenance.py otk/tests/test_set_safety.py otk/tests/test_sets_layout.py -q -n auto
     .venv/bin/ruff check otk
     .venv/bin/python -c "from random import Random; from otk.api import REGISTRY; print(REGISTRY['math.count_objects_p1'].generate(Random(1)).model_dump_json(indent=1)[:600])"
   All tests must pass and ruff must report no problems.

6. Read AGENTS.md and CONTRIBUTING.md from start to end. They are the rules for
   all work in this repository. Also look at the skills in .agents/skills/ and
   at otk/sets/INDEX.md, which lists where every problem set lives.

7. List the open tasks:
     gh issue list -R KananatSSN/openthaiknowledge --label "task: indicator"
     gh issue list -R KananatSSN/openthaiknowledge --label "task: digest"
   There may be none yet.

Then report: where the clone is, what you installed or changed on this
machine (including anything that needs a new terminal to take effect), the
test results, a two-line summary of the
rules in AGENTS.md, and the open tasks. Ask me what to work on. Do not change
any file, create a branch or commit until I tell you what to do.
```

When it reports back, give it a task: an issue to close, a curriculum
indicator that needs more practice, or a source you are allowed to use. Then
review the result yourself and open a pull request.
[CONTRIBUTING.md](CONTRIBUTING.md) says what a good contribution looks like and
what review checks. [AGENTS.md](AGENTS.md) holds the rules your agent follows.

## Layout

| Path | What it holds |
|---|---|
| `otk/api.py` | **The public surface.** Consumers import from here only. |
| `otk/sets/` | **The problem sets**: `<subject>/<level>/<unit>.py`, one file per curriculum unit. [`INDEX.md`](otk/sets/INDEX.md) lists every file and its sets; each subject has a `README.md` |
| `otk/kit/` | Shared tools for writing sets: maths problems, answer choices, concept banks, classification tables, word-problem stories |
| `otk/core/` | Content model, registry, distractors, mistake vocabulary, provenance, curriculum placement, PDF worksheets |
| `otk/pictures/` | Picture and diagram drawers, the committed PNGs, and the registry of drawable diagrams |
| `otk/sheets/` | Digested past papers, one package per sheet, plus `bank.json`, the index of the source bank |
| `otk/knowledge/` | Knowledge units extracted from sources |
| `otk/tools/` | `sheetpipe` (the digestion pipeline), `golden_draws`, `explorer_data`, `sets_index`, `curriculum_graph` |
| `otk/tests/` | The suite, including `golden_draws.json` |
| `scripts/` | Content audits and exports, and `task_queue.py` (open work as GitHub issues) |
| `explorer/` | The website for exploring every set and trying its example questions |
| `.agents/skills/` | Agent skills: `sheet-bank`, `sheet-to-generator`, `sheet-transcriber` (Claude Code reaches them through `.claude/`) |
| `docs/` | Content plans, audits and the official curriculum sources |

## Develop

The setup above, by hand:

```bash
gh repo fork KananatSSN/openthaiknowledge --clone --default-branch-only
cd openthaiknowledge
uv venv --python 3.12 && uv pip install --python .venv -e ".[test]" ruff
```

Maintainers with push access clone instead of forking
(`gh repo clone KananatSSN/openthaiknowledge`). On Windows, set
`PYTHONUTF8=1` so Python can print Thai to the console.

Before opening a pull request:

```bash
.venv/bin/python -m pytest otk/tests -q -n auto   # the full suite, ~15 min on 8 cores
.venv/bin/ruff check otk
```

The Thai layout tests need a Thai font (`fonts-thai-tlwg` on Debian/Ubuntu).
`pytest -m slow` runs the thousand-seed quality gates that CI runs nightly.

Adding or changing a set:

```bash
python -m otk.tools.golden_draws --update math.new_set_p5   # record a new or intentionally changed set
python -m otk.tools.golden_draws --retire math.old_set      # after removing a set
python -m otk.tools.sets_index                              # refresh otk/sets/INDEX.md and the subject READMEs
```

## Use

```bash
pip install "openthaiknowledge @ git+https://github.com/KananatSSN/openthaiknowledge@v0.5.4"
```

```python
from random import Random
from otk.api import REGISTRY, catalog

question = REGISTRY["math.count_objects_p1"].generate(Random(42))
```

`otk config.json` prints an offline PDF worksheet from a JSON config (`otk --help`).

### What a consumer can rely on

- **Keys are permanent.** A set's key never changes meaning and is never
  reused; a removed set's key is listed as retired.
- **Seeds are stable.** The same key, seed and params give the same question
  in every release, unless the release notes name that set as changed.
- **`otk.api` is the contract.** Anything else may move between releases.

`otk/tests/test_golden_draws.py` enforces the first two: it holds a hash of
every set's draws for five fixed seeds. Each set also states its provenance
(`otk.api.provenance(key)`): original, or adapted from cited sources.

## The source bank

The sources sets are digested from (exam compilations, textbook exercise
pages, notes) are mostly third-party material, so they are not published. They
live in a separate private repository, together with their digests and
transcripts. Everything in this repository works without it; the problem sets
that were adapted from a source cite it ([SOURCES.md](SOURCES.md)), and a
rights holder can ask for any of it to be removed.

Maintainers with access clone the bank into `sheet_database/` (ignored by git):

```bash
git lfs install   # once per machine; the bank's PDFs are Git LFS objects
git clone https://github.com/KananatSSN/openthaiknowledge-bank.git sheet_database
```

Then the `sheet-bank` skill (`.agents/skills/sheet-bank`) digests sources end to
end, and `python -m otk.tools.sheetpipe bank fetch "<pattern>"` downloads the
PDFs a stage needs.

Contributors without the bank can still digest an exam paper of their own: put
it in `sheet_database/contrib/<your GitHub name>/` and use the
`sheet-to-generator` skill (see [CONTRIBUTING.md](CONTRIBUTING.md)).

## Explorer

`explorer/` is the website for exploring the sets: the curriculum board, every
set's example questions and answers, and this page. See its
[README](explorer/README.md) to run or host it.

## License

| What | License |
|---|---|
| Code: everything not listed below, including the problem sets and the question text inside them | [Apache-2.0](LICENSE) |
| Content: knowledge units (`otk/knowledge/`) and the project's own documentation | [CC BY 4.0](LICENSE-CONTENT) |
| Third-party material: the digested papers' text and figures, and whatever an adapted set cites | Not licensed by this project; it belongs to its owners, is cited in [SOURCES.md](SOURCES.md), and is removed on request |

Contributions are accepted under the same terms, certified per commit with a
DCO sign-off (`git commit -s`; see [CONTRIBUTING.md](CONTRIBUTING.md)).
