"""Wave F slice 27 — เคมีเพิ่มเติม 1: naming organic compounds, structural
isomers, and boiling point and solubility.

Three ``additional_outcome`` indicators, each filed whole:

* ``เคมีเพิ่มเติม 1 ม.6/4`` — IUPAC names of compounds with at most one
  functional group;
* ``เคมีเพิ่มเติม 1 ม.6/5`` — structural isomers;
* ``เคมีเพิ่มเติม 1 ม.6/6`` — boiling point and solubility in water against
  functional group, size and shape.

One bank of compounds serves all three: each has its Thai IUPAC name, a
condensed formula (the molecular formula is parsed from it, never typed), its
class, and a measured boiling point where the textbook gives one.
"""

from __future__ import annotations

import re
from functools import lru_cache

SUBJECT = "เคมี"
UPPER_SIX = {"th": "ม.6"}

SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
UNSUB = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")

ALKANE, ALKENE, ALKYNE, HALO = "แอลเคน", "แอลคีน", "แอลไคน์", "แฮโลแอลเคน"
ALCOHOL, ETHER, ALDEHYDE, KETONE = "แอลกอฮอล์", "อีเทอร์", "แอลดีไฮด์", "คีโตน"
ACID, ESTER, AMINE, AMIDE = "กรดคาร์บอกซิลิก", "เอสเทอร์", "เอมีน", "เอไมด์"

# (Thai IUPAC name, condensed formula, class, straight chain, boiling point °C or None)
COMPOUNDS = (
    ("มีเทน", "CH₄", ALKANE, True, -162), ("อีเทน", "CH₃CH₃", ALKANE, True, -89),
    ("โพรเพน", "CH₃CH₂CH₃", ALKANE, True, -42), ("บิวเทน", "CH₃CH₂CH₂CH₃", ALKANE, True, -1),
    ("เพนเทน", "CH₃(CH₂)₃CH₃", ALKANE, True, 36), ("เฮกเซน", "CH₃(CH₂)₄CH₃", ALKANE, True, 69),
    ("เฮปเทน", "CH₃(CH₂)₅CH₃", ALKANE, True, 98),
    ("2-เมทิลโพรเพน", "CH₃CH(CH₃)CH₃", ALKANE, False, -12),
    ("2-เมทิลบิวเทน", "CH₃CH(CH₃)CH₂CH₃", ALKANE, False, 28),
    ("2,2-ไดเมทิลโพรเพน", "CH₃C(CH₃)₂CH₃", ALKANE, False, 10),
    ("2-เมทิลเพนเทน", "CH₃CH(CH₃)CH₂CH₂CH₃", ALKANE, False, 60),
    ("3-เมทิลเพนเทน", "CH₃CH₂CH(CH₃)CH₂CH₃", ALKANE, False, 63),
    ("2,2-ไดเมทิลบิวเทน", "CH₃C(CH₃)₂CH₂CH₃", ALKANE, False, 50),
    ("2,3-ไดเมทิลบิวเทน", "CH₃CH(CH₃)CH(CH₃)CH₃", ALKANE, False, 58),
    ("อีทีน", "CH₂=CH₂", ALKENE, True, None), ("โพรพีน", "CH₂=CHCH₃", ALKENE, True, None),
    ("บิวต์-1-อีน", "CH₂=CHCH₂CH₃", ALKENE, True, None), ("บิวต์-2-อีน", "CH₃CH=CHCH₃", ALKENE, True, None),
    ("2-เมทิลโพรพีน", "CH₂=C(CH₃)CH₃", ALKENE, False, None),
    ("เพนต์-1-อีน", "CH₂=CHCH₂CH₂CH₃", ALKENE, True, None), ("เพนต์-2-อีน", "CH₃CH=CHCH₂CH₃", ALKENE, True, None),
    ("เอไทน์", "HC≡CH", ALKYNE, True, None), ("โพรไพน์", "HC≡CCH₃", ALKYNE, True, None),
    ("บิวต์-1-ไอน์", "HC≡CCH₂CH₃", ALKYNE, True, None), ("บิวต์-2-ไอน์", "CH₃C≡CCH₃", ALKYNE, True, None),
    ("คลอโรมีเทน", "CH₃Cl", HALO, True, None), ("คลอโรอีเทน", "CH₃CH₂Cl", HALO, True, None),
    ("1-คลอโรโพรเพน", "CH₃CH₂CH₂Cl", HALO, True, None), ("2-คลอโรโพรเพน", "CH₃CHClCH₃", HALO, True, None),
    ("1-คลอโรบิวเทน", "CH₃(CH₂)₃Cl", HALO, True, None), ("2-คลอโรบิวเทน", "CH₃CHClCH₂CH₃", HALO, True, None),
    ("1-คลอโร-2-เมทิลโพรเพน", "CH₃CH(CH₃)CH₂Cl", HALO, False, None),
    ("2-คลอโร-2-เมทิลโพรเพน", "CH₃CCl(CH₃)CH₃", HALO, False, None),
    ("เมทานอล", "CH₃OH", ALCOHOL, True, 65), ("เอทานอล", "CH₃CH₂OH", ALCOHOL, True, 78),
    ("โพรพาน-1-ออล", "CH₃CH₂CH₂OH", ALCOHOL, True, 97), ("โพรพาน-2-ออล", "CH₃CH(OH)CH₃", ALCOHOL, True, 82),
    ("บิวทาน-1-ออล", "CH₃(CH₂)₃OH", ALCOHOL, True, 118), ("บิวทาน-2-ออล", "CH₃CH(OH)CH₂CH₃", ALCOHOL, True, 100),
    ("2-เมทิลโพรพาน-1-ออล", "CH₃CH(CH₃)CH₂OH", ALCOHOL, False, 108),
    ("2-เมทิลโพรพาน-2-ออล", "CH₃C(OH)(CH₃)CH₃", ALCOHOL, False, 82),
    ("เพนทาน-1-ออล", "CH₃(CH₂)₄OH", ALCOHOL, True, 138),
    ("เมทอกซีมีเทน", "CH₃OCH₃", ETHER, True, -24), ("เมทอกซีอีเทน", "CH₃OCH₂CH₃", ETHER, True, 7),
    ("อีทอกซีอีเทน", "CH₃CH₂OCH₂CH₃", ETHER, True, 35), ("1-เมทอกซีโพรเพน", "CH₃OCH₂CH₂CH₃", ETHER, True, 39),
    ("2-เมทอกซีโพรเพน", "CH₃OCH(CH₃)CH₃", ETHER, False, 32),
    ("เมทานาล", "HCHO", ALDEHYDE, True, -19), ("เอทานาล", "CH₃CHO", ALDEHYDE, True, 20),
    ("โพรพานาล", "CH₃CH₂CHO", ALDEHYDE, True, 49), ("บิวทานาล", "CH₃CH₂CH₂CHO", ALDEHYDE, True, 75),
    ("2-เมทิลโพรพานาล", "CH₃CH(CH₃)CHO", ALDEHYDE, False, 64),
    ("โพรพาโนน", "CH₃COCH₃", KETONE, True, 56), ("บิวทาโนน", "CH₃COCH₂CH₃", KETONE, True, 80),
    ("เพนทาน-2-โอน", "CH₃COCH₂CH₂CH₃", KETONE, True, 102), ("เพนทาน-3-โอน", "CH₃CH₂COCH₂CH₃", KETONE, True, 102),
    ("กรดเมทาโนอิก", "HCOOH", ACID, True, 101), ("กรดเอทาโนอิก", "CH₃COOH", ACID, True, 118),
    ("กรดโพรพาโนอิก", "CH₃CH₂COOH", ACID, True, 141), ("กรดบิวทาโนอิก", "CH₃(CH₂)₂COOH", ACID, True, 164),
    ("กรด 2-เมทิลโพรพาโนอิก", "CH₃CH(CH₃)COOH", ACID, False, 155),
    ("เมทิลเมทาโนเอต", "HCOOCH₃", ESTER, True, 32), ("เมทิลเอทาโนเอต", "CH₃COOCH₃", ESTER, True, 57),
    ("เอทิลเมทาโนเอต", "HCOOCH₂CH₃", ESTER, True, 54), ("เอทิลเอทาโนเอต", "CH₃COOCH₂CH₃", ESTER, True, 77),
    ("เมทิลโพรพาโนเอต", "CH₃CH₂COOCH₃", ESTER, True, 80), ("โพรพิลเมทาโนเอต", "HCOOCH₂CH₂CH₃", ESTER, True, 81),
    ("เมทานามีน", "CH₃NH₂", AMINE, True, -6), ("เอทานามีน", "CH₃CH₂NH₂", AMINE, True, 17),
    ("เมทานาไมด์", "HCONH₂", AMIDE, True, 210), ("เอทานาไมด์", "CH₃CONH₂", AMIDE, True, 221),
    ("โพรพานาไมด์", "CH₃CH₂CONH₂", AMIDE, True, 213),
)


@lru_cache(maxsize=None)
def atoms_of(condensed: str) -> dict[str, int]:
    """Count atoms in a condensed formula, honouring (group)ₙ. Callers must not mutate the result."""
    text = condensed.translate(UNSUB).replace("=", "").replace("≡", "")
    stack = [{}]
    for token, number in re.findall(r"(Cl|C|H|O|N|\(|\))(\d*)", text):
        count = int(number or 1)
        if token == "(":
            stack.append({})
        elif token == ")":
            group = stack.pop()
            for k, v in group.items():
                stack[-1][k] = stack[-1].get(k, 0) + v * count
        else:
            stack[-1][token] = stack[-1].get(token, 0) + count
    return stack[0]


@lru_cache(maxsize=None)
def molecular(condensed: str) -> str:
    atoms = atoms_of(condensed)
    order = ["C", "H"] + sorted(k for k in atoms if k not in ("C", "H"))
    return "".join(k + (str(atoms[k]).translate(SUB) if atoms[k] > 1 else "") for k in order if atoms.get(k))


def carbons(c) -> int:
    return atoms_of(c[1])["C"]


ISOMERS = {c[0]: tuple(x for x in COMPOUNDS if x is not c and molecular(x[1]) == molecular(c[1])) for c in COMPOUNDS}


def isomers_of(c):
    return list(ISOMERS[c[0]])


# ══ ม.6/4 — การเรียกชื่อตามระบบ IUPAC ════════════════════════════════════════════


# ══ ม.6/5 — ไอโซเมอร์โครงสร้าง ═══════════════════════════════════════════════════


# ══ ม.6/6 — จุดเดือดและการละลายน้ำ ══════════════════════════════════════════════


