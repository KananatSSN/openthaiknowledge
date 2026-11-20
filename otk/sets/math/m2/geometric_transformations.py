"""การแปลงทางเรขาคณิต

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: ค 2.2 ม.2/*

Sets moved here from: math, math_diagrams_geo, math_geometry.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.mistakes import named
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.kit.math_problems import ChoiceType, MathDraw, MathType
from otk.sets._support.math_diagrams import _img, _math_q, _text_q
from otk.sets._support.math_diagrams_geo import TRANSFORMS
from otk.sets._support.math_p2 import _maths

PROVENANCE = Provenance("original")


TRANSFORM_ALT = ("ตารางพิกัดจาก -6 ถึง 6 มีรูปสามเหลี่ยม ABC ที่แรเงา และภาพ A'B'C' "
                 "ที่ได้จากการแปลงแบบหนึ่ง")


def transform_name(move: str) -> str:
    if move.startswith("t_"):
        _, dx, dy = move.split("_")
        dx, dy = int(dx), int(dy)
        return (f"การเลื่อนขนานไปทาง{'ขวา' if dx > 0 else 'ซ้าย'} {abs(dx)} หน่วย "
                f"และ{'ขึ้น' if dy > 0 else 'ลง'} {abs(dy)} หน่วย")
    return {"rx": "การสะท้อนโดยมีแกน X เป็นเส้นสะท้อน", "ry": "การสะท้อนโดยมีแกน Y เป็นเส้นสะท้อน",
            "r180": "การหมุนรอบจุดกำเนิด 180 องศา",
            "r90": "การหมุนรอบจุดกำเนิด 90 องศา ทวนเข็มนาฬิกา"}[move]


def _pt(p) -> str:
    return f"({p[0]}, {p[1]})"


@question_type("math.reflect_point", display_name={"th": "สะท้อนจุดข้ามแกน"},
               level={"th": "ม.1"}, topic="การแปลงทางเรขาคณิต")
class ReflectPoint(MathType):
    def expr(self, rng: Random, lo: int = -9, hi: int = 9):
        x, y = rng.randint(lo, hi), rng.randint(lo, hi)
        axis, point = rng.choice([
            ("แกน x", (x, -y)), ("แกน y", (-x, y)), ("จุดกำเนิด", (-x, -y))])
        return MathDraw(f"({x}, {y})", f"({point[0]}, {point[1]})",
                        prompt=f"จงหาพิกัดของจุดหลังการสะท้อนข้าม{axis}",
                        distractors=[f"({-x}, {y})", f"({x}, {-y})",
                                     f"({-x}, {-y})", f"({y}, {x})"])


@question_type("math.translate_point", display_name={"th": "เลื่อนขนานจุด"},
               level={"th": "ม.1"}, topic="การแปลงทางเรขาคณิต")
class TranslatePoint(MathType):
    def expr(self, rng: Random, lo: int = -9, hi: int = 9):
        x, y = rng.randint(lo, hi), rng.randint(lo, hi)
        # Non-zero: "เลื่อนไป 0 หน่วย" is not a translation anyone would set.
        dx = rng.choice([n for n in range(-6, 7) if n])
        dy = rng.choice([n for n in range(-6, 7) if n])
        side = f"ไปทาง{'ขวา' if dx > 0 else 'ซ้าย'} {abs(dx)} หน่วย และ{'ขึ้น' if dy > 0 else 'ลง'} {abs(dy)} หน่วย"
        prompt = rng.choice((
            f"เลื่อนขนานจุดนี้ไปตามแนวแกน x เป็นระยะ {dx} หน่วย "
            f"และตามแนวแกน y เป็นระยะ {dy} หน่วย จะได้จุดใด",
            f"ตัวหมากบนกระดานพิกัดอยู่ที่จุดนี้ ถ้าเลื่อนตัวหมาก{side} ตัวหมากจะอยู่ที่จุดใด",
            f"หุ่นยนต์อยู่ที่จุดนี้ แล้วเคลื่อนที่{side} หุ่นยนต์จะอยู่ที่จุดใด",
        ))
        return MathDraw(
            f"({x}, {y})", f"({x + dx}, {y + dy})", prompt=prompt,
            distractors=[f"({x - dx}, {y - dy})", f"({x + dy}, {y + dx})",
                         f"({dx}, {dy})"])


@question_type("math.coordinate_transform",
               display_name={"th": "พิกัดหลังการแปลงทางเรขาคณิต"}, level={"th": "ม.1"},
               topic="การแปลงทางเรขาคณิต")
class CoordinateTransform(MathType):
    def expr(self, rng: Random):
        x, y = rng.randint(-6, 6), rng.randint(-6, 6)
        kind = rng.choice(["translate", "reflect_x", "reflect_y", "rotate90"])
        pt = lambda p, q: rf"({p}, {q})"
        if kind == "translate":
            dx, dy = rng.randint(-5, 5), rng.randint(-5, 5)
            desc = f"เลื่อนขนานด้วย ({dx}, {dy})"
            ans, wrong = (x + dx, y + dy), [(x - dx, y - dy), (x + dy, y + dx)]
        elif kind == "reflect_x":
            desc, ans, wrong = "สะท้อนข้ามแกน x", (x, -y), [(-x, y), (-x, -y)]
        elif kind == "reflect_y":
            desc, ans, wrong = "สะท้อนข้ามแกน y", (-x, y), [(x, -y), (-x, -y)]
        else:
            desc, ans, wrong = "หมุน 90° ทวนเข็มรอบจุดกำเนิด", (-y, x), \
                [(y, -x), (y, x)]
        return MathDraw(
            pt(x, y), pt(*ans), prompt=f"จุด ({x}, {y}) หลัง{desc} มีพิกัดใด?",
            distractors=[pt(*w) for w in wrong] + [pt(y, x)])


@question_type("math.transformation_picture_m2", display_name={"th": "บอกการแปลงและพิกัดของภาพจากรูป"},
               level={"th": "ม.1"}, topic="การแปลงทางเรขาคณิต")
class TransformationPictureM2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        t = rng.choice(TRANSFORMS)
        img = _img(t.asset_id, TRANSFORM_ALT)
        if rng.random() < 0.5:
            right = transform_name(t.move)
            pool = ["rx", "ry", "r180", "r90", "t_2_3", "t_-3_2"]
            others = [transform_name(m) for m in pool if transform_name(m) != right]
            rng.shuffle(others)
            return _text_q([text("รูปสามเหลี่ยม A'B'C' เป็นภาพที่ได้จากรูปสามเหลี่ยม ABC ด้วยการแปลงแบบใด"), img],
                           right, others[:3], self.topic)
        i = rng.randrange(3)
        name = "ABC"[i]
        p, q = t.tri[i], t.image()[i]
        # x and y swapped, the signs flipped, the point not moved, one square off.
        wrongs = [_pt((q[1], q[0])), _pt((-q[0], -q[1])), _pt(p), _pt((q[0] + 1, q[1])),
                  _pt((q[0], q[1] - 1)), _pt((-q[1], q[0]))]
        return _math_q([text(f"จากรูป จุด {name}' ซึ่งเป็นภาพของจุด {name} มีพิกัดเป็นเท่าใด"), img],
                       _pt(q), wrongs, self.topic)


_TRANSFORM_TOPIC = "การแปลงทางเรขาคณิต"
LEVEL_M2 = {"th": "ม.2"}


@question_type("math.rotation_about_center_m2",
               display_name={"th": "หมุนจุดรอบศูนย์กลางที่กำหนด"},
               level={"th": "ม.2"}, topic=_TRANSFORM_TOPIC)
class RotationAboutCenterM2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            h, k = rng.sample([n for n in range(-6, 7) if n], 2)
            dx, dy = rng.sample([n for n in range(-5, 6) if n], 2)
            x, y = h + dx, k + dy
            turn = rng.choice(("ทวนเข็มนาฬิกา 90", "ตามเข็มนาฬิกา 90", "180"))
            if turn.startswith("ทวน"):
                answer = (h - dy, k + dx)
                opposite = (h + dy, k - dx)
                origin = (-y, x)
            elif turn.startswith("ตาม"):
                answer = (h + dy, k - dx)
                opposite = (h - dy, k + dx)
                origin = (y, -x)
            else:
                answer = (h - dx, k - dy)
                opposite = (h + dx, k - dy)
                origin = (-x, -y)
            unchanged = (x, y)
            if len({answer, opposite, origin, unchanged}) == 4:
                break
        wrongs = [
            named("transform.reflected_instead_of_rotated" if turn == "180"
                  else "transform.wrong_rotation_direction", _pt(opposite)),
            named("transform.rotated_about_origin", _pt(origin)),
            named("transform.left_point_unchanged", _pt(unchanged)),
        ]
        return _maths([text(f"จุด A = {_pt((x, y))} ถูกหมุนรอบจุด C = {_pt((h, k))} "
                            f"เป็นมุม {turn} องศา ภาพของจุด A มีพิกัดใด")],
                      _pt(answer), wrongs, self.topic)


@question_type("math.translation_then_reflection_m2",
               display_name={"th": "เลื่อนขนานแล้วสะท้อนจุดตามลำดับ"},
               level={"th": "ม.2"}, topic=_TRANSFORM_TOPIC)
class TranslationThenReflectionM2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            x, y = rng.randint(-7, 7), rng.randint(-7, 7)
            u, v = rng.choice([n for n in range(-5, 6) if n]), rng.choice([n for n in range(-5, 6) if n])
            shifted = (x + u, y + v)
            answer = (-shifted[0], shifted[1])
            reflected_first = (-x + u, y + v)
            wrong_axis = (shifted[0], -shifted[1])
            if len({answer, shifted, reflected_first, wrong_axis}) == 4:
                break
        wrongs = [
            named("transform.reversed_order", _pt(reflected_first)),
            named("transform.skipped_reflection", _pt(shifted)),
            named("transform.reflected_wrong_axis", _pt(wrong_axis)),
        ]
        return _maths([text(f"เริ่มจากจุด A = {_pt((x, y))} เลื่อนขนานด้วยเวกเตอร์ {_pt((u, v))} "
                            "แล้วสะท้อนภาพที่ได้ข้ามแกน y จุดสุดท้ายมีพิกัดใด")],
                      _pt(answer), wrongs, self.topic)


@question_type("math.inverse_transformation_m2",
               display_name={"th": "หาจุดต้นฉบับจากภาพหลังการแปลงสองขั้น"},
               level={"th": "ม.2"}, topic=_TRANSFORM_TOPIC)
class InverseTransformationM2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            x, y = rng.randint(-7, 7), rng.randint(-7, 7)
            u, v = rng.choice([n for n in range(-5, 6) if n]), rng.choice([n for n in range(-5, 6) if n])
            image = (x + u, -y + v)
            translation_only = (image[0] - u, image[1] - v)
            added_vector = (image[0] + u, v - image[1])
            reflected_only = (image[0], -image[1])
            if len({(x, y), translation_only, added_vector, reflected_only}) == 4:
                break
        wrongs = [
            named("transform.skipped_inverse_reflection", _pt(translation_only)),
            named("transform.applied_forward_translation", _pt(added_vector)),
            named("transform.skipped_inverse_translation", _pt(reflected_only)),
        ]
        return _maths([text(f"จุด A ถูกสะท้อนข้ามแกน x แล้วเลื่อนขนานด้วยเวกเตอร์ {_pt((u, v))} "
                            f"ได้ภาพ A' = {_pt(image)} จุด A เดิมมีพิกัดใด")],
                      _pt((x, y)), wrongs, self.topic)


# ── More transformations (สสวท. ม.2 เล่ม 1 บทที่ 5): reflection in other lines, finding a translation,
# and what each transformation keeps ──


@question_type("math.reflect_line_m2", display_name={"th": "สะท้อนจุดข้ามเส้นตรงที่กำหนด"},
               level=LEVEL_M2, topic=_TRANSFORM_TOPIC)
class ReflectLineM2(QuestionType):
    """Reflection in x = k, y = k, y = x or y = −x."""

    def build(self, rng: Random) -> GeneratedQuestion:
        x, y = rng.choice([v for v in range(-8, 9) if v]), rng.choice([v for v in range(-8, 9) if v])
        kind = rng.randrange(4)
        if kind < 2:
            k = rng.choice([v for v in range(-5, 6) if v and v != (x if kind == 0 else y)])
            if kind == 0:
                line, right = f"x = {k}", (2 * k - x, y)
                # The y-axis used; k − x; the y changed instead.
                wrongs = [(-x, y), (k - x, y), (x, 2 * k - y)]
            else:
                line, right = f"y = {k}", (x, 2 * k - y)
                wrongs = [(x, -y), (x, k - y), (2 * k - x, y)]
        elif kind == 2:
            line, right = "y = x", (y, x)
            wrongs = [(-y, -x), (x, -y), (-x, y)]
        else:
            line, right = "y = −x", (-y, -x)
            wrongs = [(y, x), (-x, -y), (-x, y)]
        # When two slips land on the same point, the point not moved and the other axis fill in.
        wrongs = [w for w in dict.fromkeys([*wrongs, (x, y), (-x, -y), (x, -y), (-x, y)]) if w != right][:3]
        return _maths([text(f"จุด A = {_pt((x, y))} ถูกสะท้อนข้ามเส้นตรง {line} ภาพของจุด A มีพิกัดใด")],
                      _pt(right), [_pt(w) for w in wrongs], self.topic)


@question_type("math.translation_vector_m2", display_name={"th": "หาการเลื่อนขนานจากจุดและภาพ"},
               level=LEVEL_M2, topic=_TRANSFORM_TOPIC)
class TranslationVectorM2(QuestionType):
    """A and its image A′ fix the translation; the same move takes B to B′."""

    def build(self, rng: Random) -> GeneratedQuestion:
        a = (rng.randint(-6, 6), rng.randint(-6, 6))
        u, v = rng.choice([n for n in range(-7, 8) if n]), rng.choice([n for n in range(-7, 8) if n])
        image = (a[0] + u, a[1] + v)
        if rng.random() < 0.5:
            # Subtracted the wrong way; the image's own coordinates; the parts swapped.
            # Then one part's sign slipped, or A's own coordinates, when two of those coincide.
            wrongs = [(-u, -v), image, (v, u), (u, -v), (-u, v), a]
            wrongs = [w for w in dict.fromkeys(wrongs) if w != (u, v)][:3]
            return _maths([text(f"การเลื่อนขนานพาจุด A = {_pt(a)} ไปยังจุด A′ = {_pt(image)} "
                                f"เป็นการเลื่อนขนานด้วยเวกเตอร์ใด")], _pt((u, v)), [_pt(w) for w in wrongs], self.topic)
        b = (rng.randint(-6, 6), rng.randint(-6, 6))
        right = (b[0] + u, b[1] + v)
        wrongs = [(b[0] - u, b[1] - v), (b[0] + image[0], b[1] + image[1]), (b[0] + v, b[1] + u),
                  (b[0] + u, b[1] - v), (b[0] - u, b[1] + v), b]
        wrongs = [w for w in dict.fromkeys(wrongs) if w != right][:3]
        return _maths([text(f"การเลื่อนขนานพาจุด A = {_pt(a)} ไปยังจุด A′ = {_pt(image)} "
                            f"ถ้าเลื่อนขนานจุด B = {_pt(b)} แบบเดียวกัน ภาพของจุด B มีพิกัดใด")],
                      _pt(right), [_pt(w) for w in wrongs], self.topic)


_KINDS = ("การเลื่อนขนาน", "การสะท้อน", "การหมุน")


@question_type("math.transformation_property_m2", display_name={"th": "สมบัติของการแปลงทางเรขาคณิต"},
               level=LEVEL_M2, topic=_TRANSFORM_TOPIC)
class TransformationPropertyM2(ConceptBankType):
    """What each transformation keeps, moves and turns over."""

    ITEMS = [
        Concept("การแปลงใดที่ทุกจุดเคลื่อนที่ไปในทิศทางเดียวกันและเป็นระยะทางเท่ากัน", "การเลื่อนขนาน",
                ("การสะท้อน", "การหมุน", "การย่อขยาย")),
        Concept("การแปลงใดทำให้ภาพที่ได้กลับด้านจากรูปต้นแบบ เหมือนภาพในกระจกเงา", "การสะท้อน",
                ("การเลื่อนขนาน", "การหมุน", "การย่อขยาย")),
        Concept("การแปลงใดมีจุดหนึ่งจุดที่ไม่เปลี่ยนตำแหน่ง และจุดอื่นเคลื่อนที่เป็นมุมเท่ากันรอบจุดนั้น", "การหมุน",
                ("การเลื่อนขนาน", "การสะท้อน", "การย่อขยาย")),
        Concept("ในการสะท้อน ส่วนของเส้นตรงที่เชื่อมจุดกับภาพของจุดนั้นมีความสัมพันธ์กับเส้นสะท้อนอย่างไร",
                "เส้นสะท้อนแบ่งครึ่งและตั้งฉากกับส่วนของเส้นตรงนั้น",
                ("เส้นสะท้อนขนานกับส่วนของเส้นตรงนั้นเสมอ", "เส้นสะท้อนผ่านจุดนั้นแต่ไม่ผ่านภาพของจุดนั้น",
                 "เส้นสะท้อนทำมุม 45 องศากับส่วนของเส้นตรงนั้น")),
        Concept("ข้อใดถูกต้องเกี่ยวกับการเลื่อนขนาน การสะท้อน และการหมุน",
                "ภาพที่ได้เท่ากันทุกประการกับรูปต้นแบบ",
                ("ภาพที่ได้มีขนาดใหญ่กว่ารูปต้นแบบ", "ภาพที่ได้กลับด้านจากรูปต้นแบบทุกครั้ง",
                 "ภาพที่ได้อยู่ตำแหน่งเดิมของรูปต้นแบบเสมอ")),
        Concept("ในการหมุนรอบจุด O ข้อใดถูกต้อง", "ระยะจากจุด O ถึงจุดใด ๆ เท่ากับระยะจากจุด O ถึงภาพของจุดนั้น",
                ("ทุกจุดเคลื่อนที่เป็นระยะทางเท่ากันในทิศทางเดียวกัน", "ภาพที่ได้กลับด้านจากรูปต้นแบบเหมือนภาพในกระจกเงา",
                 "จุด O เคลื่อนที่ไปพร้อมกับรูปเป็นระยะทางเท่ากับจุดอื่น")),
    ]


# ── To fifteen (2026-11): rotation about the origin, two reflections, naming the move from a point and its
# image, the distance to a reflection, and a translation followed by a half turn ──


def _three_new(right, candidates) -> list[str]:
    out = [w for w in dict.fromkeys(candidates) if w != right]
    return [_pt(w) for w in out[:3]]


def _nonzero(rng: Random, lo: int, hi: int) -> int:
    return rng.choice([n for n in range(lo, hi + 1) if n])


@question_type("math.rotate_origin_m2", display_name={"th": "หมุนจุดรอบจุดกำเนิด"},
               level=LEVEL_M2, topic=_TRANSFORM_TOPIC)
class RotateOriginM2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            x, y = _nonzero(rng, -8, 8), _nonzero(rng, -8, 8)
            if abs(x) != abs(y):
                break
        turn = rng.randrange(4)
        ccw, cw, half = (-y, x), (y, -x), (-x, -y)
        desc, right = (("90° ทวนเข็มนาฬิกา", ccw), ("90° ตามเข็มนาฬิกา", cw), ("180°", half),
                       ("270° ทวนเข็มนาฬิกา", cw))[turn]
        # The other direction; the half turn; a reflection; the coordinates swapped.
        cands = [ccw if right == cw else cw, half, (x, -y), (y, x), (-x, y)]
        return _maths([text(f"หมุนจุด A = {_pt((x, y))} รอบจุดกำเนิด {desc} ภาพของจุด A มีพิกัดใด")],
                      _pt(right), _three_new(right, cands), self.topic)


@question_type("math.reflect_twice_m2", display_name={"th": "สะท้อนสองครั้ง"},
               level=LEVEL_M2, topic=_TRANSFORM_TOPIC)
class ReflectTwiceM2(QuestionType):
    """Across both axes is a half turn; across two parallel lines x = a then x = b is a slide of 2(b − a)."""

    def build(self, rng: Random) -> GeneratedQuestion:
        x, y = _nonzero(rng, -8, 8), _nonzero(rng, -8, 8)
        if rng.random() < 0.5:
            right = (-x, -y)
            stem = f"สะท้อนจุด A = {_pt((x, y))} ข้ามแกน x แล้วสะท้อนภาพที่ได้ข้ามแกน y ภาพสุดท้ายมีพิกัดใด"
            cands = [(x, -y), (-x, y), (x, y), (y, x)]
        else:
            a = _nonzero(rng, -4, 4)
            b = rng.choice([n for n in range(-5, 6) if n not in (a, 0)])
            first = 2 * a - x
            right = (2 * b - first, y)
            stem = (f"สะท้อนจุด A = {_pt((x, y))} ข้ามเส้นตรง x = {a} แล้วสะท้อนภาพที่ได้ข้ามเส้นตรง x = {b} "
                    f"ภาพสุดท้ายมีพิกัดใด")
            # The first reflection only; the second only; the gap counted once.
            cands = [(first, y), (2 * b - x, y), (x + (b - a), y), (x, 2 * b - y), (-x, y)]
        return _maths([text(stem)], _pt(right), _three_new(right, cands), self.topic)


_MOVES = (("การสะท้อนข้ามแกน X", lambda x, y: (x, -y)), ("การสะท้อนข้ามแกน Y", lambda x, y: (-x, y)),
          ("การหมุนรอบจุดกำเนิด 180°", lambda x, y: (-x, -y)),
          ("การหมุนรอบจุดกำเนิด 90° ทวนเข็มนาฬิกา", lambda x, y: (-y, x)),
          ("การหมุนรอบจุดกำเนิด 90° ตามเข็มนาฬิกา", lambda x, y: (y, -x)))


@question_type("math.name_the_move_m2", display_name={"th": "บอกการแปลงจากจุดและภาพ"},
               level=LEVEL_M2, topic=_TRANSFORM_TOPIC)
class NameTheMoveM2(ChoiceType):
    def compose(self, rng: Random):
        while True:
            x, y = _nonzero(rng, -7, 7), _nonzero(rng, -7, 7)
            if abs(x) != abs(y):
                break
        name, move = rng.choice(_MOVES)
        image = move(x, y)
        return (f"จุด A = {_pt((x, y))} มีภาพเป็น A′ = {_pt(image)} เป็นการแปลงแบบใด", name,
                [n for n, _ in _MOVES if n != name])


@question_type("math.reflection_distance_m2", display_name={"th": "ระยะระหว่างจุดกับภาพที่ได้จากการสะท้อน"},
               level=LEVEL_M2, topic=_TRANSFORM_TOPIC)
class ReflectionDistanceM2(QuestionType):
    """The line of reflection is halfway: the point and its image are 2|y − k| apart for y = k."""

    def build(self, rng: Random) -> GeneratedQuestion:
        x, y = rng.randint(-8, 8), rng.randint(-8, 8)
        k = rng.choice([n for n in range(-5, 6) if n != y])
        gap = abs(y - k)
        if rng.random() < 0.5:
            stem = f"สะท้อนจุด A = {_pt((x, y))} ข้ามเส้นตรง y = {k} ได้จุด A′ จุด A และ A′ อยู่ห่างกันกี่หน่วย"
            right, wrongs = 2 * gap, (gap, abs(y) + abs(k), 2 * abs(y), 2 * gap + 2)
        else:
            stem = f"สะท้อนจุด A = {_pt((x, y))} ข้ามเส้นตรง y = {k} ได้จุด A′ จุด A′ อยู่ห่างจากเส้นตรง y = {k} กี่หน่วย"
            right, wrongs = gap, (2 * gap, abs(y), abs(k), gap + 1)
        out = [str(w) for w in dict.fromkeys(wrongs) if w != right and w > 0][:3]
        n = right + 3
        while len(out) < 3:
            if str(n) not in out:
                out.append(str(n))
            n += 1
        return _maths([text(stem)], str(right), out, self.topic)


@question_type("math.translate_then_turn_m2", display_name={"th": "เลื่อนขนานแล้วหมุน 180°"},
               level=LEVEL_M2, topic=_TRANSFORM_TOPIC)
class TranslateThenTurnM2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        x, y = rng.randint(-6, 6), rng.randint(-6, 6)
        u, v = _nonzero(rng, -5, 5), _nonzero(rng, -5, 5)
        moved = (x + u, y + v)
        right = (-moved[0], -moved[1])
        # Turned first, then moved; moved only; turned only.
        # Then, when those coincide: the vector subtracted before the turn, and the vector alone.
        cands = [(-x + u, -y + v), moved, (-x, -y), (moved[0], -moved[1]), (-moved[0], moved[1]),
                 (u - x, v - y), (x - u, y - v), (-u, -v)]
        return _maths([text(f"เลื่อนขนานจุด A = {_pt((x, y))} ด้วยเวกเตอร์ {_pt((u, v))} แล้วหมุนภาพที่ได้รอบจุดกำเนิด "
                            f"180° ภาพสุดท้ายมีพิกัดใด")], _pt(right), _three_new(right, cands), self.topic)
