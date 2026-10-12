"""Wave G, slice 3 — ``Q = mL``, the half of ``ว 2.3 ม.1/1`` that had no set.

The indicator reads *คำนวณปริมาณความร้อนที่ทำให้สสารเปลี่ยนอุณหภูมิ **และเปลี่ยน
สถานะ** โดยใช้สมการ ``Q = mcΔT`` **และ** ``Q = mL``*. It names two equations.
Only one of them had a set: ``phys.heat_quantity_fluency`` computes ``Q = mcΔT``,
and searching the whole registry for ``ความร้อนแฝง`` or ``mL`` returned nothing —
at any level. A learner could finish every set filed under this indicator without
meeting the second equation it names by name.

So this trio is the missing half:

* ``phys.latent_heat_foundation`` — what ``L`` *is*. The value is per kilogram and
  the temperature does not move while it is spent; both are needed before the
  arithmetic means anything. ``standard_scope`` — stating a definition is not one
  of the indicator's verbs.
* ``phys.latent_heat_fluency`` — ``Q = mL`` itself. This one is ``exact``: the
  indicator names the equation, and this set performs it. It is the only set in
  the wave that claims the verb, and it claims it because the indicator wrote it
  down.
* ``phys.latent_heat_application`` 🖼 — the drawn heating curve, and *which* of
  the two equations a named stretch of minutes needs. This is where the pair
  stops being two formulas and becomes one decision. ``standard_scope``.

The application set reuses ``HEATING_CURVES``, so no new asset is rendered. It
asks by minute range rather than by "the flat part", which means the graph has to
be read to answer — and ``heating_curve_alt`` says only that the line rises, goes
flat, and rises again, never when, so it does not answer itself.
"""

from __future__ import annotations




# ══ ว 2.3 ม.1/1 — การคำนวณปริมาณความร้อนแฝงในการเปลี่ยนสถานะ ═══════════════════


