"""Wave F slice 2 — weight from a gravitational field, ``W = mg``.

Closes ``ฟิสิกส์เพิ่มเติม 1 ม.4/6`` อธิบายกฎความโน้มถ่วงสากลและผลของสนามโน้มถ่วง
ที่ทำให้วัตถุมีน้ำหนัก รวมทั้งคำนวณปริมาณต่าง ๆ ที่เกี่ยวข้อง — an
``additional_outcome``, filed whole.

Built while turning ``sheet_database/outputs/teaching_plan/ข้อสอบแรง.md`` into a formula-led plan.
``W = mg`` is the formula the rest of that sheet stands on: every μ question
converts a mass to a normal force with it, every pressure and buoyancy question
uses ``ρg``, and every moment question weighs a load. It had no set of its own —
``phys.spring_scale_weight_*`` *reads* a spring scale and
``phys.gravity_effect_*`` is conceptual, but nothing computed the product.

Mass and weight are kept strictly apart, because conflating them is the mistake
the sheet's ตอน 5 ข้อ 2 exists to catch: mass is in kilograms and does not
change with location, weight is a force in newtons and does.
"""

from __future__ import annotations




