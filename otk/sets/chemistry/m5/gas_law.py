"""กฎของบอยล์ กฎของชาร์ล และกฎของเกย์-ลูสแซก

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.5/1

Sets moved here from: science_wave_f24.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import (
    ATMS,
    KELVINS,
    SUBJECT,
    UPPER_FIVE,
    _find,
    _volume,
    celsius,
    exact,
)

PROVENANCE = Provenance("original")


TOPIC_GAS_LAW = "กฎของบอยล์ กฎของชาร์ล และกฎของเกย์-ลูสแซก"


LAW_CASES = (
    ("ที่อุณหภูมิคงที่ ถ้า{change}ความดันของแก๊ส{k} ปริมาตรของแก๊สจะเป็นอย่างไร", -1),
    ("ที่ความดันคงที่ ถ้า{change}อุณหภูมิเคลวินของแก๊ส{k} ปริมาตรของแก๊สจะเป็นอย่างไร", 1),
    ("ที่ปริมาตรคงที่ ถ้า{change}อุณหภูมิเคลวินของแก๊ส{k} ความดันของแก๊สจะเป็นอย่างไร", 1),
)


SCENARIOS = (
    ("กดลูกสูบกระบอกฉีดยาที่ปิดปลายไว้ ปริมาตรอากาศลดลงและความดันเพิ่มขึ้น", "กฎของบอยล์"),
    ("ฟองอากาศที่ลอยขึ้นจากก้นสระน้ำที่อุณหภูมิเท่ากันทั้งสระมีขนาดใหญ่ขึ้น", "กฎของบอยล์"),
    ("ถุงขนมที่ปิดสนิทพองขึ้นเมื่อนำขึ้นไปบนยอดเขาที่อุณหภูมิเท่าเดิม", "กฎของบอยล์"),
    ("ลูกโป่งที่นำไปแช่ในตู้เย็นแฟบลง", "กฎของชาร์ล"),
    ("ลูกปิงปองที่บุบเล็กน้อยพองกลับเมื่อแช่ในน้ำร้อน", "กฎของชาร์ล"),
    ("ความดันลมยางรถยนต์เพิ่มขึ้นหลังขับรถระยะไกลจนยางร้อน", "กฎของเกย์-ลูสแซก"),
    ("กระป๋องสเปรย์ที่ใช้หมดแล้วระเบิดได้เมื่อโยนเข้ากองไฟ", "กฎของเกย์-ลูสแซก"),
    ("ความดันในหม้ออัดแรงดันที่ปิดสนิทเพิ่มขึ้นเมื่อให้ความร้อน", "กฎของเกย์-ลูสแซก"),
)


LAWS = ("กฎของบอยล์", "กฎของชาร์ล", "กฎของเกย์-ลูสแซก", "กฎของอาโวกาโดร")


@question_type(
    "chem.gas_law_foundation",
    display_name={"th": "กฎของบอยล์: ความดันกับปริมาตรของแก๊ส"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GAS_LAW,
)
class GasLawFoundation(QuestionType):
    """How one quantity follows another, then Boyle's P₁V₁ = P₂V₂."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            template, sign = rng.choice(LAW_CASES)
            k = rng.randint(2, 4)
            up = rng.random() < 0.5
            change, times = ("เพิ่ม", f"เป็น {k} เท่า") if up else ("ลด", f"ลงเหลือ 1/{k} เท่า")
            grows = up == (sign > 0)
            right = f"เพิ่มขึ้นเป็น {k} เท่า" if grows else f"ลดลงเหลือ 1/{k} เท่า"
            other = f"ลดลงเหลือ 1/{k} เท่า" if grows else f"เพิ่มขึ้นเป็น {k} เท่า"
            square = f"เพิ่มขึ้นเป็น {k * k} เท่า" if grows else f"ลดลงเหลือ 1/{k * k} เท่า"
            return _labelled(stem=template.format(change=change, k=times), correct=right,
                             wrongs=(other, "ไม่เปลี่ยนแปลง", square), topic=TOPIC_GAS_LAW,
                             hint="บอยล์: P แปรผกผันกับ V ชาร์ล: V แปรผันตรงกับ T (เคลวิน) เกย์-ลูสแซก: P แปรผันตรงกับ T (เคลวิน)")

        def draw():
            p1, p2 = rng.sample(ATMS, 2)
            v1, unit = _volume(rng)
            v2 = p1 * v1 / p2
            return (p1, v1, p2, v2, unit) if exact(v2) else None

        p1, v1, p2, v2, unit = _find(rng, draw)
        in_kpa = rng.random() < 0.4
        p = (lambda x: f"{show(x * 100)} kPa") if in_kpa else (lambda x: f"{show(x)} atm")
        hint = "อุณหภูมิคงที่: P₁V₁ = P₂V₂"
        if rng.random() < 0.5:
            return numeric(stem=f"แก๊สปริมาตร {show(v1)} {unit} ความดัน {p(p1)} ถ้าอุณหภูมิคงที่และเปลี่ยนความดันเป็น {p(p2)} "
                                f"ปริมาตรของแก๊สจะเป็นเท่าใด",
                           answer=v2, wrongs=[p2 * v1 / p1, v1 + p2 - p1 if v1 + p2 > p1 else v1 * 2, p1 * v1],
                           unit=unit, topic=TOPIC_GAS_LAW, hint=hint)
        scale = 100 if in_kpa else 1
        return numeric(stem=f"แก๊สปริมาตร {show(v1)} {unit} ความดัน {p(p1)} ถ้าอุณหภูมิคงที่และทำให้ปริมาตรเป็น {show(v2)} {unit} "
                            f"ความดันของแก๊สจะเป็นเท่าใด",
                       answer=p2 * scale, wrongs=[p1 * v2 / v1 * scale, p1 * scale * 2, (p1 + p2) * scale],
                       unit="kPa" if in_kpa else "atm", topic=TOPIC_GAS_LAW, hint=hint)


@question_type(
    "chem.gas_law_fluency",
    display_name={"th": "กฎของชาร์ล: ปริมาตรกับอุณหภูมิของแก๊ส"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GAS_LAW,
)
class GasLawFluency(QuestionType):
    """V₁/T₁ = V₂/T₂ with T in kelvin; the slip is using °C."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            t1, t2 = rng.sample(KELVINS, 2)
            v1, unit = _volume(rng)
            v2 = Fraction(v1 * t2, t1)
            return (t1, t2, v1, v2, unit) if exact(v2) else None

        t1, t2, v1, v2, unit = _find(rng, draw)
        hint = "ความดันคงที่: V₁/T₁ = V₂/T₂ โดย T เป็นเคลวิน (K = °C + 273)"
        if rng.random() < 0.6 or t2 == 273:
            celsius_slip = Fraction(v1 * (t2 - 273), t1 - 273) if t1 != 273 else v1 * 2
            return numeric(stem=f"แก๊สปริมาตร {show(v1)} {unit} ที่ {celsius(t1)} ถ้าความดันคงที่และเปลี่ยนอุณหภูมิเป็น "
                                f"{celsius(t2)} ปริมาตรของแก๊สจะเป็นเท่าใด",
                           answer=v2, wrongs=[celsius_slip, Fraction(v1 * t1, t2), v1 + abs(t2 - t1)],
                           unit=unit, topic=TOPIC_GAS_LAW, hint=hint)
        return numeric(stem=f"แก๊สปริมาตร {show(v1)} {unit} ที่ {celsius(t1)} ถ้าความดันคงที่ ต้องเปลี่ยนอุณหภูมิเป็นกี่ °C "
                            f"ปริมาตรจึงจะเป็น {show(v2)} {unit}",
                       answer=t2 - 273, wrongs=[t2, v2 / v1 * (t1 - 273), t2 - 273 + 10],
                       unit="°C", topic=TOPIC_GAS_LAW, allow_negative=True, hint=hint)


@question_type(
    "chem.gas_law_application",
    display_name={"th": "กฎของเกย์-ลูสแซกและกฎของแก๊สในชีวิตประจำวัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GAS_LAW,
)
class GasLawApplication(QuestionType):
    """P₁/T₁ = P₂/T₂ in tyres and cans, or naming the law behind an everyday case."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.35:
            case, law = rng.choice(SCENARIOS)
            return _labelled(stem=f"\"{case}\" อธิบายได้ด้วยกฎใด", correct=law,
                             wrongs=tuple(x for x in LAWS if x != law), topic=TOPIC_GAS_LAW,
                             hint="ดูว่าปริมาณใดคงที่: T คงที่ → บอยล์ P คงที่ → ชาร์ล V คงที่ → เกย์-ลูสแซก")
        hint = "ปริมาตรคงที่: P₁/T₁ = P₂/T₂ โดย T เป็นเคลวิน"
        if rng.random() < 0.5:
            def draw():
                t1, t2 = sorted(rng.sample((273, 275, 300, 320, 325, 350), 2))
                p1 = rng.randrange(180, 321, 10)
                p2 = Fraction(p1 * t2, t1)
                return (t1, t2, p1, p2) if exact(p2) else None

            t1, t2, p1, p2 = _find(rng, draw)
            return numeric(stem=f"ยางรถยนต์มีความดันลม {p1} kPa ที่ {celsius(t1)} หลังขับรถ ยางร้อนขึ้นเป็น {celsius(t2)} "
                                "ถ้าปริมาตรยางคงที่ ความดันลมยางเป็นเท่าใด",
                           answer=p2, wrongs=[Fraction(p1 * (t2 - 273), t1 - 273) if t1 != 273 else p1 * 2,
                                              Fraction(p1 * t1, t2), p1 + t2 - t1],
                           unit="kPa", topic=TOPIC_GAS_LAW, hint=hint)

        def draw():
            t1 = rng.choice((273, 275, 300))
            t2 = rng.choice([t for t in KELVINS if t > t1 + 50])
            p1 = rng.choice(ATMS[:6])
            p2 = p1 * t2 / t1
            return (t1, t2, p1, p2) if exact(p2) else None

        t1, t2, p1, p2 = _find(rng, draw)
        return numeric(stem=f"กระป๋องสเปรย์มีความดัน {show(p1)} atm ที่ {celsius(t1)} กระป๋องทนความดันได้สูงสุด {show(p2)} atm "
                            "จะให้ความร้อนกับกระป๋องได้ถึงกี่ °C ก่อนกระป๋องระเบิด",
                       answer=t2 - 273, wrongs=[t2, p2 / p1 * (t1 - 273) if t1 != 273 else t2 - 200, t2 - 273 + 50],
                       unit="°C", topic=TOPIC_GAS_LAW, hint=hint)
