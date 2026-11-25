"""Knowledge claims for the maths entrance papers, wave 2a (re-runnable, idempotent).

Samsen Pre-Test 2567 (two days) and 2568, Roi-et Pre-Gifted 2568 and NUD Prep
Test 2019: primary-level papers for ม.1 entrance. Every question is claimed by
its exam tag. A unit's ``covered_by`` names only sets that practise that skill;
a skill no set practises yet keeps an empty list (``sheetpipe plan``).

The two Samsen 2567 papers share one template item for item (2 ธ.ค. 66's items
12 and 13 are 3 ธ.ค. 66's 13 and 12), so one unit claims the item in both.
"""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
write_topic = runpy.run_path(str(Path(__file__).with_name('sheet_digestion_primary1.py')))['write_topic']

SAMSEN_A = 'สามเสน Pre-Test 2567 (2 ธ.ค. 66)/'
SAMSEN_B = 'สามเสน Pre-Test 2567 (3 ธ.ค. 66)/'
SAMSEN_C = 'สามเสน Pre-Test 2568/'
ROIET = 'ร้อยเอ็ดวิทยาลัย Pre-Gifted 2568/'
NUD = 'สาธิต มน. NUD Prep Test 2019/'

GCD = ('entrance-primary-gcd-lcm', 'ห.ร.ม. และ ค.ร.น.', 'ป.6')
OPS = ('entrance-primary-operations', 'ลำดับการดำเนินการ', 'ป.6')
FRAC = ('entrance-primary-fractions', 'เศษส่วนและจำนวนคละ', 'ป.6')
PCT = ('entrance-primary-percent', 'ร้อยละ', 'ป.6')
PAT = ('entrance-primary-patterns', 'แบบรูป', 'ป.6')
PIE = ('entrance-primary-pie-charts', 'แผนภูมิรูปวงกลม', 'ป.6')
BAR = ('entrance-primary-bar-charts', 'แผนภูมิแท่ง', 'ป.4')
VOL = ('entrance-primary-volume', 'ปริมาตรและพื้นที่ผิว', 'ป.6')
AREA = ('entrance-primary-area', 'พื้นที่รูปสามเหลี่ยม', 'ป.6')
CIRCLE = ('entrance-primary-circles', 'วงกลม', 'ป.6')
PARALLEL = ('entrance-primary-parallel', 'เส้นขนาน', 'ป.5')
RATE = ('entrance-primary-rates', 'บัญญัติไตรยางศ์', 'ป.5')
RATIO = ('entrance-primary-ratio', 'อัตราส่วนและมาตราส่วน', 'ป.6')
TIME = ('entrance-primary-time', 'เวลา', 'ป.4')
EQ = ('entrance-primary-equations', 'สมการเชิงเส้น', 'ม.1')
STAT = ('entrance-primary-statistics', 'สถิติ', 'ม.1')
SHAPES = ('entrance-primary-shapes', 'มิติสัมพันธ์ของรูปเรขาคณิต', 'ม.1')
EXP = ('entrance-primary-exponents', 'เลขยกกำลัง', 'ม.1')
DEC = ('entrance-primary-decimals', 'ทศนิยมและเศษส่วน', 'ม.1')
PROB = ('entrance-primary-probability', 'ความน่าจะเป็นเบื้องต้น', 'ม.3')

FILES = {}
UNITS = {}


def u(file, slug, statement, tags, covered=(), note=''):
    unit = dict(id='math.entrance.' + slug, kind='procedure', title=statement[:60], statement=statement,
                steps=['ระบุสิ่งที่โจทย์กำหนดและสิ่งที่ต้องหา', statement, 'ตรวจคำตอบกับเงื่อนไขของโจทย์'],
                sources=[{'tag': t} for t in tags], covered_by=list(covered))
    if note:
        unit['note'] = note
    FILES.setdefault(file, []).append(unit)
    UNITS[slug] = unit


def claim(slug, tags, covered=()):
    unit = UNITS[slug]
    unit['sources'] += [{'tag': t} for t in tags if {'tag': t} not in unit['sources']]
    unit['covered_by'] += [k for k in covered if k not in unit['covered_by']]


def k(*names):
    return ['math.' + n for n in names]


def samsen_2567():
    """Items of the 2 ธ.ค. 66 paper; the 3 ธ.ค. 66 paper's same-numbered item is claimed too."""
    def t(n):
        other = {12: 13, 13: 12}.get(n, n)
        return [SAMSEN_A + str(n), SAMSEN_B + str(other)]
    u(GCD, 'count-multiples-either', 'นับพหุคูณของ a หรือ b ในช่วง ด้วยจำนวนพหุคูณของแต่ละตัวลบพหุคูณของ ค.ร.น.', t(1))
    u(GCD, 'gcd-spacing', 'ระยะห่างเท่ากันมากที่สุดคือ ห.ร.ม. ของความยาว แล้วนับจำนวนจุดตามแนวกว้างและยาว', t(2),
      k('gcd_word_problem_p6'), note='2 ธ.ค. 66 ข้อ 2 ไม่บอกว่าปลูกที่ขอบด้วยหรือไม่ ทรานสคริปต์ปลูกที่ขอบ')
    u(RATIO, 'group-ratio-equation', 'ใช้จำนวนกลุ่มและอัตราส่วนสมาชิกในกลุ่มตั้งสมการหาจำนวนแต่ละชนิด', t(3))
    u(GCD, 'gcd-lcm-statements', 'หา ห.ร.ม. และ ค.ร.น. ด้วยการแยกตัวประกอบเฉพาะ แล้วตรวจข้อความแต่ละข้อ', t(4),
      k('gcd', 'lcm', 'gcd_lcm_three_p6'))
    u(FRAC, 'mixed-number-quantities', 'บวกลบจำนวนคละของปริมาณแล้วคูณหรือหารตามจำนวนชิ้น', t(5),
      k('fraction_multistep_word_p6', 'mixed_number_ops_p6'))
    u(FRAC, 'fraction-order-of-operations', 'คำนวณนิพจน์เศษส่วนและจำนวนคละตามลำดับการดำเนินการและวงเล็บ', t(6),
      k('mixed_number_ops_p6', 'order_of_ops'))
    u(DEC, 'squares-from-rectangle', 'จำนวนรูปจัตุรัสที่ตัดได้ = (ส่วนจำนวนเต็มของกว้าง ÷ ด้าน) × (ส่วนจำนวนเต็มของยาว ÷ ด้าน)', t(7))
    u(FRAC, 'compare-fraction-expressions', 'คำนวณหรือทำตัวส่วนให้เท่ากันแล้วเปรียบเทียบและเรียงลำดับเศษส่วน', t(8),
      k('order_mixed_numbers_p6', 'largest_fraction_p6'))
    u(PAT, 'pattern-double-plus', 'หาความสัมพันธ์ของพจน์ติดกัน (คูณแล้วบวก) แล้วต่อแบบรูปหาพจน์ที่หายไป', t(9),
      k('pattern_multiply_p6', 'pattern_missing_middle_p6'))
    u(PAT, 'fraction-array-pattern', 'ขั้นที่ n มีเศษส่วน k/(n + 1 − k) หาผลบวกหรือจำนวนพจน์ตามขั้น', t(10))
    u(AREA, 'right-triangle-two-heights', 'พื้นที่สามเหลี่ยมมุมฉากคิดได้สองแบบ ½·ขา·ขา = ½·ด้านตรงข้ามมุมฉาก·ส่วนสูง', t(11),
      k('right_triangle_area_p6', 'triangle_area'), note='3 ธ.ค. 66 ข้อ 11 ข้อมูลในรูปไม่สอดคล้องกัน')
    u(PARALLEL, 'parallel-angle-chase', 'ใช้มุมแย้ง มุมภายในบนข้างเดียวกัน มุมตรงข้าม และผลบวกมุมในสามเหลี่ยมไล่หามุม', t(12),
      k('parallel_angle_picture_p5', 'parallel_angles'))
    u(VOL, 'composite-solid-surface', 'แยกรูปทรงประกอบเป็นทรงสี่เหลี่ยมมุมฉาก หาพื้นที่ผิวหรือปริมาตรแต่ละส่วนแล้วรวม', t(13),
      k('box_surface_area_p6', 'composite_box_volume_p6'))
    u(BAR, 'chart-two-series', 'อ่านค่าจากแผนภูมิแท่งหรือเส้นสองชุด รวม หาผลต่าง และร้อยละตามที่ถาม', t(14, ) + [SAMSEN_A + '34', SAMSEN_B + '34'],
      k('bar_chart_read_p4', 'bar_chart_diff'))
    u(PIE, 'pie-angle-share', 'มุมที่จุดศูนย์กลาง ÷ 360° = ส่วนของทั้งหมด ใช้หาร้อยละ มุม และปริมาณ', t(15),
      k('pie_angle_from_percent_p6', 'pie_chart_amount_p6'))
    u(PCT, 'cost-profit-ratio', 'แบ่งราคาขายตามอัตราส่วนทุนต่อกำไร แล้วคิดกำไรรวมหรือร้อยละ', t(16),
      k('profit_loss_p6', 'ratio_share_p6'))
    u(PCT, 'markup-then-discount', 'ราคาป้าย ราคาขายหลังลด และทุน เชื่อมด้วยร้อยละกำไรหรือส่วนลด แล้วหาค่าที่ต้องการ', t(17),
      k('discount', 'cost_from_profit_p6'))
    u(PCT, 'percent-of-mixture-volume', 'คูณปริมาตรทั้งหมดด้วยร้อยละของส่วนผสมแล้วเปลี่ยนหน่วย', t(18),
      k('percent_of_quantity_p5'))
    u(EQ, 'chase-catch-up-time', 'ไล่ตามกันใช้เวลา = ระยะห่าง ÷ ผลต่างอัตราเร็ว แล้วบวกเวลาเริ่ม', t(19))
    u(TIME, 'decimal-hours', 'รวมเวลาที่เป็นทศนิยมของชั่วโมงแล้วเปลี่ยนเป็นชั่วโมงและนาที', t(20), k('time_units_p4'))
    u(PROB, 'outfit-count-condition', 'นับคู่เสื้อกับกระโปรงด้วยหลักการคูณแล้วตัดคู่ที่ผิดเงื่อนไข', t(21), k('outfits_m4'))
    u(RATE, 'volume-proportion-materials', 'ปริมาณวัสดุแปรผันตรงกับปริมาตร เทียบปริมาตรสองแบบด้วยบัญญัติไตรยางศ์', t(22),
      k('rate_word_problem_p5', 'rectangular_prism_volume'))
    u(AREA, 'wire-shapes-perimeter', 'ความยาวลวดเท่ากับผลรวมความยาวรอบรูปของรูปที่ดัด', t(23), k('rectangle_area_perimeter'))
    u(DEC, 'ceiling-division-units', 'เปลี่ยนหน่วยให้ตรงกันแล้วหาร ปัดขึ้นเมื่อต้องใช้อย่างน้อย', t(24),
      k('decimal_word_problem_p6'))
    u(VOL, 'tank-volume-fraction', 'ปริมาตรน้ำ = กว้าง × ยาว × ความสูงน้ำ ใช้เศษส่วนของถังหรือระดับน้ำหาปริมาณที่ใช้หรือความลึก', t(25),
      k('water_level_p6', 'volume_capacity_p5'))
    u(EQ, 'linear-distribution-equation', 'ให้จำนวนคนเป็นตัวแปร เขียนจำนวนของที่แจกสองแบบเท่ากันแล้วแก้สมการ', t(26),
      k('linear_word_problem_m1'))
    u(FRAC, 'fraction-of-remainder', 'เศษส่วนของส่วนที่เหลือ คูณเศษส่วนต่อกันเพื่อหาส่วนของทั้งหมด แล้วย้อนหาจำนวนเดิม', t(27),
      k('fraction_multistep_word_p6', 'part_of_part_p6'))
    u(PAT, 'grid-pattern-relation', 'หาความสัมพันธ์ที่เหมือนกันในทุกชุดตัวเลขแล้วใช้หาค่าที่หายไป', t(28))
    u(AREA, 'trapezoid-area-difference', 'แบ่งรูปสี่เหลี่ยมคางหมูมุมฉากเป็นสามเหลี่ยมสองรูปแล้วเทียบพื้นที่', t(29), k('trapezoid_area'))
    u(PCT, 'successive-percent-increase', 'ขายต่อหลายทอดคูณด้วย (1 + กำไร) ของแต่ละทอดต่อกัน', t(30),
      k('percent_change_p6'))
    u(EQ, 'age-fraction-relations', 'เขียนอายุแต่ละคนจากเศษส่วนของอายุคนอื่นในปัจจุบันและอนาคต แล้วหาปี พ.ศ.', t(31),
      k('age_problem_m1'))
    u(FRAC, 'distance-fraction-units', 'เปลี่ยนระยะทางที่เป็นจำนวนคละและหน่วยต่างกันให้หน่วยเดียว แล้วบวกลบตามเงื่อนไข', t(32),
      k('fraction_multistep_word_p6'))
    u(PCT, 'percent-categories', 'หาจำนวนแต่ละประเภทจากร้อยละของทั้งหมดหรือของส่วนที่เหลือ แล้วตรวจข้อความ', t(33),
      k('percent_of_quantity_p5', 'find_percent_p5'))


def samsen_2568():
    t = lambda *ns: [SAMSEN_C + str(n) for n in ns]
    u(GCD, 'divisor-condition-sum', 'นิพจน์เป็นจำนวนนับเมื่อ n หารค่าคงที่ลงตัวและเงื่อนไขอื่นเป็นจริง ไล่ตัวหารแล้วรวม', t(1),
      note='ข้อ 1 ผลบวกที่ได้ (506) ไม่อยู่ในตัวเลือก')
    u(FRAC, 'estimate-sum-bounds', 'ประมาณผลบวกของเศษส่วนหลายพจน์ด้วยขอบบนและขอบล่างเพื่อหาหลักที่ต้องการ', t(2))
    claim('gcd-lcm-statements', t(3))
    u(GCD, 'gcd-with-remainders', 'จำนวนที่หารแล้วเหลือเศษตามกำหนด: ลบเศษออกก่อนแล้วหา ห.ร.ม. หรือ ค.ร.น.', t(4),
      k('gcd_word_problem_p6', 'lcm_word'))
    u(STAT, 'mean-correction', 'ผลรวมเท่ากับค่าเฉลี่ยคูณจำนวน ปรับผลรวมตามข้อมูลที่แก้แล้วหาค่าเฉลี่ยใหม่', t(5),
      k('total_from_mean_m1', 'mean_new_value_m1'))
    claim('compare-fraction-expressions', t(6))
    u(FRAC, 'halving-sum', '1 − 1/2 − 1/4 − … − 1/2ⁿ = 1/2ⁿ ใช้หาจำนวนครั้งของการคูณ 1/2', t(7))
    u(RATE, 'fuel-rate', 'ระยะทางรวมหารด้วยอัตราสิ้นเปลืองได้ปริมาณน้ำมัน แล้วคูณราคา', t(8), k('fuel_for_trip_p5'))
    u(EQ, 'savings-schedule', 'รวมเงินออมตามแผนรายวันหรือรายสัปดาห์จนถึงเป้าหมาย', t(9))
    u(RATE, 'workers-length-days', 'งานแปรผันตรงกับจำนวนคนและจำนวนวัน ใช้อัตรางานต่อคนต่อวันหาเวลาใหม่', t(10), k('workers_days_p5'))
    u(RATIO, 'ratio-chain-parts', 'รวมอัตราส่วนหลายคู่ให้เป็นอัตราส่วนต่อเนื่อง แล้วแบ่งจำนวนทั้งหมดตามส่วน', t(11),
      k('share_three_ways_p6', 'ratio_share_p6'))
    claim('parallel-angle-chase', t(12))
    u(AREA, 'triangle-area-ratio', 'สามเหลี่ยมที่ส่วนสูงเท่ากันมีอัตราส่วนพื้นที่เท่ากับอัตราส่วนฐาน', t(13), k('two_triangles_one_base_p6'))
    u(PAT, 'tiling-recurrence-count', 'นับวิธีปูแถบยาว n ด้วยแผ่นยาว 1 และ 2 จากวิธีของ n − 1 และ n − 2', t(14))
    u(AREA, 'composite-squares-area', 'แบ่งรูปประกอบหรือรูปที่ซ้อนกันเป็นสี่เหลี่ยมและสามเหลี่ยม หาพื้นที่แต่ละส่วนแล้วรวมหรือหัก', t(15),
      k('composite_area_figure_p6', 'composite_area_p6'))
    u(SHAPES, 'count-squares-figure', 'นับรูปสี่เหลี่ยมจัตุรัสทุกขนาดในรูปอย่างเป็นระบบตามขนาด', t(16))
    u(STAT, 'pairwise-sum-mean', 'ผลบวกของทุกคู่หรือทุกกลุ่มย่อยนับข้อมูลแต่ละตัวเท่ากัน ใช้หาผลรวมและค่าเฉลี่ย', t(17),
      k('mean_from_data'))
    u(VOL, 'painted-cube-faces', 'ลูกบาศก์ n×n×n ทาสีด้านนอก นับลูกเล็กที่มีสีสามด้าน สองด้าน หนึ่งด้าน และไม่มีสี', t(18))
    u(PCT, 'profit-percent-count', 'หาทุนและกำไรต่อชิ้นจากร้อยละกำไร แล้วหาจำนวนชิ้นจากกำไรรวม', t(19), k('profit_loss_p6'))
    claim('fraction-of-remainder', t(20))
    u(PCT, 'compare-discounts', 'คิดราคาหลังส่วนลดแต่ละแบบ (ลดเป็นบาทหรือร้อยละ ลดซ้อน) แล้วเปรียบเทียบ', t(21),
      k('compare_offers_p6', 'discount'))
    u(GCD, 'lcm-meeting-time', 'เหตุการณ์ที่เกิดซ้ำทุกช่วงเวลาต่างกันจะเกิดพร้อมกันทุก ค.ร.น. ของช่วงเวลา', t(22),
      k('lcm_word', 'buses_together_p6'))
    u(RATE, 'rate-over-time', 'เปลี่ยนเวลาเป็นหน่วยเดียว หาอัตราต่อหน่วยเวลาแล้วหาปริมาณหรือเวลาที่ต้องการ', t(23),
      k('rate_word_problem_p5'))
    claim('chart-two-series', t(24))
    claim('percent-categories', t(25))
    u(OPS, 'distributive-pairing', 'จับคู่พจน์ที่มีตัวร่วมแล้วใช้สมบัติการแจกแจงลดการคำนวณ', t(26), k('order_of_ops'))
    u(GCD, 'pairwise-products', 'ผลคูณทุกคู่ของสี่จำนวน: คู่ตรงข้ามมีผลคูณเท่ากันเป็นผลคูณทั้งสี่ ใช้หาค่าที่หายไป', t(27))
    u(EQ, 'scoring-equation', 'ตั้งสมการจำนวนข้อที่ตอบถูก ตอบผิด และไม่ตอบ ตามเกณฑ์คะแนน', t(28), k('linear_word_problem_m1'))
    u(EQ, 'consecutive-sum-correction', 'ผลบวกจำนวนเรียงกันคำนวณด้วยสูตรเลขคณิต เทียบผลที่ผิดเพื่อหาจำนวนที่ถูกนับผิด', t(29))
    u(EQ, 'work-backwards-money', 'ย้อนการดำเนินการจากผลสุดท้ายทีละขั้น (บวกกลับเป็นลบ คูณกลับเป็นหาร)', t(30))
    u(FRAC, 'continued-fraction', 'จัดเศษส่วนต่อเนื่องจากชั้นในสุดออกมา แล้วเทียบส่วนจำนวนเต็มและเศษ', t(31))
    claim('grid-pattern-relation', t(32))
    claim('composite-squares-area', t(33))
    claim('pie-angle-share', t(34))


def roiet():
    t = lambda *ns: [ROIET + str(n) for n in ns]
    u(OPS, 'order-of-operations-nested', 'คำนวณจากวงเล็บในสุด คูณหารก่อนบวกลบ แล้วตรวจข้อความการคำนวณ', t(1),
      k('ooo_nested_p6', 'order_of_ops_integers'))
    claim('gcd-with-remainders', t(2, 18))
    claim('parallel-angle-chase', t(3, 15, 34))
    u(PCT, 'whole-from-percent', 'จำนวนทั้งหมด = ส่วนที่รู้ ÷ ร้อยละ × 100', t(4), k('whole_from_percent_p6'))
    u(CIRCLE, 'shaded-area-circles', 'พื้นที่แรเงา = พื้นที่รูปทั้งหมด − พื้นที่วงกลมหรือส่วนของวงกลม', t(5, 23, 25),
      k('circle_area_circumference'))
    claim('percent-categories', t(6))
    u(SHAPES, 'prism-net', 'รูปคลี่ของปริซึมมีหน้าฐานสองหน้าและหน้าข้างเป็นสี่เหลี่ยมตามจำนวนด้านฐาน', t(7), k('solid_nets_m1'),
      note='ข้อ 7 พิมพ์ "สามเหลี่ยมมุมฉาก" แทนสี่เหลี่ยมมุมฉาก')
    u(PAT, 'figure-pattern-count', 'นับจำนวนชิ้นในรูปที่ 1, 2, 3 หาผลต่างหรือกฎแล้วหาจำนวนในรูปที่ n', t(8, 36),
      k('pattern_nth_term_p6'))
    claim('work-backwards-money', t(9))
    u(EQ, 'legs-count-equation', 'ให้จำนวนสัตว์ชนิดหนึ่งเป็นตัวแปร เขียนจำนวนขารวมเป็นสมการ', t(10), k('linear_word_problem_m1'),
      note='ข้อ 10 ถามไก่และแมว ได้ 11 ซึ่งไม่อยู่ในตัวเลือก')
    claim('compare-discounts', t(11))
    claim('fraction-of-remainder', t(12))
    u(AREA, 'square-rectangle-area', 'หาด้านจากความยาวรอบรูปหรือพื้นที่ที่เท่ากัน แล้วหาพื้นที่หรือเส้นทแยงมุม', t(13, 28),
      k('rectangle_area_perimeter'))
    u(SHAPES, 'polygon-diagonals-angle-sum', 'n เหลี่ยมมีเส้นทแยงมุม n(n − 3)/2 เส้น และผลบวกมุมภายใน (n − 2) × 180°', t(14),
      k('polygon_diagonals_m5', 'polygon_angle_sum'))
    u(FRAC, 'fraction-inequality-statements', 'ตรวจข้อความอสมการของเศษส่วนเมื่อตัวส่วนหรือตัวเศษเปลี่ยน ด้วยตัวอย่างค้าน', t(16))
    claim('grid-pattern-relation', t(17))
    u(EXP, 'powers-evaluate', 'หาฐานจากเลขยกกำลังที่กำหนดแล้วคำนวณนิพจน์ตามลำดับการดำเนินการ', t(19),
      k('order_of_ops_powers'))
    u(FRAC, 'telescoping-product', 'ผลคูณ (1 − 1/k) ตัดกันเป็นทอด ๆ เหลือพจน์แรกกับพจน์สุดท้าย', t(20))
    u(EQ, 'small-integer-system', 'ใช้ผลบวกและผลต่างหาตัวแปร แล้วใช้เงื่อนไขการหารหาตัวที่เหลือ', t(21))
    claim('profit-percent-count', t(22))
    claim('compare-fraction-expressions', t(24))
    u(SHAPES, 'quadrilateral-properties', 'ตรวจนิยามและสมบัติของรูปสี่เหลี่ยมแต่ละชนิด', t(26), k('parallelogram_properties'))
    u(RATE, 'work-together-rate', 'อัตรางานรวม = ผลบวกอัตรางานแต่ละคน หาเวลาของคนที่ไม่รู้', t(27), k('work_together_m4'),
      note='ข้อ 27 คำตอบ 26.4 ชั่วโมงอยู่ระหว่างตัวเลือก')
    u(OPS, 'cyclic-digit-sum', 'ผลบวกของจำนวนที่เลื่อนเลขโดดวนกันมีเลขโดดแต่ละตัวในทุกหลัก จึงเท่ากับผลบวกเลขโดดคูณ 111…1', t(29))
    u(SHAPES, 'triangle-inequality', 'ด้านสามด้านเป็นรูปสามเหลี่ยมได้เมื่อผลบวกสองด้านใด ๆ มากกว่าด้านที่สาม', t(30))
    u(EQ, 'algebraic-price', 'เขียนราคาที่ไม่รู้ด้วยตัวแปรจากยอดเงินรวม', t(31), k('linear_word_problem_m1'))
    u(PCT, 'percent-after-adding', 'จำนวนส่วนที่ไม่เปลี่ยนคงที่ ใช้ร้อยละใหม่หาจำนวนทั้งหมดแล้วหาจำนวนที่เพิ่ม', t(32))
    claim('fraction-order-of-operations', t(33))
    claim('continued-fraction', t(35))
    u(CIRCLE, 'arc-perimeter', 'ความยาวรอบรูปที่มีส่วนโค้งของวงกลมหรือครึ่งวงกลม = ผลบวกส่วนโค้งและส่วนตรง', t(37),
      k('circumference_from_diameter_p6', 'semicircle_area_p6'))
    claim('markup-then-discount', t(38))
    u(CIRCLE, 'circle-scale-area', 'เส้นรอบวงหรือรัศมีเป็น k เท่า พื้นที่เป็น k² เท่า ใช้เทียบพื้นที่วงแหวน', t(39),
      k('circle_area_circumference'))
    u(STAT, 'mean-total-parts', 'ผลรวมทั้งหมดจากค่าเฉลี่ย ลบผลรวมของกลุ่มที่รู้ แล้วแบ่งส่วนที่เหลือตามเงื่อนไข', t(40),
      k('total_from_mean_m1', 'mean_missing_value_m1'))


def nud():
    t = lambda *ns: [NUD + str(n) for n in ns]
    claim('gcd-lcm-statements', t(1))
    u(GCD, 'divisibility-chain', 'ถ้า A | B | C | D แล้ว ห.ร.ม. คือ A และ ค.ร.น. คือ D', t(2), k('gcd', 'lcm'))
    claim('lcm-meeting-time', t(3))
    u(EQ, 'arithmetic-sum', 'ผลบวกจำนวนเรียงกัน = จำนวนพจน์ × (พจน์แรก + พจน์สุดท้าย) ÷ 2', t(4),
      k('arithmetic_series_word_m6'))
    u(FRAC, 'telescoping-fraction-sum', '1/(k(k + 1)) = 1/k − 1/(k + 1) บวกแล้วตัดกันเป็นทอด ๆ', t(5),
      k('finite_telescoping_fraction_m6'))
    claim('order-of-operations-nested', t(6))
    claim('powers-evaluate', t(7))
    u(EQ, 'solve-linear-equation', 'แก้สมการเชิงเส้นตัวแปรเดียว หรือแปลงข้อความเป็นสมการแล้วแก้', t(8, 9),
      k('linear_equation', 'linear_word_problem_m1'))
    u(PAT, 'fibonacci-like-sum', 'พจน์ถัดไปเป็นผลบวกของสองพจน์ก่อนหน้า หาพจน์แล้วรวม', t(10),
      note='ข้อ 10 ผลบวกที่ถูกต้อง (12) ไม่อยู่ในตัวเลือก')
    u(DEC, 'repeating-decimal-fraction', 'เขียนทศนิยมซ้ำเป็นเศษส่วนด้วยการลบผลคูณของ 10ⁿ', t(11),
      k('repeating_decimal_to_fraction_m1'))
    u(FRAC, 'defined-operation', 'แทนค่าในตัวดำเนินการที่นิยามใหม่แล้วคำนวณเศษส่วน', t(12))
    claim('whole-from-percent', t(13))
    claim('markup-then-discount', t(14))
    claim('percent-categories', t(15))
    claim('tank-volume-fraction', t(16, 19))
    u(CIRCLE, 'square-sector-shaded', 'พื้นที่แรเงาในสี่เหลี่ยมจัตุรัส = พื้นที่สามเหลี่ยมหรือสี่เหลี่ยม − พื้นที่เซกเตอร์', t(17),
      k('circle_area_circumference'))
    claim('shaded-area-circles', t(18), )
    UNITS['shaded-area-circles'].setdefault('note', 'NUD ข้อ 18 พื้นที่ที่ถูกต้อง (4.2) ไม่อยู่ในตัวเลือก')
    claim('wire-shapes-perimeter', t(20))
    claim('circle-scale-area', t(21))
    claim('arc-perimeter', t(22))
    claim('parallel-angle-chase', t(23, 24))
    u(RATIO, 'map-directions', 'อ่านทิศจากแผนผังเทียบกับจุดอ้างอิง (แปดทิศ)', t(25))
    u(RATIO, 'map-scale-ratio', 'มาตราส่วน = ระยะบนแผนผัง : ระยะจริง ในหน่วยเดียวกัน', t(26), k('map_scale', 'scale_to_map_p6'))
    u(PROB, 'event-certainty', 'จำแนกเหตุการณ์ที่เกิดขึ้นแน่นอน ไม่เกิดแน่นอน หรืออาจเกิด และเปรียบเทียบโอกาสจากจำนวน', t(27, 28),
      k('probability_bag_m3'))
    claim('chart-two-series', t(29, 30))


def main():
    samsen_2567()
    samsen_2568()
    roiet()
    nud()
    for (slug, topic, level), units in FILES.items():
        write_topic(ROOT / f'otk/knowledge/math/{slug}.json', topic, units, level)


if __name__ == '__main__':
    main()
