"""Coverage and behavior checks for the three-stage IPST learning paths."""

from __future__ import annotations

from collections import defaultdict
from random import Random

from otk.core import REGISTRY, catalog, generate
from otk.sets._support.math_progression import ADDED_IPST_PROGRESSION_SETS


def _ipst_groups():
    groups = defaultdict(list)
    for row in catalog():
        if row["subject"] != "คณิตศาสตร์" or row["course_type"] not in {
            "สสวท. พื้นฐาน", "สสวท. เพิ่มเติม",
        }:
            continue
        node = (
            row["course_type"], row["level"], row["strand_code"],
            row["standard_code"], row["topic"],
        )
        groups[node].append(row)
    return groups


def test_every_ipst_topic_has_a_complete_three_stage_path():
    groups = _ipst_groups()
    # 183 at review; math_p1 opened ป.1 การบวกลบระคน, แบบรูป and แผนภูมิรูปภาพ;
    # math_p2 ป.2 การหาร, บวก ลบ คูณ หารระคน and แบบรูป; math_p3 ป.3 เวลา,
    # แบบรูป and โจทย์ปัญหาระคน; math_p4 ป.4 ค่าประจำหลัก, เศษส่วน, โจทย์ปัญหาระคน
    # and เวลา; math_p5 ป.5 โจทย์ปัญหาเศษส่วน, บัญญัติไตรยางศ์ and ตารางสองทาง;
    # math_p6 ป.6 แบบรูป; math_m1 ม.1 ทศนิยมและเศษส่วน and มิติสัมพันธ์ของรูปเรขาคณิต;
    # math_m2 ม.2 สถิติ; math_m3 ม.3 ความน่าจะเป็นเบื้องต้น; math_m4–m6 ม.4 ภาคตัดกรวย,
    # ม.5 ลำดับและอนุกรม, ม.6 ค่ากลางของข้อมูล and การแจกแจงความน่าจะเป็น (208).
    # Consolidating one-set fragments into their book chapters
    # (MATH_TOPIC_RENAMES, MATH_TOPIC_ASSIGNMENTS) then removed 51, and
    # math_chapters opened six chapters that had no set: ป.2 เงิน and
    # รูปเรขาคณิต, ม.2 การให้เหตุผลทางเรขาคณิต, ม.4 ฟังก์ชัน, ม.5 กฎของไซน์ and
    # ม.6 การนำเสนอข้อมูลเชิงปริมาณ (163). Filing statistics at the book's
    # grades moved mean and median to ม.2 สถิติ and box plots to ม.3, which
    # emptied ม.3 สถิติ (162). math_gaps_primary opened ป.3 and ป.4
    # การบวกและการลบ and ป.5 ความยาวและน้ำหนัก (165), and math_gaps_shape_data
    # ป.5 ปริซึม, ป.6 เศษส่วนและจำนวนคละ and ป.4 การนำเสนอข้อมูล, where the
    # two-way tables moved (168). math_gaps_secondary opened ม.2 การแยกตัว
    # ประกอบของพหุนามดีกรีสอง, the core ม.4 counting and probability topics,
    # three core ม.5 topics and ม.4 สมการและอสมการเศษส่วน (175).
    assert len(groups) == 175
    assert min(map(len, groups.values())) >= 3
    assert all({row["learning_stage"] for row in rows} == {1, 2, 3}
               for rows in groups.values())


def test_expansion_adds_the_reviewed_195_sets_in_three_delivery_batches():
    # 196 at review; ม.2 เอกนามและพหุนาม later got its own authored ladder,
    # so its fluency filler set is no longer generated. The ป.1 enrichment
    # (math_p1) then filled ป.1 โจทย์ปัญหา and การเปรียบเทียบ with authored
    # sets, retiring their two fillers; ป.2 and ป.3 (math_p2, math_p3) retired
    # 22 more, ป.4–ป.6 (math_p4–p6) 26 more, ม.1–ม.3 (math_m1–m3) 11 more, and
    # the drawn-diagram sets (math_diagrams) 5 more, and ม.4–ม.6 (math_m4–m6,
    # math_diagrams_hi) 5 more. Consolidating fragmented topics into their
    # book chapters retired 103 more: a merged chapter has three authored sets.
    # The drawn geometry sets (math_diagrams_geo) retired 5 more, in ป.5 and
    # ม.2 เส้นขนาน, ป.6 ชนิดของรูปสามเหลี่ยม and ม.2 แผนภาพกล่อง. The third
    # sets in math_thin_topics retired the last 16: every topic now has three
    # authored sets, and the filler machinery generates nothing.
    added = [row for rows in _ipst_groups().values() for row in rows
             if row["key"].startswith("math.ipst.")]
    assert ADDED_IPST_PROGRESSION_SETS == len(added) == 0


def test_supported_sets_keep_source_math_and_add_real_support():
    rows = [row for rows in _ipst_groups().values() for row in rows
            if row["key"].startswith("math.ipst.")]
    for row in rows:
        assert row["source_key"] in REGISTRY
        assert row["source_key"] != row["key"]
        question = generate(row["key"], Random(20260904))
        assert question.hint
        assert len(question.choices) == row["learning_stage"] + 1
