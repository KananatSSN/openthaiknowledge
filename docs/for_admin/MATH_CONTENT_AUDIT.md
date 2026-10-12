# Math content audit — learning curve and variety (2026-09-25)

Scope: the 738 IPST sets (`สสวท. พื้นฐาน` 544, `สสวท. เพิ่มเติม` 194) in 163
topics. สอวน. (180) and อุดมศึกษา (89) are sampled in the evidence file but not
assessed here.

Evidence: `math_content_audit.csv`, from `scripts/audit_math_content.py`.
Each set was drawn 300 times from a fixed seed. A *shape* is a stem with its
numbers, number words, and story names and colours masked. Two items that
differ only in their numbers, or in who buys the apples, share a shape.
Curriculum gaps were read against the 2560 indicator book
(`docs/curriculum_sources/_md/indicators.jsonl`).

## Summary

| Finding | Size |
|---|---|
| The three stages differ in content but not in support: 4 choices at every stage, and hints in only 15% of Foundation sets | 723 of 738 sets offer 4 choices |
| Application sets with no situation (a bare harder computation) | 44% of Application sets |
| Sets with a single stem shape | 139 (19%); 63 more have two |
| Small banks: 30 or fewer distinct items in 300 draws | 87 sets; 37 have 10 or fewer |
| Core indicators with no set that teaches them | about 30, mostly ป.2–ป.6 measurement, fractions and data |
| Content at the wrong grade | ม.2 ↔ ม.3 statistics and factorising; ป.4 two-way tables at ป.5 |
| Topics whose Application stage has 2 or fewer shapes | 22 |
| Generation failures, answer-position bias | none |

The biggest gains in order: make the stages scaffold (1), close the
curriculum gaps (2), replace the small banks (4).

## Progress since the audit

- **Stages (1):** done. Foundation sets offer 3 choices, and every
  Foundation and Fluency set shows a strategy after answering.
- **Curriculum gaps (2):** closed, with 66 new sets. `math_gaps_primary`
  has 15, `math_gaps_shape_data` 14 and `math_gaps_secondary` 24. The
  secondary sets cover ม.2 and ม.3 factorising, core ม.4 counting and
  probability, and core ม.5 radicals, functions in context and interest.
  They also add ม.4 additional rational equations and ม.6 additional
  uniform distribution. A later check went through all 157 core indicators
  and 32 additional outcomes one by one. It found 15 more that sat in an
  existing topic but that no set taught, and `math_gaps_indicators` adds 13
  sets for them:
  - two-step decimal problems (ป.4/16)
  - dividing by a decimal, and three-step decimal problems (ป.6/9–10)
  - writing a ratio (ป.6/2)
  - ห.ร.ม. and ค.ร.น. of three numbers (ป.6/4–5)
  - writing a one-way table (ค 3.1 ป.3/2)
  - naming angles, and constructing one with a protractor (ค 2.2 ป.4/1,
    ค 2.1 ป.4/2)
  - function arithmetic (additional จำนวนและพีชคณิต 2 ม.4/1)
  - degree-3 and degree-4 polynomial equations and inequalities (3 ม.4/1,
    ม.5/6)
  - the matrix transpose and row operations (3 ม.5/3, 5)

  Every indicator and outcome now has at least one set. 99 core indicators
  are still filed as their standard and grade only (`ค 1.1 ป.4/*`), because
  their topic mixes several indicators.
- **Filing (3):** done as decided. Statistics moved to the book's grades,
  two-way tables to ป.4, and ป.6 circles to ค 2.1. Factorising was added at
  ม.2 and ม.3, and no set was moved.
- **Small banks (4):** the audit counted every picture as the same
  `[image]`, so it undercounted picture sets. The script now names each
  picture. The recount, with the new sets, found 28 IPST sets with 10 or
  fewer distinct items. Widening 23 of them leaves 3. Two are limited by
  the special angles (`trig_equation_tangent`, `inverse_trig_negative`),
  and ป.3 `symmetry_axes` is limited by the shapes a ป.3 learner knows. The
  ป.2 shape pictures later gained 24 polygon drawings with 3–8 sides, each
  regular, turned or irregular, which are drawn on demand.
- **One-sentence word problems (4):** 14 sets now tell several stories.
  Among them are ป.4 estimating, the ม.5 sine rule on land and at sea, and
  ม.6 normal distributions of heights, bulb life and travel time. Most of
  the others the audit flagged are picture or instruction sets, not word
  problems.
- **Thin Application stages (4):** `math_apply_stage` adds 19 Application
  sets, and two topics moved an existing word-problem set into
  Application. No IPST topic now ends in a single bare computation.
- **Smoothness (5):**
  - *Top-heavy topics:* ป.1 การวัด, ป.3 เงิน, ป.4 เส้นตรงและมุม, ป.5 ร้อยละ,
    ม.1 สมการเชิงเส้น and ม.5 ฟังก์ชันตรีโกณมิติ each moved a word-problem
    set from Fluency into Application.
  - *ป.3 การคูณ:* three-digit × one-digit is now a Fluency step before four
    digits.
  - *ป.4 estimating:* now rounds to tens, hundreds or thousands, not only
    two-digit tens.
  - *ม.1 นิพจน์พีชคณิต:* ends in expressions in context.
  - *The audit's number measure:* it read `45{,}327` in TeX as 45 and 327,
    which made several jumps look larger than they are. That is fixed.
  - *Remaining jumps:* the number jumps left come from money and unit
    conversions, so they are real amounts. The reading-load jumps left
    are the step from a computation to its word problem.

## 1. The stages do not scaffold

The math curriculum plan described Foundation as two choices with an
explicit strategy hint, and Fluency as three choices with a checking hint.
The audit finds:

| Stage | Sets | 4 choices | Has a hint | Has a picture | Set in a situation |
|---|---:|---:|---:|---:|---:|
| 1 ปูพื้นฐาน | 255 | 98% | 15% | 22% | 33% |
| 2 ฝึกคล่อง | 261 | 99% | 13% | 10% | 40% |
| 3 ประยุกต์ | 222 | 99% | 9% | 2% | 56% |

The stated choice counts came from the retired `math.ipst.*` filler sets.
Now that every topic has authored sets, nothing lowers the load at
Foundation. What a learner meets first is as open as what they meet last,
and a first wrong answer gets no strategy.

- **Support fades on schedule.** Serve Foundation with 2–3 choices, keeping
  the strongest distractors, and a one-line strategy hint. Serve Fluency
  with 3–4 choices and a checking hint, and Application with the full set
  and no hint. This can be done where a question is served, for every set
  at once, instead of set by set.
- **Application means a new situation.** 98 Application sets are a bigger or
  two-step computation with no context. For each, add one situation or a
  "choose the right number sentence" form, as `math_apply_basic.py` did for
  ten topics.
- **Pictures at the start of ป.1–ป.3.** 17 early-grade topics open with text
  only: ป.1 การบวกลบระคน, การวัด, เรขาคณิต 3 มิติ, แบบรูป, โจทย์ปัญหา;
  ป.2 การบวกและการลบ, บวก ลบ คูณ หารระคน, แบบรูป; ป.3 การคูณ, การวัด,
  การหาร, ค่าประจำหลัก, ตารางทางเดียว, เงิน, เวลา, แบบรูป,
  โจทย์ปัญหาระคน. ป.1 การวัด has its ruler picture at Fluency, after the
  text-only Foundation.

## 2. Curriculum gaps — indicators no set teaches

Checked indicator by indicator against the set names in each grade. Codes
are the book's.

**Measurement (ค 2.1), the largest gap**
- ป.2/6 ปริมาตรและความจุเป็นลิตร: no ป.2 volume set at all.
- Estimating (คาดคะเน) length, weight and capacity: ป.3/4, ป.3/8, ป.3/12.
  No set asks for a reasonable estimate.
- Choosing a measuring tool: ป.3/3, ป.3/7, ป.3/11.
- เมตริกตัน: ป.3/9–10. No set uses tonnes.
- ป.5/1–2: word problems converting length and weight units, answered in
  decimals. ป.5 has no unit-conversion set.

**Numbers (ค 1.1)**
- ป.3/5 and ป.4/8: unknowns in addition and subtraction sentences with large
  numbers (up to 100,000 at ป.3, beyond 100,000 at ป.4). No add/subtract
  topic exists at ป.3 or ป.4.
- ป.4/4: comparing and ordering fractions whose denominators are multiples.
- ป.4/12: writing a two-step word problem. As a multiple-choice item: which
  story fits this number sentence.
- ป.6/1, ป.6/7, ป.6/8: comparing fractions and mixed numbers, mixed
  operations, and 2–3-step fraction problems. ป.6 has no fraction topic;
  one ลำดับการดำเนินการ (เศษส่วน) set touches ป.6/7.

**Geometry (ค 2.2)**
- ป.5/4 ลักษณะของปริซึม and ป.6/4 รูปคลี่. Nets appear only at ม.1.
- Constructions ป.4/2, ป.5/3, ป.6/2, ม.2/1. Only ม.1 has construction sets.
  As multiple choice: which step comes next, or which drawing follows the
  steps.

**Data (ค 3.1)**
- ป.3/1 and ป.5/2: making a pictograph or bar chart from data. Every chart
  set reads a chart; none asks which chart shows the data.

**Core ม.4–ม.5.** Since the correction of 2026-09-25, core ค 3.2 ม.4/1–2
(counting, probability), ค 1.1 ม.5/1 (radicals, rational exponents),
ค 1.2 ม.5/1 (functions) and ค 1.3 ม.5/1 (interest) have no core set. A
learner on the core track goes from ม.4 sets and logic to ม.6 statistics
with only ลำดับและอนุกรม in between. Core-level sets for these, easier than
the additional-course ones, would fill the track.

**Additional course**
- จำนวนและพีชคณิต 3 ม.4/2: rational (fractional) equations and inequalities.
- สถิติและความน่าจะเป็น 1 ม.6/1: the uniform distribution. Binomial and
  normal are covered.

## 3. Content at the wrong grade or standard

- **ม.2 ↔ ม.3 statistics.** The book puts ค่ากลางของข้อมูล at ม.2
  (ค 3.1 ม.2/1) and แผนภาพกล่อง at ม.3 (ค 3.1 ม.3/1). The catalog has the
  box-plot topic at ม.2, filed `exact` to ม.2/1, and mean and median at ม.3.
- **ม.2 ↔ ม.3 factorising.** The book has degree-2 factorising at ม.2
  (ค 1.2 ม.2/2) and degree above 2 at ม.3 (ม.3/1). ม.2 has no factorising
  set. ม.3 แยกตัวประกอบ is degree-2 work (difference of squares,
  trinomials) filed `exact` to ม.3/1. The degree-3 sets (sum and difference
  of cubes, grouping) sit in ม.4 เพิ่มเติม.
- **ป.4 two-way tables.** ค 3.1 ป.4/1 names ตารางสองทาง at ป.4. The sets are
  in ป.5 การนำเสนอข้อมูล.
- **ป.6 วงกลม.** Circumference and area are ค 2.1 ป.6/3 (measurement). The
  topic is filed under ค 2.2 because the keyword วงกลม routes to geometry.
- **Beyond the additional course.** Derivatives of sin, cos, eˣ and ln, and
  integration by parts and by substitution (6 sets), go beyond ม.6
  additional, which covers algebraic functions only. They fit the
  อุดมศึกษา course.
- **Above grade.** ป.6 ลำดับการดำเนินการ (มีเลขยกกำลัง) uses exponents, which
  the book introduces at ม.1.

Moving a set to another grade or topic changes its learner-facing identity,
so each of these needs a decision; they are not fixed here.

## 4. Variety

**Whole topics built on small banks.** A learner exhausts these within a
session:

| Topic | Sets and distinct items (of 300 draws) |
|---|---|
| ป.4 เส้นตรงและมุม | classify_line 3, angle_kind_picture 3, line_ray_picture 3 |
| ป.3 รูปสมมาตร | symmetry_axes 4, symmetry_picture 8, symmetry_regular_polygon 8, symmetry_letter 25 |
| ป.5 ชนิดของรูปสี่เหลี่ยม | parallelogram_properties 4, classify_quadrilateral 5, quadrilateral_picture 13 |
| ป.5 เส้นขนาน | parallel_pair_picture 2, parallel_angle_picture 10 |
| ป.6 วงกลม | circle_parts 4, area_circumference 18, radius_from_circumference 24 |
| ม.2 ความเท่ากันทุกประการ | congruence_case 4, congruence_picture 9 |
| ม.4 ตรรกศาสตร์ | valid_argument 4, logic_negation 5, logic_equivalence 10, truth_value 16 |
| ม.5 ตัวผกผันของฟังก์ชันตรีโกณมิติ | inverse_trig_range 4, inverse_trig_negative 6, inverse_trig 24 |
| ม.5 สมการตรีโกณมิติ | trig_equation_tangent 3, trig_equation_general 6 |
| ม.6 สถิติประยุกต์ | classify_data_type 6, measurement_scale 6, data_type_classify 12 |
| ม.6 อินทิเกรตทีละส่วน | parts_choose_u 4, parts_x_exponential 5, integration_by_parts 20 |

Other small banks: ป.1 classify_2d_shape (6), polygon_sides (8),
classify_3d_solid (8); ป.2 shape_sides_picture (8); ป.1–ป.2 ruler and scale
pictures (23, 30); ม.2 literal_equation_area (5), polygon_angle_sum (16);
ม.3 trig_special_values (9), cone_sphere_surface_area (10); ม.5
unit_circle_picture (6); ม.6 regression_correlation (6), area_two_curves
(8), repeating_decimal_to_fraction (8). The full list is the 87 rows of the
evidence file with `distinct_items` ≤ 30.

For a picture set, the fix is parameterising the figure: random side
lengths, angles and orientations, which the renderer already supports for
most figures. For a classification set, it is a larger pool of objects and
statements.

**Word problems in one sentence.** 42 context sets repeat one or two frames,
for example ป.3 change_picture (a single frame, 282 items), ป.4
estimate_sum and estimate_product, ม.1 largest_prime_factor, ม.5
triangle_area_sine and sine_rule_side, ม.6 normal_curve_picture. The list
is the rows with `shapes` ≤ 2 and `context` true. `_story.py` already has
the situations; these sets predate it.

**Thin Application stages.** 22 topics end in an Application stage with 2
or fewer shapes. Among them: ป.1 การบวก and การลบ, ป.1 and ป.2 แบบรูป, ป.6
จำนวนเฉพาะ, ป.6 ห.ร.ม. และ ค.ร.น., ม.1 แยกตัวประกอบเฉพาะ, ม.4 จัดรูปกรณฑ์,
ม.5 ทฤษฎีบททวินาม, ม.6 อนุกรม and ม.6 อินทิเกรตทีละส่วน. Five topics have 6
or fewer shapes in total: ป.1 เรขาคณิต 2 มิติ, ป.6 จำนวนเฉพาะ, ป.6 แบบรูป,
ม.1 แยกตัวประกอบเฉพาะ and ม.5 ทฤษฎีบททวินาม.

## 5. Smoothness within a topic

These are proxies (the largest number in the stem, stem length). Each needs
a look before acting.

- **One Application set after five or more earlier sets:** ป.1 การวัด,
  ป.3 เงิน, ป.4 ทศนิยม, ป.4 เส้นตรงและมุม, ป.5 ร้อยละ, ม.1 สมการเชิงเส้น,
  ม.5 ฟังก์ชันตรีโกณมิติ. The last stage is the narrowest, where it should
  be the richest.
- **Number-size jumps of 50× or more between stages:** ป.3 การคูณ (Fluency
  multiplies by two digits, Application by four), ป.4 การประมาณค่า, ป.5
  ปริมาตร (unit cubes, then litres and cm³), ป.6 ร้อยละ, ป.6 ทศนิยม, ม.4
  ความสัมพันธ์และฟังก์ชัน, ม.5 ลำดับและอนุกรม. A middle set, for example three-digit multiplication at ป.3, would smooth the step.
- **Reading-load jumps:** ม.2 สถิติ (แผนภาพกล่อง) goes from 52 to 280
  characters, and ม.5 เวกเตอร์ from 44 to 156.
- **Inverted:** ม.1 นิพจน์พีชคณิต opens with longer stems and larger numbers
  than it ends with.

## Suggested order

1. Scaffold the stages where questions are served: choice count and hints
   by stage. It touches every set, and it changes no content.
2. Fill the ป.2–ป.6 measurement gaps (estimating, tools, tonnes, ป.2
   litres, ป.5 conversions) and the ป.6 fraction topic.
3. Decide the ม.2 ↔ ม.3 swaps, the ป.4 two-way tables and the ป.6 circle
   standard. Then add ม.2 factorising and ม.3 degree-3 factorising.
4. Parameterise the small-bank topics in section 4, geometry pictures first.
5. Give the one-sentence word problems the `_story.py` situations, and
   widen the thin Application stages.
6. Add core-level ม.4–ม.5 sets and the two missing additional outcomes.

## Re-running

```bash
python -X utf8 scripts/audit_math_content.py   # ~10 minutes, rewrites the CSV
```
