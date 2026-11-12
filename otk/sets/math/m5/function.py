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

from fractions import Fraction  # noqa: E402

from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType, WordProblem  # noqa: E402
from otk.kit.math_problems import frac_tex, poly_tex  # noqa: E402
from otk.sets._support.math_m5 import M5 as LEVEL  # noqa: E402


def _nz5(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk5(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk5(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk5(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt5(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk5(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk5(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))


def _g5(n: int) -> str:
    """A whole number in TeX with grouped thousands."""
    return f"{n:,}".replace(",", "{,}")


def _gk5(*values: int, answer: int, lo: int = 1) -> list[str]:
    return _tk5(*(_g5(int(v)) for v in values if v >= lo), answer=_g5(answer))


def _deg5(*angles: int) -> str:
    return "x = " + ", ".join(f"{a}^{{\\circ}}" for a in angles)

# ── More functions in real life (2026-11): a taxi fare, a fixed cost from two prices, tripling growth, the
# break-even point, the best output for profit, a water bill in two tiers, and Celsius from Fahrenheit ──


@question_type("math.taxi_fare_m5", display_name={"th": "ค่าโดยสารที่เป็นฟังก์ชันเชิงเส้น"}, level=LEVEL,
               topic="ฟังก์ชันในชีวิตจริง")
class TaxiFareM5(WordProblem):
    def expr(self, rng: Random):
        start, per, km = rng.choice((35, 40, 50)), rng.randint(5, 12), rng.randint(3, 30)
        right = start + per * km
        prompt = f"ค่าแท็กซี่เริ่มต้น {start} บาท และคิดเพิ่มกิโลเมตรละ {per} บาท ถ้าเดินทาง {km} กิโลเมตร ต้องจ่ายกี่บาท"
        # The start fee left out; the start fee counted per kilometre; one kilometre short.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk5(per * km, (start + per) * km, start + per * (km - 1), right + per, answer=right, lo=1))


@question_type("math.fixed_cost_from_two_m5", display_name={"th": "หาค่าคงที่ของฟังก์ชันเชิงเส้นจากสองข้อมูล"},
               level=LEVEL, topic="ฟังก์ชันในชีวิตจริง")
class FixedCostFromTwoM5(WordProblem):
    def expr(self, rng: Random):
        fixed, per = rng.randint(2, 30) * 10, rng.randint(5, 40)
        n1, n2 = sorted(rng.sample(range(2, 20), 2))
        c1, c2 = fixed + per * n1, fixed + per * n2
        prompt = (f"ร้านพิมพ์เสื้อคิดค่าบล็อกครั้งเดียว และคิดค่าพิมพ์ตัวละเท่ากัน พิมพ์ {n1} ตัว จ่าย {c1} บาท "
                  f"พิมพ์ {n2} ตัว จ่าย {c2} บาท ค่าบล็อกกี่บาท")
        # The price per shirt; the gap in cost; the first bill.
        return MathDraw("", str(fixed), prompt=prompt,
                        distractors=_nk5(per, c2 - c1, c1 - per, fixed + per, answer=fixed, lo=1))


@question_type("math.tripling_growth_m5", display_name={"th": "ฟังก์ชันที่เพิ่มขึ้นเป็นสามเท่าทุกปี"}, level=LEVEL,
               topic="ฟังก์ชันในชีวิตจริง")
class TriplingGrowthM5(WordProblem):
    def expr(self, rng: Random):
        start, t = rng.choice((10, 20, 50, 100)), rng.randint(2, 5)
        right = start * 3 ** t
        prompt = f"จำนวนผู้ติดตามช่องหนึ่งเริ่มต้น {start} คน และเพิ่มเป็นสามเท่าทุกปี เมื่อผ่านไป {t} ปีจะมีผู้ติดตามกี่คน"
        # Tripled once per year added; one year short; doubled instead.
        return MathDraw("", _g5(right), prompt=prompt,
                        distractors=_gk5(start * 3 * t, start * 3 ** (t - 1), start * 2 ** t, start * 3 ** (t + 1), answer=right))


@question_type("math.break_even_m5", display_name={"th": "จุดคุ้มทุน"}, level=LEVEL, topic="ฟังก์ชันในชีวิตจริง")
class BreakEvenM5(WordProblem):
    def expr(self, rng: Random):
        cost = rng.randint(10, 60)
        price = cost + rng.randint(5, 30)
        right = rng.randint(10, 200)
        fixed = (price - cost) * right
        prompt = (f"ร้านค้ามีต้นทุนคงที่ {fixed:,} บาท และต้นทุนชิ้นละ {cost} บาท ขายชิ้นละ {price} บาท "
                  "ต้องขายกี่ชิ้นจึงจะคุ้มทุนพอดี")
        # The fixed cost over the price; over the cost; one more.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk5(fixed // price, fixed // cost, right + 1, right * 2, answer=right, lo=1))


@question_type("math.best_output_m5", display_name={"th": "จำนวนที่ผลิตแล้วได้กำไรมากที่สุด"}, level=LEVEL,
               topic="ฟังก์ชันในชีวิตจริง")
class BestOutputM5(MathType):
    def expr(self, rng: Random):
        h, c = rng.randint(5, 60), rng.randint(-200, 100)
        # P(x) = -x² + 2hx + c peaks at x = h.
        return MathDraw(f"P(x) = {poly_tex((-1, 'x^{2}'), (2 * h, 'x'), (c, ''))}", str(h),
                        prompt="กำไร P(x) บาท เมื่อผลิตสินค้า x ชิ้น ต้องผลิตกี่ชิ้นจึงได้กำไรมากที่สุด",
                        distractors=_nk5(2 * h, h * h + c, h + 1, h // 2 if h > 9 else h + 5, answer=h, lo=1))


@question_type("math.water_bill_tiers_m5", display_name={"th": "ค่าน้ำแบบขั้นบันได"}, level=LEVEL, topic="ฟังก์ชันในชีวิตจริง")
class WaterBillTiersM5(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.randint(5, 10), rng.randint(11, 20)
        units = rng.randint(11, 40)
        right = 10 * a + (units - 10) * b
        prompt = (f"ค่าน้ำประปา 10 หน่วยแรกคิดหน่วยละ {a} บาท หน่วยที่เกินจาก 10 หน่วยคิดหน่วยละ {b} บาท "
                  f"ถ้าใช้น้ำ {units} หน่วย ต้องจ่ายกี่บาท")
        # Every unit at the first price; every unit at the second; the first ten left out.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk5(units * a, units * b, (units - 10) * b, right + b, answer=right, lo=1))


@question_type("math.celsius_from_fahrenheit_m5", display_name={"th": "แปลงองศาฟาเรนไฮต์เป็นองศาเซลเซียส"}, level=LEVEL,
               topic="ฟังก์ชันในชีวิตจริง")
class CelsiusFromFahrenheitM5(WordProblem):
    def expr(self, rng: Random):
        c = 5 * rng.randint(-8, 20)
        f = 9 * c // 5 + 32
        prompt = f"ความสัมพันธ์ระหว่างอุณหภูมิคือ F = (9/5)C + 32 ถ้าอุณหภูมิเท่ากับ {f} องศาฟาเรนไฮต์ จะเป็นกี่องศาเซลเซียส"
        # 32 not taken away first; multiplied by 9/5 the wrong way; 32 added.
        return MathDraw("", str(c), prompt=prompt,
                        distractors=_nk5(5 * f // 9, 9 * (f - 32) // 5, (f + 32) * 5 // 9, c + 5, answer=c))
