"""ความสัมพันธ์ระหว่างขนาดของแรงกับระยะห่างจากแหล่งของสนาม

ฟิสิกส์ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.2/13

Sets moved here from: science_wave_d21.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d18 import SECONDARY_TWO
from otk.sets._support.science_wave_d21 import _facts

PROVENANCE = Provenance("original")


FIELD_DISTANCE_TOPIC = "ความสัมพันธ์ระหว่างขนาดของแรงกับระยะห่างจากแหล่งของสนาม"


FIELD_NAMES = ("แรงแม่เหล็ก", "แรงไฟฟ้า", "แรงโน้มถ่วง")


FIELD_SOURCES = (("แรงแม่เหล็ก", "แม่เหล็กแท่งเดียวกัน", ("คลิปเหล็ก", "ตะปูเหล็ก", "น็อตเหล็ก")),
                 ("แรงไฟฟ้า", "ลูกโป่งที่ถูกับผมลูกเดียวกัน", ("เศษกระดาษ", "เศษโฟม", "ผงชอล์ก")),
                 ("แรงโน้มถ่วง", "โลก", ("ดาวเทียม", "สถานีอวกาศ", "ยานสำรวจ")))


FIELD_DISTANCE_HINT = "แรงจากสนามทั้งสามชนิดมีขนาดลดลงเมื่อระยะห่างจากแหล่งของสนามเพิ่มขึ้น"


FIELD_DISTANCE_FACTS = (
    ("ข้อใดกล่าวถึงแรงจากสนามทั้งสามชนิดได้ถูกต้อง", "ทั้งสามชนิดมีขนาดลดลงเมื่อระยะห่างจากแหล่งของสนามเพิ่มขึ้น",
     ("มีเพียงแรงแม่เหล็กที่ลดลงตามระยะห่าง", "ทั้งสามชนิดมีขนาดเพิ่มขึ้นเมื่อระยะห่างเพิ่มขึ้น", "แรงโน้มถ่วงไม่ขึ้นกับระยะห่าง",
      "แรงไฟฟ้ามีขนาดคงที่ทุกระยะ", "ทั้งสามชนิดหายไปทันทีเมื่อไม่สัมผัสกัน")),
    ("นำแม่เหล็กเข้าใกล้คลิปเหล็กมากขึ้นเรื่อย ๆ แรงแม่เหล็กที่กระทำต่อคลิปเป็นอย่างไร", "เพิ่มขึ้น",
     ("ลดลง", "คงที่", "เป็นศูนย์ตลอด", "เพิ่มขึ้นแล้วหายไป", "เปลี่ยนเป็นแรงผลัก")),
    ("ยานอวกาศเดินทางออกห่างจากโลกไปเรื่อย ๆ แรงโน้มถ่วงที่โลกกระทำต่อยานเป็นอย่างไร", "ลดลงแต่ยังไม่เป็นศูนย์",
     ("เพิ่มขึ้น", "คงที่", "เป็นศูนย์ทันทีที่พ้นบรรยากาศ", "เปลี่ยนเป็นแรงผลัก", "เพิ่มขึ้นแล้วลดลง")),
    ("ในการทดลองวัดแรงแม่เหล็กที่ระยะต่าง ๆ ควรกำหนดสิ่งใดเป็นตัวแปรต้น", "ระยะห่างระหว่างแม่เหล็กกับวัตถุ",
     ("ขนาดของแรงแม่เหล็ก", "ชนิดของแม่เหล็ก", "ชนิดของวัตถุที่ถูกดูด", "เวลาในการทดลอง", "สีของแม่เหล็ก")),
    ("ในการทดลองวัดแรงแม่เหล็กที่ระยะต่าง ๆ ควรควบคุมสิ่งใดให้เหมือนกัน", "แม่เหล็กและวัตถุที่ใช้",
     ("ระยะห่าง", "ขนาดของแรงที่วัดได้", "ผลการทดลอง", "จำนวนครั้งที่ต่างกันในแต่ละระยะ", "ทิศของแรงที่วัดได้")),
)


FIELD_DISTANCE_SCENARIOS = (
    ("เหตุใดนักบินอวกาศที่อยู่ห่างจากโลกมาก ๆ จึงรู้สึกเสมือนไร้น้ำหนักมากกว่าตอนอยู่ใกล้โลก",
     "เพราะแรงโน้มถ่วงจากโลกมีขนาดลดลงเมื่อระยะห่างจากโลกเพิ่มขึ้น",
     ("เพราะแรงโน้มถ่วงจากโลกหายไปทันทีที่พ้นบรรยากาศ", "เพราะแรงโน้มถ่วงจากโลกมีขนาดเท่าเดิมทุกระยะ", "เพราะนักบินอวกาศไม่มีมวลอีกต่อไปเมื่อขึ้นไปอยู่ในวงโคจรรอบโลก")),
    ("เหตุใดแม่เหล็กจึงดูดคลิปหนีบกระดาษได้แรงขึ้นเรื่อย ๆ เมื่อเลื่อนเข้าใกล้",
     "ระยะห่างจากแหล่งของสนามลดลง แรงแม่เหล็กจึงมีขนาดเพิ่มขึ้น",
     ("แม่เหล็กมีแรงคงที่ไม่ว่าระยะห่างจะเป็นเท่าใด คลิปจึงถูกดูดได้ทุกระยะ", "ยิ่งเข้าใกล้ แรงแม่เหล็กยิ่งลดลง เพราะคลิปบังเส้นแรงแม่เหล็กไว้", "คลิปหนีบกระดาษมีมวลเพิ่มขึ้นเมื่อเข้าใกล้")),
    ("ลูกโป่งที่ถูกับผมแล้วดูดเศษกระดาษได้ในระยะใกล้ แต่ดูดไม่ได้เมื่อถอยห่างออกไปมาก ข้อใดอธิบายได้ถูกต้อง",
     "แรงไฟฟ้าจากลูกโป่งมีขนาดลดลงมากจนไม่พอดึงเศษกระดาษเมื่อระยะห่างเพิ่มขึ้น",
     ("แรงไฟฟ้าหมดไปเมื่อเวลาผ่านไปเท่านั้น ไม่เกี่ยวกับระยะห่าง", "แรงไฟฟ้ามีขนาดเท่าเดิมทุกระยะ แต่เศษกระดาษมีน้ำหนักมากขึ้นเมื่ออยู่ไกล", "ประจุไฟฟ้าหมดไปจากลูกโป่งทันทีที่ขยับออกห่าง ไม่เกี่ยวกับขนาดของแรงไฟฟ้า")),
    ("เหตุใดเครื่องมือแพทย์ที่เป็นแม่เหล็กแรงสูงจึงต้องกำหนดระยะปลอดภัยห้ามนำวัตถุเหล็กเข้าใกล้",
     "ยิ่งใกล้แม่เหล็ก แรงแม่เหล็กยิ่งมาก วัตถุเหล็กอาจถูกดูดพุ่งเข้าหาอย่างแรงจนเป็นอันตราย",
     ("แรงแม่เหล็กมากที่สุดเมื่ออยู่ไกล วัตถุเหล็กที่อยู่ใกล้จึงไม่ถูกดูดและไม่เป็นอันตราย", "วัตถุเหล็กที่อยู่ใกล้จะร้อนจนละลาย แรงแม่เหล็กไม่เป็นอันตรายแต่ความร้อนเป็นอันตราย", "แรงแม่เหล็กไม่ขึ้นกับระยะห่าง วัตถุเหล็กจึงถูกดูดด้วยแรงเท่ากันทั้งใกล้และไกล")),
    ("ดวงจันทร์มีผลต่อน้ำขึ้นน้ำลงบนโลกมากกว่าดวงอาทิตย์ แม้ดวงอาทิตย์มีมวลมากกว่ามาก ปัจจัยใดช่วยอธิบายได้",
     "ดวงจันทร์อยู่ใกล้โลกมากกว่าดวงอาทิตย์มาก ระยะห่างจึงมีผลต่อแรงที่กระทำอย่างมาก",
     ("ดวงจันทร์มีมวลมากกว่าดวงอาทิตย์มาก แรงโน้มถ่วงของดวงจันทร์จึงมากกว่า", "ดวงอาทิตย์ไม่มีแรงโน้มถ่วงต่อโลก เพราะอยู่ไกลเกินกว่าที่แรงจะไปถึงได้", "น้ำทะเลเป็นแม่เหล็ก ดวงจันทร์จึงดึงน้ำทะเลด้วยแรงแม่เหล็กที่มากกว่าแรงโน้มถ่วง")),
)


@question_type(
    "phys.field_distance_foundation",
    display_name={"th": "บอกแนวโน้มของแรงจากสนามเมื่อระยะห่างเปลี่ยนไป"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FIELD_DISTANCE_TOPIC,
)
class FieldDistanceFoundation(QuestionType):
    """How a field's force changes with distance, in general or for two named objects."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.3:
            return _facts(rng, FIELD_DISTANCE_FACTS, hint=FIELD_DISTANCE_HINT, topic=FIELD_DISTANCE_TOPIC)
        if roll < 0.8:
            field, source, things = rng.choice(FIELD_SOURCES)
            thing = rng.choice(things)
            unit = "กิโลเมตร" if field == "แรงโน้มถ่วง" else "เซนติเมตร"
            steps = range(400, 4001, 200) if field == "แรงโน้มถ่วง" else range(1, 21)
            a, b = rng.sample(steps, 2)
            near = "ก" if a < b else "ข"
            return _labelled(
                stem=(f"{thing} ก อยู่ห่างจาก{source} {a} {unit} {thing} ข ซึ่งเหมือนกันทุกประการอยู่ห่าง {b} {unit} "
                      f"{thing}ชิ้นใดได้รับ{field}มากกว่า"),
                correct=f"{thing} {near} เพราะอยู่ใกล้แหล่งของสนามมากกว่า",
                wrongs=(f"{thing} {'ข' if near == 'ก' else 'ก'} เพราะอยู่ไกลแหล่งของสนามมากกว่า",
                        f"เท่ากัน เพราะเป็น{thing}ที่เหมือนกัน",
                        f"{thing} {'ข' if near == 'ก' else 'ก'} เพราะอยู่ใกล้แหล่งของสนามมากกว่า"),
                hint=FIELD_DISTANCE_HINT, topic=FIELD_DISTANCE_TOPIC,
            )
        field = rng.choice(FIELD_NAMES)
        return _labelled(
            stem=f"เมื่อวัตถุอยู่ห่างจากแหล่งของสนามที่ทำให้เกิด{field}มากขึ้น {field}ที่วัตถุได้รับจะเป็นอย่างไร",
            correct="มีขนาดลดลง",
            wrongs=("มีขนาดเพิ่มขึ้น", "มีขนาดคงที่ไม่เปลี่ยนแปลง", "ไม่มีแรงกระทำอีกต่อไปทันที"),
            hint="ยิ่งอยู่ห่างจากแหล่งของสนามมาก แรงที่ได้รับยิ่งน้อยลง ไม่ว่าจะเป็นสนามชนิดใด",
            topic=FIELD_DISTANCE_TOPIC,
        )


@question_type(
    "phys.field_distance_fluency",
    display_name={"th": "วิเคราะห์ความสัมพันธ์ระหว่างขนาดของแรงกับระยะห่างจากข้อมูลที่รวบรวมได้"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FIELD_DISTANCE_TOPIC,
)
class FieldDistanceFluency(QuestionType):
    """A record of force at three distances, always falling; the relationship it shows."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        field = rng.choice(FIELD_NAMES)
        distances = sorted(rng.sample(range(5, 41, 5), 3))
        forces = sorted((rng.sample(range(2, 21), 3)), reverse=True)
        record = " / ".join(f"ระยะ {d} เซนติเมตร: แรง {f} นิวตัน" for d, f in zip(distances, forces))
        return _labelled(
            stem=(f"นักเรียนวัด{field}ที่กระทำต่อวัตถุ เมื่อวัตถุอยู่ห่างจากแหล่งของสนามระยะต่าง ๆ ได้ผลดังนี้ — {record} "
                  f"จากข้อมูลนี้ ข้อใดวิเคราะห์ความสัมพันธ์ระหว่างขนาดของ{field}กับระยะห่างจากแหล่งของสนามได้ถูกต้อง"),
            correct=f"ยิ่งระยะห่างจากแหล่งของสนามมากขึ้น {field}ยิ่งมีขนาดลดลง",
            wrongs=(f"ยิ่งระยะห่างจากแหล่งของสนามมากขึ้น {field}ยิ่งมีขนาดเพิ่มขึ้น",
                    f"ระยะห่างจากแหล่งของสนามไม่มีผลต่อขนาดของ{field}",
                    f"{field}มีค่าคงที่ไม่ว่าระยะห่างจะเป็นเท่าใด",
                    f"ยิ่งระยะห่างจากแหล่งของสนามน้อยลง {field}ยิ่งมีขนาดลดลง",
                    f"ยิ่งระยะห่างจากแหล่งของสนามน้อยลง {field}ยิ่งมีขนาดคงที่"),
            hint="เรียงระยะจากน้อยไปมาก แล้วดูว่าแรงที่วัดได้เปลี่ยนไปในทิศทางใด",
            topic=FIELD_DISTANCE_TOPIC,
        )


@question_type(
    "phys.field_distance_application",
    display_name={"th": "ใช้ความสัมพันธ์ระหว่างแรงกับระยะห่างอธิบายสถานการณ์"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FIELD_DISTANCE_TOPIC,
)
class FieldDistanceApplication(QuestionType):
    """Authored cases, and predicting a reading beyond a falling record."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            field = rng.choice(FIELD_NAMES[:2])  # a bench can measure these two over centimetres
            distances = sorted(rng.sample(range(2, 31, 2), 4))
            forces = sorted(rng.sample(range(3, 41), 3), reverse=True)
            record = " / ".join(f"ระยะ {d} เซนติเมตร: {f} นิวตัน" for d, f in zip(distances, forces))
            last = forces[-1]
            return _labelled(
                stem=(f"นักเรียนวัด{field}ที่ระยะต่าง ๆ ได้ — {record} ถ้าวัดที่ระยะ {distances[3]} เซนติเมตร "
                      "ควรได้ค่าประมาณเท่าใด"),
                correct=f"น้อยกว่า {last} นิวตัน เพราะอยู่ไกลกว่าทุกระยะที่วัดมา",
                wrongs=(f"มากกว่า {forces[0]} นิวตัน เพราะยิ่งไกลแรงยิ่งมากขึ้น", f"เท่ากับ {last} นิวตันพอดี เพราะยิ่งไกลแรงก็ไม่ลดลงอีก",
                        f"อยู่ระหว่าง {last} กับ {forces[0]} นิวตัน ซึ่งเป็นช่วงกลางของข้อมูล"),
                hint="ข้อมูลแสดงว่าแรงลดลงเมื่อระยะเพิ่มขึ้น ระยะที่ไกลกว่าทุกค่าจึงควรได้แรงน้อยกว่าค่าที่น้อยที่สุด",
                topic=FIELD_DISTANCE_TOPIC,
            )
        return _retopic(scenario_question(
            rng, FIELD_DISTANCE_SCENARIOS,
            hint="แรงจากสนามทั้งสามชนิดมีขนาดลดลงเมื่อระยะห่างจากแหล่งของสนามเพิ่มขึ้น",
        ), FIELD_DISTANCE_TOPIC)
