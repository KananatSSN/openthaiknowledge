"""ปริมาตรและความจุ

คณิตศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.3/*

Sets moved here from: math, math_measure_pictures, math_p3.
"""

from __future__ import annotations

from random import Random

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_measure_pictures import JUGS
from otk.sets._support.math_p3 import LEVEL
from otk.sets._support.math_pictures import _near

PROVENANCE = Provenance("original")


JUG_ALT = "ภาพเหยือกตวงที่มีขีดบอกปริมาตรเป็นมิลลิลิตร และมีน้ำอยู่"


_CAPACITY_TOPIC = "ปริมาตรและความจุ"


@question_type("math.convert_volume_p3",
               display_name={"th": "แปลงลิตรเป็นมิลลิลิตร"}, level={"th": "ป.3"},
               topic="ปริมาตรและความจุ")
class ConvertVolumeP3(WordProblem):
    def expr(self, rng: Random):
        lit = rng.randint(1, 20)
        p = rng.choice(_story.NAMES)
        prompt = rng.choice((
            f"{lit} ลิตร เท่ากับกี่มิลลิลิตร?",
            f"ถังใบหนึ่งจุน้ำได้ {lit} ลิตร ถังใบนี้จุน้ำได้กี่มิลลิลิตร",
            f"{p}ซื้อนมมา {lit} ลิตร เป็นนมกี่มิลลิลิตร",
        ))
        return MathDraw("", str(1000 * lit), prompt=prompt,
                        distractors=[str(100 * lit), str(10 * lit), str(500 * lit)])


@question_type("math.jug_picture_p3", display_name={"th": "อ่านปริมาตรจากเหยือกตวง"},
               level={"th": "ป.3"}, topic="ปริมาตรและความจุ")
class JugPictureP3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        j = rng.choice(JUGS)
        marks = j.level // j.step
        # One mark off either way; counting marks; reading each mark as 100.
        wrongs = [j.level + j.step, j.level - j.step, marks, marks * 100 if j.step != 100 else marks * 50]
        return _math_q([text("ในเหยือกมีน้ำกี่มิลลิลิตร"), image(j.asset_id, alt=JUG_ALT)],
                       str(j.level), _near(j.level, *wrongs, lo=1), self.topic)


@question_type("math.kitchen_measures_p3",
               display_name={"th": "ช้อนชา ช้อนโต๊ะ ถ้วยตวง และมิลลิลิตร"},
               level=LEVEL, topic=_CAPACITY_TOPIC)
class KitchenMeasuresP3(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(4)
        if kind == 0:
            n = rng.randint(2, 9)
            return MathDraw("", str(3 * n),
                            prompt=(f"กำหนดให้ 1 ช้อนโต๊ะ เท่ากับ 3 ช้อนชา "
                                    f"{n} ช้อนโต๊ะ เท่ากับกี่ช้อนชา"),
                            distractors=_story.keep(n + 3, n, 3 * n + 3, answer=3 * n))
        if kind == 1:
            n = rng.randint(2, 12)
            return MathDraw("", str(5 * n),
                            prompt=f"กำหนดให้ 1 ช้อนชา เท่ากับ 5 มิลลิลิตร ยาน้ำ {n} ช้อนชา เท่ากับกี่มิลลิลิตร",
                            distractors=_story.keep(n + 5, 15 * n, 5 * n + 5, answer=5 * n))
        if kind == 2:
            n = rng.randint(2, 8)
            return MathDraw("", str(15 * n),
                            prompt=(f"กำหนดให้ 1 ช้อนโต๊ะ เท่ากับ 15 มิลลิลิตร น้ำปลา {n} ช้อนโต๊ะ "
                                    f"เท่ากับกี่มิลลิลิตร"),
                            distractors=_story.keep(5 * n, n + 15, 15 * n + 15, answer=15 * n))
        cups = rng.randint(2, 6)
        return MathDraw("", str(16 * cups),
                        prompt=(f"กำหนดให้ 1 ถ้วยตวง เท่ากับ 16 ช้อนโต๊ะ แป้ง {cups} ถ้วยตวง "
                                f"เท่ากับกี่ช้อนโต๊ะ"),
                        distractors=_story.keep(cups + 16, 3 * 16 * cups, 16 * cups + 16,
                                                answer=16 * cups))


@question_type("math.capacity_word_problem_p3",
               display_name={"th": "โจทย์ปัญหาปริมาตรและความจุ (ลิตร มิลลิลิตร)"},
               level=LEVEL, topic=_CAPACITY_TOPIC)
class CapacityWordProblemP3(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        kind = rng.randrange(4)
        if kind == 0:
            length, ml = rng.randint(1, 9), rng.randrange(50, 1000, 50)
            ans = 1000 * length + ml
            return MathDraw("", str(ans),
                            prompt=f"น้ำ {length} ลิตร {ml} มิลลิลิตร เท่ากับกี่มิลลิลิตร",
                            distractors=_story.keep(100 * length + ml, length + ml, 10 * length + ml, answer=ans))
        if kind == 1:
            n, each = rng.randint(2, 8), rng.choice((150, 200, 250, 300, 350))
            ans = n * each
            return MathDraw("", str(ans),
                            prompt=f"{p}เทนมใส่แก้ว {n} ใบ ใบละ {each} มิลลิลิตร ใช้นมทั้งหมดกี่มิลลิลิตร",
                            distractors=_story.keep(n + each, ans + each, ans - each, answer=ans))
        if kind == 2:
            tank = rng.randint(2, 20)
            used_l, used_ml = rng.randint(0, tank - 1), rng.randrange(100, 1000, 100)
            used = 1000 * used_l + used_ml
            ans = 1000 * tank - used
            return MathDraw("", str(ans),
                            prompt=(f"ถังมีน้ำ {tank} ลิตร ใช้รดน้ำต้นไม้ไป {used_l} ลิตร {used_ml} "
                                    f"มิลลิลิตร เหลือน้ำในถังกี่มิลลิลิตร" if used_l else
                                    f"ถังมีน้ำ {tank} ลิตร ใช้รดน้ำต้นไม้ไป {used_ml} มิลลิลิตร "
                                    f"เหลือน้ำในถังกี่มิลลิลิตร"),
                            distractors=_story.keep(1000 * tank + used, ans + 1000, ans - 100,
                                                    answer=ans, lo=1))
        bottle = rng.choice((250, 500, 750))
        litres = rng.randint(1, 6)
        total = 1000 * litres
        n = total // bottle
        total = n * bottle
        length, ml = divmod(total, 1000)
        said = f"{length} ลิตร" + (f" {ml} มิลลิลิตร" if ml else "")
        return MathDraw("", str(n),
                        prompt=f"น้ำผลไม้ {said} แบ่งใส่ขวด ขวดละ {bottle} มิลลิลิตร ได้กี่ขวด",
                        distractors=_story.keep(n + 1, n * 2, n - 1, length, answer=n, lo=1))
