"""การสื่อสารด้วยคลื่นแม่เหล็กไฟฟ้าและสัญญาณแอนะล็อกกับดิจิทัล

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.6/8

Sets moved here from: science_wave_f14.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f14 import SUBJECT, UPPER_SIX, _exact

PROVENANCE = Provenance("original")


TOPIC_SIGNAL = "การสื่อสารด้วยคลื่นแม่เหล็กไฟฟ้าและสัญญาณแอนะล็อกกับดิจิทัล"


SIGNAL_FACTS = (
    ("สัญญาณแอนะล็อกมีลักษณะอย่างไร", "มีค่าต่อเนื่อง เปลี่ยนแปลงได้ทุกค่าในช่วงหนึ่ง",
     ("มีเพียงสองค่าคือ 0 และ 1 ไม่มีค่าระหว่างกลาง", "มีค่าคงตัวตลอดเวลาไม่เปลี่ยนแปลง", "มีค่าเป็นจำนวนเต็มเท่านั้นที่เปลี่ยนเป็นขั้น")),
    ("สัญญาณดิจิทัลมีลักษณะอย่างไร", "มีค่าไม่ต่อเนื่อง แทนด้วยเลขฐานสอง 0 และ 1",
     ("มีค่าต่อเนื่องทุกค่าในช่วงหนึ่งเหมือนคลื่นเสียง", "เป็นคลื่นไซน์เสมอที่มีค่าต่อเนื่อง", "ไม่สามารถส่งผ่านสายได้ ต้องส่งทางอากาศเท่านั้น")),
    ("ข้อดีของสัญญาณดิจิทัลเมื่อเทียบกับแอนะล็อกคือข้อใด", "ทนต่อสัญญาณรบกวน และทำสำเนาได้โดยคุณภาพไม่ลดลง",
     ("ใช้แบนด์วิดท์น้อยกว่าเสมอ", "ไม่ต้องแปลงสัญญาณ", "ส่งได้เฉพาะเสียง")),
    ("การผสมสัญญาณแบบ AM ต่างจาก FM อย่างไร", "AM เปลี่ยนแอมพลิจูดของคลื่นพาห์ ส่วน FM เปลี่ยนความถี่ของคลื่นพาห์",
     ("AM เปลี่ยนความถี่ ส่วน FM เปลี่ยนแอมพลิจูด", "ทั้งสองเปลี่ยนความยาวคลื่นเท่ากัน", "AM ใช้แสง ส่วน FM ใช้เสียง")),
    ("เส้นใยนำแสงส่งสัญญาณได้โดยอาศัยปรากฏการณ์ใด", "การสะท้อนกลับหมดของแสงภายในเส้นใย",
     ("การเลี้ยวเบนของแสงที่ปลายเส้นใย", "การกระเจิงของแสงภายในเส้นใย", "การเหนี่ยวนำแม่เหล็กไฟฟ้า")),
    ("ดาวเทียมสื่อสารค้างฟ้าช่วยการสื่อสารอย่างไร", "รับสัญญาณจากสถานีภาคพื้นดินแล้วส่งต่อไปยังอีกที่หนึ่งที่อยู่ไกล",
     ("สร้างคลื่นวิทยุขึ้นเองโดยไม่ต้องรับสัญญาณจากสถานีใดเลย", "สะท้อนเสียงกลับมายังโลกเพื่อให้ได้ยินไกลขึ้น", "ส่งสัญญาณผ่านสายเคเบิลใต้ทะเลที่ต่อจากดาวเทียม")),
)


@question_type(
    "phys.signal_communication_foundation",
    display_name={"th": "สัญญาณแอนะล็อกกับดิจิทัลและระบบการสื่อสาร"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SIGNAL,
)
class SignalCommunicationFoundation(QuestionType):
    """Analog against digital, AM against FM, fibres and satellites."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, correct, wrongs = rng.choice(SIGNAL_FACTS)
        if rng.random() < 0.55:
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_SIGNAL,
                             hint="แอนะล็อกต่อเนื่อง ดิจิทัลเป็น 0 กับ 1 จึงทนสัญญาณรบกวน")
        if rng.random() < 0.5:
            am = rng.random() < 0.5
            freq = f"{rng.randint(53, 160) * 10:,} kHz" if am else f"{show(Fraction(rng.randint(880, 1080), 10))} MHz"
            return _labelled(
                stem=f"สถานีวิทยุส่งคลื่นพาห์ความถี่ {freq} น่าจะเป็นสถานีระบบใด",
                correct="สถานี AM (ผสมสัญญาณทางแอมพลิจูด)" if am else "สถานี FM (ผสมสัญญาณทางความถี่)",
                wrongs=("สถานี FM (ผสมสัญญาณทางความถี่)" if am else "สถานี AM (ผสมสัญญาณทางแอมพลิจูด)",
                        "สัญญาณเส้นใยนำแสง", "สัญญาณรีโมตอินฟราเรด"),
                topic=TOPIC_SIGNAL, hint="วิทยุ AM ใช้ช่วงประมาณ 530-1,600 kHz ส่วน FM ใช้ช่วงประมาณ 88-108 MHz")
        khz = rng.choice((500, 600, 750, 800, 1000, 1200, 1250, 1500))
        return numeric(
            stem=f"สถานีวิทยุ AM ส่งคลื่นพาห์ความถี่ {khz:,} kHz ความยาวคลื่นเท่าใด (c = 3 × 10⁸ m/s)",
            answer=Fraction(3 * 10 ** 5, khz), wrongs=[Fraction(3 * 10 ** 5, khz) * 10, Fraction(3 * 10 ** 5, khz) / 10,
                                                       Fraction(khz * 1000, 3 * 10 ** 8) * 1000],
            unit="m", topic=TOPIC_SIGNAL, hint="λ = c/f เปลี่ยน kHz เป็น Hz ก่อน")


@question_type(
    "phys.signal_communication_fluency",
    display_name={"th": "จำนวนบิตกับจำนวนระดับของสัญญาณดิจิทัล"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SIGNAL,
)
class SignalCommunicationFluency(QuestionType):
    """n bits give 2ⁿ levels, and the fewest bits for a number of levels."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            n = rng.randint(1, 12)
            return numeric(stem=f"สัญญาณดิจิทัลที่ใช้ข้อมูล {n} บิตต่อหนึ่งค่า แทนระดับของสัญญาณได้กี่ระดับ",
                           answer=2 ** n, wrongs=[2 * n, n * n, 2 ** (n + 1)], unit="ระดับ", topic=TOPIC_SIGNAL,
                           hint="n บิตแทนได้ 2ⁿ ค่า")
        levels = rng.randint(3, 1000)
        bits = (levels - 1).bit_length()
        return numeric(stem=f"ต้องการแปลงสัญญาณแอนะล็อกเป็นดิจิทัลโดยแบ่งเป็น {levels} ระดับ ต้องใช้อย่างน้อยกี่บิตต่อหนึ่งค่า",
                       answer=bits, wrongs=[bits - 1, bits + 1, bits + 2], unit="บิต", topic=TOPIC_SIGNAL,
                       hint="หาจำนวนบิต n ที่น้อยที่สุดซึ่ง 2ⁿ ไม่น้อยกว่าจำนวนระดับ")


@question_type(
    "phys.signal_communication_application",
    display_name={"th": "เวลาในการส่งข้อมูลดิจิทัลและขนาดข้อมูล"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SIGNAL,
)
class SignalCommunicationApplication(QuestionType):
    """Transfer time = size × 8 ÷ rate, and the size of sampled audio."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            size, rate = rng.choice([(s, r) for s in (5, 10, 20, 25, 40, 50, 100, 200, 500, 1000)
                                     for r in (2, 4, 5, 8, 10, 16, 20, 40, 50, 100) if _exact(Fraction(s * 8, r))])
            return numeric(
                stem=f"ส่งไฟล์ขนาด {size:,} เมกะไบต์ ผ่านเครือข่ายที่อัตรา {rate} เมกะบิตต่อวินาที ใช้เวลาอย่างน้อยกี่วินาที (1 ไบต์ = 8 บิต)",
                answer=Fraction(size * 8, rate), wrongs=[Fraction(size, rate), Fraction(size * rate, 8), Fraction(size * 8, rate) * 2],
                unit="s", topic=TOPIC_SIGNAL, hint="ขนาดเป็นบิต = ไบต์ × 8 แล้วเวลา = จำนวนบิต ÷ อัตราการส่ง")
        rate_khz = rng.choice((8, 16, 22, 44, 48))
        bits = rng.choice((8, 16))
        seconds = rng.choice((1, 2, 5, 10, 60))
        total_bits = rate_khz * 1000 * bits * seconds
        return numeric(
            stem=(f"บันทึกเสียงแบบดิจิทัลช่องเดียว ชักตัวอย่าง {rate_khz} kHz ค่าละ {bits} บิต เป็นเวลา {seconds} s "
                  "ได้ข้อมูลกี่กิโลไบต์ (1 กิโลไบต์ = 1,000 ไบต์)"),
            answer=Fraction(total_bits, 8000), wrongs=[Fraction(total_bits, 1000), Fraction(total_bits, 8000) * 2,
                                                       Fraction(rate_khz * seconds * bits, 8)],
            unit="kB", topic=TOPIC_SIGNAL,
            hint="จำนวนบิต = อัตราชักตัวอย่าง × บิตต่อค่า × เวลา แล้วหารด้วย 8 ได้ไบต์ และหาร 1,000 ได้กิโลไบต์")
