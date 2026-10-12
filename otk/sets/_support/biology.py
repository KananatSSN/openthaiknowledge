"""ชีววิทยา (ชีวะ) — the biology subject module.

Two families live here:

* **Labelled diagrams** (:class:`LabeledDiagramType`) — an item shows a diagram
  with an arrow at one part; the four choices are Thai part names (the correct one
  plus real siblings). Needs *no* new rendering path: an ``ImageBlock`` with a
  ``Marker`` and ``TextBlock`` choices flow through the same pipeline as math.

* **นิเวศวิทยา concept types** (:class:`ClassifyType`, :class:`EcoLevels`) — the
  ป.6 หัวข้อ *สิ่งมีชีวิตกับสิ่งแวดล้อม*: classify an organism by feeding
  behaviour, name the รูปแบบความสัมพันธ์ of two organisms, or place an example in
  the ระดับการจัดระบบทางนิเวศวิทยา. Each draws from a small Thai data table and
  offers *real* siblings as distractors, exactly like the เคมี element types.

Assets are referenced by id only (``asset_id``); the asset store resolves them to
real images. The skeleton diagram is shipped as a built-in asset so the type works
without an administrator upload.
"""

from __future__ import annotations

SUBJECT = "ชีวะ"
TOPIC_ECOLOGY = "สิ่งมีชีวิตกับสิ่งแวดล้อม"


# ══ นิเวศวิทยา — สิ่งมีชีวิตกับสิ่งแวดล้อม ═════════════════════════════════════
# Concept types over small Thai data tables. Wrong choices are always *real*
# siblings — another category the student is studying, or an example from a
# different category — never an invented fact, mirroring the เคมี element types.
# The classify/pick machinery lives in ._classify (shared with เคมี/ฟิสิกส์/ดาราศาสตร์).


