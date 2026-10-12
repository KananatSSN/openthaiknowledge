"""ศักย์เยื่อเซลล์และการถ่ายทอดกระแสประสาท

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/3

Sets moved here from: science_wave_f65.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f65 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_IMPULSE = "ศักย์เยื่อเซลล์และการถ่ายทอดกระแสประสาท"


PHASES = (
    ("ศักย์เยื่อเซลล์ขณะพัก", "ภายในเซลล์เป็นลบเทียบกับภายนอก ประมาณ −70 mV"),
    ("ดีโพลาไรเซชัน", "ช่องโซเดียมเปิด Na⁺ แพร่เข้าเซลล์ ภายในเปลี่ยนเป็นบวก"),
    ("รีโพลาไรเซชัน", "ช่องโพแทสเซียมเปิด K⁺ แพร่ออกนอกเซลล์ ภายในกลับเป็นลบ"),
    ("ไฮเพอร์โพลาไรเซชัน", "K⁺ ออกมากเกินไปชั่วครู่ ภายในลบมากกว่าศักย์ขณะพัก"),
)


SYNAPSE = ("กระแสประสาทมาถึงปลายแอกซอน", "Ca²⁺ แพร่เข้าปลายแอกซอน", "ถุงบรรจุสารสื่อประสาทหลั่งสารออกด้วยเอกโซไซโทซิส",
           "สารสื่อประสาทจับกับตัวรับที่เยื่อของเซลล์ถัดไป", "เอนไซม์สลายสารสื่อประสาท เช่น แอซีทิลโคลีนเอสเทอเรส")


IMPULSE_HINT = ("ขณะพักภายในเป็นลบ (−70 mV) โซเดียม-โพแทสเซียมปั๊มส่ง Na⁺ ออก 3 ไอออน K⁺ เข้า 2 ไอออน "
                "ถึงระดับขีดเริ่มเปลี่ยน Na⁺ เข้าเกิดดีโพลาไรเซชัน แล้ว K⁺ ออกเกิดรีโพลาไรเซชัน")


@question_type(
    "biology.nerve_impulse_foundation",
    display_name={"th": "การเปลี่ยนแปลงศักย์ไฟฟ้าที่เยื่อหุ้มเซลล์ประสาท"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_IMPULSE,
)
class NerveImpulseFoundation(QuestionType):
    """Resting, depolarising, repolarising, overshooting."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        phase, event = rng.choice(PHASES)
        others = [p for p in PHASES if p[0] != phase]
        roll = rng.random()
        if roll < 0.35:
            events = [p[1] for p in others] + ["Ca²⁺ แพร่ออกจากเซลล์จนหมด", "เยื่อหุ้มเซลล์ถูกทำลายชั่วคราว"]
            return _labelled(stem=f"ระยะ{phase}เกิดอะไรขึ้นที่เยื่อหุ้มเซลล์ประสาท", correct=event, wrongs=tuple(events),
                             topic=TOPIC_IMPULSE, hint=IMPULSE_HINT)
        if roll < 0.7:
            names = [p[0] for p in others] + ["ระยะดื้อสัมบูรณ์", "การหลั่งสารสื่อประสาท"]
            return _labelled(stem=f"\"{event}\" เป็นระยะใด", correct=phase, wrongs=tuple(names), topic=TOPIC_IMPULSE,
                             hint=IMPULSE_HINT)
        facts = (("ขณะพัก ภายในเซลล์ประสาทมี K⁺ และ Na⁺ อย่างไรเมื่อเทียบกับภายนอก", "K⁺ มากกว่า แต่ Na⁺ น้อยกว่า",
                  ("Na⁺ มากกว่า แต่ K⁺ น้อยกว่า", "มีทั้งสองไอออนมากกว่า", "มีทั้งสองไอออนเท่ากับภายนอก", "ไม่มีไอออนทั้งสองชนิด")),
                 ("ระดับขีดเริ่มเปลี่ยน (threshold) หมายถึงข้อใด", "ระดับศักย์ไฟฟ้าที่เมื่อถึงแล้วช่องโซเดียมเปิดจำนวนมากจนเกิดกระแสประสาท",
                  ("ศักย์ไฟฟ้าสูงสุดของกระแสประสาท", "ศักย์ไฟฟ้าขณะพัก", "เวลาที่กระแสประสาทใช้ข้ามไซแนปส์", "จำนวนไอออนที่ปั๊มส่งออก")),
                 ("โซเดียม-โพแทสเซียมปั๊มทำงานโดยอาศัยอะไร", "พลังงานจาก ATP", ("แสง", "การแพร่แบบธรรมดา", "แรงดันเลือด", "ออสโมซิส")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_IMPULSE, hint=IMPULSE_HINT)


@question_type(
    "biology.nerve_impulse_fluency",
    display_name={"th": "การถ่ายทอดกระแสประสาทที่ไซแนปส์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_IMPULSE,
)
class NerveImpulseFluency(QuestionType):
    """The synapse, step by step."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            i = rng.randrange(len(SYNAPSE) - 1)
            pool = [s for s in SYNAPSE if s not in (SYNAPSE[i], SYNAPSE[i + 1])] + ["Na⁺ ถูกปั๊มเข้าสู่ปลายแอกซอน"]
            return _labelled(stem=f"ที่ไซแนปส์ หลังจาก \"{SYNAPSE[i]}\" ขั้นต่อไปคือข้อใด", correct=SYNAPSE[i + 1],
                             wrongs=tuple(pool), topic=TOPIC_IMPULSE, hint=IMPULSE_HINT)
        facts = (("เหตุใดกระแสประสาทจึงถ่ายทอดผ่านไซแนปส์ได้ทางเดียว", "สารสื่อประสาทหลั่งจากปลายแอกซอนเท่านั้น และตัวรับอยู่ที่เซลล์ถัดไป",
                  ("เดนไดรต์หลั่งสารสื่อประสาทได้ด้วย", "ไซแนปส์มีลิ้นกั้นเหมือนหัวใจ", "กระแสไฟฟ้ากระโดดข้ามช่องไซแนปส์โดยตรง",
                   "เยื่อไมอีลินกั้นไม่ให้ไหลย้อน")),
                 ("การตอบสนองแบบ \"ทั้งหมดหรือไม่มีเลย\" ของกระแสประสาทหมายถึงข้อใด", "ถ้าการกระตุ้นถึงระดับขีดเริ่มเปลี่ยนจะเกิดกระแสประสาทขนาดเท่าเดิมเสมอ",
                  ("กระตุ้นแรงขึ้นกระแสประสาทใหญ่ขึ้นเรื่อย ๆ", "กระแสประสาทเกิดได้ทุกระดับการกระตุ้น", "เซลล์ประสาทตอบสนองได้ครั้งเดียวในชีวิต",
                   "กระแสประสาทเล็กลงเมื่อเดินทางไกล")),
                 ("กระแสประสาทในใยประสาทที่มีเยื่อไมอีลินเคลื่อนที่เร็วกว่าเพราะเหตุใด", "กระแสประสาทกระโดดจากโนดออฟแรนเวียร์หนึ่งไปยังอีกโนดหนึ่ง",
                  ("เยื่อไมอีลินนำไฟฟ้าได้ดี", "แอกซอนมีขนาดเล็กลง", "ไม่ต้องใช้ไอออนเลย", "มีไซแนปส์ถี่ขึ้นตลอดแอกซอน")),
                 ("สารสื่อประสาทชนิดใดพบที่รอยต่อระหว่างเซลล์ประสาทสั่งการกับกล้ามเนื้อลาย", "แอซีทิลโคลีน",
                  ("อินซูลิน", "ฮีโมโกลบิน", "อะไมเลส", "อะดรีนาลีนจากต่อมหมวกไต")),
                 ("สารที่ยับยั้งแอซีทิลโคลีนเอสเทอเรสทำให้เกิดผลอย่างไร", "แอซีทิลโคลีนค้างที่ไซแนปส์ กล้ามเนื้อถูกกระตุ้นต่อเนื่องจนเกร็ง",
                  ("กล้ามเนื้อคลายตัวตลอดเวลา", "ไม่มีการหลั่งสารสื่อประสาท", "กระแสประสาทเคลื่อนที่เร็วขึ้นในแอกซอน", "ไซแนปส์ปิดถาวร")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_IMPULSE, hint=IMPULSE_HINT)


@question_type(
    "biology.nerve_impulse_application",
    display_name={"th": "คำนวณการเปลี่ยนแปลงศักย์เยื่อเซลล์และการทำงานของปั๊ม"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_IMPULSE,
)
class NerveImpulseApplication(QuestionType):
    """Size of the swing, ions pumped, and the refractory ceiling on firing rate."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            rest = -rng.randrange(60, 91, 5)
            peak = rng.randrange(20, 46, 5)
            return numeric(stem=f"ศักย์เยื่อเซลล์ขณะพักเท่ากับ {rest} mV และสูงสุดขณะดีโพลาไรเซชัน +{peak} mV ศักย์ไฟฟ้าเปลี่ยนไปกี่ mV",
                           answer=peak - rest, wrongs=[peak + rest if peak + rest > 0 else peak, -rest, peak], unit="mV", topic=TOPIC_IMPULSE,
                           hint="การเปลี่ยนแปลง = ค่าสูงสุด − ค่าขณะพัก")
        if roll < 0.7:
            cycles = rng.randrange(10, 501, 10)
            na = rng.random() < 0.5
            return numeric(stem=f"โซเดียม-โพแทสเซียมปั๊มทำงาน {cycles} รอบ ส่ง{'Na⁺ ออกนอก' if na else 'K⁺ เข้าสู่'}เซลล์กี่ไอออน",
                           answer=cycles * (3 if na else 2), wrongs=[cycles * (2 if na else 3), cycles, cycles * 5], unit="ไอออน",
                           topic=TOPIC_IMPULSE, hint="ปั๊ม 1 รอบส่ง Na⁺ ออก 3 ไอออน และ K⁺ เข้า 2 ไอออน โดยใช้ ATP 1 โมเลกุล")
        refractory = rng.choice((1, 2, 4, 5, 8, 10))
        return numeric(stem=f"ถ้าเซลล์ประสาทมีระยะดื้อ (refractory period) {refractory} ms เซลล์นี้ส่งกระแสประสาทได้มากที่สุดกี่ครั้งต่อวินาที",
                       answer=Fraction(1000, refractory), wrongs=[refractory * 1000, Fraction(100, refractory), refractory], unit="ครั้ง",
                       topic=TOPIC_IMPULSE, hint="ในระยะดื้อไม่เกิดกระแสประสาทใหม่ จำนวนครั้งสูงสุด = 1,000 ms ÷ ระยะดื้อ")
