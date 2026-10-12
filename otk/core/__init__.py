"""otk core domain — content model, question types, registry.

Web- and DB-free by design (nothing here imports the API or the database), the
same boundary the old ``hw_generator`` kept from ``webapp``. Importing this
package registers all built-in question types.
"""

from __future__ import annotations

from .content import (Block, CodeBlock, ImageBlock, Marker, MathBlock, TextBlock,
                      code, image, math, text)
from .question import Choice, GeneratedQuestion, PublicQuestion, Question
from .registry import (DEFAULT_SUBJECT, GENERAL_TOPIC, LEVEL_SYSTEMS, REGISTRY,
                       QuestionType, catalog, full_level, generate,
                       question_type, search, sort_key, topics_in, types_in)
from .. import sets as _sets  # noqa: F401  (registers every problem set)

__all__ = [
    "Block", "TextBlock", "MathBlock", "ImageBlock", "CodeBlock", "Marker",
    "text", "math", "image", "code",
    "Question", "Choice", "PublicQuestion", "GeneratedQuestion",
    "QuestionType", "question_type", "REGISTRY", "catalog", "generate",
    "search", "sort_key", "types_in", "topics_in", "full_level",
    "LEVEL_SYSTEMS", "DEFAULT_SUBJECT", "GENERAL_TOPIC",
]
