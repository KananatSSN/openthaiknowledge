"""ฟังก์ชันในชีวิตจริง

คณิตศาสตร์ · ม.5 · สสวท. พื้นฐาน
Indicators: ค 1.2 ม.5/1

Sets moved here from: math_gaps_secondary.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_gaps_secondary import _choices, _num

PROVENANCE = Provenance("original")


_FUNC_TOPIC = "ฟังก์ชันในชีวิตจริง"


_MODELS = (
    ("ค่าจอดรถคิดชั่วโมงละ 20 บาท เศษของชั่วโมงคิดเป็นหนึ่งชั่วโมง", "ฟังก์ชันขั้นบันได"),
    ("ค่าแท็กซี่ 35 บาทแรก และกิโลเมตรต่อไปคิดกิโลเมตรละ 6 บาทเท่ากันตลอด", "ฟังก์ชันเชิงเส้น"),
    ("ความสูงของลูกบอลที่โยนขึ้นไปแล้วตกลงมา เทียบกับเวลา", "ฟังก์ชันกำลังสอง"),
    ("จำนวนแบคทีเรียที่เพิ่มขึ้นเป็นสองเท่าทุกชั่วโมง", "ฟังก์ชันเอกซ์โพเนนเชียล"),
    ("เงินฝากที่ได้ดอกเบี้ยทบต้นร้อยละ 3 ต่อปี เทียบกับจำนวนปี", "ฟังก์ชันเอกซ์โพเนนเชียล"),
    ("ค่าไฟฟ้าที่คิดหน่วยละ 4 บาทเท่ากันทุกหน่วย เทียบกับจำนวนหน่วยที่ใช้", "ฟังก์ชันเชิงเส้น"),
    ("พื้นที่ของรูปสี่เหลี่ยมจัตุรัส เทียบกับความยาวด้าน", "ฟังก์ชันกำลังสอง"),
    ("ค่าส่งพัสดุที่คิดตามช่วงน้ำหนัก 0–1 กิโลกรัม 30 บาท 1–2 กิโลกรัม 45 บาท", "ฟังก์ชันขั้นบันได"),
    ("เงินเดือนที่เพิ่มขึ้นปีละ 1,000 บาทเท่ากันทุกปี เทียบกับจำนวนปี", "ฟังก์ชันเชิงเส้น"),
    ("มูลค่ารถยนต์ที่ลดลงร้อยละ 10 ของมูลค่าในปีก่อนทุกปี", "ฟังก์ชันเอกซ์โพเนนเชียล"),
    ("ระยะทางที่วัตถุตกอย่างอิสระ เทียบกับเวลาที่ตก", "ฟังก์ชันกำลังสอง"),
    ("ค่าโทรศัพท์ที่คิดนาทีละ 1 บาท เศษของนาทีคิดเป็นหนึ่งนาที", "ฟังก์ชันขั้นบันได"),
    ("ปริมาณสารกัมมันตรังสีที่เหลือครึ่งหนึ่งทุก 5 ปี", "ฟังก์ชันเอกซ์โพเนนเชียล"),
    ("ระยะทางที่รถวิ่งด้วยอัตราเร็วคงตัว 60 กิโลเมตรต่อชั่วโมง เทียบกับเวลา", "ฟังก์ชันเชิงเส้น"),
    ("พื้นที่ของวงกลม เทียบกับรัศมี", "ฟังก์ชันกำลังสอง"),
    ("ค่าเช่าจักรยานชั่วโมงละ 15 บาท เศษของชั่วโมงคิดเป็นหนึ่งชั่วโมง", "ฟังก์ชันขั้นบันได"),
)


_KINDS = ("ฟังก์ชันเชิงเส้น", "ฟังก์ชันกำลังสอง", "ฟังก์ชันเอกซ์โพเนนเชียล", "ฟังก์ชันขั้นบันได")


@question_type("math.function_model_type_m5", display_name={"th": "เลือกชนิดของฟังก์ชันที่อธิบายสถานการณ์"},
               level={"th": "ม.5"}, topic=_FUNC_TOPIC)
class FunctionModelTypeM5(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        situation, kind = rng.choice(_MODELS)
        return _choices([text(f"สถานการณ์ “{situation}” อธิบายได้ด้วยฟังก์ชันชนิดใดเหมาะสมที่สุด")],
                        kind, [k for k in _KINDS if k != kind], self.topic)


@question_type("math.function_context_value_m5", display_name={"th": "หาค่าของฟังก์ชันในสถานการณ์"},
               level={"th": "ม.5"}, topic=_FUNC_TOPIC)
class FunctionContextValueM5(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            rate, hours, mins = rng.choice((10, 20, 30)), rng.randint(1, 5), rng.choice((10, 20, 30, 40, 50))
            value = rate * (hours + 1)
            return MathDraw("", str(value), prompt=(
                f"ลานจอดรถคิดค่าจอดชั่วโมงละ {rate} บาท เศษของชั่วโมงคิดเป็นหนึ่งชั่วโมง "
                f"ถ้าจอดรถ {hours} ชั่วโมง {mins} นาที ต้องจ่ายกี่บาท"),
                distractors=_story.keep(rate * hours, rate * hours + mins, rate * (hours + 2), answer=value, lo=1))
        if kind == 1:
            start, per, km = rng.choice((35, 40)), rng.choice((5, 6, 7)), rng.randint(4, 20)
            value = start + per * (km - 1)
            return MathDraw("", str(value), prompt=(
                f"ค่าโดยสารแท็กซี่เป็นไปตามฟังก์ชัน f(x) = {start} + {per}(x − 1) บาท เมื่อ x คือระยะทาง "
                f"(กิโลเมตร) และ x ≥ 1 นั่งไป {km} กิโลเมตรต้องจ่ายกี่บาท"),
                distractors=_story.keep(start + per * km, (start + per) * km, per * km, answer=value, lo=1))
        start, hours = rng.choice((100, 200, 500)), rng.randint(2, 5)
        value = start * 2 ** hours
        return MathDraw("", _num(value), prompt=(
            f"แบคทีเรียมีจำนวน {start} เซลล์ และเพิ่มเป็นสองเท่าทุกชั่วโมง ตามฟังก์ชัน N(t) = {start} · 2ᵗ "
            f"เมื่อ t คือเวลา (ชั่วโมง) เมื่อเวลาผ่านไป {hours} ชั่วโมง มีแบคทีเรียกี่เซลล์"),
            distractors=[_num(int(v)) for v in
                         _story.keep(start * 2 * hours, start + 2 ** hours, start * 2 ** (hours - 1),
                                     answer=value, lo=1)])


@question_type("math.function_interpret_m5", display_name={"th": "ใช้กราฟของฟังก์ชันอธิบายสถานการณ์"},
               level={"th": "ม.5"}, topic=_FUNC_TOPIC)
class FunctionInterpretM5(WordProblem):
    def expr(self, rng: Random):
        if rng.random() < 0.5:
            # h(t) = −5t² + vt + h0 reaches its top at t = v/10.
            v = rng.choice((10, 20, 30, 40))
            h0 = rng.choice((0, 5, 10, 15))
            t = v // 10
            top = -5 * t * t + v * t + h0
            rule = f"−5t² + {v}t" + (f" + {h0}" if h0 else "")
            # Dropping the −5t², answering with the time, and h(1) instead of h(v/10).
            return MathDraw("", str(top), prompt=(
                f"โยนลูกบอลขึ้นไป ความสูง h(t) = {rule} เมตร เมื่อ t คือเวลา (วินาที) "
                f"ลูกบอลขึ้นไปได้สูงที่สุดกี่เมตร"),
                distractors=_story.keep(v * t + h0, t, v - 5 + h0, v + h0, answer=top, lo=1)[:3])
        start, per = rng.choice((200, 300, 500)), rng.choice((20, 25, 50))
        target = start + per * rng.randint(4, 12)
        months = (target - start) // per
        return MathDraw("", str(months), prompt=(
            f"เงินออม S(n) = {start} + {per}n บาท เมื่อ n คือจำนวนเดือน "
            f"ต้องออมกี่เดือนจึงจะมีเงิน {target:,} บาท"),
            distractors=_story.keep(target // per, months + 1, (target + start) // per, answer=months, lo=1))
