"""Curriculum placement for สาระภูมิศาสตร์ (ส 5), by unit.

Geography is a strand of the social-studies learning area, but its 2560
indicators were revised with mathematics and science and printed in the same
book (มาตรฐานการเรียนรู้และตัวชี้วัด คณิต วิทย์ ภูมิศาสตร์ 2560), so its sets
file into the same basic course as theirs. ``indicators.jsonl`` holds its codes
(``scripts/geography_indicators.py``).

A set is filed by its level and unit (its ``topic``), not by key: every set in a
unit file practises that unit's indicators, so one row per unit is the whole
mapping. The ม.4-6 indicators are a range (``ส 5.1 ม.4-6/3``); their sets are
filed at ม.4.
"""

from __future__ import annotations

from hashlib import sha256

from .curriculum_math import BASIC, CURRICULUM_VERSION, CurriculumPlacement

GEOGRAPHY_SUBJECT = "ภูมิศาสตร์"
GEOGRAPHY_NODE_PREFIX = "th-geo-2560-"
GEOGRAPHY_STRANDS = {"ส 5": "ภูมิศาสตร์"}
GEOGRAPHY_STRAND_ORDER = tuple(GEOGRAPHY_STRANDS)

# (level, unit) -> (standard, indicator codes).
GEOGRAPHY_UNITS: dict[tuple[str, str], tuple[str, tuple[str, ...]]] = {
    ("ป.1", "สิ่งแวดล้อมรอบตัว"): ("ส 5.1", ("ส 5.1 ป.1/1", "ส 5.2 ป.1/1")),
    ("ป.1", "ตำแหน่งและทิศของสิ่งต่าง ๆ"): ("ส 5.1", ("ส 5.1 ป.1/2", "ส 5.1 ป.1/3")),
    ("ป.2", "ทรัพยากรธรรมชาติ"): ("ส 5.2", ("ส 5.2 ป.2/2",)),
    ("ป.2", "แผนผัง แผนที่ และลูกโลก"): ("ส 5.1", ("ส 5.1 ป.2/2",)),
    ("ป.3", "ทิศและแผนที่ชุมชน"): ("ส 5.1", ("ส 5.1 ป.3/1",)),
    ("ป.3", "สิ่งแวดล้อมในชุมชน"): ("ส 5.2", ("ส 5.2 ป.3/3", "ส 5.2 ป.3/4")),
    ("ม.1", "พิกัดภูมิศาสตร์และเวลาของโลก"): ("ส 5.1", ("ส 5.1 ม.1/2",)),
    ("ม.2", "มาตราส่วน ทิศ และสัญลักษณ์"): ("ส 5.1", ("ส 5.1 ม.2/2",)),
    ("ม.4", "เครื่องมือทางภูมิศาสตร์"): ("ส 5.1", ("ส 5.1 ม.4-6/3",)),
    ("ป.1", "สภาพอากาศในรอบวัน"): ("ส 5.1", ("ส 5.1 ป.1/4",)),
    ("ป.2", "โลก ดวงอาทิตย์ และดวงจันทร์"): ("ส 5.1", ("ส 5.1 ป.2/3",)),
    ("ป.2", "ฤดูกาลกับการดำเนินชีวิต"): ("ส 5.2", ("ส 5.2 ป.2/3",)),
    ("ป.6", "ลักษณะทางกายภาพของประเทศไทย"): ("ส 5.1", ("ส 5.1 ป.6/1", "ส 5.2 ป.6/1")),
    ("ป.6", "ภัยพิบัติในประเทศไทย"): ("ส 5.1", ("ส 5.1 ป.6/2",)),
    ("ม.1", "ทวีปเอเชีย ออสเตรเลีย และโอเชียเนีย"): ("ส 5.1", ("ส 5.1 ม.1/1", "ส 5.1 ม.1/3")),
    ("ม.2", "ทวีปยุโรปและแอฟริกา"): ("ส 5.1", ("ส 5.1 ม.2/1", "ส 5.1 ม.2/3")),
    ("ม.3", "ทวีปอเมริกาเหนือและอเมริกาใต้"): ("ส 5.1", ("ส 5.1 ม.3/1", "ส 5.1 ม.3/2")),
    ("ม.3", "ความร่วมมือระหว่างประเทศด้านสิ่งแวดล้อม"): ("ส 5.2", ("ส 5.2 ม.3/5",)),
    ("ป.2", "การจัดการขยะ"): ("ส 5.2", ("ส 5.2 ป.2/4",)),
    ("ป.3", "ทรัพยากรกับการดำเนินชีวิต"): ("ส 5.2", ("ส 5.2 ป.3/2", "ส 5.2 ป.3/5")),
    ("ม.1", "ทำเลที่ตั้งของกิจกรรมทางเศรษฐกิจ"): ("ส 5.2", ("ส 5.2 ม.1/1", "ส 5.2 ม.1/2")),
    ("ม.4", "การเปลี่ยนแปลงทางกายภาพ"): ("ส 5.1", ("ส 5.1 ม.4-6/1",)),
    ("ม.4", "ประชากรและการตั้งถิ่นฐาน"): ("ส 5.2", ("ส 5.2 ม.4-6/1",)),
}


def geography_placement_for(*, level: str, topic: str) -> CurriculumPlacement:
    """The unit's filing. Every geography set's (level, topic) must be listed."""
    standard, codes = GEOGRAPHY_UNITS[(level, topic)]
    raw = "|".join((CURRICULUM_VERSION, BASIC, level, standard, topic))
    node = GEOGRAPHY_NODE_PREFIX + sha256(raw.encode("utf-8")).hexdigest()[:16]
    return CurriculumPlacement(
        CURRICULUM_VERSION, BASIC, level, "ส 5", GEOGRAPHY_STRANDS["ส 5"],
        standard, codes, topic, node, "exact", level,
    )
