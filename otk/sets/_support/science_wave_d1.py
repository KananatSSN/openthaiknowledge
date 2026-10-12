"""Wave D, slice 1 — materials at ป.1 and water absorption at ป.2.

* ``ว 2.1 ป.1/1`` สมบัติที่สังเกตได้ของวัสดุที่ใช้ทำวัตถุ — all three stages
* ``ว 2.1 ป.1/2`` ชนิดของวัสดุและการจัดกลุ่มตามสมบัติที่สังเกตได้ — all three stages
* ``ว 2.1 ป.2/1`` การดูดซับน้ำของวัสดุและการนำไปใช้ — all three stages

``ป.1/1`` names its evidence (``โดยใช้หลักฐานเชิงประจักษ์``), so the Fluency set
that puts an observation record in the stem is its single ``exact`` set; the
answer names every material the object is made of, with the property observed.
``ป.1/2`` joins two free verbs, ``ระบุชนิด`` and ``จัดกลุ่ม``, so Foundation
identifies a material and Fluency groups objects by a property, both ``exact``.
``ป.2/1`` also joins two: Foundation names the use a material's absorption is
put to, and Fluency compares absorption from an experiment's record.
"""

from __future__ import annotations

SUBJECT = "เคมี"
FIRST = {"th": "ป.1"}
SECOND = {"th": "ป.2"}


# ══ ว 2.1 ป.1/1 — สมบัติที่สังเกตได้ของวัสดุที่ใช้ทำวัตถุ ═══════════════════════════════

# What a ป.1 learner can see or feel of each material. Each is unique to its
# material, so an observation names the material without saying it.
PROPERTY = {
    "ไม้": "แข็ง มีลวดลายของเนื้อไม้",
    "โลหะ": "แข็ง ผิวมันวาว",
    "พลาสติก": "ผิวเรียบ น้ำหนักเบา มีสีสดใส",
    "ยาง": "ดึงแล้วยืดออกและหดกลับได้",
    "ผ้า": "นุ่ม พับหรือขยำได้",
    "แก้ว": "ใส มองผ่านได้",
    "กระดาษ": "บาง ฉีกขาดได้ง่าย",
}
MATERIALS = tuple(PROPERTY)


# ══ ว 2.1 ป.1/2 — ระบุชนิดของวัสดุและจัดกลุ่มวัสดุตามสมบัติที่สังเกตได้ ═════════════════


# ══ ว 2.1 ป.2/1 — การดูดซับน้ำของวัสดุและการนำไปใช้ ════════════════════════════════════


