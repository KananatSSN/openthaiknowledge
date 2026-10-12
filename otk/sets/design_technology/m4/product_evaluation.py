"""การประเมินผลและการพัฒนาต่อยอด

การออกแบบและเทคโนโลยี · ม.4 · สสวท. พื้นฐาน
Indicators: ว 4.1 ม.4/4

Sets moved here from: technology_t2s4.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1 import SUBJECT
from otk.sets._support.technology_t1s4 import _near
from otk.sets._support.technology_t2s3 import _pair_either_way
from otk.sets._support.technology_t2s4 import M4

PROVENANCE = Provenance("original")


EVALUATE_TOPIC = "การประเมินผลและการพัฒนาต่อยอด"


RUBRIC = ("ความแข็งแรง", "การใช้งานสะดวก", "ความประหยัด", "ความปลอดภัย")


EXTENSIONS = (
    ("ระบบรดน้ำอัตโนมัติที่ผู้ใช้ต้องเดินไปดูว่าน้ำในถังหมดหรือยัง",
     "เพิ่มเซนเซอร์วัดระดับน้ำในถังและแจ้งเตือนผ่านโทรศัพท์"),
    ("ชั้นวางรองเท้าที่ผู้ใช้บอกว่าย้ายตำแหน่งยากเพราะหนัก",
     "ติดล้อที่ล็อกได้ใต้ชั้นวาง"),
    ("กล่องแยกยาที่ผู้สูงอายุมักลืมเวลากินยา",
     "เพิ่มนาฬิกาที่ส่งเสียงเตือนตามมื้อยา"),
    ("โคมไฟตั้งโต๊ะที่ต้องเปลี่ยนถ่านบ่อย",
     "เปลี่ยนเป็นแบตเตอรี่ชาร์จได้พร้อมช่องชาร์จ"),
    ("ที่ให้อาหารสัตว์เลี้ยงที่ให้อาหารได้วันละครั้งเท่านั้น",
     "เพิ่มตัวตั้งเวลาให้แบ่งอาหารได้หลายมื้อต่อวัน"),
    ("ถังขยะแยกประเภทที่ส่งกลิ่นเมื่อมีขยะเศษอาหาร",
     "เพิ่มฝาปิดแบบเหยียบเปิดและช่องใส่ถุงดับกลิ่น"),
    ("ที่ชาร์จโทรศัพท์พลังงานแสงอาทิตย์ที่ใช้ไม่ได้ในวันฝนตก",
     "เพิ่มแบตเตอรี่สำรองเพื่อเก็บพลังงานไว้ใช้ในวันที่ไม่มีแดด"),
    ("ราวตากผ้าที่ผ้าเปียกเมื่อฝนตกกะทันหัน",
     "เพิ่มเซนเซอร์ตรวจฝนและกลไกดึงราวเข้าที่ร่ม"),
)


@question_type(
    "tech.product_evaluation_foundation",
    display_name={"th": "ประเมินชิ้นงานด้วยเกณฑ์การให้คะแนน"},
    level=M4, subject=SUBJECT, topic=EVALUATE_TOPIC,
)
class ProductEvaluationFoundation(QuestionType):
    def build(self, rng: Random, **params):
        # An even total keeps the percentage whole (total × 100 ÷ 40), and a
        # single lowest score keeps "which side first" to one answer.
        while True:
            scores = [rng.randint(3, 10) for _ in RUBRIC]
            if sum(scores) % 2 == 0 and scores.count(min(scores)) == 1:
                break
        listed = " ".join(f"{c} {s}" for c, s in zip(RUBRIC, scores))
        if rng.random() < 0.5:
            percent = sum(scores) * 100 // 40
            return _labelled(
                stem=f"ชิ้นงานได้คะแนนจากเกณฑ์ละ 10 คะแนน ดังนี้ {listed} คะแนนรวมคิดเป็นร้อยละเท่าใด",
                correct=f"ร้อยละ {percent}",
                wrongs=tuple(f"ร้อยละ {w}" for w in rng.sample(
                    _near(percent, (sum(scores), sum(scores) * 10, percent + 5, percent - 10)), 3)),
                hint="รวมคะแนนทุกเกณฑ์ แล้วหารด้วยคะแนนเต็มรวม 40 คูณ 100",
                topic=EVALUATE_TOPIC,
            )
        weakest = RUBRIC[scores.index(min(scores))]
        return _labelled(
            stem=f"ชิ้นงานได้คะแนนจากเกณฑ์ละ 10 คะแนน ดังนี้ {listed} ควรพัฒนาชิ้นงานในด้านใดเป็นอันดับแรก",
            correct=weakest, wrongs=tuple(c for c in RUBRIC if c != weakest),
            hint="ด้านที่ควรพัฒนาก่อนคือด้านที่ได้คะแนนต่ำที่สุด",
            topic=EVALUATE_TOPIC,
        )


@question_type(
    "tech.product_evaluation_fluency",
    display_name={"th": "เสนอแนวทางการพัฒนาต่อยอดชิ้นงาน"},
    level=M4, subject=SUBJECT, topic=EVALUATE_TOPIC,
)
class ProductEvaluationFluency(QuestionType):
    def build(self, rng: Random, **params):
        return _pair_either_way(rng, EXTENSIONS,
                                forward="ผลการประเมินพบว่า{} แนวทางพัฒนาต่อยอดใดตรงกับปัญหาที่พบมากที่สุด",
                                backward="แนวทางพัฒนาต่อยอด “{}” ตอบข้อบกพร่องของชิ้นงานใด",
                                hint="การพัฒนาต่อยอดที่ดีตอบข้อบกพร่องหรือความต้องการที่พบจากการประเมินโดยตรง",
                                topic=EVALUATE_TOPIC)


@question_type(
    "tech.product_evaluation_application",
    display_name={"th": "เปรียบเทียบความสม่ำเสมอของผลการทดสอบ"},
    level=M4, subject=SUBJECT, topic=EVALUATE_TOPIC,
)
class ProductEvaluationApplication(QuestionType):
    """Two designs, four runs each: the higher mean, or the smaller range."""

    def build(self, rng: Random, **params):
        while True:
            a = [rng.randint(40, 90) for _ in range(4)]
            b = [rng.randint(40, 90) for _ in range(4)]
            if (sum(a) % 4 == 0 and sum(b) % 4 == 0 and sum(a) != sum(b)
                    and max(a) - min(a) != max(b) - min(b)):
                break
        listed = (f"แบบ ก ได้ {' '.join(map(str, a))} แบบ ข ได้ {' '.join(map(str, b))}")
        choices = ("แบบ ก", "แบบ ข", "ทั้งสองแบบเท่ากัน", "ข้อมูลไม่พอที่จะสรุป")
        if rng.random() < 0.5:
            correct = choices[0] if max(a) - min(a) < max(b) - min(b) else choices[1]
            stem = (f"ทดสอบรถของเล่นสองแบบ แบบละ 4 ครั้ง ระยะทาง (เซนติเมตร) {listed} "
                    f"แบบใดให้ผลสม่ำเสมอกว่า เมื่อดูจากพิสัย (ค่ามากสุดลบค่าน้อยสุด)")
            hint = "พิสัยน้อยกว่าหมายความว่าผลแต่ละครั้งใกล้เคียงกันมากกว่า"
        else:
            correct = choices[0] if sum(a) > sum(b) else choices[1]
            stem = (f"ทดสอบรถของเล่นสองแบบ แบบละ 4 ครั้ง ระยะทาง (เซนติเมตร) {listed} "
                    f"แบบใดมีระยะทางเฉลี่ยมากกว่า")
            hint = "ค่าเฉลี่ยคือผลรวมหารด้วยจำนวนครั้ง จำนวนครั้งเท่ากันจึงเทียบผลรวมได้เลย"
        return _labelled(stem=stem, correct=correct, wrongs=tuple(c for c in choices if c != correct),
                         hint=hint, topic=EVALUATE_TOPIC)
