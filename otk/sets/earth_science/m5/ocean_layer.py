"""การแบ่งชั้นน้ำในมหาสมุทร

ธรณีวิทยา · ม.5 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/5

Sets moved here from: science_wave_f79.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f79 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_LAYER = "การแบ่งชั้นน้ำในมหาสมุทร"


LAYER_FACTS = (
    ("ชั้นน้ำผสมในมหาสมุทรมีลักษณะอย่างไร", "อยู่ด้านบนสุด ลมและคลื่นคลุกเคล้าจนอุณหภูมิเกือบเท่ากันตลอดชั้น",
     ("อุณหภูมิลดลงอย่างรวดเร็วตามความลึก เพราะอยู่ระหว่างน้ำอุ่นและน้ำเย็น", "อยู่ลึกที่สุด แสงส่องไม่ถึงจึงเย็นจัดและอุณหภูมิเกือบคงที่ตลอดปี", "ไม่ได้รับแสงอาทิตย์เลย", "มีความหนาแน่นมากที่สุด")),
    ("เทอร์โมไคลน์คือชั้นน้ำที่มีลักษณะอย่างไร", "อุณหภูมิลดลงอย่างรวดเร็วตามความลึกที่เพิ่มขึ้น",
     ("อุณหภูมิเท่ากันตลอดชั้นเพราะคลื่นคลุกเคล้า", "อยู่ด้านบนสุด ลมคลุกเคล้าจนอุณหภูมิเท่ากันตลอด", "อุณหภูมิเพิ่มขึ้นตามความลึก", "เป็นชั้นที่ลมพัดแรงที่สุด")),
    ("ชั้นน้ำลึกในมหาสมุทรมีลักษณะอย่างไร", "เย็นจัด อุณหภูมิเกือบคงที่ และมีความหนาแน่นมาก",
     ("ร้อนที่สุด เพราะอยู่ใกล้แกนโลกและได้รับความร้อนจากใต้พื้นทะเล", "อุณหภูมิเปลี่ยนตามฤดูกาลมาก", "คลื่นคลุกเคล้าจนอุณหภูมิเท่ากับผิวน้ำ", "อุณหภูมิเปลี่ยนตามฤดูกาลมาก และมีความหนาแน่นน้อยที่สุด")),
    ("ปัจจัยใดทำให้น้ำทะเลมีความหนาแน่นมากขึ้น", "อุณหภูมิต่ำลงหรือความเค็มสูงขึ้น",
     ("อุณหภูมิสูงขึ้นหรือความเค็มลดลง", "มีฝนตกลงมาเจือจางน้ำผิวหน้า", "มีแม่น้ำไหลลงมามาก", "ได้รับแสงอาทิตย์มากขึ้น")),
    ("เหตุใดน้ำทะเลจึงแบ่งเป็นชั้นตามความลึก", "น้ำที่ความหนาแน่นต่างกันไม่ผสมกันง่าย น้ำหนาแน่นมากจมอยู่ด้านล่าง",
     ("น้ำทุกความลึกมีอุณหภูมิเท่ากัน แต่ดวงจันทร์ดึงแต่ละชั้นแยกกัน", "แรงคอริออลิสแยกน้ำเป็นชั้น", "ดวงจันทร์ดึงน้ำแต่ละชั้นแยกกัน", "แรงคอริออลิสแยกน้ำแต่ละระดับให้ไหลคนละทิศจนไม่ผสมกัน")),
    ("บริเวณใดชั้นน้ำผสมหนาขึ้น", "บริเวณที่มีลมพัดแรงและคลื่นใหญ่",
     ("บริเวณที่ลมสงบและทะเลเรียบ", "บริเวณที่น้ำลึกเพียงไม่กี่เมตร", "บริเวณที่ลมสงบและน้ำนิ่ง", "บริเวณที่น้ำจืดไหลลงมามาก")),
    ("เหตุใดจึงแทบไม่พบเทอร์โมไคลน์ในมหาสมุทรบริเวณขั้วโลก", "น้ำผิวหน้าเย็นจัดใกล้เคียงกับน้ำลึก อุณหภูมิจึงแทบไม่ต่างกัน",
     ("น้ำขั้วโลกไม่มีเกลือละลายอยู่ ความหนาแน่นจึงเท่ากันทุกความลึก", "น้ำขั้วโลกไม่มีความเค็ม", "น้ำขั้วโลกลึกเพียงไม่กี่เมตร", "น้ำผิวหน้าร้อนกว่าน้ำลึกมาก เพราะได้รับแสงอาทิตย์ตลอดวันในฤดูร้อน")),
    ("ฮาโลไคลน์คือชั้นน้ำที่มีลักษณะอย่างไร", "ความเค็มเปลี่ยนแปลงอย่างรวดเร็วตามความลึก",
     ("อุณหภูมิเท่ากันตลอดชั้น", "ความหนาแน่นเท่ากันทุกระดับความลึก", "อุณหภูมิเท่ากันตลอดชั้นแต่ความเค็มคงที่", "มีความหนาแน่นเท่ากันทุกระดับ")),
    ("เหตุใดน้ำจืดจากปากแม่น้ำจึงไหลแผ่อยู่บนผิวน้ำทะเล", "น้ำจืดมีความหนาแน่นน้อยกว่าน้ำทะเลที่เค็มกว่า",
     ("น้ำจืดมีความหนาแน่นมากกว่าน้ำทะเล", "น้ำจืดเย็นกว่าน้ำทะเลเสมอ", "น้ำจืดมีความหนาแน่นมากกว่า แต่ถูกคลื่นยกขึ้นมา", "น้ำจืดเย็นกว่าน้ำทะเล จึงลอยอยู่ด้านบนได้")),
    ("เหตุใดเทอร์โมไคลน์ในเขตละติจูดกลางจึงเด่นชัดในฤดูร้อน", "ผิวน้ำได้รับความร้อนมาก อุณหภูมิจึงต่างจากน้ำลึกมาก",
     ("ผิวน้ำเย็นจัดเท่ากับน้ำลึก จึงแทบไม่มีชั้นใดต่างกัน", "ลมพัดแรงคลุกเคล้าน้ำทั้งมหาสมุทร", "น้ำลึกร้อนขึ้นจนเท่ากับผิวน้ำเพราะความร้อนจากแกนโลก", "ไม่มีแสงอาทิตย์ส่องถึงผิวน้ำ")),
)


LAYER_HINT = ("ตามอุณหภูมิ มหาสมุทรแบ่งเป็นชั้นน้ำผสม (ด้านบน อุณหภูมิเกือบเท่ากัน) เทอร์โมไคลน์ (อุณหภูมิลดลงเร็ว) และชั้นน้ำลึก "
              "(เย็นจัดและคงที่) น้ำยิ่งเย็นและยิ่งเค็มยิ่งหนาแน่น จึงจมอยู่ด้านล่าง")


LAYERS = ("ชั้นน้ำผสม", "เทอร์โมไคลน์", "ชั้นน้ำลึก")


@question_type(
    "geo.ocean_layer_foundation",
    display_name={"th": "ชั้นน้ำในมหาสมุทรและปัจจัยที่ทำให้แบ่งชั้น"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LAYER,
)
class OceanLayerFoundation(QuestionType):
    """Mixed layer, thermocline, deep water; temperature and salinity."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(LAYER_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_LAYER, hint=LAYER_HINT)


@question_type(
    "geo.ocean_layer_fluency",
    display_name={"th": "อ่านโปรไฟล์อุณหภูมิและเปรียบเทียบความหนาแน่นของน้ำทะเล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LAYER,
)
class OceanLayerFluency(QuestionType):
    """Which layer a depth is in; which sample is densest."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            mixed = rng.randrange(50, 201, 25)
            bottom = mixed + rng.randrange(600, 1001, 100)
            top_t = rng.randint(24, 30)
            deep_t = rng.randint(2, 5)
            layer = rng.randrange(3)
            depth = (rng.randrange(0, mixed, 5) if layer == 0 else
                     rng.randrange(mixed + 50, bottom - 49, 50) if layer == 1 else rng.randrange(bottom + 200, 4001, 100))
            return _labelled(stem=f"จากการวัดอุณหภูมิน้ำทะเล: ผิวน้ำถึงลึก {mixed} m อุณหภูมิประมาณ {top_t} °C, จาก {mixed} m ถึง {show(bottom)} m "
                                  f"อุณหภูมิลดลงจนเหลือ {deep_t} °C, ลึกกว่า {show(bottom)} m อุณหภูมิประมาณ {deep_t} °C คงที่ "
                                  f"ที่ความลึก {show(depth)} m อยู่ในชั้นน้ำใด",
                             correct=LAYERS[layer], wrongs=(*(n for n in LAYERS if n != LAYERS[layer]), "ชั้นบรรยากาศ"),
                             topic=TOPIC_LAYER, hint=LAYER_HINT)
        samples = []
        cold = rng.randint(2, 10)
        salty = rng.choice((35, 36, 37))
        samples.append((cold, salty))
        while len(samples) < 4:
            t, s = rng.randint(cold + 2, 30), rng.randint(30, salty - 1)
            if (t, s) not in samples:
                samples.append((t, s))
        order = rng.sample(range(4), 4)
        names = ("ก", "ข", "ค", "ง")
        table = " ".join(f"ตัวอย่าง {names[i]} อุณหภูมิ {samples[j][0]} °C ความเค็ม {samples[j][1]} ส่วนในพันส่วน" for i, j in enumerate(order))
        densest = names[order.index(0)]
        return _labelled(stem=f"{table} ตัวอย่างใดมีความหนาแน่นมากที่สุดและจะจมอยู่ด้านล่าง", correct=f"ตัวอย่าง {densest}",
                         wrongs=tuple(f"ตัวอย่าง {n}" for n in names if n != densest), topic=TOPIC_LAYER, hint=LAYER_HINT)


@question_type(
    "geo.ocean_layer_application",
    display_name={"th": "คำนวณอัตราการลดลงของอุณหภูมิในเทอร์โมไคลน์และปริมาณเกลือในน้ำทะเล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LAYER,
)
class OceanLayerApplication(QuestionType):
    """Temperature drop per 100 m in the thermocline; salt in a mass of seawater."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            top = rng.randrange(50, 201, 25)
            thick = rng.choice((200, 250, 400, 500, 800, 1000))
            upper, lower = rng.randint(20, 30), rng.randint(2, 8)
            rate = Fraction(upper - lower, thick) * 100
            if (rate * 100).denominator != 1:
                thick = 500
                rate = Fraction(upper - lower, thick) * 100
            return numeric(stem=f"เทอร์โมไคลน์แห่งหนึ่งอยู่ที่ความลึก {top} m ถึง {top + thick} m อุณหภูมิที่ขอบบน {upper} °C และที่ขอบล่าง {lower} °C "
                                f"อุณหภูมิลดลงเฉลี่ยกี่ °C ต่อความลึก 100 m",
                           answer=rate, wrongs=[Fraction(upper - lower, top + thick) * 100 if (Fraction(upper - lower, top + thick) * 10000).denominator == 1 else rate * 2,
                                                upper - lower, rate + Fraction(1, 2)],
                           unit="°C", topic=TOPIC_LAYER, hint="อัตรา = ผลต่างอุณหภูมิ ÷ ความหนาของชั้น × 100")
        salinity = rng.choice((30, 32, 33, 34, 35, 36, 37, 40))
        mass = rng.choice((Fraction(1, 2), 1, 2, 3, 5, 10, 20, Fraction(5, 2)))
        if rng.random() < 0.6:
            return numeric(stem=f"น้ำทะเลมีความเค็ม {salinity} ส่วนในพันส่วน (g/kg) น้ำทะเล {show(mass)} kg มีเกลือละลายอยู่กี่กรัม",
                           answer=salinity * mass, wrongs=[salinity * mass * 10, salinity, Fraction(salinity * mass, 10)], unit="g",
                           topic=TOPIC_LAYER, hint="มวลเกลือ (g) = ความเค็ม (g/kg) × มวลน้ำทะเล (kg)")
        salt = salinity * mass
        return numeric(stem=f"ระเหยน้ำทะเล {show(mass)} kg จนแห้งได้เกลือ {show(salt)} g น้ำทะเลนี้มีความเค็มกี่ส่วนในพันส่วน",
                       answer=salinity, wrongs=[salinity * 10, salt, salinity + 5], unit="ส่วนในพันส่วน", topic=TOPIC_LAYER,
                       hint="ความเค็ม (ส่วนในพันส่วน) = มวลเกลือ (g) ÷ มวลน้ำทะเล (kg)")
