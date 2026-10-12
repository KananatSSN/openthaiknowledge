"""Final tidying of generated mathematics TeX.

String-built algebra writes a unit coefficient as ``1x``, ``-1y``, ``e^{1x}``
or ``1 \\cdot 2^{x}``. A book writes ``x``, ``-y``, ``e^{x}`` and ``2^{x}``.
Generators fix this one by one (``coef_term``, ``mono_tex``), but eighteen
did not, so it is applied once more to every mathematics item as it is built.

Only a lone 1 directly before a single-letter variable, or before ``\\cdot``,
is dropped: ``11x``, ``0.1x`` and ``\\frac{1}{x}`` are left alone.
"""

from __future__ import annotations

import re

_UNIT_BEFORE_VARIABLE = re.compile(r"(?<![\d.])1(?=[a-z](?![a-zA-Z]))")
_UNIT_TIMES = re.compile(r"(?<![\d.])1\s*\\cdot\s*")


def tidy_unit_coefficients(tex: str) -> str:
    return _UNIT_TIMES.sub("", _UNIT_BEFORE_VARIABLE.sub("", tex))
