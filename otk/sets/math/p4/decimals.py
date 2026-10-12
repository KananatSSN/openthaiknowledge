"""ทศนิยม

คณิตศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.4/*

Sets moved here from: math, math_gaps_indicators, math_p4, math_pictures_extra.
"""

from __future__ import annotations

from decimal import Decimal
from random import Random

from otk.core.content import image, text
from otk.core.content import math as content_math
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_gaps_indicators import _cents
from otk.sets._support.math_gaps_indicators import _dec as _dec_math_gaps_indicators
from otk.sets._support.math_p2 import _maths, _texts, evaluate
from otk.sets._support.math_p4 import LEVEL
from otk.sets._support.math_pictures_extra import GRID_ALT, GRIDS

PROVENANCE = Provenance("original")


_DEC_TOPIC = "ทศนิยม"


_DIGIT_WORDS = ("ศูนย์", "หนึ่ง", "สอง", "สาม", "สี่", "ห้า", "หก", "เจ็ด", "แปด", "เก้า")


def dec_words(s: str) -> str:
    """How a decimal is read: 4.35 -> สี่จุดสามห้า (each place read alone)."""
    whole, frac = s.split(".")
    return _story.thai_words(int(whole)) + "จุด" + "".join(_DIGIT_WORDS[int(c)] for c in frac)


def rand_decimal(rng: Random, places: int, lo: int = 0, hi: int = 99) -> Decimal:
    q = Decimal(1).scaleb(-places)
    whole = rng.randint(lo, hi)
    frac = rng.randint(1, 10 ** places - 1)
    if frac % 10 == 0:
        frac += 1
    return Decimal(whole) + frac * q


def _misaligned(a: Decimal, b: Decimal, add: bool) -> Decimal | None:
    """a ± b with the digits lined up on the right instead of on the point."""
    pa, pb = -a.as_tuple().exponent, -b.as_tuple().exponent
    if pa == pb:
        return None
    ia, ib = int(str(a).replace(".", "")), int(str(b).replace(".", ""))
    raw = ia + ib if add else ia - ib
    return Decimal(raw).scaleb(-max(pa, pb)) if raw > 0 else None


def _baht(v: Decimal) -> str:
    return f"{v:.2f}"


def _dec(w: int, h: int) -> str:
    return f"{w}.{h:02d}".rstrip("0").rstrip(".") if h % 10 == 0 else f"{w}.{h:02d}"


@question_type("math.decimal_place_value",
               display_name={"th": "ค่าประจำหลักทศนิยม"}, level={"th": "ป.4"},
               topic="ทศนิยม")
class DecimalPlaceValue(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.randint(1, 9), rng.randint(0, 9), rng.randint(0, 9)
        pos, digit = rng.choice([("ส่วนสิบ", b), ("ส่วนร้อย", c)])
        p = rng.choice(_story.NAMES)
        prompt = rng.choice((
            f"เลขในหลัก{pos}ของ {a}.{b}{c} คือเลขใด?",
            f"{p}วิ่งได้ระยะทาง {a}.{b}{c} กิโลเมตร เลขโดดในหลัก{pos}คือเลขใด",
            f"เชือกเส้นหนึ่งยาว {a}.{b}{c} เมตร เลขโดดในหลัก{pos}คือเลขใด",
            f"แตงโมผลหนึ่งหนัก {a}.{b}{c} กิโลกรัม เลขโดดในหลัก{pos}คือเลขใด",
        ))
        return MathDraw("", str(digit), prompt=prompt,
                        distractors=[str(b), str(c), str(a), "0"])


@question_type("math.decimal_reading_p4",
               display_name={"th": "การอ่านและการเขียนทศนิยม"},
               level=LEVEL, topic=_DEC_TOPIC)
class DecimalReadingP4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        v = rand_decimal(rng, rng.choice((2, 3)), 0, 99)
        s = str(v)
        whole, frac = s.split(".")
        kind = rng.randrange(3)
        if kind == 0:
            # Reading the part after the point as a whole number comes first.
            wrongs = [_story.thai_words(int(whole)) + "จุด" + _story.thai_words(int(frac)),
                      dec_words(f"{whole}.{frac[::-1]}"), dec_words(f"{int(whole) + 1}.{frac}"),
                      dec_words(f"{whole}.{frac[:-1]}")]
            return _texts([text("ทศนิยมนี้อ่านว่าอย่างไร"), content_math(s)], dec_words(s),
                          [w for w in dict.fromkeys(wrongs) if w != dec_words(s)], self.topic)
        if kind == 1:
            wrongs = [f"{whole}.0{frac}", f"{whole}.{frac[::-1]}", f"{int(whole) + 1}.{frac}",
                      f"{whole}{frac[0]}.{frac[1:]}"]
            return _maths([text(f"“{dec_words(s)}” เขียนเป็นทศนิยมได้อย่างไร")], s,
                          [w for w in dict.fromkeys(wrongs) if w != s], self.topic)
        lead = [whole] if whole != "0" else []
        right = " + ".join(lead + [f"0.{'0' * i}{c}" for i, c in enumerate(frac) if c != "0"])
        wrongs = [" + ".join(lead + [f"0.{c}" for c in frac if c != "0"]),
                  " + ".join(lead + [c for c in frac if c != "0"]),
                  " + ".join(lead + [f"0.{'0' * (i + 1)}{c}" for i, c in enumerate(frac)
                                     if c != "0"]),
                  " + ".join([str(int(whole) + 1)] + [f"0.{'0' * i}{c}"
                                                     for i, c in enumerate(frac) if c != "0"])]
        wrongs = [w for w in dict.fromkeys(wrongs)
                  if w != right and Decimal(str(round(evaluate(w), 6))) != v]
        return _maths([text("ทศนิยมนี้เขียนในรูปกระจายได้อย่างไร"), content_math(s)], right,
                      wrongs, self.topic)


@question_type("math.decimal_grid_p4", display_name={"th": "ทศนิยมจากภาพตารางร้อยช่อง"},
               level={"th": "ป.4"}, topic="ทศนิยม")
class DecimalGridP4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        g = rng.choice(GRIDS)
        w, h = g.wholes, g.hundredths
        right = _dec(w, h)
        # Hundredths read as tenths (0.07 as 0.7); the count as a whole number;
        # the unshaded part.
        wrongs = [f"{w}.{h}" if h < 10 else f"{w}.0{h // 10}", str(100 * w + h), _dec(w, 100 - h),
                  _dec(w + 1, h), f"{w + h / 10:g}"]
        return _math_q([text("ตารางแต่ละรูปแทน 1 และแบ่งเป็น 100 ช่องเท่า ๆ กัน "
                             "ส่วนที่แรเงาแทนทศนิยมใด"), image(g.asset_id, alt=GRID_ALT)],
                       right, [x for x in dict.fromkeys(wrongs) if x != right], self.topic)


@question_type("math.decimal_compare_p4",
               display_name={"th": "เปรียบเทียบและเรียงลำดับทศนิยม"},
               level=LEVEL, topic=_DEC_TOPIC)
class DecimalCompareP4(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        # 0.5, 0.45, 0.405, 0.54: more digits is not more.
        w = rng.randint(0, 9)
        a, b = rng.sample(range(1, 10), 2)
        c = rng.choice([x for x in range(1, 10) if x not in (a, b)])
        vals = [f"{w}.{a}", f"{w}.{b}{a}", f"{w}.{b}0{a}", f"{w}.{a}{c}"]
        nums = [Decimal(v) for v in vals]
        most = rng.random() < 0.5
        pick = vals[nums.index((max if most else min)(nums))]
        longest = (max if most else min)(vals, key=len)
        wrongs = [longest] + [v for v in vals if v != longest]
        return _maths([text(f"ทศนิยมใด{'มากที่สุด' if most else 'น้อยที่สุด'}")], pick,
                      [v for v in dict.fromkeys(wrongs) if v != pick], self.topic)


@question_type("math.decimal_addsub_p4",
               display_name={"th": "การบวกและการลบทศนิยม"},
               level=LEVEL, topic=_DEC_TOPIC)
class DecimalAddSubP4(MathType):
    def expr(self, rng: Random):
        a = rand_decimal(rng, rng.choice((1, 2, 3)), 1, 60)
        b = rand_decimal(rng, rng.choice((1, 2, 3)), 0, 40)
        add = rng.random() < 0.5
        if not add and a < b:
            a, b = b, a
        ans = a + b if add else a - b
        slip = _misaligned(a, b, add)
        wrongs = [slip] if slip is not None else []
        step = Decimal(1).scaleb(ans.as_tuple().exponent)
        wrongs += [a - b if add else a + b, ans + step, ans + 1]
        return MathDraw(rf"{a} {'+' if add else '-'} {b}", str(ans), prompt="จงหาผลลัพธ์",
                        distractors=[str(w) for w in dict.fromkeys(wrongs)
                                     if w != ans and w > 0])


@question_type("math.decimal_two_step_word_p4", display_name={"th": "โจทย์ปัญหาการบวกและการลบทศนิยม 2 ขั้นตอน"},
               level={"th": "ป.4"}, topic="ทศนิยม")
class DecimalTwoStepWordP4(WordProblem):
    _ITEMS = ("สมุด", "ปากกา", "ขนมปัง", "นม", "แฟ้ม", "ดินสอสี", "น้ำผลไม้")

    def expr(self, rng: Random):
        name = rng.choice(_story.NAMES)
        kind = rng.randrange(3)
        if kind == 0:
            a, b = _cents(rng, 10, 60), _cents(rng, 10, 60)
            paid = rng.choice((100, 200)) if a + b < 100 else 200
            first, second = rng.sample(self._ITEMS, 2)
            value, places = Decimal(paid) - a - b, 2
            prompt = (f"{name}ซื้อ{first}ราคา {_dec_math_gaps_indicators(a, 2)} บาท และ{second}ราคา {_dec_math_gaps_indicators(b, 2)} บาท "
                      f"จ่ายด้วยธนบัตรใบละ {paid} บาท จะได้เงินทอนกี่บาท")
            # One step only, the total instead of the change, and adding back.
            wrongs = [Decimal(paid) - a, a + b, Decimal(paid) - a + b]
        elif kind == 1:
            places = 3
            have = Decimal(rng.randint(2000, 5000)) / 1000
            more = Decimal(rng.randint(500, 2500)) / 1000
            used = Decimal(rng.randint(1000, 3000)) / 1000
            value = have + more - used
            prompt = (f"แม่มีน้ำตาล {_dec_math_gaps_indicators(have, 3)} กิโลกรัม ซื้อมาเพิ่มอีก {_dec_math_gaps_indicators(more, 3)} กิโลกรัม "
                      f"แล้วใช้ทำขนมไป {_dec_math_gaps_indicators(used, 3)} กิโลกรัม เหลือน้ำตาลกี่กิโลกรัม")
            wrongs = [have + more, have - used, have + more + used]
        else:
            places = 2
            total = Decimal(rng.randint(500, 900)) / 100
            a, b = Decimal(rng.randint(100, 250)) / 100, Decimal(rng.randint(100, 250)) / 100
            value = total - a - b
            prompt = (f"เชือกยาว {_dec_math_gaps_indicators(total, 2)} เมตร ตัดไปผูกของ {_dec_math_gaps_indicators(a, 2)} เมตร "
                      f"และตัดไปอีก {_dec_math_gaps_indicators(b, 2)} เมตร เหลือเชือกยาวกี่เมตร")
            wrongs = [total - a, a + b, total - a + b]
        return MathDraw("", _dec_math_gaps_indicators(value, places), prompt=prompt,
                        distractors=[_dec_math_gaps_indicators(w, places) for w in dict.fromkeys(wrongs) if w != value and w > 0])


@question_type("math.decimal_word_problem_p4",
               display_name={"th": "โจทย์ปัญหาการบวกลบทศนิยม"},
               level=LEVEL, topic=_DEC_TOPIC)
class DecimalWordProblemP4(WordProblem):
    def expr(self, rng: Random):
        p = rng.choice(_story.NAMES)
        kind = rng.randrange(4)
        if kind == 0:
            a = Decimal(rng.randint(10, 99)) + Decimal(rng.choice((25, 50, 75))) / 100
            b = Decimal(rng.randint(5, 60)) + Decimal(rng.choice((25, 50, 75))) / 100
            x, y = rng.sample(("สมุด", "ปากกา", "ขนมปัง", "นม", "ยางลบ", "แฟ้ม"), 2)
            ans = a + b
            return MathDraw("", _baht(ans),
                            prompt=f"{p}ซื้อ{x}ราคา {_baht(a)} บาท และ{y}ราคา {_baht(b)} บาท รวมเป็นเงินกี่บาท",
                            distractors=[_baht(ans + 1), _baht(abs(a - b)), _baht(ans - Decimal("0.5"))])
        if kind == 1:
            note = rng.choice((100, 500))
            a = Decimal(rng.randint(10, note - 10)) + Decimal(rng.choice((25, 50, 75))) / 100
            ans = note - a
            return MathDraw("", _baht(ans),
                            prompt=f"{p}มีเงิน {note} บาท ซื้อของไป {_baht(a)} บาท เหลือเงินกี่บาท",
                            # Taking 1 from the satang but not the baht.
                            distractors=[_baht(ans + 1), _baht(note + a), _baht(ans - 1)])
        if kind == 2:
            a, b = rand_decimal(rng, rng.choice((1, 2)), 0, 5), rand_decimal(rng, rng.choice((1, 2)), 0, 5)
            ans = a + b
            slip = _misaligned(a, b, True)
            return MathDraw("", str(ans),
                            prompt=(f"{p}เดินจากบ้านไปตลาด {a} กิโลเมตร แล้วเดินต่อไปโรงเรียนอีก "
                                    f"{b} กิโลเมตร {p}เดินทั้งหมดกี่กิโลเมตร"),
                            distractors=[str(w) for w in dict.fromkeys(
                                [slip, abs(a - b), ans + 1, ans + Decimal("0.1")])
                                if w is not None and w != ans and w > 0])
        a = rand_decimal(rng, 2, 2, 9)
        b = rand_decimal(rng, rng.choice((1, 2)), 0, 1)
        if b >= a:
            b = a / 2
            b = b.quantize(Decimal("0.01"))
        ans = a - b
        slip = _misaligned(a, b, False)
        return MathDraw("", str(ans),
                        prompt=(f"ถุงข้าวสารหนัก {a} กิโลกรัม ใช้หุงไป {b} กิโลกรัม "
                                f"เหลือข้าวสารกี่กิโลกรัม"),
                        distractors=[str(w) for w in dict.fromkeys(
                            [slip, a + b, ans + Decimal("0.1"), ans + 1])
                            if w is not None and w != ans and w > 0])
