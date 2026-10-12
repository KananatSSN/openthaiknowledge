"""Repo-wide pytest configuration.

Two things live here: the temp-root guard, which runs before any fixture and so
belongs in the rootdir conftest rather than either suite's own, and the CI
sharding hook at the bottom.
"""

from __future__ import annotations

import getpass
import os
import shutil
import tempfile
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parent
WORKSPACE_TEMPROOT = ROOT / ".pytest-tmp"


def _usable(root: Path) -> bool:
    """Whether pytest could actually build its ``pytest-of-<user>`` tree here.

    ``os.access`` is not enough on Windows: a directory whose ACL denies this
    account still reports writable, and the failure only surfaces when a fixture
    tries to create a directory. So probe by doing the thing.
    """
    try:
        user = getpass.getuser()
    except Exception:  # pragma: no cover - getpass falls back to env vars
        user = "unknown"
    probe = root / f"pytest-of-{user}" / ".probe"
    try:
        probe.mkdir(parents=True, exist_ok=True)
        shutil.rmtree(probe)
    except OSError:
        return False
    return True


def _select_temproot() -> None:
    """Keep tmp_path working when the system temp root is not usable.

    On this project's Windows workstation ``%TEMP%\\pytest-of-<user>`` has an ACL
    that denies its own owner, so every fixture taking ``tmp_path`` errors at setup
    with WinError 5. That silently *skips* those tests — a full run reported 173
    errors and 3874 passes where the real numbers are 0 and 4047 — so it is worth
    handling rather than remembering a flag. A machine with a healthy temp
    directory takes the first branch and behaves exactly as before.
    """
    if os.environ.get("PYTEST_DEBUG_TEMPROOT"):
        return
    if _usable(Path(tempfile.gettempdir())):
        return
    WORKSPACE_TEMPROOT.mkdir(parents=True, exist_ok=True)
    os.environ["PYTEST_DEBUG_TEMPROOT"] = str(WORKSPACE_TEMPROOT)


_select_temproot()


def pytest_collection_modifyitems(config, items):
    """Keep one shard of the tests when CI splits the suite across jobs.

    ``PYTEST_NUM_SHARDS=n PYTEST_SHARD_ID=k`` keeps the tests whose node id
    hashes to k mod n. CRC32, not ``hash()``, so every job and every xdist worker
    agrees on the split. Unset (the usual case) runs everything.
    """
    shards = int(os.environ.get("PYTEST_NUM_SHARDS", "1"))
    if shards <= 1:
        return
    shard = int(os.environ["PYTEST_SHARD_ID"])
    keep, drop = [], []
    for item in items:
        (keep if zlib.crc32(item.nodeid.encode()) % shards == shard else drop).append(item)
    items[:] = keep
    config.hook.pytest_deselected(items=drop)
