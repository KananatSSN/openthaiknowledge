"""ตำแหน่งและทิศของสิ่งต่าง ๆ

ภูมิศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ส 5.1 ป.1/2, ส 5.1 ป.1/3
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.geography import (
    CLASSROOM_PLANS, LETTERS, P1, SUBJECT, choices, map_question, stage,
)

PROVENANCE = Provenance("original")


TOPIC = "ตำแหน่งและทิศของสิ่งต่าง ๆ"

NAMES = ("ต้น", "ฝน", "ดาว", "ภู", "น้ำ", "แก้ว", "บอล", "ฟ้า")
LINEUP_HINT = "ชี้ไล่จากคนซ้ายสุดไปทางขวาทีละคน ทางขวามือคือคนถัดไป ทางซ้ายมือคือคนก่อนหน้า"


@question_type(
    "geog.lineup_position_p1",
    display_name={"th": "บอกตำแหน่งซ้าย ขวา และระหว่าง ของคนที่ยืนเรียงแถว"},
    level=P1, subject=SUBJECT, topic=TOPIC,
)
@stage(1)
class LineupPosition(QuestionType):
    def build(self, rng: Random, **params):
        row = rng.sample(NAMES, 5)
        intro = ("เด็ก 5 คนยืนเรียงแถวหน้ากระดาน เรียงจากซ้ายไปขวาตามที่เรามองเห็น ได้แก่ "
                 + " ".join(row))
        ask = rng.choice(("right", "left", "between", "end"))
        if ask == "right":
            i = rng.randrange(4)
            stem, correct = f"ใครยืนอยู่ทางขวามือของ{row[i]}ติดกัน", row[i + 1]
            slip = row[i - 1] if i else None
        elif ask == "left":
            i = rng.randrange(1, 5)
            stem, correct = f"ใครยืนอยู่ทางซ้ายมือของ{row[i]}ติดกัน", row[i - 1]
            slip = row[i + 1] if i < 4 else None
        elif ask == "between":
            i = rng.randrange(3)
            stem, correct, slip = f"ใครยืนอยู่ระหว่าง{row[i]}กับ{row[i + 2]}", row[i + 1], None
        else:
            side = rng.choice(("ซ้าย", "ขวา"))
            correct, other = (row[0], row[4]) if side == "ซ้าย" else (row[4], row[0])
            stem, slip = f"ใครยืนอยู่{side}สุดของแถว", other
        rest = [n for n in row if n not in (correct, slip)]
        rng.shuffle(rest)
        wrongs = ([("direction.left_right_swapped", slip)] if slip else []) + rest
        return choices(stem=f"{intro} {stem}", correct=correct, wrongs=wrongs,
                       hint=LINEUP_HINT, topic=TOPIC)


@question_type(
    "geog.near_far_p1",
    display_name={"th": "เปรียบเทียบระยะใกล้ไกลจากโรงเรียน"},
    level=P1, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class NearFar(QuestionType):
    def build(self, rng: Random, **params):
        kids = rng.sample(NAMES, 4)
        metres = rng.sample(range(100, 1001, 50), 4)
        listed = " ".join(f"บ้านของ{k}ห่าง {m:,} เมตร" for k, m in zip(kids, metres))
        near = rng.random() < 0.5
        pick = min if near else max
        correct = kids[metres.index(pick(metres))]
        other = kids[metres.index((max if near else min)(metres))]
        word = "ใกล้" if near else "ไกล"
        return choices(
            stem=f"ระยะทางจากบ้านของเด็กแต่ละคนถึงโรงเรียน: {listed} บ้านของใครอยู่{word}โรงเรียนที่สุด",
            correct=correct, wrongs=[other, *(k for k in kids if k not in (correct, other))],
            hint="ระยะทางยิ่งน้อยยิ่งใกล้ ระยะทางยิ่งมากยิ่งไกล", topic=TOPIC)


# Every pair of desks in one row or one column of a plan: (plan, a, b).
PLAN_PAIRS = tuple(
    (spec, a, b) for spec in CLASSROOM_PLANS
    for a in range(len(spec.places)) for b in range(len(spec.places))
    if a != b and (spec.places[a][0] == spec.places[b][0] or spec.places[a][1] == spec.places[b][1])
)
SIDES = ("ทางขวามือ", "ทางซ้ายมือ", "ข้างหน้า", "ข้างหลัง")


def side_of(here: tuple[int, int], there: tuple[int, int]) -> str:
    """Where ``there`` is for someone at ``here`` facing the board (the top)."""
    dx, dy = there[0] - here[0], there[1] - here[1]
    if dy == 0:
        return SIDES[0] if dx > 0 else SIDES[1]
    return SIDES[2] if dy > 0 else SIDES[3]


@question_type(
    "geog.classroom_plan_p1",
    display_name={"th": "ใช้แผนผังห้องเรียนบอกตำแหน่งข้างหน้า ข้างหลัง ซ้าย ขวา"},
    level=P1, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class ClassroomPlan(QuestionType):
    def build(self, rng: Random, **params):
        spec, a, b = rng.choice(PLAN_PAIRS)
        correct = side_of(spec.places[a], spec.places[b])
        flip = {SIDES[0]: SIDES[1], SIDES[1]: SIDES[0], SIDES[2]: SIDES[3], SIDES[3]: SIDES[2]}
        mistake = "direction.left_right_swapped" if correct in SIDES[:2] else "direction.opposite"
        rest = [s for s in SIDES if s not in (correct, flip[correct])]
        return map_question(
            spec,
            stem=(f"แผนผังห้องเรียนนี้ ตัวอักษรแต่ละตัวคือโต๊ะของนักเรียน แถบด้านบนคือกระดานหน้าห้อง "
                  f"ถ้านั่งที่โต๊ะ {LETTERS[a]} และหันหน้าไปทางกระดาน โต๊ะ {LETTERS[b]} อยู่ทางใดของเรา"),
            correct=correct, wrongs=[(mistake, flip[correct]), *rest],
            hint="หันหน้าไปทางกระดานซึ่งอยู่ด้านบนของแผนผัง มือขวาของเราจะอยู่ทางขวาของภาพ",
            topic=TOPIC)
