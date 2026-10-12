"""สี่เหลี่ยมมุมฉาก

คณิตศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ค 2.2 ป.4/*

Sets moved here from: math, math_diagrams, math_gaps_shape_data, math_p4.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import RECT_FIGURES, Figure, _img, _math_q, _nums, figure_alt
from otk.sets._support.math_gaps_shape_data import _ConstructionSteps
from otk.sets._support.math_p4 import LEVEL

PROVENANCE = Provenance("original")


def _unit(f: Figure) -> str:
    return "เซนติเมตร" if f.unit == "cm" else "เมตร"


_RECT_TOPIC = "สี่เหลี่ยมมุมฉาก"


@question_type("math.rectangle_area_perimeter",
               display_name={"th": "พื้นที่/เส้นรอบรูปสี่เหลี่ยมมุมฉาก"}, level={"th": "ป.4"},
               topic="สี่เหลี่ยมมุมฉาก")
class RectangleAreaPerimeter(WordProblem):
    _THINGS = (("สมุดเล่มหนึ่ง", "เซนติเมตร"), ("กระดานดำ", "เมตร"), ("สนามฟุตบอล", "เมตร"),
               ("กระเบื้องแผ่นหนึ่ง", "เซนติเมตร"), ("ห้องนอน", "เมตร"), ("ผ้าเช็ดหน้า", "เซนติเมตร"))

    def expr(self, rng: Random):
        width, length = rng.randint(2, 20), rng.randint(2, 20)
        square = rng.random() < 0.25
        if square:
            length = width
        thing, unit = rng.choice(self._THINGS)
        shape = (f"รูปสี่เหลี่ยมจัตุรัสยาวด้านละ {width} {unit}" if square
                 else f"รูปสี่เหลี่ยมผืนผ้ากว้าง {width} {unit} ยาว {length} {unit}")
        if rng.random() < 0.5:
            ask, ans = f"พื้นที่กี่ตาราง{unit}", width * length
            wrong = [2 * (width + length), width + length, width * length + 2 * (width + length)]
        else:
            ask, ans = f"ความยาวรอบรูปกี่{unit}", 2 * (width + length)
            wrong = [width * length, width + length, 2 * width + length]
        return MathDraw("", str(ans), prompt=f"{thing}เป็น{shape} มี{ask}",
                        distractors=_story.keep(*wrong, answer=ans, lo=1))


@question_type("math.rectangle_figure_p4",
               display_name={"th": "หาพื้นที่และความยาวรอบรูปของรูปสี่เหลี่ยมมุมฉากจากรูป"},
               level={"th": "ป.4"}, topic="สี่เหลี่ยมมุมฉาก")
class RectangleFigureP4(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random) -> GeneratedQuestion:
        f = rng.choice(RECT_FIGURES)
        w, length = (f.dims[0], f.dims[0]) if f.kind == "square" else f.dims
        u = _unit(f)
        if rng.random() < 0.5:
            ans = w * length
            ask = f"รูปนี้มีพื้นที่กี่ตาราง{u}"
            wrongs = _nums(2 * (w + length), w + length, w * length * 2, answer=ans, lo=1)
        else:
            ans = 2 * (w + length)
            ask = f"รูปนี้ยาวรอบรูปกี่{u}"
            wrongs = _nums(w * length, w + length, 2 * w + length, answer=ans, lo=1)
        return _math_q([text(ask), _img(f.asset_id, figure_alt(f))], str(ans), wrongs, self.topic)


@question_type("math.construct_rectangle_p4", display_name={"th": "ขั้นตอนการสร้างรูปสี่เหลี่ยมมุมฉาก"},
               level={"th": "ป.4"}, topic="สี่เหลี่ยมมุมฉาก")
class ConstructRectangleP4(_ConstructionSteps):
    def procedures(self, rng):
        a, b = rng.randint(4, 9), rng.randint(2, 6)
        square = rng.random() < 0.3
        if square:
            b = a
        name = "รูปสี่เหลี่ยมจัตุรัส ABCD ยาวด้านละ" if square else "รูปสี่เหลี่ยมผืนผ้า ABCD ที่มี AB ยาว"
        goal = (f"การสร้าง{name} {a} เซนติเมตร" if square
                else f"การสร้าง{name} {a} เซนติเมตร และ BC ยาว {b} เซนติเมตร")
        steps = [
            f"ลากส่วนของเส้นตรง AB ยาว {a} เซนติเมตร",
            "สร้างมุมฉากที่จุด A และที่จุด B โดยใช้ไม้ฉากหรือโพรแทรกเตอร์",
            f"บนแขนของมุมฉากที่จุด B วัดยาว {b} เซนติเมตร ได้จุด C และบนแขนของมุมฉากที่จุด A วัดยาว {b} เซนติเมตร ได้จุด D",
            "ลากส่วนของเส้นตรง CD",
        ]
        faulty = [f"จากจุด B วัดยาว {b} เซนติเมตร ในทิศทางใดก็ได้ แล้วลากเส้นต่อจุด",
                  f"ลากส่วนของเส้นตรง AC ยาว {a} เซนติเมตร"]
        return goal, steps, faulty


@question_type("math.rectangle_missing_side_p4",
               display_name={"th": "หาความยาวด้านจากพื้นที่หรือความยาวรอบรูป"},
               level=LEVEL, topic=_RECT_TOPIC)
class RectangleMissingSideP4(WordProblem):
    def expr(self, rng: Random):
        w, length = rng.randint(3, 20), rng.randint(5, 30)
        kind = rng.randrange(3)
        if kind == 0:
            return MathDraw("", str(length),
                            prompt=(f"รูปสี่เหลี่ยมผืนผ้ามีพื้นที่ {w * length} ตารางเซนติเมตร กว้าง {w} "
                                    f"เซนติเมตร ยาวกี่เซนติเมตร"),
                            distractors=_story.keep(w * length - w, w * length // 2 - w, length + 1, answer=length,
                                                    lo=1))
        if kind == 1:
            per = 2 * (w + length)
            return MathDraw("", str(length),
                            prompt=(f"รูปสี่เหลี่ยมผืนผ้ายาวรอบรูป {per} เซนติเมตร กว้าง {w} "
                                    f"เซนติเมตร ยาวกี่เซนติเมตร"),
                            # Taking the width from the perimeter once, or not halving.
                            distractors=_story.keep(per - w, per - 2 * w, per // 2, answer=length, lo=1))
        s = rng.randint(3, 25)
        return MathDraw("", str(s),
                        prompt=f"รูปสี่เหลี่ยมจัตุรัสยาวรอบรูป {4 * s} เซนติเมตร ด้านยาวด้านละกี่เซนติเมตร",
                        distractors=_story.keep(2 * s, 4 * s, s * s if s * s != 4 * s else s + 2,
                                                answer=s, lo=1))


@question_type("math.rectangle_word_problem_p4",
               display_name={"th": "โจทย์ปัญหาพื้นที่และความยาวรอบรูปสี่เหลี่ยมมุมฉาก"},
               level=LEVEL, topic=_RECT_TOPIC)
class RectangleWordProblemP4(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(6)
        if kind == 3:
            w, length = rng.randint(12, 30), rng.randint(15, 40)
            s = rng.randint(3, min(w, length) - 2)
            ans = w * length - s * s
            return MathDraw("", str(ans),
                            prompt=(f"กระดาษรูปสี่เหลี่ยมผืนผ้ากว้าง {w} เซนติเมตร ยาว {length} เซนติเมตร "
                                    f"ตัดรูปสี่เหลี่ยมจัตุรัสยาวด้านละ {s} เซนติเมตร ออกไป 1 รูป "
                                    f"เหลือกระดาษพื้นที่กี่ตารางเซนติเมตร"),
                            distractors=_story.keep(w * length - 4 * s, w * length, ans - s * s,
                                                    answer=ans, lo=1))
        if kind == 4:
            w, length = rng.randint(8, 25), rng.randint(10, 35)
            ribbon = 2 * (w + length) + rng.randint(5, 60)
            ans = ribbon - 2 * (w + length)
            return MathDraw("", str(ans),
                            prompt=(f"มีริบบิ้นยาว {ribbon} เซนติเมตร นำไปติดรอบกรอบรูปสี่เหลี่ยมผืนผ้า"
                                    f"กว้าง {w} เซนติเมตร ยาว {length} เซนติเมตร พอดีหนึ่งรอบ เหลือริบบิ้นกี่เซนติเมตร"),
                            distractors=_story.keep(ribbon - w - length, ribbon - w * length
                                                    if ribbon > w * length else ans + w, ans + 2,
                                                    answer=ans, lo=1))
        if kind == 5:
            side = rng.randint(4, 25)
            return MathDraw("", str(side * side),
                            prompt=(f"สนามรูปสี่เหลี่ยมจัตุรัสยาวรอบรูป {4 * side} เมตร "
                                    f"สนามนี้มีพื้นที่กี่ตารางเมตร"),
                            distractors=_story.keep(4 * side, 16 * side * side, side * 2,
                                                    answer=side * side, lo=1))
        if kind == 0:
            w, length, cost = rng.randint(5, 30), rng.randint(8, 40), rng.randint(20, 90)
            ans = 2 * (w + length) * cost
            return MathDraw("", str(ans),
                            prompt=(f"สนามหญ้ารูปสี่เหลี่ยมผืนผ้ากว้าง {w} เมตร ยาว {length} เมตร ล้อมรั้วรอบสนาม "
                                    f"ค่ารั้วเมตรละ {cost} บาท เป็นเงินกี่บาท"),
                            distractors=_story.keep(w * length * cost, (w + length) * cost,
                                                    2 * (w + length) + cost, answer=ans))
        if kind == 1:
            tile = rng.choice((1, 2))
            w, length = tile * rng.randint(3, 12), tile * rng.randint(4, 15)
            n = (w // tile) * (length // tile)
            side = "1 เมตร" if tile == 1 else "2 เมตร"
            return MathDraw("", str(n),
                            prompt=(f"ห้องรูปสี่เหลี่ยมผืนผ้ากว้าง {w} เมตร ยาว {length} เมตร ปูด้วยแผ่นยาง"
                                    f"รูปสี่เหลี่ยมจัตุรัสยาวด้านละ {side} พอดี ต้องใช้แผ่นยางกี่แผ่น"),
                            distractors=_story.keep(w * length, 2 * (w + length) // tile, n + w // tile,
                                                    (w * length) // tile, answer=n, lo=1))
        s, price = rng.randint(3, 12), rng.randint(40, 150)
        return MathDraw("", str(s * s * price),
                        prompt=(f"ห้องรูปสี่เหลี่ยมจัตุรัสยาวด้านละ {s} เมตร ปูพื้นด้วยกระเบื้อง "
                                f"ราคาตารางเมตรละ {price} บาท เป็นเงินกี่บาท"),
                        distractors=_story.keep(4 * s * price, 2 * s * price, s * s + price,
                                                answer=s * s * price))
