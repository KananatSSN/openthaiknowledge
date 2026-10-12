"""พลังงานศักย์ไฟฟ้าและความต่างศักย์

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.5/4

Sets moved here from: science_successors, science_wave_a6.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.kit.numeric_scenario import Calc, PhysCalc, fmt, slips
from otk.sets._support.science_wave_a6 import LEVEL, SUBJECT, TOPIC
from otk.sets.physics.m3.electrical_energy_formulas import _PinnedEnergy

PROVENANCE = Provenance("original")


# ประจุ (ไมโครคูลอมบ์) และศักย์ไฟฟ้า (โวลต์) ที่จุดต้นทางและปลายทาง. Every product
# is whole, so the three directions of W = qΔV all divide exactly.
POTENTIAL_CHARGES = (2, 3, 4, 5, 6, 8, 10)


POTENTIAL_VOLTAGES = (10, 20, 30, 40, 50, 60, 80, 100, 120)


@question_type(
    "elec.electric_potential_foundation",
    display_name={"th": "พลังงานศักย์ไฟฟ้า ศักย์ไฟฟ้า และความต่างศักย์"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ElectricPotentialFoundation(ConceptBankType):
    """Tell the three quantities of ``ม.5/4`` apart before computing with any.

    `elec.energy_charge_voltage` already drills W = QV. What it cannot show is
    which of the three names each symbol carries, or that ศักย์ไฟฟ้า belongs to a
    point while ความต่างศักย์ belongs to a pair of them — the confusion that makes
    the formula look like it has two interchangeable voltages in it.
    """

    ITEMS = [
        Concept(
            "ศักย์ไฟฟ้า ณ จุดหนึ่งในสนามไฟฟ้า หมายถึงข้อใด",
            "พลังงานศักย์ไฟฟ้าต่อหนึ่งหน่วยประจุที่จุดนั้น",
            ("พลังงานศักย์ไฟฟ้าทั้งหมดของประจุที่วางอยู่ที่จุดนั้น",
             "แรงไฟฟ้าที่กระทำต่อหนึ่งหน่วยประจุที่จุดนั้น",
             "งานที่สนามไฟฟ้าทำต่อประจุขณะเคลื่อนที่ครบหนึ่งรอบ"),
        ),
        Concept(
            "ความต่างศักย์ระหว่างจุด A กับจุด B หมายถึงข้อใด",
            "งานต่อหนึ่งหน่วยประจุในการเคลื่อนประจุจากจุด A ไปยังจุด B",
            ("ผลรวมของศักย์ไฟฟ้าที่จุด A กับที่จุด B",
             "ความยาวของเส้นทางที่ประจุเคลื่อนที่จากจุด A ไปยังจุด B",
             "อัตราการเปลี่ยนพลังงานศักย์ไฟฟ้าต่อหนึ่งหน่วยเวลา"),
        ),
        Concept(
            "พลังงานศักย์ไฟฟ้ามีหน่วยเป็นอะไรในระบบเอสไอ",
            "จูล (J)",
            ("โวลต์ (V)", "คูลอมบ์ (C)", "วัตต์ (W)"),
        ),
        Concept(
            "หนึ่งโวลต์มีค่าเท่ากับข้อใด",
            "หนึ่งจูลต่อคูลอมบ์",
            ("หนึ่งคูลอมบ์ต่อจูล", "หนึ่งจูลต่อวินาที", "หนึ่งจูลต่อแอมแปร์"),
        ),
        Concept(
            "เคลื่อนประจุบวกจากจุด A ไปยังจุด B ด้วยเส้นทางต่างกันสองเส้นทาง "
            "งานที่ต้องใช้ในสองเส้นทางนี้เป็นอย่างไร",
            "เท่ากัน เพราะงานขึ้นกับศักย์ไฟฟ้าที่จุดปลายทั้งสองเท่านั้น",
            ("เส้นทางที่สั้นกว่าใช้งานน้อยกว่าเสมอ",
             "เส้นทางที่ยาวกว่าใช้งานน้อยกว่า เพราะเคลื่อนที่ช้ากว่า",
             "เปรียบเทียบไม่ได้ ถ้าไม่ทราบรูปร่างของเส้นทาง"),
        ),
        Concept(
            "ปล่อยประจุบวกให้เคลื่อนที่อย่างอิสระในสนามไฟฟ้า ประจุจะเคลื่อนที่ไปอย่างไร",
            "ไปยังบริเวณที่มีศักย์ไฟฟ้าต่ำกว่า และพลังงานศักย์ไฟฟ้าของประจุลดลง",
            ("ไปยังบริเวณที่มีศักย์ไฟฟ้าสูงกว่า และพลังงานศักย์ไฟฟ้าของประจุลดลง",
             "ไปยังบริเวณที่มีศักย์ไฟฟ้าต่ำกว่า และพลังงานศักย์ไฟฟ้าของประจุเพิ่มขึ้น",
             "อยู่นิ่ง เพราะสนามไฟฟ้าไม่ทำงานต่อประจุที่หยุดนิ่ง"),
        ),
        Concept(
            "ประจุ +2 คูลอมบ์ กับประจุ +6 คูลอมบ์ วางอยู่ที่จุดเดียวกันในสนามไฟฟ้า "
            "ข้อความใดถูกต้อง",
            "ทั้งสองประจุมีศักย์ไฟฟ้าเท่ากัน แต่ประจุ +6 คูลอมบ์ มีพลังงานศักย์ไฟฟ้ามากกว่า",
            ("ทั้งสองประจุมีทั้งศักย์ไฟฟ้าและพลังงานศักย์ไฟฟ้าเท่ากัน",
             "ประจุ +6 คูลอมบ์ มีศักย์ไฟฟ้ามากกว่า แต่มีพลังงานศักย์ไฟฟ้าเท่ากัน",
             "ประจุ +2 คูลอมบ์ มีพลังงานศักย์ไฟฟ้ามากกว่า เพราะมีประจุน้อยกว่า"),
        ),
        Concept("ประจุ +3 คูลอมบ์ เคลื่อนผ่านความต่างศักย์ 4 โวลต์ พลังงานที่เปลี่ยนไปมีค่าเท่าใด",
                "12 จูล",
                (
                 "7 จูล",
                 "0.75 จูล",
                 "4 จูล",
                 "3 จูล",
                 "24 จูล")),
        Concept("เส้นสมศักย์หมายถึงอะไร",
                "เส้นหรือผิวที่ทุกจุดมีศักย์ไฟฟ้าเท่ากัน",
                (
                 "เส้นหรือผิวที่สนามไฟฟ้ามีขนาดเท่ากันทุกจุด",
                 "เส้นแรงไฟฟ้าที่ชี้ออกจากประจุบวก",
                 "เส้นที่ประจุเคลื่อนที่ได้เร็วที่สุด",
                 "เส้นที่ศักย์ไฟฟ้าเป็นศูนย์เสมอ",
                 "เส้นที่ขนานกับทิศของสนามไฟฟ้าเสมอ")),
        Concept("งานในการเลื่อนประจุไปตามเส้นสมศักย์มีค่าเท่าใด",
                "ศูนย์ เพราะจุดบนเส้นสมศักย์มีความต่างศักย์เป็นศูนย์",
                (
                 "มีค่ามากที่สุดเมื่อเทียบกับเส้นทางอื่น",
                 "เท่ากับประจุคูณขนาดสนามไฟฟ้า",
                 "ขึ้นกับความยาวของเส้นทางที่เลื่อน ยิ่งเลื่อนไกลงานยิ่งมาก",
                 "มีค่าติดลบเสมอ เพราะประจุเคลื่อนที่ตามเส้นสมศักย์",
                 "เท่ากับศักย์ไฟฟ้าของเส้นนั้น")),
        Concept("ความต่างศักย์ระหว่างแผ่นโลหะขนานสองแผ่นที่มีสนามไฟฟ้าสม่ำเสมอ หาได้จากข้อใด",
                "ขนาดสนามไฟฟ้าคูณระยะห่างระหว่างแผ่น",
                (
                 "ขนาดสนามไฟฟ้าหารด้วยระยะห่างระหว่างแผ่น",
                 "ประจุคูณระยะห่างระหว่างแผ่น",
                 "ขนาดสนามไฟฟ้าคูณพื้นที่แผ่น",
                 "ระยะห่างระหว่างแผ่นหารด้วยขนาดสนามไฟฟ้า",
                 "ประจุหารด้วยพื้นที่แผ่น")),
    ]


@question_type(
    "elec.energy_charge_voltage",
    display_name={"th": "พลังงานศักย์ไฟฟ้าจากประจุและความต่างศักย์ (W = QV)"},
    level={"th": "ม.5"}, subject="ฟิสิกส์", topic="ไฟฟ้า",
)
class EnergyChargeVoltage(_PinnedEnergy):
    source_key = "elec.energy"
    # Wider than the shared ``elec.energy`` tables, and kept local so that set's
    # seeded draws do not move. Every product is exact to two places.
    _Q = [0.5, 2, 3, 4, 5, 10, 20]                       # คูลอมบ์
    _V = [1.5, 6, 9, 12, 24, 110, 220]                   # โวลต์

    def draw(self, rng: Random) -> Calc:
        charge, voltage = rng.choice(self._Q), rng.choice(self._V)
        energy = charge * voltage
        return Calc(
            f"เคลื่อนประจุไฟฟ้า {charge} คูลอมบ์ ผ่านความต่างศักย์ {voltage} โวลต์ "
            f"มีพลังงานไฟฟ้าถ่ายโอนขนาดเท่าใด (จูล)",
            fmt(energy),
            wrongs=slips(fmt(energy), charge + voltage, voltage / charge, energy * 2),
            hint=r"W = QV",
        )


@question_type(
    "elec.electric_potential_application",
    display_name={"th": "งานในการเคลื่อนประจุระหว่างสองตำแหน่ง"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class ElectricPotentialApplication(PhysCalc):
    """Work out the potential difference first, then use it.

    `elec.energy_charge_voltage` hands the learner ΔV directly. Here the two
    ศักย์ไฟฟ้า values are given separately, which is how ``ม.5/4`` states the
    outcome — "ระหว่างสองตำแหน่งใด ๆ" — and the difference has to be formed before
    W = qΔV means anything.
    """

    def draw(self, rng: Random) -> Calc:
        charge = rng.choice(POTENTIAL_CHARGES)
        start, end = sorted(rng.sample(POTENTIAL_VOLTAGES, 2))
        gap = end - start
        work = charge * gap
        which = rng.random()
        if which < 0.5:
            return Calc(
                f"จุด A มีศักย์ไฟฟ้า {start} โวลต์ และจุด B มีศักย์ไฟฟ้า {end} โวลต์ "
                f"ต้องใช้งานเท่าใดในการเคลื่อนประจุ {charge} ไมโครคูลอมบ์ "
                "จากจุด A ไปยังจุด B (ไมโครจูล)",
                fmt(work),
                # ใช้ศักย์ไฟฟ้าที่ปลายทางแทนความต่างศักย์, ใช้ที่ต้นทาง, หรือบวกแทนคูณ
                wrongs=slips(fmt(work), charge * end, charge * start, charge + gap),
                hint=r"W = q(V_B - V_A)")
        if which < 0.8:
            return Calc(
                f"ใช้งาน {work} ไมโครจูล ในการเคลื่อนประจุ {charge} ไมโครคูลอมบ์ "
                f"จากจุด A ซึ่งมีศักย์ไฟฟ้า {start} โวลต์ ไปยังจุด B "
                "จงหาศักย์ไฟฟ้าที่จุด B (โวลต์)",
                fmt(end),
                # ลืมบวกศักย์ไฟฟ้าต้นทางกลับเข้าไป, คูณแทนหาร, หรือลืมหารด้วยประจุ
                wrongs=slips(fmt(end), gap, work * charge, start + work),
                hint=r"V_B = V_A + \frac{W}{q}")
        return Calc(
            f"ต้องใช้งาน {work} ไมโครจูล ในการเคลื่อนประจุหนึ่งจากจุดที่มีศักย์ไฟฟ้า "
            f"{start} โวลต์ ไปยังจุดที่มีศักย์ไฟฟ้า {end} โวลต์ "
            "ประจุนี้มีขนาดเท่าใด (ไมโครคูลอมบ์)",
            fmt(charge),
            wrongs=slips(fmt(charge), work / end, work / start, work * gap),
            hint=r"q = \frac{W}{V_B - V_A}")
