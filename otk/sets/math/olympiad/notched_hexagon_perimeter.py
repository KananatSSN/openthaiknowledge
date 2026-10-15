"""Close a notched equiangular-edge hexagon to recover its perimeter."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def notched_hexagon_lengths(longest: int, shortest: int) -> tuple[int, int, int]:
    """Return the two unmarked sides and perimeter from vector closure."""
    if shortest < 1 or longest <= 4 * shortest:
        raise ValueError("the three short sides must be strictly shortest")
    sloping = longest - 3 * shortest
    base = longest - 2 * shortest
    perimeter = longest + 3 * shortest + sloping + base
    return sloping, base, perimeter


@question_type(
    "math.notched_hexagon_perimeter_olympiad",
    display_name={"th": "รอบรูปหกเหลี่ยมเว้าจากทิศทางของด้าน"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="รูปหลายเหลี่ยม",
)
class NotchedHexagonPerimeter(WordProblem):
    def expr(self, rng: Random):
        shortest = rng.randint(2, 8)
        longest = rng.randint(5 * shortest, 10 * shortest)
        _, _, answer = notched_hexagon_lengths(longest, shortest)
        return MathDraw(
            rf"L={longest},\quad s={shortest}",
            str(answer),
            prompt=("รูปหกเหลี่ยมเว้ามีด้านสามด้านยาว s และด้านยาวที่สุดหนึ่งด้านยาว L "
                    "เมื่อเดินรอบรูปจากฐานล่างไปทางขวา ทิศทางของด้านทั้งหกเทียบกับแกนแนวนอน "
                    "ตามลำดับคือ 0°, 120°, 240°, 300°, 240° และ 300° "
                    "ด้านที่สาม สี่ และหกยาว s ส่วนด้านที่สองยาว L จงหาความยาวรอบรูป"),
            hint="แยกการปิดรูปตามแกนแนวนอนและแนวตั้งเพื่อหาสองด้านที่ไม่ทราบ",
            distractors=[
                str(3 * longest),  # ignore the notch correction
                str(3 * longest - shortest),  # subtract only one short side
                str(3 * longest - 3 * shortest),  # subtract one short side too many
                str(longest + 3 * shortest),  # count only labelled sides
            ],
        )
