"""ปัจจัยที่มีผลต่อการสังเคราะห์ด้วยแสง

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/12

Sets moved here from: science_wave_f57.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f57 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_FACTOR = "ปัจจัยที่มีผลต่อการสังเคราะห์ด้วยแสง"


FACTOR_FACTS = (
    ("จุดชดเชยแสง (light compensation point) หมายถึงข้อใด", "ความเข้มแสงที่อัตราการสังเคราะห์ด้วยแสงเท่ากับอัตราการหายใจ",
     ("ความเข้มแสงที่พืชสังเคราะห์ด้วยแสงได้สูงสุด", "ความเข้มแสงที่พืชหยุดหายใจ", "ความเข้มแสงที่อัตราการสังเคราะห์ด้วยแสงสูงกว่าการหายใจมากที่สุด", "ความเข้มแสงที่อัตราการหายใจของพืชหยุดลงทั้งหมด")),
    ("เมื่ออุณหภูมิสูงเกินกว่าช่วงที่เหมาะสมมาก อัตราการสังเคราะห์ด้วยแสงลดลงเพราะเหตุใด", "เอนไซม์ในวัฏจักรคัลวินเสียสภาพ และปากใบปิด",
     ("แสงสว่างน้อยลงเมื่ออุณหภูมิสูง", "CO₂ ในอากาศหายไป", "คลอโรฟิลล์สร้างมากเกินไป", "คลอโรฟิลล์ถูกทำลายและน้ำในใบมากเกินไป")),
    ("ปัจจัยจำกัด (limiting factor) หมายถึงข้อใด", "ปัจจัยที่มีปริมาณไม่พอและควบคุมอัตราของกระบวนการในขณะนั้น",
     ("ปัจจัยที่มีปริมาณมากที่สุดและไม่ได้ควบคุมอัตราของกระบวนการ", "ปัจจัยที่ไม่มีผลต่อกระบวนการ", "ปัจจัยที่เพิ่มเท่าใดก็เพิ่มอัตราการสังเคราะห์ด้วยแสงได้เรื่อย ๆ", "ปัจจัยที่เพิ่มเท่าใดก็เพิ่มอัตราได้เสมอ")),
    ("ที่ความเข้มแสงต่ำกว่าจุดชดเชยแสง พืชมีการแลกเปลี่ยนแก๊สสุทธิอย่างไร", "ปล่อย CO₂ สุทธิ เพราะหายใจมากกว่าสังเคราะห์ด้วยแสง",
     ("ปล่อย O₂ สุทธิ เพราะสังเคราะห์ด้วยแสงมากกว่าหายใจ", "ไม่แลกเปลี่ยนแก๊สเลย เพราะอัตราทั้งสองเท่ากันพอดี", "ดูด CO₂ สุทธิมากที่สุด", "ปล่อยทั้ง O₂ และ CO₂ สุทธิเท่ากัน")),
    ("เมื่อความเข้มแสงสูงกว่าจุดอิ่มตัวแสง ถ้าเพิ่มแสงอีก อัตราการสังเคราะห์ด้วยแสงจะเป็นอย่างไร", "ไม่เพิ่มขึ้นอีก เพราะปัจจัยอื่นเป็นปัจจัยจำกัด",
     ("เพิ่มขึ้นเป็นสัดส่วนกับแสงเสมอ", "ลดลงเป็นศูนย์ทันที เพราะแสงมากเกินไปทำลายคลอโรฟิลล์", "เพิ่มขึ้นเป็นสองเท่า เพราะแสงยังเป็นปัจจัยจำกัดอยู่", "เปลี่ยนเป็นการหายใจทั้งหมด")),
    ("พืชที่ขึ้นใต้ร่มไม้มักมีจุดชดเชยแสงเป็นอย่างไรเมื่อเทียบกับพืชกลางแจ้ง", "ต่ำกว่า จึงมีอาหารเหลือสุทธิได้แม้แสงน้อย",
     ("สูงกว่า จึงต้องการแสงมากกว่า", "เท่ากับพืชกลางแจ้ง จึงต้องการแสงเท่ากัน", "สูงกว่า จึงต้องการแสงมากกว่าพืชกลางแจ้ง", "สูงกว่ามากจนสังเคราะห์ด้วยแสงไม่ได้")),
    ("ในการทดลองวัดผลของอุณหภูมิต่อการสังเคราะห์ด้วยแสง ควรควบคุมตัวแปรใดให้คงที่", "ความเข้มแสงและความเข้มข้นของ CO₂",
     ("อุณหภูมิของอากาศ", "อัตราการเกิดฟองแก๊ส", "เวลาที่ใช้วัดเท่านั้น", "ไม่ต้องควบคุมตัวแปรใดเลย")),
    ("เกษตรกรเพิ่ม CO₂ ในโรงเรือนปลูกผักที่มีแสงเพียงพอเพื่ออะไร", "เพิ่มอัตราการสังเคราะห์ด้วยแสงเพราะ CO₂ เป็นปัจจัยจำกัด",
     ("ลดการคายน้ำของผัก เพราะ CO₂ ทำให้ปากใบปิดสนิท", "ฆ่าแมลงศัตรูพืชที่อยู่ในโรงเรือนปิด เพราะ CO₂ เป็นพิษ", "ทำให้ผักหายใจมากขึ้น", "ลดอุณหภูมิในโรงเรือน")),
)


FACTOR_HINT = ("ปัจจัยจำกัดคือปัจจัยที่ถ้าเพิ่มแล้วอัตราเพิ่ม ถ้าเพิ่มแสงแล้วอัตราไม่เพิ่ม แต่เพิ่ม CO₂ แล้วเพิ่ม "
               "แสดงว่า CO₂ เป็นปัจจัยจำกัด")


@question_type(
    "biology.photosynthesis_factor_foundation",
    display_name={"th": "ความหมายของปัจจัยจำกัดและจุดชดเชยแสง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FACTOR,
)
class PhotosynthesisFactorFoundation(QuestionType):
    """Limiting factors, compensation point, heat and enzymes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(FACTOR_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_FACTOR, hint=FACTOR_HINT)


@question_type(
    "biology.photosynthesis_factor_fluency",
    display_name={"th": "หาปัจจัยจำกัดจากข้อมูลการทดลอง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FACTOR,
)
class PhotosynthesisFactorFluency(QuestionType):
    """Rate = min(k × light, CO₂ ceiling); the smaller term is what limits."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        k = rng.choice((2, 3, 4, 5))
        lights = [1000 * i for i in range(1, 7)]
        low_cap = k * rng.choice((2, 3))
        high_cap = low_cap + k * rng.choice((2, 3))
        rows = []
        for light in lights:
            base = k * light // 1000
            rows.append((light, min(base, low_cap), min(base, high_cap)))
        table = "; ".join(f"{ell} ลักซ์ → {a} และ {b}" for ell, a, b in rows)
        light = rng.choice(lights)
        base = k * light // 1000
        series = rng.choice(("low", "high"))
        if series == "high" and base >= high_cap:
            series = "low"  # nothing above 0.1% was measured, so a plateau there has no known cause
        cap = low_cap if series == "low" else high_cap
        right = "ความเข้มของแสง" if base < cap else "ความเข้มข้นของ CO₂"
        if base == cap:
            right = "ความเข้มของแสง"
            light = lights[0]
        which = "CO₂ ร้อยละ 0.04" if series == "low" else "CO₂ ร้อยละ 0.1"
        return _labelled(stem=f"อัตราการสังเคราะห์ด้วยแสง (หน่วยสัมพัทธ์) ที่ CO₂ ร้อยละ 0.04 และ 0.1 ตามลำดับ ที่ 25 °C: {table} "
                              f"ที่ความเข้มแสง {light} ลักซ์ และ {which} ปัจจัยใดเป็นปัจจัยจำกัด",
                         correct=right, wrongs=tuple(x for x in ("ความเข้มของแสง", "ความเข้มข้นของ CO₂", "อุณหภูมิของอากาศ", "ปริมาณน้ำในดิน")
                                                      if x != right)[:3],
                         topic=TOPIC_FACTOR, hint=FACTOR_HINT + " ถ้าอัตรายังเพิ่มตามแสง แสงเป็นปัจจัยจำกัด ถ้าอัตราคงที่แล้ว ให้ดูว่าเพิ่ม CO₂ แล้วอัตราเพิ่มหรือไม่")


@question_type(
    "biology.photosynthesis_factor_application",
    display_name={"th": "คำนวณอัตราการสังเคราะห์ด้วยแสงรวมและความเข้มแสงตามระยะ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FACTOR,
)
class PhotosynthesisFactorApplication(QuestionType):
    """Gross = net + respiration; light falls with the square of distance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            net = rng.randrange(2, 61)
            resp = rng.randrange(1, 21)
            if rng.random() < 0.5:
                return numeric(stem=f"ใบพืชที่ได้รับแสงปล่อย O₂ สุทธิ {net} หน่วยต่อชั่วโมง เมื่ออยู่ในที่มืดใช้ O₂ {resp} หน่วยต่อชั่วโมง "
                                    f"อัตราการสังเคราะห์ด้วยแสงรวมเป็นกี่หน่วยต่อชั่วโมง", answer=net + resp,
                               wrongs=[abs(net - resp) or net + 2 * resp, net, resp], unit="หน่วยต่อชั่วโมง", topic=TOPIC_FACTOR,
                               hint="การสังเคราะห์ด้วยแสงรวม = การปล่อย O₂ สุทธิ + O₂ ที่ใช้ในการหายใจ")
            gross = net + resp
            return numeric(stem=f"พืชสังเคราะห์ด้วยแสงรวม {gross} หน่วยต่อชั่วโมง และหายใจใช้ O₂ {resp} หน่วยต่อชั่วโมง ปล่อย O₂ สุทธิกี่หน่วยต่อชั่วโมง",
                           answer=net, wrongs=[gross + resp, gross, resp], unit="หน่วยต่อชั่วโมง", topic=TOPIC_FACTOR,
                           hint="O₂ สุทธิ = การสังเคราะห์ด้วยแสงรวม − การหายใจ")
        if roll < 0.7:
            d1 = rng.choice((10, 20, 30, 40))
            factor = rng.choice((Fraction(1, 2), 2, 4, Fraction(5, 2), Fraction(3, 2)))
            d2 = d1 * factor
            intensity = rng.randrange(100, 2001, 100)
            answer = intensity / factor ** 2
            if (Fraction(answer) * 100).denominator != 1:
                factor, d2, answer = 2, d1 * 2, Fraction(intensity, 4)
            return numeric(stem=f"หลอดไฟที่ห่างจากสาหร่ายหางกระรอก {d1} cm ให้ความเข้มแสง {intensity} ลักซ์ ถ้าเลื่อนหลอดไฟไปห่าง {show(d2)} cm "
                                f"ความเข้มแสงที่สาหร่ายได้รับเป็นกี่ลักซ์ (ความเข้มแสงแปรผกผันกับกำลังสองของระยะ)", answer=answer,
                           wrongs=[intensity / factor, intensity * factor, intensity * factor ** 2], unit="ลักซ์", topic=TOPIC_FACTOR,
                           hint="ความเข้มแสงใหม่ = ความเข้มแสงเดิม × (ระยะเดิม ÷ ระยะใหม่)²")
        rate = rng.randrange(5, 61)
        minutes = rng.choice((2, 4, 5, 10))
        return numeric(stem=f"สาหร่ายหางกระรอกปล่อยฟองแก๊ส {rate * minutes} ฟองใน {minutes} นาที อัตราการเกิดฟองแก๊สเป็นกี่ฟองต่อนาที",
                       answer=rate, wrongs=[rate * minutes, minutes, rate * 2],
                       unit="ฟองต่อนาที", topic=TOPIC_FACTOR, hint="อัตรา = จำนวนฟอง ÷ เวลา ใช้เป็นตัวแทนอัตราการสังเคราะห์ด้วยแสง")
