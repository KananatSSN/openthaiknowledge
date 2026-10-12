"""เคมี — the periodic table and atomic structure, over one table of 118 elements.

Naming a ธาตุ (topic ธาตุและตารางธาตุ):

* ``chem.symbol_to_name``   Na              → โซเดียม (Sodium)
* ``chem.name_to_symbol``   โซเดียม (Sodium) → Na
* ``chem.atomic_number``    Na โซเดียม       → 11

Reading a nuclide symbol (topic โครงสร้างอะตอม) — everything the student needs is
*on show*, so these are notation and arithmetic, not recall:

* ``chem.nuclide``    ²³₁₁Na   → เลขมวล 23 / เลขอะตอม 11
* ``chem.particles``  ²³₁₁Na⁺  → โปรตอน 11 / นิวตรอน 12 / อิเล็กตรอน 10

Which elements may appear is tunable, so a sheet can drill exactly one หมู่ or a
span of them. Groups use the **Thai A-group numbering** (หมู่ 1A–8A ⇒ ``1``…``8``);
transition metals, lanthanides and actinides all share **หมู่ 0** — so
``group_lo=1, group_hi=4`` is หมู่ 1A–4A only, and the default
``group_lo=0, group_hi=8`` is the whole table. ``z_lo``/``z_hi`` narrow by atomic
number on top of that (``z_hi=20`` gives the classic first-twenty set). The two
nuclide types add ``ask`` (pin one fact instead of drawing one per item) and
``chem.particles`` adds ``ion_chance`` (how often an ion, not a neutral atom).

Distractors are always *real* elements from the same slice — a wrong choice is
another element the student is studying, never an invented name. A narrow slice
therefore yields fewer than four choices rather than fake ones. The nuclide types
additionally offer the *near miss* first (เลขอะตอม when เลขมวล was asked, and so
on), because mixing those up is the mistake the item exists to catch.
"""

from __future__ import annotations

from abc import abstractmethod
from random import Random
from typing import Callable, NamedTuple

from otk.core.content import Block
from otk.core.distractors import DistractorStrategy, combine, sibling_answers
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType

SUBJECT = "เคมี"
TOPIC = "ธาตุและตารางธาตุ"
TOPIC_ATOM = "โครงสร้างอะตอม"
TOPIC_MATTER = "สารในชีวิตประจำวัน"        # ป.6 — สสารและการเปลี่ยนแปลง

TRANSITION = 0          # หมู่ 0 here: d-block + lanthanides + actinides
MAX_GROUP = 8           # หมู่ 8A (ก๊าซเฉื่อย)
MAX_Z = 118


class Element(NamedTuple):
    z: int              # atomic number
    symbol: str         # IUPAC symbol, e.g. "Na"
    th: str             # Thai name, e.g. "โซเดียม"
    en: str             # English name, e.g. "Sodium"
    group: int          # หมู่ 1–8 (A groups); TRANSITION for everything else
    mass: int           # เลขมวล A of its most abundant (or most stable) isotope


# The whole table. ``group`` is the Thai A-group number, or TRANSITION (0) for
# the d-block, lanthanides and actinides — those have no หมู่ A.
ELEMENTS: list[Element] = [
    Element(1, "H", "ไฮโดรเจน", "Hydrogen", 1, 1),
    Element(2, "He", "ฮีเลียม", "Helium", 8, 4),
    Element(3, "Li", "ลิเทียม", "Lithium", 1, 7),
    Element(4, "Be", "เบริลเลียม", "Beryllium", 2, 9),
    Element(5, "B", "โบรอน", "Boron", 3, 11),
    Element(6, "C", "คาร์บอน", "Carbon", 4, 12),
    Element(7, "N", "ไนโตรเจน", "Nitrogen", 5, 14),
    Element(8, "O", "ออกซิเจน", "Oxygen", 6, 16),
    Element(9, "F", "ฟลูออรีน", "Fluorine", 7, 19),
    Element(10, "Ne", "นีออน", "Neon", 8, 20),
    Element(11, "Na", "โซเดียม", "Sodium", 1, 23),
    Element(12, "Mg", "แมกนีเซียม", "Magnesium", 2, 24),
    Element(13, "Al", "อะลูมิเนียม", "Aluminium", 3, 27),
    Element(14, "Si", "ซิลิคอน", "Silicon", 4, 28),
    Element(15, "P", "ฟอสฟอรัส", "Phosphorus", 5, 31),
    Element(16, "S", "ซัลเฟอร์", "Sulfur", 6, 32),
    Element(17, "Cl", "คลอรีน", "Chlorine", 7, 35),
    Element(18, "Ar", "อาร์กอน", "Argon", 8, 40),
    Element(19, "K", "โพแทสเซียม", "Potassium", 1, 39),
    Element(20, "Ca", "แคลเซียม", "Calcium", 2, 40),
    Element(21, "Sc", "สแกนเดียม", "Scandium", TRANSITION, 45),
    Element(22, "Ti", "ไทเทเนียม", "Titanium", TRANSITION, 48),
    Element(23, "V", "วาเนเดียม", "Vanadium", TRANSITION, 51),
    Element(24, "Cr", "โครเมียม", "Chromium", TRANSITION, 52),
    Element(25, "Mn", "แมงกานีส", "Manganese", TRANSITION, 55),
    Element(26, "Fe", "เหล็ก", "Iron", TRANSITION, 56),
    Element(27, "Co", "โคบอลต์", "Cobalt", TRANSITION, 59),
    Element(28, "Ni", "นิกเกิล", "Nickel", TRANSITION, 58),
    Element(29, "Cu", "ทองแดง", "Copper", TRANSITION, 63),
    Element(30, "Zn", "สังกะสี", "Zinc", TRANSITION, 64),
    Element(31, "Ga", "แกลเลียม", "Gallium", 3, 69),
    Element(32, "Ge", "เจอร์เมเนียม", "Germanium", 4, 74),
    Element(33, "As", "อาร์เซนิก", "Arsenic", 5, 75),
    Element(34, "Se", "ซีลีเนียม", "Selenium", 6, 80),
    Element(35, "Br", "โบรมีน", "Bromine", 7, 79),
    Element(36, "Kr", "คริปทอน", "Krypton", 8, 84),
    Element(37, "Rb", "รูบิเดียม", "Rubidium", 1, 85),
    Element(38, "Sr", "สตรอนเชียม", "Strontium", 2, 88),
    Element(39, "Y", "อิตเทรียม", "Yttrium", TRANSITION, 89),
    Element(40, "Zr", "เซอร์โคเนียม", "Zirconium", TRANSITION, 90),
    Element(41, "Nb", "ไนโอเบียม", "Niobium", TRANSITION, 93),
    Element(42, "Mo", "โมลิบดีนัม", "Molybdenum", TRANSITION, 98),
    Element(43, "Tc", "เทคนีเชียม", "Technetium", TRANSITION, 98),
    Element(44, "Ru", "รูทีเนียม", "Ruthenium", TRANSITION, 102),
    Element(45, "Rh", "โรเดียม", "Rhodium", TRANSITION, 103),
    Element(46, "Pd", "แพลเลเดียม", "Palladium", TRANSITION, 106),
    Element(47, "Ag", "เงิน", "Silver", TRANSITION, 107),
    Element(48, "Cd", "แคดเมียม", "Cadmium", TRANSITION, 114),
    Element(49, "In", "อินเดียม", "Indium", 3, 115),
    Element(50, "Sn", "ดีบุก", "Tin", 4, 120),
    Element(51, "Sb", "พลวง", "Antimony", 5, 121),
    Element(52, "Te", "เทลลูเรียม", "Tellurium", 6, 130),
    Element(53, "I", "ไอโอดีน", "Iodine", 7, 127),
    Element(54, "Xe", "ซีนอน", "Xenon", 8, 132),
    Element(55, "Cs", "ซีเซียม", "Caesium", 1, 133),
    Element(56, "Ba", "แบเรียม", "Barium", 2, 138),
    Element(57, "La", "แลนทานัม", "Lanthanum", TRANSITION, 139),
    Element(58, "Ce", "ซีเรียม", "Cerium", TRANSITION, 140),
    Element(59, "Pr", "เพรซีโอดิเมียม", "Praseodymium", TRANSITION, 141),
    Element(60, "Nd", "นีโอดิเมียม", "Neodymium", TRANSITION, 142),
    Element(61, "Pm", "โพรมีเทียม", "Promethium", TRANSITION, 145),
    Element(62, "Sm", "ซาแมเรียม", "Samarium", TRANSITION, 152),
    Element(63, "Eu", "ยูโรเพียม", "Europium", TRANSITION, 153),
    Element(64, "Gd", "แกโดลิเนียม", "Gadolinium", TRANSITION, 158),
    Element(65, "Tb", "เทอร์เบียม", "Terbium", TRANSITION, 159),
    Element(66, "Dy", "ดิสโพรเซียม", "Dysprosium", TRANSITION, 164),
    Element(67, "Ho", "โฮลเมียม", "Holmium", TRANSITION, 165),
    Element(68, "Er", "เออร์เบียม", "Erbium", TRANSITION, 166),
    Element(69, "Tm", "ทูเลียม", "Thulium", TRANSITION, 169),
    Element(70, "Yb", "อิตเทอร์เบียม", "Ytterbium", TRANSITION, 174),
    Element(71, "Lu", "ลูทีเทียม", "Lutetium", TRANSITION, 175),
    Element(72, "Hf", "แฮฟเนียม", "Hafnium", TRANSITION, 180),
    Element(73, "Ta", "แทนทาลัม", "Tantalum", TRANSITION, 181),
    Element(74, "W", "ทังสเตน", "Tungsten", TRANSITION, 184),
    Element(75, "Re", "รีเนียม", "Rhenium", TRANSITION, 187),
    Element(76, "Os", "ออสเมียม", "Osmium", TRANSITION, 192),
    Element(77, "Ir", "อิริเดียม", "Iridium", TRANSITION, 193),
    Element(78, "Pt", "แพลทินัม", "Platinum", TRANSITION, 195),
    Element(79, "Au", "ทองคำ", "Gold", TRANSITION, 197),
    Element(80, "Hg", "ปรอท", "Mercury", TRANSITION, 202),
    Element(81, "Tl", "แทลเลียม", "Thallium", 3, 205),
    Element(82, "Pb", "ตะกั่ว", "Lead", 4, 208),
    Element(83, "Bi", "บิสมัท", "Bismuth", 5, 209),
    Element(84, "Po", "พอโลเนียม", "Polonium", 6, 209),
    Element(85, "At", "แอสทาทีน", "Astatine", 7, 210),
    Element(86, "Rn", "เรดอน", "Radon", 8, 222),
    Element(87, "Fr", "แฟรนเซียม", "Francium", 1, 223),
    Element(88, "Ra", "เรเดียม", "Radium", 2, 226),
    Element(89, "Ac", "แอกทิเนียม", "Actinium", TRANSITION, 227),
    Element(90, "Th", "ทอเรียม", "Thorium", TRANSITION, 232),
    Element(91, "Pa", "โพรแทกทิเนียม", "Protactinium", TRANSITION, 231),
    Element(92, "U", "ยูเรเนียม", "Uranium", TRANSITION, 238),
    Element(93, "Np", "เนปทูเนียม", "Neptunium", TRANSITION, 237),
    Element(94, "Pu", "พลูโทเนียม", "Plutonium", TRANSITION, 244),
    Element(95, "Am", "อะเมริเซียม", "Americium", TRANSITION, 243),
    Element(96, "Cm", "คูเรียม", "Curium", TRANSITION, 247),
    Element(97, "Bk", "เบอร์คีเลียม", "Berkelium", TRANSITION, 247),
    Element(98, "Cf", "แคลิฟอร์เนียม", "Californium", TRANSITION, 251),
    Element(99, "Es", "ไอน์สไตเนียม", "Einsteinium", TRANSITION, 252),
    Element(100, "Fm", "เฟอร์เมียม", "Fermium", TRANSITION, 257),
    Element(101, "Md", "เมนเดลีเวียม", "Mendelevium", TRANSITION, 258),
    Element(102, "No", "โนเบเลียม", "Nobelium", TRANSITION, 259),
    Element(103, "Lr", "ลอว์เรนเซียม", "Lawrencium", TRANSITION, 266),
    Element(104, "Rf", "รัทเทอร์ฟอร์เดียม", "Rutherfordium", TRANSITION, 267),
    Element(105, "Db", "ดุบเนียม", "Dubnium", TRANSITION, 268),
    Element(106, "Sg", "ซีบอร์เกียม", "Seaborgium", TRANSITION, 269),
    Element(107, "Bh", "โบห์เรียม", "Bohrium", TRANSITION, 270),
    Element(108, "Hs", "ฮัสเซียม", "Hassium", TRANSITION, 269),
    Element(109, "Mt", "ไมต์เนเรียม", "Meitnerium", TRANSITION, 278),
    Element(110, "Ds", "ดาร์มสตัดเทียม", "Darmstadtium", TRANSITION, 281),
    Element(111, "Rg", "เรินต์เกเนียม", "Roentgenium", TRANSITION, 282),
    Element(112, "Cn", "โคเปอร์นิเซียม", "Copernicium", TRANSITION, 285),
    Element(113, "Nh", "นิโฮเนียม", "Nihonium", 3, 286),
    Element(114, "Fl", "ฟลีโรเวียม", "Flerovium", 4, 289),
    Element(115, "Mc", "มอสโกเวียม", "Moscovium", 5, 290),
    Element(116, "Lv", "ลิเวอร์มอเรียม", "Livermorium", 6, 293),
    Element(117, "Ts", "เทนเนสซีน", "Tennessine", 7, 294),
    Element(118, "Og", "ออกาเนสซอน", "Oganesson", 8, 294),
]


def element_pool(group_lo: int = TRANSITION, group_hi: int = MAX_GROUP,
                 z_lo: int = 1, z_hi: int = MAX_Z) -> list[Element]:
    """The elements a question may draw from, given a หมู่ and เลขอะตอม window.

    Bounds are inclusive and order-insensitive (swapped bounds are sorted), so a
    single หมู่ is ``group_lo == group_hi``.
    """
    g_lo, g_hi = sorted((int(group_lo), int(group_hi)))
    z0, z1 = sorted((int(z_lo), int(z_hi)))
    pool = [e for e in ELEMENTS if g_lo <= e.group <= g_hi and z0 <= e.z <= z1]
    if not pool:
        raise ValueError(
            f"no elements in groups {g_lo}–{g_hi} with atomic number {z0}–{z1}")
    return pool


# ── หมู่ (IUPAC group 1–18) ────────────────────────────────────────────────────
# Main-group elements carry their Thai A-group (1–8) in ``Element.group``; the
# d-block transition metals are all TRANSITION there, so their หมู่ (IUPAC 3–12)
# is listed out here by symbol. The f-block (lanthanides/actinides) has no simple
# หมู่ and is left out of the หมู่ drills entirely.
DBLOCK_GROUP: dict[str, int] = {
    "Sc": 3, "Ti": 4, "V": 5, "Cr": 6, "Mn": 7, "Fe": 8, "Co": 9, "Ni": 10, "Cu": 11, "Zn": 12,
    "Y": 3, "Zr": 4, "Nb": 5, "Mo": 6, "Tc": 7, "Ru": 8, "Rh": 9, "Pd": 10, "Ag": 11, "Cd": 12,
    "La": 3, "Hf": 4, "Ta": 5, "W": 6, "Re": 7, "Os": 8, "Ir": 9, "Pt": 10, "Au": 11, "Hg": 12,
    "Ac": 3, "Rf": 4, "Db": 5, "Sg": 6, "Bh": 7, "Hs": 8, "Mt": 9, "Ds": 10, "Rg": 11, "Cn": 12,
}


def iupac_group(el: Element) -> int | None:
    """หมู่ as an IUPAC number 1–18, or ``None`` for the f-block (no simple หมู่).

    A-group numbers map straight across — 1A–2A → 1–2, 3A–8A → 13–18 — and the
    d-block transition metals come from :data:`DBLOCK_GROUP`.
    """
    if el.symbol in DBLOCK_GROUP:
        return DBLOCK_GROUP[el.symbol]
    if el.group == TRANSITION:
        return None
    return el.group if el.group <= 2 else el.group + 10


# ── Ions ─────────────────────────────────────────────────────────────────────
# The หมู่ rule as taught: an A-group element gains or loses electrons to reach a
# full outer shell. หมู่ 4A and 8A (and the f-block) form no simple ion here.
GROUP_CHARGES: dict[int, tuple[int, ...]] = {
    1: (1,), 2: (2,), 3: (3,), 5: (-3,), 6: (-2,), 7: (-1,),
}

# Familiar metal ions the หมู่ rule cannot give — the d-block, plus Sn/Pb, whose
# หมู่ (4A) has no rule. Keyed by symbol, and they win over the หมู่ rule.
METAL_CHARGES: dict[str, tuple[int, ...]] = {
    "Cr": (3,), "Mn": (2,), "Fe": (2, 3), "Co": (2,), "Ni": (2,), "Cu": (1, 2),
    "Zn": (2,), "Ag": (1,), "Cd": (2,), "Sn": (2, 4), "Pt": (2, 4),
    "Au": (1, 3), "Hg": (1, 2), "Pb": (2, 4),
}


def common_charges(el: Element) -> tuple[int, ...]:
    """Ion charges this element is drilled with — empty if it forms no simple ion."""
    return METAL_CHARGES.get(el.symbol) or GROUP_CHARGES.get(el.group, ())


# ── TeX ──────────────────────────────────────────────────────────────────────

def symbol_tex(el: Element) -> str:
    r"""Upright TeX for a symbol — ``\mathrm`` so Na isn't italicized as N·a."""
    return rf"\mathrm{{{el.symbol}}}"


def nuclide_tex(el: Element, charge: int = 0) -> str:
    r"""Nuclide notation ᴬ_Z X, e.g. ``{}^{23}_{11}\mathrm{Na}^{+}``.

    The leading empty group is the base the prescripts hang off — both KaTeX and
    matplotlib's mathtext need one before ``^``/``_``.
    """
    ion = ""
    if charge:
        size = abs(charge) if abs(charge) > 1 else ""
        # The sign gets its own group so it stays an ordinary atom: bare "3-" is
        # a binary minus, which both engines set with a gap in front of it.
        ion = f"^{{{size}{{{'+' if charge > 0 else '-'}}}}}"
    return rf"{{}}^{{{el.mass}}}_{{{el.z}}}{symbol_tex(el)}{ion}"


def full_name(el: Element) -> str:
    """The Thai name with the English one alongside, e.g. 'โซเดียม (Sodium)'."""
    return f"{el.th} ({el.en})"


# ── Items ────────────────────────────────────────────────────────────────────

ONE_ASK: tuple[str, ...] = ("",)


class Item(NamedTuple):
    """One drawn question: an element, the fact asked of it, and the ion shown."""
    el: Element
    ask: str = ""
    charge: int = 0             # 0 = a neutral atom


def fixed(*contents: list[Block]) -> DistractorStrategy:
    """Hand-picked distractors, offered before the sampled ones."""
    def strategy(correct: list[Block], rng: Random, need: int) -> list[list[Block]]:
        return list(contents[:need])
    return strategy


class ElementType(QuestionType):
    """Base: draw one element from the selected slice, ask one thing about it.

    Subclasses say what the stem asks (:meth:`stem`), what a choice looks like
    (:meth:`answer`), and optionally which near misses to offer first
    (:meth:`alternates`). Sampled distractors are :meth:`answer` for *other*
    elements of the same slice, so they are always real and always in range.

    A type with several :attr:`ASKS` picks one per item and holds it fixed for
    the distractors too — every choice answers the same question.
    """

    ASKS: tuple[str, ...] = ONE_ASK

    @abstractmethod
    def stem(self, it: Item) -> list[Block]:
        """The question, as blocks."""

    @abstractmethod
    def answer(self, it: Item) -> list[Block]:
        """One choice's content — the correct one for ``it``."""

    def alternates(self, it: Item) -> list[list[Block]]:
        """Near-miss choices for this item, offered before the sampled ones."""
        return []

    def ask_for(self, rng: Random, ask: int) -> str:
        """``1..n`` pins ``ASKS[n - 1]``; ``0`` (or out of range) draws one."""
        i = int(ask)
        return self.ASKS[i - 1] if 1 <= i <= len(self.ASKS) else rng.choice(self.ASKS)

    def question(self, draw: Callable[[], Item]) -> GeneratedQuestion:
        """Assemble one question; ``draw`` is re-called for each distractor."""
        it = draw()
        return GeneratedQuestion(
            stem=self.stem(it),
            correct=self.answer(it),
            distractors=combine(fixed(*self.alternates(it)),
                                sibling_answers(lambda: self.answer(draw()))),
            topic=self.topic,
        )

    def build(self, rng: Random, group_lo: int = TRANSITION,
              group_hi: int = MAX_GROUP, z_lo: int = 1,
              z_hi: int = MAX_Z) -> GeneratedQuestion:
        pool = element_pool(group_lo, group_hi, z_lo, z_hi)
        return self.question(lambda: Item(rng.choice(pool), self.ASKS[0]))


# ── โครงสร้างอะตอม: reading the nuclide symbol ────────────────────────────────


# ── ตารางธาตุ: หมู่ ────────────────────────────────────────────────────────────
# One slice of the table per type. The three A/d/p bands read very differently —
# a หมู่ 1–2 item has two possible answers, a d-block item has ten — so they are
# kept apart rather than merged into one control-heavy type.


# ══ สสารและการเปลี่ยนแปลง — สารในชีวิตประจำวัน (ป.6) ═══════════════════════════
# Classify-by-category types over Thai data tables (see ._classify). Each ชุดโจทย์
# is one section of the ป.6 เคมี curriculum: state a property/example and name the
# category it belongs to, or name a category and pick an example of it.


# ══ การแยกสารเนื้อผสมอย่างง่าย (ป.6) ═══════════════════════════════════════════
# สารเนื้อผสม = ส่วนผสมที่มองเห็นเนื้อสารไม่กลมกลืนกัน แยกได้ด้วยสมบัติทางกายภาพ
# (ขนาด น้ำหนัก การละลาย การถูกแม่เหล็กดูด) โดยไม่เกิดสารใหม่. ต่างจาก chem.separation
# ข้างบนที่รวมการกลั่น/โครมาโทกราฟีของสารละลายด้วย — ชุดนี้เจาะจงระดับ ป.6.


