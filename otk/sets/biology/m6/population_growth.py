"""การเพิ่มของประชากร

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 5 ม.6/7

Sets moved here from: science_wave_f72.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f72 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_GROWTH = "การเพิ่มของประชากร"


GROWTH = {
    "แบบเอ็กโพเนนเชียล": ("กราฟรูปตัว J", "เกิดเมื่อทรัพยากรไม่จำกัดและไม่มีปัจจัยจำกัด", "อัตราการเพิ่มสูงขึ้นเรื่อย ๆ ตามขนาดประชากร"),
    "แบบลอจิสติก": ("กราฟรูปตัว S", "จำนวนเพิ่มช้าลงเมื่อเข้าใกล้ความสามารถในการรองรับของสิ่งแวดล้อม",
                    "ในที่สุดประชากรคงที่อยู่รอบค่าความสามารถในการรองรับ"),
}


GROWTH_HINT = ("การเพิ่มแบบเอ็กโพเนนเชียลเป็นรูปตัว J เพิ่มเป็นทวีคูณเมื่อทรัพยากรไม่จำกัด การเพิ่มแบบลอจิสติกเป็นรูปตัว S "
               "ชะลอตัวเมื่อเข้าใกล้ความสามารถในการรองรับ (K) อัตราการเพิ่ม = (เกิด − ตาย) ÷ ประชากร")


@question_type(
    "biology.population_growth_foundation",
    display_name={"th": "ลักษณะการเพิ่มของประชากรแบบเอ็กโพเนนเชียลและลอจิสติก"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GROWTH,
)
class PopulationGrowthFoundation(QuestionType):
    """J-curve or S-curve."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(sorted(GROWTH))
        other = next(k for k in GROWTH if k != kind)
        feature = rng.choice(GROWTH[kind])
        if rng.random() < 0.5:
            return _labelled(stem=f"การเพิ่มของประชากรที่มีลักษณะ \"{feature}\" เป็นแบบใด", correct=kind,
                             wrongs=(other, *rng.sample(("การกระจายแบบสม่ำเสมอ", "การรอดชีวิตแบบที่ 3", "การกระจายแบบกลุ่ม", "การเปลี่ยนแปลงแทนที่"), 2)),
                             topic=TOPIC_GROWTH, hint=GROWTH_HINT)
        extra = ("ประชากรลดลงเป็นศูนย์เสมอ", "จำนวนประชากรไม่เปลี่ยนแปลงตั้งแต่เริ่มต้น", "เกิดเฉพาะในพืช")
        return _labelled(stem=f"ข้อใดเป็นลักษณะของการเพิ่มของประชากร{kind}", correct=feature,
                         wrongs=(*rng.sample(GROWTH[other], 2), rng.choice(extra)), topic=TOPIC_GROWTH, hint=GROWTH_HINT)


@question_type(
    "biology.population_growth_fluency",
    display_name={"th": "ตัวอย่างการเพิ่มของประชากรในธรรมชาติ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GROWTH,
)
class PopulationGrowthFluency(QuestionType):
    """Which kind of growth each case shows."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cases = (("แบคทีเรียในอาหารเลี้ยงเชื้อใหม่ช่วงแรกที่อาหารยังเหลือมาก", "แบบเอ็กโพเนนเชียล"),
                 ("ยีสต์ในขวดอาหารที่ปิดไว้ จำนวนเพิ่มแล้วคงที่เมื่ออาหารจำกัด", "แบบลอจิสติก"),
                 ("หอยเชอรี่ที่เพิ่งถูกนำเข้าไปในนาที่ไม่มีศัตรูธรรมชาติ ช่วงแรก", "แบบเอ็กโพเนนเชียล"),
                 ("ประชากรกวางบนเกาะที่มีพืชอาหารจำกัด เพิ่มขึ้นแล้วคงที่", "แบบลอจิสติก"),
                 ("พารามีเซียมในจานเลี้ยงที่เติมอาหารจำนวนจำกัดครั้งเดียว", "แบบลอจิสติก"))
        case, kind = rng.choice(cases)
        if rng.random() < 0.45:
            start = rng.choice((10, 20, 25, 40, 50))
            if rng.random() < 0.5:
                data = [start * 2 ** t for t in range(6)]
                kind = "แบบเอ็กโพเนนเชียล"
            else:
                k = start * rng.choice((8, 10, 12))
                data = [start, start * 3, k // 2, k * 9 // 10, k, k]
                kind = "แบบลอจิสติก"
            listing = ", ".join(str(d) for d in data)
            return _labelled(stem=f"นับจำนวนประชากรทุกสัปดาห์ได้ {listing} ตัว การเพิ่มของประชากรนี้เป็นแบบใด", correct=kind,
                             wrongs=("แบบลอจิสติก" if kind == "แบบเอ็กโพเนนเชียล" else "แบบเอ็กโพเนนเชียล", "ลดลงแบบเส้นตรง",
                                     "คงที่ตลอดเวลา"), topic=TOPIC_GROWTH, hint=GROWTH_HINT)
        if rng.random() < 0.3:
            return _labelled(stem="ความสามารถในการรองรับของสิ่งแวดล้อม (K) หมายถึงข้อใด", correct="จำนวนประชากรสูงสุดที่สิ่งแวดล้อมรองรับได้อย่างยั่งยืน",
                             wrongs=tuple(("จำนวนประชากรเริ่มต้น", "อัตราการเกิดสูงสุด", "จำนวนที่ตายในหนึ่งปี", "พื้นที่ทั้งหมดของแหล่งที่อยู่")),
                             topic=TOPIC_GROWTH, hint=GROWTH_HINT)
        return _labelled(stem=f"\"{case}\" มีการเพิ่มของประชากรแบบใด", correct=kind,
                         wrongs=("แบบลอจิสติก" if kind == "แบบเอ็กโพเนนเชียล" else "แบบเอ็กโพเนนเชียล", "ไม่มีการเพิ่มเลย", "ลดลงแบบเส้นตรง"),
                         topic=TOPIC_GROWTH, hint=GROWTH_HINT)


@question_type(
    "biology.population_growth_application",
    display_name={"th": "คำนวณการเพิ่มของประชากร"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GROWTH,
)
class PopulationGrowthApplication(QuestionType):
    """Doubling, per-capita rate, and dN/dt = rN(K − N)/K."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            start = rng.choice((10, 20, 50, 100, 500))
            doubling = rng.choice((20, 30, 60))
            times = rng.randint(2, 8)
            total_min = doubling * times
            return numeric(stem=f"แบคทีเรีย {start} เซลล์ แบ่งตัวเพิ่มเป็น 2 เท่าทุก {doubling} นาที โดยไม่มีปัจจัยจำกัด เมื่อผ่านไป {total_min} นาที จะมีกี่เซลล์",
                           answer=start * 2 ** times, wrongs=[start * 2 * times, start * 2 ** (times - 1), start + 2 ** times], unit="เซลล์",
                           topic=TOPIC_GROWTH, hint="จำนวนที่เวลา t = จำนวนเริ่มต้น × 2^(t ÷ เวลาที่เพิ่มเป็นสองเท่า)")
        if roll < 0.65:
            while True:
                n = rng.randrange(100, 2001, 100)
                births = rng.randrange(10, n // 2, 5)
                deaths = rng.randrange(5, births, 5)
                r = Fraction(births - deaths, n)
                if (r * 10000).denominator == 1 and (Fraction(births * 100, n) * 100).denominator == 1                         and (Fraction(deaths * 100, n) * 100).denominator == 1:
                    break
            return numeric(stem=f"ประชากร {n} ตัว ในหนึ่งปีมีการเกิด {births} ตัว และตาย {deaths} ตัว อัตราการเพิ่มต่อหัวเป็นร้อยละเท่าใดต่อปี",
                           answer=r * 100, wrongs=[Fraction(births * 100, n), Fraction(deaths * 100, n), births - deaths], unit="%",
                           topic=TOPIC_GROWTH, hint="อัตราการเพิ่ม = (จำนวนเกิด − จำนวนตาย) ÷ ประชากร × 100")
        k = rng.randrange(500, 5001, 500)
        n = rng.choice((k // 10, k // 5, k // 4, k // 2, k * 3 // 4))
        r = Fraction(rng.choice((1, 2, 4, 5)), 10)
        rate = r * n * (k - n) / k
        if (rate * 100).denominator != 1:
            n = k // 2
            rate = r * n * (k - n) / k
        return numeric(stem=f"ประชากรเพิ่มแบบลอจิสติกด้วย r = {show(r)} ต่อปี ความสามารถในการรองรับ K = {k} ตัว ขณะที่ประชากรมี {n} ตัว "
                            f"อัตราการเพิ่ม (dN/dt = rN(K − N)/K) เป็นกี่ตัวต่อปี", answer=rate, wrongs=[r * n, r * (k - n), r * k], unit="ตัวต่อปี",
                       topic=TOPIC_GROWTH, hint="แทนค่าใน dN/dt = rN(K − N) ÷ K เมื่อ N ใกล้ K อัตราการเพิ่มจะใกล้ศูนย์")
