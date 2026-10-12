"""ความยาวและน้ำหนัก

คณิตศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.5/1, ค 2.1 ป.5/2

Sets moved here from: math_gaps_primary.
"""

from __future__ import annotations

from decimal import Decimal
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("original")


def _dec(x: Decimal) -> str:
    return format(x.normalize(), "f")


# (big unit, small unit, how many small make one big)
_LENGTH = (("เมตร", "เซนติเมตร", 100), ("กิโลเมตร", "เมตร", 1000), ("เซนติเมตร", "มิลลิเมตร", 10))


_WEIGHT = (("กิโลกรัม", "กรัม", 1000), ("เมตริกตัน", "กิโลกรัม", 1000))


class _UnitToDecimal(WordProblem):
    table: tuple = ()

    def expr(self, rng: Random):
        big, small, k = rng.choice(self.table)
        whole, part = rng.randint(1, 12), rng.randint(1, k - 1)
        exact = Decimal(whole) + Decimal(part) / Decimal(k)
        # Writing the small amount straight after the point is the classic
        # slip: 2 กิโลกรัม 35 กรัม as 2.35 instead of 2.035.
        wrongs = [Decimal(f"{whole}.{part}"), exact * 10,
                  Decimal(whole) + Decimal(part) / Decimal(k * 10)]
        return MathDraw("", _dec(exact),
                        prompt=f"{whole} {big} {part} {small} เท่ากับกี่{big} (เขียนในรูปทศนิยม)",
                        distractors=[_dec(w) for w in dict.fromkeys(wrongs) if w != exact])


@question_type("math.length_decimal_p5", display_name={"th": "เขียนความยาวในรูปทศนิยม"},
               level={"th": "ป.5"}, topic="ความยาวและน้ำหนัก")
class LengthDecimalP5(_UnitToDecimal):
    table = _LENGTH


@question_type("math.weight_decimal_p5", display_name={"th": "เขียนน้ำหนักในรูปทศนิยม"},
               level={"th": "ป.5"}, topic="ความยาวและน้ำหนัก")
class WeightDecimalP5(_UnitToDecimal):
    table = _WEIGHT


@question_type("math.measure_decimal_word_p5",
               display_name={"th": "โจทย์ปัญหาความยาวและน้ำหนักที่มีการเปลี่ยนหน่วย"},
               level={"th": "ป.5"}, topic="ความยาวและน้ำหนัก")
class MeasureDecimalWordP5(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        kind = rng.randrange(4)
        if kind == 0:
            a, b = rng.randint(120, 480), rng.randint(120, 480)
            total = Decimal(a + b) / 100
            wrongs = [Decimal(a + b) / 10, Decimal(a + b) / 1000, Decimal(a + b)]
            prompt = (f"ผ้าผืนแรกยาว {a} เซนติเมตร ผืนที่สองยาว {b} เซนติเมตร "
                      f"ผ้าสองผืนยาวรวมกันกี่เมตร (เขียนในรูปทศนิยม)")
        elif kind == 1:
            n, g = rng.randint(3, 9), rng.choice((125, 250, 350, 450, 750))
            total = Decimal(n * g) / 1000
            wrongs = [Decimal(n * g) / 100, Decimal(n * g) / 10000, Decimal(n + g) / 1000]
            prompt = f"{p}ซื้อเนยถุงละ {g} กรัม จำนวน {n} ถุง เนยทั้งหมดหนักกี่กิโลกรัม (เขียนในรูปทศนิยม)"
        elif kind == 2:
            km, m = rng.randint(2, 9), rng.choice((250, 400, 600, 750, 850))
            walked = rng.randint(200, 1800)
            total = Decimal(km * 1000 + m - walked) / 1000
            wrongs = [Decimal(km * 1000 + m + walked) / 1000,
                      Decimal(km * 1000 + m - walked) / 100, Decimal(km) - Decimal(walked) / 1000]
            prompt = (f"บ้านของ{p}อยู่ห่างจากโรงเรียน {km} กิโลเมตร {m} เมตร {p}เดินมาแล้ว {walked:,} เมตร "
                      f"ยังต้องเดินอีกกี่กิโลเมตร (เขียนในรูปทศนิยม)")
        else:
            kg, g = rng.randint(1, 4), rng.choice((200, 350, 400, 650, 800))
            n = rng.randint(2, 5)
            total = Decimal(n * (kg * 1000 + g)) / 1000
            # Multiplying the kilograms and forgetting the grams; grams taken as hundredths.
            wrongs = [Decimal(n * kg) + Decimal(g) / 1000, Decimal(n * (kg * 1000 + g)) / 100,
                      Decimal(n) * (Decimal(kg) + Decimal(g) / 100)]
            prompt = (f"กล่องพัสดุหนักกล่องละ {kg} กิโลกรัม {g} กรัม มี {n} กล่อง "
                      f"หนักรวมกันกี่กิโลกรัม (เขียนในรูปทศนิยม)")
        return MathDraw("", _dec(total), prompt=prompt,
                        distractors=[_dec(w) for w in dict.fromkeys(wrongs) if w != total and w > 0])
