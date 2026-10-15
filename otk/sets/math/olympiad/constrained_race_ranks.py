"""Count distinct first/third-rank pairs under order and spacing rules."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def possible_rank_pairs(
    competitors: int,
    separation: int,
    *,
    b_not_first: bool = True,
    d_before_f: bool = True,
    a_before_c: bool = True,
) -> frozenset[tuple[str, str]]:
    """Enumerate feasible (first, third) finishers by pruned backtracking."""
    if competitors not in (6, 7) or not 1 <= separation < competitors:
        raise ValueError("expected six or seven competitors and a valid separation")
    labels = tuple("ABCDEFG"[:competitors])
    pairs: set[tuple[str, str]] = set()

    def extend(order: tuple[str, ...], unused: frozenset[str]) -> None:
        if not unused:
            positions = {label: order.index(label) for label in labels}
            if abs(positions["E"] - positions["A"]) == separation:
                pairs.add((order[0], order[2]))
            return
        for label in sorted(unused):
            if label == "B" and b_not_first and not order:
                continue
            if label == "A" and "B" in unused:
                continue
            if label == "C" and a_before_c and "A" in unused:
                continue
            if label == "F" and d_before_f and "D" in unused:
                continue
            extend(order + (label,), unused - {label})

    extend((), frozenset(labels))
    return frozenset(pairs)


@question_type(
    "math.constrained_race_rank_pairs_olympiad",
    display_name={"th": "นับคู่ผู้ได้อันดับหนึ่งและอันดับสามภายใต้เงื่อนไข"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="หลักการนับ",
)
class ConstrainedRaceRankPairs(WordProblem):
    def expr(self, rng: Random):
        competitors = rng.randint(6, 7)
        separation = rng.randint(2, competitors - 2)
        answer = len(possible_rank_pairs(competitors, separation))
        return MathDraw(
            rf"n={competitors},\quad d={separation}",
            str(answer),
            prompt=("ผู้เข้าแข่งขัน A, B, C, D, E, F "
                    + ("และ G " if competitors == 7 else "")
                    + "เข้าเส้นชัยไม่พร้อมกัน โดย B ไม่ได้อันดับหนึ่งและอยู่ก่อน A "
                    "อันดับของ A กับ E ห่างกัน d ตำแหน่ง D อยู่ก่อน F และ A อยู่ก่อน C "
                    "คู่ผู้ได้อันดับหนึ่งและอันดับสามที่ต่างกันเป็นไปได้กี่คู่"),
            hint="ไล่ลำดับโดยตัดกรณีที่ผิดเงื่อนไขทันที แล้วนับคู่ที่ไม่ซ้ำ",
            distractors=[
                str(len(possible_rank_pairs(competitors, separation, b_not_first=False))),  # allow B first
                str(len(possible_rank_pairs(competitors, separation, d_before_f=False))),  # reverse or omit D/F order
                str(len(possible_rank_pairs(competitors, separation, a_before_c=False))),  # omit A/C order
                str(competitors * (competitors - 1)),  # ignore all restrictions
            ],
        )
