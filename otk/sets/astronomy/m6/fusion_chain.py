"""การสร้างพลังงานของดาวฤกษ์

ดาราศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/5

Sets moved here from: science_wave_f82.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f82 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_FUSION = "การสร้างพลังงานของดาวฤกษ์"


FUSION_FACTS = (
    ("ผลรวมของปฏิกิริยาลูกโซ่โปรตอน-โปรตอนคือข้อใด", "ไฮโดรเจน 4 นิวเคลียสหลอมรวมเป็นฮีเลียม 1 นิวเคลียส พร้อมปล่อยพลังงาน",
     ("ฮีเลียม 4 นิวเคลียสหลอมรวมเป็นไฮโดรเจน", "ไฮโดรเจน 2 นิวเคลียสแตกตัวเป็นฮีเลียม", "คาร์บอนเผาไหม้กับออกซิเจนในแก๊สร้อน พร้อมปล่อยพลังงานความร้อน", "เหล็ก 1 นิวเคลียสแตกตัวเป็นไฮโดรเจน 56 นิวเคลียส พร้อมปล่อยพลังงาน")),
    ("ในวัฏจักรคาร์บอน-ไนโตรเจน-ออกซิเจน (CNO) คาร์บอนทำหน้าที่อะไร", "เป็นตัวเร่งปฏิกิริยา ได้คาร์บอนกลับคืนเมื่อครบวัฏจักร",
     ("เป็นเชื้อเพลิงที่ถูกใช้หมดไป", "เป็นผลิตภัณฑ์หลักของปฏิกิริยา", "เป็นเชื้อเพลิงที่ถูกใช้หมดไป จึงต้องมีคาร์บอนใหม่เสมอ", "ทำให้ดาวเย็นลง เพราะคาร์บอนดูดพลังงานที่เกิดขึ้นไว้")),
    ("พลังงานจากฟิวชันในดาวฤกษ์มาจากอะไร", "มวลที่หายไประหว่างปฏิกิริยาเปลี่ยนเป็นพลังงานตาม E = mc²",
     ("การเผาไหม้ไฮโดรเจนกับออกซิเจนในแกนดาวที่ร้อนจัด", "การสลายตัวของยูเรเนียมจำนวนมากที่อยู่ในแกนดาว", "แรงเสียดทานของแก๊สร้อนที่หมุนวนอยู่ในแกนดาว", "การสะท้อนแสงจากดาวดวงอื่น")),
    ("อนุภาคใดเกิดขึ้นจากปฏิกิริยาลูกโซ่โปรตอน-โปรตอนแล้วเคลื่อนที่ออกจากดวงอาทิตย์ได้แทบไม่ถูกดูดกลืน", "นิวทริโน",
     ("นิวตรอน", "โปรตอน", "นิวเคลียสฮีเลียม", "อะตอมคาร์บอน")),
    ("เหตุใดวัฏจักร CNO จึงเกิดเด่นในดาวฤกษ์ที่มีมวลมากกว่าดวงอาทิตย์", "แกนของดาวร้อนกว่า นิวเคลียสคาร์บอนที่มีประจุมากจึงหลอมรวมกับโปรตอนได้",
     ("ดาวมวลมากไม่มีไฮโดรเจน จึงใช้คาร์บอนเป็นเชื้อเพลิงแทนเสมอ", "ดาวมวลมากเย็นกว่าดวงอาทิตย์ จึงต้องใช้คาร์บอนช่วยเร่งปฏิกิริยา", "แกนของดาวมวลมากเย็นกว่า นิวเคลียสคาร์บอนจึงเคลื่อนที่ช้าและจับโปรตอนได้ง่าย", "ดาวมวลมากหยุดสร้างพลังงาน")),
    ("เหตุใดฟิวชันไฮโดรเจนจึงต้องการอุณหภูมิหลายล้านเคลวิน", "โปรตอนต้องเคลื่อนที่เร็วมากพอจะเอาชนะแรงผลักทางไฟฟ้าระหว่างกันได้",
     ("ไฮโดรเจนต้องถูกเผาไหม้กับออกซิเจน", "ต้องทำให้ไฮโดรเจนกลายเป็นของเหลว", "อิเล็กตรอนต้องหลอมรวมกันก่อน จึงจะดึงโปรตอนให้เข้ามาใกล้กันได้", "ไฮโดรเจนต้องถูกเผาไหม้กับออกซิเจนจนร้อนพอที่จะเปลี่ยนเป็นฮีเลียม")),
    ("ดวงอาทิตย์สร้างพลังงานด้วยกระบวนการใดเป็นหลัก", "ปฏิกิริยาลูกโซ่โปรตอน-โปรตอน",
     ("วัฏจักร CNO เพียงอย่างเดียว", "ฟิชชันของยูเรเนียม", "ฟิชชันของไฮโดรเจน", "การหลอมรวมเหล็ก")),
)


FUSION_HINT = ("ลูกโซ่โปรตอน-โปรตอน: 4 ¹H → ⁴He + 2e⁺ + 2ν + พลังงาน เด่นในดาวมวลน้อยถึงขนาดดวงอาทิตย์ "
               "วัฏจักร CNO ใช้ C N O เป็นตัวเร่ง ผลรวมเหมือนกัน เด่นในดาวมวลมากที่แกนร้อนกว่า "
               "มวลหายไปประมาณร้อยละ 0.7 กลายเป็นพลังงาน E = mc²")


@question_type(
    "astro.fusion_chain_foundation",
    display_name={"th": "ปฏิกิริยาลูกโซ่โปรตอน-โปรตอนและวัฏจักร CNO"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_FUSION,
)
class FusionChainFoundation(QuestionType):
    """Net reaction, catalysts, mass-energy, neutrinos."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(FUSION_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_FUSION, hint=FUSION_HINT)


@question_type(
    "astro.fusion_chain_fluency",
    display_name={"th": "ระบุกระบวนการสร้างพลังงานตามมวลและอุณหภูมิแกนของดาว"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_FUSION,
)
class FusionChainFluency(QuestionType):
    """Which process dominates, by mass; what each makes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            mass = Fraction(rng.choice([n for n in range(2, 101) if not 10 <= n <= 20]), 10)
            pp = mass < Fraction(13, 10)
            right = "ปฏิกิริยาลูกโซ่โปรตอน-โปรตอน" if pp else "วัฏจักรคาร์บอน-ไนโตรเจน-ออกซิเจน"
            return _labelled(stem=f"ดาวฤกษ์ในลำดับหลักมวล {show(mass)} เท่าของดวงอาทิตย์ สร้างพลังงานด้วยกระบวนการใดเป็นหลัก "
                                  f"(วัฏจักร CNO เด่นในดาวมวลมากกว่าประมาณ 1.3 เท่าของดวงอาทิตย์)",
                             correct=right, wrongs=tuple(o for o in ("ปฏิกิริยาลูกโซ่โปรตอน-โปรตอน", "วัฏจักรคาร์บอน-ไนโตรเจน-ออกซิเจน",
                                                                     "ฟิชชันของยูเรเนียม", "การเผาไหม้ของไฮโดรเจนกับออกซิเจน") if o != right),
                             topic=TOPIC_FUSION, hint=FUSION_HINT)
        items = (("ฮีเลียม", True), ("นิวทริโน", True), ("โพซิตรอน", True), ("พลังงาน", True),
                 ("ยูเรเนียม", False), ("แก๊สออกซิเจนที่ใช้หายใจ", False), ("คาร์บอนไดออกไซด์", False), ("น้ำ", False))
        made = rng.random() < 0.5
        right = rng.choice([n for n, y in items if y == made])
        wrongs = rng.sample([n for n, y in items if y != made], 3)
        return _labelled(stem=f"ข้อใด{'เป็น' if made else 'ไม่ได้เป็น'}ผลิตภัณฑ์ของปฏิกิริยาลูกโซ่โปรตอน-โปรตอน", correct=right, wrongs=tuple(wrongs),
                         topic=TOPIC_FUSION, hint=FUSION_HINT)


@question_type(
    "astro.fusion_chain_application",
    display_name={"th": "คำนวณมวลที่หายไป พลังงาน และจำนวนนิวเคลียสในฟิวชัน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_FUSION,
)
class FusionChainApplication(QuestionType):
    """0.7 % of the hydrogen mass becomes energy; four protons per helium."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            kg = rng.choice((1, 2, 4, 5, 10, 20, 50, 100))
            lost = Fraction(7 * kg, 1000)
            return numeric(stem=f"ไฮโดรเจน {kg} kg หลอมรวมเป็นฮีเลียมทั้งหมด มวลหายไปร้อยละ 0.7 มวลที่หายไปเป็นกี่กรัม",
                           answer=lost * 1000, wrongs=[Fraction(7 * kg, 10), 70 * kg, 7 * kg + 1],
                           unit="g", topic=TOPIC_FUSION, hint="มวลที่หายไป = มวลไฮโดรเจน × 0.7 ÷ 100")
        if roll < 0.7:
            grams = rng.choice((1, 2, 3, 4, 5, 7, 10, 20))
            energy = Fraction(grams, 1000) * 9 * 10 ** 16 / 10 ** 13
            return numeric(stem=f"มวล {grams} g เปลี่ยนเป็นพลังงานทั้งหมด (E = mc², c = 3 × 10⁸ m/s) ได้พลังงานกี่ × 10¹³ J",
                           answer=energy, wrongs=[energy / 10, Fraction(grams * 3, 1), energy * 1000], unit="× 10¹³ J", topic=TOPIC_FUSION,
                           hint="แปลงมวลเป็นกิโลกรัมก่อน แล้ว E = m × (3 × 10⁸)²")
        protons = 4 * rng.randint(3, 250)
        helium = protons // 4
        if rng.random() < 0.5:
            return numeric(stem=f"โปรตอน {show(protons)} อนุภาคหลอมรวมผ่านปฏิกิริยาลูกโซ่โปรตอน-โปรตอนจนหมด จะได้นิวเคลียสฮีเลียมกี่นิวเคลียส",
                           answer=helium, wrongs=[protons // 2, protons, helium * 2 + 1], unit="นิวเคลียส", topic=TOPIC_FUSION,
                           hint="ไฮโดรเจน 4 นิวเคลียสได้ฮีเลียม 1 นิวเคลียส")
        return numeric(stem=f"ปฏิกิริยาลูกโซ่โปรตอน-โปรตอนให้ฮีเลียม {show(helium)} นิวเคลียส จะเกิดนิวทริโนกี่อนุภาค",
                       answer=helium * 2, wrongs=[helium, helium * 4, helium + 2], unit="อนุภาค", topic=TOPIC_FUSION,
                       hint="ฮีเลียม 1 นิวเคลียสมาพร้อมนิวทริโน 2 อนุภาค")
