"""The public surface of otk: everything a consumer may rely on.

Consumers — TutorRank's generator service is the first — import from this
module only, never from ``otk.core``, ``otk.pictures`` or ``otk.tools``.
Everything else may move or change shape between releases; this may not
without a major version.

Two promises come with it, held by ``otk/tests/test_golden_draws.py``:

* A set's key is permanent. Consumers key ratings, mastery and history by it.
  A removed set's key is retired and never reused.
* ``REGISTRY[key].generate(Random(seed), **params)`` returns the same question
  for the same seed and params, release after release, unless the release
  notes name that set as changed.
"""

from __future__ import annotations

from .core.content import Block, ImageBlock, text
from .core.curriculum_math import MATH_SUBJECT, MATH_TOPIC_ASSIGNMENTS, MATH_TOPIC_RENAMES
from .core.mistakes import mistake_names
from .core.provenance import Provenance, provenance
from .core.question import Choice, PublicQuestion, Question
from .core.registry import (DEFAULT_LEVEL_SYSTEM, GENERAL_TOPIC, LEVEL_SYSTEMS, REGISTRY,
                            QuestionType, catalog, full_level, sheets, sort_key, types_in,
                            types_in_curriculum_node, types_in_sheet)
from .core.render.assets import is_diagram, shipped_asset, shipped_files
from .core.worksheet import Worksheet, build_worksheet

__all__ = [
    # Sets
    "REGISTRY", "QuestionType", "catalog", "sheets", "mistake_names",
    "provenance", "Provenance",
    "types_in", "types_in_curriculum_node", "types_in_sheet",
    "sort_key", "full_level", "LEVEL_SYSTEMS", "DEFAULT_LEVEL_SYSTEM", "GENERAL_TOPIC",
    # Questions
    "Question", "PublicQuestion", "Choice", "Block", "ImageBlock", "text",
    # Worksheets
    "Worksheet", "build_worksheet",
    # Pictures
    "is_diagram", "shipped_asset", "shipped_files",
    # Topic history: consumers that key data by topic migrate it with these
    "MATH_SUBJECT", "MATH_TOPIC_RENAMES", "MATH_TOPIC_ASSIGNMENTS",
]
