"""ทิศและแผนที่ชุมชน

ภูมิศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ส 5.1 ป.3/1
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.geography import (
    CARDINAL, COMMUNITY_MAPS, DIRECTIONS, LETTERS, P3, SUBJECT, bearing, choices,
    map_question, mirrored, stage, turned,
)

PROVENANCE = Provenance("original")


TOPIC = "ทิศและแผนที่ชุมชน"

PLACES = ("โรงเรียน", "วัด", "ตลาด", "สถานีอนามัย", "สวนสาธารณะ", "ที่ทำการไปรษณีย์",
          "ห้องสมุดชุมชน", "สถานีตำรวจ", "บ้านของฉัน")
TURN_HINT = ("เมื่อหันหน้าไปทางทิศเหนือ ขวามือคือทิศตะวันออก ซ้ายมือคือทิศตะวันตก ข้างหลังคือทิศใต้ "
             "หันไปทิศอื่นก็หมุนทั้งหมดตามไปเท่ากัน")


@question_type(
    "geog.facing_direction_p3",
    display_name={"th": "บอกทิศทางขวามือ ซ้ายมือ และข้างหลัง เมื่อหันหน้าไปทางทิศหนึ่ง"},
    level=P3, subject=SUBJECT, topic=TOPIC,
)
@stage(1)
class FacingDirection(QuestionType):
    def build(self, rng: Random, **params):
        facing = rng.choice(CARDINAL if rng.random() < 0.6 else DIRECTIONS)
        side = rng.choice(("ขวามือ", "ซ้ายมือ", "ข้างหลัง"))
        right, left, back = turned(facing, 2), turned(facing, -2), turned(facing, 4)
        if side == "ขวามือ":
            correct, wrongs = right, [("direction.left_right_swapped", left), back, facing]
        elif side == "ซ้ายมือ":
            correct, wrongs = left, [("direction.left_right_swapped", right), back, facing]
        else:
            correct, wrongs = back, [("direction.opposite", facing), right, left]
        return choices(stem=f"ยืนหันหน้าไปทาง{facing} {side}ของเราคือทิศใด",
                       correct=correct, wrongs=wrongs, hint=TURN_HINT, topic=TOPIC)


@question_type(
    "geog.turning_direction_p3",
    display_name={"th": "หาทิศที่หันไปเมื่อหมุนตัวตามหรือทวนเข็มนาฬิกา"},
    level=P3, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class TurningDirection(QuestionType):
    def build(self, rng: Random, **params):
        facing = rng.choice(DIRECTIONS)
        eighths = rng.choice((1, 2, 3))
        clockwise = rng.random() < 0.5
        sign = 1 if clockwise else -1
        correct = turned(facing, sign * eighths)
        way = "ตามเข็มนาฬิกา" if clockwise else "ทวนเข็มนาฬิกา"
        wrongs = [("direction.left_right_swapped", turned(facing, -sign * eighths)),
                  turned(facing, sign * (eighths + 1)), turned(facing, sign * (eighths - 1)),
                  turned(facing, 4)]
        return choices(
            stem=f"ยืนหันหน้าไปทาง{facing} แล้วหมุนตัว{way} {45 * eighths} องศา จะหันหน้าไปทางทิศใด",
            correct=correct, wrongs=wrongs,
            hint="ทิศหลักและทิศรองมี 8 ทิศ ห่างกันทิศละ 45 องศา ตามเข็มนาฬิกาเรียงจากเหนือ ตะวันออกเฉียงเหนือ ตะวันออก ...",
            topic=TOPIC)


# Every pair of places on a map that line up exactly: (map, from, to, direction).
MAP_PAIRS = tuple(
    (spec, a, b, way) for spec in COMMUNITY_MAPS
    for a, pa in enumerate(spec.places) for b, pb in enumerate(spec.places)
    if a != b and (way := bearing(pb[0] - pa[0], pb[1] - pa[1]))
)


@question_type(
    "geog.map_direction_p3",
    display_name={"th": "ใช้แผนที่ชุมชนบอกทิศของสถานที่หนึ่งเทียบกับอีกที่หนึ่ง"},
    level=P3, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class MapDirection(QuestionType):
    def build(self, rng: Random, **params):
        spec, a, b, way = rng.choice(MAP_PAIRS)
        here, there = rng.sample(PLACES, 2)
        wrongs = [("direction.opposite", turned(way, 4)),
                  ("direction.left_right_swapped", mirrored(way)),
                  *rng.sample([turned(way, 1), turned(way, -1), turned(way, 2), turned(way, -2)], 4)]
        return map_question(
            spec,
            stem=(f"จากแผนที่ชุมชน {LETTERS[a]} คือ{here} และ {LETTERS[b]} คือ{there} "
                  f"{there}อยู่ทางทิศใดของ{here}"),
            correct=way, wrongs=wrongs,
            hint=f"เริ่มที่{here} ({LETTERS[a]}) แล้วดูว่าต้องไปทางไหนจึงถึง{there} โดยด้านบนของแผนที่คือทิศเหนือ",
            topic=TOPIC)


def _walk(start, end) -> list[tuple[str, int]]:
    """The legs of a walk east-west then north-south: [(direction, squares)]."""
    dx, dy = end[0] - start[0], end[1] - start[1]
    legs = []
    if dx:
        legs.append(("ทิศตะวันออก" if dx > 0 else "ทิศตะวันตก", abs(dx)))
    if dy:
        legs.append(("ทิศเหนือ" if dy > 0 else "ทิศใต้", abs(dy)))
    return legs


WALKS = tuple((spec, a, b) for spec in COMMUNITY_MAPS
              for a in range(len(spec.places)) for b in range(len(spec.places)) if a != b)


@question_type(
    "geog.walk_route_p3",
    display_name={"th": "เดินตามทิศและระยะบนแผนที่ชุมชนแล้วบอกสถานที่ที่ไปถึง"},
    level=P3, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class WalkRoute(QuestionType):
    def build(self, rng: Random, **params):
        spec, a, b = rng.choice(WALKS)
        start, end = spec.places[a], spec.places[b]
        legs = _walk(start, end)
        rng.shuffle(legs)
        said = " แล้ว".join(f"เดินไปทาง{d} {n} ช่อง" for d, n in legs)
        dx, dy = end[0] - start[0], end[1] - start[1]
        wrongs = []
        for mistake, pos in (("direction.left_right_swapped", (start[0] - dx, end[1])),
                             ("direction.opposite", (end[0], start[1] - dy))):
            letter = spec.letter_at(pos)
            if letter and letter != LETTERS[b] and letter != LETTERS[a]:
                wrongs.append((mistake, letter))
        rest = [ch for i, ch in enumerate(LETTERS[:len(spec.places)]) if i not in (a, b)]
        rng.shuffle(rest)
        return map_question(
            spec,
            stem=f"จากแผนที่ชุมชน เริ่มที่ {LETTERS[a]} {said} จะถึงสถานที่ใด",
            correct=LETTERS[b], wrongs=[*wrongs, *rest],
            hint="ด้านบนของแผนที่คือทิศเหนือ ด้านขวาคือทิศตะวันออก นับช่องทีละช่องตามคำสั่ง",
            topic=TOPIC)
