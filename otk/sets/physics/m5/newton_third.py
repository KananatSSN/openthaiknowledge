"""แรงกิริยาและแรงปฏิกิริยา

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.5/4

Sets moved here from: science_wave_e11.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e11 import SUBJECT, UPPER_FIVE, _labelled, _numeric

PROVENANCE = Provenance("original")


TOPIC_NEWTON3 = "แรงกิริยาและแรงปฏิกิริยา"


class ActionPair(NamedTuple):
    situation: str
    action: str
    reaction: str
    # A force that looks like the reaction but acts on the same body, or has
    # the wrong direction — the misconception worth offering.
    lookalike: str


ACTION_PAIRS: tuple[ActionPair, ...] = (
    ActionPair("นักวิ่งออกตัวจากจุดเริ่มต้น", "เท้าของนักวิ่งดันพื้นไปข้างหลัง",
               "พื้นดันเท้าของนักวิ่งไปข้างหน้า", "พื้นดันเท้าของนักวิ่งไปข้างหลัง"),
    ActionPair("นักว่ายน้ำว่ายไปข้างหน้า", "มือของนักว่ายน้ำผลักน้ำไปข้างหลัง",
               "น้ำผลักมือของนักว่ายน้ำไปข้างหน้า", "น้ำผลักมือของนักว่ายน้ำไปข้างหลัง"),
    ActionPair("จรวดพุ่งขึ้นจากฐานยิง", "จรวดผลักแก๊สร้อนออกทางท้ายลงด้านล่าง",
               "แก๊สร้อนผลักจรวดขึ้นด้านบน", "อากาศรอบจรวดผลักจรวดขึ้นด้านบน"),
    ActionPair("หนังสือวางนิ่งบนโต๊ะ", "หนังสือกดโต๊ะลงด้านล่าง",
               "โต๊ะดันหนังสือขึ้นด้านบน", "โลกดึงหนังสือลงด้านล่าง"),
    ActionPair("ผลมะม่วงหล่นจากต้น", "โลกดึงผลมะม่วงเข้าหาโลก",
               "ผลมะม่วงดึงโลกเข้าหาผลมะม่วง", "อากาศต้านผลมะม่วงขึ้นด้านบน"),
    ActionPair("ค้อนตอกตะปู", "ค้อนออกแรงกระแทกตะปูลงไป",
               "ตะปูออกแรงกระแทกค้อนขึ้นมา", "ไม้ออกแรงต้านตะปูขึ้นมา"),
    ActionPair("ยิงปืน", "ปืนผลักกระสุนไปข้างหน้า",
               "กระสุนผลักปืนไปข้างหลัง", "ดินปืนผลักกระสุนไปข้างหลัง"),
    ActionPair("คนพายเรือ", "ไม้พายผลักน้ำไปข้างหลัง",
               "น้ำผลักไม้พายไปข้างหน้า", "น้ำผลักเรือไปข้างหลัง"),
    ActionPair("นักเรียนยืนผลักกำแพง", "มือของนักเรียนผลักกำแพง",
               "กำแพงผลักมือของนักเรียนกลับ", "เท้าของนักเรียนดันพื้น"),
    ActionPair("ลูกโป่งที่ปล่อยให้ลมพุ่งออก", "ลูกโป่งบีบอากาศให้พุ่งออกทางปากลูกโป่ง",
               "อากาศที่พุ่งออกผลักลูกโป่งไปทางตรงข้าม", "อากาศภายนอกดึงลูกโป่งไปข้างหน้า"),
    ActionPair("แม่เหล็กสองแท่งวางหันขั้วเหนือเข้าหากัน", "แม่เหล็ก ก ผลักแม่เหล็ก ข",
               "แม่เหล็ก ข ผลักแม่เหล็ก ก", "แม่เหล็ก ก ดึงแม่เหล็ก ข"),
    ActionPair("ดวงจันทร์โคจรรอบโลก", "โลกดึงดวงจันทร์เข้าหาโลก",
               "ดวงจันทร์ดึงโลกเข้าหาดวงจันทร์", "ดวงอาทิตย์ดึงดวงจันทร์"),
)


PAIR_FACTS = (
    ("แรงกิริยาและแรงปฏิกิริยามีขนาดและทิศทางอย่างไร",
     "มีขนาดเท่ากันและมีทิศทางตรงข้ามกัน",
     ("มีขนาดเท่ากันและมีทิศทางเดียวกัน", "แรงกิริยามีขนาดมากกว่าแรงปฏิกิริยาเสมอ",
      "มีทิศทางตรงข้ามกัน แต่แรงปฏิกิริยามีขนาดน้อยกว่า")),
    ("แรงกิริยาและแรงปฏิกิริยากระทำต่อวัตถุใด",
     "กระทำต่อวัตถุคนละก้อน จึงหักล้างกันไม่ได้",
     ("กระทำต่อวัตถุก้อนเดียวกัน จึงหักล้างกันหมด", "แรงกิริยากระทำต่อทั้งสองวัตถุพร้อมกัน",
      "กระทำต่อวัตถุใดก็ได้ ขึ้นกับว่าแรงใดมากกว่า")),
    ("แรงกิริยาและแรงปฏิกิริยาเกิดขึ้นเมื่อใด",
     "เกิดขึ้นพร้อมกันเสมอ",
     ("แรงปฏิกิริยาเกิดหลังแรงกิริยาเล็กน้อย", "แรงปฏิกิริยาเกิดเฉพาะเมื่อวัตถุหยุดนิ่ง",
      "เกิดเฉพาะเมื่อวัตถุสัมผัสกันเท่านั้น")),
)


@question_type(
    "phys.newton_third_foundation",
    display_name={"th": "สมบัติของแรงกิริยาและแรงปฏิกิริยา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NEWTON3,
)
class NewtonThirdFoundation(QuestionType):
    """The rule: equal size, opposite direction, on the other body, at once."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "แรงกิริยาและแรงปฏิกิริยาเกิดพร้อมกัน ขนาดเท่ากัน ทิศตรงข้าม และกระทำต่อวัตถุคนละก้อน"
        if rng.random() < 0.5:
            stem, correct, wrongs = rng.choice(PAIR_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs,
                             topic=TOPIC_NEWTON3, hint=hint)
        pair = rng.choice(ACTION_PAIRS)
        f = rng.randint(2, 60) * 5
        return _labelled(
            stem=f"ขณะ{pair.situation} ถ้า{pair.action}ด้วยแรง {f} นิวตัน แรงปฏิกิริยามีขนาดเท่าใด",
            correct=f"{f} นิวตัน", wrongs=(f"{f // 5} นิวตัน", f"{f * 2} นิวตัน", "0 นิวตัน"),
            topic=TOPIC_NEWTON3, hint=hint,
        )


@question_type(
    "phys.newton_third_fluency",
    display_name={"th": "ระบุแรงปฏิกิริยาของแรงกิริยาที่กำหนด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NEWTON3,
)
class NewtonThirdFluency(QuestionType):
    """The indicator: name the partner of a given force in a real situation."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        pair = rng.choice(ACTION_PAIRS)
        others = [p.reaction for p in ACTION_PAIRS if p != pair]
        return _labelled(
            stem=f"ขณะ{pair.situation} ถ้าแรงกิริยาคือ \"{pair.action}\" แรงปฏิกิริยาคือข้อใด",
            correct=pair.reaction,
            wrongs=(pair.lookalike, pair.action, rng.choice(others)),
            topic=TOPIC_NEWTON3,
            hint="สลับวัตถุที่ออกแรงกับวัตถุที่ถูกกระทำ แล้วกลับทิศของแรง",
        )


@question_type(
    "phys.newton_third_application",
    display_name={"th": "ใช้แรงกิริยาและแรงปฏิกิริยาอธิบายการชนและการผลักกัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NEWTON3,
)
class NewtonThirdApplication(QuestionType):
    """Equal forces, unequal masses: who accelerates more, and why a pair never cancels."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            f = rng.randint(2, 20) * 60
            m1 = rng.choice((40, 50, 60))
            m2 = rng.choice([m for m in (20, 30, 40, 60, 80) if m != m1])
            names = rng.choice((("พ่อ", "ลูก"), ("นักสเกตคนที่หนึ่ง", "นักสเกตคนที่สอง")))
            who = rng.randrange(2)
            m_who = (m1, m2)[who]
            return _numeric(
                stem=(f"{names[0]}มวล {m1} กิโลกรัมและ{names[1]}มวล {m2} กิโลกรัมยืนบนพื้นน้ำแข็งลื่น "
                      f"แล้วผลักกันด้วยแรง {f} นิวตัน {names[who]}มีความเร่งเท่าใด"),
                answer=Fraction(f, m_who),
                wrongs=[Fraction(f, (m2, m1)[who]), Fraction(f, m1 + m2), Fraction(2 * f, m_who)],
                unit="m/s²", topic=TOPIC_NEWTON3,
                hint="ทั้งสองได้รับแรงขนาดเท่ากัน แต่ความเร่งของแต่ละคน = แรง ÷ มวลของคนนั้น")
        if shape == 1:
            big, small = rng.choice((("รถบรรทุก", "รถยนต์"), ("รถยนต์", "รถจักรยานยนต์"),
                                     ("ลูกโบว์ลิ่ง", "ลูกปิงปอง")))
            return _labelled(
                stem=f"{big}ชนกับ{small} ข้อใดถูกต้องเกี่ยวกับแรงที่กระทำต่อกันขณะชน",
                correct=f"แรงที่กระทำต่อกันเท่ากัน แต่{small}มีมวลน้อยกว่าจึงมีความเร่งมากกว่า",
                wrongs=(f"{big}ออกแรงมากกว่า เพราะมีมวลมากกว่า {small}จึงถูกผลักไป",
                        f"{small}ออกแรงมากกว่า เพราะมีความเร่งมากกว่า {big}จึงช้าลง",
                        "แรงทั้งสองเท่ากัน ทั้งคู่จึงมีความเร่งเท่ากันและหยุดพร้อมกัน"),
                topic=TOPIC_NEWTON3,
                hint="แรงกิริยาและแรงปฏิกิริยามีขนาดเท่ากันเสมอ ความเร่งที่ต่างกันมาจากมวลที่ต่างกัน",
            )
        pair = rng.choice([p for p in ACTION_PAIRS if "นิ่ง" in p.situation or "ผลัก" in p.situation])
        return _labelled(
            stem=(f"ขณะ{pair.situation} นักเรียนคนหนึ่งบอกว่า \"{pair.action}และ{pair.reaction} "
                  "สองแรงนี้หักล้างกันพอดี\" ข้อใดอธิบายได้ถูกต้อง"),
            correct="ไม่ถูกต้อง เพราะแรงคู่นี้กระทำต่อวัตถุคนละก้อน จึงหักล้างกันไม่ได้",
            wrongs=("ถูกต้อง เพราะแรงคู่นี้มีขนาดเท่ากันและทิศตรงข้ามกัน",
                    "ไม่ถูกต้อง เพราะแรงปฏิกิริยามีขนาดน้อยกว่าแรงกิริยาเสมอในทุกกรณี",
                    "ถูกต้อง เพราะวัตถุทั้งสองไม่เคลื่อนที่ไปไหนเลย"),
            topic=TOPIC_NEWTON3,
            hint="แรงจะหักล้างกันได้ต้องกระทำต่อวัตถุก้อนเดียวกัน",
        )
