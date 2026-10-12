"""ปฏิกิริยานิวเคลียร์ฟิชชันและฟิวชัน

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/16

Sets moved here from: science_wave_f18.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f18 import SUBJECT, U_MEV, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_FISSION = "ปฏิกิริยานิวเคลียร์ฟิชชันและฟิวชัน"


FISSION_FACTS = (
    ("ปฏิกิริยาฟิชชันคืออะไร", "นิวเคลียสหนักแตกเป็นนิวเคลียสขนาดกลางสองนิวเคลียส ปล่อยนิวตรอนและพลังงาน",
     ("นิวเคลียสเบารวมกันเป็นนิวเคลียสที่หนักขึ้น", "อิเล็กตรอนหลุดออกจากอะตอมทำให้เกิดไอออนและพลังงาน", "นิวเคลียสปล่อยรังสีแกมมาอย่างเดียวโดยไม่แตกตัว")),
    ("ปฏิกิริยาฟิวชันคืออะไร", "นิวเคลียสเบารวมกันเป็นนิวเคลียสที่หนักขึ้นพร้อมปล่อยพลังงาน",
     ("นิวเคลียสหนักแตกออกเป็นสองส่วนพร้อมปล่อยพลังงาน", "อะตอมรวมกันเป็นโมเลกุลพร้อมคายความร้อน", "นิวตรอนเปลี่ยนเป็นโปรตอนพร้อมปล่อยอิเล็กตรอน")),
    ("พลังงานของดวงอาทิตย์มาจากปฏิกิริยาใด", "ฟิวชันของนิวเคลียสไฮโดรเจนเป็นฮีเลียม",
     ("ฟิชชันของยูเรเนียม", "การเผาไหม้ของแก๊สไฮโดรเจนกับออกซิเจน", "การสลายให้รังสีแอลฟา")),
    ("ปฏิกิริยาลูกโซ่ในเครื่องปฏิกรณ์นิวเคลียร์เกิดขึ้นได้อย่างไร", "นิวตรอนที่ปล่อยจากฟิชชันไปชนนิวเคลียสอื่นให้เกิดฟิชชันต่อเนื่อง",
     ("โปรตอนที่ปล่อยออกมาชนกัน", "ความร้อนทำให้นิวเคลียสแตกเอง", "อิเล็กตรอนวิ่งวนในแกนเครื่อง")),
    ("แท่งควบคุมในเครื่องปฏิกรณ์นิวเคลียร์ทำหน้าที่อะไร", "ดูดกลืนนิวตรอนเพื่อควบคุมอัตราการเกิดฟิชชัน",
     ("เพิ่มจำนวนนิวตรอนให้ปฏิกิริยาลูกโซ่เร็วขึ้น", "ระบายความร้อนออกจากแกนปฏิกรณ์", "เปลี่ยนความร้อนเป็นไฟฟ้าโดยตรง")),
    ("ฟิวชันเกิดได้ยากบนโลก เพราะเหตุใด", "ต้องใช้อุณหภูมิสูงมากให้นิวเคลียสชนะแรงผลักทางไฟฟ้า",
     ("ไม่มีไฮโดรเจนบนโลกให้ใช้เป็นเชื้อเพลิง", "ฟิวชันไม่ให้พลังงานออกมามากพอ", "นิวเคลียสเบาไม่มีประจุ จึงรวมกันเองไม่ได้")),
)


REACTIONS = (
    # (A, Z) of the heavy nucleus, the two fragments, and neutrons released.
    ((235, 92), (141, 56), (92, 36), 3, ("ยูเรเนียม-235", "แบเรียม", "คริปทอน")),
    ((235, 92), (140, 54), (94, 38), 2, ("ยูเรเนียม-235", "ซีนอน", "สตรอนเชียม")),
    ((235, 92), (144, 55), (90, 37), 2, ("ยูเรเนียม-235", "ซีเซียม", "รูบิเดียม")),
    ((235, 92), (137, 52), (97, 40), 2, ("ยูเรเนียม-235", "เทลลูเรียม", "เซอร์โคเนียม")),
    ((239, 94), (134, 54), (103, 40), 3, ("พลูโทเนียม-239", "ซีนอน", "เซอร์โคเนียม")),
)


@question_type(
    "phys.fission_fusion_foundation",
    display_name={"th": "ปฏิกิริยาฟิชชัน ฟิวชัน และเครื่องปฏิกรณ์นิวเคลียร์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_FISSION,
)
class FissionFusionFoundation(QuestionType):
    """Splitting and joining, chain reactions and control rods."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, correct, wrongs = rng.choice(FISSION_FACTS)
        if rng.random() < 0.6:
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_FISSION,
                             hint="ฟิชชัน: หนักแตกเป็นกลาง ฟิวชัน: เบารวมเป็นหนัก ทั้งสองปล่อยพลังงานจากมวลที่หายไป")
        per = rng.choice((180, 190, 200, 210))
        n = rng.randint(2, 50)
        return numeric(
            stem=f"ฟิชชันของยูเรเนียม-235 หนึ่งครั้งให้พลังงานประมาณ {per} MeV ฟิชชัน {n} ครั้งให้พลังงานกี่เมกะอิเล็กตรอนโวลต์",
            answer=per * n, wrongs=[per + n, per * n * 2, per], unit="MeV", topic=TOPIC_FISSION,
            hint="พลังงานรวม = พลังงานต่อครั้ง × จำนวนครั้ง")


@question_type(
    "phys.fission_fusion_fluency",
    display_name={"th": "ดุลเลขมวลและเลขอะตอมในสมการปฏิกิริยานิวเคลียร์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_FISSION,
)
class FissionFusionFluency(QuestionType):
    """Mass number and atomic number are both conserved: find the neutrons or a missing Z."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        (a0, z0), (a1, z1), (a2, z2), n, (heavy, f1, f2) = rng.choice(REACTIONS)
        shape = rng.randrange(4)
        if shape == 3:
            a0, z0 = rng.choice(((235, 92), (239, 94), (233, 92)))
            z1 = rng.randint(34, 58)
            a1 = rng.randint(int(z1 * 2.3), int(z1 * 2.6))
            n = rng.randint(1, 4)
            a2, z2 = a0 + 1 - a1 - n, z0 - z1
            ask_a = rng.random() < 0.5
            return numeric(
                stem=(f"นิวตรอน 1 ตัวชนนิวเคลียส (A = {a0}, Z = {z0}) เกิดฟิชชันได้นิวเคลียส (A = {a1}, Z = {z1}) นิวตรอน {n} ตัว "
                      f"และนิวเคลียส Y นิวเคลียส Y มี{'เลขมวล' if ask_a else 'เลขอะตอม'}เท่าใด"),
                answer=a2 if ask_a else z2, wrongs=[(a0 - a1 - n) if ask_a else z0 - z1 + 1, (a2 + n) if ask_a else z2 - 1,
                                                   (a0 - a1) if ask_a else z1],
                unit="", topic=TOPIC_FISSION, hint="เลขมวลและเลขอะตอมรวมต้องเท่ากันก่อนและหลัง อย่าลืมนิวตรอนที่ชนเข้าไป 1 ตัว")
        eq = f"นิวตรอน 1 ตัวชนนิวเคลียส{heavy} (Z = {z0}) ได้{f1}-{a1}"
        if shape == 0:
            return numeric(
                stem=f"{eq} (Z = {z1}) และ{f2}-{a2} (Z = {z2}) พร้อมนิวตรอนอีกจำนวนหนึ่ง ปล่อยนิวตรอนออกมากี่ตัว",
                answer=n, wrongs=[n + 1, a0 - a1 - a2, 1 if n != 1 else 4], unit="ตัว", topic=TOPIC_FISSION,
                hint="เลขมวลรวมก่อนและหลังเท่ากัน: 1 + A = A₁ + A₂ + จำนวนนิวตรอน")
        if shape == 1:
            return numeric(
                stem=f"{eq} (Z = {z1}) นิวเคลียส{f2}-{a2} และนิวตรอน {n} ตัว {f2}มีเลขอะตอมเท่าใด",
                answer=z2, wrongs=[z0 - z1 + 1, z2 + 2, a2 - z2], unit="", topic=TOPIC_FISSION,
                hint="เลขอะตอมรวมก่อนและหลังเท่ากัน (นิวตรอนมี Z = 0)")
        # Deuterium-tritium fusion, and variants from the textbook.
        fuse = rng.choice(((2, 1, 3, 1, 4, 2, "นิวตรอน", 1, 0), (2, 1, 2, 1, 3, 2, "นิวตรอน", 1, 0),
                           (2, 1, 2, 1, 3, 1, "โปรตอน", 1, 1), (1, 1, 2, 1, 3, 2, "รังสีแกมมา", 0, 0)))
        a_a, z_a, a_b, z_b, a_c, z_c, other, a_o, z_o = fuse
        ask_a = rng.random() < 0.5
        return numeric(
            stem=(f"ในปฏิกิริยาฟิวชัน นิวเคลียส (A = {a_a}, Z = {z_a}) รวมกับ (A = {a_b}, Z = {z_b}) ได้{other}และนิวเคลียส X "
                  f"นิวเคลียส X มี{'เลขมวล' if ask_a else 'เลขอะตอม'}เท่าใด"),
            answer=a_c if ask_a else z_c, wrongs=[a_a + a_b, z_a + z_b + 1, (a_c if ask_a else z_c) + 1],
            unit="", topic=TOPIC_FISSION, hint="ทั้งเลขมวลและเลขอะตอมรวมก่อนและหลังปฏิกิริยาต้องเท่ากัน")


@question_type(
    "phys.fission_fusion_application",
    display_name={"th": "คำนวณพลังงานนิวเคลียร์จากมวลที่หายไป"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_FISSION,
)
class FissionFusionApplication(QuestionType):
    """E = Δm × 931 MeV from the masses before and after."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        dm = Fraction(rng.randint(1, 25), 100)
        before = Fraction(rng.randint(2000, 24000), 100)
        after = before - dm
        what = rng.choice(("ฟิชชัน", "ฟิวชัน"))
        if rng.random() < 0.5:
            return numeric(
                stem=(f"ในปฏิกิริยา{what}หนึ่ง มวลรวมก่อนเกิดปฏิกิริยา {show(before)} u และมวลรวมหลังเกิด {show(after)} u "
                      "ปฏิกิริยานี้ปล่อยพลังงานกี่เมกะอิเล็กตรอนโวลต์ (1 u = 931 MeV)"),
                answer=dm * U_MEV, wrongs=[before * U_MEV / 1000, dm * U_MEV * 10, dm * 1000], unit="MeV",
                topic=TOPIC_FISSION, hint="หามวลที่หายไป Δm = มวลก่อน − มวลหลัง แล้ว E = Δm × 931 MeV")
        return numeric(
            stem=f"ปฏิกิริยา{what}หนึ่งมีมวลหายไป {show(dm)} u ปล่อยพลังงานกี่เมกะอิเล็กตรอนโวลต์ (1 u = 931 MeV)",
            answer=dm * U_MEV, wrongs=[dm * U_MEV * 10, dm * U_MEV / 10, Fraction(U_MEV) * dm * 2], unit="MeV",
            topic=TOPIC_FISSION, hint="E = Δm × 931 MeV")
