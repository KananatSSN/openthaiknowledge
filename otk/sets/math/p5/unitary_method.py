"""บัญญัติไตรยางศ์

คณิตศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.5/*

Sets moved here from: math_p5.
"""

from __future__ import annotations

from random import Random

from otk.core.mistakes import named
from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_p5 import LEVEL

PROVENANCE = Provenance("original")


_RULE3_TOPIC = "บัญญัติไตรยางศ์"


@question_type("math.unit_price_p5",
               display_name={"th": "บัญญัติไตรยางศ์: ราคาต่อหน่วย"},
               level=LEVEL, topic=_RULE3_TOPIC)
class UnitPriceP5(WordProblem):
    _GOODS = (("สมุด", "เล่ม"), ("ดินสอ", "แท่ง"), ("ไข่ไก่", "ฟอง"), ("ขนมปัง", "ก้อน"),
              ("น้ำดื่ม", "ขวด"), ("ปากกา", "ด้าม"))

    def expr(self, rng: Random):
        noun, cl = rng.choice(self._GOODS)
        unit = rng.randint(3, 45)
        a, b = rng.sample(range(2, 13), 2)
        ans = unit * b
        return MathDraw("", str(ans),
                        prompt=f"{noun} {a} {cl} ราคา {unit * a} บาท ถ้าซื้อ{noun} {b} {cl} ต้องจ่ายกี่บาท",
                        # Scaling by the difference, and forgetting to divide.
                        distractors=_story.keep(
                            named("proportion.additive",
                                  unit * a + (b - a) if b > a else unit * a - (a - b)),
                            named("proportion.no_divide", unit * a * b),
                            named("proportion.unit_rate_only", unit),
                            ans + unit, answer=ans, lo=1))


@question_type("math.rate_word_problem_p5",
               display_name={"th": "บัญญัติไตรยางศ์: อัตราคงที่"},
               level=LEVEL, topic=_RULE3_TOPIC)
class RateWordProblemP5(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        a, b = rng.sample(range(2, 10), 2)
        if kind == 0:
            per = rng.choice(range(40, 95, 5))
            return MathDraw("", str(per * b),
                            prompt=(f"รถยนต์แล่นด้วยอัตราเร็วคงที่ {a} ชั่วโมง ได้ระยะทาง {per * a} กิโลเมตร "
                                    f"ถ้าแล่นด้วยอัตราเร็วเท่าเดิม {b} ชั่วโมง จะได้ระยะทางกี่กิโลเมตร"),
                            distractors=_story.keep(named("proportion.no_divide", per * a * b),
                                                    named("proportion.unit_rate_only", per),
                                                    per * a + b, per * (b + 1), answer=per * b))
        if kind == 1:
            per = rng.randint(12, 80)
            return MathDraw("", str(per * b),
                            prompt=(f"เครื่องจักรผลิตขวดได้ {per * a} ใบ ใน {a} นาที ถ้าผลิตด้วยอัตราเดิม "
                                    f"{b} นาทีจะผลิตได้กี่ใบ"),
                            distractors=_story.keep(named("proportion.no_divide", per * a * b),
                                                    named("proportion.unit_rate_only", per),
                                                    per * a + b, per * (b - 1), answer=per * b, lo=1))
        per = rng.randint(2, 12)
        return MathDraw("", str(per * b),
                        prompt=(f"น้ำหยดจากก๊อกได้ {per * a} มิลลิลิตร ใน {a} นาที ถ้าหยดด้วยอัตราเดิม "
                                f"{b} นาทีจะได้น้ำกี่มิลลิลิตร"),
                        distractors=_story.keep(named("proportion.no_divide", per * a * b),
                                                named("proportion.unit_rate_only", per),
                                                per * a + b, per * b + per, answer=per * b, lo=1))


@question_type("math.recipe_scaling_p5",
               display_name={"th": "บัญญัติไตรยางศ์: ปรับสูตรอาหาร"},
               level=LEVEL, topic=_RULE3_TOPIC)
class RecipeScalingP5(WordProblem):
    _INGREDIENTS = (("แป้ง", "กรัม", (50, 400)), ("น้ำตาล", "กรัม", (20, 200)),
                    ("นม", "มิลลิลิตร", (50, 500)), ("ไข่ไก่", "ฟอง", (1, 4)))

    def expr(self, rng: Random):
        dish = rng.choice(("ขนมเค้ก", "คุกกี้", "ขนมปัง", "พุดดิ้ง"))
        name, unit, (lo, hi) = rng.choice(self._INGREDIENTS)
        people = rng.choice((2, 4, 5))
        want = people * rng.randint(2, 4)
        per = rng.randint(lo, hi) // people or 1
        amount = per * people
        ans = per * want
        return MathDraw("", str(ans),
                        prompt=(f"สูตร{dish}สำหรับ {people} คน ใช้{name} {amount} {unit} "
                                f"ถ้าทำให้ {want} คน ต้องใช้{name}กี่{unit}"),
                        distractors=_story.keep(named("proportion.additive", amount + (want - people)),
                                                named("proportion.no_divide", amount * want),
                                                named("proportion.unit_rate_only", per),
                                                ans + amount, answer=ans, lo=1))


from otk.core.registry import question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p5 import LEVEL  # noqa: E402


def _g(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _dec(value: int, places: int) -> str:
    """An integer count of 10**-places as a decimal, trailing zeros dropped: (2350, 3) -> 2.35."""
    sign = "-" if value < 0 else ""
    whole, frac = divmod(abs(value), 10 ** places)
    digits = str(frac).rjust(places, "0").rstrip("0") if places else ""
    return f"{sign}{whole}.{digits}" if digits else f"{sign}{whole}"


def _dk(*values: int, answer: int, places: int, lo: int = 0) -> list[str]:
    """``story.keep`` for decimals held as integer counts of 10**-places."""
    return [_dec(int(v), places) for v in _story.keep(*values, answer=answer, lo=lo)]


# ── More unitary method (2026-11): the better buy, more workers fewer days, fuel for a trip, days to earn an
# amount, how many for the money, changing money, and printing time ──


@question_type("math.better_buy_p5", display_name={"th": "ซื้อแบบใดคุ้มกว่า"},
               level=LEVEL, topic="บัญญัติไตรยางศ์")
class BetterBuyP5(ChoiceType):
    def compose(self, rng: Random):
        while True:
            n1, n2 = rng.sample((2, 3, 4, 5, 6, 8, 10, 12), 2)
            u1, u2 = rng.randint(8, 40), rng.randint(8, 40)
            if u1 != u2:
                break
        thing = rng.choice(("สบู่", "ขวดน้ำ", "ปากกา", "ขนมปัง"))
        a = f"แพ็ก {n1} ชิ้น ราคา {n1 * u1} บาท"
        b = f"แพ็ก {n2} ชิ้น ราคา {n2 * u2} บาท"
        right, wrong = (a, b) if u1 < u2 else (b, a)
        return (f"{thing}มีสองแบบ แบบใดราคาต่อชิ้นถูกกว่า", right,
                [wrong, "ราคาต่อชิ้นเท่ากัน", "บอกไม่ได้"])


@question_type("math.workers_days_p5", display_name={"th": "คนมากขึ้นทำงานเสร็จเร็วขึ้น"},
               level=LEVEL, topic="บัญญัติไตรยางศ์")
class WorkersDaysP5(WordProblem):
    def expr(self, rng: Random):
        while True:
            w1, w2 = rng.sample((2, 3, 4, 5, 6, 8, 10, 12), 2)
            work = w1 * rng.randint(2, 12)
            if work % w2 == 0:
                break
        d1 = work // w1
        right = work // w2
        prompt = f"คนงาน {w1} คนทาสีรั้วเสร็จใน {d1} วัน ถ้าใช้คนงาน {w2} คน ทำงานเท่ากัน จะเสร็จในกี่วัน"
        # Scaled as if more workers took longer; the total work in worker-days; one day off.
        direct = d1 * w2 // w1 if d1 * w2 % w1 == 0 else d1 + w2
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(direct, work, right + 1, right - 1, answer=right, lo=1))


@question_type("math.fuel_for_trip_p5", display_name={"th": "ใช้น้ำมันกี่ลิตรสำหรับระยะทาง"},
               level=LEVEL, topic="บัญญัติไตรยางศ์")
class FuelForTripP5(WordProblem):
    def expr(self, rng: Random):
        per = rng.randint(8, 18)
        l1 = rng.randint(2, 9)
        l2 = rng.randint(3, 40)
        while l2 == l1:
            l2 += 1
        prompt = (f"รถยนต์คันหนึ่งใช้น้ำมัน {l1} ลิตร วิ่งได้ {per * l1} กิโลเมตร "
                  f"ถ้าจะวิ่งระยะทาง {per * l2} กิโลเมตร ต้องใช้น้ำมันกี่ลิตร")
        # Kilometres per litre; the distance; one litre off.
        return MathDraw("", str(l2), prompt=prompt,
                        distractors=_story.keep(per, l2 * l1, per * l2 // l1 if per * l2 % l1 == 0 else l2 + l1,
                                                l2 + 1, answer=l2, lo=1))


@question_type("math.days_to_earn_p5", display_name={"th": "ทำงานกี่วันจึงได้เงินตามต้องการ"},
               level=LEVEL, topic="บัญญัติไตรยางศ์")
class DaysToEarnP5(WordProblem):
    def expr(self, rng: Random):
        wage = rng.randint(30, 80) * 10
        d1 = rng.randint(2, 7)
        d2 = rng.randint(8, 30)
        p = rng.choice(_story.NAMES)
        prompt = (f"{p}ทำงาน {d1} วัน ได้ค่าจ้าง {wage * d1:,} บาท "
                  f"ถ้าต้องการค่าจ้าง {wage * d2:,} บาท ต้องทำงานกี่วัน")
        # The daily wage; the days added; one day off.
        return MathDraw("", str(d2), prompt=prompt,
                        distractors=_story.keep(wage // 10, d1 + d2, d2 * d1, d2 + 1, d2 - 1, answer=d2, lo=1))


@question_type("math.how_many_for_money_p5", display_name={"th": "มีเงินเท่านี้ซื้อได้กี่ชิ้น"},
               level=LEVEL, topic="บัญญัติไตรยางศ์")
class HowManyForMoneyP5(WordProblem):
    def expr(self, rng: Random):
        price = rng.randint(4, 35)
        n1 = rng.randint(2, 6)
        right = rng.randint(7, 30)
        thing = rng.choice(("ปากกา", "สมุด", "ไข่เค็ม", "ยางลบ"))
        prompt = f"{thing} {n1} ชิ้น ราคา {price * n1} บาท มีเงิน {price * right} บาท ซื้อ{thing}ได้กี่ชิ้น"
        # The price of one; the money divided by the bundle price; one more.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(price, right // n1 if right // n1 else right + 2, right * n1,
                                                right + 1, answer=right, lo=1))


@question_type("math.exchange_money_p5", display_name={"th": "แลกเงินตราต่างประเทศ"},
               level=LEVEL, topic="บัญญัติไตรยางศ์")
class ExchangeMoneyP5(WordProblem):
    def expr(self, rng: Random):
        rate = rng.randint(30, 38)
        n1 = rng.choice((5, 10, 20))
        n2 = rng.randint(3, 60)
        while n2 == n1:
            n2 += 1
        right = rate * n2
        prompt = f"แลกเงิน {n1} ดอลลาร์สหรัฐได้ {rate * n1} บาท ถ้าแลก {n2} ดอลลาร์สหรัฐ จะได้กี่บาท"
        # The rate for one dollar; the two amounts' baht added; one dollar off.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(rate, rate * n1 + n2, rate * (n2 + 1), rate * (n2 - 1),
                                        answer=right, lo=1))


@question_type("math.printing_time_p5", display_name={"th": "เครื่องพิมพ์ใช้เวลากี่นาที"},
               level=LEVEL, topic="บัญญัติไตรยางศ์")
class PrintingTimeP5(WordProblem):
    def expr(self, rng: Random):
        per = rng.randint(6, 30)
        m1 = rng.randint(2, 5)
        m2 = rng.randint(6, 25)
        prompt = f"เครื่องพิมพ์พิมพ์ได้ {per * m1} แผ่นใน {m1} นาที ถ้าพิมพ์ {per * m2} แผ่น จะใช้เวลากี่นาที"
        # The pages a minute; the pages divided by the first minutes; one minute off.
        return MathDraw("", str(m2), prompt=prompt,
                        distractors=_story.keep(per, per * m2 // m1 if per * m2 % m1 == 0 else m2 + m1,
                                                m2 + 1, m2 - 1, answer=m2, lo=1))
