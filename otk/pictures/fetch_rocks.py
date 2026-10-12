"""Fetch the ธรณีวิทยา rock-specimen photos shipped with otk.

Unlike ``generate.py`` (which *draws* its diagrams), the rock photos backing the
``geo.rock_photo_*`` types are real hand-specimen photographs, so they are
downloaded once from Wikimedia Commons and committed alongside the drawn ones.
Run:

    python -m otk.pictures.fetch_rocks

Source: the **GeoDIL** collection (Geology Digital Image Library) on Wikimedia
Commons — studio photographs of single specimens on a plain background, released
under **CC0** (public-domain dedication, no attribution required). Every entry in
``MANIFEST`` was checked by hand: CC0, one specimen, clean background, and
visually typical of the rock it is labelled with. Field photos, outcrop shots and
extreme close-ups were rejected — a student has to identify a *specimen*.

The manifest is **pinned to exact Commons file titles**, so a re-run reproduces
byte-comparable assets instead of whatever a search returns that day. Files are
re-encoded the same way :func:`services.generator.assets` treats an
upload — metadata stripped, downscaled, saved as PNG — and additionally
quantized to a 256-colour palette, which is visually indistinguishable on these
photographs but keeps a 30-image set to a few MB in the repo.
"""

from __future__ import annotations

import urllib.parse
import urllib.request
from io import BytesIO
from pathlib import Path

from PIL import Image

_HERE = Path(__file__).parent

# Commons serves the original when no width is given; ask for a thumbnail so we
# download ~200 KB instead of ~5 MB per specimen.
_FILEPATH = "https://commons.wikimedia.org/wiki/Special:FilePath/"
_SOURCE_WIDTH = 1200          # what we ask Commons for
MAX_PX = 700                  # what we store (the quiz shows it a few hundred px wide)
PALETTE_COLORS = 256
# Commons asks automated clients to identify themselves with a contact address.
USER_AGENT = "otk-pictures/1.0 (https://github.com/; rock specimen fetch)"

# asset_id -> Commons file title (without the "File:" prefix, with extension).
# Three specimens per rock so repeated questions do not show the same picture.
MANIFEST: dict[str, str] = {
    # ── หินอัคนี ─────────────────────────────────────────────────────────────
    "rock_granite_1": "Biotite granite (GeoDIL number - 18).jpg",
    "rock_granite_2": "Biotite-hornblende granite (GeoDIL number - 21).jpg",
    "rock_granite_3": "Muscovite-biotite granite (GeoDIL number - 19).jpg",
    "rock_basalt_1": "Basalt (GeoDIL number - 455).jpg",
    "rock_basalt_2": "Vesicular basalt (GeoDIL number - 458).jpg",
    "rock_basalt_3": "Basalt with pyroxene and olivine (GeoDIL number - 390).jpg",
    "rock_obsidian_1": "Obsidian (GeoDIL number - 110).jpg",
    "rock_obsidian_2": "Obsidian (GeoDIL number - 413).jpg",
    "rock_obsidian_3": "Snowflake obsidian (GeoDIL number - 414).jpg",
    # ── หินตะกอน (หินชั้น) ───────────────────────────────────────────────────
    "rock_conglomerate_1": "Conglomerate (GeoDIL number - 466).jpg",
    "rock_conglomerate_2": "Conglomerate (GeoDIL number - 10).jpg",
    "rock_conglomerate_3": "Auriferous conglomerate (GeoDIL number - 907).jpg",
    "rock_sandstone_1": "Sandstone (GeoDIL number - 11).jpg",
    "rock_sandstone_2": "Sandstone (GeoDIL number - 474).jpg",
    "rock_sandstone_3": "Micaceous sandstone (GeoDIL number - 468).jpg",
    "rock_shale_1": "Arenaceous shale (GeoDIL number - 478).jpg",
    "rock_shale_2": "Ferruginous shale (GeoDIL number - 479).jpg",
    "rock_shale_3": "Bituminous shale (GeoDIL number - 480).jpg",
    "rock_limestone_1": "Limestone (GeoDIL number - 295).jpg",
    "rock_limestone_2": "Gray limestone (GeoDIL number - 484).jpg",
    "rock_limestone_3": "Oolitic limestone (GeoDIL number - 297).jpg",
    # ── หินแปร ───────────────────────────────────────────────────────────────
    "rock_slate_1": "Gray slate (GeoDIL number - 15).jpg",
    "rock_slate_2": "Red Slate (GeoDIL number - 421).jpg",
    "rock_slate_3": "Green slate (GeoDIL number - 422).jpg",
    "rock_marble_1": "White marble (GeoDIL number - 507).jpg",
    "rock_marble_2": "Marble (GeoDIL number - 506).jpg",
    "rock_marble_3": "Marble (GeoDIL number - 510).jpg",
    "rock_quartzite_1": "Quartzite (GeoDIL number - 328).jpg",
    "rock_quartzite_2": "Pink quartzite (GeoDIL number - 419).jpg",
    "rock_quartzite_3": "Staurolite quartzite (GeoDIL number - 336).jpg",
}


def source_url(title: str, width: int = _SOURCE_WIDTH) -> str:
    """Commons URL for a file title, as a thumbnail of the given width."""
    return f"{_FILEPATH}{urllib.parse.quote(title)}?width={width}"


def fetch(title: str) -> bytes:
    req = urllib.request.Request(source_url(title), headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=90) as resp:
        return resp.read()


def store(data: bytes, asset_id: str) -> Path:
    """Re-encode one download to the committed PNG. Mirrors ``save_upload``."""
    img = Image.open(BytesIO(data))
    img.load()
    img = img.convert("RGB")                      # drops any metadata/alpha
    img.thumbnail((MAX_PX, MAX_PX))
    img = img.quantize(colors=PALETTE_COLORS)
    dest = _HERE / f"{asset_id}.png"
    img.save(dest, format="PNG", optimize=True)
    return dest


def main() -> None:
    total = 0
    for asset_id, title in MANIFEST.items():
        dest = store(fetch(title), asset_id)
        kb = dest.stat().st_size // 1024
        total += kb
        print(f"{asset_id:<24} {kb:>5} KB   {title}")
    print(f"\n{len(MANIFEST)} assets, {total / 1024:.1f} MB")


if __name__ == "__main__":
    main()
