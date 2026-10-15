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
from otk.kit.math_problems import MathDraw, MathType
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
