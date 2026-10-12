"""sheetpipe — turn a scanned/typeset exam sheet (PDF) into working generators.

The pipeline is four stages, each with its own artifact, so a sheet can be picked
up again months later without re-deriving anything:

    1. **extract**  PDF ──▶ ``extract/`` (page text, item split, figure renders)
    2. **scaffold** ──▶ ``sheet.json`` + ``qNN.py`` solver stubs (one per question)
    3. **solve**    fill each stub in — this is the only stage a human/model does
    4. **verify**   check every solver against its own independent cross-check,
                    over the original constants *and* a randomized parameter grid

Only stage 3 is judgement. Stages 1, 2 and 4 are mechanical and live here.

The unit the later stages care about is the **solver module contract**
(:mod:`otk.tools.sheetpipe.spec`): a question is "digested" when a module
exposes ``PARAMS``/``ANSWER``/``solve()`` and — crucially — a second,
independent ``check()``. Agreement between two independently written methods
across randomized constants is what licenses the claim that a generator built on
``solve()`` is correct for constants nobody has ever checked by hand.

See ``.agents/skills/sheet-to-generator/SKILL.md`` for the worked procedure.
"""

from .spec import ItemSpec, SheetSpec, load_sheet, solver_modules
from .verify import VerifyResult, verify_item, verify_sheet

__all__ = ["ItemSpec", "SheetSpec", "load_sheet", "solver_modules",
           "VerifyResult", "verify_item", "verify_sheet"]
