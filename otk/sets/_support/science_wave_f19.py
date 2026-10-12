"""Wave F slice 19 — เคมีเพิ่มเติม 1: atomic models, electron configuration,
periodic trends, and the transition metals.

Four ``additional_outcome`` indicators, each filed whole, opening
``เคมีเพิ่มเติม``:

* ``เคมีเพิ่มเติม 1 ม.4/1`` — the evidence behind each atomic model, and how the
  model evolved;
* ``เคมีเพิ่มเติม 1 ม.4/3`` — electron configuration by main energy level and by
  subshell, from the atomic number;
* ``เคมีเพิ่มเติม 1 ม.4/5`` — trends in the properties of representative
  elements down a group and across a period;
* ``เคมีเพิ่มเติม 1 ม.4/6`` — properties of the transition metals against the
  representative metals.

Configurations are built by the aufbau order with the textbook's two
exceptions, chromium and copper. Trends are read off the periodic position,
so every comparison has one right answer.
"""

from __future__ import annotations

SUBJECT = "เคมี"
UPPER_FOUR = {"th": "ม.4"}

# (Z, symbol, Thai name, period, group) for the representative elements the textbook uses.
ELEMENTS = (
    (1, "H", "ไฮโดรเจน", 1, 1), (3, "Li", "ลิเทียม", 2, 1), (4, "Be", "เบริลเลียม", 2, 2), (5, "B", "โบรอน", 2, 13),
    (6, "C", "คาร์บอน", 2, 14), (7, "N", "ไนโตรเจน", 2, 15), (8, "O", "ออกซิเจน", 2, 16), (9, "F", "ฟลูออรีน", 2, 17),
    (11, "Na", "โซเดียม", 3, 1), (12, "Mg", "แมกนีเซียม", 3, 2), (13, "Al", "อะลูมิเนียม", 3, 13), (14, "Si", "ซิลิคอน", 3, 14),
    (15, "P", "ฟอสฟอรัส", 3, 15), (16, "S", "กำมะถัน", 3, 16), (17, "Cl", "คลอรีน", 3, 17), (19, "K", "โพแทสเซียม", 4, 1),
    (20, "Ca", "แคลเซียม", 4, 2), (31, "Ga", "แกลเลียม", 4, 13), (32, "Ge", "เจอร์เมเนียม", 4, 14), (33, "As", "สารหนู", 4, 15),
    (34, "Se", "ซีลีเนียม", 4, 16), (35, "Br", "โบรมีน", 4, 17), (37, "Rb", "รูบิเดียม", 5, 1), (38, "Sr", "สตรอนเชียม", 5, 2),
    (53, "I", "ไอโอดีน", 5, 17), (55, "Cs", "ซีเซียม", 6, 1), (56, "Ba", "แบเรียม", 6, 2),
)
REPRESENTATIVE = tuple(e for e in ELEMENTS if e[0] != 1)


# ══ ม.4/1 — แบบจำลองอะตอม ═════════════════════════════════════════════════════════


# ══ ม.4/3 — การจัดเรียงอิเล็กตรอน ═════════════════════════════════════════════════


# ══ ม.4/5 — แนวโน้มสมบัติ ════════════════════════════════════════════════════════


# ══ ม.4/6 — ธาตุแทรนซิชัน ════════════════════════════════════════════════════════


