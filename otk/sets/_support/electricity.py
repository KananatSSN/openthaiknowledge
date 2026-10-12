"""ฟิสิกส์ — question types for the หัวข้อ *ไฟฟ้า*.

ม.3 ไฟฟ้า, built from the ไฟฟ้า study sheet: นิยามและหน่วยของ V, I, R; กฎของโอห์ม;
ความต้านทานของลวดตัวนำ (R = ρL/A); การต่อตัวต้านทานแบบอนุกรมและแบบขนาน; และ
กำลังไฟฟ้ากับพลังงานไฟฟ้า. It is a second topic under the existing ``ฟิสิกส์``
subject, so it sits beside คลื่นและแสง in the nav rather than starting a subject.

Four shapes of question live here:

* **numeric drills** (``PhysCalc``, ._numeric) — the formulas themselves, each
  asked in every direction the algebra allows. Distractors are the classic slips:
  adding instead of multiplying, dropping the square in I²R, and — the one that
  costs the most marks — leaving t in นาที when W = Pt wants วินาที;
* **classify-by-category** (``ClassifyType``, ._classify) — which quantity a
  description belongs to, what a change to the wire does to its resistance, and
  which properties belong to a series versus a parallel connection;
* **concept banks** (``ConceptBankType``, ._concept) — units and symbols, and the
  กำลังไฟฟ้า/พลังงานไฟฟ้า distinction that the topic turns on;
* **circuit diagrams** (``CircuitType``) — a drawn schematic with its resistor
  values printed on it, asked three ways: the kind of connection, the total
  resistance, and the resulting current. The three types read one
  ``CIRCUIT_SPECS`` table, the "family over one data table" shape that ธรณีวิทยา's
  rock photos use.

The schematics are built-in assets rendered by
``otk/pictures/generate.py`` from ``CIRCUIT_SPECS`` below, so the
drawing and the answer cannot drift apart — the same discipline as ``WAVE_SPECS``.

Importing this module from ``types/__init__.py`` self-registers everything below.
"""

from __future__ import annotations

SUBJECT = "ฟิสิกส์"
TOPIC = "ไฟฟ้า"
LEVEL = {"th": "ม.3"}


# ══ นิยาม หน่วย และสัญลักษณ์ ═══════════════════════════════════════════════════


# ══ กฎของโอห์ม ════════════════════════════════════════════════════════════════


# ══ ความต้านทานของลวดตัวนำ ════════════════════════════════════════════════════


# ══ การต่อตัวต้านทานแบบอนุกรมและแบบขนาน ════════════════════════════════════════


# ══ กำลังไฟฟ้าและพลังงานไฟฟ้า ═════════════════════════════════════════════════


