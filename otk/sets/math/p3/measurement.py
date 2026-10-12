"""การวัด

คณิตศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.3/*

Sets moved here from: math, math_gaps_primary, math_p3.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_gaps_primary import _c, _choices, _cs
from otk.sets._support.math_p3 import LEVEL

PROVENANCE = Provenance("original")


# (object, typical amount, unit, kind of quantity). Each amount is what a
# ป.3 book would accept as a sensible estimate. The wrong choices keep the
# number and change the unit, so the question is about the size of a unit.
_ESTIMATES = (
    ("ความยาวของดินสอ", 18, "เซนติเมตร", "ยาว"),
    ("ความสูงของประตูห้องเรียน", 2, "เมตร", "ยาว"),
    ("ความหนาของเหรียญหนึ่งบาท", 2, "มิลลิเมตร", "ยาว"),
    ("ความยาวของมดตัวหนึ่ง", 5, "มิลลิเมตร", "ยาว"),
    ("ความสูงของโต๊ะนักเรียน", 70, "เซนติเมตร", "ยาว"),
    ("ความยาวของสนามฟุตบอล", 100, "เมตร", "ยาว"),
    ("ระยะทางจากกรุงเทพฯ ถึงเชียงใหม่", 700, "กิโลเมตร", "ยาว"),
    ("ความยาวของสมุดเล่มหนึ่ง", 25, "เซนติเมตร", "ยาว"),
    ("น้ำหนักของไข่ไก่หนึ่งฟอง", 60, "กรัม", "หนัก"),
    ("น้ำหนักของแตงโมหนึ่งผล", 3, "กิโลกรัม", "หนัก"),
    ("น้ำหนักของช้างหนึ่งตัว", 4, "เมตริกตัน", "หนัก"),
    ("น้ำหนักของนักเรียนชั้น ป.3 หนึ่งคน", 30, "กิโลกรัม", "หนัก"),
    ("น้ำหนักของยางลบหนึ่งก้อน", 20, "กรัม", "หนัก"),
    ("น้ำหนักของรถยนต์หนึ่งคัน", 1, "เมตริกตัน", "หนัก"),
    ("ความจุของแก้วน้ำหนึ่งใบ", 250, "มิลลิลิตร", "จุ"),
    ("ความจุของถังน้ำหนึ่งใบ", 10, "ลิตร", "จุ"),
    ("ความจุของช้อนชาหนึ่งช้อน", 5, "มิลลิลิตร", "จุ"),
    ("ความจุของอ่างอาบน้ำหนึ่งอ่าง", 200, "ลิตร", "จุ"),
)


_UNITS = {
    "ยาว": ("มิลลิเมตร", "เซนติเมตร", "เมตร", "กิโลเมตร"),
    "หนัก": ("กรัม", "กิโลกรัม", "เมตริกตัน", "ขีด"),
    "จุ": ("มิลลิลิตร", "ลิตร"),
}


# (what is measured, the tool, the kind of quantity). The wrong tools measure
# a different quantity, so exactly one choice can do the job.
_TOOLS = (
    ("ความยาวของดินสอ", "ไม้บรรทัด", "ยาว"),
    ("ความยาวของห้องเรียน", "ตลับเมตร", "ยาว"),
    ("รอบเอวของนักเรียน", "สายวัด", "ยาว"),
    ("น้ำหนักของผลไม้ที่ตลาด", "เครื่องชั่งสปริง", "หนัก"),
    ("น้ำหนักตัวของนักเรียน", "เครื่องชั่งน้ำหนักตัว", "หนัก"),
    ("น้ำหนักของรถบรรทุกที่บรรทุกข้าวสาร", "เครื่องชั่งรถบรรทุก", "หนัก"),
    ("ปริมาณน้ำ 2 ลิตร สำหรับทำอาหาร", "เหยือกตวง", "จุ"),
    ("ปริมาณยาน้ำ 5 มิลลิลิตร", "ช้อนตวง", "จุ"),
)


@question_type("math.convert_length_p3",
               display_name={"th": "แปลงหน่วยความยาว"}, level={"th": "ป.3"}, topic="การวัด")
class ConvertLengthP3(WordProblem):
    _UNITS = [("กิโลเมตร", "เมตร", 1000), ("เมตร", "เซนติเมตร", 100),
              ("เซนติเมตร", "มิลลิเมตร", 10)]

    def expr(self, rng: Random):
        src, dst, k = rng.choice(self._UNITS)
        x = rng.randint(1, 20)
        return MathDraw("", str(x * k),
                        prompt=f"{x} {src} เท่ากับกี่{dst}?",
                        distractors=[str(x * k // 10), str(x * k * 10), str(x)])


@question_type("math.estimate_measure_p3",
               display_name={"th": "คาดคะเนความยาว น้ำหนัก และปริมาตร"},
               level={"th": "ป.3"}, topic="การวัด")
class EstimateMeasureP3(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        thing, amount, unit, kind = rng.choice(_ESTIMATES)
        wrongs = [f"ประมาณ {amount} {u}" for u in _UNITS[kind] if u != unit]
        if kind == "จุ":
            # Two units only, so also offer amounts a hundred and a thousand times off.
            wrongs += [f"ประมาณ {amount * 100} {unit}", f"ประมาณ {amount * 1000} {unit}"]
        return _choices([text(f"เมื่อคาดคะเน {thing}น่าจะเป็นเท่าใด")],
                        f"ประมาณ {amount} {unit}", wrongs, self.topic)


@question_type("math.measuring_tool_p3",
               display_name={"th": "เลือกเครื่องมือวัดที่เหมาะสม"},
               level={"th": "ป.3"}, topic="การวัด")
class MeasuringToolP3(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        what, tool, kind = rng.choice(_TOOLS)
        wrongs = [t for _, t, k in _TOOLS if k != kind]
        rng.shuffle(wrongs)
        return _choices([text(f"ถ้าต้องการวัด{what} ควรใช้เครื่องมือใด")], tool, wrongs, self.topic)


@question_type("math.convert_weight_p3",
               display_name={"th": "แปลงกิโลกรัมเป็นกรัม"}, level={"th": "ป.3"}, topic="การวัด")
class ConvertWeightP3(WordProblem):
    def expr(self, rng: Random):
        kg = rng.randint(1, 20)
        p = rng.choice(_story.NAMES)
        goods = rng.choice(("ข้าวสาร", "น้ำตาลทราย", "ส้ม", "แป้ง"))
        prompt = rng.choice((
            f"{kg} กิโลกรัม เท่ากับกี่กรัม?",
            f"{p}ซื้อ{goods}หนัก {kg} กิโลกรัม {goods}หนักกี่กรัม",
            f"กระเป๋าเดินทางใบหนึ่งหนัก {kg} กิโลกรัม คิดเป็นกี่กรัม",
        ))
        return MathDraw("", str(1000 * kg), prompt=prompt,
                        distractors=[str(100 * kg), str(10 * kg),
                                     str(1000 * kg + 100)])


@question_type("math.metric_ton_p3",
               display_name={"th": "เมตริกตันและกิโลกรัม"},
               level={"th": "ป.3"}, topic="การวัด")
class MetricTonP3(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(4)
        t = rng.randint(2, 9)
        if kind == 0:
            return MathDraw("", _c(t * 1000), prompt=f"{t} เมตริกตัน เท่ากับกี่กิโลกรัม",
                            distractors=[_c(t * 100), _c(t * 10), _c(t * 10000)])
        if kind == 1:
            kg = rng.choice(range(50, 1000, 50))
            total = t * 1000 + kg
            return MathDraw("", _c(total), prompt=f"{t} เมตริกตัน {kg} กิโลกรัม เท่ากับกี่กิโลกรัม",
                            distractors=_cs(t * 100 + kg, t + kg, t * 1000 + kg * 10, answer=total))
        if kind == 2:
            sold = rng.choice(range(250, 1000, 50))
            left = t * 1000 - sold
            return MathDraw("", _c(left), prompt=(
                f"รถบรรทุกบรรทุกข้าวสาร {t} เมตริกตัน นำไปส่งร้านค้า {sold} กิโลกรัม "
                f"บนรถเหลือข้าวสารกี่กิโลกรัม"),
                distractors=_cs(t * 1000 + sold, t * 100 + sold, left + 100, answer=left))
        per, n = rng.choice((250, 400, 500)), rng.randint(3, 8)
        if per * n == 1000:
            n += 1
        total = per * n
        more = "มากกว่า" if total > 1000 else "น้อยกว่า"
        diff = abs(total - 1000)
        return MathDraw("", _c(diff), prompt=(
            f"ลังผลไม้ {n} ลัง หนักลังละ {per} กิโลกรัม ผลไม้ทั้งหมดหนัก{more} 1 เมตริกตัน "
            f"อยู่กี่กิโลกรัม"),
            distractors=_cs(total, abs(total - 100), diff + per, answer=diff))


@question_type("math.length_word_problem_p3",
               display_name={"th": "โจทย์ปัญหาความยาว (กิโลเมตร เมตร เซนติเมตร มิลลิเมตร)"},
               level=LEVEL, topic="การวัด")
class LengthWordProblemP3(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        kind = rng.randrange(4)
        if kind == 0:
            km, m = rng.randint(1, 9), rng.randrange(50, 1000, 50)
            ans = 1000 * km + m
            return MathDraw("", str(ans),
                            prompt=(f"ระยะทางจากบ้าน{p}ถึงโรงเรียน {km} กิโลเมตร {m} เมตร "
                                    f"คิดเป็นกี่เมตร"),
                            distractors=_story.keep(100 * km + m, km + m, 10000 * km + m,
                                                    answer=ans))
        if kind == 1:
            walk = rng.randrange(150, 1000, 50)
            km, m = rng.randint(1, 5), rng.randrange(100, 1000, 100)
            ans = walk + 1000 * km + m
            return MathDraw("", str(ans),
                            prompt=(f"{p}เดินไปป้ายรถ {walk} เมตร แล้วนั่งรถต่ออีก {km} "
                                    f"กิโลเมตร {m} เมตร {p}เดินทางทั้งหมดกี่เมตร"),
                            distractors=_story.keep(walk + km + m, walk + 100 * km + m,
                                                    ans - walk, answer=ans))
        if kind == 2:
            cm, mm = rng.randint(5, 30), rng.randint(1, 9)
            ans = 10 * cm + mm
            thing = rng.choice(("ดินสอ", "ตะปู", "ใบไม้", "ยางลบ", "กิ่งไม้"))
            return MathDraw("", str(ans),
                            prompt=f"{thing}ยาว {cm} เซนติเมตร {mm} มิลลิเมตร คิดเป็นกี่มิลลิเมตร",
                            distractors=_story.keep(100 * cm + mm, cm + mm, 10 * cm, answer=ans))
        piece = rng.choice((20, 25, 50))
        metres = rng.randint(2, 9)
        ans = 100 * metres // piece
        return MathDraw("", str(ans),
                        prompt=(f"ริบบิ้นยาว {metres} เมตร ตัดเป็นเส้นละ {piece} เซนติเมตร "
                                f"ได้ริบบิ้นกี่เส้น"),
                        # Dividing metres by centimetres without converting.
                        distractors=_story.keep(10 * metres // piece or metres, piece * metres,
                                                ans + 1, ans // 2, answer=ans, lo=1))


@question_type("math.weight_word_problem_p3",
               display_name={"th": "โจทย์ปัญหาน้ำหนัก (กิโลกรัม กรัม)"},
               level=LEVEL, topic="การวัด")
class WeightWordProblemP3(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        kind = rng.randrange(4)
        if kind == 0:
            k1, g1 = rng.randint(1, 4), rng.randrange(100, 1000, 50)
            k2, g2 = rng.randint(1, 4), rng.randrange(100, 1000, 50)
            x, y = rng.sample(("ส้ม", "มะม่วง", "องุ่น", "มังคุด", "เงาะ"), 2)
            ans = 1000 * (k1 + k2) + g1 + g2
            return MathDraw("", str(ans),
                            prompt=(f"แม่ซื้อ{x} {k1} กิโลกรัม {g1} กรัม และ{y} {k2} กิโลกรัม "
                                    f"{g2} กรัม รวมหนักกี่กรัม"),
                            distractors=_story.keep(100 * (k1 + k2) + g1 + g2,
                                                    1000 * (k1 + k2) + g1 + g2 - 1000,
                                                    k1 + k2 + g1 + g2, answer=ans))
        if kind == 1:
            bag = rng.randint(1, 5)
            used = rng.randrange(150, 1000 * bag, 50)
            ans = 1000 * bag - used
            return MathDraw("", str(ans),
                            prompt=f"{p}มีน้ำตาล {bag} กิโลกรัม ใช้ทำขนมไป {used} กรัม เหลือน้ำตาลกี่กรัม",
                            distractors=_story.keep(1000 * bag + used, abs(100 * bag - used),
                                                    ans + 100, answer=ans, lo=1))
        if kind == 2:
            n, g = rng.randint(3, 12), rng.randrange(150, 900, 50)
            ans = n * g
            return MathDraw("", str(ans),
                            prompt=f"กล่องใส่ขนมหนักกล่องละ {g} กรัม {n} กล่องหนักกี่กรัม",
                            distractors=_story.keep(n + g, ans + g, ans - g, answer=ans))
        a, b = sorted(rng.sample(range(1200, 9000, 50), 2), reverse=True)
        ka, ga = divmod(a, 1000)
        return MathDraw("", str(a - b),
                        prompt=(f"แตงโมผลแรกหนัก {ka} กิโลกรัม {ga} กรัม ผลที่สองหนัก {b} กรัม "
                                f"ผลแรกหนักกว่าผลที่สองกี่กรัม"),
                        distractors=_story.keep(a + b, abs(ka * 100 + ga - b), a - b + 1000,
                                                answer=a - b, lo=1))
