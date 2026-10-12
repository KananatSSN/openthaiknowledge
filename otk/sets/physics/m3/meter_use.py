"""การใช้โวลต์มิเตอร์และแอมมิเตอร์วัดปริมาณทางไฟฟ้า

ฟิสิกส์ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.3/3

Sets moved here from: science_wave_d32.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d22 import _facts
from otk.sets._support.science_wave_d32 import THIRD_SECONDARY, _vi_data

PROVENANCE = Provenance("original")


METER_USE_TOPIC = "การใช้โวลต์มิเตอร์และแอมมิเตอร์วัดปริมาณทางไฟฟ้า"


METER_FACTS = (
    ("เหตุใดจึงต้องต่อแอมมิเตอร์แบบอนุกรม แต่ต่อโวลต์มิเตอร์แบบขนานในการวัดปริมาณทางไฟฟ้า",
     "แอมมิเตอร์วัดกระแสที่ไหลผ่านจึงต่ออนุกรม ส่วนโวลต์มิเตอร์วัดความต่างศักย์ระหว่างสองจุดจึงต่อขนาน",
     ("แอมมิเตอร์วัดความต่างศักย์จึงต่อขนาน ส่วนโวลต์มิเตอร์วัดกระแสไฟฟ้าจึงต่ออนุกรม", "ทั้งแอมมิเตอร์และโวลต์มิเตอร์ต่ออนุกรม เพราะทั้งสองเครื่องวัดสิ่งที่ไหลผ่านอุปกรณ์",
      "การต่อแบบอนุกรมหรือขนานไม่มีผลต่อค่าที่วัดได้เลย", "ทั้งสองเครื่องต้องต่อแบบขนานเสมอ", "ต่อแบบใดก็ได้ขึ้นกับความสะดวก")),
    ("แอมมิเตอร์และโวลต์มิเตอร์แสดงค่าในหน่วยใดตามลำดับ", "แอมแปร์ (A) และโวลต์ (V)",
     ("โวลต์ (V) และแอมแปร์ (A)", "โอห์ม (Ω) และวัตต์ (W)", "วัตต์ (W) และจูล (J)", "จูล (J) และโอห์ม (Ω)", "แอมแปร์ (A) และโอห์ม (Ω)")),
    ("การต่อมิเตอร์เข้ากับวงจรไฟฟ้ากระแสตรงควรต่อขั้วอย่างไร", "ขั้วบวกของมิเตอร์ต่อด้านที่ใกล้ขั้วบวกของแหล่งจ่ายไฟ ขั้วลบต่อด้านที่ใกล้ขั้วลบ",
     ("ต่อขั้วใดก็ได้ เพราะมิเตอร์อ่านค่าได้ถูกต้องไม่ว่าจะต่อขั้วแบบใด", "ต่อขั้วบวกของมิเตอร์กับสายดิน และต่อขั้วลบเข้ากับจุดที่มีศักย์ไฟฟ้าสูงกว่า", "ต่อขั้วลบทั้งสองสาย", "ต่อขั้วบวกทั้งสองสาย", "ไม่ต้องต่อขั้วลบ")),
    ("โวลต์มิเตอร์ที่ดีควรมีความต้านทานภายในเป็นอย่างไร", "สูงมาก เพื่อให้กระแสไหลผ่านโวลต์มิเตอร์น้อยที่สุด",
     ("ต่ำมาก เพื่อให้กระแสไหลผ่านได้มาก", "เป็นศูนย์", "เท่ากับตัวต้านทานที่วัด", "ต่ำพอ ๆ กับแอมมิเตอร์ เพื่อให้อ่านค่าได้ละเอียดที่สุด", "เปลี่ยนตามอุณหภูมิห้องเท่านั้น")),
)


METER_HINT = "แอมมิเตอร์ต่ออนุกรมในเส้นทางของกระแส ความต้านทานภายในต่ำมาก โวลต์มิเตอร์ต่อขนานคร่อมอุปกรณ์ ความต้านทานภายในสูงมาก"


WIRING = {
    ("แอมมิเตอร์", "อนุกรม"): "วัดกระแสไฟฟ้าที่ไหลผ่าน{d}ได้ถูกต้อง",
    ("แอมมิเตอร์", "ขนาน"): "แอมมิเตอร์อาจเสียหายหรือเกิดการลัดวงจร เพราะแอมมิเตอร์มีความต้านทานภายในต่ำมาก",
    ("โวลต์มิเตอร์", "ขนาน"): "วัดความต่างศักย์ไฟฟ้าคร่อม{d}ได้ถูกต้อง",
    ("โวลต์มิเตอร์", "อนุกรม"): "กระแสไฟฟ้าในวงจรเกือบเป็นศูนย์ {d}แทบไม่ทำงาน เพราะโวลต์มิเตอร์มีความต้านทานภายในสูงมาก",
}


DEVICES = ("หลอดไฟ", "ตัวต้านทาน", "มอเตอร์ของเล่น", "ออด")


METER_USE_SCENARIOS = (
    ("นักเรียนต้องวัดความต่างศักย์ไฟฟ้าคร่อมหลอดไฟในวงจรที่กำลังทำงานอยู่ ควรต่อโวลต์มิเตอร์อย่างไรโดยไม่ต้องตัดวงจร",
     "ต่อขั้วโวลต์มิเตอร์ทั้งสองข้างคร่อมหลอดไฟโดยตรงโดยไม่ต้องตัดสายไฟใด ๆ",
     ("ต้องตัดสายไฟและแทรกโวลต์มิเตอร์เข้าไปในเส้นทางเดียวกับหลอดไฟ", "ต่อโวลต์มิเตอร์ที่ขั้วเซลล์ไฟฟ้าเท่านั้นไม่ว่าจะวัดอุปกรณ์ใด", "ไม่สามารถวัดความต่างศักย์ได้ โดยไม่ตัดวงจรแล้วต่อโวลต์มิเตอร์แทนหลอดไฟ")),
    ("ก่อนวัดกระแสไฟฟ้าในวงจรที่ไม่ทราบขนาดกระแสแน่ชัด ควรเลือกช่วงการวัด (range) ของแอมมิเตอร์อย่างไร",
     "ควรเลือกช่วงการวัดที่กว้างที่สุดก่อน แล้วค่อยปรับลดลง เพื่อป้องกันความเสียหายจากกระแสเกิน",
     ("ควรเลือกช่วงการวัดที่แคบที่สุดเสมอเพื่อความแม่นยำสูงสุด", "ช่วงการวัดของแอมมิเตอร์ไม่มีผลต่อความปลอดภัยของเครื่องมือ", "ควรปรับช่วงการวัดหลังจากอ่านค่าเสร็จแล้ว เพื่อไม่ให้ค่าที่อ่านได้เปลี่ยนไป")),
    ("นักเรียนอ่านค่าจากแอมมิเตอร์ได้ 0.5 แอมแปร์ และจากโวลต์มิเตอร์ได้ 10 โวลต์ ที่ต่อคร่อมตัวต้านทานตัวเดียวในวงจรอย่างถูกวิธี ค่าความต้านทานคำนวณได้เท่าใด",
     "20 โอห์ม เพราะ R = V/I = 10/0.5",
     ("5 โอห์ม เพราะ R = I × V = 0.5 × 10", "0.05 โอห์ม เพราะ R = I/V = 0.5/10", "15 โอห์ม เพราะ R = V + I = 10 + 0.5")),
)


@question_type(
    "elec.meter_use_foundation",
    display_name={"th": "บอกวิธีต่อโวลต์มิเตอร์และแอมมิเตอร์ในวงจรไฟฟ้า"},
    level=THIRD_SECONDARY, subject=SUBJECT, topic=METER_USE_TOPIC,
)
class MeterUseFoundation(QuestionType):
    """How each meter is wired, its units, polarity and internal resistance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _facts(rng, METER_FACTS, hint=METER_HINT, topic=METER_USE_TOPIC)


@question_type(
    "elec.meter_use_fluency",
    display_name={"th": "วิเคราะห์ผลของการต่อแอมมิเตอร์ผิดวิธี"},
    level=THIRD_SECONDARY, subject=SUBJECT, topic=METER_USE_TOPIC,
)
class MeterUseFluency(QuestionType):
    """Each meter wired each way, and reading a needle on a stated range."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            meter, way = rng.choice(tuple(WIRING))
            device = rng.choice(DEVICES)
            right = WIRING[(meter, way)].format(d=device)
            wrongs = [v.format(d=device) for k, v in WIRING.items() if k != (meter, way)]
            return _labelled(stem=f"นักเรียนต่อ{meter}แบบ{way}กับ{device}ในวงจรที่มีถ่านไฟฉาย จะเกิดผลอย่างไร", correct=right,
                             wrongs=tuple(wrongs), hint=METER_HINT, topic=METER_USE_TOPIC)
        meter, unit = rng.choice((("แอมมิเตอร์", "A"), ("โวลต์มิเตอร์", "V")))
        while True:
            full = rng.choice((1, 2, 3, 5, 10, 15, 20, 30)) if unit == "V" else rng.choice((1, 2, 3, 5))
            divisions = rng.choice((10, 20, 25, 50))
            mark = rng.randint(1, divisions)
            reading = Fraction(full * mark, divisions)
            if (reading * 100).denominator == 1:
                break
        return numeric(stem=f"{meter}ตั้งช่วงการวัด 0-{full} {unit} หน้าปัดแบ่งเป็น {divisions} ช่องเท่ากัน เข็มชี้ที่ช่องที่ {mark} อ่านค่าได้เท่าใด",
                       answer=reading, wrongs=[mark, Fraction(full * mark, 100) if Fraction(full * mark, 100) != reading else reading * 2, reading + Fraction(full, divisions)],
                       unit=unit, topic=METER_USE_TOPIC, hint="ค่าที่อ่านได้ = ช่วงการวัดเต็มสเกล × จำนวนช่องที่เข็มชี้ ÷ จำนวนช่องทั้งหมด")


@question_type(
    "elec.meter_use_application",
    display_name={"th": "ใช้โวลต์มิเตอร์และแอมมิเตอร์วัดและคำนวณปริมาณทางไฟฟ้าในสถานการณ์จริง"},
    level=THIRD_SECONDARY, subject=SUBJECT, topic=METER_USE_TOPIC,
)
class MeterUseApplication(QuestionType):
    """Authored cases, resistance from two readings, and the smallest safe range."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.25:
            return _retopic(scenario_question(
                rng, METER_USE_SCENARIOS,
                hint="โวลต์มิเตอร์ต่อขนานโดยไม่ตัดวงจร แอมมิเตอร์ต่ออนุกรมและต้องเลือกช่วงการวัดอย่างเหมาะสม",
            ), METER_USE_TOPIC)
        if roll < 0.65:
            resistance, volts, amps = _vi_data(rng)
            device = rng.choice(DEVICES)
            return numeric(stem=f"แอมมิเตอร์ที่ต่ออนุกรมกับ{device}อ่านได้ {show(amps[1])} A และโวลต์มิเตอร์ที่ต่อคร่อม{device}อ่านได้ {volts[1]} V "
                                f"{device}มีความต้านทานกี่โอห์ม", answer=resistance,
                           wrongs=[amps[1] * volts[1] if (amps[1] * volts[1] * 100).denominator == 1 else resistance * 2, resistance * 2, Fraction(resistance, 2)],
                           unit="โอห์ม", topic=METER_USE_TOPIC, hint="R = V ÷ I")
        ranges = (Fraction(1, 2), 1, 3, 5, 10) if rng.random() < 0.5 else (3, 6, 15, 30, 60)
        unit = "A" if ranges[0] == Fraction(1, 2) else "V"
        meter = "แอมมิเตอร์" if unit == "A" else "โวลต์มิเตอร์"
        while True:
            expected = Fraction(rng.randint(1, int(ranges[-1] * 10) - 1), 10)
            if expected not in ranges:
                break
        right = next(r for r in ranges if r > expected)
        options = [f"0-{show(r)} {unit}" for r in ranges]
        picked = rng.sample([o for o in options if o != f"0-{show(right)} {unit}"], 3)
        return _labelled(stem=f"คาดว่าค่าที่จะวัดได้ประมาณ {show(expected)} {unit} {meter}มีช่วงการวัดให้เลือก {' '.join(options)} "
                              f"ควรเลือกช่วงใดจึงปลอดภัยและอ่านค่าได้ละเอียดที่สุด", correct=f"0-{show(right)} {unit}", wrongs=tuple(picked),
                         hint="เลือกช่วงที่เล็กที่สุดที่ยังมากกว่าค่าที่คาดว่าจะวัดได้", topic=METER_USE_TOPIC)
