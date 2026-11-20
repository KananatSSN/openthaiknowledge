"""ค่ามาตรฐาน

คณิตศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ค 3.1 ม.6/1

Sets moved here from: math, math_data, math_m6.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import ChoiceType, MathDraw, MathType, WordProblem
from otk.sets._support.math_m6 import M6

PROVENANCE = Provenance("original")


@question_type("math.z_score",
               display_name={"th": "คะแนนมาตรฐาน (Z-score)"}, level={"th": "ม.6"},
               topic="ค่ามาตรฐาน")
class ZScore(WordProblem):
    def expr(self, rng: Random):
        mu = rng.randint(40, 70)
        sigma = rng.choice([2, 4, 5, 10])
        z = rng.choice([n for n in range(-3, 4) if n])
        x = mu + z * sigma
        p = rng.choice(_story.NAMES)
        prompt = rng.choice((
            f"ถ้า x = {x}, μ = {mu}, σ = {sigma} แล้ว Z-score เท่ากับเท่าใด?",
            f"คะแนนสอบวิชาหนึ่งมีค่าเฉลี่ย {mu} คะแนน ส่วนเบี่ยงเบนมาตรฐาน {sigma} คะแนน "
            f"{p}สอบได้ {x} คะแนน ค่ามาตรฐานของคะแนน{p}เท่ากับเท่าใด",
            f"น้ำหนักของนักเรียนชั้นหนึ่งมีค่าเฉลี่ย {mu} กิโลกรัม ส่วนเบี่ยงเบนมาตรฐาน {sigma} กิโลกรัม "
            f"{p}หนัก {x} กิโลกรัม ค่ามาตรฐานของน้ำหนัก{p}เท่ากับเท่าใด",
        ))
        return MathDraw("", str(z), prompt=prompt,
                        distractors=[str(-z), str(z * sigma * sigma),
                                     str((x - mu) * sigma)])


@question_type("math.z_score_from_value", display_name={"th": "หาค่าข้อมูลจากคะแนนมาตรฐาน"},
               level={"th": "ม.6"}, topic="ค่ามาตรฐาน")
class ZScoreFromValue(MathType):
    """Run the standardization backwards: x = μ + zσ."""

    def expr(self, rng: Random, mean_hi: int = 80, sd_hi: int = 12):
        mean = rng.randrange(20, mean_hi, 5)
        sd = rng.randint(2, sd_hi)
        z = rng.choice([-2, -1, 1, 2, 3])
        return MathDraw(
            rf"\mu = {mean}, \quad \sigma = {sd}, \quad z = {z}",
            str(mean + z * sd), prompt="จงหาค่าข้อมูล x ที่มีคะแนนมาตรฐานนี้",
            distractors=[str(mean - z * sd), str(mean + z), str(z * sd)])


@question_type("math.z_score_compare", display_name={"th": "เปรียบเทียบด้วยคะแนนมาตรฐาน"},
               level={"th": "ม.6"}, topic="ค่ามาตรฐาน")
class ZScoreCompare(ChoiceType):
    """The whole point of a z-score: comparing scores from different tests."""

    _PAIRS = (("วิชาคณิตศาสตร์", "วิชาภาษาอังกฤษ"), ("การวิ่ง 100 เมตร", "การกระโดดไกล"),
              ("การสอบกลางภาค", "การสอบปลายภาค"), ("วิชาฟิสิกส์", "วิชาเคมี"))

    def compose(self, rng: Random):
        m1, s1 = rng.randrange(50, 80, 5), rng.choice([2, 4, 5, 10])
        m2, s2 = rng.randrange(50, 80, 5), rng.choice([2, 4, 5, 10])
        z1 = rng.choice([1, 2, 3])
        z2 = rng.choice([z for z in (1, 2, 3) if z != z1])
        # The raw scores are arranged to point the other way whenever they can.
        x1, x2 = m1 + z1 * s1, m2 + z2 * s2
        a, b = rng.choice(self._PAIRS)
        better = a if z1 > z2 else b
        stem = (f"นักเรียนคนหนึ่งได้คะแนน{a} {x1} คะแนน "
                f"(ค่าเฉลี่ย {m1} ส่วนเบี่ยงเบนมาตรฐาน {s1}) "
                f"และคะแนน{b} {x2} คะแนน "
                f"(ค่าเฉลี่ย {m2} ส่วนเบี่ยงเบนมาตรฐาน {s2}) "
                "เมื่อเทียบกับกลุ่ม นักเรียนทำได้ดีกว่าในด้านใด")
        other = b if better == a else a
        return stem, better, [other, "ทั้งสองด้านเท่ากัน", "เปรียบเทียบไม่ได้"]


@question_type("math.z_score_word_m6", display_name={"th": "โจทย์ปัญหาค่ามาตรฐาน"},
               level=M6, topic="ค่ามาตรฐาน")
class ZScoreWordM6(WordProblem):
    def expr(self, rng: Random):
        mean, sd = rng.randrange(40, 80, 5), rng.choice((4, 5, 8, 10, 12))
        z = rng.choice((-2, -1.5, -1, -0.5, 0.5, 1, 1.5, 2, 2.5))
        x = mean + z * sd
        if x != int(x):
            z = int(z) or 1
            x = mean + z * sd
        x = int(x)
        p = rng.choice(_story.NAMES)
        if rng.random() < 0.5:
            return MathDraw("", str(x),
                            prompt=(f"คะแนนสอบมีค่าเฉลี่ย {mean} และส่วนเบี่ยงเบนมาตรฐาน {sd} ถ้า{p}ได้ค่ามาตรฐาน "
                                    f"{z:g} {p}ได้คะแนนเท่าใด"),
                            # z · s alone, and mean − z · s.
                            distractors=_story.keep(int(z * sd), int(mean - z * sd), mean + int(z),
                                                    answer=x, lo=-999))
        return MathDraw("", str(sd),
                        prompt=(f"คะแนนสอบมีค่าเฉลี่ย {mean} {p}ได้ {x} คะแนน คิดเป็นค่ามาตรฐาน {z:g} "
                                f"ส่วนเบี่ยงเบนมาตรฐานของคะแนนเท่ากับเท่าใด"),
                        distractors=_story.keep(abs(x - mean), int(abs(x - mean) * abs(z)) or sd + 1, sd * 2,
                                                answer=sd, lo=1))

from fractions import Fraction  # noqa: E402

from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import question_type  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathType, WordProblem  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m6 import M6 as LEVEL  # noqa: E402


def _nz6(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk6(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk6(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk6(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt6(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk6(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk6(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))


def _num6(v) -> str:
    """A terminating decimal without trailing zeros: Fraction(25, 2) -> 12.5."""
    v = Fraction(v)
    sign = "-" if v < 0 else ""
    v = abs(v)
    whole, rem = divmod(v.numerator, v.denominator)
    if not rem:
        return f"{sign}{whole}"
    digits = ""
    for _ in range(6):
        rem *= 10
        d, rem = divmod(rem, v.denominator)
        digits += str(d)
        if not rem:
            break
    return f"{sign}{whole}.{digits.rstrip('0')}"


def _dk6(*values, answer) -> list[str]:
    """Distinct decimal distractors, the answer left out."""
    return _tk6(*(_num6(v) for v in values), answer=_num6(answer))

# ── More standard scores (2026-11): the standard deviation from z, the mean from z, the gap between two z,
# what a shift does, what z-scores average to, and the share above a z ──


@question_type("math.sd_from_z_m6", display_name={"th": "หาส่วนเบี่ยงเบนมาตรฐานจากค่ามาตรฐาน"}, level=LEVEL, topic="ค่ามาตรฐาน")
class SdFromZM6(WordProblem):
    def expr(self, rng: Random):
        mu, sd = rng.randint(30, 80), rng.randint(2, 15)
        z = rng.choice((1, 2, 3, -1, -2))
        x = mu + z * sd
        prompt = f"ข้อมูลชุดหนึ่งมีค่าเฉลี่ย {mu} ค่า {x} มีค่ามาตรฐานเท่ากับ {z} ส่วนเบี่ยงเบนมาตรฐานเท่ากับเท่าใด"
        # Not divided by z; the sign kept; the value over z.
        return MathDraw("", str(sd), prompt=prompt, distractors=_nk6(abs(x - mu), -sd, abs(x // z), sd + 1, answer=sd, lo=1))


@question_type("math.mean_from_z_m6", display_name={"th": "หาค่าเฉลี่ยจากค่ามาตรฐาน"}, level=LEVEL, topic="ค่ามาตรฐาน")
class MeanFromZM6(WordProblem):
    def expr(self, rng: Random):
        mu, sd = rng.randint(30, 80), rng.randint(2, 15)
        z = rng.choice((1, 2, -1, -2, 3))
        x = mu + z * sd
        prompt = f"ข้อมูลชุดหนึ่งมีส่วนเบี่ยงเบนมาตรฐาน {sd} ค่า {x} มีค่ามาตรฐานเท่ากับ {z} ค่าเฉลี่ยเท่ากับเท่าใด"
        # The shift the wrong way; the value itself; the shift by z only.
        return MathDraw("", str(mu), prompt=prompt, distractors=_nk6(x + z * sd, x, x - z, mu + 1, answer=mu, lo=1))


@question_type("math.z_gap_m6", display_name={"th": "ผลต่างของค่ามาตรฐาน"}, level=LEVEL, topic="ค่ามาตรฐาน")
class ZGapM6(WordProblem):
    def expr(self, rng: Random):
        mu, sd = rng.randint(40, 70), rng.choice((2, 4, 5, 8, 10))
        a, b = sorted(rng.sample(range(-4, 5), 2))
        x1, x2 = mu + a * sd, mu + b * sd
        right = b - a
        prompt = (f"คะแนนสอบมีค่าเฉลี่ย {mu} และส่วนเบี่ยงเบนมาตรฐาน {sd} ก้องได้ {x2} คะแนน และหมอกได้ {x1} คะแนน "
                  "ค่ามาตรฐานของก้องมากกว่าของหมอกเท่าใด")
        # The scores' gap; not divided by the deviation; the sum.
        return MathDraw("", str(right), prompt=prompt, distractors=_nk6(x2 - x1, abs(a + b) if a + b else right + 2, right + 1, b, answer=right))


@question_type("math.z_after_shift_m6", display_name={"th": "ค่ามาตรฐานเมื่อบวกหรือคูณข้อมูล"}, level=LEVEL, topic="ค่ามาตรฐาน")
class ZAfterShiftM6(ConceptBankType):
    ITEMS = [
        Concept("ถ้าบวกคะแนนของทุกคนเพิ่ม 5 คะแนน ค่ามาตรฐานของแต่ละคนจะเป็นอย่างไร", "เท่าเดิม",
                ("เพิ่มขึ้น 5", "เพิ่มขึ้น 5 เท่า", "ลดลง 5")),
        Concept("ถ้าคูณคะแนนของทุกคนด้วย 2 ค่ามาตรฐานของแต่ละคนจะเป็นอย่างไร", "เท่าเดิม",
                ("เพิ่มเป็น 2 เท่า", "เพิ่มขึ้น 2", "ลดลงครึ่งหนึ่ง")),
        Concept("ถ้าบวกคะแนนของทุกคนเพิ่ม 5 คะแนน ส่วนเบี่ยงเบนมาตรฐานจะเป็นอย่างไร", "เท่าเดิม",
                ("เพิ่มขึ้น 5", "เพิ่มขึ้น 25", "ลดลง 5")),
        Concept("ถ้าบวกคะแนนของทุกคนเพิ่ม 5 คะแนน ค่าเฉลี่ยจะเป็นอย่างไร", "เพิ่มขึ้น 5", ("เท่าเดิม", "เพิ่มขึ้น 5 เท่า", "ลดลง 5")),
    ]


@question_type("math.z_properties_m6", display_name={"th": "สมบัติของค่ามาตรฐาน"}, level=LEVEL, topic="ค่ามาตรฐาน")
class ZPropertiesM6(ConceptBankType):
    ITEMS = [
        Concept("ค่าเฉลี่ยของค่ามาตรฐานของข้อมูลทุกตัวในชุดเดียวกันเท่ากับเท่าใด", "0", ("1", "ค่าเฉลี่ยของข้อมูล", "ไม่แน่นอน")),
        Concept("ส่วนเบี่ยงเบนมาตรฐานของค่ามาตรฐานของข้อมูลทั้งชุดเท่ากับเท่าใด", "1", ("0", "ส่วนเบี่ยงเบนมาตรฐานของข้อมูล", "ไม่แน่นอน")),
        Concept("ข้อมูลที่มีค่ามาตรฐานเป็นลบ หมายความว่าอย่างไร", "มีค่าน้อยกว่าค่าเฉลี่ย", ("มีค่าเป็นลบ", "มีค่ามากกว่าค่าเฉลี่ย", "เป็นค่าผิดปกติเสมอ")),
        Concept("ข้อมูลที่มีค่ามาตรฐานเท่ากับ 0 หมายความว่าอย่างไร", "มีค่าเท่ากับค่าเฉลี่ย", ("มีค่าเท่ากับ 0", "มีค่าน้อยที่สุด", "ไม่มีการกระจาย")),
    ]


@question_type("math.share_above_z_m6", display_name={"th": "สัดส่วนข้อมูลที่อยู่เหนือค่ามาตรฐาน (กฎ 68–95–99.7)"}, level=LEVEL,
               topic="ค่ามาตรฐาน")
class ShareAboveZM6(ConceptBankType):
    ITEMS = [
        Concept("ข้อมูลแจกแจงปกติ ข้อมูลที่มีค่ามาตรฐานมากกว่า 1 มีประมาณร้อยละเท่าใด", "ร้อยละ 16", ("ร้อยละ 34", "ร้อยละ 68", "ร้อยละ 2.5")),
        Concept("ข้อมูลแจกแจงปกติ ข้อมูลที่มีค่ามาตรฐานมากกว่า 2 มีประมาณร้อยละเท่าใด", "ร้อยละ 2.5", ("ร้อยละ 5", "ร้อยละ 16", "ร้อยละ 95")),
        Concept("ข้อมูลแจกแจงปกติ ข้อมูลที่มีค่ามาตรฐานน้อยกว่า 1 มีประมาณร้อยละเท่าใด", "ร้อยละ 84", ("ร้อยละ 68", "ร้อยละ 16", "ร้อยละ 50")),
        Concept("ข้อมูลแจกแจงปกติ ข้อมูลที่มีค่ามาตรฐานมากกว่า 0 มีประมาณร้อยละเท่าใด", "ร้อยละ 50", ("ร้อยละ 68", "ร้อยละ 34", "ร้อยละ 100")),
    ]
