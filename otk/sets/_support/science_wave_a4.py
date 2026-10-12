"""Wave A slice 4 — the ม.3 optics cluster.

Four physical-science topics that each held only one or two stages:

* ``ว 2.3 ม.3/14`` ภาพจากกระจกเงา — Foundation and Application
* ``ว 2.3 ม.3/16`` ภาพจากเลนส์ — Foundation and Application
* ``ว 2.3 ม.3/17`` ทัศนอุปกรณ์และการมองเห็น — Fluency and Application
* ``ว 2.3 ม.3/19`` ความสว่างและการมองเห็น — Foundation and Application

Every legacy set keeps its key, stage, and meaning.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.question import GeneratedQuestion

PHYSICS = "ฟิสิกส์"
WAVES = "คลื่นและแสง"


def _distinct(correct: str, candidates: list[str], want: int = 3) -> tuple[str, ...] | None:
    """`want` distractors that differ from each other and from the answer."""
    out: list[str] = []
    for value in candidates:
        if value != correct and value not in out:
            out.append(value)
    return tuple(out[:want]) if len(out) >= want else None


def _question(*, stem: str, correct: str, wrongs: tuple[str, ...],
              hint: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=WAVES,
        hint=[text(hint)],
    )


# The four image descriptions ม.3 uses for mirrors and thin lenses. Each question
# that asks "what is the image like" draws its distractors from this same list, so
# a wrong answer is always another real image type rather than an invented one.
IMAGE_REAL_SMALLER = "ภาพจริง หัวกลับ ขนาดเล็กกว่าวัตถุ"
IMAGE_REAL_SAME = "ภาพจริง หัวกลับ ขนาดเท่ากับวัตถุ"
IMAGE_REAL_LARGER = "ภาพจริง หัวกลับ ขนาดใหญ่กว่าวัตถุ"
IMAGE_VIRTUAL_LARGER = "ภาพเสมือน หัวตั้ง ขนาดใหญ่กว่าวัตถุ"
IMAGE_VIRTUAL_SMALLER = "ภาพเสมือน หัวตั้ง ขนาดเล็กกว่าวัตถุ"

IMAGE_TYPES = (
    IMAGE_REAL_SMALLER,
    IMAGE_REAL_SAME,
    IMAGE_REAL_LARGER,
    IMAGE_VIRTUAL_LARGER,
    IMAGE_VIRTUAL_SMALLER,
)

# Focal lengths that keep every region boundary (f, 2f) a whole centimetre and
# leave room for at least one integer distance strictly between f and 2f.
FOCAL_LENGTHS = (5, 6, 8, 10, 12, 15, 20)


def _image_wrongs(correct: str, rng: Random) -> tuple[str, ...]:
    others = [value for value in IMAGE_TYPES if value != correct]
    rng.shuffle(others)
    return tuple(others[:3])


def _converging_image(distance: int, focal: int) -> str:
    """The image a converging mirror or thin convex lens forms at this distance."""
    if distance > 2 * focal:
        return IMAGE_REAL_SMALLER
    if distance == 2 * focal:
        return IMAGE_REAL_SAME
    if distance > focal:
        return IMAGE_REAL_LARGER
    return IMAGE_VIRTUAL_LARGER


def _converging_distance(rng: Random, focal: int) -> int:
    """A distance in one of the four regions a ม.3 ray diagram distinguishes."""
    region = rng.randrange(4)
    if region == 0:
        return 2 * focal + rng.randint(1, focal)
    if region == 1:
        return 2 * focal
    if region == 2:
        return rng.randint(focal + 1, 2 * focal - 1)
    return rng.randint(1, focal - 1)


# ══ ว 2.3 ม.3/14 — ภาพจากกระจกเงา ═════════════════════════════════════════════


# ══ ว 2.3 ม.3/16 — ภาพจากเลนส์ ════════════════════════════════════════════════


# ══ ว 2.3 ม.3/17 — ทัศนอุปกรณ์และการมองเห็น ══════════════════════════════════


# ══ ว 2.3 ม.3/19 — ความสว่างและการมองเห็น ════════════════════════════════════


