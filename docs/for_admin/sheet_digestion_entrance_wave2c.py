"""Knowledge claims for the maths entrance papers, wave 2c (re-runnable, idempotent).

Satri Siriket's เยาวชนคนเก่งคณิตศาสตร์ papers 2566 (ป.3-4, ป.5-6, ม.1, ม.2,
ม.3), the two Patumwan ม.1 entrance recollections (2568, 2569) and the MWIT
2566 rounds 1-2 recollection. Every question is claimed by its exam tag; a
skill claimed by an earlier wave gets these tags on the same unit (``extend``).
``covered_by`` names only sets that practise the skill.
"""
from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[2]
_wave2b = runpy.run_path(str(Path(__file__).with_name('sheet_digestion_entrance_wave2b.py')))
write_topic = _wave2b['write_topic']

P34 = 'สตรีสิริเกศ ป.3-4 2566/'
P56 = 'สตรีสิริเกศ ป.5-6 2566/'
M1 = 'สตรีสิริเกศ ม.1 2566/'
M2 = 'สตรีสิริเกศ ม.2 2566/'
M3 = 'สตรีสิริเกศ ม.3 2566/'
PW68 = 'เข้า ม.1 สาธิตปทุมวัน 2568/'
PW69 = 'เข้า ม.1 สาธิตปทุมวัน 2569/'
MWIT66 = 'เข้า ม.4 MWIT 2566 '

P4NUM = ('entrance-primary-whole-numbers', 'การบวกและการลบ', 'ป.4')
P4MIX = ('entrance-primary-word-problems', 'โจทย์ปัญหาระคน', 'ป.4')
P4TIME = ('entrance-primary-time', 'เวลา', 'ป.4')
P4ANGLE = ('entrance-primary-angles', 'เส้นตรงและมุม', 'ป.4')
P4DATA = ('entrance-primary-data', 'การนำเสนอข้อมูล', 'ป.4')
P6DEC = ('entrance-primary-decimals-p6', 'ทศนิยม', 'ป.6')
P6PCT = ('entrance-primary-percent', 'ร้อยละ', 'ป.6')
M1EXP = ('entrance-primary-exponents', 'เลขยกกำลัง', 'ม.1')
M1NUM = ('entrance-number-theory', 'จำนวนเต็ม', 'ม.1')
M1ALG = ('entrance-algebra', 'นิพจน์พีชคณิต', 'ม.1')
M1GRAPH = ('entrance-linear-graphs', 'กราฟความสัมพันธ์เชิงเส้น', 'ม.1')
M1SHAPE = ('entrance-primary-shapes', 'มิติสัมพันธ์ของรูปเรขาคณิต', 'ม.1')
M2POLY = ('entrance-polynomials-m2', 'เอกนามและพหุนาม', 'ม.2')
M2EXP = ('entrance-exponents-m2', 'เลขยกกำลัง', 'ม.2')
M2REAL = ('entrance-real-numbers', 'จำนวนจริง', 'ม.2')
M2TRANS = ('entrance-transformations', 'การแปลงทางเรขาคณิต', 'ม.2')
M2CONG = ('entrance-congruence', 'ความเท่ากันทุกประการ', 'ม.2')
M2PYTH = ('entrance-pythagoras', 'ทฤษฎีบทพีทาโกรัส', 'ม.2')
M2STAT = ('entrance-statistics-m2', 'สถิติ', 'ม.2')
M3FACT = ('entrance-factorising', 'แยกตัวประกอบ', 'ม.3')
M3QUAD = ('entrance-quadratics', 'สมการกำลังสอง', 'ม.3')
M3PARAB = ('entrance-parabolas', 'กราฟของฟังก์ชันกำลังสอง', 'ม.3')
M3INEQ = ('entrance-inequalities', 'อสมการเชิงเส้น', 'ม.3')
M3SIM = ('entrance-similarity', 'ความคล้าย', 'ม.3')
M3TRIG = ('entrance-trig-m3', 'อัตราส่วนตรีโกณมิติ', 'ม.3')
M3PROB = ('entrance-primary-probability', 'ความน่าจะเป็นเบื้องต้น', 'ม.3')
M3SOLID = ('entrance-solids', 'พื้นที่ผิวและปริมาตร', 'ม.3')
M3CIRCLE = ('entrance-circles', 'วงกลม', 'ม.3')

FILES, UNITS, EXTEND = {}, {}, {}


def u(file, slug, statement, tags, covered=(), note=''):
    unit = dict(id='math.entrance.' + slug, kind='procedure', title=statement[:60], statement=statement,
                steps=['ระบุสิ่งที่โจทย์กำหนดและสิ่งที่ต้องหา', statement, 'ตรวจคำตอบกับเงื่อนไขของโจทย์'],
                sources=[{'tag': t} for t in tags], covered_by=['math.' + k for k in covered])
    if note:
        unit['note'] = note
    FILES.setdefault(file, []).append(unit)
    UNITS[slug] = unit


def claim(slug, tags):
    UNITS[slug]['sources'] += [{'tag': t} for t in tags if {'tag': t} not in UNITS[slug]['sources']]


def extend(slug, tags):
    EXTEND.setdefault('math.entrance.' + slug, []).extend(tags)


def satri_p34():
    t = lambda *ns: [P34 + n for n in ns]
    u(P4NUM, 'place-value-digit-values', 'ค่าของเลขโดดขึ้นกับหลักที่อยู่ หาค่าของเลขโดดแต่ละตัวแล้วเปรียบเทียบหรือหาผลต่าง', t('1.1'),
      ('place_value_millions_p4',))
    u(P4NUM, 'large-add-sub', 'บวกลบจำนวนนับหลายหลัก หาตัวไม่ทราบค่า และตรวจประโยคสัญลักษณ์', t('1.2', '1.5', '1.6', '1.7'),
      ('add_sub_large_p4', 'missing_addsub_large_p4', 'check_addsub_p4'))
    u(P4NUM, 'compare-large-numbers', 'เปรียบเทียบและเรียงลำดับจำนวนนับหลายหลักทีละหลักจากซ้าย', t('1.4'), ('more_less_large_p4',))
    u(P4MIX, 'capacity-units-word', 'แปลงลิตรและมิลลิลิตรให้หน่วยเดียวกันแล้วคำนวณปริมาตรจากการตักซ้ำหลายครั้ง', t('1.3'))
    u(P4MIX, 'mixed-operations', 'คำนวณการบวก ลบ คูณ หารระคน โดยทำในวงเล็บ แล้วคูณหารก่อนบวกลบ', t('1.8'), ('mixed_ops_p4',))
    u(P4MIX, 'multi-step-money', 'โจทย์ปัญหาเงินหลายขั้นตอน: หาส่วนที่เหลือหรือผลรวมก่อน แล้วหารหรือคูณตามที่ถาม', t('1.9', '1.10', '1.11'),
      ('two_step_word_problem_p4',))
    u(P4TIME, 'reading-durations', 'หาช่วงเวลาจากเวลาเริ่มและเวลาสิ้นสุดแล้วเปรียบเทียบ', t('1.12'), ('longest_duration_p4',))
    extend('workers-length-days', t('1.13'))
    u(P4TIME, 'clock-elapsed-time', 'บวกช่วงเวลาเข้ากับเวลาเริ่ม หรือใช้ผลต่างเขตเวลา หาเวลาบนหน้าปัดนาฬิกา', t('1.14', '2.4'),
      ('travel_time_p4',))
    extend('compare-fraction-expressions', t('1.15'))
    extend('fraction-order-of-operations', t('1.16'))
    extend('fraction-of-remainder', t('1.17', '1.18', '2.6'))
    u(P6DEC, 'fraction-decimal-conversion', 'เขียนเศษส่วนเป็นทศนิยมและทศนิยมเป็นเศษส่วนแล้วตรวจข้อสรุป', t('1.19'),
      ('decimal_as_fraction_p4', 'fraction_to_decimal'))
    u(P6DEC, 'decimal-money-word', 'บวกลบคูณทศนิยมของจำนวนเงินแล้วเปรียบเทียบ', t('1.20', '1.21', '1.30'),
      ('decimal_addsub_p4', 'decimal_word_problem_p6'))
    u(P4ANGLE, 'angle-sum-straight-line', 'มุมบนเส้นตรงรวมกันได้ 180° และมุมรอบจุดรวมกันได้ 360° ใช้หาขนาดมุมที่ไม่รู้', t('1.22', '1.24', '1.25'), ('angles_around_point_p4', 'vertical_angles_algebra_m2',))
    extend('clock-hands', t('1.23'))
    extend('composite-squares-area', t('1.26', '1.27', '1.28'))
    extend('mean-total-parts', t('1.29'))
    u(P4DATA, 'pictograph-reading', 'อ่านแผนภูมิรูปภาพตามจำนวนที่รูปหนึ่งรูปแทน แล้วรวมหรือเปรียบเทียบ', t('1.31', '1.32'), ('pictograph_m1',))
    u(P4DATA, 'table-reading', 'อ่านค่าจากตารางแล้วเปรียบเทียบหรือรวมเพื่อตรวจข้อสรุป', t('1.33'), ('two_way_table_read_p5',))
    extend('defined-operation', t('1.34'))
    u(P4MIX, 'arithmetic-pattern-term', 'แบบรูปที่เพิ่มขึ้นครั้งละเท่ากัน พจน์ที่ n = พจน์แรก + (n − 1) × ผลต่าง', t('1.35'),
      ('pattern_nth_term_p6',))
    u(P4MIX, 'symbol-grid-equations', 'สัญลักษณ์ในตารางแทนจำนวน ใช้ผลรวมแถวและหลักตั้งสมการหาค่าของแต่ละสัญลักษณ์', t('2.1'))
    extend('small-integer-system', t('2.2'))
    u(P4MIX, 'weight-relations', 'แทนน้ำหนักของสิ่งหนึ่งด้วยอีกสิ่งจากความสัมพันธ์ที่ให้ แล้วหาน้ำหนักที่ถาม', t('2.3'))
    extend('ratio-chain-parts', t('2.5'))
    u(P4ANGLE, 'triangle-angle-sum', 'มุมภายในสามเหลี่ยมรวมกันได้ 180° ใช้กับสามเหลี่ยมด้านเท่าและหน้าจั่ว', t('2.7'),
      ('isosceles_triangle_angle_m2',))
    extend('age-fraction-relations', t('2.8'))
    extend('chart-two-series', t('2.9'))
    extend('figure-pattern-count', t('2.10'))


def satri_p56():
    t = lambda *ns: [P56 + n for n in ns]
    extend('telescoping-fraction-sum', t('1.1'))
    extend('fraction-order-of-operations', t('1.2', '2.1'))
    extend('fraction-of-remainder', t('1.3', '1.4'))
    u(P6DEC, 'decimal-place-value', 'ค่าของเลขโดดในแต่ละหลักของทศนิยม', t('1.5'), ('decimal_place_value',))
    u(P6PCT, 'best-buy-unit-price', 'หาราคาต่อหน่วยของแต่ละข้อเสนอแล้วเลือกที่ถูกที่สุด', t('1.6'), ('better_buy_p5',))
    u(P6DEC, 'decimal-expression', 'คำนวณนิพจน์ทศนิยมตามลำดับการดำเนินการ', t('1.7'), ('decimal_ops',))
    u(P6DEC, 'compare-decimal-times', 'เปรียบเทียบเวลาหรือปริมาณที่เป็นทศนิยมเพื่อจัดอันดับ', t('1.8'), ('decimal_compare_p4',))
    extend('lcm-meeting-time', t('1.9'))
    extend('defined-operation', t('1.10'))
    extend('profit-percent-count', t('1.11', '1.12'))
    u(P6PCT, 'alloy-percent', 'ร้อยละของส่วนผสมหลังหลอมรวม = ปริมาณโลหะรวม ÷ น้ำหนักรวม × 100', t('1.13'))
    u(P6DEC, 'decimal-change', 'หาผลต่างของปริมาณทศนิยมระหว่างช่วงแล้วบอกว่าเพิ่มหรือลดเท่าใด', t('1.14'), ('decimal_addsub_p4',))
    u(P6PCT, 'shaded-percent-grid', 'นับช่องที่แรเงาในตารางร้อยช่องแล้วเขียนเป็นร้อยละ', t('1.15'), ('percent_grid_p5',))
    extend('map-scale-ratio', t('1.16'))
    extend('figure-pattern-count', t('1.17', '1.18'))
    extend('composite-squares-area', t('1.19', '1.21', '1.22'))
    extend('quadrilateral-properties', t('1.20'))
    extend('box-surface-from-relations', t('1.23'))
    extend('shaded-area-circles', t('1.24', '1.25'))
    extend('parallel-angle-chase', t('1.26', '1.27', '1.29', '2.8'))
    extend('rate-over-time', t('1.28'))
    extend('prism-net', t('1.30'))
    extend('views-surface-area', t('1.31'))
    extend('composite-solid-surface', t('1.32'))
    extend('tank-volume-fraction', t('1.33', '2.5'))
    extend('chart-two-series', t('1.34'))
    extend('pie-angle-share', t('1.35'))
    extend('ratio-chain-parts', t('2.2'))
    extend('triangle-inequality', t('2.3'))
    u(M1SHAPE, 'count-triangles-figure', 'นับรูปสามเหลี่ยมทุกรูปในภาพอย่างเป็นระบบ โดยเลือกจุดยอดจากเส้นที่ตัดกัน', t('2.4'))
    extend('gcd-spacing', t('2.6'))
    u(M1SHAPE, 'stacked-balls-count', 'ลูกบอลซ้อนเป็นพีระมิด แต่ละชั้นเป็นจำนวนกำลังสองหรือสามเหลี่ยม รวมทุกชั้น', t('2.7'))
    extend('trapezoid-area-difference', t('2.9'))
    u(M3SOLID, 'recast-volume-count', 'ปริมาตรคงที่เมื่อหลอมใหม่ จำนวนชิ้นเล็ก = ปริมาตรทั้งหมด ÷ ปริมาตรชิ้นเล็ก', t('2.10'),
      ('rectangular_prism_volume',))


def satri_m1():
    t = lambda *ns: [M1 + n for n in ns]
    extend('divisibility-chain', t('1.1'))
    u(M1NUM, 'integer-expression', 'คำนวณนิพจน์ของจำนวนเต็มบวกลบตามลำดับการดำเนินการ แทนค่าตัวแปรที่กำหนด', t('1.2', '1.3', '1.7'),
      ('order_of_ops_integers', 'evaluate_expression'))
    extend('small-integer-system', t('1.4'))
    u(M1NUM, 'integer-statements', 'ตรวจข้อความเกี่ยวกับจำนวนเต็มและเลขยกกำลังด้วยตัวอย่างค้าน', t('1.5'))
    extend('digit-position-sequence', t('1.6'))
    u(M1NUM, 'decimal-expanded-form', 'เขียนทศนิยมในรูปกระจายตามค่าประจำหลักเพื่อหาเลขโดดแต่ละหลัก', t('1.8', '2.1'), ('decimal_place_value_m1',))
    extend('fraction-of-remainder', t('1.9', '1.25'))
    extend('fraction-order-of-operations', t('1.10', '1.24'))
    u(M1EXP, 'exponent-laws-statements', 'ใช้สมบัติเลขยกกำลังและนับหลักของผลลัพธ์ เปรียบเทียบหรือตรวจข้อความ', t('1.11', '1.12', '1.13', '1.14', '2.3'),
      ('product_rule', 'compare_powers_m1', 'powers_of_ten_m1'))
    extend('angle-sum-straight-line', t('1.15'))
    extend('quadrilateral-properties', t('1.16'))
    extend('defined-operation', t('1.17'))
    extend('composite-squares-area', t('1.18'))
    extend('views-surface-area', t('1.19', '1.20', '1.21', '2.10'))
    extend('wire-shapes-perimeter', t('1.22'))
    extend('scoring-equation', t('1.23'))
    u(M1GRAPH, 'line-through-point', 'แทนพิกัดของจุดที่เส้นตรงผ่านลงในสมการเพื่อหาค่าคงที่ และหาระยะหรือพื้นที่บนระนาบพิกัด', t('1.26', '1.27', '1.28'),
      ('point_on_line_m1',))
    extend('markup-then-discount', t('1.29'))
    extend('ratio-chain-parts', t('1.30', '1.31'))
    extend('pie-angle-share', t('1.32', '1.35'))
    u(P6PCT, 'percent-change-count', 'หาจำนวนเดิมหรือจำนวนใหม่จากร้อยละการเพิ่มหรือลด', t('1.33'), ('percent_change_p6',))
    extend('chart-two-series', t('1.34'))
    extend('count-multiples-either', t('2.2'))
    u(M1NUM, 'stair-game-moves', 'ตั้งสมการจำนวนครั้งที่ชนะ แพ้ และเสมอจากตำแหน่งสุดท้ายบนบันได', t('2.4'))
    u(M1NUM, 'rational-conditions', 'ใช้นิยามจำนวนตรรกยะและเงื่อนไขที่กำหนดหาค่าที่ทำให้นิพจน์เป็นจำนวนเต็ม', t('2.5'))
    u(M1ALG, 'ratio-power-relations', 'เทียบอัตราส่วนที่เป็นกำลังของตัวแปรเพื่อหาความสัมพันธ์ แล้วแทนในนิพจน์', t('2.6'))
    extend('number-triple-conditions', t('2.7'))
    extend('circle-scale-area', t('2.8'))
    extend('linear-cost-model', t('2.9'))


def satri_m2():
    t = lambda *ns: [M2 + n for n in ns]
    u(M2PYTH, 'pythagoras-figures', 'ใช้ทฤษฎีบทพีทาโกรัสในรูปประกอบเพื่อหาความยาวหรือพื้นที่', t('1.1', '1.2', '1.3', '1.4'),
      ('pythagoras_figure_m2', 'pythagoras'))
    u(M2REAL, 'roots-arithmetic', 'คำนวณรากที่สองและรากที่สาม ใช้ผลต่างกำลังสองกับกรณฑ์', t('1.5', '1.8'),
      ('nth_root', 'roots_of_perfect_powers_m2'))
    extend('absolute-value-statements', t('1.6'))
    extend('defined-operation', t('1.7'))
    extend('box-surface-from-relations', t('1.9'))
    extend('hollow-cylinder', t('1.10'))
    extend('composite-squares-area', t('1.11', '1.14'))
    u(M2TRANS, 'transformations-coordinates', 'หาพิกัดภาพจากการเลื่อนขนาน สะท้อน และหมุน แล้วหาพื้นที่หรือจุดที่ต้องการ', t('1.12', '1.13', '2.4'),
      ('translate_point', 'reflect_point', 'rotate_origin_m2'), note='ข้อ 1.12 ข้อมูลขัดกัน จึงไม่มีคำตอบ')
    u(M2EXP, 'exponent-laws-m2', 'ใช้สมบัติเลขยกกำลังรวมเลขชี้กำลังลบ สัญกรณ์วิทยาศาสตร์ และเปรียบเทียบเลขยกกำลัง', t('1.15', '1.16', '1.17', '2.5', '2.6'),
      ('negative_exponent', 'power_of_product', 'hard_product_with_negative'), note='ข้อ 2.5 ได้ n ไม่เป็นจำนวนเต็ม จึงไม่มีคำตอบ')
    u(M2POLY, 'polynomial-operations', 'บวก ลบ คูณ และหารพหุนาม โดยรวมพจน์ที่คล้ายกัน', t('1.18', '1.19', '1.20'),
      ('polynomial_addsub', 'combine_like_terms'))
    u(M2STAT, 'mean-median-mode-conditions', 'ใช้ค่าเฉลี่ย มัธยฐาน และฐานนิยมหาข้อมูลที่ไม่รู้ หรือปรับค่าเฉลี่ยเมื่อแก้ข้อมูล', t('1.21', '1.22', '1.23', '1.24', '2.8'),
      ('mean_median_mode_m2',))
    u(M2CONG, 'congruence-reasoning', 'ใช้เงื่อนไขความเท่ากันทุกประการ (ด.ม.ด., ม.ด.ม., ด.ด.ด.) และสมบัติสามเหลี่ยมหน้าจั่วพิสูจน์และหามุม', t('1.25', '1.26', '1.27', '1.28'),
      ('congruence_case', 'congruence_proof_reason_m2'))
    extend('parallel-angle-chase', t('1.29', '1.30', '1.31', '2.9'))
    u(M3FACT, 'factor-quadratic-conditions', 'แยกตัวประกอบพหุนามดีกรีสองและใช้คู่ตัวประกอบของค่าคงที่หาสัมประสิทธิ์', t('1.32', '1.33', '1.34'),
      ('factor_trinomial_m2', 'factor_quadratic'))
    extend('row-pattern-position', t('1.35'))
    u(M3CIRCLE, 'incircle-right-triangle', 'วงกลมแนบในสามเหลี่ยมมุมฉาก: r = (a + b − c)/2 และเส้นสัมผัสจากจุดเดียวกันยาวเท่ากัน', t('2.1'))
    u(M2REAL, 'radical-exponent-equation', 'เขียนทั้งสองข้างเป็นเลขยกกำลังฐานเดียวกันแล้วเทียบเลขชี้กำลัง ตรวจโดเมนของราก', t('2.2'))
    extend('tank-volume-fraction', t('2.3'))
    extend('symmetric-sum-product', t('2.7'))
    extend('rational-substitution', t('2.10'))


def satri_m3():
    t = lambda *ns: [M3 + n for n in ns]
    u(M3INEQ, 'inequality-bounds', 'แก้อสมการเชิงเส้นหรือแปลงขอบเขตของ x เป็นขอบเขตของนิพจน์ แล้วหาจำนวนเต็มที่ต้องการ', t('1.1', '1.2', '2.1'),
      ('inequality', 'inequality_largest_integer_m3'))
    u(M3FACT, 'factor-theorem-conditions', 'ใช้ตัวประกอบและผลต่างกำลังสองหาสัมประสิทธิ์หรือรูปแยกตัวประกอบ', t('1.3', '1.4', '1.5', '1.6'),
      ('factor_difference_of_squares_m3', 'polynomial_unknown_coefficients_m4'))
    u(M3QUAD, 'quadratic-substitution-equation', 'แทนนิพจน์ที่ซ้ำด้วยตัวแปรใหม่ แก้สมการกำลังสอง แล้วตรวจคำตอบ', t('1.7', '1.19'),
      ('quadratic_equation', 'quadratic_formula_roots'))
    extend('square-rectangle-area', t('1.8'))
    extend('age-fraction-relations', t('1.9'))
    extend('work-rate-people', t('1.10'))
    u(M3SIM, 'similar-triangles-ratio', 'ใช้สามเหลี่ยมคล้ายหาความยาวและอัตราส่วนพื้นที่', t('1.11', '1.12', '1.23'), ('similar_triangle_picture_m3', 'similar_ratio_area'))
    u(M3PARAB, 'parabola-parameters', 'ใช้จุดยอด แกนสมมาตร จุดที่ผ่าน และดิสคริมิแนนต์หาพารามิเตอร์ของพาราโบลา', t('1.13', '1.14', '1.15', '2.4'),
      ('parabola_vertex', 'parabola_x_intercepts_m3'))
    extend('mean-median-mode-conditions', t('1.16'))
    extend('weighted-average', t('1.17'))
    u(M2STAT, 'box-plot-compare', 'อ่านพิสัย ควอร์ไทล์ และมัธยฐานจากแผนภาพกล่องเพื่อเปรียบเทียบข้อมูลสองชุด', t('1.18'), ('box_plot_range_m3', 'box_plot_parts_m3'))
    u(M3PROB, 'counting-arrangements', 'นับวิธีจัดหรือเลือกด้วยหลักการคูณแล้วหาความน่าจะเป็นหรือจำนวนที่ต้องการ', t('1.20', '1.21', '1.29', '1.30', '2.9'),
      ('probability_bag_m3', 'probability_two_events_m3'))
    extend('british-flag-theorem', t('1.22'))
    extend('chord-angle-chase', t('1.24'))
    extend('prism-pyramid-volume', t('1.25', '1.26', '1.27'))
    extend('recast-volume-count', t('1.28'))
    u(M3PROB, 'pentagon-probability', 'นับผลลัพธ์ที่เท่ากันอย่างแท้จริงก่อนคิดความน่าจะเป็น', t('1.31'),
      note='ข้อ 1.31 คำตอบที่ถูกต้อง (7/64) ไม่อยู่ในตัวเลือก')
    u(M3TRIG, 'trig-ratio-expressions', 'หาอัตราส่วนตรีโกณมิติจากสามเหลี่ยมมุมฉากและใช้ sin² + cos² = 1 จัดรูปนิพจน์', t('1.32', '1.33', '2.10'),
      ('trig_ratio_from_triple', 'cos_from_sin_m3'))
    extend('two-observer-elevation', t('1.34', '1.35'))
    extend('telescoping-product', t('2.2'))
    extend('reciprocal-power-identity', t('2.3'))
    extend('tangential-isosceles-trapezoid', t('2.5'))
    extend('mean-correction', t('2.6'))
    extend('ratio-after-removal', t('2.7'))
    extend('semicircle-tangent-circle', t('2.8'))


def patumwan():
    t = lambda *ns: [PW68 + str(n) for n in ns]
    extend('legs-count-equation', t(1))
    extend('parallel-angle-chase', t(2, 10, 12))
    u(M1NUM, 'cryptarithm-digits', 'แทนเลขโดดด้วยตัวอักษรในการบวกหรือคูณ แล้วใช้หลักหน่วยและการทดหาเลขโดดแต่ละตัว', t(3) + [PW69 + '6'], ('missing_digit_add_p4',))
    extend('defined-operation', t(4))
    extend('periodic-schedule-total', t(5, 21))
    extend('gcd-lcm-statements', t(6))
    extend('distinct-prime-factors', t(7))
    extend('weighted-average', t(8))
    u(M1SHAPE, 'paper-folding', 'พับกระดาษซ้ำแล้วคลี่ ติดตามรอยพับและส่วนที่ซ้อนกันทีละขั้น', t(9))
    extend('isosceles-trapezoid-area', t(11))
    extend('figure-pattern-count', t(13))
    extend('percent-after-adding', t(14))
    extend('two-price-system-discount', t(15))
    extend('work-backwards-money', t(16))
    u(M1NUM, 'distinct-digit-numbers', 'สร้างจำนวนจากบัตรตัวเลขที่ไม่ซ้ำกัน นับจำนวนที่สอดคล้องเงื่อนไขการหารลงตัว', t(17))
    u(M1NUM, 'magic-square', 'ผลรวมทุกแถว หลัก และแนวทแยงเท่ากัน ใช้ผลรวมที่รู้หาช่องที่หายไป', t(18))
    extend('coin-count-system', t(19))
    extend('scoring-equation', t(20))
    t = lambda *ns: [PW69 + str(n) for n in ns]
    extend('ratio-power-relations', t(1))
    extend('congruence-arithmetic', t(2))
    extend('meeting-speed-system', t(3))
    u(P4TIME, 'mirrored-clock-time', 'อ่านเวลาบนนาฬิกาดิจิทัลที่กลับด้าน แล้วหาช่วงเวลาที่ผ่านไป', t(4))
    u(M1NUM, 'missing-bag-total', 'ใช้ผลรวมและเงื่อนไขอัตราส่วนหรือการหารลงตัวหาว่าถุงใดหายไป', t(5))
    extend('triangle-area-ratio', t(7))
    extend('circle-scale-area', t(8))
    extend('digit-position-sequence', t(9))
    extend('clock-hands', t(10))
    extend('mean-total-parts', t(11))
    extend('work-backwards-money', t(12))
    extend('digit-triple-count', t(13))
    u(M1SHAPE, 'map-colouring', 'ระบายสีบริเวณให้บริเวณที่ติดกันต่างสี หาจำนวนสีหรือจำนวนบริเวณตามเงื่อนไข', t(14))


def mwit66():
    r1 = lambda *ns: [MWIT66 + 'รอบ 1/' + str(n) for n in ns]
    r2 = lambda *ns: [MWIT66 + 'รอบ 2/' + n for n in ns]
    extend('gcd-lcm-statements', r1(1))
    extend('sums-of-all-but-one', r1(2))
    extend('data-conditions-statistics', r1(3))
    u(M1NUM, 'factor-product-extremes', 'แยกตัวประกอบเฉพาะของผลคูณแล้วแบ่งเป็นจำนวนที่แตกต่างกัน เพื่อหาผลบวกหรือค่าที่มากหรือน้อยที่สุด', r1(4),
      ('prime_factorization',))
    extend('defined-operation', r1(5, 9))
    extend('telescoping-product', r1(6))
    u(M1SHAPE, 'max-intersections', 'เส้นตรง n เส้นตัดกันได้มากที่สุด n(n − 1)/2 จุด เมื่อไม่มีสองเส้นขนานและไม่มีสามเส้นผ่านจุดเดียว', r1(7))
    extend('cryptarithm-digits', r1(8))
    extend('profit-percent-count', r1(10))
    extend('roots-arithmetic', r1(11))
    extend('inscribed-trapezoid-area', r1(12))
    extend('ratio-chain-parts', r1(13))
    extend('integer-fraction-pairs', r1(14))
    extend('composite-squares-area', r1(15, 20))
    extend('triangle-angle-sum', r1(16))
    extend('transformations-coordinates', r1(17))
    extend('round-robin-points', r1(18, 19))
    u(M1SHAPE, 'route-count-bridges', 'นับเส้นทางที่เดินผ่านสะพานโดยแยกกรณีตามลำดับบ้านหรือสะพานที่ใช้ แล้วคูณจำนวนทางในแต่ละช่วง', r1(21))
    extend('paper-folding', r1(22))
    extend('chart-two-series', r1(23))
    extend('equilateral-triangle-area', r1(24))
    extend('circle-scale-area', r1(25, 26))
    extend('number-base-codes', r1(28, 29))
    u(M1SHAPE, 'solid-net-folding', 'พับรูปคลี่เป็นทรงสามมิติ ติดตามว่าหน้าใดอยู่ตรงข้ามหรือติดกัน', r2('1.1.1', '1.1.2', '1.1.3', '1.1.4'),
      ('net_picture_m1', 'solid_nets_m1'))
    u(M1ALG, 'arrangement-formula', 'จัดวัตถุเป็นแถวและคอลัมน์ในพื้นที่จำกัด เขียนจำนวนเป็นสูตรของขนาดและระยะห่าง', r2('3.1.1', '3.1.2', '3.1.3'))


def main():
    mwit66()
    satri_p34()
    satri_p56()
    satri_m1()
    satri_m2()
    satri_m3()
    patumwan()
    for (slug, topic, level), units in FILES.items():
        write_topic(ROOT / f'otk/knowledge/math/{slug}.json', topic, units, level)
    _wave2b['EXTEND'].clear()
    _wave2b['EXTEND'].update(EXTEND)
    _wave2b['apply_extend']()


if __name__ == '__main__':
    main()
