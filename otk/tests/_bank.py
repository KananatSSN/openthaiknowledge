"""Tests that read the private source bank (digests, transcripts).

The bank is a separate repository that maintainers clone at ``sheet_database/``;
without it these tests are skipped, and everything else still runs.
"""

from __future__ import annotations

import pytest

from otk.tools.sheetpipe import bank as bk

# A contributor's own sheet_database/ (their papers under contrib/) has digests
# too, but not the bank's; only a clone of the private bank counts.
needs_bank = pytest.mark.skipif(
    not bk.has_private_bank(),
    reason="private source bank not cloned at sheet_database/ (maintainers only)")
