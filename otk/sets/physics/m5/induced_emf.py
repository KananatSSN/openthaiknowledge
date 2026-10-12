"""การเกิดอีเอ็มเอฟเหนี่ยวนำและการนำไปใช้ประโยชน์

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.5/9

Sets moved here from: science_wave_e12.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e12 import SUBJECT, UPPER_FIVE, _labelled

PROVENANCE = Provenance("original")


TOPIC_EMF = "การเกิดอีเอ็มเอฟเหนี่ยวนำและการนำไปใช้ประโยชน์"


EMF_USES = (
    ("เครื่องกำเนิดไฟฟ้าในโรงไฟฟ้า", True),
    ("หม้อแปลงไฟฟ้า", True),
    ("เตาแม่เหล็กไฟฟ้า (เตาเหนี่ยวนำ)", True),
    ("ไดนาโมจักรยานที่ทำให้ไฟหน้าติด", True),
    ("เครื่องชาร์จโทรศัพท์แบบไร้สาย", True),
    ("เครื่องอ่านบัตรแถบแม่เหล็ก", True),
    ("ไมโครโฟนแบบขดลวดเคลื่อนที่", True),
)


NOT_EMF_USES = (
    "ถ่านไฟฉายที่ให้พลังงานไฟฟ้าจากปฏิกิริยาเคมี",
    "เซลล์สุริยะที่เปลี่ยนแสงเป็นไฟฟ้า",
    "กาต้มน้ำไฟฟ้าที่ใช้ขดลวดความร้อน",
    "หลอดไฟไส้ที่ร้อนจนเปล่งแสง",
    "แท่งแก้วที่ถูกผ้าไหมแล้วดูดเศษกระดาษ",
)


EMF_SITUATIONS = (
    ("ไฟหน้าจักรยานที่ต่อกับไดนาโมสว่างขึ้นเมื่อปั่นเร็วขึ้น",
     "ไดนาโมหมุนเร็วขึ้น สนามแม่เหล็กผ่านขดลวดเปลี่ยนเร็วขึ้น อีเอ็มเอฟเหนี่ยวนำจึงมากขึ้น"),
    ("เมื่อจักรยานจอดนิ่ง ไฟหน้าที่ต่อกับไดนาโมดับ",
     "ไดนาโมไม่หมุน สนามแม่เหล็กผ่านขดลวดไม่เปลี่ยน จึงไม่เกิดอีเอ็มเอฟเหนี่ยวนำ"),
    ("เตาแม่เหล็กไฟฟ้าทำให้หม้อเหล็กร้อนโดยตัวเตาไม่ร้อนมาก",
     "สนามแม่เหล็กที่เปลี่ยนตลอดเวลาเหนี่ยวนำกระแสไฟฟ้าในก้นหม้อ หม้อจึงร้อน"),
    ("เครื่องกำเนิดไฟฟ้าในเขื่อนผลิตไฟฟ้าได้เมื่อน้ำไหลผ่านกังหัน",
     "กังหันหมุนขดลวดในสนามแม่เหล็ก สนามแม่เหล็กผ่านขดลวดเปลี่ยน จึงเกิดอีเอ็มเอฟเหนี่ยวนำ"),
)


EMF_SITUATION_WRONG = (
    "ความร้อนจากการเสียดสีเปลี่ยนเป็นไฟฟ้าโดยตรง",
    "แม่เหล็กถาวรปล่อยอิเล็กตรอนออกมาเป็นกระแสไฟฟ้า",
    "ขดลวดเก็บประจุไฟฟ้าไว้แล้วปล่อยออกมาทีหลัง",
)


EMF_YES = (
    "เลื่อนแท่งแม่เหล็กเข้าไปในขดลวด",
    "ดึงแท่งแม่เหล็กออกจากขดลวด",
    "เลื่อนขดลวดเข้าหาแท่งแม่เหล็กที่วางนิ่ง",
    "หมุนขดลวดในสนามแม่เหล็ก",
    "เปิดหรือปิดสวิตช์ของขดลวดอีกขดที่วางอยู่ใกล้ ๆ",
)


EMF_NO = (
    "วางแท่งแม่เหล็กนิ่งไว้ในขดลวด",
    "วางแท่งแม่เหล็กนิ่งไว้ข้างขดลวด",
    "เลื่อนแท่งแม่เหล็กและขดลวดไปพร้อมกันด้วยความเร็วเท่ากัน",
    "วางขดลวดไว้ใกล้แท่งพลาสติกที่ไม่มีสนามแม่เหล็ก",
)


@question_type(
    "phys.induced_emf_foundation",
    display_name={"th": "ตัวอย่างการนำอีเอ็มเอฟเหนี่ยวนำไปใช้ประโยชน์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EMF,
)
class InducedEmfFoundation(QuestionType):
    """The second outcome, ยกตัวอย่าง: which devices put induced emf to use."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        uses = [u for u, _ in EMF_USES]
        if rng.random() < 0.6:
            return _labelled(
                stem="อุปกรณ์ใดทำงานโดยอาศัยการเกิดอีเอ็มเอฟเหนี่ยวนำ",
                correct=rng.choice(uses), wrongs=tuple(NOT_EMF_USES),
                topic=TOPIC_EMF,
                hint="อีเอ็มเอฟเหนี่ยวนำเกิดเมื่อสนามแม่เหล็กที่ผ่านขดลวดเปลี่ยนแปลง ไม่ใช่จากปฏิกิริยาเคมี แสง หรือความร้อน")
        return _labelled(
            stem="อุปกรณ์ใดไม่ได้ทำงานโดยอาศัยการเกิดอีเอ็มเอฟเหนี่ยวนำ",
            correct=rng.choice(NOT_EMF_USES), wrongs=tuple(uses),
            topic=TOPIC_EMF,
            hint="มองหาอุปกรณ์ที่ได้ไฟฟ้าจากปฏิกิริยาเคมี แสง ความร้อน หรือการขัดถู แทนการเปลี่ยนสนามแม่เหล็ก")


@question_type(
    "phys.induced_emf_fluency",
    display_name={"th": "อธิบายการเกิดอีเอ็มเอฟเหนี่ยวนำ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EMF,
)
class InducedEmfFluency(QuestionType):
    """The first outcome, อธิบายการเกิดอีเอ็มเอฟ: when a coil gets an emf, and why."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "อีเอ็มเอฟเหนี่ยวนำเกิดเมื่อสนามแม่เหล็ก (ฟลักซ์แม่เหล็ก) ที่ผ่านขดลวดเปลี่ยนแปลง"
        shape = rng.random()
        if shape < 0.4:
            return _labelled(
                stem="ขดลวดต่อกับแกลแวนอมิเตอร์ กรณีใดเข็มของแกลแวนอมิเตอร์เบน",
                correct=rng.choice(EMF_YES), wrongs=tuple(EMF_NO),
                topic=TOPIC_EMF, hint=hint)
        if shape < 0.7:
            return _labelled(
                stem="ขดลวดต่อกับแกลแวนอมิเตอร์ กรณีใดเข็มของแกลแวนอมิเตอร์ไม่เบน",
                correct=rng.choice(EMF_NO), wrongs=tuple(EMF_YES),
                topic=TOPIC_EMF, hint=hint)
        return _labelled(
            stem="ข้อใดอธิบายการเกิดอีเอ็มเอฟเหนี่ยวนำในขดลวดได้ถูกต้อง",
            correct="เกิดเมื่อสนามแม่เหล็กที่ผ่านขดลวดเปลี่ยนแปลง เช่น เมื่อแม่เหล็กหรือขดลวดเคลื่อนที่สัมพัทธ์กัน",
            wrongs=("เกิดเมื่อมีแม่เหล็กอยู่ใกล้ขดลวด แม้จะวางนิ่งอยู่",
                    "เกิดเมื่อขดลวดร้อนขึ้นจนอิเล็กตรอนเคลื่อนที่",
                    "เกิดเมื่อขดลวดทำจากโลหะที่เป็นแม่เหล็กเท่านั้น"),
            topic=TOPIC_EMF, hint=hint)


@question_type(
    "phys.induced_emf_application",
    display_name={"th": "ทำนายและเพิ่มอีเอ็มเอฟเหนี่ยวนำในสถานการณ์จริง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EMF,
)
class InducedEmfApplication(QuestionType):
    """Make the emf larger, reverse it, and reason about a generator and a transformer."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(5)
        if shape == 3:
            n_p = rng.choice((100, 200, 250, 400, 500, 1000))
            ratio = Fraction(rng.choice((1, 1, 2, 5, 10)), rng.choice((1, 2, 4, 5, 10, 20)))
            if ratio == 1:
                ratio = Fraction(1, 2)
            n_s = n_p * ratio
            if n_s.denominator != 1:
                n_p, n_s = n_p * ratio.denominator, n_p * ratio.numerator
            v_p = rng.choice((220, 240, 100, 120))
            v_s = Fraction(v_p) * Fraction(n_s) / Fraction(n_p)
            seen = [v_s]
            for w in (Fraction(v_p) * Fraction(n_p) / Fraction(n_s), Fraction(v_p), v_s * 2, v_s / 2,
                      v_s * 10, v_s / 10):
                if w not in seen and w > 0:
                    seen.append(w)

            def n(x):
                return f"{float(x):g}"
            return GeneratedQuestion(
                stem=[text(f"หม้อแปลงไฟฟ้ามีขดลวดปฐมภูมิ {int(n_p)} รอบ และขดลวดทุติยภูมิ {int(n_s)} รอบ "
                           f"ต่อขดลวดปฐมภูมิกับไฟฟ้ากระแสสลับ {v_p} โวลต์ ความต่างศักย์ที่ขดลวดทุติยภูมิเท่าใด "
                           "(ถือว่าหม้อแปลงมีประสิทธิภาพ 100%)")],
                correct=[text(f"{n(v_s)} โวลต์")],
                distractors=fixed(*[[text(f"{n(w)} โวลต์")] for w in seen[1:]]),
                topic=TOPIC_EMF,
                hint=[text("อัตราส่วนความต่างศักย์เท่ากับอัตราส่วนจำนวนรอบ: Vs/Vp = Ns/Np")])
        if shape == 4:
            situation, correct = rng.choice(EMF_SITUATIONS)
            return _labelled(
                stem=f"\"{situation}\" ข้อใดอธิบายได้ถูกต้อง",
                correct=correct,
                wrongs=tuple([w for s_, w in EMF_SITUATIONS if w != correct] + list(EMF_SITUATION_WRONG)),
                topic=TOPIC_EMF,
                hint="ถามว่าสนามแม่เหล็กที่ผ่านขดลวดเปลี่ยนเร็วขึ้น ช้าลง หรือไม่เปลี่ยน")
        if shape == 0:
            correct = rng.choice(("เลื่อนแท่งแม่เหล็กเร็วขึ้น", "ใช้แท่งแม่เหล็กที่มีสนามแม่เหล็กแรงขึ้น",
                                  "เพิ่มจำนวนรอบของขดลวด"))
            return _labelled(
                stem="นักเรียนเลื่อนแท่งแม่เหล็กเข้าไปในขดลวดแล้วเข็มแกลแวนอมิเตอร์เบนเล็กน้อย วิธีใดทำให้เข็มเบนมากขึ้น",
                correct=correct,
                wrongs=("เลื่อนแท่งแม่เหล็กช้าลง", "ลดจำนวนรอบของขดลวด",
                        "วางแท่งแม่เหล็กนิ่งไว้ในขดลวดนานขึ้น"),
                topic=TOPIC_EMF,
                hint="สนามแม่เหล็กที่ผ่านขดลวดยิ่งเปลี่ยนเร็วและยิ่งมาก และขดลวดยิ่งมีหลายรอบ อีเอ็มเอฟยิ่งมาก")
        if shape == 1:
            return _labelled(
                stem="เลื่อนแท่งแม่เหล็กเข้าไปในขดลวดแล้วเข็มแกลแวนอมิเตอร์เบนไปทางขวา ถ้าดึงแท่งแม่เหล็กออกจะเป็นอย่างไร",
                correct="เข็มเบนไปทางซ้าย เพราะสนามแม่เหล็กที่ผ่านขดลวดเปลี่ยนในทางตรงข้าม",
                wrongs=("เข็มเบนไปทางขวาเหมือนเดิม เพราะใช้แม่เหล็กแท่งเดิม",
                        "เข็มไม่เบนเลย เพราะแม่เหล็กออกจากขดลวดแล้วไม่มีการเปลี่ยนฟลักซ์",
                        "เข็มเบนไปทางขวามากขึ้น เพราะแม่เหล็กเคลื่อนที่อีกครั้ง"),
                topic=TOPIC_EMF,
                hint="ทิศของอีเอ็มเอฟขึ้นกับว่าสนามแม่เหล็กที่ผ่านขดลวดเพิ่มขึ้นหรือลดลง")
        return _labelled(
            stem="เหตุใดหม้อแปลงไฟฟ้าจึงใช้กับไฟฟ้ากระแสสลับได้ แต่ใช้แปลงแรงดันไฟฟ้ากระแสตรงที่คงตัวไม่ได้",
            correct="กระแสสลับทำให้สนามแม่เหล็กในแกนเปลี่ยนตลอด จึงเหนี่ยวนำอีเอ็มเอฟในขดลวดทุติยภูมิ",
            wrongs=("กระแสตรงมีพลังงานน้อยเกินกว่าจะผ่านหม้อแปลง",
                    "กระแสตรงไม่ทำให้เกิดสนามแม่เหล็กในขดลวดเลย ขดลวดทุติยภูมิจึงไม่มีอีเอ็มเอฟ",
                    "หม้อแปลงทำจากแกนเหล็กซึ่งนำไฟฟ้ากระแสตรงไม่ได้ จึงไม่มีกระแสผ่านไปยังขดลวดอีกขด"),
            topic=TOPIC_EMF,
            hint="อีเอ็มเอฟเหนี่ยวนำต้องการสนามแม่เหล็กที่เปลี่ยนแปลง กระแสตรงที่คงตัวให้สนามคงตัว")
