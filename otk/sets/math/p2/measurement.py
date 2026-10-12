"""การวัด

คณิตศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.2/*

Sets moved here from: math, math_gaps_primary, math_measure_pictures, math_p2.
"""

from __future__ import annotations

from random import Random

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import _text_q
from otk.sets._support.math_measure_pictures import SCALES
from otk.sets._support.math_p2 import LEVEL

PROVENANCE = Provenance("original")


SCALE_ALT = "ภาพหน้าปัดเครื่องชั่งสปริง มีเข็มชี้"


def _kg_khit(kg: int, khit: int) -> str:
    if kg == 0:
        return f"{khit} ขีด"
    return f"{kg} กิโลกรัม {khit} ขีด" if khit else f"{kg} กิโลกรัม"


@question_type("math.convert_length_p2",
               display_name={"th": "แปลงเมตรเป็นเซนติเมตร"}, level={"th": "ป.2"}, topic="การวัด")
class ConvertLengthP2(WordProblem):
    def expr(self, rng: Random):
        m = rng.randint(1, 9)
        cm = rng.choice([0, 0, rng.randint(5, 95)])
        ans = 100 * m + cm
        said = f"{m} เมตร" + (f" {cm} เซนติเมตร" if cm else "")
        thing = rng.choice(("", "ผ้าผืนหนึ่งยาว ", "เชือกเส้นหนึ่งยาว ", "โต๊ะตัวหนึ่งยาว ",
                            "ต้นไม้ต้นหนึ่งสูง "))
        prompt = (f"{thing}{said} คิดเป็นกี่เซนติเมตร?" if thing
                  else f"{said} เท่ากับกี่เซนติเมตร?")
        # Treating a metre as 10 cm, and writing the parts side by side.
        return MathDraw("", str(ans), prompt=prompt,
                        distractors=_story.keep(10 * m + cm, 1000 * m + cm, m + cm,
                                                int(f"{m}{cm}") if cm else 100 * m + 100,
                                                answer=ans))


@question_type("math.scale_picture_p2", display_name={"th": "อ่านน้ำหนักจากหน้าปัดเครื่องชั่ง"},
               level={"th": "ป.2"}, topic="การวัด")
class ScalePictureP2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(SCALES)
        right = _kg_khit(s.kg, s.khit)
        # The next kilogram mark; one small mark off either way; ขีด read as kilograms.
        wrongs = [_kg_khit(s.kg + 1, s.khit), _kg_khit(s.kg, (s.khit + 1) % 10),
                  _kg_khit(s.kg, (s.khit - 1) % 10), _kg_khit(s.khit, s.kg), _kg_khit(s.kg + 1, 0)]
        return _text_q([text("เครื่องชั่งอ่านน้ำหนักได้เท่าใด (1 กิโลกรัม มี 10 ขีด)"),
                        image(s.asset_id, alt=SCALE_ALT)],
                       right, [w for w in dict.fromkeys(wrongs) if w != right], self.topic)


@question_type("math.convert_weight_p2",
               display_name={"th": "แปลงกิโลกรัมเป็นขีด"}, level={"th": "ป.2"}, topic="การวัด")
class ConvertWeightP2(WordProblem):
    def expr(self, rng: Random):
        kg = rng.randint(1, 9)
        khit = rng.choice([0, rng.randint(1, 9)])
        ans = 10 * kg + khit
        said = f"{kg} กิโลกรัม" + (f" {khit} ขีด" if khit else "")
        thing = rng.choice(("", "ส้มหนัก ", "เนื้อหมูหนัก ", "ข้าวสารหนัก ", "แตงโมหนัก "))
        prompt = (f"{thing}{said} คิดเป็นกี่ขีด?" if thing
                  else f"{said} เท่ากับกี่ขีด?")
        return MathDraw("", str(ans), prompt=prompt,
                        distractors=_story.keep(100 * kg + khit, kg + khit, 1000 * kg + khit,
                                                10 * kg + 10, answer=ans))


@question_type("math.capacity_litre_p2",
               display_name={"th": "ปริมาตรและความจุเป็นลิตร"},
               level={"th": "ป.2"}, topic="การวัด")
class CapacityLitreP2(WordProblem):
    _BIG = ("ถังน้ำ", "หม้อ", "โอ่ง", "กะละมัง", "ตู้ปลา")
    _SMALL = ("ขวด", "เหยือก", "กระติก", "แก้วตวง")

    def expr(self, rng: Random):
        big, small = rng.choice(self._BIG), rng.choice(self._SMALL)
        kind = rng.randrange(4)
        if kind == 0:
            a, b = rng.randint(12, 60), rng.randint(2, 9)
            return MathDraw("", str(a - b), prompt=(
                f"{big}ใบหนึ่งจุน้ำได้ {a} ลิตร {small}ใบหนึ่งจุน้ำได้ {b} ลิตร "
                f"{big}จุน้ำได้มากกว่า{small}กี่ลิตร"),
                distractors=_story.keep(a + b, a - b + 1, a, answer=a - b, lo=1))
        if kind == 1:
            each, n = rng.randint(2, 5), rng.randint(3, 9)
            return MathDraw("", str(each * n), prompt=(
                f"เทน้ำจาก{small}ที่มีน้ำเต็ม {n} ใบ ใบละ {each} ลิตร ลงใน{big} "
                f"{big}มีน้ำกี่ลิตร"),
                distractors=_story.keep(each + n, each * (n - 1), each * n + each,
                                        answer=each * n, lo=1))
        if kind == 2:
            each, n = rng.randint(2, 5), rng.randint(3, 9)
            total = each * n
            return MathDraw("", str(n), prompt=(
                f"{big}จุน้ำได้ {total} ลิตร ใช้{small}ที่จุ {each} ลิตร ตักน้ำใส่ "
                f"ต้องตักกี่ครั้ง{big}จึงจะเต็มพอดี"),
                distractors=_story.keep(total - each, n + 1, each, total, answer=n, lo=1))
        full, used, more = rng.randint(10, 40), rng.randint(2, 9), rng.randint(2, 9)
        left = full - used + more
        return MathDraw("", str(left), prompt=(
            f"{big}มีน้ำ {full} ลิตร ใช้ไป {used} ลิตร แล้วเติมน้ำเพิ่มอีก {more} ลิตร "
            f"ตอนนี้{big}มีน้ำกี่ลิตร"),
            distractors=_story.keep(full - used - more, full + used + more, full - used,
                                    answer=left, lo=1))


@question_type("math.length_word_problem_p2",
               display_name={"th": "โจทย์ปัญหาความยาว (เมตร เซนติเมตร)"},
               level=LEVEL, topic="การวัด")
class LengthWordProblemP2(WordProblem):
    def expr(self, rng: Random):
        p, q = _story.names(rng)
        m1, c1 = rng.randint(1, 4), rng.randint(5, 95)
        m2, c2 = rng.randint(1, 4), rng.randint(5, 95)
        x, y = 100 * m1 + c1, 100 * m2 + c2
        kind = rng.randrange(6)
        if kind == 3:
            more = rng.randint(5, 60)
            return MathDraw("", str(x + more),
                            prompt=(f"{p}กระโดดไกลได้ {m1} เมตร {c1} เซนติเมตร {q}กระโดดได้ไกลกว่า{p} "
                                    f"{more} เซนติเมตร {q}กระโดดได้ไกลกี่เซนติเมตร"),
                            distractors=_story.keep(x - more, m1 + c1 + more, x + more + 100,
                                                    answer=x + more, lo=1))
        if kind == 4:
            n, each = rng.randint(2, 5), rng.randint(20, 95)
            return MathDraw("", str(n * each),
                            prompt=(f"{p}ต่อริบบิ้น {n} เส้น ยาวเส้นละ {each} เซนติเมตร โดยไม่ซ้อนกัน "
                                    f"ได้ริบบิ้นยาวกี่เซนติเมตร"),
                            distractors=_story.keep(n + each, each * (n - 1), n * each + 10,
                                                    answer=n * each, lo=1))
        if kind == 5:
            whole = rng.randint(2, 9)
            walked = rng.randint(30, 100 * whole - 10)
            return MathDraw("", str(100 * whole - walked),
                            prompt=(f"ทางเดินไปห้องสมุดยาว {whole} เมตร {p}เดินไปแล้ว {walked} เซนติเมตร "
                                    f"ต้องเดินอีกกี่เซนติเมตรจึงจะถึง"),
                            distractors=_story.keep(100 * whole + walked, abs(whole - walked),
                                                    100 * whole - walked + 100,
                                                    answer=100 * whole - walked, lo=1))
        if kind == 0:
            ans = x + y
            return MathDraw("", str(ans),
                            prompt=(f"ผ้าผืนแรกยาว {m1} เมตร {c1} เซนติเมตร ผืนที่สองยาว {m2} "
                                    f"เมตร {c2} เซนติเมตร ผ้าสองผืนยาวรวมกันกี่เซนติเมตร"),
                            distractors=_story.keep(10 * (m1 + m2) + c1 + c2, ans - 100,
                                                    ans + 100, abs(x - y), answer=ans))
        if kind == 1:
            # Children's heights: a little over a metre.
            big = rng.randint(115, 160)
            small = rng.randint(100, big - 3)
            hb, hs = divmod(big, 100)
            return MathDraw("", str(big - small),
                            prompt=(f"{p}สูง {hb} เมตร {hs} เซนติเมตร {q}สูง {small} "
                                    f"เซนติเมตร {p}สูงกว่า{q}กี่เซนติเมตร"),
                            distractors=_story.keep(abs(10 * hb + hs - small), big + small,
                                                    big - small + 100, answer=big - small, lo=1))
        whole = rng.randint(3, 9)
        cut = rng.randint(60, 100 * whole - 20)
        return MathDraw("", str(100 * whole - cut),
                        prompt=(f"เชือกยาว {whole} เมตร ตัดออกไป {cut} เซนติเมตร "
                                f"เหลือเชือกยาวกี่เซนติเมตร"),
                        distractors=_story.keep(abs(whole - cut), 10 * whole - cut if 10 * whole > cut
                                                else 100 * whole + cut, 100 * whole - cut + 100,
                                                answer=100 * whole - cut, lo=1))


@question_type("math.weight_word_problem_p2",
               display_name={"th": "โจทย์ปัญหาน้ำหนัก (กิโลกรัม กรัม ขีด)"},
               level=LEVEL, topic="การวัด")
class WeightWordProblemP2(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        kind = rng.randrange(4)
        if kind == 0:
            kg, g = rng.randint(1, 5), rng.choice(range(50, 1000, 50))
            ans = 1000 * kg + g
            return MathDraw("", str(ans), prompt=f"{kg} กิโลกรัม {g} กรัม เท่ากับกี่กรัม",
                            distractors=_story.keep(100 * kg + g, kg + g, 1000 * kg + 10 * g,
                                                    answer=ans))
        if kind == 1:
            k = rng.randint(2, 9)
            return MathDraw("", str(100 * k),
                            prompt=f"{k} ขีด เท่ากับกี่กรัม (1 ขีด เท่ากับ 100 กรัม)",
                            distractors=_story.keep(10 * k, 1000 * k, k, answer=100 * k))
        if kind == 2:
            a, b = rng.sample(range(2, 10), 2)
            meat, veg = rng.sample(("เนื้อหมู", "เนื้อไก่", "กุ้ง", "ผักบุ้ง", "ถั่วฝักยาว"), 2)
            return MathDraw("", str(100 * (a + b)),
                            prompt=(f"แม่ซื้อ{meat} {a} ขีด และ{veg} {b} ขีด "
                                    f"รวมหนักกี่กรัม"),
                            distractors=_story.keep(a + b, 10 * (a + b), 1000 * (a + b),
                                                    100 * abs(a - b), answer=100 * (a + b)))
        bag = rng.randint(2, 5)
        used = rng.choice(range(100, 1000 * bag, 50))
        ans = 1000 * bag - used
        return MathDraw("", str(ans),
                        prompt=(f"{p}มีแป้ง {bag} กิโลกรัม ใช้ทำขนมไป {used} กรัม "
                                f"เหลือแป้งกี่กรัม"),
                        distractors=_story.keep(100 * bag - used if 100 * bag > used else used - bag,
                                                1000 * bag + used, ans + 100, answer=ans, lo=1))
