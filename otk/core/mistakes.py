"""Named mistakes — which misconception a wrong choice stands for.

Types have always hand-picked their most diagnostic wrong answers ("adding
numerators and denominators"), but the name lived only in a comment, so a
learner's stats could say *that* they were wrong and never *how*. A type now
wraps such a value in :func:`named`:

    wrongs = [named("fraction.add_across", as_mixed(naive)), ...]

``named`` returns the value unchanged, so it slots into ``_story.keep``,
``fixed``, ``MathDraw.distractors`` or any other path without touching them.
As a side effect it records value -> mistake in a ledger scoped to the one
``QuestionType.generate`` call that is running. After distractors are drawn,
balanced and shuffled, the assembler labels each final wrong choice by looking
it up in that ledger (:func:`label_for`). A choice the balancer invented or
sampled has no entry and stays unlabelled, which is the truth: nobody can say
which mistake it represents.

Labels are server-only, like the answer index: a label on a choice says it is
wrong, so it must never reach the browser.

Keys are shared across sets on purpose. "Scaled by adding the difference" is
the same misconception in a unit-price set and a recipe set, and the stats page
aggregates by key to show the learner a pattern rather than a one-off.
"""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Iterator, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

# key -> learner-facing name. Written as what the learner did, not as a
# judgement, so the stats page can say "You often: <name>".
MISTAKES: dict[str, dict[str, str]] = {
    "series.ignored_alternation": {
        "th": "มองอนุกรมสลับเครื่องหมายเป็นอนุกรมพจน์บวกทั้งหมด",
        "en": "Ignored the alternating signs in the series",
    },
    "series.used_first_term_only": {
        "th": "ตอบเพียงพจน์แรกของอนุกรม",
        "en": "Reported only the first term of the series",
    },
    "series.reversed_first_term_sign": {
        "th": "กลับเครื่องหมายของพจน์แรกในอนุกรมสลับเครื่องหมาย",
        "en": "Reversed the sign of the first term in an alternating series",
    },
    "series.used_infinite_sum": {
        "th": "ใช้ผลบวกอนันต์แทนผลบวกถึงพจน์ที่กำหนด",
        "en": "Used the infinite sum instead of stopping at the given term",
    },
    "series.used_tail_only": {
        "th": "ตอบพจน์หางที่เหลือแทนผลบวกส่วนต้น",
        "en": "Reported the remaining tail instead of the partial sum",
    },
    "series.reversed_telescoping_fraction": {
        "th": "กลับเศษและส่วนของผลบวกหลังตัดพจน์",
        "en": "Reversed the numerator and denominator after telescoping",
    },
    "series.forgot_term_weight": {
        "th": "ละตัวคูณลำดับพจน์ n ในอนุกรมเรขาคณิตถ่วงน้ำหนัก",
        "en": "Omitted the term-number weight n from the geometric series",
    },
    "series.shifted_weight_index": {
        "th": "เลื่อนเลขชี้กำลังของอนุกรมถ่วงน้ำหนักไปหนึ่งพจน์",
        "en": "Shifted the exponent by one in the weighted series",
    },
    "series.used_plus_ratio": {
        "th": "ใช้ 1+r แทน 1-r ในสูตรผลบวกอนุกรมเรขาคณิต",
        "en": "Used 1+r in place of 1-r in the geometric-series sum",
    },
    "interest.used_simple_interest": {
        "th": "คิดดอกเบี้ยคงต้นแทนดอกเบี้ยทบต้น",
        "en": "Used simple interest instead of compound interest",
    },
    "interest.compounded_annually": {
        "th": "ทบต้นปีละครั้งแทนการทบต้นรายไตรมาส",
        "en": "Compounded annually instead of quarterly",
    },
    "interest.counted_one_year_only": {
        "th": "คิดดอกเบี้ยทบต้นเพียงปีเดียว",
        "en": "Compounded for only one year",
    },
    "interest.treated_deposits_as_one_lump": {
        "th": "รวมเงินฝากทุกงวดโดยไม่คิดดอกเบี้ยแต่ละงวด",
        "en": "Added all deposits without growing each one",
    },
    "interest.deposited_at_period_start": {
        "th": "คิดว่าฝากต้นปีแทนปลายปี",
        "en": "Treated end-of-year deposits as beginning-of-year deposits",
    },
    "interest.grew_only_first_deposit": {
        "th": "คิดดอกเบี้ยเฉพาะเงินฝากงวดแรก",
        "en": "Grew only the first deposit",
    },
    "interest.ignored_discounting": {
        "th": "รวมเงินรับในอนาคตโดยไม่คิดลดเป็นมูลค่าปัจจุบัน",
        "en": "Added future payments without discounting them",
    },
    "interest.discounted_extra_period": {
        "th": "คิดลดเงินรับเกินไปหนึ่งงวด",
        "en": "Discounted the payments one extra period",
    },
    "interest.treated_first_payment_as_immediate": {
        "th": "คิดว่าได้เงินงวดแรกทันทีแทนปลายปีแรก",
        "en": "Treated the first end-of-year payment as immediate",
    },
    "composition.reversed_order": {
        "th": "สลับลำดับของฟังก์ชันประกอบ",
        "en": "Reversed the order of the composed functions",
    },
    "composition.stopped_at_outer_function": {
        "th": "แก้สมการของฟังก์ชันด้านนอกโดยไม่คำนวณฟังก์ชันด้านใน",
        "en": "Solved only the outer-function equation",
    },
    "composition.stopped_at_inner_function": {
        "th": "แก้สมการของฟังก์ชันด้านในโดยไม่คำนวณฟังก์ชันด้านนอก",
        "en": "Solved only the inner-function equation",
    },
    "composition.inequality_direction": {
        "th": "เลือกทิศทางอสมการผิดเมื่อหาโดเมน",
        "en": "Used the wrong inequality direction when finding the domain",
    },
    "composition.excluded_zero_radicand": {
        "th": "ตัดจุดที่ค่าภายในรากเป็นศูนย์ออกจากโดเมน",
        "en": "Excluded the point where the radicand is zero",
    },
    "composition.ignored_inner_constant": {
        "th": "ไม่แทนค่าพจน์คงที่ของฟังก์ชันด้านในเมื่อหาโดเมน",
        "en": "Ignored the inner function's constant when finding the domain",
    },
    "composition.kept_outer_constant": {
        "th": "เก็บพจน์คงที่ของฟังก์ชันด้านนอกไว้ในฟังก์ชันด้านใน",
        "en": "Kept the outer function's constant in the inner function",
    },
    "composition.did_not_remove_outer_constant": {
        "th": "ไม่ลบพจน์คงที่ของฟังก์ชันด้านนอกก่อนหาฟังก์ชันด้านใน",
        "en": "Did not remove the outer constant before recovering the inner function",
    },
    "composition.swapped_inner_coefficients": {
        "th": "สลับสัมประสิทธิ์กับพจน์คงที่ของฟังก์ชันด้านใน",
        "en": "Swapped the inner function's coefficient and constant",
    },
    "similar.used_whole_side": {
        "th": "หาความยาวทั้งด้านแทนส่วนที่เหลือของด้าน",
        "en": "Found the whole side instead of its remaining segment",
    },
    "similar.copied_corresponding_segment": {
        "th": "คัดลอกความยาวส่วนที่สมนัยโดยไม่ปรับตามอัตราส่วน",
        "en": "Copied the corresponding segment without scaling it",
    },
    "similar.reversed_ratio": {
        "th": "กลับอัตราส่วนของด้านที่สมนัยกัน",
        "en": "Reversed the ratio of corresponding sides",
    },
    "similar.used_length_ratio_for_area": {
        "th": "ใช้อัตราส่วนด้านแทนอัตราส่วนพื้นที่",
        "en": "Used the side-length ratio instead of its square for area",
    },
    "similar.found_inner_area": {
        "th": "หาพื้นที่สามเหลี่ยมด้านในแทนพื้นที่ส่วนที่เหลือ",
        "en": "Found the inner triangle's area instead of the remaining area",
    },
    "similar.reported_length_ratio": {
        "th": "ตอบอัตราส่วนด้านแทนสัดส่วนพื้นที่ที่โจทย์ถาม",
        "en": "Reported the side ratio instead of the requested area fraction",
    },
    "similar.used_area_ratio_for_length": {
        "th": "ใช้อัตราส่วนพื้นที่เป็นตัวคูณความยาวด้านโดยตรง",
        "en": "Scaled a side directly by the area ratio",
    },
    "similar.kept_length_unchanged": {
        "th": "ใช้ความยาวเดิมทั้งที่รูปใหญ่มีขนาดต่างกัน",
        "en": "Kept the original side length despite the change in size",
    },
    "similar.reversed_length_ratio": {
        "th": "กลับอัตราส่วนความยาวที่ได้จากพื้นที่",
        "en": "Reversed the side ratio inferred from the areas",
    },
    "transform.wrong_rotation_direction": {
        "th": "หมุนจุดไปในทิศทางตรงข้ามกับที่โจทย์กำหนด",
        "en": "Rotated the point in the opposite direction",
    },
    "transform.reflected_instead_of_rotated": {
        "th": "สะท้อนจุดแทนการหมุนรอบศูนย์กลาง 180 องศา",
        "en": "Reflected the point instead of rotating it 180 degrees about the center",
    },
    "transform.rotated_about_origin": {
        "th": "หมุนรอบจุดกำเนิดแทนศูนย์กลางที่กำหนด",
        "en": "Rotated about the origin instead of the given center",
    },
    "transform.left_point_unchanged": {
        "th": "ใช้พิกัดจุดเดิมโดยไม่ได้หมุน",
        "en": "Kept the original coordinates without rotating",
    },
    "transform.reversed_order": {
        "th": "สลับลำดับของการแปลงสองขั้น",
        "en": "Reversed the order of the two transformations",
    },
    "transform.skipped_reflection": {
        "th": "เลื่อนขนานแล้วไม่ได้สะท้อนจุด",
        "en": "Translated the point but omitted the reflection",
    },
    "transform.reflected_wrong_axis": {
        "th": "สะท้อนข้ามแกนอีกแกนหนึ่ง",
        "en": "Reflected across the other coordinate axis",
    },
    "transform.skipped_inverse_reflection": {
        "th": "ย้อนการเลื่อนขนานแต่ไม่ได้ย้อนการสะท้อน",
        "en": "Undid the translation but not the reflection",
    },
    "transform.applied_forward_translation": {
        "th": "ใช้เวกเตอร์เลื่อนขนานทิศเดิมเมื่อต้องหาจุดต้นฉบับ",
        "en": "Used the forward translation when finding the original point",
    },
    "transform.skipped_inverse_translation": {
        "th": "ย้อนการสะท้อนแต่ไม่ได้ย้อนการเลื่อนขนาน",
        "en": "Undid the reflection but not the translation",
    },
    "proportion.direct_instead_of_inverse": {
        "th": "ใช้สัดส่วนตรงกับจำนวนคนและเวลาที่แปรผกผันกัน",
        "en": "Used direct proportion for workers and time, which vary inversely",
    },
    "proportion.kept_time_fixed": {
        "th": "ใช้เวลาเดิมทั้งที่จำนวนคนทำงานเปลี่ยนไป",
        "en": "Kept the old time after the number of workers changed",
    },
    "proportion.multiplied_without_dividing": {
        "th": "คูณจำนวนคนกับวันทำงานแล้วตอบเลยโดยไม่หารด้วยจำนวนคนใหม่",
        "en": "Stopped at worker-days without dividing by the new worker count",
    },
    "proportion.area_scaled_once": {
        "th": "คูณมาตราส่วนเพียงครั้งเดียวเมื่อแปลงพื้นที่",
        "en": "Applied the length scale only once when converting area",
    },
    "proportion.map_area_unscaled": {
        "th": "ใช้พื้นที่บนแผนที่เป็นพื้นที่จริงโดยไม่แปลงมาตราส่วน",
        "en": "Used the map area as the real area without scaling",
    },
    "proportion.scale_reversed": {
        "th": "กลับอัตราส่วนมาตราส่วนเมื่อแปลงพื้นที่",
        "en": "Reversed the map scale when converting area",
    },
    "proportion.ignored_added_part": {
        "th": "ใช้สัดส่วนเดิมโดยไม่คิดส่วนที่เติมเพิ่ม",
        "en": "Used the original proportion without the added part",
    },
    "proportion.changed_total_only": {
        "th": "เพิ่มส่วนที่เติมในจำนวนรวมแต่ไม่เพิ่มในส่วนที่โจทย์ถาม",
        "en": "Added to the total but not to the requested part",
    },
    "proportion.changed_part_only": {
        "th": "เพิ่มส่วนที่เติมในส่วนที่โจทย์ถามแต่ไม่เพิ่มในจำนวนรวม",
        "en": "Added to the requested part but not to the total",
    },
    "area.one_region_only": {
        "th": "หาพื้นที่เพียงบริเวณเดียว ทั้งที่มีหลายบริเวณ",
        "en": "Found the area of only one of several regions",
    },
    "area.added_signed_regions": {
        "th": "รวมค่าอินทิกรัลที่มีเครื่องหมายต่างกันโดยไม่แปลงเป็นพื้นที่บวก",
        "en": "Added signed integrals without taking the positive area of each region",
    },
    "area.missed_antiderivative_divisor": {
        "th": "ลืมหารด้วยเลขชี้กำลังใหม่เมื่อหาปริพันธ์ของพจน์กำลัง",
        "en": "Forgot to divide by the new exponent when integrating a power",
    },
    "area.triangle_instead_of_integral": {
        "th": "ใช้สูตรพื้นที่สามเหลี่ยมแทนการหาพื้นที่ใต้กราฟโค้ง",
        "en": "Used a triangle formula for an area bounded by a curved graph",
    },
    "area.ignored_outer_regions": {
        "th": "ไม่นับบริเวณด้านนอกจุดตัดของเส้นโค้ง",
        "en": "Omitted the regions outside the curve intersections",
    },
    "area.ignored_subtracted_curve": {
        "th": "หาพื้นที่ใต้กราฟเพียงเส้นเดียวโดยไม่ลบกราฟอีกเส้น",
        "en": "Integrated only one curve without subtracting the other",
    },
    "fraction.add_across": {
        "th": "บวกหรือลบเศษกับเศษ และส่วนกับส่วนตรง ๆ โดยไม่ทำส่วนให้เท่ากันก่อน",
        "en": "Added or subtracted numerators and denominators straight across, "
              "without a common denominator",
    },
    "operation.reversed": {
        "th": "ใช้การดำเนินการผิด เช่น บวกแทนลบ หรือคูณแทนหาร",
        "en": "Used the wrong operation, such as adding instead of subtracting "
              "or multiplying instead of dividing",
    },
    "part.complement": {
        "th": "หาส่วนที่เหลือ แทนที่จะหาส่วนที่โจทย์ถาม (หรือกลับกัน)",
        "en": "Found the other part of the whole instead of the part asked for",
    },
    "probability.double_count_overlap": {
        "th": "นับผลลัพธ์ที่ตรงทั้งสองเงื่อนไขซ้ำเมื่อรวมเหตุการณ์",
        "en": "Counted outcomes that satisfy both conditions twice when combining events",
    },
    "probability.with_replacement": {
        "th": "คิดว่าหยิบครั้งที่สองจากจำนวนเดิม ทั้งที่ไม่ได้ใส่คืน",
        "en": "Used the original number of items for the second draw without replacement",
    },
    "domain.noninteger_vertex": {
        "th": "ใช้ค่าที่จุดยอดทั้งที่ค่า x ต้องเป็นจำนวนเต็ม",
        "en": "Used the vertex value even though x must be an integer",
    },
    "domain.excluded_attained_extremum": {
        "th": "ตัดค่ามากสุดหรือน้อยสุดที่ฟังก์ชันทำได้ออกจากเรนจ์",
        "en": "Excluded an extremum that the function attains",
    },
    "domain.included_excluded_endpoint": {
        "th": "รวมค่าที่ปลายช่วงทั้งที่โดเมนเป็นช่วงเปิด",
        "en": "Included an endpoint value even though the domain is open",
    },
    "domain.curvature_reversed": {
        "th": "กลับทิศของพาราโบลาเมื่อหาเรนจ์",
        "en": "Reversed the parabola's opening direction when finding its range",
    },
    "domain.wrong_extremum": {
        "th": "ใช้ค่าที่จุดยอดหรือขอบโดเมนผิดตำแหน่งเป็นค่าสุดขีด",
        "en": "Used the vertex or domain boundary at the wrong location as the extremum",
    },
    "trig.ambiguous_second_angle": {
        "th": "ลืมหรือเพิ่มมุมคู่ที่มีค่าไซน์เท่ากันในกรณีกำกวม",
        "en": "Missed or added the supplementary angle with the same sine in the ambiguous case",
    },
    "trig.ignored_height": {
        "th": "ไม่ตรวจว่าด้านที่กำหนดยาวพอจะสร้างรูปสามเหลี่ยมได้หรือไม่",
        "en": "Did not check whether the given side reaches far enough to form a triangle",
    },
    "fraction.unit_share_only": {
        "th": "หารด้วยตัวส่วนแล้วหยุด ลืมคูณด้วยตัวเศษ",
        "en": "Divided by the denominator and forgot to multiply by the numerator",
    },
    "fraction.scaled_both_terms": {
        "th": "คูณทั้งตัวเศษและตัวส่วนด้วยจำนวนนับ",
        "en": "Multiplied both the numerator and the denominator by the whole number",
    },
    "fraction.not_worked_back": {
        "th": "หาเศษส่วนของจำนวนที่ให้มา แทนที่จะย้อนกลับไปหาจำนวนทั้งหมด",
        "en": "Took the fraction of the given part instead of working back to the whole",
    },
    "fraction.digits_as_decimal": {
        "th": "เขียนตัวเศษกับตัวส่วนต่อกันเป็นทศนิยม",
        "en": "Wrote the numerator and denominator side by side as a decimal",
    },
    "fraction.numerator_as_tenths": {
        "th": "อ่านตัวเศษเป็นจำนวนส่วนสิบ โดยไม่สนใจตัวส่วน",
        "en": "Read the numerator as tenths and ignored the denominator",
    },
    "fraction.inverted": {
        "th": "หารตัวส่วนด้วยตัวเศษ (กลับเศษส่วน)",
        "en": "Divided the denominator by the numerator, turning the fraction upside down",
    },
    "mixed.whole_part_only": {
        "th": "ใช้เฉพาะจำนวนเต็มของจำนวนคละ ทิ้งเศษส่วนไป",
        "en": "Used only the whole-number part of a mixed number",
    },
    "decimal.point_misplaced": {
        "th": "วางจุดทศนิยมผิดตำแหน่ง",
        "en": "Put the decimal point in the wrong place",
    },
    "percent.answered_the_percent": {
        "th": "ตอบเป็นร้อยละ แทนที่จะตอบเป็นจำนวน",
        "en": "Gave a percentage as the answer instead of an amount",
    },
    "percent.subtracted_the_number": {
        "th": "ลบตัวเลขร้อยละออกจากจำนวนตรง ๆ",
        "en": "Subtracted the percentage number straight from the amount",
    },
    "percent.part_as_percent": {
        "th": "ตอบจำนวนส่วนย่อยเป็นร้อยละ โดยไม่เทียบกับจำนวนทั้งหมด",
        "en": "Gave the part as the percentage without comparing it to the whole",
    },
    "steps.missed_a_step": {
        "th": "ทำไม่ครบทุกขั้นตอน ข้ามขั้นตอนใดขั้นตอนหนึ่งไป",
        "en": "Left out one of the steps",
    },
    "steps.wrong_order": {
        "th": "ทำขั้นตอนสลับลำดับกัน",
        "en": "Did the steps in the wrong order",
    },
    "units.not_converted": {
        "th": "ไม่ได้แปลงหน่วยตามที่โจทย์ถาม",
        "en": "Left the answer in the original unit instead of converting it",
    },
    "units.wrong_conversion": {
        "th": "ใช้อัตราการแปลงหน่วยผิด",
        "en": "Used the wrong conversion between units",
    },
    "volume.area_not_volume": {
        "th": "หาพื้นที่ (คูณสองด้าน) แทนปริมาตร",
        "en": "Found an area (two measures multiplied) instead of a volume",
    },
    "volume.surface_not_volume": {
        "th": "หาพื้นที่ผิวทั้งหมด แทนปริมาตร",
        "en": "Found the surface area instead of the volume",
    },
    "power.multiplied_by_exponent": {
        "th": "คูณด้วยเลขชี้กำลัง แทนการยกกำลัง",
        "en": "Multiplied by the power instead of raising to it",
    },
    "area.forgot_half": {
        "th": "ลืมคูณด้วยครึ่งหนึ่งในสูตรพื้นที่",
        "en": "Forgot the one half in the area formula",
    },
    "proportion.additive": {
        "th": "ขยายสัดส่วนด้วยการบวกผลต่าง แทนการคูณ",
        "en": "Scaled a proportion by adding the difference instead of multiplying",
    },
    "proportion.no_divide": {
        "th": "คูณจำนวนในโจทย์เข้าด้วยกัน โดยไม่หาค่าต่อหนึ่งหน่วยก่อน",
        "en": "Multiplied the given numbers together without first finding the "
              "amount for one",
    },
    "proportion.unit_rate_only": {
        "th": "หาค่าต่อหนึ่งหน่วยแล้วตอบเลย โดยไม่คูณต่อ",
        "en": "Found the amount for one and stopped there",
    },
    "direction.left_right_swapped": {
        "th": "สลับด้านซ้ายกับด้านขวา",
        "en": "Swapped left and right",
    },
    "direction.opposite": {
        "th": "ตอบทิศตรงข้ามกับทิศที่ถูก",
        "en": "Gave the opposite direction",
    },
    "time.east_west_reversed": {
        "th": "สลับว่าทางตะวันออกหรือทางตะวันตกมีเวลาเร็วกว่า จึงบวกแทนลบหรือลบแทนบวก",
        "en": "Mixed up which side is ahead in time, so added instead of "
              "subtracting or the other way round",
    },
    "count.lines_not_gaps": {
        "th": "นับจำนวนเส้นแทนจำนวนช่วงระหว่างเส้น",
        "en": "Counted the lines instead of the gaps between them",
    },
    "time.date_not_changed": {
        "th": "ไม่ได้เปลี่ยนวันที่ เมื่อเวลาเลยเที่ยงคืนหรือข้ามเส้นวันที่สากล",
        "en": "Kept the same date when the time passed midnight or crossed the date line",
    },
}


def mistake_names() -> dict[str, dict[str, str]]:
    """The catalog of mistake names, for publishing with the catalog snapshot."""
    return {key: dict(names) for key, names in sorted(MISTAKES.items())}


# value-key -> mistake key, for the generate() call in progress; None outside one.
_LEDGER: ContextVar[dict[tuple, str] | None] = ContextVar("mistake_ledger", default=None)


def _value_key(value: object) -> tuple | None:
    """How a named value is matched to a final choice. A content list matches on
    its blocks; anything else (an int, a TeX or Thai string) matches a choice
    that is exactly one block showing ``str(value)``."""
    if isinstance(value, list) and value and all(
        isinstance(b, BaseModel) and hasattr(b, "kind") for b in value
    ):
        return ("content", *(_block_key(b) for b in value))
    if isinstance(value, (str, int)) and not isinstance(value, bool):
        return ("single", str(value))
    return None


def _block_key(block) -> tuple:
    return (block.kind, getattr(block, "tex", getattr(block, "text", getattr(block, "code", ""))))


def _content_keys(content: list) -> list[tuple]:
    keys = [("content", *(_block_key(b) for b in content))]
    if len(content) == 1:
        keys.append(("single", _block_key(content[0])[1]))
    return keys


def named(key: str, value: T) -> T:
    """Mark ``value`` as the wrong answer that mistake ``key`` produces; return it.

    The first naming of a value wins. Two mistakes that land on the same value
    for a draw cannot be told apart from the learner's choice, and the earlier
    one is the more diagnostic by the authoring convention (most diagnostic
    first), the same rule ``fixed`` and ``keep`` use when they drop duplicates.
    """
    if key not in MISTAKES:
        raise KeyError(f"unknown mistake {key!r}; add it to otk.core.mistakes.MISTAKES")
    ledger = _LEDGER.get()
    value_key = _value_key(value)
    if ledger is not None and value_key is not None:
        ledger.setdefault(value_key, key)
    return value


@contextmanager
def recording() -> Iterator[dict[tuple, str]]:
    """Collect :func:`named` calls made while building one question."""
    ledger: dict[tuple, str] = {}
    token = _LEDGER.set(ledger)
    try:
        yield ledger
    finally:
        _LEDGER.reset(token)


def label_for(ledger: dict[tuple, str], content: list) -> str | None:
    """The mistake a final choice stands for, if a type named it."""
    for key in _content_keys(content):
        if key in ledger:
            return ledger[key]
    return None
