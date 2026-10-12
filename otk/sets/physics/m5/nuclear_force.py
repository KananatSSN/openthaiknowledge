"""แรงเข้มและแรงอ่อน

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.5/10

Sets moved here from: science_wave_e12.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e12 import SUBJECT, UPPER_FIVE, _labelled

PROVENANCE = Provenance("original")


TOPIC_NUCLEAR_FORCE = "แรงเข้มและแรงอ่อน"


STRONG, WEAK, ELECTRO, GRAVITY = "แรงเข้ม", "แรงอ่อน", "แรงแม่เหล็กไฟฟ้า", "แรงโน้มถ่วง"


FORCES = (STRONG, WEAK, ELECTRO, GRAVITY)


FORCE_DESCRIPTIONS = (
    ("ยึดโปรตอนและนิวตรอนไว้ด้วยกันในนิวเคลียส", STRONG),
    ("มีขนาดมากที่สุดในแรงพื้นฐานทั้งสี่ แต่มีระยะทำการสั้นมากเพียงขนาดของนิวเคลียส", STRONG),
    ("ยึดควาร์กไว้ด้วยกันภายในโปรตอนและนิวตรอน", STRONG),
    ("เกี่ยวข้องกับการสลายของนิวเคลียสแบบบีตา", WEAK),
    ("ทำให้นิวตรอนเปลี่ยนเป็นโปรตอนพร้อมปล่อยอิเล็กตรอนออกมา", WEAK),
    ("มีระยะทำการสั้นมาก และเกี่ยวข้องกับปฏิกิริยาที่เปลี่ยนชนิดของอนุภาค", WEAK),
    ("ทำให้โปรตอนสองตัวในนิวเคลียสผลักกัน", ELECTRO),
    ("ยึดอิเล็กตรอนไว้รอบนิวเคลียสของอะตอม", ELECTRO),
    ("ยึดดาวเคราะห์ให้โคจรรอบดวงอาทิตย์", GRAVITY),
    ("ทำให้วัตถุตกลงสู่พื้นโลก", GRAVITY),
)


NUCLEAR_PHENOMENA = (
    ("นิวเคลียสไม่แตกออกจากกัน แม้โปรตอนที่อยู่ใกล้กันมากจะผลักกันด้วยแรงไฟฟ้า",
     "ในระยะสั้นภายในนิวเคลียส แรงเข้มมีขนาดมากกว่าแรงผลักทางไฟฟ้าระหว่างโปรตอน",
     STRONG),
    ("คาร์บอน-14 สลายตัวแบบบีตากลายเป็นไนโตรเจน-14",
     "แรงอ่อนทำให้นิวตรอนเปลี่ยนเป็นโปรตอนและปล่อยอนุภาคบีตา",
     WEAK),
    ("นิวเคลียสที่มีโปรตอนมากเกินไปจะไม่เสถียร",
     "แรงผลักระหว่างโปรตอนมีระยะทำการไกลกว่าแรงเข้ม นิวเคลียสใหญ่จึงยึดกันได้ไม่ดี",
     STRONG),
    ("ปฏิกิริยาฟิวชันในดวงอาทิตย์เปลี่ยนโปรตอนบางตัวเป็นนิวตรอน",
     "แรงอ่อนทำให้อนุภาคเปลี่ยนชนิด โปรตอนจึงเปลี่ยนเป็นนิวตรอนได้",
     WEAK),
)


FORCE_WRONG_REASONS = (
    "แรงโน้มถ่วงระหว่างนิวคลีออนมีขนาดมากพอจะยึดนิวเคลียสไว้",
    "แรงแม่เหล็กจากอิเล็กตรอนรอบนิวเคลียสดันนิวคลีออนเข้าหากัน",
    "นิวตรอนมีประจุลบจึงดึงดูดโปรตอนไว้ในนิวเคลียสได้แน่น",
    "แรงอ่อนยึดนิวคลีออนไว้ด้วยกันแทนแรงเข้มในทุกนิวเคลียส",
    "แรงเข้มทำให้นิวตรอนเปลี่ยนเป็นโปรตอนโดยตรงและปล่อยอิเล็กตรอน",
)


@question_type(
    "phys.nuclear_force_foundation",
    display_name={"th": "แรงพื้นฐานใดทำหน้าที่ตามที่กำหนด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NUCLEAR_FORCE,
)
class NuclearForceFoundation(QuestionType):
    """Name the fundamental force from what it does, or the other way round."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        description, force = rng.choice(FORCE_DESCRIPTIONS)
        if rng.random() < 0.5:
            others = [d for d, f in FORCE_DESCRIPTIONS if f != force]
            return _labelled(
                stem=f"ข้อใดเป็นลักษณะของ{force}",
                correct=description, wrongs=tuple(others),
                topic=TOPIC_NUCLEAR_FORCE,
                hint="แรงเข้มยึดนิวเคลียส แรงอ่อนเกี่ยวกับการสลายแบบบีตา แรงแม่เหล็กไฟฟ้าเกี่ยวกับประจุ แรงโน้มถ่วงเกี่ยวกับมวล")
        return _labelled(
            stem=f"แรงพื้นฐานใด{description}",
            correct=force, wrongs=tuple(f for f in FORCES if f != force),
            topic=TOPIC_NUCLEAR_FORCE,
            hint="แรงเข้มยึดนิวเคลียส แรงอ่อนเกี่ยวกับการสลายแบบบีตา แรงแม่เหล็กไฟฟ้าเกี่ยวกับประจุ แรงโน้มถ่วงเกี่ยวกับมวล")


@question_type(
    "phys.nuclear_force_fluency",
    display_name={"th": "อธิบายปรากฏการณ์ในนิวเคลียสด้วยแรงเข้มและแรงอ่อน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NUCLEAR_FORCE,
)
class NuclearForceFluency(QuestionType):
    """The indicator's อธิบาย, reaching both forces: which one explains what happens in a nucleus."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        phenomenon, reason, _ = rng.choice(NUCLEAR_PHENOMENA)
        return _labelled(
            stem=f"\"{phenomenon}\" ข้อใดอธิบายได้ถูกต้อง",
            correct=reason, wrongs=tuple(FORCE_WRONG_REASONS),
            topic=TOPIC_NUCLEAR_FORCE,
            hint="แรงเข้มยึดโปรตอนและนิวตรอนไว้ในนิวเคลียสในระยะสั้นมาก แรงอ่อนทำให้อนุภาคเปลี่ยนชนิดในการสลายแบบบีตา")


@question_type(
    "phys.nuclear_force_application",
    display_name={"th": "เปรียบเทียบแรงพื้นฐานทั้งสี่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NUCLEAR_FORCE,
)
class NuclearForceApplication(QuestionType):
    """Compare the four forces by strength and range, and pick the one at work in a scene."""

    RANKS = {
        "มีขนาดมากที่สุด": STRONG,
        "มีขนาดน้อยที่สุด": GRAVITY,
        "มีระยะทำการไกลไม่จำกัดและมีทั้งแรงดึงดูดและแรงผลัก": ELECTRO,
        "มีระยะทำการไกลไม่จำกัดและเป็นแรงดึงดูดเสมอ": GRAVITY,
    }
    SCENES = (
        ("ภายในนิวเคลียสของอะตอมยูเรเนียม ที่ทำให้นิวตรอนและโปรตอนอยู่รวมกันได้", STRONG),
        ("ในการสลายตัวของทริเทียมซึ่งปล่อยอนุภาคบีตาออกมา", WEAK),
        ("ระหว่างดวงจันทร์กับโลกซึ่งทำให้เกิดน้ำขึ้นน้ำลง", GRAVITY),
        ("ระหว่างหวีที่ถูกผมแล้วกับเศษกระดาษที่ถูกดูดขึ้นมา", ELECTRO),
        ("ระหว่างอะตอมในโมเลกุลน้ำซึ่งยึดกันด้วยพันธะเคมี", ELECTRO),
        ("ระหว่างแม่เหล็กกับตะปูเหล็กที่ถูกดูดติด", ELECTRO),
        ("ระหว่างดวงอาทิตย์กับดาวเคราะห์ที่โคจรรอบดวงอาทิตย์", GRAVITY),
        ("ที่ยึดแก๊สจำนวนมหาศาลของดาวฤกษ์ไว้เป็นทรงกลม", GRAVITY),
        ("ในการสลายตัวของนิวตรอนอิสระกลายเป็นโปรตอน", WEAK),
        ("ในการสลายตัวของโคบอลต์-60 ซึ่งปล่อยอนุภาคบีตาออกมา", WEAK),
        ("ภายในนิวเคลียสของฮีเลียมที่ทำให้โปรตอนสองตัวอยู่ด้วยกันได้", STRONG),
    )

    STRENGTH = (STRONG, ELECTRO, WEAK, GRAVITY)   # strongest first

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.random()
        if shape < 0.3:
            a, b = rng.sample(self.STRENGTH, 2)
            stronger = a if self.STRENGTH.index(a) < self.STRENGTH.index(b) else b
            weaker = b if stronger == a else a
            return _labelled(
                stem=f"เมื่อเปรียบเทียบที่ระยะห่างขนาดนิวเคลียส ระหว่าง{a}กับ{b} ข้อใดถูกต้อง",
                correct=f"{stronger}มีขนาดมากกว่า{weaker}",
                wrongs=(f"{weaker}มีขนาดมากกว่า{stronger}", f"{a}และ{b}มีขนาดเท่ากัน",
                        "เปรียบเทียบไม่ได้ เพราะแรงทั้งสองเป็นแรงชนิดเดียวกัน"),
                topic=TOPIC_NUCLEAR_FORCE,
                hint="เรียงตามขนาด: แรงเข้ม > แรงแม่เหล็กไฟฟ้า > แรงอ่อน > แรงโน้มถ่วง")
        if shape < 0.6:
            what, force = rng.choice(list(self.RANKS.items()))
            return _labelled(
                stem=f"ในแรงพื้นฐานทั้งสี่ แรงใด{what}",
                correct=force, wrongs=tuple(f for f in FORCES if f != force),
                topic=TOPIC_NUCLEAR_FORCE,
                hint="เรียงตามขนาด: แรงเข้ม > แรงแม่เหล็กไฟฟ้า > แรงอ่อน > แรงโน้มถ่วง แรงเข้มและแรงอ่อนมีระยะทำการสั้นมาก")
        scene, force = rng.choice(self.SCENES)
        return _labelled(
            stem=f"แรงพื้นฐานที่มีบทบาทหลัก{scene}คือแรงใด",
            correct=force, wrongs=tuple(f for f in FORCES if f != force),
            topic=TOPIC_NUCLEAR_FORCE,
            hint="ดูขนาดของระบบและสิ่งที่เกิด: ภายในนิวเคลียส การเปลี่ยนชนิดอนุภาค ประจุ หรือมวลขนาดใหญ่")
