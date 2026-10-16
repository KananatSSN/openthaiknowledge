"""Specs for the biology and Earth-science diagrams: Earth's interior, food webs, cells.

Each spec names one picture that ``otk.pictures.life_earth_pictures`` draws. The
pictures carry only numbers and Latin letters; every Thai name a question needs
is in its stem or choices, as with the other science diagrams.
"""

from __future__ import annotations

from itertools import permutations
from typing import NamedTuple


# ── โครงสร้างภายในโลก (ว 3.2 ม.2/4) ───────────────────────────────────────────

#: The three chemical layers, outermost first.
EARTH_LAYERS = ("เปลือกโลก", "เนื้อโลก", "แก่นโลก")


class EarthSectionSpec(NamedTuple):
    """A cut-away Earth whose three layers carry the numbers in ``numbers``.

    ``numbers[i]`` is the label on ``EARTH_LAYERS[i]``, so the same drawing is
    not always numbered outside-in and the answer is not read off position.
    """
    numbers: tuple[int, int, int]

    @property
    def asset_id(self) -> str:
        return "earth_section_" + "".join(map(str, self.numbers))

    def layer_of(self, number: int) -> str:
        return EARTH_LAYERS[self.numbers.index(number)]


EARTH_SECTIONS = tuple(EarthSectionSpec(p) for p in permutations((1, 2, 3)))


EARTH_SECTION_ALT = ("ภาพตัดครึ่งโลกแสดงชั้นสามชั้นเป็นวงซ้อนกัน แต่ละชั้นมีหมายเลขกำกับ "
                     "ความหนาของชั้นนอกสุดถูกขยายให้มองเห็นได้")


# ── สายใยอาหาร (ว 1.1 ม.3/3) ──────────────────────────────────────────────────

class Organism(NamedTuple):
    letter: str
    name: str
    eats: tuple[str, ...]      # letters of what it eats; () for a producer
    x: float
    y: float


class FoodWebSpec(NamedTuple):
    """One food web: its place, and each organism with its letter and position.

    Arrows run from the food to the eater, the direction energy moves.
    """
    key: str
    place: str
    organisms: tuple[Organism, ...]

    @property
    def asset_id(self) -> str:
        return f"food_web_{self.key}"

    def by_letter(self, letter: str) -> Organism:
        return next(o for o in self.organisms if o.letter == letter)

    def producers(self) -> list[Organism]:
        return [o for o in self.organisms if not o.eats]

    def eaters_of(self, letter: str) -> list[Organism]:
        return [o for o in self.organisms if letter in o.eats]

    def tops(self) -> list[Organism]:
        return [o for o in self.organisms if o.eats and not self.eaters_of(o.letter)]

    def chains(self) -> list[tuple[str, ...]]:
        """Every path from a producer to an organism nothing eats."""
        found: list[tuple[str, ...]] = []

        def walk(path: tuple[str, ...]) -> None:
            nxt = self.eaters_of(path[-1])
            if not nxt:
                found.append(path)
            for o in nxt:
                walk(path + (o.letter,))

        for producer in self.producers():
            walk((producer.letter,))
        return found


FOOD_WEBS = (
    FoodWebSpec("field", "ทุ่งนา", (
        Organism("A", "ต้นข้าว", (), 0.25, 0.12),
        Organism("B", "หญ้า", (), 0.75, 0.12),
        Organism("C", "หนู", ("A",), 0.15, 0.45),
        Organism("D", "ตั๊กแตน", ("A", "B"), 0.55, 0.40),
        Organism("E", "กบ", ("D",), 0.80, 0.62),
        Organism("F", "งู", ("C", "E"), 0.40, 0.70),
        Organism("G", "เหยี่ยว", ("F", "C"), 0.30, 0.92),
    )),
    FoodWebSpec("pond", "บึงน้ำจืด", (
        Organism("A", "สาหร่าย", (), 0.50, 0.12),
        Organism("B", "ไรน้ำ", ("A",), 0.25, 0.40),
        Organism("C", "ลูกน้ำยุง", ("A",), 0.75, 0.40),
        Organism("D", "ปลาเล็ก", ("B", "C"), 0.30, 0.68),
        Organism("E", "ตัวอ่อนแมลงปอ", ("C",), 0.80, 0.70),
        Organism("F", "นกกระเต็น", ("D", "E"), 0.55, 0.92),
    )),
    FoodWebSpec("forest", "ป่าดิบ", (
        Organism("A", "ต้นไม้", (), 0.50, 0.12),
        Organism("B", "หนอนผีเสื้อ", ("A",), 0.22, 0.40),
        Organism("C", "กระรอก", ("A",), 0.78, 0.40),
        Organism("D", "นกกินแมลง", ("B",), 0.22, 0.68),
        Organism("E", "งู", ("C", "D"), 0.62, 0.68),
        Organism("F", "เหยี่ยว", ("E", "C"), 0.50, 0.92),
    )),
    FoodWebSpec("sea", "ทะเล", (
        Organism("A", "แพลงก์ตอนพืช", (), 0.50, 0.12),
        Organism("B", "แพลงก์ตอนสัตว์", ("A",), 0.22, 0.40),
        Organism("C", "กุ้ง", ("A",), 0.78, 0.40),
        Organism("D", "ปลาเล็ก", ("B",), 0.25, 0.68),
        Organism("E", "หมึก", ("C", "D"), 0.70, 0.68),
        Organism("F", "ฉลาม", ("E", "D"), 0.50, 0.92),
    )),
)


FOOD_WEB_ALT = ("แผนภาพสายใยอาหาร สิ่งมีชีวิตแทนด้วยตัวอักษรภาษาอังกฤษ "
                "ลูกศรชี้จากสิ่งที่ถูกกินไปยังผู้กิน")


# ── เซลล์พืชและเซลล์สัตว์ (ว 1.2 ม.1/1) ───────────────────────────────────────

WALL = "ผนังเซลล์"
MEMBRANE = "เยื่อหุ้มเซลล์"
NUCLEUS = "นิวเคลียส"
CHLOROPLAST = "คลอโรพลาสต์"
VACUOLE = "แวคิวโอล"
CYTOPLASM = "ไซโทพลาซึม"

PLANT_PARTS = (WALL, MEMBRANE, NUCLEUS, CHLOROPLAST, VACUOLE, CYTOPLASM)
ANIMAL_PARTS = (MEMBRANE, NUCLEUS, CYTOPLASM)


class CellSpec(NamedTuple):
    """A plant or an animal cell with its parts numbered in a given order.

    ``labelled`` lists the parts in the order of the numbers 1, 2, 3, ...
    """
    kind: str               # "plant" | "animal"
    labelled: tuple[str, ...]

    @property
    def asset_id(self) -> str:
        order = "".join(str(PLANT_PARTS.index(p)) for p in self.labelled)
        return f"cell_{self.kind}_{order}"

    def number_of(self, part: str) -> int:
        return self.labelled.index(part) + 1


CELL_DIAGRAMS = (
    CellSpec("plant", (WALL, MEMBRANE, NUCLEUS, CHLOROPLAST, VACUOLE, CYTOPLASM)),
    CellSpec("plant", (CHLOROPLAST, VACUOLE, WALL, CYTOPLASM, NUCLEUS, MEMBRANE)),
    CellSpec("plant", (NUCLEUS, WALL, VACUOLE, MEMBRANE, CYTOPLASM, CHLOROPLAST)),
    CellSpec("animal", (MEMBRANE, NUCLEUS, CYTOPLASM)),
    CellSpec("animal", (NUCLEUS, CYTOPLASM, MEMBRANE)),
    CellSpec("animal", (CYTOPLASM, MEMBRANE, NUCLEUS)),
)


CELL_ALT = ("ภาพวาดเซลล์หนึ่งเซลล์ มีเส้นชี้ไปยังส่วนต่าง ๆ ของเซลล์ "
            "แต่ละเส้นมีหมายเลขกำกับ")


# ── ชั้นหน้าตัดดิน (ว 3.2 ม.2/6) ──────────────────────────────────────────────

#: The horizons top to bottom, as in ``soil_profile.HORIZONS``.
SOIL_HORIZONS = ("ชั้นโอ", "ชั้นเอ", "ชั้นบี", "ชั้นซี", "ชั้นอาร์")


class SoilProfileSpec(NamedTuple):
    """A soil profile whose horizons, top to bottom, carry ``numbers``."""
    numbers: tuple[int, int, int, int, int]

    @property
    def asset_id(self) -> str:
        return "soil_profile_" + "".join(map(str, self.numbers))

    def horizon_of(self, number: int) -> str:
        return SOIL_HORIZONS[self.numbers.index(number)]


SOIL_PROFILES = tuple(SoilProfileSpec(n) for n in (
    (1, 2, 3, 4, 5), (5, 4, 3, 2, 1), (3, 1, 4, 5, 2), (2, 5, 1, 3, 4),
))


SOIL_PROFILE_ALT = ("ภาพหน้าตัดดินแสดงชั้นห้าชั้นซ้อนกันจากผิวดินลงไปถึงหินพื้น "
                    "แต่ละชั้นมีลวดลายต่างกันและมีหมายเลขกำกับ")


# ── วัฏจักรน้ำ (ว 3.2 ป.5/3) ───────────────────────────────────────────────────

#: The processes in cycle order, as in ``water_cycle.STEPS``.
WATER_STEPS = ("การระเหย", "การควบแน่น", "หยาดน้ำฟ้า", "การไหลกลับสู่แหล่งน้ำ")


class WaterCycleSpec(NamedTuple):
    """The cycle drawn as sea, cloud and hill, with ``numbers`` on the four arrows in step order."""
    numbers: tuple[int, int, int, int]

    @property
    def asset_id(self) -> str:
        return "water_cycle_" + "".join(map(str, self.numbers))

    def step_of(self, number: int) -> str:
        return WATER_STEPS[self.numbers.index(number)]


WATER_CYCLES = tuple(WaterCycleSpec(n) for n in (
    (1, 2, 3, 4), (3, 1, 4, 2), (2, 4, 1, 3), (4, 3, 2, 1),
))


WATER_CYCLE_ALT = ("ภาพวัฏจักรน้ำ มีดวงอาทิตย์ ทะเล เมฆ และภูเขา "
                   "ลูกศรสี่เส้นแสดงการเคลื่อนที่ของน้ำ แต่ละเส้นมีหมายเลขกำกับ")


# ── โครงสร้างดอก (ว 1.2 ม.1/12) ───────────────────────────────────────────────

#: The parts as in ``flowers_fruits_and_seeds.FLOWER_PARTS``.
FLOWER_PART_NAMES = ("กลีบเลี้ยง", "กลีบดอก", "อับเรณู", "ก้านชูอับเรณู",
                     "ยอดเกสรเพศเมีย", "ก้านเกสรเพศเมีย", "รังไข่", "ออวุล")


class FlowerSpec(NamedTuple):
    """A flower cut lengthways; ``labelled`` gives the parts for the numbers 1, 2, 3, ..."""
    labelled: tuple[str, ...]

    @property
    def asset_id(self) -> str:
        return "flower_" + "".join(str(FLOWER_PART_NAMES.index(p)) for p in self.labelled)

    def number_of(self, part: str) -> int:
        return self.labelled.index(part) + 1


FLOWERS = tuple(FlowerSpec(tuple(FLOWER_PART_NAMES[i] for i in order)) for order in (
    (0, 1, 2, 3, 4, 5, 6, 7), (4, 2, 7, 0, 5, 1, 6, 3), (6, 3, 1, 5, 0, 7, 2, 4),
))


FLOWER_ALT = ("ภาพตัดตามยาวของดอกไม้ แสดงส่วนต่าง ๆ ของดอก "
              "มีเส้นชี้แต่ละส่วนพร้อมหมายเลขกำกับ")


# ── โซ่อาหาร (ว 1.1 ป.5/3) ────────────────────────────────────────────────────

class ChainSpec(NamedTuple):
    """Four lettered circles at fixed places; ``order`` gives the letters from producer up.

    The circles are not drawn in a line, so the order has to be followed along
    the arrows rather than read left to right.
    """
    order: tuple[str, str, str, str]

    @property
    def asset_id(self) -> str:
        return "food_chain_" + "".join(self.order).lower()


#: Where each letter's circle sits, the same in every chain picture.
CHAIN_PLACES = {"A": (0.22, 0.75), "B": (0.78, 0.75), "C": (0.22, 0.25), "D": (0.78, 0.25)}


FOOD_CHAIN_PICTURES = tuple(ChainSpec(tuple(o)) for o in (
    "CABD", "DBCA", "BDAC", "ACDB", "CDBA", "BADC",
))


FOOD_CHAIN_ALT = ("แผนภาพโซ่อาหาร สิ่งมีชีวิตสี่ชนิดแทนด้วยตัวอักษร A B C D "
                  "ลูกศรชี้จากสิ่งที่ถูกกินไปยังผู้กิน")


# ── วัฏจักรหิน (ว 3.2 ป.6/1) ──────────────────────────────────────────────────

#: The five stages the rock-cycle arrows join, as in ``ROCK_CYCLE_ARROWS``.
ROCK_STAGES = ("แมกมา", "หินอัคนี", "ตะกอน", "หินตะกอน", "หินแปร")


#: Where each stage sits, by its index in ``ROCK_STAGES``: a ring, magma at the foot.
ROCK_PLACES = ((0.50, 0.12), (0.12, 0.45), (0.30, 0.88), (0.70, 0.88), (0.88, 0.45))


class RockCycleSpec(NamedTuple):
    """The cycle with lettered stages and numbered arrows.

    ``letters[i]`` labels ``ROCK_STAGES[i]``; ``numbers[j]`` labels arrow j of
    ``ROCK_CYCLE_ARROWS``. Both change between pictures.
    """
    letters: tuple[str, str, str, str, str]
    numbers: tuple[int, int, int, int, int, int]

    @property
    def asset_id(self) -> str:
        return ("rock_cycle_" + "".join(self.letters).lower() + "_"
                + "".join(map(str, self.numbers)))


ROCK_CYCLES = (
    RockCycleSpec(("A", "B", "C", "D", "E"), (1, 2, 3, 4, 5, 6)),
    RockCycleSpec(("C", "E", "A", "B", "D"), (4, 1, 6, 2, 3, 5)),
    RockCycleSpec(("E", "C", "D", "A", "B"), (6, 5, 2, 1, 4, 3)),
    RockCycleSpec(("B", "D", "E", "C", "A"), (3, 6, 1, 5, 2, 4)),
)


ROCK_CYCLE_ALT = ("แผนภาพวัฏจักรหิน มีห้าส่วนแทนด้วยตัวอักษร "
                  "และลูกศรหกเส้นแสดงการเปลี่ยนแปลง แต่ละเส้นมีหมายเลขกำกับ")


# ── แนวรอยต่อของแผ่นธรณี (ว 3.2 ม.6/3) ────────────────────────────────────────

#: The boundaries as in ``plate_boundary.BOUNDARIES``.
BOUNDARY_NAMES = ("แนวแผ่นธรณีแยกตัว", "แนวแผ่นธรณีเคลื่อนที่เข้าหากัน", "แนวแผ่นธรณีเคลื่อนที่ผ่านกัน")


class PlateSpec(NamedTuple):
    """One boundary drawn as a cut-away (or, for sliding plates, from above), maybe mirrored."""
    boundary: str
    mirrored: bool

    @property
    def asset_id(self) -> str:
        kind = ("diverge", "converge", "transform")[BOUNDARY_NAMES.index(self.boundary)]
        return f"plate_{kind}" + ("_m" if self.mirrored else "")


PLATE_PICTURES = tuple(PlateSpec(b, m) for b in BOUNDARY_NAMES for m in (False, True))


PLATE_ALT = ("ภาพแสดงแผ่นธรณีสองแผ่นบริเวณรอยต่อ มีลูกศรบอกทิศทางที่แผ่นธรณีเคลื่อนที่")


# ── หัวใจและการหมุนเวียนเลือด (ว 1.2 ม.2/7) ──────────────────────────────────

RIGHT_ATRIUM = "หัวใจห้องบนขวา"
RIGHT_VENTRICLE = "หัวใจห้องล่างขวา"
LEFT_ATRIUM = "หัวใจห้องบนซ้าย"
LEFT_VENTRICLE = "หัวใจห้องล่างซ้าย"
CHAMBERS = (RIGHT_ATRIUM, RIGHT_VENTRICLE, LEFT_ATRIUM, LEFT_VENTRICLE)


class HeartSpec(NamedTuple):
    """The heart's four chambers numbered by ``numbers`` (in ``CHAMBERS`` order),
    drawn as seen from the front, so the body's right side is on the picture's left."""
    numbers: tuple[int, int, int, int]

    @property
    def asset_id(self) -> str:
        return "heart_" + "".join(map(str, self.numbers))

    def chamber_of(self, number: int) -> str:
        return CHAMBERS[self.numbers.index(number)]


HEARTS = tuple(HeartSpec(n) for n in ((1, 2, 3, 4), (3, 1, 4, 2), (2, 4, 1, 3), (4, 3, 2, 1)))


HEART_ALT = ("แผนภาพหัวใจสี่ห้องมองจากด้านหน้า ด้านซ้ายของภาพคือซีกขวาของร่างกาย "
             "มีปอดอยู่ด้านบนและส่วนต่าง ๆ ของร่างกายอยู่ด้านล่าง ลูกศรแสดงทิศทางการไหลของเลือด "
             "ห้องหัวใจแต่ละห้องมีหมายเลขกำกับ")


# ── ระบบย่อยอาหาร (ว 1.2 ป.6/4) ───────────────────────────────────────────────

#: The organs as in ``digestive_system.DIGESTIVE_ORGANS``.
DIGESTIVE_NAMES = ("ปาก", "หลอดอาหาร", "กระเพาะอาหาร", "ลำไส้เล็ก", "ลำไส้ใหญ่", "ตับ")


class DigestiveSpec(NamedTuple):
    """The digestive organs numbered by ``numbers`` (in ``DIGESTIVE_NAMES`` order)."""
    numbers: tuple[int, int, int, int, int, int]

    @property
    def asset_id(self) -> str:
        return "digestive_" + "".join(map(str, self.numbers))

    def organ_of(self, number: int) -> str:
        return DIGESTIVE_NAMES[self.numbers.index(number)]


DIGESTIVE_PICTURES = tuple(DigestiveSpec(n) for n in (
    (1, 2, 3, 4, 5, 6), (4, 6, 1, 3, 2, 5), (6, 3, 5, 1, 4, 2),
))


DIGESTIVE_ALT = ("ภาพระบบย่อยอาหารของมนุษย์อย่างง่าย แสดงอวัยวะหกส่วน "
                 "มีเส้นชี้แต่ละอวัยวะพร้อมหมายเลขกำกับ")


# ── อวัยวะในระบบหายใจ (ว 1.2 ม.2/1) ──────────────────────────────────────────

#: The parts drawn, a subset of ``respiratory.ORGANS``.
BREATHING_PARTS = ("จมูก", "หลอดลม", "หลอดลมฝอย", "ปอด", "กะบังลม")


class BreathingSpec(NamedTuple):
    """The airway and lungs with ``numbers`` on the parts, in ``BREATHING_PARTS`` order."""
    numbers: tuple[int, int, int, int, int]

    @property
    def asset_id(self) -> str:
        return "breathing_" + "".join(map(str, self.numbers))

    def part_of(self, number: int) -> str:
        return BREATHING_PARTS[self.numbers.index(number)]


BREATHING_PICTURES = tuple(BreathingSpec(n) for n in (
    (1, 2, 3, 4, 5), (3, 5, 1, 2, 4), (5, 1, 4, 3, 2),
))


BREATHING_ALT = ("ภาพระบบหายใจของมนุษย์อย่างง่าย แสดงจมูก ทางเดินหายใจ ปอดทั้งสองข้าง "
                 "และกล้ามเนื้อใต้ปอด แต่ละส่วนมีหมายเลขกำกับ")


# ── หน้าที่ของราก ลำต้น ใบ และดอก (ว 1.2 ป.4/1) ───────────────────────────────

PLANT_ORGANS = ("ราก", "ลำต้น", "ใบ", "ดอก")


class PlantSpec(NamedTuple):
    """A flowering plant with ``numbers`` on root, stem, leaf and flower."""
    numbers: tuple[int, int, int, int]

    @property
    def asset_id(self) -> str:
        return "plant_organs_" + "".join(map(str, self.numbers))

    def organ_of(self, number: int) -> str:
        return PLANT_ORGANS[self.numbers.index(number)]


PLANT_PICTURES = tuple(PlantSpec(n) for n in ((1, 2, 3, 4), (4, 3, 2, 1), (2, 4, 1, 3), (3, 1, 4, 2)))


PLANT_ALT = "ภาพต้นพืชดอกหนึ่งต้นในกระถาง มีเส้นชี้ส่วนต่าง ๆ ของต้นพร้อมหมายเลขกำกับ"


# ── ลำดับชั้นหินและซากดึกดำบรรพ์ (ว 3.2 ป.6/3) ────────────────────────────────

class LayersSpec(NamedTuple):
    """Four flat rock layers; ``letters`` names them from the bottom up."""
    letters: tuple[str, str, str, str]

    @property
    def asset_id(self) -> str:
        return "rock_layers_" + "".join(self.letters).lower()


ROCK_LAYERS = tuple(LayersSpec(tuple(o)) for o in ("ABCD", "DCBA", "CADB", "BDAC", "DACB"))


ROCK_LAYERS_ALT = ("ภาพหน้าตัดชั้นหินตะกอนสี่ชั้นที่วางตัวในแนวราบซ้อนกัน "
                   "แต่ละชั้นมีตัวอักษรกำกับ")
