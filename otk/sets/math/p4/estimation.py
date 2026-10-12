"""การประมาณค่า

คณิตศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.4/7

Sets moved here from: math, math_number, math_p4.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_p4 import LEVEL, grouped

PROVENANCE = Provenance("original")


_PLACE_WORD = {10: "สิบ", 100: "ร้อย", 1000: "พัน"}


def _n(v: int) -> str:
    return f"{v:,}".replace(",", "{,}")


def _round_to(n: int, place: int) -> int:
    """Round to the nearest place, halves upward, as ป.4 is taught."""
    return (n + place // 2) // place * place


@question_type("math.rounding",
               display_name={"th": "การปัดเศษ"}, level={"th": "ป.4"},
               topic="การประมาณค่า")
class Rounding(WordProblem):
    _PLACES = {"สิบ": 10, "ร้อย": 100, "พัน": 1000}

    def expr(self, rng: Random):
        n = rng.randint(1000, 99999)
        place = rng.choice(list(self._PLACES))
        unit = self._PLACES[place]
        low = (n // unit) * unit
        high = low + unit
        nearest = high if (n - low) * 2 >= unit else low
        return MathDraw("", str(nearest),
                        prompt=f"ปัด {n} ให้เป็นจำนวนเต็มหลัก{place}ที่ใกล้ที่สุด "
                               f"ได้เท่าใด?",
                        distractors=[str(high), str(low),
                                     str(round(n / (unit * 10)) * unit * 10)])


@question_type("math.estimate_sum", display_name={"th": "ประมาณผลบวก"},
               level={"th": "ป.4"}, topic="การประมาณค่า")
class EstimateSum(WordProblem):
    """Round each addend to the place asked, then add: tens with two-digit
    numbers, hundreds with three, thousands with four (ค 1.1 ป.4/7)."""

    def expr(self, rng: Random, lo: int = 12, hi: int = 89):
        place = rng.choice((10, 100, 1000))
        scale = place // 10
        while True:
            a, b = rng.randint(lo * scale, hi * scale), rng.randint(lo * scale, hi * scale)
            ra, rb = _round_to(a, place), _round_to(b, place)
            if ra + rb != a + b:          # an exact sum would make estimating pointless
                break
        word = _PLACE_WORD[place]
        who = rng.choice(_story.NAMES)
        shown, prompt = rng.choice((
            (f"{a} + {b}", f"ปัดเศษแต่ละจำนวนเป็นหลัก{word}ก่อน แล้วหาผลบวกโดยประมาณ"),
            ("", f"{who}ซื้อของราคา {a:,} บาท และ {b:,} บาท ถ้าปัดราคาเป็นหลัก{word} "
                 f"ต้องเตรียมเงินประมาณกี่บาท"),
            ("", f"วันเสาร์มีคนเข้าชมงาน {a:,} คน วันอาทิตย์ {b:,} คน ถ้าปัดเป็นหลัก{word} "
                 f"สองวันมีคนเข้าชมประมาณกี่คน"),
            ("", f"โรงเรียนสองแห่งเก็บขวดพลาสติกได้ {a:,} ใบ และ {b:,} ใบ ถ้าปัดเป็นหลัก{word} "
                 f"รวมกันเก็บได้ประมาณกี่ใบ"),
        ))
        # The exact sum, one place too many or too few.
        return MathDraw(shown, _n(ra + rb), prompt=prompt,
                        hint=rf"{a} \approx {ra}, \; {b} \approx {rb}",
                        distractors=[_n(a + b), _n(ra + rb + place), _n(ra + rb - place)])


@question_type("math.estimate_product", display_name={"th": "ประมาณผลคูณ"},
               level={"th": "ป.4"}, topic="การประมาณค่า")
class EstimateProduct(WordProblem):
    def expr(self, rng: Random, lo: int = 12, hi: int = 79):
        place = rng.choice((10, 100))
        scale = place // 10
        b = rng.randint(3, 9)
        while True:
            a = rng.randint(lo * scale, hi * scale)
            ra = _round_to(a, place)
            if ra != a:
                break
        word = _PLACE_WORD[place]
        frames = [
            (rf"{a} \times {b}", f"ปัดเศษตัวตั้งเป็นหลัก{word}ก่อน แล้วหาผลคูณโดยประมาณ"),
            ("", f"ซื้อของ {b} ชิ้น ราคาชิ้นละ {a:,} บาท ถ้าปัดราคาเป็นหลัก{word} ต้องจ่ายประมาณกี่บาท"),
            ("", f"ลังหนึ่งบรรจุไข่ {a:,} ฟอง มี {b} ลัง ถ้าปัดจำนวนในหนึ่งลังเป็นหลัก{word} มีไข่ประมาณกี่ฟอง"),
        ]
        if place == 10:
            frames.append(("", f"นักเรียนนั่งรถบัสคันละ {a} คน จำนวน {b} คัน ถ้าปัดเป็นหลักสิบ "
                               f"มีนักเรียนประมาณกี่คน"))
        shown, prompt = rng.choice(frames)
        return MathDraw(shown, _n(ra * b), prompt=prompt,
                        hint=rf"{a} \approx {ra}",
                        distractors=[_n(a * b), _n((ra + place) * b), _n(max(ra - place, place) * b)])


@question_type("math.estimate_word_problem_p4",
               display_name={"th": "โจทย์ปัญหาการประมาณค่า"},
               level=LEVEL, topic="การประมาณค่า")
class EstimateWordProblemP4(WordProblem):
    _ITEMS = (("โทรทัศน์", "ตู้เย็น"), ("จักรยาน", "หมวกกันน็อก"), ("โต๊ะ", "เก้าอี้"),
              ("พัดลม", "หม้อหุงข้าว"), ("โทรศัพท์", "หูฟัง"))

    def expr(self, rng: Random):
        x, y = rng.choice(self._ITEMS)
        a, b = rng.randint(5200, 29800), rng.randint(1200, 9800)
        r = lambda n: (n + 500) // 1000 * 1000
        ans = r(a) + r(b)
        return MathDraw("", str(ans),
                        prompt=(f"{x}ราคา {grouped(a)} บาท {y}ราคา {grouped(b)} บาท "
                                f"ประมาณค่าราคาแต่ละอย่างเป็นจำนวนเต็มพันก่อน "
                                f"แล้วหาว่าซื้อทั้งสองอย่างต้องจ่ายประมาณกี่บาท"),
                        # The exact total, and each rounded down instead.
                        distractors=_story.keep(a + b, a // 1000 * 1000 + b // 1000 * 1000,
                                                ans + 1000, answer=ans))
