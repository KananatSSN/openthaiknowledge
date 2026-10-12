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
