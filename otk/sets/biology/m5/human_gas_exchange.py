"""การแลกเปลี่ยนแก๊สของมนุษย์

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/6

Sets moved here from: science_wave_f60.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f60 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_HUMAN = "การแลกเปลี่ยนแก๊สของมนุษย์"


HUMAN_FACTS = (
    ("O₂ ส่วนใหญ่ถูกลำเลียงในเลือดในรูปใด", "รวมกับฮีโมโกลบินเป็นออกซีฮีโมโกลบิน",
     ("ละลายในพลาสมาเป็นส่วนใหญ่", "อยู่ในรูปไฮโดรเจนคาร์บอเนตไอออน", "รวมกับเกล็ดเลือด", "จับกับเซลล์เม็ดเลือดขาวแล้วลำเลียงไป")),
    ("CO₂ ส่วนใหญ่ถูกลำเลียงในเลือดในรูปใด", "ไฮโดรเจนคาร์บอเนตไอออน (HCO₃⁻) ในพลาสมา",
     ("รวมกับฮีโมโกลบินทั้งหมด", "ละลายในพลาสมาในรูป CO₂ เป็นส่วนใหญ่", "จับกับเกล็ดเลือด", "อยู่ในรูปออกซีฮีโมโกลบินในเซลล์เม็ดเลือด")),
    ("เอนไซม์ใดในเซลล์เม็ดเลือดแดงเร่งการเปลี่ยน CO₂ กับน้ำเป็นกรดคาร์บอนิก", "คาร์บอนิกแอนไฮเดรส",
     ("อะไมเลสในน้ำลาย", "เพปซินในกระเพาะอาหาร", "ไลเพส", "ทริปซินในลำไส้เล็ก")),
    ("เหตุใดแก๊ส CO จึงเป็นอันตราย", "รวมกับฮีโมโกลบินได้ดีกว่า O₂ มาก เลือดจึงขนส่ง O₂ ได้น้อยลง",
     ("ทำให้ถุงลมในปอดแฟบทันที อากาศจึงเข้าปอดไม่ได้", "ทำลายกระดูกอ่อนของท่อลมจนท่อลมตีบและหายใจไม่ได้", "ทำให้เลือดเป็นเบสจัด", "ย่อยสลายเซลล์เม็ดเลือดแดงจนเลือดมีฮีโมโกลบินน้อยลงมาก")),
    ("ขณะหายใจเข้า กะบังลมและกล้ามเนื้อยึดซี่โครงด้านนอกทำงานอย่างไร", "กะบังลมหดตัวเลื่อนต่ำลง กล้ามเนื้อยึดซี่โครงด้านนอกหดตัวยกซี่โครงขึ้น",
     ("กะบังลมคลายตัวโค้งขึ้น ซี่โครงลดต่ำลง ปริมาตรช่องอกจึงเพิ่มขึ้นและอากาศเข้า", "กะบังลมไม่เปลี่ยนแปลง", "ปอดหดตัวดันอากาศเข้า", "ซี่โครงลดต่ำลงและกะบังลมยกสูง")),
    ("ศูนย์ควบคุมการหายใจอยู่ที่ใด และตอบสนองต่อสิ่งใดเป็นหลัก", "สมองส่วนเมดัลลาออบลองกาตา ตอบสนองต่อความเข้มข้นของ CO₂ ในเลือด",
     ("สมองส่วนซีรีบรัม ตอบสนองต่อความเข้มข้นของ O₂ ในอากาศที่หายใจเข้า", "ไขสันหลัง ตอบสนองต่ออุณหภูมิ", "หัวใจ ตอบสนองต่อความดันเลือดและอัตราการเต้นของหัวใจ", "ปอด ตอบสนองต่อเสียง")),
    ("การแลกเปลี่ยนแก๊สที่ถุงลมเกิดขึ้นโดยวิธีใด", "การแพร่จากบริเวณที่มีความดันย่อยของแก๊สสูงไปต่ำ",
     ("การลำเลียงแบบใช้พลังงานจากความดันต่ำไปสูง", "ออสโมซิส", "ฟาโกไซโทซิส", "การกรองด้วยแรงดันเลือดผ่านผนังถุงลมและหลอดเลือด")),
)


HUMAN_HINT = ("แก๊สแพร่จากความดันย่อยสูงไปต่ำ ที่ถุงลม O₂ เข้าเลือด CO₂ ออกจากเลือด ที่เนื้อเยื่อกลับกัน "
              "O₂ ส่วนใหญ่อยู่กับฮีโมโกลบิน CO₂ ส่วนใหญ่อยู่ในรูป HCO₃⁻")


SITES = (("อากาศในถุงลม", "เลือดในหลอดเลือดฝอยที่มาถึงปอด"), ("เลือดในหลอดเลือดฝอยที่เนื้อเยื่อ", "เซลล์กล้ามเนื้อที่กำลังทำงาน"))


@question_type(
    "biology.human_gas_exchange_foundation",
    display_name={"th": "การลำเลียง O₂ และ CO₂ ในเลือด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HUMAN,
)
class HumanGasExchangeFoundation(QuestionType):
    """Oxyhaemoglobin, bicarbonate, carbonic anhydrase and CO."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(HUMAN_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_HUMAN, hint=HUMAN_HINT)


@question_type(
    "biology.human_gas_exchange_fluency",
    display_name={"th": "ทิศทางการแพร่ของแก๊สจากความดันย่อย"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HUMAN,
)
class HumanGasExchangeFluency(QuestionType):
    """Each gas diffuses down its own partial-pressure gradient."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, b = rng.choice(SITES)
        gas = rng.choice(("O₂", "CO₂"))
        high, low = sorted(rng.sample(range(20, 111, 5), 2), reverse=True)
        a_high = rng.random() < 0.5
        pa, pb = (high, low) if a_high else (low, high)
        right = f"จาก{a}ไปยัง{b}" if pa > pb else f"จาก{b}ไปยัง{a}"
        other = f"จาก{b}ไปยัง{a}" if pa > pb else f"จาก{a}ไปยัง{b}"
        return _labelled(stem=f"ความดันย่อยของ {gas} ใน{a}เท่ากับ {pa} mmHg และใน{b}เท่ากับ {pb} mmHg {gas} จะแพร่ไปในทิศทางใด",
                         correct=right, wrongs=(other, "ไม่แพร่เพราะมีความดันย่อยต่างกัน", "แพร่ไปทั้งสองทิศเท่ากันจนหมด"),
                         topic=TOPIC_HUMAN, hint=HUMAN_HINT)


@question_type(
    "biology.human_gas_exchange_application",
    display_name={"th": "คำนวณปริมาณ O₂ และ CO₂ ที่เลือดลำเลียง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HUMAN,
)
class HumanGasExchangeApplication(QuestionType):
    """Haemoglobin × 1.34 mL O₂ per gram; CO₂ split into bicarbonate, carbamino and dissolved."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            hb = rng.randint(10, 17)
            per_100 = hb * Fraction(134, 100)
            if rng.random() < 0.5:
                return numeric(stem=f"เลือดมีฮีโมโกลบิน {hb} g ต่อ 100 mL ฮีโมโกลบิน 1 g จับ O₂ ได้ 1.34 mL เมื่ออิ่มตัว "
                                    f"เลือด 100 mL จับ O₂ ได้สูงสุดกี่มิลลิลิตร", answer=per_100,
                               wrongs=[hb, Fraction(134, 100), per_100 * 10], unit="mL", topic=TOPIC_HUMAN,
                               hint="O₂ ที่จับได้ = ปริมาณฮีโมโกลบิน × 1.34")
            litres = rng.randint(1, 6)
            return numeric(stem=f"เลือดมีฮีโมโกลบิน {hb} g ต่อ 100 mL ฮีโมโกลบิน 1 g จับ O₂ ได้ 1.34 mL เมื่ออิ่มตัว "
                                f"เลือด {litres} ลิตรจับ O₂ ได้สูงสุดกี่มิลลิลิตร", answer=per_100 * 10 * litres,
                           wrongs=[per_100 * litres, per_100 * 100 * litres, hb * 10 * litres], unit="mL", topic=TOPIC_HUMAN,
                           hint="1 ลิตร = 10 × 100 mL O₂ = ฮีโมโกลบิน × 1.34 × 10 × จำนวนลิตร")
        total = rng.randrange(20, 201, 10)
        parts = (("ไฮโดรเจนคาร์บอเนตไอออน", 70), ("คาร์บามิโนฮีโมโกลบิน", 23), ("CO₂ ละลายในพลาสมา", 7))
        name, share = rng.choice(parts)
        return numeric(stem=f"เลือดลำเลียง CO₂ ทั้งหมด {total} หน่วย ถ้าลำเลียงในรูปไฮโดรเจนคาร์บอเนตไอออนร้อยละ 70 "
                            f"คาร์บามิโนฮีโมโกลบินร้อยละ 23 และละลายในพลาสมาร้อยละ 7 ส่วนที่อยู่ในรูป{name}มีกี่หน่วย",
                       answer=Fraction(total * share, 100), wrongs=[Fraction(total * p, 100) for n, p in parts if n != name] + [share],
                       unit="หน่วย", topic=TOPIC_HUMAN, hint="ปริมาณแต่ละรูป = ปริมาณทั้งหมด × ร้อยละ ÷ 100")
