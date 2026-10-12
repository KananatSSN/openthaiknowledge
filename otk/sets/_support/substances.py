"""เคมี — สารบริสุทธิ์และสารผสม, and how a mixture is taken apart (ม.2).

Built from three study sheets: ``สารบริสุทธิ์.md``, ``การแยกสารเนื้อผสม.md`` and
``การแยกสารเนื้อเดียว.md``. Two หัวข้อ live here — what a substance *is*
(บริสุทธิ์ / ไม่บริสุทธิ์ / เนื้อผสม, ธาตุ / สารประกอบ) and how you separate one —
under the existing ``เคมี`` subject, at ม.2.

**On the ป.6 overlap.** ``chemistry.py`` already teaches separation at ป.6
(``chem.separation``, ``chem.separate_solids``, ``chem.magnetic_separation`` …).
Those ask *which method suits this example*. These ask *what property the method
exploits* and *why it works* — ความหนาแน่นต่างกัน, จุดเดือดต่างกัน, ระเหิดได้,
สารละลายอิ่มตัว, แรงหนีศูนย์กลาง — and they add the five methods ป.6 never
reaches: การระเหิด, การหลอมเหลว, เครื่องหมุนเหวี่ยง, การตกผลึก, การกลั่นลำดับส่วน.
Both layers are meant to ship; a shared example (ผงเหล็ก + ผงกำมะถัน is *the*
magnet case) is a different question about the same object.

Four shapes of question:

* **classify-by-category** (``ClassifyType``) — สารบริสุทธิ์/ไม่บริสุทธิ์/เนื้อผสม,
  ธาตุ/สารประกอบ, สารละลาย/คอลลอยด์/สารแขวนลอย, and the two method tables;
* **concept banks** (``ConceptBankType``) — the mechanisms and the conditions;
* **data reading** (``PurityFromBoiling``, ``DensityLayers``) — decide from
  numbers rather than recall, which is what ม.2 adds over ป.6;
* **diagrams** (``ChromaType``, ``ApparatusId``) — a drawn paper chromatogram
  asked four ways plus the Rf read off it, and the ชุดกลั่น / กรวยแยก / ชุดกรอง
  set-ups. The types read ``CHROMA_SPECS`` and ``APPARATUS_SPECS``, and
  ``otk/pictures/generate.py`` draws exactly those tables, so the picture and
  the answer cannot drift — the ``CIRCUIT_SPECS`` discipline.

Four sets go beyond the sheets, which name them without explaining them:
``chem.solution_colloid_suspension``, ``chem.colloid`` and ``chem.tyndall``
(``สารบริสุทธิ์.md`` lists ``[Other things] คอลลอยด์, ปรากฎการณ์ทินดอล`` and stops),
and ``chem.solvent_extraction``. ``chem.rf_value`` and ``chem.density_layers``
are computational extensions of what the sheets describe in words.

Importing this module from ``types/__init__.py`` self-registers everything below.
"""

from __future__ import annotations

SUBJECT = "เคมี"
TOPIC_PURE = "สารบริสุทธิ์และสารผสม"
TOPIC_SEP = "การแยกสาร"
LEVEL = {"th": "ม.2"}


# ══ สารบริสุทธิ์และสารผสม ═══════════════════════════════════════════════════════


# ── จุดเดือดบอกความบริสุทธิ์ ──────────────────────────────────────────────────
# The sheet's actual *test* for purity, as a data-reading item rather than
# recall: a สารบริสุทธิ์ boils at one fixed temperature, a สารผสม over a range.
# Substances are named สาร ก / ข / ค — inventing a boiling point for a named
# chemical would teach a wrong number.


# ── คอลลอยด์และปรากฏการณ์ทินดอล ──────────────────────────────────────────────
# ``สารบริสุทธิ์.md`` lists these two under [Other things] and gives no content,
# so the three sets below are authored from the standard ม.2 curriculum.


# ══ การแยกสารเนื้อผสม ═══════════════════════════════════════════════════════════


# ── ความหนาแน่นบอกชั้นของของเหลว ─────────────────────────────────────────────
# The rule in ``chem.separatory_funnel`` made computational: given two densities,
# work out which liquid sits where and which drains first. Pairs are always one
# aqueous and one organic liquid, because only immiscible liquids form layers —
# น้ำ กับ แอลกอฮอล์ would be a wrong question, not a hard one.


# ══ การแยกสารเนื้อเดียว ═════════════════════════════════════════════════════════


# ══ โครมาโทกราฟีจากแผนภาพ ══════════════════════════════════════════════════════
# A drawn paper chromatogram, read four ways plus the Rf value. The spots are
# labelled A, B, C… in ASCII *as well as* coloured, so the questions identify a
# component by letter — a worksheet printed in black and white still works, and
# no Thai font is needed to render the asset.


# ══ ชุดอุปกรณ์แยกสารจากแผนภาพ ═══════════════════════════════════════════════════


