"""The block content model — the heart of the rewrite.

A question is a tree of typed *blocks*, never a bitmap or a raw string. Each
renderer (KaTeX in the browser, matplotlib for print) consumes the same blocks,
so a new question kind is a new content shape, not a new render path.

The split also makes project rules structural rather than conventions:

* ``MathBlock`` holds notation-only TeX; ``TextBlock`` holds Thai. Thai cannot
  land in mathtext by construction — they are different types.
* ``ImageBlock`` carries normalized arrow/dot markers, so an image-with-arrow
  question (anatomy labelling) needs no special-case rendering.
* ``CodeBlock`` holds a program exactly as written — newlines and leading
  spaces are meaning, not layout — so it is shown in a monospace font and never
  reflowed, the way prose in a ``TextBlock`` is.

Blocks are Pydantic models: the same objects validate input, serialize to the
JSON the quiz client receives, and round-trip back — the API contract *is* the
content model.
"""

from __future__ import annotations

from typing import Annotated, Literal, Union

from pydantic import BaseModel, Field


class TextBlock(BaseModel):
    """Plain (Thai) text — a prompt line or a word answer."""
    kind: Literal["text"] = "text"
    text: str


class MathBlock(BaseModel):
    """A math expression as KaTeX/mathtext-compatible TeX, without ``$``.

    Notation only — no Thai. Thai belongs in a :class:`TextBlock`.
    """
    kind: Literal["math"] = "math"
    tex: str


class Marker(BaseModel):
    """An arrow or dot on an :class:`ImageBlock`, in normalized image coords.

    ``x``/``y`` are fractions of the image (0..1, origin top-left). ``angle`` is
    the arrow's heading in degrees (0 = pointing right); ignored for dots.
    """
    x: float = Field(ge=0.0, le=1.0)
    y: float = Field(ge=0.0, le=1.0)
    angle: float = 0.0
    style: Literal["arrow", "dot"] = "arrow"


class ImageBlock(BaseModel):
    """A diagram referenced by asset id, optionally annotated with markers."""
    kind: Literal["image"] = "image"
    asset_id: str
    markers: list[Marker] = Field(default_factory=list)
    alt: str = ""


class CodeBlock(BaseModel):
    """A short program shown as written: monospace, indentation and line breaks kept.

    ``language`` names the syntax (``"python"``) for readers and renderers; no
    renderer runs the code.
    """
    kind: Literal["code"] = "code"
    code: str
    language: str = "python"


# Discriminated union: Pydantic picks the class by the "kind" field, so a list
# of mixed blocks validates and serializes without custom logic.
Block = Annotated[
    Union[TextBlock, MathBlock, ImageBlock, CodeBlock],
    Field(discriminator="kind"),
]


# ── Convenience constructors ─────────────────────────────────────────────────
# Generators build blocks a lot; these keep call sites terse and readable.

def text(s: str) -> TextBlock:
    return TextBlock(text=s)


def math(tex: str) -> MathBlock:
    return MathBlock(tex=tex)


def image(asset_id: str, *markers: Marker, alt: str = "") -> ImageBlock:
    return ImageBlock(asset_id=asset_id, markers=list(markers), alt=alt)


def code(source: str, language: str = "python") -> CodeBlock:
    return CodeBlock(code=source, language=language)
