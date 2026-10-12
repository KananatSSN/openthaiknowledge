"""เส้นตรงและมุม

คณิตศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ค 2.2 ป.4/*

Sets moved here from: math, math_diagrams, math_diagrams_geo, math_gaps_indicators, math_geometry, math_p4.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem
from otk.sets._support.math_diagrams import (
    KIND_ANGLES,
    PROTRACTOR_ANGLES,
    _img,
    _math_q,
    _nums,
    _text_q,
)
from otk.sets._support.math_diagrams_geo import LINE_FIGURES, LineFigure
from otk.sets._support.math_gaps_shape_data import _choices, _ConstructionSteps
from otk.sets._support.math_p4 import LEVEL

PROVENANCE = Provenance("original")


ANGLE_KINDS = ("มุมแหลม", "มุมฉาก", "มุมป้าน", "มุมตรง", "มุมกลับ")


def angle_kind(deg: int) -> str:
    return ("มุมแหลม" if deg < 90 else "มุมฉาก" if deg == 90 else "มุมป้าน" if deg < 180
            else "มุมตรง" if deg == 180 else "มุมกลับ")


LINE_ALT = "รูปเส้นที่ผ่านจุดสองจุดซึ่งกำกับด้วยตัวอักษร"


def line_name(f: LineFigure) -> str:
    a, b = f.names
    return {"segment": f"ส่วนของเส้นตรง {a}{b}", "ray": f"รังสี {a}{b}",
            "ray_back": f"รังสี {b}{a}", "line": f"เส้นตรง {a}{b}"}[f.kind]


_TRIPLES = ("ABC", "PQR", "XYZ", "DEF", "KLM", "RST", "MNO")


@question_type("math.classify_angle",
               display_name={"th": "จำแนกชนิดของมุม"}, level={"th": "ป.4"},
               topic="เส้นตรงและมุม")
class ClassifyAngle(ChoiceType):
    _LABELS = ["มุมแหลม", "มุมฉาก", "มุมป้าน", "มุมตรง", "มุมกลับ"]

    def compose(self, rng: Random):
        kind = rng.choice(self._LABELS)
        deg = {"มุมแหลม": lambda: rng.randint(1, 89),
               "มุมฉาก": lambda: 90,
               "มุมป้าน": lambda: rng.randint(91, 179),
               "มุมตรง": lambda: 180,
               "มุมกลับ": lambda: rng.randint(181, 359)}[kind]()
        stem = f"มุมขนาด {deg} องศา เป็นมุมชนิดใด?"
        return stem, kind, [x for x in self._LABELS if x != kind]


@question_type("math.classify_line",
               display_name={"th": "จำแนกชนิดของเส้น"}, level={"th": "ป.4"},
               topic="เส้นตรงและมุม")
class ClassifyLine(ChoiceType):
    _ITEMS = [("ไม่มีจุดปลายทั้งสองข้าง ต่อออกไปได้ไม่สิ้นสุด", "เส้นตรง"),
              ("มีจุดปลายเพียงข้างเดียว อีกข้างต่อไปไม่สิ้นสุด", "รังสี"),
              ("มีจุดปลายทั้งสองข้าง", "ส่วนของเส้นตรง")]
    _NAMED = [("มีจุดปลาย 2 จุด คือจุด {a} และจุด {b}", "ส่วนของเส้นตรง"),
              ("เริ่มต้นที่จุด {a} ผ่านจุด {b} แล้วต่อออกไปไม่สิ้นสุด", "รังสี"),
              ("ผ่านจุด {a} และจุด {b} แล้วต่อออกไปไม่สิ้นสุดทั้งสองข้าง", "เส้นตรง")]
    _POINTS = ("AB", "PQ", "MN", "XY", "CD", "KL", "RS")
    # Everyday things that are modelled by each kind of line.
    _THINGS = [("แสงที่ส่องออกจากไฟฉาย", "รังสี"), ("แสงอาทิตย์ที่ส่องออกจากดวงอาทิตย์", "รังสี"),
               ("ขอบของไม้บรรทัด", "ส่วนของเส้นตรง"), ("เชือกที่ขึงตึงระหว่างเสาสองต้น", "ส่วนของเส้นตรง"),
               ("ด้านของรูปสามเหลี่ยม", "ส่วนของเส้นตรง"), ("แสงเลเซอร์ที่ยิงออกจากเครื่อง", "รังสี")]
    _LABELS = ["เส้นตรง", "รังสี", "ส่วนของเส้นตรง"]

    def compose(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            desc, label = rng.choice(self._ITEMS)
            stem = f"เส้นที่{desc} เรียกว่าอะไร?"
        elif kind == 1:
            desc, label = rng.choice(self._NAMED)
            a, b = rng.choice(self._POINTS)
            stem = f"เส้นที่{desc.format(a=a, b=b)} เรียกว่าอะไร?"
        else:
            thing, label = rng.choice(self._THINGS)
            stem = f"{thing} เป็นตัวอย่างของเส้นชนิดใด?"
        return stem, label, [x for x in self._LABELS if x != label]


@question_type("math.angle_kind_picture_p4", display_name={"th": "บอกชนิดของมุมจากรูป"},
               level={"th": "ป.4"}, topic="เส้นตรงและมุม")
class AngleKindPictureP4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        a = rng.choice(KIND_ANGLES)
        right = angle_kind(a.deg)
        order = list(ANGLE_KINDS)
        i = order.index(right)
        near = [order[j] for j in (i - 1, i + 1) if 0 <= j < len(order)]
        rest = [k for k in order if k not in near and k != right]
        return _text_q([text("มุมที่แสดงด้วยเส้นโค้งในรูปเป็นมุมชนิดใด"),
                        _img(a.asset_id, "มุมหนึ่งมุมที่มีเส้นโค้งแสดงบริเวณของมุม")],
                       right, near + rest, self.topic)


@question_type("math.line_ray_picture_p4", display_name={"th": "บอกชื่อเส้นตรง รังสี และส่วนของเส้นตรงจากรูป"},
               level={"th": "ป.4"}, topic="เส้นตรงและมุม")
class LineRayPictureP4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        f = rng.choice(LINE_FIGURES)
        right = line_name(f)
        others = [line_name(f._replace(kind=k)) for k in ("segment", "ray", "ray_back", "line") if k != f.kind]
        return _text_q([text("รูปนี้คือข้อใด"), _img(f.asset_id, LINE_ALT)], right, others, self.topic)


@question_type("math.name_angle_p4", display_name={"th": "ชื่อมุม จุดยอด แขนของมุม และสัญลักษณ์"},
               level={"th": "ป.4"}, topic="เส้นตรงและมุม")
class NameAngleP4(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, v, c = rng.choice(_TRIPLES)
        if rng.random() < 0.5:
            a, c = c, a
        kind = rng.randrange(3)
        if kind == 0:
            stem = f"มุมที่มีจุด {v} เป็นจุดยอด และมี {v}{a} กับ {v}{c} เป็นแขนของมุม เขียนเป็นสัญลักษณ์ได้อย่างไร"
            # The vertex must sit in the middle of the name.
            return _choices([text(stem)], f"∠{a}{v}{c}", [f"∠{v}{a}{c}", f"∠{a}{c}{v}", f"∠{v}{c}{a}"], self.topic)
        if kind == 1:
            return _choices([text(f"∠{a}{v}{c} มีจุดยอดคือจุดใด")], f"จุด {v}",
                            [f"จุด {a}", f"จุด {c}", f"จุด {a} และจุด {c}"], self.topic)
        return _choices([text(f"แขนของ ∠{a}{v}{c} คือข้อใด")], f"{v}{a} และ {v}{c}",
                        [f"{a}{v} และ {a}{c}", f"{a}{c} และ {c}{v}", f"{a}{v} และ {v}{c} และ {a}{c}"], self.topic)


@question_type("math.protractor_read_p4", display_name={"th": "อ่านขนาดของมุมจากโพรแทรกเตอร์"},
               level={"th": "ป.4"}, topic="เส้นตรงและมุม")
class ProtractorReadP4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        a = rng.choice(PROTRACTOR_ANGLES)
        d = a.deg
        # The other scale (180 − d) is the protractor's own trap.
        wrongs = _nums(180 - d, d + 10, d - 10, d + 5, answer=d, lo=1)
        return _math_q([text("มุมในรูปมีขนาดกี่องศา (วัดจากเส้นที่ชี้ไปทางขวา)"),
                        _img(a.asset_id, "มุมที่วางโพรแทรกเตอร์ทาบไว้ มีขีดบอกองศาทุก 10 องศา")],
                       str(d), wrongs, self.topic)


@question_type("math.construct_angle_protractor_p4", display_name={"th": "ขั้นตอนการสร้างมุมด้วยโพรแทรกเตอร์"},
               level={"th": "ป.4"}, topic="เส้นตรงและมุม")
class ConstructAngleProtractorP4(_ConstructionSteps):
    def procedures(self, rng):
        t = rng.choice([d for d in range(20, 175, 5) if d != 90])
        a, v, c = rng.choice(_TRIPLES)
        goal = f"การสร้าง ∠{a}{v}{c} ขนาด {t} องศา โดยใช้โพรแทรกเตอร์"
        steps = [
            f"ลากรังสี {v}{c} เป็นแขนข้างหนึ่งของมุม",
            f"วางจุดศูนย์กลางของโพรแทรกเตอร์ที่จุด {v} ให้เส้นฐานทับรังสี {v}{c}",
            f"อ่านสเกลที่เริ่มจาก 0 บนรังสี {v}{c} ทำจุด {a} ที่ขีด {t} องศา",
            f"ลากรังสี {v}{a} จากจุดยอดผ่านจุด {a}",
        ]
        # Reading the other scale gives 180 − t.
        faulty = [f"ทำจุด {a} ที่ขีด {180 - t} องศา บนสเกลที่เริ่มจาก 0 บนรังสี {v}{c}",
                  f"วางจุดศูนย์กลางของโพรแทรกเตอร์ที่จุด {c} ให้เส้นฐานทับรังสี {v}{c}"]
        return goal, steps, faulty


@question_type("math.angle_complement_supplement",
               display_name={"th": "มุมประกอบมุมฉาก / ประกอบสองมุมฉาก"},
               level={"th": "ป.4"}, topic="เส้นตรงและมุม")
class AngleComplementSupplement(WordProblem):
    def expr(self, rng: Random, lo: int = 10, hi: int = 80):
        a = rng.randint(lo, hi)
        if rng.random() < 0.5:
            kind, total = "มุมประกอบมุมฉาก", 90
        else:
            kind, total = "มุมประกอบสองมุมฉาก", 180
        whole = "มุมฉาก" if total == 90 else "มุมตรง"
        prompt = rng.choice((
            f"{kind}ของมุมขนาด {a} องศา มีขนาดกี่องศา",
            f"มุมสองมุมรวมกันเป็น{whole} มุมหนึ่งมีขนาด {a} องศา อีกมุมหนึ่งมีขนาดกี่องศา",
            f"ลากรังสีแบ่ง{whole}ออกเป็นสองมุม ถ้ามุมหนึ่งมีขนาด {a} องศา อีกมุมหนึ่งมีขนาดกี่องศา",
        ))
        return MathDraw("", str(total - a), prompt=prompt,
                        distractors=[str(a), str(180 - a if total == 90 else 90 - a),
                                     str(total + a)])


@question_type("math.clock_angle_p4",
               display_name={"th": "มุมระหว่างเข็มนาฬิกา"},
               level=LEVEL, topic="เส้นตรงและมุม")
class ClockAngleP4(WordProblem):
    def expr(self, rng: Random):
        h = rng.randint(1, 11)
        angle = 30 * min(h, 12 - h)
        p = rng.choice(_story.NAMES)
        face = "(หน้าปัดนาฬิกาแบ่งเป็น 12 ช่องเท่า ๆ กัน)"
        prompt = rng.choice((
            f"เวลา {h} นาฬิกาตรง เข็มสั้นกับเข็มยาวของนาฬิกาทำมุมเล็กที่สุดกี่องศา {face}",
            f"{p}ตื่นนอนเวลา {h} นาฬิกาตรง ขณะนั้นเข็มสั้นกับเข็มยาวทำมุมเล็กที่สุดกี่องศา {face}",
            # The afternoon hour reads the same on a 12-hour face.
            f"เวลา {h + 12}.00 น. เข็มสั้นกับเข็มยาวของนาฬิกาทำมุมเล็กที่สุดกี่องศา {face}",
        ))
        return MathDraw("", str(angle), prompt=prompt,
                        # One mark as 5 or 6 degrees, and the reflex side.
                        distractors=_story.keep(6 * min(h, 12 - h), 360 - angle, 5 * h,
                                                angle + 30, answer=angle, lo=1))


@question_type("math.angles_around_point_p4",
               display_name={"th": "มุมบนเส้นตรงและมุมรอบจุด"},
               level=LEVEL, topic="เส้นตรงและมุม")
class AnglesAroundPointP4(WordProblem):
    def expr(self, rng: Random):
        if rng.random() < 0.5:
            a, b = rng.randint(20, 80), rng.randint(20, 80)
            ans = 180 - a - b
            prompt = rng.choice((
                f"มุมสามมุมเรียงต่อกันบนเส้นตรงเส้นหนึ่ง ถ้ามุมสองมุมมีขนาด {a} องศา "
                f"และ {b} องศา มุมที่เหลือมีขนาดกี่องศา",
                f"ลากรังสีสองเส้นจากจุดจุดหนึ่งบนเส้นตรง แบ่งมุมตรงออกเป็นสามมุม ถ้ามุมสองมุม"
                f"มีขนาด {a} องศา และ {b} องศา มุมที่เหลือมีขนาดกี่องศา",
            ))
            return MathDraw("", str(ans), prompt=prompt,
                            distractors=_story.keep(360 - a - b, 90 - a if a < 90 else a + b,
                                                    a + b, answer=ans, lo=1))
        a, b = rng.randint(60, 150), rng.randint(60, 150)
        ans = 360 - a - b
        prompt = rng.choice((
            f"มุมสามมุมรอบจุดจุดหนึ่งรวมกันได้หนึ่งรอบ ถ้ามุมสองมุมมีขนาด {a} องศา "
            f"และ {b} องศา มุมที่เหลือมีขนาดกี่องศา",
            f"ตัดพิซซ่าถาดกลมจากจุดศูนย์กลางออกเป็น 3 ชิ้น ถ้ามุมที่จุดศูนย์กลางของสองชิ้น"
            f"มีขนาด {a} องศา และ {b} องศา ชิ้นที่เหลือมีมุมที่จุดศูนย์กลางกี่องศา",
            f"พัดลมมีใบพัด 3 ใบ มุมระหว่างใบพัดสองคู่มีขนาด {a} องศา และ {b} องศา "
            f"มุมระหว่างใบพัดคู่ที่เหลือมีขนาดกี่องศา",
        ))
        return MathDraw("", str(ans), prompt=prompt,
                        distractors=_story.keep(180 - a - b if a + b < 180 else a + b - 180,
                                                a + b, ans + 10, answer=ans, lo=1))
