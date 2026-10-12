"""Tests that read the private source bank (digests, transcripts).

The bank is a separate repository that maintainers clone at ``sheet_database/``;
without it these tests are skipped, and everything else still runs.
"""

from __future__ import annotations

import pytest

from otk.tools.sheetpipe import bank as bk

needs_bank = pytest.mark.skipif(
    not (bk.DEFAULT_ROOT / "_digest").is_dir(),
    reason="source bank not cloned at sheet_database/ (maintainers only)")
