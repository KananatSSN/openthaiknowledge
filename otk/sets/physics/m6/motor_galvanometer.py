"""หลักการทำงานของแกลแวนอมิเตอร์และมอเตอร์ไฟฟ้ากระแสตรง

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.6/3

Sets moved here from: science_wave_f13.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f13 import SUBJECT, UPPER_SIX, _exact

PROVENANCE = Provenance("original")


TOPIC_MOTOR = "หลักการทำงานของแกลแวนอมิเตอร์และมอเตอร์ไฟฟ้ากระแสตรง"


MOTOR_FACTS = (
    ("แกลแวนอมิเตอร์แบบขดลวดเคลื่อนที่ทำงานโดยอาศัยหลักการใด", "ขดลวดที่มีกระแสไฟฟ้าในสนามแม่เหล็กได้รับโมเมนต์ของแรงคู่ควบจนหมุน",
     ("การเหนี่ยวนำแม่เหล็กไฟฟ้าในขดลวด", "แรงไฟฟ้าระหว่างประจุบนเข็ม", "ความร้อนที่ทำให้ลวดขยายตัว")),
    ("คอมมิวเทเตอร์ในมอเตอร์ไฟฟ้ากระแสตรงทำหน้าที่อะไร", "กลับทิศกระแสไฟฟ้าในขดลวดทุกครึ่งรอบ ให้ขดลวดหมุนทางเดียวต่อเนื่อง",
     ("เพิ่มความต่างศักย์ให้มอเตอร์", "เปลี่ยนไฟฟ้ากระแสตรงเป็นกระแสสลับเพื่อส่งออก", "หยุดขดลวดเมื่อหมุนครบรอบ")),
    ("การเปลี่ยนแกลแวนอมิเตอร์เป็นแอมมิเตอร์ ต้องต่อตัวต้านทานอย่างไร", "ต่อตัวต้านทานค่าน้อย (ชันต์) ขนานกับแกลแวนอมิเตอร์",
     ("ต่อตัวต้านทานค่ามากอนุกรมกับแกลแวนอมิเตอร์", "ต่อตัวต้านทานค่ามากขนานกับแกลแวนอมิเตอร์", "ไม่ต้องต่อตัวต้านทาน")),
    ("การเปลี่ยนแกลแวนอมิเตอร์เป็นโวลต์มิเตอร์ ต้องต่อตัวต้านทานอย่างไร", "ต่อตัวต้านทานค่ามาก (มัลติพลายเออร์) อนุกรมกับแกลแวนอมิเตอร์",
     ("ต่อตัวต้านทานค่าน้อยขนานกับแกลแวนอมิเตอร์", "ต่อตัวต้านทานค่าน้อยอนุกรมกับแกลแวนอมิเตอร์", "ไม่ต้องต่อตัวต้านทาน")),
    ("อีเอ็มเอฟต้านกลับในมอเตอร์เกิดขึ้นเพราะเหตุใด", "ขดลวดที่หมุนตัดสนามแม่เหล็กจึงเกิดอีเอ็มเอฟเหนี่ยวนำที่ต้านแหล่งจ่าย",
     ("แบตเตอรี่มีความต้านทานภายใน", "ขดลวดร้อนขึ้นจนความต้านทานเพิ่ม", "แม่เหล็กถาวรอ่อนกำลังลง")),
)


@question_type(
    "phys.motor_galvanometer_foundation",
    display_name={"th": "หลักการทำงานของแกลแวนอมิเตอร์ มอเตอร์ และโมเมนต์ของแรงคู่ควบบนขดลวด"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MOTOR,
)
class MotorGalvanometerFoundation(QuestionType):
    """Why a coil turns, and the torque NIAB on it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            stem, correct, wrongs = rng.choice(MOTOR_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_MOTOR,
                             hint="ขดลวดที่มีกระแสในสนามแม่เหล็กได้รับแรงคู่ควบจนหมุน นี่คือหลักของแกลแวนอมิเตอร์และมอเตอร์")
        n, i, area, b = rng.choice([(n, i, Fraction(a, 1000), Fraction(t, 10)) for n in (10, 20, 50, 100, 200)
                                    for i in (1, 2, 3, 4, 5) for a in (1, 2, 4, 5, 10, 20) for t in (1, 2, 5, 10)
                                    if _exact(n * i * Fraction(a, 1000) * Fraction(t, 10))])
        torque = n * i * area * b
        return numeric(
            stem=(f"ขดลวดสี่เหลี่ยม {n} รอบ พื้นที่ {show(area * 10000)} cm² มีกระแสไฟฟ้า {i} A วางให้ระนาบขดลวดขนานกับ"
                  f"สนามแม่เหล็ก {show(b)} T โมเมนต์ของแรงคู่ควบที่กระทำต่อขดลวดเท่าใด"),
            answer=torque, wrongs=[i * area * b, torque * 10000, torque * 2], unit="N·m", topic=TOPIC_MOTOR,
            hint="τ = NIAB เมื่อระนาบขดลวดขนานกับสนาม (พื้นที่เป็นตารางเมตร 1 cm² = 10⁻⁴ m²)")


@question_type(
    "phys.motor_galvanometer_fluency",
    display_name={"th": "ดัดแปลงแกลแวนอมิเตอร์เป็นแอมมิเตอร์และโวลต์มิเตอร์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MOTOR,
)
class MotorGalvanometerFluency(QuestionType):
    """Shunt R = I_g R_g/(I − I_g) and multiplier R = V/I_g − R_g."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            # Only meters whose shunt comes out exact to the hundredth of an ohm.
            rg, ig_ma, full = rng.choice(
                [(r, g, x) for r in (9, 10, 18, 19, 20, 25, 49, 50, 99, 100, 199, 200) for g in (1, 2, 5, 10)
                 for x in (Fraction(1, 100), Fraction(1, 50), Fraction(1, 20), Fraction(1, 10), Fraction(1, 2), 1, 2, 5, 10)
                 if x > Fraction(g, 1000) and _exact(Fraction(g, 1000) * r / (x - Fraction(g, 1000)))])
            ig = Fraction(ig_ma, 1000)
            shunt = ig * rg / (full - ig)
            return numeric(
                stem=(f"แกลแวนอมิเตอร์ความต้านทาน {rg} Ω เข็มเบนเต็มสเกลที่กระแส {ig_ma} mA ต้องต่อชันต์กี่โอห์ม "
                      f"จึงวัดกระแสได้สูงสุด {show(full)} A"),
                answer=shunt, wrongs=[rg * full / ig, shunt * 10, Fraction(rg) / full], unit="Ω", topic=TOPIC_MOTOR,
                hint="ชันต์ขนานกับแกลแวนอมิเตอร์ ความต่างศักย์เท่ากัน: I_g R_g = (I − I_g) R_s")
        rg = rng.choice((10, 20, 25, 50, 100, 200))
        ig_ma = rng.choice((1, 2, 5, 10))
        ig = Fraction(ig_ma, 1000)
        volts = rng.choice([v for v in (1, 2, 3, 5, 10, 15, 20, 50, 100) if v / ig > rg])
        multiplier = volts / ig - rg
        return numeric(
            stem=(f"แกลแวนอมิเตอร์ความต้านทาน {rg} Ω เข็มเบนเต็มสเกลที่กระแส {ig_ma} mA ต้องต่อตัวต้านทานอนุกรมกี่โอห์ม "
                  f"จึงวัดความต่างศักย์ได้สูงสุด {volts} V"),
            answer=multiplier, wrongs=[volts / ig, volts / ig + rg, multiplier / 1000], unit="Ω", topic=TOPIC_MOTOR,
            hint="ความต้านทานรวม = V/I_g แล้วลบความต้านทานของแกลแวนอมิเตอร์ออก")


@question_type(
    "phys.motor_galvanometer_application",
    display_name={"th": "อีเอ็มเอฟต้านกลับ กระแส และกำลังของมอเตอร์ไฟฟ้ากระแสตรง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MOTOR,
)
class MotorGalvanometerApplication(QuestionType):
    """I = (V − E)/R for a running motor, and the mechanical power E × I."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        v, back, r = rng.choice([(v, e, r) for v in (6, 12, 24, 48, 110, 220) for e in range(1, v)
                                 for r in (Fraction(1, 2), 1, 2, 4, 5, 10) if _exact((v - e) / r)
                                 and 0.5 * v <= e and (v - e) / r <= 20])
        i = (v - back) / r
        shape = rng.randrange(3)
        given = f"มอเตอร์ไฟฟ้ากระแสตรงต่อกับแหล่งจ่าย {v} V ขดลวดมีความต้านทาน {show(r)} Ω ขณะหมุนมีอีเอ็มเอฟต้านกลับ {back} V"
        if shape == 0:
            return numeric(stem=f"{given} กระแสไฟฟ้าผ่านมอเตอร์เท่าใด", answer=i, wrongs=[v / r, back / r, (v + back) / r],
                           unit="A", topic=TOPIC_MOTOR, hint="I = (V − E) ÷ R อีเอ็มเอฟต้านกลับลดความต่างศักย์สุทธิ")
        if shape == 1:
            return numeric(stem=f"{given} กำลังกลที่มอเตอร์ให้ได้เท่าใด", answer=back * i, wrongs=[v * i, i * i * r, v * v / r],
                           unit="W", topic=TOPIC_MOTOR,
                           hint="กำลังที่ป้อน VI = กำลังกล EI + ความร้อนในขดลวด I²R ดังนั้นกำลังกล = E × I")
        return numeric(
            stem=(f"มอเตอร์ไฟฟ้ากระแสตรงต่อกับแหล่งจ่าย {v} V ขดลวดมีความต้านทาน {show(r)} Ω ขณะเริ่มหมุน (ยังไม่มีอีเอ็มเอฟต้านกลับ) "
                  "กระแสไฟฟ้าผ่านมอเตอร์เท่าใด"),
            answer=Fraction(v) / r, wrongs=[i, Fraction(v) * r, Fraction(v) / r / 2], unit="A", topic=TOPIC_MOTOR,
            hint="ตอนเริ่มหมุนยังไม่มีอีเอ็มเอฟต้านกลับ กระแส = V/R จึงสูงมาก")
