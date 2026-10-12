"""กำลังไฟฟ้าในตัวต้านทาน

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.5/9

Sets moved here from: electricity, science_wave_a6.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.kit.numeric_scenario import Calc, PhysCalc, fmt, slips
from otk.sets._support.electricity import LEVEL as LEVEL_electricity
from otk.sets._support.electricity import SUBJECT, TOPIC
from otk.sets._support.science_wave_a6 import LEVEL

PROVENANCE = Provenance("original")


# (อีเอ็มเอฟ โวลต์, ความต้านทานภายใน โอห์ม, ความต้านทานภายนอก โอห์ม). Chosen so
# the circuit current ε/(R+r) is whole, which makes every quantity below whole.
# The internal resistance is always the smaller of the two, as a real cell's is,
# and the current is never 1 A — that would hide a dropped square in I²R.
EMF_CIRCUITS = (
    (12, 1, 5), (12, 2, 4), (24, 2, 4), (9, 1, 2), (18, 2, 4), (10, 1, 4),
    (6, 1, 2), (20, 2, 3), (15, 1, 4), (12, 1, 3), (30, 2, 4), (24, 1, 5),
)


@question_type(
    "elec.power_emf_foundation",
    display_name={"th": "อีเอ็มเอฟ พลังงานไฟฟ้า และกำลังไฟฟ้า"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PowerEmfFoundation(ConceptBankType):
    """The vocabulary ``ม.5/9`` computes with: อีเอ็มเอฟ, ความต่างศักย์ปลายเซลล์,
    พลังงานไฟฟ้า and กำลังไฟฟ้า.

    `elec.power_forms` drills P = I²R and P = V²/R and never mentions the source.
    The distinction that costs marks at ม.5 is that อีเอ็มเอฟ is not the voltage
    a working battery puts across a circuit, and this set is where it is said.
    """

    ITEMS = [
        Concept(
            "อีเอ็มเอฟของแหล่งกำเนิดไฟฟ้ากระแสตรง หมายถึงข้อใด",
            "พลังงานที่แหล่งกำเนิดให้แก่ประจุหนึ่งหน่วยที่เคลื่อนผ่านแหล่งกำเนิด",
            ("แรงที่แหล่งกำเนิดใช้ผลักประจุให้เคลื่อนที่ไปตามวงจร",
             "ความต่างศักย์ระหว่างขั้วของแหล่งกำเนิดขณะจ่ายกระแสไฟฟ้า",
             "ปริมาณประจุไฟฟ้าทั้งหมดที่แหล่งกำเนิดเก็บไว้ได้"),
        ),
        Concept(
            "ขณะที่แบตเตอรี่จ่ายกระแสไฟฟ้าให้วงจร ความต่างศักย์ระหว่างขั้วของแบตเตอรี่ "
            "เป็นอย่างไรเมื่อเทียบกับอีเอ็มเอฟ",
            "น้อยกว่าอีเอ็มเอฟ เพราะเสียความต่างศักย์ไปกับความต้านทานภายใน",
            ("มากกว่าอีเอ็มเอฟ เพราะความต้านทานภายในช่วยเสริมแรงดัน",
             "เท่ากับอีเอ็มเอฟเสมอ ไม่ว่าจะจ่ายกระแสไฟฟ้ามากเพียงใด",
             "เท่ากับศูนย์ เพราะพลังงานทั้งหมดถูกใช้ไปในวงจรภายนอก"),
        ),
        Concept(
            "กำลังไฟฟ้าและพลังงานไฟฟ้าต่างกันอย่างไร",
            "กำลังไฟฟ้าคือพลังงานไฟฟ้าที่ใช้ในหนึ่งหน่วยเวลา",
            ("กำลังไฟฟ้าคือพลังงานไฟฟ้าที่ใช้ตลอดการทำงาน",
             "พลังงานไฟฟ้าคือกำลังไฟฟ้าที่ใช้ในหนึ่งหน่วยเวลา",
             "ทั้งสองเป็นปริมาณเดียวกัน ต่างกันเพียงหน่วยที่ใช้เรียก"),
        ),
        Concept(
            "กำลังไฟฟ้ามีหน่วยเป็นอะไรในระบบเอสไอ",
            "วัตต์ (W)",
            ("จูล (J)", "โวลต์ (V)", "กิโลวัตต์-ชั่วโมง (kWh)"),
        ),
        Concept(
            "ตัวต้านทานที่มีกระแสไฟฟ้าผ่าน เปลี่ยนพลังงานไฟฟ้าไปเป็นพลังงานรูปใดเป็นหลัก",
            "พลังงานความร้อน",
            ("พลังงานเคมี", "พลังงานศักย์ไฟฟ้าที่สะสมไว้ในตัวต้านทาน",
             "พลังงานกลของอิเล็กตรอนที่เคลื่อนที่เร็วขึ้นเรื่อย ๆ"),
        ),
        Concept(
            "กำลังไฟฟ้ารวมที่แหล่งกำเนิดจ่ายออกมา หาได้จากข้อใด",
            "อีเอ็มเอฟคูณกับกระแสไฟฟ้าในวงจร",
            ("ความต่างศักย์ระหว่างขั้วคูณกับอีเอ็มเอฟ",
             "อีเอ็มเอฟหารด้วยกระแสไฟฟ้าในวงจร",
             "กระแสไฟฟ้ายกกำลังสองคูณกับความต้านทานภายในเท่านั้น"),
        ),
        Concept(
            "ต่อตัวต้านทานสองตัวที่มีความต้านทานต่างกันแบบอนุกรมเข้ากับแบตเตอรี่ "
            "ตัวต้านทานใดใช้กำลังไฟฟ้ามากกว่า",
            "ตัวที่มีความต้านทานมากกว่า เพราะกระแสไฟฟ้าผ่านเท่ากันและ P = I²R",
            ("ตัวที่มีความต้านทานน้อยกว่า เพราะกระแสไฟฟ้าผ่านได้มากกว่า",
             "ทั้งสองตัวใช้กำลังไฟฟ้าเท่ากัน เพราะต่ออนุกรมกัน",
             "ตัวที่อยู่ใกล้ขั้วบวกของแบตเตอรี่มากกว่า"),
        ),
        Concept("แบตเตอรี่มีอีเอ็มเอฟ 12 โวลต์ หมายความว่าอย่างไร",
                "แบตเตอรี่ให้พลังงาน 12 จูลแก่ประจุทุก 1 คูลอมบ์ที่เคลื่อนผ่าน",
                (
                 "แบตเตอรี่จ่ายกระแสไฟฟ้า 12 แอมแปร์เสมอ",
                 "แบตเตอรี่มีความต้านทานภายใน 12 โอห์ม",
                 "แบตเตอรี่เก็บพลังงานได้ทั้งหมด 12 จูล",
                 "แบตเตอรี่ให้กำลังไฟฟ้า 12 วัตต์เสมอ",
                 "ความต่างศักย์ระหว่างขั้วเป็น 12 โวลต์เสมอแม้ขณะจ่ายกระแส")),
        Concept("เมื่อแบตเตอรี่ไม่ได้จ่ายกระแสไฟฟ้า (วงจรเปิด) ความต่างศักย์ระหว่างขั้วเป็นอย่างไร",
                "เท่ากับอีเอ็มเอฟ",
                (
                 "เป็นศูนย์",
                 "มากกว่าอีเอ็มเอฟ",
                 "เท่ากับครึ่งหนึ่งของอีเอ็มเอฟ",
                 "เท่ากับกระแสคูณความต้านทานภายใน",
                 "มีค่าติดลบ")),
        Concept("ตัวต้านทานสองตัวต่อขนานกับแหล่งกำเนิดเดียวกัน ตัวใดใช้กำลังไฟฟ้ามากกว่า",
                "ตัวที่มีความต้านทานน้อยกว่า เพราะความต่างศักย์เท่ากันและ P = V²/R",
                (
                 "ตัวที่มีความต้านทานมากกว่า เพราะ P = I²R",
                 "ใช้เท่ากัน เพราะต่อกับแหล่งกำเนิดเดียวกัน",
                 "ตัวที่อยู่ใกล้แหล่งกำเนิดมากกว่า",
                 "ตัวที่มีความต้านทานมากกว่า เพราะ P = V²/R",
                 "ตัวที่มีความต้านทานน้อยกว่า เพราะกระแสไฟฟ้าผ่านเท่ากัน")),
        Concept("กำลังไฟฟ้าที่ตัวต้านทาน R ใช้เมื่อมีกระแสไฟฟ้า I ผ่าน หาได้จากข้อใด",
                "P = I²R",
                (
                 "P = I/R",
                 "P = IR",
                 "P = R/I²",
                 "P = I²/R",
                 "P = IR²")),
    ]


@question_type("elec.power_forms",
               display_name={"th": "กำลังไฟฟ้าในรูป I²R และ V²/R"},
               level=LEVEL_electricity, subject=SUBJECT, topic=TOPIC)
class PowerForms(PhysCalc):
    """P = I²R และ P = V²/R — รูปของกำลังไฟฟ้าที่ได้จากการแทน V = IR ลงใน P = VI.

    ตัวลวงตัวแรกคือการลืมยกกำลังสองเสมอ (ตอบ IR แทน I²R, ตอบ V/R แทน V²/R)
    ซึ่งเป็นข้อผิดพลาดที่พบมากที่สุดของสองสูตรนี้.
    """

    _I = [2, 3, 4, 5]                        # กระแสไฟฟ้า (แอมแปร์)
    _R = [2, 3, 4, 5, 10]                    # ความต้านทาน (โอห์ม)
    # (V โวลต์, R โอห์ม) เลือกให้ V²/R ลงตัว
    _VR = [(10, 5), (20, 10), (30, 10), (60, 20), (20, 5), (10, 10),
           (30, 5), (60, 10), (40, 20), (50, 10)]

    def draw(self, rng: Random) -> Calc:
        which = rng.random()
        if which < 0.4:                      # ให้ I กับ R → หา P = I²R
            i, r = rng.choice(self._I), rng.choice(self._R)
            p = i * i * r
            return Calc(
                f"กระแสไฟฟ้า {i} แอมแปร์ ผ่านตัวต้านทานขนาด {r} โอห์ม "
                f"ตัวต้านทานนี้ใช้กำลังไฟฟ้าเท่าใด (วัตต์)",
                fmt(p), wrongs=slips(fmt(p), i * r, i * r * r, i * i),
                hint=r"P = I^{2}R")
        if which < 0.8:                      # ให้ V กับ R → หา P = V²/R
            v, r = rng.choice(self._VR)
            p = v * v // r
            return Calc(
                f"ต่อตัวต้านทานขนาด {r} โอห์ม เข้ากับความต่างศักย์ {v} โวลต์ "
                f"ตัวต้านทานนี้ใช้กำลังไฟฟ้าเท่าใด (วัตต์)",
                fmt(p), wrongs=slips(fmt(p), v / r, v * r, v * v),
                hint=r"P = \frac{V^{2}}{R}")
        i, r = rng.choice(self._I), rng.choice(self._R)
        p = i * i * r
        return Calc(                         # ให้ P กับ I → หา R
            f"ตัวต้านทานตัวหนึ่งมีกระแสไฟฟ้าผ่าน {i} แอมแปร์ "
            f"และใช้กำลังไฟฟ้า {p} วัตต์ จงหาความต้านทานของตัวต้านทานนี้ (โอห์ม)",
            fmt(r), wrongs=slips(fmt(r), p / i, p * i, i * i),
            hint=r"R = \frac{P}{I^{2}}")


@question_type(
    "elec.power_emf_application",
    display_name={"th": "กำลังไฟฟ้าในวงจรที่แหล่งกำเนิดมีความต้านทานภายใน"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PowerEmfApplication(PhysCalc):
    """Find the circuit current from the emf and both resistances, then use it.

    Every one of these needs the current first, and the current needs the
    internal resistance — which is exactly what a learner who has only met
    `elec.power_forms` will leave out, so ignoring it is the first distractor
    every time.
    """

    def draw(self, rng: Random) -> Calc:
        emf, internal, external = rng.choice(EMF_CIRCUITS)
        current = emf // (external + internal)
        circuit = (f"แบตเตอรี่มีอีเอ็มเอฟ {emf} โวลต์ และความต้านทานภายใน "
                   f"{internal} โอห์ม ต่อเข้ากับตัวต้านทาน {external} โอห์ม ")
        which = rng.random()
        if which < 0.4:
            power = current * current * external
            return Calc(
                circuit + "ตัวต้านทานนี้ใช้กำลังไฟฟ้าเท่าใด (วัตต์)",
                fmt(power),
                # ลืมความต้านทานภายใน, ใช้กำลังไฟฟ้ารวมของวงจร, ลืมยกกำลังสอง
                wrongs=slips(fmt(power), emf * emf / external, emf * current,
                             current * external),
                hint=r"I = \frac{\varepsilon}{R + r},\ P = I^{2}R")
        if which < 0.7:
            terminal = emf - current * internal
            return Calc(
                circuit + "ความต่างศักย์ระหว่างขั้วของแบตเตอรี่ขณะนี้เป็นเท่าใด (โวลต์)",
                fmt(terminal),
                # ตอบอีเอ็มเอฟ, ตอบส่วนที่หายไป, บวกแทนลบ
                wrongs=slips(fmt(terminal), emf, current * internal,
                             emf + current * internal),
                hint=r"V = \varepsilon - Ir")
        lost = current * current * internal
        return Calc(
            circuit + "กำลังไฟฟ้าที่สูญเสียไปในความต้านทานภายในของแบตเตอรี่เป็นเท่าใด (วัตต์)",
            fmt(lost),
            # ตอบกำลังไฟฟ้าของตัวต้านทานภายนอก, ลืมยกกำลังสอง, ตอบกำลังไฟฟ้ารวม
            wrongs=slips(fmt(lost), current * current * external,
                         current * internal, emf * current),
            hint=r"I = \frac{\varepsilon}{R + r},\ P_r = I^{2}r")
