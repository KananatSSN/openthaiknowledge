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
    "phys.area_dimension_ignored": {
        "th": 'ละมิติพื้นที่ออกจากการหารมิติ',
        "en": 'Omitted area dimensions when dividing dimensions',
    },
    "phys.time_dimension_wrong": {
        "th": 'รวมเลขชี้กำลังเวลาไม่ถูกต้อง',
        "en": 'Combined time exponents incorrectly',
    },
    "phys.dimensions_multiplied": {
        "th": 'คูณมิติตัวประกอบแทนการหารออก',
        "en": 'Multiplied dimensions instead of dividing them out',
    },
    "phys.used_full_gravity": {
        "th": 'ใช้ g แทนองค์ประกอบตามแนวราง',
        "en": 'Used full gravity instead of its tangential component',
    },
    "phys.halved_speed": {
        "th": 'หารความเร็วด้วยสองแทนใช้ความสัมพันธ์พลังงาน',
        "en": 'Halved speed instead of applying the energy relation',
    },
    "phys.ignored_lift_acceleration": {
        "th": 'ละความเร่งพื้นลิฟต์',
        "en": 'Ignored the elevator floor acceleration',
    },
    "phys.lift_acceleration_subtracted": {
        "th": 'ลบความเร่งลิฟต์ขึ้นออกจาก g',
        "en": 'Subtracted upward elevator acceleration from gravity',
    },
    "phys.halved_time": {
        "th": 'หารเวลาด้วยสองแทนแก้สมการกำลังสอง',
        "en": 'Halved the time instead of solving the quadratic relation',
    },
    "phys.ignored_weight": {
        "th": 'ละน้ำหนักในสมดุลแรงลอยตัว',
        "en": 'Omitted weight from the buoyancy balance',
    },
    "phys.added_weight_to_buoyancy": {
        "th": 'บวกน้ำหนักกับแรงลอยตัวทั้งที่ทิศตรงข้าม',
        "en": 'Added weight to the opposing buoyant force',
    },
    "phys.ignored_buoyancy": {
        "th": 'ใช้เฉพาะน้ำหนักสมดุลกับแรงต้าน',
        "en": 'Balanced drag against weight alone',
    },
    "phys.ignored_contact_weight": {
        "th": 'ละแรงน้ำหนักระหว่างช่วงสัมผัสพื้น',
        "en": 'Omitted weight during floor contact',
    },
    "phys.subtracted_rebound_speed": {
        "th": 'ลบอัตราเร็วก่อนและหลังชนที่ทิศตรงข้าม',
        "en": 'Subtracted speeds across the reversal at impact',
    },
    "phys.ignored_rebound": {
        "th": 'ละโมเมนตัมขาขึ้นหลังชน',
        "en": 'Omitted the upward rebound momentum',
    },
    "phys.used_sticking_collision": {
        "th": 'สมมติว่าวัตถุติดลูกตุ้มหลังชน',
        "en": 'Assumed the projectile remained attached to the pendulum',
    },
    "phys.conserved_collision_energy": {
        "th": 'อนุรักษ์พลังงานจลน์ผ่านการชนที่สูญเสียพลังงาน',
        "en": 'Conserved kinetic energy through a dissipative collision',
    },
    "phys.used_final_force_for_work": {
        "th": 'ใช้แรงสุดท้ายคูณระยะทั้งช่วงที่แรงเพิ่ม',
        "en": 'Used the final force over the whole extension',
    },
    "phys.kept_release_angle": {
        "th": 'ใช้มุมปล่อยเป็นมุมหลุด',
        "en": 'Used the release angle as the separation angle',
    },
    "phys.extra_factor_two": {
        "th": 'หารด้วยสองซ้ำในเงื่อนไขหลุด',
        "en": 'Divided by two again in the separation condition',
    },
    "phys.used_half_release_cosine": {
        "th": 'ใช้ครึ่งหนึ่งของโคไซน์มุมปล่อยแทนแก้แรงรัศมี',
        "en": 'Halved the release cosine instead of solving radial balance',
    },
    "phys.used_vertical_tension": {
        "th": 'ตอบองค์ประกอบแนวดิ่งแทนขนาดแรงตึง',
        "en": 'Reported vertical tension component instead of its magnitude',
    },
    "phys.weight_at_beam_end": {
        "th": 'วางน้ำหนักคานที่ปลายแทนกึ่งกลาง',
        "en": 'Placed beam weight at its end instead of its midpoint',
    },
    "phys.ignored_beam_weight": {
        "th": 'ละโมเมนต์น้ำหนักคาน',
        "en": 'Omitted the torque of the beam weight',
    },
    "phys.used_charge_ratio_not_root": {
        "th": 'ใช้สัดส่วนประจุแทนรากที่สองของสัดส่วน',
        "en": 'Used charge ratio instead of its square root',
    },
    "phys.charge_zero_between": {
        "th": 'วางจุดสนามศูนย์ระหว่างประจุต่างเครื่องหมาย',
        "en": 'Placed zero field between opposite-sign charges',
    },
    "phys.ignored_charge_weights": {
        "th": 'ใช้แนวเรขาคณิตโดยละขนาดประจุ',
        "en": 'Used geometry without weighting charge magnitudes',
    },
    "phys.reversed_charge_sign": {
        "th": 'กลับทิศองค์ประกอบสนามจากประจุลบ',
        "en": 'Reversed a field component from a negative charge',
    },
    "phys.subtracted_parallel_resistances": {
        "th": 'ลบค่าความต้านทานขนานโดยตรง',
        "en": 'Subtracted parallel resistances directly',
    },
    "phys.added_parallel_resistances": {
        "th": 'บวกค่าความต้านทานขนานโดยตรง',
        "en": 'Added parallel resistances directly',
    },
    "phys.equal_capacitor_voltage": {
        "th": 'ให้ตัวเก็บประจุอนุกรมแต่ละตัวรับแรงดันรวม',
        "en": 'Assigned the full voltage to each series capacitor',
    },
    "phys.ignored_divider": {
        "th": 'ใช้แรงดันแหล่งจ่ายแทนแรงดันที่แบ่งแล้ว',
        "en": 'Used supply voltage instead of divided voltage',
    },
    "phys.added_series_capacitance": {
        "th": 'บวกความจุอนุกรมเหมือนต่อขนาน',
        "en": 'Added series capacitances as if in parallel',
    },
    "phys.kept_wire_area": {
        "th": 'รักษาพื้นที่ลวดแทนรักษาปริมาตรลวด',
        "en": 'Kept wire area fixed instead of wire volume',
    },
    "phys.power_tracks_resistance": {
        "th": 'ให้กำลังเพิ่มตามความต้านทานเมื่อแรงดันคงเดิม',
        "en": 'Made power track resistance at fixed voltage',
    },
    "phys.used_emerged_second_volume": {
        "th": 'ใช้ส่วนพ้นน้ำของชิ้นที่สองแทนส่วนจม',
        "en": 'Used the second body emerged fraction instead of submerged fraction',
    },
    "phys.pressure_height_added": {
        "th": 'บวกความสูงคอลัมน์เมื่อความดันต้องลด',
        "en": 'Added the column height when pressure should decrease',
    },
    "phys.ignored_column_height": {
        "th": 'ละความดันต่างจากคอลัมน์ของเหลว',
        "en": 'Ignored the pressure difference from the liquid column',
    },
    "phys.pressure_height_only": {
        "th": 'ตอบความดันต่างแทนความดันสัมบูรณ์',
        "en": 'Reported pressure difference instead of absolute pressure',
    },
    "phys.ignored_oil_heat": {
        "th": 'ละความร้อนที่น้ำมันรับ',
        "en": 'Omitted the heat absorbed by oil',
    },
    "phys.final_temperature_only": {
        "th": 'ตอบอุณหภูมิสมดุลแทนอุณหภูมิเริ่มต้น',
        "en": 'Reported equilibrium instead of initial temperature',
    },
    "phys.equal_heat_capacities": {
        "th": 'ถือว่าความจุความร้อนน้ำและน้ำมันเท่ากัน',
        "en": 'Assumed equal total heat capacities for water and oil',
    },
    "phys.celsius_for_gas": {
        "th": 'ใช้เซลเซียสในสมการแก๊สแทนเคลวิน',
        "en": 'Used Celsius instead of Kelvin in the gas law',
    },
    "phys.upright_self_image": {
        "th": 'เลือกสาขาภาพตั้งตรงทั้งที่โจทย์ระบุกลับหัว',
        "en": 'Selected the upright branch despite the inverted-image condition',
    },
    "phys.mirror_focus_not_centre": {
        "th": 'ใช้โฟกัสกระจกแทนศูนย์กลางความโค้ง',
        "en": 'Used mirror focus instead of centre of curvature',
    },
    "phys.lens_sign_reversed": {
        "th": 'กลับเครื่องหมายระยะในสมการเลนส์',
        "en": 'Reversed a distance sign in the lens equation',
    },
    "phys.velocity_angle_unchanged": {
        "th": 'ให้ทิศความเร็วระหว่างทางเท่ากับมุมยิง',
        "en": 'Kept the intermediate velocity angle equal to launch angle',
    },
    "phys.height_factor_inverted": {
        "th": 'คูณเศษส่วนพลังงานที่เหลือแทนหารย้อนกลับ',
        "en": 'Multiplied by the remaining energy fraction instead of dividing back',
    },
    "phys.ignored_small_mass": {
        "th": 'ละมวลก้อนเล็กจากมวลที่เร่ง',
        "en": 'Omitted the small mass from the accelerated system',
    },
    "phys.ignored_big_mass": {
        "th": 'ละมวลกล่องใหญ่จากมวลที่เร่ง',
        "en": 'Omitted the large block from the accelerated system',
    },
    "phys.multiplied_friction_coefficient": {
        "th": 'คูณสัมประสิทธิ์เสียดทานแทนหารหาแรงขั้นต่ำ',
        "en": 'Multiplied by friction coefficient instead of dividing for threshold force',
    },
    "phys.used_one_rod_balance": {
        "th": 'ใช้สมดุลคานเพียงครั้งเดียว',
        "en": 'Used only one of the two rod balances',
    },
    "phys.wrong_pivot_distance": {
        "th": 'ใช้แขนโมเมนต์อ้างจุดรองรับผิด',
        "en": 'Used a lever arm measured from the wrong support',
    },
    "phys.added_lever_lengths": {
        "th": 'บวกแขนโมเมนต์ที่ต้องกำจัดด้วยสมดุลสองครั้ง',
        "en": 'Added lever lengths instead of eliminating them across the balances',
    },
    "phys.radial_force_only": {
        "th": 'ตอบแรงรัศมีโดยละแรงตั้งฉากอีกองค์ประกอบ',
        "en": 'Reported radial force alone without the perpendicular component',
    },
    "phys.added_perpendicular_forces": {
        "th": 'บวกขนาดแรงตั้งฉากแทนรวมแบบเวกเตอร์',
        "en": 'Added magnitudes of perpendicular forces',
    },
    "phys.kinetic_factor_two_missing": {
        "th": 'ละตัวคูณสองเมื่อเปลี่ยนพลังงานเป็นความเร็วกำลังสอง',
        "en": 'Omitted the factor two when converting energy to squared speed',
    },
    "phys.rectangle_for_force_graph": {
        "th": 'ใช้แรงสูงสุดคูณระยะทั้งกราฟ',
        "en": 'Used peak force over the full graph width',
    },
    "phys.ignored_ramp_work": {
        "th": 'ละงานส่วนแรงเพิ่มเชิงเส้น',
        "en": 'Omitted work during the rising-force segment',
    },
    "phys.total_charge_one_sphere": {
        "th": 'ใช้ประจุเริ่มต้นลูกเดียวแทนผลรวมสองลูก',
        "en": 'Used one sphere initial charge instead of the conserved total',
    },
    "phys.ignored_other_final_charge": {
        "th": 'ละการหาประจุสุดท้ายของอีกทรงกลม',
        "en": 'Skipped finding the other sphere final charge',
    },
    "phys.added_branch_currents": {
        "th": 'บวกกระแสที่ต้องลบตามทิศที่โหนด',
        "en": 'Added branch currents that should be subtracted at the node',
    },
    "phys.ignored_node_voltage": {
        "th": 'ละแรงดันระหว่างโหนดเมื่อหากระแสแขนง',
        "en": 'Omitted node voltage when computing branch current',
    },
    "phys.radius_not_area": {
        "th": 'หารด้วยรัศมีแทนรัศมีกำลังสอง',
        "en": 'Divided by radius instead of squared radius',
    },
    "phys.multiplied_tank_area": {
        "th": 'คูณพื้นที่ถังแทนหารอัตราการไหลด้วยพื้นที่',
        "en": 'Multiplied by tank area instead of dividing flow by area',
    },
    "phys.radius_not_diameter": {
        "th": 'เทียบกับรัศมีแทนเส้นผ่านศูนย์กลาง',
        "en": 'Compared with radius instead of diameter',
    },
    "phys.image_distances_as_conjugates": {
        "th": 'ใช้ระยะภาพสองครั้งเป็นคู่ระยะวัตถุและภาพ',
        "en": 'Used the two image distances as object-image conjugates',
    },
    "phys.image_distance_as_focal": {
        "th": 'ตอบระยะภาพแทนความยาวโฟกัส',
        "en": 'Reported image distance instead of focal length',
    },
    "phys.doubled_focal": {
        "th": 'เพิ่มโฟกัสสองเท่าจากการหักเหสองสถานการณ์',
        "en": 'Doubled the focal length for the two imaging situations',
    },
    "phys.kinetic_half_missing": {
        "th": "ละตัวประกอบหนึ่งส่วนสองของพลังงานจลน์",
        "en": "Omitted the one-half factor in kinetic energy",
    },
    "phys.drag_range_unchanged": {
        "th": 'ถือว่าแรงต้านไม่ลดพิสัย',
        "en": 'Assumed drag left the range unchanged',
    },
    "phys.drag_height_unchanged": {
        "th": 'ถือว่าแรงต้านไม่ลดความสูงสูงสุด',
        "en": 'Assumed drag left maximum height unchanged',
    },
    "phys.drag_increases_motion": {
        "th": 'ถือว่าแรงต้านเพิ่มทั้งความสูงและพิสัย',
        "en": 'Assumed drag increased both height and range',
    },
    "phys.ignored_counterweight_weight": {"th": 'ละน้ำหนักตุ้มถ่วงที่ต้านการลง', "en": 'Omitted the counterweight weight opposing descent'},
    "phys.ignored_counterweight": {"th": 'คิดว่าระบบรอกตกอิสระโดยไม่มีตุ้มถ่วง', "en": 'Treated the pulley system as free fall without a counterweight'},
    "phys.ignored_launch_delay": {"th": 'ใช้ความสูงสูงสุดแทนความสูงที่สวนทาง', "en": 'Used maximum height instead of the delayed-launch crossing height'},
    "phys.wrong_crossing_time": {"th": 'ใช้ช่วงเวลาโยนแทนเวลาถึงจุดสวนทาง', "en": 'Used a launch interval instead of the crossing time'},
    "phys.used_launch_instant": {"th": 'ตอบความสูงลูกแรกขณะที่ลูกถัดไปเริ่มถูกโยน', "en": 'Reported the older ball height when the newer ball was launched'},
    "phys.total_force_as_tension": {"th": 'ตอบผลรวมแรงภายนอกแทนแรงตึงภายใน', "en": 'Reported total external force instead of internal tension'},
    "phys.end_force_difference": {"th": 'ตอบผลต่างแรงภายนอกแทนแรงตึง', "en": 'Reported the end-force difference instead of tension'},
    "phys.assumed_equal_block_masses": {"th": 'แบ่งแรงเหมือนก้อนทั้งสองมีมวลเท่ากัน', "en": 'Split forces as if the blocks had equal masses'},
    "phys.used_table_edge_distance": {"th": 'ใช้ระยะถึงขอบโต๊ะแทนระยะมวลแขวนถึงพื้น', "en": 'Used distance to the table edge instead of hanging-mass floor clearance'},
    "phys.speed_ratio_as_energy": {"th": 'ใช้สัดส่วนอัตราเร็วแทนสัดส่วนพลังงาน', "en": 'Used speed ratio instead of energy ratio'},
    "phys.other_particle_velocity": {"th": 'ใช้ความเร็วอนุภาคที่ถูกชนแทนอนุภาคแรก', "en": 'Used the struck particle velocity instead of the incident particle velocity'},
    "phys.inverted_mass_ratio_energy": {"th": 'ใช้กำลังสองของอัตราส่วนมวลกลับด้านแทนแก้การชน', "en": 'Used inverse squared mass ratio instead of solving the collision'},
    "phys.friction_assists_motion": {"th": 'ให้แรงเสียดทานช่วยวัตถุเคลื่อนที่ขึ้น', "en": 'Made friction assist uphill motion'},
    "phys.ignored_friction_work": {"th": 'ละงานต้านแรงเสียดทาน', "en": 'Omitted work against friction'},
    "phys.used_full_weight_on_incline": {"th": 'ใช้ขนาดน้ำหนักทั้งหมดเป็นแรงตามพื้นเอียง', "en": 'Used full weight as the force along the incline'},
    "phys.ignored_projectile_gravity": {"th": 'ละการตกเนื่องจากแรงโน้มถ่วงของโพรเจกไทล์', "en": 'Omitted gravitational fall of the projectile'},
    "phys.half_balloon_acceleration": {"th": 'ละตัวประกอบหนึ่งส่วนสองในการหาความเร่งลูกโป่ง', "en": 'Omitted the one-half displacement factor for balloon acceleration'},
    "phys.gravity_sign_wrong": {"th": 'กลับเครื่องหมายผลของแรงโน้มถ่วง', "en": 'Reversed the sign of gravity'},
    "phys.period_not_squared": {"th": 'ใช้คาบแทนคาบกำลังสองในแรงสู่ศูนย์กลาง', "en": 'Used period instead of squared period in centripetal force'},
    "phys.ignored_pendulum_length": {"th": 'ละอัตราส่วนความยาวเชือกลูกตุ้ม', "en": 'Omitted the pendulum string-length ratio'},
    "phys.subtracted_force_squares": {"th": 'ลบกำลังสองขนาดแรงต่างจุดเหมือนเป็นองค์ประกอบแรงเดียวกัน', "en": 'Subtracted squared magnitudes of forces at different points as if components'},
    "phys.assumed_equal_vertical_hinges": {"th": 'สมมติแรงแนวดิ่งของบานพับแบ่งเท่ากัน', "en": 'Assumed the two hinges shared vertical load equally'},
    "phys.upper_vertical_as_lower": {"th": 'ตอบองค์ประกอบแรงบานพับบนแทนแรงล่าง', "en": 'Reported the upper hinge vertical component instead of the lower force'},
    "phys.edge_charge_sign": {"th": 'กลับเครื่องหมายพลังงานของคู่ตามขอบ', "en": 'Edge charge sign'},
    "phys.diagonal_charge_sign": {"th": 'กลับเครื่องหมายพลังงานของคู่ตามเส้นทแยง', "en": 'Diagonal charge sign'},
    "phys.pair_energy_doubled": {"th": 'นับพลังงานแต่ละคู่ซ้ำสองครั้ง', "en": 'Pair energy doubled'},
    "phys.charge_linear_mass": {"th": 'ให้ประจุแปรตามมวลโดยตรง', "en": 'Charge linear mass'},
    "phys.charge_inverse_root_mass": {"th": 'ให้ประจุแปรผกผันรากที่สองของมวล', "en": 'Charge inverse root mass'},
    "phys.charge_inverse_mass": {"th": 'ให้ประจุแปรผกผันกับมวล', "en": 'Charge inverse mass'},
    "phys.assumed_equal_resistors": {"th": 'สมมติตัวต้านทานทั้งสามเท่ากัน', "en": 'Assumed equal resistors'},
    "phys.series_over_smallest": {"th": 'ใช้ตัวต้านทานตัวเล็กสุดแทนค่ารวมขนาน', "en": 'Series over smallest'},
    "phys.inverse_resistance_range": {"th": 'กลับอัตราส่วนความต้านทานมากสุดต่อน้อยสุด', "en": 'Inverse resistance range'},
    "phys.full_voltage_on_series_cap": {"th": 'ให้ตัวเก็บประจุอนุกรมรับแรงดันทั้งหมด', "en": 'Full voltage on series cap'},
    "phys.ignored_parallel_capacitors": {"th": 'ละตัวเก็บประจุที่ขนานร่วมอยู่', "en": 'Ignored parallel capacitors'},
    "phys.added_series_capacitances": {"th": 'บวกความจุตัวเก็บประจุที่ต่ออนุกรม', "en": 'Added series capacitances'},
    "phys.wire_diameter_as_radius": {"th": 'ตอบเส้นผ่านศูนย์กลางแทนรัศมี', "en": 'Wire diameter as radius'},
    "phys.wire_area_as_radius": {"th": 'ตอบค่ากำลังสองของรัศมีแทนรัศมี', "en": 'Wire area as radius'},
    "phys.wire_centimeter_as_meter": {"th": 'ใช้ความยาวหน่วยเซนติเมตรแทนเมตร', "en": 'Wire centimeter as meter'},
    "phys.inverse_pressure_difference": {"th": 'กลับอัตราส่วนผลต่างความหนาแน่น', "en": 'Inverse pressure difference'},
    "phys.ignored_heavy_liquid": {"th": 'ละความดันจากของเหลวหนักด้านล่าง', "en": 'Ignored heavy liquid'},
    "phys.same_liquid_depths": {"th": 'สมมติชั้นของเหลวต่างชนิดลึกเท่ากัน', "en": 'Same liquid depths'},
    "phys.gauge_in_gas_law": {"th": 'ใช้ความดันเกจในกฎแก๊สโดยตรง', "en": 'Gauge in gas law'},
    "phys.reported_absolute_pressure": {"th": 'ตอบความดันสัมบูรณ์แทนความดันเกจ', "en": 'Reported absolute pressure'},
    "phys.ambient_pressure_added": {"th": 'บวกความดันบรรยากาศแทนการลบ', "en": 'Ambient pressure added'},
    "phys.radius_gap_as_diameter": {"th": 'ใช้ช่องว่างรัศมีเป็นผลต่างเส้นผ่านศูนย์กลาง', "en": 'Radius gap as diameter'},
    "phys.millimeter_centimeter_mix": {"th": 'สับสนหน่วยมิลลิเมตรกับเซนติเมตร', "en": 'Millimeter centimeter mix'},
    "phys.ignored_temperature_interval": {"th": 'ละช่วงอุณหภูมิในการขยายตัว', "en": 'Ignored temperature interval'},
    "phys.lid_pressure_sign": {"th": 'บวกแรงดึงกับแรงบรรยากาศแทนการลบ', "en": 'Lid pressure sign'},
    "phys.lift_pressure_as_inside": {"th": 'ใช้ความดันจากแรงดึงเป็นความดันภายใน', "en": 'Lift pressure as inside'},
    "phys.ignored_lid_lift": {"th": 'ละแรงดึงฝาในการหาความดัน', "en": 'Ignored lid lift'},
    "phys.demagnified_lens_position": {"th": 'เลือกตำแหน่งเลนส์ที่ให้ภาพเล็กลง', "en": 'Demagnified lens position'},
    "phys.focal_length_as_object_distance": {"th": 'ตอบระยะโฟกัสแทนระยะวัตถุ', "en": 'Focal length as object distance'},
    "phys.midpoint_lens_position": {"th": 'วางเลนส์กลางระยะวัตถุถึงฉาก', "en": 'Midpoint lens position'},
    "phys.rocket_ignored_coast": {"th": 'ละความสูงช่วงเครื่องยนต์ดับ', "en": 'Rocket ignored coast'},
    "phys.rocket_ignored_powered_height": {"th": 'ละความสูงช่วงเครื่องยนต์ทำงาน', "en": 'Rocket ignored powered height'},
    "phys.rocket_thrust_as_net": {"th": 'บวก g ซ้ำกับความเร่งสุทธิ', "en": 'Rocket thrust as net'},
    "phys.wedge_ignored_acceleration": {"th": 'ละความเร่งของพื้นเอียง', "en": 'Wedge ignored acceleration'},
    "phys.wedge_acceleration_sign": {"th": 'กลับทิศความเร่งพื้นเอียง', "en": 'Wedge acceleration sign'},
    "phys.wedge_wrong_component": {"th": 'สลับองค์ประกอบแรงปกติ', "en": 'Wedge wrong component'},
    "phys.cylinder_ignored_torque": {"th": 'ละสมดุลโมเมนต์ทรงกระบอก', "en": 'Cylinder ignored torque'},
    "phys.cylinder_ignored_friction": {"th": 'ละแรงเสียดทานพยุงทรงกระบอก', "en": 'Cylinder ignored friction'},
    "phys.cylinder_wrong_rope_direction": {"th": 'ใช้เชือกผิดทิศ', "en": 'Cylinder wrong rope direction'},
    "phys.incline_relative_speed_halved": {"th": 'หารความเร็วสัมพัทธ์ด้วยสอง', "en": 'Incline relative speed halved'},
    "phys.incline_ignored_gravity": {"th": 'ละความลาดเอียง', "en": 'Incline ignored gravity'},
    "phys.incline_full_height": {"th": 'ใช้ระยะตกเต็มพื้นเอียง', "en": 'Incline full height'},
    "phys.impulse_initial_momentum_sign": {"th": 'บวกโมเมนตัมเริ่มต้นผิดทิศ', "en": 'Impulse initial momentum sign'},
    "phys.impulse_peak_rectangle": {"th": 'คิดกราฟแรงเป็นสี่เหลี่ยมที่แรงสูงสุด', "en": 'Impulse peak rectangle'},
    "phys.impulse_ignored_first_trapezoid": {"th": 'ละพื้นที่สี่เหลี่ยมคางหมูช่วงแรก', "en": 'Impulse ignored first trapezoid'},
    "phys.work_ignored_weight": {"th": 'ละงานของน้ำหนัก', "en": 'Work ignored weight'},
    "phys.work_added_weight": {"th": 'บวกงานของน้ำหนักแทนการลบ', "en": 'Work added weight'},
    "phys.work_weight_only": {"th": 'คิดเฉพาะขนาดงานน้ำหนัก', "en": 'Work weight only'},
    "phys.switch_total_current_as_branch": {"th": 'ใช้กระแสรวมแทนกระแสแขนง', "en": 'Switch total current as branch'},
    "phys.switch_ignored_voltage_drop": {"th": 'ละแรงดันตกที่ตัวต้านทานร่วม', "en": 'Switch ignored voltage drop'},
    "phys.switch_change_sign": {"th": 'กลับเครื่องหมายการเปลี่ยนกระแส', "en": 'Switch change sign'},
    "phys.buoyancy_ignored_torque": {"th": 'สมดุลแรงโดยละโมเมนต์รอบจุดหมุน', "en": 'Buoyancy ignored torque'},
    "phys.buoyancy_wrong_centroid": {"th": 'วางแรงลอยตัวที่ปลายส่วนจม', "en": 'Buoyancy wrong centroid'},
    "phys.buoyancy_ratio_inverted": {"th": 'กลับอัตราส่วนความหนาแน่น', "en": 'Buoyancy ratio inverted'},
    "phys.heat_ignored_melting": {"th": 'ละความร้อนหลอมเหลว', "en": 'Heat ignored melting'},
    "phys.heat_ignored_meltwater": {"th": 'ละความร้อนที่ใช้อุ่นน้ำแข็งที่ละลายแล้ว', "en": 'Heat ignored meltwater'},
    "phys.heat_ignored_final_metal_temperature": {"th": 'ละอุณหภูมิสุดท้ายของโลหะ', "en": 'Heat ignored final metal temperature'},
    "phys.beam_added_focal_magnitudes": {"th": 'บวกขนาดระยะโฟกัสแทนผลต่าง', "en": 'Beam added focal magnitudes'},
    "phys.beam_used_convex_focus": {"th": 'ตอบโฟกัสเลนส์นูนแทนระยะระหว่างเลนส์', "en": 'Beam used convex focus'},
    "phys.beam_reversed_gap": {"th": 'กลับเครื่องหมายระยะเลนส์', "en": 'Beam reversed gap'},
    "phys.resistivity_length_sign": {"th": 'กลับเครื่องหมายเลขชี้กำลังความยาวของสภาพต้านทาน', "en": 'Resistivity length sign'},
    "phys.resistivity_as_conductivity": {"th": 'สลับสภาพต้านทานกับสภาพนำ', "en": 'Resistivity as conductivity'},
    "phys.resistivity_as_conductance": {"th": 'ใช้ความนำไฟฟ้าแทนสภาพต้านทาน', "en": 'Resistivity as conductance'},
    "phys.lens_deflection_inverted": {"th": 'กลับอัตราส่วนความสูงต่อระยะโฟกัส', "en": 'Lens deflection inverted'},
    "phys.lens_deflection_square_root": {"th": 'ถอดรากอัตราส่วนแทนมุมเล็ก', "en": 'Lens deflection square root'},
    "phys.lens_deflection_squared": {"th": 'ยกกำลังสองอัตราส่วนแทนมุมเล็ก', "en": 'Lens deflection squared'},
    "phys.siphon_pressure_inverted": {"th": 'กลับอัตราส่วนหัวความดัน', "en": 'Siphon pressure inverted'},
    "phys.siphon_gravity_multiplied": {"th": 'คูณ g แทนการหาร', "en": 'Siphon gravity multiplied'},
    "phys.siphon_density_omitted": {"th": 'ละความหนาแน่นในหัวความดัน', "en": 'Siphon density omitted'},
    "phys.tank_surface_speed_ignored": {"th": 'ละอัตราเร็วผิวน้ำในถัง', "en": 'Tank surface speed ignored'},
    "phys.tank_bernoulli_sign": {"th": 'กลับเครื่องหมายพลังงานผิวน้ำ', "en": 'Tank bernoulli sign'},
    "phys.tank_area_not_squared": {"th": 'ไม่ยกกำลังสองอัตราส่วนพื้นที่', "en": 'Tank area not squared'},
    "phys.em_speed_reciprocal": {"th": 'กลับอัตราส่วนสนามแม่เหล็กไฟฟ้า', "en": 'Em speed reciprocal'},
    "phys.em_speed_no_square_root": {"th": 'ไม่ถอดรากผลคูณค่าตัวกลาง', "en": 'Em speed no square root'},
    "phys.em_permeability_ignored": {"th": 'ละความซึมผ่านแม่เหล็กของตัวกลาง', "en": 'Em permeability ignored'},
    "phys.cone_speed_squared": {"th": 'ตอบอัตราเร็วยกกำลังสอง', "en": 'Cone speed squared'},
    "phys.cone_height_inverted": {"th": 'กลับตำแหน่งความสูงในอัตราเร็ว', "en": 'Cone height inverted'},
    "phys.cone_normal_vertical_only": {"th": 'ใช้สองเท่าของพลังงานศักย์โดยละแรงปกติ', "en": 'Cone normal vertical only'},
    "phys.conduction_drop_as_temperature": {"th": 'ตอบอุณหภูมิที่ลดลงแทนอุณหภูมิจริง', "en": 'Conduction drop as temperature'},
    "phys.conduction_distance_from_cold": {"th": 'วัดระยะจากปลายเย็นแทนปลายร้อน', "en": 'Conduction distance from cold'},
    "phys.conduction_hot_fraction": {"th": 'คูณอุณหภูมิร้อนด้วยสัดส่วนระยะ', "en": 'Conduction hot fraction'},
    "phys.pendulum_expansion_doubled": {"th": 'คูณการขยายเชิงเส้นด้วยสอง', "en": 'Pendulum expansion doubled'},
    "phys.pendulum_unity_omitted": {"th": 'ละความยาวเริ่มต้นในอัตราส่วน', "en": 'Pendulum unity omitted'},
    "phys.pendulum_period_linear_length": {"th": 'ให้คาบแปรตามความยาวโดยตรง', "en": 'Pendulum period linear length'},
    "phys.arc_potential_full_circle": {"th": 'คิดประจุส่วนโค้งเพิ่มเป็นสองเท่า', "en": 'Arc potential full circle'},
    "phys.arc_potential_half_charge": {"th": 'คิดประจุส่วนโค้งเพียงครึ่งเดียว', "en": 'Arc potential half charge'},
    "phys.arc_potential_radius_left": {"th": 'หารรัศมีซ้ำหลังแทนประจุรวม', "en": 'Arc potential radius left'},
    "phys.virtual_magnification_no_unity": {"th": 'ละพจน์หนึ่งในกำลังขยายภาพเสมือน', "en": 'Virtual magnification no unity'},
    "phys.virtual_image_sign_wrong": {"th": 'ใส่เครื่องหมายระยะภาพเสมือนผิด', "en": 'Virtual image sign wrong'},
    "phys.near_point_substituted": {"th": 'ใช้ระยะใกล้ตา 25 cm แทนระยะภาพที่กำหนด', "en": 'Near point substituted'},
    "phys.semicircle_fields_added": {"th": 'บวกสนามจากส่วนโค้งที่กระแสสวนกัน', "en": 'Semicircle fields added'},
    "phys.semicircle_full_loop": {"th": 'ใช้สูตรวงกลมเต็มกับครึ่งวงกลม', "en": 'Semicircle full loop'},
    "phys.semicircle_outer_ignored": {"th": 'ละสนามจากส่วนโค้งนอก', "en": 'Semicircle outer ignored'},
    "phys.rope_total_weight_one_side": {"th": 'ให้ข้างเดียวรับน้ำหนักเชือกทั้งหมด', "en": 'Rope total weight one side'},
    "phys.rope_end_tension_as_bottom": {"th": 'ใช้ขนาดแรงตึงปลายเชือกแทนแรงตึงจุดต่ำสุด', "en": 'Rope end tension as bottom'},
    "phys.rope_angle_from_horizontal": {"th": 'วัดมุมจากแนวระดับแทนแนวดิ่ง', "en": 'Rope angle from horizontal'},
    "phys.opposed_batteries_added": {"th": 'บวกแรงเคลื่อนไฟฟ้าที่ขั้วต้านกัน', "en": 'Opposed batteries added'},
    "phys.middle_resistance_only": {"th": 'ละตัวต้านทานในแขนงนอก', "en": 'Middle resistance only'},
    "phys.middle_current_outer_only": {"th": 'ละตัวต้านทานในแขนงกลาง', "en": 'Middle current outer only'},
    "phys.capacitor_divider_wrong_resistor": {"th": 'ใช้แรงดันคร่อมตัวต้านทานตัวบน', "en": 'Capacitor divider wrong resistor'},
    "phys.capacitor_full_source_voltage": {"th": 'ให้ตัวเก็บประจุรับแรงดันแหล่งจ่ายเต็ม', "en": 'Capacitor full source voltage'},
    "phys.capacitor_current_continuity": {"th": 'คิดว่ากระแสตัวเก็บประจุต้องต่อเนื่องเป็นศูนย์', "en": 'Capacitor current continuity'},
    "phys.collision_used_one_radius": {"th": 'ใช้รัศมีเดียวแทนผลรวมรัศมี', "en": 'Collision used one radius'},
    "phys.collision_tangent_instead_sine": {"th": 'ใช้แทนเจนต์ของระยะต่อรัศมีเดียว', "en": 'Collision tangent instead sine'},
    "phys.collision_sine_as_tangent": {"th": 'ใช้แทนเจนต์แทนไซน์ของแนวศูนย์กลาง', "en": 'Collision sine as tangent'},
    "phys.isobaric_heat_as_internal": {"th": 'ให้ความร้อนทั้งหมดเป็นพลังงานภายใน', "en": 'Isobaric heat as internal'},
    "phys.monatomic_cp_as_seven_halves": {"th": 'ใช้ความจุความร้อนเจ็ดส่วนสองสำหรับแก๊สอะตอมเดี่ยว', "en": 'Monatomic cp as seven halves'},
    "phys.isobaric_heat_as_work": {"th": 'คิดเฉพาะงานขยายตัว', "en": 'Isobaric heat as work'},
    "phys.maximum_power_missing_four": {"th": 'ละตัวหารสี่ในกำลังสูงสุด', "en": 'Maximum power missing four'},
    "phys.maximum_power_emf_unsquared": {"th": 'ไม่ยกกำลังสองแรงเคลื่อนไฟฟ้า', "en": 'Maximum power emf unsquared'},
    "phys.maximum_power_missing_internal": {"th": 'ละความต้านทานภายในในกำลังสูงสุด', "en": 'Maximum power missing internal'},
    "phys.inductor_node_voltage_sign": {"th": 'กลับเครื่องหมายศักย์หลังสับตัวเหนี่ยวนำ', "en": 'Inductor node voltage sign'},
    "phys.inductor_voltage_equals_source": {"th": 'ให้ศักย์หลังสับเท่ากับขนาดแรงเคลื่อนไฟฟ้าเดิม', "en": 'Inductor voltage equals source'},
    "phys.inductor_current_reset_zero": {"th": 'ให้กระแสตัวเหนี่ยวนำเป็นศูนย์ทันที', "en": 'Inductor current reset zero'},
    "phys.falling_rod_ignored_rotation": {"th": 'ละพลังงานจลน์การหมุนของแท่ง', "en": 'Falling rod ignored rotation'},
    "phys.falling_rod_ignored_translation": {"th": 'ละพลังงานจลน์การเลื่อนที่ของศูนย์กลาง', "en": 'Falling rod ignored translation'},
    "phys.falling_rod_half_available_energy": {"th": 'คิดพลังงานศักย์ที่เสียไปเพียงครึ่งเดียว', "en": 'Falling rod half available energy'},
    "phys.minimum_pull_horizontal_only": {"th": 'คิดเฉพาะการดึงในแนวระดับ', "en": 'Minimum pull horizontal only'},
    "phys.minimum_pull_unnormalized_components": {"th": 'รวมองค์ประกอบแรงโดยไม่ทำเวกเตอร์หน่วย', "en": 'Minimum pull unnormalized components'},
    "phys.minimum_pull_mu_omitted": {"th": 'ละตัวคูณสัมประสิทธิ์เสียดทาน', "en": 'Minimum pull mu omitted'},
    "phys.capacitor_negative_quadratic_root": {"th": 'เลือกคำตอบรากลบที่ไม่ใช่ความจุบวก', "en": 'Capacitor negative quadratic root'},
    "phys.capacitor_quadratic_missing_half": {"th": 'ละตัวหารสองในสูตรรากสมการ', "en": 'Capacitor quadratic missing half'},
    "phys.capacitor_quadratic_missing_subtraction": {"th": 'ละพจน์ลบก่อนหารสองในสูตรรากสมการ', "en": 'Capacitor quadratic missing subtraction'},
    "phys.spool_sine_threshold": {"th": 'ใช้ไซน์แทนโคไซน์ที่มุมวิกฤตล้อ', "en": 'Spool sine threshold'},
    "phys.spool_tangent_threshold": {"th": 'ใช้แทนเจนต์แทนโคไซน์ที่มุมวิกฤตล้อ', "en": 'Spool tangent threshold'},
    "phys.spool_complement_radius": {"th": 'ใช้ผลต่างรัศมีแทนรัศมีเพลา', "en": 'Spool complement radius'},
    "phys.rolling_point_speed_relative_center": {"th": 'ตอบอัตราเร็วเทียบศูนย์กลางล้อแทนพื้น', "en": 'Rolling point speed relative center'},
    "phys.rolling_point_wrong_angle_origin": {"th": 'วัดมุมจากรัศมีชี้ลงแทนชี้ขึ้น', "en": 'Rolling point wrong angle origin'},
    "phys.rolling_point_full_angle_cosine": {"th": 'ใช้มุมเต็มแทนมุมครึ่งในอัตราเร็ว', "en": 'Rolling point full angle cosine'},
    "phys.pendulum_collision_quarter_period": {"th": 'ตอบหนึ่งในสี่คาบแทนช่วงกลับมาชน', "en": 'Pendulum collision quarter period'},
    "phys.pendulum_collision_full_period": {"th": 'ตอบหนึ่งคาบเต็มแทนช่วงกลับมาชน', "en": 'Pendulum collision full period'},
    "phys.pendulum_collision_mass_ratio": {"th": 'ใส่อัตราส่วนมวลในคาบลูกตุ้ม', "en": 'Pendulum collision mass ratio'},
    "phys.ring_field_point_charge": {"th": 'ใช้สนามประจุจุดที่ระยะตามแกนโดยละรัศมีวงแหวน', "en": 'Ring field point charge'},
    "phys.ring_field_missing_projection": {"th": 'ละการฉายสนามตามแกน', "en": 'Ring field missing projection'},
    "phys.ring_field_half_ring": {"th": 'นับประจุบนวงแหวนเพียงครึ่งเดียว', "en": 'Ring field half ring'},
    "phys.symmetric_collision_one_target": {"th": 'คิดการชนเป้าเดียวแทนสองเป้าพร้อมกัน', "en": 'Symmetric collision one target'},
    "phys.symmetric_collision_no_rebound": {"th": 'กำหนดความเร็วหลังชนโดยละการกระดอนและพลังงาน', "en": 'Symmetric collision no rebound'},
    "phys.symmetric_collision_mass_lumped": {"th": 'รวมมวลเป้าสองก้อนเป็นก้อนเดียว', "en": 'Symmetric collision mass lumped'},
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
