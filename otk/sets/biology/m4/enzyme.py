"""เอนไซม์และปัจจัยที่มีผลต่อการทำงานของเอนไซม์

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 1 ม.4/9

Sets moved here from: science_wave_f46.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f46 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_ENZYME = "เอนไซม์และปัจจัยที่มีผลต่อการทำงานของเอนไซม์"


# (enzyme, substrate, where it works, optimum pH)
ENZYMES = (
    ("อะไมเลสในน้ำลาย", "แป้ง", "ปาก", 7), ("เพปซิน", "โปรตีน", "กระเพาะอาหาร", 2),
    ("ทริปซิน", "โปรตีน", "ลำไส้เล็ก", 8), ("ไลเพส", "ลิพิด", "ลำไส้เล็ก", 8),
    ("มอลเทส", "มอลโทส", "ลำไส้เล็ก", 7), ("แล็กเทส", "แล็กโทส", "ลำไส้เล็ก", 7),
)


ENZYME_FACTS = (
    ("บริเวณที่สารตั้งต้นเข้าจับกับเอนไซม์เรียกว่าอะไร", "บริเวณเร่ง (active site)",
     ("ไรโบโซม", "หมู่ R", "พันธะเพปไทด์")),
    ("เอนไซม์ชนิดหนึ่งทำงานกับสารตั้งต้นเพียงบางชนิดเพราะเหตุใด", "รูปร่างของบริเวณเร่งจำเพาะกับสารตั้งต้นนั้น",
     ("เอนไซม์มีขนาดเล็กเกินไป", "เอนไซม์ถูกใช้หมดไปในปฏิกิริยา", "สารตั้งต้นทุกชนิดมีรูปร่างเหมือนกัน")),
    ("เมื่อปฏิกิริยาสิ้นสุด เอนไซม์เป็นอย่างไร", "ยังคงเดิม นำกลับมาใช้เร่งปฏิกิริยาได้อีก",
     ("ถูกเปลี่ยนเป็นผลิตภัณฑ์", "สลายตัวไปทันที", "กลายเป็นสารตั้งต้น")),
    ("เอนไซม์ทำให้ปฏิกิริยาเกิดเร็วขึ้นได้อย่างไร", "ลดพลังงานก่อกัมมันต์ของปฏิกิริยา",
     ("เพิ่มพลังงานของผลิตภัณฑ์", "เพิ่มอุณหภูมิของเซลล์", "เปลี่ยนผลิตภัณฑ์ให้มากขึ้นกว่าที่สมดุล")),
    ("ตัวยับยั้งแบบแข่งขันยับยั้งเอนไซม์ได้อย่างไร", "มีรูปร่างคล้ายสารตั้งต้นจึงเข้าจับที่บริเวณเร่งแทน",
     ("ทำลายพันธะเพปไทด์ของเอนไซม์", "ทำให้สารตั้งต้นเปลี่ยนรูป", "เพิ่มพลังงานก่อกัมมันต์โดยไม่จับกับเอนไซม์")),
)


@question_type(
    "biology.enzyme_foundation",
    display_name={"th": "การทำงานของเอนไซม์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ENZYME,
)
class EnzymeFoundation(QuestionType):
    """Active site, specificity, reuse, and a lower activation energy."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, right, wrongs = rng.choice(ENZYME_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs),
                             topic=TOPIC_ENZYME, hint="เอนไซม์เป็นโปรตีนที่มีบริเวณเร่งจำเพาะ ลดพลังงานก่อกัมมันต์ และไม่ถูกใช้หมด")
        enzyme, substrate, place, _ = rng.choice(ENZYMES)
        others = sorted({e[1] for e in ENZYMES} - {substrate}) + ["เซลลูโลส"]
        return _labelled(stem=f"{enzyme}ซึ่งทำงานที่{place} เร่งการย่อยสารใด", correct=substrate,
                         wrongs=tuple(others), topic=TOPIC_ENZYME,
                         hint="ชื่อเอนไซม์มักบอกสารตั้งต้น เช่น อะไมเลสย่อยแป้ง ไลเพสย่อยลิพิด")


@question_type(
    "biology.enzyme_fluency",
    display_name={"th": "ผลของอุณหภูมิ pH และความเข้มข้นต่อการทำงานของเอนไซม์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ENZYME,
)
class EnzymeFluency(QuestionType):
    """A peak at the optimum; too hot or the wrong pH changes the enzyme's shape."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            enzyme, _, place, ph = rng.choice(ENZYMES)
            return numeric(stem=f"{enzyme}ซึ่งทำงานใน{place} ทำงานได้ดีที่สุดที่ pH ประมาณเท่าใด", answer=ph,
                           wrongs=[{2: 8, 7: 2, 8: 2}[ph], 14 - ph if 14 - ph != ph else ph + 3, ph + 4 if ph < 10 else ph - 4],
                           unit="", topic=TOPIC_ENZYME, hint="กระเพาะอาหารเป็นกรด (pH ~2) ลำไส้เล็กเป็นเบสอ่อน (pH ~8) ปากเป็นกลาง")
        cases = (
            ("เพิ่มอุณหภูมิจาก 20 °C เป็น 37 °C", "อัตราการทำงานของเอนไซม์ในร่างกายคนเพิ่มขึ้น"),
            ("เพิ่มอุณหภูมิจาก 37 °C เป็น 70 °C", "เอนไซม์เสียสภาพ อัตราลดลงอย่างมาก"),
            ("นำเพปซินไปไว้ในสารละลาย pH 8", "เพปซินทำงานได้น้อยลงมากเพราะ pH ไม่เหมาะสม"),
            ("เพิ่มความเข้มข้นของสารตั้งต้นในขณะที่เอนไซม์มีปริมาณคงที่", "อัตราเพิ่มขึ้นแล้วคงที่เมื่อบริเวณเร่งถูกใช้เต็ม"),
            ("เพิ่มปริมาณเอนไซม์ในขณะที่มีสารตั้งต้นมากเกินพอ", "อัตราการเกิดปฏิกิริยาเพิ่มขึ้น"),
            ("แช่เอนไซม์ไว้ในตู้เย็นแล้วนำออกมาที่ 37 °C", "เอนไซม์กลับมาทำงานได้ เพราะความเย็นเพียงทำให้ทำงานช้าลง"),
        )
        case, right = rng.choice(cases)
        others = [c[1] for c in cases if c[1] != right]
        return _labelled(stem=f"ถ้า{case} จะเกิดผลอย่างไร", correct=right, wrongs=tuple(others),
                         topic=TOPIC_ENZYME, hint="อุณหภูมิและ pH ที่เหมาะสมให้อัตราสูงสุด ความร้อนสูงทำให้เสียสภาพ แต่ความเย็นเพียงทำให้ช้า")


@question_type(
    "biology.enzyme_application",
    display_name={"th": "อ่านข้อมูลการทดลองเกี่ยวกับการทำงานของเอนไซม์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ENZYME,
)
class EnzymeApplication(QuestionType):
    """Find the optimum, or the rate over an interval, from a table."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            peak = rng.choice((30, 35, 40, 45, 50))
            temps = [peak - 20, peak - 10, peak, peak + 10, peak + 20]
            top = rng.randrange(40, 101, 5)
            rates = [top * f // 100 for f in (rng.randrange(20, 40), rng.randrange(55, 80), 100, rng.randrange(40, 70),
                                              rng.randrange(0, 15))]
            rows = "; ".join(f"{t} °C: {r} หน่วย" for t, r in zip(temps, rates))
            return numeric(stem=f"วัดอัตราการทำงานของเอนไซม์ที่อุณหภูมิต่าง ๆ ได้ {rows} อุณหภูมิที่เหมาะสมที่สุดประมาณกี่ °C",
                           answer=peak, wrongs=[temps[1], temps[3], temps[4]], unit="°C", topic=TOPIC_ENZYME,
                           hint="อุณหภูมิที่ให้อัตราสูงสุดคืออุณหภูมิที่เหมาะสม")
        minutes = rng.choice((2, 4, 5, 10))
        amount = rng.randrange(10, 201, 10)
        rate = Fraction(amount, minutes)
        return numeric(stem=f"เอนไซม์ย่อยสารตั้งต้นได้ผลิตภัณฑ์ {amount} มิลลิกรัมใน {minutes} นาที อัตราการเกิดผลิตภัณฑ์เฉลี่ยเท่าใด",
                       answer=rate, wrongs=[amount * minutes, Fraction(minutes, amount) * 100, rate * 2], unit="มิลลิกรัม/นาที",
                       topic=TOPIC_ENZYME, hint="อัตรา = ปริมาณผลิตภัณฑ์ ÷ เวลา")
