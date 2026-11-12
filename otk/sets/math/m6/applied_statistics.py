"""สถิติประยุกต์

คณิตศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ค 3.1 ม.6/1

Sets moved here from: math, math_data.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import ChoiceType

PROVENANCE = Provenance("original")


@question_type("math.data_type_classify", display_name={"th": "ข้อมูลเชิงปริมาณหรือคุณภาพ"},
               level={"th": "ม.6"}, topic="สถิติประยุกต์")
class DataTypeClassify(ChoiceType):
    QUANTITATIVE = ["ส่วนสูงของนักเรียน", "จำนวนพี่น้อง", "น้ำหนักกระเป๋า",
                    "คะแนนสอบวิชาคณิตศาสตร์", "อายุของผู้ตอบแบบสอบถาม",
                    "ระยะทางจากบ้านถึงโรงเรียน"]
    QUALITATIVE = ["สีที่ชอบ", "เพศ", "จังหวัดที่เกิด", "ยี่ห้อโทรศัพท์",
                   "ระดับความพึงพอใจ", "อาชีพของผู้ปกครอง"]

    def compose(self, rng: Random):
        if rng.random() < 0.5:
            item, answer = rng.choice(self.QUANTITATIVE), "ข้อมูลเชิงปริมาณ"
        else:
            item, answer = rng.choice(self.QUALITATIVE), "ข้อมูลเชิงคุณภาพ"
        other = ("ข้อมูลเชิงคุณภาพ" if answer == "ข้อมูลเชิงปริมาณ"
                 else "ข้อมูลเชิงปริมาณ")
        return (f"ข้อมูล “{item}” จัดเป็นข้อมูลชนิดใด", answer,
                [other, "ไม่ใช่ข้อมูลทางสถิติ", "เป็นได้ทั้งสองชนิด"])


@question_type("math.classify_data_type",
               display_name={"th": "จำแนกชนิดข้อมูล"}, level={"th": "ม.6"},
               topic="สถิติประยุกต์")
class ClassifyDataType(ChoiceType):
    _CONT, _DISC, _QUAL = ("ข้อมูลเชิงปริมาณแบบต่อเนื่อง",
                           "ข้อมูลเชิงปริมาณแบบไม่ต่อเนื่อง",
                           "ข้อมูลเชิงคุณภาพ")
    _ATTRS = [("ส่วนสูงของนักเรียน", _CONT), ("น้ำหนักของผลไม้", _CONT),
              ("อุณหภูมิของอากาศในแต่ละวัน", _CONT), ("เวลาที่ใช้วิ่ง 100 เมตร", _CONT),
              ("ปริมาณน้ำฝนในแต่ละเดือน", _CONT), ("ระยะทางจากบ้านถึงโรงเรียน", _CONT),
              ("จำนวนพี่น้อง", _DISC), ("จำนวนนักเรียนในห้อง", _DISC),
              ("จำนวนรถยนต์ที่ผ่านสี่แยกในหนึ่งชั่วโมง", _DISC),
              ("จำนวนหนังสือที่อ่านในหนึ่งเดือน", _DISC), ("จำนวนครั้งที่ขาดเรียนในภาคเรียน", _DISC),
              ("สีที่ชอบ", _QUAL), ("เพศ", _QUAL), ("กรุ๊ปเลือด", _QUAL),
              ("จังหวัดที่เกิด", _QUAL), ("ยี่ห้อโทรศัพท์ที่ใช้", _QUAL),
              ("ระดับความพึงพอใจ (มาก ปานกลาง น้อย)", _QUAL)]

    def compose(self, rng: Random):
        attr, label = rng.choice(self._ATTRS)
        others = [x for x in (self._CONT, self._DISC, self._QUAL) if x != label]
        return f"ข้อมูล “{attr}” เป็นข้อมูลชนิดใด?", label, others


@question_type("math.measurement_scale", display_name={"th": "มาตราการวัดของข้อมูล"},
               level={"th": "ม.6"}, topic="สถิติประยุกต์")
class MeasurementScale(ChoiceType):
    ITEMS = [
        ("หมายเลขเสื้อนักกีฬา", "มาตรานามบัญญัติ"),
        ("อันดับที่ได้จากการแข่งขัน", "มาตราเรียงอันดับ"),
        ("อุณหภูมิเป็นองศาเซลเซียส", "มาตราอันตรภาค"),
        ("น้ำหนักเป็นกิโลกรัม", "มาตราอัตราส่วน"),
        ("เลขประจำตัวนักเรียน", "มาตรานามบัญญัติ"),
        ("ระดับความพึงพอใจ 1–5", "มาตราเรียงอันดับ"),
        ("รหัสไปรษณีย์", "มาตรานามบัญญัติ"),
        ("กรุ๊ปเลือด", "มาตรานามบัญญัติ"),
        ("ระดับการศึกษา (ประถม มัธยม ปริญญาตรี)", "มาตราเรียงอันดับ"),
        ("ขนาดเสื้อ S M L XL", "มาตราเรียงอันดับ"),
        ("อุณหภูมิเป็นองศาฟาเรนไฮต์", "มาตราอันตรภาค"),
        ("ปีพุทธศักราช", "มาตราอันตรภาค"),
        ("ส่วนสูงเป็นเซนติเมตร", "มาตราอัตราส่วน"),
        ("รายได้ต่อเดือนเป็นบาท", "มาตราอัตราส่วน"),
        ("เวลาที่ใช้ทำข้อสอบเป็นนาที", "มาตราอัตราส่วน"),
    ]
    SCALES = ["มาตรานามบัญญัติ", "มาตราเรียงอันดับ", "มาตราอันตรภาค",
              "มาตราอัตราส่วน"]

    def compose(self, rng: Random):
        item, answer = rng.choice(self.ITEMS)
        return (f"ข้อมูล “{item}” อยู่ในมาตราการวัดใด", answer,
                [s for s in self.SCALES if s != answer])

from fractions import Fraction  # noqa: E402

from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import question_type  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem  # noqa: E402
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

# ── More applied statistics (2026-11): population and sample, sampling methods, primary and secondary data,
# a biased survey, discrete and continuous data, a stratified sample, and systematic sampling ──


@question_type("math.population_or_sample_m6", display_name={"th": "ประชากร ตัวอย่าง พารามิเตอร์ และค่าสถิติ"}, level=LEVEL,
               topic="สถิติประยุกต์")
class PopulationOrSampleM6(ConceptBankType):
    ITEMS = [
        Concept("สำรวจนักเรียน 200 คนจากนักเรียนทั้งโรงเรียน 2,000 คน นักเรียน 200 คนนี้เรียกว่าอะไร", "ตัวอย่าง",
                ("ประชากร", "พารามิเตอร์", "ค่าสถิติ")),
        Concept("ค่าเฉลี่ยส่วนสูงของนักเรียนทุกคนในโรงเรียน เรียกว่าอะไร", "พารามิเตอร์", ("ค่าสถิติ", "ตัวอย่าง", "ตัวแปร")),
        Concept("ค่าเฉลี่ยที่คำนวณจากกลุ่มตัวอย่าง เรียกว่าอะไร", "ค่าสถิติ", ("พารามิเตอร์", "ประชากร", "ค่าคงตัว")),
        Concept("ผู้มีสิทธิเลือกตั้งทั้งหมดในจังหวัดหนึ่งที่ต้องการศึกษา เรียกว่าอะไร", "ประชากร", ("ตัวอย่าง", "ค่าสถิติ", "พารามิเตอร์")),
    ]


@question_type("math.sampling_method_m6", display_name={"th": "วิธีการสุ่มตัวอย่าง"}, level=LEVEL, topic="สถิติประยุกต์")
class SamplingMethodM6(ConceptBankType):
    ITEMS = [
        Concept("จับฉลากรายชื่อนักเรียนจากกล่องที่มีรายชื่อทุกคน เป็นการสุ่มแบบใด", "การสุ่มอย่างง่าย",
                ("การสุ่มแบบแบ่งชั้นภูมิ", "การสุ่มแบบเป็นระบบ", "การสุ่มแบบกลุ่ม")),
        Concept("แบ่งนักเรียนตามระดับชั้นก่อน แล้วสุ่มจากแต่ละชั้นตามสัดส่วน เป็นการสุ่มแบบใด", "การสุ่มแบบแบ่งชั้นภูมิ",
                ("การสุ่มอย่างง่าย", "การสุ่มแบบเป็นระบบ", "การสุ่มแบบกลุ่ม")),
        Concept("เลือกทุกคนที่ 10 จากรายชื่อที่เรียงไว้ เป็นการสุ่มแบบใด", "การสุ่มแบบเป็นระบบ",
                ("การสุ่มอย่างง่าย", "การสุ่มแบบแบ่งชั้นภูมิ", "การสุ่มแบบกลุ่ม")),
        Concept("สุ่มเลือกห้องเรียนมา 3 ห้อง แล้วเก็บข้อมูลนักเรียนทุกคนในห้องนั้น เป็นการสุ่มแบบใด", "การสุ่มแบบกลุ่ม",
                ("การสุ่มอย่างง่าย", "การสุ่มแบบแบ่งชั้นภูมิ", "การสุ่มแบบเป็นระบบ")),
    ]


@question_type("math.primary_secondary_data_m6", display_name={"th": "ข้อมูลปฐมภูมิและข้อมูลทุติยภูมิ"}, level=LEVEL,
               topic="สถิติประยุกต์")
class PrimarySecondaryDataM6(ConceptBankType):
    ITEMS = [
        Concept("นักเรียนสัมภาษณ์ผู้ปกครองด้วยตนเองเพื่อเก็บข้อมูลรายได้ ข้อมูลนี้เป็นข้อมูลชนิดใด", "ข้อมูลปฐมภูมิ",
                ("ข้อมูลทุติยภูมิ", "ข้อมูลเชิงคุณภาพเสมอ", "ข้อมูลที่ใช้ไม่ได้")),
        Concept("ข้อมูลจำนวนประชากรที่นำมาจากรายงานของสำนักงานสถิติแห่งชาติ เป็นข้อมูลชนิดใด", "ข้อมูลทุติยภูมิ",
                ("ข้อมูลปฐมภูมิ", "ข้อมูลเชิงคุณภาพ", "ข้อมูลที่ใช้ไม่ได้")),
        Concept("ครูวัดส่วนสูงของนักเรียนในห้องด้วยตนเอง ข้อมูลนี้เป็นข้อมูลชนิดใด", "ข้อมูลปฐมภูมิ",
                ("ข้อมูลทุติยภูมิ", "ข้อมูลเชิงคุณภาพ", "ข้อมูลที่ใช้ไม่ได้")),
        Concept("ข้อมูลปริมาณน้ำฝนย้อนหลังที่ดาวน์โหลดจากเว็บไซต์กรมอุตุนิยมวิทยา เป็นข้อมูลชนิดใด", "ข้อมูลทุติยภูมิ",
                ("ข้อมูลปฐมภูมิ", "ข้อมูลเชิงคุณภาพ", "ข้อมูลที่ใช้ไม่ได้")),
    ]


@question_type("math.biased_survey_m6", display_name={"th": "การสำรวจที่อาจทำให้ผลลำเอียง"}, level=LEVEL, topic="สถิติประยุกต์")
class BiasedSurveyM6(ConceptBankType):
    ITEMS = [
        Concept("ต้องการรู้ว่านักเรียนทั้งโรงเรียนชอบกีฬาอะไร วิธีใดอาจทำให้ผลลำเอียงมากที่สุด",
                "ถามเฉพาะนักเรียนในชมรมฟุตบอล",
                ("สุ่มนักเรียนจากทุกระดับชั้น", "จับฉลากรายชื่อนักเรียนทั้งโรงเรียน", "เลือกทุกคนที่ 20 จากรายชื่อทั้งหมด")),
        Concept("ต้องการรู้ความพึงพอใจของผู้ใช้บริการรถเมล์ทั้งเมือง วิธีใดอาจทำให้ผลลำเอียงมากที่สุด",
                "ถามเฉพาะผู้โดยสารที่ป้ายหน้าบ้านตอนเช้า",
                ("สุ่มผู้โดยสารจากหลายสายและหลายช่วงเวลา", "สุ่มรายชื่อจากบัตรโดยสารทั้งหมด", "แบ่งตามสายรถแล้วสุ่มตามสัดส่วน")),
        Concept("ต้องการรู้เวลานอนเฉลี่ยของวัยรุ่น วิธีใดอาจทำให้ผลลำเอียงมากที่สุด", "ถามเฉพาะเพื่อนสนิทของตนเอง",
                ("สุ่มนักเรียนจากหลายโรงเรียน", "สุ่มรายชื่อจากทะเบียนนักเรียน", "แบ่งตามช่วงอายุแล้วสุ่มตามสัดส่วน")),
    ]


@question_type("math.discrete_or_continuous_m6", display_name={"th": "ข้อมูลไม่ต่อเนื่องและข้อมูลต่อเนื่อง"}, level=LEVEL,
               topic="สถิติประยุกต์")
class DiscreteOrContinuousM6(ConceptBankType):
    ITEMS = [
        Concept("จำนวนพี่น้องของนักเรียนแต่ละคน เป็นข้อมูลแบบใด", "ข้อมูลเชิงปริมาณแบบไม่ต่อเนื่อง",
                ("ข้อมูลเชิงปริมาณแบบต่อเนื่อง", "ข้อมูลเชิงคุณภาพ", "ข้อมูลที่วัดไม่ได้")),
        Concept("เวลาที่ใช้วิ่ง 100 เมตรของนักเรียนแต่ละคน เป็นข้อมูลแบบใด", "ข้อมูลเชิงปริมาณแบบต่อเนื่อง",
                ("ข้อมูลเชิงปริมาณแบบไม่ต่อเนื่อง", "ข้อมูลเชิงคุณภาพ", "ข้อมูลที่วัดไม่ได้")),
        Concept("จำนวนรถที่ผ่านสี่แยกในแต่ละชั่วโมง เป็นข้อมูลแบบใด", "ข้อมูลเชิงปริมาณแบบไม่ต่อเนื่อง",
                ("ข้อมูลเชิงปริมาณแบบต่อเนื่อง", "ข้อมูลเชิงคุณภาพ", "ข้อมูลที่วัดไม่ได้")),
        Concept("น้ำหนักของผลมะม่วงแต่ละลูก เป็นข้อมูลแบบใด", "ข้อมูลเชิงปริมาณแบบต่อเนื่อง",
                ("ข้อมูลเชิงปริมาณแบบไม่ต่อเนื่อง", "ข้อมูลเชิงคุณภาพ", "ข้อมูลที่วัดไม่ได้")),
    ]


@question_type("math.stratified_share_m6", display_name={"th": "จำนวนตัวอย่างจากแต่ละชั้นภูมิ"}, level=LEVEL, topic="สถิติประยุกต์")
class StratifiedShareM6(WordProblem):
    def expr(self, rng: Random):
        unit = rng.choice((10, 20, 25, 50))
        a, b, c = rng.randint(2, 12), rng.randint(2, 12), rng.randint(2, 12)
        sample = (a + b + c) * rng.randint(1, 4)
        k = sample // (a + b + c)
        right = a * k
        prompt = (f"โรงเรียนมีนักเรียน ม.4 {a * unit} คน ม.5 {b * unit} คน และ ม.6 {c * unit} คน ต้องการสุ่มตัวอย่าง {sample} คน "
                  "แบบแบ่งชั้นภูมิตามสัดส่วน ต้องสุ่มนักเรียน ม.4 กี่คน")
        # A third each; ม.4's own count; the share of another grade.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk6(sample // 3 if sample // 3 != right else right + 1, b * k, c * k, right + k, answer=right, lo=1))


@question_type("math.systematic_sampling_m6", display_name={"th": "การสุ่มแบบเป็นระบบ"}, level=LEVEL, topic="สถิติประยุกต์")
class SystematicSamplingM6(WordProblem):
    def expr(self, rng: Random):
        step = rng.choice((5, 10, 20, 25, 50))
        n = rng.randint(4, 20)
        total = step * n
        first = rng.randint(1, step)
        k = rng.randint(3, min(n, 8))
        right = first + (k - 1) * step
        prompt = (f"มีประชากร {total} หน่วย ต้องการสุ่มตัวอย่าง {n} หน่วยแบบเป็นระบบ ถ้าหน่วยแรกที่สุ่มได้คือหมายเลข {first} "
                  f"หน่วยที่ {k} ที่ถูกเลือกคือหมายเลขใด")
        # One step too many; the step times k; the first plus k.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk6(first + k * step, k * step, first + k, right - 1, answer=right, lo=1))
