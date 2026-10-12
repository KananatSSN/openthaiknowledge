"""ธรณีวิทยา (geology) — question types. A subject of its own.

ป.6 หัวข้อ *หินและการเปลี่ยนแปลง* (ว 3.2). The สาระ is one small table of ten
rocks, but each rock carries four independent facts — ประเภท, การเกิด, ลักษณะ
เนื้อหิน and การนำไปใช้ประโยชน์ — so the same table drives several types that
never ask the same thing twice. Four shapes of question live here:

* **classify-by-category** (``ClassifyType``, ._classify) — the rock's group, the
  process that formed it, the cooling rate behind an อัคนี rock, its ลักษณะเนื้อหิน
  and what it is used for;
* **concept banks** (``ConceptBankType``, ._concept) — หินต้นกำเนิดของหินแปร,
  คำศัพท์ธรณีวิทยา (แมกมา/ลาวา/แคลไซต์) and วัฏจักรหิน, each a set of facts with
  its own wrong choices;
* **photo identification** (``RockPhotoType``) — a real hand-specimen photograph,
  asked two ways: which rock is it, and which group does it belong to. The two
  types read one ``ROCK_PHOTOS`` table, the "family over one data table" shape
  that เคมี's element types use.

Distractors are always *real* siblings — another rock, another group, another
rock's use — never an invented fact.

The photographs are built-in assets fetched by
``otk/pictures/fetch_rocks.py`` (Wikimedia Commons GeoDIL, CC0); the
asset ids below match its ``MANIFEST``.

Importing this module from ``types/__init__.py`` self-registers everything below;
the subject ``ธรณีวิทยา`` then appears in the catalog/nav on its own.
"""

from __future__ import annotations

SUBJECT = "ธรณีวิทยา"
TOPIC = "หินและการเปลี่ยนแปลง"


# ══ Classify-by-category ชุดโจทย์ ═════════════════════════════════════════════


# ══ Concept-bank ชุดโจทย์ ═════════════════════════════════════════════════════


# ══ รูปถ่ายหินจริง: ชี้ชื่อหินและประเภทจากภาพ ═══════════════════════════════════


