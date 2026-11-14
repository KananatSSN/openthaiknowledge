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


from otk.core.registry import question_type  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p5 import LEVEL  # noqa: E402


def _g(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _dz(value: int, places: int) -> str:
    """An integer count of 10**-places as a decimal, trailing zeros dropped: (2350, 3) -> 2.35."""
    sign = "-" if value < 0 else ""
    whole, frac = divmod(abs(value), 10 ** places)
    digits = str(frac).rjust(places, "0").rstrip("0") if places else ""
    return f"{sign}{whole}.{digits}" if digits else f"{sign}{whole}"


def _dzk(*values: int, answer: int, places: int, lo: int = 0) -> list[str]:
    """``story.keep`` for decimals held as integer counts of 10**-places."""
    return [_dz(int(v), places) for v in _story.keep(*values, answer=answer, lo=lo)]


# ── More length and weight (2026-11): a decimal to the smaller unit, adding across units, the heaviest of
# four, a difference in grams, ribbon left, adding mixed units, and the right unit ──

_UNIT_PAIRS = (("กิโลเมตร", "เมตร", 1000), ("กิโลกรัม", "กรัม", 1000), ("เมตริกตัน", "กิโลกรัม", 1000),
               ("เมตร", "เซนติเมตร", 100))


@question_type("math.decimal_to_smaller_unit_p5", display_name={"th": "เปลี่ยนทศนิยมเป็นหน่วยที่เล็กกว่า"},
               level=LEVEL, topic="ความยาวและน้ำหนัก")
class DecimalToSmallerUnitP5(WordProblem):
    def expr(self, rng: Random):
        big, small, k = rng.choice(_UNIT_PAIRS)
        places = 3 if k == 1000 else 2
        v = rng.randint(10 ** places + 1, 9 * 10 ** places)
        while v % 10 == 0:
            v += 1
        right = v * k // 10 ** places
        prompt = f"{_dz(v, places)} {big} เท่ากับกี่{small}"
        # Ten or a hundred times off; one big unit too many.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(right // 10, right * 10, right // 100, right + k,
                                        answer=right, lo=1))


@question_type("math.add_across_units_p5", display_name={"th": "บวกระยะทางที่ต่างหน่วยกัน"},
               level=LEVEL, topic="ความยาวและน้ำหนัก")
class AddAcrossUnitsP5(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(1, 9) * 1000 + rng.randint(1, 19) * 50
        b = rng.randint(1, 19) * 50
        right = a + b
        p = rng.choice(_story.NAMES)
        prompt = (f"{p}เดินทาง {_dz(a, 3)} กิโลเมตร แล้วเดินต่ออีก {b} เมตร "
                  f"รวมเป็นระยะทางกี่กิโลเมตร (เขียนในรูปทศนิยม)")
        # The metres added as whole kilometres' digits; the metres as tenths; one hundred metres off.
        return MathDraw("", _dz(right, 3), prompt=prompt,
                        distractors=_dzk(a + b * 1000, a + b * 10, right + 100, right - 100,
                                        answer=right, places=3, lo=1))


@question_type("math.heaviest_of_four_p5", display_name={"th": "เปรียบเทียบน้ำหนักที่เขียนต่างหน่วย"},
               level=LEVEL, topic="ความยาวและน้ำหนัก")
class HeaviestOfFourP5(ChoiceType):
    def compose(self, rng: Random):
        while True:
            grams = rng.sample(range(1050, 4000, 50), 4)
            if len({g // 1000 for g in grams}) <= 2:
                break
        forms = []
        for i, g in enumerate(grams):
            kind = i % 3
            if kind == 0:
                forms.append(f"{_dz(g, 3)} กิโลกรัม")
            elif kind == 1:
                forms.append(f"{g:,} กรัม")
            else:
                forms.append(f"{g // 1000} กิโลกรัม {g % 1000} กรัม")
        most = rng.random() < 0.5
        pick = grams.index(max(grams) if most else min(grams))
        return (f"ข้อใด{'หนักที่สุด' if most else 'เบาที่สุด'}", forms[pick],
                [f for i, f in enumerate(forms) if i != pick])


@question_type("math.weight_difference_grams_p5", display_name={"th": "ผลต่างของน้ำหนักเป็นกรัม"},
               level=LEVEL, topic="ความยาวและน้ำหนัก")
class WeightDifferenceGramsP5(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(12, 60) * 100
        b = rng.randint(2, a // 100 - 3) * 50
        right = a - b
        x, y = rng.sample(("ถุงข้าว", "ถุงน้ำตาล", "กล่องหนังสือ", "ตะกร้าผลไม้"), 2)
        prompt = f"{x}หนัก {_dz(a, 3)} กิโลกรัม {y}หนัก {b} กรัม {x}หนักกว่า{y}กี่กรัม"
        # The kilograms read as grams; the two added; the difference ten times off.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(abs(a // 100 - b) if a // 100 != b else b + 1, a + b, right // 10,
                                        right + 100, answer=right, lo=1))


@question_type("math.ribbon_left_p5", display_name={"th": "ตัดแล้วเหลือความยาวเท่าใด (ทศนิยม)"},
               level=LEVEL, topic="ความยาวและน้ำหนัก")
class RibbonLeftP5(WordProblem):
    def expr(self, rng: Random):
        piece = rng.randint(11, 95) * 5
        count = rng.randint(2, 6)
        total = (count * piece // 100 + rng.randint(1, 4)) * 100
        right = total - count * piece
        thing = rng.choice(("ริบบิ้น", "เชือก", "ผ้า"))
        prompt = (f"{thing}ยาว {total // 100} เมตร ตัดออกเป็น {count} ท่อน ท่อนละ {_dz(piece, 2)} เมตร "
                  f"เหลือ{thing}ยาวกี่เมตร")
        # One piece cut only; everything cut; one piece more.
        return MathDraw("", _dz(right, 2), prompt=prompt,
                        distractors=_dzk(total - piece, count * piece, right - piece, right + piece,
                                        answer=right, places=2, lo=1))


@question_type("math.add_mixed_units_p5", display_name={"th": "บวกน้ำหนักที่มีสองหน่วย"},
               level=LEVEL, topic="ความยาวและน้ำหนัก")
class AddMixedUnitsP5(ChoiceType):
    def compose(self, rng: Random):
        a = rng.randint(1, 9) * 1000 + rng.randint(1, 19) * 50
        b = rng.randint(1, 9) * 1000 + rng.randint(1, 19) * 50
        total = a + b

        def form(g: int) -> str:
            return f"{g // 1000} กิโลกรัม {g % 1000} กรัม" if g % 1000 else f"{g // 1000} กิโลกรัม"

        right = form(total)
        no_carry = f"{a // 1000 + b // 1000} กิโลกรัม {a % 1000 + b % 1000} กรัม"
        wrongs = [no_carry, form(total + 1000), form(total - 100)]
        wrongs = [w for w in dict.fromkeys(wrongs) if w != right]
        if len(wrongs) < 3:
            wrongs.append(form(total + 100))
        return f"{form(a)} + {form(b)} เท่ากับเท่าใด", right, wrongs[:3]


@question_type("math.suitable_unit_p5", display_name={"th": "หน่วยที่เหมาะสมสำหรับวัดสิ่งต่าง ๆ"},
               level=LEVEL, topic="ความยาวและน้ำหนัก")
class SuitableUnitP5(ConceptBankType):
    ITEMS = [
        Concept("ควรใช้หน่วยใดบอกน้ำหนักของรถบรรทุก", "เมตริกตัน", ("กรัม", "กิโลเมตร", "มิลลิเมตร")),
        Concept("ควรใช้หน่วยใดบอกน้ำหนักของยางลบหนึ่งก้อน", "กรัม", ("เมตริกตัน", "กิโลกรัม", "เมตร")),
        Concept("ควรใช้หน่วยใดบอกระยะทางจากกรุงเทพฯ ถึงเชียงใหม่", "กิโลเมตร",
                ("เซนติเมตร", "มิลลิเมตร", "กิโลกรัม")),
        Concept("ควรใช้หน่วยใดบอกความหนาของเหรียญ", "มิลลิเมตร", ("กิโลเมตร", "เมตร", "กรัม")),
        Concept("ควรใช้หน่วยใดบอกน้ำหนักของตัวเรา", "กิโลกรัม", ("เมตริกตัน", "กรัม", "เมตร")),
        Concept("ควรใช้หน่วยใดบอกความสูงของเสาธง", "เมตร", ("กิโลเมตร", "มิลลิเมตร", "กิโลกรัม")),
    ]
