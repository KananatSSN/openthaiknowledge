"""Versioned Thai mathematics curriculum placement.

The registry's ``level`` and ``topic`` fields predate its curriculum model and
are part of persisted learner history: a topic string keys learner ratings.
This module *enriches* those identities, filing the catalog as
course -> grade -> strand -> standard -> topic. A topic is renamed only with a
matching data migration (see ``MATH_TOPIC_RENAMES``).

Reference: IPST mathematics curriculum (revised B.E. 2560) under the B.E. 2551
Basic Education Core Curriculum.  Indicator arrays containing ``/*`` mean that
the generator covers more than one indicator in that grade/standard; they are
an explicit scope, not a fabricated single-indicator claim.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256

MATH_SUBJECT = "คณิตศาสตร์"
CURRICULUM_VERSION = "หลักสูตรแกนกลาง 2551 (ฉบับปรับปรุง 2560)"

BASIC = "สสวท. พื้นฐาน"
ADDITIONAL = "สสวท. เพิ่มเติม"
ENRICHMENT = "สอวน."
SUPPLEMENTAL = "เสริมทักษะ"
TERTIARY = "อุดมศึกษา"

COURSE_ORDER = (BASIC, ADDITIONAL, ENRICHMENT, SUPPLEMENTAL, TERTIARY)

STRANDS = {
    "ค 1": "จำนวนและพีชคณิต",
    "ค 2": "การวัดและเรขาคณิต",
    "ค 3": "สถิติและความน่าจะเป็น",
    "เสริม": "ทักษะเสริมและการแข่งขัน",
    "อุดม": "คณิตศาสตร์ระดับอุดมศึกษา",
}
STRAND_ORDER = tuple(STRANDS)

SCHOOL_LEVELS = {f"ป.{n}" for n in range(1, 7)} | {f"ม.{n}" for n in range(1, 7)}


@dataclass(frozen=True)
class CurriculumPlacement:
    curriculum_version: str
    course_type: str
    level: str
    strand_code: str
    strand: str
    standard_code: str
    indicator_codes: tuple[str, ...]
    unit: str
    curriculum_node_id: str
    mapping_status: str
    legacy_level: str

    def catalog_fields(self) -> dict:
        row = asdict(self)
        row["indicator_codes"] = list(self.indicator_codes)
        return row


# Topics consolidated into the chapter they belong to in the สสวท. books,
# keyed by (grade, old topic). Several of these were one-set fragments
# (seven ป.5 fraction topics, a dozen exponent-rule topics) that could only
# reach three sets with filler. A topic string is also a learner's rating key,
# so every pair here has a matching row in the
# ``*_consolidate_math_topics.sql`` migration, which carries ratings across.
# ``test_math_topics.py`` holds the two in step.
MATH_TOPIC_RENAMES: dict[tuple[str, str], str] = {
    **{("ป.2", t): "การบวกและการลบ" for t in ("การบวกแนวตั้ง", "การลบแนวตั้ง")},
    **{("ป.2", t): "จำนวนนับไม่เกิน 1,000"
       for t in ("การนับ", "ค่าประจำหลัก", "การเปรียบเทียบจำนวน")},
    ("ป.2", "โจทย์ปัญหาระคน"): "บวก ลบ คูณ หารระคน",
    **{("ป.2", t): "เวลา" for t in ("การอ่านปฏิทิน", "การอ่านเวลา")},
    ("ป.3", "การคูณแนวตั้ง"): "การคูณ",
    **{("ป.3", t): "การหาร" for t in ("การหารมีเศษ", "การหารยาว")},
    **{("ป.3", t): "เศษส่วน" for t in ("เศษส่วนเบื้องต้น", "การบวกลบเศษส่วน")},
    ("ป.4", "การหารยาว"): "การหาร",
    **{("ป.4", t): "เส้นตรงและมุม" for t in ("จุด เส้นตรง รังสี", "มุม")},
    **{("ป.5", t): "เศษส่วน" for t in (
        "การบวกเศษส่วน", "การลบเศษส่วน", "การคูณเศษส่วน", "การหารเศษส่วน",
        "เศษส่วนระคน", "เศษส่วนอย่างต่ำ", "การเปรียบเทียบเศษส่วน")},
    ("ป.5", "การคูณและการหารทศนิยม"): "ทศนิยม",
    ("ป.5", "โจทย์ปัญหาร้อยละ"): "ร้อยละ",
    **{("ป.5", t): "การนำเสนอข้อมูล" for t in ("กราฟเส้น", "ตารางสองทาง")},
    **{("ป.6", t): "ทศนิยม" for t in ("เศษส่วนเป็นทศนิยม", "ทศนิยมเป็นเศษส่วน")},
    **{("ป.6", t): "ร้อยละ" for t in ("เศษส่วนเป็นร้อยละ", "ร้อยละเป็นเศษส่วน", "โจทย์ปัญหาร้อยละ")},
    **{("ป.6", t): "ห.ร.ม. และ ค.ร.น." for t in ("ห.ร.ม.", "ค.ร.น.")},
    ("ป.6", "ส่วนประกอบของวงกลม"): "วงกลม",
    **{("ม.1", t): "จำนวนเต็ม" for t in ("จำนวนเต็มระคน", "บวก-ลบจำนวนเต็ม")},
    **{("ม.1", t): "นิพจน์พีชคณิต" for t in ("แทนค่านิพจน์", "จัดรูปนิพจน์")},
    **{("ม.1", t): "เลขยกกำลัง" for t in (
        "กำลังของ 2", "กฎผลคูณเลขยกกำลัง", "กฎกำลังซ้อน", "เลขชี้กำลังศูนย์",
        "กำลังของจำนวนลบ", "สัญกรณ์วิทยาศาสตร์")},
    **{("ม.2", t): "จำนวนจริง" for t in ("รากที่สองอย่างง่าย", "รากของจำนวนจริง")},
    **{("ม.2", t): "เลขยกกำลัง" for t in (
        "กำลังของผลคูณ", "กำลังของผลหาร", "กฎผลคูณ + กำลังซ้อน", "กฎผลหาร + กำลังซ้อน",
        "เลขชี้กำลังลบ + กฎผลคูณ", "กำลังซ้อน + เลขชี้กำลังลบ", "เลขชี้กำลังลบ",
        "เลขชี้กำลังเศษส่วน")},
    ("ม.3", "สูตรการกระจาย"): "กระจายทวินาม",
    ("ม.4", "รากเชิงซ้อน"): "ดิสคริมิแนนต์",
    ("ม.4", "ทฤษฎีบทเศษเหลือ"): "การหารพหุนาม",
}

# Sets registered with no topic, which left them in a "ทั่วไป" bucket of one.
# An empty topic is never rated, so these need no data migration.
# Topic names the consolidation retired at every level. Consumers key learner
# data by topic name and migrated these away, so no set may be filed under one
# again (otk/tests/test_math_topics.py).
RETIRED_TOPIC_NAMES = frozenset({
    'กฎกำลังซ้อน',
    'กฎผลคูณ + กำลังซ้อน',
    'กฎผลคูณเลขยกกำลัง',
    'กฎผลหาร + กำลังซ้อน',
    'กราฟเส้น',
    'การคูณเศษส่วน',
    'การคูณแนวตั้ง',
    'การคูณและการหารทศนิยม',
    'การบวกลบเศษส่วน',
    'การบวกเศษส่วน',
    'การบวกแนวตั้ง',
    'การลบเศษส่วน',
    'การลบแนวตั้ง',
    'การหารมีเศษ',
    'การหารยาว',
    'การหารเศษส่วน',
    'การอ่านปฏิทิน',
    'การอ่านเวลา',
    'การเปรียบเทียบจำนวน',
    'การเปรียบเทียบเศษส่วน',
    'กำลังของ 2',
    'กำลังของจำนวนลบ',
    'กำลังของผลคูณ',
    'กำลังของผลหาร',
    'กำลังซ้อน + เลขชี้กำลังลบ',
    'ค.ร.น.',
    'จัดรูปนิพจน์',
    'จำนวนเต็มระคน',
    'จุด เส้นตรง รังสี',
    'ตารางสองทาง',
    'ทฤษฎีบทเศษเหลือ',
    'ทศนิยมเป็นเศษส่วน',
    'บวก-ลบจำนวนเต็ม',
    'มุม',
    'รากของจำนวนจริง',
    'รากที่สองอย่างง่าย',
    'รากเชิงซ้อน',
    'ร้อยละเป็นเศษส่วน',
    'สัญกรณ์วิทยาศาสตร์',
    'สูตรการกระจาย',
    'ส่วนประกอบของวงกลม',
    'ห.ร.ม.',
    'เลขชี้กำลังลบ',
    'เลขชี้กำลังลบ + กฎผลคูณ',
    'เลขชี้กำลังศูนย์',
    'เลขชี้กำลังเศษส่วน',
    'เศษส่วนระคน',
    'เศษส่วนอย่างต่ำ',
    'เศษส่วนเบื้องต้น',
    'เศษส่วนเป็นทศนิยม',
    'เศษส่วนเป็นร้อยละ',
    'แทนค่านิพจน์',
    'โจทย์ปัญหาร้อยละ',
})


MATH_TOPIC_ASSIGNMENTS: dict[str, str] = {
    "math.times_table": "การคูณ",
    "math.integer_muldiv": "จำนวนเต็ม",
    "math.simplify_polynomial": "เอกนามและพหุนาม",
    "math.logarithm": "ลอการิทึม",
    "math.arithmetic_sequence": "ลำดับเลขคณิต",
    "math.permutations": "การเรียงสับเปลี่ยน",
    "math.vectors": "เวกเตอร์",
}


# Placements corrected to the sequence in the IPST secondary curriculum books.
# The old level is retained in ``legacy_level`` for audits and saved links.
_LEVEL_OVERRIDES = {
    "การแปลงทางเรขาคณิต": "ม.2",
    "ระบบสมการ": "ม.3",
    "อสมการเชิงเส้น": "ม.3",
    "ระยะทาง": "ม.4",
    "สมการเส้นตรง": "ม.4",
    "สมการวงกลม": "ม.4",
    "ลอการิทึม": "ม.4",
    "อนุพันธ์": "ม.6",
    "เส้นสัมผัส": "ม.6",
    "ค่าสูงสุด-ต่ำสุดสัมพัทธ์": "ม.6",
    "อินทิกรัลจำกัดเขต": "ม.6",
    "พื้นที่": "ม.6",
    "การจัดหมู่": "ม.5",
    "ความน่าจะเป็น": "ม.5",
    "ค่าคาดหมาย": "ม.5",
    "เวกเตอร์": "ม.5",
    "การเรียงสับเปลี่ยน": "ม.5",
    # The 2560 book reads box plots at ม.3 (ค 3.1 ม.3/1).
    "สถิติ (แผนภาพกล่อง)": "ม.3",
}
_KEY_LEVEL_OVERRIDES = {
    "math.permutations": "ม.5",
    "math.vectors": "ม.5",
    # Mean, median and mode are ม.2 (ค 3.1 ม.2/1), with the other ม.2 data.
    "math.central_tendency": "ม.2",
    "math.median_from_data": "ม.2",
    # Two-way tables are ป.4 (ค 3.1 ป.4/1), a year before line graphs.
    "math.two_way_table_read_p5": "ป.4",
    "math.two_way_table_total_p5": "ป.4",
    "math.two_way_table_compare_p5": "ป.4",
}

# Core upper-secondary content: topics the 2560 core indicators teach at the
# grade these sets are filed at. Other ม.4-ม.6 topics are published under the
# IPST additional-mathematics track. Counting and probability are core at ม.4
# but additional at ม.5, where these sets sit; functions, composite functions,
# exponential equations and radicals are additional at ม.4 (core has functions
# and radicals at ม.5 only). A set keeps its grade: it is the learner-facing
# identity, so the course follows the grade rather than the other way round.
_UPPER_BASIC_TOPICS = {
    "เซต", "ตรรกศาสตร์",
    "สถิติประยุกต์", "การวัดตำแหน่งข้อมูล", "การวัดการกระจาย",
    "ค่ามาตรฐาน", "การวิเคราะห์การถดถอย", "ลำดับและอนุกรม", "ค่ากลางของข้อมูล",
    "การนำเสนอข้อมูลเชิงปริมาณ",
    # Core indicators no set taught before the 2026-09 audit.
    "หลักการนับเบื้องต้น", "ความน่าจะเป็นของเหตุการณ์",
    "จำนวนจริงในรูปกรณฑ์และเลขยกกำลัง", "ฟังก์ชันในชีวิตจริง", "ดอกเบี้ยและมูลค่าของเงิน",
}

_STATISTICS_TERMS = (
    "สถิติ", "แผนภูมิ", "ตารางทางเดียว", "ตารางสองทาง", "กราฟเส้น", "ตำแหน่งข้อมูล",
    "การกระจาย", "ค่ามาตรฐาน", "ถดถอย", "ค่ากลาง", "นำเสนอข้อมูล",
)
_PROBABILITY_TERMS = (
    "ความน่าจะเป็น", "หลักการนับ", "การเรียงสับเปลี่ยน", "การจัดหมู่",
    "ค่าคาดหมาย",
)
_MEASUREMENT_TERMS = (
    "การวัด", "เวลา", "อ่านปฏิทิน", "เงิน", "ปริมาตร", "ความจุ",
    "พื้นที่รูป", "พื้นที่ผิว", "โจทย์ปัญหาปริมาตร",
)
_GEOMETRY_TERMS = (
    "เรขาคณิต", "รูปสมมาตร", "รูปสี่เหลี่ยม", "รูปสามเหลี่ยม", "มุม",
    "จุด เส้นตรง", "เส้นขนาน", "วงกลม", "พีทาโกรัส", "ความคล้าย",
    "เท่ากันทุกประการ", "ตรีโกณมิติ", "ระยะทาง", "สมการเส้นตรง",
    "สมการวงกลม", "เวกเตอร์", "ภาคตัดกรวย", "กฎของไซน์", "กฎของโคไซน์",
)
_RELATION_TERMS = (
    "แบบรูป", "ฟังก์ชัน", "กราฟความสัมพันธ์", "พหุนาม", "แยกตัวประกอบ",
    "กระจายทวินาม", "ลำดับ", "อนุกรม", "ลิมิต",
    "อนุพันธ์", "อินทิกรัล", "อินทิเกรต", "พื้นที่ระหว่างเส้นโค้ง",
)
_EQUATION_TERMS = (
    "สมการ", "อสมการ", "ระบบสมการ", "ค่าสัมบูรณ์",
)


def _contains(topic: str, terms: tuple[str, ...]) -> bool:
    return any(term in topic for term in terms)


# Topics whose words mislead the keyword rules below, checked against the
# 2560 indicator book: order of operations is not a ลำดับ (sequence); prime
# factorisation is number work (ค 1.1), not polynomial factorising; graphs,
# linear relations and linear functions are ค 1.3 (ม.1/2-3), not ค 1.2;
# completing the square serves the quadratic function (ค 1.2 ม.3/2).
_STANDARD_BY_TOPIC = {
    "ลำดับการดำเนินการ": ("ค 1", "ค 1.1"),
    "แยกตัวประกอบเฉพาะ": ("ค 1", "ค 1.1"),
    "กราฟความสัมพันธ์เชิงเส้น": ("ค 1", "ค 1.3"),
    "ฟังก์ชันเชิงเส้น": ("ค 1", "ค 1.3"),
    "กำลังสองสมบูรณ์": ("ค 1", "ค 1.2"),
    "ความยาวและน้ำหนัก": ("ค 2", "ค 2.1"),
    "ปริซึม": ("ค 2", "ค 2.2"),
    # Interest is ค 1.3 ม.5/1, not money as measurement (ค 2.1).
    "ดอกเบี้ยและมูลค่าของเงิน": ("ค 1", "ค 1.3"),
}

# Core topics taught at a grade where the 2560 book lists no indicator for
# them. ป.2 แบบรูป is printed as "(มีการจัดการเรียนการสอนเพื่อเป็นพื้นฐาน
# แต่ไม่วัดผล)"; the others have no indicator at their grade at all. They are
# filed under their standard without claiming an indicator.
# The same topic name can mean different standards at different grades: ป.6
# วงกลม is circumference and area (ค 2.1 ป.6/3), ม.3 วงกลม is circle theorems
# (ค 2.2 ม.3/3).
_STANDARD_BY_LEVEL_TOPIC = {
    ("ป.6", "วงกลม"): ("ค 2", "ค 2.1"),
}

# Sets whose own indicator is exact while their topic's scope is not. The set
# keeps its topic's standard and curriculum node, so it stays in the topic's
# practice pool; only the indicator it cites is narrower. Constructing an angle
# with a protractor is measurement (ค 2.1 ป.4/2), taught in the ป.4 angles
# topic, which is geometry (ค 2.2).
_KEY_INDICATORS = {
    "math.construct_angle_protractor_p4": ("ค 2.1 ป.4/2",),
}

# The additional (เพิ่มเติม) course's indicators, by the topic a set is filed
# under. One topic may serve two indicators (logarithms: graphs and equations).
_AN = "ค เพิ่มเติม จำนวนและพีชคณิต"
_AG = "ค เพิ่มเติม การวัดและเรขาคณิต"
_AS = "ค เพิ่มเติม สถิติและความน่าจะเป็น"
_AC = "ค เพิ่มเติม แคลคูลัส"
_ADDITIONAL_INDICATORS: dict[tuple[str, str], tuple[str, ...]] = {
    ("ม.4", "จัดรูปกรณฑ์"): (f"{_AN} 1 ม.4/3",),
    ("ม.4", "ค่าสัมบูรณ์"): (f"{_AN} 1 ม.4/3", f"{_AN} 3 ม.4/3"),
    ("ม.4", "ฟังก์ชัน"): (f"{_AN} 2 ม.4/2",),
    ("ม.4", "ความสัมพันธ์และฟังก์ชัน"): (f"{_AN} 2 ม.4/2",),
    ("ม.4", "เรนจ์ของฟังก์ชันกำลังสอง"): (f"{_AN} 2 ม.4/2",),
    ("ม.4", "ฟังก์ชันประกอบ"): (f"{_AN} 2 ม.4/1",),
    ("ม.4", "ลอการิทึม"): (f"{_AN} 2 ม.4/3", f"{_AN} 3 ม.4/4"),
    ("ม.4", "สมการเลขชี้กำลัง"): (f"{_AN} 3 ม.4/4",),
    ("ม.4", "แยกตัวประกอบ"): (f"{_AN} 3 ม.4/1",),
    ("ม.4", "การหารพหุนาม"): (f"{_AN} 3 ม.4/1",),
    ("ม.4", "ความสัมพันธ์ราก-สัมประสิทธิ์"): (f"{_AN} 3 ม.4/1",),
    ("ม.4", "ดิสคริมิแนนต์"): (f"{_AN} 3 ม.4/1",),
    ("ม.4", "อสมการกำลังสอง"): (f"{_AN} 3 ม.4/1",),
    ("ม.4", "สมการและอสมการเศษส่วน"): (f"{_AN} 3 ม.4/2",),
    ("ม.4", "เรขาคณิตวิเคราะห์"): (f"{_AG} 1 ม.4/1",),
    ("ม.4", "ระยะทาง"): (f"{_AG} 1 ม.4/1",),
    ("ม.4", "สมการเส้นตรง"): (f"{_AG} 1 ม.4/1",),
    ("ม.4", "สมการวงกลม"): (f"{_AG} 1 ม.4/1",),
    ("ม.4", "หาสมการพาราโบลา"): (f"{_AG} 1 ม.4/1",),
    ("ม.4", "ภาคตัดกรวย"): (f"{_AG} 1 ม.4/1",),
    ("ม.5", "จำนวนเชิงซ้อน"): (f"{_AN} 1 ม.5/1",),
    ("ม.5", "อัตราส่วนตรีโกณมิติ"): (f"{_AN} 2 ม.5/1",),
    ("ม.5", "ฟังก์ชันตรีโกณมิติ"): (f"{_AN} 2 ม.5/1",),
    ("ม.5", "ตัวผกผันของฟังก์ชันตรีโกณมิติ"): (f"{_AN} 2 ม.5/1",),
    ("ม.5", "สมการตรีโกณมิติ"): (f"{_AN} 3 ม.5/1",),
    ("ม.5", "กฎของโคไซน์"): (f"{_AN} 3 ม.5/2",),
    ("ม.5", "กฎของไซน์"): (f"{_AN} 3 ม.5/2",),
    ("ม.5", "เมทริกซ์"): (f"{_AN} 3 ม.5/3",),
    ("ม.5", "เวกเตอร์"): (f"{_AG} 2 ม.5/1",),
    ("ม.5", "หลักการนับ"): (f"{_AS} 1 ม.5/1",),
    ("ม.5", "การเรียงสับเปลี่ยน"): (f"{_AS} 1 ม.5/1",),
    ("ม.5", "การจัดหมู่"): (f"{_AS} 1 ม.5/1",),
    ("ม.5", "ทฤษฎีบททวินาม"): (f"{_AS} 1 ม.5/1",),
    ("ม.5", "ความน่าจะเป็น"): (f"{_AS} 1 ม.5/2",),
    ("ม.5", "ค่าคาดหมาย"): (f"{_AS} 1 ม.5/2",),
    ("ม.6", "การแจกแจงความน่าจะเป็น"): (f"{_AS} 1 ม.6/1",),
    ("ม.6", "ลำดับเลขคณิต"): (f"{_AN} 2 ม.6/2", f"{_AN} 2 ม.6/4"),
    ("ม.6", "ลำดับเรขาคณิต"): (f"{_AN} 2 ม.6/2", f"{_AN} 2 ม.6/4"),
    ("ม.6", "อนุกรม"): (f"{_AN} 2 ม.6/3",),
    ("ม.6", "ลิมิต"): (f"{_AC} 1 ม.6/1",),
    ("ม.6", "อนุพันธ์"): (f"{_AC} 1 ม.6/2",),
    ("ม.6", "เส้นสัมผัส"): (f"{_AC} 1 ม.6/2",),
    ("ม.6", "ค่าสูงสุด-ต่ำสุดสัมพัทธ์"): (f"{_AC} 1 ม.6/2",),
    ("ม.6", "อินทิกรัลจำกัดเขต"): (f"{_AC} 1 ม.6/3",),
    ("ม.6", "อินทิเกรตโดยการแทนค่า"): (f"{_AC} 1 ม.6/3",),
    ("ม.6", "อินทิเกรตทีละส่วน"): (f"{_AC} 1 ม.6/3",),
    ("ม.6", "พื้นที่"): (f"{_AC} 1 ม.6/3",),
    ("ม.6", "พื้นที่ระหว่างเส้นโค้ง"): (f"{_AC} 1 ม.6/3",),
}

# Sets narrower or wider than their topic's indicators.
_ADDITIONAL_KEY_INDICATORS: dict[str, tuple[str, ...]] = {
    "math.complex_nth_roots_m5": (f"{_AN} 1 ม.5/2",),
    "math.complex_polar_m5": (f"{_AN} 1 ม.5/1", f"{_AN} 1 ม.5/2"),
    "math.complex_conjugate_root_m5": (f"{_AN} 1 ม.5/1", f"{_AN} 3 ม.5/6"),
    "math.complex_polynomial_solve_m5": (f"{_AN} 1 ม.5/1", f"{_AN} 3 ม.5/6"),
    "math.matrix_inverse_m5": (f"{_AN} 3 ม.5/4",),
    "math.matrix_equation_m5": (f"{_AN} 3 ม.5/4",),
    "math.cramer_rule_m5": (f"{_AN} 3 ม.5/5",),
    "math.matrix_unique_solution_m5": (f"{_AN} 3 ม.5/5",),
    "math.matrix_system_word_m5": (f"{_AN} 3 ม.5/5",),
    "math.matrix_row_operations_m5": (f"{_AN} 3 ม.5/5",),
    "math.vector_points_m5": (f"{_AG} 2 ม.5/1", f"{_AG} 2 ม.5/2"),
    "math.vector_triple_product_m5": (f"{_AG} 2 ม.5/1", f"{_AG} 2 ม.5/2"),
    "math.vector_resultant_word_m5": (f"{_AG} 2 ม.5/2",),
    "math.series_converges": (f"{_AN} 2 ม.6/1", f"{_AN} 2 ม.6/3"),
    "math.sequence_limit_m6": (f"{_AN} 2 ม.6/1",),
    "math.piecewise_limit_m6": (f"{_AC} 1 ม.6/1",),
}

# Basic-course topics whose content the additional course also names: the sets
# keep their basic indicator and cite the additional one too.
_ALSO_ADDITIONAL: dict[tuple[str, str], tuple[str, ...]] = {
    ("ม.4", "เซต"): (f"{_AN} 1 ม.4/1",),
    ("ม.4", "ตรรกศาสตร์"): (f"{_AN} 1 ม.4/2",),
}

_NO_INDICATOR = {
    ("ป.2", "แบบรูป"),
    ("ม.1", "แยกตัวประกอบเฉพาะ"),
    ("ม.2", "ฟังก์ชันเชิงเส้น"),
    ("ม.2", "แก้สมการหลายตัวแปร"),
}


def _strand_and_standard(key: str, topic: str) -> tuple[str, str]:
    if topic in _STANDARD_BY_TOPIC:
        return _STANDARD_BY_TOPIC[topic]
    if "permutation" in key or "combination" in key or "probability" in key:
        return "ค 3", "ค 3.2"
    if "vector" in key:
        return "ค 2", "ค 2.2"
    # Before the geometry terms: ลำดับเรขาคณิต is a sequence, not geometry.
    if _contains(topic, ("ลำดับ", "อนุกรม")):
        return "ค 1", "ค 1.2"
    if _contains(topic, _STATISTICS_TERMS):
        return "ค 3", "ค 3.1"
    if _contains(topic, _PROBABILITY_TERMS):
        return "ค 3", "ค 3.2"
    if _contains(topic, _MEASUREMENT_TERMS):
        return "ค 2", "ค 2.1"
    if _contains(topic, _GEOMETRY_TERMS):
        return "ค 2", "ค 2.2"
    if _contains(topic, _EQUATION_TERMS):
        return "ค 1", "ค 1.3"
    if _contains(topic, _RELATION_TERMS) or (not topic and "sequence" in key):
        return "ค 1", "ค 1.2"
    return "ค 1", "ค 1.1"


def _indicator_scope(key: str, level: str, standard: str, topic: str) -> tuple[str, ...]:
    """Return exact indicators where the current topic is unambiguous.

    Broad legacy topics such as ``การวัด`` legitimately combine several
    indicators, and are represented by the standard's grade wildcard.
    """
    exact: dict[tuple[str, str], tuple[int, ...]] = {
        ("ป.1", "การนับ"): (1,),
        ("ป.1", "การเปรียบเทียบ"): (2, 3),
        ("ป.1", "การบวก"): (4,),
        ("ป.1", "การลบ"): (4,),
        ("ป.1", "โจทย์ปัญหา"): (5,),
        ("ป.1", "การบวกลบระคน"): (4, 5),
        ("ป.1", "แบบรูป"): (1,),
        ("ป.1", "แผนภูมิรูปภาพ"): (1,),
        ("ป.2", "การคูณ"): (5,),
        ("ป.2", "แผนภูมิรูปภาพ"): (1,),
        ("ป.3", "แบบรูป"): (1,),
        ("ป.6", "แบบรูป"): (1,),
        ("ป.3", "ค่าประจำหลัก"): (1, 2),
        ("ป.3", "การคูณ"): (6,),
        ("ป.3", "การหาร"): (7,),
        ("ป.4", "การประมาณค่า"): (7,),
        ("ป.4", "การคูณยาว"): (9,),
        ("ป.4", "การหาร"): (9,),
        ("ป.4", "แผนภูมิแท่ง"): (1,),
        ("ป.5", "เส้นขนาน"): (1,),
        ("ป.6", "แผนภูมิรูปวงกลม"): (1,),
        ("ม.1", "อัตราส่วนและสัดส่วน"): (3,),
        ("ม.1", "กราฟความสัมพันธ์เชิงเส้น"): (2, 3),
        ("ม.1", "สถิติ"): (1,),
        ("ม.2", "เอกนามและพหุนาม"): (1,),
        ("ม.2", "ทฤษฎีบทพีทาโกรัส"): (5,),
        ("ม.3", "สถิติ (แผนภาพกล่อง)"): (1,),
        ("ป.6", "วงกลม"): (3,),
        ("ม.3", "กราฟของฟังก์ชันกำลังสอง"): (2,),
        ("ม.3", "อสมการเชิงเส้น"): (1,),
        ("ม.3", "สมการกำลังสอง"): (2,),
        ("ม.3", "ระบบสมการ"): (3,),
        ("ม.3", "ความคล้าย"): (1,),
        ("ม.3", "อัตราส่วนตรีโกณมิติ"): (2,),
        ("ม.3", "วงกลม"): (3,),
        ("ม.3", "ความน่าจะเป็น"): (1,),
        ("ม.3", "ความน่าจะเป็นเบื้องต้น"): (1,),
        ("ม.4", "เซต"): (1,),
        ("ม.4", "ตรรกศาสตร์"): (1,),
        ("ม.6", "สถิติประยุกต์"): (1,),
        ("ม.6", "การวัดตำแหน่งข้อมูล"): (1,),
        ("ม.6", "การวัดการกระจาย"): (1,),
        ("ม.6", "ค่ามาตรฐาน"): (1,),
        ("ม.6", "การวิเคราะห์การถดถอย"): (1,),
        ("ม.6", "การนำเสนอข้อมูลเชิงปริมาณ"): (1,),
        ("ป.2", "การบวกและการลบ"): (4,),
        ("ป.3", "การบวกและการลบ"): (5,),
        ("ป.4", "การบวกและการลบ"): (8,),
        ("ป.5", "ความยาวและน้ำหนัก"): (1, 2),
        ("ป.5", "ปริซึม"): (4,),
        ("ป.6", "เศษส่วนและจำนวนคละ"): (1, 7, 8),
        ("ป.4", "การนำเสนอข้อมูล"): (1,),
        ("ป.5", "การนำเสนอข้อมูล"): (1, 2),
        ("ป.2", "จำนวนนับไม่เกิน 1,000"): (1, 2, 3),
        ("ม.2", "การแยกตัวประกอบของพหุนามดีกรีสอง"): (2,),
        ("ม.4", "หลักการนับเบื้องต้น"): (1,),
        ("ม.4", "ความน่าจะเป็นของเหตุการณ์"): (2,),
        ("ม.5", "จำนวนจริงในรูปกรณฑ์และเลขยกกำลัง"): (1,),
        ("ม.5", "ฟังก์ชันในชีวิตจริง"): (1,),
        ("ม.5", "ดอกเบี้ยและมูลค่าของเงิน"): (1,),
    }
    numbers = exact.get((level, topic))
    if numbers:
        return tuple(f"{standard} {level}/{number}" for number in numbers)
    return (f"{standard} {level}/*",)


def _stable_node_id(course: str, level: str, standard: str, topic: str) -> str:
    raw = "|".join((CURRICULUM_VERSION, course, level, standard, topic))
    return f"th-math-2560-{sha256(raw.encode('utf-8')).hexdigest()[:16]}"


def placement_for(*, key: str, subject: str, level: str, topic: str) -> CurriculumPlacement:
    """Return the canonical filing metadata for one registered problem set."""
    legacy_level = level
    unit = topic or "ทั่วไป"

    if subject != MATH_SUBJECT:
        return CurriculumPlacement("", "ทั่วไป", level, "", "", "", (), unit, "", "not_applicable", level)

    if level == "โอลิมปิก (สอวน.)":
        course, strand_code, standard, status = ENRICHMENT, "เสริม", "สอวน.", "enrichment"
        effective_level = level
    elif level == "เทคนิคคิดเลขเร็ว":
        course, strand_code, standard, status = SUPPLEMENTAL, "เสริม", "เสริม", "supplemental"
        effective_level = level
    elif level.startswith("แคลคูลัส"):
        course, strand_code, standard, status = TERTIARY, "อุดม", "อุดมศึกษา", "outside_scope"
        effective_level = level
    else:
        effective_level = _KEY_LEVEL_OVERRIDES.get(key, _LEVEL_OVERRIDES.get(topic, level))
        strand_code, standard = _STANDARD_BY_LEVEL_TOPIC.get(
            (effective_level, topic), None) or _strand_and_standard(key, topic)
        if effective_level in {"ม.4", "ม.5", "ม.6"} and topic not in _UPPER_BASIC_TOPICS:
            course, status = ADDITIONAL, "additional_outcome"
        elif (effective_level, topic) in _NO_INDICATOR:
            course, status = BASIC, "no_indicator"
        else:
            course, status = BASIC, "exact" if (effective_level, topic) in {
                (level_, topic_) for level_, topic_ in _EXACT_INDICATOR_KEYS
            } else "standard_scope"

    strand = STRANDS[strand_code]
    indicators = (
        _indicator_scope(key, effective_level, standard, topic)
        if course == BASIC and standard and status != "no_indicator" else ()
    )
    if course == BASIC and key in _KEY_INDICATORS:
        indicators, status = _KEY_INDICATORS[key], "exact"
    if course == ADDITIONAL:
        indicators = _ADDITIONAL_KEY_INDICATORS.get(
            key, _ADDITIONAL_INDICATORS.get((effective_level, topic), ()))
    elif course == BASIC:
        indicators = indicators + _ALSO_ADDITIONAL.get((effective_level, topic), ())
    node_id = _stable_node_id(course, effective_level, standard, unit)
    return CurriculumPlacement(
        CURRICULUM_VERSION if course in {BASIC, ADDITIONAL} else "",
        course,
        effective_level,
        strand_code,
        strand,
        standard,
        indicators,
        unit,
        node_id,
        status,
        legacy_level,
    )


# Kept independently of the helper's local dict so mapping status is cheap and
# testable without parsing a wildcard string.
_EXACT_INDICATOR_KEYS = {
    ("ป.1", "การนับ"), ("ป.1", "การเปรียบเทียบ"), ("ป.1", "การบวก"),
    ("ป.1", "การลบ"), ("ป.1", "โจทย์ปัญหา"), ("ป.1", "การบวกลบระคน"),
    ("ป.1", "แบบรูป"), ("ป.1", "แผนภูมิรูปภาพ"), ("ป.2", "การคูณ"),
    ("ป.2", "แผนภูมิรูปภาพ"), ("ป.3", "แบบรูป"),
    ("ป.6", "แบบรูป"), ("ป.3", "ค่าประจำหลัก"), ("ป.3", "การคูณ"), ("ป.3", "การหาร"),
    ("ป.4", "การประมาณค่า"), ("ป.4", "การคูณยาว"), ("ป.4", "การหาร"),
    ("ป.4", "แผนภูมิแท่ง"), ("ป.5", "เส้นขนาน"), ("ป.6", "แผนภูมิรูปวงกลม"),
    ("ม.1", "อัตราส่วนและสัดส่วน"), ("ม.1", "กราฟความสัมพันธ์เชิงเส้น"),
    ("ม.1", "สถิติ"), ("ม.2", "เอกนามและพหุนาม"), ("ม.2", "ทฤษฎีบทพีทาโกรัส"),
    ("ม.3", "สถิติ (แผนภาพกล่อง)"), ("ป.6", "วงกลม"),
    ("ม.3", "กราฟของฟังก์ชันกำลังสอง"), ("ม.3", "อสมการเชิงเส้น"),
    ("ม.3", "สมการกำลังสอง"), ("ม.3", "ระบบสมการ"), ("ม.3", "ความคล้าย"),
    ("ม.3", "อัตราส่วนตรีโกณมิติ"), ("ม.3", "วงกลม"),
    ("ม.3", "ความน่าจะเป็น"), ("ม.3", "ความน่าจะเป็นเบื้องต้น"), ("ม.4", "เซต"),
    ("ม.4", "ตรรกศาสตร์"), ("ม.6", "สถิติประยุกต์"),
    ("ม.6", "การวัดตำแหน่งข้อมูล"), ("ม.6", "การวัดการกระจาย"),
    ("ม.6", "ค่ามาตรฐาน"), ("ม.6", "การวิเคราะห์การถดถอย"),
    ("ป.2", "การบวกและการลบ"), ("ป.2", "จำนวนนับไม่เกิน 1,000"),
    ("ป.3", "การบวกและการลบ"), ("ป.4", "การบวกและการลบ"), ("ป.5", "ความยาวและน้ำหนัก"),
    ("ป.5", "ปริซึม"), ("ป.6", "เศษส่วนและจำนวนคละ"), ("ป.4", "การนำเสนอข้อมูล"),
    ("ป.5", "การนำเสนอข้อมูล"),
    ("ม.6", "การนำเสนอข้อมูลเชิงปริมาณ"),
    ("ม.2", "การแยกตัวประกอบของพหุนามดีกรีสอง"), ("ม.4", "หลักการนับเบื้องต้น"),
    ("ม.4", "ความน่าจะเป็นของเหตุการณ์"), ("ม.5", "จำนวนจริงในรูปกรณฑ์และเลขยกกำลัง"),
    ("ม.5", "ฟังก์ชันในชีวิตจริง"), ("ม.5", "ดอกเบี้ยและมูลค่าของเงิน"),
}


def curriculum_sort_fields(course: str, strand_code: str) -> tuple[int, int]:
    course_rank = COURSE_ORDER.index(course) if course in COURSE_ORDER else len(COURSE_ORDER)
    strand_rank = STRAND_ORDER.index(strand_code) if strand_code in STRAND_ORDER else len(STRAND_ORDER)
    return course_rank, strand_rank

