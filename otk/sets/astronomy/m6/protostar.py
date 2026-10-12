"""กระบวนการเกิดดาวฤกษ์

ดาราศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/4

Sets moved here from: science_wave_f82.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f82 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_PROTO = "กระบวนการเกิดดาวฤกษ์"


STAGES = ("เนบิวลา", "เนบิวลายุบตัวเป็นก้อน", "ดาวฤกษ์ก่อนเกิด (โปรโตสตาร์)", "ดาวฤกษ์ก่อนลำดับหลัก", "ดาวฤกษ์ในลำดับหลัก")


PROTO_FACTS = (
    ("เนบิวลาที่เป็นต้นกำเนิดของดาวฤกษ์ประกอบด้วยอะไรเป็นส่วนใหญ่", "แก๊สไฮโดรเจนและฝุ่น",
     ("เหล็กและนิกเกิล", "ฝุ่นเหล็กและนิกเกิล", "คาร์บอนไดออกไซด์", "หินและเหล็กร้อน")),
    ("แรงใดทำให้เนบิวลายุบตัวลงเป็นดาวฤกษ์ก่อนเกิด", "แรงโน้มถ่วงระหว่างมวลของแก๊สและฝุ่น",
     ("แรงหนีศูนย์กลางจากการหมุนของเนบิวลา", "แรงผลักทางไฟฟ้าระหว่างอนุภาคของแก๊ส", "แรงเสียดทานของลมสุริยะเท่านั้น", "แรงผลักจากหลุมดำทุกกรณี")),
    ("ขณะดาวฤกษ์ก่อนเกิดยุบตัว อุณหภูมิที่แกนสูงขึ้นเพราะเหตุใด", "พลังงานศักย์โน้มถ่วงเปลี่ยนเป็นพลังงานความร้อน",
     ("เกิดฟิวชันไฮโดรเจนตั้งแต่เริ่มยุบตัว", "ได้รับความร้อนจากดวงอาทิตย์", "เกิดปฏิกิริยาเคมีเผาไหม้ของไฮโดรเจนกับออกซิเจน", "เกิดฟิวชันไฮโดรเจนที่แกนตั้งแต่เริ่มยุบตัวครั้งแรก")),
    ("ดาวฤกษ์ก่อนเกิดกลายเป็นดาวฤกษ์เมื่อใด", "เมื่ออุณหภูมิที่แกนสูงพอให้เกิดฟิวชันไฮโดรเจนเป็นฮีเลียม",
     ("เมื่อเริ่มสะท้อนแสงจากดาวข้างเคียงจนสว่างเท่าดาวฤกษ์", "เมื่อมีดาวเคราะห์เกิดขึ้นและโคจรรอบแกนที่ยุบตัวแล้ว", "เมื่อหยุดหมุนรอบตัวเองและแรงโน้มถ่วงหายไปทั้งหมด", "เมื่อเย็นลงจนต่ำกว่า 0 °C")),
    ("ดาวฤกษ์ในลำดับหลักมีขนาดคงที่ได้เพราะเหตุใด", "แรงดันจากแก๊สร้อนและรังสีภายในสมดุลกับแรงโน้มถ่วง",
     ("แรงโน้มถ่วงหายไป เพราะแก๊สร้อนจนเบากว่าเดิม", "ไม่มีการสร้างพลังงานแล้ว แรงทั้งหมดจึงเป็นศูนย์", "แรงแม่เหล็กดึงผิวดาวออก", "ดาวหยุดหมุนรอบตัวเอง จึงไม่มีแรงเหวี่ยงออก")),
    ("เหตุใดดาวฤกษ์ก่อนเกิดจึงสังเกตได้ยากด้วยแสงที่ตามองเห็น แต่สังเกตได้ด้วยรังสีอินฟราเรด", "ถูกฝุ่นหนาในเนบิวลาบัง แต่อินฟราเรดทะลุฝุ่นได้ดีกว่า",
     ("ดาวฤกษ์ก่อนเกิดไม่ปล่อยพลังงานใดเลยจนกว่าจะเกิดฟิวชัน", "ดาวฤกษ์ก่อนเกิดร้อนกว่าดวงอาทิตย์หลายล้านเท่า", "แสงที่ตามองเห็นเดินทางช้ากว่าอินฟราเรด", "ดาวฤกษ์ก่อนเกิดอยู่ใกล้เกินไป แสงจึงจ้าจนกล้องรับไม่ได้")),
    ("ก้อนแก๊สที่มีมวลน้อยเกินไปจนแกนร้อนไม่พอเกิดฟิวชันไฮโดรเจนจะกลายเป็นวัตถุใด", "ดาวแคระน้ำตาล",
     ("ดาวยักษ์แดง", "ซูเปอร์โนวา", "ดาวนิวตรอน", "ดาวฤกษ์มวลมาก")),
)


PROTO_HINT = ("เนบิวลายุบตัวด้วยแรงโน้มถ่วง → ดาวฤกษ์ก่อนเกิด ขนาดเล็กลง ความดันและอุณหภูมิสูงขึ้นจากพลังงานศักย์โน้มถ่วง "
              "→ แกนร้อนพอเกิดฟิวชันไฮโดรเจน → ดาวฤกษ์ในลำดับหลัก ที่แรงดันสมดุลกับแรงโน้มถ่วง")


@question_type(
    "astro.protostar_foundation",
    display_name={"th": "จากเนบิวลาสู่ดาวฤกษ์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PROTO,
)
class ProtostarFoundation(QuestionType):
    """Nebula, collapse, heating, ignition, balance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(PROTO_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_PROTO, hint=PROTO_HINT)


@question_type(
    "astro.protostar_fluency",
    display_name={"th": "การเปลี่ยนแปลงความดัน อุณหภูมิ และขนาดระหว่างการเกิดดาวฤกษ์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PROTO,
)
class ProtostarFluency(QuestionType):
    """Order of stages; which way size, pressure and temperature go."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            picked = sorted(rng.sample(range(len(STAGES)), 4))
            order = tuple(STAGES[i] for i in picked)
            perms = [p for p in permutations(order) if p != order]
            return _labelled(stem="ข้อใดเรียงลำดับขั้นการเกิดดาวฤกษ์จากก่อนไปหลังได้ถูกต้อง", correct=" → ".join(order),
                             wrongs=tuple(" → ".join(p) for p in rng.sample(perms, 3)), topic=TOPIC_PROTO, hint=PROTO_HINT)
        if rng.random() < 0.5:
            i = rng.randrange(len(STAGES) - 1)
            nxt = rng.random() < 0.5 or i == 0
            if nxt:
                right = STAGES[i + 1]
                wrongs = [s for s in STAGES if s not in (right, STAGES[i])]
                return _labelled(stem=f"ในกระบวนการเกิดดาวฤกษ์ ขั้นถัดจาก\"{STAGES[i]}\"คือขั้นใด", correct=right,
                                 wrongs=tuple(wrongs), topic=TOPIC_PROTO, hint=PROTO_HINT)
            right = STAGES[i - 1]
            wrongs = [s for s in STAGES if s not in (right, STAGES[i])]
            return _labelled(stem=f"ในกระบวนการเกิดดาวฤกษ์ ขั้นก่อน\"{STAGES[i]}\"คือขั้นใด", correct=right,
                             wrongs=tuple(wrongs), topic=TOPIC_PROTO, hint=PROTO_HINT)
        prop = rng.choice(("ขนาด", "ความดันที่แกน", "อุณหภูมิที่แกน", "ความหนาแน่น"))
        right = "ลดลง" if prop == "ขนาด" else "เพิ่มขึ้น"
        return _labelled(stem=f"ขณะเนบิวลายุบตัวจนเป็นดาวฤกษ์ก่อนเกิด {prop}เปลี่ยนแปลงอย่างไร", correct=right,
                         wrongs=tuple(o for o in ("เพิ่มขึ้น", "ลดลง", "คงที่", "เพิ่มขึ้นแล้วลดลงเป็นศูนย์") if o != right),
                         topic=TOPIC_PROTO, hint=PROTO_HINT)


@question_type(
    "astro.protostar_application",
    display_name={"th": "คำนวณความหนาแน่นเมื่อยุบตัวและอุณหภูมิในหน่วยเคลวิน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PROTO,
)
class ProtostarApplication(QuestionType):
    """Same mass, radius shrinks k times, density grows k³; K = °C + 273."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            k = rng.randint(2, 10)
            if rng.random() < 0.5:
                return numeric(stem=f"ก้อนแก๊สมวลคงที่ยุบตัวจนรัศมีลดลงเหลือ 1/{k} ของเดิม ความหนาแน่นเฉลี่ยเพิ่มขึ้นกี่เท่า",
                               answer=k ** 3, wrongs=[k, k ** 2, 3 * k], unit="เท่า", topic=TOPIC_PROTO,
                               hint="ความหนาแน่น = มวล ÷ ปริมาตร ปริมาตรแปรตามรัศมีกำลังสาม")
            return numeric(stem=f"ก้อนแก๊สมวลคงที่ยุบตัวจนความหนาแน่นเฉลี่ยเพิ่มขึ้น {k ** 3} เท่า รัศมีลดลงกี่เท่า",
                           answer=k, wrongs=[k ** 2, k ** 3, k + 1], unit="เท่า", topic=TOPIC_PROTO,
                           hint="รัศมีลดลง k เท่า ความหนาแน่นเพิ่ม k³ เท่า")
        if roll < 0.7:
            celsius = rng.choice((-263, -253, -243, -223, -173, 727, 1727, 2727, 9727))
            return numeric(stem=f"แก๊สในเนบิวลาบริเวณหนึ่งมีอุณหภูมิ {show(celsius)} °C คิดเป็นกี่เคลวิน (K = °C + 273)",
                           answer=celsius + 273, wrongs=[abs(celsius - 273), abs(celsius), celsius + 373 if celsius + 373 > 0 else 1], unit="K",
                           topic=TOPIC_PROTO, hint="K = °C + 273")
        suns = rng.choice((10, 20, 50, 100, 200, 500, 1000))
        share = rng.choice((1, 2, 5, 10, 20, 25, 30))
        return numeric(stem=f"เนบิวลามวล {show(suns)} เท่าของดวงอาทิตย์ ถ้าร้อยละ {share} ของมวลกลายเป็นดาวฤกษ์ จะได้มวลดาวฤกษ์รวมกี่เท่าของดวงอาทิตย์",
                       answer=Fraction(suns * share, 100), wrongs=[suns - Fraction(suns * share, 100), share, Fraction(suns * share, 10)],
                       unit="เท่าของดวงอาทิตย์", topic=TOPIC_PROTO, hint="มวลดาวฤกษ์ = มวลเนบิวลา × ร้อยละ ÷ 100")
